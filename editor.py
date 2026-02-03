import os
import json
import itertools
import re
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, CompositeAudioClip, vfx
from moviepy.config import change_settings
from rich.console import Console

console = Console()

# ==============================================================================
# 🔧 RUTAS
# ==============================================================================
possible_paths = [
    r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe",
    r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
]
path_found = False
for path in possible_paths:
    if os.path.exists(path):
        change_settings({"IMAGEMAGICK_BINARY": path})
        path_found = True
        break

AUDIO_PATH = "audio_final.mp3"
VIDEO_FOLDER = "videos_stock"
MUSIC_FOLDER = "musica"
OVERLAY_PATH = "overlay.mp4" # VHS (Opcional)
DATA_FILE = "datos_video.json"
OUTPUT_FILE = "reel_definitivo.mp4"

# ==============================================================================
# 🎨 CONFIGURACIÓN SHORTS (VERTICAL)
# ==============================================================================
KEYWORDS_HIGHLIGHT = [
    "MUERTE", "PELIGRO", "MIEDO", "TERROR", "SANGRE", 
    "CORRE", "MATAR", "ALIEN", "FANTASMA", "OSCURO", 
    "PESADILLA", "GRITAR", "DIABLO", "DEMONIO", "NUNCA", "NADIE"
]

FACTOR_SYNC = 1.08
FONT = 'Arial-Bold'
COLOR_TITULO = 'red'
BORDE_TITULO = 'white'
FONT_SIZE_SUB = 65
MARCA_TEXTO = "@ElVeloOculto"

COLOR_SUB = 'white'
COLOR_FONDO_SUB = 'black'
OPACIDAD_FONDO = 0.6
COLOR_SUB_HIGH = 'yellow'
COLOR_FONDO_HIGH = 'black'

def zoom_inquietante(clip):
    return clip.resize(lambda t: 1 + 0.04 * t)

def procesar_clip_visual(clip):
    # LÓGICA VERTICAL (9:16)
    # 1. Ajustar altura a 1920
    if clip.h != 1920:
        ratio = 1920 / clip.h
        clip = clip.resize(ratio)
    
    # 2. Recortar centro para ancho 1080
    if clip.w > 1080:
        clip = clip.crop(x1=clip.w/2 - 540, width=1080, height=1920)
    elif clip.w < 1080:
        # Si es muy angosto (raro), estiramos
        clip = clip.resize(width=1080)
        clip = clip.crop(y1=clip.h/2 - 960, height=1920)
    
    clip = clip.fx(vfx.colorx, 0.6)
    clip = zoom_inquietante(clip)
    return clip

def generar_titulo_gancho(titulo):
    palabras = titulo.upper().split()
    texto_corto = " ".join(palabras[:4]) + "..." if len(palabras) > 5 else titulo.upper()
    return (TextClip(texto_corto, fontsize=110, color=COLOR_TITULO, 
                     font=FONT, stroke_color=BORDE_TITULO, stroke_width=3,
                     method='caption', size=(950, None))
            .set_position('center').set_start(0).set_duration(2.5).crossfadeout(0.5))

def generar_marca_agua(duracion):
    return (TextClip(MARCA_TEXTO, fontsize=35, color='white', font=FONT)
            .set_position(('center', 200)).set_opacity(0.5).set_duration(duracion))

def preparar_overlay_vhs(duracion_total):
    if not os.path.exists(OVERLAY_PATH): return None
    clip_overlay = VideoFileClip(OVERLAY_PATH).without_audio()
    # Ajuste vertical del overlay
    if clip_overlay.h != 1920:
        clip_overlay = clip_overlay.resize(height=1920)
        if clip_overlay.w < 1080: clip_overlay = clip_overlay.resize(width=1080)
    clip_overlay = clip_overlay.crop(x1=clip_overlay.w/2 - 540, width=1080, height=1920)
    clip_overlay = vfx.loop(clip_overlay, duration=duracion_total)
    return clip_overlay.set_opacity(0.15)

def limpiar_palabra(palabra):
    return re.sub(r'[^\w\s]', '', palabra).upper()

def generar_subtitulos(texto, duracion_total):
    palabras = texto.split()
    bloques = []
    palabras_por_bloque = 3 
    for i in range(0, len(palabras), palabras_por_bloque):
        bloque = " ".join(palabras[i:i + palabras_por_bloque])
        bloques.append(bloque.upper())
    
    duracion_ajustada = duracion_total * FACTOR_SYNC
    tiempo_por_bloque = duracion_ajustada / len(bloques)
    text_clips = []
    
    for i, texto_bloque in enumerate(bloques):
        start_time = i * tiempo_por_bloque
        palabras_en_bloque = texto_bloque.split()
        es_highlight = False
        for p in palabras_en_bloque:
            if limpiar_palabra(p) in KEYWORDS_HIGHLIGHT:
                es_highlight = True
                break
        
        color_txt = COLOR_SUB_HIGH if es_highlight else COLOR_SUB
        color_bg = COLOR_FONDO_HIGH if es_highlight else COLOR_FONDO_SUB
        
        txt_clip = (TextClip(texto_bloque, fontsize=FONT_SIZE_SUB, color=color_txt, 
                             font=FONT, method='caption', size=(900, None), 
                             bg_color=color_bg).set_opacity(OPACIDAD_FONDO)
                    .set_position(('center', 1400)).set_start(start_time).set_duration(tiempo_por_bloque))
        text_clips.append(txt_clip)
    return text_clips

def obtener_musica_fondo(duracion_video):
    if not os.path.exists(MUSIC_FOLDER): return None
    import random
    canciones = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith(".mp3")]
    if not canciones: return None
    musica = AudioFileClip(os.path.join(MUSIC_FOLDER, random.choice(canciones)))
    if musica.duration < duracion_video: musica = vfx.loop(musica, duration=duracion_video)
    return musica.subclip(0, duracion_video).volumex(0.15)

def editor_pro():
    console.rule("[bold magenta]⚡ EDITOR SHORTS: MODO CPU (CALIDAD SEGURA)[/bold magenta]")

    if not os.path.exists(AUDIO_PATH): return
    voz = AudioFileClip(AUDIO_PATH)
    duracion_meta = voz.duration

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        titulo_video = data.get("titulo_video", "MISTERIO")
        texto_guion = data.get("texto_para_narrar", "")

    # Montaje Visual Vertical
    archivos = [f for f in os.listdir(VIDEO_FOLDER) if f.endswith(".mp4")]
    archivos.sort(key=lambda f: int(f.split('_')[1].split('.')[0]) if '_' in f else 0)
    videos_ordenados = [os.path.join(VIDEO_FOLDER, f) for f in archivos]
    ciclo_videos = itertools.cycle(videos_ordenados)
    
    clips_video = []
    tiempo_actual = 0.0
    
    console.print(f"[yellow]🎞️ Montando Short Vertical...[/yellow]")
    while tiempo_actual < duracion_meta:
        ruta = next(ciclo_videos)
        try:
            clip = VideoFileClip(ruta).without_audio()
            clip = procesar_clip_visual(clip)
            restante = duracion_meta - tiempo_actual
            clip = clip.subclip(0, min(3.5, restante))
            if tiempo_actual > 0: clip = clip.fx(vfx.fadein, 0.3)
            clips_video.append(clip)
            tiempo_actual += clip.duration
        except: continue

    fondo_video = concatenate_videoclips(clips_video, method="compose").set_duration(duracion_meta)
    musica = obtener_musica_fondo(duracion_meta)
    audio_final = CompositeAudioClip([voz, musica]) if musica else voz

    # Capas
    capas = [fondo_video]
    overlay = preparar_overlay_vhs(duracion_meta)
    if overlay: capas.append(overlay)

    if path_found:
        capas.append(generar_marca_agua(duracion_meta))
        capas.append(generar_titulo_gancho(titulo_video))
        if texto_guion: capas.extend(generar_subtitulos(texto_guion, duracion_meta))

    console.print("[bold green]🚀 RENDERIZANDO CON CPU (SIN FILTRO VERDE)...[/bold green]")
    
    # RENDERIZADO CPU (FIX PARA EL VERDE)
    video_final = CompositeVideoClip(capas).set_audio(audio_final)
    video_final.write_videofile(
        OUTPUT_FILE, 
        fps=30, 
        codec="libx264",        # <--- CAMBIO: Usamos CPU en lugar de GPU
        audio_codec="libmp3lame", 
        threads=4,              # Hilos seguros
        preset="medium",        # Calidad equilibrada
        ffmpeg_params=["-pix_fmt", "yuv420p"], # <--- ESTO ELIMINA EL VERDE
        logger=None
    )
    console.print(f"✅ ¡Short Listo! [bold]{OUTPUT_FILE}[/bold]")

if __name__ == "__main__":
    editor_pro()
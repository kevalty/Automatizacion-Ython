import os
import json
import requests
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()

# TU API KEY DE PIXABAY
PIXABAY_KEY = os.getenv("PIXABAY_API_KEY")

def buscar_videos_stock():
    console.rule("[bold green]👁️ OJOS V5: MOTOR PIXABAY ACTIVADO[/bold green]")

    # 1. Verificaciones de Seguridad
    if not PIXABAY_KEY:
        console.print("[bold red]❌ ERROR: No encontré 'PIXABAY_API_KEY' en el archivo .env[/bold red]")
        console.print("Por favor ve a Pixabay, copia tu key y pégala en .env")
        return

    if not os.path.exists("datos_video.json"):
        console.print("[red]❌ No hay guion (datos_video.json). Ejecuta cerebro.py primero.[/red]")
        return

    # 2. Leer Palabras Clave
    with open("datos_video.json", "r", encoding="utf-8") as f:
        keywords = json.load(f).get("busqueda_visual_keywords", [])

    if not keywords:
        console.print("[red]❌ La lista de palabras clave está vacía.[/red]")
        return

    # 3. Preparar Carpeta
    if not os.path.exists("videos_stock"):
        os.makedirs("videos_stock")
    
    # Limpieza total para no mezclar historias
    console.print("[yellow]🧹 Limpiando videos anteriores...[/yellow]")
    for f in os.listdir("videos_stock"):
        os.remove(os.path.join("videos_stock", f))

    # 4. Bucle de Descarga
    # Descargamos 4 clips por cada palabra clave para tener material de sobra
    CLIPS_POR_KEYWORD = 4
    clip_global_counter = 0

    for keyword in keywords:
        console.print(f"🔎 Buscando en Pixabay: [cyan]'{keyword}'[/cyan]")
        
        # URL de la API de Pixabay
        # q = búsqueda | video_type = film (realista) | per_page = cuantos resultados pedir
        url = f"https://pixabay.com/api/videos/?key={PIXABAY_KEY}&q={keyword}&video_type=film&per_page={CLIPS_POR_KEYWORD + 2}"
        
        try:
            response = requests.get(url)
            data = response.json()
            hits = data.get('hits', [])
            
            if not hits:
                console.print(f"   ⚠️ No encontré videos para: '{keyword}' (Intentando siguiente...)")
                continue

            # Tomamos los primeros X videos encontrados
            seleccionados = hits[:CLIPS_POR_KEYWORD]
            
            for video in seleccionados:
                # Lógica para elegir la mejor calidad (Medium o Large, evitando 4k pesado o tiny)
                videos_disponibles = video.get('videos', {})
                link_descarga = None

                # Preferencia: Large (1080p) > Medium (720p) > Small
                if 'large' in videos_disponibles and videos_disponibles['large']['width'] <= 1920:
                    link_descarga = videos_disponibles['large']['url']
                elif 'medium' in videos_disponibles:
                    link_descarga = videos_disponibles['medium']['url']
                elif 'small' in videos_disponibles:
                    link_descarga = videos_disponibles['small']['url']
                
                if not link_descarga:
                    continue

                # Nombre del archivo secuencial (clip_0, clip_1...)
                # Esto es CRUCIAL para que el editor mantenga el orden de la historia
                nombre_archivo = f"videos_stock/clip_{clip_global_counter}.mp4"
                
                # Descargar el video
                with requests.get(link_descarga, stream=True) as r:
                    r.raise_for_status()
                    with open(nombre_archivo, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                
                console.print(f"   ⬇️ Guardado: clip_{clip_global_counter}.mp4")
                clip_global_counter += 1

        except Exception as e:
            console.print(f"[red]❌ Error descargando '{keyword}': {e}[/red]")

    if clip_global_counter > 0:
        console.print(f"[bold green]✅ ¡LISTO! {clip_global_counter} videos descargados de Pixabay.[/bold green]")
    else:
        console.print("[bold red]⚠️ No se descargó ningún video. Revisa tu API KEY o tus palabras clave.[/bold red]")

if __name__ == "__main__":
    buscar_videos_stock()
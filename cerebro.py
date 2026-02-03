import json
import asyncio
import edge_tts
import os
from rich.console import Console
from rich.panel import Panel

console = Console()

TITULO_DEL_VIDEO = "El Universo podría eliminarse HOY"

# CRONOLOGÍA VISUAL: Burbuja espacial -> Explosión luz -> Átomos rompiéndose -> Oscuridad total
BUSQUEDA_VISUAL = [
    "space bubble expanding universe",
    "supernova explosion bright light",
    "atoms breaking physics",
    "total black screen darkness"
]

GUION_TEXTO = """
¿Y si el universo tiene un botón de autodestrucción?
La física cuántica dice que sí. Se llama "La Decadencia del Falso Vacío".
Básicamente, el universo es como una bola en equilibrio sobre una cuerda floja. Es estable, pero precario.
Si algo empuja esa bola, el universo podría colapsar a un estado de "Vacío Verdadero".
Esto crearía una burbuja de destrucción que se expande a la velocidad de la luz.
No la veríamos venir.
Simplemente, en un nanosegundo, la Tierra, tú y las leyes de la física dejarían de existir.
Podría pasar dentro de mil millones de años... o justo ahora.
¿Sigues ahí?
Suscríbete a El Velo Oculto si sobreviviste.
"""

async def generar_audio_manual():
    console.rule(f"[bold purple]👁️ EL VELO OCULTO: Creando '{TITULO_DEL_VIDEO}'[/bold purple]")
    
    texto_final = GUION_TEXTO.strip()
    palabras = len(texto_final.split())
    
    # Estimación
    console.print(Panel(f"📝 Palabras: {palabras}\n⏱️ Duración estimada: ~48 segundos", title="Análisis de Guion"))

    if palabras > 145:
        console.print("[bold red]⚠️ CUIDADO: Tienes muchas palabras. Podría pasar de 60s.[/bold red]")

    # Generar Audio
    console.print("[blue]🗣️ Invocando la voz del narrador...[/blue]")
    archivo_salida = "audio_final.mp3"
    
    # RATE +5%: Un poco más rápido para dar sensación de misterio y urgencia
    # PITCH -2Hz: Un poco más grave para que suene más "oscuro"
    comunicate = edge_tts.Communicate(texto_final, "es-CO-GonzaloNeural", rate="+5%", pitch="-2Hz")
    
    await comunicate.save(archivo_salida)
    
    console.print(f"[green]✅ Audio del Velo Oculto listo: {archivo_salida}[/green]")

    # Guardar datos
    datos = {
        "titulo_video": TITULO_DEL_VIDEO,
        "texto_para_narrar": texto_final,
        "busqueda_visual_keywords": BUSQUEDA_VISUAL
    }
    
    with open("datos_video.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    asyncio.run(generar_audio_manual())
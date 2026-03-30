import asyncio
from rich.console import Console
from rich.panel import Panel

import cerebro
import ojos
import editor
import subir

console = Console()

async def flujo_completo():
    console.clear()
    console.rule("[bold magenta]🏭 FÁBRICA DE SHORTS: EL VELO OCULTO[/bold magenta]")

    # PASO 1: CEREBRO (Seleccionar guion del historial + Generar Audio)
    console.print(Panel("1️⃣  ACTIVANDO CEREBRO (Guion desde historial + Audio)", style="cyan"))
    try:
        await cerebro.generar_audio_manual()
    except Exception as e:
        console.print(f"[red]❌ Error en Cerebro: {e}[/red]")
        return

    # PASO 2: OJOS (Descargar videos de Pixabay)
    console.print(Panel("2️⃣  ACTIVANDO OJOS (Pixabay)", style="green"))
    try:
        ojos.buscar_videos_stock()
    except Exception as e:
        console.print(f"[red]❌ Error en Ojos: {e}[/red]")
        return

    # PASO 3: EDITOR (Montaje y Efectos)
    console.print(Panel("3️⃣  ACTIVANDO EDITOR (Montaje Pro)", style="yellow"))
    try:
        editor.editor_pro()
    except Exception as e:
        console.print(f"[red]❌ Error en Editor: {e}[/red]")
        return

    # PASO 4: SUBIR (Publicar en YouTube)
    console.print(Panel("4️⃣  SUBIENDO A YOUTUBE", style="red"))
    try:
        subir.subir_video()
    except Exception as e:
        console.print(f"[red]❌ Error subiendo a YouTube: {e}[/red]")
        return

    console.rule("[bold green]✨ PROCESO TERMINADO CON ÉXITO ✨[/bold green]")
    console.print("El video ya está publicado en YouTube Shorts.")

if __name__ == "__main__":
    asyncio.run(flujo_completo())

import asyncio
from rich.console import Console
from rich.panel import Panel

# Importamos tus módulos nuevos
# Asegúrate de que los archivos se llamen cerebro.py, ojos.py y editor.py
import cerebro
import ojos
import editor

console = Console()

async def flujo_completo():
    console.clear()
    console.rule("[bold magenta]🏭 FÁBRICA DE SHORTS: EL VELO OCULTO[/bold magenta]")

    # PASO 1: CEREBRO (Generar Audio y JSON)
    console.print(Panel("1️⃣  ACTIVANDO CEREBRO (Guion + Audio)", style="cyan"))
    # Llamamos a la función manual que creamos (verifica que en cerebro.py se llame así)
    try:
        await cerebro.generar_audio_manual()
    except AttributeError:
        # Por si acaso tienes una versión vieja con otro nombre
        if hasattr(cerebro, 'generar_guion_viral'):
            await cerebro.generar_guion_viral()
        else:
            console.print("[red]❌ Error: No encuentro la función en cerebro.py[/red]")
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

    console.rule("[bold green]✨ PROCESO TERMINADO CON ÉXITO ✨[/bold green]")
    console.print("Revisa el archivo: [bold]reel_definitivo.mp4[/bold]")

if __name__ == "__main__":
    asyncio.run(flujo_completo())
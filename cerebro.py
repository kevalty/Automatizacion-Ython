import json
import asyncio
import edge_tts
import os
import sys
from rich.console import Console
from rich.panel import Panel

console = Console()

GUIONES_FILE = "data/guionesVeloOculto.json"
HISTORIAL_FILE = "data/historial.json"
AUDIO_PATH = "audio_final.mp3"
DATA_FILE = "datos_video.json"

def cargar_siguiente_guion():
    if not os.path.exists(GUIONES_FILE):
        console.print(f"[bold red]❌ No encontré el archivo de guiones: {GUIONES_FILE}[/bold red]")
        sys.exit(1)

    if not os.path.exists(HISTORIAL_FILE):
        historial = {"usados": [], "fallidos": []}
    else:
        with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
            historial = json.load(f)

    with open(GUIONES_FILE, "r", encoding="utf-8") as f:
        todos = json.load(f)["guiones"]

    usados = set(historial.get("usados", []))
    fallidos = set(historial.get("fallidos", []))
    excluidos = usados | fallidos

    disponibles = [g for g in todos if g["id"] not in excluidos]

    if not disponibles:
        console.print("[bold red]⚠️ Ya se usaron todos los guiones disponibles. Reinicia el historial.[/bold red]")
        sys.exit(1)

    guion = disponibles[0]
    console.print(Panel(
        f"[bold]ID:[/bold] {guion['id']}\n"
        f"[bold]Título:[/bold] {guion['titulo']}\n"
        f"[bold]Disponibles restantes:[/bold] {len(disponibles) - 1}",
        title="📋 Guion Seleccionado"
    ))
    return guion, historial

async def generar_audio_manual():
    console.rule("[bold purple]👁️ EL VELO OCULTO: Cargando Guion[/bold purple]")

    guion, historial = cargar_siguiente_guion()

    texto_final = guion["texto_narrado"].strip()
    palabras = len(texto_final.split())
    console.print(Panel(f"📝 Palabras: {palabras}\n⏱️ Duración estimada: ~{round(palabras/2.5)}s", title="Análisis de Guion"))

    if palabras > 145:
        console.print("[bold yellow]⚠️ Guion largo, podría pasar de 60s.[/bold yellow]")

    console.print("[blue]🗣️ Generando audio...[/blue]")
    comunicate = edge_tts.Communicate(texto_final, "es-CO-GonzaloNeural", rate="+5%", pitch="-2Hz")
    await comunicate.save(AUDIO_PATH)
    console.print(f"[green]✅ Audio listo: {AUDIO_PATH}[/green]")

    # Guardar datos completos para el editor y para subir.py
    datos = {
        "id_guion": guion["id"],
        "titulo_video": guion["titulo"],
        "texto_para_narrar": texto_final,
        "busqueda_visual_keywords": guion.get("keywords_imagenes", []),
        "descripcion_youtube": guion.get("descripcion_youtube", ""),
        "tags": guion.get("tags", [])
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

    # Marcar como usado en el historial
    historial["usados"].append(guion["id"])
    with open(HISTORIAL_FILE, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=4)

    console.print(f"[green]✅ Historial actualizado. ID {guion['id']} marcado como usado.[/green]")

if __name__ == "__main__":
    asyncio.run(generar_audio_manual())

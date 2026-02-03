import os
import json
import time
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from rich.console import Console

console = Console()

# --- CONFIGURACIÓN ---
CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

VIDEO_FILE = "reel_definitivo.mp4"
METADATA_FILE = "datos_video.json"

def autenticar_youtube():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRET_FILE):
                console.print(f"[red]❌ Faltan las credenciales: {CLIENT_SECRET_FILE}[/red]")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return build(API_NAME, API_VERSION, credentials=creds)

def subir_video():
    console.rule("[bold red]📡 SUBIENDO DIRECTO A PÚBLICO[/bold red]")

    # 1. Autenticación
    youtube = autenticar_youtube()
    if not youtube:
        return

    # 2. Leer datos
    titulo = "Video Viral"
    descripcion = "Suscríbete para más misterios. #Shorts #Misterio #Curiosidades"
    tags = ["misterio", "curiosidades", "shorts", "elvelooculto"]

    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            titulo = data.get("titulo_video", titulo)
            if len(titulo) > 95: titulo = titulo[:95] # Límite de seguridad
            
            # Descripción optimizada
            descripcion = f"{data.get('texto_para_narrar', '')[:100]}...\n\n👇 SUSCRÍBETE AHORA 👇\n#Misterio #Shorts #ElVeloOculto #Terror #Curiosidades"

    console.print(f"📝 Título: [cyan]{titulo}[/cyan]")
    console.print(f"🌍 Estado: [bold green]PÚBLICO[/bold green]")
    
    # 3. Preparar subida
    if not os.path.exists(VIDEO_FILE):
        console.print(f"[red]❌ No encuentro el video: {VIDEO_FILE}[/red]")
        return

    body = {
        'snippet': {
            'title': titulo,
            'description': descripcion,
            'tags': tags,
            'categoryId': '24' # Categoría 24 = Entretenimiento (Mejor para viralidad)
        },
        'status': {
            'privacyStatus': 'public', # <--- ¡AQUÍ ESTÁ EL CAMBIO!
            'selfDeclaredMadeForKids': False
        }
    }

    # 4. Subir
    console.print("[yellow]🚀 Enviando a los servidores de YouTube...[/yellow]")
    media = MediaFileUpload(VIDEO_FILE, chunksize=-1, resumable=True)
    
    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            console.print(f"   ⬆️ Subiendo: {int(status.progress() * 100)}%")

    console.rule("[bold green]✅ ¡PUBLICADO CON ÉXITO![/bold green]")
    console.print(f"El video ya está visible para todo el mundo.")
    console.print(f"🔗 Link: https://youtube.com/shorts/{response['id']}")

if __name__ == "__main__":
    subir_video()
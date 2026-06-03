# preprocessing.py
import re
import urllib.parse as urlparse
from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY, RE_LEXICON

def limpiar_texto(texto):
    """Limpia el texto eliminando caracteres especiales y dejando solo minúsculas."""
    if not isinstance(texto, str):
        return ""
    texto = texto.lower()
    texto = re.sub(r'[^a-zA-ZáéíóúñÁÉÍÓÚÑ𠖇 ]', '', texto)
    return texto.strip()

def calcular_densidad_insultos(texto_limpio):
    """Calcula cuántas palabras del léxico especializado aparecen en el texto."""
    if not texto_limpio:
        return 0, 0.0
    palabras = texto_limpio.split()
    coincidencias = RE_LEXICON.findall(texto_limpio)
    conteo = len(coincidencias)
    densidad = conteo / len(palabras) if palabras else 0.0
    return conteo, densidad

def extraer_id_video(url):
    """Extrae el ID único de un video a partir de su URL de YouTube."""
    url_data = urlparse.urlparse(url)
    query = urlparse.parse_qs(url_data.query)
    video_id = query.get("v")
    if video_id:
        return video_id[0]
    if url_data.netloc == "youtu.be":
        return url_data.path[1:]
    return None

def extraer_comentarios_de_link(url_enlace):
    """
    Se conecta a la API de YouTube usando tu clave, extrae los comentarios 
    reales del video y los devuelve en una lista de texto plano.
    """
    video_id = extraer_id_video(url_enlace)
    if not video_id:
        print("❌ URL de YouTube no válida o no se pudo extraer el ID del video.")
        return []

    try:
        # Inicializar el servicio de la API de Google con tu llave guardada
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        # Solicitar los hilos de comentarios reales del video
        respuesta = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=50,  # Extraer los últimos 50 comentarios reales de la gente
            textFormat='plainText'
        ).execute()

        comentarios_reales = []
        for item in respuesta.get('items', []):
            comentario = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comentarios_reales.append(comentario)
            
        return comentarios_reales

    except Exception as e:
        print(f"❌ Error al consultar la API de YouTube: {e}")
        print("Verifica tu conexión a internet o que tu YOUTUBE_API_KEY en config.py sea la correcta.")
        return []
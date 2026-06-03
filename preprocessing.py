# preprocessing.py
import re
import urllib.parse as urlparse
from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY, RE_LEXICON

def limpiar_texto(texto):
    """
    Normaliza el texto de entrada removiendo caracteres especiales,
    elementos de puntuacion y forzando codificacion en minusculas.
    """
    if not isinstance(texto, str):
        return ""
    texto = texto.lower()
    texto = re.sub(r'[^a-zA-ZáéíóúñÁÉÍÓÚÑ ]', '', texto)
    return texto.strip()

def calcular_densidad_insultos(texto_limpio):
    """
    Cuantifica la frecuencia absoluta y calcula la densidad estadistica
    de coincidencias basadas en el automata de expresiones regulares.
    """
    if not texto_limpio:
        return 0, 0.0
    palabras = texto_limpio.split()
    coincidencias = RE_LEXICON.findall(texto_limpio)
    conteo = len(coincidencias)
    densidad = conteo / len(palabras) if palabras else 0.0
    return conteo, density

def extraer_id_video(url):
    """
    Ejecuta el analisis sintactico de una URL de la plataforma para 
    aislar y extraer el identificador alfanumerico unico del recurso.
    """
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
    Establece conexion sincrona con el protocolo remoto de la API de YouTube,
    recuperando los hilos de publicaciones asociados al identificador del video.
    """
    video_id = extraer_id_video(url_enlace)
    if not video_id:
        print("ERROR: Sintaxis de URL no valida o identificador de recurso ausente.")
        return []

    try:
        # Instanciacion del servicio de consulta bajo el protocolo cliente-servidor
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        # Peticion estructurada de transferencia de estado de recursos (REST)
        respuesta = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=50,  
            textFormat='plainText'
        ).execute()

        comentarios_reales = []
        for item in respuesta.get('items', []):
            comentario = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comentarios_reales.append(comentario)
            
        return comentarios_reales

    except Exception as error:
        print(f"ERROR: Fallo en la resolucion de la peticion del servicio web: {error}")
        print("Verifique las credenciales de autenticacion de red (YOUTUBE_API_KEY).")
        return []
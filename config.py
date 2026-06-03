# config.py
import os
import re


YOUTUBE_API_KEY = "AIzaSyAlSvJpd7QpETzNQLaj-dOAdq3YUyDyrW8"

# 1. Rutas de almacenamiento del proyecto
DATA_DIR = "data"
MODEL_DIR = "models"
GRAPH_DIR = "outputs"

# Crear carpetas si no existen de forma automática
for carpeta in [DATA_DIR, MODEL_DIR, GRAPH_DIR]:
    os.makedirs(carpeta, exist_ok=True)

# Variables globales de archivos
DATASET_CSV = os.path.join(DATA_DIR, "dataset_odio_internet.csv")
MODELO_PKL = os.path.join(MODEL_DIR, "red_neuronal_odio.pkl")
VECTORIZADOR_PKL = os.path.join(MODEL_DIR, "vectorizador_tfidf.pkl")

# 2. Léxico especializado en insultos descriptivos y palabras altisonantes
# config.py (Sección del Léxico Expandida)

# 4. Léxico Especializado de Alta Densidad (Expandido y Robustecido)
LEXICON_INSULTOS = [
    # --- Bloque Original Optimizado ---
    r"pendej[oa]s?", r"estupid[oa]s?", r"estúpid[oa]s?", r"imbécil(es)?", r"imbecil(es)?",
    r"idiotas?", r"mierdas?", r"put[oa]s?", r"cabrón(es)?", r"cabron[aa]s?",
    r"inept[oa]s?", r"basuras?", r"escorias?", r"infeli(z|ces)", r"lacras?", 
    r"parásitos?", r"parasitos?", r"ignorantes?", r"miserables?", r"ratas?", 
    r"incompetentes?", r"maldit[oa]s?", r"culer[oa]s?", r"perr[oa]s?",

    # --- Bloque Expandido: Chovinismo, Xenofobia y Deshumanización ---
    r"asqueros[oa]s?", r"repulsiv[oa]s?", r"ascos?", r"vómitos?", r"vómitos?",
    r"plagas?", r"parásitos?", r"parásitas?", r"garrapatas?", r"piojos[oa]s?",
    r"marranos?", r"puerc[oa]s?", r"cerd[oa]s?", r"animal(es)?", r"bestias?",
    r"retrógradas?", r"mediocres?", r"fracasad[oa]s?", r"nefast[oa]s?",

    # --- Bloque Expandido: Mexicanismos y Argot de Internet (Hostilidad Dirigida) ---
    r"chingad[oa]s?", r"chingaquedito", r"cul[oa]s?", r"maricones?", r"maricón",
    r"jotos?", r"nacos?", r"nacas?", r"mamones?", r"mamonas?", r"mamón",
    r"babos[oa]s?", r"tarad[oa]s?", r"zoquetes?", r"pendejadas?", r"pendejetes?",
    r"huevón(es)?", r"huevona(s)?", r"pinches?", r"pencos?", r"mediocres?",

    # --- Bloque Expandido: Violencia Verbal / Amenazas y Odio Político Grupal ---
    r"lacras?", r"ratas?", r"rater[oa]s?", r"corrupt[oa]s?", r"mafios[oa]s?",
    r"vándalos?", r"vándalas?", r"delincuentes?", r"criminal(es)?", r"asesin[oa]s?",
    r"malnacid[oa]s?", r"desgraciad[oa]s?", r"maldit[oa]s?", r"linchar?", r"muérete",
    r"muéranse", r"mátanlo", r"mátenlos", r"lárgate", r"lárguense", r"estorbos?"
]

def obtener_regex_lexicon():
    """Compila el léxico en una expresión regular optimizada."""
    patron = r'\b(' + '|'.join(LEXICON_INSULTOS) + r')\b'
    return re.compile(patron, re.IGNORECASE)

RE_LEXICON = obtener_regex_lexicon()
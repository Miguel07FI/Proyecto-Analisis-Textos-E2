# config.py
import os
import re

# Credenciales de API de Google Cloud Platform
YOUTUBE_API_KEY = "AIzaSyAlSvJpd7QpETzNQLaj-dOAdq3YUyDyrW8"

# Infraestructura de almacenamiento local
DATA_DIR = "data"
MODEL_DIR = "models"
GRAPH_DIR = "outputs"

for carpeta in [DATA_DIR, MODEL_DIR, GRAPH_DIR]:
    os.makedirs(carpeta, exist_ok=True)

# Rutas globales de archivos para el flujo de datos
DATASET_CSV = os.path.join(DATA_DIR, "dataset_odio_internet.csv")
MODELO_PKL = os.path.join(MODEL_DIR, "red_neuronal_odio.pkl")
VECTORIZADOR_PKL = os.path.join(MODEL_DIR, "vectorizador_tfidf.pkl")

# Hiperparametros estructurales para la Red Neuronal Convolucional (CNN 1D)
MAX_WORDS_VOCAB = 5000     
MAX_SEQUENCE_LEN = 100     
CNN_FILTERS = 128          
EMBEDDING_DIM = 64         
BATCH_SIZE = 64            
EPOCHS = 20                

# Lexico especializado compilado mediante patrones morfologicos (Regex)
LEXICON_INSULTOS = [
    # Cadenas base con flexiones gramaticales basicas
    r"pendej[oa]s?", r"estupid[oa]s?", r"estúpid[oa]s?", r"imbécil(es)?", r"imbecil(es)?",
    r"idiotas?", r"mierdas?", r"put[oa]s?", r"cabrón(es)?", r"cabron[aa]s?",
    r"inept[oa]s?", r"basuras?", r"escorias?", r"infeli(z|ces)", r"lacras?", 
    r"parásitos?", r"parasitos?", r"ignorantes?", r"miserables?", r"ratas?", 
    r"incompetentes?", r"maldit[oa]s?", r"culer[oa]s?", r"perr[oa]s?",

    # Patrones orientados a deshumanizacion y adjetivos hostiles
    r"asqueros[oa]s?", r"repulsiv[oa]s?", r"ascos?", r"vómitos?", r"vómitos?",
    r"plagas?", r"parásitos?", r"parásitas?", r"garrapatas?", r"piojos[oa]s?",
    r"marranos?", r"puerc[oa]s?", r"cerd[oa]s?", r"animal(es)?", r"bestias?",
    r"retrógradas?", r"mediocres?", r"fracasad[oa]s?", r"nefast[oa]s?",

    # Localismos regionales y argot informal de redes sociales
    r"chingad[oa]s?", r"chingaquedito", r"cul[oa]s?", r"maricones?", r"maricón",
    r"jotos?", r"nacos?", r"nacas?", r"mamones?", r"mamonas?", r"mamón",
    r"babos[oa]s?", r"tarad[oa]s?", r"zoquetes?", r"pendejadas?", r"pendejetes?",
    r"huevón(es)?", r"huevona(s)?", r"pinches?", r"pencos?", r"mediocres?",

    # Indicadores de violencia directa, imperativos y hostilidad dirigida
    r"lacras?", r"ratas?", r"rater[oa]s?", r"corrupt[oa]s?", r"mafios[oa]s?",
    r"vándalos?", r"vándalas?", r"delincuentes?", r"criminal(es)?", r"asesin[oa]s?",
    r"malnacid[oa]s?", r"desgraciad[oa]s?", r"maldit[oa]s?", r"linchar?", r"muérete",
    r"muéranse", r"mátanlo", r"mátenlos", r"lárgate", r"lárguense", r"estorbos?"
]

def obtener_regex_lexicon():
    """
    Compila el listado de patrones en una sola expresion regular optimizada, 
    estableciendo fronteras de palabra (\b) para acelerar la busqueda en C.
    """
    patron = r'\b(' + '|'.join(LEXICON_INSULTOS) + r')\b'
    return re.compile(patron, re.IGNORECASE)

RE_LEXICON = obtener_regex_lexicon()
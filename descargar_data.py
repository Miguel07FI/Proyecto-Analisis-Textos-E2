# descargar_data.py
import pandas as pd
import random
from config import DATASET_CSV

print("\n[CLI] Generando conjunto de datos sinteticos con ruido linguistico...")

# Matrices lexicas para la construccion de la Clase 1 (Discurso de Odio)
sujetos = ["Ese usuario", "El creador del video", "La diputada", "Este tipo", "Esa mujer", "El moderador", "Ese hater", "El streamer", "El candidato", "El árbitro"]
verbos_agresivos = ["es una completa", "demuestra ser una", "se comporta como una", "no es más que una", "resultó ser una"]
insultos_reales = ["escoria", "lacra", "basura", "rata", "parásito", "plaga", "mierda", "incompetente", "miserable", "inepto", "ignorante", "pendejo", "pendeja", "imbécil", "idiota", "cabrón"]
conclusiones_odio = ["deberían banearlo ya", "hay que lincharlo entre todos", "da asco que exista", "lárgate de esta plataforma", "ojalá te pase algo malo", "eres un peligro social"]

# Estructuras linguisticas informales para la Clase 0 (Control/No Odio)
vulgari_casual = [
    "Qué pendejo estoy, olvidé el archivo en la otra computadora.",
    "El examen de la facultad estuvo de la chingada, pero alcancé a pasar.",
    "No mames, está cabrón el tráfico de hoy en la avenida principal.",
    "Qué pendejada acabo de hacer con el café, lo derramé sobre el teclado.",
    "Ya valió madre, se cayó el sistema de la escuela otra vez.",
    "Está cabrón terminar este proyecto final para el lunes."
]

# Estructuras linguisticas formales para la Clase 0 (Control/No Odio)
neutros_academia = [
    "El proyecto final de ingeniería quedó agendada para el próximo lunes.",
    "Recomiendo ampliamente este libro para aprender estructuras de datos.",
    "Muchas gracias por compartir el enlace con la documentación de la API.",
    "¿Alguien sabe a qué hora abre la biblioteca central de la facultad?",
    "Excelente participación de los alumnos en la conferencia de tecnología.",
    "El procesamiento de lenguaje natural requiere un análisis estadístico profundo."
]

# Inicializacion de semilla estatica para garantizar la reproducibilidad matematica
random.seed(42)
registros = []
total_registros = 12000
mitad_registros = total_registros // 2

# Generacion y balanceo de la Clase 1: Discurso de Odio (6,000 instancias)
while len([r for r in registros if r["label"] == 1]) < mitad_registros:
    # 90% combinatoria explicita, 10% estructuras de hostilidad implicita sin lexico directo
    if random.random() > 0.1:
        txt = f"{random.choice(sujetos)} {random.choice(verbos_agresivos)} {random.choice(insultos_reales)} y {random.choice(conclusiones_odio)}."
    else:
        txt = f"{random.choice(sujetos)} debería desaparecer, arruina la comunidad y nadie lo quiere aquí."
    
    # Inyeccion de ruido mediante capitalizacion total periodica
    if random.random() > 0.8: 
        txt = txt.upper()
        
    registros.append({"texto": txt, "label": 1})

# Generacion y balanceo de la Clase 0: No Odio / Control (6,000 instancias)
vocabulario_no_odio = vulgari_casual + neutros_academia
while len([r for r in registros if r["label"] == 0]) < mitad_registros:
    txt = random.choice(vocabulario_no_odio)
    
    # Concatenacion de interjecciones coloquiales peyorativas sin blanco dirigido (ruido estructural)
    if random.random() > 0.6:
        txt = f"{txt} Qué dolor de cabeza, puta madre."
        
    registros.append({"texto": txt, "label": 0})

# Consolidacion, aleatorizacion e instanciacion del DataFrame final
df_masivo = pd.DataFrame(registros)
df_masivo = df_masivo.sample(frac=1, random_state=42).reset_index(drop=True)
df_masivo.to_csv(DATASET_CSV, index=False, encoding='utf-8')

print(f"REGISTRO: Conjunto de datos exportado a '{DATASET_CSV}' ({total_registros} instancias binarias).")
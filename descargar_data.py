# descargar_data.py
import pandas as pd
import random
from config import DATASET_CSV

print("\n[CLI] Generando dataset masivo con factor de ruido lingüístico...")

sujetos = ["Ese usuario", "El creador del video", "La diputada", "Este tipo", "Esa mujer", "El moderador", "Ese hater", "El streamer", "El candidato", "El árbitro"]
verbos_agresivos = ["es una completa", "demuestra ser una", "se comporta como una", "no es más que una", "resultó ser una"]
insultos_reales = ["escoria", "lacra", "basura", "rata", "parásito", "plaga", "mierda", "incompetente", "miserable", "inepto", "ignorante", "pendejo", "pendeja", "imbécil", "idiota", "cabrón"]
conclusiones_odio = ["deberían banearlo ya", "hay que lincharlo entre todos", "da asco que exista", "lárgate de esta plataforma", "ojalá te pase algo malo", "eres un peligro social"]

vulgari_casual = [
    "Qué pendejo estoy, olvidé el archivo en la otra computadora.",
    "El examen de la facultad estuvo de la chingada, pero alcancé a pasar.",
    "No mames, está cabrón el tráfico de hoy en la avenida principal.",
    "Qué pendejada acabo de hacer con el café, lo derramé sobre el teclado.",
    "Ya valió madre, se cayó el sistema de la escuela otra vez.",
    "Está cabrón terminar este proyecto final para el lunes."
]

neutros_academia = [
    "El proyecto final de ingeniería quedó agendada para el próximo lunes.",
    "Recomiendo ampliamente este libro para aprender estructuras de datos.",
    "Muchas gracias por compartir el enlace con la documentación de la API.",
    "¿Alguien sabe a qué hora abre la biblioteca central de la facultad?",
    "Excelente participación de los alumnos en la conferencia de tecnología.",
    "El procesamiento de lenguaje natural requiere un análisis estadístico profundo."
]

random.seed(42)
registros = []
total_registros = 12000

# Clase 1: Odio (6,000 registros)
while len([r for r in registros if r["label"] == 1]) < (total_registros // 2):
    # 90% odio explícito, 10% odio sutil sin insultos del léxico para confundir a la red
    if random.random() > 0.1:
        txt = f"{random.choice(sujetos)} {random.choice(verbos_agresivos)} {random.choice(insultos_reales)} y {random.choice(conclusiones_odio)}."
    else:
        txt = f"{random.choice(sujetos)} debería desaparecer, arruina la comunidad y nadie lo quiere aquí."
    
    if random.random() > 0.8: txt = txt.upper()
    registros.append({"texto": txt, "label": 1})

# Clase 0: No Odio (6,000 registros)
vocabulario_no_odio = vulgari_casual + neutros_academia
while len([r for r in registros if r["label"] == 0]) < (total_registros // 2):
    txt = random.choice(vocabulario_no_odio)
    # Mezclar oraciones limpias con groserías para forzar a la red a entender el contexto
    if random.random() > 0.6:
        txt = f"{txt} Qué dolor de cabeza, puta madre."
    registros.append({"texto": txt, "label": 0})

df_masivo = pd.DataFrame(registros)
df_masivo = df_masivo.sample(frac=1, random_state=42).reset_index(drop=True)
df_masivo.to_csv(DATASET_CSV, index=False, encoding='utf-8')

print(f"✅ ¡Dataset con ruido guardado en {DATASET_CSV}! (12,000 registros)")
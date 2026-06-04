# descargar_data.py
import pandas as pd
import random
from config import DATASET_CSV

print("\n[CLI] Generando conjunto de datos masivo expandido para corregir falsos positivos...")

# 1. Ampliación de la Clase 1: Discurso de Odio (Matrices Léxicas Multi-Estructura)
sujetos_odio = [
    "Ese usuario", "El creador", "Este tipo", "Esa mujer", "El streamer", "El candidato", 
    "Este ratero", "Ese sinvergüenza", "Pinche perro", "Mugroso resentido", "Esa lacra", 
    "El político", "Los trabajadores", "Ese mentiroso", "Usurero", "Esa basura", "Gente ignorante"
]

verbos_odio = [
    "es una completa", "demuestra ser una", "se comporta como una", "no es más que una", 
    "resultó ser una", "insulta a todos como", "roba y es una", "da asco ver que es una"
]

insultos_odio = [
    "escoria", "lacra", "basura", "rata", "parásito", "plaga", "mierda", "incompetente", 
    "miserable", "inepto", "ignorante", "pendejo", "pendeja", "imbécil", "idiota", "cabrón",
    "ratero", "sinvergüenza", "chillón", "mentiroso", "manoso", "corrupto", "mediocre"
]

conclusiones_odio = [
    "deberían banearlo ya", "hay que lincharlo entre todos", "da asco que exista", 
    "lárgate de esta plataforma", "ojalá te pase algo malo", "eres un peligro social",
    "hay que quemar todo", "nadie le cree nada", "debería desaparecer ya"
]

# Frases crudas completas inspiradas en comentarios reales de internet (Ataques dirigidos)
frases_odio_directas = [
    "Quien es este tipo ratero singuenza mugroso tipo resentido ignorante y manoso.",
    "A este perro mentiroso nadie le cree por chillón.",
    "Usurero ay que quemar Elektra no comprar nada.",
    "Malditos corruptos de mierda ojalá se mueran todos.",
    "Qué pinche asco de persona, una verdadera basura humana.",
    "Lárguense de aquí malditas plagas nadie los quiere.",
    "Este delincuente debería estar en la cárcel, escoria social."
]

# 2. Ampliación de la Clase 0: Mensajes Neutros, Saludos y Control Coloquial
saludos_y_agradecimientos = [
    "Hola Wicha te mando saludos y muchas Gracias por tus Noticias.",
    "Excelente video amigo muchas gracias por compartir la información.",
    "Saludos cordiales profesor desde la Facultad de Ingeniería.",
    "Hola buenos días gracias por el gran aporte al canal.",
    "Hola qué buen contenido me suscribo de inmediato saludos.",
    "Muchas gracias por mantenernos informados todos los días.",
    "Hola comunidad espero que tengan una excelente semana bendiciones."
]

vulgari_casual = [
    "Qué pendejo estoy, olvidé el archivo en la otra computadora.",
    "El examen de la facultad estuvo de la chingada, pero alcancé a pasar.",
    "No mames, está cabrón el tráfico de hoy en la avenida principal.",
    "Qué pendejada acabo de hacer con el café, lo derramé sobre el teclado.",
    "Ya valió madre, se cayó el sistema de la escuela otra vez.",
    "Está cabrón terminar este proyecto final para el lunes.",
    "Puta madre me dolió mucho el golpe en el pie.",
    "Qué buena peda nos pusimos ayer estuvo chingón."
]

neutros_academia = [
    "El proyecto final de ingeniería quedó agendada para el próximo lunes.",
    "Recomiendo ampliamente este libro para aprender estructuras de datos.",
    "Muchas gracias por compartir el enlace con la documentación de la API.",
    "¿Alguien sabe a qué hora abre la biblioteca central de la facultad?",
    "Excelente participación de los alumnos en la conferencia de tecnología.",
    "El procesamiento de lenguaje natural requiere un análisis estadístico profundo."
]

# Inicialización de semilla estática para garantizar la reproducibilidad matemática
random.seed(42)
registros = []
total_registros = 20000  # Aumentamos a 20,000 ejemplos para darle más estabilidad a la CNN
mitad_registros = total_registros // 2

# --- GENERACIÓN DE LA CLASE 1: DISCURSO DE ODIO ---
while len([r for r in registros if r["label"] == 1]) < mitad_registros:
    prob = random.random()
    if prob < 0.6:
        # Combinatoria clásica dinámica
        txt = f"{random.choice(sujetos_odio)} {random.choice(verbos_odio)} {random.choice(insultos_odio)} y {random.choice(conclusiones_odio)}."
    elif prob < 0.9:
        # Estructuras explícitas e implícitas variadas
        txt = f"{random.choice(sujetos_odio)} debería desaparecer, arruina la comunidad y {random.choice(conclusiones_odio)}."
    else:
        # Inyección directa de las frases del mundo real con las que fallaba
        txt = random.choice(frases_odio_directas)
    
    # Ruido estructural por capitalización
    if random.random() > 0.8: 
        txt = txt.upper()
        
    registros.append({"texto": txt, "label": 1})

# --- GENERACIÓN DE LA CLASE 0: NO ODIO / CONTROL ---
while len([r for r in registros if r["label"] == 0]) < mitad_registros:
    prob = random.random()
    if prob < 0.4:
        txt = random.choice(saludos_y_agradecimientos)
    elif prob < 0.7:
        txt = random.choice(vulgari_casual)
    else:
        txt = random.choice(neutros_academia)
    
    # Concatenación de interjecciones coloquiales peyorativas sin blanco dirigido (ruido estructural)
    if random.random() > 0.7 and txt not in saludos_y_agradecimientos:
        txt = f"{txt} Qué dolor de cabeza, puta madre."
        
    registros.append({"texto": txt, "label": 0})

# Consolidación, aleatorización e instanciacion del DataFrame final
df_masivo = pd.DataFrame(registros)
df_masivo = df_masivo.sample(frac=1, random_state=42).reset_index(drop=True)
df_masivo.to_csv(DATASET_CSV, index=False, encoding='utf-8')

print(f"REGISTRO: ¡Dataset corregido con éxito! Exportado a '{DATASET_CSV}' ({total_registros} instancias balanceadas).")
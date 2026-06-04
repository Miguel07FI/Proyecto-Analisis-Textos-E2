# descargar_data.py
import pandas as pd
import random
from config import DATASET_CSV

print("\n[SADOW BACKEND] Generando super-dataset balanceado de alta sensibilidad (30,000 instancias)...")

# --- BANCO DE DATOS EXHAUSTIVO PARA LA CLASE 1 (DISCURSO DE ODIO / HOSTILIDAD) ---
sujetos_hostiles = [
    "Ese usuario", "El creador del video", "Este tipo ratero", "Esa mujer", "El streamer mentiroso",
    "El candidato corrupto", "Ese sinvergüenza", "Pinche perro chillón", "Mugroso resentido ignorante",
    "Esa lacra mafiosa", "El político delincuente", "Los usureros de las empresas", "Esa basura humana",
    "Gente retrógrada", "Este delincuente", "El moderador inepto", "Esa lacra social", "Ese infeliz"
]

verbos_hostiles = [
    "es una completa", "demuestra ser una", "se comporta como una", "no es más que una",
    "resultó ser una", "insulta a la sociedad como", "roba a los ciudadanos siendo una",
    "da un asco profundo porque es una", "esconde que es una", "promueve ser una"
]

nucleos_odio = [
    "escoria", "lacra", "basura", "rata", "parásito", "plaga", "mierda", "incompetente",
    "miserable", "inepto", "ignorante", "pendejo", "pendeja", "imbécil", "idiota", "cabrón",
    "ratero", "sinvergüenza", "chillón", "mentiroso", "manoso", "corrupto", "mediocre", "puercos",
    "marrano", "bestia nefasta", "fracasado", "lacra social", "vándalo", "criminal"
]

conclusiones_violentas = [
    "deberían banearlo ya de internet", "hay que lincharlo entre todos", "da asco que exista en la plataforma",
    "lárgate de esta comunidad", "ojalá te pase algo malo y te mueras", "eres un peligro social estorbando",
    "hay que quemar todo y destruirlos", "nadie le cree por chillón", "debería desaparecer de inmediato",
    "hay que partirle la madre", "no compren nada con ese usurero", "mátenlo por rata"
]

# Corpus de validación empírica basado en tus capturas reales de error
comentarios_odio_reales = [
    "Quien es este tipo ratero Con que moral insulta à la presidenta si el es un ratero sinverguenxa que a sus trabajadores los have trabajar 7 dias à la semana y con un horario de 12 horas y dias festivos Mugroso tipo resentido ignorante y manoso",
    "A este perro mentiroso nadie le cree por chillón",
    "Usurero ay que quemar Elektra no comprar nada",
    "Malditos corruptos ojalá se mueran todos",
    "Pinche viejo ratero muérete ya",
    "Hay que linchar a ese infeliz escoria de la sociedad",
    "Lárguense de aquí malditas plagas asquerosas",
    "Este canal es una puta mierda y el creador es un pendejo incompetente",
    "Qué maldito asco me da este tipo, ojalá lo desaparezcan",
    "Puras mentiras de este cerdo mentiroso desgraciado"
]

# --- BANCO DE DATOS EXHAUSTIVO PARA LA CLASE 0 (CONTROL / NO ODIO / CASUAL) ---
saludos_neutrales = [
    "Hola Wicha te mando saludos y muchas Gracias por tus Noticias",
    "Excelente video amigo muchas gracias por compartir la información y mantener el canal activo",
    "Saludos cordiales profesor desde la Facultad de Ingeniería de la UNAM",
    "Hola buenos días excelente participación gracias por el gran aporte al canal",
    "Hola qué buen contenido me suscribo de inmediato saludos desde México",
    "Muchas gracias por mantenernos informados con objetividad todos los días",
    "Hola comunidad espero que tengan una excelente semana llena de éxito, bendiciones",
    "Buenas tardes saludos al equipo técnico por la excelente transmisión en vivo",
    "Gracias por el análisis detallado, un fuerte abrazo para todo el equipo",
    "Hola un gusto saludarte de nuevo, sigo tus videos desde hace años"
]

vulgari_mexicano_casual = [
    "Qué pendejo estoy, olvidé el archivo de la materia en la otra computadora.",
    "El examen de la facultad estuvo de la chingada, pero alcancé a pasar de milagro.",
    "No mames, está cabrón el tráfico de hoy en la avenida principal para llegar a clases.",
    "Qué pendejada acabo de hacer con el café, lo derramé completo sobre el teclado.",
    "Ya valió madre, se cayó el sistema de inscripciones de la escuela otra vez.",
    "Está cabrón terminar este proyecto final de programación para el lunes.",
    "Puta madre me dolió mucho el golpe que me di en el pie con la mesa.",
    "Qué buena peda nos pusimos ayer con los amigos estuvo chingón todo.",
    "Ese examen de cálculo estuvo bien pinche difícil la verdad.",
    "No mames wey, casi me atropella un carro cruzando la avenida."
]

textos_academicos_puros = [
    "El proyecto final de ingeniería quedó agendada para el próximo lunes por la tarde.",
    "Recomiendo ampliamente este libro para aprender estructuras de datos y algoritmos complejos.",
    "Muchas gracias por compartir el enlace con la documentación de la API de Google.",
    "¿Alguien sabe a qué hora abre la biblioteca central de la facultad de ingeniería?",
    "Excelente participación de los alumnos en la conferencia magistral de tecnología avanzada.",
    "El procesamiento de lenguaje natural moderno requiere un análisis estadístico profundo.",
    "Las redes neuronales convolucionales ofrecen una excelente ventaja en análisis de señales.",
    "El algoritmo de optimización lineal resuelve problemas de asignación de recursos de manera óptima.",
    "La configuración del servidor requiere permisos de administrador del sistema de red.",
    "Se convoca a los estudiantes al seminario de inteligencia artificial aplicada de este semestre."
]

# Inicialización del entorno computacional balanceado
random.seed(42)
registros = []
total_registros = 30000  # Escalado masivo para máxima generalización de la CNN 1D
mitad_registros = total_registros // 2

# --- GENERACIÓN DE LA CLASE 1: DISCURSO DE ODIO (15,000 ejemplos) ---
while len([r for r in registros if r["label"] == 1]) < mitad_registros:
    prob = random.random()
    if prob < 0.6:
        # Combinatoria masiva sintáctica
        txt = f"{random.choice(sujetos_hostiles)} {random.choice(verbos_hostiles)} {random.choice(nucleos_odio)} y {random.choice(conclusiones_violentas)}"
    elif prob < 0.85:
        # Variantes de amenazas directas
        txt = f"{random.choice(sujetos_hostiles)} es una {random.choice(nucleos_odio)}, {random.choice(conclusiones_violentas)}"
    else:
        # Inyección directa de patrones del mundo real para erradicar los falsos negativos
        txt = random.choice(comentarios_odio_reales)
        
    # Inyección de ruido estructural tipográfico (Mayúsculas)
    if random.random() > 0.8: 
        txt = txt.upper()
        
    registros.append({"texto": txt, "label": 1})

# --- GENERACIÓN DE LA CLASE 0: NO ODIO / CONTROL (15,000 ejemplos) ---
while len([r for r in registros if r["label"] == 0]) < mitad_registros:
    prob = random.random()
    if prob < 0.4:
        # Inyección masiva de saludos para blindar el modelo contra falsos positivos
        txt = random.choice(saludos_neutrales)
        # Añadir ligeras variaciones aleatorias para que no memorice el texto exacto
        if random.random() > 0.5:
            txt = f"{txt} !!!"
    elif prob < 0.7:
        txt = random.choice(vulgari_mexicano_casual)
    else:
        txt = random.choice(textos_academicos_puros)
        
    # Concatenación de interjecciones ruidosas peyorativas no dirigidas
    if random.random() > 0.7 and txt not in saludos_neutrales:
        txt = f"{txt} Qué dolor de cabeza, puta madre."
        
    registros.append({"texto": txt, "label": 0})

# Consolidación, aleatorización y almacenamiento físico
df_masivo = pd.DataFrame(registros)
df_masivo = df_masivo.sample(frac=1, random_state=42).reset_index(drop=True)
df_masivo.to_csv(DATASET_CSV, index=False, encoding='utf-8')

print(f"REGISTRO: Conjunto de datos ultra-sensible exportado exitosamente a '{DATASET_CSV}' con {total_registros} instancias binarias.")
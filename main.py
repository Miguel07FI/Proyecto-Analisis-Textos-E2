# main.py
import os
import sys
import joblib
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

from config import YOUTUBE_API_KEY
from preprocessing import extraer_comentarios_de_link, limpiar_texto
from generar_reporte import crear_reporte_pdf 

MODEL_PATH = os.path.join("models", "cnn_odio_model.keras")
TOKENIZER_PATH = os.path.join("models", "tokenizer_cnn.pkl")

def mostrar_bienvenida():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 70)
    print("UNIVERSIDAD NACIONAL AUTONOMA DE MEXICO - FACULTAD DE INGENIERIA")
    print("SISTEMA DE AUDITORIA DE CONTENIDO BASADO EN APRENDIZAJE PROFUNDO")
    print("=" * 70)
    print("Arquitectura: Word Embeddings + Red Neuronal Convolucional (CNN 1D)")
    print("Proposito: Clasificacion semantica y analisis de hostilidad dirigida")
    print("=" * 70)

def inicializar_sistema():
    if not (os.path.exists(MODEL_PATH) and os.path.exists(TOKENIZER_PATH)):
        print("ERROR CRITICO: No se detectan los artefactos logicos en 'models/'.")
        print("Ejecute 'python train_nn.py' para entrenar la arquitectura convolucional.")
        sys.exit(1)
    return tf.keras.models.load_model(MODEL_PATH), joblib.load(TOKENIZER_PATH)

def obtener_comentarios_simulados():
    print("\n[MODO CONTROL]: Cargando banco de datos sinteticos para pruebas locales...")
    return [
        "Eres la mas pende.ja del planeta pu.ta feminista pinc.he cancion culera la del mundial ponte ver.gas",
        "Muchas gracias por compartir el enlace con la documentación de la API de Google.",
        "Oy nomas a este perro, yo vivo aqui,y lo k ay,es un desmadre que asco es cuchar a este wey",
        "Qué pendejo estoy, olvidé las llaves del departamento otra vez.",
        "Felicidades a todos los ingenieros que hicieron posible este gran proyecto, excelente video.",
        "Ese candidato es una completa escoria y una lacra miserable, deberían lincharlo entre todos.",
        "¿Alguien sabe a qué hora abre la biblioteca central de la facultad el día de mañana?",
        "Este canal es una puta basura, lárgate de la plataforma, das repulsión total."
    ]

def main():
    mostrar_bienvenida()
    model, tokenizer = inicializar_sistema()
    print("\nSTATUS: Red Neuronal Convolucional y Tokenizador cargados en memoria.")
    
    print("\nSeleccione el modo de ejecucion para la inferencia:")
    print("  [1] MODO PRUEBA (Procesamiento de datos sinteticos locales)")
    print("  [2] MODO PRODUCCION (Conexion a la API de streaming de YouTube)")
    
    opcion = input("\nSeleccion (1 o 2) > ").strip()
    
    if opcion == "1":
        comentarios_reales = obtener_comentarios_simulados()
        objetivo_texto = "Simulador de Entorno Web Local"
    elif opcion == "2":
        if YOUTUBE_API_KEY == "AIzaSyAlSvJpd7QpETzNQLaj-dOAdq3YUyDyrW8" or YOUTUBE_API_KEY == "":
            print("ERROR: Clave de interfaz de programacion (API Key) no parametrizada.")
            return
        print("\nIngrese la URL del recurso de video objetivo:")
        link_usuario = input("URL > ").strip()
        if not link_usuario: 
            return
        comentarios_reales = extraer_comentarios_de_link(link_usuario)
        objetivo_texto = link_usuario
    else:
        print("ERROR: Seleccion no valida.")
        return

    total_comentarios = len(comentarios_reales)
    if total_comentarios == 0: 
        return

    print("\n" + "=" * 70)
    print("PROCESO: EJECUTANDO EVALUACION VECTORIAL")
    print(f"OBJETIVO: {objetivo_texto}")
    print("=" * 70)

    conteo_odio = 0
    datos_para_reporte = []  

    for i, comentario in enumerate(comentarios_reales, 1):
        comentario_limpio = limpiar_texto(comentario)
        secuencia = tokenizer.texts_to_sequences([comentario_limpio])
        pad_individual = pad_sequences(secuencia, maxlen=100, padding='post', truncating='post')
        
        probabilidad_odio = float(model.predict(pad_individual, verbose=0)[0][0]) * 100
        es_odio = probabilidad_odio >= 50.0

        comentario_corto = comentario.replace("\n", " ")
        if len(comentario_corto) > 110:
            comentario_corto = comentario_corto[:110] + "..."

        if es_odio:
            conteo_odio += 1
            dictamen = "DISCURSO DE ODIO"
            print(f"Instancia #{i}: \"{comentario_corto}\"\n   DICTAMEN: [{dictamen}] | Probabilidad: {probabilidad_odio:.2f}%\n")
        else:
            dictamen = "NEUTRO / COLOQUIAL"
            print(f"Instancia #{i}: \"{comentario_corto}\"\n   DICTAMEN: [{dictamen}] | Probabilidad: {probabilidad_odio:.2f}%\n")
            
        datos_para_reporte.append((i, comentario, probabilidad_odio, dictamen))

    indice_odio_global = (conteo_odio / total_comentarios) * 100
    print("-" * 70)
    print("METRICAS DE AUDITORIA GLOBAL:")
    print(f"   -> Total de instancias analizadas: {total_comentarios}")
    print(f"   -> Instancias confirmadas con hostilidad: {conteo_odio}")
    print(f"   -> INDICE DE ODIO GLOBAL CALCULADO: {indice_odio_global:.2f}%")
    print("=" * 70)
    
    print("\nPROCESO: Compilando informe ejecutivo formal (PDF)...")
    crear_reporte_pdf(
        url_video=objetivo_texto,
        total_comentarios=total_comentarios,
        total_odio=conteo_odio,
        indice_global=indice_odio_global,
        datos_tabla=datos_para_reporte
    )
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
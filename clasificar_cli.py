# clasificar_cli.py
import os
import sys
import numpy as np
import joblib
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

from preprocessing import extraer_comentarios_de_link, limpiar_texto, calcular_densidad_insultos
from config import MAX_SEQUENCE_LEN

def analizar_pagina_web(url_enlace):
    """
    Extrae las publicaciones de una URL, procesa las cadenas a través de 
    la arquitectura CNN 1D entrenada y determina las métricas globales de hostilidad.
    """
    print(f"\n" + "=" * 70)
    print(f"SISTEMA DE AUDITORÍA: INICIANDO ANÁLISIS EN EL ENLACE")
    print(f"URL: {url_enlace}")
    print("=" * 70 + "\n")
    
    # Definición de rutas nativas de la Red Neuronal Convolucional (CNN 1D)
    ruta_modelo_keras = os.path.join("models", "cnn_odio_model.keras")
    ruta_tokenizer_pkl = os.path.join("models", "tokenizer_cnn.pkl")
    
    if not (os.path.exists(ruta_modelo_keras) and os.path.exists(ruta_tokenizer_pkl)):
        print("ERROR: Los artefactos lógicos de la CNN no se encuentran en el directorio.")
        print("Ejecute 'python train_nn.py' para entrenar y sincronizar los pesos de la red.")
        return

    # Carga de la arquitectura profunda de Keras y el mapeo del tokenizador
    modelo_cnn = tf.keras.models.load_model(ruta_modelo_keras)
    tokenizer = joblib.load(ruta_tokenizer_pkl)

    comentarios_crudos = extraer_comentarios_de_link(url_enlace)
    
    if not comentarios_crudos:
        print("ADVERTENCIA: No se recuperaron registros del enlace proporcionado.")
        return

    print(f"REGISTRO: {len(comentarios_crudos)} publicaciones recuperadas.")
    print("PROCESAMIENTO: Evaluando secuencias con la Red Neuronal Convolucional (CNN 1D)...")
    print("-" * 70)

    conteo_odio = 0
    datos_tabla_reporte = [] # Estructura auxiliar por si integras con generar_reporte.py
    
    for idx, comentario in enumerate(comentarios_crudos, 1):
        # 1. Preprocesamiento y limpieza
        texto_limpio = limpiar_texto(comentario)
        
        # 2. Vectorización y Padding para la CNN 1D
        secuencia = tokenizer.texts_to_sequences([texto_limpio])
        X_input = pad_sequences(secuencia, maxlen=MAX_SEQUENCE_LEN, padding='post', truncating='post')
        
        # 3. Inferencia probabilística del modelo profundo
        # Predict devuelve un array bidimensional [[probabilidad]]
        porcentaje_odio = modelo_cnn.predict(X_input, verbose=0)[0][0] * 100
        
        # Umbral estándar de decisión binaria (Threshold = 50%)
        if porcentaje_odio >= 50.0:
            dictamen = "DISCURSO DE ODIO DETECTADO"
            conteo_odio += 1
        else:
            dictamen = "MENSAJE NEUTRO O COLOQUIAL"
            
        # Guardar registro para trazabilidad estructural
        datos_tabla_reporte.append((idx, comentario, porcentaje_odio, dictamen))

        # Despliegue de resultados en consola limpia
        print(f"Publicación #{idx}: \"{comentario}\"")
        if porcentaje_odio >= 50.0:
            print(f"   DICTAMEN: [\033[1;31m{dictamen}\033[0m]") # Texto rojo en terminales compatibles
        else:
            print(f"   DICTAMEN: [\033[1;32m{dictamen}\033[0m]") # Texto verde en terminales compatibles
            
        print(f"   PROBABILIDAD CNN: {porcentaje_odio:.2f}%\n")

    # 4. Cálculo de métricas agregadas macro
    porcentaje_odio_global = (conteo_odio / len(comentarios_crudos)) * 100
    
    print("-" * 70)
    print(f"MÉTRICAS FINALES DE EVALUACIÓN:")
    print(f"   -> Total de elementos procesados: {len(comentarios_crudos)}")
    print(f"   -> Elementos positivos a hostilidad: {conteo_odio}")
    print(f"   -> ÍNDICE DE ODIO GLOBAL CALCULADO: {porcentaje_odio_global:.2f}%")
    
    # Imprimir pre-veredicto rápido en consola según el umbral del 35%
    if porcentaje_odio_global > 35.0:
        print("   -> ESTADO: \033[1;31mALTA VULNERABILIDAD - ATAQUE DE ODIO EN CURSO\033[0m")
    else:
        print("   -> ESTADO: \033[1;32mENTORNO SEGURO - COMUNIDAD SALUDABLE\033[0m")
    print("=" * 70 + "\n")
    
    return comentarios_crudos, conteo_odio, porcentaje_odio_global, datos_tabla_reporte

if __name__ == "__main__":
    if len(sys.argv) > 1:
        enlace_usuario = sys.argv[1]
        analizar_pagina_web(enlace_usuario)
    else:
        print("ERROR: Falta el argumento de entrada.")
        print("Sintaxis requerida: python clasificar_cli.py <URL>")
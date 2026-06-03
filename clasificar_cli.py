# clasificar_cli.py
import os
import sys
import numpy as np
import joblib
from preprocessing import extraer_comentarios_de_link, limpiar_texto, calcular_densidad_insultos
from config import MODELO_PKL, VECTORIZADOR_PKL

def analizar_pagina_web(url_enlace):
    """
    Extrae las publicaciones de una URL, procesa las cadenas a traves de 
    la arquitectura entrenada y determina las metricas globales de hostilidad.
    """
    print(f"\n" + "=" * 70)
    print(f"SISTEMA DE AUDITORIA: INICIANDO ANALISIS EN EL ENLACE")
    print(f"URL: {url_enlace}")
    print("=" * 70 + "\n")
    
    if not (os.path.exists(MODELO_PKL) and os.path.exists(VECTORIZADOR_PKL)):
        print("ERROR: Los artefactos logicos del modelo no se encuentran en el directorio.")
        print("Ejecute 'python train_nn.py' para sincronizar los pesos de la red.")
        return

    modelo_red = joblib.load(MODELO_PKL)
    vectorizer = joblib.load(VECTORIZADOR_PKL)

    comentarios_crudos = extraer_comentarios_de_link(url_enlace)
    
    if not comentarios_crudos:
        print("ADVERTENCIA: No se recuperaron registros del enlace proporcionado.")
        return

    print(f"REGISTRO: {len(comentarios_crudos)} publicaciones recuperadas.")
    print("PROCESAMIENTO: Evaluando secuencias con el Perceptron Multicapa...")
    print("-" * 70)

    conteo_odio = 0
    
    for idx, comentario in enumerate(comentarios_crudos, 1):
        texto_limpio = limpiar_texto(comentario)
        _, densidad = calcular_densidad_insultos(texto_limpio)
        
        vector_texto = vectorizer.transform([texto_limpio]).toarray()
        X_input = np.hstack((vector_texto, [[densidad]]))
        
        prediccion_clase = modelo_red.predict(X_input)[0]
        probabilidades = modelo_red.predict_proba(X_input)[0]
        porcentaje_odio = probabilidades[1] * 100

        print(f"Publicacion #{idx}: \"{comentario}\"")
        if prediccion_clase == 1:
            print(f"   DICTAMEN: [DISCURSO DE ODIO DETECTADO]")
            conteo_odio += 1
        else:
            print(f"   DICTAMEN: [MENSAJE NEUTRO O COLOQUIAL]")
            
        print(f"   PROBABILIDAD: {porcentaje_odio:.2f}%\n")

    porcentaje_odio_global = (conteo_odio / len(comentarios_crudos)) * 100
    
    print("-" * 70)
    print(f"METRICAS FINALES DE EVALUACION:")
    print(f"   -> Total de elementos procesados: {len(comentarios_crudos)}")
    print(f"   -> Elementos positivos a hostilidad: {conteo_odio}")
    print(f"   -> INDICE DE ODIO GLOBAL CALCULADO: {porcentaje_odio_global:.2f}%")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        enlace_usuario = sys.argv[1]
        analizar_pagina_web(enlace_usuario)
    else:
        print("ERROR: Falta el argumento de entrada.")
        print("Sintaxis requerida: python clasificar_cli.py <URL>")
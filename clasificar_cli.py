# clasificar_cli.py
import os
import sys
import numpy as np
import joblib
from preprocessing import extraer_comentarios_de_link, limpiar_texto, calcular_densidad_insultos
from config import MODELO_PKL, VECTORIZADOR_PKL

def analizar_pagina_web(url_enlace):
    """
    Recibe un enlace de una red social, extrae sus publicaciones,
    las procesa a través de la red neuronal y calcula el índice de odio global.
    """
    print(f"\n=================================================================")
    print(f"🕵️‍♂️ INICIANDO ANÁLISIS DE ODIO EN EL ENLACE:")
    print(f"🔗 {url_enlace}")
    print(f"=================================================================\n")
    
    # 1. Verificar que los modelos entrenados existan
    if not (os.path.exists(MODELO_PKL) and os.path.exists(VECTORIZADOR_PKL)):
        print("❌ Error: No se detectan los modelos de la red neuronal.")
        print("Ejecuta primero 'python train_nn.py' para entrenar el cerebro del sistema.")
        return

    # 2. Cargar los artefactos lógicos guardados
    modelo_red = joblib.load(MODELO_PKL)
    vectorizer = joblib.load(VECTORIZADOR_PKL)

    # 3. Extraer comentarios de la URL (Módulo de extracción simulado)
    comentarios_crudos = extraer_comentarios_de_link(url_enlace)
    
    if not comentarios_crudos:
        print("⚠️ No se pudieron recuperar comentarios o publicaciones de este enlace.")
        return

    print(f"📥 Se han recuperado {len(comentarios_crudos)} publicaciones del tablón web.\n")
    print("🧠 Procesando y evaluando con el Perceptrón Multicapa...")
    print("-" * 65)

    conteo_odio = 0
    
    # Evaluar publicación por publicación
    for idx, comentario in enumerate(comentarios_crudos, 1):
        # Preprocesamiento obligatorio
        texto_limpio = limpiar_texto(comentario)
        _, densidad = calcular_densidad_insultos(texto_limpio)
        
        # Extracción de características semánticas (TF-IDF)
        vector_texto = vectorizer.transform([texto_limpio]).toarray()
        
        # Fusión híbrida de características (Texto + Léxico)
        X_input = np.hstack((vector_texto, [[densidad]]))
        
        # Predicción de la Red Neuronal (Clase y Probabilidad)
        prediccion_clase = modelo_red.predict(X_input)[0]
        # predict_proba nos devuelve la probabilidad de pertenecer a [Clase 0, Clase 1]
        probabilidades = modelo_red.predict_proba(X_input)[0]
        porcentaje_odio = probabilidades[1] * 100

        # Mostrar desglose individual en la consola
        print(f"📝 Publicación #{idx}: \"{comentario}\"")
        if prediccion_clase == 1:
            print(f"   🔴 CLASIFICACIÓN: [DISCURSO DE ODIO DETECTADO]")
            conteo_odio += 1
        else:
            print(f"   🟢 CLASIFICACIÓN: [MENSAJE NEUTRO O COLOQUIAL]")
            
        print(f"   📊 Probabilidad de Odio: {porcentaje_odio:.2f}%\n")

    # 4. Cálculo de Métricas Globales del Tablón Web
    porcentaje_odio_global = (conteo_odio / len(comentarios_crudos)) * 100
    
    print("-" * 65)
    print(f"📊 REPORTE DE RESULTADOS GLOBAL PARA EL TABLÓN WEB:")
    print(f"   -> Total de comentarios analizados: {len(comentarios_crudos)}")
    print(f"   -> Mensajes con violencia/odio dirigidos: {conteo_odio}")
    print(f"   -> ÍNDICE DE ODIO GLOBAL DEL SITIO: {porcentaje_odio_global:.2f}%")
    print(f"=================================================================\n")

if __name__ == "__main__":
    # Permite pasar la URL directo por la terminal (CLI)
    if len(sys.argv) > 1:
        enlace_usuario = sys.argv[1]
        analizar_pagina_web(enlace_usuario)
    else:
        print("❌ Uso incorrecto en terminal.")
        print("Ejemplo de ejecución: python clasificar_cli.py 'http://misitio.com/debate_politica'")
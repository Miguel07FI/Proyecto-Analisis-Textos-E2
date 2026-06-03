# main.py
import os
import sys
import joblib
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Importaciones locales de la arquitectura
from config import YOUTUBE_API_KEY
from preprocessing import extraer_comentarios_de_link, limpiar_texto
from generar_reporte import crear_reporte_pdf  # <--- IMPORTACIÓN NUEVA

MODEL_PATH = "models/cnn_odio_model.keras"
TOKENIZER_PATH = "models/tokenizer_cnn.pkl"

def mostrar_bienvenida():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 75)
    print("      🏛️  FACULTAD DE INGENIERÍA - UNAM  🏛️")
    print("   SISTEMA DE AUDITORÍA BASADO EN APRENDIZAJE PROFUNDO (DEEP LEARNING)")
    print("=" * 75)
    print(" Arquitectura Avanzada: Word Embeddings + Red Convolucional 1D (CNN)")
    print(" Propósito: Detección semántica de hostilidad sin falsos positivos léxicos.")
    print("=" * 75)

def inicializar_sistema():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(TOKENIZER_PATH):
        print("\n❌ [ERROR CRÍTICO]: No se encontraron los archivos de Deep Learning en 'models/'.")
        print("💡 Por favor, ejecuta primero: 'python train_nn.py' para forjar la CNN.")
        sys.exit(1)
    return tf.keras.models.load_model(MODEL_PATH), joblib.load(TOKENIZER_PATH)

def obtener_comentarios_simulados():
    print("\n⚙️  [MODO PRUEBA]: Cargando banco de datos simulados local (0 créditos API)...")
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
    print("\n🟢 [SISTEMA]: Red Convolucional Profunda y Tokenizador cargados en memoria.")
    
    print("\n[?] Seleccione el modo de ejecución para el análisis:")
    print("  [1] MODO PRUEBA (Utiliza comentarios simulados locales - NO GASTA API)")
    print("  [2] MODO PRODUCCIÓN (Se conecta en vivo a la API de YouTube Real)")
    
    opcion = input("\nSelección (1 o 2) ➔ ").strip()
    
    if opcion == "1":
        comentarios_reales = obtener_comentarios_simulados()
        objetivo_texto = "Simulador de Entorno Web Local"
    elif opcion == "2":
        if YOUTUBE_API_KEY == "AIzaSyAlSvJpd7QpETzNQLaj-dOAdq3YUyDyrW8" or YOUTUBE_API_KEY == "":
            print("\n❌ [ERROR]: Configura tu API Key real en 'config.py'.")
            return
        print("\n📬 Ingrese la URL completa del video de YouTube:")
        link_usuario = input("🔗 URL ➔ ").strip()
        if not link_usuario: return
        comentarios_reales = extraer_comentarios_de_link(link_usuario)
        objetivo_texto = link_usuario
    else:
        return

    total_comentarios = len(comentarios_reales)
    if total_comentarios == 0: return

    print("\n" + "=" * 75)
    print(f"🕵️‍♂️ INICIANDO AUDITORÍA CON RED CONVOLUCIONAL DE TEXTO")
    print(f"🎯 Objetivo: {objetivo_texto}")
    print("=" * 75)

    conteo_odio = 0
    datos_para_reporte = []  # <--- CONTENEDOR NUEVO PARA EL PDF

    for i, comentario in enumerate(comentarios_reales, 1):
        comentario_limpio = limpiar_texto(comentario)
        secuencia = tokenizer.texts_to_sequences([comentario_limpio])
        pad_individual = pad_sequences(secuencia, maxlen=100, padding='post', truncating='post')
        
        probabilidad_odio = float(model.predict(pad_individual, verbose=0)[0][0]) * 100
        es_odio = probabilidad_odio >= 50.0

        comentario_corto = comentario.replace("\n", " ")[:110] + "..." if len(comentario) > 110 else comentario.replace("\n", " ")

        if es_odio:
            conteo_odio += 1
            dictamen = "DISCURSO DE ODIO"
            print(f"📝 Publicación #{i}: \"{comentario_corto}\"\n   🔴 CLASIFICACIÓN: [{dictamen}] (📊 {probabilidad_odio:.2f}%)\n")
        else:
            dictamen = "NEUTRO / COLOQUIAL"
            print(f"📝 Publicación #{i}: \"{comentario_corto}\"\n   🟢 CLASIFICACIÓN: [{dictamen}] (📊 {probabilidad_odio:.2f}%)\n")
            
        # Guardar la tupla con los resultados estructurados para pasárselos al PDF
        datos_para_reporte.append((i, comentario, probabilidad_odio, dictamen))

    indice_odio_global = (conteo_odio / total_comentarios) * 100
    print("-" * 75)
    print("📊 REPORTE DE RESULTADOS GLOBAL PARA EL TABLÓN WEB:")
    print(f"   -> Total de comentarios analizados: {total_comentarios}")
    print(f"   -> Mensajes con violencia/odio dirigidos: {conteo_odio}")
    print(f"   -> ÍNDICE DE ODIO GLOBAL DEL SITIO: {indice_odio_global:.2f}%")
    print("=" * 75)
    
    # 🚀 DISPARO AUTOMÁTICO COMPILADOR DEL REPORTE PDF
    print("\n🖨️  Compilando reporte ejecutivo en PDF...")
    crear_reporte_pdf(
        url_video=objetivo_texto,
        total_comentarios=total_comentarios,
        total_odio=conteo_odio,
        indice_global=indice_odio_global,
        datos_tabla=datos_para_reporte
    )
    print("=" * 75 + "\n")

if __name__ == "__main__":
    main()
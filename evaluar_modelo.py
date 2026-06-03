# evaluar_modelo.py
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
from config import GRAPH_DIR, DATA_DIR

print("\n" + "=" * 70)
print("SISTEMA DE EVALUACION: EXTRACTOR DE METRICAS DE APRENDIZAJE PROFUNDO (CNN 1D)")
print("=" * 70)

MODEL_PATH = os.path.join("models", "cnn_odio_model.keras")
X_EVAL_PATH = os.path.join(DATA_DIR, "X_eval.npy")
Y_EVAL_PATH = os.path.join(DATA_DIR, "y_eval.npy")
HISTORIAL_PATH = os.path.join(GRAPH_DIR, "historial_perdida.npy")

if not (os.path.exists(MODEL_PATH) and os.path.exists(X_EVAL_PATH) and os.path.exists(Y_EVAL_PATH)):
    print("ERROR: No se detectan los artefactos logicos o los conjuntos de validacion.")
    print("Ejecute 'python train_nn.py' para entrenar la arquitectura convolucional.")
    exit()

print("\n[1/4] Cargando el modelo serializado y los tensores de validacion ciega...")
model = tf.keras.models.load_model(MODEL_PATH)
X_eval = np.load(X_EVAL_PATH)
y_real = np.load(Y_EVAL_PATH)

print("[2/4] Calculando inferencias probabilisticas sobre el conjunto de control (20%)...")
y_prob = model.predict(X_eval, verbose=0)
# Binarizacion mediante umbral estandar de decision (Threshold = 0.5)
y_pred = (y_prob >= 0.5).astype(int).flatten()

print("\n" + "-" * 30 + " REPORT DE CLASIFICACION " + "-" * 30)
print(classification_report(y_real, y_pred, target_names=["No Odio", "Discurso de Odio"]))
print("-" * 85 + "\n")

print("[3/4] Generando matriz de confusion estadistica...")
matriz = confusion_matrix(y_real, y_pred)

plt.figure(figsize=(7, 5))
sns.heatmap(matriz, annot=True, fmt='d', cmap='Blues',
            xticklabels=['No Odio', 'Odio'],
            yticklabels=['No Odio', 'Odio'],
            annot_kws={"size": 14, "weight": "bold"})

plt.title('Matriz de Confusión - Red Convolucional (CNN 1D)', fontsize=12, pad=15, weight='bold')
plt.xlabel('Predicción del Modelo (Deep Learning)', fontsize=10, labelpad=10)
plt.ylabel('Clase Real (Validación Humana)', fontsize=10, labelpad=10)
plt.tight_layout()

ruta_matriz = os.path.join(GRAPH_DIR, "matriz_confusion.png")
plt.savefig(ruta_matriz, dpi=300)
plt.close()
print(f"REGISTRO: Grafica exportada a '{ruta_matriz}'")

print("[4/4] Trazando la curva de perdida por optimizacion de gradiente...")
if os.path.exists(HISTORIAL_PATH):
    historial_perdida = np.load(HISTORIAL_PATH)

    plt.figure(figsize=(7, 4.5))
    plt.plot(range(1, len(historial_perdida) + 1), historial_perdida, 
             marker='o', linestyle='-', color='#e74c3c', linewidth=2, label='Pérdida (Loss)')

    plt.title('Curva de Aprendizaje - Entropía Cruzada Binaria (Adam)', fontsize=12, pad=15, weight='bold')
    plt.xlabel('Épocas de Entrenamiento (Epochs)', fontsize=10)
    plt.ylabel('Loss (Binary Crossentropy)', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=10)
    plt.tight_layout()

    ruta_curva = os.path.join(GRAPH_DIR, "curva_perdida.png")
    plt.savefig(ruta_curva, dpi=300)
    plt.close()
    print(f"REGISTRO: Grafica exportada a '{ruta_curva}'")
else:
    print("ADVERTENCIA: No se encontro el historico de perdida en el directorio.")

print("\nPROCESO TERMINADO: Elementos graficos actualizados en la carpeta 'outputs/'.")
print("=" * 70 + "\n")
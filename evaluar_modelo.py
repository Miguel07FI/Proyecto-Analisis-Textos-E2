# evaluar_modelo.py
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
from config import GRAPH_DIR, DATA_DIR

print("\n" + "="*75)
print("[CLI] EXTRACTOR DE MÉTRICAS: EVALUACIÓN DE ARQUITECTURA DEEP LEARNING (CNN 1D)")
print("="*75)

# 1. Rutas y carga de artefactos nativos de Keras
MODEL_PATH = "models/cnn_odio_model.keras"
if not (os.path.exists(MODEL_PATH) and os.path.exists(os.path.join(DATA_DIR, "X_eval.npy"))):
    print("❌ [ERROR]: No se encontraron los modelos entrenados o los datos de validación.")
    print("💡 Por favor, ejecuta primero: 'python train_nn.py'")
    exit()

print("\n[1/4] Levantando el modelo convolucional y los conjuntos de validación ciega...")
model = tf.keras.models.load_model(MODEL_PATH)
X_eval = np.load(os.path.join(DATA_DIR, "X_eval.npy"))
y_real = np.load(os.path.join(DATA_DIR, "y_eval.npy"))

# 2. Inferencia y binarización matemática
print("[2/4] Ejecutando predicciones probabilísticas sobre el entorno ciego (20%)...")
# La CNN devuelve probabilidades continuas entre 0.0 y 1.0
y_prob = model.predict(X_eval, verbose=0)
# Aplicamos el umbral estándar del 50% para la clasificación dura
y_pred = (y_prob >= 0.5).astype(int).flatten()

print("\n================ REPORT DE CLASIFICACIÓN DE ODIO REAL ================")
print(classification_report(y_real, y_pred, target_names=["No Odio", "Discurso de Odio"]))
print("=================================================================\n")

# 3. Generación y renderizado de la Matriz de Confusión
print("[3/4] Forjando la nueva Matriz de Confusión estadística...")
matriz = confusion_matrix(y_real, y_pred)

plt.figure(figsize=(7, 5))
sns.heatmap(matriz, annot=True, fmt='d', cmap='Blues',
            xticklabels=['No Odio', 'Odio'],
            yticklabels=['No Odio', 'Odio'],
            annot_kws={"size": 14, "weight": "bold"})

plt.title('Matriz de Confusión - Red Convolucional (CNN 1D)', fontsize=14, pad=15, weight='bold')
plt.xlabel('Predicción del Modelo de Deep Learning', fontsize=12, labelpad=10)
plt.ylabel('Clase Real (Validación Humana)', fontsize=12, labelpad=10)
plt.tight_layout()

ruta_matriz = os.path.join(GRAPH_DIR, "matriz_confusion.png")
plt.savefig(ruta_matriz, dpi=300)
plt.close()
print(f"   📊 Matriz guardada con éxito en: {ruta_matriz}")

# 4. Generación de la Curva de Aprendizaje (Loss Termodinámica)
print("[4/4] Trazando la Curva de Pérdida Iterativa (Loss Curve)...")
historial_perdida = np.load(os.path.join(GRAPH_DIR, "historial_perdida.npy"))

plt.figure(figsize=(7, 4.5))
plt.plot(range(1, len(historial_perdida) + 1), historial_perdida, 
         marker='o', linestyle='-', color='#e74c3c', linewidth=2, label='Pérdida (Loss)')

plt.title('Curva de Aprendizaje - Optimización del Gradiente (Adam)', fontsize=13, pad=15, weight='bold')
plt.xlabel('Épocas de Entrenamiento (Epochs)', fontsize=11)
plt.ylabel('Entropía Cruzada Binaria (Binary Crossentropy)', fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=11)
plt.tight_layout()

ruta_curva = os.path.join(GRAPH_DIR, "curva_perdida.png")
plt.savefig(ruta_curva, dpi=300)
plt.close()
print(f"   📈 Curva de pérdida guardada con éxito en: {ruta_curva}")

print("\n✅ ¡Métricas visuales actualizadas perfectamente en la carpeta 'outputs/'!")
print("="*75 + "\n")
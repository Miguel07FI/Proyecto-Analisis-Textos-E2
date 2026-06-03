# train_nn.py
import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout, Input
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from preprocessing import limpiar_texto
from config import DATASET_CSV, MODELO_PKL, VECTORIZADOR_PKL, GRAPH_DIR, DATA_DIR

print("\n" + "="*75)
print("🚀 [DEEP LEARNING] ENTRENANDO RED NEURONAL CONVOLUCIONAL (CNN 1D) PARA TEXTO")
print("="*75)

# 1. Cargar el corpus de 12,000 registros
df = pd.read_csv(DATASET_CSV, encoding="utf-8")
df['texto_limpio'] = df['texto'].apply(limpiar_texto)

# 2. Tokenización y Secuenciación (En lugar de TF-IDF tradicional)
max_palabras = 5000  # Tamaño del vocabulario máximo
max_longitud = 100   # Longitud máxima de cada comentario de internet

tokenizer = Tokenizer(num_words=max_palabras, oov_token="<OOV>")
tokenizer.fit_on_texts(df['texto_limpio'])

# Convertir textos a secuencias numéricas y aplicar padding
secuencias = tokenizer.texts_to_sequences(df['texto_limpio'])
X_pad = pad_sequences(secuencias, maxlen=max_longitud, padding='post', truncating='post')
y = df['label'].values

# Split científico de datos (80% entrenamiento, 20% validación ciega)
X_train, X_test, y_train, y_test = train_test_split(X_pad, y, test_size=0.20, random_state=42)

# Guardar datos de validación para scripts independientes
np.save(os.path.join(DATA_DIR, "X_eval.npy"), X_test)
np.save(os.path.join(DATA_DIR, "y_eval.npy"), y_test)

# 3. Construcción de la Arquitectura Deep Learning CNN-1D
print("\n🧠 Configurando topología convolucional profunda...")
model = Sequential([
    Input(shape=(max_longitud,)),
    # Capa de Embedding: Crea vectores densos de 64 dimensiones por palabra
    Embedding(input_dim=max_palabras, output_dim=64),
    
    # Capa Convolucional: 128 filtros para extraer patrones de frases (trigramas)
    Conv1D(filters=128, kernel_size=3, activation='relu'),
    GlobalMaxPooling1D(), # Extrae la señal más fuerte del mapa de características
    
    # Capas Densas de Clasificación con control de Overfitting (Dropout)
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(32, activation='relu'),
    Dropout(0.2),
    Dense(1, activation='sigmoid') # Salida binaria de probabilidad [0, 1]
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

# 4. Entrenamiento con Parada Temprana Inteligente
print("\n🏋️‍♂️ Iniciando el entrenamiento del modelo de Deep Learning...")
early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

historial = model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=64,
    validation_split=0.1,
    callbacks=[early_stop],
    verbose=1
)

print("\n💾 Guardando artefactos de Deep Learning de alta fidelidad...")
# TensorFlow maneja sus propios formatos, guardamos el modelo nativo y el tokenizador por separado
model.save(os.path.join(os.path.dirname(MODELO_PKL), "cnn_odio_model.keras"))
joblib.dump(tokenizer, os.path.join(os.path.dirname(VECTORIZADOR_PKL), "tokenizer_cnn.pkl"))

# Guardar historial de pérdida para las gráficas
np.save(os.path.join(GRAPH_DIR, "historial_perdida.npy"), np.array(historial.history['loss']))
print("✅ ¡Red Neuronal Convolucional (CNN) guardada con éxito en 'models/'!")
print("="*75 + "\n")
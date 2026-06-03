# train_nn.py
import os
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout, Input
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from preprocessing import limpiar_texto
from config import (
    DATASET_CSV, MODELO_PKL, VECTORIZADOR_PKL, GRAPH_DIR, DATA_DIR,
    MAX_WORDS_VOCAB, MAX_SEQUENCE_LEN, CNN_FILTERS, EMBEDDING_DIM, BATCH_SIZE, EPOCHS
)

print("\n" + "=" * 70)
print("SISTEMA DE ENTRENAMIENTO: ARQUITECTURA DE RED NEURONAL CONVOLUCIONAL (CNN 1D)")
print("=" * 70)

# 1. Carga y normalizacion del corpus
df = pd.read_csv(DATASET_CSV, encoding="utf-8")
df['texto_limpio'] = df['texto'].apply(limpiar_texto)

# 2. Tokenizacion y estructuracion de secuencias vectoriales
tokenizer = Tokenizer(num_words=MAX_WORDS_VOCAB, oov_token="<OOV>")
tokenizer.fit_on_texts(df['texto_limpio'])

secuencias = tokenizer.texts_to_sequences(df['texto_limpio'])
X_pad = pad_sequences(secuencias, maxlen=MAX_SEQUENCE_LEN, padding='post', truncating='post')
y = df['label'].values

# Division estadistica de conjuntos de datos (80% entrenamiento, 20% validacion externa)
X_train, X_test, y_train, y_test = train_test_split(X_pad, y, test_size=0.20, random_state=42)

# Persistencia de tensores para procesos independientes de evaluacion
np.save(os.path.join(DATA_DIR, "X_eval.npy"), X_test)
np.save(os.path.join(DATA_DIR, "y_eval.npy"), y_test)

# 3. Defincion de la topologia de la Red Neuronal Convolucional
print("\nPROCESO: Configurando topologia estructural profunda...")
model = Sequential([
    Input(shape=(MAX_SEQUENCE_LEN,)),
    # Capa de proyeccion vectorial densa (Word Embeddings)
    Embedding(input_dim=MAX_WORDS_VOCAB, output_dim=EMBEDDING_DIM),
    
    # Capa de extraccion de caracteristicas locales de coocurrencia
    Conv1D(filters=CNN_FILTERS, kernel_size=3, activation='relu'),
    GlobalMaxPooling1D(), 
    
    # Capas densas de clasificacion y regularizacion mediante Dropout
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(32, activation='relu'),
    Dropout(0.2),
    Dense(1, activation='sigmoid') 
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

# 4. Optimizacion de gradiente con criterio de parada temprana (Early Stopping)
print("\nPROCESO: Iniciando el ajuste jerarquico del modelo...")
early_stop = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss', 
    patience=3, 
    restore_best_weights=True
)

historial = model.fit(
    X_train, y_train,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_split=0.1,
    callbacks=[early_stop],
    verbose=1
)

print("\nPROCESO: Serializando artefactos logicos y registros historicos...")
# Exportacion nativa de la arquitectura Keras y del mapeo del tokenizador
ruta_modelo_keras = os.path.join(os.path.dirname(MODELO_PKL), "cnn_odio_model.keras")
ruta_tokenizer_pkl = os.path.join(os.path.dirname(VECTORIZADOR_PKL), "tokenizer_cnn.pkl")
ruta_historial_loss = os.path.join(GRAPH_DIR, "historial_perdida.npy")

model.save(ruta_modelo_keras)
joblib.dump(tokenizer, ruta_tokenizer_pkl)

# Almacenamiento de metricas iterativas para analisis grafico
np.save(ruta_historial_loss, np.array(historial.history['loss']))

print(f"REGISTRO: Modelo convolucional persistido correctamente en '{ruta_modelo_keras}'")
print("=" * 70 + "\n")
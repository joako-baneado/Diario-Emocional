"""
Analizador de Emociones en Audio
--------------------------------

Este módulo analiza archivos de audio para detectar emociones utilizando procesamiento
de señales de audio y aprendizaje automático. Utiliza la biblioteca librosa para
extraer características MFCC (Mel Frequency Cepstral Coefficients) y un modelo
pre-entrenado para clasificar las emociones.

El script:
1. Busca el archivo de audio WAV más reciente en la carpeta de entrada
2. Extrae características MFCC del audio
3. Predice la emoción usando un modelo pre-entrenado
4. Guarda los resultados en un archivo de texto con marca de tiempo

Dependencias:
    - librosa: para procesamiento de audio
    - numpy: para operaciones numéricas
    - joblib: para cargar el modelo pre-entrenado
"""

import librosa
import numpy as np
import os
import joblib
from datetime import datetime

# === Configuración de Rutas y Constantes ===
CARPETA_AUDIO = "audio_inputs"     # Directorio donde se buscarán los archivos WAV
CARPETA_SALIDA = "text_outputs"    # Directorio donde se guardarán los resultados
MODELO_AUDIO = "app/modelo_audio_emocion.pkl"  # Ruta al modelo pre-entrenado de emociones

def extraer_caracteristicas(file_path):
    """
    Extrae características MFCC de un archivo de audio.

    Args:
        file_path (str): Ruta al archivo de audio WAV a analizar

    Returns:
        numpy.ndarray: Vector de 40 características MFCC promediadas sobre el tiempo

    Raises:
        LibrosaError: Si hay un error al cargar o procesar el archivo de audio
    """
    audio, sr = librosa.load(file_path, sr=None)
    mfccs = np.mean(librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40).T, axis=0)
    return mfccs

# === Proceso Principal ===

# Buscar el archivo WAV más reciente
archivos = [f for f in os.listdir(CARPETA_AUDIO) if f.endswith(".wav")]
if not archivos:
    print("No hay archivos de audio.")
    exit()

ultimo_archivo = max(archivos, key=lambda x: os.path.getctime(os.path.join(CARPETA_AUDIO, x)))
ruta_audio = os.path.join(CARPETA_AUDIO, ultimo_archivo)

# Cargar modelo y realizar predicción
modelo = joblib.load(MODELO_AUDIO)
caracteristicas = extraer_caracteristicas(ruta_audio).reshape(1, -1)
emocion = modelo.predict(caracteristicas)[0]
print(f"Emoción detectada por audio: {emocion}")

# Guardar resultados en archivo de texto con timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
archivo_salida = os.path.join(CARPETA_SALIDA, f"audio_emocion_{timestamp}.txt")
with open(archivo_salida, "w", encoding="utf-8") as f:
    f.write(f"Archivo de audio: {ultimo_archivo}\n")
    f.write(f"Emoción detectada (audio): {emocion}\n")

print(f"Resultado guardado en: {archivo_salida}")

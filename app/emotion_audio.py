# audio_emotion_analyzer.py
import librosa
import numpy as np
import os
import joblib  # para cargar el modelo
from datetime import datetime

# === Configuración ===
CARPETA_AUDIO = "audio_inputs"
CARPETA_SALIDA = "text_outputs"
MODELO_AUDIO = "app/modelo_audio_emocion.pkl"  # ajusta si está en otro lado

# === Cargar último archivo .wav ===
archivos = [f for f in os.listdir(CARPETA_AUDIO) if f.endswith(".wav")]
if not archivos:
    print("No hay archivos de audio.")
    exit()

ultimo_archivo = max(archivos, key=lambda x: os.path.getctime(os.path.join(CARPETA_AUDIO, x)))
ruta_audio = os.path.join(CARPETA_AUDIO, ultimo_archivo)

# === Extraer características con librosa ===
def extraer_caracteristicas(file_path):
    audio, sr = librosa.load(file_path, sr=None)
    mfccs = np.mean(librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40).T, axis=0)
    return mfccs

# === Cargar modelo y predecir ===
modelo = joblib.load(MODELO_AUDIO)
caracteristicas = extraer_caracteristicas(ruta_audio).reshape(1, -1)
emocion = modelo.predict(caracteristicas)[0]
print(f"Emoción detectada por audio: {emocion}")

# === Guardar en .txt ===
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
archivo_salida = os.path.join(CARPETA_SALIDA, f"audio_emocion_{timestamp}.txt")
with open(archivo_salida, "w", encoding="utf-8") as f:
    f.write(f"Archivo de audio: {ultimo_archivo}\n")
    f.write(f"Emoción detectada (audio): {emocion}\n")

print(f"Resultado guardado en: {archivo_salida}")

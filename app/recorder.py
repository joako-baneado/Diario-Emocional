# app/grabar_audio.py
import speech_recognition as sr
import os
from datetime import datetime

# Crear carpeta de audios si no existe
CARPETA_AUDIO = "audio_inputs"
os.makedirs(CARPETA_AUDIO, exist_ok=True)

# Timestamp para nombre de archivo
timestamp = datetime.now()
nombre_archivo = timestamp.strftime("grabacion_%Y-%m-%d_%H-%M")
archivo_audio = os.path.join(CARPETA_AUDIO, f"{nombre_archivo}.wav")

# Duración
DURACION_SEGUNDOS = 5

# Grabación
r = sr.Recognizer()
mic = sr.Microphone()

print("Ajustando al ruido ambiente...")
with mic as source:
    r.adjust_for_ambient_noise(source)

print(f"Grabando por {DURACION_SEGUNDOS} segundos...")
with mic as source:
    audio = r.record(source, duration=DURACION_SEGUNDOS)

# Guardar audio
with open(archivo_audio, "wb") as f:
    f.write(audio.get_wav_data())

print(f"Audio guardado como: {archivo_audio}")

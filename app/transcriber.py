# app/transcribir_texto.py
import speech_recognition as sr
import os
from datetime import datetime

# Carpetas
CARPETA_AUDIO = "audio_inputs"
CARPETA_TEXTO = "text_outputs"
os.makedirs(CARPETA_TEXTO, exist_ok=True)

# Buscar el archivo de audio más reciente
archivos = [f for f in os.listdir(CARPETA_AUDIO) if f.endswith(".wav")]
if not archivos:
    print("No se encontraron archivos de audio en", CARPETA_AUDIO)
    exit()

archivo_mas_reciente = max(archivos, key=lambda f: os.path.getctime(os.path.join(CARPETA_AUDIO, f)))
ruta_audio = os.path.join(CARPETA_AUDIO, archivo_mas_reciente)

# Timestamp para encabezado y texto
timestamp = datetime.now()
fecha_hora_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
nombre_txt = os.path.splitext(archivo_mas_reciente)[0] + ".txt"
ruta_texto = os.path.join(CARPETA_TEXTO, nombre_txt)

# Reconocimiento
r = sr.Recognizer()
with sr.AudioFile(ruta_audio) as source:
    audio = r.record(source)

try:
    print("Reconociendo texto desde:", ruta_audio)
    texto = r.recognize_google(audio, language="es-PE")
    print("Texto reconocido:", texto)

    with open(ruta_texto, "w", encoding="utf-8") as f:
        f.write(f"Fecha y hora de transcripción: {fecha_hora_str}\n")
        f.write("Texto reconocido:\n")
        f.write(texto)
    print(f"Texto guardado en: {ruta_texto}")

except sr.UnknownValueError:
    print("No se pudo entender el audio.")
except sr.RequestError as e:
    print(f"Error con Google Speech: {e}")

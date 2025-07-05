import speech_recognition as sr
import os
from datetime import datetime

# Crear carpetas si no existen
CARPETA_AUDIO = "audio_inputs"
CARPETA_TEXTO = "outputs"
os.makedirs(CARPETA_AUDIO, exist_ok=True)
os.makedirs(CARPETA_TEXTO, exist_ok=True)

# Timestamp legible para nombre de archivo
timestamp = datetime.now()
nombre_archivo = timestamp.strftime("grabacion_%Y-%m-%d_%H-%M")
fecha_hora_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")

# Archivos de salida
archivo_audio = os.path.join(CARPETA_AUDIO, f"{nombre_archivo}.wav")
archivo_texto = os.path.join(CARPETA_TEXTO, f"{nombre_archivo}.txt")

# Duración de la grabación
DURACION_SEGUNDOS = 5

# Inicializa micrófono y reconocedor
r = sr.Recognizer()
mic = sr.Microphone()

print("Ajustando al ruido ambiente...")
with mic as source:
    r.adjust_for_ambient_noise(source)

print(f"Grabando por {DURACION_SEGUNDOS} segundos...")
with mic as source:
    audio = r.record(source, duration=DURACION_SEGUNDOS)

# Guardar archivo de audio
with open(archivo_audio, "wb") as f:
    f.write(audio.get_wav_data())
print(f"Audio guardado como '{archivo_audio}'")

# Reconocimiento de voz
try:
    print("Reconociendo...")
    texto = r.recognize_google(audio, language="es-PE")
    print("Texto: ", texto)

    # Guardar texto con encabezado de fecha y hora
    with open(archivo_texto, "w", encoding="utf-8") as f:
        f.write(f"Fecha y hora de grabación: {fecha_hora_str}\n")
        f.write("Texto reconocido:\n")
        f.write(texto)
    print(f"Texto guardado en '{archivo_texto}'")

except sr.UnknownValueError:
    print("No se pudo entender el audio.")
except sr.RequestError as e:
    print(f"Error al comunicarse con Google Speech: {e}")

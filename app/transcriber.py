import speech_recognition as sr
import wave

# Configura duración y nombre del archivo
DURACION_SEGUNDOS = 5
ARCHIVO_SALIDA = "grabacion.wav"

# Inicializa el reconocedor y el micrófono
r = sr.Recognizer()
mic = sr.Microphone()

print("Ajustando al ruido ambiente...")
with mic as source:
    r.adjust_for_ambient_noise(source)

print(f"Grabando por {DURACION_SEGUNDOS} segundos...")
with mic as source:
    audio = r.record(source, duration=DURACION_SEGUNDOS)

# Guarda el audio en WAV
with open(ARCHIVO_SALIDA, "wb") as f:
    f.write(audio.get_wav_data())

print(f"Audio guardado como '{ARCHIVO_SALIDA}'")

# Reconocimiento de voz con Google
try:
    print("Reconociendo...")
    texto = r.recognize_google(audio, language="es-PE")
    print("Texto reconocido:", texto)
except sr.UnknownValueError:
    print("No se pudo entender el audio.")
except sr.RequestError as e:
    print(f"Error al comunicarse con Google Speech: {e}")

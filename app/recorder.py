"""
Módulo de Grabación de Audio para la Aplicación de Diario Emocional

Este módulo maneja la funcionalidad de grabación de audio para la aplicación de diario emocional.
Captura la entrada de audio del micrófono del usuario, la procesa para reducir el ruido ambiente,
y la guarda como un archivo WAV con un nombre basado en timestamp.

Dependencias:
    - speech_recognition: Para captura y procesamiento de audio
    - os: Para operaciones del sistema de archivos
    - datetime: Para generación de timestamps

Uso:
    Este módulo está diseñado para ser ejecutado como un script para grabar entrada de audio
    para posterior transcripción y análisis emocional.

Funcionalidades principales:
    - Ajuste automático al ruido ambiente
    - Grabación de audio con duración configurable
    - Guardado automático con nombres únicos basados en timestamp
    - Formato WAV para máxima compatibilidad
"""

import speech_recognition as sr
import os
from datetime import datetime

# Constantes de Configuración
CARPETA_AUDIO = "audio_inputs"  # Directorio donde se almacenarán los archivos de audio
DURACION_SEGUNDOS = 5  # Duración de la grabación en segundos

# Crear directorio de audio si no existe
# Esto asegura que la ubicación de almacenamiento esté disponible antes de grabar
os.makedirs(CARPETA_AUDIO, exist_ok=True)

# Generar nombre de archivo basado en timestamp
# Formato: grabacion_AAAA-MM-DD_HH-MM.wav
# Esto asegura nombres de archivo únicos y organización cronológica
timestamp = datetime.now()
nombre_archivo = timestamp.strftime("grabacion_%Y-%m-%d_%H-%M")
archivo_audio = os.path.join(CARPETA_AUDIO, f"{nombre_archivo}.wav")

# Inicializar componentes de grabación de audio
# Recognizer: Maneja el procesamiento y reconocimiento de audio
# Microphone: Captura entrada de audio del dispositivo de micrófono predeterminado
r = sr.Recognizer()
mic = sr.Microphone()

# Fase de ajuste al ruido ambiente
# Este paso es crucial para mejorar la calidad de grabación adaptándose al
# nivel de ruido de fondo del entorno actual
print("Ajustando al ruido ambiente...")
with mic as source:
    r.adjust_for_ambient_noise(source)

# Fase de grabación de audio
# Graba por la duración especificada y almacena los datos de audio en memoria
print(f"Grabando por {DURACION_SEGUNDOS} segundos...")
with mic as source:
    audio = r.record(source, duration=DURACION_SEGUNDOS)

# Guardar audio en archivo
# Convierte los datos de audio grabados a formato WAV y los escribe al disco
# El formato WAV se elige por su compatibilidad y preservación de calidad
with open(archivo_audio, "wb") as f:
    f.write(audio.get_wav_data())

print(f"Audio guardado como: {archivo_audio}")

"""
Módulo de Transcripción de Audio para la Aplicación de Diario Emocional

Este módulo maneja la funcionalidad de transcripción de audio a texto para la aplicación 
de diario emocional. Procesa archivos de audio previamente grabados y los convierte a 
texto utilizando el API de Google Speech Recognition.

Dependencias:
    - speech_recognition: Para reconocimiento de voz y transcripción
    - os: Para operaciones del sistema de archivos
    - datetime: Para generación de timestamps

Funcionalidades principales:
    - Búsqueda automática del archivo de audio más reciente
    - Transcripción usando Google Speech Recognition (idioma español-Perú)
    - Guardado del texto transcrito con timestamp
    - Manejo robusto de errores de reconocimiento

Flujo de trabajo:
    1. Busca el archivo de audio más reciente en la carpeta de entrada
    2. Configura el reconocedor de voz
    3. Procesa el archivo de audio
    4. Transcribe usando Google Speech API
    5. Guarda el resultado en un archivo de texto con timestamp

Formatos de archivo:
    - Entrada: Archivos WAV en directorio 'audio_inputs'
    - Salida: Archivos TXT en directorio 'text_outputs'
"""

import speech_recognition as sr
import os
from datetime import datetime

# Configuración de directorios
CARPETA_AUDIO = "audio_inputs"    # Directorio de archivos de audio de entrada
CARPETA_TEXTO = "text_outputs"    # Directorio de archivos de texto de salida

# Crear directorio de salida si no existe
# Garantiza que el directorio de destino esté disponible para guardar transcripciones
os.makedirs(CARPETA_TEXTO, exist_ok=True)

# Búsqueda del archivo de audio más reciente
# Filtra solo archivos WAV y selecciona el más reciente basado en fecha de creación
archivos = [f for f in os.listdir(CARPETA_AUDIO) if f.endswith(".wav")]

# Verificar que existan archivos de audio para procesar
if not archivos:
    print("No se encontraron archivos de audio en", CARPETA_AUDIO)
    exit()

# Seleccionar el archivo más reciente usando timestamp de creación
archivo_mas_reciente = max(archivos, key=lambda f: os.path.getctime(os.path.join(CARPETA_AUDIO, f)))
ruta_audio = os.path.join(CARPETA_AUDIO, archivo_mas_reciente)

# Configuración de archivo de salida
# Genera timestamp para el encabezado del archivo de transcripción
timestamp = datetime.now()
fecha_hora_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")

# Crear nombre del archivo de texto basado en el archivo de audio
# Mantiene el mismo nombre base pero cambia la extensión a .txt
nombre_txt = os.path.splitext(archivo_mas_reciente)[0] + ".txt"
ruta_texto = os.path.join(CARPETA_TEXTO, nombre_txt)

# Proceso de reconocimiento de voz
# Inicializar el reconocedor de speech recognition
r = sr.Recognizer()

# Cargar y procesar el archivo de audio
# AudioFile context manager maneja automáticamente la apertura y cierre del archivo
with sr.AudioFile(ruta_audio) as source:
    audio = r.record(source)

# Intentar transcripción con manejo de errores
try:
    print("Reconociendo texto desde:", ruta_audio)
    
    # Utilizar Google Speech Recognition API con configuración para español de Perú
    # El parámetro language="es-PE" optimiza el reconocimiento para dialectos peruanos
    texto = r.recognize_google(audio, language="es-PE")
    print("Texto reconocido:", texto)

    # Guardar transcripción en archivo de texto
    # Incluye timestamp y formato estructurado para fácil lectura
    with open(ruta_texto, "w", encoding="utf-8") as f:
        f.write(f"Fecha y hora de transcripción: {fecha_hora_str}\n")
        f.write("Texto reconocido:\n")
        f.write(texto)
    
    print(f"Texto guardado en: {ruta_texto}")

# Manejo de errores específicos del reconocimiento de voz
except sr.UnknownValueError:
    print("No se pudo entender el audio.")
    print("Posibles causas: audio poco claro, ruido excesivo, o idioma no reconocido.")
    
except sr.RequestError as e:
    print(f"Error con Google Speech: {e}")
    print("Verifica tu conexión a internet y la disponibilidad del servicio.")

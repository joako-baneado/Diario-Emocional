"""
Módulo de Interfaz Gráfica para la Aplicación de Diario Emocional

Este módulo contiene la interfaz gráfica principal de la aplicación de diario emocional.
Proporciona una interfaz moderna y amigable que integra grabación de voz, análisis de
emociones, generación de respuestas empáticas y visualización en tiempo real de la cámara.

Dependencias principales:
    - tkinter: Framework de GUI base
    - customtkinter: Framework de GUI moderno con temas
    - PIL (Pillow): Procesamiento de imágenes
    - cv2 (OpenCV): Captura y procesamiento de video
    - threading: Manejo de hilos para grabación asíncrona
    - speech_recognition: Reconocimiento de voz
    - transformers: Modelos de IA para clasificación de emociones
    - empathy: Módulo personalizado para respuestas empáticas

Funcionalidades principales:
    - Interfaz gráfica moderna con tema oscuro
    - Grabación de voz en tiempo real
    - Procesamiento de texto escrito
    - Análisis automático de emociones
    - Generación de respuestas empáticas
    - Visualización de cámara en vivo
    - Chat log con timestamps
    - Guardado automático de conversaciones
"""

import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import threading
import time
import speech_recognition as sr
from empathy import EmpatheticResponseGenerator
from transformers import pipeline
import datetime

# ==================== CONFIGURACIONES INICIALES ====================

# Configurar tema visual de la aplicación
# Modo oscuro para una experiencia visual moderna y cómoda
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Inicializar clasificador de emociones usando modelo preentrenado
# Utiliza DistilRoBERTa optimizado para clasificación de emociones en inglés
emotion_classifier = pipeline(
    "text-classification", 
    model="j-hartmann/emotion-english-distilroberta-base", 
    return_all_scores=False
)

# ==================== CLASE PRINCIPAL ====================

class EmotionalDiaryApp:
    """
    Aplicación Principal del Diario Emocional
    
    Esta clase gestiona toda la interfaz gráfica y lógica de la aplicación.
    Integra múltiples componentes para crear una experiencia completa de
    diario emocional con análisis en tiempo real.
    
    Atributos principales:
        window: Ventana principal de CustomTkinter
        recognizer: Reconocedor de voz de speech_recognition
        is_recording: Estado de grabación de voz
        empathetic_generator: Generador de respuestas empáticas
        camera_on: Estado de la cámara
        cap: Capturador de video de OpenCV
        
    Componentes de interfaz:
        - main_frame: Marco principal de la aplicación
        - camera_label: Label para mostrar video de cámara
        - record_button: Botón de grabación de voz
        - send_button: Botón para enviar texto
        - chat_display: Área de visualización del chat
        - input_box: Campo de entrada de texto
    """
    
    def __init__(self):
        """
        Inicializa la aplicación del diario emocional.
        
        Configura todos los componentes necesarios:
        - Ventana principal con CustomTkinter
        - Reconocedor de voz
        - Generador de respuestas empáticas
        - Captura de cámara
        - Interfaz de usuario
        - Bucle de actualización de cámara
        """
        # Configurar ventana principal
        self.window = ctk.CTk()
        self.window.title("Diario Emocional")
        self.window.geometry("1000x800")

        # Inicializar componentes de reconocimiento de voz
        self.recognizer = sr.Recognizer()
        self.is_recording = False
        
        # Inicializar generador de respuestas empáticas
        self.empathetic_generator = EmpatheticResponseGenerator()

        # Configurar captura de cámara
        self.camera_on = True
        self.cap = cv2.VideoCapture(0)

        # Construir interfaz de usuario y iniciar actualización de cámara
        self.build_ui()
        self.update_camera()

    def build_ui(self):
        """
        Construye la interfaz de usuario completa.
        
        Crea y organiza todos los elementos de la interfaz:
        - Marco principal
        - Visualización de cámara
        - Botones de control (grabar voz, enviar texto)
        - Área de chat con scroll
        - Campo de entrada de texto
        
        Layout:
        - Cámara en la parte superior
        - Botones de control en el centro
        - Chat log expandible
        - Campo de entrada en la parte inferior
        """
        # Crear marco principal que contiene todos los elementos
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Visualización de cámara en tiempo real
        self.camera_label = ctk.CTkLabel(self.main_frame, text="Cámara")
        self.camera_label.pack(pady=5)

        # Marco para botones de control organizados horizontalmente
        button_frame = ctk.CTkFrame(self.main_frame)
        button_frame.pack(pady=10)

        # Botón de grabación de voz con toggle de estado
        self.record_button = ctk.CTkButton(button_frame, text="🎙️ Grabar voz", command=self.toggle_recording)
        self.record_button.grid(row=0, column=0, padx=10)

        # Botón para procesar entrada de texto manual
        self.send_button = ctk.CTkButton(button_frame, text="✉️ Enviar texto", command=self.process_text_input)
        self.send_button.grid(row=0, column=1, padx=10)

        # Área de visualización del chat con scroll automático
        self.chat_display = ctk.CTkTextbox(self.main_frame, height=300, wrap="word")
        self.chat_display.pack(padx=10, pady=10, fill="both", expand=False)
        self.chat_display.insert("1.0", "[Diario iniciado]\n")
        self.chat_display.configure(state="disabled")

        # Campo de entrada de texto con placeholder y binding de Enter
        self.input_box = ctk.CTkEntry(self.main_frame, placeholder_text="Escribe tu mensaje aquí...", width=800)
        self.input_box.pack(padx=10, pady=(0,10))
        self.input_box.bind("<Return>", lambda event: self.process_text_input())

    def toggle_recording(self):
        """
        Alterna el estado de grabación de voz entre activo e inactivo.
        
        Maneja el inicio y detención de la grabación de voz:
        - Si no está grabando: inicia grabación en hilo separado
        - Si está grabando: detiene la grabación
        - Actualiza la interfaz del botón según el estado
        
        Threading:
        La grabación se ejecuta en un hilo separado para evitar bloquear
        la interfaz de usuario durante el proceso de escucha.
        """
        if not self.is_recording:
            # Iniciar grabación
            self.is_recording = True
            self.record_button.configure(text="⏹️ Detener")
            # Ejecutar grabación en hilo separado para no bloquear UI
            threading.Thread(target=self.record_audio).start()
        else:
            # Detener grabación
            self.is_recording = False
            self.record_button.configure(text="🎙️ Grabar voz")

    def record_audio(self):
        """
        Graba audio de forma continua mientras el estado de grabación esté activo.
        
        Proceso de grabación:
        1. Utiliza el micrófono como fuente de audio
        2. Escucha continuamente con timeout de 1 segundo
        3. Reconoce texto usando Google Speech Recognition (español)
        4. Añade el texto reconocido al chat
        5. Genera respuesta empática automáticamente
        
        Manejo de errores:
        - Timeouts de escucha se ignoran para continuar grabación
        - Errores de reconocimiento se ignoran silenciosamente
        - La grabación continúa hasta que se desactive el estado
        
        Configuración:
        - Idioma: Español de España (es-ES)
        - Timeout: 1 segundo para evitar bloqueos largos
        """
        with sr.Microphone() as source:
            while self.is_recording:
                try:
                    # Escuchar audio con timeout corto para responsividad
                    audio = self.recognizer.listen(source, timeout=1)
                    # Reconocer texto en español
                    text = self.recognizer.recognize_google(audio, language="es-ES")
                    # Mostrar texto reconocido en chat
                    self.append_chat("Tú", text)
                    # Generar respuesta empática automática
                    self.generate_response(text)
                except:
                    # Continuar grabación ignorando errores temporales
                    continue

    def process_text_input(self):
        """
        Procesa la entrada de texto manual del usuario.
        
        Flujo de procesamiento:
        1. Obtiene el texto del campo de entrada
        2. Limpia el campo de entrada
        3. Muestra el texto en el chat como mensaje del usuario
        4. Genera respuesta empática basada en el texto
        
        Validación:
        - Solo procesa si hay texto no vacío
        - Limpia automáticamente el campo después del envío
        """
        text = self.input_box.get()
        if text:
            # Limpiar campo de entrada
            self.input_box.delete(0, tk.END)
            # Mostrar mensaje del usuario en chat
            self.append_chat("Tú", text)
            # Procesar y generar respuesta empática
            self.generate_response(text)

    def generate_response(self, text):
        """
        Genera una respuesta empática basada en el análisis emocional del texto.
        
        Proceso de generación:
        1. Analiza el texto usando el clasificador de emociones DistilRoBERTa
        2. Obtiene la emoción principal detectada
        3. Utiliza el generador empático para crear respuesta personalizada
        4. Muestra la respuesta en el chat incluyendo la emoción detectada
        
        Manejo de errores:
        - Captura excepciones durante el análisis o generación
        - Muestra mensaje de error informativo en caso de fallo
        - Continúa funcionando aunque falle una respuesta específica
        
        Datos mostrados:
        - Respuesta empática generada
        - Emoción detectada (para logging y análisis)
        """
        try:
            # Clasificar emoción usando modelo DistilRoBERTa
            emotion = emotion_classifier(text)[0]['label']
            # Generar respuesta empática personalizada
            response = self.empathetic_generator.generate_empathetic_response(text, emotion)
            # Mostrar respuesta del bot con emoción detectada
            self.append_chat("Bot", response, emotion)
        except Exception as e:
            # Mostrar error en caso de fallo en el procesamiento
            self.append_chat("Bot", f"Error generando respuesta empática: {e}")

    def append_chat(self, speaker, message, emotion="Input"):
        """
        Añade un nuevo mensaje al área de chat con timestamp y logging automático.
        
        Funcionalidades:
        1. Genera timestamp actual en formato [HH:MM]
        2. Formatea el mensaje con speaker y contenido
        3. Añade el mensaje al área de chat (habilitando/deshabilitando edición)
        4. Hace scroll automático para mostrar el último mensaje
        5. Guarda la entrada en el archivo de log
        
        Parámetros:
            speaker (str): Identificador del emisor ("Tú" o "Bot")
            message (str): Contenido del mensaje
            emotion (str): Emoción detectada (solo para respuestas del bot)
        
        Logging:
        - Mensajes del usuario: [timestamp] speaker: message
        - Respuestas del bot: [timestamp] speaker: message / emotion
        - Archivos guardados en ./logs/diario_emocional_log.txt
        """
        # Generar timestamp para el mensaje
        timestamp = datetime.datetime.now().strftime("[%H:%M]")
        
        # Habilitar edición temporal del área de chat
        self.chat_display.configure(state="normal")
        # Insertar nuevo mensaje al final
        self.chat_display.insert(tk.END, f"{timestamp} {speaker}: {message}\n")
        # Deshabilitar edición para prevenir modificaciones del usuario
        self.chat_display.configure(state="disabled")
        # Scroll automático al último mensaje
        self.chat_display.see(tk.END)
        
        # Guardar en log con formato apropiado
        if (emotion != "Input"):
            # Guardar respuesta del bot con emoción detectada
            self.save_log(f"{timestamp} {speaker}: {message} / {emotion}\n")
        else:
            # Guardar mensaje del usuario sin emoción
            self.save_log(f"{timestamp} {speaker}: {message}\n")

    def save_log(self, entry):
        """
        Guarda una entrada en el archivo de log del diario emocional.
        
        Características del logging:
        - Archivo: ./logs/diario_emocional_log.txt
        - Codificación: UTF-8 para soporte de caracteres especiales
        - Modo: Append (añadir) para preservar historial completo
        - Formato: Mismo formato que se muestra en la interfaz
        
        Parámetros:
            entry (str): Entrada formateada lista para escribir al archivo
        
        Estructura del log:
        - Cada línea representa una interacción
        - Incluye timestamps, speakers y contenido
        - Las respuestas del bot incluyen emoción detectada
        """
        # Escribir entrada al archivo de log con codificación UTF-8
        with open("./logs/diario_emocional_log.txt", "a", encoding="utf-8") as f:
            f.write(entry)

    def update_camera(self):
        """
        Actualiza la visualización de la cámara en tiempo real.
        
        Proceso de actualización:
        1. Verifica que la cámara esté habilitada
        2. Captura frame actual de la cámara
        3. Redimensiona frame a 640x360 para interfaz
        4. Convierte color de BGR (OpenCV) a RGB (PIL)
        5. Convierte a formato compatible con Tkinter
        6. Actualiza el label de la cámara
        7. Programa siguiente actualización después de 30ms
        
        Características:
        - Actualización a ~33 FPS (cada 30ms)
        - Redimensionamiento automático para UI
        - Conversión de formato de color automática
        - Bucle continuo mientras la aplicación esté activa
        
        Manejo de errores:
        - Si no hay frame disponible, mantiene imagen anterior
        - Continúa el bucle de actualización independientemente
        """
        if self.camera_on:
            # Capturar frame de la cámara
            ret, frame = self.cap.read()
            if ret:
                # Redimensionar frame para interfaz (640x360)
                frame = cv2.resize(frame, (640, 360))
                # Convertir de BGR (OpenCV) a RGB (PIL/Tkinter)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Convertir a formato PIL
                img = Image.fromarray(frame)
                # Convertir a formato Tkinter
                imgtk = ImageTk.PhotoImage(image=img)
                # Actualizar label de cámara
                self.camera_label.configure(image=imgtk, text="")
                # Mantener referencia para evitar garbage collection
                self.camera_label.imgtk = imgtk
        
        # Programar siguiente actualización en 30ms
        self.window.after(30, self.update_camera)

    def run(self):
        """
        Inicia la aplicación y maneja el ciclo principal.
        
        Funciones principales:
        1. Inicia el bucle principal de Tkinter (mainloop)
        2. Gestiona la limpieza de recursos al cerrar:
           - Libera la captura de cámara
           - Cierra ventanas de OpenCV
        
        Limpieza de recursos:
        - self.cap.release(): Libera el dispositivo de cámara
        - cv2.destroyAllWindows(): Cierra ventanas de OpenCV
        
        Esta función bloquea hasta que se cierra la aplicación.
        """
        # Iniciar bucle principal de la aplicación
        self.window.mainloop()
        # Limpiar recursos al cerrar la aplicación
        self.cap.release()
        cv2.destroyAllWindows()

# ==================== PUNTO DE ENTRADA PRINCIPAL ====================

if __name__ == "__main__":
    """
    Punto de entrada principal de la aplicación.
    
    Crea una instancia de EmotionalDiaryApp y la ejecuta.
    Este bloque solo se ejecuta cuando el archivo se ejecuta directamente,
    no cuando se importa como módulo.
    
    Uso:
        python interface.py
    
    La aplicación se iniciará con:
    - Interfaz gráfica moderna
    - Cámara activada
    - Reconocimiento de voz listo
    - Sistema de respuestas empáticas activo
    """
    app = EmotionalDiaryApp()
    app.run()

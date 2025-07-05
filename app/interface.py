# Menú simple por consola o flujo automatizado
import tkinter as tk
import customtkinter as ctk
import speech_recognition as sr
import threading
import time
from PIL import Image, ImageTk

class EmotionalDiaryApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Diario Emocional")
        self.window.geometry("800x600")
        
        # Configurar tema oscuro
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variables de estado
        self.is_recording = False
        self.recognizer = sr.Recognizer()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Diario Emocional",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Botón de grabación
        self.record_button = ctk.CTkButton(
            main_frame,
            text="Iniciar Grabación",
            command=self.toggle_recording,
            width=200,
            height=40
        )
        self.record_button.pack(pady=20)
        
        # Frame para los textos
        text_frame = ctk.CTkFrame(main_frame)
        text_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Área de texto transcrito
        transcription_label = ctk.CTkLabel(
            text_frame,
            text="Tu mensaje:",
            font=ctk.CTkFont(size=16)
        )
        transcription_label.pack(anchor="w", padx=10, pady=5)
        
        self.transcription_text = ctk.CTkTextbox(
            text_frame,
            width=700,
            height=100
        )
        self.transcription_text.pack(padx=10, pady=5)
        
        # Área de respuesta empática
        response_label = ctk.CTkLabel(
            text_frame,
            text="Respuesta empática:",
            font=ctk.CTkFont(size=16)
        )
        response_label.pack(anchor="w", padx=10, pady=5)
        
        self.response_text = ctk.CTkTextbox(
            text_frame,
            width=700,
            height=150
        )
        self.response_text.pack(padx=10, pady=5)
        
    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def start_recording(self):
        self.is_recording = True
        self.record_button.configure(text="Detener Grabación", fg_color="red")
        self.recording_thread = threading.Thread(target=self.record_audio)
        self.recording_thread.start()
        
    def stop_recording(self):
        self.is_recording = False
        self.record_button.configure(text="Iniciar Grabación", fg_color=["#3B8ED0", "#1F6AA5"])
        
    def record_audio(self):
        with sr.Microphone() as source:
            while self.is_recording:
                try:
                    audio = self.recognizer.listen(source, timeout=1)
                    text = self.recognizer.recognize_google(audio, language="es-ES")
                    self.update_transcription(text)
                    self.generate_empathetic_response(text)
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    self.show_error("Error de conexión con el servicio de reconocimiento de voz")
                    break
                    
    def update_transcription(self, text):
        self.transcription_text.delete("1.0", tk.END)
        self.transcription_text.insert("1.0", text)
        
    def generate_empathetic_response(self, text):
        # Aquí puedes integrar tu lógica de generación de respuestas empáticas
        # Por ahora, usaremos respuestas simples basadas en palabras clave
        response = self.get_simple_empathetic_response(text)
        self.response_text.delete("1.0", tk.END)
        self.response_text.insert("1.0", response)
        
    def get_simple_empathetic_response(self, text):
        text = text.lower()
        if any(word in text for word in ["triste", "mal", "dolor"]):
            return "Entiendo que estés pasando por un momento difícil. Es normal sentirse así, y está bien expresar tus emociones. ¿Quieres hablar más sobre lo que te preocupa?"
        elif any(word in text for word in ["feliz", "alegre", "contento"]):
            return "¡Me alegro mucho de que te sientas así! Es maravilloso experimentar esos momentos de felicidad. ¿Qué te ha hecho sentir tan bien?"
        elif any(word in text for word in ["preocupado", "ansioso", "miedo"]):
            return "Es comprensible sentir preocupación. Respira profundo y recuerda que estoy aquí para escucharte. ¿Quieres compartir qué te está causando esta ansiedad?"
        else:
            return "Te escucho y estoy aquí para apoyarte. ¿Quieres contarme más sobre cómo te sientes?"
            
    def show_error(self, message):
        tk.messagebox.showerror("Error", message)
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = EmotionalDiaryApp()
    app.run()
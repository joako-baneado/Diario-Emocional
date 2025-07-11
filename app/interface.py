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

# Configuraciones iniciales
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Clasificador de emociones con modelo de HuggingFace
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=False)

# Clase principal
class EmotionalDiaryApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Diario Emocional")
        self.window.geometry("1000x800")

        self.recognizer = sr.Recognizer()
        self.is_recording = False
        self.empathetic_generator = EmpatheticResponseGenerator()

        self.camera_on = True
        self.cap = cv2.VideoCapture(0)

        self.build_ui()
        self.update_camera()

    def build_ui(self):
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.camera_label = ctk.CTkLabel(self.main_frame, text="Cámara")
        self.camera_label.pack(pady=5)

        # Botones de control
        button_frame = ctk.CTkFrame(self.main_frame)
        button_frame.pack(pady=10)

        self.record_button = ctk.CTkButton(button_frame, text="🎙️ Grabar voz", command=self.toggle_recording)
        self.record_button.grid(row=0, column=0, padx=10)

        self.send_button = ctk.CTkButton(button_frame, text="✉️ Enviar texto", command=self.process_text_input)
        self.send_button.grid(row=0, column=1, padx=10)

        # Chat log
        self.chat_display = ctk.CTkTextbox(self.main_frame, height=300, wrap="word")
        self.chat_display.pack(padx=10, pady=10, fill="both", expand=False)
        self.chat_display.insert("1.0", "[Diario iniciado]\n")
        self.chat_display.configure(state="disabled")

        # Entrada de texto
        self.input_box = ctk.CTkEntry(self.main_frame, placeholder_text="Escribe tu mensaje aquí...", width=800)
        self.input_box.pack(padx=10, pady=(0,10))

    def toggle_recording(self):
        if not self.is_recording:
            self.is_recording = True
            self.record_button.configure(text="⏹️ Detener")
            threading.Thread(target=self.record_audio).start()
        else:
            self.is_recording = False
            self.record_button.configure(text="🎙️ Grabar voz")

    def record_audio(self):
        with sr.Microphone() as source:
            while self.is_recording:
                try:
                    audio = self.recognizer.listen(source, timeout=1)
                    text = self.recognizer.recognize_google(audio, language="es-ES")
                    self.append_chat("Tú", text)
                    self.generate_response(text)
                except:
                    continue

    def process_text_input(self):
        text = self.input_box.get()
        if text:
            self.input_box.delete(0, tk.END)
            self.append_chat("Tú", text)
            self.generate_response(text)

    def generate_response(self, text):
        try:
            emotion = emotion_classifier(text)[0]['label']
            response = self.empathetic_generator.generate_empathetic_response(text, emotion)
            self.append_chat("Bot", response, emotion)
        except Exception as e:
            self.append_chat("Bot", f"Error generando respuesta empática: {e}")

    def append_chat(self, speaker, message, emotion = "Input"):
        timestamp = datetime.datetime.now().strftime("[%H:%M]")
        self.chat_display.configure(state="normal")
        self.chat_display.insert(tk.END, f"{timestamp} {speaker}: {message}\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see(tk.END)
        if (emotion != "Input"):
            # Guardar en el log
            self.save_log(f"{timestamp} {speaker}: {message} / {emotion}\n")
        else:
            self.save_log(f"{timestamp} {speaker}: {message}\n")

    def save_log(self, entry):
        with open("./logs/diario_emocional_log.txt", "a", encoding="utf-8") as f:
            f.write(entry)

    def update_camera(self):
        if self.camera_on:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (640, 360))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.camera_label.configure(image=imgtk, text="")
                self.camera_label.imgtk = imgtk
        self.window.after(30, self.update_camera)

    def run(self):
        self.window.mainloop()
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = EmotionalDiaryApp()
    app.run()

# app/gui_app.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import customtkinter as ctk
import threading
import queue
import os
from datetime import datetime

# Import our modules
from .recorder import AudioRecorder
from .transcriber import AudioTranscriber
from .empathy import EmpatheticResponseGenerator


class EmotionalDiaryGUI:
    def __init__(self):
        # Initialize components
        self.recorder = AudioRecorder()
        self.transcriber = AudioTranscriber()
        self.empathy_generator = EmpatheticResponseGenerator()
        
        # GUI State
        self.is_recording = False
        self.message_queue = queue.Queue()
        
        # Setup main window
        self.setup_window()
        self.setup_ui()
        
        # Start message queue processing
        self.check_message_queue()
    
    def setup_window(self):
        """Setup the main window with modern styling"""
        # Configure customtkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Diario Emocional - Emotional Diary")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="Diario Emocional",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(20, 10), sticky="ew")
        
        # Recording controls frame
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        controls_frame.grid_columnconfigure(0, weight=1)
        
        # Recording button
        self.record_button = ctk.CTkButton(
            controls_frame,
            text="🎤 Iniciar Grabación",
            command=self.toggle_recording,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            width=200
        )
        self.record_button.grid(row=0, column=0, pady=15)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            controls_frame,
            text="Listo para grabar",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=1, column=0, pady=(0, 15))
        
        # Content frame
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Transcription section
        transcription_label = ctk.CTkLabel(
            content_frame,
            text="Texto Transcrito:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        transcription_label.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 5))
        
        self.transcription_text = ctk.CTkTextbox(
            content_frame,
            height=120,
            font=ctk.CTkFont(size=12)
        )
        self.transcription_text.grid(row=0, column=0, sticky="nsew", padx=15, pady=(35, 10))
        
        # Empathetic response section
        response_label = ctk.CTkLabel(
            content_frame,
            text="Respuesta Empática:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        response_label.grid(row=1, column=0, sticky="w", padx=15, pady=(5, 5))
        
        self.response_text = ctk.CTkTextbox(
            content_frame,
            height=120,
            font=ctk.CTkFont(size=12)
        )
        self.response_text.grid(row=1, column=0, sticky="nsew", padx=15, pady=(25, 15))
        
        # Footer
        footer_frame = ctk.CTkFrame(main_frame)
        footer_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        
        # Clear button
        clear_button = ctk.CTkButton(
            footer_frame,
            text="Limpiar",
            command=self.clear_all,
            width=100,
            height=30
        )
        clear_button.grid(row=0, column=0, padx=15, pady=10)
        
        # Save button
        save_button = ctk.CTkButton(
            footer_frame,
            text="Guardar",
            command=self.save_session,
            width=100,
            height=30
        )
        save_button.grid(row=0, column=1, padx=15, pady=10)
    
    def toggle_recording(self):
        """Toggle recording state"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start recording audio"""
        try:
            success = self.recorder.start_recording()
            if success:
                self.is_recording = True
                self.record_button.configure(text="⏹️ Detener Grabación")
                self.status_label.configure(text="Grabando... Haz clic para detener")
                self.clear_all()
            else:
                messagebox.showerror("Error", "No se pudo iniciar la grabación")
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar grabación: {str(e)}")
    
    def stop_recording(self):
        """Stop recording and process audio"""
        try:
            self.is_recording = False
            self.record_button.configure(text="🎤 Iniciar Grabación")
            self.status_label.configure(text="Procesando audio...")
            
            # Process in separate thread to avoid blocking UI
            thread = threading.Thread(target=self.process_audio)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al detener grabación: {str(e)}")
            self.reset_ui()
    
    def process_audio(self):
        """Process recorded audio (transcription and empathy generation)"""
        try:
            # Stop recording and get audio file
            audio_file = self.recorder.stop_recording()
            
            if not audio_file:
                self.message_queue.put(("error", "No se pudo obtener el archivo de audio"))
                return
            
            # Transcribe audio
            self.message_queue.put(("status", "Transcribiendo audio..."))
            transcribed_text = self.transcriber.transcribe_audio_file(audio_file)
            
            if not transcribed_text:
                self.message_queue.put(("error", "No se pudo transcribir el audio"))
                return
            
            # Generate empathetic response
            self.message_queue.put(("status", "Generando respuesta empática..."))
            empathetic_response = self.empathy_generator.generate_empathetic_response(
                transcribed_text, 
                "neutral"  # Default emotion, could be enhanced with emotion detection
            )
            
            # Update UI
            self.message_queue.put(("transcription", transcribed_text))
            self.message_queue.put(("response", empathetic_response))
            self.message_queue.put(("status", "Procesamiento completado"))
            
        except Exception as e:
            self.message_queue.put(("error", f"Error procesando audio: {str(e)}"))
    
    def check_message_queue(self):
        """Check for messages from background threads"""
        try:
            while True:
                message_type, message = self.message_queue.get_nowait()
                
                if message_type == "status":
                    self.status_label.configure(text=message)
                elif message_type == "transcription":
                    self.transcription_text.delete("1.0", tk.END)
                    self.transcription_text.insert("1.0", message)
                elif message_type == "response":
                    self.response_text.delete("1.0", tk.END)
                    self.response_text.insert("1.0", message)
                elif message_type == "error":
                    self.status_label.configure(text="Error - Listo para grabar")
                    messagebox.showerror("Error", message)
                    self.reset_ui()
                    
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_message_queue)
    
    def reset_ui(self):
        """Reset UI to initial state"""
        self.is_recording = False
        self.record_button.configure(text="🎤 Iniciar Grabación")
        self.status_label.configure(text="Listo para grabar")
    
    def clear_all(self):
        """Clear all text areas"""
        self.transcription_text.delete("1.0", tk.END)
        self.response_text.delete("1.0", tk.END)
    
    def save_session(self):
        """Save current session to file"""
        try:
            transcription = self.transcription_text.get("1.0", tk.END).strip()
            response = self.response_text.get("1.0", tk.END).strip()
            
            if not transcription and not response:
                messagebox.showwarning("Advertencia", "No hay contenido para guardar")
                return
            
            # Create session folder if it doesn't exist
            session_folder = "sessions"
            os.makedirs(session_folder, exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now()
            filename = timestamp.strftime("session_%Y-%m-%d_%H-%M-%S.txt")
            filepath = os.path.join(session_folder, filename)
            
            # Save session
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"Sesión del Diario Emocional\n")
                f.write(f"Fecha: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                
                f.write("TRANSCRIPCIÓN:\n")
                f.write(transcription + "\n\n")
                
                f.write("RESPUESTA EMPÁTICA:\n")
                f.write(response + "\n")
            
            messagebox.showinfo("Éxito", f"Sesión guardada en: {filepath}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando sesión: {str(e)}")
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


def main():
    """Main function to run the application"""
    try:
        app = EmotionalDiaryGUI()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
# app/simple_gui.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, font
import threading
import queue
import os
from datetime import datetime

# Import our modules
from .empathy import EmpatheticResponseGenerator


class SimpleEmotionalDiaryGUI:
    def __init__(self):
        # Initialize components
        self.empathy_generator = EmpatheticResponseGenerator()
        
        # GUI State
        self.message_queue = queue.Queue()
        
        # Setup main window
        self.setup_window()
        self.setup_ui()
        
        # Start message queue processing
        self.check_message_queue()
    
    def setup_window(self):
        """Setup the main window"""
        # Create main window
        self.root = tk.Tk()
        self.root.title("Diario Emocional - Emotional Diary")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Configure colors and fonts
        self.bg_color = "#2b2b2b"
        self.fg_color = "#ffffff"
        self.button_color = "#4472c4"
        self.text_bg = "#3c3c3c"
        
        self.root.configure(bg=self.bg_color)
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Configure fonts
        self.title_font = font.Font(family="Arial", size=24, weight="bold")
        self.header_font = font.Font(family="Arial", size=14, weight="bold")
        self.button_font = font.Font(family="Arial", size=12, weight="bold")
        self.text_font = font.Font(family="Arial", size=10)
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Diario Emocional",
            font=self.title_font,
            bg=self.bg_color,
            fg=self.fg_color
        )
        title_label.grid(row=0, column=0, pady=(0, 20), sticky="ew")
        
        # Controls frame
        controls_frame = tk.Frame(main_frame, bg=self.bg_color)
        controls_frame.grid(row=1, column=0, sticky="ew", pady=10)
        controls_frame.grid_columnconfigure(0, weight=1)
        
        # Since we don't have audio recording, we'll simulate it with text input
        input_label = tk.Label(
            controls_frame,
            text="Escribe cómo te sientes:",
            font=self.header_font,
            bg=self.bg_color,
            fg=self.fg_color
        )
        input_label.grid(row=0, column=0, pady=(0, 10), sticky="w")
        
        # Input text area
        self.input_text = scrolledtext.ScrolledText(
            controls_frame,
            height=4,
            font=self.text_font,
            bg=self.text_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            wrap=tk.WORD
        )
        self.input_text.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        # Process button
        self.process_button = tk.Button(
            controls_frame,
            text="💭 Procesar Emociones",
            command=self.process_emotions,
            font=self.button_font,
            bg=self.button_color,
            fg=self.fg_color,
            activebackground="#3a5998",
            activeforeground=self.fg_color,
            relief="flat",
            height=2,
            cursor="hand2"
        )
        self.process_button.grid(row=2, column=0, pady=10)
        
        # Status label
        self.status_label = tk.Label(
            controls_frame,
            text="Listo para procesar emociones",
            font=self.text_font,
            bg=self.bg_color,
            fg="#cccccc"
        )
        self.status_label.grid(row=3, column=0, pady=(0, 10))
        
        # Content frame
        content_frame = tk.Frame(main_frame, bg=self.bg_color)
        content_frame.grid(row=2, column=0, sticky="nsew", pady=10)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Transcription section
        transcription_label = tk.Label(
            content_frame,
            text="Tu texto:",
            font=self.header_font,
            bg=self.bg_color,
            fg=self.fg_color
        )
        transcription_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        # Frame for transcription text
        trans_frame = tk.Frame(content_frame, bg=self.bg_color)
        trans_frame.grid(row=0, column=0, sticky="nsew", pady=(25, 5))
        trans_frame.grid_rowconfigure(0, weight=1)
        trans_frame.grid_columnconfigure(0, weight=1)
        
        self.transcription_text = scrolledtext.ScrolledText(
            trans_frame,
            font=self.text_font,
            bg=self.text_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.transcription_text.grid(row=0, column=0, sticky="nsew")
        
        # Empathetic response section
        response_label = tk.Label(
            content_frame,
            text="Respuesta Empática:",
            font=self.header_font,
            bg=self.bg_color,
            fg=self.fg_color
        )
        response_label.grid(row=1, column=0, sticky="w", pady=(15, 5))
        
        # Frame for response text
        resp_frame = tk.Frame(content_frame, bg=self.bg_color)
        resp_frame.grid(row=1, column=0, sticky="nsew", pady=(40, 0))
        resp_frame.grid_rowconfigure(0, weight=1)
        resp_frame.grid_columnconfigure(0, weight=1)
        
        self.response_text = scrolledtext.ScrolledText(
            resp_frame,
            font=self.text_font,
            bg=self.text_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.response_text.grid(row=0, column=0, sticky="nsew")
        
        # Footer
        footer_frame = tk.Frame(main_frame, bg=self.bg_color)
        footer_frame.grid(row=3, column=0, sticky="ew", pady=(20, 0))
        
        # Clear button
        clear_button = tk.Button(
            footer_frame,
            text="🗑️ Limpiar",
            command=self.clear_all,
            font=self.text_font,
            bg="#666666",
            fg=self.fg_color,
            activebackground="#555555",
            relief="flat",
            height=1,
            cursor="hand2"
        )
        clear_button.grid(row=0, column=0, padx=(0, 10), pady=5)
        
        # Save button
        save_button = tk.Button(
            footer_frame,
            text="💾 Guardar",
            command=self.save_session,
            font=self.text_font,
            bg="#2d7d32",
            fg=self.fg_color,
            activebackground="#1b5e20",
            relief="flat",
            height=1,
            cursor="hand2"
        )
        save_button.grid(row=0, column=1, padx=(0, 10), pady=5)
        
        # Example button
        example_button = tk.Button(
            footer_frame,
            text="📝 Ejemplo",
            command=self.load_example,
            font=self.text_font,
            bg="#f57c00",
            fg=self.fg_color,
            activebackground="#ef6c00",
            relief="flat",
            height=1,
            cursor="hand2"
        )
        example_button.grid(row=0, column=2, padx=(0, 10), pady=5)
    
    def process_emotions(self):
        """Process the input text and generate empathetic response"""
        input_text = self.input_text.get("1.0", tk.END).strip()
        
        if not input_text:
            messagebox.showwarning("Advertencia", "Por favor, escribe algo antes de procesar.")
            return
        
        # Update status
        self.status_label.configure(text="Procesando emociones...")
        self.process_button.configure(state=tk.DISABLED)
        
        # Process in separate thread to avoid blocking UI
        thread = threading.Thread(target=self.process_text_thread, args=(input_text,))
        thread.daemon = True
        thread.start()
    
    def process_text_thread(self, text):
        """Process text in a separate thread"""
        try:
            # Generate empathetic response
            empathetic_response = self.empathy_generator.generate_empathetic_response(
                text, 
                "neutral"  # Default emotion, could be enhanced with emotion detection
            )
            
            # Update UI
            self.message_queue.put(("transcription", text))
            self.message_queue.put(("response", empathetic_response))
            self.message_queue.put(("status", "Procesamiento completado"))
            
        except Exception as e:
            self.message_queue.put(("error", f"Error procesando texto: {str(e)}"))
    
    def check_message_queue(self):
        """Check for messages from background threads"""
        try:
            while True:
                message_type, message = self.message_queue.get_nowait()
                
                if message_type == "status":
                    self.status_label.configure(text=message)
                    self.process_button.configure(state=tk.NORMAL)
                elif message_type == "transcription":
                    self.transcription_text.configure(state=tk.NORMAL)
                    self.transcription_text.delete("1.0", tk.END)
                    self.transcription_text.insert("1.0", message)
                    self.transcription_text.configure(state=tk.DISABLED)
                elif message_type == "response":
                    self.response_text.configure(state=tk.NORMAL)
                    self.response_text.delete("1.0", tk.END)
                    self.response_text.insert("1.0", message)
                    self.response_text.configure(state=tk.DISABLED)
                elif message_type == "error":
                    self.status_label.configure(text="Error - Listo para procesar")
                    self.process_button.configure(state=tk.NORMAL)
                    messagebox.showerror("Error", message)
                    
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_message_queue)
    
    def clear_all(self):
        """Clear all text areas"""
        self.input_text.delete("1.0", tk.END)
        self.transcription_text.configure(state=tk.NORMAL)
        self.transcription_text.delete("1.0", tk.END)
        self.transcription_text.configure(state=tk.DISABLED)
        self.response_text.configure(state=tk.NORMAL)
        self.response_text.delete("1.0", tk.END)
        self.response_text.configure(state=tk.DISABLED)
        self.status_label.configure(text="Listo para procesar emociones")
    
    def load_example(self):
        """Load an example text"""
        example_text = "Hoy me siento muy frustrado en el trabajo. Mi jefe me dio una tarea con un plazo imposible y no sé cómo voy a terminarla a tiempo. Me siento abrumado y preocupado."
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert("1.0", example_text)
        messagebox.showinfo("Ejemplo", "Se ha cargado un ejemplo. Haz clic en 'Procesar Emociones' para ver la respuesta empática.")
    
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
                
                f.write("TEXTO ORIGINAL:\n")
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
        app = SimpleEmotionalDiaryGUI()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
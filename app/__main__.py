"""
Diario Emocional - Punto de entrada principal
-------------------------------------------

Este módulo es el punto de entrada principal de la aplicación Diario Emocional.
Permite al usuario elegir entre:
1. Usar el diario emocional (grabar y escribir nuevas entradas)
2. Ver el historial del diario (visualizar entradas pasadas)

Uso:
    Ejecutar desde línea de comandos:
        python -m app

La aplicación mostrará un menú para seleccionar la funcionalidad deseada.
"""

import customtkinter as ctk
# Importaciones lazy - solo cuando se necesiten
# from interface import EmotionalDiaryApp
# from diary_viewer import DiaryViewerApp

class MainMenu:
    """
    Menú principal para seleccionar la funcionalidad del diario.
    """
    
    def __init__(self):
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Crear ventana principal
        self.window = ctk.CTk()
        self.window.title("Diario Emocional - Menú Principal")
        self.window.geometry("850x700")
        
        # Centrar ventana
        #self.center_window()
        
        # Construir interfaz
        self.build_ui()
    
    def center_window(self):
        """
        Centra la ventana en la pantalla.
        """
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def build_ui(self):
        """
        Construye la interfaz del menú principal.
        """
        # Marco principal
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame, 
            text="📖 Diario Emocional", 
            font=ctk.CTkFont(size=36, weight="bold")
        )
        title_label.pack(pady=(40, 15))
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            main_frame, 
            text="Registra y analiza tus emociones",
            font=ctk.CTkFont(size=18)
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Botones principales
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=30)
        
        # Botón para nuevo diario
        new_diary_btn = ctk.CTkButton(
            button_frame,
            text="✍️ Escribir en mi Diario",
            command=self.open_diary,
            font=ctk.CTkFont(size=18, weight="bold"),
            height=60,
            width=400
        )
        new_diary_btn.pack(pady=15)
        
        # Descripción del botón de nuevo diario
        new_diary_desc = ctk.CTkLabel(
            button_frame,
            text="Graba voz o escribe texto para registrar\ntus emociones en tiempo real",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        new_diary_desc.pack(pady=(0, 25))
        
        # Botón para ver historial
        view_diary_btn = ctk.CTkButton(
            button_frame,
            text="📚 Ver mi Historial",
            command=self.open_viewer,
            font=ctk.CTkFont(size=18, weight="bold"),
            height=60,
            width=400
        )
        view_diary_btn.pack(pady=15)
        
        # Descripción del botón de historial
        view_diary_desc = ctk.CTkLabel(
            button_frame,
            text="Revisa tus entradas pasadas, busca por emociones\ny visualiza estadísticas de tu estado emocional",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        view_diary_desc.pack(pady=(0, 25))
        
        # Botón de salir
        exit_btn = ctk.CTkButton(
            button_frame,
            text="❌ Salir",
            command=self.window.quit,
            font=ctk.CTkFont(size=16),
            height=45,
            width=180,
            fg_color="transparent",
            border_width=2
        )
        exit_btn.pack(pady=(15, 0))
    
    def open_diary(self):
        """
        Abre la aplicación principal del diario emocional.
        """
        # Importación lazy - solo cuando se necesita
        from interface import EmotionalDiaryApp
        
        self.window.withdraw()  # Ocultar en lugar de destruir
        app = EmotionalDiaryApp(return_to_menu=self.show_menu)
        app.run()
    
    def open_viewer(self):
        """
        Abre el visor del historial del diario.
        """
        # Importación lazy - solo cuando se necesita
        from diary_viewer import DiaryViewerApp
        
        self.window.withdraw()  # Ocultar en lugar de destruir
        viewer = DiaryViewerApp(return_to_menu=self.show_menu)
        viewer.run()
    
    def show_menu(self):
        """
        Muestra el menú principal.
        """
        self.window.deiconify()  # Mostrar ventana nuevamente
    
    def run(self):
        """
        Inicia el menú principal.
        """
        self.window.mainloop()

if __name__ == "__main__":
    menu = MainMenu()
    menu.run()

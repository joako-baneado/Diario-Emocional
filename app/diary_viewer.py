"""
Visor del Diario Emocional
-------------------------

Este módulo proporciona una interfaz gráfica para visualizar y navegar
por el historial del diario emocional del usuario. Permite ver todas
las entradas pasadas, filtrar por emociones, buscar contenido específico
y obtener estadísticas de las emociones registradas.

Funcionalidades principales:
    - Visualización cronológica de entradas del diario
    - Filtrado por tipo de emoción
    - Búsqueda de texto en las entradas
    - Estadísticas de emociones
    - Navegación por fechas
    - Exportar entradas seleccionadas

Dependencias:
    - customtkinter: Framework de GUI moderno
    - tkinter: Widgets adicionales
    - matplotlib: Gráficos de estadísticas
    - datetime: Manejo de fechas
    - re: Expresiones regulares para parsing
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime
import re
from collections import Counter, defaultdict
import os

# Importaciones lazy - se cargarán solo cuando se necesiten
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def load_matplotlib():
    """
    Carga matplotlib de forma lazy cuando se necesite.
    """
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    return plt, FigureCanvasTkAgg

class DiaryViewerApp:
    """
    Aplicación para visualizar el historial del diario emocional.
    
    Esta clase gestiona la interfaz gráfica para ver, filtrar y analizar
    las entradas del diario emocional previamente guardadas.
    """
    
    def __init__(self, return_to_menu=None):
        """
        Inicializa la aplicación del visor del diario.
        
        Args:
            return_to_menu: Función callback para regresar al menú principal
        """
        # Guardar callback para navegación
        self.return_to_menu = return_to_menu
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configurar ventana principal
        self.window = ctk.CTk()
        self.window.title("Visor del Diario Emocional")
        self.window.geometry("1200x800")
        
        # Configurar protocolo de cierre
        if self.return_to_menu:
            self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Variables de control
        self.diary_entries = []
        self.filtered_entries = []
        self.log_file_path = "./logs/diario_emocional_log.txt"
        
        # Colores para emociones
        self.emotion_colors = {
            'joy': '#4CAF50',      # Verde
            'sadness': '#2196F3',  # Azul
            'anger': '#F44336',    # Rojo
            'fear': '#9C27B0',     # Púrpura
            'surprise': '#FF9800', # Naranja
            'neutral': '#9E9E9E',  # Gris
            'disgust': '#795548',  # Marrón
            'Input': '#607D8B'     # Azul gris
        }
        
        # Construir interfaz
        self.build_ui()
        self.load_diary_entries()
        self.update_display()
        
    def build_ui(self):
        """
        Construye la interfaz de usuario del visor.
        """
        # Marco principal
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Panel superior - Controles
        control_frame = ctk.CTkFrame(main_frame)
        control_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        # Título
        title_label = ctk.CTkLabel(control_frame, text="📖 Mi Diario Emocional", 
                                 font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=10)
        
        # Controles de filtrado y búsqueda
        filter_frame = ctk.CTkFrame(control_frame)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        # Búsqueda de texto
        search_label = ctk.CTkLabel(filter_frame, text="Buscar:")
        search_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.search_entry = ctk.CTkEntry(filter_frame, placeholder_text="Buscar en las entradas...", width=200)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        self.search_entry.bind("<KeyRelease>", self.on_search_change)
        
        # Filtro por emoción
        emotion_label = ctk.CTkLabel(filter_frame, text="Emoción:")
        emotion_label.grid(row=0, column=2, padx=(20, 5), pady=5, sticky="w")
        
        self.emotion_filter = ctk.CTkComboBox(filter_frame, 
                                            values=["Todas", "joy", "sadness", "anger", "fear", "surprise", "neutral", "disgust"],
                                            command=self.on_filter_change)
        self.emotion_filter.grid(row=0, column=3, padx=5, pady=5)
        self.emotion_filter.set("Todas")
        
        # Botones de acción
        button_frame = ctk.CTkFrame(filter_frame)
        button_frame.grid(row=0, column=4, padx=(20, 5), pady=5)
        
        refresh_btn = ctk.CTkButton(button_frame, text="🔄 Actualizar", 
                                   command=self.refresh_data, width=100)
        refresh_btn.pack(side="left", padx=2)
        
        stats_btn = ctk.CTkButton(button_frame, text="📊 Estadísticas", 
                                 command=self.show_statistics, width=100)
        stats_btn.pack(side="left", padx=2)
        
        export_btn = ctk.CTkButton(button_frame, text="💾 Exportar", 
                                  command=self.export_entries, width=100)
        export_btn.pack(side="left", padx=2)
        
        # Botones de navegación (si hay callback del menú)
        if self.return_to_menu:
            nav_frame = ctk.CTkFrame(filter_frame)
            nav_frame.grid(row=0, column=5, padx=(10, 5), pady=5)
            
            menu_btn = ctk.CTkButton(nav_frame, text="🏠 Menú", 
                                   command=self.go_to_menu, width=80)
            menu_btn.pack(side="left", padx=2)
            
            diary_btn = ctk.CTkButton(nav_frame, text="✍️ Diario", 
                                    command=self.go_to_diary, width=80)
            diary_btn.pack(side="left", padx=2)
        
        # Panel principal - dividido en dos columnas
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Columna izquierda - Lista de entradas
        left_frame = ctk.CTkFrame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
        
        entries_label = ctk.CTkLabel(left_frame, text="Entradas del Diario", 
                                   font=ctk.CTkFont(size=16, weight="bold"))
        entries_label.pack(pady=(10, 5))
        
        # Lista de entradas con scrollbar
        self.entries_listbox = tk.Listbox(left_frame, bg="#2b2b2b", fg="white", 
                                         selectbackground="#1f538d", font=("Arial", 10))
        scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=self.entries_listbox.yview)
        self.entries_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.entries_listbox.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(0, 10))
        scrollbar.pack(side="right", fill="y", pady=(0, 10))
        
        self.entries_listbox.bind("<<ListboxSelect>>", self.on_entry_select)
        
        # Columna derecha - Detalles de entrada
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)
        
        details_label = ctk.CTkLabel(right_frame, text="Detalles de la Entrada", 
                                   font=ctk.CTkFont(size=16, weight="bold"))
        details_label.pack(pady=(10, 5))
        
        # Área de detalles
        self.details_text = ctk.CTkTextbox(right_frame, wrap="word", font=ctk.CTkFont(size=12))
        self.details_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Panel inferior - Información de resumen
        summary_frame = ctk.CTkFrame(main_frame)
        summary_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.summary_label = ctk.CTkLabel(summary_frame, text="", font=ctk.CTkFont(size=12))
        self.summary_label.pack(pady=10)
        
    def load_diary_entries(self):
        """
        Carga las entradas del diario desde el archivo de log.
        """
        self.diary_entries = []
        
        if not os.path.exists(self.log_file_path):
            messagebox.showwarning("Archivo no encontrado", 
                                 f"No se encontró el archivo de log: {self.log_file_path}")
            return
        
        try:
            with open(self.log_file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            current_entry = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Parsear línea del log
                # Formato: [HH:MM] Speaker: Message / Emotion (opcional)
                match = re.match(r'\[(\d{2}:\d{2})\] (Tú|Bot): (.+?)(?:\s*/\s*(.+))?$', line)
                
                if match:
                    time_str, speaker, message, emotion = match.groups()
                    
                    entry = {
                        'time': time_str,
                        'speaker': speaker,
                        'message': message,
                        'emotion': emotion if emotion else 'Input',
                        'full_line': line,
                        'date': datetime.datetime.now().strftime("%Y-%m-%d")  # Usar fecha actual como aproximación
                    }
                    
                    self.diary_entries.append(entry)
            
            print(f"Cargadas {len(self.diary_entries)} entradas del diario")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo de log: {e}")
    
    def update_display(self):
        """
        Actualiza la visualización de entradas basada en los filtros actuales.
        """
        # Aplicar filtros
        search_text = self.search_entry.get().lower()
        emotion_filter = self.emotion_filter.get()
        
        self.filtered_entries = []
        
        for entry in self.diary_entries:
            # Filtro de búsqueda
            if search_text and search_text not in entry['message'].lower():
                continue
            
            # Filtro de emoción
            if emotion_filter != "Todas" and entry['emotion'] != emotion_filter:
                continue
            
            self.filtered_entries.append(entry)
        
        # Actualizar lista
        self.entries_listbox.delete(0, tk.END)
        
        for entry in self.filtered_entries:
            # Formatear entrada para mostrar
            emotion_emoji = self.get_emotion_emoji(entry['emotion'])
            display_text = f"{entry['time']} {emotion_emoji} {entry['speaker']}: {entry['message'][:50]}..."
            self.entries_listbox.insert(tk.END, display_text)
            
            # Colorear según emoción
            color = self.emotion_colors.get(entry['emotion'], '#FFFFFF')
            self.entries_listbox.itemconfig(tk.END, {'fg': color})
        
        # Actualizar resumen
        self.update_summary()
    
    def get_emotion_emoji(self, emotion):
        """
        Retorna el emoji correspondiente a una emoción.
        """
        emoji_map = {
            'joy': '😊',
            'sadness': '😢',
            'anger': '😠',
            'fear': '😰',
            'surprise': '😲',
            'neutral': '😐',
            'disgust': '🤢',
            'Input': '💭'
        }
        return emoji_map.get(emotion, '❓')
    
    def on_entry_select(self, event):
        """
        Maneja la selección de una entrada en la lista.
        """
        selection = self.entries_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        if index < len(self.filtered_entries):
            entry = self.filtered_entries[index]
            self.show_entry_details(entry)
    
    def show_entry_details(self, entry):
        """
        Muestra los detalles de una entrada seleccionada.
        """
        self.details_text.delete("1.0", tk.END)
        
        # Formatear detalles
        details = f"""Hora: {entry['time']}
Fecha: {entry['date']}
Hablante: {entry['speaker']}
Emoción: {entry['emotion']} {self.get_emotion_emoji(entry['emotion'])}

Mensaje:
{entry['message']}

Línea completa del log:
{entry['full_line']}
"""
        
        self.details_text.insert("1.0", details)
    
    def on_search_change(self, event):
        """
        Maneja cambios en el campo de búsqueda.
        """
        self.update_display()
    
    def on_filter_change(self, value):
        """
        Maneja cambios en el filtro de emoción.
        """
        self.update_display()
    
    def refresh_data(self):
        """
        Recarga los datos del archivo de log.
        """
        self.load_diary_entries()
        self.update_display()
        messagebox.showinfo("Actualizado", "Datos del diario actualizados correctamente")
    
    def update_summary(self):
        """
        Actualiza el resumen de entradas mostradas.
        """
        total_entries = len(self.filtered_entries)
        user_entries = len([e for e in self.filtered_entries if e['speaker'] == 'Tú'])
        bot_entries = len([e for e in self.filtered_entries if e['speaker'] == 'Bot'])
        
        # Contar emociones
        emotions = [e['emotion'] for e in self.filtered_entries if e['emotion'] != 'Input']
        emotion_counts = Counter(emotions)
        
        summary_text = f"Mostrando {total_entries} entradas | Usuario: {user_entries} | Bot: {bot_entries}"
        
        if emotion_counts:
            most_common = emotion_counts.most_common(1)[0]
            summary_text += f" | Emoción más frecuente: {most_common[0]} ({most_common[1]})"
        
        self.summary_label.configure(text=summary_text)
    
    def show_statistics(self):
        """
        Muestra una ventana con estadísticas detalladas.
        """
        # Cargar matplotlib solo cuando se necesite
        plt, FigureCanvasTkAgg = load_matplotlib()
        
        stats_window = ctk.CTkToplevel(self.window)
        stats_window.title("Estadísticas del Diario")
        stats_window.geometry("800x600")
        
        # Preparar datos para estadísticas
        emotions = [e['emotion'] for e in self.diary_entries if e['emotion'] != 'Input']
        emotion_counts = Counter(emotions)
        
        if not emotion_counts:
            no_data_label = ctk.CTkLabel(stats_window, text="No hay datos de emociones para mostrar")
            no_data_label.pack(pady=50)
            return
        
        # Crear gráfico
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.patch.set_facecolor('#2b2b2b')
        
        # Gráfico de barras
        emotions_list = list(emotion_counts.keys())
        counts_list = list(emotion_counts.values())
        colors = [self.emotion_colors.get(emotion, '#FFFFFF') for emotion in emotions_list]
        
        ax1.bar(emotions_list, counts_list, color=colors)
        ax1.set_title('Distribución de Emociones', color='white')
        ax1.set_xlabel('Emociones', color='white')
        ax1.set_ylabel('Frecuencia', color='white')
        ax1.tick_params(colors='white')
        ax1.set_facecolor('#2b2b2b')
        
        # Gráfico circular
        ax2.pie(counts_list, labels=emotions_list, colors=colors, autopct='%1.1f%%', 
                textprops={'color': 'white'})
        ax2.set_title('Proporción de Emociones', color='white')
        ax2.set_facecolor('#2b2b2b')
        
        # Mostrar gráfico en la ventana
        canvas = FigureCanvasTkAgg(fig, stats_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # Estadísticas textuales
        stats_text = ctk.CTkTextbox(stats_window, height=150)
        stats_text.pack(fill="x", padx=10, pady=(0, 10))
        
        total_user_entries = len([e for e in self.diary_entries if e['speaker'] == 'Tú'])
        total_bot_entries = len([e for e in self.diary_entries if e['speaker'] == 'Bot'])
        
        stats_info = f"""Estadísticas Generales:
• Total de entradas del usuario: {total_user_entries}
• Total de respuestas del bot: {total_bot_entries}
• Total de emociones detectadas: {len(emotions)}
• Emociones únicas identificadas: {len(emotion_counts)}

Emociones más frecuentes:
"""
        
        for emotion, count in emotion_counts.most_common():
            percentage = (count / len(emotions)) * 100
            emoji = self.get_emotion_emoji(emotion)
            stats_info += f"• {emoji} {emotion}: {count} veces ({percentage:.1f}%)\n"
        
        stats_text.insert("1.0", stats_info)
        stats_text.configure(state="disabled")
    
    def export_entries(self):
        """
        Exporta las entradas filtradas a un archivo.
        """
        if not self.filtered_entries:
            messagebox.showwarning("Sin datos", "No hay entradas para exportar")
            return
        
        # Seleccionar archivo de destino
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt"), ("Todos los archivos", "*.*")],
            title="Guardar entradas del diario"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("=== EXPORTACIÓN DEL DIARIO EMOCIONAL ===\n")
                f.write(f"Fecha de exportación: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total de entradas: {len(self.filtered_entries)}\n\n")
                
                for entry in self.filtered_entries:
                    f.write(f"[{entry['time']}] {entry['speaker']}: {entry['message']}")
                    if entry['emotion'] != 'Input':
                        f.write(f" / {entry['emotion']}")
                    f.write("\n")
            
            messagebox.showinfo("Exportado", f"Entradas exportadas correctamente a:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {e}")
    
    def on_closing(self):
        """
        Maneja el cierre de la ventana.
        """
        self.window.destroy()
        if self.return_to_menu:
            self.return_to_menu()
    
    def go_to_menu(self):
        """
        Navega al menú principal.
        """
        self.window.destroy()
        if self.return_to_menu:
            self.return_to_menu()
    
    def go_to_diary(self):
        """
        Navega al diario principal.
        """
        self.window.destroy()
        if self.return_to_menu:
            from interface import EmotionalDiaryApp
            diary = EmotionalDiaryApp(return_to_menu=self.return_to_menu)
            diary.run()
    
    def run(self):
        """
        Inicia la aplicación del visor.
        """
        self.window.mainloop()

def main():
    """
    Función principal para ejecutar el visor del diario.
    """
    app = DiaryViewerApp()
    app.run()

if __name__ == "__main__":
    main()

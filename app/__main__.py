"""
Diario Emocional - Punto de entrada principal
-------------------------------------------

Este módulo es el punto de entrada principal de la aplicación Diario Emocional.
Inicia la interfaz gráfica principal y gestiona el ciclo de vida de la aplicación.

Uso:
    Ejecutar desde línea de comandos:
        python -m app

La aplicación iniciará la interfaz gráfica que permite:
- Grabar audio para análisis emocional
- Procesar texto para detección de emociones
- Visualizar resultados del análisis
"""

from interface import EmotionalDiaryApp

if __name__ == "__main__":
    app = EmotionalDiaryApp()
    app.run()

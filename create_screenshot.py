#!/usr/bin/env python3
# create_screenshot.py - Create a mock screenshot of the application
import sys
import os
from PIL import Image, ImageDraw, ImageFont

def create_mock_screenshot():
    """Create a mock screenshot of the GUI application"""
    
    # Create a new image with dark background
    width, height = 800, 600
    bg_color = (43, 43, 43)  # Dark gray background
    
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Colors
    text_color = (255, 255, 255)  # White text
    button_color = (68, 114, 196)  # Blue button
    text_area_color = (60, 60, 60)  # Dark gray text areas
    
    # Try to use default font, fallback to basic font
    try:
        title_font = ImageFont.truetype("arial.ttf", 24)
        header_font = ImageFont.truetype("arial.ttf", 14)
        text_font = ImageFont.truetype("arial.ttf", 10)
    except:
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Title
    draw.text((width//2 - 100, 30), "Diario Emocional", fill=text_color, font=title_font)
    
    # Input section
    draw.text((50, 80), "Escribe cómo te sientes:", fill=text_color, font=header_font)
    
    # Input text area
    draw.rectangle([50, 100, width-50, 180], fill=text_area_color, outline=(100, 100, 100))
    draw.text((60, 110), "Hoy me siento muy frustrado en el trabajo.", fill=text_color, font=text_font)
    draw.text((60, 130), "Mi jefe me dio una tarea con un plazo imposible", fill=text_color, font=text_font)
    draw.text((60, 150), "y no sé cómo voy a terminarla a tiempo.", fill=text_color, font=text_font)
    
    # Process button
    draw.rectangle([width//2 - 100, 200, width//2 + 100, 240], fill=button_color, outline=(100, 100, 100))
    draw.text((width//2 - 85, 215), "💭 Procesar Emociones", fill=text_color, font=header_font)
    
    # Status
    draw.text((width//2 - 80, 250), "Procesamiento completado", fill=(200, 200, 200), font=text_font)
    
    # Results section
    draw.text((50, 290), "Tu texto:", fill=text_color, font=header_font)
    draw.rectangle([50, 310, width-50, 390], fill=text_area_color, outline=(100, 100, 100))
    draw.text((60, 320), "Hoy me siento muy frustrado en el trabajo.", fill=text_color, font=text_font)
    draw.text((60, 340), "Mi jefe me dio una tarea con un plazo imposible", fill=text_color, font=text_font)
    draw.text((60, 360), "y no sé cómo voy a terminarla a tiempo.", fill=text_color, font=text_font)
    
    draw.text((50, 410), "Respuesta Empática:", fill=text_color, font=header_font)
    draw.rectangle([50, 430, width-50, 520], fill=text_area_color, outline=(100, 100, 100))
    draw.text((60, 440), "Puedo sentir tu frustración sobre esta situación", fill=text_color, font=text_font)
    draw.text((60, 460), "laboral. Debe ser muy difícil lidiar con plazos", fill=text_color, font=text_font)
    draw.text((60, 480), "imposibles. ¿Cómo te sientes respecto a todo esto?", fill=text_color, font=text_font)
    
    # Footer buttons
    draw.rectangle([50, 540, 120, 570], fill=(102, 102, 102), outline=(100, 100, 100))
    draw.text((65, 550), "🗑️ Limpiar", fill=text_color, font=text_font)
    
    draw.rectangle([140, 540, 210, 570], fill=(45, 125, 50), outline=(100, 100, 100))
    draw.text((155, 550), "💾 Guardar", fill=text_color, font=text_font)
    
    draw.rectangle([230, 540, 300, 570], fill=(245, 124, 0), outline=(100, 100, 100))
    draw.text((245, 550), "📝 Ejemplo", fill=text_color, font=text_font)
    
    # Save the screenshot
    screenshot_path = "app_screenshot.png"
    img.save(screenshot_path)
    print(f"Mock screenshot saved as: {screenshot_path}")
    
    return screenshot_path

if __name__ == "__main__":
    create_mock_screenshot()
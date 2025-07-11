"""
Análisis de Emociones en Texto
-----------------------------

Este módulo implementa un analizador de emociones basado en procesamiento de lenguaje natural (NLP)
utilizando un modelo pre-entrenado de Transformers. El modelo está optimizado para detectar
emociones en texto en español e inglés.

El módulo:
1. Carga un modelo pre-entrenado de la arquitectura Transformers
2. Procesa el texto de entrada utilizando tokenización
3. Realiza la predicción de la emoción usando el modelo
4. Decodifica y retorna la emoción detectada

Dependencias:
    - torch: Para la inferencia del modelo
    - transformers: Para el modelo y tokenizador
    - joblib: Para cargar el codificador de etiquetas
    - numpy: Para operaciones numéricas
"""

# Análisis emocional del texto (NLP)
import torch
import joblib
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np

# === Configuración de Rutas y Modelo ===
model_path = "ml_models/transformers/emotion_model/"

# Cargar componentes del modelo
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
label_encoder = joblib.load(model_path + "label_encoder.pkl")

# Configurar dispositivo (GPU/CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

def predict_emotion(text):
    """
    Predice la emoción predominante en un texto dado.

    Args:
        text (str): Texto de entrada para analizar

    Returns:
        str: Emoción detectada (ej: 'alegría', 'tristeza', 'enojo', etc.)

    Example:
        >>> emotion = predict_emotion("¡Hoy fue un día maravilloso!")
        >>> print(emotion)
        'alegría'
    """
    # Tokenizar el texto
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=128)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Predecir
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class_id = torch.argmax(logits, dim=1).item()

    # Decodificar la etiqueta
    predicted_emotion = label_encoder.inverse_transform([predicted_class_id])[0]
    return predicted_emotion

# === Ejemplo de uso ===
if __name__ == "__main__":
    text_input = "Me siento muy feliz hoy"
    predicted = predict_emotion(text_input)
    print(f"Emoción detectada: {predicted}")

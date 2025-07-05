# Análisis emocional del texto (NLP)
import torch
import joblib
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np

# Ruta donde guardaste el modelo
model_path = "ml_models/transformers/emotion_model/"

# Cargar tokenizer, modelo y label encoder
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
label_encoder = joblib.load(model_path + "label_encoder.pkl")

# Mover a GPU si está disponible
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

def predict_emotion(text):
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

text_input = "IM FABIAN TODAY IM GOING TO KILL MYSELF BY HANGING MYSELF IN THE BATHROOM"
predicted = predict_emotion(text_input)
print(f"Emoción detectada: {predicted}")

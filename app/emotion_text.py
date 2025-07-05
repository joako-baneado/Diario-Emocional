# emocionador.py
from transformers import pipeline

# Carga del modelo fine-tuned (ajusta si es otro nombre o ruta)
modelo_emocional = pipeline("text-classification", model="app/modelo_emocional", tokenizer="app/modelo_emocional")

def predecir_emocion(texto):
    resultado = modelo_emocional(texto)[0]
    emocion = resultado["label"]
    score = resultado["score"]
    return emocion, score

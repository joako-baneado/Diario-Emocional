
import pandas as pd
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)         # quitar URLs
    text = re.sub(r"@\w+", "", text)            # quitar menciones
    text = re.sub(r"[^a-záéíóúñü\s]", "", text)  # solo letras y espacios
    text = re.sub(r"\s+", " ", text).strip()    # quitar espacios extras
    return text

def preprocess_dataset(input_path, output_path):
    df = pd.read_csv(input_path)

    if 'text' not in df.columns or 'emotion' not in df.columns:
        raise ValueError("El CSV debe tener columnas 'text' y 'emotion'")

    df['text'] = df['text'].astype(str).apply(clean_text)
    df.dropna(subset=['text', 'emotion'], inplace=True)
    df.to_csv(output_path, index=False)
    print(f"Preprocesamiento completado. Guardado en {output_path}")

#Ejemplo de uso:
# preprocess_dataset("raw_dataset.csv", "dataset.csv")

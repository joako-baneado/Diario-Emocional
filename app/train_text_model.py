import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from sklearn.preprocessing import LabelEncoder
import torch
import numpy as np
import os

# Cargar y codificar dataset
df = pd.read_csv("app/dataset.csv")

label_encoder = LabelEncoder()
df['label'] = label_encoder.fit_transform(df['emotion'])

dataset = Dataset.from_pandas(df[['text', 'label']])
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize(batch):
    return tokenizer(batch["text"], padding="max_length", truncation=True)

tokenized_dataset = dataset.map(tokenize, batched=True)
tokenized_dataset = tokenized_dataset.train_test_split(test_size=0.2)

# Modelo
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=len(label_encoder.classes_)
)

# Parámetros de entrenamiento
training_args = TrainingArguments(
    output_dir="./model",
    evaluation_strategy="epoch",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=4,
    save_strategy="epoch",
    logging_dir="./logs",
    logging_steps=10
)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=1)
    acc = np.mean(preds == labels)
    return {"accuracy": acc}

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

trainer.train()
model.save_pretrained("../../ml_models/transformers/emotion_model/")
tokenizer.save_pretrained("../../ml_models/transformers/emotion_model/")

# Guardar codificador de etiquetas
import joblib
joblib.dump(label_encoder, "../../ml_models/transformers/emotion_model/label_encoder.pkl")

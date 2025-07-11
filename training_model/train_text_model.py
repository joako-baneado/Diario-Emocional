if __name__ == '__main__':
    import pandas as pd
    from datasets import Dataset
    from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
    from sklearn.preprocessing import LabelEncoder
    import torch
    import numpy as np
    import joblib
    import os

    # Entrenamiento con optimización incluida
    df = pd.read_csv("./training_model/datasets/dataset.csv")
    label_encoder = LabelEncoder()
    df['label'] = label_encoder.fit_transform(df['emotion'])

    dataset = Dataset.from_pandas(df[['text', 'label']])
    model_name = "distilbert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    def tokenize(batch):
        return tokenizer(batch["text"], padding="max_length", truncation=True, max_length=128)

    tokenized_dataset = dataset.map(tokenize, batched=True)
    tokenized_dataset = tokenized_dataset.train_test_split(test_size=0.2)
    tokenized_dataset = tokenized_dataset.remove_columns(["text"])

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=len(label_encoder.classes_)
    ).to(device)

    training_args = TrainingArguments(
        output_dir="./model",
        eval_strategy="epoch",
        save_strategy="no",
        logging_dir="./logs",
        logging_steps=50,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        num_train_epochs=2,
        warmup_steps=0,
        weight_decay=0.01,
        fp16=torch.cuda.is_available(),
        dataloader_num_workers=2,  # ✅ Este valor requiere el bloque __main__ en Windows
        disable_tqdm=True
    )

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        preds = np.argmax(logits, axis=1)
        acc = np.mean(preds == labels)
        return {"accuracy": acc}

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["test"],
        tokenizer=tokenizer,
        compute_metrics=compute_metrics
    )

    trainer.train()

    save_path = "./ml_models/transformers/emotion_model/"
    model.save_pretrained(save_path)
    tokenizer.save_pretrained(save_path)
    joblib.dump(label_encoder, os.path.join(save_path, "label_encoder.pkl"))

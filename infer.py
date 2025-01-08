import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import argparse

# Настройка устройства
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def infer_model(model_dir, text):
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    model.to(DEVICE)

    tokens = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    tokens = {k: v.to(DEVICE) for k, v in tokens.items()}
    
    model.eval()
    with torch.no_grad():
        outputs = model(**tokens)
        probabilities = torch.softmax(outputs.logits, dim=-1)
    
    return probabilities.tolist()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Инференс с медицинской нейросетью")
    parser.add_argument("--model", required=True, help="Путь к сохраненной модели")
    parser.add_argument("--text", required=True, help="Текст для анализа")
    args = parser.parse_args()

    result = infer_model(args.model, args.text)
    print(f"Результаты предсказания: {result}")

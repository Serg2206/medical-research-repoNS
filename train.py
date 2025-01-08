import os
import argparse
import logging
from datetime import datetime
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AdamW

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Параметры модели
MODEL_NAME = "bert-base-uncased"  # Измените на свою модель
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# Заготовка для датасета
class MedicalDataset(Dataset):
    def __init__(self, file_path, tokenizer, max_length=128):
        self.data = self._load_data(file_path)
        self.tokenizer = tokenizer
        self.max_length = max_length

    def _load_data(self, file_path):
        # Заглушка: загрузите данные из CSV или другого источника
        logger.info(f"Загрузка данных из {file_path}")
        return [{"text": "Пример текста", "label": 1}]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        tokens = self.tokenizer(
            item["text"], truncation=True, padding="max_length", max_length=self.max_length, return_tensors="pt"
        )
        return tokens["input_ids"].squeeze(), tokens["attention_mask"].squeeze(), torch.tensor(item["label"])


def train_model(data_path, output_dir, epochs=3, batch_size=16, learning_rate=2e-5):
    logger.info("Инициализация модели...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
    model.to(DEVICE)

    dataset = MedicalDataset(data_path, tokenizer)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    optimizer = AdamW(model.parameters(), lr=learning_rate)

    model.train()
    for epoch in range(epochs):
        logger.info(f"Эпоха {epoch + 1}/{epochs}")
        for batch in dataloader:
            input_ids, attention_mask, labels = [x.to(DEVICE) for x in batch]
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

        logger.info(f"Эпоха {epoch + 1} завершена. Потеря: {loss.item()}")

    logger.info(f"Сохранение модели в {output_dir}")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Обучение нейросети на медицинских данных")
    parser.add_argument("--data", required=True, help="Путь к обучающим данным")
    parser.add_argument("--output", required=True, help="Путь для сохранения модели")
    args = parser.parse_args()

    train_model(args.data, args.output)

import os
import argparse
import logging
import pandas as pd
from sklearn.model_selection import train_test_split
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
    def __init__(self, data, tokenizer, max_length=128):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data.iloc[idx]
        tokens = self.tokenizer(
            item["text"], truncation=True, padding="max_length", max_length=self.max_length, return_tensors="pt"
        )
        return tokens["input_ids"].squeeze(), tokens["attention_mask"].squeeze(), torch.tensor(item["label"])


def prepare_data(input_csv, output_dir, test_size=0.2):
    """
    Подготовить данные: разделить на обучающую и тестовую выборки.
    :param input_csv: Путь к входному CSV-файлу.
    :param output_dir: Директория для сохранения обработанных данных.
    :param test_size: Размер тестовой выборки (доля от общего объема данных).
    """
    logger.info(f"Чтение данных из {input_csv}")
    data = pd.read_csv(input_csv)

    # Проверка наличия необходимых столбцов
    if "text" not in data.columns or "label" not in data.columns:
        raise ValueError("CSV-файл должен содержать столбцы 'text' и 'label'")

    # Очистка данных (пример)
    data["text"] = data["text"].str.strip()

    # Разделение данных
    train_data, test_data = train_test_split(data, test_size=test_size, random_state=42)
    logger.info(f"Разделение данных: {len(train_data)} для обучения, {len(test_data)} для теста")

    # Сохранение данных
    os.makedirs(output_dir, exist_ok=True)
    train_data.to_csv(os.path.join(output_dir, "train.csv"), index=False)
    test_data.to_csv(os.path.join(output_dir, "test.csv"), index=False)
    logger.info(f"Обработанные данные сохранены в {output_dir}")


def train_model(data_dir, output_dir, epochs=3, batch_size=16, learning_rate=2e-5):
    logger.info("Инициализация модели...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
    model.to(DEVICE)

    # Загрузка данных
    train_data = pd.read_csv(os.path.join(data_dir, "train.csv"))
    dataset = MedicalDataset(train_data, tokenizer)
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
    parser.add_argument("--data", required=True, help="Путь к исходным данным CSV")
    parser.add_argument("--output", required=True, help="Директория для сохранения модели и данных")
    args = parser.parse_args()

    # Подготовка данных
    prepare_data(args.data, args.output)

    # Обучение модели
    train_model(args.output, args.output)

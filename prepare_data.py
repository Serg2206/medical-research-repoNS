import os
import pandas as pd
from sklearn.model_selection import train_test_split
import argparse
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    train_data, test_data = train_test_split(
        data, test_size=test_size, random_state=42)
    logger.info(
        f"Разделение данных: {len(train_data)} для обучения, {len(test_data)} для теста")

    # Сохранение данных
    os.makedirs(output_dir, exist_ok=True)
    train_data.to_csv(os.path.join(output_dir, "train.csv"), index=False)
    test_data.to_csv(os.path.join(output_dir, "test.csv"), index=False)
    logger.info(f"Обработанные данные сохранены в {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Подготовка данных для обучения нейросети")
    parser.add_argument(
        "--input",
        required=True,
        help="Путь к исходным данным CSV")
    parser.add_argument(
        "--output",
        required=True,
        help="Директория для сохранения обработанных данных")
    args = parser.parse_args()

    prepare_data(args.input, args.output)

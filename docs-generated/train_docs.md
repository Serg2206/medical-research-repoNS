# Documentation: train.py

**Файл:** `train.py`

**Дата:** 2025-11-12

---

# Документация

## Описание функционала

Этот код представляет собой скрипт для обучения модели классификации текста на основе BERT. Он использует библиотеку transformers для загрузки предобученной модели и токенизатора. Данные для обучения и тестирования загружаются из CSV-файла и разделяются на обучающую и тестовую выборки.

## Параметры и возвращаемые значения

### Класс MedicalDataset

- `data`: DataFrame, содержащий данные для обучения или тестирования. Ожидается, что он содержит столбцы "text" и "label".
- `tokenizer`: Токенизатор из библиотеки transformers, используемый для преобразования текста в токены.
- `max_length`: Максимальная длина последовательности токенов. Все последовательности, которые превышают эту длину, обрезаются.

### Функция prepare_data

- `input_csv`: Путь к входному CSV-файлу. Файл должен содержать столбцы "text" и "label".
- `output_dir`: Директория для сохранения обработанных данных.
- `test_size`: Доля данных, которая будет использоваться для тестирования. По умолчанию равна 0.2.

## Примеры использования

```python
# Загрузка данных
data = pd.read_csv("data.csv")

# Разделение данных на обучающую и тестовую выборки
train_data, test_data = train_test_split(data, test_size=0.2)

# Создание токенизатора
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Создание датасетов
train_dataset = MedicalDataset(train_data, tokenizer)
test_dataset = MedicalDataset(test_data, tokenizer)

# Создание загрузчиков данных
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32)
```

После этого вы можете использовать `train_loader` и `test_loader` для обучения и тестирования вашей модели соответственно.
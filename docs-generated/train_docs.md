# Documentation: train.py

**Файл:** `train.py`

**Дата:** 2025-11-19

---

# Документация

## Описание функционала

Этот код представляет собой пример обучения классификационной модели на основе BERT с использованием библиотеки transformers от Hugging Face. Он включает в себя следующие основные компоненты:

- Загрузка и предварительная обработка данных
- Создание датасета для обучения и тестирования
- Подготовка модели и токенизатора
- Обучение модели

## Классы и функции

### Класс `MedicalDataset`

Этот класс представляет собой настраиваемый датасет для обучения и тестирования модели.

#### Параметры

- `data`: DataFrame, содержащий данные для обучения или тестирования. Ожидается, что он будет содержать столбцы "text" и "label".
- `tokenizer`: Токенизатор, используемый для преобразования текста в токены.
- `max_length`: Максимальная длина последовательности токенов.

#### Методы

- `__len__`: Возвращает количество элементов в датасете.
- `__getitem__`: Возвращает токенизированный текст и соответствующую метку для указанного индекса.

### Функция `prepare_data`

Эта функция загружает данные из CSV-файла, разделяет их на обучающую и тестовую выборки и сохраняет их в указанной директории.

#### Параметры

- `input_csv`: Путь к входному CSV-файлу.
- `output_dir`: Директория для сохранения обработанных данных.
- `test_size`: Доля данных, которая будет использоваться для тестирования. По умолчанию равна 0.2.

#### Возвращаемые значения

Функция не возвращает значения, но сохраняет обработанные данные в указанной директории.

## Примеры использования

```python
# Подготовка данных
prepare_data("data.csv", "processed_data")

# Загрузка токенизатора и модели
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Создание датасета
train_data = pd.read_csv("processed_data/train.csv")
test_data = pd.read_csv("processed_data/test.csv")
train_dataset = MedicalDataset(train_data, tokenizer)
test_dataset = MedicalDataset(test_data, tokenizer)

# Обучение модели (пример)
model.train()
for batch in DataLoader(train_dataset, batch_size=32):
    input_ids, attention_mask, labels = batch
    outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
    loss = outputs.loss
    loss.backward()
    # ...
```
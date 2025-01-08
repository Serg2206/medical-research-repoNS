## Использование

### Подготовка данных

Убедитесь, что ваши данные соответствуют формату, описанному в [docs/data_format.md](docs/data_format.md).

### Обучение модели

Запустите скрипт `train.py` для обучения модели:

```bash
python scripts/train.py --data_path data/medical_data.csv --model_output models/модель.pkl

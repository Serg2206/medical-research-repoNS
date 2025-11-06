# 📊 ML Training Report

**Дата:** 2025-11-06 20:31:36

## 📈 Результаты

### Датасет
- **Всего:** 200
    - **Train:** 160
    - **Test:** 40
### Распределение
```
label
moderate    90
normal      73
critical    37
```

### 🏆 Лучшая модель: LogisticRegression

| Модель | Accuracy | CV Mean | CV Std |
|--------|----------|---------|--------|
|    RandomForest | 0.5750 | 0.7375 | 0.0643 |
|    GradientBoosting | 0.6250 | 0.6937 | 0.0914 |
| 🏆 LogisticRegression | 0.6750 | 0.6687 | 0.0545 |


### Category Classifier
- **Accuracy:** 0.2250

## 💾 Сохраненные модели
1. `ml-models/severity_classifier.pkl`
2. `ml-models/category_classifier.pkl`
3. `ml-models/text_vectorizer.pkl`

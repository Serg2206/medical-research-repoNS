# 📊 ML Training Report

**Дата:** 2025-11-06 20:22:01

## 📈 Результаты

### Датасет
- **Всего:** 81
    - **Train:** 64
    - **Test:** 17
### Распределение
```
label
critical    29
moderate    27
normal      25
```

### 🏆 Лучшая модель: GradientBoosting

| Модель | Accuracy | CV Mean | CV Std |
|--------|----------|---------|--------|
|    RandomForest | 0.7059 | 0.6397 | 0.0819 |
| 🏆 GradientBoosting | 0.8235 | 0.6859 | 0.0908 |
|    LogisticRegression | 0.8235 | 0.6718 | 0.1641 |


### Category Classifier
- **Accuracy:** 0.0588

## 💾 Сохраненные модели
1. `ml-models/severity_classifier.pkl`
2. `ml-models/category_classifier.pkl`
3. `ml-models/text_vectorizer.pkl`

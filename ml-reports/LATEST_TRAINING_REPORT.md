# 📊 ML Training Report

**Дата:** 2026-05-03 03:25:26

## 📈 Результаты

### Датасет
- **Всего:** 276
    - **Train:** 220
    - **Test:** 56
### Распределение
```
label
moderate    116
critical     87
normal       73
```

### 🏆 Лучшая модель: LogisticRegression

| Модель | Accuracy | CV Mean | CV Std |
|--------|----------|---------|--------|
|    RandomForest | 0.6964 | 0.6318 | 0.0464 |
|    GradientBoosting | 0.5714 | 0.6318 | 0.0752 |
| 🏆 LogisticRegression | 0.7500 | 0.6818 | 0.0380 |


### Category Classifier
- **Accuracy:** 0.3750

## 💾 Сохраненные модели
1. `ml-models/severity_classifier.pkl`
2. `ml-models/category_classifier.pkl`
3. `ml-models/text_vectorizer.pkl`

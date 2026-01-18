# 📊 ML Training Report

**Дата:** 2026-01-18 01:59:47

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

### 🏆 Лучшая модель: RandomForest

| Модель | Accuracy | CV Mean | CV Std |
|--------|----------|---------|--------|
| 🏆 RandomForest | 0.7857 | 0.6273 | 0.0549 |
|    GradientBoosting | 0.6071 | 0.6091 | 0.0545 |
|    LogisticRegression | 0.7679 | 0.6636 | 0.0334 |


### Category Classifier
- **Accuracy:** 0.4286

## 💾 Сохраненные модели
1. `ml-models/severity_classifier.pkl`
2. `ml-models/category_classifier.pkl`
3. `ml-models/text_vectorizer.pkl`

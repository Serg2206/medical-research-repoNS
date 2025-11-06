# 📊 ML Training Report

**Дата:** 2025-11-06 21:46:21

## 📈 Результаты

### Датасет
- **Всего:** 243
    - **Train:** 194
    - **Test:** 49
### Распределение
```
label
moderate    101
normal       73
critical     69
```

### 🏆 Лучшая модель: RandomForest

| Модель | Accuracy | CV Mean | CV Std |
|--------|----------|---------|--------|
| 🏆 RandomForest | 0.7755 | 0.7162 | 0.0869 |
|    GradientBoosting | 0.7551 | 0.6748 | 0.0709 |
|    LogisticRegression | 0.7755 | 0.7057 | 0.0859 |


### Category Classifier
- **Accuracy:** 0.3265

## 💾 Сохраненные модели
1. `ml-models/severity_classifier.pkl`
2. `ml-models/category_classifier.pkl`
3. `ml-models/text_vectorizer.pkl`

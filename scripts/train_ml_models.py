#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ML Medical Data Training Script

This script trains machine learning models on medical data for classification
of patient case severity and medical categories.
"""

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib
from datetime import datetime
import os
import sys

def main():
    print("🚀 Начало обучения ML моделей на медицинских данных...")
    print("=" * 80)
    
    # Load training data
    print("\n📊 Загрузка тренировочных данных...")
    try:
        df = pd.read_csv('training-data/medical_training_data.csv')
    except FileNotFoundError:
        print("❌ Error: training-data/medical_training_data.csv not found!")
        sys.exit(1)
    
    print(f"✅ Загружено {len(df)} записей")
    print(f"\nРаспределение классов:")
    print(df['label'].value_counts())
    
    # Create directories
    os.makedirs('ml-models', exist_ok=True)
    os.makedirs('ml-reports', exist_ok=True)
    
    # Train severity classifier
    print("\n🔬 Обучение модели классификации критичности...")
    X = df['text']
    y = df['label']
    
    # Vectorize text
    vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
    X_vectorized = vectorizer.fit_transform(X)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_vectorized, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train multiple models
    models = {
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
        'GradientBoosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
        'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42)
    }
    
    results = {}
    best_model_name = None
    best_accuracy = 0
    best_model = None
    
    print("\n📈 Результаты обучения:")
    print("-" * 80)
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        cv_scores = cross_val_score(model, X_train, y_train, cv=5)
        
        results[name] = {
            'accuracy': float(accuracy),
            'cv_mean': float(cv_scores.mean()),
            'cv_std': float(cv_scores.std()),
            'report': classification_report(y_test, y_pred, zero_division=0)
        }
        
        print(f"\n{name}:")
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model_name = name
            best_model = model
    
    print(f"\n🏆 Лучшая модель: {best_model_name} ({best_accuracy:.4f})")
    
    # Save best model
    joblib.dump(best_model, 'ml-models/severity_classifier.pkl')
    joblib.dump(vectorizer, 'ml-models/text_vectorizer.pkl')
    print("\n💾 Модели сохранены")
    
    # Train category classifier
    print("\n🔬 Обучение классификатора категорий...")
    y_category = df['category']
    X_train_cat, X_test_cat, y_train_cat, y_test_cat = train_test_split(
        X_vectorized, y_category, test_size=0.2, random_state=42
    )
    
    category_model = RandomForestClassifier(n_estimators=100, random_state=42)
    category_model.fit(X_train_cat, y_train_cat)
    y_pred_cat = category_model.predict(X_test_cat)
    category_accuracy = accuracy_score(y_test_cat, y_pred_cat)
    
    print(f"  Category Accuracy: {category_accuracy:.4f}")
    joblib.dump(category_model, 'ml-models/category_classifier.pkl')
    
    # Generate report
    report = generate_report(df, results, best_model_name, best_accuracy, 
                            category_accuracy, X_train, X_test)
    
    with open('ml-reports/LATEST_TRAINING_REPORT.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("\n" + "=" * 80)
    print("✅ Обучение завершено успешно!")
    print(f"📄 Отчет: ml-reports/LATEST_TRAINING_REPORT.md")
    print(f"🎯 Точность: {best_accuracy:.2%}")

def generate_report(df, results, best_model_name, best_accuracy, 
                   category_accuracy, X_train, X_test):
    report = f"""# 📊 ML Training Report

**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📈 Результаты

### Датасет
- **Всего:** {len(df)}
    - **Train:** {X_train.shape[0]}
    - **Test:** {X_test.shape[0]}
### Распределение
```
{df['label'].value_counts().to_string()}
```

### 🏆 Лучшая модель: {best_model_name}

| Модель | Accuracy | CV Mean | CV Std |
|--------|----------|---------|--------|
"""
    
    for name, metrics in results.items():
        marker = "🏆" if name == best_model_name else "  "
        report += f"| {marker} {name} | {metrics['accuracy']:.4f} | {metrics['cv_mean']:.4f} | {metrics['cv_std']:.4f} |\n"
    
    report += f"""

### Category Classifier
- **Accuracy:** {category_accuracy:.4f}

## 💾 Сохраненные модели
1. `ml-models/severity_classifier.pkl`
2. `ml-models/category_classifier.pkl`
3. `ml-models/text_vectorizer.pkl`
"""
    return report

if __name__ == "__main__":
    main()

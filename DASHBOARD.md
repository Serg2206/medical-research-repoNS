# 🚀 AI Self-Learning System Dashboard

> **medical-research-repoNS** - Автоматизированная система самообучения и самооптимизации

---

## 📊 Статус Системы

| Компонент | Статус | Последний запуск | Расписание |
|-----------|--------|------------------|------------|
| 🤖 AI Code Optimizer | [![AI Code Optimizer](https://github.com/Serg2206/medical-research-repoNS/actions/workflows/ai-code-optimizer.yml/badge.svg)](https://github.com/Serg2206/medical-research-repoNS/actions/workflows/ai-code-optimizer.yml) | Автоматически | Ежедневно 3:00 UTC |
| 🧠 ML Pattern Learning | [![ML Pattern Learning](https://github.com/Serg2206/medical-research-repoNS/actions/workflows/ml-pattern-learning.yml/badge.svg)](https://github.com/Serg2206/medical-research-repoNS/actions/workflows/ml-pattern-learning.yml) | Автоматически | Воскресенье 4:00 UTC |
| 🔧 Auto Refactoring | [![Auto Refactoring](https://github.com/Serg2206/medical-research-repoNS/actions/workflows/auto-refactoring.yml/badge.svg)](https://github.com/Serg2206/medical-research-repoNS/actions/workflows/auto-refactoring.yml) | Автоматически | Суббота 2:00 UTC |
| 📊 Performance Monitor | [![Performance Monitor](https://github.com/Serg2206/medical-research-repoNS/actions/workflows/performance-monitor.yml/badge.svg)](https://github.com/Serg2206/medical-research-repoNS/actions/workflows/performance-monitor.yml) | Автоматически | Каждые 6 часов |
| 🔬 Research Analyzer | [![Research Analyzer](https://github.com/Serg2206/medical-research-repoNS/actions/workflows/research-analyzer.yml/badge.svg)](https://github.com/Serg2206/medical-research-repoNS/actions/workflows/research-analyzer.yml) | Автоматически | Понедельник 10:00 UTC |
| 📝 Docs Improver | [![Docs Improver](https://github.com/Serg2206/medical-research-repoNS/actions/workflows/docs-improver.yml/badge.svg)](https://github.com/Serg2206/medical-research-repoNS/actions/workflows/docs-improver.yml) | Автоматически | Среда 5:00 UTC |

---

## 🎯 Возможности Системы

### 🤖 AI Code Optimizer
- ✅ Автоматический анализ кода с помощью GPT-4
- ✅ Оценка сложности кода (Cyclomatic Complexity)
- ✅ Индекс поддерживаемости кода
- ✅ Рекомендации по оптимизации
- 📁 Отчеты: `ai-reports/LATEST_AI_ANALYSIS.md`

### 🧠 ML Pattern Learning
- ✅ Анализ паттернов разработки
- ✅ Изучение истории коммитов
- ✅ Выявление часто изменяемых файлов
- ✅ ML-инсайты для улучшения процесса
- 📁 Отчеты: `ml-insights/LATEST_ML_INSIGHTS.md`

### 🔧 Auto Refactoring
- ✅ Автоматическое форматирование с autopep8
- ✅ Применение Black для единообразия стиля
- ✅ Организация импортов с isort
- ✅ Автоматический коммит изменений

### 📊 Performance Monitor
- ✅ Мониторинг использования CPU
- ✅ Отслеживание использования памяти
- ✅ Контроль размера репозитория
- ✅ Подсчет файлов проекта
- 📁 Отчеты: `performance-logs/LATEST_PERFORMANCE.md`

### 🔬 Research Analyzer
- ✅ AI-анализ исследовательских файлов
- ✅ Рекомендации по улучшению
- ✅ Поддержка .py, .md, .ipynb файлов
- 📁 Отчеты: `research-insights/LATEST_RESEARCH.md`

### 📝 Documentation Improver
- ✅ Автоматическая генерация документации
- ✅ AI-создание описаний функций
- ✅ Примеры использования
- ✅ Markdown форматирование
- 📁 Отчеты: `docs-generated/README.md`

---

## 🚦 Быстрый Старт

### 1. Добавить OpenAI API Key

```bash
# Перейдите в Settings → Secrets → Actions
# Добавьте секрет: OPENAI_API_KEY
```

### 2. Запустить Workflow Вручную

1. Перейдите в **Actions** → Выберите workflow
2. Нажмите **Run workflow** → **Run workflow**

### 3. Просмотреть Результаты

- 🤖 AI Analysis: `ai-reports/LATEST_AI_ANALYSIS.md`
- 🧠 ML Insights: `ml-insights/LATEST_ML_INSIGHTS.md`
- 📊 Performance: `performance-logs/LATEST_PERFORMANCE.md`
- 🔬 Research: `research-insights/LATEST_RESEARCH.md`
- 📝 Docs: `docs-generated/README.md`

---

## 📈 Расписание Автоматизации

```
┌─────────────── Минута (0 - 59)
│ ┌───────────── Час (0 - 23)
│ │ ┌─────────── День месяца (1 - 31)
│ │ │ ┌───────── Месяц (1 - 12)
│ │ │ │ ┌─────── День недели (0 - 6) (Воскресенье=0)
│ │ │ │ │
│ │ │ │ │
0 3 * * *   ← AI Code Optimizer (ежедневно)
0 */6 * * * ← Performance Monitor (каждые 6 часов)
0 4 * * 0   ← ML Pattern Learning (воскресенье)
0 2 * * 6   ← Auto Refactoring (суббота)
0 10 * * 1  ← Research Analyzer (понедельник)
0 5 * * 3   ← Docs Improver (среда)
```

---

## 🔗 Полезные Ссылки

- 📊 [GitHub Actions](https://github.com/Serg2206/medical-research-repoNS/actions)
- ⚙️ [Settings → Secrets](https://github.com/Serg2206/medical-research-repoNS/settings/secrets/actions)
- 📖 [OpenAI Platform](https://platform.openai.com/api-keys)
- 📁 [Workflows Directory](https://github.com/Serg2206/medical-research-repoNS/tree/main/.github/workflows)

---

## 🎓 Как Работает Система

### Цикл Самообучения

```
┌─────────────────────────────────────────┐
│  1. Мониторинг изменений в коде         │
│     ├─ Автоматический триггер push      │
│     └─ Расписание по cron               │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  2. AI Анализ и Обучение                │
│     ├─ GPT-4 анализирует код            │
│     ├─ ML выявляет паттерны             │
│     └─ Генерирует рекомендации          │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  3. Автоматическая Оптимизация          │
│     ├─ Рефакторинг кода                 │
│     ├─ Улучшение документации           │
│     └─ Применение best practices        │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  4. Генерация Отчетов                   │
│     ├─ Markdown отчеты                  │
│     ├─ JSON метрики                     │
│     └─ Автоматический commit            │
└─────────────────────────────────────────┘
```

---

## 💡 Советы по Использованию

### ⚡ Для Максимальной Эффективности:

1. **Регулярно проверяйте отчеты** в папках:
   - `ai-reports/`
   - `ml-insights/`
   - `performance-logs/`
   - `research-insights/`
   - `docs-generated/`

2. **Используйте manual triggers** для немедленного анализа:
   - Actions → Choose workflow → Run workflow

3. **Мониторьте статус** через badges в этом файле

4. **Настройте уведомления** в Settings → Notifications

---

## 🛡️ Безопасность

- ✅ **API ключи хранятся в GitHub Secrets** (зашифровано)
- ✅ **Workflow запускаются в изолированной среде**
- ✅ **Автоматическое управление правами доступа**
- ✅ **Логи доступны только владельцу репозитория**

---

## 📞 Поддержка

Если у вас возникли вопросы или проблемы:

1. Проверьте [Actions logs](https://github.com/Serg2206/medical-research-repoNS/actions)
2. Убедитесь, что `OPENAI_API_KEY` добавлен в Secrets
3. Проверьте наличие credits на OpenAI аккаунте

---

<div align="center">

**🚀 Система запущена и работает автоматически! 🚀**

*Последнее обновление: Автоматически генерируется GitHub Actions*

</div>


#!/usr/bin/env python3
"""
Вспомогательные утилиты для генератора рукописей
"""

import re
from pathlib import Path
from typing import List, Dict, Optional


def extract_metadata_from_markdown(content: str) -> Dict:
    """
    Извлекает метаданные из Markdown файла
    
    Args:
        content: Содержимое Markdown файла
    
    Returns:
        Словарь с метаданными
    """
    metadata = {
        'title': '',
        'author': '',
        'institution': '',
        'date': '',
        'keywords': '',
        'abstract': ''
    }
    
    # Извлечение заголовка
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        metadata['title'] = title_match.group(1).strip()
    
    # Извлечение автора
    author_match = re.search(r'\*\*Автор:\*\*\s+(.+)$', content, re.MULTILINE)
    if author_match:
        metadata['author'] = author_match.group(1).strip()
    
    # Извлечение института
    inst_match = re.search(r'\*\*Институт:\*\*\s+(.+)$', content, re.MULTILINE)
    if inst_match:
        metadata['institution'] = inst_match.group(1).strip()
    
    # Извлечение даты
    date_match = re.search(r'\*\*Дата:\*\*\s+(.+)$', content, re.MULTILINE)
    if date_match:
        metadata['date'] = date_match.group(1).strip()
    
    # Извлечение ключевых слов
    keywords_match = re.search(r'\*\*Ключевые слова:\*\*\s+(.+)$', content, re.MULTILINE)
    if keywords_match:
        metadata['keywords'] = keywords_match.group(1).strip()
    
    return metadata


def validate_table_syntax(table_text: str) -> bool:
    """
    Проверяет корректность синтаксиса Markdown таблицы
    
    Args:
        table_text: Текст таблицы
    
    Returns:
        True если синтаксис корректен
    """
    lines = table_text.strip().split('\n')
    
    if len(lines) < 2:
        return False
    
    # Проверяем разделитель заголовка
    if not re.match(r'^\|[\s\-\|:]+\|$', lines[1]):
        return False
    
    # Проверяем что все строки содержат одинаковое количество колонок
    col_counts = []
    for line in lines:
        cols = line.split('|')
        col_counts.append(len([c for c in cols if c.strip()]))
    
    return len(set(col_counts)) == 1


def count_words(text: str) -> int:
    """
    Подсчитывает количество слов в тексте
    
    Args:
        text: Текст для подсчета
    
    Returns:
        Количество слов
    """
    # Удаляем Markdown разметку
    text = re.sub(r'[#*_\[\]()]', '', text)
    # Удаляем специальные блоки
    text = re.sub(r':::[^:]+:::', '', text, flags=re.DOTALL)
    
    words = text.split()
    return len(words)


def generate_toc(content: str, max_level: int = 3) -> str:
    """
    Генерирует оглавление на основе заголовков
    
    Args:
        content: Markdown контент
        max_level: Максимальный уровень заголовков для включения
    
    Returns:
        HTML оглавление
    """
    headings = re.findall(r'^(#{1,%d})\s+(.+)$' % max_level, content, re.MULTILINE)
    
    toc = ['<nav class="table-of-contents">']
    toc.append('<h2>Содержание</h2>')
    toc.append('<ul>')
    
    for level_marks, title in headings:
        level = len(level_marks)
        anchor = re.sub(r'[^\w\s-]', '', title.lower())
        anchor = re.sub(r'[\s_-]+', '-', anchor)
        
        indent = '  ' * (level - 1)
        toc.append(f'{indent}<li><a href="#{anchor}">{title}</a></li>')
    
    toc.append('</ul>')
    toc.append('</nav>')
    
    return '\n'.join(toc)


def sanitize_filename(filename: str) -> str:
    """
    Очищает имя файла от недопустимых символов
    
    Args:
        filename: Исходное имя файла
    
    Returns:
        Очищенное имя файла
    """
    # Удаляем недопустимые символы
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Заменяем пробелы на дефисы
    filename = re.sub(r'\s+', '-', filename)
    # Убираем множественные дефисы
    filename = re.sub(r'-+', '-', filename)
    # Приводим к нижнему регистру
    filename = filename.lower()
    
    return filename


def detect_language(text: str) -> str:
    """
    Определяет язык текста (ru или en)
    
    Args:
        text: Текст для анализа
    
    Returns:
        Код языка ('ru' или 'en')
    """
    # Простая эвристика: подсчитываем кириллические символы
    cyrillic_chars = len(re.findall(r'[а-яА-ЯёЁ]', text))
    latin_chars = len(re.findall(r'[a-zA-Z]', text))
    
    return 'ru' if cyrillic_chars > latin_chars else 'en'


class ProgressTracker:
    """Класс для отслеживания прогресса генерации"""
    
    def __init__(self, total_steps: int):
        self.total_steps = total_steps
        self.current_step = 0
    
    def step(self, message: str):
        """Увеличивает счетчик шагов и выводит сообщение"""
        self.current_step += 1
        percent = (self.current_step / self.total_steps) * 100
        print(f"[{self.current_step}/{self.total_steps}] ({percent:.0f}%) {message}")
    
    def complete(self):
        """Завершает отслеживание прогресса"""
        print("✅ Генерация завершена успешно!")

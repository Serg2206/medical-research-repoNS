
#!/usr/bin/env python3
"""
Скрипт для валидации качества рукописей
Проверяет форматирование, структуру, полноту метаданных
"""

import re
import sys
from pathlib import Path
import argparse
from typing import List, Tuple


class ManuscriptValidator:
    """Валидатор качества медицинских рукописей"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
    
    def validate_file(self, filepath: str) -> Tuple[bool, List[str], List[str]]:
        """
        Валидирует Markdown файл
        
        Returns:
            (is_valid, errors, warnings)
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            self.errors.append(f"Файл не найден: {filepath}")
            return False, self.errors, self.warnings
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Проверки
        self._check_metadata(content)
        self._check_structure(content)
        self._check_tables(content)
        self._check_figures(content)
        self._check_citations(content)
        self._check_special_boxes(content)
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings
    
    def _check_metadata(self, content: str):
        """Проверка метаданных"""
        required_fields = {
            'Автор': r'\*\*Автор:\*\*\s+(.+)',
            'Дата': r'\*\*Дата:\*\*\s+(.+)',
            'Ключевые слова': r'\*\*Ключевые слова:\*\*\s+(.+)'
        }
        
        for field, pattern in required_fields.items():
            if not re.search(pattern, content):
                self.warnings.append(f"Отсутствует поле: {field}")
    
    def _check_structure(self, content: str):
        """Проверка структуры документа"""
        # Проверка заголовка первого уровня
        if not re.search(r'^#\s+.+$', content, re.MULTILINE):
            self.errors.append("Отсутствует заголовок первого уровня (H1)")
        
        # Проверка наличия разделов
        sections = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
        if len(sections) < 3:
            self.warnings.append(f"Мало разделов: {len(sections)}. Рекомендуется минимум 5-7")
        
        # Проверка аннотации
        if 'аннотация' not in content.lower() and 'abstract' not in content.lower():
            self.warnings.append("Отсутствует аннотация")
    
    def _check_tables(self, content: str):
        """Проверка таблиц"""
        tables = re.findall(r'\|.+\|', content)
        
        if not tables:
            self.info.append("Таблицы не обнаружены")
            return
        
        # Проверка подписей таблиц
        table_captions = re.findall(r'Таблица\s+\d+\.', content)
        if len(table_captions) == 0:
            self.warnings.append("Таблицы без подписей")
        
        self.info.append(f"Найдено таблиц: {len(set(table_captions))}")
    
    def _check_figures(self, content: str):
        """Проверка рисунков"""
        figures = re.findall(r'!\[.*?\]\(.*?\)', content)
        
        if not figures:
            self.info.append("Рисунки не обнаружены")
            return
        
        # Проверка подписей рисунков
        figure_captions = re.findall(r'\*Рисунок\s+\d+\.', content)
        
        if len(figures) != len(figure_captions):
            self.warnings.append(
                f"Несоответствие количества рисунков ({len(figures)}) "
                f"и подписей ({len(figure_captions)})"
            )
        
        self.info.append(f"Найдено рисунков: {len(figures)}")
    
    def _check_citations(self, content: str):
        """Проверка цитирований"""
        # Проверка ссылок в тексте
        citations = re.findall(r'\[\d+\]', content)
        
        if citations:
            self.info.append(f"Найдено цитирований: {len(citations)}")
        else:
            self.warnings.append("Цитирования не обнаружены")
        
        # Проверка списка литературы
        if 'список литературы' not in content.lower() and 'references' not in content.lower():
            self.warnings.append("Отсутствует список литературы")
    
    def _check_special_boxes(self, content: str):
        """Проверка специальных блоков"""
        box_types = {
            'key-points': r':::key-points',
            'warning': r':::warning',
            'clinical-implications': r':::clinical-implications',
            'evidence-grading': r':::evidence-grading'
        }
        
        found_boxes = {}
        for box_type, pattern in box_types.items():
            matches = re.findall(pattern, content)
            if matches:
                found_boxes[box_type] = len(matches)
        
        if found_boxes:
            self.info.append(f"Найдены специальные блоки: {found_boxes}")
        else:
            self.info.append("Специальные блоки не используются (рекомендуется добавить)")
    
    def print_report(self):
        """Выводит отчет о валидации"""
        print("\n" + "="*60)
        print("📋 ОТЧЕТ О ВАЛИДАЦИИ РУКОПИСИ")
        print("="*60)
        
        if self.errors:
            print(f"\n❌ ОШИБКИ ({len(self.errors)}):")
            for error in self.errors:
                print(f"   • {error}")
        
        if self.warnings:
            print(f"\n⚠️  ПРЕДУПРЕЖДЕНИЯ ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        if self.info:
            print(f"\nℹ️  ИНФОРМАЦИЯ:")
            for info_msg in self.info:
                print(f"   • {info_msg}")
        
        print("\n" + "="*60)
        
        if not self.errors:
            print("✅ ВАЛИДАЦИЯ ПРОЙДЕНА УСПЕШНО")
        else:
            print("❌ ВАЛИДАЦИЯ НЕ ПРОЙДЕНА")
        print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Валидация качества медицинских рукописей'
    )
    parser.add_argument(
        'file',
        help='Путь к Markdown файлу для проверки'
    )
    
    args = parser.parse_args()
    
    validator = ManuscriptValidator()
    is_valid, errors, warnings = validator.validate_file(args.file)
    
    validator.print_report()
    
    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()

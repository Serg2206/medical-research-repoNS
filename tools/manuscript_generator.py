#!/usr/bin/env python3
"""
Профессиональный генератор научных медицинских рукописей
Преобразует Markdown в HTML с форматированием мирового класса
Основан на анализе ведущих медицинских журналов (Nature, Lancet, BMC Surgery, NCCN)
"""

import re
import json
import markdown
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import argparse


class ManuscriptGenerator:
    """Генератор профессиональных медицинских рукописей"""
    
    def __init__(self, specs_path: str = None):
        """
        Инициализация генератора
        
        Args:
            specs_path: Путь к файлу спецификаций форматирования
        """
        if specs_path is None:
            specs_path = Path(__file__).parent.parent / "training-materials" / "formatting-specifications.json"
        
        with open(specs_path, 'r', encoding='utf-8') as f:
            self.specs = json.load(f)
        
        # Настройка Markdown с расширениями
        self.md = markdown.Markdown(extensions=[
            'extra',
            'codehilite',
            'toc',
            'tables',
            'fenced_code',
            'attr_list',
            'def_list',
            'footnotes'
        ])
        
        self.figure_counter = 0
        self.table_counter = 0
        self.reference_counter = 0
    
    def process_special_boxes(self, content: str) -> str:
        """
        Обрабатывает специальные блоки контента
        
        Поддерживаемые типы:
        - ::: key-points ... :::
        - ::: warning ... :::
        - ::: clinical-implications ... :::
        - ::: evidence-grading ... :::
        """
        
        # Key Points Box
        key_points_pattern = r':::key-points\s*\n(.*?)\n:::'
        content = re.sub(
            key_points_pattern,
            self._render_key_points_box,
            content,
            flags=re.DOTALL
        )
        
        # Warning Box
        warning_pattern = r':::warning\s*\n(.*?)\n:::'
        content = re.sub(
            warning_pattern,
            self._render_warning_box,
            content,
            flags=re.DOTALL
        )
        
        # Clinical Implications
        clinical_pattern = r':::clinical-implications\s*\n(.*?)\n:::'
        content = re.sub(
            clinical_pattern,
            self._render_clinical_implications,
            content,
            flags=re.DOTALL
        )
        
        # Evidence Grading
        evidence_pattern = r':::evidence-grading\s+(\w+)\s*\n(.*?)\n:::'
        content = re.sub(
            evidence_pattern,
            self._render_evidence_grading,
            content,
            flags=re.DOTALL
        )
        
        return content
    
    def _render_key_points_box(self, match) -> str:
        """Рендеринг блока ключевых пунктов"""
        content = match.group(1) if hasattr(match, 'group') else match
        html = f'''
<div class="special-box key-points-box">
    <div class="box-title">Ключевые положения</div>
    <div class="box-content">
        {self.md.convert(content)}
    </div>
</div>
'''
        return html
    
    def _render_warning_box(self, match) -> str:
        """Рендеринг блока предупреждений"""
        content = match.group(1) if hasattr(match, 'group') else match
        html = f'''
<div class="special-box warning-box">
    <div class="box-title">⚠️ Важное предупреждение</div>
    <div class="box-content">
        {self.md.convert(content)}
    </div>
</div>
'''
        return html
    
    def _render_clinical_implications(self, match) -> str:
        """Рендеринг блока клинических выводов"""
        content = match.group(1) if hasattr(match, 'group') else match
        html = f'''
<div class="special-box clinical-implications-box">
    <div class="box-title">КЛИНИЧЕСКИЕ ВЫВОДЫ</div>
    <div class="box-content">
        {self.md.convert(content)}
    </div>
</div>
'''
        return html
    
    def _render_evidence_grading(self, match) -> str:
        """Рендеринг блока оценки уровня доказательности"""
        grade = match.group(1).lower() if hasattr(match, 'group') else 'moderate'
        content = match.group(2) if hasattr(match, 'group') else match
        
        grade_specs = self.specs['evidence_grading']['grade_system'].get(
            grade, 
            self.specs['evidence_grading']['grade_system']['moderate']
        )
        
        html = f'''
<div class="special-box evidence-grading-box" data-grade="{grade}">
    <div class="box-title">
        <span class="evidence-symbol">{grade_specs['symbol']}</span>
        Уровень доказательности: {grade.upper()}
    </div>
    <div class="box-content">
        {self.md.convert(content)}
    </div>
</div>
'''
        return html
    
    def process_tables(self, content: str) -> str:
        """Обрабатывает таблицы и добавляет профессиональное форматирование"""
        
        # Паттерн для обнаружения таблиц с заголовками
        table_pattern = r'\n(Таблица\s+\d+\.\s+.+?)\n\n(\|.+?\|(?:\n\|.+?\|)*)'
        
        def replace_table(match):
            self.table_counter += 1
            caption = match.group(1)
            table_md = match.group(2)
            
            # Конвертируем таблицу в HTML
            table_html = self.md.convert(table_md)
            
            # Оборачиваем в профессиональный контейнер
            return f'''
<div class="table-container">
    <div class="table-caption">{caption}</div>
    {table_html}
</div>
'''
        
        content = re.sub(table_pattern, replace_table, content, flags=re.DOTALL)
        return content
    
    def process_figures(self, content: str) -> str:
        """Обрабатывает рисунки и добавляет подписи"""
        
        # Паттерн для изображений с подписями
        figure_pattern = r'!\[(.*?)\]\((.*?)\)\s*\n\*Рисунок\s+(\d+)\.\s+(.*?)\*'
        
        def replace_figure(match):
            alt_text = match.group(1)
            image_path = match.group(2)
            figure_num = match.group(3)
            caption = match.group(4)
            
            return f'''
<div class="figure-container">
    <img src="{image_path}" alt="{alt_text}" class="figure-image">
    <div class="figure-caption">
        <strong>Рисунок {figure_num}.</strong> {caption}
    </div>
</div>
'''
        
        content = re.sub(figure_pattern, replace_figure, content, flags=re.MULTILINE)
        return content
    
    def generate_html(self, markdown_content: str, metadata: Dict = None) -> str:
        """
        Генерирует полный HTML документ из Markdown
        
        Args:
            markdown_content: Содержимое в формате Markdown
            metadata: Метаданные документа (название, автор, дата)
        
        Returns:
            Полный HTML документ
        """
        
        if metadata is None:
            metadata = {}
        
        # Предобработка специальных блоков
        markdown_content = self.process_special_boxes(markdown_content)
        markdown_content = self.process_tables(markdown_content)
        markdown_content = self.process_figures(markdown_content)
        
        # Конвертируем в HTML
        body_html = self.md.convert(markdown_content)
        
        # Генерируем полный документ
        html_template = self._get_html_template()
        
        html_document = html_template.format(
            title=metadata.get('title', 'Научная рукопись'),
            author=metadata.get('author', ''),
            date=metadata.get('date', datetime.now().strftime('%d.%m.%Y')),
            body=body_html
        )
        
        return html_document
    
    def _get_html_template(self) -> str:
        """Возвращает базовый HTML шаблон"""
        return '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="../tools/styles/professional-medical.css">
</head>
<body>
    <article class="manuscript">
        <header class="manuscript-header">
            <h1 class="manuscript-title">{title}</h1>
            <div class="manuscript-meta">
                <div class="author">{author}</div>
                <div class="date">{date}</div>
            </div>
        </header>
        <main class="manuscript-body">
            {body}
        </main>
    </article>
</body>
</html>'''
    
    def convert_file(self, input_path: str, output_path: str = None, metadata: Dict = None):
        """
        Конвертирует Markdown файл в HTML
        
        Args:
            input_path: Путь к входному Markdown файлу
            output_path: Путь к выходному HTML файлу (опционально)
            metadata: Метаданные документа
        """
        
        input_path = Path(input_path)
        
        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}.html"
        else:
            output_path = Path(output_path)
        
        # Читаем Markdown файл
        with open(input_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Извлекаем метаданные из контента, если не предоставлены
        if metadata is None:
            metadata = self._extract_metadata(markdown_content)
        
        # Генерируем HTML
        html_content = self.generate_html(markdown_content, metadata)
        
        # Сохраняем HTML файл
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Успешно создан: {output_path}")
        return output_path
    
    def _extract_metadata(self, content: str) -> Dict:
        """Извлекает метаданные из Markdown контента"""
        metadata = {}
        
        # Извлечение заголовка
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            metadata['title'] = title_match.group(1)
        
        # Извлечение автора
        author_match = re.search(r'\*\*Автор:\*\*\s+(.+)$', content, re.MULTILINE)
        if author_match:
            metadata['author'] = author_match.group(1)
        
        # Извлечение даты
        date_match = re.search(r'\*\*Дата:\*\*\s+(.+)$', content, re.MULTILINE)
        if date_match:
            metadata['date'] = date_match.group(1)
        
        return metadata


def main():
    """Основная функция CLI"""
    parser = argparse.ArgumentParser(
        description='Профессиональный генератор медицинских рукописей'
    )
    parser.add_argument(
        'input',
        help='Путь к входному Markdown файлу'
    )
    parser.add_argument(
        '-o', '--output',
        help='Путь к выходному HTML файлу',
        default=None
    )
    parser.add_argument(
        '--title',
        help='Заголовок документа',
        default=None
    )
    parser.add_argument(
        '--author',
        help='Автор документа',
        default=None
    )
    parser.add_argument(
        '--specs',
        help='Путь к файлу спецификаций',
        default=None
    )
    
    args = parser.parse_args()
    
    # Создаем генератор
    generator = ManuscriptGenerator(specs_path=args.specs)
    
    # Подготавливаем метаданные
    metadata = {}
    if args.title:
        metadata['title'] = args.title
    if args.author:
        metadata['author'] = args.author
    
    # Конвертируем файл
    try:
        output_path = generator.convert_file(
            args.input,
            args.output,
            metadata if metadata else None
        )
        print(f"\n🎉 Документ успешно создан!")
        print(f"📄 Выходной файл: {output_path}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())

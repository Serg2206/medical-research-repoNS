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

# Import visual components module
from visual_components import (
    ImageGallery, MultiPanelFigure, AnnotatedImage, 
    ComparisonSlider, StepByStepProcedure, SurgicalPhotoPanel,
    ImageMetadata, Annotation, PanelLayout
)


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
    
    def process_visual_content(self, content: str, base_dir: str = "") -> str:
        """
        Process all visual content syntax in the manuscript.
        
        Supported syntax:
        - :::gallery ... :::
        - :::figure-panel ... :::
        - :::annotated-image ... :::
        - :::comparison ... :::
        - :::procedure-steps ... :::
        - :::surgical-photos ... :::
        """
        content = self.process_image_gallery(content, base_dir)
        content = self.process_multi_panel_figure(content, base_dir)
        content = self.process_annotated_image(content, base_dir)
        content = self.process_comparison_slider(content, base_dir)
        content = self.process_procedure_steps(content, base_dir)
        content = self.process_surgical_photos(content, base_dir)
        
        return content
    
    def process_image_gallery(self, content: str, base_dir: str = "") -> str:
        """
        Process :::gallery ... ::: blocks
        
        Syntax:
        :::gallery columns=3 caption="Gallery title"
        - image1.jpg | Alt text 1 | Caption 1
        - image2.jpg | Alt text 2 | Caption 2
        :::
        """
        pattern = r':::gallery\s*(.*?)\n(.*?)\n:::'
        
        def replace_gallery(match):
            # Parse attributes
            attrs_str = match.group(1)
            images_str = match.group(2)
            
            columns = 3
            caption = None
            enable_lightbox = True
            
            # Parse attributes
            if 'columns=' in attrs_str:
                columns_match = re.search(r'columns=(\d+)', attrs_str)
                if columns_match:
                    columns = int(columns_match.group(1))
            
            if 'caption=' in attrs_str:
                caption_match = re.search(r'caption="([^"]+)"', attrs_str)
                if caption_match:
                    caption = caption_match.group(1)
            
            if 'lightbox=false' in attrs_str:
                enable_lightbox = False
            
            # Parse images
            images = []
            for line in images_str.strip().split('\n'):
                if line.startswith('- '):
                    parts = [p.strip() for p in line[2:].split('|')]
                    if len(parts) >= 2:
                        img_path = parts[0]
                        alt_text = parts[1]
                        img_caption = parts[2] if len(parts) > 2 else None
                        
                        images.append(ImageMetadata(
                            path=img_path,
                            alt_text=alt_text,
                            caption=img_caption
                        ))
            
            # Generate gallery HTML
            gallery = ImageGallery(
                images=images,
                columns=columns,
                enable_lightbox=enable_lightbox,
                caption=caption
            )
            
            return gallery.generate_html()
        
        return re.sub(pattern, replace_gallery, content, flags=re.DOTALL)
    
    def process_multi_panel_figure(self, content: str, base_dir: str = "") -> str:
        """
        Process :::figure-panel ... ::: blocks
        
        Syntax:
        :::figure-panel layout=2x2 number="1" caption="Multi-panel figure"
        - A: image1.jpg | Alt text 1 | Panel A caption
        - B: image2.jpg | Alt text 2 | Panel B caption
        :::
        """
        pattern = r':::figure-panel\s*(.*?)\n(.*?)\n:::'
        
        def replace_panel(match):
            attrs_str = match.group(1)
            panels_str = match.group(2)
            
            # Parse attributes
            layout = PanelLayout.GRID_2x2
            figure_number = None
            caption = None
            
            if 'layout=' in attrs_str:
                layout_match = re.search(r'layout=([\dx]+)', attrs_str)
                if layout_match:
                    layout_str = layout_match.group(1).upper()
                    try:
                        layout = PanelLayout(f"GRID_{layout_str.replace('X', 'x')}")
                    except ValueError:
                        layout = PanelLayout.GRID_2x2
            
            if 'number=' in attrs_str:
                number_match = re.search(r'number="([^"]+)"', attrs_str)
                if number_match:
                    figure_number = number_match.group(1)
                else:
                    self.figure_counter += 1
                    figure_number = str(self.figure_counter)
            
            if 'caption=' in attrs_str:
                caption_match = re.search(r'caption="([^"]+)"', attrs_str)
                if caption_match:
                    caption = caption_match.group(1)
            
            # Parse panels
            panels = []
            for line in panels_str.strip().split('\n'):
                if line.startswith('- '):
                    # Format: - A: image.jpg | Alt text | Caption
                    line_content = line[2:].strip()
                    
                    label = None
                    if ':' in line_content:
                        label, rest = line_content.split(':', 1)
                        label = label.strip()
                        line_content = rest.strip()
                    
                    parts = [p.strip() for p in line_content.split('|')]
                    if len(parts) >= 2:
                        img_path = parts[0]
                        alt_text = parts[1]
                        panel_caption = parts[2] if len(parts) > 2 else None
                        
                        panels.append(ImageMetadata(
                            path=img_path,
                            alt_text=alt_text,
                            caption=panel_caption,
                            label=label
                        ))
            
            # Generate multi-panel figure HTML
            figure = MultiPanelFigure(
                panels=panels,
                layout=layout,
                figure_number=figure_number,
                caption=caption,
                auto_label=(not any(p.label for p in panels))
            )
            
            return figure.generate_html()
        
        return re.sub(pattern, replace_panel, content, flags=re.DOTALL)
    
    def process_annotated_image(self, content: str, base_dir: str = "") -> str:
        """
        Process :::annotated-image ... ::: blocks
        
        Syntax:
        :::annotated-image number="2" caption="Annotated surgical view"
        image: surgery.jpg | Alt text for surgery
        annotations:
        - arrow: 50, 30 | Target structure | red
        - circle: 60, 40 | yellow
        - label: 70, 20 | Important landmark | white
        :::
        """
        pattern = r':::annotated-image\s*(.*?)\n(.*?)\n:::'
        
        def replace_annotated(match):
            attrs_str = match.group(1)
            content_str = match.group(2)
            
            # Parse attributes
            figure_number = None
            if 'number=' in attrs_str:
                number_match = re.search(r'number="([^"]+)"', attrs_str)
                if number_match:
                    figure_number = number_match.group(1)
            
            # Parse image and annotations
            image = None
            annotations = []
            
            lines = content_str.strip().split('\n')
            in_annotations = False
            
            for line in lines:
                line = line.strip()
                
                if line.startswith('image:'):
                    img_content = line[6:].strip()
                    parts = [p.strip() for p in img_content.split('|')]
                    if len(parts) >= 2:
                        image = ImageMetadata(
                            path=parts[0],
                            alt_text=parts[1],
                            caption=parts[2] if len(parts) > 2 else None
                        )
                
                elif line.startswith('annotations:'):
                    in_annotations = True
                
                elif in_annotations and line.startswith('- '):
                    # Format: - type: x, y | text | color
                    ann_content = line[2:].strip()
                    
                    # Parse annotation type and coordinates
                    if ':' in ann_content:
                        ann_type, rest = ann_content.split(':', 1)
                        ann_type = ann_type.strip()
                        rest = rest.strip()
                        
                        parts = [p.strip() for p in rest.split('|')]
                        
                        # Parse coordinates
                        coords = parts[0].split(',')
                        x = float(coords[0].strip()) if len(coords) > 0 else 50
                        y = float(coords[1].strip()) if len(coords) > 1 else 50
                        
                        text = parts[1] if len(parts) > 1 else None
                        color = parts[2] if len(parts) > 2 else "red"
                        
                        annotations.append(Annotation(
                            type=ann_type,
                            text=text,
                            x=x,
                            y=y,
                            color=color
                        ))
            
            if image:
                # Generate annotated image HTML
                annotated = AnnotatedImage(
                    image=image,
                    annotations=annotations,
                    figure_number=figure_number
                )
                return annotated.generate_html()
            
            return match.group(0)  # Return original if parsing failed
        
        return re.sub(pattern, replace_annotated, content, flags=re.DOTALL)
    
    def process_comparison_slider(self, content: str, base_dir: str = "") -> str:
        """
        Process :::comparison ... ::: blocks
        
        Syntax:
        :::comparison number="3" caption="Before and after treatment"
        before: before.jpg | Pre-operative image
        after: after.jpg | Post-operative image
        :::
        """
        pattern = r':::comparison\s*(.*?)\n(.*?)\n:::'
        
        def replace_comparison(match):
            attrs_str = match.group(1)
            content_str = match.group(2)
            
            # Parse attributes
            figure_number = None
            caption = None
            
            if 'number=' in attrs_str:
                number_match = re.search(r'number="([^"]+)"', attrs_str)
                if number_match:
                    figure_number = number_match.group(1)
            
            if 'caption=' in attrs_str:
                caption_match = re.search(r'caption="([^"]+)"', attrs_str)
                if caption_match:
                    caption = caption_match.group(1)
            
            # Parse before/after images
            before_image = None
            after_image = None
            
            for line in content_str.strip().split('\n'):
                line = line.strip()
                
                if line.startswith('before:'):
                    img_content = line[7:].strip()
                    parts = [p.strip() for p in img_content.split('|')]
                    if len(parts) >= 2:
                        before_image = ImageMetadata(
                            path=parts[0],
                            alt_text=parts[1]
                        )
                
                elif line.startswith('after:'):
                    img_content = line[6:].strip()
                    parts = [p.strip() for p in img_content.split('|')]
                    if len(parts) >= 2:
                        after_image = ImageMetadata(
                            path=parts[0],
                            alt_text=parts[1]
                        )
            
            if before_image and after_image:
                # Generate comparison slider HTML
                comparison = ComparisonSlider(
                    before_image=before_image,
                    after_image=after_image,
                    caption=caption,
                    figure_number=figure_number
                )
                return comparison.generate_html()
            
            return match.group(0)
        
        return re.sub(pattern, replace_comparison, content, flags=re.DOTALL)
    
    def process_procedure_steps(self, content: str, base_dir: str = "") -> str:
        """
        Process :::procedure-steps ... ::: blocks
        
        Syntax:
        :::procedure-steps title="Laparoscopic Technique" number="4" layout="vertical"
        - step1.jpg | Initial trocar placement | Port insertion at umbilicus
        - step2.jpg | Dissection phase | Mobilization of greater curvature
        - step3.jpg | Resection | Gastric transection
        :::
        """
        pattern = r':::procedure-steps\s*(.*?)\n(.*?)\n:::'
        
        def replace_procedure(match):
            attrs_str = match.group(1)
            steps_str = match.group(2)
            
            # Parse attributes
            title = None
            figure_number = None
            layout = "vertical"
            
            if 'title=' in attrs_str:
                title_match = re.search(r'title="([^"]+)"', attrs_str)
                if title_match:
                    title = title_match.group(1)
            
            if 'number=' in attrs_str:
                number_match = re.search(r'number="([^"]+)"', attrs_str)
                if number_match:
                    figure_number = number_match.group(1)
            
            if 'layout=' in attrs_str:
                layout_match = re.search(r'layout="([^"]+)"', attrs_str)
                if layout_match:
                    layout = layout_match.group(1)
            
            # Parse steps
            steps = []
            for line in steps_str.strip().split('\n'):
                if line.startswith('- '):
                    parts = [p.strip() for p in line[2:].split('|')]
                    if len(parts) >= 2:
                        img_path = parts[0]
                        alt_text = parts[1]
                        step_caption = parts[2] if len(parts) > 2 else None
                        
                        steps.append(ImageMetadata(
                            path=img_path,
                            alt_text=alt_text,
                            caption=step_caption
                        ))
            
            # Generate procedure steps HTML
            procedure = StepByStepProcedure(
                steps=steps,
                title=title,
                layout=layout,
                figure_number=figure_number
            )
            
            return procedure.generate_html()
        
        return re.sub(pattern, replace_procedure, content, flags=re.DOTALL)
    
    def process_surgical_photos(self, content: str, base_dir: str = "") -> str:
        """
        Process :::surgical-photos ... ::: blocks
        
        Syntax:
        :::surgical-photos title="Intraoperative Findings" number="5" columns=2
        - photo1.jpg | Surgical view 1 | Tumor location
        - photo2.jpg | Surgical view 2 | After resection
        :::
        """
        pattern = r':::surgical-photos\s*(.*?)\n(.*?)\n:::'
        
        def replace_surgical(match):
            attrs_str = match.group(1)
            photos_str = match.group(2)
            
            # Parse attributes
            title = None
            figure_number = None
            columns = 2
            
            if 'title=' in attrs_str:
                title_match = re.search(r'title="([^"]+)"', attrs_str)
                if title_match:
                    title = title_match.group(1)
            
            if 'number=' in attrs_str:
                number_match = re.search(r'number="([^"]+)"', attrs_str)
                if number_match:
                    figure_number = number_match.group(1)
            
            if 'columns=' in attrs_str:
                columns_match = re.search(r'columns=(\d+)', attrs_str)
                if columns_match:
                    columns = int(columns_match.group(1))
            
            # Parse photos
            photos = []
            for line in photos_str.strip().split('\n'):
                if line.startswith('- '):
                    parts = [p.strip() for p in line[2:].split('|')]
                    if len(parts) >= 2:
                        img_path = parts[0]
                        alt_text = parts[1]
                        photo_caption = parts[2] if len(parts) > 2 else None
                        
                        photos.append(ImageMetadata(
                            path=img_path,
                            alt_text=alt_text,
                            caption=photo_caption
                        ))
            
            # Generate surgical photo panel HTML
            panel = SurgicalPhotoPanel(
                photos=photos,
                title=title,
                columns=columns,
                figure_number=figure_number
            )
            
            return panel.generate_html()
        
        return re.sub(pattern, replace_surgical, content, flags=re.DOTALL)
    
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
        markdown_content = self.process_visual_content(markdown_content)  # NEW: Process visual content
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
    <script src="../tools/scripts/visual-interactions.js"></script>
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

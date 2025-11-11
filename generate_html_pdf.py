#!/usr/bin/env python3
"""Generate HTML and PDF from the Russian manuscript"""

import markdown
from pathlib import Path
import subprocess

def generate_html():
    """Generate HTML from markdown"""
    
    # Read the manuscript
    with open('manuscripts/proximal-gastrectomy-double-tract-ru.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Convert to HTML with extensions
    md = markdown.Markdown(extensions=[
        'extra',
        'codehilite',
        'toc',
        'tables',
        'fenced_code',
        'attr_list',
        'def_list',
        'footnotes',
        'nl2br'
    ])
    
    html_body = md.convert(content)
    
    # Read the CSS template
    css_styles = """
        body {
            font-family: 'Times New Roman', Times, serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
            color: #333;
        }
        
        h1 {
            color: #003366;
            border-bottom: 3px solid #003366;
            padding-bottom: 10px;
            margin-top: 40px;
        }
        
        h2 {
            color: #0066cc;
            margin-top: 30px;
            border-bottom: 1px solid #0066cc;
            padding-bottom: 5px;
        }
        
        h3 {
            color: #0088cc;
            margin-top: 25px;
        }
        
        h4 {
            color: #00aacc;
            margin-top: 20px;
        }
        
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
            border: 1px solid #ddd;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        
        table, th, td {
            border: 1px solid #ddd;
        }
        
        th {
            background-color: #003366;
            color: white;
            padding: 12px;
            text-align: left;
        }
        
        td {
            padding: 10px;
        }
        
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        
        .multi-panel-figure {
            margin: 30px 0;
            padding: 20px;
            border: 2px solid #0066cc;
            background-color: #f9f9f9;
        }
        
        .panel-grid {
            display: grid;
            gap: 20px;
            margin: 20px 0;
        }
        
        .panel-grid[data-rows="2"][data-cols="2"] {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .panel-grid[data-rows="1"] {
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        }
        
        .panel-item {
            position: relative;
            border: 1px solid #ddd;
            padding: 10px;
            background-color: white;
        }
        
        .panel-label {
            position: absolute;
            top: 10px;
            left: 10px;
            background-color: rgba(0, 51, 102, 0.8);
            color: white;
            padding: 5px 10px;
            font-weight: bold;
            border-radius: 3px;
        }
        
        .panel-caption {
            font-size: 0.9em;
            color: #666;
            margin-top: 10px;
            font-style: italic;
        }
        
        figcaption {
            font-size: 0.95em;
            color: #444;
            margin-top: 15px;
            padding: 10px;
            background-color: #f0f0f0;
            border-left: 4px solid #0066cc;
        }
        
        .procedure-container {
            margin: 30px 0;
        }
        
        .procedure-title {
            color: #003366;
            text-align: center;
            margin-bottom: 20px;
        }
        
        .procedure-steps {
            display: grid;
            gap: 25px;
        }
        
        .grid-layout .procedure-steps {
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        }
        
        .procedure-step {
            border: 2px solid #0066cc;
            padding: 15px;
            background-color: #fafafa;
            border-radius: 5px;
        }
        
        .step-number {
            background-color: #003366;
            color: white;
            padding: 5px 15px;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 10px;
            border-radius: 3px;
        }
        
        .step-caption {
            font-size: 0.9em;
            color: #555;
            margin-top: 10px;
            line-height: 1.4;
        }
        
        blockquote {
            border-left: 4px solid #0066cc;
            padding-left: 20px;
            margin: 20px 0;
            background-color: #f0f8ff;
            padding: 15px 20px;
        }
        
        @media print {
            body {
                font-size: 11pt;
            }
            
            h1 {
                page-break-before: always;
            }
            
            h1:first-of-type {
                page-break-before: avoid;
            }
            
            .multi-panel-figure, .procedure-container {
                page-break-inside: avoid;
            }
        }
    """
    
    # Create complete HTML document
    html_template = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Проксимальная субтотальная резекция желудка с реконструкцией по типу «двойной тракт»</title>
    <style>
        """ + css_styles + """
    </style>
</head>
<body>
    """ + html_body + """
    
    <script>
        // Simple lightbox functionality for images
        document.addEventListener('DOMContentLoaded', function() {
            const images = document.querySelectorAll('img');
            images.forEach(img => {
                img.style.cursor = 'pointer';
                img.addEventListener('click', function() {
                    window.open(this.src, '_blank');
                });
            });
        });
    </script>
</body>
</html>
"""
    
    # Save HTML
    output_file = 'manuscripts/proximal-gastrectomy-double-tract-ru.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f'✓ HTML файл создан: {output_file}')
    
    # Get file size
    file_size = Path(output_file).stat().st_size / 1024  # KB
    print(f'  Размер: {file_size:.1f} KB')
    
    return output_file


def generate_pdf():
    """Generate PDF from HTML using wkhtmltopdf"""
    
    html_file = 'manuscripts/proximal-gastrectomy-double-tract-ru.html'
    pdf_file = 'manuscripts/proximal-gastrectomy-double-tract-ru.pdf'
    
    # Check if wkhtmltopdf is installed
    try:
        result = subprocess.run(['which', 'wkhtmltopdf'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print('⚠ wkhtmltopdf не установлен. Установка...')
            subprocess.run(['sudo', 'apt-get', 'update', '-qq'], check=False)
            subprocess.run(['sudo', 'apt-get', 'install', '-y', '-qq', 'wkhtmltopdf'], 
                         check=False)
    except Exception as e:
        print(f'⚠ Не удалось установить wkhtmltopdf: {e}')
        print('  PDF не будет создан, но HTML доступен')
        return None
    
    # Generate PDF
    try:
        cmd = [
            'wkhtmltopdf',
            '--enable-local-file-access',
            '--encoding', 'UTF-8',
            '--page-size', 'A4',
            '--margin-top', '20mm',
            '--margin-bottom', '20mm',
            '--margin-left', '20mm',
            '--margin-right', '20mm',
            html_file,
            pdf_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f'✓ PDF файл создан: {pdf_file}')
            file_size = Path(pdf_file).stat().st_size / 1024  # KB
            print(f'  Размер: {file_size:.1f} KB')
            return pdf_file
        else:
            print(f'⚠ Ошибка создания PDF: {result.stderr}')
            return None
            
    except Exception as e:
        print(f'⚠ Ошибка при создании PDF: {e}')
        return None


if __name__ == "__main__":
    print("Генерация HTML и PDF выходных файлов...")
    print("=" * 70)
    
    # Generate HTML
    html_file = generate_html()
    
    print()
    
    # Generate PDF
    pdf_file = generate_pdf()
    
    print()
    print("=" * 70)
    
    if html_file and pdf_file:
        print("✓ Все выходные файлы успешно созданы!")
    elif html_file:
        print("✓ HTML создан. PDF не создан (установите wkhtmltopdf для генерации PDF)")
    else:
        print("✗ Ошибка создания выходных файлов")

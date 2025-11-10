
#!/usr/bin/env python3
"""
Скрипт для массовой конвертации Markdown рукописей в HTML
"""

import os
import sys
from pathlib import Path
import argparse
from manuscript_generator import ManuscriptGenerator

def batch_convert(input_dir, output_dir, recursive=True):
    """
    Массовая конвертация всех Markdown файлов в директории
    
    Args:
        input_dir: Директория с Markdown файлами
        output_dir: Директория для HTML файлов
        recursive: Рекурсивный поиск в поддиректориях
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Создаем генератор
    generator = ManuscriptGenerator()
    
    # Находим все Markdown файлы
    pattern = '**/*.md' if recursive else '*.md'
    md_files = list(input_path.glob(pattern))
    
    if not md_files:
        print(f"⚠️  В директории {input_dir} не найдено Markdown файлов")
        return
    
    print(f"📚 Найдено файлов для конвертации: {len(md_files)}")
    print()
    
    success_count = 0
    error_count = 0
    
    for i, md_file in enumerate(md_files, 1):
        print(f"[{i}/{len(md_files)}] Обработка: {md_file.name}")
        
        try:
            # Формируем путь для выходного файла
            relative_path = md_file.relative_to(input_path)
            output_file = output_path / relative_path.parent / f"{md_file.stem}.html"
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Конвертируем файл
            generator.convert_file(str(md_file), str(output_file))
            success_count += 1
            
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
            error_count += 1
        
        print()
    
    # Итоговая статистика
    print("=" * 60)
    print("📊 ИТОГИ ОБРАБОТКИ:")
    print(f"   ✅ Успешно конвертировано: {success_count}")
    if error_count > 0:
        print(f"   ❌ Ошибок: {error_count}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description='Массовая конвертация Markdown рукописей в HTML'
    )
    parser.add_argument(
        'input_dir',
        help='Директория с Markdown файлами'
    )
    parser.add_argument(
        '-o', '--output-dir',
        help='Директория для HTML файлов',
        default='generated_manuscripts'
    )
    parser.add_argument(
        '--no-recursive',
        help='Не искать в поддиректориях',
        action='store_true'
    )
    
    args = parser.parse_args()
    
    batch_convert(
        args.input_dir,
        args.output_dir,
        recursive=not args.no_recursive
    )


if __name__ == '__main__':
    main()

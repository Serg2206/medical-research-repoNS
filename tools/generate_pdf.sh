
#!/bin/bash
#
# Скрипт для генерации PDF из HTML рукописей
# Использует wkhtmltopdf или weasyprint
#

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функция вывода с цветом
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка аргументов
if [ $# -lt 1 ]; then
    echo "Использование: $0 <input.html> [output.pdf]"
    echo ""
    echo "Примеры:"
    echo "  $0 manuscript.html"
    echo "  $0 manuscript.html output.pdf"
    echo "  $0 generated_manuscripts/*.html  # массовая конвертация"
    exit 1
fi

# Проверка наличия инструментов
check_tools() {
    if command -v wkhtmltopdf &> /dev/null; then
        TOOL="wkhtmltopdf"
        print_info "Используется: wkhtmltopdf"
    elif command -v weasyprint &> /dev/null; then
        TOOL="weasyprint"
        print_info "Используется: weasyprint"
    elif command -v chromium-browser &> /dev/null; then
        TOOL="chromium"
        print_info "Используется: chromium"
    else
        print_error "Не найдены инструменты для генерации PDF"
        echo ""
        echo "Установите один из:"
        echo "  sudo apt-get install wkhtmltopdf"
        echo "  pip install weasyprint"
        echo "  sudo apt-get install chromium-browser"
        exit 1
    fi
}

# Конвертация одного файла
convert_single() {
    local input="$1"
    local output="$2"
    
    if [ -z "$output" ]; then
        output="${input%.html}.pdf"
    fi
    
    print_info "Конвертация: $input -> $output"
    
    case $TOOL in
        wkhtmltopdf)
            wkhtmltopdf \
                --page-size A4 \
                --margin-top 20mm \
                --margin-bottom 20mm \
                --margin-left 25mm \
                --margin-right 25mm \
                --enable-local-file-access \
                --print-media-type \
                "$input" "$output"
            ;;
        weasyprint)
            weasyprint "$input" "$output"
            ;;
        chromium)
            chromium-browser \
                --headless \
                --disable-gpu \
                --print-to-pdf="$output" \
                --no-margins \
                "$input"
            ;;
    esac
    
    if [ $? -eq 0 ]; then
        print_info "✅ Успешно создан: $output"
    else
        print_error "❌ Ошибка при создании: $output"
        return 1
    fi
}

# Основная логика
check_tools

# Обработка аргументов
if [ $# -eq 1 ]; then
    # Один входной файл
    convert_single "$1"
elif [ $# -eq 2 ]; then
    # Входной и выходной файл
    convert_single "$1" "$2"
else
    # Массовая конвертация
    print_info "Массовая конвертация ${#@} файлов..."
    echo ""
    
    success=0
    failed=0
    
    for file in "$@"; do
        if convert_single "$file"; then
            ((success++))
        else
            ((failed++))
        fi
        echo ""
    done
    
    echo "========================================"
    echo "ИТОГИ:"
    echo "  ✅ Успешно: $success"
    if [ $failed -gt 0 ]; then
        echo "  ❌ Ошибок: $failed"
    fi
    echo "========================================"
fi

# Manuscript Generator

## 📋 Overview

**Manuscript Generator** is a comprehensive Python tool designed to automate the generation of scientific medical documents from structured markdown files. It provides professional formatting, automatic table of contents, bibliography management, and exports to multiple formats compatible with Microsoft Publisher (DOCX, HTML, PDF).

### Key Features

- ✅ **Multi-format Export**: Generate DOCX, HTML, and PDF documents simultaneously
- ✅ **Automatic Numbering**: Sections, figures, and tables with hierarchical numbering
- ✅ **Table of Contents**: Auto-generated TOC with customizable depth
- ✅ **Bibliography Management**: Automatic reference extraction and formatting
- ✅ **Image & Table Support**: Insert figures and tables with captions and numbering
- ✅ **Configurable Styling**: Customizable fonts, margins, and formatting via YAML
- ✅ **CLI Interface**: Easy-to-use command-line interface
- ✅ **Publisher Compatible**: Optimized for Microsoft Publisher workflows
- ✅ **GitHub Actions Ready**: Easy integration with CI/CD pipelines

---

## 🚀 Quick Start

### Installation

1. **Clone or download the repository:**
```bash
cd ~
# Files should be in your home directory:
# - manuscript_generator.py
# - config.yaml
# - requirements.txt
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Make the script executable (optional):**
```bash
chmod +x manuscript_generator.py
```

### Basic Usage

Generate documents from your markdown file:

```bash
python manuscript_generator.py double_tract_research.md
```

This will create DOCX, HTML, and PDF files in the `./output` directory.

---

## 📖 Usage Examples

### Example 1: Generate with Default Configuration

```bash
python manuscript_generator.py double_tract_research.md
```

**Output:**
```
output/
├── double_tract_research.docx
├── double_tract_research.html
└── double_tract_research.pdf
```

### Example 2: Use Custom Configuration

```bash
python manuscript_generator.py double_tract_research.md -c config.yaml
```

### Example 3: Generate Specific Formats Only

Generate only DOCX and PDF:

```bash
python manuscript_generator.py double_tract_research.md -f docx pdf
```

### Example 4: Specify Custom Output Directory

```bash
python manuscript_generator.py double_tract_research.md -o ./manuscripts
```

### Example 5: Verbose Mode for Debugging

```bash
python manuscript_generator.py double_tract_research.md -v
```

### Example 6: Complete Command with All Options

```bash
python manuscript_generator.py double_tract_research.md \
  --config config.yaml \
  --output ./output/medical_docs \
  --formats docx pdf \
  --verbose
```

---

## ⚙️ Configuration

The tool uses a YAML configuration file (`config.yaml`) to control document formatting and generation options.

### Configuration File Structure

```yaml
# Document metadata
document:
  title: "Scientific Medical Manuscript"
  author: "Research Team"
  date: "2025-11-10"
  language: "en"

# Formatting settings
formatting:
  font_family: "Times New Roman"
  font_size: 12
  line_spacing: 1.5
  margins:
    top: 2.54
    bottom: 2.54
    left: 2.54
    right: 2.54

# Numbering options
numbering:
  sections: true
  figures: true
  tables: true
  format: "decimal"

# Table of Contents
toc:
  enabled: true
  depth: 3
  page_break_after: true

# Bibliography
bibliography:
  enabled: true
  style: "numbered"
  title: "References"

# Output formats
output:
  formats:
    - docx
    - html
    - pdf
  output_dir: "./output"
```

### Customizing Configuration

1. **Copy the default config:**
```bash
cp config.yaml my_config.yaml
```

2. **Edit settings as needed**

3. **Use your custom config:**
```bash
python manuscript_generator.py input.md -c my_config.yaml
```

---

## 📝 Markdown Format Guidelines

### Document Structure

Your markdown file should follow this structure:

```markdown
# Main Title

**Metadata Field:** Value
**Date:** 2025-11-10

---

## 1. Introduction

Content for the introduction section...

### 1.1 Background

Subsection content...

## 2. Methods

Content for methods section...

---
### References

[Reference 1 Title](https://url.com)
[Reference 2 Title](https://url2.com)
```

### Supported Markdown Features

- **Headers**: `#`, `##`, `###` (up to 6 levels)
- **Bold text**: `**bold**`
- **Italic text**: `*italic*`
- **Lists**: Unordered (`-`, `*`) and ordered (`1.`, `2.`)
- **Links**: `[text](url)`
- **Images**: `![caption](path/to/image.png)`
- **Tables**: Standard markdown tables
- **Horizontal rules**: `---`

### Best Practices

1. **Use hierarchical headings** (don't skip levels)
2. **Add metadata** at the top using bold labels
3. **Include a references section** at the end
4. **Use descriptive image captions**
5. **Keep content well-structured** with clear sections

---

## 🎨 Output Formats

### DOCX (Microsoft Word)

- **Compatible with**: Microsoft Word, LibreOffice, Google Docs
- **Features**: Full formatting, styles, TOC fields
- **Publisher Ready**: Can be imported directly into Microsoft Publisher
- **Editable**: Can be further edited in Word

### HTML

- **Compatible with**: All web browsers
- **Features**: Responsive design, print-optimized CSS
- **Use cases**: Web publishing, online documentation
- **Portable**: Single file with embedded styles

### PDF

- **Compatible with**: All PDF readers
- **Features**: Print-ready, embedded fonts, hyperlinks
- **Use cases**: Final distribution, archival
- **Professional**: High-quality typography

---

## 🔧 Command-Line Interface

### Full CLI Reference

```
usage: manuscript_generator.py [-h] [-c CONFIG] [-o OUTPUT] 
                               [-f {docx,html,pdf} [{docx,html,pdf} ...]]
                               [-v] input

positional arguments:
  input                 Input markdown file path

optional arguments:
  -h, --help            Show this help message and exit
  -c CONFIG, --config CONFIG
                        Configuration file path (YAML)
  -o OUTPUT, --output OUTPUT
                        Output directory
  -f {docx,html,pdf} [{docx,html,pdf} ...], --formats {docx,html,pdf} [{docx,html,pdf} ...]
                        Output formats (default: all)
  -v, --verbose         Enable verbose logging
```

---

## 🔗 GitHub Actions Integration

### Workflow Example

Create `.github/workflows/generate-docs.yml`:

```yaml
name: Generate Documentation

on:
  push:
    paths:
      - '**.md'
      - 'research/**'
  workflow_dispatch:

jobs:
  generate-docs:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Generate documents
        run: |
          python manuscript_generator.py double_tract_research.md \
            --config config.yaml \
            --output ./docs-generated \
            --formats docx pdf
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: generated-documents
          path: docs-generated/
      
      - name: Commit generated files
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git add docs-generated/
          git commit -m "📄 Auto-generated documentation [automated]" || echo "No changes"
          git push || echo "No changes to push"
```

### Integration with Existing Workflow

If you have an existing workflow (like `docs-improver.yml`), add this step:

```yaml
- name: Generate formatted documents
  run: |
    python ~/manuscript_generator.py docs-generated/README.md \
      --config ~/config.yaml \
      --formats docx pdf
```

---

## 🏥 Medical Research Use Case

### Example: Double Tract Reconstruction Research

The tool was designed specifically for medical oncology research documentation:

```bash
# Generate comprehensive research document
python manuscript_generator.py ~/double_tract_research.md \
  --config ~/config.yaml \
  --output ~/medical-docs \
  --formats docx pdf

# Output:
# - Professional DOCX for manuscript submission
# - PDF for peer review and distribution
# - HTML for online repository
```

**Features for Medical Research:**

- ✅ Automatic section numbering (1, 1.1, 1.1.1)
- ✅ Bibliography with medical journal format
- ✅ Figure and table numbering
- ✅ Table of contents with page numbers
- ✅ Professional typography for publication

---

## 📚 Advanced Features

### Custom Styling

Modify `config.yaml` to customize document appearance:

```yaml
styles:
  heading1:
    font_size: 18
    bold: true
    color: "1a4d2e"  # Dark green
    space_before: 30
    space_after: 15
  
  body:
    font_size: 11
    alignment: "justify"
    first_line_indent: 0.5
```

### Bibliography Styles

Supported citation styles:

- **numbered**: `[1], [2], [3]`
- **apa**: American Psychological Association
- **mla**: Modern Language Association

### Figure and Table Management

Automatic detection and numbering:

```markdown
![Survival Curves for DTR vs Total Gastrectomy](figures/survival_curve.png)

Table caption will be auto-generated as "Table 1"
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Error for WeasyPrint

**Problem:**
```
ImportError: cannot import name 'HTML' from 'weasyprint'
```

**Solution:**
```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get install -y \
  python3-dev \
  python3-pip \
  python3-setuptools \
  python3-wheel \
  python3-cffi \
  libcairo2 \
  libpango-1.0-0 \
  libpangocairo-1.0-0 \
  libgdk-pixbuf2.0-0 \
  libffi-dev \
  shared-mime-info

# Reinstall WeasyPrint
pip install --upgrade weasyprint
```

#### 2. Font Not Found

**Problem:** Specified font is not available

**Solution:** Use system fonts or install custom fonts:
```bash
# List available fonts
fc-list | grep "Times"

# Or use alternative fonts in config.yaml
font_family: "Liberation Serif"  # Instead of Times New Roman
```

#### 3. Encoding Errors

**Problem:** `UnicodeDecodeError` when reading markdown

**Solution:** Ensure your markdown file is UTF-8 encoded:
```bash
# Convert to UTF-8
iconv -f ISO-8859-1 -t UTF-8 input.md > input_utf8.md
```

---

## 🧪 Testing

### Test the Installation

```bash
# Quick test
python manuscript_generator.py --help

# Generate sample document
echo "# Test Document

## Introduction
This is a test.

### References
[Test Reference](https://example.com)
" > test.md

python manuscript_generator.py test.md
```

### Verify Output

Check the `./output` directory for generated files:
```bash
ls -lh output/
```

---

## 📦 Project Structure

```
~/
├── manuscript_generator.py  # Main script
├── config.yaml              # Configuration file
├── requirements.txt         # Python dependencies
├── README.md                # This documentation
├── double_tract_research.md # Research content
└── output/                  # Generated documents
    ├── *.docx
    ├── *.html
    └── *.pdf
```

---

## 🤝 Contributing

### Extending the Tool

To add new export formats:

1. Create a new generator class inheriting from `DocumentGenerator`
2. Implement the `generate()` method
3. Register in `ManuscriptGenerator.generate()`

Example:
```python
class MarkdownGenerator(DocumentGenerator):
    def generate(self, output_path: Path):
        # Implementation
        pass
```

---

## 📄 License

MIT License - Free to use for research and commercial purposes.

---

## 🆘 Support

### Getting Help

1. Check the troubleshooting section above
2. Review configuration examples
3. Run with `--verbose` flag for detailed logs
4. Check the GitHub repository issues

### Reporting Issues

When reporting issues, include:
- Python version: `python --version`
- OS information
- Error message with `--verbose` output
- Sample markdown file (if possible)

---

## 🔮 Future Enhancements

Planned features:

- [ ] BibTeX bibliography integration
- [ ] LaTeX export support
- [ ] Advanced table formatting
- [ ] Template system for different document types
- [ ] Cross-reference support (see Section X)
- [ ] Citation manager integration (Zotero, Mendeley)
- [ ] Equation rendering (MathJax/KaTeX)
- [ ] Multi-language support with translations

---

## 📞 Contact

For questions about medical research documentation workflows:
- Repository: See GitHub workflow integration
- Documentation: This README file

---

**Version:** 1.0.0  
**Last Updated:** November 10, 2025  
**Maintainer:** Medical Research Documentation System

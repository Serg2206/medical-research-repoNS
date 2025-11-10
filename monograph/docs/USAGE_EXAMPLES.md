# Manuscript Generator - Usage Examples

## Quick Reference

### Basic Commands

```bash
# Generate all formats (DOCX, HTML, PDF)
python manuscript_generator.py research.md

# Generate specific formats only
python manuscript_generator.py research.md -f docx pdf

# Use custom configuration
python manuscript_generator.py research.md -c my_config.yaml

# Specify output directory
python manuscript_generator.py research.md -o ./publications

# Verbose mode for debugging
python manuscript_generator.py research.md -v
```

---

## Example 1: Medical Research Paper

**Command:**
```bash
python manuscript_generator.py double_tract_research.md \
  --config config.yaml \
  --output ./medical-papers \
  --formats docx pdf
```

**Result:**
- `medical-papers/double_tract_research.docx` - Editable Word document
- `medical-papers/double_tract_research.pdf` - Print-ready PDF

**Use Case:** Preparing manuscript for journal submission

---

## Example 2: Conference Abstract

**Configuration:** `config_abstract.yaml`
```yaml
document:
  title: "Conference Abstract"
  
formatting:
  font_size: 11
  margins:
    top: 2.0
    bottom: 2.0
    left: 2.0
    right: 2.0

toc:
  enabled: false  # No TOC for abstracts

bibliography:
  style: "numbered"

output:
  formats: ['pdf']
```

**Command:**
```bash
python manuscript_generator.py conference_abstract.md \
  -c config_abstract.yaml \
  -f pdf
```

---

## Example 3: Technical Report with Images

**Markdown File:** `technical_report.md`
```markdown
# Technical Report: DTR Surgical Outcomes

## Introduction
This report analyzes...

## Methodology

![Figure 1: Surgical Procedure](images/procedure.png)

**Figure 1:** Double Tract Reconstruction procedure overview.

## Results

| Outcome | DTR | TG | P-value |
|---------|-----|-----|---------|
| 5-year survival | 92% | 88% | 0.04 |
| QoL score | 85 | 72 | <0.01 |

**Table 1:** Comparison of outcomes between DTR and total gastrectomy.

### References
[Study 1](https://example.com/study1)
[Study 2](https://example.com/study2)
```

**Command:**
```bash
python manuscript_generator.py technical_report.md
```

---

## Example 4: Batch Processing Multiple Files

**Bash Script:** `generate_all.sh`
```bash
#!/bin/bash

# Generate documents for all markdown files in research directory
for file in research/*.md; do
    echo "Processing: $file"
    python manuscript_generator.py "$file" \
        --config config.yaml \
        --output publications \
        --formats docx pdf
done

echo "All documents generated!"
```

**Usage:**
```bash
chmod +x generate_all.sh
./generate_all.sh
```

---

## Example 5: Custom Styling for Publisher

**Configuration:** `config_publisher.yaml`
```yaml
formatting:
  font_family: "Arial"
  font_size: 11
  line_spacing: 1.15
  
styles:
  heading1:
    font_size: 14
    bold: true
    color: "1a4d2e"
  
  heading2:
    font_size: 12
    bold: true
    color: "2d6a4f"

publisher:
  optimize_for_publisher: true
  
output:
  formats: ['docx']
```

**Command:**
```bash
python manuscript_generator.py manuscript.md -c config_publisher.yaml
```

---

## Example 6: Academic Thesis Chapter

**Configuration:** `config_thesis.yaml`
```yaml
document:
  title: "Thesis Chapter 3"
  author: "PhD Candidate"

formatting:
  font_family: "Times New Roman"
  font_size: 12
  line_spacing: 2.0  # Double spacing
  margins:
    top: 2.54
    bottom: 2.54
    left: 3.81   # Wider left margin for binding
    right: 2.54

numbering:
  sections: true
  format: "decimal"

toc:
  enabled: true
  depth: 4  # Include more levels

bibliography:
  style: "apa"
  title: "References"

output:
  formats: ['docx', 'pdf']
```

---

## Example 7: Integration with Git Workflow

**Pre-commit Hook:** `.git/hooks/pre-commit`
```bash
#!/bin/bash

# Auto-generate documents before commit
if git diff --cached --name-only | grep -q "research.*.md"; then
    echo "Generating updated documents..."
    python manuscript_generator.py research/main.md -o docs
    git add docs/
fi
```

---

## Example 8: Creating Document Templates

**Template:** `template_research_paper.md`
```markdown
# [Your Paper Title Here]

**Author:** [Your Name]
**Date:** [Date]
**Institution:** [Your Institution]

---

## Abstract

[Write your abstract here - 250 words max]

## 1. Introduction

### 1.1 Background

[Background information]

### 1.2 Research Question

[Your research question]

## 2. Methods

### 2.1 Study Design

[Study design details]

## 3. Results

[Present your results]

## 4. Discussion

[Discuss implications]

## 5. Conclusion

[Summarize findings]

---

### References

[Reference 1](url1)
[Reference 2](url2)
```

**Usage:**
```bash
cp template_research_paper.md my_new_paper.md
# Edit my_new_paper.md with your content
python manuscript_generator.py my_new_paper.md
```

---

## Example 9: Automating with Makefile

**Makefile:**
```makefile
.PHONY: all clean generate-docs

SOURCES := $(wildcard research/*.md)
OUTPUTS := $(patsubst research/%.md,output/%.pdf,$(SOURCES))

all: generate-docs

generate-docs: $(OUTPUTS)

output/%.pdf: research/%.md
	@mkdir -p output
	python manuscript_generator.py $< -c config.yaml -o output -f pdf

clean:
	rm -rf output/*

help:
	@echo "Usage:"
	@echo "  make              - Generate all documents"
	@echo "  make clean        - Remove generated files"
	@echo "  make help         - Show this help"
```

**Usage:**
```bash
make              # Generate all
make clean        # Clean up
```

---

## Example 10: Environment-Specific Configurations

**Development:** `config_dev.yaml`
```yaml
output:
  formats: ['html']  # Fast preview
  
advanced:
  verbose_logging: true
```

**Production:** `config_prod.yaml`
```yaml
output:
  formats: ['docx', 'pdf']
  
advanced:
  verbose_logging: false
  create_backup: true
```

**Usage:**
```bash
# Development
python manuscript_generator.py paper.md -c config_dev.yaml

# Production
python manuscript_generator.py paper.md -c config_prod.yaml
```

---

## Troubleshooting Common Scenarios

### Problem: PDF Generation Fails

**Solution:** Install system dependencies
```bash
sudo apt-get install -y libcairo2 libpango-1.0-0 libgdk-pixbuf2.0-0
pip install --upgrade weasyprint
```

### Problem: Unicode Errors

**Solution:** Ensure UTF-8 encoding
```bash
file -i your_file.md  # Check encoding
iconv -f ISO-8859-1 -t UTF-8 input.md > output.md  # Convert if needed
```

### Problem: Missing Images

**Solution:** Use absolute or relative paths
```markdown
# Good
![Caption](./images/figure1.png)
![Caption](/home/user/images/figure2.png)

# Avoid
![Caption](~/images/figure.png)
```

---

## Tips and Best Practices

1. **Use version control** for your markdown files
2. **Keep images in a separate directory** (e.g., `images/` or `figures/`)
3. **Test configurations** before batch processing
4. **Use verbose mode** (`-v`) when debugging
5. **Backup original files** before making changes
6. **Check output files** after generation
7. **Use templates** for consistent formatting
8. **Document your workflow** for reproducibility

---

## Advanced: Python API Usage

```python
from pathlib import Path
from manuscript_generator import ManuscriptGenerator

# Create generator with custom config
generator = ManuscriptGenerator(config_path=Path('config.yaml'))

# Generate documents
output_files = generator.generate(
    input_path=Path('research.md'),
    output_dir=Path('./output')
)

print(f"Generated: {output_files}")
```

---

For more information, see the main [README.md](README.md)

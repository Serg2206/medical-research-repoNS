# 🚀 Getting Started with Manuscript Generator

## Welcome! 

Your **Manuscript Generator** tool is fully set up and ready to use.

---

## ✅ What's Been Created

### Core Files (in ~/):
1. **manuscript_generator.py** - Main Python tool (900 lines)
2. **config.yaml** - Configuration file with all settings
3. **requirements.txt** - Python dependencies
4. **README.md** - Complete documentation
5. **USAGE_EXAMPLES.md** - 10+ practical examples
6. **github-workflow-example.yml** - GitHub Actions template
7. **PROJECT_SUMMARY.md** - Full project summary

### Test Output (in ~/output/):
- ✅ double_tract_research.docx (50KB)
- ✅ double_tract_research.html (75KB)  
- ✅ double_tract_research.pdf (86KB)

---

## 🎯 Quick Start (3 Steps)

### Step 1: Verify Installation
```bash
cd ~
python manuscript_generator.py --help
```

### Step 2: Generate Your First Document
```bash
python manuscript_generator.py double_tract_research.md
```

### Step 3: Check Output
```bash
ls -lh output/
```

That's it! Your documents are in the `output/` directory.

---

## 📝 Basic Usage

### Generate All Formats
```bash
python manuscript_generator.py your_file.md
```
Creates: DOCX, HTML, and PDF

### Generate Specific Format
```bash
python manuscript_generator.py your_file.md -f docx
```
Creates: Only DOCX

### Use Custom Config
```bash
python manuscript_generator.py your_file.md -c config.yaml
```

### Specify Output Directory
```bash
python manuscript_generator.py your_file.md -o ./my_output
```

---

## 🏥 For Your Medical Research

### Process Your Research File
```bash
python manuscript_generator.py ~/double_tract_research.md \
  --config ~/config.yaml \
  --output ~/medical-publications \
  --formats docx pdf
```

### Batch Process Multiple Files
```bash
# Create a simple script
for file in *.md; do
  python manuscript_generator.py "$file" -o publications
done
```

---

## ⚙️ Customize Configuration

Edit `config.yaml` to change:
- **Fonts**: Times New Roman, Arial, etc.
- **Margins**: Page margins in cm
- **Numbering**: Section, figure, table numbering
- **TOC Depth**: How many heading levels to include
- **Output Formats**: Which formats to generate

Example customization:
```yaml
formatting:
  font_family: "Arial"
  font_size: 11

numbering:
  sections: true
  format: "decimal"

output:
  formats: ['docx', 'pdf']
```

---

## 🔗 GitHub Integration

### Option 1: Copy Workflow File
```bash
# In your repository
mkdir -p .github/workflows
cp ~/github-workflow-example.yml .github/workflows/generate-docs.yml
git add .github/workflows/generate-docs.yml
git commit -m "Add manuscript generator workflow"
git push
```

### Option 2: Add to Existing Workflow
Add this step to your existing `docs-improver.yml`:

```yaml
- name: Generate formatted documents
  run: |
    python ~/manuscript_generator.py docs-generated/README.md \
      --config ~/config.yaml \
      --output docs-final \
      --formats docx pdf
```

---

## 📚 Documentation

- **Full Documentation**: [README.md](README.md)
- **Usage Examples**: [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)  
- **Project Summary**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- **This Guide**: GETTING_STARTED.md

---

## 🛠️ Troubleshooting

### Issue: "Module not found"
```bash
pip install -r requirements.txt
```

### Issue: PDF generation fails
```bash
sudo apt-get install -y libcairo2 libpango-1.0-0
pip install --upgrade weasyprint
```

### Issue: Font not available
Edit `config.yaml` and change to available font:
```yaml
formatting:
  font_family: "Liberation Serif"  # or "DejaVu Serif"
```

---

## 💡 Pro Tips

1. **Test first**: Try with a small markdown file before batch processing
2. **Use verbose mode**: Add `-v` flag to see detailed logs
3. **Backup originals**: Keep original markdown files safe
4. **Check output**: Always verify generated documents
5. **Use templates**: Create markdown templates for consistency

---

## 🎓 Example Workflow

### Daily Research Documentation

```bash
# 1. Write your research in markdown
vim my_research.md

# 2. Generate documents
python manuscript_generator.py my_research.md -f docx pdf

# 3. Review output
xdg-open output/my_research.pdf

# 4. Share DOCX with collaborators
cp output/my_research.docx ~/shared/
```

---

## 🚀 Next Actions

### Immediate:
1. ✅ Tool is installed and tested
2. ✅ Sample documents generated
3. ✅ All documentation available

### Recommended:
1. 📝 Process your existing markdown files
2. ⚙️ Customize `config.yaml` for your needs
3. 🔗 Set up GitHub Actions workflow
4. 📤 Share tool with your team

### Advanced:
1. 🎨 Create custom configurations for different document types
2. 🤖 Automate with cron jobs or CI/CD
3. 📊 Generate reports from multiple sources
4. 🌐 Integrate with your publication workflow

---

## ✨ Key Features You Can Use Now

✅ **Automatic Section Numbering**
- Your sections get numbered: 1, 1.1, 1.1.1, etc.

✅ **Table of Contents**
- Auto-generated from your headings

✅ **Bibliography**
- References extracted from links

✅ **Professional Formatting**
- Times New Roman, justified text, proper spacing

✅ **Multiple Formats**
- DOCX for editing, PDF for distribution

✅ **Publisher Compatible**
- Import DOCX directly into Microsoft Publisher

---

## 📞 Need Help?

- **Documentation**: Check README.md
- **Examples**: See USAGE_EXAMPLES.md
- **Configuration**: Review config.yaml comments
- **Debugging**: Run with `-v` flag

---

## 🎉 You're All Set!

Your Manuscript Generator is ready to transform your markdown files into professional scientific documents.

**Try it now:**
```bash
python manuscript_generator.py double_tract_research.md
```

**Happy writing! 📝✨**

---

*Tool Version: 1.0.0*  
*Created: November 10, 2025*  
*Location: /home/ubuntu/*

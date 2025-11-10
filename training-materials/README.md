# Training Materials for Professional Medical Manuscript Generation

## Overview

This directory contains comprehensive training materials created from the analysis of 8 world-class oncological surgery publications. The materials are designed to improve the manuscript generation tool to produce publication-quality documents.

## Contents

### 1. Main Training Guide
**File:** `professional-formatting-guide-RU.md` (47,000+ words)

Comprehensive Russian-language guide covering:
- Document structure and organization
- Typography and font systems
- Layout and page composition
- Color schemes and visual hierarchy
- Professional table design (3 styles)
- Figure and chart specifications
- Citation and reference systems
- Evidence grading presentation
- Algorithm and flowchart design
- Special medical publication elements
- Before/after comparison analysis
- Practical implementation steps
- Quality control checklist

### 2. Technical Specifications
**File:** `formatting-specifications.json`

Machine-readable specifications including:
- Document settings (page formats, margins)
- Typography scales (fonts, sizes, spacing)
- Color palettes (4 professional schemes)
- Table styling (formal, grid, modern)
- Figure requirements (resolution, formats)
- Chart color palettes (5 and 10 color sets)
- CSS variables (31 custom properties)
- Responsive breakpoints
- Accessibility guidelines
- Print specifications

### 3. Analysis Summary
**File:** `ANALYSIS_SUMMARY.md`

Executive summary in English covering:
- Sources analyzed (8 publications)
- Key findings by category
- Current vs. target manuscript comparison
- Implementation recommendations
- Phased improvement plan
- Technical implementation guide
- Quality checklist (3 levels)
- Success metrics

## Sources Analyzed

### Medical Publications (PDF)
1. NCCN Patient Guidelines - Stomach Cancer 2025 (102 pages)
2. JGCA Guidelines 2021 - Full Article (25 pages)
3. Japanese Classification of Gastric Carcinoma - 15th Edition (19 pages)
4. Laparoscopic Proximal Gastrectomy with DTR (7 pages)
5. JGCA Guidelines 2021 - Summary (7 pages)

### Reference Materials (Markdown)
6. Double Tract Reconstruction - Systematic Review
7. Gastric Cancer Comprehensive Review
8. NIH Surgical Management

### Target for Improvement
9. Current manuscript: `/manuscripts/surgical-techniques/double-tract-reconstruction.md`

## Quick Start

### For Developers

1. **Review technical specifications:**
   ```bash
   cat formatting-specifications.json | jq '.'
   ```

2. **Study the training guide:**
   ```bash
   # Open in markdown viewer or browser
   code professional-formatting-guide-RU.md
   ```

3. **Read implementation summary:**
   ```bash
   cat ANALYSIS_SUMMARY.md
   ```

### For Implementation

**Phase 1: Foundation** (1-2 days)
- Create CSS with base styles
- Convert tables to HTML
- Apply heading hierarchy
- Implement color scheme

**Phase 2: Enhancement** (2-3 days)  
- Add special content boxes
- Create table templates
- Standardize captions
- Implement spacing

**Phase 3: Visualization** (3-5 days)
- Generate data charts
- Create surgical diagrams
- Design algorithm flowcharts

**Phase 4: Polish** (1-2 days)
- Quality checks
- Consistency review
- Accessibility audit
- Final optimization

## Key Specifications

### Typography
```
Body text: 11-12pt, line-height 1.5
H1: 24pt | H2: 18pt | H3: 14pt | H4: 12pt
Captions: 10pt | Footnotes: 9pt
```

### Color Scheme (Modern Medical)
```
Primary: #003366 (dark blue)
Accent: #0066CC (bright blue)
Success: #28A745 (green)
Warning: #FFC107 (orange)
Danger: #DC3545 (red)
```

### Table Styles
1. **Formal (Three-line)** - High-impact journals
2. **Grid** - Clinical guidelines
3. **Modern** - Contemporary publications

### Figure Requirements
- Print: 300+ DPI, CMYK
- Web: 96 DPI, RGB
- Formats: TIFF/EPS/PDF (print), PNG/JPEG/SVG (web)

## Directory Structure

```
training-materials/
├── README.md                                  (this file)
├── professional-formatting-guide-RU.md        (main guide, 47k+ words)
├── professional-formatting-guide-RU.pdf       (PDF version)
├── formatting-specifications.json             (technical specs)
├── ANALYSIS_SUMMARY.md                        (executive summary)
└── ANALYSIS_SUMMARY.pdf                       (PDF version)
```

## Analysis Data

Raw analysis data available in parent directory:
- `/home/ubuntu/comprehensive_design_patterns.json` - Extracted patterns
- `/home/ubuntu/analysis_*.txt` - Individual PDF analyses
- `/home/ubuntu/pdf_structure_analysis.json` - Structure data

## Quality Levels

### ✓ Minimum Acceptable
- Clear structure
- Captioned tables/figures
- Readable fonts (≥10pt)
- Adequate margins (≥2cm)

### ✓✓ High Quality  
- Professional color scheme
- Styled tables
- Visual hierarchy
- Special boxes
- Professional charts

### ✓✓✓ World-Class
- Journal-standard design
- Perfect typography
- High-resolution images (≥300 DPI)
- Visual algorithms
- Accessibility compliant

## Tools & Resources

### Recommended Tools
- **HTML/CSS**: VS Code + Live Server
- **Charts**: Python (Matplotlib, Seaborn, Plotly)
- **Diagrams**: Adobe Illustrator, Inkscape, BioRender
- **Conversion**: WeasyPrint, Pandoc, Prince XML

### Color Resources
- ColorBrewer 2.0 (chart palettes)
- Coolors.co (palette generator)
- Adobe Color (harmony)

### Fonts
- Serif: Times New Roman, Georgia
- Sans-serif: Arial, Helvetica, Open Sans
- Monospace: Courier New, Consolas

## Success Metrics

### Quantitative
- All images ≥300 DPI
- Color contrast ≥4.5:1
- 5+ font hierarchy levels
- 10+ visual elements

### Qualitative
- Matches top-tier journals
- Clear visual hierarchy
- Comfortable readability
- Consistent styling
- Accessible design

## Contact & Support

**Created:** November 10, 2025  
**Version:** 1.0  
**Purpose:** Training materials for manuscript generation tool improvement

For questions or updates, refer to the main training guide or technical specifications.

## License

These training materials are created for internal use in the medical research manuscript generation project.

---

**Next Steps:** Review the training guide, implement Phase 1 improvements, and test with the current manuscript.

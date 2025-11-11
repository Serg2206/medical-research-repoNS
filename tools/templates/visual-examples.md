# Visual Content Examples for Medical Manuscript System

**Date:** November 10, 2025  
**Version:** 1.0  
**Purpose:** Comprehensive guide for creating rich visual content in medical manuscripts

---

## Table of Contents

1. [Introduction](#introduction)
2. [Image Gallery](#image-gallery)
3. [Multi-Panel Figures](#multi-panel-figures)
4. [Annotated Images](#annotated-images)
5. [Before/After Comparison](#beforeafter-comparison)
6. [Step-by-Step Procedures](#step-by-step-procedures)
7. [Surgical Photo Panels](#surgical-photo-panels)
8. [Best Practices](#best-practices)
9. [Accessibility Guidelines](#accessibility-guidelines)

---

## Introduction

The Medical Manuscript System now supports rich visual content through simple Markdown syntax. This document provides examples and documentation for all available visual components.

### Key Features

- **Responsive Design:** All components adapt to different screen sizes
- **Interactive Elements:** Lightbox, comparison sliders, and zoom functionality
- **Accessibility:** WCAG 2.1 AA compliant with keyboard navigation
- **Professional Styling:** Based on leading medical journal standards
- **Easy Syntax:** Simple Markdown-like syntax for all components

---

## Image Gallery

Create responsive image galleries with optional lightbox functionality.

### Basic Syntax

```markdown
:::gallery columns=3 caption="Collection of surgical images"
- image1.jpg | Description of first image | Optional caption for image 1
- image2.jpg | Description of second image | Optional caption for image 2
- image3.jpg | Description of third image
:::
```

### Example 1: Basic 3-Column Gallery

```markdown
:::gallery columns=3 caption="3D Reconstructions of Gastric Anatomy"
- reference-materials/visual-surgical-content/3d-reconstructions/BMC_Surgery_004_685x427.png | 3D reconstruction showing anterior view
- reference-materials/visual-surgical-content/3d-reconstructions/BMC_Surgery_005_685x662.png | 3D reconstruction showing lateral view
- reference-materials/visual-surgical-content/3d-reconstructions/BMC_Surgery_006_685x629.png | 3D reconstruction showing posterior view
:::
```

### Example 2: 2-Column Gallery Without Lightbox

```markdown
:::gallery columns=2 lightbox=false
- reference-materials/visual-surgical-content/anatomical-diagrams/Frontiers_Oncology_009_1949x1185.jpeg | Lymph node stations diagram | D1 and D2 lymphadenectomy stations
- reference-materials/visual-surgical-content/anatomical-diagrams/Frontiers_Oncology_010_1940x953.jpeg | Vascular anatomy | Celiac trunk and branches
:::
```

### Options

- `columns=N` - Number of columns (1-4, default: 3)
- `caption="Text"` - Overall gallery caption
- `lightbox=false` - Disable lightbox (enabled by default)

### When to Use

- Showcasing multiple related images
- Before/after series (multiple time points)
- Comparative imaging from different modalities
- Collection of surgical cases

---

## Multi-Panel Figures

Create scientific multi-panel figures with automatic labeling (A, B, C, D).

### Basic Syntax

```markdown
:::figure-panel layout=2x2 number="1" caption="Figure caption goes here"
- A: image1.jpg | Alt text for panel A | Subpanel caption A
- B: image2.jpg | Alt text for panel B | Subpanel caption B
- C: image3.jpg | Alt text for panel C | Subpanel caption C
- D: image4.jpg | Alt text for panel D | Subpanel caption D
:::
```

### Example 1: 2×2 Grid Figure

```markdown
:::figure-panel layout=2x2 number="1" caption="Multi-modal imaging of gastric tumor. (A) CT scan showing tumor location, (B) Endoscopic view, (C) Histopathological examination, (D) 3D reconstruction."
- A: reference-materials/visual-surgical-content/3d-reconstructions/BMC_Surgery_004_685x427.png | CT reconstruction
- B: reference-materials/visual-surgical-content/surgical-photos/Korean_Journal_Radiology_017_792x449.jpeg | Endoscopic view
- C: reference-materials/visual-surgical-content/surgical-photos/Korean_Journal_Radiology_016_793x374.jpeg | Histopathology
- D: reference-materials/visual-surgical-content/3d-reconstructions/BMC_Surgery_005_685x662.png | 3D reconstruction
:::
```

### Example 2: 3×2 Grid (6 Panels)

```markdown
:::figure-panel layout=3x2 number="2" caption="Surgical technique steps for laparoscopic gastrectomy"
- image1.jpg | Step 1: Port placement
- image2.jpg | Step 2: Greater curvature mobilization
- image3.jpg | Step 3: Lesser curvature dissection
- image4.jpg | Step 4: Lymph node dissection
- image5.jpg | Step 5: Gastric transection
- image6.jpg | Step 6: Reconstruction
:::
```

### Example 3: Horizontal Layout

```markdown
:::figure-panel layout=horizontal number="3" caption="Progression of tumor response to chemotherapy"
- Baseline: pretreat.jpg | Baseline CT scan
- 3 months: month3.jpg | After 3 months of treatment
- 6 months: month6.jpg | After 6 months of treatment
:::
```

### Available Layouts

- `2x2` - 2 rows × 2 columns (4 panels)
- `3x2` - 2 rows × 3 columns (6 panels)
- `2x3` - 3 rows × 2 columns (6 panels)
- `3x3` - 3 rows × 3 columns (9 panels)
- `4x2` - 2 rows × 4 columns (8 panels)
- `horizontal` - Single row with multiple columns
- `vertical` - Single column with multiple rows

### When to Use

- Comparing multiple views or modalities
- Showing progression or time series
- Demonstrating surgical steps
- Complex anatomical illustrations with multiple perspectives

---

## Annotated Images

Add arrows, labels, circles, and highlights to images.

### Basic Syntax

```markdown
:::annotated-image number="4" caption="Annotated surgical anatomy"
image: surgery.jpg | Surgical field view
annotations:
- arrow: 50, 30 | Tumor location | red
- circle: 60, 40 | yellow
- label: 70, 20 | Important vessel | white
- rectangle: 40, 60 | Safe dissection plane | green
:::
```

### Example 1: Surgical Anatomy with Annotations

```markdown
:::annotated-image number="4" caption="Key anatomical landmarks during laparoscopic gastrectomy. Red arrows indicate critical vascular structures, yellow circles highlight lymph node stations."
image: reference-materials/visual-surgical-content/surgical-photos/Korean_Journal_Radiology_017_792x449.jpeg | Intraoperative view during gastrectomy
annotations:
- arrow: 35, 45 | Left gastric artery | red
- arrow: 55, 40 | Right gastric artery | red
- circle: 45, 30 | Station 3 lymph nodes | yellow
- circle: 60, 55 | Station 7 lymph nodes | yellow
- label: 70, 25 | Celiac trunk | white
:::
```

### Example 2: Pathology Slide Annotation

```markdown
:::annotated-image number="5" caption="Histopathological features of gastric adenocarcinoma"
image: pathology-slide.jpg | H&E stained section
annotations:
- arrow: 40, 35 | Tumor cells | red
- arrow: 55, 50 | Lymphatic invasion | red
- circle: 30, 60 | Inflammatory infiltrate | blue
- rectangle: 60, 40 | Normal gastric mucosa | green
:::
```

### Annotation Types

1. **arrow** - Directional arrow pointing to structure
2. **circle** - Circular highlight around area
3. **rectangle** - Rectangular highlight
4. **label** - Text label without pointer

### Coordinate System

- X and Y are percentages (0-100) from top-left corner
- X: 0 (left) to 100 (right)
- Y: 0 (top) to 100 (bottom)

### Colors

Standard colors: `red`, `blue`, `yellow`, `green`, `white`, `black`

### When to Use

- Highlighting key anatomical structures
- Marking tumor locations
- Identifying critical landmarks
- Educational illustrations

---

## Before/After Comparison

Interactive slider for comparing two images (before/after treatment, pre/post-op, etc.).

### Basic Syntax

```markdown
:::comparison number="6" caption="Comparison description"
before: before-image.jpg | Description of before image
after: after-image.jpg | Description of after image
:::
```

### Example 1: Treatment Response

```markdown
:::comparison number="6" caption="CT imaging showing tumor response to neoadjuvant chemotherapy. Left: Pre-treatment scan showing large gastric tumor. Right: Post-treatment scan demonstrating significant tumor reduction."
before: reference-materials/visual-surgical-content/3d-reconstructions/BMC_Surgery_004_685x427.png | Pre-treatment CT scan
after: reference-materials/visual-surgical-content/3d-reconstructions/BMC_Surgery_005_685x662.png | Post-treatment CT scan
:::
```

### Example 2: Surgical Outcome

```markdown
:::comparison number="7" caption="Endoscopic view before and after endoscopic submucosal dissection"
before: pre-esd.jpg | Pre-procedure endoscopy showing early gastric cancer
after: post-esd.jpg | Post-procedure endoscopy showing complete resection
:::
```

### Features

- **Interactive Slider:** Drag the handle to reveal before/after
- **Keyboard Navigation:** Use arrow keys to move slider
- **Labels:** "Before" and "After" labels auto-generated
- **Responsive:** Works on mobile with touch gestures

### When to Use

- Treatment response comparison
- Pre/post-operative imaging
- Before/after surgical reconstruction
- Temporal changes in disease progression

---

## Step-by-Step Procedures

Sequential visualization of surgical or procedural steps.

### Basic Syntax

```markdown
:::procedure-steps title="Procedure Title" number="8" layout="vertical"
- step1.jpg | Step description | Detailed caption for step 1
- step2.jpg | Step description | Detailed caption for step 2
- step3.jpg | Step description | Detailed caption for step 3
:::
```

### Example 1: Vertical Procedure Steps

```markdown
:::procedure-steps title="Laparoscopic Distal Gastrectomy - Key Steps" number="8" layout="vertical"
- reference-materials/visual-surgical-content/procedure-steps/Korean_Journal_Radiology_010_714x680.jpeg | Port placement | Initial trocar placement in standard 5-port configuration
- reference-materials/visual-surgical-content/procedure-steps/Korean_Journal_Radiology_011_691x502.jpeg | Omental dissection | Division of gastrocolic ligament along greater curvature
- reference-materials/visual-surgical-content/procedure-steps/Korean_Journal_Radiology_015_792x375.jpeg | D2 lymphadenectomy | Systematic lymph node dissection including stations 7, 8a, 9, 11p
- reference-materials/visual-surgical-content/procedure-steps/Int_J_Surgery_Case_Reports_009_675x734.jpeg | Reconstruction | Billroth II gastrojejunostomy anastomosis
:::
```

### Example 2: Horizontal Procedure Steps

```markdown
:::procedure-steps title="Endoscopic Submucosal Dissection Technique" layout="horizontal"
- marking.jpg | Marking | Circumferential marking around lesion
- injection.jpg | Submucosal injection | Lifting solution injection
- circumferential-cut.jpg | Circumferential incision | Mucosal incision around marks
- dissection.jpg | Submucosal dissection | Careful dissection of submucosal layer
:::
```

### Example 3: Grid Layout

```markdown
:::procedure-steps title="Minimally Invasive Gastrectomy" layout="grid"
- step1.jpg | Patient positioning
- step2.jpg | Port placement
- step3.jpg | Greater curvature mobilization
- step4.jpg | Lesser curvature dissection
- step5.jpg | Lymph node dissection
- step6.jpg | Resection and reconstruction
:::
```

### Layout Options

- `vertical` - Stacked vertically (default, best for detailed steps)
- `horizontal` - Side by side (good for quick overview)
- `grid` - Auto-fitting grid layout (good for many steps)

### When to Use

- Surgical technique descriptions
- Procedural protocols
- Educational materials
- Method sections in research papers

---

## Surgical Photo Panels

Professional presentation of intraoperative photographs with privacy notice.

### Basic Syntax

```markdown
:::surgical-photos title="Panel Title" number="9" columns=2
- photo1.jpg | Description | Caption for photo 1
- photo2.jpg | Description | Caption for photo 2
:::
```

### Example 1: Intraoperative Findings

```markdown
:::surgical-photos title="Intraoperative Findings - Advanced Gastric Cancer" number="9" columns=2
- reference-materials/visual-surgical-content/surgical-photos/Korean_Journal_Radiology_017_792x449.jpeg | Overall view | Laparoscopic view showing large tumor at gastric body
- reference-materials/visual-surgical-content/surgical-photos/Korean_Journal_Radiology_016_793x374.jpeg | Vascular anatomy | Identification of left gastric artery prior to ligation
- reference-materials/visual-surgical-content/surgical-photos/Korean_Journal_Radiology_014_793x376.jpeg | Lymph node dissection | D2 lymphadenectomy in progress
- reference-materials/visual-surgical-content/surgical-photos/Korean_Journal_Radiology_018_792x308.jpeg | Specimen | Resected specimen showing tumor margins
:::
```

### Example 2: Surgical Complications

```markdown
:::surgical-photos title="Management of Anastomotic Leak" number="10" columns=1
- leak-discovery.jpg | Initial presentation | CT scan showing anastomotic leak on POD 5
- reoperation.jpg | Re-exploration | Intraoperative finding of leak at gastrojejunostomy
- drainage.jpg | Management | Placement of drainage tubes and repair
- healing.jpg | Resolution | Healed anastomosis at 3-month follow-up
:::
```

### Features

- **Privacy Notice:** Auto-generated notice about patient consent and de-identification
- **Professional Styling:** Red-themed border matching surgical context
- **Flexible Columns:** 1-3 columns supported
- **Responsive:** Automatically stacks on mobile devices

### Column Options

- `columns=1` - Single column (large, detailed view)
- `columns=2` - Two columns (most common)
- `columns=3` - Three columns (compact overview)

### When to Use

- Intraoperative photographs
- Surgical findings documentation
- Case reports
- Technique descriptions

### Important Note

⚠️ **Patient Privacy:** Always ensure:
- Patient consent obtained for photography
- All identifying information removed
- Institutional review board approval for publication
- Compliance with HIPAA and local privacy regulations

---

## Best Practices

### Image Quality

1. **Resolution:**
   - Minimum 800px width for main figures
   - 1200-2000px for detailed anatomical diagrams
   - Compress images to <500KB for web display

2. **Format Selection:**
   - **PNG:** For diagrams, illustrations, 3D reconstructions
   - **JPEG:** For photographs, radiological images, surgical photos
   - **WebP:** For modern browsers (with JPEG fallback)

3. **Naming Convention:**
   - Use descriptive filenames: `gastric-anatomy-anterior.png`
   - Avoid spaces: use hyphens or underscores
   - Include dimensions in filename for tracking: `image_1200x800.jpg`

### Caption Writing

1. **Figure Captions:**
   - Start with brief description
   - Include technical details (staining, magnification, modality)
   - Explain abbreviations
   - Reference panels with capital letters in parentheses

   Example:
   ```
   Figure 1: Histopathological examination of gastric adenocarcinoma. 
   (A) H&E staining showing poorly differentiated tumor cells (×100). 
   (B) Immunohistochemistry for HER2 showing 3+ positive staining (×200). 
   (C) Ki-67 staining demonstrating high proliferative index (×100). 
   Scale bar = 100 μm.
   ```

2. **Alt Text Best Practices:**
   - Describe what the image shows, not what it means
   - Keep it concise (< 125 characters)
   - Don't start with "Image of..." or "Picture of..."
   - Include key visual elements

### Accessibility

1. **Color Choices:**
   - Don't rely solely on color to convey information
   - Use patterns or textures in addition to color
   - Ensure sufficient contrast (4.5:1 minimum)
   - Consider colorblind-friendly palettes

2. **Text Annotations:**
   - Use legible font sizes (minimum 14px)
   - Provide high contrast between text and background
   - Include text alternatives for color-coded information

3. **Keyboard Navigation:**
   - All interactive elements accessible via keyboard
   - Tab key to navigate between elements
   - Enter/Space to activate
   - Arrow keys for sliders and galleries

### Organization

1. **File Structure:**
   ```
   manuscript-project/
   ├── manuscript.md
   ├── figures/
   │   ├── fig1-patient-flow.png
   │   ├── fig2-survival-analysis.png
   │   └── surgical-photos/
   │       ├── photo1.jpg
   │       ├── photo2.jpg
   │       └── photo3.jpg
   └── supplementary/
       └── additional-images/
   ```

2. **Reference Paths:**
   - Use relative paths from manuscript location
   - Keep images in organized subdirectories
   - Use consistent path structure across manuscript

### Figure Numbering

1. **Sequential Numbering:**
   - Number figures consecutively: 1, 2, 3...
   - Use section prefixes for supplements: S1, S2, S3...
   - Use subsection numbering: 1.1, 1.2, 2.1...

2. **Reference in Text:**
   - Reference figures before they appear
   - Use consistent format: "Figure 1", "Fig. 1", etc.
   - Explain what reader should observe

---

## Accessibility Guidelines

### WCAG 2.1 Compliance

All visual components meet WCAG 2.1 Level AA standards:

1. **Perceivable:**
   - Alt text for all images
   - Sufficient color contrast
   - No information conveyed by color alone

2. **Operable:**
   - Keyboard accessible
   - No keyboard traps
   - Sufficient time for interactions

3. **Understandable:**
   - Clear navigation patterns
   - Consistent behavior
   - Error prevention and recovery

4. **Robust:**
   - Valid HTML/CSS
   - Compatibility with assistive technologies
   - Progressive enhancement

### Screen Reader Support

Components are optimized for screen readers:

- Proper ARIA labels and roles
- Semantic HTML structure
- Descriptive link text
- Logical navigation order

### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Open lightbox | Enter or Space on gallery item |
| Close lightbox | Escape |
| Next image | Right Arrow |
| Previous image | Left Arrow |
| Move comparison slider | Left/Right Arrow |
| Navigate between items | Tab |

### Testing Checklist

Before publishing, verify:

- [ ] All images have descriptive alt text
- [ ] Color contrast meets minimum standards (use WebAIM contrast checker)
- [ ] All interactive elements keyboard accessible
- [ ] No keyboard traps
- [ ] Screen reader announces content correctly
- [ ] Components work without JavaScript (progressive enhancement)
- [ ] Responsive design tested on mobile devices
- [ ] Print stylesheet displays images appropriately

---

## Putting It All Together

### Complete Manuscript Example

Here's a complete example combining multiple visual component types:

```markdown
# Laparoscopic Distal Gastrectomy for Advanced Gastric Cancer: A Case Report

## Introduction

Gastric cancer remains a significant global health challenge...

## Case Presentation

### Patient Characteristics

A 62-year-old male presented with dyspepsia and weight loss...

### Preoperative Imaging

:::figure-panel layout=2x2 number="1" caption="Preoperative imaging studies. (A) CT scan axial view showing gastric tumor, (B) Coronal reconstruction demonstrating tumor extent, (C) 3D reconstruction, (D) Endoscopic view of lesion."
- A: figures/ct-axial.jpg | CT scan axial view
- B: figures/ct-coronal.jpg | CT scan coronal view
- C: figures/3d-reconstruction.jpg | 3D reconstruction
- D: figures/endoscopy.jpg | Endoscopic view
:::

### Surgical Technique

:::procedure-steps title="Key Steps of Laparoscopic Distal Gastrectomy with D2 Lymphadenectomy" number="2" layout="vertical"
- figures/step1-ports.jpg | Port placement | Five-port technique with camera at umbilicus
- figures/step2-mobilization.jpg | Greater curvature mobilization | Division of gastrocolic ligament
- figures/step3-lymph-nodes.jpg | Lymph node dissection | Systematic D2 lymphadenectomy
- figures/step4-resection.jpg | Gastric resection | Transection using linear stapler
- figures/step5-reconstruction.jpg | Reconstruction | Billroth II gastrojejunostomy
:::

### Intraoperative Findings

:::surgical-photos title="Critical Intraoperative Findings" number="3" columns=2
- figures/intraop1.jpg | Tumor location | Large ulcerative tumor at gastric antrum
- figures/intraop2.jpg | Vascular anatomy | Identification of left gastric artery
- figures/intraop3.jpg | Lymph nodes | Enlarged station 6 lymph nodes
- figures/intraop4.jpg | Final specimen | Resected stomach with adequate margins
:::

### Pathological Analysis

:::annotated-image number="4" caption="Histopathological examination showing poorly differentiated adenocarcinoma with extensive lymphovascular invasion."
image: figures/pathology.jpg | H&E stained section
annotations:
- arrow: 40, 35 | Tumor cells | red
- arrow: 55, 50 | Lymphatic invasion | red
- circle: 65, 30 | Signet ring cells | yellow
- label: 30, 60 | Normal mucosa | white
:::

### Treatment Response

:::comparison number="5" caption="Comparison of preoperative and postoperative imaging demonstrating successful tumor resection."
before: figures/preop-ct.jpg | Preoperative CT showing tumor
after: figures/postop-ct.jpg | Postoperative CT showing successful resection
:::

## Discussion

The surgical management of advanced gastric cancer...

## Conclusion

Laparoscopic distal gastrectomy with D2 lymphadenectomy...
```

---

## Troubleshooting

### Common Issues and Solutions

1. **Images not displaying:**
   - Check file path is correct and relative to manuscript location
   - Verify image files exist
   - Check file extensions match actual format

2. **Lightbox not working:**
   - Ensure `visual-interactions.js` is loaded
   - Check browser console for JavaScript errors
   - Verify lightbox HTML is generated

3. **Comparison slider stuck:**
   - Ensure images are same dimensions
   - Check CSS is loaded correctly
   - Try different browser

4. **Layout issues on mobile:**
   - Verify responsive CSS is active
   - Test in browser dev tools mobile view
   - Check image sizes aren't too large

5. **Annotations not visible:**
   - Check coordinate values (0-100 range)
   - Verify color contrast with image
   - Test with different annotation types

### Getting Help

For issues or questions:

1. Check this documentation
2. Review examples in `/tools/templates/`
3. Inspect browser developer console for errors
4. Verify all files are in correct locations

---

## Version History

- **v1.0** (November 10, 2025) - Initial release
  - Image galleries with lightbox
  - Multi-panel figures
  - Annotated images
  - Comparison sliders
  - Procedure steps
  - Surgical photo panels

---

## Conclusion

The visual components system provides professional, accessible, and interactive visual content for medical manuscripts. By following these examples and best practices, you can create publication-ready documents that meet the standards of leading medical journals.

For the most up-to-date information and additional examples, refer to:
- Technical documentation: `/tools/visual_components.py`
- CSS styles: `/tools/styles/professional-medical.css`
- JavaScript interactions: `/tools/scripts/visual-interactions.js`
- Visual content analysis: `/training-materials/visual-content-analysis.md`

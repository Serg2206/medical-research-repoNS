"""
Visual Components Module for Medical Manuscript Generation System

This module provides classes for creating rich visual content in medical manuscripts:
- ImageGallery: Grid layout galleries with lightbox functionality
- MultiPanelFigure: Scientific multi-panel figure layouts (2×2, 3×3, custom grids)
- AnnotatedImage: Images with labels, arrows, and callouts
- ComparisonSlider: Interactive before/after image comparisons
- StepByStepProcedure: Sequential procedure visualization
- SurgicalPhotoPanel: Professional surgical photo presentations

Author: Medical Research System
Date: November 10, 2025
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ImageFormat(Enum):
    """Supported image formats"""
    JPEG = "jpeg"
    JPG = "jpg"
    PNG = "png"
    WEBP = "webp"
    SVG = "svg"


class PanelLayout(Enum):
    """Common panel layout configurations"""
    GRID_2x2 = "2x2"
    GRID_3x2 = "3x2"
    GRID_2x3 = "2x3"
    GRID_3x3 = "3x3"
    GRID_4x2 = "4x2"
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    CUSTOM = "custom"


@dataclass
class ImageMetadata:
    """Metadata for an image"""
    path: str
    alt_text: str
    caption: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    label: Optional[str] = None  # For multi-panel figures (A, B, C, etc.)
    

@dataclass
class Annotation:
    """Annotation for an image (arrow, label, highlight)"""
    type: str  # 'arrow', 'label', 'circle', 'rectangle'
    text: Optional[str] = None
    x: Optional[float] = None  # Position as percentage (0-100)
    y: Optional[float] = None
    color: str = "red"
    size: str = "medium"


class ImageGallery:
    """
    Creates a responsive image gallery with grid layout and lightbox.
    
    Example usage:
        gallery = ImageGallery(
            images=[ImageMetadata(path="img1.jpg", alt_text="Image 1"), ...],
            columns=3,
            gap=20,
            enable_lightbox=True
        )
        html = gallery.generate_html()
    """
    
    def __init__(
        self,
        images: List[ImageMetadata],
        columns: int = 3,
        gap: int = 20,
        enable_lightbox: bool = True,
        gallery_id: Optional[str] = None,
        caption: Optional[str] = None
    ):
        self.images = images
        self.columns = columns
        self.gap = gap
        self.enable_lightbox = enable_lightbox
        self.gallery_id = gallery_id or f"gallery-{id(self)}"
        self.caption = caption
    
    def generate_html(self) -> str:
        """Generate HTML for the image gallery"""
        html_parts = []
        
        # Gallery container
        html_parts.append(f'<div class="image-gallery" id="{self.gallery_id}" '
                         f'data-columns="{self.columns}" '
                         f'style="gap: {self.gap}px;">')
        
        # Add images
        for idx, img in enumerate(self.images):
            item_class = "gallery-item"
            if self.enable_lightbox:
                item_class += " lightbox-enabled"
            
            html_parts.append(f'  <div class="{item_class}" data-index="{idx}">')
            html_parts.append(f'    <img src="{img.path}" alt="{img.alt_text}" loading="lazy">')
            
            if img.caption:
                html_parts.append(f'    <div class="gallery-caption">{img.caption}</div>')
            
            html_parts.append('  </div>')
        
        html_parts.append('</div>')
        
        # Overall caption
        if self.caption:
            html_parts.append(f'<div class="gallery-main-caption">{self.caption}</div>')
        
        # Lightbox HTML
        if self.enable_lightbox:
            html_parts.append(self._generate_lightbox_html())
        
        return '\n'.join(html_parts)
    
    def _generate_lightbox_html(self) -> str:
        """Generate lightbox overlay HTML"""
        return f'''
<div class="lightbox-overlay" id="{self.gallery_id}-lightbox" style="display: none;">
  <div class="lightbox-content">
    <span class="lightbox-close">&times;</span>
    <img class="lightbox-image" src="" alt="">
    <div class="lightbox-caption"></div>
    <button class="lightbox-nav lightbox-prev">&#10094;</button>
    <button class="lightbox-nav lightbox-next">&#10095;</button>
  </div>
</div>'''


class MultiPanelFigure:
    """
    Creates multi-panel scientific figures with labeled panels.
    
    Example usage:
        figure = MultiPanelFigure(
            panels=[ImageMetadata(...), ImageMetadata(...), ...],
            layout=PanelLayout.GRID_2x2,
            figure_number="1",
            caption="Figure 1: Multi-panel demonstration"
        )
        html = figure.generate_html()
    """
    
    def __init__(
        self,
        panels: List[ImageMetadata],
        layout: PanelLayout = PanelLayout.GRID_2x2,
        custom_grid: Optional[Tuple[int, int]] = None,  # (rows, cols)
        figure_number: Optional[str] = None,
        caption: Optional[str] = None,
        figure_id: Optional[str] = None,
        auto_label: bool = True
    ):
        self.panels = panels
        self.layout = layout
        self.custom_grid = custom_grid
        self.figure_number = figure_number
        self.caption = caption
        self.figure_id = figure_id or f"figure-{id(self)}"
        self.auto_label = auto_label
        
        # Auto-assign labels (A, B, C, ...) if not provided
        if self.auto_label:
            for idx, panel in enumerate(self.panels):
                if not panel.label:
                    panel.label = chr(65 + idx)  # A, B, C, ...
    
    def _get_grid_dimensions(self) -> Tuple[int, int]:
        """Get rows and columns for the layout"""
        if self.layout == PanelLayout.CUSTOM and self.custom_grid:
            return self.custom_grid
        
        layout_map = {
            PanelLayout.GRID_2x2: (2, 2),
            PanelLayout.GRID_3x2: (2, 3),
            PanelLayout.GRID_2x3: (3, 2),
            PanelLayout.GRID_3x3: (3, 3),
            PanelLayout.GRID_4x2: (2, 4),
            PanelLayout.HORIZONTAL: (1, len(self.panels)),
            PanelLayout.VERTICAL: (len(self.panels), 1),
        }
        
        return layout_map.get(self.layout, (2, 2))
    
    def generate_html(self) -> str:
        """Generate HTML for the multi-panel figure"""
        rows, cols = self._get_grid_dimensions()
        
        html_parts = []
        
        # Figure container
        html_parts.append(f'<figure class="multi-panel-figure" id="{self.figure_id}">')
        
        # Grid container
        html_parts.append(f'  <div class="panel-grid" data-rows="{rows}" data-cols="{cols}">')
        
        # Add panels
        for panel in self.panels:
            html_parts.append('    <div class="panel-item">')
            
            # Panel label
            if panel.label:
                html_parts.append(f'      <div class="panel-label">{panel.label}</div>')
            
            # Panel image
            html_parts.append(f'      <img src="{panel.path}" alt="{panel.alt_text}">')
            
            # Panel caption
            if panel.caption:
                html_parts.append(f'      <div class="panel-caption">{panel.caption}</div>')
            
            html_parts.append('    </div>')
        
        html_parts.append('  </div>')
        
        # Figure caption
        if self.caption:
            caption_html = self.caption
            if self.figure_number:
                caption_html = f"<strong>Figure {self.figure_number}:</strong> {caption_html}"
            html_parts.append(f'  <figcaption>{caption_html}</figcaption>')
        
        html_parts.append('</figure>')
        
        return '\n'.join(html_parts)


class AnnotatedImage:
    """
    Creates an image with annotations (arrows, labels, highlights).
    
    Example usage:
        annotated = AnnotatedImage(
            image=ImageMetadata(path="surgery.jpg", alt_text="Surgical view"),
            annotations=[
                Annotation(type="arrow", text="Target area", x=50, y=30, color="red"),
                Annotation(type="circle", x=60, y=40, color="yellow")
            ]
        )
        html = annotated.generate_html()
    """
    
    def __init__(
        self,
        image: ImageMetadata,
        annotations: List[Annotation],
        figure_number: Optional[str] = None,
        image_id: Optional[str] = None
    ):
        self.image = image
        self.annotations = annotations
        self.figure_number = figure_number
        self.image_id = image_id or f"annotated-{id(self)}"
    
    def generate_html(self) -> str:
        """Generate HTML for the annotated image"""
        html_parts = []
        
        html_parts.append(f'<div class="annotated-image-container" id="{self.image_id}">')
        html_parts.append('  <div class="annotated-image-wrapper">')
        
        # Base image
        html_parts.append(f'    <img src="{self.image.path}" alt="{self.image.alt_text}" '
                         f'class="base-image">')
        
        # Annotation overlay
        html_parts.append('    <svg class="annotation-overlay" viewBox="0 0 100 100" '
                         'preserveAspectRatio="none">')
        
        for idx, annotation in enumerate(self.annotations):
            if annotation.type == "arrow":
                html_parts.append(self._generate_arrow(annotation, idx))
            elif annotation.type == "circle":
                html_parts.append(self._generate_circle(annotation, idx))
            elif annotation.type == "rectangle":
                html_parts.append(self._generate_rectangle(annotation, idx))
            elif annotation.type == "label":
                html_parts.append(self._generate_label(annotation, idx))
        
        html_parts.append('    </svg>')
        html_parts.append('  </div>')
        
        # Caption
        if self.image.caption:
            caption_html = self.image.caption
            if self.figure_number:
                caption_html = f"<strong>Figure {self.figure_number}:</strong> {caption_html}"
            html_parts.append(f'  <div class="annotated-image-caption">{caption_html}</div>')
        
        html_parts.append('</div>')
        
        return '\n'.join(html_parts)
    
    def _generate_arrow(self, annotation: Annotation, idx: int) -> str:
        """Generate SVG arrow"""
        x, y = annotation.x or 50, annotation.y or 50
        return f'''
      <g class="annotation annotation-arrow" data-idx="{idx}">
        <line x1="{x-5}" y1="{y-5}" x2="{x}" y2="{y}" 
              stroke="{annotation.color}" stroke-width="0.5" marker-end="url(#arrowhead-{idx})"/>
        <defs>
          <marker id="arrowhead-{idx}" markerWidth="10" markerHeight="10" 
                  refX="5" refY="3" orient="auto">
            <polygon points="0 0, 10 3, 0 6" fill="{annotation.color}"/>
          </marker>
        </defs>
        {f'<text x="{x-7}" y="{y-7}" class="annotation-text" fill="{annotation.color}">{annotation.text}</text>' if annotation.text else ''}
      </g>'''
    
    def _generate_circle(self, annotation: Annotation, idx: int) -> str:
        """Generate SVG circle highlight"""
        x, y = annotation.x or 50, annotation.y or 50
        radius = 5 if annotation.size == "small" else 8 if annotation.size == "medium" else 12
        return f'''
      <circle class="annotation annotation-circle" data-idx="{idx}"
              cx="{x}" cy="{y}" r="{radius}"
              stroke="{annotation.color}" stroke-width="0.5" fill="none" opacity="0.7"/>'''
    
    def _generate_rectangle(self, annotation: Annotation, idx: int) -> str:
        """Generate SVG rectangle highlight"""
        x, y = annotation.x or 40, annotation.y or 40
        width = 10 if annotation.size == "small" else 15 if annotation.size == "medium" else 20
        height = width * 0.75
        return f'''
      <rect class="annotation annotation-rectangle" data-idx="{idx}"
            x="{x}" y="{y}" width="{width}" height="{height}"
            stroke="{annotation.color}" stroke-width="0.5" fill="none" opacity="0.7"/>'''
    
    def _generate_label(self, annotation: Annotation, idx: int) -> str:
        """Generate SVG text label"""
        x, y = annotation.x or 50, annotation.y or 50
        return f'''
      <text class="annotation annotation-label" data-idx="{idx}"
            x="{x}" y="{y}" fill="{annotation.color}">{annotation.text}</text>'''


class ComparisonSlider:
    """
    Creates an interactive before/after image comparison slider.
    
    Example usage:
        comparison = ComparisonSlider(
            before_image=ImageMetadata(path="before.jpg", alt_text="Before surgery"),
            after_image=ImageMetadata(path="after.jpg", alt_text="After surgery"),
            caption="Comparison of pre- and post-operative imaging"
        )
        html = comparison.generate_html()
    """
    
    def __init__(
        self,
        before_image: ImageMetadata,
        after_image: ImageMetadata,
        caption: Optional[str] = None,
        figure_number: Optional[str] = None,
        slider_id: Optional[str] = None,
        default_position: int = 50  # Percentage (0-100)
    ):
        self.before_image = before_image
        self.after_image = after_image
        self.caption = caption
        self.figure_number = figure_number
        self.slider_id = slider_id or f"comparison-{id(self)}"
        self.default_position = default_position
    
    def generate_html(self) -> str:
        """Generate HTML for the comparison slider"""
        html_parts = []
        
        html_parts.append(f'<div class="comparison-slider-container" id="{self.slider_id}">')
        html_parts.append('  <div class="comparison-slider-wrapper">')
        
        # After image (background)
        html_parts.append(f'    <img src="{self.after_image.path}" '
                         f'alt="{self.after_image.alt_text}" '
                         f'class="comparison-image comparison-after">')
        
        # Before image (foreground with clip)
        html_parts.append(f'    <div class="comparison-before-wrapper" '
                         f'style="width: {self.default_position}%;">')
        html_parts.append(f'      <img src="{self.before_image.path}" '
                         f'alt="{self.before_image.alt_text}" '
                         f'class="comparison-image comparison-before">')
        html_parts.append('    </div>')
        
        # Slider handle
        html_parts.append('    <div class="comparison-slider-handle" '
                         f'style="left: {self.default_position}%;">')
        html_parts.append('      <div class="slider-line"></div>')
        html_parts.append('      <div class="slider-button">&#8596;</div>')
        html_parts.append('    </div>')
        
        # Labels
        html_parts.append('    <div class="comparison-label comparison-label-before">Before</div>')
        html_parts.append('    <div class="comparison-label comparison-label-after">After</div>')
        
        html_parts.append('  </div>')
        
        # Caption
        if self.caption:
            caption_html = self.caption
            if self.figure_number:
                caption_html = f"<strong>Figure {self.figure_number}:</strong> {caption_html}"
            html_parts.append(f'  <div class="comparison-caption">{caption_html}</div>')
        
        html_parts.append('</div>')
        
        return '\n'.join(html_parts)


class StepByStepProcedure:
    """
    Creates a sequential visualization of surgical or procedural steps.
    
    Example usage:
        procedure = StepByStepProcedure(
            steps=[
                ImageMetadata(path="step1.jpg", alt_text="Step 1", caption="Initial incision"),
                ImageMetadata(path="step2.jpg", alt_text="Step 2", caption="Dissection"),
                ...
            ],
            title="Laparoscopic Gastrectomy Procedure"
        )
        html = procedure.generate_html()
    """
    
    def __init__(
        self,
        steps: List[ImageMetadata],
        title: Optional[str] = None,
        layout: str = "vertical",  # "vertical", "horizontal", or "grid"
        figure_number: Optional[str] = None,
        procedure_id: Optional[str] = None,
        numbered: bool = True
    ):
        self.steps = steps
        self.title = title
        self.layout = layout
        self.figure_number = figure_number
        self.procedure_id = procedure_id or f"procedure-{id(self)}"
        self.numbered = numbered
    
    def generate_html(self) -> str:
        """Generate HTML for the step-by-step procedure"""
        html_parts = []
        
        html_parts.append(f'<div class="procedure-container {self.layout}-layout" '
                         f'id="{self.procedure_id}">')
        
        # Title
        if self.title:
            title_html = self.title
            if self.figure_number:
                title_html = f"Figure {self.figure_number}: {title_html}"
            html_parts.append(f'  <h3 class="procedure-title">{title_html}</h3>')
        
        # Steps
        html_parts.append('  <div class="procedure-steps">')
        
        for idx, step in enumerate(self.steps, start=1):
            html_parts.append('    <div class="procedure-step">')
            
            # Step number
            if self.numbered:
                html_parts.append(f'      <div class="step-number">Step {idx}</div>')
            
            # Step image
            html_parts.append(f'      <img src="{step.path}" alt="{step.alt_text}" '
                             f'class="step-image">')
            
            # Step caption
            if step.caption:
                html_parts.append(f'      <div class="step-caption">{step.caption}</div>')
            
            html_parts.append('    </div>')
        
        html_parts.append('  </div>')
        html_parts.append('</div>')
        
        return '\n'.join(html_parts)


class SurgicalPhotoPanel:
    """
    Creates a professional presentation of surgical photographs.
    
    Example usage:
        panel = SurgicalPhotoPanel(
            photos=[ImageMetadata(...), ImageMetadata(...), ...],
            title="Intraoperative Findings",
            columns=2
        )
        html = panel.generate_html()
    """
    
    def __init__(
        self,
        photos: List[ImageMetadata],
        title: Optional[str] = None,
        columns: int = 2,
        figure_number: Optional[str] = None,
        panel_id: Optional[str] = None,
        show_privacy_notice: bool = True
    ):
        self.photos = photos
        self.title = title
        self.columns = columns
        self.figure_number = figure_number
        self.panel_id = panel_id or f"surgical-panel-{id(self)}"
        self.show_privacy_notice = show_privacy_notice
    
    def generate_html(self) -> str:
        """Generate HTML for the surgical photo panel"""
        html_parts = []
        
        html_parts.append(f'<div class="surgical-photo-panel" id="{self.panel_id}">')
        
        # Title
        if self.title:
            title_html = self.title
            if self.figure_number:
                title_html = f"Figure {self.figure_number}: {title_html}"
            html_parts.append(f'  <h3 class="panel-title">{title_html}</h3>')
        
        # Privacy notice
        if self.show_privacy_notice:
            html_parts.append('  <div class="privacy-notice">')
            html_parts.append('    <em>Note: All patient identifiers have been removed. '
                             'Informed consent obtained.</em>')
            html_parts.append('  </div>')
        
        # Photo grid
        html_parts.append(f'  <div class="photo-grid" data-columns="{self.columns}">')
        
        for photo in self.photos:
            html_parts.append('    <div class="photo-item">')
            html_parts.append(f'      <img src="{photo.path}" alt="{photo.alt_text}" '
                             f'class="surgical-photo">')
            
            if photo.caption:
                html_parts.append(f'      <div class="photo-caption">{photo.caption}</div>')
            
            html_parts.append('    </div>')
        
        html_parts.append('  </div>')
        html_parts.append('</div>')
        
        return '\n'.join(html_parts)


# Utility functions for image processing

def validate_image_path(path: str, base_dir: Optional[str] = None) -> bool:
    """Validate that an image path exists and is accessible"""
    if base_dir:
        full_path = os.path.join(base_dir, path)
    else:
        full_path = path
    
    return os.path.isfile(full_path)


def get_relative_path(absolute_path: str, base_dir: str) -> str:
    """Convert absolute path to relative path from base directory"""
    return os.path.relpath(absolute_path, base_dir)


def auto_generate_alt_text(filename: str) -> str:
    """Generate basic alt text from filename"""
    # Remove extension and convert separators to spaces
    name = Path(filename).stem
    name = re.sub(r'[-_]', ' ', name)
    return f"Medical image: {name}"


def create_figure_number(section: int, figure: int) -> str:
    """Create a formatted figure number (e.g., "3.2" for section 3, figure 2)"""
    return f"{section}.{figure}"


# Export all classes
__all__ = [
    'ImageGallery',
    'MultiPanelFigure',
    'AnnotatedImage',
    'ComparisonSlider',
    'StepByStepProcedure',
    'SurgicalPhotoPanel',
    'ImageMetadata',
    'Annotation',
    'ImageFormat',
    'PanelLayout',
    'validate_image_path',
    'get_relative_path',
    'auto_generate_alt_text',
    'create_figure_number',
]

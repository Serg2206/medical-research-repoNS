#!/usr/bin/env python3
"""
Comprehensive script to download and extract visual content from gastrectomy publications
Focuses on open access sources with high-quality images
"""

import os
import sys
import json
import time
import re
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime
import hashlib

# Install required packages
import subprocess
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "pymupdf", "beautifulsoup4", "lxml", "requests", "pillow"], check=True)

import fitz  # PyMuPDF
from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO

# Configuration
BASE_DIR = Path("/home/ubuntu/github_repos/medical-research-repoNS/reference-materials/visual-surgical-content")
TEMP_DIR = BASE_DIR / "temp"
MIN_IMAGE_SIZE = 300  # Minimum width/height in pixels
MAX_IMAGE_SIZE = 50 * 1024 * 1024  # 50MB max file size

# Open access sources we'll download from
OPEN_ACCESS_SOURCES = [
    {
        "name": "BMC Surgery - Double Tract Reconstruction",
        "url": "https://bmcsurg.biomedcentral.com/articles/10.1186/s12893-024-02454-8",
        "type": "html",
        "license": "CC BY 4.0",
        "procedure": "Double Tract Reconstruction"
    },
    {
        "name": "Annals of Laparoscopic Surgery - DTR Review",
        "url": "https://ales.amegroups.org/article/view/7407/html",
        "type": "html",
        "license": "CC BY-NC-ND 4.0",
        "procedure": "Minimally Invasive Proximal Gastrectomy"
    },
    {
        "name": "Korean Journal Radiology - Postop Imaging",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7289697/",
        "type": "html",
        "license": "CC BY-NC 4.0",
        "procedure": "Postoperative Imaging"
    },
    {
        "name": "Frontiers Oncology - 3D Navigation",
        "url": "https://www.frontiersin.org/journals/oncology/articles/10.3389/fonc.2023.1140175/full",
        "type": "html",
        "license": "CC BY 4.0",
        "procedure": "3D Surgical Navigation"
    },
    {
        "name": "Scientific Reports - 3D Visualization",
        "url": "https://www.nature.com/articles/s41598-019-40269-3",
        "type": "html",
        "license": "CC BY 4.0",
        "procedure": "3D Laparoscopic Visualization"
    },
    {
        "name": "Int J Surgery Case Reports - DTR Surveillance",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC5544470/",
        "type": "html",
        "license": "CC BY-NC-ND 4.0",
        "procedure": "Double Tract with Duodenal Surveillance"
    }
]

# Index data structure
index_data = []
download_log = []

def setup_directories():
    """Ensure all directories exist"""
    for subdir in ['surgical-photos', 'anatomical-diagrams', 'procedure-steps', 'results-data', '3d-reconstructions', 'videos', 'temp']:
        (BASE_DIR / subdir).mkdir(parents=True, exist_ok=True)
    print(f"✓ Directory structure verified")

def sanitize_filename(name):
    """Create a safe filename"""
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '_', name)
    return name[:200]

def get_image_hash(img_data):
    """Generate hash for image deduplication"""
    return hashlib.md5(img_data).hexdigest()

def categorize_image(filename, alt_text, context, img_url):
    """Determine appropriate category for an image"""
    combined_text = f"{filename} {alt_text} {context}".lower()
    
    # Priority-based categorization
    if any(word in combined_text for word in ['intraoperative', 'surgical field', 'laparoscopic view', 'operative', 'dissection']):
        return 'surgical-photos'
    elif any(word in combined_text for word in ['anatomy', 'anatomical', 'vessel', 'artery', 'vein', 'lymph node']):
        return 'anatomical-diagrams'
    elif any(word in combined_text for word in ['step', 'procedure', 'technique', 'reconstruction', 'anastomosis', 'schematic']):
        return 'procedure-steps'
    elif any(word in combined_text for word in ['graph', 'chart', 'table', 'result', 'outcome', 'data', 'survival']):
        return 'results-data'
    elif any(word in combined_text for word in ['3d', 'ct', 'mri', 'reconstruction', 'model', 'virtual']):
        return '3d-reconstructions'
    elif 'fig' in combined_text or 'figure' in combined_text:
        # Default figures to procedure-steps
        return 'procedure-steps'
    else:
        # Default category
        return 'anatomical-diagrams'

def download_image(img_url, source_name, base_url=""):
    """Download an image and return its data"""
    try:
        # Handle relative URLs
        if img_url.startswith('//'):
            img_url = 'https:' + img_url
        elif img_url.startswith('/'):
            parsed = urllib.parse.urlparse(base_url)
            img_url = f"{parsed.scheme}://{parsed.netloc}{img_url}"
        elif not img_url.startswith('http'):
            img_url = urllib.parse.urljoin(base_url, img_url)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(img_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Check file size
        if len(response.content) > MAX_IMAGE_SIZE:
            print(f"  ⚠ Image too large: {len(response.content)} bytes")
            return None
        
        # Verify it's actually an image
        try:
            img = Image.open(BytesIO(response.content))
            width, height = img.size
            
            # Check minimum dimensions
            if width < MIN_IMAGE_SIZE or height < MIN_IMAGE_SIZE:
                print(f"  ⚠ Image too small: {width}x{height}px")
                return None
            
            return response.content, img.format.lower(), width, height
        except Exception as e:
            print(f"  ⚠ Not a valid image: {e}")
            return None
            
    except Exception as e:
        print(f"  ⚠ Failed to download {img_url}: {e}")
        return None

def extract_from_html(source):
    """Extract images from HTML article"""
    print(f"\n{'='*80}")
    print(f"Processing: {source['name']}")
    print(f"URL: {source['url']}")
    print(f"{'='*80}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(source['url'], headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Find all images
        images = soup.find_all('img')
        print(f"Found {len(images)} images in HTML")
        
        downloaded_hashes = set()
        image_count = 0
        
        for idx, img in enumerate(images, 1):
            img_url = img.get('src') or img.get('data-src')
            if not img_url:
                continue
            
            # Get context information
            alt_text = img.get('alt', '')
            title = img.get('title', '')
            
            # Try to find figure caption
            parent_figure = img.find_parent('figure')
            caption = ''
            if parent_figure:
                caption_elem = parent_figure.find(['figcaption', 'caption'])
                if caption_elem:
                    caption = caption_elem.get_text(strip=True)
            
            context = f"{alt_text} {title} {caption}"
            
            print(f"\n  Image {idx}/{len(images)}: {img_url[:80]}...")
            
            # Download image
            result = download_image(img_url, source['name'], source['url'])
            if not result:
                continue
            
            img_data, img_format, width, height = result
            
            # Check for duplicates
            img_hash = get_image_hash(img_data)
            if img_hash in downloaded_hashes:
                print(f"  ⚠ Duplicate image, skipping")
                continue
            downloaded_hashes.add(img_hash)
            
            # Categorize image
            category = categorize_image(img_url, alt_text, context, img_url)
            
            # Generate filename
            source_abbrev = sanitize_filename(source['name'].split('-')[0].strip())
            img_filename = f"{source_abbrev}_{idx:03d}_{width}x{height}.{img_format}"
            
            # Save image
            output_path = BASE_DIR / category / img_filename
            with open(output_path, 'wb') as f:
                f.write(img_data)
            
            print(f"  ✓ Saved to: {category}/{img_filename} ({width}x{height}px)")
            
            # Add to index
            index_entry = {
                "filename": img_filename,
                "category": category,
                "source": source['name'],
                "source_url": source['url'],
                "image_url": img_url,
                "license": source['license'],
                "procedure": source['procedure'],
                "dimensions": f"{width}x{height}",
                "format": img_format,
                "alt_text": alt_text[:200],
                "caption": caption[:500],
                "download_date": datetime.now().isoformat()
            }
            index_data.append(index_entry)
            image_count += 1
        
        download_log.append({
            "source": source['name'],
            "url": source['url'],
            "status": "success",
            "images_downloaded": image_count,
            "timestamp": datetime.now().isoformat()
        })
        
        print(f"\n✓ Successfully downloaded {image_count} images from {source['name']}")
        time.sleep(2)  # Be respectful to servers
        
    except Exception as e:
        print(f"\n✗ Error processing {source['name']}: {e}")
        download_log.append({
            "source": source['name'],
            "url": source['url'],
            "status": "failed",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })

def extract_from_pmc(pmc_url):
    """Special handler for PubMed Central articles with better image quality"""
    try:
        # PMC articles often have high-res images in specific patterns
        # We'll try to get the full-size versions
        response = requests.get(pmc_url, timeout=30)
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Look for links to full-size images
        img_links = soup.find_all('a', href=re.compile(r'\.(jpg|jpeg|png|gif)$'))
        return [link['href'] for link in img_links]
    except:
        return []

def generate_visual_index():
    """Create comprehensive index markdown file"""
    print(f"\n{'='*80}")
    print("Generating visual content index...")
    print(f"{'='*80}")
    
    index_path = BASE_DIR / "visual-content-index.md"
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("# Visual Surgical Content Index\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total Images:** {len(index_data)}\n\n")
        
        # Summary by category
        f.write("## Content Summary by Category\n\n")
        categories = {}
        for entry in index_data:
            cat = entry['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        for cat, count in sorted(categories.items()):
            f.write(f"- **{cat.replace('-', ' ').title()}**: {count} images\n")
        
        # Summary by source
        f.write("\n## Content Summary by Source\n\n")
        sources = {}
        for entry in index_data:
            src = entry['source']
            sources[src] = sources.get(src, 0) + 1
        
        for src, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- **{src}**: {count} images\n")
        
        # Detailed listing by category
        f.write("\n## Detailed Image Inventory\n\n")
        
        for category in sorted(set(e['category'] for e in index_data)):
            category_images = [e for e in index_data if e['category'] == category]
            if not category_images:
                continue
            
            f.write(f"\n### {category.replace('-', ' ').title()} ({len(category_images)} images)\n\n")
            
            for entry in category_images:
                f.write(f"#### {entry['filename']}\n\n")
                f.write(f"- **Dimensions:** {entry['dimensions']}\n")
                f.write(f"- **Format:** {entry['format'].upper()}\n")
                f.write(f"- **Source:** {entry['source']}\n")
                f.write(f"- **Source URL:** {entry['source_url']}\n")
                f.write(f"- **License:** {entry['license']}\n")
                f.write(f"- **Procedure:** {entry['procedure']}\n")
                if entry['alt_text']:
                    f.write(f"- **Alt Text:** {entry['alt_text']}\n")
                if entry['caption']:
                    f.write(f"- **Caption:** {entry['caption']}\n")
                f.write(f"- **Downloaded:** {entry['download_date']}\n")
                f.write("\n---\n\n")
        
        # Download log
        f.write("\n## Download Log\n\n")
        for log_entry in download_log:
            status_icon = "✓" if log_entry['status'] == 'success' else "✗"
            f.write(f"{status_icon} **{log_entry['source']}**\n")
            f.write(f"   - URL: {log_entry['url']}\n")
            f.write(f"   - Status: {log_entry['status']}\n")
            if log_entry['status'] == 'success':
                f.write(f"   - Images Downloaded: {log_entry['images_downloaded']}\n")
            else:
                f.write(f"   - Error: {log_entry.get('error', 'Unknown')}\n")
            f.write(f"   - Timestamp: {log_entry['timestamp']}\n\n")
    
    print(f"✓ Index generated at: {index_path}")
    
    # Also save as JSON
    json_path = BASE_DIR / "visual-content-index.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            "generated": datetime.now().isoformat(),
            "total_images": len(index_data),
            "images": index_data,
            "download_log": download_log
        }, f, indent=2)
    
    print(f"✓ JSON index generated at: {json_path}")

def main():
    """Main execution"""
    print("\n" + "="*80)
    print("Visual Content Download and Extraction Pipeline")
    print("Focus: Open Access Gastrectomy Publications")
    print("="*80 + "\n")
    
    setup_directories()
    
    # Process all open access sources
    for source in OPEN_ACCESS_SOURCES:
        extract_from_html(source)
    
    # Generate comprehensive index
    generate_visual_index()
    
    # Final summary
    print("\n" + "="*80)
    print("DOWNLOAD COMPLETE")
    print("="*80)
    print(f"Total images downloaded: {len(index_data)}")
    print(f"Successful sources: {sum(1 for log in download_log if log['status'] == 'success')}")
    print(f"Failed sources: {sum(1 for log in download_log if log['status'] == 'failed')}")
    print(f"\nAll content saved to: {BASE_DIR}")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()

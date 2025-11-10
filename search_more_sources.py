#!/usr/bin/env python3
"""
Search and download additional gastrectomy images from open access sources
"""

import sys
import subprocess
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "requests", "beautifulsoup4", "lxml"], check=True)

import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path
import hashlib
from PIL import Image
from io import BytesIO
import time

BASE_DIR = Path("/home/ubuntu/github_repos/medical-research-repoNS/reference-materials/visual-surgical-content")
MIN_SIZE = 250
MAX_SIZE = 50 * 1024 * 1024

# Curated list of specific high-quality figures from the source document
CURATED_FIGURES = [
    # From Springer Nature articles
    "https://media.springernature.com/lw685/springer-static/image/art%3A10.1007%2Fs12893-024-02454-8/MediaObjects/12893_2024_2454_Fig1_HTML.png",
    "https://media.springernature.com/lw685/springer-static/image/art%3A10.1007%2Fs12893-024-02454-8/MediaObjects/12893_2024_2454_Fig2_HTML.png",
    "https://media.springernature.com/lw685/springer-static/image/art%3A10.1186%2Fs41598-019-40269-3/MediaObjects/41598_2019_40269_Fig1_HTML.png",
    "https://media.springernature.com/lw685/springer-static/image/art%3A10.1186%2Fs41598-019-40269-3/MediaObjects/41598_2019_40269_Fig2_HTML.png",
    "https://media.springernature.com/lw685/springer-static/image/art%3A10.1186%2Fs41598-019-40269-3/MediaObjects/41598_2019_40269_Fig3_HTML.png",
    # Frontiers images
    "https://www.frontiersin.org/files/Articles/1140175/fonc-13-1140175-HTML/image_m/fonc-13-1140175-g001.jpg",
    "https://www.frontiersin.org/files/Articles/1140175/fonc-13-1140175-HTML/image_m/fonc-13-1140175-g002.jpg",
    "https://www.frontiersin.org/files/Articles/1140175/fonc-13-1140175-HTML/image_m/fonc-13-1140175-g003.jpg",
    "https://www.frontiersin.org/files/Articles/1140175/fonc-13-1140175-HTML/image_m/fonc-13-1140175-g004.jpg",
    # Korean Journal of Radiology - PMC figures
    "https://www.kjronline.org/upload/thumbnails/kjr-21-793-g001-l.jpg",
    "https://www.kjronline.org/upload/thumbnails/kjr-21-793-g002-l.jpg",
    "https://www.kjronline.org/upload/thumbnails/kjr-21-793-g003-l.jpg",
    "https://www.kjronline.org/upload/thumbnails/kjr-21-793-g004-l.jpg",
]

def load_existing():
    """Load existing image hashes"""
    hashes = set()
    for ext in ['*.png', '*.jpg', '*.jpeg']:
        for img_path in BASE_DIR.rglob(ext):
            if img_path.parent.name != 'temp':
                with open(img_path, 'rb') as f:
                    hashes.add(hashlib.md5(f.read()).hexdigest())
    return hashes

def download_and_save(url, category, source_name, existing_hashes):
    """Download image and save if valid"""
    try:
        if not url.startswith('http'):
            url = 'https:' + url if url.startswith('//') else 'https://' + url
        
        print(f"  Fetching: {url[:80]}...")
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; ResearchBot/1.0)'}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        if len(response.content) > MAX_SIZE or len(response.content) < 1000:
            return False
        
        # Check hash
        img_hash = hashlib.md5(response.content).hexdigest()
        if img_hash in existing_hashes:
            print(f"    ⚠ Duplicate")
            return False
        
        # Validate
        img = Image.open(BytesIO(response.content))
        w, h = img.size
        
        if w < MIN_SIZE or h < MIN_SIZE:
            print(f"    ⚠ Too small: {w}x{h}")
            return False
        
        # Generate filename
        source_abbr = re.sub(r'[^\w]', '_', source_name)[:30]
        count = len(list((BASE_DIR / category).glob(f"{source_abbr}*"))) + 1
        filename = f"{source_abbr}_{count:03d}_{w}x{h}.{img.format.lower()}"
        
        output_path = BASE_DIR / category / filename
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        existing_hashes.add(img_hash)
        print(f"    ✓ Saved: {category}/{filename} ({w}x{h})")
        return True
        
    except Exception as e:
        print(f"    ✗ Error: {str(e)[:60]}")
        return False

def main():
    print("\n" + "="*80)
    print("Searching for Additional High-Quality Gastrectomy Images")
    print("="*80 + "\n")
    
    existing_hashes = load_existing()
    print(f"Loaded {len(existing_hashes)} existing image hashes\n")
    
    downloaded = 0
    
    # Download curated high-quality figures
    print("--- Downloading Curated High-Quality Figures ---\n")
    
    for idx, url in enumerate(CURATED_FIGURES, 1):
        print(f"[{idx}/{len(CURATED_FIGURES)}]")
        
        # Determine source and category from URL
        if 'springer' in url or 'nature' in url:
            source = "Springer_Nature"
            category = 'procedure-steps' if 'Fig1' in url or 'Fig2' in url else '3d-reconstructions'
        elif 'frontiers' in url:
            source = "Frontiers"
            category = '3d-reconstructions'
        elif 'kjronline' in url or 'kjr' in url:
            source = "KJR_PMC"
            category = 'anatomical-diagrams'
        else:
            source = "OpenAccess"
            category = 'procedure-steps'
        
        if download_and_save(url, category, source, existing_hashes):
            downloaded += 1
        
        time.sleep(0.5)  # Be respectful
    
    print("\n" + "="*80)
    print(f"Search Complete: {downloaded} new images downloaded")
    print(f"Total collection: {len(existing_hashes) + downloaded} images")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()

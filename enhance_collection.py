#!/usr/bin/env python3
"""
Enhanced script to collect more visual content with adjusted parameters
"""

import sys
import subprocess
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "requests", "beautifulsoup4", "lxml", "pillow"], check=True)

import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re
import hashlib
from PIL import Image
from io import BytesIO
import json

BASE_DIR = Path("/home/ubuntu/github_repos/medical-research-repoNS/reference-materials/visual-surgical-content")
MIN_IMAGE_SIZE = 250  # Slightly lower threshold for diagrams
MAX_IMAGE_SIZE = 50 * 1024 * 1024

# Additional open access sources from research
ADDITIONAL_SOURCES = [
    {
        "name": "Springer - DTR Figure",
        "url": "https://media.springernature.com/lw1200/springer-static/image/art%3A10.1007%2Fs00423-024-03339-3/MediaObjects/423_2024_3339_Fig8_HTML.png",
        "type": "direct_image",
        "license": "Open Access",
        "procedure": "Double Tract Reconstruction"
    },
    {
        "name": "Wikimedia - Billroth II",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Diagram_showing_the_anatomy_after_a_partial_gastrectomy_%28Bilroth_02%29_CRUK_281.svg/1200px-Diagram_showing_the_anatomy_after_a_partial_gastrectomy_%28Bilroth_02%29_CRUK_281.svg.png",
        "type": "direct_image",
        "license": "CC BY-SA 4.0",
        "procedure": "Billroth II Gastrectomy"
    },
    {
        "name": "PMC Surgical Education",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC5544470/",
        "type": "html",
        "license": "CC BY-NC-ND 4.0",
        "procedure": "Double Tract Reconstruction"
    }
]

# Try to fetch high-res versions from PMC
PMC_HIGHRES_PATTERNS = [
    "/articles/PMC7289697/bin/",
    "/articles/PMC5544470/bin/"
]

def load_existing_hashes():
    """Load hashes of existing images to avoid duplicates"""
    hashes = set()
    for img_path in BASE_DIR.rglob("*.png"):
        with open(img_path, 'rb') as f:
            hashes.add(hashlib.md5(f.read()).hexdigest())
    for img_path in BASE_DIR.rglob("*.jpg"):
        with open(img_path, 'rb') as f:
            hashes.add(hashlib.md5(f.read()).hexdigest())
    return hashes

def download_image(url, source_name, existing_hashes):
    """Download image if not duplicate"""
    try:
        if not url.startswith('http'):
            if url.startswith('//'):
                url = 'https:' + url
            else:
                return None
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        if len(response.content) > MAX_IMAGE_SIZE:
            return None
        
        # Check hash
        img_hash = hashlib.md5(response.content).hexdigest()
        if img_hash in existing_hashes:
            print(f"  ⚠ Duplicate image, skipping")
            return None
        
        # Validate image
        img = Image.open(BytesIO(response.content))
        width, height = img.size
        
        if width < MIN_IMAGE_SIZE or height < MIN_IMAGE_SIZE:
            print(f"  ⚠ Image too small: {width}x{height}px")
            return None
        
        existing_hashes.add(img_hash)
        return response.content, img.format.lower(), width, height, img_hash
        
    except Exception as e:
        print(f"  ⚠ Failed: {e}")
        return None

def categorize_image(url, alt_text, context):
    """Categorize image based on content"""
    combined = f"{url} {alt_text} {context}".lower()
    
    if any(w in combined for w in ['3d', 'ct', 'mri', 'reconstruction']):
        return '3d-reconstructions'
    elif any(w in combined for w in ['intraoperative', 'surgical field', 'laparoscopic']):
        return 'surgical-photos'
    elif any(w in combined for w in ['anatomy', 'vessel', 'lymph', 'diagram']):
        return 'anatomical-diagrams'
    elif any(w in combined for w in ['step', 'procedure', 'technique', 'anastomosis']):
        return 'procedure-steps'
    elif any(w in combined for w in ['graph', 'chart', 'table', 'data']):
        return 'results-data'
    else:
        return 'procedure-steps'

def fetch_pmc_highres(pmc_id):
    """Try to fetch high-resolution images from PMC"""
    images_found = []
    try:
        # PMC articles often have full-res images in /bin/ directory
        base_url = f"https://pmc.ncbi.nlm.nih.gov/articles/{pmc_id}/"
        response = requests.get(base_url, timeout=30)
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Look for figure links
        fig_links = soup.find_all('a', href=re.compile(r'bin/.*\.(jpg|jpeg|png|gif)'))
        for link in fig_links:
            img_url = link['href']
            if not img_url.startswith('http'):
                img_url = 'https://pmc.ncbi.nlm.nih.gov' + img_url
            images_found.append(img_url)
        
        # Also check for inline high-res images
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if '/bin/' in src or 'large' in src or 'fig' in src.lower():
                if not src.startswith('http'):
                    if src.startswith('//'):
                        src = 'https:' + src
                    else:
                        src = 'https://pmc.ncbi.nlm.nih.gov' + src
                images_found.append(src)
        
    except Exception as e:
        print(f"Error fetching PMC high-res: {e}")
    
    return images_found

def main():
    print("\n" + "="*80)
    print("Enhanced Visual Content Collection")
    print("="*80 + "\n")
    
    existing_hashes = load_existing_hashes()
    print(f"Loaded {len(existing_hashes)} existing image hashes")
    
    new_images = []
    total_downloaded = 0
    
    # Try to get high-res from PMC articles
    print("\n--- Fetching High-Resolution PMC Images ---")
    pmc_ids = ["PMC7289697", "PMC5544470"]
    for pmc_id in pmc_ids:
        print(f"\nSearching {pmc_id}...")
        highres_urls = fetch_pmc_highres(pmc_id)
        print(f"Found {len(highres_urls)} potential high-res images")
        
        for idx, url in enumerate(highres_urls, 1):
            print(f"  [{idx}/{len(highres_urls)}] {url[:80]}...")
            result = download_image(url, f"PMC-{pmc_id}", existing_hashes)
            if result:
                img_data, fmt, w, h, img_hash = result
                category = categorize_image(url, "", pmc_id)
                filename = f"PMC_{pmc_id}_{idx:03d}_{w}x{h}.{fmt}"
                output_path = BASE_DIR / category / filename
                
                with open(output_path, 'wb') as f:
                    f.write(img_data)
                
                print(f"  ✓ Saved: {category}/{filename} ({w}x{h}px)")
                total_downloaded += 1
                
                new_images.append({
                    "filename": filename,
                    "category": category,
                    "source": f"PubMed Central {pmc_id}",
                    "dimensions": f"{w}x{h}",
                    "format": fmt
                })
    
    # Download direct image links
    print("\n--- Downloading Direct Image Links ---")
    for source in ADDITIONAL_SOURCES:
        if source['type'] == 'direct_image':
            print(f"\n{source['name']}")
            print(f"  URL: {source['url'][:80]}...")
            
            result = download_image(source['url'], source['name'], existing_hashes)
            if result:
                img_data, fmt, w, h, img_hash = result
                category = categorize_image(source['url'], source['procedure'], source['name'])
                
                safe_name = re.sub(r'[^\w\s-]', '', source['name'])
                safe_name = re.sub(r'[-\s]+', '_', safe_name)
                filename = f"{safe_name}_{w}x{h}.{fmt}"
                output_path = BASE_DIR / category / filename
                
                with open(output_path, 'wb') as f:
                    f.write(img_data)
                
                print(f"  ✓ Saved: {category}/{filename} ({w}x{h}px)")
                total_downloaded += 1
                
                new_images.append({
                    "filename": filename,
                    "category": category,
                    "source": source['name'],
                    "license": source['license'],
                    "procedure": source['procedure'],
                    "dimensions": f"{w}x{h}",
                    "format": fmt
                })
        
        elif source['type'] == 'html':
            print(f"\n{source['name']}")
            print(f"  Scraping: {source['url']}")
            try:
                response = requests.get(source['url'], timeout=30)
                soup = BeautifulSoup(response.text, 'lxml')
                images = soup.find_all('img')
                
                for idx, img in enumerate(images, 1):
                    img_url = img.get('src') or img.get('data-src')
                    if not img_url:
                        continue
                    
                    result = download_image(img_url, source['name'], existing_hashes)
                    if result:
                        img_data, fmt, w, h, img_hash = result
                        category = categorize_image(img_url, img.get('alt', ''), source['procedure'])
                        
                        safe_name = re.sub(r'[^\w\s-]', '', source['name'])
                        safe_name = re.sub(r'[-\s]+', '_', safe_name)
                        filename = f"{safe_name}_{idx:03d}_{w}x{h}.{fmt}"
                        output_path = BASE_DIR / category / filename
                        
                        with open(output_path, 'wb') as f:
                            f.write(img_data)
                        
                        print(f"  ✓ Saved: {category}/{filename}")
                        total_downloaded += 1
                        
                        new_images.append({
                            "filename": filename,
                            "category": category,
                            "source": source['name'],
                            "dimensions": f"{w}x{h}",
                            "format": fmt
                        })
            except Exception as e:
                print(f"  ✗ Error: {e}")
    
    # Save summary
    if new_images:
        summary_path = BASE_DIR / "enhanced-collection-summary.json"
        with open(summary_path, 'w') as f:
            json.dump({
                "total_new_images": total_downloaded,
                "images": new_images
            }, f, indent=2)
        
        print(f"\n✓ Summary saved to: {summary_path}")
    
    print("\n" + "="*80)
    print(f"Enhanced Collection Complete: {total_downloaded} new images downloaded")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()

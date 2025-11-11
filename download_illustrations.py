#!/usr/bin/env python3
"""Download all 25 generated illustrations from CDN URLs."""

import requests
import os
from pathlib import Path

# Base directory
base_dir = Path("training-materials/generated-illustrations")
base_dir.mkdir(parents=True, exist_ok=True)

# All illustrations with their CDN URLs
illustrations = [
    ("01_stomach_anatomy_detailed.png", "https://static.abacusaicdn.net/images/3311b1fa-b2a1-45ae-9107-c585157b32b2.png"),
    ("02_stomach_blood_supply.png", "https://static.abacusaicdn.net/images/f9d114c7-dbd1-4b6c-b5b4-d94b792c72f2.png"),
    ("03_lymph_node_stations.png", "https://static.abacusaicdn.net/images/1f2ecdbc-cf7a-429f-8356-106da5a13ea9.png"),
    ("04_stomach_anatomical_relationships.png", "https://static.abacusaicdn.net/images/d24b4ba6-12f3-4012-b62c-cf6e183c1cae.png"),
    ("05_step1_patient_positioning.png", "https://static.abacusaicdn.net/images/79a23933-157b-40c5-8e33-9df0bdb1a15d.png"),
    ("06_step2_stomach_mobilization.png", "https://static.abacusaicdn.net/images/d3486eda-58cb-468f-9897-550fb303f7d0.png"),
    ("07_step3_lymph_node_dissection.png", "https://static.abacusaicdn.net/images/45e43abc-c021-4f07-94bd-2646f2a5ae3d.png"),
    ("08_step4_vascular_ligation.png", "https://static.abacusaicdn.net/images/53385515-f890-442d-8b43-1442a7f98402.png"),
    ("09_step5_gastric_resection.png", "https://static.abacusaicdn.net/images/1bc5e29b-9839-4ee8-9c1f-fa1828067512.png"),
    ("10_step6_esophageal_preparation.png", "https://static.abacusaicdn.net/images/d1bfefe7-8a96-4c4f-8b2b-f1b46b70a396.png"),
    ("11_step7_reconstruction_preparation.png", "https://static.abacusaicdn.net/images/5a4272f1-eeb8-4f88-97ab-b935b7f78f6e.png"),
    ("12_step8_final_anastomosis.png", "https://static.abacusaicdn.net/images/b6715551-9191-4d9a-b796-4c8c5f9f5f4f.png"),
    ("13_double_tract_configuration.png", "https://static.abacusaicdn.net/images/9fa4a1f6-50a1-4ce8-8821-54a25748f31b.png"),
    ("14_esophagogastrostomy_technique.png", "https://static.abacusaicdn.net/images/e9894f58-a467-4792-8880-3d46e6a0f60d.png"),
    ("15_gastrojejunostomy_technique.png", "https://static.abacusaicdn.net/images/412b7520-8a4f-4500-ad67-ff10adfdd432.png"),
    ("16_jejunojejunostomy_roux.png", "https://static.abacusaicdn.net/images/3ceb3076-883b-47fb-9e18-94805bfa845c.png"),
    ("17_alternative_variations.png", "https://static.abacusaicdn.net/images/9e08f9a0-69e7-4169-921b-71f96b474c6c.png"),
    ("18_3d_reconstruction_complete.png", "https://static.abacusaicdn.net/images/9bea937c-a318-44df-8592-0ad654e56454.png"),
    ("19_handsewn_anastomosis.png", "https://static.abacusaicdn.net/images/850234d2-769d-495f-87fa-a5a737918d2c.png"),
    ("20_stapled_anastomosis.png", "https://static.abacusaicdn.net/images/dad4b374-9ae2-4416-a06d-b86af3616843.png"),
    ("21_circular_stapler_steps.png", "https://static.abacusaicdn.net/images/4af7a95d-caa5-4f1b-a68a-194daa8568d8.png"),
    ("22_linear_stapler_detail.png", "https://static.abacusaicdn.net/images/ce153d4b-2275-4f76-b895-fb82c3924bd6.png"),
    ("23_reflux_prevention.png", "https://static.abacusaicdn.net/images/6154bb77-4e89-4ca2-9225-fe9418828737.png"),
    ("24_drainage_placement.png", "https://static.abacusaicdn.net/images/c4d157bc-e67d-4210-99a4-ce95dafac8e4.png"),
    ("25_safety_zones.png", "https://static.abacusaicdn.net/images/4fe544a4-142d-4668-961b-94cea54529ac.png"),
]

print("Starting download of 25 illustrations...")
print("=" * 70)

success_count = 0
failed = []

for filename, url in illustrations:
    filepath = base_dir / filename
    
    # Skip if already exists
    if filepath.exists():
        print(f"✓ Already exists: {filename}")
        success_count += 1
        continue
    
    try:
        print(f"Downloading: {filename}...", end=" ")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        size_kb = len(response.content) / 1024
        print(f"✓ Success ({size_kb:.1f} KB)")
        success_count += 1
        
    except Exception as e:
        print(f"✗ Failed: {e}")
        failed.append((filename, str(e)))

print("=" * 70)
print(f"\nDownload Summary:")
print(f"  Successfully downloaded: {success_count}/25")
if failed:
    print(f"  Failed downloads: {len(failed)}")
    for filename, error in failed:
        print(f"    - {filename}: {error}")
else:
    print("  All illustrations downloaded successfully!")

print(f"\nImages saved to: {base_dir.absolute()}")

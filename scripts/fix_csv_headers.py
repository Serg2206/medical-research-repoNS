#!/usr/bin/env python3
"""Fix CSV file by removing invalid header rows"""

import csv
import sys

# Read the CSV file
with open("training-data/medical_training_data.csv", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Filter out lines that don't have proper CSV structure
# Invalid lines are those that don't contain commas (are just section headers)
valid_lines = []
for i, line in enumerate(lines):
    # Skip if line is just a header without commas
    if i == 0:  # Keep the header row
        valid_lines.append(line)
    elif "," in line:  # Only keep lines with CSV data
        valid_lines.append(line)
    else:
        print(f"Removing invalid line {i+1}: {line.strip()}")

# Write back the cleaned CSV
with open("training-data/medical_training_data.csv", "w", encoding="utf-8") as f:
    f.writelines(valid_lines)

print(
    f"\nDone! Kept {len(valid_lines)} valid lines, removed {len(lines) - len(valid_lines)} invalid lines"
)

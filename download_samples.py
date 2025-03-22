#!/usr/bin/env python
"""
Script to download sample CISSP study materials for testing.
"""
import os
import sys
import requests
from pathlib import Path
from tqdm import tqdm

# Add the project root to the path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

import config

# Sample CISSP materials (these are public domain or freely available resources)
SAMPLE_MATERIALS = [
    {
        "name": "NIST.SP.800-53r5.pdf",
        "url": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf",
        "description": "NIST Special Publication 800-53 (Security and Privacy Controls)"
    },
    {
        "name": "NIST.SP.800-171r2.pdf",
        "url": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-171r2.pdf",
        "description": "NIST Special Publication 800-171 (Protecting Controlled Unclassified Information)"
    },
    {
        "name": "NIST.CSWP.04162018.pdf",
        "url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.04162018.pdf",
        "description": "NIST Cybersecurity Framework"
    }
]


def download_file(url, destination):
    """
    Download a file from a URL to a destination with progress bar.
    
    Args:
        url: URL to download from
        destination: Path to save the file to
    """
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    block_size = 8192
    
    with open(destination, 'wb') as f:
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=os.path.basename(destination)) as pbar:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))


def main():
    """Main function to download sample materials."""
    # Create the PDF directory if it doesn't exist
    os.makedirs(config.PDF_DIR, exist_ok=True)
    
    print(f"Downloading sample CISSP study materials to {config.PDF_DIR}")
    
    for material in SAMPLE_MATERIALS:
        destination = os.path.join(config.PDF_DIR, material["name"])
        
        if os.path.exists(destination):
            print(f"File already exists: {material['name']}")
            continue
        
        print(f"Downloading {material['description']}...")
        try:
            download_file(material["url"], destination)
            print(f"Successfully downloaded {material['name']}")
        except Exception as e:
            print(f"Error downloading {material['name']}: {e}")
    
    print("\nDownload complete!")
    print(f"Downloaded {len(SAMPLE_MATERIALS)} sample documents to {config.PDF_DIR}")
    print("\nNext steps:")
    print("1. Run 'python -m src.ingestion.ingest' to process the PDFs")
    print("2. Run 'python run_app.py' to start the web interface")
    print("   or 'python cli.py ask \"What is the CIA triad?\"' to use the CLI")


if __name__ == "__main__":
    main()

import os
import sys
from typing import List
from .core.scholar_downloader import ScholarDownloader

def read_titles(file_path: str) -> List[str]:
    """Read paper titles from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def main():
    if len(sys.argv) != 2:
        print("Usage: python -m citescholareasy <titles_file>")
        sys.exit(1)

    titles_file = sys.argv[1]
    if not os.path.exists(titles_file):
        print(f"Error: File '{titles_file}' not found.")
        sys.exit(1)

    # Read titles from file
    titles = read_titles(titles_file)
    if not titles:
        print("No titles found in the input file.")
        sys.exit(1)

    # Create output directory
    output_dir = 'downloads'
    
    # Download citations
    print(f"Found {len(titles)} titles. Starting download...")
    with ScholarDownloader(headless=True) as downloader:
        downloaded_files = downloader.download_citations(titles, output_dir)
    
    # Print summary
    print("\nDownload Summary:")
    print(f"Successfully downloaded: {len(downloaded_files)} citations")
    print(f"Failed: {len(titles) - len(downloaded_files)} citations")
    print(f"\nFiles saved in: {os.path.abspath(output_dir)}")

if __name__ == '__main__':
    main() 
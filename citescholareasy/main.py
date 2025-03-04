import os
from core.scholar_search import ScholarSearcher
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_titles(file_path: str) -> list:
    """Read paper titles from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        logger.error(f"Error reading titles file: {str(e)}")
        return []

def save_endnote(title: str, content: str, output_dir: str = 'output'):
    """Save EndNote content to a file."""
    try:
        os.makedirs(output_dir, exist_ok=True)
        # Create a valid filename from the title
        filename = "".join(x for x in title if x.isalnum() or x in (' ', '-', '_'))
        filename = filename.replace(' ', '_')[:100] + '.enw'
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Saved EndNote file: {filepath}")
    except Exception as e:
        logger.error(f"Error saving EndNote file: {str(e)}")

def main():
    # Initialize the searcher
    searcher = ScholarSearcher()
    
    # Read titles from file
    titles = read_titles('title.txt')
    if not titles:
        logger.error("No titles found in title.txt")
        return
        
    # Process each title
    for title in titles:
        logger.info(f"Processing title: {title}")
        
        # Search for the paper
        paper_info = searcher.search_paper(title)
        if not paper_info:
            logger.warning(f"No results found for: {title}")
            continue
            
        # Format and save EndNote
        endnote_content = searcher.format_endnote(paper_info)
        if endnote_content:
            save_endnote(title, endnote_content)
        else:
            logger.warning(f"Could not generate EndNote content for: {title}")

if __name__ == "__main__":
    main() 
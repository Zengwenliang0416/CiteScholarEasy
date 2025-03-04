from scholarly import scholarly
import time
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScholarSearcher:
    def __init__(self):
        """Initialize the ScholarSearcher."""
        self.delay = 2  # Delay between requests to avoid being blocked

    def search_paper(self, title: str) -> Optional[Dict]:
        """
        Search for a paper on Google Scholar and return the best match.
        
        Args:
            title (str): The title of the paper to search for
            
        Returns:
            dict: Paper information if found, None otherwise
        """
        try:
            logger.info(f"Searching for paper: {title}")
            search_query = scholarly.search_pubs(title)
            first_result = next(search_query, None)
            
            if first_result:
                # Add delay to avoid too many requests
                time.sleep(self.delay)
                return {
                    'title': first_result['bib'].get('title', ''),
                    'author': first_result['bib'].get('author', []),
                    'year': first_result['bib'].get('year', ''),
                    'venue': first_result['bib'].get('venue', ''),
                    'abstract': first_result['bib'].get('abstract', ''),
                    'url': first_result.get('pub_url', '')
                }
            return None
            
        except Exception as e:
            logger.error(f"Error searching for paper: {str(e)}")
            return None

    def format_endnote(self, paper_info: Dict) -> str:
        """
        Format paper information into EndNote format.
        
        Args:
            paper_info (dict): Paper information
            
        Returns:
            str: EndNote formatted citation
        """
        if not paper_info:
            return ""
            
        endnote = "%0 Journal Article\n"
        endnote += f"%T {paper_info['title']}\n"
        
        # Add authors
        for author in paper_info['author']:
            endnote += f"%A {author}\n"
            
        if paper_info['year']:
            endnote += f"%D {paper_info['year']}\n"
        if paper_info['venue']:
            endnote += f"%J {paper_info['venue']}\n"
        if paper_info['abstract']:
            endnote += f"%X {paper_info['abstract']}\n"
        if paper_info['url']:
            endnote += f"%U {paper_info['url']}\n"
            
        return endnote 
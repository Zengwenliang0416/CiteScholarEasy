import os
import time
from typing import List, Optional
from playwright.sync_api import sync_playwright, Browser, Page
from tqdm import tqdm

class ScholarDownloader:
    def __init__(self, headless: bool = True):
        """
        Initialize the ScholarDownloader.
        
        Args:
            headless (bool): Whether to run browser in headless mode
        """
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None
        
    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.page:
            self.page.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
            
    def download_citations(self, titles: List[str], output_dir: str) -> List[str]:
        """
        Download EndNote citations for given paper titles.
        
        Args:
            titles (List[str]): List of paper titles to search for
            output_dir (str): Directory to save the EndNote files
            
        Returns:
            List[str]: List of paths to downloaded files
        """
        os.makedirs(output_dir, exist_ok=True)
        downloaded_files = []
        
        for title in tqdm(titles, desc="Downloading citations"):
            try:
                file_path = self._download_single_citation(title, output_dir)
                if file_path:
                    downloaded_files.append(file_path)
                time.sleep(2)  # Add delay between requests
            except Exception as e:
                print(f"Error downloading citation for '{title}': {str(e)}")
                
        return downloaded_files
    
    def _download_single_citation(self, title: str, output_dir: str) -> Optional[str]:
        """
        Download EndNote citation for a single paper title.
        
        Args:
            title (str): Paper title to search for
            output_dir (str): Directory to save the EndNote file
            
        Returns:
            Optional[str]: Path to downloaded file if successful, None otherwise
        """
        # Navigate to Google Scholar
        self.page.goto('https://scholar.google.com')
        
        # Search for the paper
        self.page.fill('input[name="q"]', title)
        self.page.press('input[name="q"]', 'Enter')
        self.page.wait_for_load_state('networkidle')
        
        # Click on cite button for the first result
        cite_button = self.page.get_by_role('button', name='Cite').first
        if not cite_button:
            print(f"No citation button found for '{title}'")
            return None
            
        cite_button.click()
        self.page.wait_for_selector('div[role="dialog"]')
        
        # Click on EndNote link
        endnote_link = self.page.get_by_role('link', name='EndNote').first
        if not endnote_link:
            print(f"No EndNote export option found for '{title}'")
            return None
            
        # Setup download path
        safe_title = "".join(x for x in title if x.isalnum() or x in (' ', '-', '_'))[:100]
        download_path = os.path.join(output_dir, f"{safe_title}.enw")
        
        # Download the file
        with self.page.expect_download() as download_info:
            endnote_link.click()
        download = download_info.value
        download.save_as(download_path)
        
        return download_path 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import os
import random
from difflib import SequenceMatcher
import undetected_chromedriver as uc
import sys
import glob
import shutil
from pathlib import Path
import urllib3
from urllib3.exceptions import MaxRetryError, NewConnectionError
import socket
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CiteDownloader:
    def __init__(self, download_dir="downloads", headless=True, max_retries=3):
        """Initialize the downloader with Chrome options"""
        self.download_dir = os.path.abspath(download_dir)
        self.max_retries = max_retries
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
        
        # 初始化选项移到单独的方法
        self.options = self._initialize_chrome_options(headless)
        
    def _initialize_chrome_options(self, headless):
        """Initialize Chrome options with all necessary settings"""
        options = uc.ChromeOptions()
        
        # Add preferences
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.default_content_settings.popups": 0,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
        options.add_experimental_option("prefs", prefs)
        
        if headless:
            options.add_argument('--headless=new')
        
        # Add additional arguments for stability and privacy
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-automation')
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Add random user agent
        user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        ]
        options.add_argument(f'--user-agent={random.choice(user_agents)}')
        
        return options

    def _initialize_driver(self):
        """Initialize WebDriver with retry mechanism"""
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                driver = uc.Chrome(options=self.options)
                # 测试连接是否正常
                driver.get("about:blank")
                return driver
            except (socket.error, urllib3.exceptions.MaxRetryError,
                    urllib3.exceptions.NewConnectionError) as e:
                retry_count += 1
                logger.warning(f"WebDriver 初始化失败 (尝试 {retry_count}/{self.max_retries}): {str(e)}")
                if retry_count < self.max_retries:
                    time.sleep(2 ** retry_count)  # 指数退避
                    continue
                else:
                    raise Exception("WebDriver 初始化失败，已达到最大重试次数")
            except Exception as e:
                logger.error(f"WebDriver 初始化时发生未知错误: {str(e)}")
                raise

    def random_sleep(self, min_time=2, max_time=5):
        """Sleep for a random amount of time"""
        time.sleep(random.uniform(min_time, max_time))
        
    def simulate_human_typing(self, element, text):
        """Simulate human-like typing with variable speed and occasional mistakes"""
        for char in text:
            if random.random() < 0.05:  # 5% chance to make a typo
                typo = random.choice('qwertyuiopasdfghjklzxcvbnm')
                element.send_keys(typo)
                time.sleep(random.uniform(0.1, 0.3))
                element.send_keys(Keys.BACKSPACE)
                time.sleep(random.uniform(0.1, 0.3))
            element.send_keys(char)
            # Vary typing speed
            if char in [' ', '.', ',']:
                time.sleep(random.uniform(0.3, 0.7))  # Longer pause after punctuation
            else:
                time.sleep(random.uniform(0.1, 0.4))  # Normal typing speed
            
    def add_random_noise(self, text):
        """Add random spaces and line breaks to text to avoid pattern detection"""
        words = text.split()
        result = []
        for word in words:
            if random.random() < 0.1:  # 10% chance to add extra space
                result.append(word + ' ')
            else:
                result.append(word)
        return ' '.join(result)
        
    def wait_and_find_element(self, driver, wait, by, value, timeout=15):
        """Helper method to wait for and find an element"""
        try:
            element = wait.until(EC.presence_of_element_located((by, value)))
            wait.until(EC.element_to_be_clickable((by, value)))
            return element
        except TimeoutException:
            print(f"Timeout waiting for element: {value}")
            return None
        
    def scroll_to_element(self, driver, element):
        """Scroll element into view with human-like behavior"""
        # Get the element's location
        location = element.location_once_scrolled_into_view
        
        # Add some random offset
        offset = random.randint(-100, 100)
        
        # Scroll in smaller steps
        current_scroll = driver.execute_script("return window.pageYOffset;")
        target_scroll = location['y'] + offset
        steps = random.randint(5, 10)
        
        for i in range(steps):
            scroll_to = current_scroll + (target_scroll - current_scroll) * (i + 1) / steps
            driver.execute_script(f"window.scrollTo(0, {scroll_to});")
            time.sleep(random.uniform(0.1, 0.3))
        
    def handle_captcha(self, driver):
        """Handle CAPTCHA page"""
        print("\n" + "="*50)
        print("Google Scholar 需要验证")
        print("请在浏览器窗口中：")
        print('1. 点击"我不是机器人"复选框')
        print('2. 如果出现图片验证，请完成验证')
        print('3. 验证完成后，脚本将自动继续')
        print("\n您有 5 分钟时间完成验证")
        print("完成验证后无需其他操作，脚本会自动继续")
        print("="*50 + "\n")
        
        # Wait for manual intervention
        max_wait = 300  # 5 minutes
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            try:
                # Check if we're still on the CAPTCHA page
                if "sorry" not in driver.page_source.lower():
                    print("\n验证成功！继续处理...")
                    self.random_sleep(2, 3)  # Wait a bit after CAPTCHA
                    return True
                
                # Check for specific error messages
                if '请证明您不是机器人' in driver.page_source:
                    print('请点击"我不是机器人"复选框...')
                elif '请选择所有匹配的图片' in driver.page_source:
                    print('请完成图片验证...')
                
                time.sleep(1)
            except Exception as e:
                print(f"检查验证状态时出错: {str(e)}")
                time.sleep(1)
            
        print("\n验证超时。请重新运行脚本。")
        return False
        
    def find_and_click_cite_button(self, driver, wait, result_container):
        """Find and click the cite button in Google Scholar"""
        try:
            # Find the cite button within the result container
            cite_link = result_container.find_element(By.CLASS_NAME, "gs_or_cit")
            self.scroll_to_element(driver, cite_link)
            
            # Simulate human-like clicking
            action = ActionChains(driver)
            action.move_to_element(cite_link)
            action.pause(random.uniform(0.1, 0.3))
            action.click()
            action.perform()
            return True
        except Exception as e:
            print(f"Could not find cite button: {str(e)}")
            return False

    def find_and_click_endnote(self, driver, wait):
        """Find and click the EndNote link in Google Scholar citation window"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # Wait for citation popup with shorter timeout
                wait.until(EC.presence_of_element_located((By.ID, "gs_cit-pop")))
                
                # Try multiple selectors for EndNote link with shorter timeouts
                endnote_selectors = [
                    (By.XPATH, "//a[contains(@href, 'citation?format=enw')]"),
                    (By.XPATH, "//a[contains(text(), 'EndNote')]"),
                    (By.CSS_SELECTOR, "a[href*='citation?format=enw']")
                ]
                
                endnote_link = None
                for selector in endnote_selectors:
                    try:
                        # Use shorter timeout for each attempt
                        short_wait = WebDriverWait(driver, 5)
                        endnote_link = short_wait.until(EC.element_to_be_clickable(selector))
                        if endnote_link:
                            break
                    except:
                        continue
                
                if endnote_link:
                    # Try JavaScript click if normal click fails
                    try:
                        # First try normal click
                        action = ActionChains(driver)
                        action.move_to_element(endnote_link)
                        action.pause(0.1)  # Reduced pause time
                        action.click()
                        action.perform()
                    except:
                        # Fallback to JavaScript click
                        driver.execute_script("arguments[0].click();", endnote_link)
                    
                    return True
                    
            except Exception as e:
                print(f"尝试点击 EndNote 链接失败 (尝试 {retry_count + 1}/{max_retries}): {str(e)}")
                retry_count += 1
                if retry_count < max_retries:
                    time.sleep(1)  # Short delay between retries
                continue
                
        print("无法点击 EndNote 链接")
        return False
        
    def similarity_ratio(self, str1, str2):
        """Calculate similarity ratio between two strings"""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
        
    def perform_search(self, driver, search_box):
        """Perform search with human-like behavior"""
        try:
            # Sometimes move mouse away first
            if random.random() < 0.3:
                body = driver.find_element(By.TAG_NAME, "body")
                action = ActionChains(driver)
                action.move_to_element(body)
                action.perform()
                self.random_sleep(0.5, 1)
            
            # Try to find the search button
            try:
                search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                visible = search_button.is_displayed()
            except:
                visible = False
            
            # Decide how to perform the search
            if visible and random.random() < 0.3:  # 30% chance to click button if visible
                action = ActionChains(driver)
                action.move_to_element(search_button)
                action.pause(random.uniform(0.1, 0.3))
                action.click()
                action.perform()
            else:  # Otherwise press Enter
                search_box.send_keys(Keys.RETURN)
            
            return True
        except Exception as e:
            print(f"Error performing search: {str(e)}")
            # Fallback to Enter key
            search_box.send_keys(Keys.RETURN)
            return True

    def clean_search_query(self, title):
        """Clean the search query to handle special characters"""
        # First, handle special cases like "GPT-3" to keep them intact
        special_terms = ["GPT-3", "BERT", "T5", "XL-Net"]  # Add more as needed
        preserved_terms = {}
        for i, term in enumerate(special_terms):
            if term in title:
                placeholder = f"__TERM{i}__"
                preserved_terms[placeholder] = term
                title = title.replace(term, placeholder)
        
        # Remove or replace problematic characters
        cleaned = title
        for char in [':', '(', ')', '[', ']', '{', '}', '/', '\\']:
            cleaned = cleaned.replace(char, ' ')
        
        # Restore preserved terms
        for placeholder, term in preserved_terms.items():
            cleaned = cleaned.replace(placeholder, term)
        
        # Handle hyphens that are not part of preserved terms
        cleaned = ' '.join(word if word in preserved_terms.values() else word.replace('-', ' ')
                         for word in cleaned.split())
        
        # Remove multiple spaces and trim
        cleaned = ' '.join(cleaned.split())
        
        # Add quotes for exact match
        return f'"{cleaned}"'
        
    def wait_for_download(self, timeout=30):
        """Wait for the download to complete and return the path of the downloaded file"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            # Look for .enw files in the download directory
            files = glob.glob(os.path.join(self.download_dir, "*.enw"))
            if files:
                # Get the most recently modified file
                latest_file = max(files, key=os.path.getmtime)
                # Wait a bit to ensure the file is completely downloaded
                time.sleep(1)
                return latest_file
            time.sleep(0.5)
        return None

    def sanitize_filename(self, filename):
        """Remove invalid characters from filename"""
        # Replace invalid characters with underscore
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        # Remove leading/trailing spaces and dots
        filename = filename.strip('. ')
        # Limit length
        if len(filename) > 200:
            filename = filename[:197] + '...'
        return filename

    def get_endnote_title(self, file_path):
        """从 EndNote 文件中提取论文标题"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # EndNote 文件中标题通常以 %T 开头
                for line in content.split('\n'):
                    if line.startswith('%T'):
                        return line[2:].strip()
            return None
        except Exception as e:
            print(f"读取 EndNote 文件时出错: {str(e)}")
            return None

    def rename_downloaded_file(self, old_path, search_title):
        """使用 EndNote 文件中的实际标题重命名文件"""
        if not old_path or not os.path.exists(old_path):
            return None

        try:
            # 从 EndNote 文件中获取实际标题
            actual_title = self.get_endnote_title(old_path)
            if not actual_title:
                print(f"警告：无法从 EndNote 文件中提取标题，使用搜索标题: {search_title}")
                actual_title = search_title

            # 创建安全的文件名
            safe_title = self.sanitize_filename(actual_title)
            new_filename = f"{safe_title}.enw"
            new_path = os.path.join(self.download_dir, new_filename)

            # 如果文件已存在，添加数字后缀
            counter = 1
            base_path = new_path
            while os.path.exists(new_path):
                name, ext = os.path.splitext(base_path)
                new_path = f"{name}_{counter}{ext}"
                counter += 1

            # 重命名文件
            shutil.move(old_path, new_path)
            print(f"EndNote 文件中的标题: {actual_title}")
            return new_path
        except Exception as e:
            print(f"重命名文件时出错: {str(e)}")
            return old_path

    def download_citations(self, titles_file):
        """Download EndNote citations for papers listed in the titles file"""
        # Read paper titles
        with open(titles_file, 'r', encoding='utf-8') as f:
            titles = [line.strip() for line in f if line.strip()]
        
        driver = None
        try:
            # Initialize WebDriver with retry mechanism
            print("\n初始化浏览器...")
            driver = self._initialize_driver()
            wait = WebDriverWait(driver, 15)
            
            for i, title in enumerate(titles, 1):
                retry_count = 0
                while retry_count < self.max_retries:
                    try:
                        print(f"\n处理第 {i}/{len(titles)} 篇论文: {title}")
                        
                        # Navigate to Google Scholar with random delay
                        print("访问 Google Scholar...")
                        driver.get("https://scholar.google.com/")
                        self.random_sleep(1, 2)  # 减少等待时间
                        
                        # Check for and handle any captcha
                        if "sorry" in driver.page_source.lower() or "请证明您不是机器人" in driver.page_source:
                            if not self.handle_captcha(driver):
                                break
                        
                        # Find and fill the search box
                        print("搜索论文...")
                        search_box = self.wait_and_find_element(
                            driver, wait, By.NAME, "q"
                        )
                        if not search_box:
                            print("找不到搜索框")
                            continue
                        
                        # 清空搜索框并输入完整标题
                        search_box.clear()
                        # 直接使用标题作为搜索词，不添加引号
                        search_query = title
                        print(f"输入搜索词: {search_query}")
                        # 使用 JavaScript 直接设置值，确保完整标题被输入
                        driver.execute_script("arguments[0].value = arguments[1];", search_box, search_query)
                        self.random_sleep(0.5, 1)
                        
                        # 执行搜索
                        search_box.send_keys(Keys.RETURN)
                        
                        self.random_sleep(2, 3)  # 减少等待时间
                        
                        # Check for CAPTCHA again
                        if "sorry" in driver.page_source.lower() or "请证明您不是机器人" in driver.page_source:
                            if not self.handle_captcha(driver):
                                break
                        
                        # Print page source for debugging
                        print("\n调试信息：")
                        print("页面标题:", driver.title)
                        print("当前URL:", driver.current_url)
                        print("页面内容片段:", driver.page_source[:500])
                        
                        # Try different selectors for search results
                        results = []
                        selectors = [
                            (By.CLASS_NAME, "gs_ri"),  # 标准结果容器
                            (By.CSS_SELECTOR, "div.gs_r.gs_or.gs_scl"),  # 替代结果容器
                            (By.CSS_SELECTOR, "div[data-aid]"),  # 基于数据属性
                            (By.CSS_SELECTOR, "div.gs_or")  # 最简单的选择器
                        ]
                        
                        for selector in selectors:
                            try:
                                results = driver.find_elements(*selector)
                                if results:
                                    print(f"使用选择器 {selector[1]} 找到结果")
                                    break
                            except Exception as e:
                                print(f"选择器 {selector[1]} 失败: {str(e)}")
                                continue
                        
                        if not results:
                            print("未找到搜索结果")
                            continue
                        
                        print(f"找到 {len(results)} 个结果")
                        
                        # Find the best matching result
                        best_match = None
                        best_ratio = 0
                        for result in results:
                            try:
                                # Try different title selectors
                                title_selectors = [
                                    (By.CLASS_NAME, "gs_rt"),  # 标准标题
                                    (By.CSS_SELECTOR, "h3.gs_rt"),  # 带标签的标题
                                    (By.CSS_SELECTOR, "a.gsc_a_at"),  # 替代标题链接
                                    (By.TAG_NAME, "a")  # 任何链接
                                ]
                                
                                result_title = None
                                for title_selector in title_selectors:
                                    try:
                                        title_element = result.find_element(*title_selector)
                                        result_title = title_element.text
                                        if result_title:
                                            break
                                    except:
                                        continue
                                
                                if not result_title:
                                    continue
                                    
                                # Remove [PDF], [BOOK], etc. from title
                                result_title = ' '.join([part for part in result_title.split() if not (part.startswith('[') and part.endswith(']'))])
                                ratio = self.similarity_ratio(result_title, title)
                                print(f"比较: {result_title} (相似度: {ratio:.2f})")
                                if ratio > best_ratio:
                                    best_ratio = ratio
                                    best_match = result
                            except Exception as e:
                                print(f"处理搜索结果时出错: {str(e)}")
                                continue
                        
                        if not best_match:
                            print("未找到匹配的论文")
                            continue
                        
                        print(f"找到最佳匹配论文 (相似度: {best_ratio:.2f})")
                        
                        # Try to find cite button with different selectors
                        cite_button = None
                        cite_selectors = [
                            (By.CLASS_NAME, "gs_or_cit"),  # 标准引用按钮
                            (By.CSS_SELECTOR, "a.gs_or_cit"),  # 带标签的引用按钮
                            (By.XPATH, "//a[contains(@onclick, 'gs_ocit')]"),  # 基于onclick
                            (By.XPATH, "//a[contains(text(), 'Cite')]")  # 基于文本
                        ]
                        
                        print("查找引用按钮...")
                        for selector in cite_selectors:
                            try:
                                cite_button = best_match.find_element(*selector)
                                if cite_button:
                                    print(f"使用选择器 {selector[1]} 找到引用按钮")
                                    break
                            except:
                                continue
                        
                        if not cite_button:
                            print("未找到引用按钮")
                            continue
                        
                        # Click cite button
                        print("点击引用按钮...")
                        self.scroll_to_element(driver, cite_button)
                        action = ActionChains(driver)
                        action.move_to_element(cite_button)
                        action.pause(random.uniform(0.1, 0.3))
                        action.click()
                        action.perform()
                        
                        self.random_sleep(2, 4)
                        
                        # Try to find EndNote link with different selectors
                        endnote_link = None
                        endnote_selectors = [
                            (By.XPATH, "//a[contains(@href, 'citation?format=enw')]"),
                            (By.XPATH, "//a[contains(text(), 'EndNote')]"),
                            (By.CSS_SELECTOR, "a[href*='citation?format=enw']")
                        ]
                        
                        print("查找 EndNote 链接...")
                        for selector in endnote_selectors:
                            try:
                                endnote_link = wait.until(EC.element_to_be_clickable(selector))
                                if endnote_link:
                                    print(f"使用选择器 {selector[1]} 找到 EndNote 链接")
                                    break
                            except:
                                continue
                        
                        if not endnote_link:
                            print("未找到 EndNote 链接")
                            continue
                        
                        # Click EndNote link
                        print("下载 EndNote 格式引用...")
                        action = ActionChains(driver)
                        action.move_to_element(endnote_link)
                        action.pause(random.uniform(0.1, 0.3))
                        action.click()
                        action.perform()
                        
                        # Wait for download to complete and rename the file
                        print("等待下载完成...")
                        downloaded_file = self.wait_for_download()
                        if downloaded_file:
                            new_path = self.rename_downloaded_file(downloaded_file, title)
                            if new_path:
                                print(f"成功下载并重命名引用文件: {os.path.basename(new_path)}")
                            else:
                                print("下载成功但重命名失败")
                        else:
                            print("下载超时")
                            continue
                        
                        break  # 如果成功处理，跳出重试循环
                    except (socket.error, urllib3.exceptions.MaxRetryError,
                            urllib3.exceptions.NewConnectionError) as e:
                        retry_count += 1
                        logger.warning(f"处理论文时发生连接错误 (尝试 {retry_count}/{self.max_retries}): {str(e)}")
                        if retry_count < self.max_retries:
                            # 重新初始化 WebDriver
                            if driver:
                                try:
                                    driver.quit()
                                except:
                                    pass
                            time.sleep(2 ** retry_count)
                            driver = self._initialize_driver()
                            wait = WebDriverWait(driver, 15)
                            continue
                        else:
                            logger.error(f"处理论文失败，已达到最大重试次数: {title}")
                            break
                    except Exception as e:
                        logger.error(f"处理论文时发生未知错误: {str(e)}")
                        break
                
                # Add longer delay between papers
                if i < len(titles):
                    print(f"\n等待处理下一篇论文...")
                    self.random_sleep(5, 10)
                    
        finally:
            if driver:
                try:
                    print("\n关闭浏览器...")
                    driver.quit()
                except:
                    pass

def main():
    print("\nCiteScholarEasy - Google Scholar 引用下载工具")
    print("="*50)
    print("提示：")
    print("1. 程序会自动打开浏览器并访问 Google Scholar")
    print("2. 如果遇到验证码，会提示您手动完成验证")
    print("3. 验证完成后，程序会自动继续运行")
    print("4. 引用文件将保存在 downloads 目录中")
    print("="*50)
    
    try:
        downloader = CiteDownloader(headless=False)  # 使用有界面模式
        downloader.download_citations("title.txt")
    except KeyboardInterrupt:
        print("\n\n程序被用户中断。")
    except Exception as e:
        print(f"\n\n程序出错: {str(e)}")
    finally:
        print("\n程序结束。")

if __name__ == "__main__":
    main() 
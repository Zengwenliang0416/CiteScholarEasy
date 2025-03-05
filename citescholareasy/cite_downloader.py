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
    """
    Google Scholar 引用下载器类
    用于自动化下载论文的引用信息，支持 EndNote 格式
    
    主要功能：
    1. 自动访问 Google Scholar
    2. 搜索论文标题
    3. 下载引用信息
    4. 处理验证码
    5. 智能重试机制
    """
    
    def __init__(self, download_dir="downloads", headless=True, max_retries=3):
        """
        初始化下载器
        
        参数：
        download_dir (str): 下载文件保存目录
        headless (bool): 是否使用无头模式（不显示浏览器界面）
        max_retries (int): 最大重试次数
        """
        self.download_dir = os.path.abspath(download_dir)
        self.max_retries = max_retries
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
        
        # 初始化 Chrome 选项
        self.options = self._initialize_chrome_options(headless)
        
    def _initialize_chrome_options(self, headless):
        """
        初始化 Chrome 浏览器选项
        
        参数：
        headless (bool): 是否使用无头模式
        
        返回：
        ChromeOptions: 配置好的浏览器选项
        """
        options = uc.ChromeOptions()
        
        # 设置下载和安全相关首选项
        prefs = {
            "download.default_directory": self.download_dir,  # 设置下载目录
            "download.prompt_for_download": False,  # 禁用下载提示
            "download.directory_upgrade": True,  # 允许升级下载目录
            "safebrowsing.enabled": True,  # 启用安全浏览
            "profile.default_content_settings.popups": 0,  # 禁用弹窗
            "credentials_enable_service": False,  # 禁用凭据服务
            "profile.password_manager_enabled": False  # 禁用密码管理器
        }
        options.add_experimental_option("prefs", prefs)
        
        # 配置浏览器选项
        if headless:
            options.add_argument('--headless=new')  # 启用新版无头模式
        
        # 添加其他参数以提高稳定性和隐私性
        options.add_argument('--no-sandbox')  # 禁用沙箱
        options.add_argument('--disable-dev-shm-usage')  # 禁用共享内存
        options.add_argument('--disable-gpu')  # 禁用 GPU 加速
        options.add_argument('--start-maximized')  # 最大化窗口
        options.add_argument('--disable-notifications')  # 禁用通知
        options.add_argument('--disable-popup-blocking')  # 禁用弹窗拦截
        options.add_argument('--disable-automation')  # 禁用自动化标志
        options.add_argument('--disable-blink-features=AutomationControlled')  # 禁用自动化控制特征
        
        # 随机选择一个用户代理
        user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        ]
        options.add_argument(f'--user-agent={random.choice(user_agents)}')
        
        return options

    def _initialize_driver(self):
        """
        初始化 WebDriver，包含重试机制
        
        返回：
        WebDriver: 配置好的 Chrome WebDriver 实例
        
        异常：
        Exception: 初始化失败时抛出异常
        """
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                # 使用 selenium 原生的 Chrome WebDriver
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=self.options)
                
                # 测试连接
                driver.get("about:blank")
                return driver
            except (socket.error, urllib3.exceptions.MaxRetryError,
                    urllib3.exceptions.NewConnectionError) as e:
                retry_count += 1
                logger.warning(f"WebDriver 初始化失败 (尝试 {retry_count}/{self.max_retries}): {str(e)}")
                if retry_count < self.max_retries:
                    time.sleep(2 ** retry_count)  # 指数退避策略
                    continue
                else:
                    raise Exception("WebDriver 初始化失败，已达到最大重试次数")
            except Exception as e:
                logger.error(f"WebDriver 初始化时发生未知错误: {str(e)}")
                raise

    def random_sleep(self, min_time=0.1, max_time=0.2):
        """
        随机等待一段时间，模拟人类操作间隔
        
        参数：
        min_time (float): 最小等待时间（秒）
        max_time (float): 最大等待时间（秒）
        """
        time.sleep(random.uniform(min_time, max_time))
        
    def simulate_human_typing(self, element, text):
        """
        模拟人类输入文字的行为
        
        参数：
        element (WebElement): 要输入文字的网页元素
        text (str): 要输入的文字
        
        特点：
        1. 随机的输入速度
        2. 偶尔会输入错误并修正
        3. 在标点符号后停顿较长时间
        """
        for char in text:
            if random.random() < 0.05:  # 5% 的概率输入错误
                typo = random.choice('qwertyuiopasdfghjklzxcvbnm')
                element.send_keys(typo)
                time.sleep(random.uniform(0.1, 0.3))
                element.send_keys(Keys.BACKSPACE)
                time.sleep(random.uniform(0.1, 0.3))
            element.send_keys(char)
            if char in [' ', '.', ',']:
                time.sleep(random.uniform(0.3, 0.7))  # 标点后停顿较长
            else:
                time.sleep(random.uniform(0.1, 0.4))  # 正常输入速度
            
    def add_random_noise(self, text):
        """
        向文本中添加随机的空格和换行，避免被检测为机器人
        
        参数：
        text (str): 原始文本
        
        返回：
        str: 添加了随机噪声的文本
        """
        words = text.split()
        result = []
        for word in words:
            if random.random() < 0.1:  # 10% 的概率添加额外空格
                result.append(word + ' ')
            else:
                result.append(word)
        return ' '.join(result)
        
    def wait_and_find_element(self, driver, wait, by, value, timeout=15):
        """
        等待并查找网页元素，包含错误处理
        
        参数：
        driver (WebDriver): 浏览器驱动
        wait (WebDriverWait): 等待对象
        by (By): 查找方式（如 By.ID, By.CLASS_NAME 等）
        value (str): 要查找的值
        timeout (int): 超时时间（秒）
        
        返回：
        WebElement/None: 找到的元素或 None（如果未找到）
        """
        try:
            element = wait.until(EC.presence_of_element_located((by, value)))
            wait.until(EC.element_to_be_clickable((by, value)))
            return element
        except TimeoutException:
            print(f"等待元素超时: {value}")
            return None
        
    def scroll_to_element(self, driver, element):
        """
        以人类般自然的方式滚动到指定元素
        
        参数：
        driver (WebDriver): 浏览器驱动
        element (WebElement): 目标元素
        
        特点：
        1. 分步滚动
        2. 随机的滚动偏移
        3. 每步之间有短暂停顿
        """
        location = element.location_once_scrolled_into_view
        offset = random.randint(-100, 100)
        current_scroll = driver.execute_script("return window.pageYOffset;")
        target_scroll = location['y'] + offset
        steps = random.randint(5, 10)
        
        for i in range(steps):
            scroll_to = current_scroll + (target_scroll - current_scroll) * (i + 1) / steps
            driver.execute_script(f"window.scrollTo(0, {scroll_to});")
            time.sleep(random.uniform(0.1, 0.3))
        
    def handle_captcha(self, driver):
        """
        处理 Google Scholar 的验证码页面
        
        参数：
        driver (WebDriver): 浏览器驱动
        
        返回：
        bool: 验证是否成功
        
        工作流程：
        1. 提示用户需要验证
        2. 等待用户完成验证
        3. 检查验证结果
        4. 超时处理
        """
        print("\n" + "="*50)
        print("Google Scholar 需要验证")
        print("请在浏览器窗口中：")
        print('1. 点击"我不是机器人"复选框')
        print('2. 如果出现图片验证，请完成验证')
        print('3. 验证完成后，脚本将自动继续')
        print("\n您有 5 分钟时间完成验证")
        print("完成验证后无需其他操作，脚本会自动继续")
        print("="*50 + "\n")
        
        max_wait = 300  # 5 分钟超时
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            try:
                if "sorry" not in driver.page_source.lower():
                    print("\n验证成功！继续处理...")
                    self.random_sleep(2, 3)
                    return True
                
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
        """
        在 Google Scholar 搜索结果中查找并点击引用按钮
        
        参数：
        driver (WebDriver): 浏览器驱动
        wait (WebDriverWait): 等待对象
        result_container (WebElement): 包含搜索结果的容器元素
        
        返回：
        bool: 是否成功点击引用按钮
        """
        try:
            cite_link = result_container.find_element(By.CLASS_NAME, "gs_or_cit")
            self.scroll_to_element(driver, cite_link)
            
            action = ActionChains(driver)
            action.move_to_element(cite_link)
            action.pause(random.uniform(0.1, 0.3))
            action.click()
            action.perform()
            return True
        except Exception as e:
            print(f"无法找到引用按钮: {str(e)}")
            return False

    def find_and_click_endnote(self, driver, wait):
        """
        在 Google Scholar 引用窗口中查找并点击 EndNote 链接
        
        参数：
        driver (WebDriver): 浏览器驱动
        wait (WebDriverWait): 等待对象
        
        返回：
        bool: 是否成功点击 EndNote 链接
        
        特点：
        1. 多种选择器尝试
        2. 短超时重试机制
        3. 备用点击方法
        """
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # 等待引用弹窗出现
                wait.until(EC.presence_of_element_located((By.ID, "gs_cit-pop")))
                
                # 尝试多个选择器
                endnote_selectors = [
                    (By.XPATH, "//a[contains(@href, 'citation?format=enw')]"),
                    (By.XPATH, "//a[contains(text(), 'EndNote')]"),
                    (By.CSS_SELECTOR, "a[href*='citation?format=enw']")
                ]
                
                endnote_link = None
                for selector in endnote_selectors:
                    try:
                        short_wait = WebDriverWait(driver, 5)
                        endnote_link = short_wait.until(EC.element_to_be_clickable(selector))
                        if endnote_link:
                            break
                    except:
                        continue
                
                if endnote_link:
                    try:
                        # 尝试常规点击
                        action = ActionChains(driver)
                        action.move_to_element(endnote_link)
                        action.pause(0.1)
                        action.click()
                        action.perform()
                    except:
                        # 使用 JavaScript 点击作为备选方案
                        driver.execute_script("arguments[0].click();", endnote_link)
                    
                    return True
                    
            except Exception as e:
                print(f"尝试点击 EndNote 链接失败 (尝试 {retry_count + 1}/{max_retries}): {str(e)}")
                retry_count += 1
                if retry_count < max_retries:
                    time.sleep(1)
                continue
                
        print("无法点击 EndNote 链接")
        return False
        
    def similarity_ratio(self, str1, str2):
        """
        计算两个字符串的相似度
        
        参数：
        str1 (str): 第一个字符串
        str2 (str): 第二个字符串
        
        返回：
        float: 相似度比率（0-1之间的浮点数）
        """
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
        
    def perform_search(self, driver, search_box):
        """
        执行搜索操作，模拟人类行为
        
        参数：
        driver (WebDriver): 浏览器驱动
        search_box (WebElement): 搜索输入框元素
        
        返回：
        bool: 搜索是否成功执行
        
        特点：
        1. 随机选择点击搜索按钮或按回车键
        2. 模拟鼠标移动
        3. 包含随机延迟
        """
        try:
            # 随机决定是否先将鼠标移开
            if random.random() < 0.3:
                body = driver.find_element(By.TAG_NAME, "body")
                action = ActionChains(driver)
                action.move_to_element(body)
                action.perform()
                self.random_sleep(0.5, 1)
            
            # 尝试找到搜索按钮
            try:
                search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                visible = search_button.is_displayed()
            except:
                visible = False
            
            # 随机选择搜索方式
            if visible and random.random() < 0.3:  # 30% 的概率点击按钮
                action = ActionChains(driver)
                action.move_to_element(search_button)
                action.pause(random.uniform(0.1, 0.3))
                action.click()
                action.perform()
            else:  # 否则按回车键
                search_box.send_keys(Keys.RETURN)
            
            return True
        except Exception as e:
            print(f"执行搜索时出错: {str(e)}")
            # 使用回车键作为备选方案
            search_box.send_keys(Keys.RETURN)
            return True

    def clean_search_query(self, title):
        """
        清理搜索查询，处理特殊字符
        
        参数：
        title (str): 原始论文标题
        
        返回：
        str: 处理后的搜索查询
        
        特点：
        1. 保留特殊术语（如 GPT-3, BERT 等）
        2. 移除或替换特殊字符
        3. 处理连字符
        4. 添加引号实现精确匹配
        """
        # 保护特殊术语
        special_terms = ["GPT-3", "BERT", "T5", "XL-Net"]
        preserved_terms = {}
        for i, term in enumerate(special_terms):
            if term in title:
                placeholder = f"__TERM{i}__"
                preserved_terms[placeholder] = term
                title = title.replace(term, placeholder)
        
        # 处理特殊字符
        cleaned = title
        for char in [':', '(', ')', '[', ']', '{', '}', '/', '\\']:
            cleaned = cleaned.replace(char, ' ')
        
        # 恢复特殊术语
        for placeholder, term in preserved_terms.items():
            cleaned = cleaned.replace(placeholder, term)
        
        # 处理连字符
        cleaned = ' '.join(word if word in preserved_terms.values() else word.replace('-', ' ')
                         for word in cleaned.split())
        
        # 移除多余空格并修剪
        cleaned = ' '.join(cleaned.split())
        
        # 添加引号实现精确匹配
        return f'"{cleaned}"'
        
    def wait_for_download(self, timeout=30):
        """
        等待下载完成并返回下载文件的路径
        
        参数：
        timeout (int): 超时时间（秒）
        
        返回：
        str/None: 下载文件的路径，如果超时则返回 None
        
        工作流程：
        1. 监控下载目录
        2. 检查新的 .enw 文件
        3. 返回最新下载的文件路径
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            # 查找 .enw 文件
            files = glob.glob(os.path.join(self.download_dir, "*.enw"))
            if files:
                # 获取最新修改的文件
                latest_file = max(files, key=os.path.getmtime)
                # 等待文件完全下载
                time.sleep(1)
                return latest_file
            time.sleep(0.5)
        return None

    def sanitize_filename(self, filename):
        """
        清理文件名，移除非法字符
        
        参数：
        filename (str): 原始文件名
        
        返回：
        str: 处理后的合法文件名
        
        处理内容：
        1. 替换非法字符
        2. 移除首尾空格和点号
        3. 限制文件名长度
        """
        # 替换非法字符
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        # 移除首尾空格和点号
        filename = filename.strip('. ')
        # 限制长度
        if len(filename) > 200:
            filename = filename[:197] + '...'
        return filename

    def get_endnote_title(self, file_path):
        """
        从 EndNote 文件中提取论文标题
        
        参数：
        file_path (str): EndNote 文件路径
        
        返回：
        str/None: 论文标题，如果提取失败则返回 None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 查找以 %T 开头的行
                for line in content.split('\n'):
                    if line.startswith('%T'):
                        return line[2:].strip()
            return None
        except Exception as e:
            print(f"读取 EndNote 文件时出错: {str(e)}")
            return None

    def rename_downloaded_file(self, old_path, search_title):
        """
        使用 EndNote 文件中的实际标题重命名下载的文件
        
        参数：
        old_path (str): 原文件路径
        search_title (str): 搜索时使用的标题
        
        返回：
        str/None: 新文件路径，如果重命名失败则返回原路径
        
        工作流程：
        1. 从 EndNote 文件中提取标题
        2. 生成安全的文件名
        3. 处理文件名冲突
        4. 执行重命名
        """
        if not old_path or not os.path.exists(old_path):
            return None

        try:
            # 获取实际标题
            actual_title = self.get_endnote_title(old_path)
            if not actual_title:
                print(f"警告：无法从 EndNote 文件中提取标题，使用搜索标题: {search_title}")
                actual_title = search_title

            # 生成安全的文件名
            safe_title = self.sanitize_filename(actual_title)
            new_filename = f"{safe_title}.enw"
            new_path = os.path.join(self.download_dir, new_filename)

            # 处理文件名冲突
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
        """
        下载论文引用信息的主方法
        
        参数：
        titles_file (str): 包含论文标题的文件路径
        
        工作流程：
        1. 读取论文标题列表
        2. 初始化浏览器
        3. 对每个标题：
           - 访问 Google Scholar
           - 搜索论文
           - 处理验证码（如果出现）
           - 查找最佳匹配结果
           - 下载引用
           - 重命名文件
        4. 处理异常情况
        """
        # 读取论文标题
        with open(titles_file, 'r', encoding='utf-8') as f:
            titles = [line.strip() for line in f if line.strip()]
        
        driver = None
        try:
            # 初始化 WebDriver
            print("\n初始化浏览器...")
            driver = self._initialize_driver()
            wait = WebDriverWait(driver, 2)
            
            # 处理每篇论文
            for i, title in enumerate(titles, 1):
                retry_count = 0
                while retry_count < self.max_retries:
                    try:
                        print(f"\n处理第 {i}/{len(titles)} 篇论文: {title}")
                        
                        # 访问 Google Scholar
                        print("访问 Google Scholar...")
                        driver.get("https://scholar.google.com/")
                        self.random_sleep(1, 2)
                        
                        # 处理验证码
                        if "sorry" in driver.page_source.lower() or "请证明您不是机器人" in driver.page_source:
                            if not self.handle_captcha(driver):
                                break
                                
                        # 搜索论文
                        print("搜索论文...")
                        search_box = self.wait_and_find_element(
                            driver, wait, By.NAME, "q"
                        )
                        if not search_box:
                            print("找不到搜索框")
                            continue
                        
                        # 输入搜索词
                        search_box.clear()
                        search_query = title
                        print(f"输入搜索词: {search_query}")
                        driver.execute_script("arguments[0].value = arguments[1];", search_box, search_query)
                        self.random_sleep(0.5, 1)
                        
                        # 执行搜索
                        search_box.send_keys(Keys.RETURN)
                        self.random_sleep(2, 3)
                        
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
                        try:
                            # 直接使用 JavaScript 点击，更快速可靠
                            driver.execute_script("arguments[0].click();", cite_button)
                        except:
                            # 如果 JavaScript 点击失败，回退到常规点击
                            action = ActionChains(driver)
                            action.move_to_element(cite_button)
                            action.click()
                            action.perform()
                        
                        # 减少等待时间
                        self.random_sleep(0.3, 0.5)
                        
                        # 使用更高效的选择器直接查找 EndNote 链接
                        print("查找 EndNote 链接...")
                        try:
                            # 首选：直接通过 href 属性查找
                            endnote_link = wait.until(
                                EC.element_to_be_clickable(
                                    (By.CSS_SELECTOR, "a[href*='citation?format=enw']")
                                )
                            )
                        except:
                            try:
                                # 备选：通过文本内容查找
                                endnote_link = wait.until(
                                    EC.element_to_be_clickable(
                                        (By.XPATH, "//a[contains(text(), 'EndNote')]")
                                    )
                                )
                            except:
                                print("未找到 EndNote 链接")
                                continue
                        
                        # 直接使用 JavaScript 点击 EndNote 链接
                        print("下载 EndNote 格式引用...")
                        try:
                            driver.execute_script("arguments[0].click();", endnote_link)
                        except:
                            action = ActionChains(driver)
                            action.move_to_element(endnote_link)
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
    """
    主函数，程序入口点
    
    功能：
    1. 显示程序信息和使用说明
    2. 初始化下载器
    3. 执行下载任务
    4. 处理异常情况
    """
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
# CiteScholarEasy

一个帮助学术工作者高效管理文献引用的工具。本工具可以自动从 Google Scholar 批量下载论文的引用信息，支持 EndNote 格式，让文献管理变得简单高效。

## 主要功能

- **自动化引用下载**：批量从 Google Scholar 下载论文引用信息
- **智能引用管理**：自动整理和命名下载的引用文件
- **多格式支持**：支持 EndNote (ENW) 格式，可用于各种文献管理软件
- **中英文支持**：完全支持中英文论文标题
- **自动重试机制**：网络问题自动重试，验证码智能提醒
- **人性化交互**：清晰的进度显示和错误提示

## 系统要求

- **Python 环境**：
  - Python 3.8 或更高版本
  - pip 包管理器
  - 建议使用虚拟环境

- **浏览器要求**：
  - Google Chrome 浏览器（最新版本）
  - Chrome WebDriver（程序会自动安装）

- **网络环境**：
  - 能够访问 Google Scholar
  - 稳定的网络连接
  - 建议使用代理（如果所在地区无法直接访问 Google）

- **操作系统**：
  - Windows 10/11
  - macOS 10.15+
  - Linux（主流发行版）

## 详细安装步骤

1. **获取代码**：
```bash
# 克隆仓库
git clone https://github.com/yourusername/CiteScholarEasy.git

# 进入项目目录
cd CiteScholarEasy
```

2. **配置 Python 环境**：

Windows 系统：
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 如果激活时报错，请先执行
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

macOS/Linux 系统：
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate
```

3. **安装依赖**：
```bash
# 更新 pip
python -m pip install --upgrade pip

# 安装依赖包
pip install -r requirements.txt
```

4. **验证安装**：
```bash
# 检查 Python 版本
python --version  # 应显示 3.8 或更高版本

# 检查依赖安装
pip list  # 应该看到 selenium、requests 等包
```

## 使用指南

### 基本使用

1. **准备论文列表**：

创建 `title.txt` 文件，每行一个论文标题：
```
# 支持中英文标题
Attention Is All You Need
BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
基于深度学习的中文命名实体识别研究
人工智能在自然语言处理中的应用综述
```

2. **启动程序**：
```bash
# 确保在项目根目录下
python citescholareasy/cite_downloader.py
```

3. **运行过程**：
   - 程序启动后会显示进度信息
   - 每篇论文处理后会显示下载状态
   - 如果遇到验证码会暂停并提示
   - 完成后会显示总结信息

### 高级使用

1. **自定义下载目录**：
```python
# 修改 cite_downloader.py 中的配置
downloader = CiteDownloader(download_dir="your_path")
```

2. **调整下载参数**：
```python
# 修改重试次数和等待时间
downloader = CiteDownloader(
    max_retries=5,  # 增加重试次数
    headless=True   # 使用无头模式
)
```

3. **批量处理策略**：
   - 建议将大量论文分批处理，每批 30-50 篇
   - 每批次之间建议间隔 30 分钟
   - 可以创建多个 title.txt 文件分批处理

### 使用场景示例

1. **撰写学术论文**：
   - 准备参考文献列表
   - 批量下载引用信息
   - 导入到 EndNote 等文献管理软件

2. **文献综述整理**：
   - 收集领域内重要文献
   - 批量获取引用信息
   - 统一管理和格式化

3. **学位论文写作**：
   - 分章节整理参考文献
   - 批量下载和管理
   - 统一引用格式

## 常见问题解决

### 1. 安装问题

- **pip 安装失败**：
  ```bash
  # 尝试使用国内镜像
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```

- **Chrome 驱动问题**：
  ```bash
  # 手动下载对应版本的 ChromeDriver
  # 将路径添加到环境变量
  ```

### 2. 运行问题

- **程序启动失败**：
  - 检查 Python 版本
  - 确认虚拟环境已激活
  - 验证所有依赖已安装

- **浏览器无法启动**：
  - 确认 Chrome 已安装
  - 检查 ChromeDriver 版本匹配
  - 尝试更新 Chrome 到最新版本

- **Chrome 版本兼容性问题**：
  ```bash
  # 如果遇到 ChromeDriver 版本与 Chrome 不匹配的错误
  # 1. 删除旧的 ChromeDriver 文件
  rm -rf ~/Library/Application\ Support/undetected_chromedriver/
  
  # 2. 让程序重新下载匹配的 ChromeDriver
  # 程序会自动下载与当前 Chrome 版本匹配的 ChromeDriver
  ```

### 3. 下载问题

- **验证码处理**：
  - 手动完成验证
  - 等待几分钟后再试
  - 考虑使用代理服务

- **下载超时**：
  - 检查网络连接
  - 增加超时时间
  - 减少批量下载数量

### 4. 文件问题

- **中文乱码**：
  ```bash
  # Windows 用户使用记事本打开 title.txt
  # 另存为时选择 UTF-8 编码
  ```

- **文件命名冲突**：
  - 程序会自动添加序号
  - 可以预先清理 downloads 目录
  - 检查标题是否重复

## 更多资源

- [EndNote 格式详细说明](docs/enw_guide.md)
- [引用样式指南](docs/ens_guide.md)
- [Google Scholar 使用技巧](https://scholar.google.com/intl/en/scholar/help.html)

## 项目贡献

欢迎贡献代码和提出建议！

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 发起 Pull Request

重大更改请先开 issue 讨论。

## 开源协议

[MIT](https://choosealicense.com/licenses/mit/) - 可以自由使用、修改和分发 
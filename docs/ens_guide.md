## EndNote Style (ENS) 文件格式指南

### 1. ENS 文件是什么？
ENS 文件是 EndNote 的样式文件（EndNote Style），用于定义参考文献的输出格式。它控制了引用在文中的显示方式和参考文献列表的格式。

### 2. 如何获取 ENS 文件
1. EndNote 软件自带样式库
2. 期刊官网下载
3. EndNote 官方样式库：[EndNote Style Download](https://endnote.com/style_download/)
4. 学术机构网站

### 3. 常用中文期刊样式
- **GB/T 7714-2015** - 中文文献著录标准
- **CSCD** - 中国科学引文数据库样式
- **中国社会科学引文索引** (CSSCI) 样式
- **《中国农业科学》** 期刊样式
- **《中国图书馆学报》** 期刊样式

### 4. 如何安装 ENS 文件
1. EndNote 软件中安装：
   - 打开 EndNote
   - 选择 `Edit > Output Styles > Open Style Manager`
   - 点击 `Install` 或将 ENS 文件拖入窗口

2. 手动安装：
   - Windows: 复制到 `C:\\Program Files\\EndNote\\Styles`
   - Mac: 复制到 `Applications/EndNote/Styles`

### 5. 如何修改 ENS 文件
1. EndNote 中修改：
   - 打开 EndNote
   - 选择 `Edit > Output Styles > Edit [样式名称]`
   - 修改各项设置
   - 保存为新样式文件

2. 主要修改项：
   - Templates（模板）
   - Author Lists（作者列表）
   - Author Name（作者姓名格式）
   - Citations（引用格式）
   - Bibliography（参考文献格式）
   - Footnotes（脚注格式）
   - Figures & Tables（图表格式）

### 6. 常见设置说明

#### 1. 作者姓名格式设置
1. 进入 `Author Name` 设置：
   - 选择 `Edit > Output Styles > Edit [当前样式]`
   - 左侧面板选择 `Author Name`
2. 调整选项：
   - `Name Format`: 姓名显示格式（Jane Smith 或 Smith, Jane）
   - `Initials`: 名字缩写格式（J.S. 或 JS）
   - `Capitalization`: 大小写（SMITH 或 Smith）
3. 中文作者设置：
   - 勾选 `Use Asian rules for names with no spaces between characters`

#### 2. 作者列表设置
1. 进入 `Author Lists` 设置：
   - 左侧面板选择 `Author Lists`
2. 调整选项：
   - `Number of Authors`: 显示作者数量
   - `Show only first ___ authors`: 限制显示作者数
   - `Use ... for more than ___ authors`: 超过特定数量使用省略符
   - `Separator between authors`: 作者间隔符（通常是 ", "）
   - `Before last author`: 最后作者前的连接词（"and" 或 "&"）

#### 3. 期刊名称格式
1. 进入 `Journal Names` 设置：
   - 左侧面板选择 `Journal Names`
2. 选择显示方式：
   - `Full Journal Name`: 完整期刊名
   - `ISO Abbreviation`: ISO 标准缩写
   - `Use full journal name`: 使用完整名称
   - `Use abbreviation`: 使用缩写
3. 期刊名称斜体：
   - 在 `Bibliography > Templates` 中给期刊名添加斜体标记

#### 4. 引用格式设置
1. 进入 `Citations` 设置：
   - 左侧面板选择 `Citations > Templates`
2. 调整选项：
   - `Multiple citation separator`: 多引用间隔符
   - `Year format`: 年份格式
   - `Citation order`: 引用排序方式
3. 常见格式：
   - 作者年份格式：(Smith, 2020)
   - 数字格式：[1]
   - 上标格式：<sup>1</sup>

#### 5. 参考文献排序
1. 进入 `Bibliography > Sort Order` 设置：
2. 选择排序方式：
   - `Order of appearance`: 按引用顺序
   - `Author + Title`: 按作者和标题
   - `Author + Year + Title`: 按作者年份标题
3. 设置多级排序：
   - 可添加多个排序规则
   - 设置升序或降序

#### 6. 标题格式设置
1. 进入 `Bibliography > Templates`：
2. 调整选项：
   - 标题大小写：句首大写/每词首字母大写
   - 标题标点：使用"."或不使用
   - 标题引号：是否使用引号包围

#### 7. 年份和卷期格式
1. 年份格式：
   - 括号样式：(2020) 或 2020
   - 位置：作者后或期刊名后
2. 卷期格式：
   - 是否使用"Vol." "No."前缀
   - 粗体卷号：在模板中添加粗体标记
   - 括号样式：12(3) 或 12, no.3

#### 8. 输出格式设置
1. 进入 `Bibliography > Layout`：
2. 调整选项：
   - `Start each reference with`: 每条参考文献起始符号
   - `End each reference with`: 结束符号
   - `Line Spacing`: 行间距
   - `Hanging indent`: 悬挂缩进

### 7. 注意事项
1. 修改后的样式建议另存为新文件
2. 备份原始样式文件
3. 测试修改后的样式
4. 注意期刊特殊要求

### 8. 常见问题解决
- **样式不显示**：检查安装路径
- **格式异常**：检查模板设置
- **中文显示问题**：确认语言设置
- **作者顺序错误**：检查作者列表设置

### 9. 推荐工具
- EndNote X9 或更新版本
- Style Editor
- Reference Manager
- Zotero（支持导入 ENS） 
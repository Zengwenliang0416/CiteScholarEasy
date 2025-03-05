## EndNote (ENW) 文件格式指南

### 1. ENW 文件是什么？
ENW 文件是 EndNote 引用管理软件使用的文件格式，用于存储文献的引用信息。每个 ENW 文件包含一篇或多篇文献的详细信息。

### 2. ENW 文件结构
每个条目以 `%0` 开始，包含多个标记字段。主要字段包括：

```
%0 类型标识（如：Journal Article, Book, Conference Paper等）
%T 标题
%A 作者（每个作者占一行）
%J 期刊名称
%D 出版年份
%V 卷号
%N 期号
%P 页码
%R DOI
%U URL
%X 摘要
```

### 3. 如何修改 ENW 文件
1. 使用文本编辑器打开 ENW 文件（如记事本、VS Code等）
2. 按照以下格式修改内容：
   ```
   %0 Journal Article
   %T 论文标题
   %A 第一作者
   %A 第二作者
   %J 期刊名称
   %D 2024
   %V 1
   %N 2
   %P 1-10
   %R doi:10.1234/example
   %U https://example.com
   %X 这里是论文摘要
   ```
3. 保存文件时确保使用 UTF-8 编码

### 4. 常见问题解决
- **中文显示乱码**：确保文件以 UTF-8 编码保存
- **EndNote 无法识别**：检查字段标记格式是否正确（%0、%T 等）
- **作者顺序错误**：每个作者单独一行，使用 %A 标记

### 5. 注意事项
- 每个字段标记必须在行首
- 字段之间不要有空行
- 保持字段标记的大写形式
- 一个文件可以包含多个文献条目，每个条目以 %0 开始

### 6. 批量修改建议
1. 使用 Excel 等工具批量处理数据
2. 使用脚本自动化修改（Python 示例）：
   ```python
   def modify_enw(input_file, output_file):
       with open(input_file, 'r', encoding='utf-8') as f:
           content = f.read()
       
       # 进行必要的修改
       # 例如：修改标题、作者等
       
       with open(output_file, 'w', encoding='utf-8') as f:
           f.write(modified_content)
   ```

### 7. 实用工具推荐
- EndNote（商业软件）
- JabRef（开源工具）
- Zotero（免费工具）
- BibDesk（Mac平台）

这些工具都可以帮助你更方便地编辑和管理 ENW 文件。

## EndNote Style (ENS) 文件格式指南

### 10. ENW 文件中的参考文献类型及格式详解

#### 1. 期刊论文 (Journal Article)
最常用的文献类型，用于引用学术期刊中发表的论文。

**必需字段**：
- `%0 Journal Article`: 文献类型标识
- `%T`: 论文完整标题
- `%A`: 作者（每位作者单独一行）
- `%J`: 期刊全名
- `%D`: 出版年份

**可选但推荐字段**：
- `%V`: 卷号（Volume）
- `%N`: 期号（Number/Issue）
- `%P`: 页码范围（如：123-145）
- `%R`: DOI号（建议格式：10.xxxx/xxxxx）
- `%U`: 论文URL链接
- `%X`: 摘要内容
- `%K`: 关键词（每个关键词用分号分隔）
- `%L`: 语言

**示例**：
```
%0 Journal Article
%T Attention Is All You Need
%A Vaswani, Ashish
%A Shazeer, Noam
%A Parmar, Niki
%J Neural Information Processing Systems
%D 2017
%V 30
%P 5998-6008
%R 10.48550/arXiv.1706.03762
%K attention mechanism; transformer; deep learning
%X We propose a new simple network architecture, the Transformer...
```

#### 2. 会议论文 (Conference Paper/Proceedings)
用于引用会议论文集或会议报告。

**必需字段**：
- `%0 Conference Paper`: 文献类型标识
- `%T`: 论文标题
- `%A`: 作者
- `%B`: 会议名称（完整名称）
- `%D`: 会议年份

**可选但推荐字段**：
- `%C`: 会议地点（城市, 国家）
- `%P`: 论文在会议论文集中的页码
- `%E`: 会议论文集编辑（如有）
- `%I`: 出版单位
- `%S`: 会议简称（如：ICML, NeurIPS）
- `%X`: 摘要
- `%U`: 在线链接
- `%L`: 语言

**示例**：
```
%0 Conference Paper
%T BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
%A Devlin, Jacob
%A Chang, Ming-Wei
%B Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics
%S NAACL
%C Minneapolis, USA
%D 2019
%P 4171-4186
%I Association for Computational Linguistics
%U https://aclanthology.org/N19-1423/
```

#### 3. 学位论文 (Thesis)
用于引用硕士或博士学位论文。

**必需字段**：
- `%0 Thesis`: 文献类型标识
- `%T`: 论文标题
- `%A`: 作者（学位获得者）
- `%I`: 授予学位的学校
- `%D`: 学位授予年份
- `%9`: 学位类型

**可选但推荐字段**：
- `%C`: 学校所在地
- `%E`: 导师姓名
- `%O`: 学院/系所
- `%X`: 摘要
- `%U`: 论文库链接
- `%L`: 语言
- `%K`: 关键词

**示例**：
```
%0 Thesis
%T 基于深度学习的自然语言处理研究
%A 张三
%I 清华大学
%D 2023
%9 PhD Thesis
%C 北京, 中国
%E 李四
%O 计算机科学与技术系
%X 本文研究了深度学习在自然语言处理中的应用...
%L 中文
```

#### 4. 图书 (Book)
用于引用整本图书。

**必需字段**：
- `%0 Book`: 文献类型标识
- `%T`: 书名
- `%A`: 作者/编者
- `%I`: 出版社
- `%D`: 出版年份

**可选但推荐字段**：
- `%C`: 出版地
- `%N`: 版次（如：第2版）
- `%@`: ISBN号
- `%G`: 丛书名称
- `%P`: 总页数
- `%E`: 译者（如果是译著）
- `%X`: 内容简介
- `%L`: 语言
- `%Y`: 原作语言（如果是译著）

**示例**：
```
%0 Book
%T 人工智能：一种现代方法
%A Stuart Russell
%A Peter Norvig
%I 人民邮电出版社
%D 2021
%C 北京
%N 第4版
%@ 978-7115559967
%E 姚天顺
%Y 英文
%L 中文
%P 1132
```

#### 5. 图书章节 (Book Section)
用于引用图书中的特定章节。

**必需字段**：
- `%0 Book Section`: 文献类型标识
- `%T`: 章节标题
- `%A`: 章节作者
- `%B`: 书名
- `%E`: 图书主编
- `%I`: 出版社
- `%D`: 出版年份

**可选但推荐字段**：
- `%C`: 出版地
- `%P`: 章节页码范围
- `%@`: ISBN号
- `%N`: 章节编号
- `%X`: 章节摘要
- `%K`: 关键词
- `%L`: 语言

**示例**：
```
%0 Book Section
%T 深度学习基础
%A 李明
%B 机器学习实践指南
%E 王强
%I 科学出版社
%D 2023
%C 北京
%P 45-89
%N 第3章
%@ 978-7-03-XXXXXX-X
%X 本章介绍深度学习的基本概念和应用...
```

#### 6. 报告 (Report)
用于引用技术报告、研究报告等。

**必需字段**：
- `%0 Report`: 文献类型标识
- `%T`: 报告标题
- `%A`: 作者
- `%I`: 发布机构
- `%D`: 发布年份

**可选但推荐字段**：
- `%9`: 报告类型和编号
- `%C`: 发布地点
- `%U`: 报告链接
- `%X`: 摘要
- `%K`: 关键词
- `%P`: 页数
- `%L`: 语言

**示例**：
```
%0 Report
%T 2023年人工智能发展报告
%A 中国科学院
%I 中国科学院人工智能研究所
%D 2023
%9 Technical Report No. AI2023-001
%C 北京
%P 156
%X 本报告总结了2023年人工智能领域的主要进展...
```

#### 7. 专利 (Patent)
用于引用专利文献。

**必需字段**：
- `%0 Patent`: 文献类型标识
- `%T`: 专利名称
- `%A`: 发明人
- `%I`: 专利权人
- `%D`: 申请/授权年份
- `%N`: 专利号

**可选但推荐字段**：
- `%C`: 专利授权国家/地区
- `%B`: 专利类型（发明/实用新型/外观设计）
- `%8`: 申请日期
- `%7`: 授权日期
- `%X`: 摘要
- `%U`: 专利文献链接
- `%K`: 关键词
- `%L`: 语言

**示例**：
```
%0 Patent
%T 一种基于深度学习的图像识别方法
%A 张三
%A 李四
%I XX科技有限公司
%D 2023
%N CN123456789A
%C 中国
%B 发明专利
%8 2023-01-15
%7 2023-12-20
%X 本发明提供了一种基于深度学习的图像识别方法...
```

#### 8. 网页 (Web Page)
用于引用网络资源。

**必需字段**：
- `%0 Web Page`: 文献类型标识
- `%T`: 网页标题
- `%A`: 作者/维护者
- `%D`: 访问年份
- `%U`: URL

**可选但推荐字段**：
- `%I`: 网站名称
- `%O`: 具体访问日期（格式：YYYY-MM-DD）
- `%X`: 内容描述
- `%E`: 编辑/维护者
- `%L`: 语言
- `%K`: 关键词
- `%Z`: 存档URL（如有）

**示例**：
```
%0 Web Page
%T 深度学习最新进展
%A OpenAI
%I OpenAI Blog
%D 2024
%U https://openai.com/blog/example
%O 2024-01-20
%X 这篇博客介绍了深度学习领域的最新研究进展...
%Z https://web.archive.org/web/...
```

#### 9. 数据集 (Dataset)
用于引用研究数据集。

**必需字段**：
- `%0 Dataset`: 文献类型标识
- `%T`: 数据集名称
- `%A`: 数据集作者/整理者
- `%D`: 发布年份
- `%U`: DOI或URL

**可选但推荐字段**：
- `%I`: 发布机构/平台
- `%V`: 版本号
- `%X`: 数据集描述
- `%C`: 数据收集地点
- `%K`: 关键词
- `%L`: 语言
- `%O`: 数据收集时间范围
- `%Z`: 数据格式

**示例**：
```
%0 Dataset
%T ImageNet数据集
%A Deng, Jia
%A Dong, Wei
%I Stanford University
%D 2009
%V 2012
%U https://doi.org/10.1109/CVPR.2009.5206848
%X ImageNet是一个包含超过1500万张标注图像的数据集...
%Z JPEG, XML
```

#### 10. 软件 (Computer Program)
用于引用软件程序。

**必需字段**：
- `%0 Computer Program`: 文献类型标识
- `%T`: 软件名称
- `%A`: 开发者
- `%D`: 发布年份
- `%V`: 版本号

**可选但推荐字段**：
- `%I`: 发布机构/公司
- `%U`: 下载链接
- `%X`: 软件描述
- `%C`: 开发语言
- `%L`: 界面语言
- `%O`: 操作系统要求
- `%K`: 关键词
- `%R`: DOI（如有）
- `%Z`: 许可证类型

**示例**：
```
%0 Computer Program
%T TensorFlow
%A Google Brain Team
%I Google LLC
%D 2024
%V 2.15.0
%U https://github.com/tensorflow/tensorflow
%X TensorFlow是一个开源机器学习框架...
%C Python, C++
%L 多语言
%O Linux, Windows, macOS
%Z Apache 2.0
```

#### 11. 论文集/文集 (Collection)
用于引用论文集、文集等集合性出版物。

**必需字段**：
- `%0 Collection`: 文献类型标识
- `%T`: 文集标题
- `%A`: 编者/作者
- `%I`: 出版社
- `%D`: 出版年份
- `%C`: 出版地

**可选但推荐字段**：
- `%G`: 丛书类型（如：论文集、文集等）
- `%E`: 其他编者
- `%P`: 总页数
- `%@`: ISBN号
- `%X`: 内容简介
- `%L`: 语言

**示例**：
```
%0 Collection
%T 职工教育研究论文集
%A 中国职工教育研究会
%I 人民教育出版社
%D 1985
%C 北京
%G 论文集
%L 中文
```

#### 12. 会议论文集 (Conference Proceedings)
用于引用完整的会议论文集。

**必需字段**：
- `%0 Conference Proceedings`: 文献类型标识
- `%T`: 会议论文集标题
- `%A`: 主办单位/编者
- `%I`: 出版社
- `%D`: 出版年份
- `%C`: 出版地

**可选但推荐字段**：
- `%B`: 会议名称
- `%S`: 会议简称
- `%E`: 编辑委员会
- `%P`: 总页数
- `%@`: ISBN号
- `%X`: 内容简介
- `%L`: 语言

**示例**：
```
%0 Conference Proceedings
%T 台湾光复六十五周年暨抗战史实学术研讨会论文集
%A 中国社会科学院台湾史研究中心
%I 九州出版社
%D 2012
%C 北京
%L 中文
```

#### 13. 报纸文章 (Newspaper Article)
用于引用报纸上的文章。

**必需字段**：
- `%0 Newspaper Article`: 文献类型标识
- `%T`: 文章标题
- `%A`: 作者
- `%B`: 报纸名称
- `%D`: 发表日期
- `%P`: 版次

**可选但推荐字段**：
- `%C`: 出版地
- `%X`: 内容摘要
- `%K`: 关键词
- `%L`: 语言
- `%U`: 电子版链接（如有）

**示例**：
```
%0 Newspaper Article
%T 数字革命与竞争国际化
%A 丁文详
%B 中国青年报
%D 2000-11-20
%P 15
%L 中文
```

#### 14. 档案文献 (Archive)
用于引用档案馆藏的历史文献。

**必需字段**：
- `%0 Archive`: 文献类型标识
- `%T`: 档案文献名称
- `%A`: 档案馆名称
- `%I`: 出版社（如果出版）
- `%D`: 出版/整理年份
- `%C`: 出版/收藏地

**可选但推荐字段**：
- `%N`: 档案号/分类号
- `%E`: 整理者
- `%X`: 内容描述
- `%L`: 语言
- `%O`: 档案形成时间
- `%Z`: 档案类型

**示例**：
```
%0 Archive
%T 中国明朝档案总汇
%A 中国第一历史档案馆
%A 辽宁省档案馆
%I 广西师范大学出版社
%D 2001
%C 桂林
%L 中文
```

#### 15. 电子期刊文章 (Electronic Journal Article)
用于引用在线发表的期刊文章。

**必需字段**：
- `%0 Electronic Article`: 文献类型标识
- `%T`: 文章标题
- `%A`: 作者
- `%J`: 期刊名称
- `%D`: 出版年份
- `%V`: 卷号
- `%N`: 期号
- `%P`: 页码
- `%U`: URL
- `%O`: 访问日期

**可选但推荐字段**：
- `%R`: DOI
- `%X`: 摘要
- `%K`: 关键词
- `%L`: 语言
- `%Z`: 其他在线信息

**示例**：
```
%0 Electronic Article
%T 恶性肿瘤个体化治疗靶向药物的临床表现
%A 储大同
%J 中华肿瘤杂志
%D 2010
%V 32
%N 10
%P 721-724
%U http://vip.calis.edu.cn/asp/Detailasp
%O 2014-06-25
%L 中文
```

#### 16. 电子图书 (Electronic Book)
用于引用电子版图书。

**必需字段**：
- `%0 Electronic Book`: 文献类型标识
- `%T`: 书名
- `%A`: 作者
- `%I`: 出版社
- `%D`: 出版年份
- `%U`: URL
- `%O`: 访问日期

**可选但推荐字段**：
- `%C`: 出版地
- `%E`: 编者/译者
- `%@`: ISBN/DOI
- `%X`: 内容简介
- `%L`: 语言
- `%Z`: 电子书格式

**示例**：
```
%0 Electronic Book
%T 当代美国外交
%A 赵学功
%I 社会科学文献出版社
%D 2001
%C 北京
%U http://www.cadal.zju.edu.cn/book/trySinglePage/33023884/l
%O 2014-06-11
%L 中文
```

#### 17. 电子报纸文章 (Electronic Newspaper Article)
用于引用在线报纸文章。

**必需字段**：
- `%0 Electronic Newspaper Article`: 文献类型标识
- `%T`: 文章标题
- `%A`: 作者
- `%B`: 报纸名称
- `%D`: 发表日期
- `%U`: URL
- `%O`: 访问日期

**可选但推荐字段**：
- `%P`: 版次（如有）
- `%X`: 内容摘要
- `%C`: 出版地
- `%L`: 语言
- `%Z`: 存档URL

**示例**：
```
%0 Electronic Newspaper Article
%T 大风沙过后的思考
%A 傅刚
%A 赵承
%A 李佳路
%B 北京青年报
%D 2001-12-19
%U http://www.bjyouth.com.cn/Bqb/20000412/GB/4216%5ED0412B1401.htm
%O 2005-09-28
%L 中文
```

#### 18. 网络资源 (Web Resource)
用于引用一般性网络资源。

**必需字段**：
- `%0 Web Resource`: 文献类型标识
- `%T`: 资源标题
- `%A`: 作者/创建者
- `%D`: 发布日期
- `%U`: URL
- `%O`: 访问日期

**可选但推荐字段**：
- `%I`: 网站名称
- `%E`: 编辑/维护者
- `%X`: 内容描述
- `%L`: 语言
- `%Z`: 资源类型

**示例**：
```
%0 Web Resource
%T 电子资源出版业信息化迈入快车道
%A 萧饪
%D 2001-12-19
%U http://www.ereader.com/news/20011219/200112190019.html
%O 2002-04-15
%L 中文
```

### 11. 通用注意事项
1. **字段顺序**：
   - `%0` 必须是第一个字段
   - 建议将重要字段（标题、作者、年份等）放在前面
   - 其他字段顺序可灵活调整

2. **多值字段处理**：
   - 作者：每个作者单独一行，都使用 `%A`
   - 关键词：使用分号分隔或每个关键词单独一行
   - 多个URL：主URL使用 `%U`，其他使用 `%Z`

3. **特殊字符处理**：
   - 避免使用 `%` 作为文本内容
   - 保留换行符和制表符的原始格式
   - 特殊符号（如±, ©, ™等）使用UTF-8编码

4. **最佳实践**：
   - 保持一致的格式和风格
   - 确保必需字段完整
   - 适当添加可选字段以提供更多信息
   - 定期验证URL的有效性
   - 使用标准的日期格式（YYYY-MM-DD）

5. **编码和保存**：
   - 始终使用UTF-8编码保存
   - 避免使用特殊字符作为文件名
   - 定期备份ENW文件 
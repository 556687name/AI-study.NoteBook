#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成Day1学习笔记Word文档：环境搭建与Python初探"""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import datetime

doc = Document()

# ===== 全局样式设置 =====
style = doc.styles['Normal']
style.font.name = '微软雅黑'
style.font.size = Pt(11)
style.paragraph_format.line_spacing = 1.5
style.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

# 设置标题样式
for i in range(1, 4):
    heading_style = doc.styles[f'Heading {i}']
    heading_style.font.name = '微软雅黑'
    heading_style.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    if i == 1:
        heading_style.font.size = Pt(18)
        heading_style.font.color.rgb = RGBColor(0x1A, 0x56, 0xDB)
    elif i == 2:
        heading_style.font.size = Pt(15)
        heading_style.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)
    elif i == 3:
        heading_style.font.size = Pt(13)
        heading_style.font.color.rgb = RGBColor(0x34, 0x49, 0x5E)

# ===== 辅助函数 =====
def add_code_block(doc, code_text, caption=""):
    """添加代码块"""
    if caption:
        p = doc.add_paragraph()
        run = p.add_run(f"📌 {caption}")
        run.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    p = doc.add_paragraph()
    p.style = doc.styles['Normal']
    run = p.add_run(code_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(0x2D, 0x2D, 0x2D)
    # 添加灰色背景效果（通过段落底纹）
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), 'F5F5F5')
    shading_elm.set(qn('w:val'), 'clear')
    p.paragraph_format.element.get_or_add_pPr().append(shading_elm)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    return p

def add_tip(doc, text):
    """添加提示框"""
    p = doc.add_paragraph()
    run = p.add_run(f"💡 提示：{text}")
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0xE6, 0x7E, 0x22)
    run.italic = True
    return p

def add_warning(doc, text):
    """添加注意事项"""
    p = doc.add_paragraph()
    run = p.add_run(f"⚠️ 注意：{text}")
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0xE7, 0x4C, 0x3C)
    run.bold = True
    return p

def add_table_with_data(doc, headers, rows, col_widths=None):
    """添加格式化表格"""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Light Grid Accent 1'
    # 表头
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = header
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.bold = True
                run.font.size = Pt(10)
    # 数据行
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = table.rows[ri + 1].cells[ci]
            cell.text = str(val)
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(10)
    doc.add_paragraph()  # 表后空行
    return table

# ==========================================
# 封面/标题
# ==========================================
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(80)
run = p.add_run("Python 学习笔记")
run.font.size = Pt(28)
run.font.color.rgb = RGBColor(0x1A, 0x56, 0xDB)
run.bold = True

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Day 1：环境搭建与 Python 初探")
run.font.size = Pt(20)
run.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(30)
run = p.add_run(f"日期：2026年8月5日（周二）  |  学习时长：约6-7小时  |  阶段：Python基础")
run.font.size = Pt(11)
run.font.color.rgb = RGBColor(0x7F, 0x8C, 0x8D)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(10)
run = p.add_run("学习目标：从零搭建完整Python开发环境，掌握变量、数据类型、运算符与输入输出")
run.font.size = Pt(10)
run.font.italic = True

doc.add_page_break()

# ==========================================
# 目录
# ==========================================
doc.add_heading('📑 目录', level=1)
toc_items = [
    "一、Python 开发环境搭建",
    "  1.1 安装 Python 3.10+",
    "  1.2 安装 VS Code 与插件配置",
    "  1.3 安装 Anaconda / Miniconda",
    "  1.4 创建虚拟环境",
    "  1.5 Jupyter Notebook 基本使用",
    "  1.6 注册 GitHub 账号",
    "二、编程语言基础概念",
    "  2.1 编译型语言 vs 解释型语言",
    "  2.2 Python 语言特点与优缺点",
    "三、Python 注释",
    "  3.1 单行注释",
    "  3.2 多行注释",
    "  3.3 注释的快捷键与最佳实践",
    "四、print() 输出函数详解",
    "五、变量与标识符",
    "  5.1 变量的定义与赋值",
    "  5.2 标识符命名规则（PEP8）",
    "  5.3 变量的动态类型特性",
    "六、Python 数据类型",
    "  6.1 数值类型：int / float / bool / complex",
    "  6.2 字符串 str",
    "  6.3 类型查看与转换",
    "  6.4 None 类型",
    "七、字符串详解",
    "  7.1 字符串的定义方式",
    "  7.2 字符串的索引与切片",
    "  7.3 字符串常用方法",
    "  7.4 转义字符",
    "  7.5 原始字符串",
    "八、字符串格式化",
    "  8.1 % 占位符格式化",
    "  8.2 f-string 格式化（推荐）",
    "  8.3 str.format() 方法",
    "九、运算符",
    "  9.1 算术运算符",
    "  9.2 赋值运算符",
    "  9.3 比较运算符",
    "  9.4 逻辑运算符",
    "  9.5 位运算符",
    "  9.6 成员运算符",
    "  9.7 身份运算符",
    "  9.8 运算符优先级总表",
    "十、input() 输入函数",
    "十一、综合练习",
    "十二、本日学习检查清单",
]
for item in toc_items:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    run = p.add_run(item)
    run.font.size = Pt(10)
    if not item.startswith("  "):
        run.bold = True

doc.add_page_break()

# ==========================================
# 一、Python 开发环境搭建
# ==========================================
doc.add_heading('一、Python 开发环境搭建', level=1)

doc.add_heading('1.1 安装 Python 3.10+', level=2)
doc.add_paragraph('Python 官网：https://www.python.org/downloads/')
doc.add_paragraph('下载 Windows 安装包（64-bit），安装时务必勾选 "Add Python to PATH"。')
doc.add_paragraph('验证安装：打开终端（PowerShell），输入以下命令：')
add_code_block(doc, 'python --version\n# 预期输出：Python 3.10.x（或更高版本）')
add_warning(doc, '如果出现 "python 不是内部或外部命令"，说明 PATH 未配置成功，需要重新安装并勾选 "Add Python to PATH"。')

doc.add_heading('1.2 安装 VS Code 与插件配置', level=2)
doc.add_paragraph('VS Code 官网：https://code.visualstudio.com/')
doc.add_paragraph('下载并安装 VS Code，然后安装以下必备插件：')
add_table_with_data(doc,
    ['插件名称', '用途', '安装方式'],
    [
        ['Python (Microsoft)', 'Python 语言支持、调试、智能提示', '扩展商店搜索 "Python"'],
        ['Jupyter (Microsoft)', '在 VS Code 中运行 .ipynb 笔记本', '扩展商店搜索 "Jupyter"'],
        ['GitLens', 'Git 可视化增强工具', '扩展商店搜索 "GitLens"'],
        ['Chinese Language Pack', 'VS Code 中文界面（可选）', '扩展商店搜索 "Chinese"'],
    ]
)

doc.add_heading('1.3 安装 Anaconda / Miniconda', level=2)
doc.add_paragraph('Anaconda 是一个包含 Python + 常用数据科学库 + conda 包管理器的集成环境。Miniconda 是其精简版。')
doc.add_paragraph('下载地址：https://docs.anaconda.com/miniconda/')
doc.add_paragraph('安装后验证：')
add_code_block(doc, 'conda --version\n# 预期输出：conda 24.x.x')
add_tip(doc, '推荐使用 Miniconda，体积更小，需要什么包再装什么。')

doc.add_heading('1.4 创建虚拟环境', level=2)
doc.add_paragraph('虚拟环境可以隔离不同项目的依赖，避免包冲突。这是 Python 开发的标准做法。')
add_code_block(doc,
    '# 创建名为 "study" 的虚拟环境，指定 Python 3.10\n'
    'conda create -n study python=3.10\n\n'
    '# 激活虚拟环境\n'
    'conda activate study\n\n'
    '# 退出虚拟环境（需要时使用）\n'
    'conda deactivate\n\n'
    '# 查看所有虚拟环境\n'
    'conda env list',
    'conda 虚拟环境操作命令'
)
add_warning(doc, '每次开始学习前，记得先执行 conda activate study 激活学习环境！')

doc.add_heading('1.5 Jupyter Notebook 基本使用', level=2)
doc.add_paragraph('Jupyter Notebook 是一个交互式编程环境，可以在浏览器中编写和运行代码，非常适合学习和数据探索。')
add_code_block(doc,
    '# 安装 Jupyter\n'
    'pip install jupyter\n\n'
    '# 启动 Jupyter Notebook\n'
    'jupyter notebook\n\n'
    '# 或者直接在 VS Code 中创建 .ipynb 文件',
    '安装与启动 Jupyter'
)
doc.add_paragraph('Jupyter 基本操作：')
add_table_with_data(doc,
    ['操作', '快捷键/方法', '说明'],
    [
        ['运行当前单元格', 'Shift + Enter', '执行代码并跳到下一个单元格'],
        ['运行当前单元格（不跳转）', 'Ctrl + Enter', '执行代码，留在当前单元格'],
        ['新建上方单元格', 'A（命令模式）', '按 Esc 进入命令模式，再按 A'],
        ['新建下方单元格', 'B（命令模式）', '按 Esc 进入命令模式，再按 B'],
        ['删除单元格', 'D D（命令模式）', '按 Esc 进入命令模式，连按两下 D'],
        ['切换为 Markdown', 'M（命令模式）', '将代码单元格切换为文本单元格'],
        ['切换为代码', 'Y（命令模式）', '将文本单元格切换为代码单元格'],
        ['显示行号', 'L（命令模式）', '在代码单元格中显示行号'],
    ]
)

doc.add_heading('1.6 注册 GitHub 账号', level=2)
doc.add_paragraph('GitHub 是全球最大的代码托管平台，是程序员的"社交网络"。')
doc.add_paragraph('注册地址：https://github.com/')
doc.add_paragraph('注册后完成以下操作：')
doc.add_paragraph('① 创建 study-log 仓库（Repository）：用于记录每日学习笔记和代码')
doc.add_paragraph('② 学习 Git 基本概念：仓库(Repo)、提交(Commit)、推送(Push)、拉取(Pull)')
doc.add_paragraph('③ 了解 README.md 文件的 Markdown 写法')

doc.add_page_break()

# ==========================================
# 二、编程语言基础概念
# ==========================================
doc.add_heading('二、编程语言基础概念', level=1)

doc.add_heading('2.1 编译型语言 vs 解释型语言', level=2)
add_table_with_data(doc,
    ['对比维度', '编译型语言（C/C++/Java）', '解释型语言（Python/JavaScript）'],
    [
        ['执行方式', '先整体翻译为机器码，再执行', '逐行翻译并即时执行'],
        ['运行速度', '快（直接运行机器码）', '较慢（需要解释器参与）'],
        ['开发效率', '编写→编译→运行，周期较长', '写即运行，开发效率高'],
        ['跨平台性', '需为不同平台单独编译', '只要有解释器即可跨平台运行'],
        ['典型场景', '操作系统、游戏引擎、嵌入式', '数据分析、Web开发、AI/ML'],
        ['错误发现', '编译时就能发现语法错误', '运行时才能发现错误'],
    ]
)

doc.add_heading('2.2 Python 语言特点', level=2)
doc.add_paragraph('Python 由 Guido van Rossum 于 1991 年发布，是目前最流行的编程语言之一。')
doc.add_paragraph('核心特点：')
doc.add_paragraph('• 语法简洁优雅 — 使用缩进代替花括号，代码像自然语言一样可读')
doc.add_paragraph('• 动态类型 — 变量不需要声明类型，运行时自动推断')
doc.add_paragraph('• 丰富的标准库 — "电池已包含"，内置了大量实用模块')
doc.add_paragraph('• 强大的第三方生态 — NumPy、Pandas、PyTorch、Django 等')
doc.add_paragraph('• 应用广泛 — AI/机器学习、Web开发、自动化运维、科学计算')

doc.add_page_break()

# ==========================================
# 三、Python 注释
# ==========================================
doc.add_heading('三、Python 注释', level=1)
doc.add_paragraph('注释是写在代码中的解释性文字，不会被 Python 执行。注释的作用是让代码更好理解、更方便维护。')

doc.add_heading('3.1 单行注释', level=2)
add_code_block(doc,
    '# 这是单行注释，以 # 开头\n'
    '# 解释器会忽略 # 后面的所有内容\n'
    'print("Hello World")  # 也可以写在代码的同一行后面'
)

doc.add_heading('3.2 多行注释', level=2)
doc.add_paragraph('Python 没有专门的多行注释语法，但可以用三引号（"""或\'\'\'）实现类似效果：')
add_code_block(doc,
    '"""\n'
    '这是多行注释（本质上是字符串）\n'
    '可以跨越多行书写\n'
    '不会被解释器执行\n'
    '"""\n\n'
    '# 单引号版本效果相同\n'
    "'''\n"
    "这也是一种多行注释\n"
    "'''"
)
add_tip(doc, '三引号本质上是多行字符串。如果它没有被赋值给变量或用在表达式中，Python 会忽略它，效果等同注释。')

doc.add_heading('3.3 注释的快捷键与最佳实践', level=2)
doc.add_paragraph('• VS Code 快捷键：选中多行，按 Ctrl + / 可以批量添加/取消注释')
doc.add_paragraph('• 注释应该解释"为什么"而不是"是什么" — 代码本身说明了"是什么"')
doc.add_paragraph('• 复杂的业务逻辑必须加注释')
doc.add_paragraph('• 不要用注释来保留废弃代码，用 Git 版本管理即可')

doc.add_page_break()

# ==========================================
# 四、print() 输出函数详解
# ==========================================
doc.add_heading('四、print() 输出函数详解', level=1)
doc.add_paragraph('print() 是 Python 中最常用的函数之一，用于将信息输出到控制台。')

doc.add_heading('4.1 基本用法', level=2)
add_code_block(doc,
    '# 输出单个值\n'
    'print("Hello World")       # 输出：Hello World\n\n'
    '# 输出多个值（用逗号分隔）\n'
    'print("姓名:", "张三", "年龄:", 20)'
    '# 输出：姓名: 张三 年龄: 20'
)

doc.add_heading('4.2 sep 参数 — 设置分隔符', level=2)
doc.add_paragraph('多个值之间的默认分隔符是空格，可以用 sep 修改：')
add_code_block(doc,
    'print("2026", "08", "05", sep="-")   # 输出：2026-08-05\n'
    'print("a", "b", "c", sep=", ")       # 输出：a, b, c\n'
    'print("a", "b", "c", sep="")         # 输出：abc（无分隔）'
)

doc.add_heading('4.3 end 参数 — 设置结尾字符', level=2)
doc.add_paragraph('print() 默认以换行符 \\n 结尾，可以用 end 修改：')
add_code_block(doc,
    'print("第一行", end=" --- ")\n'
    'print("接在同一行")   # 输出：第一行 --- 接在同一行\n\n'
    'print("不换行", end="")  # end="" 让下一个 print 紧跟在后面输出'
)
add_tip(doc, 'end=" " 可以让多次 print 的结果打印在同一行，用空格分隔。这在循环输出时非常实用。')

doc.add_page_break()

# ==========================================
# 五、变量与标识符
# ==========================================
doc.add_heading('五、变量与标识符', level=1)

doc.add_heading('5.1 变量的定义与赋值', level=2)
doc.add_paragraph('变量是存储数据的"容器"。在 Python 中，变量不需要声明类型，直接赋值即可创建。')
add_code_block(doc,
    '# 基本格式：变量名 = 值\n'
    'name = "小明"        # 字符串类型\n'
    'age = 20             # 整数类型\n'
    'height = 1.75        # 浮点类型\n'
    'is_student = True    # 布尔类型\n\n'
    '# 同时给多个变量赋值\n'
    'a, b, c = 1, 2, 3\n'
    'x = y = z = 100      # 三个变量都等于 100'
)
doc.add_paragraph('变量的本质：变量名指向内存中的一个地址（就像门牌号指向一个房间）。Python 中的变量更像"标签"，贴在数据对象上。')

doc.add_heading('5.2 同一个变量可以反复赋值', level=2)
add_code_block(doc,
    'x = 10        # x 是整数\n'
    'x = "hello"   # x 现在是字符串（动态类型！）\n'
    'x = [1,2,3]   # x 又变成了列表'
)
add_tip(doc, 'Python 是动态类型语言，变量可以随时指向不同类型的值。这带来了灵活性，但也需要自己注意类型的正确使用。')

doc.add_heading('5.3 标识符命名规则（PEP8 规范）', level=2)
doc.add_paragraph('标识符就是程序员定义的变量名、函数名、类名等。命名规则：')
doc.add_paragraph('① 只能包含字母（A-Z, a-z）、数字（0-9）和下划线（_）')
doc.add_paragraph('② 不能以数字开头（1var ❌，var1 ✅）')
doc.add_paragraph('③ 不能是 Python 关键字（如 if, for, class, def 等）')
doc.add_paragraph('④ 严格区分大小写（Name 和 name 是两个不同的变量）')
doc.add_paragraph('⑤ Python 推荐使用 snake_case 命名：全部小写，单词间用下划线连接')
add_code_block(doc,
    '# ✅ 好的命名\n'
    'user_name = "张三"\n'
    'total_score = 95\n'
    'max_retry_count = 3\n\n'
    '# ❌ 不好的命名\n'
    'a = "张三"          # 看不出含义\n'
    'userName = "张三"   # 驼峰命名在 Python 中不推荐\n'
    '1st_place = "NO"    # 不能以数字开头'
)
add_warning(doc, '查看 Python 关键字：在 Python 中执行 import keyword; print(keyword.kwlist)')

doc.add_page_break()

# ==========================================
# 六、Python 数据类型
# ==========================================
doc.add_heading('六、Python 数据类型', level=1)

doc.add_heading('6.1 数值类型', level=2)

doc.add_heading('① int（整型）', level=3)
doc.add_paragraph('表示整数，Python 3 的整数没有大小限制（只受内存限制）。')
add_code_block(doc,
    'a = 100\n'
    'b = -50\n'
    'c = 0\n'
    'big_num = 10 ** 100  # 10的100次方，Python 可以轻松表示\n\n'
    '# 不同进制表示\n'
    'bin_num = 0b1010    # 二进制，等于10进制的10\n'
    'oct_num = 0o17      # 八进制，等于10进制的15\n'
    'hex_num = 0xFF      # 十六进制，等于10进制的255'
)

doc.add_heading('② float（浮点型）', level=3)
doc.add_paragraph('表示小数，Python 使用 IEEE 754 双精度浮点数标准（约15-17位有效数字）。')
add_code_block(doc,
    'pi = 3.14159\n'
    'e = 2.718\n'
    'sci = 1.5e-3        # 科学记数法：1.5 × 10⁻³ = 0.0015\n\n'
    '# 注意浮点数精度问题\n'
    'print(0.1 + 0.2)    # 输出：0.30000000000000004（不是精确的 0.3！）'
)
add_warning(doc, '由于二进制无法精确表示某些小数，浮点数运算会出现微小的精度误差。涉及金钱计算时请使用 Decimal 类型！')

doc.add_heading('③ bool（布尔型）', level=3)
doc.add_paragraph('只有两个值：True（真）和 False（假）。本质上是 int 的子类，True = 1，False = 0。')
add_code_block(doc,
    'print(True == 1)    # True\n'
    'print(False == 0)   # True\n'
    'print(True + 1)     # 2（True 被当作 1 参与运算）\n'
    'print(False + 1)    # 1'
)
add_warning(doc, 'True/False 严格区分大小写！true/false 会报 NameError。')

doc.add_heading('④ complex（复数型）', level=3)
doc.add_paragraph('Python 原生支持复数，格式为 a + bj，其中 a 是实部，b 是虚部。')
add_code_block(doc,
    'c1 = 3 + 4j\n'
    'c2 = complex(3, 4)   # 等价写法\n\n'
    'print(c1.real)       # 输出实部：3.0\n'
    'print(c1.imag)       # 输出虚部：4.0\n'
    'print(c1 + c2)       # 复数运算：(6+8j)'
)

doc.add_heading('6.2 类型查看与转换', level=2)
doc.add_paragraph('使用 type() 查看变量类型，使用类型名作为函数进行类型转换：')
add_code_block(doc,
    'x = 42\n'
    'print(type(x))         # <class \'int\'>\n\n'
    '# 类型转换\n'
    'int("123")    → 123        # 字符串转整数\n'
    'float("3.14") → 3.14       # 字符串转浮点\n'
    'str(100)      → "100"      # 整数转字符串\n'
    'bool(1)       → True       # 非0为True\n'
    'bool(0)       → False      # 0为False\n'
    'bool("")      → False      # 空字符串为False\n'
    'bool("abc")   → True       # 非空字符串为True',
    '常用类型转换函数'
)
add_tip(doc, 'int() 转换浮点数时会直接截断小数部分（不是四舍五入）：int(3.9) = 3。如需四舍五入，用 round(3.9)。')

doc.add_heading('6.3 None 类型', level=2)
doc.add_paragraph('None 是 Python 中的"空值"，表示"没有"或"不存在"。它既不是 0，也不是空字符串，也不是 False。')
add_code_block(doc,
    'result = None           # 初始化变量，暂不赋值\n'
    'print(type(None))      # <class \'NoneType\'>\n'
    'print(None == False)   # False（None 不等于 False）\n'
    'print(None is None)    # True（判断 None 用 is，不用 ==）'
)
add_warning(doc, '判断一个值是否为 None，必须使用 "is None" 或 "is not None"，而不是 "== None"。')

doc.add_page_break()

# ==========================================
# 七、字符串详解
# ==========================================
doc.add_heading('七、字符串详解', level=1)
doc.add_paragraph('字符串是 Python 中最常用的数据类型之一，用来表示文本信息。')

doc.add_heading('7.1 字符串的定义方式', level=2)
add_code_block(doc,
    "# 四种方式定义字符串\n"
    "s1 = 'Hello'            # 单引号\n"
    's2 = "Hello"            # 双引号（效果相同）\n'
    "s3 = '''多行\n"
    "字符串'''              # 三单引号，可以跨行\n"
    's4 = """多行\n'
    '字符串"""              # 三双引号，也可以跨行'
)
add_tip(doc, '如果字符串里含有单引号，外面用双引号包裹；含有双引号，外面用单引号包裹。这样就不用转义了。')

doc.add_heading('7.2 字符串的索引与切片', level=2)
doc.add_paragraph('字符串中的每个字符都有一个编号（索引），从左到右从 0 开始，从右到左从 -1 开始。')
add_code_block(doc,
    's = "Hello Python"\n\n'
    '# 索引（取单个字符）\n'
    's[0]    → "H"      # 第1个字符\n'
    's[-1]   → "n"      # 倒数第1个字符\n'
    's[6]    → "P"      # 第7个字符\n\n'
    '# 切片（取一段字符）— 格式：[start:stop:step]\n'
    's[0:5]   → "Hello" # 索引0到4（左闭右开，不含索引5）\n'
    's[6:]    → "Python"# 从索引6到末尾\n'
    's[:5]    → "Hello" # 从头到索引4\n'
    's[::2]   → "HloPto"# 每2个字符取1个\n'
    's[::-1]  → "nohtyP olleH"  # 倒序！',
    '字符串索引与切片'
)
add_warning(doc, '切片是"左闭右开"区间：s[0:5] 包含索引 0~4，不包含索引 5。这是 Python 的重要约定！')

doc.add_heading('7.3 字符串常用方法', level=2)
doc.add_paragraph('字符串方法是对字符串进行各种操作的函数。注意：字符串是不可变的，所有方法都返回新字符串，不会修改原字符串！')
add_table_with_data(doc,
    ['方法', '作用', '示例', '结果'],
    [
        ['s.upper()', '全部转大写', '"hello".upper()', '"HELLO"'],
        ['s.lower()', '全部转小写', '"HELLO".lower()', '"hello"'],
        ['s.strip()', '去除首尾空格', '" hi ".strip()', '"hi"'],
        ['s.replace(a,b)', '替换子串', '"abc".replace("a","x")', '"xbc"'],
        ['s.split(",")', '按分隔符分割', '"a,b,c".split(",")', '["a","b","c"]'],
        ['s.join(list)', '用分隔符拼接列表', '",".join(["a","b"])', '"a,b"'],
        ['s.find("x")', '查找子串位置', '"abc".find("b")', '1（未找到返回-1）'],
        ['s.count("x")', '统计子串出现次数', '"abca".count("a")', '2'],
        ['s.startswith("x")', '是否以x开头', '"abc".startswith("a")', 'True'],
        ['s.endswith("x")', '是否以x结尾', '"abc".endswith("c")', 'True'],
        ['s.isdigit()', '是否全是数字', '"123".isdigit()', 'True'],
        ['len(s)', '字符串长度（函数）', 'len("abc")', '3'],
    ]
)

doc.add_heading('7.4 转义字符', level=2)
doc.add_paragraph('转义字符以反斜杠 \\ 开头，用于表示特殊字符：')
add_table_with_data(doc,
    ['转义字符', '含义', '示例代码', '输出效果'],
    [
        ['\\\\n', '换行', 'print("a\\\\nb")', 'a（换行）b'],
        ['\\\\t', '制表符（Tab）', 'print("a\\\\tb")', 'a    b'],
        ['\\\\r', '回车', 'print("abc\\\\rX")', 'Xbc'],
        ['\\\\\\\\', '反斜杠本身', 'print("a\\\\\\\\b")', 'a\\\\b'],
        ["\\\\'", '单引号', "print('It\\'s ok')", "It's ok"],
        ['\\\\"', '双引号', 'print("He said \\"Hi\\"")', 'He said "Hi"'],
    ]
)
add_tip(doc, '\\r（回车）将光标移到行首，后续内容会覆盖之前的字符。这在制作进度条效果时很常用。')

doc.add_heading('7.5 原始字符串（raw string）', level=2)
doc.add_paragraph('在字符串前加 r，转义字符将原样输出，常用于正则表达式和文件路径：')
add_code_block(doc,
    '# 普通字符串：\\n 被当作换行\n'
    'print("C:\\new\\test.txt")   # 输出错误\n\n'
    '# 原始字符串：\\n 只是两个字符\n'
    'print(r"C:\\new\\test.txt")  # 正确输出：C:\\new\\test.txt'
)

doc.add_page_break()

# ==========================================
# 八、字符串格式化
# ==========================================
doc.add_heading('八、字符串格式化', level=1)
doc.add_paragraph('字符串格式化就是把变量的值"嵌入"到字符串的指定位置。')

doc.add_heading('8.1 % 占位符格式化（传统方式）', level=2)
add_table_with_data(doc,
    ['占位符', '含义', '示例'],
    [
        ['%s', '字符串（万能，可替代任何类型）', 'print("name: %s" % "Tom")'],
        ['%d', '整数', 'print("age: %d" % 20)'],
        ['%f', '浮点数（默认6位小数）', 'print("pi: %f" % 3.14)'],
        ['%.2f', '浮点数（保留2位小数）', 'print("pi: %.2f" % 3.14159) → 3.14'],
        ['%4d', '整数，占4位，右对齐', 'print("%4d" % 5) → "   5"'],
        ['%04d', '整数，占4位，用0填充', 'print("%04d" % 5) → "0005"'],
        ['%%', '输出一个百分号', 'print("得分：%d%%" % 95) → 得分：95%'],
    ]
)
add_code_block(doc,
    'name = "刘鑫"\n'
    'age = 19\n'
    'print("我的名字：%s，我的年龄：%d" % (name, age))\n'
    '# 输出：我的名字：刘鑫，我的年龄：19',
    '% 占位符示例'
)

doc.add_heading('8.2 f-string 格式化（推荐方式 ⭐）', level=2)
doc.add_paragraph('Python 3.6+ 引入，是目前最推荐的方式，简洁直观且执行速度快。')
add_code_block(doc,
    'name = "小明"\n'
    'age = 19\n'
    '# 基本用法：在字符串前加 f，用 {变量名} 嵌入变量\n'
    'print(f"姓名：{name}，年龄：{age}")  # 姓名：小明，年龄：19\n\n'
    '# 花括号内可以写表达式\n'
    'print(f"明年：{age + 1}岁")          # 明年：20岁\n'
    'print(f"10的3次方：{10**3}")         # 10的3次方：1000\n\n'
    '# 指定格式\n'
    'pi = 3.1415926\n'
    'print(f"π ≈ {pi:.2f}")              # π ≈ 3.14（保留2位小数）\n'
    'print(f"π ≈ {pi:.4f}")              # π ≈ 3.1416（保留4位小数，四舍五入）\n\n'
    '# 对齐与填充\n'
    'print(f"{name:>10}")                 # 右对齐，占10位\n'
    'print(f"{name:<10}")                 # 左对齐，占10位\n'
    'print(f"{name:^10}")                 # 居中，占10位',
    'f-string 用法大全'
)
add_tip(doc, 'f-string 不仅可读性好，而且是三种格式化方式中执行速度最快的。新建代码请优先使用 f-string！')

doc.add_heading('8.3 str.format() 方法（了解即可）', level=2)
add_code_block(doc,
    'name = "小明"\n'
    'age = 19\n'
    'print("姓名：{}，年龄：{}".format(name, age))\n'
    'print("姓名：{0}，年龄：{1}，{0}同学你好".format(name, age))\n'
    '# {0} 表示第一个参数，{1} 表示第二个参数'
)

doc.add_page_break()

# ==========================================
# 九、运算符
# ==========================================
doc.add_heading('九、运算符', level=1)

doc.add_heading('9.1 算术运算符', level=2)
add_table_with_data(doc,
    ['运算符', '含义', '示例', '结果'],
    [
        ['+', '加法', '5 + 3', '8'],
        ['-', '减法', '5 - 3', '2'],
        ['*', '乘法', '5 * 3', '15'],
        ['/', '除法（结果为float）', '5 / 2', '2.5'],
        ['//', '整除（取商）', '5 // 2', '2'],
        ['%', '取余（取模）', '5 % 2', '1'],
        ['**', '幂运算', '2 ** 3', '8'],
    ]
)
add_warning(doc, '/ 永远返回 float 类型！即使 4 / 2 的结果也是 2.0 而不是 2。')
add_tip(doc, '// 和 % 配合使用很实用：例如 17 // 5 = 3（商），17 % 5 = 2（余数）。')

doc.add_heading('9.2 赋值运算符', level=2)
add_table_with_data(doc,
    ['运算符', '含义', '等价写法'],
    [
        ['=', '基本赋值', 'x = 10'],
        ['+=', '加法赋值', 'x += 5 → x = x + 5'],
        ['-=', '减法赋值', 'x -= 5 → x = x - 5'],
        ['*=', '乘法赋值', 'x *= 2 → x = x * 2'],
        ['/=', '除法赋值', 'x /= 2 → x = x / 2'],
        ['//=', '整除赋值', 'x //= 2 → x = x // 2'],
        ['%=', '取余赋值', 'x %= 3 → x = x % 3'],
        ['**=', '幂赋值', 'x **= 2 → x = x ** 2'],
    ]
)
add_warning(doc, '+= 和 -= 必须连着写，中间不能有空格。另外，5 += 3 是错误的，赋值运算符左边必须是变量。')

doc.add_heading('9.3 比较运算符', level=2)
doc.add_paragraph('比较运算符的结果是布尔值（True / False）：')
add_table_with_data(doc,
    ['运算符', '含义', '示例', '结果'],
    [
        ['==', '等于', '5 == 5', 'True'],
        ['!=', '不等于', '5 != 3', 'True'],
        ['>', '大于', '5 > 3', 'True'],
        ['<', '小于', '5 < 3', 'False'],
        ['>=', '大于等于', '5 >= 5', 'True'],
        ['<=', '小于等于', '3 <= 5', 'True'],
    ]
)
add_warning(doc, '== 是比较是否相等，= 是赋值。把 == 写成 = 是初学者最常见的错误！')

doc.add_heading('9.4 逻辑运算符', level=2)
doc.add_paragraph('逻辑运算符用于组合多个条件：')
add_code_block(doc,
    '# and：两边都为 True，结果才是 True\n'
    'True and True   → True\n'
    'True and False  → False\n\n'
    '# or：只要一边为 True，结果就是 True\n'
    'True or False   → True\n'
    'False or False  → False\n\n'
    '# not：取反\n'
    'not True        → False\n'
    'not False       → True\n\n'
    '# 实际应用\n'
    'age = 20\n'
    'has_ticket = True\n'
    'can_enter = age >= 18 and has_ticket  # 两个条件都满足才行',
    '逻辑运算符'
)
add_tip(doc, 'Python 的逻辑运算符使用英文单词（and/or/not），而不是符号（&&/||/!）。这是和 C/Java 等语言的一个重要区别。')

doc.add_heading('9.5 位运算符', level=2)
doc.add_paragraph('位运算符直接对整数的二进制位进行操作（初学可先了解，后续深度学习用到时再深入）：')
add_table_with_data(doc,
    ['运算符', '含义', '示例', '结果'],
    [
        ['&', '按位与', '5 & 3 (101 & 011)', '1 (001)'],
        ['|', '按位或', '5 | 3 (101 | 011)', '7 (111)'],
        ['^', '按位异或', '5 ^ 3 (101 ^ 011)', '6 (110)'],
        ['~', '按位取反', '~5', '-6（涉及补码）'],
        ['<<', '左移', '5 << 1', '10（相当于×2）'],
        ['>>', '右移', '5 >> 1', '2（相当于//2）'],
    ]
)

doc.add_heading('9.6 成员运算符', level=2)
doc.add_paragraph('判断一个值是否存在于一个容器（字符串、列表、元组、字典等）中：')
add_code_block(doc,
    '# in：在...之中\n'
    'print("a" in "abc")        # True\n'
    'print(2 in [1, 2, 3])      # True\n\n'
    '# not in：不在...之中\n'
    'print("x" not in "abc")    # True\n'
    'print(9 not in [1, 2, 3])  # True'
)

doc.add_heading('9.7 身份运算符', level=2)
doc.add_paragraph('判断两个变量是否引用同一个内存对象（不是判断值是否相等！）：')
add_code_block(doc,
    'a = [1, 2, 3]\n'
    'b = [1, 2, 3]\n'
    'c = a\n\n'
    'print(a == b)   # True（值相同）\n'
    'print(a is b)   # False（不同对象）\n'
    'print(a is c)   # True（同一个对象）\n\n'
    '# is 判断的是内存地址是否相同，== 判断的是值是否相同'
)

doc.add_heading('9.8 运算符优先级总表', level=2)
doc.add_paragraph('从高到低排列（同级运算符从左到右执行）：')
add_code_block(doc,
    '1. **            幂运算\n'
    '2. ~ + -         按位取反、正负号\n'
    '3. * / % //      乘除、取余、整除\n'
    '4. + -           加减\n'
    '5. << >>         位移\n'
    '6. &             按位与\n'
    '7. ^             按位异或\n'
    '8. |             按位或\n'
    '9. == != > < >= <= 比较\n'
    '10. not          逻辑非\n'
    '11. and          逻辑与\n'
    '12. or           逻辑或',
    '运算符优先级（高→低）'
)
add_tip(doc, '不确定优先级时，用括号 () 明确指定运算顺序。括号内的先执行，代码也更易读。')

doc.add_page_break()

# ==========================================
# 十、input() 输入函数
# ==========================================
doc.add_heading('十、input() 输入函数', level=1)
doc.add_paragraph('input() 用于从键盘接收用户输入的数据。程序执行到 input() 时会暂停，等待用户输入并按下回车。')

doc.add_heading('10.1 基本用法', level=2)
add_code_block(doc,
    '# 格式：变量 = input("提示文字")\n'
    'name = input("请输入你的名字：")\n'
    'print(f"你好，{name}！")\n\n'
    '# 运行效果：\n'
    '# 请输入你的名字：小明（回车）\n'
    '# 你好，小明！'
)

doc.add_heading('10.2 重要：input() 返回的一定是字符串！', level=2)
add_code_block(doc,
    'age = input("请输入年龄：")   # 用户输入 19\n'
    'print(type(age))              # <class \'str\'> — 是字符串，不是整数！\n\n'
    '# 需要数学运算时，必须先转换类型\n'
    'age = int(input("请输入年龄："))\n'
    'print(f"明年你 {age + 1} 岁")  # 正确：先转 int 再做加法'
)
add_warning(doc, 'input() 无论用户输入什么，返回的永远是字符串类型。需要数字时请务必使用 int() 或 float() 转换！')

doc.add_page_break()

# ==========================================
# 十一、综合练习
# ==========================================
doc.add_heading('十一、综合练习', level=1)

doc.add_heading('练习 1：简单计算器', level=2)
doc.add_paragraph('编写一个程序，让用户输入两个数字，然后输出它们的和、差、积、商。')
add_code_block(doc,
    'num1 = float(input("请输入第一个数字："))\n'
    'num2 = float(input("请输入第二个数字："))\n\n'
    'print(f"{num1} + {num2} = {num1 + num2}")\n'
    'print(f"{num1} - {num2} = {num1 - num2}")\n'
    'print(f"{num1} × {num2} = {num1 * num2}")\n'
    'print(f"{num1} ÷ {num2} = {num1 / num2:.2f}")',
    '简单计算器'
)

doc.add_heading('练习 2：个人信息名片', level=2)
doc.add_paragraph('编写程序收集用户信息并格式化输出：')
add_code_block(doc,
    'print("=" * 30)\n'
    'name = input("姓名：")\n'
    'age = input("年龄：")\n'
    'school = input("学校：")\n'
    'hobby = input("爱好：")\n'
    'print("=" * 30)\n'
    'print(f"【个人名片】\\n姓名：{name}\\n年龄：{age}\\n学校：{school}\\n爱好：{hobby}")',
    '个人名片生成器'
)

doc.add_page_break()

# ==========================================
# 十二、本日学习检查清单
# ==========================================
doc.add_heading('十二、本日学习检查清单 ✅', level=1)
doc.add_paragraph('完成以下所有项目后，才算真正掌握了 Day 1 的内容：')
doc.add_paragraph('□ Python 3.10+ 已正确安装，python --version 正常')
doc.add_paragraph('□ VS Code 已安装，Python 和 Jupyter 插件已启用')
doc.add_paragraph('□ 已创建 conda 虚拟环境 study，并激活使用')
doc.add_paragraph('□ 能在 Jupyter Notebook 中编写和运行代码')
doc.add_paragraph('□ 已注册 GitHub 账号，创建了 study-log 仓库')
doc.add_paragraph('□ 理解编译型语言和解释型语言的区别')
doc.add_paragraph('□ 掌握单行注释（#）和多行注释（三引号）的用法')
doc.add_paragraph('□ 能灵活使用 print() 的 sep 和 end 参数')
doc.add_paragraph('□ 知道标识符的命名规则（字母/数字/下划线，不能数字开头，不能关键字）')
doc.add_paragraph('□ 掌握 4 种数值类型：int、float、bool、complex')
doc.add_paragraph('□ 能用 type() 查看类型，能用 int()/float()/str() 进行类型转换')
doc.add_paragraph('□ 理解 None 的含义和判断方式（is None）')
doc.add_paragraph('□ 掌握字符串索引（[n]）和切片（[start:stop:step]）')
doc.add_paragraph('□ 会用字符串常用方法：upper、lower、strip、replace、split、join、find')
doc.add_paragraph('□ 理解转义字符：\\\\n、\\\\t、\\\\r，知道原始字符串 r"..." 的用法')
doc.add_paragraph('□ 推荐使用 f-string 进行字符串格式化')
doc.add_paragraph('□ 掌握所有运算符：算术、赋值、比较、逻辑、位、成员、身份')
doc.add_paragraph('□ 理解 =（赋值）和 ==（比较）的区别')
doc.add_paragraph('□ 能用 input() 接收用户输入，并正确进行类型转换')
doc.add_paragraph('□ 完成综合练习：简单计算器和信息名片')

# 保存
output_path = r'D:\NoteBook\Day1_学习笔记_环境搭建与Python初探.docx'
doc.save(output_path)
print(f"✅ Day 1 文档已生成：{output_path}")

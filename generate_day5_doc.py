#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate Day 5 Word Document: NumPy and Pandas"""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

style = doc.styles['Normal']
style.font.name = '微软雅黑'; style.font.size = Pt(11)
style.paragraph_format.line_spacing = 1.5
style.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

for i in range(1, 4):
    hs = doc.styles[f'Heading {i}']
    hs.font.name = '微软雅黑'; hs.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    if i == 1: hs.font.size = Pt(18); hs.font.color.rgb = RGBColor(0x1A,0x56,0xDB)
    elif i == 2: hs.font.size = Pt(15); hs.font.color.rgb = RGBColor(0x2C,0x3E,0x50)
    elif i == 3: hs.font.size = Pt(13); hs.font.color.rgb = RGBColor(0x34,0x49,0x5E)

def add_code(doc, code, caption=""):
    if caption:
        p = doc.add_paragraph(); r = p.add_run(f"📌 {caption}")
        r.bold = True; r.font.size = Pt(10); r.font.color.rgb = RGBColor(0x66,0x66,0x66)
    p = doc.add_paragraph(); r = p.add_run(code)
    r.font.name = 'Consolas'; r.font.size = Pt(9.5); r.font.color.rgb = RGBColor(0x2D,0x2D,0x2D)
    shd = OxmlElement('w:shd'); shd.set(qn('w:fill'), 'F5F5F5'); shd.set(qn('w:val'), 'clear')
    p.paragraph_format.element.get_or_add_pPr().append(shd)
    p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2)

def add_tip(doc, text):
    p = doc.add_paragraph(); r = p.add_run(f"💡 提示：{text}")
    r.font.size = Pt(10); r.font.color.rgb = RGBColor(0xE6,0x7E,0x22); r.italic = True

def add_warn(doc, text):
    p = doc.add_paragraph(); r = p.add_run(f"⚠️ 注意：{text}")
    r.font.size = Pt(10); r.font.color.rgb = RGBColor(0xE7,0x4C,0x3C); r.bold = True

def add_table(doc, headers, rows):
    t = doc.add_table(rows=1+len(rows), cols=len(headers))
    t.style = 'Light Grid Accent 1'
    for i,h in enumerate(headers):
        c = t.rows[0].cells[i]; c.text = h
        for p in c.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs: r.bold = True; r.font.size = Pt(10)
    for ri,row in enumerate(rows):
        for ci,val in enumerate(row):
            c = t.rows[ri+1].cells[ci]; c.text = str(val)
            for p in c.paragraphs:
                for r in p.runs: r.font.size = Pt(10)
    doc.add_paragraph()
    return t

# ===== 封面 =====
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_before = Pt(80)
r = p.add_run("Python 学习笔记"); r.font.size = Pt(28); r.font.color.rgb = RGBColor(0x1A,0x56,0xDB); r.bold = True
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Day 5：NumPy 与 Pandas 实战"); r.font.size = Pt(20); r.font.color.rgb = RGBColor(0x2C,0x3E,0x50)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_before = Pt(30)
r = p.add_run("日期：2026年8月9日（周六）  |  学习时长：约6-7小时  |  阶段：Python基础")
r.font.size = Pt(11); r.font.color.rgb = RGBColor(0x7F,0x8C,0x8D)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("学习目标：掌握 NumPy 数组操作与广播机制，熟练使用 Pandas 进行数据清洗与分析")
r.font.size = Pt(10); r.font.italic = True

doc.add_page_break()

doc.add_heading('📑 目录', level=1)
toc = [
    "第一部分：NumPy 篇",
    "一、NumPy 简介与安装", "二、ndarray 数组基础",
    "  2.1 创建 ndarray", "  2.2 ndarray 属性", "  2.3 数据类型与转换",
    "三、NumPy 索引与切片", "  3.1 基本索引与切片",
    "  3.2 花式索引（Fancy Indexing）", "  3.3 布尔索引",
    "四、NumPy 数组操作", "  4.1 形状变换", "  4.2 数组拼接与分割",
    "五、NumPy 数学运算", "  5.1 向量化运算", "  5.2 常用数学函数",
    "  5.3 矩阵运算", "六、广播机制（Broadcasting）",
    "七、NumPy 随机数", "八、实战：用 NumPy 实现梯度下降",
    "第二部分：Pandas 篇",
    "九、Pandas 简介", "十、Series 与 DataFrame",
    "  10.1 Series", "  10.2 DataFrame 的创建",
    "  10.3 DataFrame 常用属性",
    "十一、数据读取与写入", "十二、数据选择与过滤",
    "  12.1 选择列", "  12.2 选择行", "  12.3 条件过滤",
    "十三、数据清洗", "十四、数据排序与分组",
    "  14.1 排序", "  14.2 分组聚合 groupby",
    "十五、数据合并：merge / join / concat", "十六、数据变换：apply / map",
    "十七、Pandas 数据可视化入门", "十八、Matplotlib 基础绘图",
    "十九、综合实战：分析游戏数据", "二十、本日学习检查清单",
]
for item in toc:
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(1); p.paragraph_format.space_after = Pt(1)
    r = p.add_run(item); r.font.size = Pt(10)
    if not item.startswith("  "): r.bold = True

doc.add_page_break()

# ========================
# PART 1: NumPy
# ========================
doc.add_heading('第一部分：NumPy 篇', level=1)

doc.add_heading('一、NumPy 简介与安装', level=1)
doc.add_paragraph('NumPy（Numerical Python）是 Python 科学计算的基础库。它提供了高性能的多维数组对象（ndarray）和丰富的数学运算工具。')
doc.add_paragraph('几乎所有 Python 数据科学库（Pandas、Matplotlib、Scikit-learn、PyTorch 等）都依赖 NumPy。')
add_code(doc, 'pip install numpy', '安装 NumPy')
add_code(doc, 'import numpy as np  # 约定俗成的别名', '导入约定')

doc.add_heading('二、ndarray 数组基础', level=1)
doc.add_paragraph('ndarray（N-dimensional array）是 NumPy 的核心数据结构，是一个同质（所有元素同类型）的多维数组。')

doc.add_heading('2.1 创建 ndarray', level=2)
doc.add_paragraph('创建数组有六种常用方式：')
add_code(doc,
    'import numpy as np\n\n'
    '# ① 从 Python 列表创建\n'
    'a = np.array([1, 2, 3])\n'
    'b = np.array([[1, 2, 3], [4, 5, 6]])  # 二维数组\n\n'
    '# ② arange：类似 range，返回数组\n'
    'c = np.arange(0, 10, 2)      # array([0, 2, 4, 6, 8])\n'
    'd = np.arange(15).reshape(3, 5)  # 0~14，重塑为3行5列\n\n'
    '# ③ zeros / ones：全0或全1数组\n'
    'zeros = np.zeros((3, 4))     # 3行4列的全0数组\n'
    'ones = np.ones((2, 3))       # 2行3列的全1数组\n\n'
    '# ④ full：填充指定值\n'
    'full = np.full((2, 3), 7)    # 2行3列，全部填7\n\n'
    '# ⑤ eye / identity：单位矩阵\n'
    'identity = np.eye(3)          # 3x3 单位矩阵\n\n'
    '# ⑥ linspace：等间距序列\n'
    'linear = np.linspace(0, 1, 5) # array([0, 0.25, 0.5, 0.75, 1.0])',
    '创建 ndarray 的六种方式'
)

doc.add_heading('2.2 ndarray 常用属性', level=2)
add_table(doc,
    ['属性', '含义', '示例（a = np.array([[1,2,3],[4,5,6]])）'],
    [
        ['a.ndim', '数组的维数（轴的数量）', '2'],
        ['a.shape', '数组的形状（各维度大小）', '(2, 3) — 2行3列'],
        ['a.size', '数组的元素总数', '6'],
        ['a.dtype', '数组元素的数据类型', 'int32 或 int64'],
        ['a.itemsize', '每个元素的字节数', '4（int32）或 8（int64）'],
        ['a.nbytes', '数组占用的总字节数', '24（= 6 × 4）'],
    ]
)

doc.add_heading('2.3 数据类型与转换', level=2)
add_code(doc,
    '# 创建时指定类型\n'
    'a = np.array([1, 2, 3], dtype=np.float64)  # 浮点型\n'
    'b = np.array([1, 2, 3], dtype=np.int32)    # 32位整型\n\n'
    '# 转换已有数组的类型（astype 返回新数组）\n'
    'arr = np.array([1.5, 2.7, 3.2])\n'
    'arr_int = arr.astype(np.int32)  # array([1, 2, 3]) — 截断，不是四舍五入！',
    '数据类型指定与转换'
)
add_table(doc,
    ['类型名', '含义', '范围'],
    [
        ['np.int32', '32位有符号整数', '-2³¹ ~ 2³¹-1'],
        ['np.int64', '64位有符号整数（默认）', '很大'],
        ['np.float32', '32位浮点数', '约7位有效数字'],
        ['np.float64', '64位浮点数（默认）', '约15位有效数字'],
        ['np.bool_', '布尔型', 'True / False'],
        ['np.str_', '字符串', ''],
    ]
)

doc.add_page_break()

doc.add_heading('三、NumPy 索引与切片', level=1)

doc.add_heading('3.1 基本索引与切片', level=2)
add_code(doc,
    'arr = np.array([[1, 2, 3, 4],\n'
    '                [5, 6, 7, 8],\n'
    '                [9, 10, 11, 12]])\n\n'
    '# 索引（与列表语法相同）\n'
    'arr[0, 0]       → 1       # 第0行第0列\n'
    'arr[2, 3]       → 12      # 第2行第3列\n'
    'arr[-1, -1]     → 12      # 最后一行最后一列\n\n'
    '# 切片（每维独立切片）\n'
    'arr[:2, 1:3]    → [[2, 3],    # 前2行，第1~2列\n'
    '                    [6, 7]]\n'
    'arr[:, ::2]     → [[1, 3],    # 所有行，每隔一列\n'
    '                    [5, 7],\n'
    '                    [9, 11]]',
    '二维数组索引与切片'
)

doc.add_heading('3.2 花式索引（Fancy Indexing）', level=2)
doc.add_paragraph('使用整数列表指定要取哪些行/列，可以跳过不需要的维度：')
add_code(doc,
    'arr = np.arange(1, 13).reshape(3, 4)\n'
    '# array([[1, 2, 3, 4],\n'
    '#        [5, 6, 7, 8],\n'
    '#        [9,10,11,12]])\n\n'
    '# 取第0行和第2行\n'
    'arr[[0, 2]]      → [[1,2,3,4], [9,10,11,12]]\n\n'
    '# 取第0行和第2行，且只取第1列和第3列\n'
    'arr[[0, 2]][:, [1, 3]]  → [[2, 4], [10, 12]]',
    '花式索引'
)

doc.add_heading('3.3 布尔索引', level=2)
doc.add_paragraph('用条件表达式筛选数据，是非常强大且常用的功能：')
add_code(doc,
    'arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])\n\n'
    '# 筛选大于3的元素\n'
    'mask = arr > 3           # 创建布尔数组\n'
    'print(mask)              # [False, False, True, False, True, True, False, True]\n'
    'print(arr[mask])         # [4, 5, 9, 6]\n\n'
    '# 链式条件：与(&) 或(|) 非(~)\n'
    'print(arr[(arr > 2) & (arr < 6)])   # [3, 4, 5] — 条件必须用括号\n'
    'print(arr[~((arr < 3) | (arr > 6))]) # [3, 4, 5, 6]',
    '布尔索引'
)
add_warn(doc, '组合条件时用 & | ~（按位运算符），不是 and/or/not（逻辑运算符）。每个条件必须用括号包裹！')

doc.add_page_break()

doc.add_heading('四、NumPy 数组操作', level=1)

doc.add_heading('4.1 形状变换', level=2)
add_code(doc,
    'arr = np.arange(12)\n\n'
    '# reshape：改变形状（元素总数必须一致）\n'
    'arr.reshape(3, 4)        # (3,4) 3行4列\n'
    'arr.reshape(2, -1)       # -1 表示自动计算 → (2,6)\n\n'
    '# flatten / ravel：展平为一维\n'
    'arr_2d = np.array([[1,2],[3,4]])\n'
    'arr_2d.flatten()         # [1,2,3,4] — 返回副本\n'
    'arr_2d.ravel()           # [1,2,3,4] — 尽量返回视图\n\n'
    '# T / transpose：转置\n'
    'arr_2d.T                  # [[1,3],[2,4]]\n\n'
    '# 增加维度\n'
    'a = np.array([1,2,3])\n'
    'a[:, np.newaxis]         # 变为列向量 (3,1)',
    '形状变换'
)

doc.add_heading('4.2 数组拼接与分割', level=2)
add_code(doc,
    'a = np.array([[1,2],[3,4]])\n'
    'b = np.array([[5,6],[7,8]])\n\n'
    '# 拼接 — 水平方向（按列拼）\n'
    'np.hstack([a, b])         # [[1,2,5,6],[3,4,7,8]]\n'
    'np.concatenate([a, b], axis=1)  # 等价写法\n\n'
    '# 拼接 — 垂直方向（按行拼）\n'
    'np.vstack([a, b])         # [[1,2],[3,4],[5,6],[7,8]]\n'
    'np.concatenate([a, b], axis=0)  # 等价写法\n\n'
    '# 分割\n'
    'arr = np.arange(1, 13).reshape(3, 4)\n'
    'np.split(arr, 3, axis=0)  # 按行均分为3份\n'
    'np.hsplit(arr, 2)          # 按列均分为2份',
    '数组拼接与分割'
)

doc.add_page_break()

doc.add_heading('五、NumPy 数学运算', level=1)

doc.add_heading('5.1 向量化运算', level=2)
doc.add_paragraph('NumPy 的最大优势是"向量化"：对整个数组进行批量运算，无需写循环，速度提升数十到数百倍。')
add_code(doc,
    'a = np.array([1, 2, 3])\n'
    'b = np.array([4, 5, 6])\n\n'
    '# 逐元素运算（element-wise）\n'
    'a + b        → [5, 7, 9]\n'
    'a * b        → [4, 10, 18]   # 不是矩阵乘法！\n'
    'a ** 2       → [1, 4, 9]\n'
    'a + 10       → [11, 12, 13]  # 标量广播\n'
    'np.sqrt(a)   → [1.0, 1.414, 1.732]',
    '向量化运算'
)

doc.add_heading('5.2 常用数学函数', level=2)
add_table(doc,
    ['函数', '作用', '示例'],
    [
        ['np.sum(arr)', '求和', 'np.sum([1,2,3]) → 6'],
        ['np.mean(arr)', '均值', 'np.mean([1,2,3]) → 2.0'],
        ['np.std(arr)', '标准差', ''],
        ['np.min(arr) / np.max(arr)', '最小/最大值', ''],
        ['np.argmin(arr) / np.argmax(arr)', '最小/最大值的索引', ''],
        ['np.cumsum(arr)', '累积和', 'np.cumsum([1,2,3]) → [1,3,6]'],
        ['np.percentile(arr, q)', '百分位数', 'np.percentile(arr, 50) → 中位数'],
        ['np.abs(arr)', '绝对值', ''],
        ['np.round(arr, n)', '四舍五入到n位', ''],
    ]
)
add_code(doc,
    '# 按轴（axis）计算\n'
    'arr = np.array([[1, 2, 3],\n'
    '                [4, 5, 6]])\n\n'
    'np.sum(arr, axis=0)  → [5, 7, 9]   # 按列求和（沿行方向）\n'
    'np.sum(arr, axis=1)  → [6, 15]      # 按行求和（沿列方向）\n\n'
    '# 记忆口诀：axis=0 是"压扁行"，axis=1 是"压扁列"',
    'axis 参数理解'
)

doc.add_heading('5.3 矩阵运算', level=2)
add_code(doc,
    'A = np.array([[1, 2],\n'
    '              [3, 4]])\n'
    'B = np.array([[5, 6],\n'
    '              [7, 8]])\n\n'
    '# 矩阵乘法（不是逐元素相乘！）\n'
    'A @ B          → [[19, 22], [43, 50]]  # Python 3.5+ 写法\n'
    'np.dot(A, B)   → [[19, 22], [43, 50]]  # 等价写法\n'
    'np.matmul(A, B)→ [[19, 22], [43, 50]]  # 等价写法\n\n'
    '# ⚠️ A * B 是逐元素相乘，不是矩阵乘法！\n\n'
    '# 矩阵求逆\n'
    'A_inv = np.linalg.inv(A)\n\n'
    '# 特征值与特征向量\n'
    'eigenvalues, eigenvectors = np.linalg.eig(A)\n\n'
    '# 奇异值分解 SVD\n'
    'U, S, Vh = np.linalg.svd(A)',
    '矩阵运算'
)
add_warn(doc, 'A * B 是逐元素乘法！想做矩阵乘法请用 A @ B 或 np.dot(A, B)。这是新手最常见的错误之一。')

doc.add_page_break()

doc.add_heading('六、广播机制（Broadcasting）', level=1)
doc.add_paragraph('广播是 NumPy 对形状不同的数组进行运算时的自动扩展机制。它让代码更简洁、运行更快，但要理解其规则。')

doc.add_heading('广播规则', level=2)
doc.add_paragraph('从后往前比较两个数组的每个维度：')
doc.add_paragraph('① 如果两个维度大小相等 → 兼容')
doc.add_paragraph('② 如果其中一个维度大小为 1 → 广播为另一者的大小')
doc.add_paragraph('③ 如果两者都不相等且都不为 1 → 报错')

add_code(doc,
    'a = np.array([[1, 2, 3],\n'
    '              [4, 5, 6]])     # shape: (2, 3)\n\n'
    '# 示例1：标量与数组\n'
    'a + 10            # 标量 shape: () → 广播为 (2,3)\n\n'
    '# 示例2：行向量与矩阵\n'
    'b = np.array([10, 20, 30])    # shape: (3,) → 广播为 (1,3) → (2,3)\n'
    'a + b            → [[11,22,33], [14,25,36]]\n\n'
    '# 示例3：列向量与矩阵\n'
    'c = np.array([[10], [20]])    # shape: (2,1) → 广播为 (2,3)\n'
    'a + c            → [[11,12,13], [24,25,26]]\n\n'
    '# 示例4：不兼容的形状 ❌\n'
    '# d = np.array([1, 2])  # shape: (2,) — 与 (2,3) 不兼容，报错！',
    '广播机制详解'
)
add_tip(doc, '广播时 NumPy 并不会真的复制数据，只是在计算时"假装"扩展了。所以广播不浪费内存，非常高效。')

doc.add_page_break()

doc.add_heading('七、NumPy 随机数', level=1)
add_code(doc,
    'import numpy as np\n\n'
    '# 设定随机种子（保证结果可复现！）\n'
    'np.random.seed(42)\n\n'
    '# rand：均匀分布 [0, 1)\n'
    'arr = np.random.rand(3, 4)     # (3,4) 的 [0,1) 随机数组\n\n'
    '# randint：随机整数 [low, high)\n'
    'arr = np.random.randint(0, 10, size=(3, 4))  # 0~9的整数\n\n'
    '# randn：标准正态分布（均值0，标准差1）\n'
    'arr = np.random.randn(3, 4)    # 正态分布随机数\n\n'
    '# normal：自定义正态分布\n'
    'arr = np.random.normal(loc=70, scale=10, size=100)  # 均值70分，标准差10\n\n'
    '# uniform：均匀分布\n'
    'arr = np.random.uniform(-1, 5, size=(3, 4))  # [-1, 5) 均匀分布\n\n'
    '# choice：从给定数组中随机选择\n'
    'items = ["原神", "星铁", "绝区零"]\n'
    'np.random.choice(items, size=5)  # 随机选5次',
    'NumPy 随机数生成'
)
add_warn(doc, '随机数种子 np.random.seed(42) 对于实验可复现性非常重要！训练模型时一定要设置。')

doc.add_page_break()

doc.add_heading('八、实战：用 NumPy 实现梯度下降', level=1)
doc.add_paragraph('这是 Day 5 学习计划的重点实战任务。梯度下降是机器学习的核心优化算法，我们用 NumPy 来可视化它的工作过程。')
add_code(doc,
    'import numpy as np\n'
    'import matplotlib.pyplot as plt\n\n'
    '# 目标函数：f(x) = x² + 2x + 1（最小值为 x=-1, f(-1)=0）\n'
    'def f(x): return x**2 + 2*x + 1\n'
    'def df(x): return 2*x + 2  # 导数\n\n'
    '# 梯度下降参数\n'
    'x = 3.0              # 初始值\n'
    'lr = 0.1             # 学习率\n'
    'n_iter = 20          # 迭代次数\n'
    'history = [x]\n\n'
    'for i in range(n_iter):\n'
    '    grad = df(x)     # 计算梯度\n'
    '    x = x - lr * grad  # 更新参数（向梯度的反方向走）\n'
    '    history.append(x)\n'
    '    print(f"迭代{i+1:2d}: x={x:.4f}, f(x)={f(x):.6f}")\n\n'
    '# 输出示例：x 从 3.0 → -1.0 逐步收敛\n'
    '# 迭代 1: x=2.2000, f(x)=8.040000\n'
    '# 迭代 2: x=1.5600, f(x)=4.993600\n'
    '# ...\n'
    '# 迭代10: x=-0.8926, f(x)=0.011529\n'
    '# 迭代20: x=-0.9999, f(x)=0.000000  ← 接近最小值 -1',
    '梯度下降算法'
)

add_code(doc,
    '# 可视化梯度下降过程\n'
    'x_vals = np.linspace(-5, 5, 100)\n'
    'plt.figure(figsize=(10, 5))\n'
    'plt.plot(x_vals, f(x_vals), \'b-\', label=\'f(x)=x²+2x+1\')\n'
    'plt.plot(history, [f(x) for x in history], \'ro-\', markersize=4, label=\'梯度下降路径\')\n'
    'plt.axvline(x=-1, color=\'gray\', linestyle=\'--\', label=\'最优解 x=-1\')\n'
    'plt.xlabel(\'x\'); plt.ylabel(\'f(x)\')\n'
    'plt.legend(); plt.grid(alpha=0.3)\n'
    'plt.title(\'梯度下降可视化：寻找函数最小值\')\n'
    '# plt.show()  # 如果运行请取消注释',
    '可视化梯度下降'
)
add_tip(doc, '这是你接触的第一个机器学习相关算法！理解梯度下降对后续学习 PyTorch 和 ML 至关重要。')

doc.add_page_break()

# ========================
# PART 2: Pandas
# ========================
doc.add_heading('第二部分：Pandas 篇', level=1)

doc.add_heading('九、Pandas 简介', level=1)
doc.add_paragraph('Pandas 是 Python 中最强大的数据分析和处理库，基于 NumPy 构建。它提供了两个核心数据结构：')
doc.add_paragraph('• Series — 一维标注数组（类似带标签的列表）')
doc.add_paragraph('• DataFrame — 二维表格（类似 Excel 表格或 SQL 表）')
add_code(doc, 'pip install pandas\nimport pandas as pd  # 约定俗成的别名', '安装与导入')

doc.add_heading('十、Series 与 DataFrame', level=1)

doc.add_heading('10.1 Series', level=2)
add_code(doc,
    'import pandas as pd\n\n'
    '# 从列表创建（自动生成 0,1,2... 索引）\n'
    's1 = pd.Series([85, 92, 78, 90])\n\n'
    '# 从字典创建（键=索引，值=数据）\n'
    's2 = pd.Series({"语文": 85, "数学": 92, "英语": 78})\n\n'
    '# 自定义索引\n'
    's3 = pd.Series([85, 92, 78], index=["小明", "小红", "小刚"])\n\n'
    '# Series 属性\n'
    's3.index      # Index([\'小明\', \'小红\', \'小刚\'])\n'
    's3.values     # array([85, 92, 78])\n'
    's3.dtype      # int64',
    'Series 的创建与属性'
)

doc.add_heading('10.2 DataFrame 的创建', level=2)
add_code(doc,
    '# 最常用：从字典创建\n'
    'df = pd.DataFrame({\n'
    '    "姓名": ["小明", "小红", "小刚", "小丽"],\n'
    '    "年龄": [19, 20, 18, 19],\n'
    '    "分数": [85, 92, 78, 88],\n'
    '    "城市": ["上海", "北京", "广州", "上海"]\n'
    '})\n\n'
    '# 从列表套字典创建\n'
    'df2 = pd.DataFrame([\n'
    '    {"name": "小明", "score": 85},\n'
    '    {"name": "小红", "score": 92},\n'
    '])',
    'DataFrame 的创建'
)

doc.add_heading('10.3 DataFrame 常用属性', level=2)
add_table(doc,
    ['属性/方法', '含义', '示例'],
    [
        ['df.index', '行索引', 'RangeIndex(0, 4)'],
        ['df.columns', '列名', "Index(['姓名','年龄','分数','城市'])"],
        ['df.values', '数据（NumPy数组）', '二维数组'],
        ['df.dtypes', '每列的数据类型', ''],
        ['df.shape', '形状（行数, 列数）', '(4, 4)'],
        ['df.size', '元素总数', '16'],
        ['df.head(n)', '查看前 n 行', 'df.head(3)'],
        ['df.tail(n)', '查看后 n 行', 'df.tail(2)'],
        ['df.info()', '数据摘要（类型、非空值数）', ''],
        ['df.describe()', '数值列的统计摘要', 'count/mean/std/min/max等'],
    ]
)

doc.add_page_break()

doc.add_heading('十一、数据读取与写入', level=1)
doc.add_paragraph('Pandas 支持读取和写入多种文件格式，是数据处理的"瑞士军刀"。')
add_code(doc,
    '# 读取\n'
    'df_csv = pd.read_csv("data.csv", encoding="utf-8")\n'
    'df_excel = pd.read_excel("data.xlsx", sheet_name="Sheet1")\n'
    'df_json = pd.read_json("data.json")\n\n'
    '# 常用参数\n'
    '# pd.read_csv("file.csv",\n'
    '#     usecols=["姓名", "分数"],      # 只读指定列\n'
    '#     nrows=100,                     # 只读前100行\n'
    '#     dtype={"分数": float},          # 指定数据类型\n'
    '#     na_values=["-", "N/A"])        # 将这些值识别为NaN\n\n'
    '# 写入\n'
    'df.to_csv("output.csv", index=False, encoding="utf-8-sig")  # 不保存行索引\n'
    'df.to_excel("output.xlsx", index=False)\n'
    'df.to_json("output.json", orient="records", force_ascii=False)',
    '数据读写'
)
add_tip(doc, '写入 CSV 时用 index=False 避免多出一列不必要的索引列；encoding="utf-8-sig" 让 Excel 能正确显示中文。')

doc.add_heading('十二、数据选择与过滤', level=1)

doc.add_heading('12.1 选择列', level=2)
add_code(doc,
    '# 选择单列 → 返回 Series\n'
    'df["语文"]             # 或 df.语文（列名不含空格时可用）\n\n'
    '# 选择多列 → 返回 DataFrame\n'
    'df[["姓名", "语文", "数学"]]  # 注意：双层括号！外层是索引，内层是列表',
    '列选择'
)

doc.add_heading('12.2 选择行', level=2)
add_code(doc,
    '# iloc：按位置索引（Integer LOCation）\n'
    'df.iloc[0]            # 第1行 → Series\n'
    'df.iloc[0:3]          # 第1~3行 → DataFrame\n'
    'df.iloc[0, 2]         # 第1行第3列的值\n'
    'df.iloc[:3, [0, 2]]   # 前3行，第0、2列\n\n'
    '# loc：按标签索引（Label LOCation）\n'
    'df.loc[0]             # 标签为0的行（默认标签=位置）\n'
    'df.loc[:, "姓名"]      # 所有行，"姓名"列\n'
    'df.loc[df["分数"]>80, ["姓名", "分数"]]  # 分数>80的行，只看姓名和分数字段',
    'iloc 与 loc'
)
add_warn(doc, 'iloc 是左闭右开（[0:3] 取 0,1,2），loc 是左闭右闭（[0:3] 取 0,1,2,3）。这点非常容易混淆！')

doc.add_heading('12.3 条件过滤', level=2)
add_code(doc,
    '# 单条件过滤\n'
    'df[df["分数"] >= 85]   # 分数 >= 85 的行\n\n'
    '# 多条件过滤（用 & | ~，每个条件加括号！）\n'
    'df[(df["分数"] >= 80) & (df["城市"] == "上海")]  # 且\n'
    'df[(df["分数"] < 80) | (df["年龄"] < 19)]        # 或\n'
    'df[~(df["城市"] == "北京")]                       # 非\n\n'
    '# isin：判断值是否在列表中\n'
    'df[df["城市"].isin(["上海", "北京"])]  # 城市是上海或北京\n\n'
    '# query：用字符串写条件（可读性强）\n'
    'df.query("分数 >= 80 and 城市 == \'上海\'")',
    '条件过滤'
)

doc.add_page_break()

doc.add_heading('十三、数据清洗', level=1)
doc.add_paragraph('数据清洗是数据分析中最费时但也最重要的环节。"Garbage in, garbage out"。')

doc.add_heading('（1）缺失值处理', level=3)
add_code(doc,
    '# 检测缺失值\n'
    'df.isnull()          # 返回布尔 DataFrame，True 表示缺失\n'
    'df.isnull().sum()    # 每列缺失值统计\n\n'
    '# 处理缺失值\n'
    'df.dropna()                    # 删除含缺失值的行\n'
    'df.dropna(subset=["分数"])     # 只关注"分数"列\n'
    'df.fillna(0)                   # 用 0 填充\n'
    'df.fillna(df["分数"].mean())    # 用均值填充\n'
    'df.fillna(method="ffill")      # 用前一行的值填充（向前填充）\n'
    'df.fillna(method="bfill")      # 用后一行的值填充（向后填充）',
    '缺失值处理'
)

doc.add_heading('（2）重复值处理', level=3)
add_code(doc,
    '# 检测重复\n'
    'df.duplicated()            # 返回布尔 Series\n'
    'df.duplicated().sum()      # 重复行数\n\n'
    '# 删除重复\n'
    'df.drop_duplicates()                    # 完全重复的行\n'
    'df.drop_duplicates(subset=["姓名"])     # 指定列去重\n'
    'df.drop_duplicates(keep="first")        # 保留第一个（默认）',
    '重复值处理'
)

doc.add_heading('（3）数据转换', level=3)
add_code(doc,
    '# 类型转换\n'
    'df["年龄"] = df["年龄"].astype(int)\n\n'
    '# 字符串处理（通过 .str 访问器）\n'
    'df["姓名"].str.strip()           # 去除首尾空格\n'
    'df["日期"].str.replace("/", "-")  # 替换字符\n'
    'df["姓名"].str.upper()            # 转大写\n\n'
    '# 数值处理\n'
    'df["分数"] = df["分数"].abs()     # 取绝对值（防止负分）\n'
    'df["分数"].clip(0, 100)           # 限制在 [0, 100] 区间',
    '数据转换'
)

doc.add_page_break()

doc.add_heading('十四、数据排序与分组', level=1)

doc.add_heading('14.1 排序', level=2)
add_code(doc,
    '# sort_values：按值排序\n'
    'df.sort_values("分数", ascending=False)      # 降序\n'
    'df.sort_values("分数", ascending=True)        # 升序（默认）\n\n'
    '# 多列排序\n'
    'df.sort_values(["城市", "分数"], ascending=[True, False])\n'
    '# 先按城市升序，同城市内按分数降序\n\n'
    '# sort_index：按索引排序\n'
    'df.sort_index()',
    '排序'
)

doc.add_heading('14.2 分组聚合 groupby', level=2)
doc.add_paragraph('groupby 是 Pandas 中最强大的功能之一，类似 SQL 的 GROUP BY：按某列分组，然后对每组进行聚合计算。')
add_code(doc,
    '# 基本用法：分组 → 聚合\n'
    '# 按城市分组，计算每组分数的平均值\n'
    'df.groupby("城市")["分数"].mean()\n\n'
    '# 一次计算多个聚合\n'
    'df.groupby("城市")["分数"].agg(["mean", "max", "min", "count", "std"])\n\n'
    '# 对不同列使用不同聚合\n'
    'df.groupby("城市").agg({\n'
    '    "分数": ["mean", "max"],\n'
    '    "年龄": "count"\n'
    '})\n\n'
    '# 自定义聚合函数\n'
    'def range_func(x):\n'
    '    return x.max() - x.min()\n'
    'df.groupby("城市")["分数"].agg(range_func)',
    'groupby 分组聚合'
)

doc.add_page_break()

doc.add_heading('十五、数据合并：merge / join / concat', level=1)
add_code(doc,
    '# concat：沿轴拼接（堆叠）\n'
    'pd.concat([df1, df2], axis=0)   # 按行拼接（上下堆）\n'
    'pd.concat([df1, df2], axis=1)   # 按列拼接（左右拼）\n\n'
    '# merge：类似 SQL JOIN，按共同列合并\n'
    'students = pd.DataFrame({"学号": [1,2,3], "姓名": ["A","B","C"]})\n'
    'scores = pd.DataFrame({"学号": [1,2,3], "分数": [85,92,78]})\n\n'
    'pd.merge(students, scores, on="学号")  # 内连接（默认）\n'
    'pd.merge(students, scores, on="学号", how="left")   # 左连接\n'
    'pd.merge(students, scores, on="学号", how="right")  # 右连接\n'
    'pd.merge(students, scores, on="学号", how="outer")  # 全外连接',
    '数据合并'
)
add_tip(doc, 'merge 的 how 参数：inner(取交集，默认) / left(保留左表所有行) / right / outer(保留所有行)。')

doc.add_heading('十六、数据变换：apply / map', level=1)
add_code(doc,
    '# apply：对行或列应用函数\n'
    'df["分数等级"] = df["分数"].apply(lambda x: "优秀" if x >= 90 else "良好" if x >= 80 else "及格")\n\n'
    '# apply 到整行\n'
    'df["总分"] = df[["语文", "数学", "英语"]].apply(sum, axis=1)  # 每行求和\n\n'
    '# map：字典映射替换\n'
    'city_map = {"上海": "SH", "北京": "BJ", "广州": "GZ"}\n'
    'df["城市代码"] = df["城市"].map(city_map)\n\n'
    '# applymap：对 DataFrame 中每个元素应用函数\n'
    'df.select_dtypes(include="number").applymap(lambda x: f"{x:.1f}")',
    'apply / map / applymap'
)

doc.add_page_break()

doc.add_heading('十七、Pandas 数据可视化入门', level=1)
add_code(doc,
    '# Pandas 内置绘图（底层是 Matplotlib）\n'
    '# 折线图\n'
    'df.plot(x="日期", y="分数", kind="line")\n\n'
    '# 柱状图\n'
    'df.groupby("城市")["分数"].mean().plot(kind="bar")\n'
    'df.groupby("城市")["分数"].mean().plot(kind="barh")  # 水平柱状图\n\n'
    '# 饼图\n'
    'df["城市"].value_counts().plot(kind="pie", autopct="%1.1f%%")\n\n'
    '# 直方图\n'
    'df["分数"].plot(kind="hist", bins=10)\n\n'
    '# 散点图\n'
    'df.plot(kind="scatter", x="年龄", y="分数")',
    'Pandas 内置可视化'
)

doc.add_heading('十八、Matplotlib 基础绘图', level=1)
doc.add_paragraph('Matplotlib 是 Python 最基础的绘图库，Pandas 的绘图功能底层也是调用它。')
add_code(doc,
    'import matplotlib.pyplot as plt\n\n'
    '# 设置中文字体（重要！否则中文显示为方框）\n'
    'plt.rcParams["font.sans-serif"] = ["SimHei"]  # 使用黑体\n'
    'plt.rcParams["axes.unicode_minus"] = False    # 解决负号显示问题\n\n'
    '# 折线图\n'
    'x = [1, 2, 3, 4, 5]\n'
    'y = [2, 4, 6, 8, 10]\n'
    'plt.plot(x, y, "bo-", label="y=2x", markersize=5)\n'
    'plt.xlabel("x轴"); plt.ylabel("y轴")\n'
    'plt.title("示例折线图"); plt.legend(); plt.grid(alpha=0.3)\n'
    '# plt.show()\n\n'
    '# 柱状图\n'
    'names = ["小明", "小红", "小刚"]\n'
    'scores = [85, 92, 78]\n'
    'plt.bar(names, scores, color=["#3498db", "#e74c3c", "#2ecc71"])\n'
    'plt.ylabel("分数"); plt.title("学生成绩")\n'
    '# plt.show()\n\n'
    '# 散点图\n'
    'plt.scatter(x, y, c="red", alpha=0.5, s=50)  # s=点的大小，alpha=透明度',
    'Matplotlib 基础绘图'
)

doc.add_page_break()

doc.add_heading('十九、综合实战：分析游戏数据', level=1)
doc.add_paragraph('这是 Day 5 的重点任务。下面用 Pandas 分析模拟的游戏玩家登录数据。')

add_code(doc,
    'import pandas as pd\n'
    'import numpy as np\n\n'
    '# 1. 生成模拟数据\n'
    'np.random.seed(42)\n'
    'n = 500  # 500条记录\n\n'
    'df = pd.DataFrame({\n'
    '    "玩家ID": range(1001, 1001 + n),\n'
    '    "日期": np.random.choice(pd.date_range("2026-08-01", "2026-08-09"), n),\n'
    '    "游戏": np.random.choice(["原神", "星穹铁道", "绝区零"], n, p=[0.4, 0.35, 0.25]),\n'
    '    "登录时长(分钟)": np.random.normal(45, 20, n).clip(1, 120).astype(int),\n'
    '    "等级": np.random.randint(1, 61, n),\n'
    '    "是否付费": np.random.choice([True, False], n, p=[0.3, 0.7]),\n'
    '})\n\n'
    '# 2. 数据概览\n'
    'print(df.head(10))\n'
    'print(df.describe())\n'
    'print(df.info())\n\n'
    '# 3. 按游戏分析\n'
    '# 各游戏的平均登录时长\n'
    'print(df.groupby("游戏")["登录时长(分钟)"].mean())\n\n'
    '# 各游戏的付费率\n'
    'pay_rate = df.groupby("游戏")["是否付费"].mean() * 100\n'
    'print(pay_rate)\n\n'
    '# 4. 等级分布分析\n'
    '# 将等级分段\n'
    'bins = [0, 10, 20, 30, 40, 50, 60]\n'
    'labels = ["1-10", "11-20", "21-30", "31-40", "41-50", "51-60"]\n'
    'df["等级段"] = pd.cut(df["等级"], bins=bins, labels=labels)\n'
    'print(df.groupby("等级段").size())  # 各等级段人数\n\n'
    '# 5. 各游戏每日登录人数趋势\n'
    'daily = df.groupby(["日期", "游戏"]).size().unstack(fill_value=0)\n'
    'print(daily)\n\n'
    '# 6. 找出高质量玩家（登录时长>60分钟且已付费）\n'
    'vip = df[(df["登录时长(分钟)"] > 60) & (df["是否付费"])]\n'
    'print(f"核心玩家数：{len(vip)}，占比：{len(vip)/len(df)*100:.1f}%")\n\n'
    '# 7. 可视化\n'
    'import matplotlib.pyplot as plt\n'
    'plt.rcParams["font.sans-serif"] = ["SimHei"]\n'
    'plt.rcParams["axes.unicode_minus"] = False\n\n'
    'fig, axes = plt.subplots(2, 2, figsize=(12, 10))\n\n'
    '# 子图1：各游戏平均登录时长\n'
    'df.groupby("游戏")["登录时长(分钟)"].mean().plot(kind="bar", ax=axes[0,0], color=["#3498db","#e74c3c","#2ecc71"])\n'
    'axes[0,0].set_title("各游戏平均登录时长"); axes[0,0].set_ylabel("分钟")\n\n'
    '# 子图2：等级段分布\n'
    'df["等级段"].value_counts().sort_index().plot(kind="bar", ax=axes[0,1])\n'
    'axes[0,1].set_title("玩家等级分布")\n\n'
    '# 子图3：每日登录人数\n'
    'daily.plot(ax=axes[1,0], marker="o")\n'
    'axes[1,0].set_title("每日登录人数趋势"); axes[1,0].set_xlabel("日期"); axes[1,0].grid(alpha=0.3)\n\n'
    '# 子图4：登录时长直方图\n'
    'df["登录时长(分钟)"].plot(kind="hist", bins=20, ax=axes[1,1], edgecolor="black")\n'
    'axes[1,1].set_title("登录时长分布"); axes[1,1].set_xlabel("分钟")\n\n'
    'plt.tight_layout()\n'
    '# plt.show()  # 取消注释以显示图表',
    '游戏数据分析完整示例'
)

add_tip(doc, '这个综合示例涵盖了 Pandas 的核心操作：创建数据→数据概览→分组统计→条件筛选→数据分段→可视化。是面试和实际工作中最常见的分析流程。')

doc.add_page_break()

# ===== 二十、检查清单 =====
doc.add_heading('二十、本日学习检查清单 ✅', level=1)
doc.add_paragraph('□ NumPy 篇：')
doc.add_paragraph('  □ 能用 np.array() / arange() / zeros() / ones() 创建数组')
doc.add_paragraph('  □ 理解 ndarray 的 ndim / shape / size / dtype 属性')
doc.add_paragraph('  □ 能对二维数组进行索引和切片操作')
doc.add_paragraph('  □ 会使用布尔索引和花式索引筛选数据')
doc.add_paragraph('  □ 掌握 reshape / flatten / transpose 等形状变换')
doc.add_paragraph('  □ 会用 hstack / vstack / concatenate 拼接数组')
doc.add_paragraph('  □ 理解向量化运算的优势（无需循环）')
doc.add_paragraph('  □ 掌握常用数学函数：sum, mean, std, min, max, argmax')
doc.add_paragraph('  □ 会用 @ 或 np.dot() 进行矩阵乘法')
doc.add_paragraph('  □ 理解广播机制的规则（从后往前对齐，1可以扩展）')
doc.add_paragraph('  □ 会用 np.random 生成均匀/正态分布的随机数')
doc.add_paragraph('  □ 会用 np.random.seed() 固定随机种子')
doc.add_paragraph('  □ 能用 NumPy 实现简单的梯度下降并可视化')
doc.add_paragraph('□ Pandas 篇：')
doc.add_paragraph('  □ 能创建 Series 和 DataFrame')
doc.add_paragraph('  □ 理解 df.index / columns / values / shape / dtypes 属性')
doc.add_paragraph('  □ 会用 head() / tail() / info() / describe() 浏览数据')
doc.add_paragraph('  □ 能用 pd.read_csv() 读取数据文件')
doc.add_paragraph('  □ 能区分并正确使用 df.iloc（按位置）和 df.loc（按标签）')
doc.add_paragraph('  □ 会写条件表达式过滤数据（& | ~）')
doc.add_paragraph('  □ 掌握缺失值处理：isnull / dropna / fillna')
doc.add_paragraph('  □ 掌握重复值处理：duplicated / drop_duplicates')
doc.add_paragraph('  □ 会用 sort_values 进行单列和多列排序')
doc.add_paragraph('  □ 理解 groupby 分组聚合（mean / sum / count / agg）')
doc.add_paragraph('  □ 会使用 merge / concat 合并数据')
doc.add_paragraph('  □ 理解 apply / map 的使用场景')
doc.add_paragraph('  □ 会用 Pandas 内置 plot 进行简单可视化')
doc.add_paragraph('  □ 会用 Matplotlib 绘制折线图、柱状图、散点图')
doc.add_paragraph('  □ 完成游戏数据分析综合实战')

output_path = r'D:\NoteBook\Day5_学习笔记_NumPy与Pandas实战.docx'
doc.save(output_path)
print(f"Day 5 saved: {output_path}")

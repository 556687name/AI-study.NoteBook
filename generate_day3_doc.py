#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成Day3学习笔记Word文档：函数与模块化编程"""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

style = doc.styles['Normal']
style.font.name = '微软雅黑'
style.font.size = Pt(11)
style.paragraph_format.line_spacing = 1.5
style.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

for i in range(1, 4):
    hs = doc.styles[f'Heading {i}']
    hs.font.name = '微软雅黑'
    hs.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    if i == 1: hs.font.size = Pt(18); hs.font.color.rgb = RGBColor(0x1A,0x56,0xDB)
    elif i == 2: hs.font.size = Pt(15); hs.font.color.rgb = RGBColor(0x2C,0x3E,0x50)
    elif i == 3: hs.font.size = Pt(13); hs.font.color.rgb = RGBColor(0x34,0x49,0x5E)

def add_code(doc, code, caption=""):
    if caption:
        p = doc.add_paragraph()
        r = p.add_run(f"📌 {caption}"); r.bold = True; r.font.size = Pt(10); r.font.color.rgb = RGBColor(0x66,0x66,0x66)
    p = doc.add_paragraph()
    r = p.add_run(code)
    r.font.name = 'Consolas'; r.font.size = Pt(9.5); r.font.color.rgb = RGBColor(0x2D,0x2D,0x2D)
    shd = OxmlElement('w:shd'); shd.set(qn('w:fill'), 'F5F5F5'); shd.set(qn('w:val'), 'clear')
    p.paragraph_format.element.get_or_add_pPr().append(shd)
    p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2)

def add_tip(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(f"💡 提示：{text}"); r.font.size = Pt(10); r.font.color.rgb = RGBColor(0xE6,0x7E,0x22); r.italic = True

def add_warn(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(f"⚠️ 注意：{text}"); r.font.size = Pt(10); r.font.color.rgb = RGBColor(0xE7,0x4C,0x3C); r.bold = True

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
r = p.add_run("Day 3：函数与模块化编程"); r.font.size = Pt(20); r.font.color.rgb = RGBColor(0x2C,0x3E,0x50)

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_before = Pt(30)
r = p.add_run("日期：2026年8月7日（周四）  |  学习时长：约6-7小时  |  阶段：Python基础")
r.font.size = Pt(11); r.font.color.rgb = RGBColor(0x7F,0x8C,0x8D)

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("学习目标：掌握函数定义与参数类型，理解作用域与闭包，学会模块/包的使用，熟悉常用标准库")
r.font.size = Pt(10); r.font.italic = True

doc.add_page_break()

doc.add_heading('📑 目录', level=1)
toc = [
    "一、函数基础", "  1.1 函数的定义与调用", "  1.2 return 与 print 的区别",
    "  1.3 文档字符串（docstring）", "  1.4 类型提示（Type Hints）",
    "二、函数参数详解", "  2.1 必备参数", "  2.2 默认参数", "  2.3 可变参数 *args",
    "  2.4 关键字参数 **kwargs", "  2.5 参数传递顺序规则",
    "三、作用域与变量", "  3.1 局部变量与全局变量", "  3.2 global 关键字",
    "  3.3 nonlocal 关键字", "  3.4 LEGB 规则",
    "四、高阶函数与匿名函数", "  4.1 lambda 匿名函数", "  4.2 map / filter / reduce",
    "  4.3 闭包（Closure）",
    "五、递归函数", "六、装饰器入门", "七、生成器与迭代器",
    "  7.1 迭代器概念", "  7.2 生成器与 yield",
    "八、拆包（Unpacking）", "九、模块与包",
    "  9.1 模块的导入与使用", "  9.2 __name__ 变量", "  9.3 包 Package",
    "十、常用标准库详解", "  10.1 os", "  10.2 sys", "  10.3 pathlib",
    "  10.4 datetime", "  10.5 random", "  10.6 collections",
    "十一、第三方库：requests 与 JSON", "十二、综合练习", "十三、本日学习检查清单",
]
for item in toc:
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(1); p.paragraph_format.space_after = Pt(1)
    r = p.add_run(item); r.font.size = Pt(10)
    if not item.startswith("  "): r.bold = True

doc.add_page_break()

# ===== 一、函数基础 =====
doc.add_heading('一、函数基础', level=1)
doc.add_paragraph('函数是一段可以重复使用的代码块。把常用的操作封装成函数，可以大大提高代码的复用性和可维护性。')

doc.add_heading('1.1 函数的定义与调用', level=2)
add_code(doc,
    '# 定义格式：\n'
    '# def 函数名(形参列表):\n'
    '#     """文档字符串（可选）"""\n'
    '#     函数体\n'
    '#     return 返回值（可选）\n\n'
    'def greet(name):\n'
    '    """向指定的人打招呼"""\n'
    '    return f"你好，{name}！"\n\n'
    '# 调用格式：\n'
    'result = greet("小明")\n'
    'print(result)  # 你好，小明！',
    '函数的定义与调用'
)
add_warn(doc, '定义时括号里的参数叫"形参"（形式参数），调用时传入的值叫"实参"（实际参数）。数量和顺序必须匹配（除默认参数外）。')

doc.add_heading('1.2 return 与 print 的区别', level=2)
add_table(doc,
    ['对比维度', 'return', 'print'],
    [
        ['本质', '返回一个值给调用者', '在屏幕上显示信息'],
        ['函数是否继续', 'return 后函数立即结束', 'print 后函数继续执行'],
        ['能否被赋值', '可以，result = func()', '不可以，result = print() 得到 None'],
        ['用途', '把计算结果交给其他代码使用', '给用户看信息 / 调试'],
    ]
)
add_code(doc,
    '# return 返回多个值时，自动打包为元组\n'
    'def get_min_max(nums):\n'
    '    return min(nums), max(nums)\n\n'
    'result = get_min_max([3, 1, 4, 1, 5])\n'
    'print(result)         # (1, 5) — 是一个元组！',
    'return 多个值'
)

doc.add_heading('1.3 文档字符串（docstring）', level=2)
doc.add_paragraph('函数的第一行字符串被称为 docstring，用于说明函数的功能。可以用 help() 或 .__doc__ 来查看。')
add_code(doc,
    'def calculate_bmi(weight, height):\n'
    '    """\n'
    '    计算身体质量指数 BMI\n'
    '    参数：weight — 体重（kg）\n'
    '          height — 身高（m）\n'
    '    返回：BMI 值（float）\n'
    '    """\n'
    '    return weight / (height ** 2)\n\n'
    'help(calculate_bmi)  # 查看文档\n'
    'print(calculate_bmi.__doc__)  # 等价方式',
    'docstring 文档字符串'
)
add_tip(doc, '养成写 docstring 的好习惯！这是专业程序员的基本素养，也是代码可维护性的关键。')

doc.add_heading('1.4 类型提示（Type Hints）', level=2)
doc.add_paragraph('Python 3.5+ 支持类型提示，让代码意图更清晰（但不会在运行时强制检查）：')
add_code(doc,
    'def calculate_bmi(weight: float, height: float) -> float:\n'
    '    """计算 BMI"""\n'
    '    return weight / (height ** 2)\n\n'
    'def get_top_students(scores: list[int], n: int = 3) -> list[int]:\n'
    '    """返回前 n 名成绩"""\n'
    '    return sorted(scores, reverse=True)[:n]\n\n'
    '# 类型提示只是"提示"，传错类型也不会报错\n'
    '# 但它让 IDE 能给出更好的自动补全和警告',
    '类型提示'
)

doc.add_page_break()

# ===== 二、函数参数详解 =====
doc.add_heading('二、函数参数详解', level=1)
doc.add_paragraph('Python 支持四种参数类型，且可以混合使用。理解它们的使用场景和顺序至关重要。')

doc.add_heading('2.1 必备参数（位置参数）', level=2)
doc.add_paragraph('调用时按位置顺序传递，数量和顺序必须完全匹配。')
add_code(doc, 'def add(a, b):\n    return a + b\n\nprint(add(3, 5))  # 8 — 3传给a, 5传给b\n# add(3)    ← 报错：参数数量不够\n# add(3,5,7) ← 报错：参数数量太多', '必备参数示例')

doc.add_heading('2.2 默认参数', level=2)
doc.add_paragraph('定义时给参数一个默认值，调用时可以不传该参数，使用默认值。')
add_code(doc,
    'def greet(name, greeting="你好"):\n'
    '    return f"{greeting}，{name}！"\n\n'
    'print(greet("小明"))           # 你好，小明！\n'
    'print(greet("Tom", "Hello"))   # Hello，Tom！',
    '默认参数示例'
)
add_warn(doc, '默认参数必须放在非默认参数后面！def f(a=1, b) 是错误的。所有调用时的位置参数必须放在默认参数之前。')
add_tip(doc, '默认参数的默认值只在定义时计算一次。不要把可变对象（如空列表 []）作为默认值！参考：def f(lst=None): if lst is None: lst = []')

doc.add_heading('2.3 可变参数 *args（接收位置参数）', level=2)
doc.add_paragraph('*args 可以接收任意数量的位置参数，在函数内部以元组形式使用。')
add_code(doc,
    'def sum_all(*args):\n'
    '    """求和任意多个数"""\n'
    '    print(f"收到了 {len(args)} 个参数：{args}")\n'
    '    return sum(args)\n\n'
    'print(sum_all(1, 2, 3))       # 3个参数 → 6\n'
    'print(sum_all(1, 2, 3, 4, 5)) # 5个参数 → 15\n'
    'print(sum_all())               # 0个参数 → 0',
    '*args 可变参数'
)

doc.add_heading('2.4 关键字参数 **kwargs（接收关键字参数）', level=2)
doc.add_paragraph('**kwargs 可以接收任意数量的"键=值"形式的参数，在函数内部以字典形式使用。')
add_code(doc,
    'def build_profile(**kwargs):\n'
    '    """构建用户信息"""\n'
    '    profile = {}\n'
    '    for key, value in kwargs.items():\n'
    '        profile[key] = value\n'
    '    return profile\n\n'
    'user = build_profile(name="小明", age=19, city="上海", hobby="编程")\n'
    'print(user)\n'
    '# {\'name\': \'小明\', \'age\': 19, \'city\': \'上海\', \'hobby\': \'编程\'}',
    '**kwargs 关键字参数'
)

doc.add_heading('2.5 参数传递顺序规则', level=2)
doc.add_paragraph('定义函数时，四种参数的顺序必须是（严格按此顺序）：')
add_code(doc,
    'def func(必备参数, 默认参数, *args, **kwargs):\n'
    '    pass\n\n'
    '# 具体示例：\n'
    'def student_info(name, age=18, *scores, **extra):\n'
    '    print(f"姓名：{name}，年龄：{age}")\n'
    '    print(f"成绩：{scores}")\n'
    '    print(f"其他信息：{extra}")\n\n'
    'student_info("小明", 20, 95, 87, 92, city="上海", hobby="编程")\n'
    '# 姓名：小明，年龄：20\n'
    '# 成绩：(95, 87, 92)\n'
    '# 其他信息：{\'city\': \'上海\', \'hobby\': \'编程\'}',
    '四种参数的完整组合'
)

doc.add_page_break()

# ===== 三、作用域 =====
doc.add_heading('三、作用域与变量', level=1)

doc.add_heading('3.1 局部变量与全局变量', level=2)
add_code(doc,
    'total = 100  # 全局变量 — 在整个文件中都可以访问\n\n'
    'def my_func():\n'
    '    local = 50  # 局部变量 — 只在函数内部有效\n'
    '    print(f"访问全局变量：{total}")\n'
    '    print(f"访问局部变量：{local}")\n\n'
    'my_func()\n'
    '# print(local)   ← 报错！局部变量在函数外无法访问\n'
    'print(total)      # 100 — 全局变量在函数外可以访问',
    '局部变量与全局变量'
)
add_warn(doc, '函数内如果定义了和全局变量同名的局部变量，会"遮蔽"全局变量。函数内优先使用局部变量。')

doc.add_heading('3.2 global 关键字', level=2)
doc.add_paragraph('如果需要在函数内部修改全局变量，必须先用 global 声明：')
add_code(doc,
    'count = 0\n\n'
    'def increment():\n'
    '    global count    # 声明要修改全局变量\n'
    '    count += 1\n\n'
    'increment()\n'
    'print(count)  # 1',
    'global 关键字'
)
add_warn(doc, 'global 声明和赋值必须分开写！不能写成 global count = 0。全局变量尽量少用，容易造成代码混乱。')

doc.add_heading('3.3 nonlocal 关键字', level=2)
doc.add_paragraph('在嵌套函数中，内层函数用 nonlocal 可以修改外层（非全局）的变量：')
add_code(doc,
    'def outer():\n'
    '    x = 10  # 外层函数的变量\n\n'
    '    def inner():\n'
    '        nonlocal x  # 声明要修改外层变量\n'
    '        x += 5\n'
    '        print(f"内层：{x}")\n\n'
    '    inner()\n'
    '    print(f"外层：{x}")\n\n'
    'outer()\n'
    '# 内层：15\n'
    '# 外层：15   ← 外层变量也被修改了！',
    'nonlocal 关键字'
)

doc.add_heading('3.4 LEGB 规则', level=2)
doc.add_paragraph('Python 查找变量时遵循 LEGB 顺序：')
doc.add_paragraph('L — Local：当前函数内部')
doc.add_paragraph('E — Enclosing：外层函数（嵌套函数的情况）')
doc.add_paragraph('G — Global：全局作用域（模块级别）')
doc.add_paragraph('B — Built-in：内置作用域（如 print、len 等内置函数）')

doc.add_page_break()

# ===== 四、高阶函数与匿名函数 =====
doc.add_heading('四、高阶函数与匿名函数', level=1)

doc.add_heading('4.1 lambda 匿名函数', level=2)
doc.add_paragraph('lambda 是一种快速定义简单函数的方式，适合只用一次的小函数。')
add_code(doc,
    '# 普通函数写法\n'
    'def add(a, b):\n'
    '    return a + b\n\n'
    '# lambda 等价写法\n'
    'add = lambda a, b: a + b\n\n'
    'print(add(3, 5))  # 8\n\n'
    '# 常见用法：作为 sorted/map/filter 等函数的参数\n'
    'students = [(\"小明\", 85), (\"小红\", 92), (\"小刚\", 78)]\n'
    'students.sort(key=lambda s: s[1])  # 按分数排序\n'
    'print(students)',
    'lambda 匿名函数'
)
add_tip(doc, 'lambda 只能写一个表达式，不能写复杂逻辑（不能用 if-elif-else 语句块，但可以用三元表达式）。保持简单！')

doc.add_heading('4.2 map / filter / reduce', level=2)
add_table(doc,
    ['函数', '作用', '示例', '结果'],
    [
        ['map(f, seq)', '对序列中每个元素应用函数f', 'map(str, [1,2,3])', "['1','2','3']"],
        ['filter(f, seq)', '过滤出函数f返回True的元素', 'filter(lambda x:x>2,[1,2,3])', '[3]'],
        ['reduce(f, seq)', '累积计算（需import functools）', 'reduce(lambda a,b:a+b,[1,2,3])', '6'],
    ]
)
add_code(doc,
    'from functools import reduce\n\n'
    '# map：每个元素平方\n'
    'nums = [1, 2, 3, 4, 5]\n'
    'squares = list(map(lambda x: x**2, nums))\n'
    'print(squares)  # [1, 4, 9, 16, 25]\n\n'
    '# filter：筛选偶数\n'
    'evens = list(filter(lambda x: x % 2 == 0, nums))\n'
    'print(evens)    # [2, 4]\n\n'
    '# reduce：累加\n'
    'total = reduce(lambda a, b: a + b, nums)\n'
    'print(total)    # 15',
    'map/filter/reduce 实战'
)

doc.add_heading('4.3 闭包（Closure）', level=2)
doc.add_paragraph('闭包 = 嵌套函数 + 内层函数使用外层变量 + 外层函数返回内层函数。它的作用是"记住"外层函数的状态。')
add_code(doc,
    'def make_multiplier(n):\n'
    '    """返回一个把输入乘以 n 的函数"""\n'
    '    def multiplier(x):\n'
    '        return x * n  # n 是外层函数的变量\n'
    '    return multiplier\n\n'
    'double = make_multiplier(2)   # n = 2\n'
    'triple = make_multiplier(3)   # n = 3\n\n'
    'print(double(5))  # 10 — "记住"了 n = 2\n'
    'print(triple(5))  # 15 — "记住"了 n = 3',
    '闭包示例'
)
add_tip(doc, '闭包的核心价值是：在多次调用中"记住"创建时的状态，而不需要全局变量。这是装饰器的基础。')

doc.add_page_break()

# ===== 五、递归 =====
doc.add_heading('五、递归函数', level=1)
doc.add_paragraph('递归是函数自己调用自己的编程技巧，适合处理树形结构、分治算法等场景。')
add_code(doc,
    '# 经典示例：计算阶乘\n'
    'def factorial(n: int) -> int:\n'
    '    """n! = n × (n-1) × ... × 1"""\n'
    '    if n <= 1:\n'
    '        return 1              # 基线条件（停止递归）\n'
    '    return n * factorial(n - 1)  # 递归条件\n\n'
    'print(factorial(5))  # 120\n\n'
    '# 递归必须有两个要素：\n'
    '# 1. 基线条件：何时停止（否则无限递归导致栈溢出）\n'
    '# 2. 递归条件：问题向基线条件缩小的方式',
    '递归：阶乘'
)
add_warn(doc, 'Python 默认递归深度限制为 1000 层。递归太深会触发 RecursionError。能用循环解决的问题建议用循环。')

doc.add_page_break()

# ===== 六、装饰器 =====
doc.add_heading('六、装饰器入门', level=1)
doc.add_paragraph('装饰器是 Python 中非常强大的语法糖，可以在不修改原函数的前提下给函数增加额外功能。')
add_code(doc,
    '# 装饰器本质：接受函数作为参数，返回一个新函数\n'
    'def timer(func):\n'
    '    """计算函数执行时间的装饰器"""\n'
    '    import time\n'
    '    def wrapper(*args, **kwargs):\n'
    '        start = time.time()\n'
    '        result = func(*args, **kwargs)\n'
    '        end = time.time()\n'
    '        print(f"{func.__name__} 耗时：{end - start:.4f}秒")\n'
    '        return result\n'
    '    return wrapper\n\n'
    '@timer  # 语法糖：等价于 slow_func = timer(slow_func)\n'
    'def slow_func():\n'
    '    total = sum(range(10000000))\n'
    '    return total\n\n'
    'slow_func()  # 自动打印耗时',
    '装饰器：计算函数耗时'
)
add_tip(doc, '@装饰器名 写在函数定义上方，就相当于 func = 装饰器(func)。装饰器是面试常考点。')

doc.add_page_break()

# ===== 七、生成器与迭代器 =====
doc.add_heading('七、生成器与迭代器', level=1)

doc.add_heading('7.1 迭代器概念', level=2)
doc.add_paragraph('迭代器是实现了 __iter__() 和 __next__() 方法的对象，可以用 for 循环遍历。')
add_code(doc,
    '# 用 iter() 和 next() 手动迭代\n'
    'nums = [1, 2, 3]\n'
    'it = iter(nums)          # 获取迭代器\n'
    'print(next(it))          # 1\n'
    'print(next(it))          # 2\n'
    'print(next(it))          # 3\n'
    '# print(next(it))        # StopIteration — 没有更多元素了',
    '手动使用迭代器'
)

doc.add_heading('7.2 生成器与 yield', level=2)
doc.add_paragraph('生成器是一种特殊的迭代器，用 yield 关键字逐个产生值，每次只生成一个值，大大节省内存。')
add_code(doc,
    '# 生成器函数：用 yield 替代 return\n'
    'def countdown(n):\n'
    '    """倒计时生成器"""\n'
    '    while n > 0:\n'
    '        yield n\n'
    '        n -= 1\n\n'
    'for num in countdown(5):\n'
    '    print(num, end=" ")  # 5 4 3 2 1\n\n'
    '# 生成器 vs 列表的区别\n'
    'big_list = [i for i in range(1000000)]   # 立即占用大量内存\n'
    'big_gen = (i for i in range(1000000))    # 生成器表达式，不占内存\n'
    '# 注意：生成器表达式用 () 而不是 []！',
    '生成器与 yield'
)
add_tip(doc, '处理大量数据时优先使用生成器（比如读一个 10GB 的文件，用生成器逐行读，内存只占几KB）。')

doc.add_page_break()

# ===== 八、拆包 =====
doc.add_heading('八、拆包（Unpacking）', level=1)
add_code(doc,
    '# 基本拆包\n'
    'a, b, c = [1, 2, 3]\n'
    'print(a, b, c)  # 1 2 3\n\n'
    '# 用 * 收集剩余元素\n'
    'first, *rest = [1, 2, 3, 4, 5]\n'
    'print(first)  # 1\n'
    'print(rest)   # [2, 3, 4, 5]\n\n'
    '# 多层拆包\n'
    'a, *b, c = [1, 2, 3, 4, 5]\n'
    'print(a, c)   # 1 5\n'
    'print(b)      # [2, 3, 4]\n\n'
    '# * 可以收集也可以展开\n'
    'nums1 = [1, 2, 3]\n'
    'nums2 = [*nums1, 4, 5]  # [1, 2, 3, 4, 5]\n'
    'combined = [*nums1, *nums2]  # 合并两个列表',
    '拆包与星号表达式'
)

doc.add_page_break()

# ===== 九、模块与包 =====
doc.add_heading('九、模块与包', level=1)
doc.add_paragraph('随着代码量增长，把所有代码放在一个文件里会变得难以维护。模块化编程可以让代码结构更清晰。')

doc.add_heading('9.1 模块的导入与使用', level=2)
add_table(doc,
    ['导入方式', '语法', '调用方式', '适用场景'],
    [
        ['导入整个模块', 'import math', 'math.sqrt(16)', '需要用到模块的多个功能'],
        ['导入特定功能', 'from math import sqrt', 'sqrt(16)', '只需要一两个功能'],
        ['导入全部功能', 'from math import *', 'sqrt(16)', '⚠️ 不推荐，会污染命名空间'],
        ['起别名', 'import numpy as np', 'np.array([1,2])', '简化常用模块的调用'],
        ['起别名（功能）', 'from math import sqrt as sq', 'sq(16)', '给功能起简短别名'],
    ]
)
add_warn(doc, 'from module import * 会把模块中所有公开名称导入当前命名空间，可能造成名称冲突，不推荐使用。')

doc.add_heading('9.2 __name__ == "__main__" 的意义', level=2)
doc.add_paragraph('这是一个非常重要的 Python 约定：__name__ 变量在文件直接运行时等于 "__main__"，在被导入时等于模块名。')
add_code(doc,
    '# 在 my_tools.py 文件中写：\n'
    'def helper():\n'
    '    return "I am helper"\n\n'
    'if __name__ == "__main__":\n'
    '    # 这部分代码只在直接运行 my_tools.py 时执行\n'
    '    # 当其他文件 import my_tools 时，这部分不会执行\n'
    '    print("测试模式：", helper())',
    '__name__ == "__main__"'
)
add_tip(doc, '每个模块文件都应该加上 if __name__ == "__main__" 来写测试代码。这样可以即当模块用，又能独立运行测试。')

doc.add_heading('9.3 包（Package）', level=2)
doc.add_paragraph('包是包含 __init__.py 文件的文件夹，用于组织多个相关模块。')
add_code(doc,
    '# 包的结构示例：\n'
    '# my_package/\n'
    '#   __init__.py       ← 必须有，可以为空\n'
    '#   module_a.py       ← from my_package import module_a\n'
    '#   module_b.py\n'
    '#   sub_package/\n'
    '#       __init__.py\n'
    '#       module_c.py\n\n'
    '# __init__.py 中可以写导入逻辑：\n'
    '# from .module_a import func_a\n'
    '# from .module_b import func_b\n\n'
    '# __all__ 列表控制 from package import * 的行为：\n'
    '# __all__ = ["func_a", "func_b"]',
    '包的结构'
)

doc.add_page_break()

# ===== 十、常用标准库 =====
doc.add_heading('十、常用标准库详解', level=1)
doc.add_paragraph('Python 的标准库非常丰富，被称为"电池已包含"。以下是学习计划重点要求的几个模块。')

doc.add_heading('10.1 os 模块 — 操作系统接口', level=2)
add_code(doc,
    'import os\n\n'
    '# 目录操作\n'
    'cwd = os.getcwd()           # 获取当前工作目录\n'
    'os.mkdir("new_folder")       # 创建目录（父目录必须存在）\n'
    'os.makedirs("a/b/c")         # 递归创建目录（自动创建父目录）\n'
    'items = os.listdir(".")      # 列出目录下的所有文件和文件夹\n\n'
    '# 路径操作\n'
    'path = os.path.join("folder", "file.txt")  # 拼接路径（跨平台！）\n'
    'exists = os.path.exists("file.txt")        # 判断路径是否存在\n'
    'is_file = os.path.isfile("file.txt")       # 判断是否是文件\n'
    'is_dir = os.path.isdir("folder")           # 判断是否是文件夹\n'
    'dirname = os.path.dirname("/a/b/c.txt")    # → /a/b\n'
    'basename = os.path.basename("/a/b/c.txt")  # → c.txt\n\n'
    '# 遍历目录树\n'
    'for root, dirs, files in os.walk("."):\n'
    '    print(f"文件夹：{root}，文件：{files}")',
    'os 模块常用操作'
)

doc.add_heading('10.2 sys 模块 — 系统相关', level=2)
add_code(doc,
    'import sys\n\n'
    'print(sys.version)          # Python 版本信息\n'
    'print(sys.path)             # 模块搜索路径列表\n'
    'print(sys.argv)             # 命令行参数列表\n\n'
    '# sys.exit()                # 立即终止程序\n'
    '# sys.stdin / sys.stdout    # 标准输入输出流',
    'sys 模块'
)

doc.add_heading('10.3 pathlib — 现代路径操作（推荐）', level=2)
add_code(doc,
    'from pathlib import Path\n\n'
    '# 创建 Path 对象\n'
    'p = Path("D:/NoteBook/study_plan.txt")\n\n'
    '# 常用操作\n'
    'print(p.exists())            # 文件是否存在\n'
    'print(p.is_file())           # 是否是文件\n'
    'print(p.suffix)              # 后缀 → .txt\n'
    'print(p.stem)                # 文件名（无后缀）→ study_plan\n'
    'print(p.parent)              # 父目录\n'
    'print(p.name)                # 完整文件名\n\n'
    '# 路径拼接（最优雅的方式）\n'
    'data_dir = Path("D:/NoteBook") / "data" / "raw"\n\n'
    '# 读写文件\n'
    'content = p.read_text(encoding="utf-8")  # 读取文本\n'
    'p.write_text("Hello", encoding="utf-8")  # 写入文本',
    'pathlib 模块（推荐替代 os.path）'
)
add_tip(doc, 'Python 3.6+ 使用 pathlib 替代 os.path。它的 API 更直观、更面向对象，是未来的标准。')

doc.add_heading('10.4 datetime 模块 — 日期时间处理', level=2)
add_code(doc,
    'from datetime import datetime, date, timedelta\n\n'
    '# 获取当前时间\n'
    'now = datetime.now()\n'
    'print(now)  # 2026-08-07 14:30:00.123456\n\n'
    '# 格式化输出 strftime\n'
    'print(now.strftime("%Y-%m-%d %H:%M:%S"))  # 2026-08-07 14:30:00\n\n'
    '# 解析字符串 strptime\n'
    'd = datetime.strptime("2026-08-07", "%Y-%m-%d")\n\n'
    '# 时间加减 timedelta\n'
    'tomorrow = now + timedelta(days=1)\n'
    'last_week = now - timedelta(weeks=1)\n'
    'three_hours_later = now + timedelta(hours=3)\n\n'
    '# 常用格式码：%Y=年 %m=月 %d=日 %H=时 %M=分 %S=秒',
    'datetime 模块'
)

doc.add_heading('10.5 random 模块 — 随机数', level=2)
add_code(doc,
    'import random\n\n'
    '# 设置随机种子（保证结果可复现，调试用）\n'
    'random.seed(42)\n\n'
    '# 生成随机数\n'
    'random.randint(1, 10)       # [1,10] 之间的随机整数\n'
    'random.uniform(0, 1)        # [0,1) 之间的随机浮点数\n'
    'random.random()             # [0,1) 之间的随机浮点数\n\n'
    '# 随机选择\n'
    'items = ["原神", "星铁", "绝区零", "崩坏3"]\n'
    'random.choice(items)        # 随机选一个\n'
    'random.sample(items, 2)     # 随机选2个（不重复）\n'
    'random.shuffle(items)       # 原地打乱顺序\n\n'
    '# 按正态分布生成随机数\n'
    'random.gauss(0, 1)          # 均值0，标准差1',
    'random 模块'
)

doc.add_heading('10.6 collections 模块 — 高级容器', level=2)
add_code(doc,
    'from collections import Counter, defaultdict, namedtuple\n\n'
    '# Counter：计数器\n'
    'words = ["a", "b", "a", "c", "b", "a"]\n'
    'cnt = Counter(words)\n'
    'print(cnt)                 # Counter({\'a\': 3, \'b\': 2, \'c\': 1})\n'
    'print(cnt.most_common(2))  # [(\'a\', 3), (\'b\', 2)]\n\n'
    '# defaultdict：带默认值的字典\n'
    '# 普通字典访问不存在的键会报错\n'
    'dd = defaultdict(int)      # 不存在时默认返回 0\n'
    'dd["a"] += 1               # 即使 "a" 不存在也不会报错\n'
    'print(dd["a"])             # 1\n\n'
    '# namedtuple：有名字的元组\n'
    'Point = namedtuple("Point", ["x", "y"])\n'
    'p = Point(10, 20)\n'
    'print(p.x, p.y)           # 10 20 — 可以用属性名访问',
    'collections 模块'
)

doc.add_page_break()

# ===== 十一、requests与JSON =====
doc.add_heading('十一、第三方库：requests 与 JSON', level=1)

doc.add_heading('11.1 pip 安装第三方库', level=2)
add_code(doc,
    '# 在终端中执行（不是在 Python 代码里！）\n'
    'pip install requests\n'
    'pip install requests==2.31.0  # 安装特定版本\n'
    'pip list                       # 查看已安装的包\n'
    'pip show requests              # 查看某个包的详细信息',
    'pip 命令'
)

doc.add_heading('11.2 requests 发送 HTTP 请求', level=2)
add_code(doc,
    'import requests\n\n'
    '# GET 请求：获取数据\n'
    'response = requests.get("https://api.github.com")\n'
    'print(response.status_code)  # 200 表示成功\n'
    'print(response.text[:200])   # 前200个字符\n\n'
    '# 带参数的请求\n'
    'params = {"q": "python", "sort": "stars"}\n'
    'resp = requests.get("https://api.github.com/search/repositories", params=params)\n\n'
    '# POST 请求：提交数据\n'
    'data = {"name": "小明", "age": 19}\n'
    'resp = requests.post("https://httpbin.org/post", data=data)',
    'requests 基本用法'
)

doc.add_heading('11.3 JSON 数据处理', level=2)
add_code(doc,
    'import json\n\n'
    '# Python 对象 → JSON 字符串（序列化）\n'
    'data = {"name": "小明", "age": 19, "scores": [95, 87, 92]}\n'
    'json_str = json.dumps(data, ensure_ascii=False, indent=2)\n'
    'print(json_str)\n'
    '# {\n'
    '#   "name": "小明",\n'
    '#   "age": 19,\n'
    '#   "scores": [95, 87, 92]\n'
    '# }\n\n'
    '# JSON 字符串 → Python 对象（反序列化）\n'
    'parsed = json.loads(json_str)\n'
    'print(parsed["name"])          # 小明\n\n'
    '# 处理 API 返回的 JSON\n'
    'resp = requests.get("https://api.github.com")\n'
    'data = resp.json()             # 直接解析为 Python 对象',
    'JSON 数据处理'
)
add_tip(doc, 'ensure_ascii=False 让中文正常显示而不是变成 \\uXXXX。indent 参数让 JSON 输出更美观。')

doc.add_page_break()

# ===== 十二、综合练习 =====
doc.add_heading('十二、综合练习', level=1)

doc.add_heading('练习 1：支持多种统计函数的工具模块', level=2)
doc.add_paragraph('编写一个 stats_utils.py 模块，包含求均值、中位数、方差、标准差的函数。')
add_code(doc,
    '# stats_utils.py\n'
    'def mean(nums):\n'
    '    """均值"""\n'
    '    return sum(nums) / len(nums) if nums else 0\n\n'
    'def median(nums):\n'
    '    """中位数"""\n'
    '    sorted_nums = sorted(nums)\n'
    '    n = len(sorted_nums)\n'
    '    mid = n // 2\n'
    '    if n % 2 == 0:\n'
    '        return (sorted_nums[mid-1] + sorted_nums[mid]) / 2\n'
    '    return sorted_nums[mid]\n\n'
    'def variance(nums):\n'
    '    """方差"""\n'
    '    m = mean(nums)\n'
    '    return sum((x - m)**2 for x in nums) / len(nums)\n\n'
    'def std_dev(nums):\n'
    '    """标准差"""\n'
    '    return variance(nums) ** 0.5\n\n'
    'if __name__ == "__main__":\n'
    '    data = [85, 92, 78, 90, 88]\n'
    '    print(f"均值: {mean(data):.2f}")\n'
    '    print(f"中位数: {median(data)}")\n'
    '    print(f"方差: {variance(data):.2f}")\n'
    '    print(f"标准差: {std_dev(data):.2f}")',
    '统计工具模块'
)

doc.add_heading('练习 2：用 requests 爬取网页并解析 JSON', level=2)
add_code(doc,
    'import requests\n\n'
    'def get_weather(city):\n'
    '    """获取指定城市的天气信息（示例API）"""\n'
    '    # 使用免费的天气API\n'
    '    url = f"https://api.open-meteo.com/v1/forecast"\n'
    '    params = {\n'
    '        "latitude": 31.23,   # 上海纬度\n'
    '        "longitude": 121.47, # 上海经度\n'
    '        "current_weather": True\n'
    '    }\n'
    '    resp = requests.get(url, params=params)\n'
    '    if resp.status_code == 200:\n'
    '        data = resp.json()\n'
    '        weather = data["current_weather"]\n'
    '        return f"温度: {weather[\'temperature\']}°C, 风速: {weather[\'windspeed\']}km/h"\n'
    '    return "获取天气失败"\n\n'
    'print(get_weather("上海"))',
    '爬取天气数据'
)

doc.add_page_break()

# ===== 十三、检查清单 =====
doc.add_heading('十三、本日学习检查清单 ✅', level=1)
doc.add_paragraph('□ 能将常用操作封装为函数，提高代码复用性')
doc.add_paragraph('□ 理解 return 和 print 的本质区别')
doc.add_paragraph('□ 为函数编写 docstring 文档字符串')
doc.add_paragraph('□ 掌握四种参数类型：必备 / 默认 / *args / **kwargs')
doc.add_paragraph('□ 知道参数定义的正确顺序')
doc.add_paragraph('□ 理解局部变量和全局变量的作用域差异')
doc.add_paragraph('□ 会用 global 和 nonlocal 修改不同作用域的变量')
doc.add_paragraph('□ 能使用 lambda 写出简单的匿名函数')
doc.add_paragraph('□ 掌握 map / filter / reduce 的用法')
doc.add_paragraph('□ 理解闭包的原理：嵌套函数 + 记住外层变量')
doc.add_paragraph('□ 了解递归的基本概念（基线条件 + 递归条件）')
doc.add_paragraph('□ 认识装饰器的作用和基本写法（@语法）')
doc.add_paragraph('□ 理解迭代器和生成器（yield）的概念')
doc.add_paragraph('□ 会用拆包（*）灵活处理列表和元组')
doc.add_paragraph('□ 掌握 import 的多种导入方式')
doc.add_paragraph('□ 理解 __name__ == "__main__" 的作用')
doc.add_paragraph('□ 了解包的结构（__init__.py / __all__）')
doc.add_paragraph('□ 能使用 os / sys / pathlib 进行文件和目录操作')
doc.add_paragraph('□ 能使用 datetime 处理日期时间')
doc.add_paragraph('□ 能使用 random 生成随机数')
doc.add_paragraph('□ 知道 collections.Counter 和 defaultdict 的用法')
doc.add_paragraph('□ 能用 pip 安装第三方库')
doc.add_paragraph('□ 能用 requests 发送 HTTP 请求')
doc.add_paragraph('□ 能用 json 模块解析和生成 JSON 数据')

output_path = r'D:\NoteBook\Day3_学习笔记_函数与模块化编程.docx'
doc.save(output_path)
print(f"Day 3 saved: {output_path}")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成Day2学习笔记Word文档：控制流与数据结构"""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# ===== 全局样式 =====
style = doc.styles['Normal']
style.font.name = '微软雅黑'
style.font.size = Pt(11)
style.paragraph_format.line_spacing = 1.5
style.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

for i in range(1, 4):
    hs = doc.styles[f'Heading {i}']
    hs.font.name = '微软雅黑'
    hs.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    if i == 1:
        hs.font.size = Pt(18)
        hs.font.color.rgb = RGBColor(0x1A, 0x56, 0xDB)
    elif i == 2:
        hs.font.size = Pt(15)
        hs.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)
    elif i == 3:
        hs.font.size = Pt(13)
        hs.font.color.rgb = RGBColor(0x34, 0x49, 0x5E)

def add_code(doc, code, caption=""):
    if caption:
        p = doc.add_paragraph()
        r = p.add_run(f"📌 {caption}")
        r.bold = True; r.font.size = Pt(10); r.font.color.rgb = RGBColor(0x66,0x66,0x66)
    p = doc.add_paragraph()
    r = p.add_run(code)
    r.font.name = 'Consolas'; r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(0x2D,0x2D,0x2D)
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), 'F5F5F5'); shd.set(qn('w:val'), 'clear')
    p.paragraph_format.element.get_or_add_pPr().append(shd)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)

def add_tip(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(f"💡 提示：{text}")
    r.font.size = Pt(10); r.font.color.rgb = RGBColor(0xE6,0x7E,0x22); r.italic = True

def add_warn(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(f"⚠️ 注意：{text}")
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
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(80)
r = p.add_run("Python 学习笔记")
r.font.size = Pt(28); r.font.color.rgb = RGBColor(0x1A,0x56,0xDB); r.bold = True

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Day 2：控制流与数据结构")
r.font.size = Pt(20); r.font.color.rgb = RGBColor(0x2C,0x3E,0x50)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(30)
r = p.add_run("日期：2026年8月6日（周三）  |  学习时长：约6-7小时  |  阶段：Python基础")
r.font.size = Pt(11); r.font.color.rgb = RGBColor(0x7F,0x8C,0x8D)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("学习目标：掌握条件判断与循环，熟练使用列表/元组/字典/集合，入门正则表达式")
r.font.size = Pt(10); r.font.italic = True

doc.add_page_break()

# ===== 目录 =====
doc.add_heading('📑 目录', level=1)
toc = [
    "一、条件判断 if / elif / else",
    "  1.1 if 基本结构", "  1.2 if-else", "  1.3 if-elif-else 多分支",
    "  1.4 条件嵌套", "  1.5 三元运算符（条件表达式）", "  1.6 pass 语句",
    "二、循环语句", "  2.1 while 循环", "  2.2 for 循环",
    "  2.3 range() 函数详解", "  2.4 break 和 continue",
    "  2.5 for-else / while-else 结构", "  2.6 enumerate() 和 zip()",
    "三、列表 List", "  3.1 列表的定义与特性", "  3.2 列表索引与切片",
    "  3.3 列表常用操作（增删改查排序）", "  3.4 列表推导式",
    "  3.5 列表的复制与深拷贝", "  3.6 sorted() 与列表嵌套",
    "四、元组 Tuple", "五、字典 Dict", "  5.1 基本操作", "  5.2 字典遍历与常用方法",
    "六、集合 Set", "  6.1 基本操作", "  6.2 集合运算",
    "七、字符串进阶操作", "八、正则表达式入门",
    "九、综合练习（LeetCode实战）", "十、本日学习检查清单",
]
for item in toc:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    r = p.add_run(item)
    r.font.size = Pt(10)
    if not item.startswith("  "): r.bold = True

doc.add_page_break()

# ==========================================
# 一、条件判断
# ==========================================
doc.add_heading('一、条件判断 if / elif / else', level=1)
doc.add_paragraph('条件判断让程序能根据不同情况执行不同的代码，这是程序"智能"的基础。')

doc.add_heading('1.1 if 基本结构', level=2)
doc.add_paragraph('Python 用缩进（通常是4个空格）来表示代码块，而不是其他语言中的花括号 {}。')
add_code(doc,
    '# 基本格式：if 条件:\n'
    '#              执行内容（注意前面有4个空格缩进！）\n\n'
    'age = 18\n'
    'if age >= 18:\n'
    '    print("你已成年，可以进入")  # 缩进表示这行属于 if\n'
    'print("程序继续...")              # 不缩进，不在 if 内\n\n'
    '# ⚠️ 条件后面的冒号 : 不能忘记！\n'
    '# ⚠️ 缩进必须一致，不能有的用2格有的用4格！',
    'if 语句基本格式'
)

doc.add_heading('1.2 if-else 结构', level=2)
add_code(doc,
    'age = 16\n'
    'if age >= 18:\n'
    '    print("已成年")\n'
    'else:\n'
    '    print("未成年")  # 条件不成立时执行这里',
    'if-else 双分支'
)

doc.add_heading('1.3 if-elif-else 多分支结构', level=2)
doc.add_paragraph('elif = else if，用于判断多个条件。从上到下依次检查，第一个成立的就执行，后面的不再检查。')
add_code(doc,
    'score = 85\n\n'
    'if score >= 90:\n'
    '    grade = "A"\n'
    'elif score >= 80:\n'
    '    grade = "B"\n'
    'elif score >= 70:\n'
    '    grade = "C"\n'
    'elif score >= 60:\n'
    '    grade = "D"\n'
    'else:\n'
    '    grade = "F"\n\n'
    'print(f"成绩等级：{grade}")  # 输出：B',
    '成绩等级判断'
)
add_tip(doc, '可以有多个 elif，但 else 最多只有一个，且必须放在最后。elif 和 else 都是可选的。')

doc.add_heading('1.4 条件嵌套', level=2)
doc.add_paragraph('在 if 内部可以再写 if，实现更复杂的逻辑判断：')
add_code(doc,
    'has_ticket = True\n'
    'age = 20\n\n'
    'if has_ticket:\n'
    '    if age >= 18:\n'
    '        print("可以进入成人区")\n'
    '    else:\n'
    '        print("只能进入儿童区")\n'
    'else:\n'
    '    print("请先购票")',
    '嵌套条件判断'
)

doc.add_heading('1.5 三元运算符（条件表达式）', level=2)
doc.add_paragraph('Python 中的三元运算符是一种简洁的单行条件赋值方式：')
add_code(doc,
    '# 格式：值1 if 条件 else 值2\n'
    'age = 20\n'
    'status = "成年" if age >= 18 else "未成年"\n\n'
    '# 等价于：\n'
    '# if age >= 18:\n'
    '#     status = "成年"\n'
    '# else:\n'
    '#     status = "未成年"',
    '三元运算符'
)

doc.add_heading('1.6 pass 语句', level=2)
doc.add_paragraph('pass 是一个"什么都不做"的占位语句，当你还没想好写什么代码时先用它占住位置：')
add_code(doc,
    '# 例如：后续再实现具体功能\n'
    'if age >= 18:\n'
    '    pass  # TODO: 后续添加逻辑\n'
    'else:\n'
    '    print("未成年")\n\n'
    '# pass 也常用于定义空的类或函数\n'
    'def my_function():\n'
    '    pass  # 先占位，后面再实现',
    'pass 占位语句'
)

doc.add_page_break()

# ==========================================
# 二、循环语句
# ==========================================
doc.add_heading('二、循环语句', level=1)

doc.add_heading('2.1 while 循环', level=2)
doc.add_paragraph('while 循环："当条件为真时，重复执行"。需要自己管理循环变量的变化。')
add_code(doc,
    '# 基本结构：while 条件:\n'
    '#               循环体\n'
    '#               改变循环变量（重要！）\n\n'
    'count = 1\n'
    'while count <= 5:\n'
    '    print(f"第 {count} 次循环")\n'
    '    count += 1  # ⚠️ 必须有这行，否则会死循环！\n\n'
    '# 输出：第 1~5 次循环',
    'while 循环示例'
)
add_warn(doc, 'while 循环最怕"死循环"——条件永远为 True，程序卡住不动。务必确保循环变量在每次迭代中向终止条件靠近！')

doc.add_heading('2.2 for 循环', level=2)
doc.add_paragraph('for 循环："依次取出可迭代对象中的每个元素"。Python 的 for 循环比 while 更常用。')
add_code(doc,
    '# 格式：for 临时变量 in 可迭代对象:\n'
    '#           循环体\n\n'
    '# 遍历字符串\n'
    'for char in "Hello":\n'
    '    print(char, end=" ")  # 输出：H e l l o\n\n'
    '# 遍历列表\n'
    'fruits = ["苹果", "香蕉", "橙子"]\n'
    'for fruit in fruits:\n'
    '    print(f"我喜欢吃{fruit}")',
    'for 循环基本用法'
)
add_tip(doc, '"可迭代对象"是指能逐个返回元素的对象，包括：字符串、列表、元组、字典、集合、range() 等。')

doc.add_heading('2.3 range() 函数详解', level=2)
doc.add_paragraph('range() 用于生成一个整数序列，常和 for 循环配合使用：')
add_code(doc,
    '# range(stop)：从 0 到 stop-1（左闭右开）\n'
    'for i in range(5):\n'
    '    print(i, end=" ")     # 输出：0 1 2 3 4\n\n'
    '# range(start, stop)：从 start 到 stop-1\n'
    'for i in range(2, 6):\n'
    '    print(i, end=" ")     # 输出：2 3 4 5\n\n'
    '# range(start, stop, step)：步长为 step\n'
    'for i in range(1, 10, 2):\n'
    '    print(i, end=" ")     # 输出：1 3 5 7 9（奇数）\n\n'
    '# 倒序：步长为负\n'
    'for i in range(5, 0, -1):\n'
    '    print(i, end=" ")     # 输出：5 4 3 2 1',
    'range() 四种用法'
)
add_warn(doc, 'range(start, stop, step) 也是左闭右开区间！range(1, 5) 是 1, 2, 3, 4，不包含 5。')

doc.add_heading('2.4 break 和 continue', level=2)
add_table(doc,
    ['关键字', '作用', '比喻'],
    [
        ['break', '立即终止整个循环，不再执行后续迭代', '提前下班走人'],
        ['continue', '跳过当前这一轮迭代，继续下一轮', '这一轮请假，下一轮继续'],
    ]
)
add_code(doc,
    '# break 示例：找到第一个偶数就停止\n'
    'for num in [1, 3, 5, 6, 7, 8]:\n'
    '    if num % 2 == 0:\n'
    '        print(f"找到了：{num}")\n'
    '        break          # 输出"找到了：6"后立即退出\n\n'
    '# continue 示例：只打印奇数\n'
    'for num in range(1, 11):\n'
    '    if num % 2 == 0:\n'
    '        continue       # 偶数就跳过\n'
    '    print(num, end=" ") # 输出：1 3 5 7 9',
    'break 与 continue'
)
add_warn(doc, 'continue 之前一定要先更新循环变量！否则可能导致无限循环。break 和 continue 只对最近的循环起作用。')

doc.add_heading('2.5 for-else / while-else 结构', level=2)
doc.add_paragraph('Python 特有语法：当循环正常结束（没有被 break 打断）时，执行 else 块。')
add_code(doc,
    '# 判断一个数是否为质数\n'
    'n = 17\n'
    'for i in range(2, int(n**0.5) + 1):\n'
    '    if n % i == 0:\n'
    '        print(f"{n} 不是质数")\n'
    '        break\n'
    'else:\n'
    '    # 只有循环没有被 break 打断时才执行\n'
    '    print(f"{n} 是质数")',
    'for-else 判断质数'
)

doc.add_heading('2.6 enumerate() 和 zip()', level=2)
add_code(doc,
    '# enumerate()：同时获取索引和值\n'
    'fruits = ["苹果", "香蕉", "橙子"]\n'
    'for i, fruit in enumerate(fruits):\n'
    '    print(f"{i}: {fruit}")    # 0: 苹果  1: 香蕉  2: 橙子\n\n'
    '# enumerate() 可以指定起始索引\n'
    'for i, fruit in enumerate(fruits, start=1):\n'
    '    print(f"{i}: {fruit}")    # 1: 苹果  2: 香蕉  3: 橙子',
    'enumerate() 用法'
)
add_code(doc,
    '# zip()：同时遍历多个可迭代对象\n'
    'names = ["小明", "小红", "小刚"]\n'
    'scores = [95, 87, 92]\n\n'
    'for name, score in zip(names, scores):\n'
    '    print(f"{name}: {score}分")\n\n'
    '# 如果长度不一致，以最短的那个为准\n'
    'for a, b in zip([1,2,3,4], "ab"):\n'
    '    print(a, b)  # 只输出 1 a  2 b',
    'zip() 用法'
)

doc.add_page_break()

# ==========================================
# 三、列表 List
# ==========================================
doc.add_heading('三、列表 List', level=1)
doc.add_paragraph('列表是 Python 中最重要的数据结构之一。它是一个有序、可变、可包含任意类型元素的容器。')

doc.add_heading('3.1 列表的定义与特性', level=2)
add_code(doc,
    '# 用方括号 [] 定义列表\n'
    'empty_list = []                    # 空列表\n'
    'numbers = [1, 2, 3, 4, 5]         # 整数列表\n'
    'mixed = [1, "hello", 3.14, True]   # 混合类型（不推荐但可以）\n'
    'nested = [[1, 2], [3, 4], [5, 6]] # 嵌套列表（二维数组）',
    '创建列表'
)
add_code(doc,
    '# 列表的特性\n'
    'li = [1, 2, 3]\n'
    'print(len(li))       # 3 — 获取长度\n'
    'print(type(li))      # <class \'list\'>\n'
    'print(li[1])         # 2 — 通过索引访问\n'
    'li[1] = 100          # 可以修改元素（可变性）\n'
    'print(li)            # [1, 100, 3]',
    '列表基本属性'
)

doc.add_heading('3.2 列表索引与切片', level=2)
doc.add_paragraph('列表的索引和切片语法与字符串完全一致：')
add_code(doc,
    'li = [10, 20, 30, 40, 50, 60]\n\n'
    '# 正向索引：0    1    2    3    4    5\n'
    '# 负向索引：-6   -5   -4   -3   -2   -1\n\n'
    'li[0]       → 10        # 第一个元素\n'
    'li[-1]      → 60        # 最后一个元素\n'
    'li[1:4]     → [20,30,40] # 索引1到3（左闭右开）\n'
    'li[:3]      → [10,20,30] # 从开头到索引2\n'
    'li[3:]      → [40,50,60] # 从索引3到末尾\n'
    'li[::2]     → [10,30,50] # 每隔一个取一个\n'
    'li[::-1]    → [60,50,40,30,20,10]  # 反向（快速反转列表！）',
    '列表索引与切片'
)

doc.add_heading('3.3 列表常用操作', level=2)

doc.add_heading('（1）新增元素', level=3)
add_code(doc,
    'li = [1, 2, 3]\n\n'
    '# append(x)：在末尾添加一个元素（整体添加）\n'
    'li.append(4)          # [1, 2, 3, 4]\n'
    'li.append([5, 6])     # [1, 2, 3, 4, [5, 6]] ← 整个列表作为一个元素！\n\n'
    '# extend(iterable)：将可迭代对象的每个元素逐个添加（分散添加）\n'
    'li = [1, 2, 3]\n'
    'li.extend([4, 5])     # [1, 2, 3, 4, 5] ← 和上面对比！\n\n'
    '# insert(index, x)：在指定位置插入\n'
    'li = [1, 2, 3]\n'
    'li.insert(1, "x")     # [1, "x", 2, 3] ← 在索引1处插入',
    '列表新增操作'
)
add_tip(doc, 'append vs extend：append 把参数当成一个整体加进去；extend 把参数里的每个元素一个个加进去。记住：extend = 扩展/展开。')

doc.add_heading('（2）删除元素', level=3)
add_code(doc,
    'li = [10, 20, 30, 20, 40]\n\n'
    '# del：按索引删除\n'
    'del li[0]             # [20, 30, 20, 40]\n\n'
    '# pop([index])：弹出并返回元素，默认弹出最后一个\n'
    'li = [10, 20, 30]\n'
    'last = li.pop()       # last=30, li→[10,20]\n'
    'second = li.pop(0)    # second=10, li→[20]\n\n'
    '# remove(x)：按值删除（删除第一个匹配项）\n'
    'li = [10, 20, 30, 20]\n'
    'li.remove(20)         # [10, 30, 20] ← 只删第一个20\n\n'
    '# clear()：清空整个列表\n'
    'li.clear()            # []',
    '列表删除操作'
)

doc.add_heading('（3）查询元素', level=3)
add_code(doc,
    'li = [10, 20, 30, 20, 40]\n\n'
    '# in / not in：判断元素是否存在\n'
    'print(20 in li)       # True\n'
    'print(50 not in li)   # True\n\n'
    '# index(x)：返回元素第一次出现的索引\n'
    'print(li.index(20))   # 1（不是3）\n\n'
    '# count(x)：统计元素出现次数\n'
    'print(li.count(20))   # 2',
    '列表查询操作'
)

doc.add_heading('（4）排序与反转', level=3)
add_code(doc,
    'li = [3, 1, 4, 1, 5, 9]\n\n'
    '# sort()：原地排序（修改原列表）\n'
    'li.sort()                    # [1, 1, 3, 4, 5, 9] 升序\n'
    'li.sort(reverse=True)        # [9, 5, 4, 3, 1, 1] 降序\n\n'
    '# reverse()：反转顺序（不是排序！）\n'
    'li = [1, 2, 3]\n'
    'li.reverse()                 # [3, 2, 1]\n\n'
    '# sorted()：返回新排序列表（不修改原列表）⭐\n'
    'li = [3, 1, 4, 1, 5, 9]\n'
    'new_li = sorted(li)          # [1, 1, 3, 4, 5, 9]\n'
    'print(li)                    # [3, 1, 4, 1, 5, 9] 原列表不变！',
    '列表排序操作'
)
add_warn(doc, 'sort() 会修改原列表且返回 None！不要写 li = li.sort()（这会让 li 变成 None）。')

doc.add_heading('3.4 列表推导式', level=2)
doc.add_paragraph('列表推导式是 Python 的一大特色，用一行代码完成"循环+条件+生成"的操作：')
add_code(doc,
    '# 基本格式：[表达式 for 变量 in 可迭代对象]\n'
    'squares = [x**2 for x in range(1, 6)]\n'
    'print(squares)  # [1, 4, 9, 16, 25]\n\n'
    '# 带条件过滤：[表达式 for 变量 in 可迭代对象 if 条件]\n'
    'evens = [x for x in range(1, 11) if x % 2 == 0]\n'
    'print(evens)    # [2, 4, 6, 8, 10]\n\n'
    '# 带 if-else 的推导式（注意顺序变了！）\n'
    'labels = ["偶数" if x%2==0 else "奇数" for x in range(1,6)]\n'
    'print(labels)   # [\'奇数\', \'偶数\', \'奇数\', \'偶数\', \'奇数\']',
    '列表推导式'
)
add_tip(doc, '推导式比传统的 for+append 快得多，而且更 Pythonic。但不要写得太复杂，影响可读性就得不偿失了。')

doc.add_heading('3.5 列表的复制与深拷贝', level=2)
doc.add_paragraph('这是初学者最容易掉坑的地方！直接赋值不是复制，只是贴了另一个标签：')
add_code(doc,
    '# 直接赋值：两个变量指向同一个列表\n'
    'a = [1, 2, 3]\n'
    'b = a            # b 和 a 指向同一个对象！\n'
    'b[0] = 999\n'
    'print(a)         # [999, 2, 3] — a 也被改了！！\n\n'
    '# 浅拷贝：创建新列表，但嵌套列表还是共享的\n'
    'a = [1, 2, [3, 4]]\n'
    'b = a.copy()     # 或 b = a[:] 或 b = list(a)\n'
    'b[0] = 999       # 只影响 b\n'
    'b[2][0] = 888    # 影响 b 里面的嵌套列表...也影响 a 的！！！\n\n'
    '# 深拷贝：完全独立，包括嵌套对象\n'
    'import copy\n'
    'a = [1, 2, [3, 4]]\n'
    'b = copy.deepcopy(a)\n'
    'b[2][0] = 888    # 完全不影响 a',
    '直接赋值 vs 浅拷贝 vs 深拷贝'
)
add_warn(doc, '列表中有嵌套列表/字典时，用 .copy()（浅拷贝）是不够的，必须用 copy.deepcopy()！')

doc.add_heading('3.6 sorted() 与列表嵌套', level=2)
add_code(doc,
    '# sorted() 的 key 参数：指定排序依据\n'
    'students = [\n'
    '    {"name": "小明", "score": 85},\n'
    '    {"name": "小红", "score": 92},\n'
    '    {"name": "小刚", "score": 78}\n'
    ']\n'
    '# 按分数排序（lambda 是一个小函数，下一章会讲）\n'
    'ranked = sorted(students, key=lambda s: s["score"], reverse=True)\n'
    'for s in ranked:\n'
    '    print(f"{s[\'name\']}: {s[\'score\']}")\n'
    '# 输出：小红: 92  小明: 85  小刚: 78',
    'sorted() 按指定规则排序'
)

doc.add_page_break()

# ==========================================
# 四、元组 Tuple
# ==========================================
doc.add_heading('四、元组 Tuple', level=1)
doc.add_paragraph('元组和列表很像，但有一个关键区别：元组创建后不能修改（不可变）。')

add_code(doc,
    '# 用圆括号 () 定义元组\n'
    't1 = (1, 2, 3)\n'
    't2 = ("a", "b", "c")\n'
    't3 = (1,)              # ⚠️ 只有一个元素时必须加逗号！否则 (1) 就是整数\n\n'
    '# 元组的不可变性\n'
    't = (1, 2, 3)\n'
    '# t[0] = 5             ← 会报 TypeError！元组不支持修改\n\n'
    '# 元组支持的操作（和列表相同的部分）\n'
    'len(t)                  # 3\n'
    't[0]                    # 1 — 索引\n'
    't[1:3]                  # (2, 3) — 切片\n'
    '2 in t                  # True — 成员判断\n'
    't.count(2)              # 1 — 计数',
    '元组基本操作'
)

doc.add_heading('元组的主要应用场景', level=2)
doc.add_paragraph('① 函数返回多个值（本质返回的是元组）')
doc.add_paragraph('② 格式化字符串后面的 () 本质也是元组')
doc.add_paragraph('③ 保护数据不被意外修改（如常量配置）')
doc.add_paragraph('④ 作为字典的键（列表不能作为字典键，但元组可以）')

doc.add_page_break()

# ==========================================
# 五、字典 Dict
# ==========================================
doc.add_heading('五、字典 Dict', level=1)
doc.add_paragraph('字典是"键-值对"（key-value）的集合，通过键来快速查找对应的值，就像现实中的字典用字来查释义。')

doc.add_heading('5.1 基本操作', level=2)
add_code(doc,
    '# 用花括号 {} 定义字典\n'
    'person = {\n'
    '    "name": "小明",\n'
    '    "age": 19,\n'
    '    "city": "上海"\n'
    '}\n\n'
    '# 访问元素（通过键，不是索引！）\n'
    'print(person["name"])   # 小明\n\n'
    '# 修改和添加\n'
    'person["age"] = 20      # 修改已有键的值\n'
    'person["hobby"] = "编程" # 添加新键值对\n\n'
    '# 删除\n'
    'del person["city"]      # 删除指定键值对\n'
    'value = person.pop("age")  # 弹出并返回值\n'
    'person.clear()          # 清空字典（保留字典本身）',
    '字典基本操作'
)
add_warn(doc, '用 person["key"] 访问不存在的键会报 KeyError。安全的访问方式是用 get() 方法。')

doc.add_heading('5.2 字典遍历与常用方法', level=2)
add_code(doc,
    'd = {"a": 1, "b": 2, "c": 3}\n\n'
    '# 遍历键\n'
    'for key in d:\n'
    '    print(key, d[key])\n\n'
    '# 遍历键值对（推荐）\n'
    'for key, value in d.items():\n'
    '    print(f"{key} → {value}")\n\n'
    '# 只遍历键 / 只遍历值\n'
    'd.keys()      # dict_keys([\'a\', \'b\', \'c\'])\n'
    'd.values()    # dict_values([1, 2, 3])\n'
    'd.items()     # dict_items([(\'a\',1), (\'b\',2), (\'c\',3)])',
    '字典遍历'
)
add_table(doc,
    ['方法', '作用', '示例'],
    [
        ['d.get(key, default)', '安全获取值，键不存在返回默认值', 'd.get("x", 0) → 0'],
        ['d.setdefault(key, val)', '键存在返回值，不存在则设置并返回', 'd.setdefault("a", 0)'],
        ['d.update(d2)', '用 d2 更新 d 的内容', 'd.update({"b": 10})'],
        ['d.pop(key, default)', '弹出键值对，不存在返回默认值', 'd.pop("x", None)'],
        ['d.popitem()', '弹出最后一个键值对（Python 3.7+ 有序）', ''],
        ['len(d)', '返回键值对个数', 'len({"a":1,"b":2}) → 2'],
    ]
)
add_tip(doc, '优先使用 d.get(key, default) 而不是 d[key]，可以避免程序因 KeyError 而崩溃。')

doc.add_heading('字典的应用场景', level=2)
doc.add_paragraph('• 存储结构化信息（用户信息、配置参数等）')
doc.add_paragraph('• 做映射/查找表（如：中文→英文翻译）')
doc.add_paragraph('• 计数统计（如统计每个单词出现次数）')
add_code(doc,
    '# 实用示例：词频统计\n'
    'text = "apple banana apple orange banana apple"\n'
    'words = text.split()\n'
    'word_count = {}\n'
    'for word in words:\n'
    '    word_count[word] = word_count.get(word, 0) + 1\n'
    'print(word_count)\n'
    '# {\'apple\': 3, \'banana\': 2, \'orange\': 1}',
    '词频统计'
)

doc.add_page_break()

# ==========================================
# 六、集合 Set
# ==========================================
doc.add_heading('六、集合 Set', level=1)
doc.add_paragraph('集合是无序的、元素唯一的容器，和数学中的集合概念一致。')

doc.add_heading('6.1 基本操作', level=2)
add_code(doc,
    '# 用花括号定义（但空集合必须用 set()！）\n'
    's = {1, 2, 3, 3, 2, 1}\n'
    'print(s)       # {1, 2, 3} — 自动去重！\n\n'
    'empty_set = set()   # 正确：空集合\n'
    '# empty_set = {}    # 这是空字典！！不是空集合！！\n\n'
    '# 添加\n'
    's.add(4)             # 添加一个元素（整体添加）\n'
    's.update([5, 6, 7])  # 添加多个（逐个添加）\n\n'
    '# 删除\n'
    's.remove(2)          # 删除元素，不存在会报错\n'
    's.discard(10)        # 删除元素，不存在不会报错（推荐）\n'
    'item = s.pop()       # 随机弹出（集合无序，不确定弹出哪个）',
    '集合基本操作'
)
add_warn(doc, '集合内部是基于哈希表实现的，所以元素必须是"可哈希"的类型（如 int、str、tuple），不能是列表或字典。')

doc.add_heading('6.2 集合运算（交并差）', level=2)
add_code(doc,
    'a = {1, 2, 3, 4}\n'
    'b = {3, 4, 5, 6}\n\n'
    '# 交集：两个集合中都有的元素\n'
    'print(a & b)          # {3, 4}\n'
    'print(a.intersection(b))  # 等价写法\n\n'
    '# 并集：两个集合中所有元素（去重）\n'
    'print(a | b)          # {1, 2, 3, 4, 5, 6}\n'
    'print(a.union(b))     # 等价写法\n\n'
    '# 差集：在 a 但不在 b 中的元素\n'
    'print(a - b)          # {1, 2}\n'
    'print(a.difference(b))  # 等价写法\n\n'
    '# 对称差集：只在其中一个集合中的元素\n'
    'print(a ^ b)          # {1, 2, 5, 6}\n\n'
    '# 判断子集/超集\n'
    'print({1,2}.issubset(a))    # True — {1,2} 是 a 的子集\n'
    'print(a.issuperset({1,2}))  # True — a 是 {1,2} 的超集',
    '集合运算'
)

doc.add_page_break()

# ==========================================
# 七、字符串进阶操作
# ==========================================
doc.add_heading('七、字符串进阶操作', level=1)
add_code(doc,
    '# split()：按分隔符切分字符串\n'
    'text = "苹果,香蕉,橙子,葡萄"\n'
    'fruits = text.split(",")\n'
    'print(fruits)    # [\'苹果\', \'香蕉\', \'橙子\', \'葡萄\']\n\n'
    '# join()：用分隔符将列表拼接为字符串\n'
    'fruits = ["苹果", "香蕉", "橙子"]\n'
    'result = " → ".join(fruits)\n'
    'print(result)    # 苹果 → 香蕉 → 橙子\n\n'
    '# strip() / lstrip() / rstrip()：去除空白字符\n'
    's = "  hello  \\n"\n'
    'print(s.strip())      # "hello"（去掉两端空白）\n\n'
    '# replace(old, new, count)：替换\n'
    's = "apple apple apple"\n'
    'print(s.replace("apple", "orange", 2))  # orange orange apple\n\n'
    '# find() / rfind()：查找子串位置\n'
    's = "hello world"\n'
    'print(s.find("o"))    # 4（第一个 o 的位置）\n'
    'print(s.rfind("o"))   # 7（最后一个 o 的位置）\n\n'
    '# count()：统计子串出现次数\n'
    'print("banana".count("a"))  # 3',
    '字符串常用方法汇总'
)

doc.add_page_break()

# ==========================================
# 八、正则表达式入门
# ==========================================
doc.add_heading('八、正则表达式入门', level=1)
doc.add_paragraph('正则表达式（Regular Expression）是用一种"模式字符串"来匹配和提取文本的工具，在数据清洗、日志分析、表单验证中非常常用。')

doc.add_heading('8.1 基本符号速查', level=2)
add_table(doc,
    ['符号', '含义', '示例', '匹配的内容'],
    [
        [r'\d', '一个数字（0-9）', r'\d\d', '12, 99, 00'],
        [r'\w', '字母/数字/下划线', r'\w+', 'hello, abc123, _name'],
        [r'\s', '空白字符（空格、Tab、换行）', r'a\sb', 'a b, a\tb'],
        [r'.', '任意一个字符（除换行）', r'a.c', 'abc, a1c, a@c'],
        [r'+', '前面的内容出现1次或多次', r'\d+', '5, 123, 9999'],
        [r'*', '前面的内容出现0次或多次', r'ab*c', 'ac, abc, abbc'],
        [r'?', '前面的内容出现0次或1次', r'colou?r', 'color, colour'],
        [r'{n}', '前面的内容恰好出现n次', r'\d{3}', '123, 999'],
        [r'{n,m}', '前面的内容出现n到m次', r'\d{2,4}', '12, 123, 1234'],
        [r'[]', '字符组，匹配其中任意一个', r'[aeiou]', 'a, e, i, o, u'],
        [r'[^]', '排除字符组', r'[^0-9]', '非数字字符'],
        [r'^', '匹配字符串开头', r'^Hello', '以Hello开头的行'],
        [r'$', '匹配字符串结尾', r'world$', '以world结尾的行'],
        [r'()', '分组，可提取匹配的内容', r'(\d{3})-(\d{4})', '提取区号和号码'],
    ]
)
doc.add_paragraph('Python 中使用正则表达式需要先 import re 模块。')

doc.add_heading('8.2 re 模块三个核心函数', level=2)
add_code(doc,
    'import re\n\n'
    '# 1. re.match()：从字符串开头匹配（只看开头！）\n'
    'result = re.match(r"\\d+", "123abc")\n'
    'print(result.group())    # "123" — 匹配成功\n\n'
    'result = re.match(r"\\d+", "abc123")\n'
    'print(result)            # None — 因为开头是字母，不匹配\n\n'
    '# 2. re.search()：在字符串任意位置搜索（找到第一个就返回）\n'
    'result = re.search(r"\\d+", "abc123def")\n'
    'print(result.group())    # "123" — 在中间也能找到\n\n'
    '# 3. re.findall()：找到所有匹配项，返回列表\n'
    'result = re.findall(r"\\d+", "a1 b22 c333")\n'
    'print(result)            # [\'1\', \'22\', \'333\']',
    're.match / re.search / re.findall'
)
add_warn(doc, 're.match() 只从字符串开头匹配，不是全文搜索！大部分情况下你可能想要的是 re.search()。')

doc.add_heading('8.3 分组提取', level=2)
add_code(doc,
    'import re\n'
    '# 用 () 提取需要的内容\n'
    'text = "姓名：张三，年龄：20，电话：138-1234-5678"\n'
    'pattern = r"姓名：(\\w+)，年龄：(\\d+)，电话：(\\d{3}-\\d{4}-\\d{4})"\n'
    'match = re.search(pattern, text)\n'
    'if match:\n'
    '    print(f"姓名：{match.group(1)}")   # 张三\n'
    '    print(f"年龄：{match.group(2)}")   # 20\n'
    '    print(f"电话：{match.group(3)}")   # 138-1234-5678',
    '正则表达式分组提取'
)

doc.add_page_break()

# ==========================================
# 九、综合练习（LeetCode实战）
# ==========================================
doc.add_heading('九、综合练习（LeetCode 实战）', level=1)

doc.add_heading('练习 1：LeetCode 1 — 两数之和（Two Sum）⭐', level=2)
doc.add_paragraph('问题描述：给定一个整数数组 nums 和一个目标值 target，找出和为目标值的两个数的索引。')
add_code(doc,
    '# 暴力解法（O(n²)）— 帮助理解问题\n'
    'def two_sum_brute(nums, target):\n'
    '    for i in range(len(nums)):\n'
    '        for j in range(i + 1, len(nums)):\n'
    '            if nums[i] + nums[j] == target:\n'
    '                return [i, j]\n\n'
    '# 哈希表解法（O(n)）— 推荐！用字典存"值→索引"\n'
    'def two_sum(nums, target):\n'
    '    seen = {}  # {值: 索引}\n'
    '    for i, num in enumerate(nums):\n'
    '        complement = target - num\n'
    '        if complement in seen:\n'
    '            return [seen[complement], i]\n'
    '        seen[num] = i\n\n'
    'print(two_sum([2, 7, 11, 15], 9))  # [0, 1]',
    'LeetCode 1 — 两数之和'
)

doc.add_heading('练习 2：词频统计器', level=2)
doc.add_paragraph('编写程序统计一段文本中每个单词出现的次数，并按出现次数降序输出。')
add_code(doc,
    'text = "apple banana apple orange banana apple grape orange apple"\n'
    'words = text.split()\n\n'
    '# 方法一：手动用字典统计\n'
    'word_count = {}\n'
    'for word in words:\n'
    '    word_count[word] = word_count.get(word, 0) + 1\n\n'
    '# 按频率降序排序\n'
    'sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)\n'
    'for word, count in sorted_words:\n'
    '    print(f"{word}: {count}")\n\n'
    '# 方法二：用 collections.Counter 更简洁\n'
    'from collections import Counter\n'
    'word_count = Counter(words)\n'
    'print(word_count.most_common(3))  # 前3个最多的',
    '词频统计器'
)

doc.add_heading('练习 3：LeetCode 26 — 删除有序数组中的重复项', level=2)
add_code(doc,
    'def remove_duplicates(nums):\n'
    '    """原地删除重复项，返回新长度"""\n'
    '    if not nums:\n'
    '        return 0\n'
    '    # 双指针法\n'
    '    slow = 0  # 指向最后一个不重复元素\n'
    '    for fast in range(1, len(nums)):\n'
    '        if nums[fast] != nums[slow]:\n'
    '            slow += 1\n'
    '            nums[slow] = nums[fast]\n'
    '    return slow + 1\n\n'
    'nums = [1, 1, 2, 2, 3]\n'
    'length = remove_duplicates(nums)\n'
    'print(nums[:length])  # [1, 2, 3]',
    'LeetCode 26 — 删除有序数组中的重复项'
)

doc.add_page_break()

# ==========================================
# 十、本日学习检查清单
# ==========================================
doc.add_heading('十、本日学习检查清单 ✅', level=1)
doc.add_paragraph('□ 能用 if/elif/else 写出多分支判断逻辑')
doc.add_paragraph('□ 理解 Python 缩进的重要性，能正确区分代码块')
doc.add_paragraph('□ 会用三元运算符 (x if 条件 else y) 写简洁的条件表达式')
doc.add_paragraph('□ 知道 pass 语句的用途')
doc.add_paragraph('□ 能用 while 循环处理需要条件控制的重复操作')
doc.add_paragraph('□ 能用 for 循环遍历字符串、列表、字典等')
doc.add_paragraph('□ 掌握 range(start, stop, step) 的三种用法')
doc.add_paragraph('□ 理解 break（跳出循环）和 continue（跳过本轮）的区别')
doc.add_paragraph('□ 会用 enumerate() 同时获取索引和值')
doc.add_paragraph('□ 会用 zip() 同时遍历多个序列')
doc.add_paragraph('□ 能熟练对列表进行增删改查排序操作')
doc.add_paragraph('□ 理解 append vs extend、sort vs sorted 的区别')
doc.add_paragraph('□ 能用列表推导式简化代码')
doc.add_paragraph('□ 理解直接赋值 vs 浅拷贝 vs 深拷贝的区别')
doc.add_paragraph('□ 知道元组不可变，适用哪些场景')
doc.add_paragraph('□ 能用字典存储键值对，用 get() 安全获取值')
doc.add_paragraph('□ 知道字典的 keys()、values()、items() 方法')
doc.add_paragraph('□ 理解集合的无序性和唯一性')
doc.add_paragraph('□ 能用集合的交并差运算（& | - ^）处理数据')
doc.add_paragraph('□ 掌握字符串的 split、join、strip、replace 方法')
doc.add_paragraph('□ 认识正则表达式的基本符号（\\d \\w \\s . + * ?）')
doc.add_paragraph('□ 会用 re.search() 和 re.findall() 提取文本')
doc.add_paragraph('□ 完成 LeetCode 1（两数之和）和 LeetCode 26（去重）')

# 保存
output_path = r'D:\NoteBook\Day2_学习笔记_控制流与数据结构.docx'
doc.save(output_path)
print(f"Day 2 saved: {output_path}")

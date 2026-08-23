#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成Day4学习笔记Word文档：面向对象编程与异常处理"""

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
r = p.add_run("Day 4：面向对象编程与异常处理"); r.font.size = Pt(20); r.font.color.rgb = RGBColor(0x2C,0x3E,0x50)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_before = Pt(30)
r = p.add_run("日期：2026年8月8日（周五）  |  学习时长：约6-7小时  |  阶段：Python基础")
r.font.size = Pt(11); r.font.color.rgb = RGBColor(0x7F,0x8C,0x8D)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("学习目标：理解面向对象三大特性，掌握类与对象、继承多态、异常处理、文件读写")
r.font.size = Pt(10); r.font.italic = True

doc.add_page_break()

doc.add_heading('📑 目录', level=1)
toc = [
    "一、编程范式：面向过程 vs 面向对象",
    "二、类与对象", "  2.1 类的定义", "  2.2 创建和使用对象", "  2.3 self 关键字",
    "  2.4 属性：对象属性 vs 类属性",
    "三、魔法方法（Magic Methods）", "  3.1 __init__ 构造方法",
    "  3.2 __str__ 和 __repr__", "  3.3 其他常用魔法方法",
    "四、面向对象三大特性",
    "  4.1 封装 + 私有属性与方法 + @property",
    "  4.2 继承：单继承/多继承/多层继承",
    "  4.3 super() 与 MRO", "  4.4 多态",
    "五、类的高级特性", "  5.1 @classmethod 类方法",
    "  5.2 @staticmethod 静态方法", "  5.3 抽象类 ABC",
    "六、综合实战：设计游戏角色类体系",
    "七、异常处理", "  7.1 try/except/else/finally",
    "  7.2 常见异常类型", "  7.3 raise 抛出异常", "  7.4 自定义异常",
    "八、文件读写", "  8.1 文件打开与关闭", "  8.2 文件读写操作",
    "  8.3 上下文管理器 with", "  8.4 文件路径与编码",
    "九、CSV 文件读写", "十、JSON 文件读写",
    "十一、综合练习", "十二、本日学习检查清单",
]
for item in toc:
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(1); p.paragraph_format.space_after = Pt(1)
    r = p.add_run(item); r.font.size = Pt(10)
    if not item.startswith("  "): r.bold = True

doc.add_page_break()

# ===== 一、编程范式 =====
doc.add_heading('一、编程范式：面向过程 vs 面向对象', level=1)
add_table(doc,
    ['对比维度', '面向过程（Procedural）', '面向对象（OOP）'],
    [
        ['核心思想', '把问题拆解为步骤和函数', '把问题建模为对象和交互'],
        ['关注点', '怎么做（算法和步骤）', '谁来做（对象和职责）'],
        ['代码组织', '以函数为单位', '以类为单位，封装数据+行为'],
        ['数据与行为', '分离的（数据传给函数处理）', '绑定在一起（对象自己管理）'],
        ['可维护性', '小项目可以，大项目难维护', '大项目结构清晰，易扩展'],
        ['典型场景', '脚本、简单工具、数据处理', '游戏开发、GUI、大型系统'],
    ]
)

doc.add_heading('面向对象的三大优点', level=2)
doc.add_paragraph('① 更符合人的思维习惯 — 用"对象"来模拟现实世界中的事物')
doc.add_paragraph('② 把复杂的事情简单化 — 每个对象负责自己的行为，分工明确')
doc.add_paragraph('③ 把人从执行者变为指挥者 — 你告诉对象做什么，而不是怎么做')

doc.add_heading('面向对象的三大特性', level=2)
doc.add_paragraph('① 封装（Encapsulation）— 隐藏内部细节，只暴露必要的接口')
doc.add_paragraph('② 继承（Inheritance）— 子类复用父类的代码，建立"is-a"关系')
doc.add_paragraph('③ 多态（Polymorphism）— 同一个接口，不同对象有不同实现')

doc.add_page_break()

# ===== 二、类与对象 =====
doc.add_heading('二、类与对象', level=1)
doc.add_paragraph('类（Class）是抽象的模板，对象（Object）是具体的实例。好比"汽车设计图"是类，"你开的那辆车"是对象。')

doc.add_heading('2.1 类的定义', level=2)
add_code(doc,
    '# 格式：class 类名:\n'
    '#           # 属性（数据/名词）\n'
    '#           # 方法（行为/动词）\n\n'
    'class Dog:\n'
    '    """狗类"""\n'
    '    species = "犬科"  # 类属性 — 所有对象共享\n\n'
    '    def bark(self):\n'
    '        """叫的方法"""\n'
    '        print("汪汪！")',
    '类的定义'
)
add_tip(doc, '类名通常使用 PascalCase（大驼峰）：每个单词首字母大写，如 Dog、GameCharacter。')

doc.add_heading('2.2 创建和使用对象', level=2)
add_code(doc,
    '# 创建对象（实例化）\n'
    'my_dog = Dog()          # 就像"造"了一只狗\n\n'
    '# 调用对象的方法\n'
    'my_dog.bark()           # 汪汪！\n\n'
    '# 访问类属性\n'
    'print(my_dog.species)   # 犬科\n'
    'print(Dog.species)      # 犬科（也可以直接用类名访问）',
    '对象的创建与使用'
)

doc.add_heading('2.3 self 关键字', level=2)
doc.add_paragraph('self 是类中方法的第一个参数，代表"调用这个方法的对象本身"。它让方法知道是哪个对象在调用它。')
add_code(doc,
    'class Cat:\n'
    '    def set_name(self, name):\n'
    '        self.name = name  # self.name 是对象自己的属性\n\n'
    '    def meow(self):\n'
    '        print(f"{self.name}：喵喵！")  # 用 self 访问自己的属性\n\n'
    'cat1 = Cat()\n'
    'cat1.set_name("小黑")    # 等价于 Cat.set_name(cat1, "小黑")\n'
    'cat1.meow()              # 小黑：喵喵！\n\n'
    'cat2 = Cat()\n'
    'cat2.set_name("小白")\n'
    'cat2.meow()              # 小白：喵喵！',
    'self 关键字'
)
add_warn(doc, '定义方法时 self 必须写，但调用时不用传（Python 会自动把对象作为第一个参数传入）。')

doc.add_heading('2.4 属性：对象属性 vs 类属性', level=2)
add_table(doc,
    ['对比维度', '对象属性（实例属性）', '类属性'],
    [
        ['定义位置', '在 __init__ 中用 self.xxx 定义', '直接在 class 内定义（方法外）'],
        ['归属', '每个对象一份，值可以不同', '整个类共享一份'],
        ['访问方式', '对象名.属性名', '类名.属性名 或 对象名.属性名'],
        ['修改影响', '只影响当前对象', '影响所有对象（慎用！）'],
        ['典型用途', 'name, age, score', 'species, count, MAX_VALUE'],
    ]
)

doc.add_page_break()

# ===== 三、魔法方法 =====
doc.add_heading('三、魔法方法（Magic Methods）', level=1)
doc.add_paragraph('魔法方法是以双下划线开头和结尾的特殊方法（如 __init__），在特定时机会被 Python 自动调用。')

doc.add_heading('3.1 __init__ 构造方法', level=2)
doc.add_paragraph('__init__ 在创建对象时自动调用，用于初始化对象的属性。这是最常用的魔法方法。')
add_code(doc,
    '# 无参版：属性值固定\n'
    'class Student:\n'
    '    def __init__(self):\n'
    '        self.name = "未知"\n'
    '        self.score = 0\n\n'
    's = Student()          # 自动调用 __init__\n'
    'print(s.name)          # 未知\n\n'
    '# 有参版：创建时传入属性值（推荐）\n'
    'class Student:\n'
    '    def __init__(self, name, score):\n'
    '        self.name = name\n'
    '        self.score = score\n\n'
    's1 = Student("小明", 85)\n'
    's2 = Student("小红", 92)\n'
    'print(f"{s1.name}: {s1.score}")  # 小明: 85',
    '__init__ 构造方法'
)

doc.add_heading('3.2 __str__ 和 __repr__', level=2)
add_table(doc,
    ['方法', '触发时机', '目的', '格式要求'],
    [
        ['__str__', 'print(obj) 或 str(obj)', '给用户看的友好字符串', '返回字符串'],
        ['__repr__', '直接输入 obj 或 repr(obj)', '给开发者看的调试信息', '返回字符串（尽量可直接eval）'],
    ]
)
add_code(doc,
    'class Game:\n'
    '    def __init__(self, title, year):\n'
    '        self.title = title\n'
    '        self.year = year\n\n'
    '    def __str__(self):\n'
    '        return f"《{self.title}》（{self.year}）"\n\n'
    '    def __repr__(self):\n'
    '        return f"Game(\'{self.title}\', {self.year})"\n\n'
    'g = Game("原神", 2020)\n'
    'print(g)      # 《原神》（2020）— 调用 __str__\n'
    '# g             # Game(\'原神\', 2020) — 调用 __repr__（在交互环境）',
    '__str__ 与 __repr__'
)
add_tip(doc, '如果只定义 __repr__ 不定义 __str__，则 print() 会自动用 __repr__。反之不行。建议两个都定义。')

doc.add_heading('3.3 其他常用魔法方法', level=2)
add_table(doc,
    ['方法', '触发方式', '说明'],
    [
        ['__len__', 'len(obj)', '返回对象的"长度"'],
        ['__eq__', 'obj1 == obj2', '定义相等比较规则'],
        ['__lt__', 'obj1 < obj2', '定义小于比较（排序用）'],
        ['__add__', 'obj1 + obj2', '定义加法操作'],
        ['__getitem__', 'obj[key]', '支持下标访问'],
        ['__call__', 'obj()', '让对象可以像函数一样调用'],
    ]
)

doc.add_page_break()

# ===== 四、三大特性 =====
doc.add_heading('四、面向对象三大特性', level=1)

doc.add_heading('4.1 封装 + 私有属性与方法', level=2)
doc.add_paragraph('封装就是把数据和操作数据的方法绑定在一起，并隐藏内部实现细节。')

doc.add_heading('私有属性与方法', level=3)
doc.add_paragraph('在名称前加双下划线 __，表示"私有"，外部不能直接访问（实际是名称被改写为 _类名__名称）。')
add_code(doc,
    'class BankAccount:\n'
    '    def __init__(self, owner, balance):\n'
    '        self.owner = owner         # 公有属性\n'
    '        self.__balance = balance   # 私有属性 — 外部不能直接访问\n\n'
    '    # 通过公开方法安全访问私有属性\n'
    '    def get_balance(self):\n'
    '        """获取余额（只读接口）"""\n'
    '        return self.__balance\n\n'
    '    def deposit(self, amount):\n'
    '        """存款"""\n'
    '        if amount > 0:\n'
    '            self.__balance += amount\n'
    '            return True\n'
    '        return False\n\n'
    '    def withdraw(self, amount):\n'
    '        """取款（需要验证）"""\n'
    '        if 0 < amount <= self.__balance:\n'
    '            self.__balance -= amount\n'
    '            return True\n'
    '        return False',
    '私有属性封装'
)
add_warn(doc, 'Python 的私有是"约定"为主，实际上可以通过 _类名__属性名 访问。但这违反了封装原则，不要这样做！')

doc.add_heading('@property 装饰器', level=3)
doc.add_paragraph('@property 可以让方法像属性一样访问，兼顾封装性和便利性：')
add_code(doc,
    'class Circle:\n'
    '    def __init__(self, radius):\n'
    '        self._radius = radius\n\n'
    '    @property\n'
    '    def radius(self):\n'
    '        """获取半径"""\n'
    '        return self._radius\n\n'
    '    @radius.setter\n'
    '    def radius(self, value):\n'
    '        """设置半径（带验证）"""\n'
    '        if value <= 0:\n'
    '            raise ValueError("半径必须为正数")\n'
    '        self._radius = value\n\n'
    '    @property\n'
    '    def area(self):\n'
    '        """面积（只读，计算属性）"""\n'
    '        return 3.14159 * self._radius ** 2\n\n'
    'c = Circle(5)\n'
    'print(c.radius)   # 5 — 像属性一样访问\n'
    'print(c.area)     # 78.53975 — 计算属性\n'
    'c.radius = 10     # 像属性一样赋值，但有验证',
    '@property 装饰器'
)

doc.add_heading('4.2 继承', level=2)

doc.add_heading('单继承', level=3)
add_code(doc,
    '# 父类（基类）\n'
    'class Animal:\n'
    '    def __init__(self, name):\n'
    '        self.name = name\n\n'
    '    def speak(self):\n'
    '        print(f"{self.name} 发出声音")\n\n'
    '# 子类（派生类）继承父类\n'
    'class Dog(Animal):\n'
    '    def speak(self):  # 重写父类方法\n'
    '        print(f"{self.name}：汪汪！")\n\n'
    'd = Dog("旺财")\n'
    'd.speak()  # 旺财：汪汪！— 调用子类自己的方法',
    '单继承'
)

doc.add_heading('多层继承', level=3)
add_code(doc,
    '# A → B → C 多层继承链\n'
    'class Animal:\n'
    '    def breathe(self):\n'
    '        print("呼吸")\n\n'
    'class Mammal(Animal):\n'
    '    def feed_milk(self):\n'
    '        print("哺乳")\n\n'
    'class Dog(Mammal):\n'
    '    def bark(self):\n'
    '        print("汪汪")\n\n'
    'd = Dog()\n'
    'd.breathe()    # 来自 Animal\n'
    'd.feed_milk()  # 来自 Mammal\n'
    'd.bark()       # 来自 Dog 自己',
    '多层继承'
)

doc.add_heading('多继承', level=3)
add_code(doc,
    'class Flyable:\n'
    '    def fly(self):\n'
    '        print("飞")\n\n'
    'class Swimmable:\n'
    '    def swim(self):\n'
    '        print("游")\n\n'
    'class Duck(Flyable, Swimmable):  # 同时继承两个\n'
    '    def quack(self):\n'
    '        print("嘎嘎")\n\n'
    'duck = Duck()\n'
    'duck.fly()    # 飞\n'
    'duck.swim()   # 游\n'
    'duck.quack()  # 嘎嘎',
    '多继承'
)
add_warn(doc, '多继承功能强大但也容易导致混乱（"菱形继承"问题）。使用时要谨慎设计。')

doc.add_heading('4.3 super() 与 MRO', level=2)
doc.add_paragraph('super() 用于在子类中调用父类的方法（通常初始化时用）：')
add_code(doc,
    'class Animal:\n'
    '    def __init__(self, name):\n'
    '        self.name = name\n\n'
    'class Dog(Animal):\n'
    '    def __init__(self, name, breed):\n'
    '        super().__init__(name)  # 调用父类的 __init__\n'
    '        self.breed = breed\n\n'
    'd = Dog("旺财", "金毛")\n'
    'print(d.name, d.breed)  # 旺财 金毛',
    'super() 调用父类方法'
)
doc.add_paragraph('MRO（Method Resolution Order，方法解析顺序）：在多继承中，Python 按特定顺序查找方法。')
add_code(doc,
    'class A: pass\n'
    'class B(A): pass\n'
    'class C(A): pass\n'
    'class D(B, C): pass\n\n'
    'print(D.__mro__)  # D → B → C → A → object\n'
    '# 或 print(D.mro())',
    '查看 MRO'
)

doc.add_heading('4.4 多态', level=2)
doc.add_paragraph('多态 = 同一个方法名，不同的类有不同的实现。核心条件：有继承 + 子类重写父类方法。')
add_code(doc,
    'class Game:\n'
    '    def play(self):\n'
    '        print("玩游戏")\n\n'
    'class Genshin(Game):\n'
    '    def play(self):\n'
    '        print("玩原神：探索提瓦特大陆")\n\n'
    'class StarRail(Game):\n'
    '    def play(self):\n'
    '        print("玩星铁：银河冒险")\n\n'
    '# 多态：同一个接口 play()，不同对象有不同表现\n'
    'games = [Game(), Genshin(), StarRail()]\n'
    'for g in games:\n'
    '    g.play()\n'
    '# 玩游戏\n'
    '# 玩原神：探索提瓦特大陆\n'
    '# 玩星铁：银河冒险',
    '多态示例'
)

doc.add_page_break()

# ===== 五、类的高级特性 =====
doc.add_heading('五、类的高级特性', level=1)

doc.add_heading('5.1 @classmethod 类方法', level=2)
doc.add_paragraph('类方法的第一个参数是 cls（类本身），而不是 self（对象）。用来操作类级别的属性和创建对象。')
add_code(doc,
    'class Student:\n'
    '    count = 0  # 类属性，统计学生总数\n\n'
    '    def __init__(self, name):\n'
    '        self.name = name\n'
    '        Student.count += 1\n\n'
    '    @classmethod\n'
    '    def get_count(cls):\n'
    '        return cls.count\n\n'
    '    @classmethod\n'
    '    def from_string(cls, info):\n'
    '        """工厂方法：从字符串创建对象"""\n'
    '        name, age = info.split(",")\n'
    '        return cls(name)',
    '@classmethod'
)

doc.add_heading('5.2 @staticmethod 静态方法', level=2)
doc.add_paragraph('静态方法不需要 self 或 cls 参数，跟普通函数一样，只是放在类的命名空间里。')
add_code(doc,
    'class MathUtils:\n'
    '    @staticmethod\n'
    '    def is_even(n):\n'
    '        return n % 2 == 0\n\n'
    '    @staticmethod\n'
    '    def clamp(value, min_val, max_val):\n'
    '        return max(min_val, min(value, max_val))\n\n'
    'print(MathUtils.is_even(4))     # True\n'
    'print(MathUtils.clamp(15, 0, 10))  # 10',
    '@staticmethod'
)

doc.add_heading('5.3 抽象类 ABC', level=2)
doc.add_paragraph('抽象类定义了子类必须实现的"接口规范"，不能直接实例化。')
add_code(doc,
    'from abc import ABC, abstractmethod\n\n'
    'class GameCharacter(ABC):\n'
    '    """游戏角色抽象类 — 所有角色的模板"""\n'
    '    @abstractmethod\n'
    '    def attack(self):\n'
    '        """攻击方法 — 子类必须实现！"""\n'
    '        pass\n\n'
    '    @abstractmethod\n'
    '    def skill(self):\n'
    '        """技能方法"""\n'
    '        pass',
    '抽象类'
)

doc.add_page_break()

# ===== 六、游戏角色类体系 =====
doc.add_heading('六、综合实战：设计游戏角色类体系', level=1)
doc.add_paragraph('目标：演示面向对象的三大特性 — 封装（属性私有 + getter）、继承（不同职业）、多态（各自的 attack 实现）。')
add_code(doc,
    'from abc import ABC, abstractmethod\n\n'
    '# 抽象基类\n'
    'class GameCharacter(ABC):\n'
    '    """游戏角色基类"""\n'
    '    def __init__(self, name: str, hp: int, atk: int):\n'
    '        self.name = name\n'
    '        self.__hp = hp     # 私有：外部不能直接修改血量\n'
    '        self.atk = atk\n\n'
    '    def take_damage(self, damage: int):\n'
    '        """受到伤害（通过公开方法修改私有属性）"""\n'
    '        self.__hp -= damage\n'
    '        if self.__hp <= 0:\n'
    '            self.__hp = 0\n'
    '            self.on_death()\n\n'
    '    def get_hp(self) -> int:\n'
    '        return self.__hp\n\n'
    '    def is_alive(self) -> bool:\n'
    '        return self.__hp > 0\n\n'
    '    @abstractmethod\n'
    '    def attack(self):\n'
    '        """子类必须实现攻击方式"""\n'
    '        pass\n\n'
    '    @abstractmethod\n'
    '    def on_death(self):\n'
    '        """子类必须实现死亡效果"""\n'
    '        pass\n\n'
    '    def __str__(self):\n'
    '        return f"[{self.__class__.__name__}] {self.name} HP:{self.__hp} ATK:{self.atk}"\n\n'
    '# 战士\n'
    'class Warrior(GameCharacter):\n'
    '    def attack(self):\n'
    '        return f"{self.name} 挥动巨剑，造成 {self.atk} 点伤害！"\n'
    '    def on_death(self):\n'
    '        print(f"{self.name} 壮烈牺牲！")\n\n'
    '# 法师\n'
    'class Mage(GameCharacter):\n'
    '    def __init__(self, name, hp, atk, mp=100):\n'
    '        super().__init__(name, hp, atk)\n'
    '        self.mp = mp\n'
    '    def attack(self):\n'
    '        if self.mp >= 10:\n'
    '            self.mp -= 10\n'
    '            return f"{self.name} 释放火球术，造成 {self.atk*1.5:.0f} 点魔法伤害！"\n'
    '        return f"{self.name} 魔力不足！"\n'
    '    def on_death(self):\n'
    '        print(f"{self.name} 化为光点消散...")\n\n'
    '# 测试\n'
    'w = Warrior("亚瑟", hp=100, atk=15)\n'
    'm = Mage("甘道夫", hp=60, atk=12)\n\n'
    'print(w)\n'
    'print(w.attack())\n'
    'w.take_damage(30)\n'
    'print(f"剩余血量：{w.get_hp()}")\n'
    'print(m.attack())',
    '游戏角色类体系完整示例'
)

doc.add_page_break()

# ===== 七、异常处理 =====
doc.add_heading('七、异常处理', level=1)
doc.add_paragraph('程序运行时出现的错误叫"异常"。如果不处理异常，程序会直接崩溃。异常处理让程序能够优雅地应对意外情况。')

doc.add_heading('7.1 try/except/else/finally 完整结构', level=2)
add_code(doc,
    '# 完整结构（按顺序）\n'
    'try:\n'
    '    # 可能出错的代码\n'
    '    num = int(input("请输入一个数字："))\n'
    '    result = 100 / num\n'
    'except ValueError:\n'
    '    # 捕获特定异常 — 输入不是数字\n'
    '    print("输入的不是数字！")\n'
    'except ZeroDivisionError:\n'
    '    # 捕获特定异常 — 除以零\n'
    '    print("不能除以零！")\n'
    'except Exception as e:\n'
    '    # 捕获其他所有异常（兜底）\n'
    '    print(f"出错了：{e}")\n'
    'else:\n'
    '    # 没有异常时执行\n'
    '    print(f"计算结果：{result}")\n'
    'finally:\n'
    '    # 无论有没有异常，一定会执行\n'
    '    print("程序结束")',
    'try/except/else/finally 完整结构'
)
add_tip(doc, '捕获范围从窄到宽：先捕获具体的异常（ValueError），再捕获通用的（Exception）。不要把具体异常放在后面，会被前面的宽泛捕获拦截。')

doc.add_heading('7.2 常见异常类型速查', level=2)
add_table(doc,
    ['异常类型', '触发条件', '示例'],
    [
        ['ValueError', '值类型正确但值不合适', 'int("abc")'],
        ['TypeError', '对不合适的类型进行操作', '"a" + 1'],
        ['KeyError', '字典中不存在的键', 'd["not_exist"]'],
        ['IndexError', '列表索引超出范围', '[1,2,3][10]'],
        ['FileNotFoundError', '文件不存在', 'open("no.txt")'],
        ['ZeroDivisionError', '除以零', '1 / 0'],
        ['AttributeError', '对象没有这个属性', 'None.upper()'],
        ['ImportError', '导入模块失败', 'import not_exist'],
        ['NameError', '使用未定义的变量', 'print(x)'],
        ['SyntaxError', '语法错误（无法被捕获）', 'if True print("x")'],
    ]
)

doc.add_heading('7.3 raise 抛出异常', level=2)
doc.add_paragraph('使用 raise 可以主动抛出异常，当检测到不符合预期的输入或状态时使用：')
add_code(doc,
    'def validate_age(age):\n'
    '    if age < 0:\n'
    '        raise ValueError("年龄不能为负数！")\n'
    '    if age > 150:\n'
    '        raise ValueError(f"年龄 {age} 不合理")\n'
    '    return age\n\n'
    'try:\n'
    '    validate_age(-5)\n'
    'except ValueError as e:\n'
    '    print(f"验证失败：{e}")',
    'raise 抛出异常'
)

doc.add_heading('7.4 自定义异常', level=2)
add_code(doc,
    'class InsufficientBalanceError(Exception):\n'
    '    """余额不足异常"""\n'
    '    def __init__(self, balance, amount):\n'
    '        self.balance = balance\n'
    '        self.amount = amount\n'
    '        super().__init__(f"余额{balance}元，无法取出{amount}元")\n\n'
    '# 使用自定义异常\n'
    'def withdraw(balance, amount):\n'
    '    if amount > balance:\n'
    '        raise InsufficientBalanceError(balance, amount)\n'
    '    return balance - amount\n\n'
    'try:\n'
    '    withdraw(100, 500)\n'
    'except InsufficientBalanceError as e:\n'
    '    print(f"取款失败：{e}")',
    '自定义异常'
)

doc.add_page_break()

# ===== 八、文件读写 =====
doc.add_heading('八、文件读写', level=1)

doc.add_heading('8.1 文件打开与关闭', level=2)
doc.add_paragraph('open() 函数用于打开文件，返回一个文件对象。操作完成后必须用 close() 关闭。')
add_code(doc,
    '# open(filename, mode, encoding)\n'
    '# mode 的第一个字母表示操作类型\n\n'
    '# "r" — 只读（文件必须存在）\n'
    'f = open("test.txt", "r", encoding="utf-8")\n'
    '# ... 读取操作 ...\n'
    'f.close()\n\n'
    '# "w" — 只写（文件不存在则创建，存在则清空内容）\n'
    'f = open("output.txt", "w", encoding="utf-8")\n'
    'f.write("Hello World\\n")\n'
    'f.close()\n\n'
    '# "a" — 追加（在文件末尾添加，不会清空）\n'
    'f = open("log.txt", "a", encoding="utf-8")\n'
    'f.write("新的一行\\n")\n'
    'f.close()\n\n'
    '# "x" — 创建新文件（文件不存在才创建，存在会报错）\n'
    '# "b" — 二进制模式（如图片、视频等）\n'
    '# "t" — 文本模式（默认，等同于不写）',
    '文件打开模式'
)
add_warn(doc, '用 "w" 模式打开已有文件会清空原文件内容！如果不确定文件是否有用，先用 "a" 或 "x" 模式。')

doc.add_heading('8.2 文件读写操作', level=2)
add_code(doc,
    '# 写文件\n'
    'with open("test.txt", "w", encoding="utf-8") as f:\n'
    '    f.write("第一行\\n")\n'
    '    f.write("第二行\\n")\n'
    '    f.writelines(["第三行\\n", "第四行\\n"])  # 写入多行\n\n'
    '# 读文件\n'
    'with open("test.txt", "r", encoding="utf-8") as f:\n'
    '    # 方法1：一次性读取全部\n'
    '    content = f.read()\n\n'
    '# with open("test.txt", "r", encoding="utf-8") as f:\n'
    '    # 方法2：读取所有行（返回列表）\n'
    '    # lines = f.readlines()\n\n'
    '# with open("test.txt", "r", encoding="utf-8") as f:\n'
    '    # 方法3：逐行读取（最省内存）\n'
    '    # for line in f:\n'
    '    #     print(line.strip())',
    '文件读写完整示例'
)

doc.add_heading('8.3 上下文管理器 with 语句 ⭐', level=2)
doc.add_paragraph('with 语句自动管理资源的打开和关闭，即使发生异常也能确保文件被正确关闭。')
add_code(doc,
    '# ✅ 推荐：使用 with（自动关闭文件）\n'
    'with open("file.txt", "r", encoding="utf-8") as f:\n'
    '    content = f.read()\n'
    '    # 处理 content...\n'
    '# 退出 with 块时，文件自动关闭，即使中途出错！\n\n'
    '# ❌ 不推荐：手动 close（容易忘记，异常时不会关闭）\n'
    'f = open("file.txt", "r", encoding="utf-8")\n'
    'content = f.read()\n'
    'f.close()  # 如果上面抛出异常，这行不会执行',
    'with 语句 vs 手动关闭'
)
add_tip(doc, '永远使用 with 语句处理文件！这是 Python 的最佳实践，也是面试中经常被问到的问题。')

doc.add_heading('8.4 文件路径与编码', level=2)
doc.add_paragraph('编码（encoding）决定了如何把字符转为字节。中文 Windows 默认使用 GBK，但推荐明确指定 UTF-8：')
add_code(doc,
    '# 跨平台友好的写法\n'
    'from pathlib import Path\n\n'
    'file_path = Path("data") / "scores.txt"\n'
    'file_path.parent.mkdir(parents=True, exist_ok=True)  # 确保目录存在\n\n'
    'with open(file_path, "w", encoding="utf-8") as f:\n'
    '    f.write("姓名,分数\\n")\n'
    '    f.write("小明,85\\n")\n\n'
    '# 读取时指定相同编码\n'
    'with open(file_path, "r", encoding="utf-8") as f:\n'
    '    print(f.read())',
    '路径与编码'
)
add_warn(doc, 'Windows 记事本创建的文本文件默认是 GBK 编码。如果用 Python 打开中文文件报 UnicodeDecodeError，试试 encoding="gbk"。')

doc.add_page_break()

# ===== 九、CSV 文件 =====
doc.add_heading('九、CSV 文件读写', level=1)
doc.add_paragraph('CSV（Comma-Separated Values）是用逗号分隔数据的纯文本格式，表格软件和数据库都支持。')
add_code(doc,
    'import csv\n\n'
    '# 写入 CSV\n'
    'with open("students.csv", "w", newline="", encoding="utf-8-sig") as f:\n'
    '    writer = csv.writer(f)\n'
    '    writer.writerow(["姓名", "年龄", "分数"])  # 写表头\n'
    '    writer.writerow(["小明", 19, 85])\n'
    '    writer.writerow(["小红", 20, 92])\n'
    '    writer.writerows([["小刚", 18, 78], ["小丽", 19, 88]])  # 写多行\n\n'
    '# 读取 CSV\n'
    'with open("students.csv", "r", encoding="utf-8-sig") as f:\n'
    '    reader = csv.reader(f)\n'
    '    for row in reader:\n'
    '        print(row)  # [\'姓名\', \'年龄\', \'分数\'] ...\n\n'
    '# DictWriter / DictReader：用字典方式操作（更直观）\n'
    'with open("students.csv", "w", newline="", encoding="utf-8-sig") as f:\n'
    '    fieldnames = ["姓名", "年龄", "分数"]\n'
    '    writer = csv.DictWriter(f, fieldnames=fieldnames)\n'
    '    writer.writeheader()\n'
    '    writer.writerow({"姓名": "小明", "年龄": 19, "分数": 85})\n\n'
    'with open("students.csv", "r", encoding="utf-8-sig") as f:\n'
    '    reader = csv.DictReader(f)\n'
    '    for row in reader:\n'
    '        print(f"{row[\'姓名\']}: {row[\'分数\']}分")',
    'CSV 读写完整示例'
)
add_tip(doc, 'newline="" 保证换行符正确；encoding="utf-8-sig" 让 Excel 双击打开 CSV 不会乱码（带 BOM 标记）。')

doc.add_page_break()

# ===== 十、JSON 文件 =====
doc.add_heading('十、JSON 文件读写', level=1)
doc.add_paragraph('JSON（JavaScript Object Notation）是当前最流行的数据交换格式，几乎所有 API 都用它传输数据。')
add_code(doc,
    'import json\n\n'
    '# Python 字典/列表 → JSON 文件（序列化/导出）\n'
    'data = {\n'
    '    "game": "原神",\n'
    '    "characters": ["刻晴", "甘雨", "钟离"],\n'
    '    "stats": {"level": 60, "adventure_rank": 55}\n'
    '}\n'
    'with open("game_data.json", "w", encoding="utf-8") as f:\n'
    '    json.dump(data, f, ensure_ascii=False, indent=2)\n\n'
    '# JSON 文件 → Python 对象（反序列化/导入）\n'
    'with open("game_data.json", "r", encoding="utf-8") as f:\n'
    '    loaded = json.load(f)\n'
    '    print(loaded["characters"][0])  # 刻晴\n\n'
    '# json.dumps() / json.loads()：处理字符串（不从文件）\n'
    'json_str = json.dumps(data, ensure_ascii=False)  # 对象→字符串\n'
    'parsed = json.loads(json_str)                     # 字符串→对象',
    'JSON 文件读写'
)
add_table(doc,
    ['函数', '操作', '方向'],
    [
        ['json.dump(obj, file)', '把 Python 对象写入 JSON 文件', '对象 → 文件'],
        ['json.load(file)', '从 JSON 文件读取为 Python 对象', '文件 → 对象'],
        ['json.dumps(obj)', '把 Python 对象转为 JSON 字符串', '对象 → 字符串'],
        ['json.loads(str)', '把 JSON 字符串解析为 Python 对象', '字符串 → 对象'],
    ]
)

doc.add_page_break()

# ===== 十一、综合练习 =====
doc.add_heading('十一、综合练习', level=1)

doc.add_heading('练习 1：图书管理系统', level=2)
doc.add_paragraph('用 OOP 设计一个简单的图书管理系统，包含 Book 类和 Library 类：')
add_code(doc,
    'class Book:\n'
    '    def __init__(self, title, author, isbn):\n'
    '        self.title = title\n'
    '        self.author = author\n'
    '        self.isbn = isbn\n'
    '        self.is_borrowed = False\n\n'
    '    def __str__(self):\n'
    '        status = "已借出" if self.is_borrowed else "可借阅"\n'
    '        return f"《{self.title}》— {self.author} [{status}]"\n\n'
    'class Library:\n'
    '    def __init__(self):\n'
    '        self.books = []\n\n'
    '    def add_book(self, book):\n'
    '        self.books.append(book)\n\n'
    '    def borrow(self, title):\n'
    '        for book in self.books:\n'
    '            if book.title == title and not book.is_borrowed:\n'
    '                book.is_borrowed = True\n'
    '                return f"借阅成功：《{title}》"\n'
    '        return f"借阅失败：{title}"\n\n'
    '    def list_books(self):\n'
    '        for book in self.books:\n'
    '            print(book)',
    '图书管理系统'
)

doc.add_heading('练习 2：日志文件分析器', level=2)
doc.add_paragraph('读取一个游戏日志文件，统计错误数量和类型：')
add_code(doc,
    'def analyze_log(filepath):\n'
    '    """分析日志文件中的错误"""\n'
    '    errors = {"ERROR": 0, "WARNING": 0, "FATAL": 0}\n'
    '    try:\n'
    '        with open(filepath, "r", encoding="utf-8") as f:\n'
    '            for line in f:\n'
    '                for level in errors:\n'
    '                    if level in line:\n'
    '                        errors[level] += 1\n'
    '    except FileNotFoundError:\n'
    '        print(f"文件不存在：{filepath}")\n'
    '        return None\n'
    '    return errors\n\n'
    '# 生成模拟日志并分析\n'
    'log_content = """\n'
    '2026-08-08 10:00:01 INFO 游戏启动\n'
    '2026-08-08 10:00:05 WARNING 内存使用率85%\n'
    '2026-08-08 10:05:30 ERROR 连接超时\n'
    '2026-08-08 10:06:00 ERROR 数据加载失败\n'
    '2026-08-08 10:10:00 FATAL 客户端崩溃\n'
    '"""\n'
    'with open("game.log", "w", encoding="utf-8") as f:\n'
    '    f.write(log_content)\n\n'
    'result = analyze_log("game.log")\n'
    'print(result)  # {\'ERROR\': 2, \'WARNING\': 1, \'FATAL\': 1}',
    '日志文件分析器'
)

doc.add_page_break()

# ===== 十二、检查清单 =====
doc.add_heading('十二、本日学习检查清单 ✅', level=1)
doc.add_paragraph('□ 理解面向对象和面向过程的区别及适用场景')
doc.add_paragraph('□ 能在 Python 中定义类并创建对象')
doc.add_paragraph('□ 理解 self 的作用 — 指向调用方法的对象本身')
doc.add_paragraph('□ 能区分对象属性（self.xxx）和类属性')
doc.add_paragraph('□ 会使用 __init__ 初始化对象属性（有参/无参）')
doc.add_paragraph('□ 会重写 __str__ 和 __repr__ 让 print 更友好')
doc.add_paragraph('□ 理解封装的理念 — 私有属性 + 公开接口')
doc.add_paragraph('□ 会用 @property 装饰器创建计算属性')
doc.add_paragraph('□ 掌握单继承的语法：class Son(Father)')
doc.add_paragraph('□ 能在子类中通过 super() 调用父类方法')
doc.add_paragraph('□ 理解多继承和 MRO（方法解析顺序）')
doc.add_paragraph('□ 理解多态的条件：继承 + 重写 + 父类引用指向子类对象')
doc.add_paragraph('□ 知道 @classmethod 和 @staticmethod 的区别和用法')
doc.add_paragraph('□ 了解抽象类 ABC 的概念')
doc.add_paragraph('□ 完成游戏角色类体系设计练习')
doc.add_paragraph('□ 掌握 try/except/else/finally 的完整结构')
doc.add_paragraph('□ 熟记常见异常类型（ValueError, TypeError, KeyError 等）')
doc.add_paragraph('□ 能使用 raise 主动抛出异常')
doc.add_paragraph('□ 了解如何自定义异常类')
doc.add_paragraph('□ 理解文件打开模式 r/w/a/x/b/t 的含义')
doc.add_paragraph('□ 能用 with 语句安全地读写文件')
doc.add_paragraph('□ 能处理文件编码问题（utf-8 vs gbk）')
doc.add_paragraph('□ 会读写 CSV 文件（csv.reader / csv.writer）')
doc.add_paragraph('□ 会读写 JSON 文件（json.load / json.dump）')

output_path = r'D:\NoteBook\Day4_学习笔记_面向对象编程与异常处理.docx'
doc.save(output_path)
print(f"Day 4 saved: {output_path}")

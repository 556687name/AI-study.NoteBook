#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成《40天学习计划 · 视频观看清单》Word 文档"""

from docx import Document
from docx.shared import Pt, RGBColor
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
        hs.font.size = Pt(18); hs.font.color.rgb = RGBColor(0x1A, 0x56, 0xDB)
    elif i == 2:
        hs.font.size = Pt(15); hs.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)
    elif i == 3:
        hs.font.size = Pt(13); hs.font.color.rgb = RGBColor(0x34, 0x49, 0x5E)


def add_hyperlink(paragraph, url, text, color="0563C1"):
    """在段落中插入可点击的超链接"""
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)
    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    c = OxmlElement('w:color'); c.set(qn('w:val'), color); rPr.append(c)
    u = OxmlElement('w:u'); u.set(qn('w:val'), 'single'); rPr.append(u)
    sz = OxmlElement('w:sz'); sz.set(qn('w:val'), '20'); rPr.append(sz)
    new_run.append(rPr)
    t = OxmlElement('w:t'); t.text = text; new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)
    return hyperlink


def add_video_row(title, url, note=""):
    """添加一条视频：加粗标题 + 可点击链接 + 可选备注"""
    p = doc.add_paragraph()
    r = p.add_run(f"▶ {title}")
    r.bold = True; r.font.size = Pt(11)
    p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(0)
    p2 = doc.add_paragraph()
    p2.paragraph_format.left_indent = Pt(18)
    p2.paragraph_format.space_before = Pt(0); p2.paragraph_format.space_after = Pt(0)
    r2 = p2.add_run("链接："); r2.font.size = Pt(10); r2.font.color.rgb = RGBColor(0x7F, 0x8C, 0x8D)
    add_hyperlink(p2, url, url)
    if note:
        p3 = doc.add_paragraph()
        p3.paragraph_format.left_indent = Pt(18)
        p3.paragraph_format.space_before = Pt(0); p3.paragraph_format.space_after = Pt(0)
        r3 = p3.add_run(note); r3.font.size = Pt(10); r3.font.color.rgb = RGBColor(0x66, 0x66, 0x66)


def add_tip(text):
    p = doc.add_paragraph()
    r = p.add_run(f"💡 提示：{text}")
    r.font.size = Pt(10); r.font.color.rgb = RGBColor(0xE6, 0x7E, 0x22); r.italic = True


def add_warn(text):
    p = doc.add_paragraph()
    r = p.add_run(f"⚠️ 注意：{text}")
    r.font.size = Pt(10); r.font.color.rgb = RGBColor(0xE7, 0x4C, 0x3C); r.bold = True


# ===== 封面 =====
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_before = Pt(90)
r = p.add_run("暑假 40 天学习计划"); r.font.size = Pt(30); r.font.color.rgb = RGBColor(0x1A, 0x56, 0xDB); r.bold = True
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("视频观看清单（含链接）"); r.font.size = Pt(22); r.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_before = Pt(30)
r = p.add_run("整理自《暑假40天学习计划_张豪实验室_米哈游游戏测试.docx》")
r.font.size = Pt(11); r.font.color.rgb = RGBColor(0x7F, 0x8C, 0x8D)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("覆盖：信息论 / 线性代数 / 微积分 / 机器学习 / 深度学习 / 联邦学习")
r.font.size = Pt(11); r.font.italic = True

doc.add_page_break()

# ===== 目录 =====
doc.add_heading('📑 目录', level=1)
toc = [
    "第一部分：信息论（Day 9 重点）",
    "第二部分：线性代数（Day 10）",
    "第三部分：微积分与梯度（Day 10）",
    "第四部分：机器学习（Day 15 起）",
    "第五部分：深度学习 / PyTorch（Day 15 起）",
    "第六部分：联邦学习（Day 29 起）",
    "第七部分：观看优先级与时间安排",
]
for item in toc:
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2)
    r = p.add_run(item); r.font.size = Pt(11); r.bold = True

doc.add_page_break()

# ========================
# 第一部分：信息论
# ========================
doc.add_heading('第一部分：信息论（Day 9 重点）', level=1)
doc.add_paragraph('对应知识点：熵、交叉熵、KL 散度、互信息。这是张豪老师"信息瓶颈理论"研究的基础。')
doc.add_paragraph('计划未单独指定视频，最贴合的是 3Blue1Brown「压缩即智能 / 重新发明熵」系列（B站官方双语）。')

add_video_row(
    "3Blue1Brown 重新发明熵（压缩即智能 Part 1，官方双语）",
    "https://www.bilibili.com/video/av116913858418468",
    "约 32 分钟，从香农猜字母实验讲起，讲透熵、信息量、交叉熵与大模型预训练的内在联系。"
)
add_video_row(
    "同系列另一版（BV 号，中文标题：信息论之父香农：压缩=智能？）",
    "https://www.bilibili.com/video/BV1FLMJ6VExg/",
    "与上一条同一内容的不同上传版本，可互为备份。"
)
add_warn("互信息：3Blue1Brown 官方未见单独一集，建议用吴恩达/李沐课程中「交叉熵、KL散度」的章节补充互信息概念。")

doc.add_page_break()

# ========================
# 第二部分：线性代数
# ========================
doc.add_heading('第二部分：线性代数（Day 10）', level=1)
doc.add_paragraph('主合集：《线性代数的本质》官方双语合集（3Blue1Brown）。')
add_video_row("《线性代数的本质》官方双语合集", "https://www.bilibili.com/video/av6731067/")

doc.add_heading('知识点 → 分集对照', level=2)
doc.add_paragraph('● 向量、点积 → 07 点积与对偶性')
add_video_row("07 点积与对偶性", "https://www.bilibili.com/video/BV1ys411472E/?p=10")
doc.add_paragraph('● 线性变换的几何理解 → 03 矩阵与线性变换')
add_video_row("03 矩阵与线性变换", "https://www.bilibili.com/video/BV1ys411472E/?p=4")
doc.add_paragraph('● 矩阵乘法 → 04 矩阵乘法与线性变换复合')
add_video_row("04 矩阵乘法与线性变换复合", "https://www.bilibili.com/video/BV1ys411472E/?p=5")
doc.add_paragraph('● 特征值与特征向量 → 10 特征向量与特征值')
add_video_row("10 特征向量与特征值（P14）", "https://www.bilibili.com/video/BV1ys411472E/?p=14")
doc.add_paragraph('● 基变换（PCA 思想基础）→ 09 基变换')
add_video_row("09 基变换", "https://www.bilibili.com/video/BV1ys411472E/?p=13")

add_warn("SVD / PCA 降维：3Blue1Brown 线代系列没有单独讲 SVD 和 PCA，最接近的基础是「特征值（P14）」+「基变换（P13）」两集。Day 10 下午更主要是用 NumPy 自己实现 PCA。")

doc.add_page_break()

# ========================
# 第三部分：微积分
# ========================
doc.add_heading('第三部分：微积分与梯度（Day 10）', level=1)
doc.add_paragraph('对应知识点：梯度、Jacobian 矩阵、Hessian 矩阵（线代系列未覆盖）。')

add_video_row(
    "《微积分的本质》官方双语合集（梯度、导数直观）",
    "https://www.bilibili.com/video/av24325548/",
    "覆盖一元微积分：导数、链式法则、泰勒级数等，是理解梯度的基础。"
)
add_video_row(
    "多元微积分 part11：线性变换与雅可比矩阵",
    "https://www.bilibili.com/video/av590724682/",
    "重点看 11.3 什么是雅可比矩阵、11.4 计算雅可比矩阵。"
)
add_warn("Hessian 矩阵：3Blue1Brown 没有专门一集，把「高阶导数」那集 + Jacobian 看懂后自然能推，属于二阶导推广。")

doc.add_page_break()

# ========================
# 第四部分：机器学习
# ========================
doc.add_heading('第四部分：机器学习（Day 15 起）', level=1)
doc.add_paragraph('计划推荐：吴恩达《机器学习》，看前 5 周即可。')

add_video_row(
    "吴恩达 2025 机器学习（斯坦福·中英字幕，136集）",
    "https://www.bilibili.com/video/BV13PemzREpa/",
    "完整版+配套教程，B站推荐度最高的版本之一。"
)
add_video_row(
    "吴恩达机器学习（中英完结，99集，附课件+代码）",
    "https://www.bilibili.com/video/BV1T8HCzME3d/",
    "附课件 PPT + 作业 + 代码习题，适合新手入门。"
)

doc.add_page_break()

# ========================
# 第五部分：深度学习
# ========================
doc.add_heading('第五部分：深度学习 / PyTorch（Day 15 起）', level=1)

add_video_row(
    "李沐《动手学深度学习 v2》官方合集（跟李沐学AI）",
    "https://space.bilibili.com/1567748478/channel/seriesdetail?sid=358497",
    "PyTorch 版，代码 + 理论并重，计划推荐。"
)
add_video_row(
    "PyTorch 60 分钟入门（官网英文，计划必看）",
    "https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html",
    "官方 60min blitz，覆盖 Tensor / Autograd / 神经网络 / 训练分类器。"
)
add_video_row(
    "PyTorch 60min 中文翻译（GitHub）",
    "https://github.com/bat67/Deep-Learning-with-PyTorch-A-60-Minute-Blitz-cn",
    "官网教程的中文翻译版，含章节整理。"
)

doc.add_page_break()

# ========================
# 第六部分：联邦学习
# ========================
doc.add_heading('第六部分：联邦学习（Day 29 起）', level=1)
doc.add_paragraph('计划指定：观看联邦学习入门视频（推荐杨强教授的报告）。')

add_video_row(
    "杨强《可信联邦学习》演讲（B站）",
    "https://www.bilibili.com/video/BV1GY4y1q7ek",
    "机器之心 AI 科技年会，系统回顾联邦学习进展与挑战。"
)
add_video_row(
    "杨强《可信联邦学习与开源生态》演讲（腾讯云）",
    "https://cloud.tencent.com.cn/developer/article/2257238",
    "介绍 FATE 开源社区，讲开源对隐私计算的重要性。"
)
add_video_row(
    "FATE 联邦学习开源框架（跑 demo 用）",
    "https://github.com/FederatedAI/FATE",
    "计划资源清单中的 FL 框架，可跑 demo。"
)

doc.add_page_break()

# ========================
# 第七部分：观看优先级
# ========================
doc.add_heading('第七部分：观看优先级与时间安排', level=1)
doc.add_paragraph('以下按 40 天时间线排出的观看顺序，每天控制视频在 2~2.5 小时内，其余时间留给代码练习。')

order = [
    ("Day 9", "3B1B 重新发明熵", "30 分钟，直接对应熵/交叉熵"),
    ("Day 10 上午", "03 矩阵与线性变换 → 04 矩阵乘法 → 07 点积与对偶性 → 10 特征值与特征值", "线性代数主线"),
    ("Day 10 下午", "09 基变换 → Jacobian 合集 11.3 / 11.4", "PCA 与梯度/雅可比"),
    ("Day 15+", "吴恩达机器学习前几周", "ML 主线"),
    ("Day 16", "PyTorch 60min", "必看，代码入门"),
    ("Day 17+", "李沐《动手学深度学习》", "MLP / CNN / Transformer 章节"),
    ("Day 29", "杨强联邦学习报告", "联邦学习入门"),
]

t = doc.add_table(rows=1 + len(order), cols=3)
t.style = 'Light Grid Accent 1'
headers = ['时间节点', '观看内容', '说明']
for i, h in enumerate(headers):
    c = t.rows[0].cells[i]; c.text = h
    for pp in c.paragraphs:
        pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for rr in pp.runs: rr.bold = True; rr.font.size = Pt(10)
for ri, row in enumerate(order):
    for ci, val in enumerate(row):
        c = t.rows[ri + 1].cells[ci]; c.text = str(val)
        for pp in c.paragraphs:
            for rr in pp.runs: rr.font.size = Pt(10)

doc.add_paragraph()
add_tip("视频是辅助理解，计划的重点是「用 NumPy / PyTorch 自己实现」。看完每部分一定要动手写代码验证。")

output_path = r'D:\NoteBook\视频观看清单（信息论·数学·ML·DL·联邦学习）.docx'
doc.save(output_path)
print(f"Saved: {output_path}")

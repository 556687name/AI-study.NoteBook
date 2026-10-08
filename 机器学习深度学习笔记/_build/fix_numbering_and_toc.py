# -*- coding: utf-8 -*-
"""修复 ch8/ch16 小节编号重复 + 全面同步目录的小节列表。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import load_nb, save_json

NB = r"D:\NoteBook\机器学习深度学习笔记\机器学习深度学习完整笔记.ipynb"
nb = load_nb(NB)

# ---------- 1. 修复正文重复编号 ----------
def fix_header(old, new):
    for c in nb["cells"]:
        if c["cell_type"] != "markdown":
            continue
        src = "".join(c["source"])
        if src.lstrip().startswith(old):
            c["source"] = src.replace(old, new, 1).splitlines(keepends=True)
            print(f"  正文编号修复: {old} -> {new}")
            return
    print(f"  !! 未找到 {old}")

fix_header("## 8.9 【李沐 d2l】权重衰减与 Dropout 的 PyTorch 实现",
           "## 8.8 【李沐 d2l】权重衰减与 Dropout 的 PyTorch 实现")
fix_header("## 16.8 【李沐 d2l】深度学习计算：自定义块、参数管理、读写模型",
           "## 16.7 【李沐 d2l】深度学习计算：自定义块、参数管理、读写模型")

# ---------- 2. 同步目录 ----------
toc_idx = 2
src = "".join(nb["cells"][toc_idx]["source"])

repls = [
    # ch4
    ("- 4.5 sklearn 实战：LinearRegression\n- 4.6 本章小结",
     "- 4.5 sklearn 实战：LinearRegression\n- 4.6 线性回归从零实现（李沐 d2l）\n- 4.7 线性回归简洁实现（李沐 d2l）\n- 4.8 本章小结"),
    # ch8
    ("- 8.7 早停 Early Stopping\n- 8.8 本章小结",
     "- 8.7 早停 Early Stopping\n- 8.8 权重衰减与 Dropout 的 PyTorch 实现（李沐 d2l）\n- 8.9 本章小结"),
    # ch9
    ("- 9.6 sklearn 实战\n- 9.7 本章小结",
     "- 9.6 sklearn 实战\n- 9.7 softmax 从零实现（李沐 d2l）\n- 9.8 softmax 简洁实现（李沐 d2l）\n- 9.9 本章小结"),
    # ch11
    ("- 11.6 梯度消失与梯度爆炸\n- 11.7 本章小结",
     "- 11.6 梯度消失与梯度爆炸\n- 11.7 多层感知机 MLP：从零与简洁实现（李沐 d2l）\n- 11.8 本章小结"),
    # ch14
    ("- 14.4 Autograd 三个关键细节\n- 14.5 本章小结",
     "- 14.4 Autograd 三个关键细节\n- 14.5 预备知识·线性代数（李沐 d2l）\n- 14.6 预备知识·概率（李沐 d2l）\n- 14.7 数据预处理与查阅文档（李沐 d2l）\n- 14.8 本章小结"),
    # ch15
    ("- 15.4 图像数据标准流水线\n- 15.5 本章小结",
     "- 15.4 图像数据标准流水线\n- 15.5 图像增广：翻转/裁剪/颜色抖动（李沐 d2l）\n- 15.6 本章小结"),
    # ch16
    ("- 16.6 保存与加载 checkpoint\n- 16.7 本章小结",
     "- 16.6 保存与加载 checkpoint\n- 16.7 深度学习计算：自定义块/参数管理/读写模型（李沐 d2l）\n- 16.8 本章小结"),
]

for old, new in repls:
    if old in src:
        src = src.replace(old, new, 1)
        print(f"  目录同步: {old.splitlines()[0]} ...")
    else:
        print(f"  !! 目录未匹配: {old.splitlines()[0]} ...")

nb["cells"][toc_idx]["source"] = src.splitlines(keepends=True)
save_json(nb, NB)
print("编号修复 + 目录同步完成 ✔")

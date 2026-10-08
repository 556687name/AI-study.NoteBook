# -*- coding: utf-8 -*-
"""更新目录：第六章（+Adadelta/凸性）、第十三章（+注意力评分函数/Bahdanau）的小节重编号。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import load_nb, save_json

NB = r"D:\NoteBook\机器学习深度学习笔记\机器学习深度学习完整笔记.ipynb"
nb = load_nb(NB)

toc_idx = None
for i, c in enumerate(nb["cells"]):
    if "".join(c["source"]).strip().startswith("# 📑 目录"):
        toc_idx = i
        break
src = "".join(nb["cells"][toc_idx]["source"])

# 第六章
src = src.replace(
    """- 6.4 三种优化器：AdaGrad / RMSProp / Adam
- 6.5 学习率调度
- 6.6 本章小结""",
    """- 6.4 三种优化器：AdaGrad / RMSProp / Adam
- 6.5 学习率调度
- 6.6 Adadelta：连学习率都不用设（李沐 d2l）
- 6.7 凸性：为什么凸优化能保证收敛（李沐 d2l）
- 6.8 本章小结"""
)

# 第十三章
src = src.replace(
    """- 13.6 Transformer 完整结构
- 13.7 本章小结""",
    """- 13.6 Transformer 完整结构
- 13.7 注意力评分函数：加性 vs 缩放点积（李沐 d2l）
- 13.8 Bahdanau 注意力：注意力用于 seq2seq（李沐 d2l）
- 13.9 本章小结"""
)

nb["cells"][toc_idx]["source"] = src
save_json(nb, NB)
print("目录更新完成 ✔ (第6/13章小节)")

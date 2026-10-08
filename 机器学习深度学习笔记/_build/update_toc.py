# -*- coding: utf-8 -*-
"""更新主笔记目录：修正章节总数、补 ch12 现代 CNN 小节、新增第20/21章。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import load_nb, save_json

NB = r"D:\NoteBook\机器学习深度学习笔记\机器学习深度学习完整笔记.ipynb"
nb = load_nb(NB)

# 定位目录 cell（以 '# 📑 目录' 开头的 markdown cell）
toc_idx = None
for i, c in enumerate(nb["cells"]):
    if "".join(c["source"]).strip().startswith("# 📑 目录"):
        toc_idx = i
        break
assert toc_idx is not None

src = "".join(nb["cells"][toc_idx]["source"])

# 1) 更新总数与说明
src = src.replace(
    "「机器学习基础 → 深度学习 → PyTorch 实战」三部分，外加附录。共 **19 章 + 附录**。",
    "「机器学习基础 → 深度学习 → PyTorch 实战」三部分，外加「李沐 d2l 补充章节」和附录。共 **21 章 + 附录**。"
)
src = src.replace(
    "方便回到 B 站对照原视频。",
    "方便回到 B 站对照原视频；标注「李沐《动手学深度学习 V2》」的小节为后续融合进来的补充内容，配套代码在 `实战代码_李沐/` 文件夹。"
)

# 2) 补 ch12 现代 CNN 小节
src = src.replace(
    """- 12.5 经典结构：LeNet
- 12.6 ResNet 与残差连接
- 12.7 本章小结""",
    """- 12.5 经典结构：LeNet
- 12.6~12.12 现代 CNN（李沐 d2l）：AlexNet / VGG / NiN / GoogLeNet / BatchNorm / ResNet / DenseNet
- 12.13 本章小结"""
)

# 3) 在「## 附录」前插入第四部分（李沐 d2l 补充章节）
new_block = """---

## 第四部分 · 李沐《动手学深度学习 V2》补充章节

> 以下章节为李沐 d2l 的补充内容（现有笔记原缺），逻辑上属于「深度学习」（RNN 是序列模型，位于 CNN 与 Transformer 之间），编号接在现有章节之后、放在附录之前。

**第二十章 循环神经网络 RNN**（d2l 第 8 章）
- 20.1 为什么需要 RNN：处理「序列」数据
- 20.2 循环结构：隐藏状态 + 参数共享
- 20.3 从零 vs 简洁实现
- 20.4 通过时间反向传播 BPTT

**第二十一章 现代循环神经网络：GRU / LSTM / seq2seq**（d2l 第 9 章）
- 21.1 为什么要「门」：RNN 记不住长依赖
- 21.2 GRU（门控循环单元）
- 21.3 LSTM（长短期记忆网络）
- 21.4 seq2seq 与机器翻译

---

## 附录"""

src = src.replace("\n---\n\n## 附录", new_block, 1)

# 写回
nb["cells"][toc_idx]["source"] = src
save_json(nb, NB)
print("目录更新完成 ✔")

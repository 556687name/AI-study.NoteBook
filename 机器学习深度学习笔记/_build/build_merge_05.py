# -*- coding: utf-8 -*-
"""批次5融合：李沐 d2l 注意力评分函数/Bahdanau 注意力 → 第十三章；Adadelta/凸性 → 第六章。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, load_nb, save_json

NB = r"D:\NoteBook\机器学习深度学习笔记\机器学习深度学习完整笔记.ipynb"
nb = load_nb(NB)
cells = nb["cells"]

# ---- 第十三章：插入注意力评分函数 + Bahdanau 注意力，小结重编号 ----
sec_att = md("""## 13.7 注意力评分函数：加性 vs 缩放点积（李沐 d2l 第 10 章）

> 📌 **出处**：李沐《动手学深度学习 V2》第 10 章「注意力评分函数」

13.2 讲的注意力用**点积**算 Query 和 Key 的相似度（「缩放点积注意力」）。但「相似度」有多种算法，统称**注意力评分函数** $a(\\mathbf{q}, \\mathbf{k})$。最常见两种：

**① 加性注意力（Additive Attention，Bahdanau）**

$$a(\\mathbf{q}, \\mathbf{k}) = \\mathbf{w}_v^\\top \\tanh(\\mathbf{W}_q \\mathbf{q} + \\mathbf{W}_k \\mathbf{k})$$

把 query 和 key 各过一个线性层相加，再 $\\tanh$，最后用向量 $\\mathbf{w}_v$ 打成分数。**query 和 key 维度可以不同**，适合序列到序列场景。

**② 缩放点积注意力（Scaled Dot-Product Attention）**

$$a(\\mathbf{q}, \\mathbf{k}) = \\frac{\\mathbf{q} \\cdot \\mathbf{k}}{\\sqrt{d}}$$

直接点积，再除以 $\\sqrt{d}$（$d$ 是维度）防止维度大时点积值过大、softmax 后梯度消失。**计算高效（矩阵乘法），是 Transformer 的选择**。

> 💡 **记忆**：**加性注意力 = 线性 + tanh + 打分**（灵活，维度可不同）；**缩放点积 = q·k/√d**（快，Transformer 用）。除 $\\sqrt{d}$ 是关键——不除的话大维度下 softmax 会饱和。

## 13.8 注意力在 seq2seq 中的应用：Bahdanau 注意力（李沐 d2l 第 10 章）

> 📌 **出处**：李沐《动手学深度学习 V2》第 10 章「Bahdanau 注意力」

第二十一章的 seq2seq 有个缺陷：解码器每一步只能用编码器**最后一个**隐藏状态，句子一长信息就「挤爆」。**Bahdanau 注意力**让解码器每一步都能「回看」编码器的**所有**位置：

- 解码器当前状态 $\\mathbf{q}$ 当 Query，编码器每个位置输出 $\\mathbf{k}_i$ 当 Key；
- 用**加性注意力**算出每个位置的相关分数 → softmax → 得到「该关注编码器哪些位置」的权重；
- 加权求和编码器的 Value，得到**上下文向量**，拼进解码器的输入。

效果：解码「翻译第 i 个词」时能自动对齐到源句里最相关的位置——**对齐（alignment）**。这是机器翻译的巨大进步，也是 Transformer「交叉注意力」的前身。
""")

sec_opt = md("""## 6.6 Adadelta：连学习率都不用设（李沐 d2l 第 11 章）

> 📌 **出处**：李沐《动手学深度学习 V2》第 11 章「Adadelta」

6.4 的三种优化器都要手设一个全局学习率。**Adadelta** 更进一步：**不设置学习率**，自己根据历史梯度自动调整步长。

它维护两个「指数滑动平均」——梯度的均方根 RMS 和参数更新量的均方根，用两者的比值来缩放更新：

$$\\mathbf{s}_t = \\rho\\, \\mathbf{s}_{t-1} + (1-\\rho)\\, \\mathbf{g}_t^2 \\quad\\text{（梯度平方的滑动平均）}$$

$$\\Delta\\mathbf{x}_t = -\\frac{\\text{RMS}[\\Delta\\mathbf{x}]_{t-1}}{\\text{RMS}[\\mathbf{g}]_t}\\, \\mathbf{g}_t \\quad\\text{（两个 RMS 之比，无需学习率）}$$

> 💡 相比 AdaGrad（累加所有历史，只增不减），Adadelta 用滑动平均只关注「近期」梯度；相比 RMSProp，Adadelta 把「学习率」也替换成了「历史更新量的 RMS 比」，完全消除了学习率这个超参数。

## 6.7 凸性：为什么凸优化能保证收敛到全局最优（李沐 d2l 第 11 章）

> 📌 **出处**：李沐《动手学深度学习 V2》第 11 章「凸性」

深度学习的目标函数通常**非凸**，但理解**凸性（convexity）**能帮我们判断「什么时候能放心收敛」。

- **凸函数**：定义域内任意两点连成的线段都在函数图像**上方**，即 $f(\\lambda x + (1-\\lambda)y) \\le \\lambda f(x) + (1-\\lambda)f(y)$；
- **凸函数的关键性质**：**局部最小值就是全局最小值**，梯度下降能保证收敛到全局最优；
- **线性回归的 MSE 是凸的**（所以正规方程能一步解出最优），但**神经网络的损失通常非凸**（有很多鞍点/局部最小）——这正是 6.2 讲「高维空间里鞍点才是主要麻烦」的理论背景。

> 💡 **记忆**：凸函数「局部最小 = 全局最小」；MSE 是凸的，神经网络损失非凸。判断是否凸，看二阶导（Hessian）是否半正定。
""")

def insert_before_section(section_header, new_cells, new_header):
    for i, c in enumerate(cells):
        src = "".join(c["source"])
        if src.strip().startswith(section_header):
            # 重命名小结标题
            c["source"] = src.replace(section_header, new_header, 1)
            # 在该 cell 前插入新 section
            cells[i:i] = new_cells
            return
    raise RuntimeError(f"未找到 {section_header}")

insert_before_section("## 13.7 本章小结", [sec_att], "## 13.9 本章小结")
insert_before_section("## 6.6 本章小结", [sec_opt], "## 6.8 本章小结")

save_json(nb, NB)
print("批次5融合完成 ✔ (第13章 +13.7/13.8；第6章 +6.6/6.7)")

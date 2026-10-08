# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# 注意力机制 Attention · 从零实现（PyTorch）

> 📌 **出处**：李沐《动手学深度学习 V2》第 10 章「注意力机制」
> 🎯 **目标**：手写**加性注意力**、**缩放点积注意力**、**多头注意力**、**自注意力 + 位置编码**，并可视化注意力权重，彻底搞懂 Transformer 的零件。

## 核心公式

$$\\text{Attention}(Q, K, V) = \\text{softmax}\\!\\left(\\frac{Q K^\\top}{\\sqrt{d_k}}\\right) V$$

- 用 Query 和每个 Key 算相似度（注意力评分函数）→ softmax 归一化成权重 → 加权求和 Value。
"""))

cells.append(code(ENV))

cells.append(code("""# ---- 工具导入 ----
import math
import torch.nn.functional as F
from torch import nn
"""))

cells.append(md("""## 1. 注意力机制的直觉：Nadaraya-Watson 核回归

注意力最早来自「非参数核回归」：预测某点的值时，**附近**的点权重更大。这里的「权重」就是注意力。
"""))

cells.append(code("""# ---- 用核回归演示：注意力 = 按相似度加权平均 ----
def nadaraya_watson(x_train, y_train, x_val, sigma=0.5):
    # 高斯核：key 与 query 的相似度 -> softmax 成权重 -> 加权平均 value
    dist = (x_val.reshape(-1, 1) - x_train.reshape(1, -1)) ** 2
    attn = np.exp(-dist / (2 * sigma ** 2))
    attn = attn / attn.sum(axis=1, keepdims=True)     # 归一化：就是 softmax(-dist/2σ²)
    return attn @ y_train, attn

x_train = np.sort(np.random.uniform(0, 10, 40))
y_train = np.sin(x_train) + np.random.randn(40) * 0.2
x_val = np.linspace(0, 10, 200)
y_pred, attn = nadaraya_watson(x_train, y_train, x_val)

import matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.scatter(x_train, y_train, s=15, label="训练点")
ax1.plot(x_val, y_pred, color=橙, lw=2, label="核回归预测")
ax1.set_title("注意力 = 相似度加权平均（拟合出正弦曲线）")
ax1.legend()
# 可视化某一点的注意力权重
q = 60
ax2.plot(x_train, attn[q], 'o-', color=蓝)
ax2.axvline(x_val[q], color=红, ls='--')
ax2.set_title(f"query={x_val[q]:.1f} 时，各 key 的注意力权重（靠近的高）")
plt.tight_layout(); plt.show()
"""))

cells.append(md("""## 2. 注意力评分函数：加性 vs 缩放点积

「相似度」有两种主流算法（对应笔记 13.7 节）。
"""))

cells.append(code("""# ---- ① 缩放点积注意力 ----
def scaled_dot_product_attention(Q, K, V, mask=None):
    d = Q.shape[-1]
    scores = Q @ K.transpose(-2, -1) / math.sqrt(d)   # 除以 √d 防梯度消失
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    attn = F.softmax(scores, dim=-1)
    return attn @ V, attn

# ---- ② 加性注意力（Bahdanau）----
class AdditiveAttention(nn.Module):
    def __init__(self, key_size, query_size, num_hiddens):
        super().__init__()
        self.W_k = nn.Linear(key_size, num_hiddens, bias=False)
        self.W_q = nn.Linear(query_size, num_hiddens, bias=False)
        self.w_v = nn.Linear(num_hiddens, 1, bias=False)
    def forward(self, queries, keys, values):
        # queries: (batch, num_q, q_size)；keys/values: (batch, num_k, k_size)
        features = self.W_q(queries).unsqueeze(2) + self.W_k(keys).unsqueeze(1)
        features = torch.tanh(features)
        scores = self.w_v(features).squeeze(-1)        # (batch, num_q, num_k)
        attn = F.softmax(scores, dim=-1)
        return torch.bmm(attn, values), attn

# 验证两者形状
Q = torch.rand(2, 5, 8); K = torch.rand(2, 6, 8); V = torch.rand(2, 6, 16)
out_dot, _ = scaled_dot_product_attention(Q, K, V)
out_add, _ = AdditiveAttention(8, 8, 32)(Q, K, V)
print("缩放点积输出：", tuple(out_dot.shape))   # (2, 5, 16)
print("加性注意力输出：", tuple(out_add.shape)) # (2, 5, 16)
"""))

cells.append(md("""## 3. 多头注意力：多角度「关注」

多组独立的 Q/K/V 投影并行做注意力，最后拼接，让每个位置从多个角度关注全局。
"""))

cells.append(code("""# ---- 多头注意力 ----
class MultiHeadAttention(nn.Module):
    def __init__(self, num_hiddens, num_heads, dropout=0.0):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = num_hiddens // num_heads
        self.W_q = nn.Linear(num_hiddens, num_hiddens)
        self.W_k = nn.Linear(num_hiddens, num_hiddens)
        self.W_v = nn.Linear(num_hiddens, num_hiddens)
        self.W_o = nn.Linear(num_hiddens, num_hiddens)
        self.dropout = nn.Dropout(dropout)

    def forward(self, queries, keys, values, mask=None):
        B, T, _ = queries.shape
        def split(x):
            return x.reshape(B, T, self.num_heads, self.head_dim).transpose(1, 2)  # (B, heads, T, head_dim)
        Q, K, V = split(self.W_q(queries)), split(self.W_k(keys)), split(self.W_v(values))
        scores = Q @ K.transpose(-2, -1) / math.sqrt(self.head_dim)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        attn = F.softmax(scores, dim=-1)
        attn = self.dropout(attn)
        out = (attn @ V).transpose(1, 2).reshape(B, T, -1)
        return self.W_o(out)

num_hiddens, num_heads = 64, 8
mha = MultiHeadAttention(num_hiddens, num_heads)
X = torch.rand(2, 10, num_hiddens)
out = mha(X, X, X)
print("多头注意力输出：", tuple(out.shape), "（不变输入形状，内部 8 个头并行）")
"""))

cells.append(md("""## 4. 自注意力 + 位置编码：让序列「互相看」且「记住顺序」

自注意力 = Q、K、V 都来自同一个序列。位置编码给每个位置加一个正弦/余弦向量，补上顺序信息。
"""))

cells.append(code("""# ---- 位置编码（原论文正弦/余弦）----
class PositionalEncoding(nn.Module):
    def __init__(self, num_hiddens, max_len=100):
        super().__init__()
        pe = torch.zeros(max_len, num_hiddens)
        position = torch.arange(max_len).float().unsqueeze(1)
        div = torch.exp(torch.arange(0, num_hiddens, 2).float() * (-math.log(10000.0) / num_hiddens))
        pe[:, 0::2] = torch.sin(position * div)   # 偶数位 sin
        pe[:, 1::2] = torch.cos(position * div)   # 奇数位 cos
        self.register_buffer('pe', pe.unsqueeze(0))
    def forward(self, X):
        return X + self.pe[:, :X.shape[1]]

# 可视化位置编码
pe = PositionalEncoding(64).pe[0].numpy()
plt.figure(figsize=(8, 3))
plt.imshow(pe[:30].T, aspect='auto', cmap='RdBu')
plt.xlabel("位置"); plt.ylabel("维度")
plt.title("位置编码：每个位置一个独特向量，不同维度是不同频率的 sin/cos")
plt.colorbar(); plt.show()

# 自注意力：Q=K=V
B, T = 2, 12
words = torch.rand(B, T, num_hiddens)
words_pe = PositionalEncoding(num_hiddens)(words)
attn = MultiHeadAttention(num_hiddens, 4)
out, _ = None, None  # 只看形状
out = attn(words_pe, words_pe, words_pe)
print("自注意力输出：", tuple(out.shape), "（每个位置都融合了全局信息 + 位置信息）")
"""))

cells.append(md("""## 5. 可视化：一句话里每个词「关注」谁

用缩放点积注意力算一句话里词与词的注意力权重矩阵，看看「它」是怎么自动指向「小明」的。
"""))

cells.append(code("""# ---- 词与词的注意力权重热力图 ----
词 = ['小明', '很', '聪明', '他', '考了', '第一']
d = 8
torch.manual_seed(1)
emb = torch.randn(len(词), d)               # 6 个词各一个向量
scores = emb @ emb.T / math.sqrt(d)
attn = F.softmax(scores, dim=-1).numpy()

fig, ax = plt.subplots(figsize=(5, 4))
im = ax.imshow(attn, cmap='Blues')
ax.set_xticks(range(len(词))); ax.set_xticklabels(词)
ax.set_yticks(range(len(词))); ax.set_yticklabels(词)
plt.setp(ax.get_xticklabels(), rotation=45)
for i in range(len(词)):
    for j in range(len(词)):
        ax.text(j, i, f"{attn[i, j]:.2f}", ha="center", va="center", fontsize=8)
plt.title("自注意力权重（每行是一个词对全句的关注）")
plt.colorbar(im); plt.show()
print("（真实模型里，权重是学出来的，会学到『他』重点关注『小明』）")
"""))

cells.append(md("""## 小结

| 概念 | 一句话直觉 |
| --- | --- |
| 注意力 | softmax(相似度) 加权求和 Value |
| 加性注意力 | 线性 + tanh + 打分（维度灵活） |
| 缩放点积 | QKᵀ/√d（快，Transformer 用） |
| 多头注意力 | 多组投影并行，多角度关注再拼接 |
| 位置编码 | sin/cos 向量补上「顺序」 |

> 🔑 **记忆**：注意力就一句话——**「按相似度加权求和」**。缩放点积注意力 + 多头 + 位置编码，就是 Transformer 的全部零件。下一节 `Transformer.ipynb` 把它们组装起来。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\注意力机制.ipynb", cells)
print("注意力机制 ✔")

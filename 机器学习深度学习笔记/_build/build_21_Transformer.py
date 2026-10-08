# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

CORPUS = """The Time Traveller (for so it will be convenient to speak of him) was expounding a recondite matter to us. His grey eyes shone and twinkled, and his usually pale face was flushed and animated. The fire burned brightly, and the soft radiance of the incandescent lights in the lilies of silver caught the bubbles that flashed and passed in our glasses.

Our chairs, being his patents, embraced and caressed us rather than submitted to be sat upon, and there was that luxurious after-dinner atmosphere when thought roams gracefully free of the trammels of precision. And he put it to us in this way, marking the points with a lean forefinger, as we sat and lazily admired his earnestness over this new paradox, as we thought it, and his fecundity.

You must follow me carefully. I shall have to controvert one or two ideas that are almost universally accepted. The geometry, for instance, they taught you at school is founded on a misconception."""

cells = []

cells.append(md("""# Transformer · 从零搭建 + 字符级语言模型（PyTorch）

> 📌 **出处**：李沐《动手学深度学习 V2》第 10 章「Transformer」
> 🎯 **目标**：把注意力零件**组装成 Transformer**——先搭完整编码器块并验证形状，再用「带因果掩码」的 Transformer 训练一个字符级语言模型（GPT 的核心思想）。

## Transformer 块 = 多头注意力 + FFN + 残差 + 层归一化

一个块依次做：**多头自注意力 → 残差+LayerNorm → 前馈网络 → 残差+LayerNorm**。
"""))

cells.append(code(ENV))

cells.append(code("""# ---- 零件 1：多头注意力 + 位置编码（见上一节）----
import math
import torch.nn.functional as F
from torch import nn

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
            return x.reshape(B, T, self.num_heads, self.head_dim).transpose(1, 2)
        Q, K, V = split(self.W_q(queries)), split(self.W_k(keys)), split(self.W_v(values))
        scores = Q @ K.transpose(-2, -1) / math.sqrt(self.head_dim)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        attn = F.softmax(scores, dim=-1)
        attn = self.dropout(attn)
        out = (attn @ V).transpose(1, 2).reshape(B, T, -1)
        return self.W_o(out)

class PositionalEncoding(nn.Module):
    def __init__(self, num_hiddens, max_len=100):
        super().__init__()
        pe = torch.zeros(max_len, num_hiddens)
        position = torch.arange(max_len).float().unsqueeze(1)
        div = torch.exp(torch.arange(0, num_hiddens, 2).float() * (-math.log(10000.0) / num_hiddens))
        pe[:, 0::2] = torch.sin(position * div)
        pe[:, 1::2] = torch.cos(position * div)
        self.register_buffer('pe', pe.unsqueeze(0))
    def forward(self, X):
        return X + self.pe[:, :X.shape[1]]
"""))

cells.append(md("""## 1. 残差 + 层归一化（Add & Norm）

Transformer 大量用**残差连接**（缓解梯度消失）+ **层归一化**（稳定训练）。
"""))

cells.append(code("""# ---- 零件 2：Add & Norm + 前馈网络 ----
class AddNorm(nn.Module):
    def __init__(self, norm_shape, dropout):
        super().__init__()
        self.ln = nn.LayerNorm(norm_shape)
        self.dropout = nn.Dropout(dropout)
    def forward(self, X, Y):
        return self.ln(self.dropout(Y) + X)     # 残差 + 归一化

class PositionWiseFFN(nn.Module):
    def __init__(self, num_hiddens, ffn_hiddens):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(num_hiddens, ffn_hiddens), nn.ReLU(),
                                 nn.Linear(ffn_hiddens, num_hiddens))
    def forward(self, X):
        return self.net(X)

class EncoderBlock(nn.Module):
    def __init__(self, num_hiddens, num_heads, ffn_hiddens, dropout):
        super().__init__()
        self.attention = MultiHeadAttention(num_hiddens, num_heads, dropout)
        self.addnorm1 = AddNorm(num_hiddens, dropout)
        self.ffn = PositionWiseFFN(num_hiddens, ffn_hiddens)
        self.addnorm2 = AddNorm(num_hiddens, dropout)
    def forward(self, X, mask=None):
        Y = self.addnorm1(X, self.attention(X, X, X, mask))   # 自注意力 + 残差归一化
        return self.addnorm2(Y, self.ffn(Y))                  # FFN + 残差归一化

class TransformerEncoder(nn.Module):
    def __init__(self, vocab_size, num_hiddens, num_heads, num_layers, ffn_hiddens, dropout):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, num_hiddens)
        self.pos_encoding = PositionalEncoding(num_hiddens)
        self.blks = nn.Sequential(*[EncoderBlock(num_hiddens, num_heads, ffn_hiddens, dropout)
                                    for _ in range(num_layers)])
    def forward(self, X, mask=None):
        X = self.pos_encoding(self.embedding(X))
        for blk in self.blks:
            X = blk(X, mask)
        return X

# 验证前向
enc = TransformerEncoder(vocab_size=37, num_hiddens=64, num_heads=4, num_layers=2, ffn_hiddens=128, dropout=0.1)
X = torch.randint(0, 37, (2, 10))
out = enc(X)
print("Transformer 编码器输出：", tuple(out.shape), "（2 句 × 10 词 × 64 维）")
print("参数量：", sum(p.numel() for p in enc.parameters()))
"""))

cells.append(md("""## 2. 因果掩码 + 字符级语言模型（GPT 的核心）

GPT 是「只用解码器」的 Transformer：预测下一个词时，**只能看左边的词**（不能偷看未来）。做法是给注意力加一个**下三角因果掩码**，把「未来位置」的分数设为 −∞。
"""))

cells.append(code(f'''# ---- 语料与词表（与 RNN 系列一致）----
TEXT = """{CORPUS}"""
vocab = sorted(set(TEXT))
vocab_size = len(vocab)
char2idx = {{c: i for i, c in enumerate(vocab)}}
idx2char = {{i: c for i, c in enumerate(vocab)}}
corpus = [char2idx[c] for c in TEXT]

block_size = 35
batch_size = 32
def get_batch(batch_size, block_size):
    X = torch.zeros(batch_size, block_size, dtype=torch.long)
    y = torch.zeros(batch_size, block_size, dtype=torch.long)
    n = len(corpus)
    for i in range(batch_size):
        start = np.random.randint(0, n - block_size - 1)
        X[i] = torch.tensor(corpus[start:start + block_size])
        y[i] = torch.tensor(corpus[start + 1:start + block_size + 1])
    return X, y

def causal_mask(T):
    return torch.tril(torch.ones(T, T)).unsqueeze(0).unsqueeze(0)   # (1,1,T,T) 下三角
'''))

cells.append(code("""# ---- GPT 风格：解码器（带因果掩码）+ 语言模型头 ----
class MiniGPT(nn.Module):
    def __init__(self, vocab_size, num_hiddens, num_heads, num_layers, ffn_hiddens, block_size, dropout):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, num_hiddens)
        self.pos_encoding = PositionalEncoding(num_hiddens, max_len=block_size)
        self.blks = nn.Sequential(*[EncoderBlock(num_hiddens, num_heads, ffn_hiddens, dropout)
                                    for _ in range(num_layers)])
        self.ln = nn.LayerNorm(num_hiddens)
        self.head = nn.Linear(num_hiddens, vocab_size)
        self.block_size = block_size

    def forward(self, X):
        B, T = X.shape
        mask = causal_mask(T).to(X.device)
        X = self.pos_encoding(self.embedding(X))
        for blk in self.blks:
            X = blk(X, mask)                     # 🔑 因果掩码：只看左边
        return self.head(self.ln(X))             # (B, T, vocab)

model = MiniGPT(vocab_size, 64, 4, 2, 128, block_size, 0.1)
X, y = get_batch(batch_size, block_size)
logits = model(X)
print("语言模型输出：", tuple(logits.shape), "（每个位置预测下一个字符的概率）")
print("参数量：", sum(p.numel() for p in model.parameters()))
"""))

cells.append(md("""## 3. 训练：Transformer 也能学「下一个字符」

和 RNN 系列同样的字符级任务，只是把 RNN 换成了 Transformer。
"""))

cells.append(code("""# ---- 训练 ----
trainer = torch.optim.Adam(model.parameters(), lr=1e-3)
num_epochs = 200
losses = []

for epoch in range(1, num_epochs + 1):
    X, y = get_batch(batch_size, block_size)
    logits = model(X)                              # (B, T, vocab)
    l = F.cross_entropy(logits.reshape(-1, vocab_size), y.reshape(-1))
    trainer.zero_grad(); l.backward(); trainer.step()
    losses.append(l.item())
    if epoch == 1 or epoch % 50 == 0:
        print(f"epoch {epoch:3d}: 损失 {l.item():.3f}  困惑度 {math.exp(l.item()):.2f}")

import matplotlib.pyplot as plt
plt.plot(losses)
plt.xlabel("epoch"); plt.ylabel("loss")
plt.title("Transformer 字符级语言模型 · 训练损失曲线")
plt.show()
"""))

cells.append(md("""## 4. 续写：GPT 风格逐字生成

给一个前缀，用因果 Transformer 逐字预测下一个字符（和 GPT 生成文本是同一个机制）。
"""))

cells.append(code("""# ---- 生成续写 ----
@torch.no_grad()
def generate(model, prefix, num_preds=60):
    model.eval()
    idx = torch.tensor([[char2idx[c] for c in prefix]])
    out = [c for c in prefix]
    for _ in range(num_preds):
        logits = model(idx[:, -model.block_size:])      # 只取最后 block_size 个字符
        probs = F.softmax(logits[:, -1, :], dim=-1)     # 最后一个位置的预测
        nxt = torch.multinomial(probs, 1).item()        # 按概率采样
        out.append(idx2char[nxt])
        idx = torch.cat([idx, torch.tensor([[nxt]])], dim=1)
    return ''.join(out)

print("续写结果：", generate(model, "the time", 80))
"""))

cells.append(md("""## 小结

| 零件 | 作用 |
| --- | --- |
| 多头注意力 | 全局信息融合（多角度） |
| Add & Norm | 残差 + 层归一化，训练稳定 |
| Position-wise FFN | 每位置独立非线性变换 |
| 位置编码 | 补顺序信息 |
| 因果掩码 | GPT 关键：预测时只看左边 |

> 🔑 **记忆**：Transformer 块 = **多头注意力 → 残差+LN → FFN → 残差+LN**，堆 N 层。**「只用编码器 = BERT，只用解码器(加因果掩码) = GPT」**。它没有循环结构，靠注意力一步看到全局，训练可并行——这正是它取代 RNN 成为大模型基座的原因。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\Transformer.ipynb", cells)
print("Transformer ✔")

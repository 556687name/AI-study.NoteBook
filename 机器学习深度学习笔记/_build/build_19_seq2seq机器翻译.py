# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# seq2seq 机器翻译 · 编码器-解码器（PyTorch）

> 📌 **出处**：李沐《动手学深度学习 V2》第 9 章「机器翻译 / 编码器-解码器 / seq2seq」
> 🎯 **目标**：用两个 GRU 搭一个**序列到序列**模型，把英语句子翻译成法语——理解「编码器把输入压成语义向量，解码器逐词生成输出」。

## 核心思想

- **编码器 Encoder**：逐词读入英语句子，最后输出一个隐藏状态（「语义向量」）；
- **解码器 Decoder**：以语义向量为起点，逐词生成法语——每生成一个词，作为下一步的输入；
- **训练时用 teacher forcing**：把**正确答案**喂给下一步（而非上一步的预测），让训练更快更稳；
- **推理时贪心解码**：每步选概率最大的词。
"""))

cells.append(code(ENV))

cells.append(code("""# ---- 小规模英→法 平行语料（自包含，无需下载）----
import torch.nn.functional as F
from torch import nn

pairs = [
    ("i am happy", "je suis content"),
    ("he is happy", "il est content"),
    ("she is tired", "elle est fatiguee"),
    ("we are students", "nous sommes etudiants"),
    ("they are teachers", "ils sont professeurs"),
    ("you are kind", "tu es gentil"),
    ("i like books", "j aime les livres"),
    ("he likes music", "il aime la musique"),
    ("she reads a book", "elle lit un livre"),
    ("we go home", "nous allons a la maison"),
    ("they speak french", "ils parlent francais"),
    ("i drink water", "je bois de l eau"),
    ("you eat bread", "tu manges du pain"),
    ("he sleeps early", "il dort tot"),
    ("she works hard", "elle travaille dur"),
]

# 加句子边界标记 <bos> <eos>
raw_src = ["<bos> " + s + " <eos>" for s, _ in pairs]
raw_tgt = ["<bos> " + t + " <eos>" for _, t in pairs]

def build_vocab(sentences):
    tokens = sorted(set(tok for s in sentences for tok in s.split()))
    return {tok: i for i, tok in enumerate(tokens)}, {i: tok for i, tok in enumerate(tokens)}

src_vocab, src_ivocab = build_vocab(raw_src)
tgt_vocab, tgt_ivocab = build_vocab(raw_tgt)
print("源词表大小：", len(src_vocab), " 目标词表大小：", len(tgt_vocab))
print("示例源句：", raw_src[0])
print("示例目标句：", raw_tgt[0])
"""))

cells.append(md("""## 1. 编码器 Encoder：把输入句压成一个隐藏状态

逐词读入（用 `nn.Embedding` + `nn.GRU`），取最后一个时间步的隐藏状态作为「语义向量」。
"""))

cells.append(code("""# ---- 编码器 ----
class Encoder(nn.Module):
    def __init__(self, vocab_size, embed_size, num_hiddens):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.gru = nn.GRU(embed_size, num_hiddens)

    def forward(self, X):
        # X: (num_steps, batch) 词索引
        emb = self.embedding(X)              # (num_steps, batch, embed)
        output, state = self.gru(emb)        # state: (1, batch, hidden)
        return output, state                 # 返回输出 + 最终隐藏状态（语义向量）

# 把句子变成词索引序列（按最长句补齐）
def to_tensor(sentences, vocab):
    seqs = [[vocab[tok] for tok in s.split()] for s in sentences]
    max_len = max(len(s) for s in seqs)
    seqs = [s + [vocab["<eos>"]] * (max_len - len(s)) for s in seqs]
    return torch.tensor(seqs).T              # (num_steps, batch)

embed_size, num_hiddens = 64, 64
encoder = Encoder(len(src_vocab), embed_size, num_hiddens)
X = to_tensor(raw_src[:3], src_vocab)
out, state = encoder(X)
print("编码器输出形状：", tuple(out.shape), " 语义向量形状：", tuple(state.shape))
"""))

cells.append(md("""## 2. 解码器 Decoder：从语义向量出发逐词生成

- **训练**：输入 `<bos>` 起步，每步用**正确答案**（teacher forcing）作为下一步输入；
- **推理**：每步用上一步预测的词（贪心）。
"""))

cells.append(code("""# ---- 解码器 ----
class Decoder(nn.Module):
    def __init__(self, vocab_size, embed_size, num_hiddens):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.gru = nn.GRU(embed_size + num_hiddens, num_hiddens)  # 输入=嵌入+上下文（简化：用上一输出）
        self.dense = nn.Linear(num_hiddens, vocab_size)

    def forward(self, X, state):
        # X: (num_steps, batch)；state 来自编码器
        emb = self.embedding(X)
        # 简化版：把隐藏状态广播后与嵌入拼接（d2l 完整版用注意力，这里先用拼接示意）
        ctx = state.repeat(emb.shape[0], 1, 1)
        output, state = self.gru(torch.cat([emb, ctx], dim=2), state)
        Y = self.dense(output)
        return Y.reshape(-1, Y.shape[-1]), state

decoder = Decoder(len(tgt_vocab), embed_size, num_hiddens)
print("解码器定义完成 ✔")
"""))

cells.append(md("""## 3. 训练（teacher forcing）

每个 epoch 遍历全部句对，用交叉熵损失端到端训练编码器+解码器。
"""))

cells.append(code("""# ---- 训练 ----
encoder = Encoder(len(src_vocab), embed_size, num_hiddens)
decoder = Decoder(len(tgt_vocab), embed_size, num_hiddens)
trainer = torch.optim.Adam(list(encoder.parameters()) + list(decoder.parameters()), lr=0.01)
loss_fn = nn.CrossEntropyLoss()

def train(epochs=300):
    losses = []
    for epoch in range(1, epochs + 1):
        total_l, n = 0.0, 0
        for s, t in zip(raw_src, raw_tgt):
            X = to_tensor([s], src_vocab)                 # 源句
            Y = to_tensor([t], tgt_vocab)                 # 目标句（完整）
            # teacher forcing：解码器输入是目标句（去掉最后 <eos>），标签是右移一位
            dec_input = Y[:-1, :]                          # 不含 <eos>
            dec_label = Y[1:, :].reshape(-1)               # 不含 <bos>
            _, state = encoder(X)
            out, _ = decoder(dec_input, state)
            l = loss_fn(out, dec_label)
            trainer.zero_grad(); l.backward(); trainer.step()
            total_l += l.item(); n += 1
        losses.append(total_l / n)
        if epoch == 1 or epoch % 50 == 0:
            print(f"epoch {epoch:3d}: 平均损失 {total_l / n:.3f}")
    return losses

losses = train(300)

import matplotlib.pyplot as plt
plt.plot(losses)
plt.xlabel("epoch"); plt.ylabel("loss")
plt.title("seq2seq · 训练损失曲线")
plt.show()
"""))

cells.append(md("""## 4. 推理：贪心解码翻译

从 `<bos>` 起步，每步取概率最大的词，直到 `<eos>` 或达到最大长度。
"""))

cells.append(code("""# ---- 贪心解码 ----
def translate(sentence):
    encoder.eval(); decoder.eval()
    tokens = ("<bos> " + sentence + " <eos>").split()
    X = to_tensor([" ".join(tokens)], src_vocab)
    _, state = encoder(X)
    dec_input = torch.tensor([[tgt_vocab["<bos>"]]])      # 从 <bos> 开始
    out_tokens = []
    for _ in range(15):
        out, state = decoder(dec_input, state)
        pred = out.argmax(dim=1).item()                    # 贪心：概率最大
        if tgt_ivocab[pred] == "<eos>":
            break
        out_tokens.append(tgt_ivocab[pred])
        dec_input = torch.tensor([[pred]])                 # 上一步预测作为下一步输入
    return ' '.join(out_tokens)

for s, t in pairs[:5]:
    print(f"输入: {s:20s} -> 预测: {translate(s):25s} (目标: {t})")
"""))

cells.append(md("""## 小结

| 概念 | 一句话直觉 |
| --- | --- |
| 编码器 | 输入句 → 一个语义向量 |
| 解码器 | 语义向量 → 逐词生成输出 |
| teacher forcing | 训练时喂正确答案，更快更稳 |
| 贪心解码 | 推理时每步取概率最大的词 |
| 束搜索 | 保留 top-k 候选，比贪心更好（见笔记） |

> 🔑 **记忆**：seq2seq = **编码器 + 解码器**，是机器翻译/摘要的基础框架。它的局限是「整句压成一个向量」——句子一长信息就挤爆，这正是**注意力机制**要解决的（下一步 Transformer）。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\seq2seq机器翻译.ipynb", cells)
print("seq2seq机器翻译 ✔")

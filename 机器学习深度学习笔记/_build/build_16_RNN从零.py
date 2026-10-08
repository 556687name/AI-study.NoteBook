# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

CORPUS = """The Time Traveller (for so it will be convenient to speak of him) was expounding a recondite matter to us. His grey eyes shone and twinkled, and his usually pale face was flushed and animated. The fire burned brightly, and the soft radiance of the incandescent lights in the lilies of silver caught the bubbles that flashed and passed in our glasses.

Our chairs, being his patents, embraced and caressed us rather than submitted to be sat upon, and there was that luxurious after-dinner atmosphere when thought roams gracefully free of the trammels of precision. And he put it to us in this way, marking the points with a lean forefinger, as we sat and lazily admired his earnestness over this new paradox, as we thought it, and his fecundity.

You must follow me carefully. I shall have to controvert one or two ideas that are almost universally accepted. The geometry, for instance, they taught you at school is founded on a misconception."""

cells = []

cells.append(md("""# RNN 循环神经网络 · 从零实现（PyTorch）

> 📌 **出处**：李沐《动手学深度学习 V2》第 8 章「循环神经网络」
> 🎯 **目标**：不调用 `nn.RNN`，**手写** RNN 的隐藏状态更新、循环、训练（含梯度裁剪），做一个**字符级语言模型**（给定前面几个字符，预测下一个字符）。

## 核心公式

$$\\mathbf{H}_t = \\tanh(\\mathbf{X}_t \\mathbf{W}_{xh} + \\mathbf{H}_{t-1} \\mathbf{W}_{hh} + \\mathbf{b}_h),\\qquad \\mathbf{O}_t = \\mathbf{H}_t \\mathbf{W}_{hq} + \\mathbf{b}_q$$

每读入一个字符，就更新一次隐藏状态 $\\mathbf{H}$（「记忆」），并用它预测下一个字符。同一个权重在所有时间步**复用**。
"""))

cells.append(code(ENV))

cells.append(code(f'''# ---- 语料：《时间机器》开头（公有领域，约 1100 字符）----
import math
import torch.nn.functional as F
from torch import nn

TEXT = """{CORPUS}"""

# 构建词表（字符级）：每个不重复字符一个编号
vocab = sorted(set(TEXT))
vocab_size = len(vocab)
char2idx = {{c: i for i, c in enumerate(vocab)}}
idx2char = {{i: c for i, c in enumerate(vocab)}}
corpus = [char2idx[c] for c in TEXT]

print("词表大小：", vocab_size)
print("词表：", ''.join(vocab))
'''))

cells.append(md("""## 1. 随机采样生成小批量

每次从语料里随机切一段连续序列，输入 `X` 是「当前字符」，标签 `y` 是「下一个字符」。
"""))

cells.append(code("""# ---- 随机采样：X 是当前字符序列，y 是右移一位的下一字符 ----
num_steps = 35        # 每个序列的长度
batch_size = 32

def get_batch(batch_size, num_steps):
    X = torch.zeros(batch_size, num_steps, dtype=torch.long)
    y = torch.zeros(batch_size, num_steps, dtype=torch.long)
    n = len(corpus)
    for i in range(batch_size):
        start = np.random.randint(0, n - num_steps - 1)
        X[i] = torch.tensor(corpus[start:start + num_steps])
        y[i] = torch.tensor(corpus[start + 1:start + num_steps + 1])
    return X, y

X, y = get_batch(batch_size, num_steps)
print("X 形状：", tuple(X.shape), " y 形状：", tuple(y.shape))
print("一条样本：", ''.join(idx2char[int(i)] for i in X[0][:20]))
"""))

cells.append(md("""## 2. 从零定义 RNN 模型

手写权重 $\\mathbf{W}_{xh}, \\mathbf{W}_{hh}, \\mathbf{W}_{hq}$ 和偏置；`rnn()` 用 for 循环遍历时间步更新隐藏状态。
"""))

cells.append(code("""# ---- 从零实现 RNN ----
class RNNModelScratch:
    def __init__(self, vocab_size, num_hiddens):
        self.vocab_size = vocab_size
        self.num_hiddens = num_hiddens
        self.W_xh = nn.Parameter(torch.randn(vocab_size, num_hiddens) * 0.01)
        self.W_hh = nn.Parameter(torch.randn(num_hiddens, num_hiddens) * 0.01)
        self.b_h  = nn.Parameter(torch.zeros(num_hiddens))
        self.W_hq = nn.Parameter(torch.randn(num_hiddens, vocab_size) * 0.01)
        self.b_q  = nn.Parameter(torch.zeros(vocab_size))
        self.params = [self.W_xh, self.W_hh, self.b_h, self.W_hq, self.b_q]

    def rnn(self, inputs, state):
        # inputs: 每个时间步一个 (batch, vocab) 的 one-hot
        H, = state
        outputs = []
        for X in inputs:
            H = torch.tanh(X @ self.W_xh + H @ self.W_hh + self.b_h)   # 隐藏状态更新
            outputs.append(H @ self.W_hq + self.b_q)                   # 输出（预测下一个字符）
        return torch.stack(outputs), (H,)

    def begin_state(self, batch_size):
        return (torch.zeros(batch_size, self.num_hiddens),)

def inputs_from(X):
    # X: (batch, num_steps) -> 列表[每步 (batch, vocab) one-hot]
    oh = F.one_hot(X.T, vocab_size).float()
    return [oh[t] for t in range(oh.shape[0])]

num_hiddens = 256
model = RNNModelScratch(vocab_size, num_hiddens)
state = model.begin_state(batch_size)
out, state = model.rnn(inputs_from(X), state)
print("输出形状：", tuple(out.shape), "（num_steps, batch, vocab）")
"""))

cells.append(md("""## 3. 训练（含梯度裁剪）

RNN 梯度会沿时间轴连乘，容易**梯度爆炸**，所以用**梯度裁剪**：把所有参数梯度的范数限制在阈值内。
"""))

cells.append(code("""# ---- 训练：梯度裁剪 + SGD ----
def grad_clipping(params, theta):
    norm = torch.sqrt(sum(torch.sum((p.grad ** 2)) for p in params if p.grad is not None))
    if norm > theta:
        for p in params:
            if p.grad is not None:
                p.grad[:] *= theta / norm

trainer = torch.optim.SGD(model.params, lr=1.0)
num_epochs = 300
losses = []

for epoch in range(1, num_epochs + 1):
    state = model.begin_state(batch_size)
    X, y = get_batch(batch_size, num_steps)
    outputs, state = model.rnn(inputs_from(X), state)                 # 前向
    l = F.cross_entropy(outputs.reshape(-1, vocab_size), y.T.reshape(-1))
    trainer.zero_grad()
    l.backward()
    grad_clipping(model.params, 1.0)                                  # 梯度裁剪
    trainer.step()
    losses.append(l.item())
    if epoch == 1 or epoch % 50 == 0:
        print(f"epoch {epoch:3d}: 损失 {l.item():.3f}  困惑度 {math.exp(l.item()):.2f}")

# 损失曲线
import matplotlib.pyplot as plt
plt.plot(losses)
plt.xlabel("epoch"); plt.ylabel("loss")
plt.title("RNN 从零实现 · 训练损失曲线")
plt.show()
"""))

cells.append(md("""## 4. 预测：给定前缀，续写文本

训练前模型只会「胡言乱语」（困惑度接近词表大小），训练后能学到基本的字符搭配规律。
"""))

cells.append(code("""# ---- 预测：给定前缀，自动续写 ----
def predict(model, prefix, num_preds=50):
    state = model.begin_state(1)
    outputs = [char2idx[prefix[0]]]
    get_input = lambda: F.one_hot(torch.tensor([[outputs[-1]]]), vocab_size).float().reshape(1, -1)
    for i in range(len(prefix) + num_preds - 1):
        Y, state = model.rnn([get_input()], state)
        if i < len(prefix) - 1:
            outputs.append(char2idx[prefix[i + 1]])
        else:
            outputs.append(int(Y[0].argmax(dim=1)))
    return ''.join(idx2char[i] for i in outputs)

print("续写结果：", predict(model, "the tim", num_preds=80))
"""))

cells.append(md("""## 小结

| 概念 | 一句话直觉 |
| --- | --- |
| 隐藏状态 H | 「记忆」，随每个时间步更新 |
| 参数共享 | 同一权重在所有时间步复用 |
| one-hot 输入 | 字符级模型用 one-hot 表示当前字符 |
| 梯度裁剪 | 防止 RNN 沿时间轴梯度爆炸 |

> 🔑 **记忆**：RNN 从零实现的核心就三样——**隐藏状态更新**（`tanh(X@W_xh + H@W_hh + b)`）、**时间步 for 循环**、**梯度裁剪**。困惑度从接近词表大小降到个位数，说明模型真的学会了「下一个字符」的规律。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\RNN-从零实现.ipynb", cells)
print("RNN-从零实现 ✔")

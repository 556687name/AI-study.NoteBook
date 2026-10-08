# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

CORPUS = """The Time Traveller (for so it will be convenient to speak of him) was expounding a recondite matter to us. His grey eyes shone and twinkled, and his usually pale face was flushed and animated. The fire burned brightly, and the soft radiance of the incandescent lights in the lilies of silver caught the bubbles that flashed and passed in our glasses.

Our chairs, being his patents, embraced and caressed us rather than submitted to be sat upon, and there was that luxurious after-dinner atmosphere when thought roams gracefully free of the trammels of precision. And he put it to us in this way, marking the points with a lean forefinger, as we sat and lazily admired his earnestness over this new paradox, as we thought it, and his fecundity.

You must follow me carefully. I shall have to controvert one or two ideas that are almost universally accepted. The geometry, for instance, they taught you at school is founded on a misconception."""

cells = []

cells.append(md("""# GRU 与 LSTM · 用「门」解决梯度消失（PyTorch）

> 📌 **出处**：李沐《动手学深度学习 V2》第 9 章「门控循环单元 GRU / 长短期记忆 LSTM」
> 🎯 **目标**：从零实现 **GRU（2 个门）** 和 **LSTM（3 个门 + 细胞状态）**，理解它们如何用「门」选择性记住/遗忘信息，从而缓解 RNN 的长依赖问题。

## 为什么普通 RNN 不够

RNN 每步都**整体覆盖**隐藏状态，序列一长早期信息就被冲淡（梯度消失）。GRU/LSTM 引入**门**，让网络自己决定「记住什么、忘记什么」。

## GRU：更新门 + 重置门

$$\\mathbf{R}_t = \\sigma(\\mathbf{X}_t \\mathbf{W}_{xr} + \\mathbf{H}_{t-1} \\mathbf{W}_{hr} + b_r) \\quad\\text{（重置门）}$$

$$\\mathbf{Z}_t = \\sigma(\\mathbf{X}_t \\mathbf{W}_{xz} + \\mathbf{H}_{t-1} \\mathbf{W}_{hz} + b_z) \\quad\\text{（更新门）}$$

$$\\mathbf{H}_t = \\mathbf{Z}_t \\odot \\mathbf{H}_{t-1} + (1 - \\mathbf{Z}_t) \\odot \\tanh(\\mathbf{X}_t \\mathbf{W}_{xh} + (\\mathbf{R}_t \\odot \\mathbf{H}_{t-1}) \\mathbf{W}_{hh} + b_h)$$

## LSTM：遗忘门 + 输入门 + 输出门 + 细胞状态 C
"""))

cells.append(code(ENV))

cells.append(code(f'''# ---- 语料与词表（与前两节一致）----
import math
import torch.nn.functional as F
from torch import nn

TEXT = """{CORPUS}"""

vocab = sorted(set(TEXT))
vocab_size = len(vocab)
char2idx = {{c: i for i, c in enumerate(vocab)}}
idx2char = {{i: c for i, c in enumerate(vocab)}}
corpus = [char2idx[c] for c in TEXT]

num_steps = 35
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
'''))

cells.append(md("""## 1. 从零实现 GRU（2 个门）

相比 RNN 多出**重置门 R** 和**更新门 Z**：更新门接近 1 时保留旧记忆，接近 0 时整体刷新。
"""))

cells.append(code("""# ---- 从零实现 GRU ----
def gru_from_scratch(inputs, state, params):
    W_xz, W_hz, b_z, W_xr, W_hr, b_r, W_xh, W_hh, b_h, W_hq, b_q = params
    H, = state
    outputs = []
    for X in inputs:
        Z = torch.sigmoid(X @ W_xz + H @ W_hz + b_z)                          # 更新门
        R = torch.sigmoid(X @ W_xr + H @ W_hr + b_r)                          # 重置门
        H_tilde = torch.tanh(X @ W_xh + (R * H) @ W_hh + b_h)                 # 候选记忆
        H = Z * H + (1 - Z) * H_tilde                                         # 选择性更新
        outputs.append(H @ W_hq + b_q)
    return torch.stack(outputs), (H,)

# 初始化 GRU 参数
def init_gru_params(vocab_size, num_hiddens):
    def normal(shape):
        return nn.Parameter(torch.randn(*shape) * 0.01)
    def three():
        return (normal((vocab_size, num_hiddens)), normal((num_hiddens, num_hiddens)),
                nn.Parameter(torch.zeros(num_hiddens)))
    W_xz, W_hz, b_z = three()
    W_xr, W_hr, b_r = three()
    W_xh, W_hh, b_h = three()
    W_hq = normal((num_hiddens, vocab_size))
    b_q = nn.Parameter(torch.zeros(vocab_size))
    return [W_xz, W_hz, b_z, W_xr, W_hr, b_r, W_xh, W_hh, b_h, W_hq, b_q]

num_hiddens = 256
gru_params = init_gru_params(vocab_size, num_hiddens)
print("GRU 参数个数：", len(gru_params))
"""))

cells.append(md("""## 2. 从零实现 LSTM（3 个门 + 细胞状态）

LSTM 多一个独立的**细胞状态 C**，像「传送带」一样几乎无损地传递长距离信息。
"""))

cells.append(code("""# ---- 从零实现 LSTM ----
def lstm_from_scratch(inputs, state, params):
    W_xi, W_hi, b_i, W_xf, W_hf, b_f, W_xo, W_ho, b_o, W_xc, W_hc, b_c, W_hq, b_q = params
    H, C = state                          # H 隐藏状态，C 细胞状态
    outputs = []
    for X in inputs:
        I = torch.sigmoid(X @ W_xi + H @ W_hi + b_i)     # 输入门
        F = torch.sigmoid(X @ W_xf + H @ W_hf + b_f)     # 遗忘门
        O = torch.sigmoid(X @ W_xo + H @ W_ho + b_o)     # 输出门
        C_tilde = torch.tanh(X @ W_xc + H @ W_hc + b_c)  # 候选细胞状态
        C = F * C + I * C_tilde                          # 细胞状态：选择性遗忘+写入
        H = O * torch.tanh(C)                            # 隐藏状态
        outputs.append(H @ W_hq + b_q)
    return torch.stack(outputs), (H, C)

def init_lstm_params(vocab_size, num_hiddens):
    def normal(shape):
        return nn.Parameter(torch.randn(*shape) * 0.01)
    def four():
        return (normal((vocab_size, num_hiddens)), normal((num_hiddens, num_hiddens)),
                nn.Parameter(torch.zeros(num_hiddens)))
    W_xi, W_hi, b_i = four(); W_xf, W_hf, b_f = four()
    W_xo, W_ho, b_o = four(); W_xc, W_hc, b_c = four()
    W_hq = normal((num_hiddens, vocab_size))
    b_q = nn.Parameter(torch.zeros(vocab_size))
    return [W_xi, W_hi, b_i, W_xf, W_hf, b_f, W_xo, W_ho, b_o, W_xc, W_hc, b_c, W_hq, b_q]

lstm_params = init_lstm_params(vocab_size, num_hiddens)
print("LSTM 参数个数：", len(lstm_params))
"""))

cells.append(md("""## 3. 训练 GRU 与 LSTM，对比效果

用同样的超参分别训练，绘制两条损失曲线对比。
"""))

cells.append(code("""# ---- 训练循环（通用）：给定模型函数 + 参数 ----
def grad_clipping(params, theta):
    norm = torch.sqrt(sum(torch.sum((p.grad ** 2)) for p in params if p.grad is not None))
    if norm > theta:
        for p in params:
            if p.grad is not None:
                p.grad[:] *= theta / norm

def train(model_fn, params, begin_state, num_epochs=300, label=""):
    trainer = torch.optim.SGD(params, lr=1.0)
    losses = []
    for epoch in range(1, num_epochs + 1):
        state = begin_state(batch_size)
        X, y = get_batch(batch_size, num_steps)
        inputs = F.one_hot(X.T, vocab_size).float()
        inputs = [inputs[t] for t in range(inputs.shape[0])]
        outputs, state = model_fn(inputs, state, params)
        l = F.cross_entropy(outputs.reshape(-1, vocab_size), y.T.reshape(-1))
        trainer.zero_grad(); l.backward()
        grad_clipping(params, 1.0)
        trainer.step()
        losses.append(l.item())
    print(f"{label}: 最终损失 {losses[-1]:.3f}  困惑度 {math.exp(losses[-1]):.2f}")
    return losses

gru_state = lambda b: (torch.zeros(b, num_hiddens),)
lstm_state = lambda b: (torch.zeros(b, num_hiddens), torch.zeros(b, num_hiddens))

loss_gru = train(gru_from_scratch, gru_params, gru_state, label="GRU ")
loss_lstm = train(lstm_from_scratch, lstm_params, lstm_state, label="LSTM")

import matplotlib.pyplot as plt
plt.plot(loss_gru, label="GRU"); plt.plot(loss_lstm, label="LSTM")
plt.xlabel("epoch"); plt.ylabel("loss"); plt.legend()
plt.title("GRU vs LSTM · 训练损失曲线")
plt.show()
"""))

cells.append(md("""## 4. PyTorch 简洁实现：nn.GRU / nn.LSTM

实际工程中直接用内置实现，只需改 `nn.RNN` → `nn.GRU` / `nn.LSTM` 即可（LSTM 返回 `(输出, (H, C))` 两个状态）。
"""))

cells.append(code("""# ---- 简洁实现对比：nn.GRU / nn.LSTM ----
class GRUModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.gru = nn.GRU(vocab_size, num_hiddens)
        self.linear = nn.Linear(num_hiddens, vocab_size)
    def forward(self, X, state):
        Y, state = self.gru(X, state)
        return self.linear(Y.reshape(-1, Y.shape[-1])), state

class LSTMModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(vocab_size, num_hiddens)
        self.linear = nn.Linear(num_hiddens, vocab_size)
    def forward(self, X, state):
        Y, state = self.lstm(X, state)
        return self.linear(Y.reshape(-1, Y.shape[-1])), state

for name, m in [("nn.GRU ", GRUModel()), ("nn.LSTM", LSTMModel())]:
    X, y = get_batch(2, num_steps)
    inputs = F.one_hot(X.T, vocab_size).float()
    out, _ = m(inputs, None)
    print(name, "输出形状：", tuple(out.shape))
"""))

cells.append(md("""## 小结

| | RNN | GRU | LSTM |
| --- | --- | --- | --- |
| 门数量 | 0 | 2（重置+更新） | 3（遗忘+输入+输出） |
| 细胞状态 | 无 | 无 | 有（长距离传送带） |
| 参数 | 最少 | 中等 | 最多 |
| 长依赖 | 差 | 好 | 最好 |

> 🔑 **记忆**：GRU = **2 门**结构简单；LSTM = **3 门 + 细胞状态 C**，表达力最强。二者核心都是「**用门做选择性遗忘**」——网络学会在长序列里保留关键信息，是 RNN 的实际标配。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\GRU与LSTM.ipynb", cells)
print("GRU与LSTM ✔")

# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

CORPUS = """The Time Traveller (for so it will be convenient to speak of him) was expounding a recondite matter to us. His grey eyes shone and twinkled, and his usually pale face was flushed and animated. The fire burned brightly, and the soft radiance of the incandescent lights in the lilies of silver caught the bubbles that flashed and passed in our glasses.

Our chairs, being his patents, embraced and caressed us rather than submitted to be sat upon, and there was that luxurious after-dinner atmosphere when thought roams gracefully free of the trammels of precision. And he put it to us in this way, marking the points with a lean forefinger, as we sat and lazily admired his earnestness over this new paradox, as we thought it, and his fecundity.

You must follow me carefully. I shall have to controvert one or two ideas that are almost universally accepted. The geometry, for instance, they taught you at school is founded on a misconception."""

cells = []

cells.append(md("""# RNN 循环神经网络 · 简洁实现（PyTorch）

> 📌 **出处**：李沐《动手学深度学习 V2》第 8 章「循环神经网络」
> 🎯 **目标**：用 PyTorch 内置的 `nn.RNN` / `nn.RNNCell` 一行搞定隐藏状态更新，对比上一节 `RNN-从零实现.ipynb` 的手写实现。

## nn.RNN 做了什么

`nn.RNN(input_size, hidden_size)` 内部自动完成：

$$\\mathbf{H}_t = \\tanh(\\mathbf{X}_t \\mathbf{W}_{xh} + \\mathbf{H}_{t-1} \\mathbf{W}_{hh} + \\mathbf{b}_h)$$

不用手写 for 循环，直接传入整个序列即可；它还支持**多层堆叠**（`num_layers`）。
"""))

cells.append(code(ENV))

cells.append(code(f'''# ---- 语料与词表（与「从零实现」完全一致）----
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

cells.append(md("""## 1. 用 nn.RNN 定义模型

注意：`nn.RNN` 的输入形状是 `(num_steps, batch, input_size)`，one-hot 编码后直接喂进去。
"""))

cells.append(code("""# ---- 简洁实现：nn.RNN ----
class RNNModel(nn.Module):
    def __init__(self, vocab_size, num_hiddens):
        super().__init__()
        self.rnn = nn.RNN(vocab_size, num_hiddens)   # 输入是 one-hot（维度=词表大小）
        self.linear = nn.Linear(num_hiddens, vocab_size)

    def forward(self, inputs, state):
        # inputs: (num_steps, batch, vocab)
        Y, state = self.rnn(inputs, state)           # Y: (num_steps, batch, hidden)
        output = self.linear(Y.reshape(-1, Y.shape[-1]))  # 每个时间步过一个线性层
        return output, state

    def begin_state(self, batch_size):
        return torch.zeros(1, batch_size, self.rnn.hidden_size)  # (num_layers, batch, hidden)

num_hiddens = 256
model = RNNModel(vocab_size, num_hiddens)

# 验证前向
X, y = get_batch(batch_size, num_steps)
inputs = F.one_hot(X.T, vocab_size).float()          # (num_steps, batch, vocab)
state = model.begin_state(batch_size)
out, state = model(inputs, state)
print("输出形状：", tuple(out.shape), "（num_steps*batch, vocab）")
"""))

cells.append(md("""## 2. 训练（结构与从零实现相同，只是不需要手写梯度裁剪的 for 循环）

`nn.utils.clip_grad_norm_` 是 PyTorch 内置的梯度裁剪。
"""))

cells.append(code("""# ---- 训练 ----
trainer = torch.optim.SGD(model.parameters(), lr=1.0)
num_epochs = 300
losses = []

for epoch in range(1, num_epochs + 1):
    state = model.begin_state(batch_size)
    X, y = get_batch(batch_size, num_steps)
    inputs = F.one_hot(X.T, vocab_size).float()
    outputs, state = model(inputs, state)
    l = F.cross_entropy(outputs, y.T.reshape(-1))
    trainer.zero_grad()
    l.backward()
    nn.utils.clip_grad_norm_(model.parameters(), 1.0)   # 内置梯度裁剪
    trainer.step()
    losses.append(l.item())
    if epoch == 1 or epoch % 50 == 0:
        print(f"epoch {epoch:3d}: 损失 {l.item():.3f}  困惑度 {math.exp(l.item()):.2f}")

import matplotlib.pyplot as plt
plt.plot(losses)
plt.xlabel("epoch"); plt.ylabel("loss")
plt.title("RNN 简洁实现 · 训练损失曲线")
plt.show()
"""))

cells.append(md("""## 3. 预测续写

用 `nn.RNN` 逐字符预测，注意简洁实现里隐藏状态用 `nn.RNN` 维护，`begin_state` 传 batch=1。
"""))

cells.append(code("""# ---- 预测续写 ----
def predict(model, prefix, num_preds=50):
    state = model.begin_state(1)
    outputs = [char2idx[prefix[0]]]
    get_input = lambda: F.one_hot(torch.tensor([[outputs[-1]]]), vocab_size).float().reshape(1, 1, -1)
    for i in range(len(prefix) + num_preds - 1):
        Y, state = model(get_input(), state)
        if i < len(prefix) - 1:
            outputs.append(char2idx[prefix[i + 1]])
        else:
            outputs.append(int(Y.argmax(dim=1).item()))   # forward 返回 2D：(1, vocab)
    return ''.join(idx2char[i] for i in outputs)

print("续写结果：", predict(model, "the tim", num_preds=80))
"""))

cells.append(md("""## 小结

| 从零实现 | 简洁实现 `nn.RNN` |
| --- | --- |
| 手写 `W_xh, W_hh, W_hq` + for 循环 | 一行定义，自动循环 |
| 手写 `grad_clipping` | `nn.utils.clip_grad_norm_` |
| 隐藏状态手动管理 | `begin_state` + 返回值自动管理 |

> 🔑 **记忆**：`nn.RNN` 的输入是 `(num_steps, batch, input_size)`，内部自动做隐藏状态更新。学会从零实现后，用 `nn.RNN` 一行替换，是理解底层 → 高效实践的必经之路。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\RNN-简洁实现.ipynb", cells)
print("RNN-简洁实现 ✔")

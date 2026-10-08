# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# 优化算法实战 · 从零实现六大优化器并对比（PyTorch/numpy）

> 📌 **出处**：李沐《动手学深度学习 V2》第 11 章「优化算法」
> 🎯 **目标**：手写 **SGD / Momentum / AdaGrad / RMSProp / Adam / Adadelta** 六个优化器，在「香蕉函数」上对比收敛轨迹，再用 Adam 训练一个真实的 MLP。

## 更新公式速查

| 优化器 | 核心更新（$\\mathbf{g}$ 为梯度） |
| --- | --- |
| SGD | $\\mathbf{x} \\leftarrow \\mathbf{x} - \\eta\\mathbf{g}$ |
| Momentum | $\\mathbf{v} \\leftarrow \\gamma\\mathbf{v} + \\mathbf{g},\\; \\mathbf{x} \\leftarrow \\mathbf{x} - \\eta\\mathbf{v}$ |
| AdaGrad | $\\mathbf{s} \\leftarrow \\mathbf{s} + \\mathbf{g}^2,\\; \\mathbf{x} \\leftarrow \\mathbf{x} - \\eta\\mathbf{g}/(\\sqrt{\\mathbf{s}}+\\epsilon)$ |
| RMSProp | $\\mathbf{s} \\leftarrow \\rho\\mathbf{s} + (1-\\rho)\\mathbf{g}^2$（指数滑动平均） |
| Adam | Momentum + RMSProp，加**偏差修正** |
| Adadelta | 用两个 RMS 之比，**无需设置学习率** |
"""))

cells.append(code(ENV))

cells.append(code("""# ---- 六大优化器（numpy 从零实现）----
import numpy as np

def sgd(x, g, state, lr):
    return x - lr * g, state

def momentum(x, g, state, lr, gamma=0.9):
    v = state.get('v', np.zeros_like(x)) * gamma + g
    return x - lr * v, {'v': v}

def adagrad(x, g, state, lr, eps=1e-6):
    s = state.get('s', np.zeros_like(x)) + g**2
    return x - lr * g / (np.sqrt(s) + eps), {'s': s}

def rmsprop(x, g, state, lr, rho=0.9, eps=1e-6):
    s = state.get('s', np.zeros_like(x)) * rho + (1 - rho) * g**2
    return x - lr * g / (np.sqrt(s) + eps), {'s': s}

def adam(x, g, state, lr, beta1=0.9, beta2=0.999, eps=1e-8):
    t = state.get('t', 0) + 1
    v = state.get('v', np.zeros_like(x)) * beta1 + (1 - beta1) * g
    s = state.get('s', np.zeros_like(x)) * beta2 + (1 - beta2) * g**2
    vh = v / (1 - beta1 ** t)   # 偏差修正
    sh = s / (1 - beta2 ** t)
    return x - lr * vh / (np.sqrt(sh) + eps), {'v': v, 's': s, 't': t}

def adadelta(x, g, state, lr, rho=0.9, eps=1e-6):
    s = state.get('s', np.zeros_like(x)) * rho + (1 - rho) * g**2
    u = state.get('u', np.zeros_like(x))
    delta = -np.sqrt(u + eps) / np.sqrt(s + eps) * g    # 无需 lr
    u = rho * u + (1 - rho) * delta**2
    return x + delta, {'s': s, 'u': u}

def optimize(grad, init, optimizer, lr, steps=200):
    x = np.array(init, dtype=float)
    trace = [x.copy()]
    state = {}
    for _ in range(steps):
        x, state = optimizer(x, grad(x), state, lr)
        trace.append(x.copy())
    return np.array(trace)
"""))

cells.append(md("""## 1. 在「香蕉函数」（Rosenbrock）上对比

$$f(x, y) = (1 - x)^2 + 100\\, (y - x^2)^2$$

它有一条**又窄又弯的谷**，普通 SGD 很难走到底——是最经典的优化器试金石。
"""))

cells.append(code("""# ---- Rosenbrock 香蕉函数 ----
def rosen(x):
    return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

def rosen_grad(x):
    dx = -2 * (1 - x[0]) - 400 * x[0] * (x[1] - x[0]**2)
    dy = 200 * (x[1] - x[0]**2)
    return np.array([dx, dy])

import matplotlib.pyplot as plt

# 画等高线
xs = np.linspace(-1.5, 1.8, 200); ys = np.linspace(-0.5, 3.0, 200)
Xg, Yg = np.meshgrid(xs, ys)
Z = (1 - Xg)**2 + 100 * (Yg - Xg**2)**2
plt.figure(figsize=(7, 6))
plt.contour(Xg, Yg, np.log10(Z + 1), levels=20, cmap='viridis', alpha=0.6)

# 各优化器从同一点出发
init = [-1.2, 1.0]
configs = [
    ("SGD",        sgd,       0.001),
    ("Momentum",   momentum,  0.001),
    ("AdaGrad",    adagrad,   0.5),
    ("RMSProp",    rmsprop,   0.01),
    ("Adam",       adam,      0.1),
    ("Adadelta",   adadelta,  0.0),   # 无需学习率
]
for name, opt, lr in configs:
    trace = optimize(rosen_grad, init, opt, lr, steps=300)
    plt.plot(trace[:, 0], trace[:, 1], '-o', ms=2, label=f"{name}  (终点损失 {rosen(trace[-1]):.1e})")

plt.plot(1, 1, '*', ms=14, color=红, label="全局最优 (1,1)")
plt.scatter(*init, color='k', s=40, zorder=5, label="起点")
plt.legend(fontsize=9); plt.xlabel("x"); plt.ylabel("y")
plt.title("Rosenbrock 香蕉函数 · 六大优化器收敛轨迹对比")
plt.show()
"""))

cells.append(md("""## 2. 分析：为什么结果差这么多

- **SGD** 卡在窄谷里来回震荡，几乎不动；
- **Momentum** 靠惯性冲过震荡，但仍慢；
- **AdaGrad** 对陡方向学习率降得太快，后期走不动；
- **RMSProp / Adam / Adadelta** 用滑动平均自适应学习率，能顺着窄谷快速逼近最优，**Adam 通常最快最稳**。

> 💡 这也是为什么**实践里默认用 Adam**（笔记 6.4 的结论）。
"""))

cells.append(md("""## 3. 实战：Adam 训练 MLP（Fashion-MNIST）

对比 **SGD** 和 **Adam** 在真实神经网络上的收敛速度。
"""))

cells.append(code("""# ---- MLP 训练：SGD vs Adam ----
from torch import nn
import torch.nn.functional as F

def mlp():
    return nn.Sequential(nn.Flatten(), nn.Linear(784, 256), nn.ReLU(),
                         nn.Linear(256, 128), nn.ReLU(), nn.Linear(128, 10))

def load(batch_size):
    from torchvision import datasets, transforms
    from torch.utils import data
    trans = transforms.ToTensor()
    tr = datasets.FashionMNIST(root='../data', train=True,  transform=trans, download=True)
    te = datasets.FashionMNIST(root='../data', train=False, transform=trans, download=True)
    return data.DataLoader(tr, batch_size, shuffle=True), data.DataLoader(te, batch_size, shuffle=False)

batch_size = 256
train_iter, test_iter = load(batch_size)
loss_fn = nn.CrossEntropyLoss()

def train_model(opt_name, lr, epochs=10):
    net = mlp()
    opt = torch.optim.SGD(net.parameters(), lr=lr) if opt_name == "SGD" else torch.optim.Adam(net.parameters(), lr=lr)
    accs = []
    for epoch in range(epochs):
        net.train()
        for X, y in train_iter:
            l = loss_fn(net(X), y); opt.zero_grad(); l.backward(); opt.step()
        net.eval()
        correct = sum((net(X).argmax(1) == y).sum().item() for X, y in test_iter)
        accs.append(correct / len(test_iter.dataset))
    return accs

torch.manual_seed(0)
acc_sgd = train_model("SGD", 0.1)
torch.manual_seed(0)
acc_adam = train_model("Adam", 1e-3)

plt.plot(acc_sgd, '-o', label="SGD (lr=0.1)")
plt.plot(acc_adam, '-o', label="Adam (lr=1e-3)")
plt.xlabel("epoch"); plt.ylabel("测试准确率"); plt.legend()
plt.title("Fashion-MNIST · SGD vs Adam 收敛对比")
plt.show()
print(f"10 epoch 后：SGD {acc_sgd[-1]:.4f}  vs  Adam {acc_adam[-1]:.4f}")
"""))

cells.append(md("""## 小结

| 优化器 | 特点 |
| --- | --- |
| SGD | 最基础，窄谷震荡慢 |
| Momentum | 加惯性，冲过平坦/震荡区 |
| AdaGrad | 梯度平方累加（只增不减，后期太慢） |
| RMSProp | 近期梯度平方的滑动平均 |
| Adam | Momentum + RMSProp + 偏差修正，**默认首选** |
| Adadelta | 无需设置学习率 |

> 🔑 **记忆**：**Adam = 动量 + 自适应学习率 + 偏差修正**，是深度学习默认优化器；SGD 需要仔细调学习率（常配合学习率调度）。选 Adam 起步，几乎不会错。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\优化算法实战.ipynb", cells)
print("优化算法实战 ✔")

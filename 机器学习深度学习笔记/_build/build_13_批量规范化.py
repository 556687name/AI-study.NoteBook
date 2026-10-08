# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# 批量规范化 BatchNorm · 让每一层输入稳定（PyTorch）

> 📌 **出处**：李沐《动手学深度学习 V2》第 7 章「批量规范化」
> 🎯 **目标**：给 LeNet 加上 **BatchNorm**，理解它是怎么「把小批量的激活归一化到均值 0、方差 1，再用可学习参数缩放平移」的。

## 为什么需要 BatchNorm

训练深层网络时，每层输入的分布会随训练不断漂移（**内部协变量偏移**），导致要小心翼翼地调学习率。BatchNorm 对每个小批量、每个通道做归一化：

$$\\hat x = \\frac{x - \\mu_\\text{batch}}{\\sqrt{\\sigma^2_\\text{batch} + \\epsilon}},\\qquad y = \\gamma \\hat x + \\beta$$

好处：**训练更稳、可用更大学习率、对初始化不敏感、自带一点正则化**。

> ⚠️ **训练 vs 推理**：训练用本批统计量，推理用全局移动平均（`nn.BatchNorm2d` 自动切换）。BatchNorm 加在**卷积/全连接层之后、激活函数之前**。
"""))

cells.append(code(ENV))

cells.append(md("""## 1. 给 LeNet 加 BatchNorm

在每个卷积层后插 `nn.BatchNorm2d`，每个全连接层后插 `nn.BatchNorm1d`（都在激活函数**之前**）。
"""))

cells.append(code("""# ---- 带 BatchNorm 的 LeNet ----
from torch import nn

net = nn.Sequential(
    nn.Conv2d(1, 6, kernel_size=5), nn.BatchNorm2d(6), nn.Sigmoid(),
    nn.AvgPool2d(kernel_size=2, stride=2),
    nn.Conv2d(6, 16, kernel_size=5), nn.BatchNorm2d(16), nn.Sigmoid(),
    nn.AvgPool2d(kernel_size=2, stride=2),
    nn.Flatten(),
    nn.Linear(256, 120), nn.BatchNorm1d(120), nn.Sigmoid(),
    nn.Linear(120, 84),  nn.BatchNorm1d(84),  nn.Sigmoid(),
    nn.Linear(84, 10),
)

X = torch.rand(2, 1, 28, 28)   # batch=2：BatchNorm 在训练模式需要 batch>1 才能算批统计量
print("输出形状：", tuple(net(X).shape), "（28→24→12→8→4，展平 16×4×4=256）")
"""))

cells.append(md("""## 2. 完整训练（28×28 小图，CPU 可跑）

LeNet 是 28×28 的小模型，CPU 上也能完整训练。BatchNorm 让训练更稳定，用 `lr=0.1` 就能平滑收敛。
"""))

cells.append(code("""# ---- 加载 Fashion-MNIST 并训练 ----
from torchvision import datasets, transforms
from torch.utils import data

def load_data(batch_size):
    trans = transforms.ToTensor()
    tr = datasets.FashionMNIST(root='../data', train=True,  transform=trans, download=True)
    te = datasets.FashionMNIST(root='../data', train=False, transform=trans, download=True)
    return data.DataLoader(tr, batch_size, shuffle=True), data.DataLoader(te, batch_size, shuffle=False)

batch_size = 256
train_iter, test_iter = load_data(batch_size)

loss = nn.CrossEntropyLoss()
trainer = torch.optim.SGD(net.parameters(), lr=0.1)

def accuracy(it):
    net.eval()
    with torch.no_grad():
        h, t = 0.0, 0
        for X, y in it:
            h += float((net(X).argmax(axis=1) == y).sum()); t += y.numel()
    return h / t

num_epochs = 20
for epoch in range(num_epochs):
    net.train()
    for X, y in train_iter:
        l = loss(net(X), y); trainer.zero_grad(); l.backward(); trainer.step()
    print(f"epoch {epoch+1:2d}: 训练准确率 {accuracy(train_iter):.4f}")

print(f"\\n带 BatchNorm 的 LeNet 测试集准确率：{accuracy(test_iter):.4f}")
"""))

cells.append(md("""## 小结

| 概念 | 一句话直觉 |
| --- | --- |
| 内部协变量偏移 | 每层输入分布随训练漂移 |
| BatchNorm | 小批量归一化 + 可学习缩放平移 |
| γ / β | 归一化后拉回合适尺度的两个可学习参数 |
| 训练 vs 推理 | 训练用本批统计，推理用全局移动平均 |

> 🔑 **记忆**：BatchNorm 把每层输入拉回标准分布（均值 0、方差 1），再学 γ、β 恢复表达力，是训练深层网络（ResNet 等）的**标配**。和上一节 `LeNet.ipynb`（无 BatchNorm）对比，可看到 BN 让训练更稳、收敛更快。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\批量规范化.ipynb", cells)

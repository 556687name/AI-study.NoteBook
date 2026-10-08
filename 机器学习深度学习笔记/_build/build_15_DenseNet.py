# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# DenseNet · 每一层都连到「前面所有层」（PyTorch）

> 📌 **出处**：李沐《动手学深度学习 V2》第 7 章「DenseNet」
> 🎯 **目标**：搭出 DenseNet，理解**密集连接**（每一层的输出拼接到前面所有层的输入）如何做到「特征极致复用 + 梯度流极强 + 参数更少」。

## 密集连接 vs 残差连接

- **ResNet**：`输出 = F(x) + x`，是「**加**」；
- **DenseNet**：`x_l = H([x_0, x_1, …, x_{l-1}])`，是「**拼**」（通道维拼接）。

DenseNet 里每一层都能直接看到前面**所有**层的特征，所以特征复用极致、梯度流极强；但也因此通道数随层数暴涨，需要**过渡层（1×1 卷积）**把通道数压回去。
"""))

cells.append(code(ENV))

cells.append(code("""# ---- 定义 DenseNet ----
from torch import nn

def conv_block(input_channels, num_channels):
    return nn.Sequential(
        nn.BatchNorm2d(input_channels), nn.ReLU(),
        nn.Conv2d(input_channels, num_channels, kernel_size=3, padding=1))

class DenseBlock(nn.Module):
    '''密集块：每层输出拼接到前面所有层，通道数按增长率 growth_rate 递增。'''
    def __init__(self, num_convs, input_channels, num_channels):
        super().__init__()
        layer = []
        for i in range(num_convs):
            layer.append(conv_block(num_channels * i + input_channels, num_channels))
        self.net = nn.Sequential(*layer)
    def forward(self, X):
        for blk in self.net:
            Y = blk(X)
            X = torch.cat((X, Y), dim=1)   # 🔑 密集连接：通道维拼接
        return X

def transition_block(input_channels, num_channels):
    return nn.Sequential(
        nn.BatchNorm2d(input_channels), nn.ReLU(),
        nn.Conv2d(input_channels, num_channels, kernel_size=1),   # 1×1 卷积压通道
        nn.AvgPool2d(kernel_size=2, stride=2))                     # 池化减尺寸

def densenet():
    b1 = nn.Sequential(
        nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3),
        nn.BatchNorm2d(64), nn.ReLU(),
        nn.MaxPool2d(kernel_size=3, stride=2, padding=1))
    num_channels, growth_rate = 64, 32
    num_convs_in_dense_blocks = [4, 4, 4, 4]
    blks = []
    for i, num_convs in enumerate(num_convs_in_dense_blocks):
        blks.append(DenseBlock(num_convs, num_channels, growth_rate))
        num_channels += num_convs * growth_rate
        if i != len(num_convs_in_dense_blocks) - 1:
            blks.append(transition_block(num_channels, num_channels // 2))
            num_channels = num_channels // 2
    return nn.Sequential(b1, *blks,
        nn.BatchNorm2d(num_channels), nn.ReLU(),
        nn.AdaptiveAvgPool2d((1, 1)), nn.Flatten(), nn.Linear(num_channels, 10))

net = densenet()
X = torch.rand(1, 1, 96, 96)
print("DenseNet 输出形状：", tuple(net(X).shape))
print("参数总量：", sum(p.numel() for p in net.parameters()), "（注意：比同规模 ResNet 少，因为特征复用）")
"""))

cells.append(md("""## 2. 训练 sanity check

DenseNet 同样是大网络，完整训练需 GPU。这里跑一个 batch 确认前向/反向正常。
"""))

cells.append(code("""# ---- 训练 sanity check ----
from torchvision import datasets, transforms
from torch.utils import data

trans = transforms.Compose([transforms.ToTensor(), transforms.Resize(96)])
tr = datasets.FashionMNIST(root='../data', train=True, transform=trans, download=True)
it = data.DataLoader(tr, 64, shuffle=True)

loss = nn.CrossEntropyLoss()
trainer = torch.optim.SGD(net.parameters(), lr=0.1)

net.train()
X, y = next(iter(it))
l = loss(net(X), y); trainer.zero_grad(); l.backward(); trainer.step()
print(f"第一个 batch 损失 {l.item():.4f}（随机水平），前向/反向正常 ✔")
print("完整训练需 GPU + 全量数据。")
"""))

cells.append(md("""## 小结

| 概念 | 一句话直觉 |
| --- | --- |
| 密集连接 | 每层输出拼接到前面所有层 |
| 增长率 growth_rate | 每个卷积层新增的通道数 |
| 过渡层 | 1×1 卷积压通道 + 池化减尺寸 |

> 🔑 **记忆**：ResNet 是「**加**」（`F(x)+x`），DenseNet 是「**拼**」（`[x_0,…,x_{l-1}]` 通道拼接）。DenseNet 把特征复用做到极致，参数量反而更少，但内存占用大（通道数增长快）。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\DenseNet.ipynb", cells)

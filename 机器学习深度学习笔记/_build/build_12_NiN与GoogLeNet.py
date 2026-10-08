# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# NiN 与 GoogLeNet · 两个「改造全连接 / 并行多尺度」的思路（PyTorch）

> 📌 **出处**：李沐《动手学深度学习 V2》第 7 章「NiN / GoogLeNet」
> 🎯 **目标**：搞懂两个关键发明——**NiN 的 1×1 卷积 + 全局平均池化**，以及 **GoogLeNet 的 Inception 并行多尺度块**。

## 第一部分 · NiN（Network in Network，2013）

传统 CNN 末尾接一大段**全连接层**，参数巨多、易过拟合。NiN 的两个替代思路：

- **1×1 卷积**：在每个像素位置对「通道」做线性组合 + 非线性，等价于逐像素的全连接，参数少得多，还能灵活调通道数；
- **全局平均池化（Global Avg Pooling）**：把每张特征图求平均，直接得到「每类一个分数」，**彻底丢掉 FC 层**。

NiN 块 = `Conv(3×3) + Conv(1×1) + Conv(1×1)`，各接 ReLU。
"""))

cells.append(code(ENV))

cells.append(code("""# ---- 定义 NiN ----
from torch import nn

def nin_block(in_channels, out_channels, kernel_size, strides, padding):
    return nn.Sequential(
        nn.Conv2d(in_channels, out_channels, kernel_size, strides, padding), nn.ReLU(),
        nn.Conv2d(out_channels, out_channels, kernel_size=1), nn.ReLU(),   # 1×1 卷积
        nn.Conv2d(out_channels, out_channels, kernel_size=1), nn.ReLU())

net_nin = nn.Sequential(
    nin_block(1, 96, kernel_size=11, strides=4, padding=0),
    nn.MaxPool2d(3, stride=2),
    nin_block(96, 256, kernel_size=5, strides=1, padding=2),
    nn.MaxPool2d(3, stride=2),
    nin_block(256, 384, kernel_size=3, strides=1, padding=1),
    nn.MaxPool2d(3, stride=2), nn.Dropout(0.5),
    nin_block(384, 10, kernel_size=3, strides=1, padding=1),
    nn.AdaptiveAvgPool2d((1, 1)),   # 全局平均池化：替代全连接
    nn.Flatten())

X = torch.rand(1, 1, 224, 224)
print("NiN 输出形状：", tuple(net_nin(X).shape), "（每类一个分数，无全连接层）")
print("NiN 参数总量：", sum(p.numel() for p in net_nin.parameters()))
"""))

cells.append(md("""## 第二部分 · GoogLeNet（2014）：Inception 块

GoogLeNet 的 **Inception 块**让输入同时走 **4 条并行支路**（1×1、3×3、5×5 卷积 + 3×3 最大池化），再**通道维拼接**——同一层捕捉不同尺度特征。每条支路前后用 **1×1 卷积做「瓶颈」降维**，省算力。
"""))

cells.append(code("""# ---- 定义 GoogLeNet（Inception）----
class Inception(nn.Module):
    def __init__(self, in_channels, c1, c2, c3, c4):
        super().__init__()
        self.p1_1 = nn.Conv2d(in_channels, c1, kernel_size=1)
        self.p2_1 = nn.Conv2d(in_channels, c2[0], kernel_size=1)
        self.p2_2 = nn.Conv2d(c2[0], c2[1], kernel_size=3, padding=1)
        self.p3_1 = nn.Conv2d(in_channels, c3[0], kernel_size=1)
        self.p3_2 = nn.Conv2d(c3[0], c3[1], kernel_size=5, padding=2)
        self.p4_1 = nn.MaxPool2d(kernel_size=3, stride=1, padding=1)
        self.p4_2 = nn.Conv2d(in_channels, c4, kernel_size=1)
    def forward(self, x):
        p1 = torch.relu(self.p1_1(x))
        p2 = torch.relu(self.p2_2(torch.relu(self.p2_1(x))))
        p3 = torch.relu(self.p3_2(torch.relu(self.p3_1(x))))
        p4 = torch.relu(self.p4_2(self.p4_1(x)))
        return torch.cat((p1, p2, p3, p4), dim=1)   # 通道维拼接

b1 = nn.Sequential(nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3), nn.ReLU(),
                   nn.MaxPool2d(kernel_size=3, stride=2, padding=1))
b2 = nn.Sequential(nn.Conv2d(64, 64, kernel_size=1), nn.ReLU(),
                   nn.Conv2d(64, 192, kernel_size=3, padding=1), nn.ReLU(),
                   nn.MaxPool2d(kernel_size=3, stride=2, padding=1))
b3 = nn.Sequential(Inception(192, 64, (96, 128), (16, 32), 32),
                   Inception(256, 128, (128, 192), (32, 96), 64),
                   nn.MaxPool2d(kernel_size=3, stride=2, padding=1))
b4 = nn.Sequential(Inception(480, 192, (96, 208), (16, 48), 64),
                   Inception(512, 160, (112, 224), (24, 64), 64),
                   Inception(512, 128, (128, 256), (24, 64), 64),
                   Inception(512, 112, (144, 288), (32, 64), 64),
                   Inception(528, 256, (160, 320), (32, 128), 128),
                   nn.MaxPool2d(kernel_size=3, stride=2, padding=1))
b5 = nn.Sequential(Inception(832, 256, (160, 320), (32, 128), 128),
                   Inception(832, 384, (192, 384), (48, 128), 128),
                   nn.AdaptiveAvgPool2d((1, 1)), nn.Flatten())
net_google = nn.Sequential(b1, b2, b3, b4, b5, nn.Linear(1024, 10))

X = torch.rand(1, 1, 96, 96)   # GoogLeNet 用 96×96
print("GoogLeNet 输出形状：", tuple(net_google(X).shape))
print("GoogLeNet 参数总量：", sum(p.numel() for p in net_google.parameters()))
"""))

cells.append(md("""## 3. 训练 sanity check

NiN / GoogLeNet 同样是大网络，完整训练需 GPU。这里各跑一个 batch 确认前向/反向正常。
"""))

cells.append(code("""# ---- 训练 sanity check ----
from torchvision import datasets, transforms
from torch.utils import data

loss = nn.CrossEntropyLoss()

for name, net, resize in [("NiN", net_nin, 224), ("GoogLeNet", net_google, 96)]:
    trans = transforms.Compose([transforms.ToTensor(), transforms.Resize(resize)])
    tr = datasets.FashionMNIST(root='../data', train=True, transform=trans, download=True)
    it = data.DataLoader(tr, 64, shuffle=True)
    trainer = torch.optim.SGD(net.parameters(), lr=0.1)
    net.train()
    X, y = next(iter(it))
    l = loss(net(X), y); trainer.zero_grad(); l.backward(); trainer.step()
    print(f"{name}: 第一个 batch 损失 {l.item():.4f}（随机水平），前向/反向正常 ✔")
"""))

cells.append(md("""## 小结

| 概念 | 一句话直觉 |
| --- | --- |
| 1×1 卷积 | 逐像素调通道 + 加非线性，参数少 |
| 全局平均池化 | 每通道求平均 → 每类一分数，替代 FC |
| Inception 块 | 4 条不同尺度支路并行，通道维拼接 |
| 1×1 瓶颈 | 降维省算力 |

> 🔑 **记忆**：**1×1 卷积**是「调通道 + 加非线性」的万能工具；**Inception = 多尺度并行 + 拼接**；二者都让网络「更聪明地」使用参数。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\NiN与GoogLeNet.ipynb", cells)

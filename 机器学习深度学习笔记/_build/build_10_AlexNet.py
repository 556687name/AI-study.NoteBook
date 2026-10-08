# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# AlexNet · 深度学习的「引爆点」（PyTorch）

> 📌 **出处**：李沐《动手学深度学习 V2》第 7 章「AlexNet」
> 🎯 **目标**：搭出 2012 年 ImageNet 冠军 **AlexNet**，理解它凭什么把 CNN 从 LeNet 的「玩具」变成「主力」。

## AlexNet 相比 LeNet 的三大升级

| 升级 | 作用 |
| --- | --- |
| **更深更宽** | 5 个卷积层 + 3 个全连接层，通道数上千 |
| **ReLU 激活** | 比 sigmoid 训练快得多，缓解梯度消失 |
| **Dropout + 数据增广** | 抑制过拟合（当时没这么多数据） |
| **最大池化** | 取代 LeNet 的平均池化 |

> 💡 AlexNet 是「大数据 + 大模型 + GPU」路线的开端——它证明了**只要数据够多、算力够强，深度学习就能赢**。
"""))

cells.append(code(ENV))

cells.append(md("""## 1. 定义 AlexNet（输入 224×224）

第一层用 **11×11 大卷积核、步长 4**，后面换成 5×5、3×3。注意 Fashion-MNIST 是 28×28 灰度图，要先 `Resize` 到 224×224（单通道），否则大卷积核会把图压没了。
"""))

cells.append(code("""# ---- 定义 AlexNet ----
from torch import nn

net = nn.Sequential(
    nn.Conv2d(1, 96, kernel_size=11, stride=4, padding=1), nn.ReLU(),   # 224→54
    nn.MaxPool2d(kernel_size=3, stride=2),                               # 54→26
    nn.Conv2d(96, 256, kernel_size=5, padding=2), nn.ReLU(),             # 26→26
    nn.MaxPool2d(kernel_size=3, stride=2),                               # 26→12
    nn.Conv2d(256, 384, kernel_size=3, padding=1), nn.ReLU(),            # 12→12
    nn.Conv2d(384, 384, kernel_size=3, padding=1), nn.ReLU(),            # 12→12
    nn.Conv2d(384, 256, kernel_size=3, padding=1), nn.ReLU(),            # 12→12
    nn.MaxPool2d(kernel_size=3, stride=2),                               # 12→5
    nn.Flatten(),                                                        # 256×5×5=6400
    nn.Linear(6400, 4096), nn.ReLU(), nn.Dropout(p=0.5),                 # 全连接
    nn.Linear(4096, 4096), nn.ReLU(), nn.Dropout(p=0.5),
    nn.Linear(4096, 10),
)

# 用一张假图走一遍前向，确认尺寸链正确
X = torch.rand(1, 1, 224, 224)
for layer in net:
    X = layer(X)
    if hasattr(layer, 'weight') and layer.weight.dim() == 4 or layer.__class__.__name__ in ('Flatten',):
        print(f"{layer.__class__.__name__:14s} 输出形状：{tuple(X.shape)}")
print("\\n参数总量：", sum(p.numel() for p in net.parameters()))
"""))

cells.append(md("""## 2. 训练 sanity check：确认前向 / 反向能跑通

AlexNet 有约 **5800 万参数**，完整训练（60k 张 224×224 图 × 几十轮）需要 GPU——CPU 上单 epoch 就要十几分钟，且几十个 batch 内几乎不会看到准确率上升。这里只跑几个 batch 做**冒烟测试**：确认前向、反向、参数更新都正常。
"""))

cells.append(code("""# ---- 训练 sanity check（完整训练需 GPU）----
from torchvision import datasets, transforms
from torch.utils import data

trans = transforms.Compose([transforms.ToTensor(), transforms.Resize(224)])
tr = datasets.FashionMNIST(root='../data', train=True, transform=trans, download=True)
train_iter = data.DataLoader(tr, 64, shuffle=True)

loss = nn.CrossEntropyLoss()
trainer = torch.optim.SGD(net.parameters(), lr=0.01)   # d2l 官方学习率

net.train()
for i, (X, y) in enumerate(train_iter):
    l = loss(net(X), y)
    trainer.zero_grad(); l.backward(); trainer.step()
    if i == 0:
        print(f"第 1 个 batch：损失 {l.item():.4f}（≈ ln10 = 2.30，随机水平，训练前正常）")
    if i >= 8:
        break
print("\\n→ 前向 / 反向传播正常，模型可以训练。")
print("→ 完整训练到高准确率需要 GPU + 全量数据；训练循环与 LeNet 完全一致（见 LeNet.ipynb）。")
"""))

cells.append(md("""## 小结

| 概念 | 一句话直觉 |
| --- | --- |
| 大卷积核 | 第一层 11×11 抓大范围结构 |
| ReLU | 训练快、不饱和、缓解梯度消失 |
| Dropout | 全连接层随机丢神经元，防过拟合 |
| 深度+宽度 | AlexNet 用「更大」证明了深度学习的威力 |

> 🔑 **记忆**：AlexNet = LeNet 骨架 + **ReLU / Dropout / 最大池化 / 数据增广**，靠「又大又深」拿下 ImageNet，开启深度学习时代。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\AlexNet.ipynb", cells)

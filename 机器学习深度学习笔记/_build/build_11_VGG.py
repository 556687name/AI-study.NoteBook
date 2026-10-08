# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# VGG · 用「卷积块」堆出又深又规整的网络（PyTorch）

> 📌 **出处**：李沐《动手学深度学习 V2》第 7 章「VGG」
> 🎯 **目标**：理解 VGG 的核心思想——**只用 3×3 小卷积核，把「若干卷积 + 一个池化」打包成「块」反复堆叠**，让网络又深又规整。

## 为什么用多个 3×3 代替一个大核

两个 3×3 卷积的感受野 = 一个 5×5；三个 3×3 = 一个 7×7。但**参数量更少、非线性更多**（每个卷积后都能过 ReLU），所以表达能力更强。
"""))

cells.append(code(ENV))

cells.append(md("""## 1. 定义 VGG-11

`vgg_block` 打包「`num_convs` 个 3×3 卷积 + 一个 2×2 池化」；通道数逐块翻倍（64→128→256→512→512），尺寸逐块减半。VGG-11 共 8 个卷积 + 3 个全连接。
"""))

cells.append(code("""# ---- 定义 VGG ----
from torch import nn

def vgg_block(num_convs, in_channels, out_channels):
    layers = []
    for _ in range(num_convs):
        layers.append(nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1))
        layers.append(nn.ReLU())
        in_channels = out_channels
    layers.append(nn.MaxPool2d(kernel_size=2, stride=2))   # 块尾池化，尺寸减半
    return nn.Sequential(*layers)

conv_arch = ((1, 64), (1, 128), (2, 256), (2, 512), (2, 512))   # (卷积数, 输出通道)

def vgg(conv_arch):
    conv_blks = []
    in_channels = 1
    for (num_convs, out_channels) in conv_arch:
        conv_blks.append(vgg_block(num_convs, in_channels, out_channels))
        in_channels = out_channels
    return nn.Sequential(*conv_blks, nn.Flatten(),
        nn.Linear(out_channels * 7 * 7, 4096), nn.ReLU(), nn.Dropout(0.5),   # 224/2⁵=7
        nn.Linear(4096, 4096), nn.ReLU(), nn.Dropout(0.5),
        nn.Linear(4096, 10))

net = vgg(conv_arch)

# 形状验证：224×224 走一遍
X = torch.rand(1, 1, 224, 224)
for blk in net:
    X = blk(X)
    if isinstance(blk, nn.Sequential):
        print(f"块输出形状：{tuple(X.shape)}")
print("\\n参数总量：", sum(p.numel() for p in net.parameters()))
"""))

cells.append(md("""## 2. 训练 sanity check

VGG-11 有约 **1.3 亿参数**（比 AlexNet 还大），完整训练必须用 GPU。这里跑几个 batch 确认前向/反向正常。
"""))

cells.append(code("""# ---- 训练 sanity check（完整训练需 GPU）----
from torchvision import datasets, transforms
from torch.utils import data

trans = transforms.Compose([transforms.ToTensor(), transforms.Resize(224)])
tr = datasets.FashionMNIST(root='../data', train=True, transform=trans, download=True)
train_iter = data.DataLoader(tr, 64, shuffle=True)

loss = nn.CrossEntropyLoss()
trainer = torch.optim.SGD(net.parameters(), lr=0.05)   # d2l 官方学习率

net.train()
for i, (X, y) in enumerate(train_iter):
    l = loss(net(X), y)
    trainer.zero_grad(); l.backward(); trainer.step()
    if i == 0:
        print(f"第 1 个 batch：损失 {l.item():.4f}（≈ ln10 = 2.30，随机水平）")
    if i >= 5:
        break
print("\\n→ 前向 / 反向传播正常，模型可以训练。完整训练需 GPU + 全量数据。")
"""))

cells.append(md("""## 小结

| 概念 | 一句话直觉 |
| --- | --- |
| VGG 块 | 若干 3×3 卷积 + 一个池化，反复堆叠 |
| 小核代替大核 | 感受野相同，但参数少、非线性多 |
| 通道翻倍/尺寸减半 | 空间分辨率降，语义通道涨 |

> 🔑 **记忆**：VGG 的哲学 = **「小卷积核 + 规整块」**。`3×3 + padding=1` 保持尺寸，靠池化减半，网络又深又规整、好迁移。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\VGG.ipynb", cells)

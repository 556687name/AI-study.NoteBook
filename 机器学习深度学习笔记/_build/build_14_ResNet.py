# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# ResNet · 残差连接让网络可以非常深（PyTorch）

> 📌 **出处**：李沐《动手学深度学习 V2》第 7 章「ResNet」
> 🎯 **目标**：搭出 ResNet-18，理解**残差连接** `输出 = F(x) + x` 如何缓解深层网络的梯度消失，让网络能堆到几十上百层。

## 残差块（Residual Block）

每个残差块把输入 `x` 直接「抄近路」加到两层卷积的输出上：

$$\\text{输出} = \\mathrm{ReLU}(F(x) + x)$$

- 梯度能沿捷径直接回传，**缓解梯度消失**；
- 网络学习目标变成「学残差 `F(x) = H(x) - x`」，比学整个映射更容易；
- ResNet 里每个卷积后都配 **BatchNorm**（上一节），训练更稳。
"""))

cells.append(code(ENV))

cells.append(code("""# ---- 定义 ResNet-18 ----
from torch import nn

class Residual(nn.Module):
    '''残差块：两条 3×3 卷积（各带 BN），输出 + 输入 x 再过 ReLU。'''
    def __init__(self, input_channels, num_channels, use_1x1conv=False, strides=1):
        super().__init__()
        self.conv1 = nn.Conv2d(input_channels, num_channels, kernel_size=3, padding=1, stride=strides)
        self.conv2 = nn.Conv2d(num_channels, num_channels, kernel_size=3, padding=1)
        if use_1x1conv:
            self.conv3 = nn.Conv2d(input_channels, num_channels, kernel_size=1, stride=strides)
        else:
            self.conv3 = None
        self.bn1 = nn.BatchNorm2d(num_channels)
        self.bn2 = nn.BatchNorm2d(num_channels)

    def forward(self, X):
        Y = torch.relu(self.bn1(self.conv1(X)))
        Y = self.bn2(self.conv2(Y))
        if self.conv3:
            X = self.conv3(X)      # 通道数/尺寸不一致时，用 1×1 卷积对齐
        Y += X                     # 🔑 残差连接：F(x) + x
        return torch.relu(Y)

def resnet_block(input_channels, num_channels, num_residuals, first_block=False):
    blk = []
    for i in range(num_residuals):
        if i == 0 and not first_block:
            blk.append(Residual(input_channels, num_channels, use_1x1conv=True, strides=2))
        else:
            blk.append(Residual(num_channels, num_channels))
    return blk

b1 = nn.Sequential(nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3),
                   nn.BatchNorm2d(64), nn.ReLU(),
                   nn.MaxPool2d(kernel_size=3, stride=2, padding=1))

def resnet18():
    b2 = nn.Sequential(*resnet_block(64, 64, 2, first_block=True))
    b3 = nn.Sequential(*resnet_block(64, 128, 2))
    b4 = nn.Sequential(*resnet_block(128, 256, 2))
    b5 = nn.Sequential(*resnet_block(256, 512, 2))
    return nn.Sequential(b1, b2, b3, b4, b5,
                         nn.AdaptiveAvgPool2d((1, 1)), nn.Flatten(), nn.Linear(512, 10))

net = resnet18()
X = torch.rand(1, 1, 96, 96)   # ResNet 用 96×96
print("ResNet-18 输出形状：", tuple(net(X).shape))
print("参数总量：", sum(p.numel() for p in net.parameters()))
"""))

cells.append(md("""## 2. 训练 sanity check

ResNet-18 有约 1100 万参数，完整训练需 GPU。这里跑一个 batch 确认前向/反向正常（注意它大量用了 BatchNorm）。
"""))

cells.append(code("""# ---- 训练 sanity check ----
from torchvision import datasets, transforms
from torch.utils import data

trans = transforms.Compose([transforms.ToTensor(), transforms.Resize(96)])
tr = datasets.FashionMNIST(root='../data', train=True, transform=trans, download=True)
it = data.DataLoader(tr, 64, shuffle=True)

loss = nn.CrossEntropyLoss()
trainer = torch.optim.SGD(net.parameters(), lr=0.05)   # d2l 官方学习率

net.train()
X, y = next(iter(it))
l = loss(net(X), y); trainer.zero_grad(); l.backward(); trainer.step()
print(f"第一个 batch 损失 {l.item():.4f}（随机水平），前向/反向正常 ✔")
print("完整训练需 GPU + 全量数据；ResNet 残差连接的训练代码结构与此完全一致。")
"""))

cells.append(md("""## 小结

| 概念 | 一句话直觉 |
| --- | --- |
| 残差连接 | 输出 = F(x) + x，梯度走捷径 |
| 1×1 对齐 | 通道/尺寸不一致时对齐再相加 |
| 残差块 | 两层 3×3 卷积 + BN + 跳跃连接 |

> 🔑 **记忆**：ResNet 的**残差连接 `F(x) + x`** 是让网络能变深的钥匙——梯度沿捷径直传，缓解梯度消失。ResNet = **卷积 + BatchNorm + 残差连接**的组合，是至今仍在大量使用的骨干网络。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\ResNet.ipynb", cells)

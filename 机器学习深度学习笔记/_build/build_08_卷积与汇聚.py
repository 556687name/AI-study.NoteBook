# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# 卷积与汇聚（池化）· 从零理解核心运算（PyTorch）

> 📌 **出处**：李沐《动手学深度学习 V2》第 6 章「图像卷积 / 填充和步幅 / 多输入多输出通道 / 汇聚层」
> 🎯 **目标**：彻底搞懂 **卷积** 和 **汇聚** 这两个 CNN 的核心运算——从「手写 2D 卷积」到理解 `nn.Conv2d` 的每个参数。

## 为什么是卷积

全连接层把图片展平成 1 维，会**丢失空间结构**（相邻像素的关系）。卷积用一个小窗口（卷积核）在图上**滑动**，每个位置只关注局部，天然保留空间信息，而且**参数共享**（一个核全图复用），参数量大幅下降。
"""))

cells.append(code(ENV))

cells.append(md("""## 1. 手写二维卷积：卷积核在图上滑动

卷积 = 卷积核在每个位置「对应相乘再求和」。下面手写一个 `corr2d`（互相关运算），并分别用「垂直边缘」「水平边缘」两个卷积核去看效果。
"""))

cells.append(code("""# ---- 手写二维卷积（互相关运算） ----
def corr2d(X, K):
    '''二维互相关：卷积核 K 在输入 X 上滑动，逐位置对应相乘求和。'''
    h, w = K.shape
    Y = torch.zeros((X.shape[0] - h + 1, X.shape[1] - w + 1))
    for i in range(Y.shape[0]):
        for j in range(Y.shape[1]):
            Y[i, j] = (X[i:i + h, j:j + w] * K).sum()
    return Y

# 一张 6×8 的图：左边黑（0）右边白（1），中间有一条垂直边缘
X = torch.ones(6, 8)
X[:, 2:6] = 0
print("输入图（1=白，0=黑）：\\n", X)

# 垂直边缘检测核：1×2 的核 [1, -1]，检测「左到右」的变化
K = torch.tensor([[1.0, -1.0]])
Y = corr2d(X, K)
print("\\n垂直边缘检测结果（非零处就是边缘）：\\n", Y)
"""))

cells.append(md("""## 2. 学习卷积核：让机器自己「学」出边缘检测器

有趣的实验：只给机器「输入图 + 真实边缘」，让它用梯度下降**自己学出**卷积核。结果会惊人地接近 `[1, -1]` 这个手工设计的边缘核。
"""))

cells.append(code("""# ---- 学习卷积核：梯度下降学出边缘检测核 ----
K = torch.randn(1, 2, requires_grad=True)   # 随机初始化一个 1×2 核
Y_true = corr2d(X, torch.tensor([[1.0, -1.0]]))   # 真实边缘（目标）

lr = 0.1
for step in range(40):
    Y_pred = corr2d(X, K)                  # 前向：用当前核算卷积
    l = ((Y_pred - Y_true) ** 2).mean()    # 损失：和真实边缘的平均平方误差
    l.backward()                           # 反向求核的梯度
    with torch.no_grad():
        K -= lr * K.grad                   # 更新核
        K.grad.zero_()
    if step % 10 == 0:
        print(f"step {step}: loss {l.item():.4f}")

print("\\n学到的核：", K.detach().numpy(), "（目标是 [[1, -1]]）")
"""))

cells.append(md("""## 3. 填充与步幅：控制输出尺寸

- **填充 padding**：在输入四周补 0，让输出不至于越缩越小；
- **步幅 stride**：卷积核每次滑多远。

输出尺寸公式：$\\lfloor (n_h - k_h + p_h + s_h)/s_h \\rfloor \\times \\lfloor (n_w - k_w + p_w + s_w)/s_w \\rfloor$（忽略 $p,s$ 下标简化理解即可）。
"""))

cells.append(code("""# ---- 填充与步幅 ----
def comp_conv2d(conv2d, X):
    X = X.reshape((1, 1) + X.shape)          # 加 batch 维和通道维
    Y = conv2d(X)
    return Y.reshape(Y.shape[2:])            # 去掉前两维

import torch.nn as nn
X = torch.rand(8, 8)

print("卷积核 3×3 无填充：", tuple(comp_conv2d(nn.Conv2d(1, 1, kernel_size=3), X).shape))          # (6,6)
print("卷积核 3×3 填充 1 ：", tuple(comp_conv2d(nn.Conv2d(1, 1, kernel_size=3, padding=1), X).shape))  # (8,8)
print("卷积核 3×3 步幅 2 ：", tuple(comp_conv2d(nn.Conv2d(1, 1, kernel_size=3, stride=2), X).shape))  # (3,3)
print("卷积核 3×3 填充1步幅2：", tuple(comp_conv2d(nn.Conv2d(1, 1, kernel_size=3, padding=1, stride=2), X).shape))  # (4,4)
"""))

cells.append(md("""## 4. 多输入多输出通道：彩色图与多特征图

真实图片有 **3 个通道**（RGB），CNN 也要输出**多个特征图**。`nn.Conv2d(in_channels, out_channels, ...)` 的两个参数就是这个含义——每个输出通道对应一个独立的卷积核，各通道的结果**相加**。
"""))

cells.append(code("""# ---- 多输入多输出通道 ----
def corr2d_multi_in_out(X, K):
    '''多通道卷积：对每个输出通道，把「输入各通道 × 对应核」的结果相加。'''
    return torch.stack([corr2d(X, k) for k in K], 0)   # 演示：单输入通道，多个输出核

X = torch.rand(3, 3)
K = torch.stack([torch.tensor([[1.0, 0], [0, -1.0]]),   # 核 1：检测某种模式
                 torch.tensor([[0.0, 1], [1, 0.0]])])   # 核 2：检测另一种模式
Y = corr2d_multi_in_out(X, K)
print("多输出通道结果形状：", tuple(Y.shape), "（2 个输出通道，每个 2×2）")

# 用 nn.Conv2d 直接做 3 通道 → 6 通道
conv = nn.Conv2d(3, 6, kernel_size=3, padding=1)
rgb = torch.rand(1, 3, 32, 32)   # 1 张 32×32 的 RGB 图
print("3 通道输入 → 6 通道输出：", tuple(conv(rgb).shape))
"""))

cells.append(md("""## 5. 汇聚层（池化）：压缩信息、提取主导特征

汇聚也是滑动窗口，但**不做加权求和**，而是取窗口内的统计量——**最大池化**（取最大）或**平均池化**（取平均）。作用：**缩小尺寸、增强平移不变性**。

> 💡 汇聚层**没有可学习参数**，所以它不参与梯度更新。
"""))

cells.append(code("""# ---- 最大池化 vs 平均池化 ----
def pool2d(X, pool_size, mode='max'):
    p_h, p_w = pool_size
    Y = torch.zeros((X.shape[0] - p_h + 1, X.shape[1] - p_w + 1))
    for i in range(Y.shape[0]):
        for j in range(Y.shape[1]):
            window = X[i:i + p_h, j:j + p_w]
            Y[i, j] = window.max() if mode == 'max' else window.mean()
    return Y

X = torch.tensor([[0.0, 1.0, 2.0],
                  [3.0, 4.0, 5.0],
                  [6.0, 7.0, 8.0]])
print("输入：\\n", X)
print("最大池化（2×2）：\\n", pool2d(X, (2, 2), 'max'))   # 取每个 2×2 窗口的最大值
print("平均池化（2×2）：\\n", pool2d(X, (2, 2), 'avg'))   # 取每个 2×2 窗口的平均值

# nn 自带池化层
X4 = torch.rand(1, 1, 8, 8)
print("\\nnn.MaxPool2d(2) 输出：", tuple(nn.MaxPool2d(2)(X4).shape))   # 8×8 → 4×4
"""))

cells.append(md("""## 小结

| 概念 | 一句话直觉 |
| --- | --- |
| 卷积 | 小窗口滑动 + 对应相乘求和，提取局部特征 |
| 填充/步幅 | 控制输出尺寸的两个参数 |
| 多通道 | 输入 RGB=3 通道；输出多特征图，每通道一个核 |
| 汇聚（池化） | 取窗口统计量，缩小尺寸、增强平移不变，无可学习参数 |

> 🔑 **记忆**：`nn.Conv2d(in, out, kernel_size, padding, stride)` 和 `nn.MaxPool2d(size)` 是 CNN 的两块基本积木，下一节用它们搭 LeNet。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\卷积与汇聚层.ipynb", cells)

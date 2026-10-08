# -*- coding: utf-8 -*-
"""批次3融合：李沐 d2l 的现代 CNN（AlexNet/VGG/NiN/GoogLeNet/BatchNorm/DenseNet）并入第 12 章。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, load_nb, save_json

NB = r"D:\NoteBook\机器学习深度学习笔记\机器学习深度学习完整笔记.ipynb"
nb = load_nb(NB)
cells = nb["cells"]

alexnet = md("""## 12.6 【李沐 d2l】AlexNet：第一个「又深又宽」的 CNN（2012）

> 📌 **出处**：李沐《动手学深度学习 V2》第 7 章「AlexNet」
> 📎 **完整可运行代码**：`实战代码_李沐/AlexNet.ipynb`

LeNet（1998）之后沉寂了近 14 年，直到 2012 年 **AlexNet** 在 ImageNet 上把错误率从 26% 降到 15%，才引爆了深度学习。它和 LeNet 骨架相似（卷积→池化→全连接），但**更宽更深**，并用了几个关键新技巧：

| 技巧 | 作用 |
| --- | --- |
| **ReLU** 激活 | 比 sigmoid/tanh 训练快得多，缓解梯度消失 |
| **Dropout** | 在 FC 层随机丢神经元，抑制过拟合 |
| **最大池化** | 取代 LeNet 的平均池化 |
| **数据增广** | 翻转/裁剪扩充训练集 |
| **GPU 训练** | 两张 GPU 并行（现代已普及） |

结构（输入 224×224，第一层用 **11×11 大卷积核**、步长 4）：

```
Conv(11×11, s=4) → MaxPool(3×3, s=2) → Conv(5×5) → MaxPool(3×3, s=2)
→ Conv(3×3) ×3 → MaxPool(3×3, s=2) → FC(4096) → FC(4096) → FC(10)
```

> 🔑 **记忆**：AlexNet = LeNet 的「加深加宽版」+ **ReLU + Dropout + 最大池化**三件套，是「大数据 + 大模型 + GPU」路线的开端。
""")

vgg = md("""## 12.7 【李沐 d2l】VGG：用「卷积块」堆出又深又规整的网络（2014）

> 📌 **出处**：李沐《动手学深度学习 V2》第 7 章「VGG」
> 📎 **完整可运行代码**：`实战代码_李沐/VGG.ipynb`

AlexNet 的卷积核大小不一（11、5、3），结构杂乱。**VGG** 提出一个规整的想法：**只用 3×3 小卷积核，把「若干个 3×3 卷积 + 一个池化」打包成「VGG 块」，反复堆叠**。

为什么用**多个 3×3 代替一个大核**？

- 两个 3×3 的感受野 = 一个 5×5；三个 3×3 = 一个 7×7；
- 但参数量更少、非线性更多（每个卷积后都能过 ReLU），表达能力更强。

```
def vgg_block(num_convs, in_ch, out_ch):   # 一个 VGG 块
    layers = []
    for _ in range(num_convs):
        layers += [nn.Conv2d(in_ch, out_ch, 3, padding=1), nn.ReLU()]
        in_ch = out_ch
    layers += [nn.MaxPool2d(kernel_size=2, stride=2)]   # 块尾池化，尺寸减半
    return nn.Sequential(*layers)
```

VGG-11 就是「8 个卷积（5 个块）+ 3 个全连接」。通道数逐块翻倍（64→128→256→512→512），尺寸逐块减半。

> 🔑 **记忆**：VGG 的哲学 = **「小卷积核 + 规整块」**。用 `3×3 + padding=1` 保持尺寸不变，靠池化减半，网络又深又好看、容易迁移。
""")

nin = md("""## 12.8 【李沐 d2l】NiN：用「1×1 卷积」和「全局平均池化」替代全连接（2013）

> 📌 **出处**：李沐《动手学深度学习 V2》第 7 章「NiN（网络中的网络）」
> 📎 **完整可运行代码**：`实战代码_李沐/NiN与GoogLeNet.ipynb`

传统 CNN 最后接一大段**全连接层**，参数巨多、易过拟合。**NiN** 提出两个替代思路：

**① 1×1 卷积 = 逐像素的全连接层**：它在每个像素位置对「通道」做线性组合 + 非线性，等价于对每个位置独立跑一个全连接，但**参数少得多**，还能灵活调通道数（升维/降维）。

**② 全局平均池化（Global Avg Pooling）**：把最后一层每个通道的整张特征图**求平均**，直接得到「每类一个分数」，**彻底丢掉 FC 层**，几乎没参数、天然抗过拟合。

NiN 块 = `Conv(3×3) + Conv(1×1) + Conv(1×1)` 各接 ReLU；堆 4 个块，最后接全局平均池化。

> 🔑 **记忆**：**1×1 卷积**是「调通道数 + 加非线性」的利器（后面 GoogLeNet/ResNet 都在用）；**全局平均池化**是「扔掉 FC 层」的做法，参数少、不易过拟合。
""")

googlenet = md("""## 12.9 【李沐 d2l】GoogLeNet：Inception 块「多条支路并行」再拼接（2014）

> 📌 **出处**：李沐《动手学深度学习 V2》第 7 章「GoogLeNet」
> 📎 **完整可运行代码**：`实战代码_李沐/NiN与GoogLeNet.ipynb`

2014 年 ImageNet 冠军 **GoogLeNet** 的核心是 **Inception 块**：输入同时走 **4 条并行支路**（1×1 卷积、3×3 卷积、5×5 卷积、3×3 最大池化），再把结果在**通道维拼接**起来。这样网络能**在同一层捕捉不同尺度的特征**。

```
                ┌─ Conv(1×1)
                ├─ Conv(1×1) → Conv(3×3)
输入 ───────────┼─ Conv(1×1) → Conv(5×5)      → 通道维拼接
                ├─ MaxPool(3×3) → Conv(1×1)
                └────────────────
```

> 💡 每条支路前面/后面都插 **1×1 卷积做「瓶颈」降维**，把 3×3、5×5 的计算量压下来——这是它能在深度、宽度都远超 AlexNet 的同时还保持可控算力的关键。

> 🔑 **记忆**：**Inception 块 = 多条不同尺度支路并行 + 通道拼接**；**1×1 卷积瓶颈**用来降维省算力。
""")

batchnorm = md("""## 12.10 【李沐 d2l】批量规范化 BatchNorm：让每一层输入稳定（2015）

> 📌 **出处**：李沐《动手学深度学习 V2》第 7 章「批量规范化」
> 📎 **完整可运行代码**：`实战代码_李沐/批量规范化.ipynb`

训练深层网络时，每层输入的分布会随训练不断漂移（**内部协变量偏移**），导致要小心翼翼地调学习率。**批量规范化（BatchNorm）** 的做法：对每个**小批量**，把每个通道的激活值**归一化到均值 0、方差 1**，再用两个**可学习参数** $\\gamma$（缩放）和 $\\beta$（平移）拉回合适尺度：

$$\\hat x = \\frac{x - \\mu_\\text{batch}}{\\sqrt{\\sigma^2_\\text{batch} + \\epsilon}},\\qquad y = \\gamma \\hat x + \\beta$$

好处：

1. **训练更稳**，可以放心用**更大的学习率**，收敛更快；
2. 对参数初始化**不那么敏感**；
3. 自带一点**正则化**效果（每次用本批的统计量，有随机性）。

> ⚠️ **训练 vs 推理**：训练时用**本批**的均值/方差；推理时用**全局移动平均**的均值/方差（`nn.BatchNorm2d` 会自动切换）。BatchNorm 也**只能加在全连接层或卷积层之后、激活函数之前**。

> 🔑 **记忆**：BatchNorm = 「小批量归一化 + 可学习缩放平移」，把每层输入拉回标准分布，是训练深层网络（ResNet 等）的标配。
""")

densenet = md("""## 12.12 【李沐 d2l】DenseNet：每一层都连到「前面所有层」（2017）

> 📌 **出处**：李沐《动手学深度学习 V2》第 7 章「DenseNet」
> 📎 **完整可运行代码**：`实战代码_李沐/DenseNet.ipynb`

ResNet 让每层连到「上一层」；**DenseNet** 更激进：**每一层的输出都拼接到「前面所有层」的输入里**（**密集连接**）。

$$\\mathbf{x}_l = H([\\mathbf{x}_0, \\mathbf{x}_1, \\dots, \\mathbf{x}_{l-1}])$$

- `[...]` 表示**通道维拼接**（不是相加）；
- 好处：**特征极致复用**（后面的层能直接看到前面所有特征）、**梯度流极强**、**参数量反而更少**（因为每层不需要重新学已经有的特征）；
- 代价：特征图通道随层数增长，内存占用大——所以用「过渡层」用 1×1 卷积把通道数压回去。

> 🔑 **记忆**：ResNet 是「加」（残差 `F(x)+x`），DenseNet 是「**拼**」（密集连接 `[x₀,…,x_{l-1}]` 通道拼接）；两者都用「跳跃连接」解决深层梯度问题，DenseNet 把特征复用做到极致。
""")

def find(prefix):
    for i, c in enumerate(cells):
        if "".join(c["source"]).startswith(prefix):
            return i
    raise RuntimeError("未找到: " + prefix)

# ① ResNet 12.6 → 12.11，并在它之前插入 AlexNet/VGG/NiN/GoogLeNet/BatchNorm
resnet_idx = find("## 12.6 ResNet")
cells[resnet_idx]["source"] = "".join(cells[resnet_idx]["source"]).replace("## 12.6 ResNet", "## 12.11 ResNet", 1).splitlines(keepends=True)
cells[resnet_idx:resnet_idx] = [alexnet, vgg, nin, googlenet, batchnorm]

# ② 小结 12.7 → 12.13，并在它之前插入 DenseNet（12.12）
sum_idx = find("## 12.7 本章小结")
cells[sum_idx]["source"] = "".join(cells[sum_idx]["source"]).replace("## 12.7 本章小结", "## 12.13 本章小结", 1).splitlines(keepends=True)
cells[sum_idx:sum_idx] = [densenet]

save_json(nb, NB)
print("批次3融合完成 ✔  (第12章新增 AlexNet/VGG/NiN/GoogLeNet/BatchNorm/DenseNet)")

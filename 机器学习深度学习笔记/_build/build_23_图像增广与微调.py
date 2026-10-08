# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# 图像增广与微调 · 小数据的两大救星（PyTorch）

> 📌 **出处**：李沐《动手学深度学习 V2》第 13 章「图像增广 / 微调」
> 🎯 **目标**：① 用 torchvision 做**图像增广**（翻转/裁剪/颜色抖动）并可视化；② 理解**微调**——在大模型上改最后一层，用少量数据继续训练。

## 为什么这俩重要

数据少时模型容易过拟合，两大解法：**增广**（把现有数据「变多」）和**微调**（复用别人在 ImageNet 上训练好的特征，不用从零学）。
"""))

cells.append(code(ENV))

cells.append(md("""## 第一部分 · 图像增广：把一张图「变出」很多张

对训练图随机扰动，模型就见过更多变体，泛化更好。**增广只用于训练集**。
"""))

cells.append(code("""# ---- 加载一张样本图 ----
from torchvision import datasets, transforms
import torchvision.transforms.functional as TF

def load_loader(batch_size, train_aug=None):
    from torch.utils import data
    tr = datasets.FashionMNIST(root='../data', train=True, transform=train_aug, download=True)
    return data.DataLoader(tr, batch_size, shuffle=True)

# 取一张原始图
img, label = datasets.FashionMNIST(root='../data', train=True, download=True)[0]
print("原始图像形状：", img.size, " 标签：", label)
"""))

cells.append(code("""# ---- 可视化各种增广 ----
import matplotlib.pyplot as plt

aug_list = [
    ("原图", transforms.ToTensor()),
    ("水平翻转", transforms.Compose([transforms.RandomHorizontalFlip(p=1.0), transforms.ToTensor()])),
    ("随机裁剪+缩放", transforms.Compose([transforms.RandomResizedCrop(28, scale=(0.5, 1.0)), transforms.ToTensor()])),
    ("颜色抖动", transforms.Compose([transforms.ColorJitter(brightness=0.6, contrast=0.6, saturation=0.6), transforms.ToTensor()])),
    ("随机旋转", transforms.Compose([transforms.RandomRotation(30), transforms.ToTensor()])),
]

fig, axes = plt.subplots(1, len(aug_list), figsize=(13, 3))
for ax, (name, aug) in zip(axes, aug_list):
    ax.imshow(aug(img).squeeze(0), cmap='gray')
    ax.set_title(name, fontsize=10); ax.axis('off')
plt.suptitle("图像增广：同一张图的 5 种「变体」")
plt.show()
"""))

cells.append(md("""## 第二部分 · 微调：复用预训练权重，只改最后一层

微调三步：**① 拿一个在大数据集上训练好的模型 → ② 把最后一层（分类头）换成你的类别数 → ③ 用你的小数据继续训练**（可冻结 backbone 只训新头，也可全量微调）。

下面用一个**自包含的迁移演示**说明原理：先用「源任务」训练一个小 CNN，再把它的特征层复用去解「目标任务」，对比「从零训练」和「迁移微调」的收敛速度。
"""))

cells.append(code("""# ---- 自包含迁移演示：源任务(全部10类) -> 目标任务(4个服装类) ----
from torch import nn
import torch.nn.functional as F

def small_cnn(n_classes):
    return nn.Sequential(
        nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Flatten(), nn.Linear(32 * 7 * 7, 64), nn.ReLU(), nn.Linear(64, n_classes))

# 数据：源任务用全部 10 类，目标任务只用其中 4 个「服装类」
def make_loader(classes, batch_size=128, train=True):
    from torch.utils import data
    tr = datasets.FashionMNIST(root='../data', train=train, transform=transforms.ToTensor(), download=True)
    idx = [i for i, (_, y) in enumerate(tr) if y in classes]
    sub = torch.utils.data.Subset(tr, idx)
    class_map = {int(c): i for i, c in enumerate(classes)}   # 🔑 原始标签重映射成 0..k-1

    class Remap(data.Dataset):
        def __len__(self): return len(sub)
        def __getitem__(self, i):
            x, y = sub[i]
            return x, class_map[int(y)]
    return data.DataLoader(Remap(), batch_size, shuffle=True)

src_classes = list(range(10))
tgt_classes = [0, 2, 3, 4]     # T-shirt / Pullover / Dress / Coat（都是衣服，难区分）
train_src = make_loader(src_classes)
train_tgt = make_loader(tgt_classes)
test_tgt = make_loader(tgt_classes, train=False)
print("源任务训练样本：", len(train_src.dataset), " 目标任务训练样本：", len(train_tgt.dataset))
"""))

cells.append(code("""# ---- 源任务预训练（几轮即可，模拟 ImageNet 预训练）----
loss_fn = nn.CrossEntropyLoss()
def train_epochs(net, loader, epochs, lr=1e-3):
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    for _ in range(epochs):
        net.train()
        for X, y in loader:
            l = loss_fn(net(X), y); opt.zero_grad(); l.backward(); opt.step()

def accuracy(net, loader):
    net.eval()
    correct = sum((net(X).argmax(1) == y).sum().item() for X, y in loader)
    return correct / len(loader.dataset)

torch.manual_seed(0)
src_net = small_cnn(10)
train_epochs(src_net, train_src, epochs=3)
print("源任务（10类）测试准确率：", f"{accuracy(src_net, make_loader(src_classes, train=False)):.4f}")
"""))

cells.append(code("""# ---- 迁移微调：复用特征层，只换最后一层；对比从零训练 ----
def fine_tune_from(pretrained, n_classes, freeze=True):
    net = small_cnn(n_classes)
    # 只复制两个卷积层（索引 0、3）的权重，其他层（fc 等）重新初始化
    conv_idx = (0, 3)
    with torch.no_grad():
        for i in conv_idx:
            net[i].weight.copy_(pretrained[i].weight); net[i].bias.copy_(pretrained[i].bias)
    if freeze:
        for i in conv_idx:
            for p in net[i].parameters(): p.requires_grad = False
    return net

# 1) 迁移微调（冻结 backbone，只训新分类头）
torch.manual_seed(0)
net_ft = fine_tune_from(src_net, 4, freeze=True)
train_epochs(net_ft, train_tgt, epochs=3, lr=1e-3)
acc_ft = accuracy(net_ft, test_tgt)

# 2) 从零训练（对照组）
torch.manual_seed(0)
net_scratch = small_cnn(4)
train_epochs(net_scratch, train_tgt, epochs=3, lr=1e-3)
acc_scratch = accuracy(net_scratch, test_tgt)

print(f"目标任务（4类，仅 3 轮）：迁移微调 {acc_ft:.4f}  vs  从零训练 {acc_scratch:.4f}")
print("（迁移微调收敛更快——因为特征层已经学会『看图像』了）")
"""))

cells.append(md("""## 真实微调的标准代码（torchvision 预训练模型）

工程里微调用的是 ImageNet 预训练模型（如下）。CPU 上跑 224×224 的 ResNet 较慢，这里给出标准写法：

```python
import torchvision
net = torchvision.models.resnet18(weights=torchvision.models.ResNet18_Weights.IMAGENET1K_V1)
net.fc = nn.Linear(net.fc.in_features, 你的类别数)   # 只改最后一层
# 冻结 backbone，只训新 fc：
for p in net.parameters(): p.requires_grad = False
for p in net.fc.parameters(): p.requires_grad = True
```

## 小结

| 概念 | 一句话直觉 |
| --- | --- |
| 图像增广 | 随机翻转/裁剪/颜色抖动，把数据「变多」，抑制过拟合 |
| 微调 | 复用预训练特征，只改最后一层，小数据也能训好 |
| 冻结 backbone | 只训新分类头，更省算力、更不易过拟合 |

> 🔑 **记忆**：**增广当正则化用，微调当「站在巨人肩膀上」用**。数据少 → 增广 + 微调，是小数据集 CV 的黄金组合。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\图像增广与微调.ipynb", cells)
print("图像增广与微调 ✔")

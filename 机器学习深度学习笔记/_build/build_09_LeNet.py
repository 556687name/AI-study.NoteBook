# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# LeNet · 第一个卷积神经网络（PyTorch）

> 📌 **出处**：李沐《动手学深度学习 V2》第 6 章「卷积神经网络（LeNet）」
> 🎯 **目标**：搭出历史上第一个成功的 CNN——**LeNet**（1998，Yann LeCun 用于识别手写数字），体会「**卷积 → 池化 → 全连接**」这个沿用至今的经典范式。

## LeNet 的结构

| 层 | 类型 | 输出尺寸（28×28 输入） |
| --- | --- | --- |
| 1 | Conv(1→6, 5×5, padding=2) + Sigmoid | 28×28×6 |
| 2 | AvgPool(2×2) | 14×14×6 |
| 3 | Conv(6→16, 5×5) + Sigmoid | 10×10×16 |
| 4 | AvgPool(2×2) | 5×5×16 |
| 5 | Flatten + 三个全连接层 | 400 → 120 → 84 → 10 |

> 💡 和现代 CNN 相比，LeNet 用 **Sigmoid** 激活、**平均池化**；现代网络改用 **ReLU** + **最大池化**，效果更好。但整体「卷积提特征、池化降维、全连接分类」的骨架没变。
"""))

cells.append(code(ENV))

cells.append(md("""## 1. 用 nn.Sequential 搭 LeNet

注意尺寸链：`padding=2` 让第一个卷积保持 28×28 不变；两层池化把 28 → 14 → 5，最后展平成 400 维进全连接。
"""))

cells.append(code("""# ---- 定义 LeNet ----
from torch import nn

net = nn.Sequential(
    nn.Conv2d(1, 6, kernel_size=5, padding=2), nn.Sigmoid(),   # 28×28 → 28×28×6
    nn.AvgPool2d(kernel_size=2, stride=2),                     # → 14×14×6
    nn.Conv2d(6, 16, kernel_size=5), nn.Sigmoid(),             # → 10×10×16
    nn.AvgPool2d(kernel_size=2, stride=2),                     # → 5×5×16
    nn.Flatten(),                                              # → 400
    nn.Linear(16 * 5 * 5, 120), nn.Sigmoid(),
    nn.Linear(120, 84), nn.Sigmoid(),
    nn.Linear(84, 10),
)

# 用一张假图走一遍前向，确认尺寸正确
X = torch.rand(1, 1, 28, 28)   # 1 张 28×28 灰度图
for layer in net:
    X = layer(X)
    print(f"{layer.__class__.__name__:12s} 输出形状：{tuple(X.shape)}")
"""))

cells.append(md("""## 2. 加载 Fashion-MNIST 并训练 LeNet

LeNet 有卷积层，能利用像素的空间结构，比上一节「把图展平成 784 维再全连接」的 MLP 更适合图像任务。
"""))

cells.append(code("""# ---- 加载数据 ----
from torchvision import datasets, transforms
from torch.utils import data

def load_data_fashion_mnist(batch_size, root='../data'):
    trans = transforms.ToTensor()
    tr = datasets.FashionMNIST(root=root, train=True,  transform=trans, download=True)
    te = datasets.FashionMNIST(root=root, train=False, transform=trans, download=True)
    return data.DataLoader(tr, batch_size, shuffle=True), data.DataLoader(te, batch_size, shuffle=False)

batch_size = 256
train_iter, test_iter = load_data_fashion_mnist(batch_size)

# 训练准备
def init_weights(m):
    if type(m) == nn.Linear or type(m) == nn.Conv2d:
        nn.init.xavier_uniform_(m.weight)
net.apply(init_weights)

loss = nn.CrossEntropyLoss()
trainer = torch.optim.SGD(net.parameters(), lr=0.9)   # LeNet 用较大学习率 0.9

num_epochs = 20
for epoch in range(num_epochs):
    net.train()
    for X, y in train_iter:
        l = loss(net(X), y)
        trainer.zero_grad(); l.backward(); trainer.step()
    net.eval()
    with torch.no_grad():
        命中, 总数 = 0.0, 0
        for X, y in train_iter:
            命中 += float((net(X).argmax(axis=1) == y).sum()); 总数 += y.numel()
        print(f"epoch {epoch+1:2d}: 训练准确率 {命中/总数:.4f}")
"""))

cells.append(md("""## 3. 测试集评估 + 预测可视化

LeNet（CNN）在 Fashion-MNIST 上测试准确率约 **85%**，和 MLP（约 85%）基本相当、略高一点点。这不是 bug——**Fashion-MNIST 太简单**，MLP 已经能靠全连接吃下大部分信息，CNN「利用空间结构」的优势要在**更复杂、空间结构更关键**的任务（如手写数字 MNIST、ImageNet）上才明显拉开差距。
"""))

cells.append(code("""# ---- 测试集准确率 + 可视化 ----
net.eval()
with torch.no_grad():
    命中, 总数 = 0.0, 0
    for X, y in test_iter:
        命中 += float((net(X).argmax(axis=1) == y).sum()); 总数 += y.numel()
print(f"LeNet 测试集准确率：{命中/总数:.4f}")

类别名 = ['T恤', '裤子', '套头衫', '连衣裙', '外套', '凉鞋', '衬衫', '运动鞋', '包', '短靴']
X, y = next(iter(test_iter))
with torch.no_grad():
    预测 = net(X).argmax(axis=1)

fig, axes = plt.subplots(2, 5, figsize=(11, 5))
for i, ax in enumerate(axes.flat):
    ax.imshow(X[i].squeeze().numpy(), cmap='gray')
    color = 绿 if 预测[i] == y[i] else 红
    ax.set_title(f"{类别名[y[i].item()]}→{类别名[预测[i].item()]}", color=color, fontsize=9)
    ax.axis('off')
fig.suptitle('LeNet 测试集预测（绿=对，红=错）', fontsize=13)
plt.tight_layout(); plt.show()
"""))

cells.append(md("""## 小结

| 概念 | 一句话直觉 |
| --- | --- |
| LeNet | 第一个成功的 CNN：卷积→池化→全连接 |
| 卷积 | 提取局部空间特征 |
| 池化 | 降维 + 增强平移不变性 |
| 全连接 | 把卷积提的特征映射到类别分数 |

> 📌 **下一步**：现代 CNN 在 LeNet 基础上加了**更深的卷积、ReLU、最大池化、批量规范化、残差连接**等技巧（见 `实战代码_李沐/AlexNet.ipynb` 等）。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\LeNet.ipynb", cells)

# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# Kaggle 图像分类 · 完整流水线 + 提交文件（PyTorch）

> 📌 **出处**：李沐《动手学深度学习 V2》第 13 章「Kaggle 实战：图像分类」
> 🎯 **目标**：走一遍 Kaggle 竞赛的完整流程——**数据增强 → 训练 CNN → 对测试集预测 → 生成提交 CSV**。

## Kaggle 竞赛是什么流程

拿到「训练集（有标签）+ 测试集（无标签）」，训练模型后对测试集预测，提交一个 `id,label` 的 CSV 让平台评分。我们用 Fashion-MNIST 模拟这个过程。
"""))

cells.append(code(ENV))

cells.append(code("""# ---- 数据：训练集加增广，测试集只 ToTensor ----
from torch import nn
from torchvision import datasets, transforms
from torch.utils import data

class_names = ['T恤', '裤子', '套头衫', '连衣裙', '外套', '凉鞋', '衬衫', '运动鞋', '包', '短靴']

train_aug = transforms.Compose([
    transforms.RandomHorizontalFlip(),                 # 增广：随机翻转
    transforms.RandomCrop(28, padding=4),              # 增广：随机裁剪
    transforms.ToTensor(),
])
test_trans = transforms.ToTensor()

batch_size = 256
train_iter = data.DataLoader(datasets.FashionMNIST(root='../data', train=True,  transform=train_aug, download=True), batch_size, shuffle=True)
test_iter  = data.DataLoader(datasets.FashionMNIST(root='../data', train=False, transform=test_trans, download=True), batch_size, shuffle=False)
print("训练样本：", len(train_iter.dataset), " 测试样本：", len(test_iter.dataset))
"""))

cells.append(md("""## 1. 定义 CNN 模型

一个三层卷积的小网络，适合 Fashion-MNIST。
"""))

cells.append(code("""# ---- 小 CNN ----
net = nn.Sequential(
    nn.Conv2d(1, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),   # 28->14
    nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),  # 14->7
    nn.Flatten(), nn.Linear(64 * 7 * 7, 128), nn.ReLU(), nn.Dropout(0.2),
    nn.Linear(128, 10))

loss_fn = nn.CrossEntropyLoss()
opt = torch.optim.Adam(net.parameters(), lr=1e-3)
print("参数量：", sum(p.numel() for p in net.parameters()))
"""))

cells.append(md("""## 2. 训练（带增广）

增广让每个 epoch 看到的数据都不一样，相当于「免费扩增」了数据。
"""))

cells.append(code("""# ---- 训练 ----
def accuracy(loader):
    net.eval()
    correct = sum((net(X).argmax(1) == y).sum().item() for X, y in loader)
    return correct / len(loader.dataset)

num_epochs = 8
for epoch in range(num_epochs):
    net.train()
    for X, y in train_iter:
        l = loss_fn(net(X), y); opt.zero_grad(); l.backward(); opt.step()
    print(f"epoch {epoch+1}: 测试准确率 {accuracy(test_iter):.4f}")
"""))

cells.append(md("""## 3. 对测试集预测，生成提交 CSV

Kaggle 提交格式：`image_id,label` 两列。
"""))

cells.append(code("""# ---- 预测并保存提交文件 ----
net.eval()
preds = []
with torch.no_grad():
    for X, _ in test_iter:
        preds.append(net(X).argmax(1))
all_preds = torch.cat(preds).numpy()

import csv
out_path = "../kaggle_submission.csv"
with open(out_path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["image_id", "label"])
    for i, p in enumerate(all_preds):
        w.writerow([i, int(p)])
print(f"已保存 {len(all_preds)} 条预测到 {out_path}")

# 展示前几条 + 可视化几个预测
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 6, figsize=(13, 2.5))
ds = datasets.FashionMNIST(root='../data', train=False, download=True)
for ax, i in zip(axes, range(6)):
    img, _ = ds[i]
    ax.imshow(img, cmap='gray'); ax.axis('off')
    ax.set_title(f"预测: {class_names[all_preds[i]]}", fontsize=9)
plt.suptitle("测试集前 6 张的预测结果")
plt.show()
"""))

cells.append(md("""## 小结

| 步骤 | 关键点 |
| --- | --- |
| 数据增强 | 训练集 RandomFlip/RandomCrop，测试集不增广 |
| 训练 CNN | 小卷积网络 + Adam |
| 预测测试集 | 逐批预测，拼接所有结果 |
| 提交 CSV | `image_id,label` 两列 |

> 🔑 **记忆**：Kaggle 图像分类流水线 = **增强数据 → 训练 → 预测 → CSV**。竞赛里真正的提分靠更深的骨干（ResNet）、更强的增广、集成和测试时增强（TTA）。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\Kaggle-图像分类.ipynb", cells)
print("Kaggle-图像分类 ✔")

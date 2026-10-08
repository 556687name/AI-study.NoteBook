# -*- coding: utf-8 -*-
CELLS = [
    ("markdown", r'''# 第十五章 数据加载与数据增强

> 📌 **出处**：⭐ **40 天计划补充**（计划 Day15「PyTorch 基础：DataLoader」、Day17「数据增强」）。上一章学了 Tensor 和 autograd，这一章解决「**怎么高效地把数据喂给模型**」和「**数据不够怎么造**」两个问题。
> 🎓 **推荐配套**：李沐《动手学深度学习》PyTorch 版第 3~4 章。

---

## 15.1 为什么需要 Dataset 和 DataLoader？

训练时数据可能有几十万条，不能一次全塞进内存，也不能一条条手动喂。PyTorch 用两个组件分工解决：

- **`Dataset`（数据集）**：定义「**数据从哪来、怎么读取一条**」——它只负责「第 i 条数据是什么」，不管批量；
- **`DataLoader`（数据加载器）**：把 Dataset 包装起来，负责「**自动分批（batch）、打乱（shuffle）、并行加载（num_workers）**」，把一批批数据送到训练循环。

这个「Dataset 管单条、DataLoader 管批量」的分工，是 PyTorch 最优雅的设计之一。

> 💡 一句话：**Dataset 回答「单条数据怎么取」，DataLoader 回答「怎么打包成一批批高效喂给模型」。**
'''),
    ("code", r'''# ---- 自定义 Dataset：把「数据 + 标签」组织起来 ----
from torch.utils.data import Dataset, DataLoader

# 自定义一个数据集：继承 Dataset，实现 __len__ 和 __getitem__ 两个方法
class 线性数据集(Dataset):
    """生成 y = 3x + 2 + 噪声 的 100 条数据。"""
    def __init__(self, n=100):
        torch.manual_seed(42)
        self.x = torch.rand(n, 1) * 10            # 输入 x ∈ [0, 10)
        self.y = 3.0 * self.x + 2.0 + torch.randn(n, 1) * 0.5   # 真实关系 + 噪声

    def __len__(self):
        return len(self.x)                        # 数据集有多大

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]           # 返回第 idx 条 (输入, 标签)

ds = 线性数据集(100)
print("数据集大小：", len(ds))
print("第 0 条数据：(x, y) =", ds[0][0].item(), ",", ds[0][1].item(), "\n")

# DataLoader 打包：每批 16 条、打乱、用 0 个额外进程
loader = DataLoader(ds, batch_size=16, shuffle=True, num_workers=0)

print("DataLoader 遍历一个 batch：")
for 批x, 批y in loader:
    print("  x 形状：", 批x.shape, "  y 形状：", 批y.shape, "（16 条 × 1 维）")
    break
'''),
    ("markdown", r'''## 15.2 DataLoader 的三个关键参数

- **`batch_size`**：每批多少条。太小训练慢、太大会爆内存，常见 32/64/128（呼应第六章）；
- **`shuffle=True`**：每个 epoch 随机打乱顺序。**训练时一定要 True**（防止模型记住数据顺序），验证/测试时 False；
- **`num_workers`**：用几个子进程并行读数据。CPU 加载慢时可以调大（如 4），但 Windows 上常设 0 避免多进程问题。

还有一个容易忽略的点：**`drop_last=True`** 会在「最后一批不足 batch_size」时丢弃它，避免最后一批形状不一致导致某些操作报错。

> 💡 一个 epoch = 把整个数据集完整过一遍（`shuffle=True` 时每轮顺序都不同）。训练通常要跑很多个 epoch。
'''),
    ("markdown", r'''## 15.3 数据增强：数据不够，就「无中生有」

**数据增强（Data Augmentation）** 是抑制过拟合（第八章）的一大利器，尤其对**图像**。核心思想：**对已有训练样本做「合理的小变形」，制造新的训练样本**。

为什么有效？第八章说过拟合的根源是「模型记住了训练数据」。数据增强让模型每次看到「同一张图的不同样子」，它就没法去死记原图，被迫学到**真正的、变换不变的本质特征**——猫翻转了还是猫，模型必须认出来。

常见图像增强（`torchvision.transforms` 里都有）：

| 增强 | 效果 | 说明 |
| --- | --- | --- |
| `RandomHorizontalFlip` | 随机水平翻转 | 猫脸朝左朝右都是猫 |
| `RandomRotation` | 随机旋转 | 旋转 ±N 度 |
| `RandomCrop` | 随机裁剪 | 裁出一块再缩放 |
| `ColorJitter` | 随机调亮度/对比度/饱和度 | 模拟不同光照 |
| `RandomResizedCrop` | 随机缩放再裁剪 | 模拟不同距离/构图 |
| `Normalize` | 标准化 | 让像素均值 0、方差 1（配合缩放） |

> 💡 关键：增强**只在训练时用**，测试时只用「缩放 + 归一化」这些确定性的变换（不做随机变形）。
'''),
    ("code", r'''# ---- 数据增强演示：同一张图的不同"增强"版本 ----
from PIL import Image
from torchvision import transforms

# 造一张简单的"测试图"：左上画一个圆、右下画一个方块
img_arr = np.zeros((80, 80, 3), dtype=np.uint8)
img_arr[5:35, 5:35] = [255, 100, 100]        # 左上：红色方块
yy, xx = np.ogrid[:30, :30]
circle = (xx - 15) ** 2 + (yy - 15) ** 2 <= 14 ** 2
img_arr[45:75, 45:75][circle] = [100, 150, 255]   # 右下：蓝色圆
原图 = Image.fromarray(img_arr)

# 定义一组增强变换（每个都是"随机"的）
增强组 = transforms.Compose([
    transforms.RandomHorizontalFlip(p=1.0),      # 一定水平翻转
    transforms.RandomRotation(degrees=30),       # 随机旋转 ±30°
    transforms.ColorJitter(brightness=0.5, contrast=0.5),  # 随机亮度/对比度
    transforms.RandomResizedCrop(size=80, scale=(0.7, 1.0)),  # 随机缩放裁剪
])

fig, axes = plt.subplots(1, 4, figsize=(13, 4))
axes[0].imshow(原图); axes[0].set_title('原图'); axes[0].axis('off')
for ax in axes[1:]:
    增强图 = 增强组(原图)          # 每次调用产生不同的随机结果
    ax.imshow(增强图); ax.set_title('数据增强后'); ax.axis('off')
plt.suptitle('数据增强：同一张图，随机生成多种"合法变形"', fontsize=13)
plt.tight_layout()
plt.show()

# 观察：翻转、旋转、变色、缩放裁剪，让模型学到"变换不变"的本质特征。
'''),
    ("markdown", r'''## 15.4 图像数据的标准流水线：transform 组合

实际处理图像时，会把「增强 + 预处理」组合成一个 `transforms.Compose` 流水线，训练集和测试集用**不同的** transform：

```python
# 训练集：随机增强 + 转张量 + 归一化
train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ToTensor(),               # PIL图/H×W×C → 张量 C×H×W，且缩到 [0,1]
    transforms.Normalize(mean=[0.5,0.5,0.5], std=[0.5,0.5,0.5]),  # 标准化到 [-1,1]
])

# 测试集：只做确定的变换
test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5,0.5,0.5], std=[0.5,0.5,0.5]),
])
```

两个要点：

- **`ToTensor()`**：把 `PIL` 图像或 numpy 数组转成 PyTorch 张量，并**自动把像素从 [0,255] 缩到 [0,1]**、把形状从 `H×W×C` 变成 `C×H×W`（PyTorch 卷积要求通道在前）；
- **`Normalize(mean, std)`**：对每个通道做 $(x - \text{mean})/\text{std}$，把数据缩到利于训练的范围（呼应第七章的 Z-Score 标准化）。

> 💡 这些就是标准套路，训练图像模型时基本照搬即可。
'''),
    ("markdown", r'''## 15.5 本章小结

| 概念 | 一句话直觉 |
| --- | --- |
| Dataset | 定义「第 i 条数据怎么取」，实现 `__len__`/`__getitem__` |
| DataLoader | 自动分批、打乱、并行加载 |
| batch_size / shuffle | 每批条数 / 训练时是否打乱 |
| 数据增强 | 对训练样本做随机变形，制造新样本、抑制过拟合 |
| ToTensor / Normalize | 转张量并缩到 [0,1] / 标准化到均值 0 方差 1 |

🔑 **记忆**：Dataset 管单条、DataLoader 管批量；训练集增强（随机变形）、测试集只用确定性预处理；`ToTensor` 自动缩像素并转成 `C×H×W`。

> 📌 **下一步**：第十六章讲**标准训练循环与模型搭建**——用 `nn.Module` 定义网络、`nn.Linear`/`nn.ReLU` 搭层，写出工业级训练循环（含优化器、checkpoint）。
'''),
]

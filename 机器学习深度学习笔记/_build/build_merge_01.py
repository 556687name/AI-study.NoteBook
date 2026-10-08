# -*- coding: utf-8 -*-
"""批次1融合：把李沐 d2l 的「线性回归/softmax/预备知识」知识点并入现有笔记对应章节。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, load_nb, save_json

NB = r"D:\NoteBook\机器学习深度学习笔记\机器学习深度学习完整笔记.ipynb"
nb = load_nb(NB)
cells = nb["cells"]

# ---------- 1. 环境准备单元格：加入 torch ----------
for c in cells:
    src = "".join(c["source"])
    if "环境准备" in src and "import numpy" in src:
        c["source"] = src.replace(
            "import pandas as pd\n",
            "import pandas as pd\nimport torch\n"
        ).replace(
            "np.random.seed(0)   # 固定随机种子，保证结果可复现\n",
            "np.random.seed(0)   # 固定随机种子，保证结果可复现\ntorch.manual_seed(0)   # 固定 PyTorch 随机种子\n"
        ).replace(
            "print(\"✓ 环境准备完成：numpy\", np.__version__, \"| matplotlib\", plt.matplotlib.__version__)",
            "print(\"✓ 环境准备完成：numpy\", np.__version__, \"| torch\", torch.__version__)"
        ).splitlines(keepends=True)
        print("已更新环境准备单元格：加入 torch")
        break

# ---------- 2. 各章节要插入的新小节（markdown 知识点） ----------

ch4_new = [
md("""## 4.6 【李沐 d2l】线性回归的从零实现：模型→损失→优化三步曲

> 📌 **出处**：李沐《动手学深度学习 V2》第 3 章「线性回归的从零开始实现」
> 📎 **完整可运行代码**：`实战代码_李沐/线性回归-从零实现.ipynb`

李宏毅老师的「训练三步曲」在李沐 d2l 里被落到 **PyTorch 代码**。这一节把「从零实现」的三个零件讲透——**不用 `torch.nn`，只用 `torch.Tensor` 和自动求导**。

### 三步曲对照

| 三步曲 | 从零实现的代码 | 一句话 |
| --- | --- | --- |
| ① 模型 | `def linreg(X, w, b): return X @ w + b` | 参数 `w`、`b` 要标 `requires_grad=True` |
| ② 损失 | `def squared_loss(y_hat, y): return (y_hat - y)**2 / 2` | 平方损失，除以 2 让导数更简洁 |
| ③ 优化 | `def sgd(params, lr, batch_size)` | 小批量 SGD，更新后 `grad.zero_()` |

### 训练循环的四行核心

```python
for X, y in data_iter(batch_size, features, labels):
    l = loss(net(X, w, b), y)    # ① 前向：算一个小批量的损失
    l.sum().backward()           # ② 反向：自动求梯度
    sgd([w, b], lr, batch_size)  # ③ 更新参数
```

> 🔑 **记忆（从零实现的关键细节）**：
> - 参数要 `requires_grad=True` 才会被自动求导跟踪；
> - 损失要先 `.sum()`（或 `.mean()`）聚成一个**标量**再 `.backward()`；
> - 更新参数时用 `with torch.no_grad()` 包住，更新后必须 `grad.zero_()` **清零**，否则梯度会累加。
"""),

md("""## 4.7 【李沐 d2l】线性回归的简洁实现：框架 API 一行代替

> 📌 **出处**：李沐《动手学深度学习 V2》第 3 章「线性回归的简洁实现」
> 📎 **完整可运行代码**：`实战代码_李沐/线性回归-简洁实现.ipynb`

工业界直接用框架封装好的 API，代码量少一大半、还不易出错：

| 手写（从零） | 框架 API（简洁） |
| --- | --- |
| 手写 `data_iter` | `DataLoader` + `TensorDataset` |
| 手写 `linreg` | `nn.Sequential(nn.Linear(2, 1))` |
| 手写 `squared_loss` | `nn.MSELoss` |
| 手写 `sgd` | `optim.SGD(net.parameters(), lr=...)` |

```python
net = nn.Sequential(nn.Linear(2, 1))               # 模型：2 输入 → 1 输出
loss = nn.MSELoss()                                 # 损失：均方误差
trainer = torch.optim.SGD(net.parameters(), lr=0.03) # 优化器

for X, y in data_iter:
    l = loss(net(X), y)   # ① 前向 + 损失
    trainer.zero_grad()   # ② 清零梯度（= 从零实现的 grad.zero_()）
    l.backward()          # ③ 反向求梯度
    trainer.step()        # ④ 更新参数
```

> 🔑 **记忆**：简洁实现的训练循环骨架是**四步**——前向算 loss → `zero_grad()` → `backward()` → `step()`。这套骨架后面所有神经网络（CNN/RNN/Transformer）都通用，要背下来。
"""),
]

ch9_new = [
md("""## 9.7 【李沐 d2l】softmax 回归的从零实现：多分类的标准套路

> 📌 **出处**：李沐《动手学深度学习 V2》第 3 章「softmax 回归的从零开始实现」
> 📎 **完整可运行代码**：`实战代码_李沐/softmax回归-从零实现.ipynb`

9.5 节的 softmax 在这里被写成**完整的多分类模型**，数据集是 Fashion-MNIST（10 类服装图片，每张 28×28 展平成 784 维）。核心是把公式落到代码：

```python
def softmax(X):
    X_exp = torch.exp(X - X.max(dim=1, keepdim=True).values)  # 减最大值防溢出
    return X_exp / X_exp.sum(dim=1, keepdim=True)

def net(X):                          # 展平 784 维 → 线性变换 → softmax
    return softmax(X.reshape(-1, W.shape[0]) @ W + b)

def cross_entropy(y_hat, y):         # 交叉熵：只取真实类别对应的概率
    return -torch.log(y_hat[range(len(y_hat)), y])
```

> 🔑 **记忆**：
> - softmax 输出 **10 个和为 1 的概率**，预测类别 = `argmax` 取最大概率的下标；
> - 交叉熵损失**只对「真实类别」那个概率取 `-log`**，其余类别不参与；
> - 准确率 = 预测类别与真实标签一致的样本占比（`(y_hat.argmax(1) == y).sum() / len(y)`）。
"""),

md("""## 9.8 【李沐 d2l】softmax 回归的简洁实现 + CrossEntropyLoss 的坑

> 📌 **出处**：李沐《动手学深度学习 V2》第 3 章「softmax 回归的简洁实现」
> 📎 **完整可运行代码**：`实战代码_李沐/softmax回归-简洁实现.ipynb`

```python
net = nn.Sequential(nn.Flatten(), nn.Linear(784, 10))  # 模型：注意没有 softmax！
loss = nn.CrossEntropyLoss()                            # 损失：内部自带 softmax
trainer = torch.optim.SGD(net.parameters(), lr=0.1)
```

> 🔑 **关键坑（务必记住）**：`nn.CrossEntropyLoss` **内部自己会做 softmax**，所以模型的最后一层**不要再写 softmax**，直接输出 10 个**原始分数（logits）**。若多写一层 softmax，等于做了两次，结果会出错。
>
> 💡 另一处细节：`nn.Flatten()` 自动把 28×28 展平成 784 维，省去手写 `reshape`。softmax 回归的默认学习率是 `lr=0.1`（比线性回归的 0.03 大，因为这里损失是交叉熵、量级不同）。
"""),
]

ch14_new = [
md("""## 14.5 【李沐 d2l】预备知识 · 线性代数：张量的矩阵运算

> 📌 **出处**：李沐《动手学深度学习 V2》第 2 章「线性代数」

深度学习里张量（Tensor）的运算本质就是**线性代数**。几个高频操作：

```python
A = torch.arange(20, dtype=torch.float32).reshape(5, 4)  # 5×4 矩阵
A @ A.T           # 矩阵乘（@ 是矩阵乘法）
A.sum()           # 所有元素求和
A.sum(axis=0)     # 沿第 0 维压缩（结果行数变 1），常用来求每列统计量
A.mean(axis=1)    # 沿第 1 维求均值
torch.norm(A)     # L2 范数（所有元素平方和开根号）
```

> 🔑 **记忆**：
> - `@` 是**矩阵乘法**，`*` 是**逐元素相乘**（两者别搞混）；
> - `sum(axis=0)` 是「沿行方向压缩」，把行数压成 1，常用来求每列的均值/方差（例如后面 BatchNorm 会用到）；
> - 张量的「形状 shape」就是线性代数里的「维度」，`reshape` 只是换个视角、不改变数据。
"""),

md("""## 14.6 【李沐 d2l】预备知识 · 概率：从分布里抽样

> 📌 **出处**：李沐《动手学深度学习 V2》第 2 章「概率」

机器学习处理的是**不确定性**，概率是它的语言。用 torch 从不同分布抽样：

```python
torch.normal(mean=0, std=1, size=(3, 4))  # 正态分布抽样（最常用）
torch.rand(2, 3)                           # [0,1) 均匀分布
torch.randint(0, 10, (2, 3))              # 整数均匀分布
```

> 🔑 **记忆**：
> - 初始化网络权重常用 `torch.normal(0, 0.01, ...)`（小方差正态，避免一开始就饱和）；
> - 「训练 = 从数据分布里学规律」：模型要拟合的是数据的**概率分布**，而不只是背下每个样本；
> - 概率论三件套——**概率质量函数（离散）/ 概率密度函数（连续）/ 条件概率**，是后面所有损失函数（交叉熵等）的数学地基。
"""),

md("""## 14.7 【李沐 d2l】预备知识 · 数据预处理与查阅文档

> 📌 **出处**：李沐《动手学深度学习 V2》第 2 章「数据预处理 / 查阅文档」

- **数据预处理**：用 `pandas.read_csv()` 读表格数据、处理缺失值（删除 / 插值）——本笔记第 7 章已系统展开；
- **查阅文档**：遇到不认识的 API，用 `dir(对象)` 看有哪些方法、`help(函数)` 看说明。这是李沐反复强调的「会查文档」基本功。

> 💡 预备知识总结：**数据操作（Tensor）+ 线性代数 + 微积分（自动求导）+ 概率**，四块拼成深度学习的数学地基，后面所有章节都是在这四块上盖楼。
"""),
]

# ---------- 3. 按「小结」定位，从后往前插入，避免索引漂移 ----------
def find_summary(prefix):
    for i, c in enumerate(cells):
        if "".join(c["source"]).startswith(prefix):
            return i
    raise RuntimeError("未找到小结单元格: " + prefix)

# 需要把小结标题重命名（新内容加入后小结顺延到最后）
plan = [
    ("## 14.5 本章小结", "## 14.8 本章小结", ch14_new),
    ("## 9.7 本章小结",  "## 9.9 本章小结", ch9_new),
    ("## 4.6 本章小结",  "## 4.8 本章小结", ch4_new),
]

for old_prefix, new_prefix, new_cells in plan:
    idx = find_summary(old_prefix)
    # 重命名小结标题
    src = "".join(cells[idx]["source"])
    cells[idx]["source"] = src.replace(old_prefix, new_prefix, 1).splitlines(keepends=True)
    # 在小结之前插入新小节
    cells[idx:idx] = list(new_cells)
    print(f"在 {new_prefix} 前插入 {len(new_cells)} 个小节")

save_json(nb, NB)
print("融合完成 ✔")

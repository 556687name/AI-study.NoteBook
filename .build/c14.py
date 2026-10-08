# -*- coding: utf-8 -*-
CELLS = [
    ("markdown", r'''# 第十四章 PyTorch 基础：Tensor 与 Autograd

> 📌 **出处**：⭐ **40 天计划补充**（计划 Day15「PyTorch 基础」）。课程主线到第十三章结束，从这一章起进入 **PyTorch 实战**——把前面学到的「张量、自动求导、反向传播」用工业界最主流的框架真正落地。
> 🎓 **推荐配套**：李沐《动手学深度学习》PyTorch 版（B 站 BV1EY6FBwE8P）第 2~4 章。

---

## 14.1 为什么需要 PyTorch？

前面几章我们都是用 numpy 手写梯度、手写反向传播。这在「两层网络、4 个样本」时还行，但一到**几百层的网络、几百万参数**，手写就完全不可行了。

**PyTorch** 是 Facebook（现 Meta）开源的深度学习框架，它帮我们解决两件最麻烦的事：

1. **自动求导（autograd）**：只要用 PyTorch 定义好「前向计算」，它会**自动算出所有参数的梯度**（第十一章手写的反向传播，它内部全自动做掉了）；
2. **GPU 加速**：张量（Tensor）可以在 GPU 上做海量并行运算，训练大模型快成百上千倍。

> 💡 一句话：**numpy 是「科学计算」，PyTorch 是「能自动求导、能上 GPU 的科学计算」。** 它们的 API 非常像，学起来会很顺。
'''),
    ("code", r'''# ---- PyTorch 环境准备 ----
import torch
import numpy as np

print("PyTorch 版本：", torch.__version__)
# 检测是否有 GPU（没有就退回 CPU）
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print("使用的设备：", device, "（GPU 可用：", torch.cuda.is_available(), "）")
# 注：本机是 CPU 版 PyTorch，所有代码仍可正常运行，只是没有 GPU 加速。
'''),
    ("markdown", r'''## 14.2 Tensor（张量）：PyTorch 的「numpy 数组」

**Tensor（张量）** 是 PyTorch 的核心数据结构，可以理解成「能上 GPU、能自动求导的 numpy 数组」。

- **标量** = 0 维张量；**向量** = 1 维张量；**矩阵** = 2 维张量；更高维的统称张量；
- 图像是 `(通道, 高, 宽)` 的 3 维张量，一批图像是 `(批量, 通道, 高, 宽)` 的 4 维张量。

创建张量的常用方式（和 numpy 一一对应）：

| numpy | PyTorch | 说明 |
| --- | --- | --- |
| `np.array(...)` | `torch.tensor(...)` | 从列表创建 |
| `np.zeros / ones` | `torch.zeros / ones` | 全 0 / 全 1 |
| `np.arange(n)` | `torch.arange(n)` | 等差序列 |
| `np.random.rand` | `torch.rand` | [0,1) 均匀随机 |
| `np.random.randn` | `torch.randn` | 标准正态随机 |
'''),
    ("code", r'''# ---- Tensor 基本操作：创建、属性、索引、运算 ----
# ① 创建张量
a = torch.tensor([[1.0, 2.0, 3.0],
                  [4.0, 5.0, 6.0]])
print("张量 a：\n", a)
print("形状 a.shape：", a.shape, "   维度 a.dim()：", a.dim(), "   元素个数 a.numel()：", a.numel())
print("数据类型 a.dtype：", a.dtype, "   所在设备 a.device：", a.device, "\n")

# ② 索引与切片（和 numpy 一样）
print("a[0, 1] =", a[0, 1].item(), "   # .item() 把标量张量取成 Python 数字")
print("a[:, 1] =", a[:, 1], "   # 取第 2 列\n")

# ③ 运算（和 numpy 一样）
b = torch.ones(2, 3)
print("a + b = \n", a + b)
print("a * b = \n", a * b, "   # 逐元素乘（不是矩阵乘！）")
print("a @ b.T = \n", a @ b.T, "   # @ 才是矩阵乘法\n")

# ④ 常用函数
print("a.sum() =", a.sum().item(), "   a.mean() =", a.mean().item(), "   a.max() =", a.max().item())
'''),
    ("code", r'''# ---- Tensor 与 numpy 互转、以及搬上 GPU ----
# ① Tensor → numpy（共享内存，改一个另一个也变，注意！）
t = torch.tensor([1.0, 2.0, 3.0])
n = t.numpy()
print("Tensor → numpy：", n, type(n))

# ② numpy → Tensor
n2 = np.array([4.0, 5.0, 6.0])
t2 = torch.from_numpy(n2)
print("numpy → Tensor：", t2, type(t2), "\n")

# ③ 搬上 GPU（本机无 GPU，代码仍写出正确写法，运行会自动退回 CPU）
x = torch.randn(3, 3)
x_gpu = x.to(device)     # .to(device) 把张量搬到指定设备
print("搬到设备后：", x_gpu.device, "（本机为 CPU）")

# ④ 修改形状：reshape / view
y = torch.arange(12)
print("reshape 成 3×4：\n", y.reshape(3, 4))
'''),
    ("markdown", r'''## 14.3 Autograd（自动求导）：PyTorch 的「反向传播引擎」

这是 PyTorch 最核心、也最该**吃透**的功能。回忆第十一章：我们手写了「前向传播 + 反向传播」来算梯度。**PyTorch 的 autograd 会自动完成反向传播**，只要三步：

1. **标记要跟踪的参数**：创建张量时设 `requires_grad=True`；
2. **前向计算**：正常写运算，PyTorch 会在后台**悄悄记录一张「计算图」**；
3. **`.backward()` 求梯度**：调用一次，PyTorch 自动沿计算图反向算出所有参数的梯度，存到各张量的 `.grad` 属性里。

### 原理：一张「计算图」

PyTorch 在你做每个运算时，都把「输入是谁、做了什么运算」记下来，形成一张**有向无环图（DAG）**。`.backward()` 就是沿这张图**从损失出发、用链式法则一路反推**——这正是第十一章「反向传播」的自动化版本。

> 🔑 **记忆**：`requires_grad=True` 标记参数 → 前向计算（自动建图）→ `loss.backward()` 自动求梯度 → 梯度在 `x.grad` 里。
'''),
    ("code", r'''# ---- Autograd 演示：自动求导，对比手算 ----
# 用 y = x² 在 x=3 处的导数，验证 autograd 算得对不对。
x = torch.tensor(3.0, requires_grad=True)   # ① 标记要跟踪梯度

y = x ** 2                                   # ② 前向计算（PyTorch 悄悄建图）
y.backward()                                 # ③ 反向传播，自动求梯度

print(f"y = x²，在 x=3 处的导数 dy/dx = 2x = 6")
print(f"autograd 算得 x.grad = {x.grad.item()}  ✅ 正确")

# 再来一个多步的：y = (x² + 3x)²，验证链式法则
x2 = torch.tensor(2.0, requires_grad=True)
z = x2 ** 2 + 3 * x2
y2 = z ** 2
y2.backward()
# 手算：dy/dx = 2(x²+3x)·(2x+3)，x=2 时 = 2·(4+6)·(4+3) = 140
print(f"\ny = (x²+3x)²，x=2 时手算 dy/dx = 2·10·7 = 140")
print(f"autograd 算得 x2.grad = {x2.grad.item()}  ✅ 自动完成了链式法则")
'''),
    ("code", r'''# ---- Autograd 与第十一章手写反向传播的对应 ----
# 把第十一章"两层网络反向传播"用 autograd 重写，体会它省了多少事。
def sigmoid_t(z):
    return 1 / (1 + torch.exp(-z))

# 同样的单个样本：x=0.6, y=1.0
x = torch.tensor(0.6)
y = torch.tensor(1.0)

# 参数：requires_grad=True 让 PyTorch 跟踪它们
w1 = torch.tensor(0.5, requires_grad=True)
b1 = torch.tensor(-0.3, requires_grad=True)
w2 = torch.tensor(0.2, requires_grad=True)
b2 = torch.tensor(0.1, requires_grad=True)

# 前向传播（和第十一章一模一样，但不用手写反向）
z1 = w1 * x + b1
a1 = sigmoid_t(z1)
y_hat = w2 * a1 + b2
L = 0.5 * (y_hat - y) ** 2

# 一句话自动求所有梯度！
L.backward()

print("第十一章手写反向传播算出的梯度 vs autograd 自动算的梯度：")
print(f"  ∂L/∂w1：手写 -0.0240 vs autograd {w1.grad.item():.4f}")
print(f"  ∂L/∂w2：手写 -0.4000 vs autograd {w2.grad.item():.4f}")
print(f"  ∂L/∂b1：手写 -0.0400 vs autograd {b1.grad.item():.4f}")
print(f"  ∂L/∂b2：手写 -0.8000 vs autograd {b2.grad.item():.4f}")
print("两者一致 → autograd 就是自动化的反向传播 ✅")
'''),
    ("markdown", r'''## 14.4 Autograd 的三个关键细节

### ① 梯度会「累加」，要记得清零

默认情况下，每次 `.backward()` 得到的梯度会**累加**到 `.grad` 上（而不是覆盖）。所以每个训练步之前，要手动把梯度清零。两种写法：

- 优化器方式：`optimizer.zero_grad()`（第十六章会讲优化器）；
- 手动方式：`param.grad.zero_()` 或 `param.grad = None`。

### ② 不需要梯度的计算，要「关掉」它

预测、评估模型时，我们**只算前向、不算梯度**。若还开着梯度跟踪，会白耗内存和算力。两种关法：

- `torch.no_grad()` 上下文：`with torch.no_grad():` 块里的计算不建图；
- `x.detach()`：把张量从计算图里「摘」出来，得到不跟踪梯度的副本。

### ③ 计算图默认「用完即弃」

`.backward()` 之后，中间的计算图会被释放以省内存。所以**不能对同一个计算结果重复调用 `.backward()`**（除非设 `retain_graph=True`）。
'''),
    ("code", r'''# ---- Autograd 的三个细节演示 ----
# ① 梯度累加问题
x = torch.tensor(2.0, requires_grad=True)
for i in range(3):
    y = x ** 2
    y.backward()
    print(f"第 {i+1} 次 backward 后 x.grad = {x.grad.item()}（在累加！）")

print("\n正确做法：每次 backward 前清零")
x2 = torch.tensor(2.0, requires_grad=True)
for i in range(3):
    if x2.grad is not None:
        x2.grad.zero_()          # 清零
    y = x2 ** 2
    y.backward()
    print(f"  第 {i+1} 次：x2.grad = {x2.grad.item()}（恒为 4，不再累加）")

# ② 用 no_grad 关闭梯度跟踪（预测时用）
x3 = torch.tensor(3.0, requires_grad=True)
with torch.no_grad():
    y3 = x3 ** 2
print(f"\nno_grad 块里的计算结果 requires_grad = {y3.requires_grad}（False = 不跟踪）")
'''),
    ("markdown", r'''## 14.5 本章小结

| 概念 | 一句话直觉 |
| --- | --- |
| Tensor | 能上 GPU、能自动求导的「numpy 数组」 |
| 创建/索引/运算 | 和 numpy 几乎一样（`@` 是矩阵乘） |
| requires_grad | 标记要跟踪梯度的参数 |
| 计算图 | PyTorch 前向时偷偷记录，反向时沿它求导 |
| backward | 一句话自动算出所有参数的梯度 |
| 梯度清零 | 梯度默认累加，每步要 `zero_grad()` |

🔑 **记忆**：三步曲 = `requires_grad=True` → 前向算 loss → `loss.backward()`；梯度在 `.grad` 里，训练每步前要清零；预测用 `torch.no_grad()`。

> 📌 **下一步**：第十五章讲**数据加载与数据增强**——用 `Dataset` / `DataLoader` 高效喂数据，并学会扩充数据、抑制过拟合。
'''),
]

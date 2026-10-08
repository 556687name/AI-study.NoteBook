# -*- coding: utf-8 -*-
CELLS = [
    ("markdown", r'''# 第十六章 模型搭建与标准训练循环

> 📌 **出处**：⭐ **40 天计划补充**（计划 Day15「PyTorch 基础：nn.Module、训练循环」、Day17「checkpoint」）。前两章学了 Tensor、autograd、DataLoader，这一章把它们组装成**一个真正能跑的完整模型**，写出工业级标准的训练循环。
> 🎓 **推荐配套**：李沐《动手学深度学习》PyTorch 版第 4~6 章。

---

## 16.1 用 nn.Module 定义模型

前面（第十一、十四章）我们都是「手动管理参数 $w, b$」。真实项目里，用 PyTorch 的 **`nn.Module`** 来组织模型，好处是：**自动管理参数、能打印结构、能一键迁移到 GPU、能保存加载**。

定义模型的两个要点：

1. **继承 `nn.Module`**；
2. 在 `__init__` 里定义层，在 `forward` 里写「前向计算」（输入怎么一层层变成输出）。

`forward` 定义好之后，PyTorch 会自动为它建计算图、支持反向传播。
'''),
    ("code", r'''# ---- nn.Module 定义一个多层感知机 MLP ----
import torch.nn as nn

class 简单MLP(nn.Module):
    """三层 MLP：输入 → 隐藏(ReLU) → 隐藏(ReLU) → 输出。"""
    def __init__(self, 输入维度, 隐藏维度, 输出维度):
        super().__init__()
        self.层1 = nn.Linear(输入维度, 隐藏维度)   # 线性层：z = Wx + b
        self.层2 = nn.Linear(隐藏维度, 隐藏维度)
        self.层3 = nn.Linear(隐藏维度, 输出维度)
        self.relu = nn.ReLU()                      # 激活函数（可复用）

    def forward(self, x):
        x = self.relu(self.层1(x))                 # 线性 → 激活
        x = self.relu(self.层2(x))
        x = self.层3(x)                            # 输出层不做激活（回归）
        return x

model = 简单MLP(输入维度=2, 隐藏维度=8, 输出维度=1)
print(model)          # 打印模型结构
print("\n模型参数量：", sum(p.numel() for p in model.parameters()))

# 试跑一次前向
x = torch.randn(4, 2)      # 4 个样本、2 个特征
y = model(x)
print("输入形状", x.shape, "→ 输出形状", y.shape)
'''),
    ("markdown", r'''## 16.2 常用层：nn.Linear、激活函数、nn.Sequential

| 层 | 作用 | 说明 |
| --- | --- | --- |
| `nn.Linear(in, out)` | 全连接层 $y = Wx + b$ | 权重 $W$ 和偏置 $b$ 自动注册为参数 |
| `nn.ReLU()` | ReLU 激活 | `max(0, x)` |
| `nn.Sigmoid()` | sigmoid | 压到 (0,1) |
| `nn.Dropout(p)` | Dropout（第八章） | 训练时随机丢弃，测试自动关闭 |
| `nn.Conv2d(...)` | 卷积层（第十二章） | 图像特征提取 |
| `nn.MaxPool2d(...)` | 最大池化（第十二章） | 下采样 |

如果网络是**顺序的一串层**，可以用 **`nn.Sequential`** 写得更简洁：

```python
model = nn.Sequential(
    nn.Linear(2, 8), nn.ReLU(),
    nn.Linear(8, 8), nn.ReLU(),
    nn.Linear(8, 1),
)
```

> 💡 `nn.Module` 适合复杂结构（有分支、跳跃连接），`nn.Sequential` 适合简单顺序结构。两者都能打印、训练、保存。
'''),
    ("markdown", r'''## 16.3 损失函数与优化器：nn 和 optim 全家桶

PyTorch 把第十章「损失函数」和第六章「优化器」都封装好了：

**损失函数（`torch.nn`）**：

- `nn.MSELoss()`：均方误差，回归用；
- `nn.L1Loss()`：平均绝对误差 MAE，抗离群点；
- `nn.CrossEntropyLoss()`：交叉熵，分类用（**注意：它内部已包含 softmax**，所以模型最后一层不要再加 softmax）；
- `nn.BCEWithLogitsLoss()`：二分类交叉熵（内部含 sigmoid）。

**优化器（`torch.optim`）**：

- `optim.SGD(params, lr, momentum=0.9)`：小批量梯度下降，可加动量；
- `optim.Adam(params, lr=0.001)`：Adam（第六章），默认首选；
- 都支持 `weight_decay` 参数 = 第八章的 **L2 权重衰减**。

> 🔑 **记忆**：分类用 `CrossEntropyLoss`（自带 softmax），回归用 `MSELoss`；优化器默认 `Adam`；`weight_decay` = L2 正则。
'''),
    ("code", r'''# ---- 损失函数 + 优化器的使用 ----
import torch.optim as optim

# 造一个小例子：多分类（3 类）
logits = torch.randn(2, 3)               # 2 个样本，每个输出 3 个"分数"（未过 softmax）
target = torch.tensor([0, 2])            # 真实类别

ce = nn.CrossEntropyLoss()               # 交叉熵（内部自动 softmax）
loss = ce(logits, target)
print("交叉熵损失 =", loss.item(), "（CrossEntropyLoss 内部已含 softmax）")

# 回归例子：MSE
mse = nn.MSELoss()
pred = torch.tensor([1.0, 2.0, 3.0]); true = torch.tensor([1.5, 2.5, 2.5])
print("MSE 损失 =", mse(pred, true).item(), "\n")

# 优化器：把模型参数交给它
model2 = 简单MLP(2, 8, 1)
opt_sgd = optim.SGD(model2.parameters(), lr=0.01, momentum=0.9, weight_decay=1e-4)
opt_adam = optim.Adam(model2.parameters(), lr=0.001)
print("SGD 优化器（含动量 + L2 权重衰减）：", opt_sgd)
print("Adam 优化器：", opt_adam)
'''),
    ("markdown", r'''## 16.4 标准训练循环（五段式模板）

把前面所有零件串起来，就是一个**工业级标准训练循环**。它的骨架（🔑 要背下来）：

```python
for epoch in range(总轮数):
    # ---------- 训练阶段 ----------
    model.train()                              # 打开训练模式（Dropout 生效）
    for x, y in train_loader:
        x, y = x.to(device), y.to(device)      # 搬上 GPU
        optimizer.zero_grad()                  # ① 清零梯度
        pred = model(x)                        # ② 前向
        loss = criterion(pred, y)              # ③ 算损失
        loss.backward()                        # ④ 反向求梯度
        optimizer.step()                       # ⑤ 更新参数

    # ---------- 验证阶段 ----------
    model.eval()                               # 打开评估模式（Dropout 关闭）
    with torch.no_grad():                      # 不跟踪梯度，省内存
        for x, y in valid_loader:
            pred = model(x)
            # 累积验证损失 / 准确率
```

五个核心动作的顺序绝不能乱：**`zero_grad → forward → loss → backward → step`**。

- `model.train()` / `model.eval()` 切换模式，影响 Dropout、BatchNorm 等层的表现；
- `torch.no_grad()` 关掉验证时的梯度计算，提速省内存。

下面的代码用回归问题完整跑一遍，并加上**早停 + 保存最优 checkpoint**（第八章的早停、checkpoint 落到代码）。
'''),
    ("code", r'''# ---- 完整训练循环：回归 + 早停 + 保存最优模型 ----
from torch.utils.data import DataLoader, TensorDataset

# 造数据：y = 3x + 2 + 噪声（x ∈ [0,10]）
torch.manual_seed(0)
X = torch.rand(800, 1) * 10
y = 3.0 * X + 2.0 + torch.randn(800, 1) * 1.5

# 划分：训练 600 / 验证 200
X_train, X_valid = X[:600], X[600:]
y_train, y_valid = y[:600], y[600:]

# TensorDataset 直接把 (x, y) 包成 Dataset
train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=32, shuffle=True)
valid_loader = DataLoader(TensorDataset(X_valid, y_valid), batch_size=128, shuffle=False)

model = 简单MLP(1, 32, 1)                    # 1 输入 → 32 隐藏 → 1 输出
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

train_losses, valid_losses = [], []
最佳验证损失 = float('inf')
早停计数 = 0

for epoch in range(200):
    # ---- 训练 ----
    model.train()
    for xb, yb in train_loader:
        optimizer.zero_grad()                 # ① 清零
        pred = model(xb)                      # ② 前向
        loss = criterion(pred, yb)            # ③ 损失
        loss.backward()                       # ④ 反向
        optimizer.step()                      # ⑤ 更新

    # ---- 验证 ----
    model.eval()
    with torch.no_grad():
        总损失 = sum(criterion(model(xb), yb).item() for xb, yb in valid_loader)
        验证损失 = 总损失 / len(valid_loader)
    train_losses.append(loss.item())
    valid_losses.append(验证损失)

    # ---- 早停 + 保存最优 ----
    if 验证损失 < 最佳验证损失:
        最佳验证损失 = 验证损失
        torch.save(model.state_dict(), 'best_model.pt')   # 保存最优参数
        早停计数 = 0
    else:
        早停计数 += 1
        if 早停计数 >= 20:                                # 连续 20 轮没进步就停
            print(f"第 {epoch} 轮触发早停！")
            break

print(f"最佳验证损失 = {最佳验证损失:.4f}")

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(train_losses, color=蓝, lw=2, label='训练损失')
ax.plot(valid_losses, color=红, lw=2, label='验证损失')
ax.set_xlabel('epoch'); ax.set_ylabel('MSE 损失')
ax.set_title('训练/验证损失曲线')
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# 加载最优模型验证：在几个 x 上预测，对比真实关系 y=3x+2
model.load_state_dict(torch.load('best_model.pt'))
model.eval()
with torch.no_grad():
    测试x = torch.tensor([[0.0], [2.0], [5.0], [8.0], [10.0]])
    预测 = model(测试x)
    真实 = 3.0 * 测试x + 2.0
print("加载最优模型后，对比预测值和真实关系 y=3x+2：")
for xi, pi, yi in zip(测试x.ravel(), 预测.ravel(), 真实.ravel()):
    print(f"  x={xi:4.0f} → 预测 {pi:.2f}，真实 {yi:.2f}")
'''),
    ("markdown", r'''## 16.5 分类任务的标准训练循环（含准确率）

回归用 MSE，分类用**交叉熵 + 准确率（accuracy）**。分类循环和回归几乎一样，只是多一步「把预测分数转成类别，算准确率」。这里用 sklearn 造一个三分类数据完整演示。

> 💡 关于模型评估（准确率、混淆矩阵、精确率/召回率/F1），第十七章会专门展开——这一章先体会「分类训练循环」和「回归」的异同。
'''),
    ("code", r'''# ---- 分类训练循环：三分类 + 准确率 ----
from sklearn.datasets import make_classification

# 造三分类数据（4 个特征）
Xc, yc = make_classification(n_samples=600, n_features=4, n_informative=4,
                             n_redundant=0, n_classes=3, random_state=1)
Xc = torch.tensor(Xc, dtype=torch.float32)
yc = torch.tensor(yc, dtype=torch.long)

Xc_train, Xc_valid = Xc[:480], Xc[480:]
yc_train, yc_valid = yc[:480], yc[480:]

train_loader = DataLoader(TensorDataset(Xc_train, yc_train), batch_size=32, shuffle=True)
valid_loader = DataLoader(TensorDataset(Xc_valid, yc_valid), batch_size=128)

# 模型：4 输入 → 16 隐藏 → 3 输出（多分类）
model_c = nn.Sequential(
    nn.Linear(4, 16), nn.ReLU(),
    nn.Linear(16, 3),          # 输出 3 个分数（CrossEntropyLoss 会自己 softmax）
)
criterion_c = nn.CrossEntropyLoss()
optimizer_c = optim.Adam(model_c.parameters(), lr=0.01)

for epoch in range(100):
    model_c.train()
    for xb, yb in train_loader:
        optimizer_c.zero_grad()
        loss = criterion_c(model_c(xb), yb)
        loss.backward()
        optimizer_c.step()

# 验证：算准确率
model_c.eval()
with torch.no_grad():
    logits = model_c(Xc_valid)
    pred类 = logits.argmax(dim=1)                 # 取分数最高的类
    准确率 = (pred类 == yc_valid).float().mean()
print(f"验证集准确率 = {准确率.item():.4f}（{准确率.item()*100:.1f}%）")
'''),
    ("markdown", r'''## 16.6 保存与加载模型（checkpoint）

训练到一半的模型、最优模型，都要能存下来再恢复。两种保存方式：

- **只存参数**（推荐）：`torch.save(model.state_dict(), path)`，加载时先建好同结构模型再 `model.load_state_dict(torch.load(path))`；
- **存整个模型**：`torch.save(model, path)`，加载 `model = torch.load(path)`——简单但和代码结构绑定，换环境易出问题。

> 💡 更完整的 checkpoint 会把「模型参数 + 优化器状态 + 当前 epoch + 最佳指标」一起存，方便**断点续训**（训练大模型时尤其重要，第十九章还会遇到）。
'''),
    ("code", r'''# ---- 保存 / 加载 checkpoint（含优化器状态，可断点续训） ----
checkpoint = {
    'model_state': model_c.state_dict(),        # 模型参数
    'optimizer_state': optimizer_c.state_dict(),# 优化器状态（Adam 的动量等）
    'epoch': 100,
    'best_acc': 准确率.item(),
}
torch.save(checkpoint, 'checkpoint.pt')
print("已保存 checkpoint（含模型 + 优化器 + 指标）")

# 模拟"恢复训练"
model新 = nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 3))
optimizer新 = optim.Adam(model新.parameters(), lr=0.01)
ck = torch.load('checkpoint.pt')
model新.load_state_dict(ck['model_state'])
optimizer新.load_state_dict(ck['optimizer_state'])
print(f"已恢复：epoch={ck['epoch']}, 最优准确率={ck['best_acc']:.4f}，可继续训练")
'''),
    ("markdown", r'''## 16.7 本章小结

| 概念 | 一句话直觉 |
| --- | --- |
| nn.Module | 定义模型：`__init__` 建层、`forward` 写前向 |
| nn.Sequential | 顺序层的一行简写 |
| 损失函数 | MSELoss（回归）、CrossEntropyLoss（分类，自带 softmax） |
| 优化器 | SGD（可加动量）、Adam，`weight_decay` = L2 |
| 训练循环五步 | zero_grad → forward → loss → backward → step |
| checkpoint | 保存模型/优化器状态，支持断点续训 |

🔑 **记忆**：训练循环五步顺序绝不能乱；`CrossEntropyLoss` 已含 softmax（输出层不要再加）；`model.train()`/`model.eval()` 切换模式；早停看验证损失。

> 📌 **下一步**：第十七章讲**模型评估**——准确率之外，还要看懂混淆矩阵、精确率/召回率/F1，才能正确判断模型好坏（40 天计划重点）。
'''),
]

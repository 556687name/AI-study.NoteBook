# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# 线性回归 · 简洁实现（PyTorch）

> 📌 **出处**：李沐《动手学深度学习 V2》第 3 章「线性回归的简洁实现」
> 🎯 **目标**：用 PyTorch 的**高级 API** 重写上一节的从零实现，体会框架帮我们省掉了多少事。

## 简洁实现 vs 从零实现

上一节我们手写了模型、损失、优化、数据迭代。这一节用框架三件套**一行代替**：

| 手写（从零） | 框架 API（简洁） |
| --- | --- |
| 手写 `data_iter` | `DataLoader` + `TensorDataset` |
| 手写 `linreg` | `nn.Sequential(nn.Linear(2, 1))` |
| 手写 `squared_loss` | `nn.MSELoss` |
| 手写 `sgd` | `optim.SGD` |

> 🔑 **记忆**：工业界 99% 的模型都用「简洁实现」，因为代码更少、更不易出错；但**从零实现才是理解底层原理的关键**，两者都要会。
"""))

cells.append(code(ENV))

cells.append(md("""## 1. 造数据 + DataLoader：框架帮你切 batch

用和上一节相同的合成数据，但这次用 `TensorDataset` 把「特征 + 标签」打包，再用 `DataLoader` 自动完成「随机打乱 → 切 batch → 多线程加载」。
"""))

cells.append(code("""# ---- 合成数据 + DataLoader ----
import random
from torch.utils import data

def synthetic_data(w, b, num_examples):
    X = torch.normal(0, 1, (num_examples, len(w)))
    y = torch.matmul(X, w) + b + torch.normal(0, 0.01, (num_examples,))
    return X, y.reshape((-1, 1))

真实w = torch.tensor([2.0, -3.4]); 真实b = 4.2
features, labels = synthetic_data(真实w, 真实b, 1000)

def load_array(data_arrays, batch_size, is_train=True):
    '''把 (features, labels) 包成 DataLoader：训练集打乱，测试集不打乱。'''
    dataset = data.TensorDataset(*data_arrays)
    return data.DataLoader(dataset, batch_size, shuffle=is_train)

batch_size = 10
data_iter = load_array((features, labels), batch_size)
print("DataLoader 长度（batch 数）：", len(data_iter))
print("一个 batch：", next(iter(data_iter)))
"""))

cells.append(md("""## 2. 定义模型：nn.Sequential 一行搞定

`nn.Sequential` 是「一层接一层的容器」。这里只有一层全连接层 `nn.Linear(2, 1)`：输入 2 个特征，输出 1 个预测值。

> 💡 `nn.Linear(2, 1)` 内部就是 $y = Wx + b$，它已经替我们创建好了 `weight` 和 `bias` 两个参数，且默认 `requires_grad=True`。
"""))

cells.append(code("""# ---- 定义模型 + 初始化参数 ----
from torch import nn

net = nn.Sequential(nn.Linear(2, 1))   # 一层全连接：2 输入 → 1 输出

# 初始化：权重用均值为 0、标准差 0.01 的正态，偏置置 0
net[0].weight.data.normal_(0, 0.01)
net[0].bias.data.fill_(0)

print("模型结构：", net)
print("权重形状：", tuple(net[0].weight.shape), "偏置形状：", tuple(net[0].bias.shape))
"""))

cells.append(md("""## 3. 损失 + 优化器 + 训练循环

- 损失用 `nn.MSELoss`（默认 `reduction='mean'`，即均方误差）；
- 优化器用 `optim.SGD`，只要把「要更新的参数」`net.parameters()` 和「学习率」传进去；
- 训练循环的三步和从零实现一模一样：**清零梯度 → 反向 → 更新**。
"""))

cells.append(code("""# ---- 损失 + 优化器 + 训练 ----
loss = nn.MSELoss()               # 均方误差
trainer = torch.optim.SGD(net.parameters(), lr=0.03)   # 小批量 SGD

num_epochs = 3
for epoch in range(num_epochs):
    for X, y in data_iter:
        l = loss(net(X), y)        # ① 前向 + 算损失
        trainer.zero_grad()        # ② 清零梯度（等价于从零实现的 grad.zero_()）
        l.backward()               # ③ 反向求梯度
        trainer.step()             # ④ 更新参数
    l = loss(net(features), labels)
    print(f"epoch {epoch + 1}, loss {l.item():.6f}")

print()
print("学到的 w =", net[0].weight.data.flatten().numpy(), "（真实 [2.0, -3.4]）")
print("学到的 b =", net[0].bias.data.item(), "（真实 4.2）")
"""))

cells.append(md("""## 4. 观察结果：3 轮就收敛，和从零实现一样好

画出损失曲线和参数对比。可以看到：**简洁实现的代码量少了一大半，结果却和从零实现完全一致**——因为底层做的是同一件事。
"""))

cells.append(code("""# ---- 可视化 ----
net2 = nn.Sequential(nn.Linear(2, 1))
net2[0].weight.data.normal_(0, 0.01); net2[0].bias.data.fill_(0)
loss2 = nn.MSELoss(); trainer2 = torch.optim.SGD(net2.parameters(), lr=0.03)
hist = []
for epoch in range(5):
    for X, y in data_iter:
        l = loss2(net2(X), y)
        trainer2.zero_grad(); l.backward(); trainer2.step()
    hist.append(loss2(net2(features), labels).item())

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].plot(range(1, 6), hist, marker='o', color=橙)
axes[0].set_xlabel('epoch'); axes[0].set_ylabel('loss'); axes[0].set_title('简洁实现：损失一路下降')

学到的w = net2[0].weight.data.flatten().numpy(); 真实w_np = 真实w.numpy()
import numpy as np
x_pos = np.arange(len(真实w_np))
axes[1].bar(x_pos - 0.2, 真实w_np, width=0.4, label='真实 w', color=灰)
axes[1].bar(x_pos + 0.2, 学到的w, width=0.4, label='学到 w', color=蓝)
axes[1].set_xticks(x_pos); axes[1].set_ylabel('值'); axes[1].set_title('参数对比'); axes[1].legend()
plt.tight_layout(); plt.show()
print(f"真实 b = {真实b}，学到 b = {net2[0].bias.data.item():.3f}")
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\线性回归-简洁实现.ipynb", cells)

# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# 深度学习计算 · 层、块、参数管理与读写模型（PyTorch）

> 📌 **出处**：李沐《动手学深度学习 V2》第 5 章「层和块 / 参数管理 / 自定义层 / 读写文件 / GPU」
> 🎯 **目标**：学会像搭积木一样**自定义网络块**、管理模型**参数**、保存与加载**模型**——这是写任何复杂网络的基本功。

## 核心概念：块（Block）

在 PyTorch 里，**块 = `nn.Module`**。一个块可以是一个单层，也可以是「多个层嵌套」的复杂网络。块的关键是一个 `forward` 方法，定义数据怎么流过它。
"""))

cells.append(code(ENV))

cells.append(md("""## 1. 自定义块：组合几个层成一个「小网络」

继承 `nn.Module`，在 `__init__` 里建层，在 `forward` 里定义前向逻辑。下面这个 `MLP` 块组合了两个 `nn.Linear` 和一个 `nn.ReLU`。
"""))

cells.append(code("""# ---- 自定义块：MLP ----
from torch import nn

class MLP(nn.Module):
    '''一个自定义块：输入 20 维 → 隐藏 256 维（ReLU）→ 输出 10 维'''
    def __init__(self):
        super().__init__()
        self.hidden = nn.Linear(20, 256)   # 子块 1：全连接层
        self.out = nn.Linear(256, 10)      # 子块 2：全连接层

    def forward(self, X):
        return self.out(nn.functional.relu(self.hidden(X)))

net = MLP()
X = torch.rand(2, 20)
print("网络结构：", net)
print("输入 (2,20) → 输出形状：", tuple(net(X).shape), "（2 条样本，各 10 个分数）")
"""))

cells.append(md("""## 2. 自定义层：带参数的层 与 无参数的层

**带参数的层**需要同时继承 `nn.Module` 并实现 `__init__`（创建参数）和 `forward`；**无参数的层**则只需 `forward`。下面各写一个。
"""))

cells.append(code("""# ---- ① 无参数的层：把输入减去均值（中心化） ----
class CenteredLayer(nn.Module):
    def forward(self, X):
        return X - X.mean()

layer = CenteredLayer()
print("无参数层 · 输出：", layer(torch.tensor([[1.0, 2.0, 3.0]])).tolist(), "（每个数减去了均值 2）")

# ---- ② 带参数的层：可学习的仿射变换 ----
class MyLinear(nn.Module):
    '''自己写一个等价于 nn.Linear 的层：output = input @ weight.T + bias'''
    def __init__(self, in_units, units):
        super().__init__()
        self.weight = nn.Parameter(torch.randn(in_units, units))   # 用 nn.Parameter 声明可学习参数
        self.bias   = nn.Parameter(torch.randn(units,))

    def forward(self, X):
        linear = torch.matmul(X, self.weight.data) + self.bias.data
        return nn.functional.relu(linear)

线性层 = MyLinear(5, 3)
print("带参数层 · 输入(2,5) → 输出形状：", tuple(线性层(torch.rand(2, 5)).shape))
print("它的参数：", [p.shape for p in 线性层.parameters()])
"""))

cells.append(md("""## 3. 参数管理：访问、初始化、共享

- **访问**：`net.state_dict()` 是「层名 → 参数张量」的字典；`net[i].weight` 按层取；
- **初始化**：用 `nn.init.normal_ / constant_ / xavier_uniform_` 等；
- **共享**：让两个层指向**同一个参数对象**，训练时会一起更新。
"""))

cells.append(code("""# ---- 参数访问、初始化、共享 ----
net = MLP()
print("state_dict 的键：", list(net.state_dict().keys()))

# 访问某个参数并初始化
nn.init.normal_(net.hidden.weight, mean=0, std=0.01)
nn.init.zeros_(net.hidden.bias)
print("hidden 层权重均值（初始化为 N(0,0.01)）：", f"{net.hidden.weight.detach().mean().item():.5f}")

# 参数共享：让同一个层在网络里「用两次」，权重就是同一份（训练时同步更新）
shared = nn.Linear(8, 8)
net = nn.Sequential(shared, nn.ReLU(), shared)   # 同一个 shared 层出现两次
print("两个位置指向同一份权重？", net[0].weight is net[2].weight)
print("权重形状：", tuple(shared.weight.shape))
"""))

cells.append(md("""## 4. 读写模型：保存 / 加载 checkpoint

- **只存参数**（推荐）：`torch.save(net.state_dict(), path)`，加载时先建同结构模型再 `load_state_dict`；
- **存整个对象**：`torch.save(net, path)`，简单但可移植性差；
- **断点续训**：把「参数 + 优化器状态 + epoch」一起存进 dict。
"""))

cells.append(code("""# ---- 保存 / 加载模型 ----
import tempfile, os
net = MLP()
X = torch.rand(2, 20)

# ① 保存 state_dict（只存参数）
os.makedirs('../data', exist_ok=True)
torch.save(net.state_dict(), '../data/_mlp.params')

# ② 加载：先建同结构模型，再 load_state_dict
clone = MLP()
clone.load_state_dict(torch.load('../data/_mlp.params'))
print("加载成功，两个模型参数一致：", all(torch.equal(a, b) for a, b in zip(net.parameters(), clone.parameters())))

# ③ 断点续训：存「参数 + 优化器 + epoch」
trainer = torch.optim.SGD(net.parameters(), lr=0.1)
torch.save({'model': net.state_dict(), 'optimizer': trainer.state_dict(), 'epoch': 5},
           '../data/_checkpoint.pt')
ckpt = torch.load('../data/_checkpoint.pt')
print("checkpoint 里存的键：", list(ckpt.keys()), "| epoch =", ckpt['epoch'])
"""))

cells.append(md("""## 5. 小结

| 概念 | 一句话直觉 |
| --- | --- |
| 块 nn.Module | 网络的基本积木：`__init__` 建层、`forward` 写前向 |
| 自定义层 | 带参数的层要 `nn.Parameter` 声明参数 |
| state_dict | 「层名 → 参数」字典，保存/加载就靠它 |
| 参数共享 | 两个层指向同一参数对象，训练时一起更新 |
| 保存模型 | 只存 `state_dict`（推荐）或存整个对象 |

> 💡 本机是 CPU 版 PyTorch，没装 GPU 驱动；有 GPU 时用 `net.to('cuda')` 把模型和张量一起搬上 GPU 即可，代码只多一行。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\深度学习计算-自定义层与参数管理.ipynb", cells)

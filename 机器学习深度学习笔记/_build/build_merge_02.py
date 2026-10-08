# -*- coding: utf-8 -*-
"""批次2融合：李沐 d2l 的「MLP / 权重衰减与Dropout / 深度学习计算」并入对应章节。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, load_nb, save_json

NB = r"D:\NoteBook\机器学习深度学习笔记\机器学习深度学习完整笔记.ipynb"
nb = load_nb(NB)
cells = nb["cells"]

ch11_new = [md("""## 11.7 【李沐 d2l】多层感知机 MLP：从零与简洁实现

> 📌 **出处**：李沐《动手学深度学习 V2》第 4 章「多层感知机」
> 📎 **完整可运行代码**：`实战代码_李沐/多层感知机-从零与简洁实现.ipynb`

第 2 章从概念上讲了神经元和层，这一节把**多层感知机（MLP）**落到 PyTorch 代码。MLP 就是在输入输出之间加**隐藏层 + ReLU**：

$$H = \\mathrm{ReLU}(XW_1+b_1), \\quad O = HW_2+b_2$$

### 从零实现 vs 简洁实现

| | 从零 | 简洁 |
| --- | --- | --- |
| 参数 | 手动 `W1,b1,W2,b2` | `nn.Linear(784,256)` + `nn.Linear(256,10)` |
| 激活 | 手写 `relu = max(x,0)` | `nn.ReLU()` |
| 组装 | 手写 `net(X)` | `nn.Sequential(Flatten, Linear, ReLU, Linear)` |

```python
# 简洁实现（一行网络）
net = nn.Sequential(nn.Flatten(), nn.Linear(784, 256), nn.ReLU(), nn.Linear(256, 10))
```

> 🔑 **记忆**：
> - MLP = **线性层 + 非线性激活函数**反复堆叠；
> - 隐藏层神经元数（如 256）是**超参数**，越大模型越强但也越容易过拟合；
> - 隐藏层常配 **ReLU**，输出层按任务选（回归=线性、二分类=sigmoid、多分类=softmax）。
""")]

ch8_new = [md("""## 8.9 【李沐 d2l】权重衰减与 Dropout 的 PyTorch 实现

> 📌 **出处**：李沐《动手学深度学习 V2》第 4 章「权重衰减 / 暂退法」
> 📎 **完整可运行代码**：`实战代码_李沐/权重衰减与Dropout.ipynb`

8.6 节讲了概念，这里给出 d2l 的两行落地写法：

**权重衰减（L2）**：在损失里加 `λ·‖w‖²/2`

```python
l = loss(net(X), y) + lambd * (w ** 2).sum() / 2    # 从零：手动加 L2 惩罚
trainer = optim.SGD(..., weight_decay=lambd)         # 简洁：optim 自带 weight_decay
```

**Dropout**：训练时随机置零一部分激活，并除以 `1-p` 补偿幅度

```python
def dropout_layer(X, p):
    mask = (torch.rand(X.shape) > p).float()
    return mask * X / (1.0 - p)        # 除以 1-p 保持期望不变

net = nn.Sequential(..., nn.Dropout(0.5))   # 简洁：nn.Dropout 一行
```

> 🔑 **记忆**：
> - 权重衰减作用于**参数**（逼权重变小），Dropout 作用于**激活值**（逼不依赖单个神经元）；
> - Dropout **只在训练时用**：`model.train()` 开、`model.eval()` 关；
> - 实验结论：特征多、样本少时（如 200 特征、20 样本），权重衰减能把过拟合的测试损失大幅拉回来。
""")]

ch16_new = [md("""## 16.8 【李沐 d2l】深度学习计算：自定义块、参数管理、读写模型

> 📌 **出处**：李沐《动手学深度学习 V2》第 5 章「层和块 / 参数管理 / 自定义层 / 读写文件」
> 📎 **完整可运行代码**：`实战代码_李沐/深度学习计算-自定义层与参数管理.ipynb`

16.1 讲了用 `nn.Module` 定义 MLP，这一节补上更底层的三件事：

```python
# ① 自定义块：继承 nn.Module
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden = nn.Linear(20, 256)
        self.out = nn.Linear(256, 10)
    def forward(self, X):
        return self.out(torch.relu(self.hidden(X)))

# ② 自定义带参数的层：用 nn.Parameter 声明
self.weight = nn.Parameter(torch.randn(in_, out_))

# ③ 保存 / 加载：只存 state_dict（推荐）
torch.save(net.state_dict(), 'model.params')
net.load_state_dict(torch.load('model.params'))
```

> 🔑 **记忆**：
> - **块 = `nn.Module`**：`__init__` 建层、`forward` 写前向，是所有复杂网络的地基；
> - 可学习参数要用 **`nn.Parameter`** 包起来，才会被 `parameters()` 收集、被优化器更新；
> - 保存模型**只存 `state_dict()`**（比存整个对象更可移植），断点续训再把优化器状态一起存进 dict。
""")]

def find_summary(prefix):
    for i, c in enumerate(cells):
        if "".join(c["source"]).startswith(prefix):
            return i
    raise RuntimeError("未找到小结: " + prefix)

plan = [
    ("## 16.7 本章小结", "## 16.8 本章小结", ch16_new),
    ("## 11.7 本章小结", "## 11.8 本章小结", ch11_new),
    ("## 8.8 本章小结",  "## 8.9 本章小结", ch8_new),
]
for old, new, new_cells in plan:
    idx = find_summary(old)
    cells[idx]["source"] = "".join(cells[idx]["source"]).replace(old, new, 1).splitlines(keepends=True)
    cells[idx:idx] = list(new_cells)
    print(f"在 {new} 前插入 {len(new_cells)} 个小节")

save_json(nb, NB)
print("批次2融合完成 ✔")

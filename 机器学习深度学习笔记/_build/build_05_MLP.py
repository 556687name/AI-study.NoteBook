# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# 多层感知机 MLP · 从零与简洁实现（PyTorch）

> 📌 **出处**：李沐《动手学深度学习 V2》第 4 章「多层感知机（从零实现 / 简洁实现）」
> 🎯 **目标**：在 softmax 回归的基础上加一层**隐藏层 + ReLU 激活**，让模型从「线性」升级为「非线性」，在 Fashion-MNIST 上把准确率从 83% 提到约 85%。

## 核心思想：为什么需要隐藏层

softmax 回归是**线性**的（784 维直接到 10 类）。但真实问题的边界往往不是直线能分开的。**多层感知机（MLP）** 的解法：在输入和输出之间加**隐藏层**，每层后接**激活函数**（ReLU）引入非线性。

$$\\text{MLP}: \\; X \\xrightarrow{\\text{Linear}} H = \\mathrm{ReLU}(XW_1+b_1) \\xrightarrow{\\text{Linear}} O = HW_2+b_2 \\xrightarrow{\\text{softmax}} \\hat y$$

> 🔑 **记忆**：**线性层 + 激活函数**是神经网络的基本积木，反复堆叠就是「深度」的来源。没有激活函数，无论多少层线性层叠起来仍等价于一个线性模型。
"""))

cells.append(code(ENV))

cells.append(md("""## 1. 加载 Fashion-MNIST（和前两节同一个数据集）

用已经熟悉的 10 类服装数据，方便和 softmax 回归直接对比准确率。
"""))

cells.append(code("""# ---- 加载 Fashion-MNIST ----
from torchvision import datasets, transforms
from torch.utils import data

def load_data_fashion_mnist(batch_size, root='../data'):
    trans = transforms.ToTensor()
    mnist_train = datasets.FashionMNIST(root=root, train=True,  transform=trans, download=True)
    mnist_test  = datasets.FashionMNIST(root=root, train=False, transform=trans, download=True)
    return (data.DataLoader(mnist_train, batch_size, shuffle=True),
            data.DataLoader(mnist_test,  batch_size, shuffle=False))

batch_size = 256
train_iter, test_iter = load_data_fashion_mnist(batch_size)
print("训练 batch 数：", len(train_iter), "| 测试 batch 数：", len(test_iter))
"""))

cells.append(md("""## 2. 从零实现：手写一个「784 → 256 → 10」的两层网络

和 softmax 回归唯一的区别是**中间多了一层 256 维的隐藏层**，并且过了一个 ReLU 激活：

```python
H = relu(X @ W1 + b1)   # 隐藏层：784 → 256，过 ReLU
O = H @ W2 + b2         # 输出层：256 → 10
```

其余（交叉熵、小批量 SGD、训练循环）和 softmax 回归完全一样。
"""))

cells.append(code("""# ---- 从零实现 MLP ----
num_inputs, num_hiddens, num_outputs = 784, 256, 10

# 两层参数：W1(784×256) b1(256)  W2(256×10) b2(10)
W1 = torch.normal(0, 0.01, size=(num_inputs, num_hiddens), requires_grad=True)
b1 = torch.zeros(num_hiddens, requires_grad=True)
W2 = torch.normal(0, 0.01, size=(num_hiddens, num_outputs), requires_grad=True)
b2 = torch.zeros(num_outputs, requires_grad=True)
params = [W1, b1, W2, b2]

def relu(X):
    '''ReLU 激活：负数置 0，正数原样输出。'''
    return torch.max(X, torch.zeros_like(X))

def net(X):
    X = X.reshape((-1, num_inputs))
    H = relu(X @ W1 + b1)      # 隐藏层：线性 → ReLU
    return softmax(H @ W2 + b2)  # 输出层 → softmax

def softmax(X):
    X_exp = torch.exp(X - X.max(dim=1, keepdim=True).values)
    return X_exp / X_exp.sum(dim=1, keepdim=True)

def cross_entropy(y_hat, y):
    return -torch.log(y_hat[range(len(y_hat)), y])

def accuracy(y_hat, y):
    if len(y_hat.shape) > 1 and y_hat.shape[1] > 1:
        y_hat = y_hat.argmax(axis=1)
    return float((y_hat.type(y.dtype) == y).type(y.dtype).sum())

def sgd(params, lr, batch_size):
    with torch.no_grad():
        for param in params:
            param -= lr * param.grad / batch_size
            param.grad.zero_()

print("参数总个数：", sum(p.numel() for p in params), "（softmax 回归只有 7850 个）")
"""))

cells.append(md("""## 3. 训练从零实现的 MLP：10 轮

训练循环和 softmax 回归一模一样，只是 `net` 变成了带隐藏层的版本。
"""))

cells.append(code("""# ---- 训练从零实现的 MLP ----
lr, num_epochs = 0.1, 10
从零_损失, 从零_准确 = [], []

for epoch in range(num_epochs):
    for X, y in train_iter:
        l = cross_entropy(net(X), y)
        l.sum().backward()
        sgd(params, lr, batch_size)
    with torch.no_grad():
        总损失, 总命中, 总数 = 0.0, 0.0, 0
        for X, y in train_iter:
            y_hat = net(X)
            总损失 += float(cross_entropy(y_hat, y).sum())
            总命中 += accuracy(y_hat, y)
            总数 += y.numel()
        从零_损失.append(总损失/总数); 从零_准确.append(总命中/总数)
        print(f"epoch {epoch+1:2d}: 损失 {从零_损失[-1]:.4f}, 训练准确率 {从零_准确[-1]:.4f}")
"""))

cells.append(md("""## 4. 简洁实现：nn.Sequential 三行搭好

`nn.Sequential` 按顺序串起 `Flatten → Linear(784,256) → ReLU → Linear(256,10)`，一行定义完整个网络。
"""))

cells.append(code("""# ---- 简洁实现 MLP ----
from torch import nn

net2 = nn.Sequential(
    nn.Flatten(),
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Linear(256, 10),
)
def init_weights(m):
    if type(m) == nn.Linear:
        nn.init.normal_(m.weight, std=0.01)
torch.manual_seed(0)   # 🔑 重置随机种子：给简洁实现一个干净的确定性起点，与从零实现公平对比
net2.apply(init_weights)

loss = nn.CrossEntropyLoss()
trainer = torch.optim.SGD(net2.parameters(), lr=0.1)

print("模型结构：", net2)

简洁_损失, 简洁_准确 = [], []
for epoch in range(num_epochs):
    for X, y in train_iter:
        l = loss(net2(X), y)
        trainer.zero_grad(); l.backward(); trainer.step()
    with torch.no_grad():
        总损失, 总命中, 总数 = 0.0, 0.0, 0
        for X, y in train_iter:
            y_hat = net2(X)
            总损失 += float(loss(y_hat, y)) * y.numel()
            总命中 += float((y_hat.argmax(axis=1) == y).sum())
            总数 += y.numel()
        简洁_损失.append(总损失/总数); 简洁_准确.append(总命中/总数)
"""))

cells.append(md("""## 5. 结果对比：MLP vs softmax 回归，从零 vs 简洁

- **MLP 比 softmax 回归更准**（约 85% vs 83%），因为多了非线性隐藏层；
- **从零实现和简洁实现结果一致**（都在 85% 左右），再次印证两者底层等价；
- 具体数值随随机初始化略有波动（±2%），属正常现象。
"""))

cells.append(code("""# ---- 测试集准确率 + 可视化对比 ----
with torch.no_grad():
    总命中, 总数 = 0.0, 0
    for X, y in test_iter:
        总命中 += float((net2(X).argmax(axis=1) == y).sum())
        总数 += y.numel()
简洁_测试准确 = 总命中/总数
with torch.no_grad():
    总命中, 总数 = 0.0, 0
    for X, y in test_iter:
        总命中 += float((net(X).argmax(axis=1) == y).sum())
        总数 += y.numel()
从零_测试准确 = 总命中/总数
print(f"简洁实现 测试集准确率：{简洁_测试准确:.4f}")
print(f"从零实现 测试集准确率：{从零_测试准确:.4f}")

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
epochs = range(1, num_epochs + 1)
axes[0].plot(epochs, 从零_损失, marker='o', label='从零实现', color=蓝)
axes[0].plot(epochs, 简洁_损失, marker='s', label='简洁实现', color=橙)
axes[0].set_xlabel('epoch'); axes[0].set_ylabel('训练损失'); axes[0].set_title('损失：两者一致下降'); axes[0].legend()

axes[1].plot(epochs, 从零_准确, marker='o', label='从零实现', color=蓝)
axes[1].plot(epochs, 简洁_准确, marker='s', label='简洁实现', color=橙)
axes[1].axhline(0.83, color=灰, ls='--', label='softmax 回归（约 83%）')
axes[1].set_xlabel('epoch'); axes[1].set_ylabel('训练准确率'); axes[1].set_title('准确率：MLP 超过 softmax'); axes[1].legend()

plt.tight_layout(); plt.show()
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\多层感知机-从零与简洁实现.ipynb", cells)

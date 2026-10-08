# -*- coding: utf-8 -*-
CELLS = [
    ("markdown", r'''# 第十一章 神经网络与反向传播

> 📌 **出处**：李宏毅 2026《机器学习》**神经网络专题**（神经元、激活函数、多层感知机 MLP、前向传播、反向传播 Backpropagation、梯度消失）
> ⭐ **40 天重点**：对应计划 Day12「神经网络与反向传播」、Day13「深度学习基础」。第二章已经建立了「神经元、激活函数、层、深度」的直觉，这一章把它推进到**神经网络最核心的机制：反向传播**——深度学习能训练成千上万个参数，全靠它。

---

## 11.1 从逻辑回归到神经网络：把「一个」变成「很多个」

回想逻辑回归：输入 $\mathbf{x}$，线性变换 $z = \mathbf{w}^\top\mathbf{x} + b$，再过一个 sigmoid 得到概率。这是一个**单个「神经元」**做的事。

神经网络做的事，本质上就是：**把很多个这样的神经元「叠」起来、连起来**，让它们分层协作：

- **输入层**：接收原始特征 $\mathbf{x}$；
- **隐藏层**：一层或多层，每层有多个神经元，做「线性变换 + 非线性激活」；
- **输出层**：产生最终预测（回归输出数值 / 分类输出概率）。

因为有了「隐藏层」和「非线性激活函数」，神经网络能表达远复杂的函数——这正是它能解决 XOR、识别图像、理解语言的根源。

> 💡 一句话：**神经网络 = 一堆神经元分层堆叠 + 非线性激活**。而「怎么训练这么复杂的东西」的答案，就是本章主角**反向传播**。
'''),
    ("markdown", r'''## 11.2 前向传播：把输入一层层「算」到输出

**前向传播（forward propagation）** 就是「从输入算出预测」的过程，逐层执行两个步骤（以一层为例）：

1. **线性变换**：$z^{[l]} = W^{[l]} a^{[l-1]} + b^{[l]}$（第 $l$ 层把上一层输出 $a^{[l-1]}$ 加权求和）；
2. **非线性激活**：$a^{[l]} = g(z^{[l]})$（$g$ 是激活函数，如 ReLU、sigmoid）。

其中 $a^{[0]} = \mathbf{x}$（第 0 层就是输入），最后一层的 $a^{[L]}$ 就是预测 $\hat y$。整个网络就是一个**层层嵌套的函数**：

$$\hat y = g^{[L]}\big(W^{[L]}\,g^{[L-1]}(\cdots g^{[1]}(W^{[1]}x + b^{[1]})\cdots) + b^{[L]}\big)$$

### 为什么必须要有「非线性」激活函数？

如果每一层都只是线性变换（没有激活），那多层线性变换叠加起来**仍然只是一个线性变换**（矩阵乘法再乘法还是矩阵乘法）。那样「再深的网络」也只能表达线性函数，等于白堆了。**非线性激活函数**是神经网络「能表达复杂函数」的钥匙。

> 🔑 **记忆**：没有激活函数的深层网络退化成线性模型；非线性激活让「深度」真正有意义。
'''),
    ("markdown", r'''## 11.3 反向传播：用「链式法则」把梯度从后往前传

**反向传播（Backpropagation）** 是**计算神经网络里每个参数梯度的算法**，本质就是微积分的**链式法则（chain rule）**，只是被高效地组织成「从输出层一路往回传」。

### 为什么需要它？

神经网络有成千上万个参数。如果对每个参数都「单独算一次梯度」（用数值差分 $\frac{L(w+\epsilon)-L(w)}{\epsilon}$），参数一多就慢到不可接受。反向传播的高明之处在于：**一次「前向 + 反向」就把所有参数的梯度全算出来**，计算量和前向传播同量级。

### 核心直觉：梯度沿「计算图」反向流动

把网络的每一步看成一张**计算图**（计算图：每个节点是一个运算，边是数据的流向）。前向传播时数据从左到右流；反向传播时，**梯度从右（损失）往左（参数）流**，每经过一个运算就按「链式法则」把梯度拆解传播。

链式法则一句话版：若 $L$ 通过 $a$ 依赖 $z$，$z$ 又依赖 $w$，则

$$\frac{\partial L}{\partial w} = \frac{\partial L}{\partial a}\cdot\frac{\partial a}{\partial z}\cdot\frac{\partial z}{\partial w}$$

即「梯度 = 外层梯度 × 本层局部梯度」，一层层往回乘。
'''),
    ("markdown", r'''## 11.4 反向传播的逐步推导（以两层网络为例）

下面用一个**两层网络 + MSE 损失**的完整例子，把反向传播的每一步算清楚。设网络结构：输入 $x$ → 隐藏层（1 个神经元，sigmoid）→ 输出 $\hat y$。

### 记号

- 隐藏层：$z_1 = w_1 x + b_1$，$a_1 = \sigma(z_1)$；
- 输出层：$\hat y = w_2 a_1 + b_2$；
- 损失（单个样本）：$L = \frac12(\hat y - y)^2$（系数 $\frac12$ 让求导好看）。

### 反向传播四步（🔑 要会跟着推）

**第一步：算损失对输出的梯度**

$$\frac{\partial L}{\partial \hat y} = \hat y - y$$

**第二步：把梯度传到输出层参数 $w_2, b_2$**

$$\frac{\partial L}{\partial w_2} = \frac{\partial L}{\partial \hat y}\cdot\frac{\partial \hat y}{\partial w_2} = (\hat y - y)\cdot a_1, \qquad \frac{\partial L}{\partial b_2} = (\hat y - y)\cdot 1$$

**第三步：把梯度继续传到隐藏层输出 $a_1$**

$$\frac{\partial L}{\partial a_1} = \frac{\partial L}{\partial \hat y}\cdot\frac{\partial \hat y}{\partial a_1} = (\hat y - y)\cdot w_2$$

**第四步：穿过 sigmoid，传到隐藏层参数 $w_1, b_1$**

sigmoid 的导数是 $\sigma'(z_1) = \sigma(z_1)(1-\sigma(z_1)) = a_1(1-a_1)$，所以：

$$\frac{\partial L}{\partial z_1} = \frac{\partial L}{\partial a_1}\cdot a_1(1-a_1)$$

$$\frac{\partial L}{\partial w_1} = \frac{\partial L}{\partial z_1}\cdot x, \qquad \frac{\partial L}{\partial b_1} = \frac{\partial L}{\partial z_1}\cdot 1$$

### 看出规律了吗？

每一步都是「**拿到从后面传来的梯度 $\frac{\partial L}{\partial a}$，乘上本层的局部导数 $\frac{\partial a}{\partial z}$、$\frac{\partial z}{\partial w}$，继续往前传**」。这正是「反向传播」名字的由来——梯度从损失出发，一层层往输入方向「传播」。下面的代码把上面的公式完整实现出来。
'''),
    ("code", r'''# ---- 从零实现两层网络的前向传播 + 反向传播（手动求梯度） ----
# 用上面 11.4 节推导的公式，手动实现一次前向 + 反向，验证梯度正确。

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# 单个样本：x=0.6, y=1.0
x, y = 0.6, 1.0

# 随机初始化参数
np.random.seed(5)
w1, b1 = 0.5, -0.3
w2, b2 = 0.2, 0.1

# ---- 前向传播 ----
z1 = w1 * x + b1
a1 = sigmoid(z1)
y_hat = w2 * a1 + b2
L = 0.5 * (y_hat - y) ** 2

print(f"前向传播：z1={z1:.4f}, a1={a1:.4f}, ŷ={y_hat:.4f}, 损失 L={L:.4f}")

# ---- 反向传播（按 11.4 节公式一步步算） ----
dL_dyhat = y_hat - y                      # 第一步
dL_dw2 = dL_dyhat * a1                    # 第二步
dL_db2 = dL_dyhat * 1
dL_da1 = dL_dyhat * w2                    # 第三步
dL_dz1 = dL_da1 * a1 * (1 - a1)           # 第四步（穿过 sigmoid）
dL_dw1 = dL_dz1 * x
dL_db1 = dL_dz1 * 1

print("反向传播得到的梯度：")
print(f"  ∂L/∂w1 = {dL_dw1:.4f},  ∂L/∂b1 = {dL_db1:.4f}")
print(f"  ∂L/∂w2 = {dL_dw2:.4f},  ∂L/∂b2 = {dL_db2:.4f}")

# ---- 用数值梯度（差分法）验证反向传播是否正确 ----
def 损失(w1, b1, w2, b2):
    a1 = sigmoid(w1 * x + b1)
    return 0.5 * (w2 * a1 + b2 - y) ** 2

eps = 1e-5
数值_dw1 = (损失(w1+eps, b1, w2, b2) - 损失(w1-eps, b1, w2, b2)) / (2*eps)
数值_dw2 = (损失(w1, b1, w2+eps, b2) - 损失(w1, b1, w2-eps, b2)) / (2*eps)

print(f"\n数值梯度验证：∂L/∂w1 ≈ {数值_dw1:.4f}（反向传播算得 {dL_dw1:.4f}）")
print(f"               ∂L/∂w2 ≈ {数值_dw2:.4f}（反向传播算得 {dL_dw2:.4f}）")
print("两者几乎一致 → 反向传播的公式正确 ✅")
'''),
    ("markdown", r'''## 11.5 完整的训练循环：前向 + 反向 + 更新

把「前向传播、反向传播、参数更新」串起来，就是一个完整的神经网络训练循环（这正是第十六章 PyTorch 训练循环的「手写版」）：

1. **前向**：算预测 $\hat y$ 和损失 $L$；
2. **反向**：算每个参数的梯度 $\frac{\partial L}{\partial \theta}$；
3. **更新**：$\theta \leftarrow \theta - \eta \cdot \frac{\partial L}{\partial \theta}$（梯度下降）。

下面的代码用这个完整流程，训练一个两层网络解决 **XOR（异或）问题**——一个经典的「线性模型解不了、必须靠神经网络」的问题。XOR 真值表：输入 $(0,0)\to0,\ (0,1)\to1,\ (1,0)\to1,\ (1,1)\to0$，两个输入相同时输出 0、不同时输出 1。
'''),
    ("code", r'''# ---- 从零训练两层网络解决 XOR（异或）问题 ----
# XOR 是线性不可分的，必须用带非线性隐藏层的网络才能学会。
np.random.seed(1)

# XOR 数据
X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_xor = np.array([[0], [1], [1], [0]])

# 网络结构：2 输入 → 2 隐藏神经元(sigmoid) → 1 输出(sigmoid)
n_in, n_hid, n_out = 2, 2, 1
W1 = np.random.randn(n_in, n_hid) * 0.5
b1 = np.zeros((1, n_hid))
W2 = np.random.randn(n_hid, n_out) * 0.5
b2 = np.zeros((1, n_out))

lr = 0.5
损失记录 = []
for epoch in range(5000):
    # ---- 前向 ----
    Z1 = X_xor @ W1 + b1
    A1 = sigmoid(Z1)                 # 隐藏层激活
    Z2 = A1 @ W2 + b2
    A2 = sigmoid(Z2)                 # 输出（概率）
    # MSE 损失
    L = np.mean((A2 - y_xor) ** 2)
    损失记录.append(L)

    # ---- 反向（向量化，一次算整批 4 个样本） ----
    dA2 = (A2 - y_xor) * (A2 * (1 - A2))      # 穿过输出层 sigmoid
    dW2 = A1.T @ dA2
    db2 = np.sum(dA2, axis=0, keepdims=True)
    dA1 = dA2 @ W2.T
    dZ1 = dA1 * (A1 * (1 - A1))               # 穿过隐藏层 sigmoid
    dW1 = X_xor.T @ dZ1
    db1 = np.sum(dZ1, axis=0, keepdims=True)

    # ---- 更新 ----
    W1 -= lr * dW1; b1 -= lr * db1
    W2 -= lr * dW2; b2 -= lr * db2

print("训练后网络的预测（应接近 [0,1,1,0]）：")
print(np.round(A2.ravel(), 3))
print(f"\n最终损失 = {损失记录[-1]:.6f}")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].plot(损失记录, color=橙, lw=2)
axes[0].set_xlabel('epoch'); axes[0].set_ylabel('损失')
axes[0].set_title('XOR 训练：损失一路下降')
axes[0].grid(alpha=0.3)
axes[1].bar(range(4), A2.ravel(), color=蓝, alpha=0.8)
axes[1].axhline(0.5, color=灰, ls='--', lw=1, label='阈值 0.5')
axes[1].set_xticks(range(4)); axes[1].set_xticklabels(['(0,0)→0', '(0,1)→1', '(1,0)→1', '(1,1)→0'])
axes[1].set_ylabel('预测概率'); axes[1].set_title('四个输入的预测')
axes[1].legend()
plt.tight_layout()
plt.show()

# 关键：XOR 是线性不可分的（没法画一条直线分开 0 和 1），
# 但两层网络通过隐藏层学到了非线性决策，成功拟合。
'''),
    ("markdown", r'''## 11.6 反向传播中的经典问题：梯度消失与梯度爆炸

反向传播要把梯度**一层层乘回去**。当网络很深时，这个「连乘」会带来两个著名问题：

- **梯度消失（vanishing gradient）**：如果每一层的局部梯度都小于 1（比如 sigmoid 导数最大才 0.25），几十层乘下来，梯度会**指数级地衰减到接近 0**——前面的层几乎学不到任何东西，训练停滞；
- **梯度爆炸（exploding gradient）**：反之，如果局部梯度都大于 1，连乘会让梯度**指数级膨胀**，参数一步更新飞出天际，损失变成 NaN。

### 为什么会这样？关键在激活函数和权重初始化

- **sigmoid / tanh** 在两端「饱和」，导数趋近 0，是梯度消失的重灾区；
- **ReLU** 在正半轴导数恒为 1，大大缓解了梯度消失（这也是它流行的原因之一）；
- 合理的**权重初始化**（如 Xavier、He 初始化）能控制每层的梯度尺度，避免爆炸。

> 💡 这些是深度网络训练的经典难题，现代架构（残差连接 ResNet、归一化层、更好的激活函数）很大程度就是为了「修」梯度传播。第十二、十三章会继续遇到。
'''),
    ("markdown", r'''## 11.7 本章小结

| 概念 | 一句话直觉 |
| --- | --- |
| 神经网络 | 神经元分层堆叠 + 非线性激活 |
| 前向传播 | 输入逐层算到输出 |
| 反向传播 | 用链式法则把梯度从后往前传 |
| 链式法则 | 梯度 = 外层梯度 × 本层局部梯度，层层相乘 |
| 梯度消失/爆炸 | 深层连乘导致梯度趋近 0 或爆炸 |

🔑 **记忆**：反向传播 = 链式法则的高效实现；sigmoid 导数 $\sigma'(z)=\sigma(z)(1-\sigma(z))$；「前向算损失、反向算梯度、更新参数」是训练循环三步。

> 📌 **下一步**：第十二章讲 **CNN（卷积神经网络）**——把「全连接」换成「卷积」，专门处理图像，并引出 ResNet 等现代结构。
'''),
]

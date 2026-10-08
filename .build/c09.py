# -*- coding: utf-8 -*-
CELLS = [
    ("markdown", r'''# 第九章 逻辑回归

> 📌 **出处**：李宏毅 2026《机器学习》**分类与逻辑回归**专题（Sigmoid、决策边界、交叉熵 Cross Entropy、逻辑回归与线性回归、softmax、分类问题的损失函数）
> ⭐ **40 天重点**：对应计划 Day16「逻辑回归 + 第一个模型」。逻辑回归是**分类任务的入门模型**，它名字里有「回归」，做的却是**分类**——这一章讲清楚它为什么叫这个名字、以及背后的核心思想。

---

## 9.1 从「预测数值」到「预测类别」

前面几章都在做**回归**：输出一个连续数值（如房价 500 万）。但很多问题要的是**分类（classification）**：输出一个**类别**，比如「这封邮件是不是垃圾邮件？」「这张图是猫还是狗？」「明天会不会下雨？」

最直观的想法：能不能还用线性回归，让它输出一个数，再根据这个数判断类别？比如输出 $z = w x + b$，然后规定「$z > 0.5$ 算正类，$z < 0.5$ 算负类」？

这个想法**有个严重问题**：线性回归的输出是**无界的**（可以从 $-\infty$ 到 $+\infty$），而「概率」应该被限制在 $[0, 1]$ 之间。而且直接拿「距离 0.5 多远」当作置信度，在数学上很不舒服。

**逻辑回归的解决办法**：在线性输出的外面，**套一个把任意实数「压」到 $[0,1]$ 的函数**，让输出变成「属于正类的概率」。这个函数就是 **sigmoid**。
'''),
    ("markdown", r'''## 9.2 Sigmoid 函数：把任意实数压成 [0,1] 的概率

Sigmoid 函数（也叫逻辑函数 logistic function）的定义：

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

它的图像是一条 **S 形曲线**：

- 当 $z \to +\infty$，$\sigma(z) \to 1$；
- 当 $z \to -\infty$，$\sigma(z) \to 0$；
- 当 $z = 0$，$\sigma(0) = 0.5$。

于是**逻辑回归**把线性回归的输出 $z = w x + b$ 送进 sigmoid，得到「概率」：

$$\hat y = \sigma(w x + b) = \frac{1}{1 + e^{-(w x + b)}}$$

这个 $\hat y$ 就解释为「样本属于正类（$y=1$）的概率」。

> 💡 **为什么叫「逻辑回归」？** 因为它内部用了 sigmoid（逻辑）函数做非线性变换，但核心仍是「线性回归 + 一个非线性映射」。它本质是一个**分类器**，却继承了「回归」的名字——这是历史原因，别被名字骗了。
'''),
    ("code", r'''# ---- Sigmoid 函数可视化：S 形曲线 ----
z = np.linspace(-8, 8, 300)
sig = 1 / (1 + np.exp(-z))

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(z, sig, color=蓝, lw=2.5, label=r'$\sigma(z) = 1/(1+e^{-z})$')
ax.axhline(0.5, color=灰, ls='--', lw=1, label='z=0 时 σ=0.5')
ax.axvline(0, color=灰, ls='--', lw=1)
ax.axhline(0, color=灰, lw=0.8); ax.axhline(1, color=灰, lw=0.8)
ax.set_xlabel('z（线性输出 w·x+b）'); ax.set_ylabel('σ(z)（概率）')
ax.set_title('Sigmoid：把 (-∞,+∞) 压到 (0,1)，z=0 对应概率 0.5')
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# 记忆点：z 越大 → 概率越接近 1；z 越小 → 概率越接近 0；z=0 → 正好 0.5。
'''),
    ("markdown", r'''## 9.3 决策边界：模型在哪里「划线」分类

有了概率 $\hat y$，怎么判断类别？通常规定：

$$\text{预测类别} = \begin{cases} 1\ (\text{正类}) & \text{若}\ \hat y \ge 0.5 \\ 0\ (\text{负类}) & \text{若}\ \hat y < 0.5 \end{cases}$$

由于 $\sigma(z) = 0.5$ 当且仅当 $z = 0$，所以「判断为正类」等价于：

$$\hat y \ge 0.5 \iff z = w x + b \ge 0$$

这条 $w x + b = 0$ 就是**决策边界（decision boundary）**——模型在这条线（或面）的两侧分别预测不同类别。

- **一维特征**：决策边界是一个**点**（$x = -b/w$）；
- **二维特征**：决策边界是一条**直线**（$w_1 x_1 + w_2 x_2 + b = 0$）；
- **高维特征**：决策边界是一个**超平面**。

> 💡 注意：**逻辑回归只能画「直线」决策边界**（线性分类器）。这是它的局限——遇到「一个圈套一个圈」这种非线性分布的数据就无能为力，需要特征组合（第七章）或神经网络（第十一章）来画「曲线」边界。
'''),
    ("code", r'''# ---- 逻辑回归的决策边界可视化 ----
# 造一个线性可分的数据，训练逻辑回归，画出它的决策边界。
from sklearn.linear_model import LogisticRegression

np.random.seed(7)
n = 100
# 两类数据：一类在左上、一类在右下
X0 = np.random.randn(n, 2) * 0.7 + np.array([-2, -2])
X1 = np.random.randn(n, 2) * 0.7 + np.array([2, 2])
Xc = np.vstack([X0, X1])
yc = np.array([0] * n + [1] * n)

model = LogisticRegression()
model.fit(Xc, yc)

w1, w2 = model.coef_[0]
b = model.intercept_[0]
print(f"学到的参数：w1={w1:.3f}, w2={w2:.3f}, b={b:.3f}")
print(f"决策边界：{w1:.2f}·x1 + {w2:.2f}·x2 + {b:.2f} = 0")

# 画数据和决策边界（直线 w1·x1 + w2·x2 + b = 0）
xx = np.linspace(Xc[:, 0].min() - 1, Xc[:, 0].max() + 1, 100)
边界y = -(w1 * xx + b) / w2        # 由 w1·x + w2·y + b = 0 解出 y

fig, ax = plt.subplots(figsize=(7, 6))
ax.scatter(X0[:, 0], X0[:, 1], color=蓝, s=25, alpha=0.8, label='类别 0')
ax.scatter(X1[:, 0], X1[:, 1], color=橙, s=25, alpha=0.8, label='类别 1')
ax.plot(xx, 边界y, color=红, lw=2.5, label='决策边界')
ax.set_xlabel('特征 x1'); ax.set_ylabel('特征 x2')
ax.set_title('逻辑回归：一条直线把两类分开')
ax.legend()
plt.tight_layout()
plt.show()

# 记忆点：决策边界就是 z = w·x + b = 0 那条线，两侧分别预测不同类别。
'''),
    ("markdown", r'''## 9.4 交叉熵损失：为什么逻辑回归不用 MSE

现在要训练逻辑回归，用哪个损失函数？先看看「如果硬用 MSE 会怎样」。

### 为什么 MSE 不合适

预测值是概率 $\hat y \in (0,1)$，真实标签 $y \in \{0, 1\}$。用 MSE $=\frac{1}{m}\sum(\hat y - y)^2$：

- 数学上会导致**非凸**的损失曲面（出现很多局部最小），梯度下降难收敛；
- 而且当预测「错得很离谱」（比如真实是 1 却预测接近 0）时，MSE 给出的梯度**反而很小**（因为 sigmoid 两端很平），模型「错得越狠越学不动」——这非常不合理。

### 交叉熵（Cross Entropy）：分类任务的标准损失

交叉熵损失（二元分类）的定义：

$$L = -\frac{1}{m}\sum_{i=1}^{m}\Big[\, y_i \log \hat y_i + (1 - y_i)\log(1 - \hat y_i)\Big]$$

逐项看它的妙处：

- 当真实 $y_i = 1$ 时，只剩 $-\log \hat y_i$ 这一项。若预测 $\hat y_i$ 接近 1，$-\log \hat y_i$ 接近 0（惩罚小）；若预测接近 0，$-\log \hat y_i$ 冲向 $+\infty$（惩罚极大）——**错得越狠，惩罚越狠**；
- 当真实 $y_i = 0$ 时，只剩 $-\log(1 - \hat y_i)$，道理对称；
- 它天然和「概率」配合：我们想让「真实类别的预测概率」尽可能大，等价于让「负对数概率」尽可能小。

> 🔑 **记忆**：**分类任务用交叉熵，回归任务用 MSE**。交叉熵对「自信地犯错」惩罚极重，这正是我们想要的。下面代码对比两者的梯度行为。
'''),
    ("code", r'''# ---- 交叉熵 vs MSE：为什么分类要用交叉熵 ----
# 对比两种损失函数随"预测概率"变化的曲线（假设真实标签 y=1）。
p = np.linspace(0.001, 0.999, 400)      # 预测概率（避开 log(0)）

# 真实 y=1 时：
#   交叉熵 = -log(p)
#   MSE    = (p - 1)^2
交叉熵 = -np.log(p)
MSE损失 = (p - 1) ** 2

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(p, 交叉熵, color=红, lw=2.5, label='交叉熵 -log(p)（真实 y=1）')
ax.plot(p, MSE损失, color=蓝, lw=2.5, label='MSE (p-1)²（真实 y=1）')
ax.set_xlabel('预测概率 p'); ax.set_ylabel('损失')
ax.set_title('交叉熵 vs MSE：预测错得越离谱，交叉熵惩罚越狠')
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# 观察：当 p 接近 0（错得很离谱）时，交叉熵冲上去了（惩罚巨大），
# 而 MSE 最多到 1（惩罚封顶）。所以交叉熵能让模型"更卖力地改掉大错误"。
'''),
    ("markdown", r'''## 9.5 多分类：从二分类到「一对多」与 Softmax

前面只处理**两类**。现实常有多类（猫/狗/鸟/鱼）。有两种主流扩展方式。

### 方式一：一对多 OVR（One-vs-Rest）

把「K 类」拆成 **K 个二分类问题**：第 $k$ 个分类器回答「是不是第 $k$ 类？」，把「第 k 类」当正类、其余全当负类。预测时跑 K 个分类器，取**概率最高**的那个类。

- 优点：思路简单、可直接复用二分类逻辑回归；
- 缺点：K 类就要训练 K 个模型，且每个模型看到的「负类」都很多，数据不平衡。

### 方式二：Softmax 回归（多分类的标准做法）

Softmax 直接把一个「K 维的原始分数向量」转成「K 个类别的概率分布」，且**所有概率加起来 = 1**：

$$\text{softmax}(\mathbf{z})_k = \frac{e^{z_k}}{\sum_{j=1}^{K} e^{z_j}}$$

- 先对每个分数取指数 $e^{z_k}$（把负数变正、拉开差距）；
- 再除以所有指数之和，做**归一化**，保证和为 1；
- 得到的每个值就是「属于第 $k$ 类的概率」。

配合 softmax 的损失是**多分类交叉熵**：$L = -\sum_k y_k \log \hat y_k$（其中 $y_k$ 是 one-hot 真实标签）。

> 💡 **softmax 与 sigmoid 的关系**：二分类的 softmax 实际上退化成 sigmoid。所以可以理解为：**sigmoid 是 softmax 在「两类」时的特例**。
'''),
    ("code", r'''# ---- Softmax 演示：把任意分数变成"和为 1 的概率分布" ----
def softmax(z):
    e = np.exp(z - np.max(z))       # 减去最大值，防止数值溢出（结果不变）
    return e / e.sum()

分数 = np.array([2.0, 1.0, 0.1, 3.0])
概率 = softmax(分数)

print("原始分数（logits）：", 分数)
print("softmax 后概率：  ", np.round(概率, 4))
print("概率之和 =", 概率.sum(), "（一定等于 1）")

# 可视化：分数 → 概率
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].bar(['类0', '类1', '类2', '类3'], 分数, color=蓝, alpha=0.8)
axes[0].set_title('原始分数 z（可正可负，无约束）')
axes[0].set_ylabel('分数')
axes[1].bar(['类0', '类1', '类2', '类3'], 概率, color=橙, alpha=0.8)
axes[1].set_title('softmax 后：概率分布（和为 1）')
axes[1].set_ylabel('概率')
plt.tight_layout()
plt.show()

# 记忆点：softmax 让"最大的分数"变成"最高的概率"，且所有概率归一化到 1。
'''),
    ("markdown", r'''## 9.6 sklearn 实战：LogisticRegression 多分类

sklearn 里 `LogisticRegression` 一行搞定，多分类默认用 OVR 或 multinomial（softmax），通过 `multi_class` 参数控制：

- `multi_class='ovr'`：一对多；
- `multi_class='multinomial'`：softmax 回归（真正的多分类）；
- 默认 `multi_class='auto'` 会自动根据数据选择。

训练后和线性回归一样有 `.coef_`、`.intercept_`，但注意**多分类时** `.coef_` 形状是 `(类别数, 特征数)`——每个类有一组权重。
'''),
    ("code", r'''# ---- sklearn 多分类逻辑回归 ----
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression

# 造一个 3 类、2 特征的分类数据（便于画图）
Xm, ym = make_classification(n_samples=300, n_features=2, n_informative=2,
                             n_redundant=0, n_classes=3, n_clusters_per_class=1,
                             random_state=3)

model = LogisticRegression(multi_class='multinomial', max_iter=1000)
model.fit(Xm, ym)

print("多分类模型的 coef_ 形状：", model.coef_.shape, "（3 个类 × 2 个特征）")
print("训练集准确率：", model.score(Xm, ym))

# 画决策边界（用网格染色）
xx = np.linspace(Xm[:, 0].min() - 1, Xm[:, 0].max() + 1, 300)
yy = np.linspace(Xm[:, 1].min() - 1, Xm[:, 1].max() + 1, 300)
XX, YY = np.meshgrid(xx, yy)
ZZ = model.predict(np.c_[XX.ravel(), YY.ravel()]).reshape(XX.shape)

fig, ax = plt.subplots(figsize=(7, 6))
ax.contourf(XX, YY, ZZ, alpha=0.3, cmap='viridis')
ax.scatter(Xm[:, 0], Xm[:, 1], c=ym, cmap='viridis', s=25, edgecolors='k', linewidths=0.5)
ax.set_xlabel('特征 x1'); ax.set_ylabel('特征 x2')
ax.set_title('多分类逻辑回归（softmax）：三块决策区域')
plt.tight_layout()
plt.show()

# 观察：三种颜色=三个类，背景色块=模型预测的类别区域，边界就是决策边界。
'''),
    ("markdown", r'''## 9.7 本章小结

| 概念 | 一句话直觉 |
| --- | --- |
| 逻辑回归 | 线性回归 + sigmoid，输出「属于正类的概率」 |
| sigmoid | $\sigma(z)=1/(1+e^{-z})$，把任意实数压到 [0,1] |
| 决策边界 | $w x + b = 0$ 那条线，两侧预测不同类别（线性） |
| 交叉熵 | 分类标准损失：错得越离谱，惩罚越狠 |
| OVR | 一对多：拆成 K 个二分类 |
| softmax | 多分类：分数 → 和为 1 的概率分布 |

🔑 **记忆**：分类用**交叉熵**（回归用 MSE）；sigmoid 是 softmax 在两类的特例；softmax 输出和为 1 的概率。

> 📌 **下一步**：第十章专门把**损失函数「全家桶」**（MSE/MAE/交叉熵/Hinge）横向对比，从更高的视角统一理解「损失函数」这个贯穿全书的概念。
'''),
]

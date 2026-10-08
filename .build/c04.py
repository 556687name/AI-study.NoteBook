# -*- coding: utf-8 -*-
CELLS = [
    ("markdown", r'''# 第四章 线性回归与正规方程

> 📌 **出处**：李宏毅 2026《机器学习》**第 4~9 讲**（线性回归基本概念 1/2、正规方程介绍、求解多元一次方程、sklearn 运算、带截距运算）
> ⭐ **40 天重点**：对应计划 Day16「逻辑回归 + 第一个模型」的前置内容。线性回归是**最基础、最经典的机器学习模型**，正规方程是「一步解出最优参数」的解析方法。

---

## 4.1 线性回归：最基础的机器学习模型

第一章讲过，**回归（Regression）** 是「输出一个连续数值」的任务。而**线性回归（Linear Regression）** 是最简单的回归模型——它假设输出 $y$ 是输入特征 $x$ 的**线性组合**。

### 一元线性回归（只有一个特征 $x$）

$$y = w \cdot x + b$$

- $w$ 是**权重（weight）**，即这条直线的**斜率**；
- $b$ 是**偏置（bias）**，即这条直线的**截距**（与 y 轴的交点）；
- 我们要做的，就是**从数据里学出最合适的 $w$ 和 $b$**。

### 多元线性回归（多个特征 $x_1, x_2, \dots, x_n$）

$$y = w_1 x_1 + w_2 x_2 + \cdots + w_n x_n + b = \mathbf{w}^\top \mathbf{x} + b$$

写成向量形式更简洁：$\mathbf{w}^\top \mathbf{x} = [w_1,\dots,w_n] \cdot [x_1,\dots,x_n]^\top$ 是权重和特征的点积。比如预测房价时，$x_1$ 是面积、$x_2$ 是地段评分、$x_3$ 是房龄……每个特征对应一个权重，权重的大小表示「这个特征对房价影响多大」。

> 💡 一句话：**线性回归 = 用一条直线（或超平面）去拟合数据，让「预测值」尽量接近「真实值」。**
'''),
    ("code", r'''# ---- 一元线性回归：直观感受"用直线拟合数据" ----
np.random.seed(4)
X6 = np.linspace(0, 1, 30)
真实w6, 真实b6 = 3.0, 0.5
y6 = 真实w6 * X6 + 真实b6 + np.random.randn(30) * 0.2

# 用 numpy 的 polyfit（内部就是最小二乘法/正规方程）拟一条 1 阶直线
w6, b6 = np.polyfit(X6, y6, 1)
print(f"学到的参数：w = {w6:.3f}（真实 {真实w6}），b = {b6:.3f}（真实 {真实b6}）")

fig, ax = plt.subplots(figsize=(7.5, 5))
ax.scatter(X6, y6, color=蓝, alpha=0.8, s=25, label='数据点')
ax.plot(X6, w6 * X6 + b6, color=橙, lw=2.5, label=f'拟合直线 y = {w6:.2f}x + {b6:.2f}')
ax.plot(X6, 真实w6 * X6 + 真实b6, color=灰, lw=1.5, ls='--', label='真实关系')
ax.set_xlabel('x'); ax.set_ylabel('y')
ax.set_title('线性回归：找一条"误差最小"的直线穿过数据')
ax.legend()
plt.tight_layout()
plt.show()
'''),
    ("markdown", r'''## 4.2 代价函数：给这条直线「打分」

怎么判断一条直线好不好？看它**预测值和真实值差多少**。这就是**代价函数（cost function）**，线性回归最常用的是**均方误差 MSE**：

$$J(w, b) = \frac{1}{m}\sum_{i=1}^{m}\big(\hat y_i - y_i\big)^2 = \frac{1}{m}\sum_{i=1}^{m}\big((w x_i + b) - y_i\big)^2$$

逐项看：

- $m$ 是样本数量；
- $\hat y_i = w x_i + b$ 是第 $i$ 个样本的**预测值**（代入当前参数算出来的）；
- $y_i$ 是第 $i$ 个样本的**真实值**；
- **平方**让误差恒为正，且「大误差」被惩罚得更狠（第一章 1.5 讲过）；
- 整个式子就是「所有样本误差平方的**平均值**」。

我们的目标很明确：**找到让 $J(w,b)$ 最小的一组 $(w, b)$**。

那么「怎么找最小值」？有两条路：

1. **正规方程（Normal Equation）**：直接套公式，**一步解出**最优参数（本讲主角，解析解）；
2. **梯度下降（Gradient Descent）**：迭代逼近（第五章主角，数值解）。

> 💡 关键点：$J(w,b)$ 是**凸函数**（像一口「碗」，只有一个最低点），所以最小值在「导数等于 0」的地方——这为正规方程提供了理论依据。
'''),
    ("code", r'''# ---- 代价函数 J(w,b) 是一口"碗"：最低点就是最优参数 ----
# 把 (w,b) 铺成网格，每个点算一次 MSE，画出代价函数的等高线/曲面。
def 代价(w, b):
    return np.mean((w * X6 + b - y6) ** 2)     # MSE

ws = np.linspace(0, 6, 100)
bs = np.linspace(-1, 2, 100)
W6, B6 = np.meshgrid(ws, bs)
Z6 = np.array([[代价(w, b) for w in ws] for b in bs])

fig, ax = plt.subplots(figsize=(7, 6))
c = ax.contourf(W6, B6, Z6, levels=30, cmap='Blues')
fig.colorbar(c, label='代价 J(w,b)')
ax.scatter(真实w6, 真实b6, color=红, s=90, zorder=5, label=f'最低点（真实参数 {真实w6},{真实b6}）')
ax.set_xlabel('w'); ax.set_ylabel('b')
ax.set_title('代价函数 J(w,b) 是凸的"碗"：只有一个最低点')
ax.legend()
plt.tight_layout()
plt.show()

# 看到红点（真实参数）正好落在"碗底"（颜色最深处），
# 说明"让代价最小"确实等价于"找回真实参数"。
'''),
    ("markdown", r'''## 4.3 正规方程（Normal Equation）：一步解出最优参数

因为代价函数 $J$ 是凸的，最小值在**导数等于 0** 的地方。我们可以直接对 $J$ 求导、令导数为 0，**解出解析解**——这个解就是**正规方程**：

$$\boldsymbol{\theta} = \big(\mathbf{X}^\top \mathbf{X}\big)^{-1} \mathbf{X}^\top \mathbf{y}$$

其中：

- $\mathbf{X}$ 是样本矩阵，形状 $(m, n)$：$m$ 个样本、$n$ 个特征；
- 通常会在 $\mathbf{X}$ 最左边**补一列全 1**，用来表示截距 $b$（这样 $b$ 也变成一个「权重」，统一处理）；
- $\boldsymbol{\theta}$ 是要求的所有参数（包含 $w$ 和 $b$），形状 $(n+1, 1)$；
- $(\cdot)^{-1}$ 是矩阵求逆。

### 推导直觉（不用死记，理解思路即可）

我们要解「让 $J$ 最小的 $\boldsymbol{\theta}$」。把预测写成矩阵形式 $\hat{\mathbf{y}} = \mathbf{X}\boldsymbol{\theta}$，我们的目标是让 $\hat{\mathbf{y}}$ 尽量接近 $\mathbf{y}$，即 $\mathbf{X}\boldsymbol{\theta} \approx \mathbf{y}$。

对 $J = \frac{1}{m}\|\mathbf{X}\boldsymbol{\theta} - \mathbf{y}\|^2$ 求关于 $\boldsymbol{\theta}$ 的梯度并令其为 0，经过推导（后面 4.4 节逐步展开）就得到上面的正规方程。它本质就是**最小二乘法（least squares）**的解。

### 正规方程 vs 梯度下降

| | 正规方程 | 梯度下降 |
| --- | --- | --- |
| 需要选学习率 | ❌ 不需要 | ✅ 需要 |
| 需要迭代 | ❌ 一步到位 | ✅ 多次迭代 |
| 特征很多时 | 求逆慢，复杂度约 $O(n^3)$ | 仍然可行 |
| 适用场景 | 特征少、样本少 | 特征多、大数据 |

> 💡 一句话：**正规方程 = 用线性代数「一步」解出线性回归的最优参数**，特征不多时最省事；特征一多（几万、几十万维），求逆太慢，就要改用梯度下降。
'''),
    ("markdown", r'''## 4.4 正规方程的推导（最小二乘法视角）

这一节把 4.3 的公式一步步推出来，帮助理解它「为什么长这样」。核心思想是**最小二乘**：让所有样本的误差平方和最小。

### 第一步：写成矩阵形式

假设有 $m$ 个样本、$n$ 个特征，把数据写成矩阵：

$$\mathbf{X} = \begin{bmatrix} 1 & x_1^{(1)} & \cdots & x_n^{(1)} \\ 1 & x_1^{(2)} & \cdots & x_n^{(2)} \\ \vdots & \vdots & \ddots & \vdots \\ 1 & x_1^{(m)} & \cdots & x_n^{(m)} \end{bmatrix},\quad \mathbf{y} = \begin{bmatrix} y^{(1)} \\ y^{(2)} \\ \vdots \\ y^{(m)} \end{bmatrix},\quad \boldsymbol{\theta} = \begin{bmatrix} b \\ w_1 \\ \vdots \\ w_n \end{bmatrix}$$

注意 $\mathbf{X}$ 最左边补了一列全 1，对应偏置 $b$。这样预测值就是 $\hat{\mathbf{y}} = \mathbf{X}\boldsymbol{\theta}$，误差向量是 $\mathbf{X}\boldsymbol{\theta} - \mathbf{y}$。

### 第二步：代价函数写成矩阵形式

$$J(\boldsymbol{\theta}) = \frac{1}{m}\big(\mathbf{X}\boldsymbol{\theta} - \mathbf{y}\big)^\top\big(\mathbf{X}\boldsymbol{\theta} - \mathbf{y}\big)$$

（右边就是「误差向量的平方和」的矩阵写法：一个列向量和自己做内积，等于各分量平方之和。）

### 第三步：对 $\boldsymbol{\theta}$ 求导，令为 0

利用矩阵求导公式 $\frac{\partial}{\partial \boldsymbol{\theta}}\|\mathbf{X}\boldsymbol{\theta} - \mathbf{y}\|^2 = 2\mathbf{X}^\top(\mathbf{X}\boldsymbol{\theta} - \mathbf{y})$，令其等于 0：

$$2\mathbf{X}^\top(\mathbf{X}\boldsymbol{\theta} - \mathbf{y}) = 0 \;\Longrightarrow\; \mathbf{X}^\top\mathbf{X}\boldsymbol{\theta} = \mathbf{X}^\top\mathbf{y}$$

### 第四步：解出 $\boldsymbol{\theta}$

两边同乘 $(\mathbf{X}^\top\mathbf{X})^{-1}$，得到：

$$\boldsymbol{\theta} = \big(\mathbf{X}^\top\mathbf{X}\big)^{-1}\mathbf{X}^\top\mathbf{y}$$

这就是正规方程。🔑 这个公式要能默写出来。
'''),
    ("code", r'''# ---- 用 numpy 从零实现正规方程：θ = (XᵀX)⁻¹ Xᵀ y ----
# 造一个"多元"线性数据，然后用正规方程一步解出所有参数。

np.random.seed(9)
m = 100
X_true = np.random.rand(m, 2)                  # 2 个特征
真实theta = np.array([1.5, -2.0])              # 真实的两个权重
真实b = 0.7
y_true = X_true @ 真实theta + 真实b + np.random.randn(m) * 0.1   # y = w1*x1 + w2*x2 + b + 噪声

# 关键：在 X 左边补一列全 1，用来表示截距 b
X_b = np.concatenate([np.ones((m, 1)), X_true], axis=1)   # 形状 (m, 3)

# 🔑 记忆：正规方程一步求解
theta_hat = np.linalg.inv(X_b.T @ X_b) @ X_b.T @ y_true   # θ = (XᵀX)⁻¹ Xᵀ y

print("正规方程解出的参数：")
print(f"  截距 b  = {theta_hat[0]:.3f}  （真实 {真实b}）")
print(f"  权重 w1 = {theta_hat[1]:.3f}  （真实 {真实theta[0]}）")
print(f"  权重 w2 = {theta_hat[2]:.3f}  （真实 {真实theta[1]}）")

# 验证：用解出的参数预测，和真实值对比
y_pred = X_b @ theta_hat
print(f"\n均方误差 MSE = {np.mean((y_pred - y_true) ** 2):.5f}（很小，说明解得很准）")
'''),
    ("markdown", r'''## 4.5 sklearn 实战：LinearRegression（第八、九讲）

实际开发中不用手写正规方程，`sklearn` 已经封装好了。两个关键点：

- **`LinearRegression()`**：默认 `fit_intercept=True`，**自动带截距**（相当于自动帮你补全 1 列）；
- **`fit_intercept=False`**：强制过原点（$b=0$），用于「理论上 $y$ 必须经过 0」的场景。

训练完 `fit(X, y)` 之后，可以：

- `.coef_` 查看权重 $w$；
- `.intercept_` 查看截距 $b$；
- `.predict(X)` 做预测；
- `.score(X, y)` 算 $R^2$（拟合优度，越接近 1 越好，1 表示完美拟合）。

> 💡 注意：`fit_intercept=True` 时，**不需要**手动往 X 里补全 1 列，sklearn 会自动处理；但如果你已经手动补了全 1 列，就应该设 `fit_intercept=False`，否则会重复算截距。
'''),
    ("code", r'''# ---- sklearn 的 LinearRegression：带截距 vs 不带截距 ----
from sklearn.linear_model import LinearRegression as LR

# ① 默认：自动带截距（内部自动补全 1 列）
model1 = LR()                       # fit_intercept=True（默认）
model1.fit(X_true, y_true)          # 直接喂原始特征，不需要手动补 1
print("① 带截距（默认）：")
print(f"   截距 intercept = {model1.intercept_:.3f}  （真实 {真实b}）")
print(f"   权重 coef_     = {np.round(model1.coef_, 3)}  （真实 {真实theta}）")

# ② 手动补了全 1 列，就要关掉自动截距
model2 = LR(fit_intercept=False)
model2.fit(X_b, y_true)             # 喂的 X 已经含全 1 列
print("\n② 手动补 1 列 + 关截距：")
print(f"   参数 = {np.round(model2.coef_, 3)}  （第一个是截距，后两个是权重）")

# ③ 强制过原点（b=0）
model3 = LR(fit_intercept=False)
model3.fit(X_true, y_true)
print("\n③ 强制过原点（b=0）：")
print(f"   权重 = {np.round(model3.coef_, 3)}  （没有截距）")

# 用 ① 的模型算 R² 评分
print(f"\n模型①的 R² = {model1.score(X_true, y_true):.4f}（越接近 1 越好）")
'''),
    ("markdown", r'''## 4.6 本章小结

| 概念 | 一句话直觉 |
| --- | --- |
| 线性回归 | 用直线（超平面）拟合数据，输出连续数值 |
| 假设函数 | $y = \mathbf{w}^\top\mathbf{x} + b$，待学的参数是 $w$ 和 $b$ |
| 代价函数 MSE | 预测值和真实值差的平方的平均，越小越好 |
| 正规方程 | $\boldsymbol{\theta}=(X^\top X)^{-1}X^\top y$，一步解出最优参数 |
| sklearn | `LinearRegression(fit_intercept=...)` 一行搞定线性回归 |

🔑 **记忆**：正规方程公式 $\boldsymbol{\theta} = (\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{y}$；`LinearRegression` 默认带截距、不需要手动补 1 列。

> 📌 **下一步**：第五章讲梯度下降（数值解），把正规方程的「解析解」和梯度下降的「数值解」真正对应起来。
'''),
]

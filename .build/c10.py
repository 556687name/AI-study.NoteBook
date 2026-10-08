# -*- coding: utf-8 -*-
CELLS = [
    ("markdown", r'''# 第十章 损失函数全家桶

> 📌 **出处**：李宏毅 2026《机器学习》**损失函数**专题（均方误差 MSE、平均绝对误差 MAE、交叉熵 Cross Entropy、分类问题的损失、Hinge Loss）
> ⭐ **40 天重点**：对应计划 Day11「损失函数」。前面几章已经零散遇到 MSE、交叉熵，这一章把它们**放回同一条线索**上，从「损失函数到底是什么、怎么选」的视角统一梳理。

---

## 10.1 损失函数：模型和优化器之间的「裁判」

回顾训练三步曲：模型 → 损失 → 优化。**损失函数（loss function）** 是中间的「裁判」，它给「模型预测得有多差」打一个分数，优化器再根据这个分数去改参数。

一个损失函数好不好，关键看两点：

1. **能不能正确反映「误差」**：错得越离谱，分数应该越高（惩罚越重）；
2. **好不好优化**：它的梯度（导数）是否稳定、能否引导参数走向更好的解。

不同任务需要不同「裁判」，于是有了下面这些主流损失函数。选择的第一原则很简单：

> 🔑 **回归任务 → MSE / MAE；分类任务 → 交叉熵 / Hinge。** 这是最核心的对应关系，先记住它，再理解每个的细节。

---

## 10.2 MSE（均方误差）：回归任务的老朋友

**均方误差（Mean Squared Error）** 已经用过很多次：

$$L_{\text{MSE}} = \frac{1}{m}\sum_{i=1}^{m}\big(\hat y_i - y_i\big)^2$$

- **优点**：数学性质好（可导、凸、处处光滑），梯度随误差线性增长，方便梯度下降；
- **缺点**：因为用了**平方**，对**离群点（outlier）极度敏感**——一个离群点的误差平方后会被放大得不成比例，把整条拟合线「拽偏」。

### 为什么平方对离群点敏感？

误差 2 的平方是 4，误差 10 的平方是 100——误差扩大 5 倍，惩罚扩大 25 倍。所以模型会「拼命去迁就」那个离群点，牺牲对大多数正常点的拟合。

> 💡 适用场景：数据**噪声符合正态分布、没有明显离群点**时，MSE 是最优选择（它是「正态噪声下最大似然」的自然结果）。
'''),
    ("markdown", r'''## 10.3 MAE（平均绝对误差）：对离群点更稳健

**平均绝对误差（Mean Absolute Error）** 把平方换成绝对值：

$$L_{\text{MAE}} = \frac{1}{m}\sum_{i=1}^{m}\big|\hat y_i - y_i\big|$$

- **优点**：离群点不会被「平方放大」，模型更**稳健（robust）**，不容易被少数极端值带偏；
- **缺点**：在 $y_i = \hat y_i$ 处**不可导**（绝对值尖点），且梯度是「常数」（不是随误差变大），优化时不如 MSE 平滑。

### 对比：MSE 放大离群点，MAE 一视同仁

误差 10 时，MSE 惩罚 100，MAE 惩罚 10——MSE 对「大误差」惩罚是平方级的，MAE 是线性级的。所以：**有离群点用 MAE，数据干净用 MSE**。
'''),
    ("code", r'''# ---- MSE vs MAE：对离群点的敏感度对比 ----
# 造一条接近直线的数据，故意混入一个离群点，看两种损失拟合的直线差多少。
np.random.seed(11)
Xe = np.linspace(0, 10, 30)
ye = 2 * Xe + 1 + np.random.randn(30) * 1.5
# 混入一个离群点
Xe = np.append(Xe, [9.5]); ye = np.append(ye, [-20])   # 明显偏离正常趋势的点

from sklearn.linear_model import LinearRegression

def 拟合_MAE(Xe, ye, lr=0.01, 步数=2000):
    """用次梯度下降拟合 y = w·x + b，损失用 MAE（|误差|）。"""
    w, b = 0.0, 0.0
    for _ in range(步数):
        残差 = w * Xe + b - ye
        # MAE 在残差=0 处不可导，用次梯度 sign(残差)
        gw = np.mean(np.sign(残差) * Xe)
        gb = np.mean(np.sign(残差))
        w -= lr * gw
        b -= lr * gb
    return w, b

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
for ax, 损失, t in zip(axes, ['squared_error', 'absolute_error'],
                       ['MSE 拟合（被离群点拽偏）', 'MAE 拟合（对离群点稳健）']):
    if 损失 == 'squared_error':
        # 默认 LinearRegression 就是最小二乘 = MSE
        m = LinearRegression()
        m.fit(Xe.reshape(-1, 1), ye)
        w, b = m.coef_[0], m.intercept_
    else:
        # 手动用 MAE 损失拟合
        w, b = 拟合_MAE(Xe, ye)
    ax.scatter(Xe[:-1], ye[:-1], color=蓝, s=20, alpha=0.8, label='正常数据')
    ax.scatter([Xe[-1]], [ye[-1]], color=红, s=90, zorder=5, label='离群点')
    xs = np.linspace(0, 10, 50)
    ax.plot(xs, w * xs + b, color=橙, lw=2.5, label=f'拟合线 y={w:.2f}x+{b:.2f}')
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_title(t, fontsize=12)
    ax.legend(fontsize=9)
plt.suptitle('MSE 被离群点"平方放大"拽偏，MAE 更能守住正常趋势', fontsize=13)
plt.tight_layout()
plt.show()

# 观察：左图（MSE）拟合线明显向离群点倾斜；右图（MAE）拟合线更贴近正常数据。
'''),
    ("markdown", r'''## 10.4 交叉熵（Cross Entropy）：分类任务的标准损失

交叉熵是**分类任务的标准损失**（第九章已细讲）。二分类形式：

$$L = -\frac{1}{m}\sum_{i=1}^{m}\Big[\, y_i \log \hat y_i + (1 - y_i)\log(1 - \hat y_i)\Big]$$

多分类（配合 softmax）形式：

$$L = -\frac{1}{m}\sum_{i=1}^{m}\sum_{k=1}^{K} y_{ik} \log \hat y_{ik}$$

核心思想：**让「真实类别的预测概率」尽可能大**，等价于让「负对数概率」尽可能小。

> 💡 **为什么交叉熵适合分类、MSE 不适合？** 第九章说过：因为分类的预测是「概率」，交叉熵在「自信地犯错」时惩罚是无穷大（$-\log 0 \to \infty$），能狠狠纠正大错误；而 MSE 配合 sigmoid 会产生非凸曲面、且「错得越狠梯度越小」，反而学不动。所以：**回归用 MSE/MAE，分类用交叉熵**，这是实践中最重要的一条经验。
'''),
    ("markdown", r'''## 10.5 Hinge Loss（合页损失）：SVM 的损失

**Hinge Loss（合页损失）** 是支持向量机 SVM 的经典损失，专为**二分类（标签 $y \in \{-1, +1\}$）**设计：

$$L_{\text{hinge}} = \max\big(0,\; 1 - y_i \cdot \hat y_i\big)$$

理解它：

- $\hat y_i$ 是模型的「分数」（不是概率），$y_i$ 是真实标签（+1 或 -1）；
- 当预测**正确且足够自信**（$y_i \cdot \hat y_i \ge 1$）时，损失为 0——「已经对了，不再惩罚」；
- 当预测错误，或「对是对了但不够自信」（$y_i \cdot \hat y_i < 1$）时，损失随「不自信程度」线性增长。

和交叉熵的对比：

- 交叉熵：即使已经分对了，只要概率不是 1，就会继续「逼」模型更自信；
- Hinge：分对且过了一个「安全距离」（$y_i\hat y_i \ge 1$）就**撒手不管**（损失 0），只关心「有没有分对、分对得够不够远」，不追求极致概率。

> 💡 这是 SVM「最大间隔」思想的体现：Hinge Loss 鼓励模型把两类数据分得**尽量远**（大间隔），而不是只追求概率接近 1。
'''),
    ("code", r'''# ---- 各种损失函数的曲线对比 ----
# 假设真实标签 y=1，画"预测值 → 损失"的曲线，横向对比四种损失。
预测 = np.linspace(-3, 3, 500)

MSE曲线 = (预测 - 1) ** 2
MAE曲线 = np.abs(预测 - 1)
# 交叉熵（真实 y=1，先过 sigmoid 得到概率）
p = 1 / (1 + np.exp(-预测))
交叉熵曲线 = -np.log(np.clip(p, 1e-8, 1))
# Hinge（真实 y=+1，直接算 max(0, 1 - y·ŷ)）
Hinge曲线 = np.maximum(0, 1 - 预测)

fig, axes = plt.subplots(2, 2, figsize=(12, 9))
for ax, y值, name, c in zip(axes.ravel(),
                            [MSE曲线, MAE曲线, 交叉熵曲线, Hinge曲线],
                            ['MSE（回归）', 'MAE（回归）', '交叉熵（分类）', 'Hinge（SVM 分类）'],
                            [蓝, 绿, 红, 紫]):
    ax.plot(预测, y值, color=c, lw=2.5)
    ax.axvline(1, color=灰, ls='--', lw=1, label='真实值/正确预测')
    ax.set_xlabel('预测值'); ax.set_ylabel('损失')
    ax.set_title(name, fontsize=12); ax.grid(alpha=0.3); ax.legend(fontsize=9)
plt.suptitle('四大损失函数曲线（真实 y=1）', fontsize=14)
plt.tight_layout()
plt.show()

# 观察各自形状：
# MSE 是抛物线、MAE 是 V 形（尖点在 0，不可导）、
# 交叉熵在"预测接近 0"时冲向无穷、Hinge 在"预测≥1"后为 0。
'''),
    ("markdown", r'''## 10.6 怎么选：一张表记住

| 任务 | 推荐损失 | 一句话理由 |
| --- | --- | --- |
| 回归（数据干净） | **MSE** | 光滑、可导，正态噪声下最优 |
| 回归（有离群点） | **MAE** | 不平方放大离群点，稳健 |
| 二分类 | **交叉熵** | 概率语义天然匹配，惩罚自信犯错 |
| 多分类 | **交叉熵 + softmax** | 输出 K 类概率分布 |
| 分类（最大间隔） | **Hinge** | 分对够远就撒手，SVM 思想 |

补充两个常听到的「折中」损失（了解即可）：

- **Huber Loss**：MSE 和 MAE 的折中——误差小用平方（光滑），误差大用线性（抗离群点），两边的好处都要；
- **Focal Loss**：交叉熵的改进，专门解决「正负样本极不平衡」的分类问题，给「难分的样本」更高权重（第十九章大模型里也会遇到类似思想）。

> 🔑 **记忆**：回归 MSE/MAE，分类交叉熵/Hinge。损失函数贯穿全书——后面神经网络（第十一章）、PyTorch（第十六章）里，每一处「训练」都绕不开它。
'''),
    ("markdown", r'''## 10.7 本章小结

这一章把前面散落的损失函数串成了一条线：

1. **损失函数是「裁判」**，衡量预测有多差，引导优化方向；
2. **回归用 MSE/MAE**：MSE 光滑但怕离群点，MAE 稳健但在 0 点不可导；
3. **分类用交叉熵/Hinge**：交叉熵求「概率准」，Hinge 求「分得远」；
4. 选损失的第一原则：**看任务类型**（回归 vs 分类），再看数据特性（有没有离群点）。

> 📌 **下一步**：第十一章进入**深度学习**——讲**神经网络与反向传播**。到这里为止我们都是「单个模型」；从下一章起，把模型「叠起来」，进入深度学习的核心。
'''),
]

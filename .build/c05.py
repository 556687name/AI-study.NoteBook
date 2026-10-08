# -*- coding: utf-8 -*-
CELLS = [
    ("markdown", r'''# 第五章 梯度下降

> 📌 **出处**：李宏毅 2026《机器学习》**第 10~17 讲**（梯度下降专题：概念 → 代码 → 可视化 → BGD/SGD/MBGD → 学习率/特征缩放/动量）
> ⭐ **40 天重点**：对应计划 Day11「最优化基础」——*梯度下降及其变体、动量法、Adam 优化器原理*。这一章把第一章「梯度下降」的直觉，落地成能真正跑起来的算法，并系统讲解三种变体和两个关键技巧（特征缩放、动量）。

---

## 5.1 回顾：梯度下降到底在做什么

第一章 1.6 建立了直觉，这里先快速回顾并补齐细节。梯度下降的更新公式：

$$\theta \leftarrow \theta - \eta \cdot \nabla L(\theta)$$

- $\theta$：要优化的参数（如 $w, b$）；
- $\nabla L(\theta)$：损失对参数的**梯度**（指向损失上升最快的方向）；
- $\eta$：**学习率**，控制步长。

对一元线性回归 $y = wx + b$、损失 MSE，可以手推两个偏导（🔑 要会推）：

$$\frac{\partial L}{\partial w} = \frac{2}{m}\sum_{i=1}^{m}(\hat y_i - y_i)\,x_i, \qquad \frac{\partial L}{\partial b} = \frac{2}{m}\sum_{i=1}^{m}(\hat y_i - y_i)$$

> 💡 **停止条件**：理论上梯度 = 0 时到最低点，但实际几乎不会正好等于 0，通常**人为设定迭代次数**或「误差小于某个阈值」就停。
'''),
    ("code", r'''# ---- 从零实现梯度下降：求解一元线性回归 y = w·x + b ----
# 把第一章的"三步曲 + 梯度下降"重新完整走一遍，并记录收敛过程。
np.random.seed(10)
X7 = np.linspace(0, 1, 60)
y7 = 2.0 * X7 + 1.0 + np.random.randn(60) * 0.15     # 真实 w=2, b=1

def 损失7(w, b):
    return np.mean((w * X7 + b - y7) ** 2)

# 梯度下降（普通批量版 BGD）
w, b = 0.0, 0.0
lr = 0.3
历史 = []                       # 记录每一步的 (w, b, 损失)
for step in range(200):
    历史.append((w, b, 损失7(w, b)))
    y_pred = w * X7 + b
    dw = np.mean(2 * (y_pred - y7) * X7)    # ∂L/∂w
    db = np.mean(2 * (y_pred - y7))         # ∂L/∂b
    w -= lr * dw
    b -= lr * db
历史.append((w, b, 损失7(w, b)))

print(f"结果：w = {w:.4f}（真实 2），b = {b:.4f}（真实 1），损失 = {损失7(w,b):.5f}")

# 可视化收敛曲线
hist = np.array(历史)
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].plot(hist[:, 2], color=橙, lw=2)
axes[0].set_xlabel('迭代步数'); axes[0].set_ylabel('损失 L')
axes[0].set_title('损失随迭代下降（先快后慢）')
axes[0].grid(alpha=0.3)

axes[1].scatter(X7, y7, color=蓝, s=20, alpha=0.8, label='数据')
axes[1].plot(X7, w * X7 + b, color=橙, lw=2.5, label=f'拟合 y={w:.2f}x+{b:.2f}')
axes[1].plot(X7, 2 * X7 + 1, color=灰, lw=1.5, ls='--', label='真实 y=2x+1')
axes[1].set_xlabel('x'); axes[1].set_ylabel('y'); axes[1].legend(fontsize=9)
axes[1].set_title('学到的直线 vs 真实关系')
plt.tight_layout()
plt.show()

# 左图注意：损失一开始掉得飞快（坡度大），越到后面越平缓（逼近谷底、梯度变小）。
'''),
    ("markdown", r'''## 5.2 三种梯度下降：BGD / SGD / MBGD

梯度下降有一个关键变体问题：**每次更新参数时，用多少条数据来算梯度？** 据此分成三种：

| 方法 | 一次更新用多少数据 | 优点 | 缺点 |
| --- | --- | --- | --- |
| **BGD 批量梯度下降** | **全部**样本 | 梯度稳、方向准 | 每次都要扫全量数据，慢 |
| **SGD 随机梯度下降** | **1 条**样本 | 快、能逃离局部最小 | 梯度抖、方向乱 |
| **MBGD 小批量梯度下降** | **一小批**（如 32/64） | 折中：稳又快 | 要选 batch size |

### 更新公式对比（设 $\hat y_i = w x_i + b$）

- **BGD**：用全部 $m$ 条数据求平均梯度

  $$w \leftarrow w - \eta\,\frac{2}{m}\sum_{i=1}^{m}(\hat y_i - y_i)\,x_i$$

- **SGD**：每次随机抽 **1 条** $i$ 更新

  $$w \leftarrow w - \eta \cdot 2(\hat y_i - y_i)\,x_i$$

- **MBGD**：每次随机抽**一小批** $B$ 更新

  $$w \leftarrow w - \eta\,\frac{2}{|B|}\sum_{i \in B}(\hat y_i - y_i)\,x_i$$

### 为什么 SGD 能「逃离局部最小」？

BGD 用全量数据算梯度，方向非常「稳」，但也容易一头扎进某个局部最低点出不来。SGD 每次只用一条数据，梯度里带着这条数据的「随机性」——方向有点「抖」，反而有机会从局部最小的坑里「抖」出来。但也因为抖，SGD 收敛到最后会围着最优解来回震荡，不如 BGD 稳。

> 💡 实际深度学习里几乎都用 **MBGD**（PyTorch 里叫 mini-batch SGD）。注意：很多论文里的 "SGD" 其实泛指「小批量随机梯度下降」。
'''),
    ("code", r'''# ---- 三种梯度下降对比：BGD / SGD / MBGD 的收敛轨迹 ----
# 用同一个损失曲面，对比三种方法的收敛路径。
def 计算梯度(w, b, X_batch, y_batch):
    y_pred = w * X_batch + b
    dw = np.mean(2 * (y_pred - y_batch) * X_batch)
    db = np.mean(2 * (y_pred - y_batch))
    return dw, db

def 跑梯度下降(方法, lr, 步数=40, batch=8):
    w, b = 0.0, 0.0
    轨 = [(w, b)]
    idx = np.arange(len(X7))
    for _ in range(步数):
        if 方法 == 'BGD':
            dw, db = 计算梯度(w, b, X7, y7)              # 全量
        elif 方法 == 'SGD':
            i = np.random.randint(len(X7))               # 随机 1 条
            dw, db = 计算梯度(w, b, X7[i:i+1], y7[i:i+1])
        else:  # MBGD
            b_idx = np.random.choice(idx, batch, replace=False)   # 随机一小批
            dw, db = 计算梯度(w, b, X7[b_idx], y7[b_idx])
        w -= lr * dw; b -= lr * db
        轨.append((w, b))
    return np.array(轨)

# 造损失曲面（复用 X7/y7）
ws7 = np.linspace(-1, 5, 80); bs7 = np.linspace(-2, 4, 80)
W7, B7 = np.meshgrid(ws7, bs7)
Z7 = np.array([[损失7(w, b) for w in ws7] for b in bs7])

fig, axes = plt.subplots(1, 3, figsize=(16, 4.6))
for ax, 方法, t in zip(axes, ['BGD', 'SGD', 'MBGD'],
                       ['BGD：用全部数据，轨迹平滑', 'SGD：每次 1 条，轨迹抖动', 'MBGD：一小批，折中']):
    轨 = 跑梯度下降(方法, 0.3, 40)
    ax.contourf(W7, B7, Z7, levels=25, cmap='Blues')
    ax.plot(轨[:, 0], 轨[:, 1], 'o-', color=橙, lw=1.2, ms=2.5)
    ax.scatter(*轨[-1], color=红, s=60, zorder=5)
    ax.set_title(t, fontsize=10)
    ax.set_xlabel('w'); ax.set_ylabel('b')
plt.tight_layout()
plt.show()

# 观察：BGD 轨迹平滑直达谷底；SGD 轨迹弯弯曲曲（每条数据的方向不同）；MBGD 介于两者之间。
'''),
    ("markdown", r'''## 5.3 学习率与特征缩放：让梯度下降「快而稳」的两个关键

### 学习率 $\eta$ 的影响（第一章已演示，这里补一个实用经验）

学习率太小「蚂蚁爬」，太大「青蛙乱跳」甚至发散（第一章 1.7 有图）。一个实用观察是：收敛过程中损失往往**先快后慢**，并可能在最优解附近**来回震荡**（尤其 SGD/MBGD）。

### 特征缩放（Feature Scaling）：为什么梯度下降需要它

如果特征的**量纲差别很大**（比如「面积 100 平米」vs「房间数 3 间」），会发生一件坏事：**损失曲面变成一个又窄又长的「碗」**。

- 大尺度特征方向曲率很大（梯度很大），小尺度特征方向曲率很小（梯度很小）；
- 一个学习率顾得了这头就顾不了那头——用小学习率，大尺度方向走不动；用大学习率，小尺度方向直接飞出碗；
- 结果：**小尺度特征几乎学不到**，收敛极慢。

**特征缩放**就是把所有特征缩到相近的范围，让损失曲面变「圆」，一个学习率就能同时照顾所有方向。

两种常见方法（第七章特征工程会详细展开）：

- **Min-Max 归一化**：$x' = \dfrac{x - \min}{\max - \min}$，缩到 $[0, 1]$；
- **标准化（Z-Score）**：$x' = \dfrac{x - \mu}{\sigma}$，变成均值 0、标准差 1（**最常用**）。
'''),
    ("code", r'''# ---- 特征缩放：为什么梯度下降需要它 ----
# 造一个"面积(大数值)"和"房间数(小数值)"量纲悬殊的例子，对比缩放前后的损失曲面形状。
np.random.seed(12)
面积 = np.random.rand(50) * 100        # 面积：0 ~ 100（大数值）
房间数 = np.random.rand(50) * 4        # 房间数：0 ~ 4（小数值）
房价 = 面积 * 2 + 房间数 * 10 + np.random.randn(50) * 5

X_raw = np.c_[面积, 房间数]            # 原始特征：量纲悬殊

def 损失二维(w1, w2, Xm, ym):
    return np.mean((Xm @ np.array([w1, w2]) - ym) ** 2)

# 标准化（Z-Score）：(x - 均值) / 标准差
mu = X_raw.mean(axis=0); sigma = X_raw.std(axis=0)
X_scale = (X_raw - mu) / sigma

fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
for ax, Xm, t in zip(axes, [X_raw, X_scale], ['缩放前：窄长的碗（难训练）', '缩放后：圆润的碗（好训练）']):
    w1s = np.linspace(-30, 30, 60) if Xm is X_raw else np.linspace(-5, 5, 60)
    w2s = np.linspace(-30, 30, 60) if Xm is X_raw else np.linspace(-5, 5, 60)
    WW1, WW2 = np.meshgrid(w1s, w2s)
    ZZ = np.array([[损失二维(w1, w2, Xm, 房价) for w1 in w1s] for w2 in w2s])
    ax.contourf(WW1, WW2, ZZ, levels=25, cmap='Blues')
    ax.set_title(t, fontsize=11)
    ax.set_xlabel('w1（面积权重）'); ax.set_ylabel('w2（房间数权重）')
plt.tight_layout()
plt.show()

# 左图（缩放前）：等高线是"又窄又长"的椭圆，梯度下降会在窄方向上震荡、宽方向上爬不动；
# 右图（缩放后）：等高线接近"圆"，梯度下降能又快又稳地直达中心。
'''),
    ("markdown", r'''## 5.4 动量 Momentum：给梯度下降「带上惯性」

普通梯度下降只看「当前梯度」。如果损失曲面有**平坦区**（梯度很小，几乎不动）或**窄长谷**（来回震荡），收敛会很慢。**动量（Momentum）** 给更新「带上惯性」，像球滚下山，能更快冲过平坦区、减少震荡：

$$v \leftarrow \gamma\, v + \eta\,\nabla L(\theta), \qquad \theta \leftarrow \theta - v$$

- $v$ 是「速度」，累积了**历史梯度**，$v$ 初始为 0；
- $\gamma$ 是**动量系数**（通常取 0.9），控制「保留多少上一次的方向」；
- 更新时**参考了之前的方向**：震荡方向（正负来回）会被抵消，一致方向会被加速。

直觉：就像从山上滚下来的球——它滚的方向不仅由当前坡度决定，还带着之前的「惯性」。遇到平坦区，惯性会带着它继续往前冲；在窄谷里震荡时，惯性会把来回的晃动「抹平」。

> 📌 **出处**：Momentum 是 **Adam** 等现代优化器的基础。第六章「Batch 与优化器」会讲 Momentum 之上的完整优化器家族（AdaGrad / RMSProp / Adam）。
'''),
    ("code", r'''# ---- 动量 vs 普通梯度下降：谁更快冲过"窄长谷" ----
# 用一个狭长的损失函数，对比普通 GD 和带动量的 GD 的收敛速度。
def 窄长损失(w, b):
    return 0.05 * w**2 + 5 * b**2      # w 方向平缓（系数小）、b 方向陡峭（系数大）→ 窄长谷

def 跑(带动量, lr=0.05, 动量系数=0.9, 步数=40):
    w, b = -5.0, 3.0
    vw, vb = 0.0, 0.0
    轨 = [(w, b)]
    for _ in range(步数):
        gw, gb = 0.1 * w, 10 * b          # 梯度：∂L/∂w = 0.1w，∂L/∂b = 10b
        if 带动量:
            vw = 动量系数 * vw + lr * gw   # 累积速度
            vb = 动量系数 * vb + lr * gb
            w -= vw; b -= vb               # 用速度更新
        else:
            w -= lr * gw; b -= lr * gb     # 普通 GD
        轨.append((w, b))
    return np.array(轨)

轨_普通 = 跑(False, lr=0.05, 步数=40)
轨_动量 = 跑(True, lr=0.05, 步数=40)

ww = np.linspace(-8, 8, 100); bb = np.linspace(-8, 8, 100)
WW, BB = np.meshgrid(ww, bb)
ZZ = 0.05 * WW**2 + 5 * BB**2

fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
for ax, 轨, t in zip(axes, [轨_普通, 轨_动量], ['普通梯度下降', '动量 Momentum（γ=0.9）']):
    ax.contourf(WW, BB, ZZ, levels=30, cmap='Blues')
    ax.plot(轨[:, 0], 轨[:, 1], 'o-', color=橙, lw=1.3, ms=3)
    ax.scatter(*轨[-1], color=红, s=80, zorder=5, label='终点')
    ax.set_title(t, fontsize=12)
    ax.set_xlabel('w'); ax.set_ylabel('b'); ax.legend()
plt.tight_layout()
plt.show()

# 观察：普通 GD 在窄长谷里"之字形"震荡、前进缓慢；动量累积了往左的速度，震荡被抵消，更快冲到中心。
'''),
    ("markdown", r'''## 5.5 本章小结

| 概念 | 一句话直觉 |
| --- | --- |
| 梯度下降 | 每次朝负梯度方向走一小步，逼近最优解 |
| BGD / SGD / MBGD | 一次更新用全部 / 1 条 / 一小批数据 |
| 学习率 | 步长：太小慢、太大发散 |
| 特征缩放 | 把特征缩到同量级，让损失曲面变「圆」，收敛更快 |
| 动量 Momentum | 带惯性下坡，冲过平坦区、减少震荡 |

🔑 **记忆**：三种梯度下降的更新公式（5.2 节表格）；特征缩放的 Z-Score 公式 $x'=(x-\mu)/\sigma$；动量公式 $v \leftarrow \gamma v + \eta\nabla L$。

> 📌 **下一步**：第六章讲 **Batch 与优化器**——batch size 怎么选、Momentum 之上的自适应学习率（AdaGrad/RMSProp/Adam）、以及「局部最小值 vs 鞍点」的真相。
'''),
]

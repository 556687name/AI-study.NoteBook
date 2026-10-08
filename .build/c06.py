# -*- coding: utf-8 -*-
CELLS = [
    ("markdown", r'''# 第六章 Batch 与优化器

> 📌 **出处**：李宏毅 2026《机器学习》**第 22~35 讲**（批次 batch 与动量 momentum、自动调整学习速率、局部最小值与鞍点）
> ⭐ **40 天重点**：对应计划 Day11「最优化基础」——*动量法、Adam 优化器原理*。这一章把梯度下降升级成「现代优化器」，讲清楚 batch size 怎么选、学习率怎么自动调、以及「卡在局部最小」这个担忧到底成不成立。

---

## 6.1 Batch Size：一次更新用多少数据，影响的不只是速度

第五章讲过 BGD/SGD/MBGD 的区别是「一次用多少数据」。这个「多少」就是 **batch size（批大小）**。这一节深入它带来的**三种影响**。

### ① 训练速度（一次更新耗时）

直觉上「batch 越大一次更新越慢」，但在有 GPU 的现代环境里没那么简单：

- **大 batch**：每次算梯度要扫很多数据，单次更新慢；但 GPU 擅长**并行**，一次算 1000 条的梯度和算 1 条的耗时差不多（并行度上来了），所以**总耗时未必更大**；
- **小 batch**：单次更新快，但要更新很多次才能看完全部数据。

> 结论：在 GPU 上，「大 batch 慢、小 batch 快」这个直觉**不总是成立**，因为大 batch 能充分利用并行。真正决定速度的往往是别的因素。

### ② 收敛稳定性与噪声

- **大 batch**：梯度是「大量数据的平均」，噪声小、方向稳，收敛平稳；
- **小 batch**：梯度噪声大、方向抖，收敛过程「吵吵闹闹」。

### ③ 泛化能力（这是最反直觉、也最重要的一点）

研究发现：**小 batch 训练出来的模型，泛化能力往往更好**（在测试集上表现更佳），而大 batch 容易「泛化差」。一个被普遍接受的解释是：小 batch 的梯度噪声像一种「隐式正则化」，让模型不容易卡在尖锐的、泛化差的解里；大 batch 走得太「顺」，容易停在尖锐的最优点。

> 💡 实用建议：batch size 是一个**要调的超参数**，常见取值 32、64、128、256。没有「越大越好」或「越小越好」，要看具体任务，通常在小 batch 上更容易得到好结果，但要用并行补偿速度。
'''),
    ("code", r'''# ---- Batch Size 对收敛的影响：不同 batch size 的损失曲线对比 ----
# 用同一个线性回归问题，对比 batch size = 1 / 8 / 全量 的收敛过程。
np.random.seed(20)
X8 = np.linspace(0, 1, 100)
y8 = 3.0 * X8 + 0.5 + np.random.randn(100) * 0.3

def 损失8(w, b):
    return np.mean((w * X8 + b - y8) ** 2)

def 梯度8(w, b, idx):
    y_pred = w * X8[idx] + b
    return np.mean(2 * (y_pred - y8[idx]) * X8[idx]), np.mean(2 * (y_pred - y8[idx]))

def 跑_batch(batch_size, lr=0.3, 轮数=30):
    """每个 epoch 用 batch_size 的 mini-batch 扫一遍数据，记录损失。"""
    w, b = 0.0, 0.0
    曲线 = []
    idx = np.arange(len(X8))
    for _ in range(轮数):
        np.random.shuffle(idx)                  # 每轮先打乱
        for start in range(0, len(X8), batch_size):
            batch_idx = idx[start:start + batch_size]
            dw, db = 梯度8(w, b, batch_idx)
            w -= lr * dw; b -= lr * db
        曲线.append(损失8(w, b))
    return 曲线

fig, ax = plt.subplots(figsize=(9, 5.5))
for bs, c, name in [(1, 橙, 'batch=1（SGD）'), (8, 绿, 'batch=8'), (100, 蓝, 'batch=100（BGD）')]:
    曲线 = 跑_batch(bs, lr=0.3, 轮数=30)
    ax.plot(曲线, color=c, lw=2, label=name)
ax.set_xlabel('epoch（扫过多少轮数据）'); ax.set_ylabel('损失 L')
ax.set_title('不同 batch size 的收敛曲线')
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# 观察：batch=1 抖动明显但收敛快；batch=100 平滑；batch=8 折中。
'''),
    ("markdown", r'''## 6.2 局部最小值 vs 鞍点：深度学习真正怕的是哪一个？

第一章提过梯度下降的两个隐患：**局部最小值**和**鞍点**。这一节揭示一个颠覆常识的结论。

### 先分清这两个概念

梯度 $\nabla L = 0$ 的点，统称「临界点（critical point）」。但临界点有三种：

- **局部最小值（local minimum）**：四周都比它高，真「坑底」；
- **局部最大值（local maximum）**：四周都比它低（少见，不关心）；
- **鞍点（saddle point）**：马鞍形——沿某些方向是「谷」（下坡），沿另一些方向是「峰」（上坡）。梯度为 0，但不是最低点。

### 高维空间里，鞍点远比局部最小值多

直觉上，在一个 $d$ 维空间里，一个点是「局部最小值」需要**所有** $d$ 个方向都往上翘；而「鞍点」只需要**一部分方向翘、一部分方向凹**。随着维度 $d$ 变大，「所有方向都翘」的概率急剧下降，而「一半翘一半凹」的组合越来越多。

> 💡 结论：**在深度学习的高维参数空间里，真正的局部最小值其实非常罕见，我们遇到的大多数「梯度为 0」的点都是鞍点。** 所以「梯度下降会卡在局部最小」这个担忧，在深度学习里很大程度上是**多虑**了——真正让人头疼的是鞍点（以及损失曲面的形状），而 Momentum、Adam 这些方法正是在帮我们更快穿过鞍点和平坦区。
'''),
    ("code", r'''# ---- 鞍点 vs 局部最小值：3D 可视化 ----
from mpl_toolkits.mplot3d import Axes3D

x = np.linspace(-2, 2, 100); y = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(x, y)

fig = plt.figure(figsize=(14, 6))
# 左：鞍点 z = x² - y²（马鞍形：x 方向是谷，y 方向是峰）
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
Z1 = X**2 - Y**2
ax1.plot_surface(X, Y, Z1, cmap='Blues', alpha=0.85)
ax1.set_title('鞍点：z = x² - y²\nx 方向下坡，y 方向上坡')
ax1.set_xlabel('x'); ax1.set_ylabel('y'); ax1.set_zlabel('L')

# 右：局部最小值 z = x² + y²（碗形：所有方向都往上翘）
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
Z2 = X**2 + Y**2
ax2.plot_surface(X, Y, Z2, cmap='Oranges', alpha=0.85)
ax2.set_title('局部最小值：z = x² + y²\n所有方向都往上翘')
ax2.set_xlabel('x'); ax2.set_ylabel('y'); ax2.set_zlabel('L')

plt.tight_layout()
plt.show()

# 左图中心点：梯度为 0，但不是最低点（沿 x 方向还能往下走）——这就是鞍点；
# 右图中心点：真正的"坑底"，四周都是上坡——局部最小值。
'''),
    ("markdown", r'''## 6.3 为什么需要「自动调整学习速率」：每个参数该有不同的学习率

前面所有梯度下降都用一个**全局统一的学习率** $\eta$ 更新所有参数。这带来一个问题：**不同的参数，需要的学习率可能天差地别**。

回想第五章特征缩放里的「窄长碗」：有的方向陡、有的方向平。一个统一的学习率，对陡方向可能太大（震荡发散）、对平方向又太小（爬不动）。特征缩放能在一定程度上缓解，但更根本的解决思路是：**让每个参数拥有自己的、能自动调整的学习率**。

这就是**自适应学习率优化器**的思想。它们共同的做法是：**根据每个参数「历史梯度」的大小，自动缩放它的学习率**——梯度一直很大的参数，学习率自动变小；梯度一直很小的参数，学习率自动变大。下面看三种经典实现。
'''),
    ("markdown", r'''## 6.4 三种自适应学习率优化器：AdaGrad / RMSProp / Adam

### ① AdaGrad：用「所有历史梯度平方和」缩放

设第 $t$ 步参数 $\theta_i$ 的梯度为 $g_i^t$，AdaGrad 维护一个**梯度平方的累加和**：

$$v_i^t = v_i^{t-1} + (g_i^t)^2, \qquad \theta_i^{t+1} = \theta_i^t - \frac{\eta}{\sqrt{v_i^t + \epsilon}}\; g_i^t$$

- 分母 $\sqrt{v_i^t}$ 是「历史梯度平方和」的开方：某个参数的梯度一直很大，$v$ 就大，学习率自动变小；反之变大；
- 缺点：$v$ **只增不减**，训练到后期分母越来越大，学习率被压到几乎为 0，**过早停止学习**。

### ② RMSProp：只记「近期」的梯度平方

为了修 AdaGrad 的「只增不减」，RMSProp 把「累加」改成**指数加权移动平均**，让久远的梯度影响力衰减：

$$v_i^t = \beta\, v_i^{t-1} + (1-\beta)(g_i^t)^2, \qquad \theta_i^{t+1} = \theta_i^t - \frac{\eta}{\sqrt{v_i^t + \epsilon}}\; g_i^t$$

- $\beta$（通常 0.9）控制「记住多少历史」：越接近 1 记得越久；
- 这样 $v$ 会随近期梯度变化，不会无限增长。

### ③ Adam：Momentum + RMSProp 的结合体

Adam（Adaptive Moment Estimation）是**目前最常用的优化器**，把「动量」和「自适应学习率」合二为一：

$$m_i^t = \beta_1 m_i^{t-1} + (1-\beta_1) g_i^t \quad(\text{一阶矩，类似动量})$$
$$v_i^t = \beta_2 v_i^{t-1} + (1-\beta_2)(g_i^t)^2 \quad(\text{二阶矩，类似 RMSProp})$$
$$\hat m_i^t = \frac{m_i^t}{1-\beta_1^t}, \quad \hat v_i^t = \frac{v_i^t}{1-\beta_2^t} \quad(\text{偏差校正})$$
$$\theta_i^{t+1} = \theta_i^t - \frac{\eta}{\sqrt{\hat v_i^t} + \epsilon}\,\hat m_i^t$$

- $m$ 提供「惯性」（方向），$v$ 提供「自适应步长」（缩放）；
- 两个「偏差校正」是为了修正 $m,v$ 初始为 0 带来的前期偏小（$t$ 是步数，$\beta^t$ 随 $t$ 增大趋近 0）；
- 常用超参数：$\eta=0.001,\ \beta_1=0.9,\ \beta_2=0.999,\ \epsilon=10^{-8}$。

> 🔑 **记忆**：**Adam = 动量 + RMSProp**，默认首选优化器；它的四个默认超参数（lr=0.001, β1=0.9, β2=0.999, ε=1e-8）值得记住。
'''),
    ("code", r'''# ---- AdaGrad / RMSProp / Adam 从零实现 + 收敛对比 ----
# 在第五章那个"窄长谷"问题上，对比普通 GD 和三种自适应优化器。
def 窄长损失2(w, b):
    return 0.05 * w**2 + 5 * b**2

def 梯度_窄长(w, b):
    return 0.1 * w, 10 * b      # ∂L/∂w = 0.1w，∂L/∂b = 10b

def 跑优化器(方法, lr, 步数=60):
    w, b = -5.0, 3.0
    vw, vb = 0.0, 0.0           # 二阶矩（AdaGrad/RMSProp/Adam 用）
    mw, mb = 0.0, 0.0           # 一阶矩（Adam 用）
    轨 = [(w, b)]
    for t in range(1, 步数 + 1):
        gw, gb = 梯度_窄长(w, b)
        if 方法 == 'GD':
            w -= lr * gw; b -= lr * gb
        elif 方法 == 'AdaGrad':
            vw += gw**2; vb += gb**2                 # 累加平方（只增不减）
            w -= lr * gw / (np.sqrt(vw) + 1e-8); b -= lr * gb / (np.sqrt(vb) + 1e-8)
        elif 方法 == 'RMSProp':
            vw = 0.9 * vw + 0.1 * gw**2; vb = 0.9 * vb + 0.1 * gb**2   # 指数平均
            w -= lr * gw / (np.sqrt(vw) + 1e-8); b -= lr * gb / (np.sqrt(vb) + 1e-8)
        elif 方法 == 'Adam':
            mw = 0.9 * mw + 0.1 * gw; mb = 0.9 * mb + 0.1 * gb          # 一阶矩(动量)
            vw = 0.999 * vw + 0.001 * gw**2; vb = 0.999 * vb + 0.001 * gb**2  # 二阶矩
            mw_h = mw / (1 - 0.9**t); mb_h = mb / (1 - 0.9**t)          # 偏差校正
            vw_h = vw / (1 - 0.999**t); vb_h = vb / (1 - 0.999**t)
            w -= lr * mw_h / (np.sqrt(vw_h) + 1e-8); b -= lr * mb_h / (np.sqrt(vb_h) + 1e-8)
        轨.append((w, b))
    return np.array(轨)

ww = np.linspace(-8, 8, 100); bb = np.linspace(-8, 8, 100)
WW, BB = np.meshgrid(ww, bb)
ZZ = 0.05 * WW**2 + 5 * BB**2

fig, axes = plt.subplots(2, 2, figsize=(12, 11))
for ax, 方法, lr in zip(axes.ravel(), ['GD', 'AdaGrad', 'RMSProp', 'Adam'], [0.05, 0.8, 0.3, 0.3]):
    轨 = 跑优化器(方法, lr)
    ax.contourf(WW, BB, ZZ, levels=30, cmap='Blues')
    ax.plot(轨[:, 0], 轨[:, 1], 'o-', color=橙, lw=1.2, ms=3)
    ax.scatter(*轨[-1], color=红, s=80, zorder=5)
    ax.set_title(f'{方法}（lr={lr}）', fontsize=12)
    ax.set_xlabel('w'); ax.set_ylabel('b')
plt.suptitle('四种优化器在"窄长谷"问题上的收敛对比', fontsize=14)
plt.tight_layout()
plt.show()

# 观察：普通 GD 之字形震荡；AdaGrad/RMSProp 给每个参数自适应学习率，走得直；
# Adam 结合了动量 + 自适应，通常又快又稳（这也是它成为默认选择的原因）。
'''),
    ("markdown", r'''## 6.5 学习率调度：让学习率随训练「动态变化」

除了「自适应学习率」，还有一类方法叫**学习率调度（learning rate scheduling）**——让全局学习率 $\eta$ 随训练进程主动变化：

- **学习率衰减（decay）**：训练前期用大学习率快速下降，后期逐步减小学习率，好让参数稳定收敛到最优解附近。常见衰减方式：阶梯式（每 N 步乘 0.1）、指数衰减、余弦退火等；
- **Warmup（预热）**：训练**最开始**的若干步，用从小到大的学习率「预热」，避免一开始梯度很大时用大学习率导致发散，等稳定后再按正常策略下降。

> 💡 这些「调度」在现代大模型训练里非常关键（第十三、十九章的 Transformer 训练会再次遇到），入门阶段先了解思想：**学习率不是一成不变的常数，而是可以按时间表主动调节的**。
'''),
    ("markdown", r'''## 6.6 本章小结

| 概念 | 一句话直觉 |
| --- | --- |
| Batch size | 一次更新用多少数据；小 batch 泛化往往更好，大 batch 更稳 |
| 局部最小 vs 鞍点 | 高维空间里鞍点远比局部最小常见，真正该怕的是鞍点 |
| AdaGrad | 用历史梯度平方和缩放学习率（缺点：只增不减） |
| RMSProp | 用「近期」梯度平方的指数平均缩放 |
| Adam | Momentum + RMSProp 的结合，默认首选 |
| 学习率调度 | 让学习率随训练动态变化（衰减 / warmup） |

🔑 **记忆**：**Adam = 动量 + 自适应学习率**，默认超参数 lr=0.001、β1=0.9、β2=0.999、ε=1e-8。

> 📌 **下一步**：第七章讲**特征工程**（归一化/标准化/one-hot/特征组合），把第五章提过的特征缩放展开成完整的工程方法。
'''),
]

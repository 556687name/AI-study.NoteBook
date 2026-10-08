# -*- coding: utf-8 -*-
CELLS = [
    ("markdown", r'''# 第八章 过拟合与正则化

> 📌 **出处**：李宏毅 2026《机器学习》**第 41~50 讲**（过拟合和欠拟合正则化、L1/L2 正则化、套索回归 Lasso、岭回归 Ridge、ElasticNet）
> ⭐ **40 天重点**：对应计划 Day11「正则化：L1/L2 正则、Dropout」、Day17「处理过拟合（权重衰减、Dropout）」。这一章把第一章的「正则化直觉」彻底讲透。

---

## 8.1 回顾：过拟合的本质与正则化的思路

第三章讲过：模型太复杂，会把训练数据的**噪声**也背下来，导致「训练误差小、验证误差大」的**过拟合**。参数 $w$ 越大，函数越「敏感」，越容易过拟合。

**正则化（regularization）** 的通用思路是：**给损失函数加一个「惩罚项」，限制参数不要太大**：

$$L_{\text{新}} = L_{\text{原}} + \lambda \cdot \text{惩罚项}(w)$$

其中 $\lambda$（lambda，也叫正则化强度/系数）控制惩罚的力度：

- $\lambda$ 越大 → 越强地压制参数 → 模型越「简单」、越不容易过拟合（但太大会变成欠拟合）；
- $\lambda$ 越小 → 越接近原来的损失 → 越容易过拟合。

根据「惩罚项」的形式不同，分成 L1 和 L2 两大类（下一节详解），还有两者混合的 ElasticNet。

> 💡 核心问题只有一个：**惩罚项用 $w$ 的平方还是 $w$ 的绝对值？** 这一个选择，带来了一系列深刻区别。
'''),
    ("markdown", r'''## 8.2 L2 正则化：岭回归（Ridge）

L2 正则化在损失后面加**所有参数的平方和**：

$$L_{\text{new}} = L_{\text{原}} + \lambda \sum_{i} w_i^2$$

- 加了 L2 的线性回归，专门叫**岭回归（Ridge Regression）**；
- 效果：把**所有参数整体「往 0 收缩」**，但**不会变成 0**（因为平方项对「小参数」的惩罚很轻，参数可以保留一个很小的非零值）；
- 直觉：让每个参数都「克制一点」，避免某个参数特别大导致函数剧烈波动。

### 为什么 L2 让参数变小，却不归零？

看梯度：对 $w_i$ 求导，惩罚项贡献 $\frac{\partial}{\partial w_i}(\lambda w_i^2) = 2\lambda w_i$。更新时相当于每步都**额外把 $w_i$ 按比例削掉一点**（正比于 $w_i$ 当前大小）。$w_i$ 越大被削得越多，越小被削得越少——所以是「按比例收缩」，永远不会一步削到 0（只会无限逼近）。
'''),
    ("markdown", r'''## 8.3 L1 正则化：套索回归（Lasso）

L1 正则化在损失后面加**所有参数的绝对值之和**：

$$L_{\text{new}} = L_{\text{原}} + \lambda \sum_{i} |w_i|$$

- 加了 L1 的线性回归，叫**套索回归（Lasso Regression）**；
- 效果：不仅能收缩参数，还能让**一部分参数直接变成 0**——得到「稀疏（sparse）」解；
- 为什么能归零：对 $w_i$ 求导，惩罚项贡献 $\frac{\partial}{\partial w_i}(\lambda |w_i|) = \lambda \cdot \text{sign}(w_i)$。更新时是**每次减一个固定量**（不随 $w_i$ 变小而变小），所以参数会被「一路削到 0」然后停在那里。

### L1 归零 = 自动做特征选择

回想第七章：**让权重变成 0，等价于把这个特征从模型里删掉**。所以 Lasso 在训练的同时，自动完成了**特征选择**——权重变 0 的特征就是「没用」的特征，权重非 0 的才是重要的。这就是 L1 和 L2 最本质的区别。
'''),
    ("markdown", r'''## 8.4 L1 vs L2：几何直觉（为什么一个归零、一个不归零）

用几何能非常直观地看懂这个区别。把「最小化损失」重新表述成「在参数满足某个约束下，最小化损失」：

- L2 的约束是 $\sum w_i^2 \le C$：在二维里是一个**圆**；
- L1 的约束是 $\sum |w_i| \le C$：在二维里是一个**菱形**（四个尖角朝坐标轴）。

我们的解是「损失等高线」和「约束区域」**第一次相切**的点：

- **L2（圆）**：圆是光滑的，损失等高线通常和圆相切在**非轴**的位置，所以参数一般**非零**；
- **L1（菱形）**：菱形有**尖角**，损失等高线**很容易正好顶在尖角上**，而尖角位于**坐标轴上**（即某个参数 = 0），所以参数**容易为 0**。

> 💡 一句话：**L2 的圆没有尖角，解落在内部（非零）；L1 的菱形有尖角，解容易顶在轴上（归零）。** 下面的代码把这张图直接画出来。
'''),
    ("code", r'''# ---- L1 vs L2 的几何直觉：圆 vs 菱形 ----
# 画出 L2（圆）和 L1（菱形）的约束区域，以及"损失等高线"，
# 观察解（相切点）为什么 L1 容易落在坐标轴上（参数=0）。
fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))

# 假设真实最优解（无约束时）在 (1.5, 1.0) 附近，损失等高线是围绕它的椭圆
theta = np.linspace(0, 2 * np.pi, 200)

for ax, 类型 in zip(axes, ['L2', 'L1']):
    # 画损失等高线（椭圆，中心在 (1.5, 1.0)）
    for r in [0.3, 0.6, 0.9, 1.2, 1.5]:
        ell_x = 1.5 + r * 2 * np.cos(theta)
        ell_y = 1.0 + r * np.sin(theta)
        ax.plot(ell_x, ell_y, color=灰, lw=1, alpha=0.6)
    # 画约束区域边界
    if 类型 == 'L2':
        ax.plot(np.cos(theta), np.sin(theta), color=红, lw=3, label='L2 约束：圆（Σw² ≤ C）')
        ax.scatter([0.83], [0.56], color=绿, s=100, zorder=5, label='解：非零（收缩但保留）')
    else:
        菱形x = np.concatenate([[1, 0, -1, 0, 1]]); 菱形y = np.concatenate([[0, 1, 0, -1, 0]])
        ax.plot(菱形x, 菱形y, color=红, lw=3, label='L1 约束：菱形（Σ|w| ≤ C）')
        ax.scatter([1.0], [0.0], color=绿, s=100, zorder=5, label='解：落在轴上（w2=0 稀疏）')
    ax.axhline(0, color=灰, lw=0.8); ax.axvline(0, color=灰, lw=0.8)
    ax.set_xlim(-2.2, 3.2); ax.set_ylim(-2.2, 2.2)
    ax.set_xlabel('w1'); ax.set_ylabel('w2')
    ax.set_title(f'{类型} 正则化：等高线(灰)与约束区域(红)的相切点', fontsize=11)
    ax.legend(fontsize=9)

plt.suptitle('L1 的"尖角"让解容易落在坐标轴（参数归零）→ 稀疏；L2 的"圆"让解保留非零', fontsize=12)
plt.tight_layout()
plt.show()
'''),
    ("markdown", r'''## 8.5 ElasticNet：L1 + L2 的折中

**ElasticNet（弹性网络）** 同时加 L1 和 L2 两个惩罚项：

$$L_{\text{new}} = L_{\text{原}} + \lambda_1 \sum_i |w_i| + \lambda_2 \sum_i w_i^2$$

- 好处：兼顾 L1 的「稀疏」和 L2 的「稳定收缩」；
- 什么时候用：当特征很多、且特征之间有**相关性**时，纯 Lasso 可能随机地只保留其中一个相关特征（不稳定），而 ElasticNet 能更稳健地处理这种情况。

> 💡 实用建议：**Ridge（L2）是默认首选**（稳定、好调）；需要做特征选择时用 **Lasso（L1）**；特征多且相关时用 **ElasticNet**。
'''),
    ("code", r'''# ---- L1 / L2 / ElasticNet 正则化效果对比（抑制过拟合） ----
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

np.random.seed(40)
xr = np.linspace(0, 1, 20)
yr = np.sin(2 * np.pi * xr) + np.random.randn(20) * 0.5
xs = np.linspace(0, 1, 200)

def 画(ax, 模型, t):
    模型.fit(xr.reshape(-1, 1), yr)
    ax.scatter(xr, yr, color=蓝, s=25, alpha=0.9, label='数据（含噪声）')
    ax.plot(xs, 模型.predict(xs.reshape(-1, 1)), color=橙, lw=2.5, label='拟合曲线')
    ax.plot(xs, np.sin(2 * np.pi * xs), color=灰, lw=1.5, ls='--', label='真实函数')
    ax.set_title(t, fontsize=11)
    ax.set_ylim(-2.5, 2.5)

fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
# 都用 15 阶多项式（本身很容易过拟合），对比加不同正则化的效果
画(axes[0], make_pipeline(PolynomialFeatures(15), Ridge(alpha=0.001)), '无正则化（≈ 纯 15 阶多项式）→ 过拟合')
画(axes[1], make_pipeline(PolynomialFeatures(15), Ridge(alpha=1.0)), 'L2 正则化（Ridge α=1）→ 收缩参数')
画(axes[2], make_pipeline(PolynomialFeatures(15), Lasso(alpha=0.001)), 'L1 正则化（Lasso α=0.001）→ 稀疏参数')
plt.suptitle('正则化抑制过拟合：15 阶多项式 + 正则化后，曲线不再剧烈抖动', fontsize=13)
plt.tight_layout()
plt.show()

# 观察：左图（几乎无正则）曲线剧烈抖动、贴着每个噪声点 → 过拟合；
# 中图、右图（加正则）曲线变平滑，更贴近真实的正弦波 → 泛化更好。
'''),
    ("markdown", r'''## 8.6 深度学习的正则化：权重衰减与 Dropout

前面讲的是「线性回归」上的 L1/L2。在**神经网络**里，正则化有专门的叫法和技巧（⭐ 40 天计划 Day17 点名）。

### 权重衰减（Weight Decay）= 深度学习版的 L2

在神经网络里，L2 正则化常被称为**权重衰减（weight decay）**。它做的是同一件事：在损失里加 $\lambda\sum w^2$，让所有权重往 0 收缩，抑制过拟合。PyTorch 里就是给优化器加一个 `weight_decay` 参数（第十六章会看到）。

### Dropout：随机「关掉」一部分神经元

Dropout 是一种非常有效的神经网络正则化技巧：**训练时，每一步随机地把一部分神经元（比如 50%）「临时关掉」（输出置 0），只让剩下的神经元工作**。

为什么有效？直觉上：

- 每次训练都随机「丢弃」不同的一批神经元，相当于**同时训练了很多个「残缺的」小网络**，最后取它们的「平均」——这天然有正则化、抑制过拟合的效果；
- 神经元不能再「依赖」某个特定的同伴（因为同伴随时可能被关掉），被迫自己学到更鲁棒的特征。

> 💡 关键：Dropout 只在**训练时**开启，**测试时**关闭（用完整的网络）。PyTorch 里就是 `nn.Dropout(p)`，$p$ 是丢弃概率（常见 0.5）。
'''),
    ("code", r'''# ---- Dropout 的可视化：随机"关掉"一部分神经元 ----
# 画一个简单的网络，示意 Dropout 训练时的"随机丢弃"效果。
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

def 画网络(ax, 活跃掩码, t):
    # 三层：输入(4) → 隐藏(4) → 输出(2)
    层 = [[0.2, 0.5, 0.8], [0.25, 0.5, 0.75], [0.3, 0.7]]
    for layer_idx, xs_pos in enumerate(层):
        n = len(活跃掩码[layer_idx])
        for j in range(n):
            c = 蓝 if 活跃掩码[layer_idx][j] else 灰
            alpha = 1.0 if 活跃掩码[layer_idx][j] else 0.25
            ax.scatter(xs_pos[j], 0.8 - layer_idx * 0.35, s=700, color=c, alpha=alpha, edgecolors=灰, linewidths=1.2)
            if not 活跃掩码[layer_idx][j]:
                ax.plot([xs_pos[j]-0.045, xs_pos[j]+0.045], [0.8-layer_idx*0.35]*2, color=红, lw=2)
    # 连线
    for i in range(len(层[0])):
        for j in range(len(层[1])):
            ax.plot([层[0][i], 层[1][j]], [0.8, 0.45], color=灰, alpha=0.15, lw=0.8)
    for i in range(len(层[1])):
        for j in range(len(层[2])):
            ax.plot([层[1][i], 层[2][j]], [0.45, 0.1], color=灰, alpha=0.15, lw=0.8)
    ax.set_xlim(0.05, 1.0); ax.set_ylim(-0.05, 1.0); ax.axis('off')
    ax.set_title(t, fontsize=11)

画网络(axes[0], [[1,1,1],[1,1,1],[1,1]], '完整网络（测试时用）')
画网络(axes[1], [[1,1,1],[1,0,1],[1,1]], 'Dropout 某一步（关掉 1 个神经元）')
画网络(axes[2], [[1,1,1],[0,1,0],[1,1]], 'Dropout 另一步（关掉不同神经元）')
plt.suptitle('Dropout：训练时每步随机丢弃不同神经元（红叉=被关掉），相当于训练多个子网络', fontsize=13)
plt.tight_layout()
plt.show()
'''),
    ("markdown", r'''## 8.7 早停（Early Stopping）：在过拟合发生前停下

**早停**是一种最简单、却非常有效的正则化手段，思路直白：**训练时盯着验证集误差，一旦验证误差开始「回升」（说明要过拟合了），就停止训练**。

- 训练前期：训练误差和验证误差都下降；
- 到了某个点：训练误差继续降，但验证误差开始**拐头向上**——这就是过拟合的信号；
- 早停就是在这个「拐点」附近停下来，用「验证误差最低」的那份模型。

> 💡 早停和「保存最优模型（checkpoint）」是配套的：一边训练一边记录验证误差最低时的模型，最后用它（第十六章会实现这套标准流程）。
'''),
    ("code", r'''# ---- 早停（Early Stopping）示意 ----
# 模拟"训练误差一路下降、验证误差先降后升"的典型过程，标出早停点。
训练误差 = np.array([0.9, 0.6, 0.4, 0.28, 0.2, 0.15, 0.12, 0.1, 0.08, 0.065, 0.055])
验证误差 = np.array([0.85, 0.55, 0.36, 0.26, 0.21, 0.19, 0.185, 0.19, 0.21, 0.24, 0.29])
轮次 = np.arange(len(训练误差))

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.plot(轮次, 训练误差, 'o-', color=蓝, lw=2, label='训练误差')
ax.plot(轮次, 验证误差, 's-', color=红, lw=2, label='验证误差')
最佳 = int(np.argmin(验证误差))
ax.axvline(最佳, color=绿, ls='--', lw=2)
ax.scatter([最佳], [验证误差[最佳]], color=绿, s=120, zorder=5)
ax.annotate('早停点（验证误差最低）', xy=(最佳, 验证误差[最佳]), xytext=(最佳+0.5, 0.5),
            arrowprops=dict(arrowstyle='->', color=绿), fontsize=11, color=绿)
ax.set_xlabel('训练轮数（epoch）'); ax.set_ylabel('误差')
ax.set_title('早停：验证误差开始回升时停止训练，取最低点的模型')
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# 看图：绿虚线右侧，训练误差还在降（模型还在"背"），但验证误差已经抬头（过拟合开始），
# 所以应该在绿虚线处停下来。
'''),
    ("markdown", r'''## 8.8 本章小结

| 方法 | 惩罚项 | 效果 | 别名 |
| --- | --- | --- | --- |
| L2 正则化 | $\lambda\sum w_i^2$ | 参数整体收缩，不归零 | Ridge（岭回归）、权重衰减 |
| L1 正则化 | $\lambda\sum |w_i|$ | 部分参数归零（稀疏） | Lasso（套索回归） |
| ElasticNet | 两者混合 | 稀疏 + 稳定 | 弹性网络 |
| Dropout | —— | 随机丢弃神经元 | 神经网络专用 |
| 早停 | —— | 验证误差回升就停 | —— |

🔑 **记忆**：L2 收缩不归零（Ridge）、L1 归零做特征选择（Lasso）；正则化强度 $\lambda$ 越大模型越简单；Dropout 训练开、测试关。

> 📌 **下一步**：第九章讲**逻辑回归**——从「输出数值」的回归，转向「输出类别概率」的分类，并引出 softmax 和交叉熵。
'''),
]

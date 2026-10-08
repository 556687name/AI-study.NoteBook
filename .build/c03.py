# -*- coding: utf-8 -*-
CELLS = [
    ("markdown", r'''# 第三章 机器学习任务攻略：偏差、方差与交叉验证

> 📌 **出处**：李宏毅 2026《机器学习》**第 3 讲「机器学习任务攻略」**（B 站 BV1RnikBvE8m）
> ⭐ **40 天重点**：对应计划 Day15「机器学习概览」——*训练/验证/测试集划分、偏差-方差权衡、过拟合与欠拟合诊断*。这一章解决一个最实际的问题：**模型训练效果不好时，到底该怎么办**。

---

## 3.1 从实际问题出发：模型效果不好，怎么办？

先设想一个真实场景：你花了一天训练好一个模型，满怀期待地放到测试集上一看——准确率很差。这时候你该怎么办？

很多人的第一反应是「换个更复杂的模型」或「再多训练一会儿」，但这些都是**瞎撞**。真正高效的做法是：**先诊断问题出在哪，再对症下药**。李宏毅老师在这一讲给了一张「攻略地图」，核心就一句话：

> **分别看训练集误差和验证集误差，判断模型是「没学够」还是「学过头了」。**

这两个数就像医生的两个化验指标，能告诉你病根是「偏差大（欠拟合）」还是「方差大（过拟合）」，然后才能开对药。本章就系统讲清这套诊断方法。

---

## 3.2 为什么要把数据分成三份：训练 / 验证 / 测试

### 为什么不能只看训练集？

第一章讲过「过拟合」：模型可能把训练数据的噪声都背下来，在训练集上表现近乎完美，但换一批新数据就崩。**所以「训练集上的误差」不能代表模型真实的好坏**——它可能是「背题背出来的高分」。

### 三个集合的分工

为了既训练模型、又客观评价模型，标准做法是把数据切成三份：

| 集合 | 作用 | 类比 |
| --- | --- | --- |
| **训练集 train** | 用来**训练**模型（更新参数） | 平时做作业 |
| **验证集 validation** | 用来**调超参数、选模型**（比如挑学习率、挑模型复杂度），**不参与训练** | 模拟考试 |
| **测试集 test** | **只在最后**评估一次模型的最终泛化能力 | 高考 |

> 🔑 **记忆**：三个集合的分工是「训练集出参数，验证集出选择，测试集出成绩」。**测试集从头到尾只能碰一次**，绝对不能拿它反复调模型，否则测试集就变成了「另一个验证集」，评估结果会虚高。

### 为什么需要单独的验证集？

因为「调超参数」本身也是一种「拟合」：你反复在验证集上挑最好的模型/参数，其实是在「拟合验证集」。如果验证集和测试集是同一份，那你等于在测试集上调参，最终成绩必然虚高。所以需要**把验证集和测试集分开**，保证测试集是「从没被模型/你见过」的干净数据。
'''),
    ("code", r'''# ---- 数据划分可视化：训练 / 验证 / 测试 三份的分工 ----
# 用颜色把同一批数据标成三段，直观理解"谁用来训练、谁用来调参、谁用来考试"。
np.random.seed(2)
n = 60
X3 = np.linspace(0, 1, n)
y3 = np.sin(2 * np.pi * X3) + np.random.randn(n) * 0.3

# 按 60% / 20% / 20% 划分（这里只做示意，实际用 sklearn 的 train_test_split 更规范）
train_end, val_end = int(n * 0.6), int(n * 0.8)
fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(X3[:train_end], y3[:train_end], color=蓝, s=30, label='训练集 train（更新参数）')
ax.scatter(X3[train_end:val_end], y3[train_end:val_end], color=橙, s=30, label='验证集 val（调超参数）')
ax.scatter(X3[val_end:], y3[val_end:], color=红, s=40, marker='^', label='测试集 test（最后评估一次）')
ax.set_xlabel('x'); ax.set_ylabel('y')
ax.set_title('数据三划分：训练集出参数，验证集出选择，测试集出成绩')
ax.legend()
plt.tight_layout()
plt.show()
'''),
    ("markdown", r'''## 3.3 诊断第一步：对比「训练误差」和「验证误差」

拿到一个效果不好的模型，先算两个数：

- **训练误差（training error）**：模型在**训练集**上的误差；
- **验证误差（validation error）**：模型在**验证集**（训练时没见过的数据）上的误差。

这两个数的大小关系，直接暴露问题所在：

| 现象 | 诊断 | 通俗说法 |
| --- | --- | --- |
| 训练误差**大**，验证误差也大 | **偏差大** → 欠拟合 | 模型太简单，连训练数据都没学好 |
| 训练误差**小**，但验证误差**大** | **方差大** → 过拟合 | 模型太复杂，只会背题不会举一反三 |
| 训练误差小，验证误差也小 | 刚刚好 | 理想状态 |

> 💡 一句话：**训练误差大 = 没学够（欠拟合）；训练误差小但验证误差大 = 学过头（过拟合）。** 诊断出是哪一种，下一节的对策才有方向。
'''),
    ("code", r'''# ---- 模型复杂度 vs 训练/验证误差：诊断 U 型曲线 ----
# 用不同阶数的多项式拟合同一份数据，分别算训练误差和验证误差，
# 画出"模型复杂度 → 误差"的曲线，这是诊断欠拟合/过拟合的核心图。
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error

np.random.seed(5)
X4 = np.linspace(0, 1, 30)
y4 = np.sin(2 * np.pi * X4) + np.random.randn(30) * 0.4
X_tr, X_va, y_tr, y_va = train_test_split(X4, y4, test_size=0.4, random_state=0)

复杂度 = list(range(1, 16))          # 多项式阶数 1~15
训练误差, 验证误差 = [], []
for d in 复杂度:
    model = make_pipeline(PolynomialFeatures(d), LinearRegression())
    model.fit(X_tr.reshape(-1, 1), y_tr)
    训练误差.append(mean_squared_error(y_tr, model.predict(X_tr.reshape(-1, 1))))
    验证误差.append(mean_squared_error(y_va, model.predict(X_va.reshape(-1, 1))))

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.plot(复杂度, 训练误差, 'o-', color=蓝, lw=2, label='训练误差')
ax.plot(复杂度, 验证误差, 's-', color=红, lw=2, label='验证误差')
ax.axvline(3, color=灰, ls='--', lw=1)
ax.text(1.2, 0.35, '欠拟合区\n(偏差大)', fontsize=10, color=灰)
ax.text(9.5, 0.35, '过拟合区\n(方差大)', fontsize=10, color=灰)
ax.set_xlabel('模型复杂度（多项式阶数）'); ax.set_ylabel('均方误差 MSE')
ax.set_title('诊断图：训练误差和验证误差的差距，暴露了模型的问题')
ax.legend()
plt.tight_layout()
plt.show()

# 看图：
#   左端（1~2 阶）：训练误差、验证误差都大 → 欠拟合（偏差大）；
#   右端（8 阶以上）：训练误差越来越小，验证误差反而变大 → 过拟合（方差大）；
#   中间（3~5 阶）：验证误差最低，是最合适的复杂度。
'''),
    ("markdown", r'''## 3.4 偏差（Bias）与方差（Variance）：两个误差的深层含义

「欠拟合」和「过拟合」背后，是统计学习里两个根本概念：**偏差**和**方差**。

### 偏差 Bias：模型「平均而言」离真相有多远

想象我们反复做实验：每次抽一批不同的训练数据，训练一个模型。**偏差**衡量的是「所有这些模型预测的**平均值**」和「真实值」之间的差距。

- 如果模型**太简单**（比如用直线去拟合正弦波），不管换多少批数据，它预测的平均值都系统性地偏离真相——**偏差就大**。这对应**欠拟合**。

### 方差 Variance：模型对「训练数据的波动」有多敏感

**方差**衡量的是「换一批训练数据，模型的预测会变化多大」。

- 如果模型**太复杂**（比如 15 阶多项式），它会把每一批数据里的噪声都死死记住，于是换一批数据，模型就变成完全不同的形状——预测结果波动巨大，**方差就大**。这对应**过拟合**。

### 误差的分解：误差 = 偏差² + 方差 + 噪声

统计上可以证明（不要求推导，但要记住结论），模型的期望误差可以分解成三项：

$$\text{期望误差} = \underbrace{\text{偏差}^2}_{\text{模型太简单导致}} + \underbrace{\text{方差}}_{\text{模型太复杂导致}} + \underbrace{\text{噪声}}_{\text{数据本身固有的，无法消除}}$$

这个公式揭示了一个**权衡（bias-variance tradeoff）**：模型越简单，偏差越大、方差越小；模型越复杂，偏差越小、方差越大。**好的模型要在两者之间取平衡**——既不太简单（偏差别太大），也不太复杂（方差别太大）。这就是「诊断 U 型曲线」里验证误差先降后升的根本原因。
'''),
    ("code", r'''# ---- 偏差 vs 方差：同一复杂度，换多批数据看模型抖不抖 ----
# 固定一个阶数，随机抽多批训练数据各拟合一次，看模型形状的"离散程度"。
def 拟合多项式(X_, y_, d):
    return np.polyfit(X_, y_, d)

xs = np.linspace(0, 1, 200)
真函数 = np.sin(2 * np.pi * xs)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
for ax, d, t in zip(axes, [1, 9], ['低复杂度（1 阶）→ 高偏差、低方差', '高复杂度（9 阶）→ 低偏差、高方差']):
    for k in range(6):
        np.random.seed(100 + k)
        Xk = np.sort(np.random.rand(20))
        yk = np.sin(2 * np.pi * Xk) + np.random.randn(20) * 0.3
        系数 = 拟合多项式(Xk, yk, d)
        ax.plot(xs, np.polyval(系数, xs), alpha=0.6, lw=1.5)
    ax.plot(xs, 真函数, color=灰, lw=2.5, ls='--', label='真实函数')
    ax.set_title(t)
    ax.set_ylim(-2.5, 2.5)
    ax.legend(fontsize=9)

plt.suptitle('偏差 vs 方差：左图 6 条线挤在一起（方差小）但都偏离真相（偏差大）；右图反之', fontsize=12)
plt.tight_layout()
plt.show()

# 左边（1 阶）：6 条直线几乎重合（方差小），但它们全是直线、离正弦波很远（偏差大）；
# 右边（9 阶）：6 条曲线各贴各的噪声、彼此差很多（方差大），但平均起来接近真相（偏差小）。
'''),
    ("markdown", r'''## 3.5 对症下药：欠拟合和过拟合分别怎么解决

诊断出问题之后，对策就很清晰了：

### 如果欠拟合（偏差大，训练误差就大）

核心思路：**让模型更强**。

- **换更复杂的模型**：直线换成高次多项式、浅网络换成深网络；
- **加更多特征**：把更多有用的输入信息喂给模型；
- **减少正则化**：如果正则化太狠把模型「压」得太死，就放松一点。

### 如果过拟合（方差大，训练误差小但验证误差大）

核心思路：**让模型别「死记」，学会「泛化」**。有几类经典手段：

- **收集更多数据**：数据越多，噪声越难被「记住」，模型越容易学到真实规律（最有效的办法，但数据往往不够）；
- **数据增强（data augmentation）**：人为扩充数据，比如把图片旋转、裁剪、变色，相当于「造」更多样本（第十五章会讲）；
- **正则化**：给损失加惩罚项，限制模型复杂度（第八章系统讲 L1/L2/Dropout/早停）；
- **简化模型**：减少参数、减少层数，让模型没能力去背噪声。

> 📌 **出处**：正则化（L1/L2/Lasso/Ridge/Dropout/早停）的完整内容在**第八章**，数据增强在**第十五章**。
'''),
    ("markdown", r'''## 3.6 交叉验证 Cross-Validation：更可靠的评估方法

前面用「固定的一份验证集」来挑模型。但如果验证集切得不好（比如恰好切到一批噪声特别大的点），评估结果会不稳定。**交叉验证（Cross-Validation）** 是更稳健的做法。

### K 折交叉验证（K-fold Cross-Validation）

做法：把训练数据分成 $K$ 份（fold），然后做 $K$ 轮：

1. 每次拿其中 **1 份当验证集**，剩下 $K-1$ 份当训练集；
2. 训练并记录这次在验证集上的误差；
3. 轮换「哪一份当验证集」，重复 $K$ 次；
4. 最后把 $K$ 次的验证误差**取平均**，作为这个模型/超参数的评估结果。

好处是：**每一份数据都被当过验证集**，评估结果不再依赖某一次「切得巧不巧」，更稳定可靠。

### 什么时候用交叉验证？

- **调超参数、选模型时**用交叉验证，能更可靠地比较不同选择的好坏；
- 交叉验证计算量是原来的 $K$ 倍，所以**数据量大、模型贵时**常用简单的「单次验证集划分」代替；数据量小时交叉验证尤其有价值。
'''),
    ("code", r'''# ---- K 折交叉验证演示 ----
from sklearn.model_selection import KFold

np.random.seed(11)
X5 = np.linspace(0, 1, 40)
y5 = np.sin(2 * np.pi * X5) + np.random.randn(40) * 0.4
X5 = X5.reshape(-1, 1)

kf = KFold(n_splits=5, shuffle=True, random_state=0)
折号 = 1
分数 = []
fig, axes = plt.subplots(1, 5, figsize=(18, 3.5))
for (train_idx, val_idx), ax in zip(kf.split(X5), axes):
    model = make_pipeline(PolynomialFeatures(3), LinearRegression())
    model.fit(X5[train_idx], y5[train_idx])
    sc = mean_squared_error(y5[val_idx], model.predict(X5[val_idx]))
    分数.append(sc)
    # 画出每一折：训练点（蓝）和验证点（红）
    ax.scatter(X5[train_idx], y5[train_idx], color=蓝, s=15)
    ax.scatter(X5[val_idx], y5[val_idx], color=红, s=15)
    ax.set_title(f'第 {折号} 折\n验证MSE={sc:.3f}', fontsize=9)
    ax.set_xticks([]); ax.set_yticks([])
    折号 += 1

plt.suptitle('5 折交叉验证：每次换一份数据当验证集（红点），最后把 5 次误差平均', fontsize=12)
plt.tight_layout()
plt.show()
print("5 折的验证 MSE：", [round(s, 3) for s in 分数])
print("平均验证 MSE：", round(np.mean(分数), 3), "（这就是该模型更可靠的评估结果）")
'''),
    ("markdown", r'''## 3.7 本章小结

这一章给了一张**「模型效果不好时的攻略地图」**：

1. 数据要分**训练 / 验证 / 测试**三份，测试集只在最后碰一次；
2. 诊断看两个数：**训练误差大 → 欠拟合（偏差大）；训练误差小、验证误差大 → 过拟合（方差大）**；
3. 根源是**偏差-方差权衡**：模型太简单偏差大，太复杂方差大，误差 = 偏差² + 方差 + 噪声；
4. 对症下药：欠拟合→换更强模型；过拟合→加数据/正则化/简化模型；
5. **交叉验证**（K 折）能更可靠地评估模型好坏。

🔑 **记忆**：**训练误差 vs 验证误差的对比，是判断欠拟合/过拟合的最核心方法**。这张诊断图（3.3 的 U 型曲线）要能自己画出来、讲清楚。
'''),
]

# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# 决策树与随机森林（sklearn 实战）

> 📌 **出处**：李沐《实用机器学习》「树模型」——决策树、随机森林
> 🎯 **目标**：搞懂「用 if-else 划分数据」的**决策树**，以及「种很多棵、投票表决」的**随机森林**，并理解它们为什么是表格数据（结构化数据）的王者。

## 树模型为什么好用

表格数据（特征是一列列数字/类别）上，**树模型 + 集成**常比深度学习更强、更省算力、更易解释。核心直觉：**不断问「哪个特征、在哪个值切一刀，能最快把数据分干净」。**
"""))

cells.append(code(ENV))

cells.append(md("""## 1. 决策树：用「信息纯度」指导切分

每一步选一个特征 + 一个阈值，把数据切成两块，让**每一块越来越「纯」**（同类挤在一起）。衡量「纯度」的指标有两个：

- **基尼不纯度 Gini**：随机抽两个样本，标到不同类的概率。越小越纯。
- **信息熵 Entropy**：$H = -\\sum_k p_k \\log p_k$，越乱越大。

每次切分选「纯度提升最大」的那一刀，直到叶子基本纯净或达到深度上限。
"""))

cells.append(code("""# ---- 造一个 2D 数据：三类月牙，看决策树怎么「划线」切分 ----
from sklearn.datasets import make_moons
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

X, y = make_moons(n_samples=300, noise=0.25, random_state=0)
y = y + 1  # 0/1 -> 1/2，便于绘图区分

# 训练决策树（max_depth 控制树的「复杂度」）
tree = DecisionTreeClassifier(max_depth=4, random_state=0)
tree.fit(X, y)

# 画决策边界
xx = np.linspace(X[:, 0].min() - 0.3, X[:, 0].max() + 0.3, 300)
yy = np.linspace(X[:, 1].min() - 0.3, X[:, 1].max() + 0.3, 300)
XX, YY = np.meshgrid(xx, yy)
Z = tree.predict(np.c_[XX.ravel(), YY.ravel()]).reshape(XX.shape)

fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
ax[0].contourf(XX, YY, Z, alpha=0.4, cmap='viridis')
ax[0].scatter(X[:, 0], X[:, 1], c=y, s=20, cmap='viridis', edgecolor='k')
ax[0].set_title("决策边界：横平竖直的「刀」，因为每次只切一个特征")

plot_tree(tree, filled=True, ax=ax[1], feature_names=['x1', 'x2'], class_names=['1', '2'])
ax[1].set_title("决策树结构：每个节点 = 一个问题")
plt.tight_layout()
plt.show()
print("训练准确率：", f"{tree.score(X, y):.3f}（max_depth=4）")
"""))

cells.append(md("""## 2. 随机森林：种很多棵「不一样的树」，投票表决

单棵树容易过拟合（把噪声也记住）。随机森林的解法：**装袋 + 随机选特征**——

1. **Bootstrap 采样**：有放回地抽 N 个样本，每棵树用「不同的一份数据」训练；
2. **随机选特征**：每次切分只从**随机抽出的 k 个特征**里选最优（不是全部）；
3. 最终**多数投票**（分类）或平均（回归）。

「每棵树都不同」+「投票」，让整体方差大幅下降，稳定又好用。
"""))

cells.append(code("""# ---- 随机森林 vs 单棵决策树：在真数据(鸢尾花)上比 ----
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

iris = load_iris()
Xtr, Xte, ytr, yte = train_test_split(iris.data, iris.target, test_size=0.3, random_state=0)

tree = DecisionTreeClassifier(random_state=0)
rf = RandomForestClassifier(n_estimators=100, random_state=0)
tree.fit(Xtr, ytr); rf.fit(Xtr, ytr)

print("单棵决策树 测试准确率：", f"{tree.score(Xte, yte):.4f}")
print("随机森林(100棵) 测试准确率：", f"{rf.score(Xte, yte):.4f}")

# 特征重要性：随机森林告诉我们「哪个特征最有用」
import pandas as pd
imp = pd.Series(rf.feature_importances_, index=iris.feature_names).sort_values()
fig, ax = plt.subplots(figsize=(6, 3))
imp.plot.barh(ax=ax, color=绿)
ax.set_title("随机森林的特征重要性：花瓣尺寸最关键")
plt.show()
"""))

cells.append(md("""## 小结

| 概念 | 一句话直觉 |
| --- | --- |
| 决策树 | 不断「切一刀」把数据分纯，像一张 if-else 流程图 |
| 基尼/熵 | 衡量「乱不乱」的指标，越小越纯 |
| 随机森林 | 种很多棵随机树，投票表决，方差小、稳定 |
| Bootstrap | 有放回采样，让每棵树看到「不同数据」 |
| 特征重要性 | 随机森林可输出「哪个特征最有用」 |

> 🔑 **记忆**：**决策树 = 递归切分**；**随机森林 = 一堆不同的树投票**。树模型是表格数据的「默认首选」，几乎不需要特征缩放、能自动抓非线性。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\决策树与随机森林.ipynb", cells)
print("决策树与随机森林 ✔")

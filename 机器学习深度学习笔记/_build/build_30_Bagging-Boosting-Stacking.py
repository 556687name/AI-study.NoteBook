# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# 集成学习三大流派：Bagging / Boosting / Stacking（sklearn 实战）

> 📌 **出处**：李沐《实用机器学习》「组合模型」——Bagging、Boosting、Stacking
> 🎯 **目标**：把「单模型 → 多个模型合起来」的三种组合方式一网打尽，搞懂它们**分别解决什么问题、怎么组合**。

## 为什么要「组合」模型

单个模型总有偏差或方差。**集成（Ensemble）**：训练多个模型，把它们的输出**合起来**，通常比任何一个单独模型都强。三种组合思路：

| 流派 | 组合方式 | 解决什么 |
| --- | --- | --- |
| **Bagging** | 并行训练多个模型，**投票/平均** | 降**方差**（更稳） |
| **Boosting** | 串行训练，每个**修正前一个**的错 | 降**偏差**（更准） |
| **Stacking** | 多个模型的输出**喂给一个「元模型」**再学 | 让模型互相「取长补短」 |
"""))

cells.append(code(ENV))

cells.append(md("""## 1. Bagging：并行投票（代表：随机森林）

**Bootstrap 采样**出多份「有放回」的数据，各训一个模型，最后投票。模型之间**独立、并行**，平均后方差变小、更抗过拟合。
"""))

cells.append(code("""# ---- Bagging：多个决策树投票 vs 单棵树 ----
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

X, y = load_breast_cancer(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)

single = DecisionTreeClassifier(random_state=0).fit(Xtr, ytr)
bag = BaggingClassifier(DecisionTreeClassifier(), n_estimators=100, random_state=0).fit(Xtr, ytr)

print("单棵决策树 测试准确率：", f"{single.score(Xte, yte):.4f}")
print("Bagging(100棵树) 测试准确率：", f"{bag.score(Xte, yte):.4f}")

# 看「树越多，方差越小、越稳」的趋势
fig, ax = plt.subplots(figsize=(7, 3.5))
ns = [1, 5, 10, 20, 50, 100, 200]
accs = []
for n in ns:
    m = BaggingClassifier(DecisionTreeClassifier(), n_estimators=n, random_state=0).fit(Xtr, ytr)
    accs.append(m.score(Xte, yte))
ax.plot(ns, accs, 'o-', color=蓝)
ax.axhline(single.score(Xte, yte), ls='--', color=灰, label='单棵树')
ax.set_xlabel('树的数量'); ax.set_ylabel('测试准确率')
ax.set_title('Bagging：树越多越稳（收敛到随机森林水平）')
ax.legend()
plt.show()
"""))

cells.append(md("""## 2. Boosting：串行补漏（代表：GBDT / AdaBoost）

一个个**串行**训练，后一个专注前一个的错。能把偏差压得很低，但要小心过拟合、训练慢（无法并行）。
"""))

cells.append(code("""# ---- Boosting：AdaBoost 串行提升弱学习器 ----
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier

ada = AdaBoostClassifier(n_estimators=100, random_state=0).fit(Xtr, ytr)
gb = GradientBoostingClassifier(n_estimators=100, random_state=0).fit(Xtr, ytr)

print("AdaBoost       测试准确率：", f"{ada.score(Xte, yte):.4f}")
print("梯度提升 GBDT  测试准确率：", f"{gb.score(Xte, yte):.4f}")
"""))

cells.append(md("""## 3. Stacking：让「元模型」学怎么融合

不简单地投票/平均，而是把**多个异质模型的输出当成新特征**，再训一个**元模型（meta-learner）**来学「该更信谁」。本质是「用模型来融合模型」。
"""))

cells.append(code("""# ---- Stacking：多个异质模型 -> 元模型 ----
from sklearn.ensemble import StackingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

base = [
    ('knn', KNeighborsClassifier()),
    ('rf', RandomForestClassifier(n_estimators=100, random_state=0)),
    ('svm', SVC(probability=True, random_state=0)),
]
stack = StackingClassifier(estimators=base, final_estimator=LogisticRegression(), cv=5)
stack.fit(Xtr, ytr)

print("Stacking(KNN+RF+SVM -> LR) 测试准确率：", f"{stack.score(Xte, yte):.4f}")

# 汇总对比
names = ['单棵树', 'Bagging', 'AdaBoost', 'GBDT', 'Stacking']
scores = [single.score(Xte, yte), bag.score(Xte, yte), ada.score(Xte, yte),
          gb.score(Xte, yte), stack.score(Xte, yte)]
fig, ax = plt.subplots(figsize=(7, 3.5))
ax.bar(names, scores, color=[灰, 蓝, 橙, 红, 绿])
for i, s in enumerate(scores):
    ax.text(i, s + 0.003, f"{s:.3f}", ha='center', fontsize=9)
ax.set_ylim(0.9, 1.0)
ax.set_ylabel('测试准确率'); ax.set_title('集成学习：组合起来通常都更强')
plt.show()
"""))

cells.append(md("""## 小结

| 流派 | 并行/串行 | 代表 | 核心作用 |
| --- | --- | --- | --- |
| Bagging | 并行 | 随机森林 | 降方差 |
| Boosting | 串行 | GBDT / XGBoost | 降偏差 |
| Stacking | 并行 + 元模型 | StackingClassifier | 取长补短 |

> 🔑 **记忆**：**Bagging 平均多个独立模型**（稳），**Boosting 串行补漏**（准），**Stacking 用元模型融合**（聪明）。实战中「梯度提升树（XGB/LGBM）」和「随机森林」是最常用的两把利剑。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\Bagging-Boosting-Stacking.ipynb", cells)
print("Bagging-Boosting-Stacking ✔")

# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# 模型调参与超参数优化（sklearn 实战）

> 📌 **出处**：李沐《实用机器学习》「模型调参（超参数优化）」
> 🎯 **目标**：搞懂「超参数 vs 参数」的区别，以及怎么系统地找到好的超参数——**网格搜索 Grid Search、随机搜索 Random Search**。

## 参数 vs 超参数

- **参数**：模型**自己学**出来的（如权重 w、b）；
- **超参数**：人**在训练前定**的（如学习率、树的数量、深度、正则化系数）。

调参 = 给超参数找一组好取值。靠感觉一个个试太低效，要**系统地搜**。
"""))

cells.append(code(ENV))

cells.append(md("""## 1. 网格搜索 GridSearchCV：把候选值「穷举」一遍

给定每个超参数一组候选值，把**所有组合**都试一遍，用交叉验证评分，选出最优组合。
"""))

cells.append(code("""# ---- 网格搜索：随机森林的 n_estimators × max_depth ----
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_breast_cancer
import matplotlib.pyplot as plt

X, y = load_breast_cancer(return_X_y=True)

param_grid = {
    'n_estimators': [10, 50, 100],
    'max_depth': [3, 6, 10, None],
    'min_samples_split': [2, 5],
}
grid = GridSearchCV(RandomForestClassifier(random_state=0), param_grid, cv=5, n_jobs=-1)
grid.fit(X, y)

print("最优超参数：", grid.best_params_)
print("最优交叉验证准确率：", f"{grid.best_score_:.4f}")
print("候选组合总数：", len(param_grid['n_estimators']) * len(param_grid['max_depth']) * len(param_grid['min_samples_split']))
"""))

cells.append(md("""## 2. 随机搜索 RandomizedSearchCV：高维空间更高效

网格搜索会**指数爆炸**（组合数 = 各候选个数相乘）。**随机搜索**：从超参数分布里**随机抽 N 组**来试。在高维、超参数多时，同样的预算下随机搜索常能找到更好的解。
"""))

cells.append(code("""# ---- 随机搜索：从分布里抽 N 组试 ----
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

param_dist = {
    'n_estimators': randint(20, 200),
    'max_depth': randint(2, 15),
    'min_samples_split': randint(2, 10),
    'max_features': uniform(0.3, 0.7),
}
random_search = RandomizedSearchCV(
    RandomForestClassifier(random_state=0), param_dist, n_iter=30, cv=5, random_state=0, n_jobs=-1)
random_search.fit(X, y)

print("随机搜索最优超参数：", random_search.best_params_)
print("随机搜索最优交叉验证准确率：", f"{random_search.best_score_:.4f}")
print("（只试了 30 组，而不是穷举所有组合）")
"""))

cells.append(md("""## 3. 可视化：超参数对性能的影响

调参不是玄学，可以「画」出某个超参数对分数的影响，找到「甜点区」。
"""))

cells.append(code("""# ---- 画出 max_depth 对验证分数的曲线，找「甜点区」 ----
from sklearn.model_selection import validation_curve
import numpy as np

depths = [1, 2, 3, 4, 6, 8, 12, 20]
tr_scores, va_scores = validation_curve(
    RandomForestClassifier(n_estimators=50, random_state=0), X, y,
    param_name='max_depth', param_range=depths, cv=5)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(depths, tr_scores.mean(axis=1), 'o-', color=蓝, label='训练分数')
ax.plot(depths, va_scores.mean(axis=1), 'o-', color=红, label='验证分数')
ax.set_xlabel('max_depth'); ax.set_ylabel('准确率')
ax.set_title('验证分数先升后稳：再加深就过拟合了')
ax.legend()
plt.show()
"""))

cells.append(md("""## 小结

| 方法 | 怎么搜 | 适用 |
| --- | --- | --- |
| 手动调参 | 凭经验一个个试 | 快速验证 |
| 网格搜索 | 穷举所有组合 | 超参数少、范围小 |
| 随机搜索 | 从分布随机抽 N 组 | 高维、超参数多 |
| 贝叶斯优化 | 用历史结果「聪明地」选下一组 | 评估一次很贵时 |

> 🔑 **记忆**：**参数是学的，超参数是调的**。超参数少 → 网格；超参数多 → 随机/贝叶斯。每次评估都用**交叉验证**，避免被一次划分带偏。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\模型调参与超参数优化.ipynb", cells)
print("模型调参与超参数优化 ✔")

# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# 梯度提升树 GBDT（sklearn 实战）

> 📌 **出处**：李沐《实用机器学习》「梯度提升树」
> 🎯 **目标**：理解「一棵棵小树，专门修正前一轮的错误」的**梯度提升（Boosting）**，掌握工业界表格数据最强的武器 XGBoost / LightGBM / CatBoost。

## Boosting 的核心：加法模型，逐个补漏

和随机森林「并行种一堆树再投票」不同，Boosting 是**串行**的：每棵新树专门去拟合「前一轮**没学好**的残差」，让整体误差一步步下降。这就是 **GBDT（Gradient Boosting Decision Tree）**——每一棵都往**损失下降最快**的方向（梯度方向）修。
"""))

cells.append(code(ENV))

cells.append(md("""## 1. 手动演示「逐轮拟合残差」：看到提升是怎么发生的

用一个一维回归：先训一棵小树，算出它的**残差**（真实值 - 预测值），再训下一棵树去拟合这些残差，逐步逼近真实曲线。
"""))

cells.append(code("""# ---- 手动 boosting：一棵树不够，就再补一棵拟合残差 ----
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt

# 造一个非线性的真函数
x = np.linspace(0, 10, 200).reshape(-1, 1)
y_true = np.sin(x).ravel() + 0.1 * x.ravel()

# 第 1 轮：用一棵浅树粗拟合
trees = []
residual = y_true.copy()
pred = np.zeros_like(y_true)
n_rounds = 6
fig, axes = plt.subplots(2, 3, figsize=(13, 7))
for r in range(n_rounds):
    t = DecisionTreeRegressor(max_depth=2, random_state=0)
    t.fit(x, residual)                     # 🔑 拟合「残差」，而不是原始 y
    pred += 0.5 * t.predict(x)             # 以小步长累加
    residual = y_true - pred               # 更新残差
    trees.append(t)
    ax = axes[r // 3][r % 3]
    ax.plot(x, y_true, 'k--', lw=1.5, label='真实')
    ax.plot(x, pred, color=红, lw=1.5, label='累计预测')
    ax.set_title(f"第 {r+1} 轮（{r+1} 棵树）")
    ax.legend(fontsize=8)
plt.suptitle("梯度提升：每棵小树拟合残差，逐步逼近真实曲线")
plt.tight_layout()
plt.show()
"""))

cells.append(md("""## 2. sklearn 的梯度提升 + 工业级库

sklearn 有 `GradientBoostingClassifier`（经典）和更快的 `HistGradientBoostingClassifier`。工业界常用**更快的实现**：

| 库 | 特点 |
| --- | --- |
| **XGBoost** | 最早流行，支持 GPU、正则化、缺失值 |
| **LightGBM** | 基于直方图，训练快、内存省，大规模数据首选 |
| **CatBoost** | 对**类别特征**原生支持，几乎不用编码 |

下面用 sklearn 在一个分类任务上对比：单树 / 随机森林 / 梯度提升。
"""))

cells.append(code("""# ---- 三个模型在分类任务上对比 ----
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split

X, y = load_wine(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)

models = {
    "决策树": DecisionTreeClassifier(random_state=0),
    "随机森林": RandomForestClassifier(n_estimators=100, random_state=0),
    "梯度提升": GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=0),
}
for name, m in models.items():
    m.fit(Xtr, ytr)
    print(f"{name:6s} 测试准确率：{m.score(Xte, yte):.4f}")

# 可视化：GBDT 的 learning_rate 越小越稳（但要更多树）
fig, ax = plt.subplots(figsize=(7, 3.5))
for lr in [0.05, 0.1, 0.3, 1.0]:
    gb = GradientBoostingClassifier(n_estimators=100, learning_rate=lr, random_state=0)
    gb.fit(Xtr, ytr)
    ax.plot(gb.train_score_, label=f'lr={lr}')
ax.set_xlabel('树的数量'); ax.set_ylabel('训练损失')
ax.set_title("learning_rate：步长小收敛慢但更稳")
ax.legend()
plt.show()
"""))

cells.append(md("""## 小结

| 概念 | 一句话直觉 |
| --- | --- |
| Boosting | 串行种树，每棵专门修正前面的错误 |
| 残差 | 真实值 - 当前预测，是「还没学好」的部分 |
| 学习率 | 每棵树贡献的「步长」，小步慢走更稳 |
| XGBoost/LightGBM | 工业级梯度提升，表格数据竞赛标配 |

> 🔑 **记忆**：**随机森林 = 并行投票**（降方差），**梯度提升 = 串行补漏**（降偏差）。GBDT 一路「拟合残差」把偏差压到很低，配上合适的正则化就是表格数据的「天花板」方案。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\梯度提升树.ipynb", cells)
print("梯度提升树 ✔")

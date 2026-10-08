# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# 数据获取与标注（机器学习的第一步）

> 📌 **出处**：李沐《实用机器学习》「数据获取、网页数据抓取、数据标注」
> 🎯 **目标**：搞懂「数据从哪来」——公开数据集、API、网页抓取——以及「怎么给数据打上标签」——人工标注、半自动标注、主动学习。

## 机器学习先有「数据」，才有「模型」

模型再好，数据不行也白搭。数据工作分两半：**获取**（把数据拿到手）和**标注**（给数据贴上标签 y）。
"""))

cells.append(code(ENV))

cells.append(md("""## 1. 数据获取的几种途径

| 途径 | 例子 | 特点 |
| --- | --- | --- |
| **公开数据集** | ImageNet、COCO、Kaggle | 现成、干净，首选 |
| **API 接口** | 天气、股票、社交媒体 API | 结构化 JSON，实时 |
| **网页抓取** | requests + 解析库爬网页 | 灵活，但要注意反爬和版权 |
| **数据库/日志** | 公司内部 SQL、埋点日志 | 最真实，但要清洗 |

下面演示最常用的两种：从 **CSV 文件**读取（磁盘 / URL），和从 **内置数据集**加载。
"""))

cells.append(code("""# ---- 数据获取①：pandas 从 CSV 读取（磁盘 / URL 通用）----
import pandas as pd

# 造一份小 CSV 写盘，模拟「从文件获取数据」
raw = pd.DataFrame({
    '年龄': [25, 34, 28, 45, 19],
    '收入(万)': [12, 20, 15, 30, 6],
    '是否购买': [0, 1, 0, 1, 0],
})
raw.to_csv('_sample_users.csv', index=False)

df = pd.read_csv('_sample_users.csv')
print("从 CSV 读取的数据：")
print(df.head())

# 数据获取②：从 sklearn 内置数据集直接拿（最省事，无需下载）
from sklearn.datasets import load_diabetes
data = load_diabetes()
X, y = data.data, data.target
print("\\n从内置数据集获取：糖尿病数据，", X.shape[0], "条样本，", X.shape[1], "个特征")
print("特征名：", data.feature_names[:3], "...  目标：一年后病情进展指标")
"""))

cells.append(md("""## 2. 数据标注：从「全人工」到「半自动」

有数据没标签，就要**标注**。三种方式：

1. **人工标注**：外包平台（众包）逐条标，质量高但慢、贵；
2. **半自动标注**：先用已有模型**预标**，人只**复核/纠错**低置信度的部分；
3. **主动学习（Active Learning）**：让模型挑「自己最不确定的样本」让人标，**花最少的标注量换来最大提升**。

下面演示「半自动标注 + 主动学习」的核心思想：用置信度挑样本。
"""))

cells.append(code("""# ---- 半自动标注：模型预标 + 置信度筛「需要人工」的样本 ----
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# 假设我们只有少量已标注数据，其余未标注
X, y = load_iris(return_X_y=True)
X_labeled, X_pool, y_labeled, _ = train_test_split(X, y, train_size=30, random_state=0, stratify=y)

# 先用 30 条「已标注」数据训一个小模型
model = RandomForestClassifier(n_estimators=50, random_state=0)
model.fit(X_labeled, y_labeled)

# 对「未标注池」预测，得到置信度
probs = model.predict_proba(X_pool)
conf = probs.max(axis=1)          # 每个样本模型最确信的类别的概率
preds = probs.argmax(axis=1)

import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# 左：置信度分布
axes[0].hist(conf, bins=20, color=蓝, edgecolor='k')
axes[0].axvline(0.7, ls='--', color=红, label='阈值 0.7')
axes[0].set_xlabel('模型置信度'); axes[0].set_ylabel('样本数')
axes[0].set_title('主动学习：置信度低的样本最「值得」人工标')
axes[0].legend()

# 右：低置信度样本数量（这些才需要人工复核）
n_low = (conf < 0.7).sum(); n_high = (conf >= 0.7).sum()
axes[1].bar(['低置信度(需人工)', '高置信度(可信任)'], [n_low, n_high], color=[红, 绿])
axes[1].set_ylabel('样本数'); axes[1].set_title(f'仅 {n_low} 条需人工复核，省下 {n_high} 条标注量')
for i, v in enumerate([n_low, n_high]):
    axes[1].text(i, v + 1, str(v), ha='center')
plt.tight_layout()
plt.show()
print(f"未标注池共 {len(X_pool)} 条，只需人工复核 {n_low} 条（置信度<0.7），其余 {n_high} 条可直接采用模型预测")
"""))

cells.append(md("""## 小结

| 概念 | 一句话直觉 |
| --- | --- |
| 数据获取 | 公开数据集 / API / 爬虫 / 数据库 |
| 数据标注 | 给数据打标签 y，人工或半自动 |
| 半自动标注 | 模型预标 + 人工复核低置信样本 |
| 主动学习 | 让模型挑「最不确定」的样本让人标 |

> 🔑 **记忆**：**获取 → 标注 → 清洗 → 特征 → 模型**，数据工作是机器学习流水线的「上游」，上游质量决定下游天花板。标注贵，就用「半自动 + 主动学习」把人工花在刀刃上。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\数据获取与标注.ipynb", cells)
print("数据获取与标注 ✔")

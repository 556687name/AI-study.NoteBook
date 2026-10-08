# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# Kaggle 房价预测：完整流水线（PyTorch 实战）

> 📌 **出处**：李沐《动手学深度学习 V2》第 4 章「Kaggle 房价预测」
> 🎯 **目标**：走一遍真实 Kaggle 表格竞赛的完整流程——**下载数据 → 特征预处理 → 训练模型 → 对测试集预测 → 生成提交 CSV**。

## 这个任务在做什么

给定房子的 79 个特征（面积、地段、建造年份…），预测其售价 `SalePrice`。这是**回归**任务，评估指标是预测价格与真实价格的对数 RMSE。数据来自 Ames 房价数据集（1460 条训练 + 1459 条测试）。
"""))

cells.append(code(ENV))

cells.append(code("""# ---- 下载数据（d2l 官方镜像，缓存到本地） ----
import os
import pandas as pd
import numpy as np
import urllib.request

def download(url, path):
    if not os.path.exists(path):
        urllib.request.urlretrieve(url, path)
    return path

os.makedirs('../data/kaggle_house', exist_ok=True)
train_path = download('http://d2l-data.s3-accelerate.amazonaws.com/kaggle_house_pred_train.csv',
                      '../data/kaggle_house/train.csv')
test_path  = download('http://d2l-data.s3-accelerate.amazonaws.com/kaggle_house_pred_test.csv',
                      '../data/kaggle_house/test.csv')

train = pd.read_csv(train_path)
test  = pd.read_csv(test_path)
print("训练集：", train.shape, " 测试集：", test.shape)
print("目标列 SalePrice 前 5：", train['SalePrice'].head().tolist())
"""))

cells.append(md("""## 1. 特征预处理：数值标准化 + 类别独热

真实表格数据要「清洗 + 变换」才能喂给模型：数值特征**标准化**（均值 0 方差 1），类别特征**独热编码**，缺失值填充。训练集和测试集要**一起**处理，保证特征维度一致。
"""))

cells.append(code("""# ---- 预处理：标准化 + 独热 + 缺失填充 ----
# 标签取对数（房价是长尾分布，取 log 更接近正态，更好预测）
y = np.log(train['SalePrice']).values.astype(np.float32)

train_feat = train.drop(columns=['Id', 'SalePrice'])
test_ids = test['Id']
test_feat = test.drop(columns=['Id'])

# 训练/测试拼一起处理，保证独热后列数一致
all_feat = pd.concat([train_feat, test_feat], axis=0, ignore_index=True)

numeric_cols = all_feat.select_dtypes(include=[np.number]).columns
cat_cols = all_feat.select_dtypes(exclude=[np.number]).columns

num = all_feat[numeric_cols].fillna(all_feat[numeric_cols].mean())
num = (num - num.mean()) / num.std()          # 标准化
cat = all_feat[cat_cols].fillna('NA')
cat = pd.get_dummies(cat, dummy_na=True).astype(float)   # 独热

X_all = pd.concat([num, cat], axis=1).values.astype(np.float32)
n_train = len(train_feat)
X_train, X_test = X_all[:n_train], X_all[n_train:]

print("特征维度：", X_all.shape, "（79 个原始特征 →", X_all.shape[1], "维独热后）")
print("训练样本：", X_train.shape, " 测试样本：", X_test.shape)
"""))

cells.append(md("""## 2. 模型与训练

一个小 MLP（两个隐藏层），用 `MSELoss` 回归，`Adam` 优化。把训练集再切一部分当验证集，实时看**对数 RMSE**。
"""))

cells.append(code("""# ---- 训练/验证切分 + MLP 训练 ----
from torch import nn
from torch.utils import data as tdata

# 切训练/验证
n_val = 200
perm = np.random.permutation(n_train)
idx_val, idx_tr = perm[:n_val], perm[n_val:]
Xtr, ytr = torch.tensor(X_train[idx_tr]), torch.tensor(y[idx_tr])
Xva, yva = torch.tensor(X_train[idx_val]), torch.tensor(y[idx_val])

# 小 MLP
net = nn.Sequential(
    nn.Linear(X_all.shape[1], 128), nn.ReLU(), nn.Dropout(0.1),
    nn.Linear(128, 64), nn.ReLU(),
    nn.Linear(64, 1))

def log_rmse(net, X, y):
    with torch.no_grad():
        pred = net(X).squeeze()
        return float(torch.sqrt(((pred - y) ** 2).mean()))

loss_fn = nn.MSELoss()
opt = torch.optim.Adam(net.parameters(), lr=1e-2, weight_decay=1e-4)
train_ds = tdata.TensorDataset(Xtr, ytr)
train_iter = tdata.DataLoader(train_ds, batch_size=128, shuffle=True)

for epoch in range(80):
    net.train()
    for Xb, yb in train_iter:
        l = loss_fn(net(Xb).squeeze(), yb)
        opt.zero_grad(); l.backward(); opt.step()
    if epoch % 20 == 0 or epoch == 79:
        net.eval()
        print(f"epoch {epoch+1:3d}: 训练 logRMSE {log_rmse(net, Xtr, ytr):.4f}  验证 logRMSE {log_rmse(net, Xva, yva):.4f}")
"""))

cells.append(md("""## 3. 对测试集预测，生成提交文件

Kaggle 提交格式：`Id,SalePrice` 两列。预测值取回指数（因为标签取了 log）。
"""))

cells.append(code("""# ---- 预测并保存提交文件 ----
net.eval()
with torch.no_grad():
    test_pred = net(torch.tensor(X_test)).squeeze().numpy()
test_pred = np.exp(test_pred)   # log -> 原价

sub = pd.DataFrame({'Id': test_ids, 'SalePrice': test_pred})
sub_path = '../kaggle_house_submission.csv'
sub.to_csv(sub_path, index=False)
print(f"已保存 {len(sub)} 条预测到 {sub_path}")
print(sub.head())

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(7, 3.5))
ax.hist(test_pred, bins=40, color=蓝, edgecolor='k')
ax.set_xlabel('预测房价（美元）'); ax.set_ylabel('频数')
ax.set_title('测试集房价预测分布（长尾，符合房价真实分布）')
plt.show()
"""))

cells.append(md("""## 小结

| 步骤 | 关键点 |
| --- | --- |
| 下载数据 | d2l 镜像缓存到本地 |
| 特征预处理 | 数值标准化 + 类别独热 + 缺失填充，训练/测试一起处理 |
| 目标变换 | 房价取 `log`，长尾变正态，更好回归 |
| 训练 | MLP + MSE + Adam + 权重衰减 |
| 提交 | 预测值取 `exp` 还原，输出 `Id,SalePrice` |

> 🔑 **记忆**：表格竞赛流水线 = **下载 → 预处理（标准化+独热）→ 训练 → 预测 → 提交**。房价/金额类目标**先取 log**，是回归任务的标准技巧。真实竞赛提分靠更复杂的特征工程 + 树模型/集成。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\Kaggle-房价预测.ipynb", cells)
print("Kaggle-房价预测 ✔")

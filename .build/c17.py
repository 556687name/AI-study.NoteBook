# -*- coding: utf-8 -*-
CELLS = [
    ("markdown", r'''# 第十七章 模型评估：混淆矩阵、精确率、召回率、F1

> 📌 **出处**：⭐ **40 天计划补充**（计划 Day16「模型评估：混淆矩阵、P/R/F1」）。上一章训练完只看了「准确率」，但**准确率会骗人**。这一章讲清楚：面对一个分类模型，怎么正确地判断它到底好不好。

---

## 17.1 为什么「准确率」不够用？

准确率（accuracy）= 预测对的 / 总数。看起来直观，但遇到**类别不平衡**就彻底失灵。

经典例子：判断「某疾病」的模型，1000 人里只有 10 人患病。若模型**啥都不学、一律预测「没病」**，准确率高达 99%——但它一个病人都没抓出来，**毫无用处**。

问题根源：准确率把「没病的 990 人」和「有病的 10 人」**一视同仁**。而在很多场景里（疾病、欺诈、垃圾邮件），「少数的重要类别」才是我们真正关心的。

> 💡 所以我们需要**更细的评估指标**，它们都建立在一个基础工具上——**混淆矩阵**。
'''),
    ("markdown", r'''## 17.2 混淆矩阵：把「对错」拆成四种情况

**混淆矩阵（Confusion Matrix）** 把预测结果和真实标签交叉，分成四类。以「正类 = 患病」为例（🔑 四个词必须分清）：

| | 预测为正类 | 预测为负类 |
| --- | --- | --- |
| **真实为正类** | **TP**（真阳性：病人被查出） | **FN**（假阴性：病人被漏掉 ❌） |
| **真实为负类** | **FP**（假阳性：好人被误诊 ❌） | **TN**（真阴性：好人被排除） |

- **TP（True Positive）**：真阳性——正类预测成正类 ✅；
- **TN（True Negative）**：真阴性——负类预测成负类 ✅；
- **FP（False Positive）**：假阳性——负类被误报成正类 ❌（第一类错误，误报）；
- **FN（False Negative）**：假阴性——正类被漏报成负类 ❌（第二类错误，漏报）。

准确率 = $\frac{TP + TN}{TP + TN + FP + FN}$——它把四种情况混在一起，所以会掩盖「FN 很多」这种致命问题。
'''),
    ("code", r'''# ---- 混淆矩阵可视化 ----
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# 假设：真实标签（1=患病，0=健康）和模型预测
真实 = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0])
预测 = np.array([1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0])

cm = confusion_matrix(真实, 预测, labels=[0, 1])
print("混淆矩阵（行=真实，列=预测）：")
print("       预测0  预测1")
print(f"真实0   {cm[0,0]:4d}   {cm[0,1]:4d}")
print(f"真实1   {cm[1,0]:4d}   {cm[1,1]:4d}")

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['健康(0)', '患病(1)'])
disp.plot(cmap='Blues')
plt.title('混淆矩阵：对角线是对的分类，其他是错误')
plt.show()

# 解读：TP=6（病人被查出）、FN=3（病人漏诊）、FP=1（好人误诊）、TN=10（好人排除）。
'''),
    ("markdown", r'''## 17.3 精确率（Precision）与召回率（Recall）

从混淆矩阵的四个数，能提炼出两个「专门关注正类」的指标（🔑 核心）：

### 精确率 Precision = 预测的正类里，有多少是真对的

$$\text{Precision} = \frac{TP}{TP + FP}$$

它回答：**「模型说是正类的，有多少真的是正类？」** —— 衡量「**宁缺毋滥**」。Precision 高 = 不怎么冤枉好人（误报少）。

### 召回率 Recall = 真实的正类里，有多少被找出来了

$$\text{Recall} = \frac{TP}{TP + FN}$$

它回答：**「真实的正类，模型抓出了多少？」** —— 衡量「**宁错杀不放过**」。Recall 高 = 很少漏掉病人（漏报少）。

### 两者的「跷跷板」

Precision 和 Recall 常常**此消彼长**：把判断标准调严格（更难判成阳性），Precision 升、Recall 降；调宽松，Recall 升、Precision 降。

> 💡 怎么选，看业务：
> - **疾病筛查 / 欺诈检测**：要 **Recall 高**（宁可多查，不能漏诊）；
> - **垃圾邮件过滤 / 推荐**：要 **Precision 高**（宁可漏掉，不能误伤正常邮件）。
'''),
    ("code", r'''# ---- 精确率 / 召回率 / F1 计算 ----
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report

精确率 = precision_score(真实, 预测)
召回率 = recall_score(真实, 预测)
F1 = f1_score(真实, 预测)

print(f"精确率 Precision = {精确率:.3f}  （预测为正的里面，真的为正的比例）")
print(f"召回率 Recall   = {召回率:.3f}  （真实为正的里面，被找出来的比例）")
print(f"F1 分数         = {F1:.3f}\n")

# 一张表看全所有指标
print("完整分类报告（classification_report）：")
print(classification_report(真实, 预测, target_names=['健康', '患病'], zero_division=0))
'''),
    ("markdown", r'''## 17.4 F1 分数：Precision 和 Recall 的「调和平均」

Precision 和 Recall 单独看都片面，**F1 分数**把它们综合成一个数：

$$F_1 = \frac{2 \cdot P \cdot R}{P + R} = \frac{2}{\frac{1}{P} + \frac{1}{R}}$$

- 用的是**调和平均**（不是算术平均），所以**只要 P 或 R 有一个很低，F1 就会被拉低**——它「惩罚」单方面差劲，要求两者都高；
- 取值范围 [0, 1]，1 表示 P 和 R 都完美。

> 💡 F1 是「类别不平衡」场景下最常用的综合指标。除了 F1，还有给不同权重的一般形式 $F_\beta$（$\beta>1$ 偏重 Recall，$\beta<1$ 偏重 Precision）。
'''),
    ("markdown", r'''## 17.5 ROC 曲线与 AUC：衡量「排序」能力

还有一个重要的评估视角：模型输出的是**概率/分数**，而不只是硬分类。**ROC 曲线**和 **AUC** 衡量「模型把正类排在负类前面」的能力：

- **ROC 曲线**：横轴是「假阳性率 FPR」、纵轴是「真阳性率 TPR（= Recall）」，通过变化分类阈值画出一条曲线；
- **AUC**：ROC 曲线下的面积，取值 [0.5, 1]。AUC = 1 表示完美排序；AUC = 0.5 表示和瞎猜一样；AUC 越高，模型越能把正负类区分开。

> 💡 AUC 的好处：**不依赖具体阈值**，也不受「类别比例」影响，适合比较不同模型。但需要模型输出概率，所以要 `predict_proba` 或分数。
'''),
    ("code", r'''# ---- ROC 曲线与 AUC 演示 ----
from sklearn.metrics import roc_curve, auc

# 造两组"模型分数"：正类的分数应该普遍更高
np.random.seed(0)
正类分数 = np.random.randn(50) + 1.5      # 均值高
负类分数 = np.random.randn(50)            # 均值低
分数 = np.concatenate([负类分数, 正类分数])
标签 = np.array([0]*50 + [1]*50)

fpr, tpr, _ = roc_curve(标签, 分数)
auc值 = auc(fpr, tpr)

fig, ax = plt.subplots(figsize=(6.5, 6))
ax.plot(fpr, tpr, color=红, lw=2.5, label=f'ROC 曲线（AUC={auc值:.3f}）')
ax.plot([0, 1], [0, 1], color=灰, ls='--', lw=1.5, label='瞎猜（AUC=0.5）')
ax.set_xlabel('假阳性率 FPR'); ax.set_ylabel('真阳性率 TPR（=召回率）')
ax.set_title('ROC 曲线：越贴近左上角，区分能力越强')
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# 记忆点：AUC 越接近 1 越好，0.5 等于瞎猜；ROC 曲线越"拱"向左上角越好。
'''),
    ("markdown", r'''## 17.6 多分类的评估：微平均 / 宏平均

前面的 P/R/F1 都是**二分类**的。多分类怎么办？两种聚合方式：

- **宏平均（macro）**：先对**每个类**分别算 P/R/F1，再取**算术平均**——每个类**同等重要**（小类不被大类别淹没，适合类别不平衡）；
- **微平均（micro）**：把所有类的 TP/FP/FN **加起来**再统一算——按样本量加权，大类主导；
- **加权平均（weighted）**：按每个类的样本数加权平均。

`classification_report` 里三行都会给（macro avg / weighted avg 等）。看哪个，取决于「小类重不重要」。
'''),
    ("markdown", r'''## 17.7 本章小结

| 概念 | 一句话直觉 | 公式 |
| --- | --- | --- |
| 混淆矩阵 | 把预测拆成 TP/TN/FP/FN 四类 | —— |
| 准确率 | 对的比例（类别不平衡时会骗人） | (TP+TN)/总数 |
| 精确率 | 预测为正的里面，真的为正 | TP/(TP+FP) |
| 召回率 | 真实为正的里面，抓出多少 | TP/(TP+FN) |
| F1 | P 和 R 的调和平均 | 2PR/(P+R) |
| AUC | 区分正负类的排序能力 | ROC 下面积 |

🔑 **记忆**：精确率看「误报」、召回率看「漏报」；筛查重召回、过滤重精确；类别不平衡看 F1/AUC 而不是准确率。

> 📌 **下一步**：第十八章讲**迁移学习**——不再从零训练，而是「站在巨人的肩膀上」复用预训练模型（40 天计划重点）。
'''),
]

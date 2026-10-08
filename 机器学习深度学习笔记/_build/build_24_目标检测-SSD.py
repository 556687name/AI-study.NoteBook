# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# 目标检测 · 边界框 / 锚框 / IoU / NMS（PyTorch）

> 📌 **出处**：李沐《动手学深度学习 V2》第 13 章「目标检测 / 锚框 / SSD」
> 🎯 **目标**：搞懂目标检测的四个地基——**边界框、锚框、IoU、NMS**——并可视化理解 SSD 的思路。完整 SSD 训练需 GPU + COCO 数据集，这里把核心部件逐个实现。

## 目标检测在做什么

分类只回答「图里是什么」，检测还要回答「**在哪**」：输出若干**边界框 + 类别 + 置信度**。
"""))

cells.append(code(ENV))

cells.append(md("""## 1. 边界框：两种表示方式

框可用「中心 + 宽高」`(cx, cy, w, h)` 或「左上 + 右下」`(x1, y1, x2, y2)` 表示，两者可互换。
"""))

cells.append(code("""# ---- 边界框两种表示的互转 ----
def corner_to_center(boxes):
    # (x1, y1, x2, y2) -> (cx, cy, w, h)
    x1, y1, x2, y2 = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
    return torch.stack([(x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1], dim=1)

def center_to_corner(boxes):
    # (cx, cy, w, h) -> (x1, y1, x2, y2)
    cx, cy, w, h = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
    return torch.stack([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], dim=1)

import matplotlib.pyplot as plt
# 画两个框（一只猫 + 一只狗）
fig, ax = plt.subplots(figsize=(5, 5))
boxes = torch.tensor([[0.1, 0.1, 0.5, 0.5], [0.55, 0.4, 0.9, 0.8]])  # (x1,y1,x2,y2)
for i, b in enumerate(boxes):
    ax.add_patch(plt.Rectangle((b[0], b[1]), b[2]-b[0], b[3]-b[1],
                 fill=False, edgecolor=[蓝, 红][i], lw=2))
    cx, cy, w, h = corner_to_center(b.unsqueeze(0))[0]
    ax.plot(cx.item(), cy.item(), 'o', color=[蓝, 红][i])
    ax.text(cx, cy, f"中心({cx:.2f},{cy:.2f})", fontsize=9)
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect('equal')
ax.set_title("边界框：中心点 + 宽高 定位物体")
plt.show()
print("角点表示：", boxes[0].tolist(), " -> 中心表示：", corner_to_center(boxes[:1]).tolist())
"""))

cells.append(md("""## 2. IoU 交并比：衡量两个框「重叠多少」

$$\\text{IoU}(A, B) = \\frac{|A \\cap B|}{|A \\cup B|}$$

IoU 是「预测框对不对」的评判标准（一般 IoU > 0.5 算预测正确）。
"""))

cells.append(code("""# ---- IoU 计算 ----
def box_iou(boxes1, boxes2):
    # 输入都是 (n, 4) 的角点表示，输出 (len(boxes1), len(boxes2))
    lt = torch.max(boxes1[:, None, :2], boxes2[:, :2])    # 交集的左上
    rb = torch.min(boxes1[:, None, 2:], boxes2[:, 2:])    # 交集的右下
    wh = (rb - lt).clamp(min=0)                            # 交集宽高
    inter = wh[:, :, 0] * wh[:, :, 1]                     # 交集面积
    area1 = (boxes1[:, 2] - boxes1[:, 0]) * (boxes1[:, 3] - boxes1[:, 1])
    area2 = (boxes2[:, 2] - boxes2[:, 0]) * (boxes2[:, 3] - boxes2[:, 1])
    return inter / (area1[:, None] + area2 - inter + 1e-6)

A = torch.tensor([[0.0, 0.0, 0.6, 0.6]])
B = torch.tensor([[0.2, 0.2, 0.8, 0.8]])
print("两个框的 IoU：", f"{box_iou(A, B).item():.3f}（交集 / 并集）")
"""))

cells.append(md("""## 3. 锚框：密集撒「候选框」

检测器在特征图每个位置生成**多个预设框**（不同尺度 s、不同宽高比 r），网络再预测「这个锚框里有没有物体、是什么、框怎么微调」。
"""))

cells.append(code("""# ---- 生成锚框：每个位置 × 多个尺度/宽高比 ----
def generate_anchors(feature_size, scales=(0.5, 0.8, 1.2), ratios=(0.5, 1.0, 2.0)):
    anchors = []
    H, W = feature_size
    for i in range(H):
        for j in range(W):
            cy, cx = (i + 0.5) / H, (j + 0.5) / W   # 中心归一化
            for s in scales:
                for r in ratios:
                    w = s * (r ** 0.5); h = s / (r ** 0.5)   # 宽高比 r 的框
                    anchors.append((cx, cy, min(w, 1), min(h, 1)))
    return anchors

anchors = generate_anchors((3, 3), scales=(0.4, 0.7), ratios=(0.5, 1.0, 2.0))
print(f"3×3 特征图生成 {len(anchors)} 个锚框（每位置 2×3=6 个）")

# 可视化一个位置的 6 个锚框
fig, ax = plt.subplots(figsize=(4, 4))
cx, cy = 0.5, 0.5
for s in (0.4, 0.7):
    for r in (0.5, 1.0, 2.0):
        w, h = s * (r ** 0.5), s / (r ** 0.5)
        ax.add_patch(plt.Rectangle((cx - w/2, cy - h/2), w, h, fill=False, edgecolor=蓝, lw=1))
ax.plot(cx, cy, 'o', color=红)
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect('equal')
ax.set_title("一个位置上的 6 个锚框（2 尺度 × 3 宽高比）")
plt.show()
"""))

cells.append(md("""## 4. NMS 非极大值抑制：删掉重叠的重复框

检测器常对同一物体输出一堆重叠框。**NMS** 按置信度排序，保留最高分，删掉与它 IoU 过大的冗余框。
"""))

cells.append(code("""# ---- NMS 实现 ----
def nms(boxes, scores, iou_threshold=0.5):
    order = scores.argsort(descending=True).tolist()   # 按分数降序
    keep = []
    while order:
        i = order.pop(0)                                # 取最高分
        keep.append(i)
        order = [j for j in order if box_iou(boxes[i:i+1], boxes[j:j+1]).item() < iou_threshold]
    return keep

# 造 5 个重叠的框（模拟检测器对同一只猫输出 5 个框）
boxes = torch.tensor([
    [0.1, 0.1, 0.5, 0.5], [0.12, 0.1, 0.52, 0.48], [0.15, 0.12, 0.5, 0.5],
    [0.6, 0.6, 0.9, 0.9], [0.08, 0.15, 0.48, 0.55]])
scores = torch.tensor([0.9, 0.75, 0.6, 0.95, 0.5])

keep = nms(boxes, scores, iou_threshold=0.5)
fig, axes = plt.subplots(1, 2, figsize=(8, 4))
for ax, idxs, title in [(axes[0], range(5), "NMS 前：一堆重叠框"),
                        (axes[1], keep, "NMS 后：每物体留一个")]:
    for i in idxs:
        b = boxes[i]
        ax.add_patch(plt.Rectangle((b[0], b[1]), b[2]-b[0], b[3]-b[1],
                     fill=False, edgecolor=蓝, lw=2))
        ax.text(b[0], b[1], f"{scores[i]:.2f}", fontsize=9, color=红)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect('equal'); ax.set_title(title)
plt.show()
print("保留的框索引：", keep)
"""))

cells.append(md("""## 5. SSD 的整体思路（完整训练需 GPU）

**SSD（单发多框检测）** = 骨干 CNN + 多尺度特征图上的锚框 + 两个预测头：

1. 骨干网络提取特征；
2. 在**多个尺度**的特征图上各设锚框（浅层大图抓小物体，深层小图抓大物体）；
3. 每个锚框预测「**类别分数**」和「**框偏移量**」，一次前向全部输出；
4. 训练用锚框和真实框配对的 IoU 做正负样本匹配；推理用 NMS 去重。

> 💡 检测器分**单阶段**（SSD、YOLO：直接回归，快）和**两阶段**（R-CNN 系列：先提候选再精修，准）。YOLO 是实时检测的主流。

## 小结

| 概念 | 一句话直觉 |
| --- | --- |
| 边界框 | 中心+宽高 或 左上+右下 定位物体 |
| 锚框 | 密集预设的候选框，多尺度多宽高比 |
| IoU | 交并比，判断框对不对 |
| NMS | 按分数排序，删掉重叠的冗余框 |

> 🔑 **记忆**：检测四件套 **框（bbox）→ 锚框（anchor）→ IoU（评判）→ NMS（去重）**。SSD/YOLO 都是「一次前向，对密集锚框同时预测类别+偏移」，再 NMS 收尾。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\目标检测-SSD.ipynb", cells)
print("目标检测-SSD ✔")

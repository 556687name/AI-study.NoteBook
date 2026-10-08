# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# 风格迁移 · 内容损失 + 风格损失（PyTorch）

> 📌 **出处**：李沐《动手学深度学习 V2》第 13 章「风格迁移」
> 🎯 **目标**：用预训练 VGG19 当特征提取器，把「内容图的内容」+「风格图的风格」合成一张新图——理解 **内容损失（特征匹配）** 和 **风格损失（Gram 矩阵匹配）**。

## 核心思想

- **内容损失**：生成图在某层特征要**接近**内容图（保留「画的是什么」）；
- **风格损失**：生成图各层特征的 **Gram 矩阵**要接近风格图（保留「颜色/纹理怎么分布」）；
- 直接优化**生成图的像素**，让两个损失都最小。
"""))

cells.append(code(ENV))

cells.append(code("""# ---- 加载预训练 VGG19（特征提取器，冻结）----
import torchvision
from torch import nn
import torch.nn.functional as F

vgg = torchvision.models.vgg19(weights=torchvision.models.VGG19_Weights.IMAGENET1K_V1).features.eval()
for p in vgg.parameters():
    p.requires_grad = False
print("VGG19 特征提取器加载完成 ✔")

# 关键层索引：内容用 relu4_2，风格用 relu1_1~relu5_1
content_layer = [22]
style_layers = [1, 6, 11, 20, 29]
"""))

cells.append(md("""## 1. 准备内容图和风格图

内容图：一张 Fashion-MNIST 的衣服图（放大到 224×224）；风格图：彩色条纹图案。
"""))

cells.append(code("""# ---- 构造内容图（Fashion-MNIST 放大）+ 风格图（彩色条纹）----
from torchvision import datasets, transforms
import matplotlib.pyplot as plt

# 内容图：取一张 T-shirt，放大到 224，转 3 通道
content_pil = datasets.FashionMNIST(root='../data', train=True, download=True)[1][0]
content_pil = content_pil.resize((224, 224))
content_t = transforms.ToTensor()(content_pil).repeat(3, 1, 1).unsqueeze(0)   # (1,3,224,224)

# 风格图：彩色竖条纹
style = np.zeros((224, 224, 3), dtype=np.float32)
for x in range(224):
    style[:, x, :] = [0.9, 0.4, 0.2] if (x // 28) % 2 == 0 else [0.2, 0.4, 0.9]   # 橙/蓝相间
style_t = torch.from_numpy(style).permute(2, 0, 1).unsqueeze(0)

fig, axes = plt.subplots(1, 2, figsize=(7, 3))
axes[0].imshow(content_t[0].permute(1, 2, 0)); axes[0].set_title("内容图（衣服）"); axes[0].axis('off')
axes[1].imshow(style_t[0].permute(1, 2, 0)); axes[1].set_title("风格图（橙蓝条纹）"); axes[1].axis('off')
plt.show()
"""))

cells.append(md("""## 2. 特征提取 + Gram 矩阵

用 hook 一次前向抓取多个层的特征；**Gram 矩阵**刻画了「哪些通道一起被激活」——即纹理/颜色风格。
"""))

cells.append(code("""# ---- 提取指定层特征（hook）----
def extract_features(x, layers):
    feats = {}
    handles = []
    def make_hook(k):
        def h(m, inp, out): feats[k] = out
        return h
    for k in layers:
        handles.append(vgg[k].register_forward_hook(make_hook(k)))
    vgg(x)
    for h in handles: h.remove()
    return feats

def gram(f):
    b, c, h, w = f.shape
    F = f.view(c, h * w)
    return F @ F.T / (c * h * w)

def style_loss(gen_feats, style_feats):
    return sum(((gram(gen_feats[k]) - gram(style_feats[k])) ** 2).mean() for k in style_feats)

# 预计算内容/风格特征
content_feats = extract_features(content_t, content_layer)
style_feats = extract_features(style_t, style_layers)
print("内容特征层：", [f.shape for f in content_feats.values()])
print("风格特征层数：", len(style_feats))
"""))

cells.append(md("""## 3. 优化生成图：内容损失 + 风格损失

生成图初始化为内容图，用 Adam 直接优化像素，逐步「染上」条纹风格。
"""))

cells.append(code("""# ---- 风格迁移优化 ----
gen = content_t.clone().requires_grad_(True)
opt = torch.optim.Adam([gen], lr=0.05)
content_weight, style_weight = 1.0, 1e5

for it in range(120):
    gen_feats_all = extract_features(gen, content_layer + style_layers)
    c_loss = ((gen_feats_all[22] - content_feats[22]) ** 2).mean()          # 内容损失
    s_loss = style_loss(gen_feats_all, style_feats)                          # 风格损失
    total = content_weight * c_loss + style_weight * s_loss
    opt.zero_grad(); total.backward(); opt.step()
    gen.data.clamp_(0, 1)
    if it % 30 == 0:
        print(f"迭代 {it:3d}: 内容损失 {c_loss.item():.4f}  风格损失 {s_loss.item():.6f}")

fig, axes = plt.subplots(1, 3, figsize=(10, 3))
axes[0].imshow(content_t[0].permute(1, 2, 0)); axes[0].set_title("内容图"); axes[0].axis('off')
axes[1].imshow(style_t[0].permute(1, 2, 0)); axes[1].set_title("风格图"); axes[1].axis('off')
axes[2].imshow(gen[0].detach().permute(1, 2, 0)); axes[2].set_title("风格迁移结果"); axes[2].axis('off')
plt.show()
"""))

cells.append(md("""## 小结

| 概念 | 一句话直觉 |
| --- | --- |
| 内容损失 | 生成图与内容图在深层特征要接近 |
| 风格损失 | 生成图与风格图的 Gram 矩阵要接近 |
| Gram 矩阵 | 刻画「哪些通道一起激活」= 纹理/颜色风格 |
| 优化对象 | 直接优化生成图的像素，而非网络权重 |

> 🔑 **记忆**：风格迁移 = **内容损失（特征 MSE）+ 风格损失（Gram MSE）**，用预训练 CNN 当特征提取器，直接优化像素。这个「用预训练网络提取特征算损失」的思路，也被后来的感知损失/GAN 广泛借鉴。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\风格迁移.ipynb", cells)
print("风格迁移 ✔")

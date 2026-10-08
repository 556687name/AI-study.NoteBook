# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import md, code, save_nb, ENV

cells = []

cells.append(md("""# 语义分割 · 转置卷积与 FCN（PyTorch）

> 📌 **出处**：李沐《动手学深度学习 V2》第 13 章「转置卷积 / 全卷积网络 FCN」
> 🎯 **目标**：理解「小特征图 → 大标签图」的**转置卷积**，并用一个**编码器-解码器 FCN** 完成一个像素级分割任务。

## 语义分割 = 逐像素分类

分类输出「一个标签」，分割输出「**和输入同尺寸的标签图**」，每个像素都判断属于哪一类。
"""))

cells.append(code(ENV))

cells.append(md("""## 1. 转置卷积：把「小图」放大成「大图」

普通卷积下采样（大→小），转置卷积上采样（小→大）：把每个像素按卷积核权重「扩散」到更大区域。
"""))

cells.append(code("""# ---- 转置卷积上采样演示 ----
from torch import nn

# 一个 4×4 的小特征图，转置卷积放大到 8×8
small = torch.rand(1, 1, 4, 4)
upconv = nn.ConvTranspose2d(1, 1, kernel_size=3, stride=2, padding=1, output_padding=1)
big = upconv(small)
print("输入特征图：", tuple(small.shape), " -> 转置卷积输出：", tuple(big.shape))

import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(7, 3))
axes[0].imshow(small[0, 0].numpy(), cmap='viridis'); axes[0].set_title("输入 4×4")
axes[1].imshow(big[0, 0].detach().numpy(), cmap='viridis'); axes[1].set_title("转置卷积输出 8×8")
plt.suptitle("转置卷积：把小特征图上采样回大图")
plt.show()
"""))

cells.append(md("""## 2. 一个小的 FCN：编码器（卷积+池化）+ 解码器（转置卷积+跳跃连接）

- 编码器逐层**下采样**提取语义；
- 解码器用转置卷积**上采样**恢复尺寸；
- **跳跃连接**把浅层细节拼到深层，让分割边界更精细。
"""))

cells.append(code("""# ---- 定义小 FCN（编码器-解码器 + 跳跃连接）----
class SmallFCN(nn.Module):
    def __init__(self):
        super().__init__()
        # 编码器（下采样）
        self.enc1 = nn.Sequential(nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2))   # 32->16
        self.enc2 = nn.Sequential(nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2))  # 16->8
        self.enc3 = nn.Sequential(nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2))  # 8->4
        # 解码器（上采样）
        self.up1 = nn.ConvTranspose2d(64, 32, 2, stride=2)   # 4->8
        self.up2 = nn.ConvTranspose2d(32, 16, 2, stride=2)   # 8->16
        self.up3 = nn.ConvTranspose2d(16, 8, 2, stride=2)    # 16->32
        self.head = nn.Conv2d(8, 2, 1)                        # 每像素 2 类
    def forward(self, x):
        x1 = self.enc1(x)          # (16,16,16)
        x2 = self.enc2(x1)         # (32,8,8)
        x3 = self.enc3(x2)         # (64,4,4)
        y = self.up1(x3)           # (32,8,8)
        y = self.up2(y + x2)       # (16,16,16)  🔑 跳跃连接
        y = self.up3(y + x1)       # (8,32,32)
        return self.head(y)        # (2,32,32)

net = SmallFCN()
X = torch.rand(1, 1, 32, 32)
print("输入 32×32 图 -> 输出：", tuple(net(X).shape), "（2 通道 = 每像素前景/背景分数）")
"""))

cells.append(md("""## 3. 训练：分割圆形区域

造一个合成数据集：每张 32×32 图里有一个随机圆（前景=1，背景=0），训练 FCN 输出每个像素的类别。
"""))

cells.append(code("""# ---- 合成分割数据：随机圆 ----
def make_seg_data(n, size=32):
    X = np.zeros((n, 1, size, size), dtype=np.float32)
    Y = np.zeros((n, size, size), dtype=np.int64)
    for i in range(n):
        cx, cy = np.random.randint(6, size - 6, size=2)
        r = np.random.randint(5, 10)          # 更大的圆，前景占比更高
        yy, xx = np.mgrid[0:size, 0:size]
        mask = (xx - cx) ** 2 + (yy - cy) ** 2 <= r ** 2
        X[i, 0] = mask; Y[i] = mask
    return torch.tensor(X), torch.tensor(Y)

X_train, Y_train = make_seg_data(800)
X_test, Y_test = make_seg_data(200)
print("训练样本：", X_train.shape, " 标签：", Y_train.shape)
"""))

cells.append(code("""# ---- 训练 FCN（小批量逐像素交叉熵，给前景类更高权重）----
from torch.utils import data as tdata
train_loader = tdata.DataLoader(tdata.TensorDataset(X_train, Y_train), batch_size=64, shuffle=True)

loss_fn = nn.CrossEntropyLoss(weight=torch.tensor([0.5, 2.0]))  # 前景类少，加大权重
opt = torch.optim.Adam(net.parameters(), lr=1e-3)

for epoch in range(10):
    net.train()
    for Xb, Yb in train_loader:
        logits = net(Xb)                 # (B, 2, 32, 32)
        l = loss_fn(logits, Yb)          # 逐像素分类损失
        opt.zero_grad(); l.backward(); opt.step()
    if epoch in (0, 4, 9):
        net.eval()
        with torch.no_grad():
            pred = net(X_test).argmax(1)
            acc = (pred == Y_test).float().mean().item()
            fg = (Y_test == 1)           # 只看前景（圆）像素
            fg_acc = (pred[fg] == 1).float().mean().item()
        print(f"epoch {epoch+1:2d}: 整体准确率 {acc:.4f}  前景准确率 {fg_acc:.4f}")

# 可视化：输入 / 真实掩码 / 预测掩码
net.eval()
with torch.no_grad():
    pred = net(X_test[:1]).argmax(1)[0].numpy()
fig, axes = plt.subplots(1, 3, figsize=(9, 3))
axes[0].imshow(X_test[0, 0], cmap='gray'); axes[0].set_title("输入图")
axes[1].imshow(Y_test[0], cmap='gray'); axes[1].set_title("真实掩码")
axes[2].imshow(pred, cmap='gray'); axes[2].set_title("预测掩码")
for a in axes: a.axis('off')
plt.suptitle("语义分割：逐像素预测圆形区域")
plt.show()
"""))

cells.append(md("""## 小结

| 概念 | 一句话直觉 |
| --- | --- |
| 语义分割 | 逐像素分类，输出同尺寸标签图 |
| 转置卷积 | 上采样：小特征图放大成大图 |
| 编码器-解码器 | 先下采样提语义，再上采样恢复尺寸 |
| 跳跃连接 | 融合浅层细节，边界更精细 |

> 🔑 **记忆**：分割 = **下采样提特征 + 转置卷积上采样 + 跳跃连接**，这个「编码器-解码器 + skip」结构就是 **U-Net**，是医学影像/语义分割的标准范式。
"""))

save_nb(r"D:\NoteBook\机器学习深度学习笔记\实战代码_李沐\语义分割-FCN.ipynb", cells)
print("语义分割-FCN ✔")

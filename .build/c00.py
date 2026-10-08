# -*- coding: utf-8 -*-
CELLS = [
    ("markdown", r'''# 📘 机器学习 + 深度学习 基础完整笔记

> 一份**自包含、可运行、带可视化与记忆标记**的完整学习笔记，覆盖机器学习与深度学习的全部基础内容。

## 课程来源

- 📺 **主课程**：2026 李宏毅机器学习入门（B 站，共 67 讲）
  👉 https://www.bilibili.com/video/BV1RnikBvE8m
- 📺 **辅助教材**：李沐《动手学深度学习 V2》（PyTorch 版，用于补充 PyTorch 实战）
  👉 https://www.bilibili.com/video/BV1EY6FBwE8P
- 🎯 **结合材料**：`暑假40天学习计划_张豪实验室_米哈游游戏测试.docx`（第三阶段「机器学习入门 + PyTorch 实战」）

## 笔记结构

- **第一部分：机器学习基础**（课程主线）—— 第一章 ~ 第十章
- **第二部分：深度学习**（课程主线）—— 第十一章 ~ 第十三章
- **第三部分：PyTorch 实战与进阶**（40 天计划补充）—— 第十四章 ~ 第十九章
- **附录**：公式速查表 + 记忆清单

## 使用说明

1. 请从**第一个代码单元格**开始**按顺序运行**，后面的代码会复用前面定义好的变量与函数；
2. 每个代码单元格都加了详细注释，标了 `🔑 记忆` 的写法是需要背下来的；
3. 图表全部用 matplotlib 绘制，`plt.rcParams` 已配好中文显示。

## 标记说明

| 标记 | 含义 |
| --- | --- |
| 📌 **出处** | 这段内容来自课程哪一讲 / 哪个视频 / 40 天计划哪一天 |
| 🔑 **记忆** | 需要**背下来**的公式、代码写法、关键结论 |
| ⭐ | 40 天学习计划点名的**重点**（对应实验室 / 米哈游岗位要求） |
| 💡 | 补充的直觉理解 / 易错点提醒 |

---
'''),
    ("code", r'''# ==================== 环境准备（全笔记的第一个代码单元格）====================
# 后面所有章节都会复用这里导入的库、字体设置和配色，请务必先运行本格。

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 让 matplotlib 能正常显示中文（Windows 常见字体）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'PingFang SC', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False   # 让负号 "-" 正常显示

# 全笔记统一配色（风格一致，方便看图）
蓝 = '#2b7bba'   # 主色：数据点 / 类别 A
橙 = '#e69f00'   # 强调：拟合线 / 类别 B
灰 = '#999999'   # 辅助：真实值 / 背景
红 = '#d62728'   # 警示：发散 / 过拟合
绿 = '#2ca02c'   # 成功：收敛 / 正确
紫 = '#9467bd'   # 第三类

np.random.seed(0)   # 固定随机种子，保证结果可复现

print("✓ 环境准备完成：numpy", np.__version__, "| matplotlib", plt.matplotlib.__version__)
'''),
]

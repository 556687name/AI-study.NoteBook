# -*- coding: utf-8 -*-
"""更新目录：23 章、ch3/ch7 新小节、新增 ch22/ch23。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb import load_nb, save_json

NB = r"D:\NoteBook\机器学习深度学习笔记\机器学习深度学习完整笔记.ipynb"
nb = load_nb(NB)
src = "".join(nb["cells"][2]["source"])

# 1. 章节总数
src = src.replace("共 **21 章 + 附录**", "共 **23 章 + 附录**")

# 2. ch3：3.7 模型验证 + 3.8 小结
src = src.replace(
    "- 3.6 交叉验证 Cross-Validation\n- 3.7 本章小结",
    "- 3.6 交叉验证 Cross-Validation\n- 3.7 模型验证：训练/验证/测试 + K 折 + 学习曲线（李沐 实用ML）\n- 3.8 本章小结",
)

# 3. ch7：7.7 数据获取/EDA/清理 + 7.8 小结
src = src.replace(
    "- 7.6 特征选择\n- 7.7 本章小结",
    "- 7.6 特征选择\n- 7.7 数据获取、EDA 与数据清理（李沐 实用ML）\n- 7.8 本章小结",
)

# 4. 新增 ch22 / ch23（接在 ch21 之后）
src = src.replace(
    "- 21.4 seq2seq 与机器翻译\n\n---\n\n## 附录",
    """- 21.4 seq2seq 与机器翻译

**第二十二章 计算机视觉实战：目标检测 / 语义分割 / 风格迁移**（d2l 第 13 章）
- 22.1 计算机视觉的四大任务
- 22.2 目标检测：边界框与锚框
- 22.3 IoU 与非极大值抑制 NMS
- 22.4 单发多框检测 SSD
- 22.5 语义分割与转置卷积
- 22.6 全卷积网络 FCN
- 22.7 风格迁移：内容 + 风格损失

**第二十三章 树模型与集成学习**（李沐《实用机器学习》）
- 23.1 为什么表格数据用树模型
- 23.2 决策树：递归切分
- 23.3 随机森林：并行投票（降方差）
- 23.4 梯度提升树 GBDT：串行补漏（降偏差）
- 23.5 集成三大流派对比
- 23.6 树模型 vs 深度学习：怎么选
- 23.7 本章小结

---

## 附录""",
)

nb["cells"][2]["source"] = src.splitlines(keepends=True)
save_json(nb, NB)
print("目录更新完成 ✔")

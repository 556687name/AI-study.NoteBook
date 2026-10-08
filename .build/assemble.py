# -*- coding: utf-8 -*-
"""把所有章节组装成一个完整的大笔记 .ipynb。

运行方式（在 D:\\NoteBook\\.build 目录下）：
    python assemble.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _builder import build

# 章节顺序：封面 → 目录 → 第1~19章 → 附录
import c00, toc
import c01, c02, c03, c04, c05, c06, c07, c08, c09, c10
import c11, c12, c13
import c14, c15, c16, c17, c18, c19
import cap

章节列表 = [c00, toc, c01, c02, c03, c04, c05, c06, c07, c08, c09, c10,
            c11, c12, c13, c14, c15, c16, c17, c18, c19, cap]

# 合并所有 cells
all_cells = []
for 模块 in 章节列表:
    all_cells.extend(模块.CELLS)

# 输出路径：放回上级目录的 机器学习深度学习笔记 文件夹
输出目录 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '机器学习深度学习笔记')
os.makedirs(输出目录, exist_ok=True)
输出文件 = os.path.join(输出目录, '机器学习深度学习完整笔记.ipynb')

build(输出文件, all_cells)

print(f"✅ 组装完成：共 {len(all_cells)} 个单元格")
print(f"   输出文件：{os.path.abspath(输出文件)}")
print(f"   各章单元格数：", {f'c{i:02d}': len(getattr(模块, 'CELLS')) for i, 模块 in enumerate(章节列表, start=0)})

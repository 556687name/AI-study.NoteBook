# -*- coding: utf-8 -*-
"""notebook 构建辅助：生成独立 notebook、向现有 notebook 插入单元格。"""
import json

def md(text):
    """markdown 单元格"""
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}

def code(text):
    """代码单元格"""
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": text.splitlines(keepends=True)}

def new_nb(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.13"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

def save_nb(path, cells):
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(new_nb(cells), f, ensure_ascii=False, indent=1)
    print(f"saved {path}  ({len(cells)} cells)")

def load_nb(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(nb, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print(f"updated {path}  ({len(nb['cells'])} cells)")

# 统一的环境准备代码块（每个独立 notebook 开头）
ENV = '''# ==================== 环境准备 ====================
import torch
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'PingFang SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

蓝 = '#2b7bba'; 橙 = '#e69f00'; 灰 = '#999999'; 红 = '#d62728'; 绿 = '#2ca02c'; 紫 = '#9467bd'
np.random.seed(0); torch.manual_seed(0)

print("✓ 环境就绪：torch", torch.__version__)
'''

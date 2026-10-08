# -*- coding: utf-8 -*-
"""把 (cell_type, source) 列表构建成 Jupyter notebook 的辅助工具。"""
import json

META = {
    "kernelspec": {"display_name": "Python 3 (ipykernel)", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.10.20"},
}


def build(path, cells):
    out = []
    for i, (kind, src) in enumerate(cells):
        cell = {"cell_type": kind, "metadata": {}, "id": "c%03d" % i}
        if kind == "code":
            cell["execution_count"] = None
            cell["outputs"] = []
        cell["source"] = src.splitlines(True)
        out.append(cell)
    nb = {"cells": out, "metadata": META, "nbformat": 4, "nbformat_minor": 5}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print("wrote", path, "(%d cells)" % len(out))

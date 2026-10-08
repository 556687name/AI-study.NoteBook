# -*- coding: utf-8 -*-
"""修复 notebook 里 BatchNorm 小节被转义污染的 $\beta$（backspace → beta）。"""
import json

P = r"D:\NoteBook\机器学习深度学习笔记\机器学习深度学习完整笔记.ipynb"
nb = json.load(open(P, encoding="utf-8"))

fixed = 0
for c in nb["cells"]:
    src = "".join(c["source"])
    if chr(8) in src:  # backspace
        src = src.replace("$" + chr(8) + "eta$", "$\\beta$")
        c["source"] = src.splitlines(keepends=True)
        fixed += 1

json.dump(nb, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# 验证
nb2 = json.load(open(P, encoding="utf-8"))
src = "".join(nb2["cells"][134]["source"])
print("修复 cell 数:", fixed)
print("beta 处:", src[src.find("可学习参数"):src.find("可学习参数") + 30])
print("含 backspace?", chr(8) in src)

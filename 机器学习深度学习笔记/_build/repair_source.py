# -*- coding: utf-8 -*-
"""修复 build_merge_03.py 源文件：把 BatchNorm 小节里单反斜杠的 $\gamma$ / $\beta$ 改成双反斜杠，
使 Python 解析后得到单反斜杠（与其他 build 脚本的 \\text 约定一致）。"""
import io

BS = chr(92)  # 单个反斜杠
P = "build_merge_03.py"
s = io.open(P, encoding="utf-8").read()

old = "可学习参数** $" + BS + "gamma$（缩放）和 $" + BS + "beta$（平移）拉回合适尺度"
new = "可学习参数** $" + BS + BS + "gamma$（缩放）和 $" + BS + BS + "beta$（平移）拉回合适尺度"

assert old in s, "未找到目标串（可能已被修复或内容有差异）"
s = s.replace(old, new)
io.open(P, "w", encoding="utf-8").write(s)

# 验证：重新读回，确认该行现在是双反斜杠
for i, l in enumerate(io.open(P, encoding="utf-8").read().splitlines()):
    if "可学习参数" in l:
        seg = l[l.find("参数"):l.find("参数") + 30]
        print("修复后行", i, ":", seg)
        print("该段含反斜杠数:", seg.count(BS))
print("源脚本修复完成 ✔")

# -*- coding: utf-8 -*-
"""执行一个 notebook 的所有代码单元格，验证可运行。用法：python verify.py <nb路径>"""
import sys, json, io, contextlib
import matplotlib
matplotlib.use("Agg")  # 无界面后端，避免 plt.show() 阻塞

def main(path):
    nb = json.load(open(path, encoding="utf-8"))
    g = {"__name__": "__main__"}
    n_code = 0
    for i, c in enumerate(nb["cells"]):
        if c["cell_type"] != "code":
            continue
        src = "".join(c["source"])
        n_code += 1
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                exec(compile(src, f"<cell {i}>", "exec"), g)
            out = buf.getvalue().strip()
            tail = (" | " + out.replace("\n", " ")[:120]) if out else ""
            print(f"[cell {i}] OK{tail}")
        except Exception as e:
            print(f"[cell {i}] FAIL -> {type(e).__name__}: {e}")
            return 1
    print(f"\n全部 {n_code} 个代码单元格运行通过 ✔")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))

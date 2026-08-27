#!/usr/bin/env python3
"""Generate deterministic NN-09--12 textbook figures.

The plates use the shared paper-and-ink palette while giving each concept a
different visual grammar: executable graph, operator action, reverse ledger,
and differential/adjoint accounting.  Only the Python standard library is
required.
"""

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "neural-networks"


def computation_graph_forward():
    out = begin(
        "计算图：从依赖关系到可回放的执行记录",
        "共享输入形成 fan-out；拓扑调度只执行已就绪算子；tape 还需保存形状、缓存、随机状态与存储版本。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "表达式展开为 DAG", BLUE)
    pts = {
        "x₁": (78, 235), "x₂": (78, 380), "×": (205, 325),
        "sin": (205, 150), "+": (315, 235), "sq": (365, 235),
    }
    for label, (x, y) in pts.items():
        color = BLUE if label.startswith("x") else TEAL if label in ("×", "sin", "+") else RED
        out += [circle(x, y, 24, color, BG, 2.5), text(x, y + 6, label, 16, 700, "middle", color)]
    for a, b in (("x₁", "sin"), ("x₁", "×"), ("x₂", "×"), ("sin", "+"), ("×", "+"), ("+", "sq")):
        x1, y1 = pts[a]; x2, y2 = pts[b]
        out += [line(x1 + 24, y1, x2 - 26, y2, INK, 2.2, marker="a3")]
    out += [text(45, 445, "a=x₁x₂; b=sin x₁; c=a+b; L=c²", 16, 650, cls="math")]
    out += [text(45, 482, "x₁ 只有一个 value，但被两条分支读取。", 15, fill=MUTED)]

    heading(out, 430, "B", "Kahn 调度：ready 才可执行", TEAL)
    rows = (
        (112, "0", "{x₁,x₂}", "read inputs"),
        (192, "1", "{sin,×}", "independent"),
        (272, "2", "{+}", "both parents ready"),
        (352, "3", "{sq}", "loss ready"),
    )
    out += [text(442, 94, "step", 15, 700, fill=TEAL), text(510, 94, "ready set", 15, 700, fill=TEAL), text(650, 94, "meaning", 15, 700, fill=TEAL)]
    out += [line(435, 102, 765, 102, TEAL, 2)]
    for y, step, ready, meaning in rows:
        out += [text(450, y + 24, step, 17, 700, fill=BLUE), rect(500, y, 125, 42, TEAL, "#ECFDF5", 6, 2), text(562, y + 27, ready, 15, 650, "middle", TEAL), text(645, y + 27, meaning, 15, 500)]
    out += [text(438, 442, "输出数 < |V|  ⇒  剩余子图含 cycle", 16, 700, fill=RED)]
    out += [text(438, 480, "合法顺序可不唯一；依赖偏序不可违反。", 15, fill=MUTED)]

    heading(out, 830, "C", "tape 不只记节点名", RED)
    ledger = (
        (105, "value + shape", "c : scalar", BLUE),
        (182, "local cache", "x₁,x₂,c", TEAL),
        (259, "mode / RNG", "train, key, counter", RED),
        (336, "state / alias", "version + storage", BLUE),
        (413, "cost metadata", "FLOPs, bytes, path", TEAL),
    )
    for y, key, val, color in ledger:
        out += [rect(840, y, 300, 54, color, BG, 7, 2), text(855, y + 23, key, 15, 700, fill=color), text(855, y + 45, val, 15, 500, fill=INK)]
    return finish(out, "可求导执行 = DAG 依赖 + 类型形状 + 实际 trace + 可回放的状态。")


def local_jacobian_actions():
    out = begin(
        "局部微分：一个线性算子的两种方向作用",
        "Derivative 是从输入扰动到输出扰动的线性映射；JVP 前推 tangent，VJP 回拉 cotangent，二者由点积恒等式配对。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Df 是算子，J 是坐标表", BLUE)
    out += [circle(120, 245, 76, BLUE, "#EFF6FF", 2.5), circle(300, 245, 64, TEAL, "#ECFDF5", 2.5)]
    out += [text(120, 230, "input", 17, 700, "middle", BLUE), text(120, 258, "Rⁿ", 24, 700, "middle", BLUE)]
    out += [text(300, 230, "output", 17, 700, "middle", TEAL), text(300, 258, "Rᵐ", 24, 700, "middle", TEAL)]
    out += [line(197, 225, 235, 225, BLUE, 3, marker="a0"), text(216, 207, "Df(x)", 16, 700, "middle", BLUE)]
    out += [text(47, 380, "f(x+h)=f(x)+Df(x)[h]+o(||h||)", 16, 650, cls="math")]
    out += [rect(58, 420, 284, 58, RED, BG, 7, 2), text(200, 445, "J : [m,n]", 18, 700, "middle", RED), text(200, 467, "坐标选择后的数组", 15, 500, "middle", MUTED)]

    heading(out, 430, "B", "tangent 前推；dual 反向拉回", TEAL)
    node(out, 445, 110, 90, 54, "v : [n]", BLUE)
    node(out, 655, 110, 90, 54, "Jv : [m]", TEAL)
    out += [line(540, 137, 650, 137, BLUE, 3, marker="a0"), text(595, 121, "JVP", 16, 700, "middle", BLUE)]
    node(out, 655, 280, 90, 54, "u : [m]", RED)
    node(out, 445, 280, 100, 54, "Jᵀu : [n]", TEAL)
    out += [line(650, 307, 550, 307, RED, 3, marker="a2"), text(600, 291, "VJP", 16, 700, "middle", RED)]
    out += [path("M520 190C555 235 630 235 670 190", GRID, 2.5, "none", "6 5")]
    out += [text(600, 230, "uᵀ(Jv) = (Jᵀu)ᵀv", 18, 700, "middle", fill=INK, cls="math")]
    out += [text(435, 405, "broadcast ↔ sum； transpose 是伴随，不是 inverse。", 15, fill=MUTED)]
    out += [text(435, 457, "dot test 同时检查轴、转置与累加。", 16, 700, fill=TEAL)]

    heading(out, 830, "C", "不物化巨型 Jacobian", RED)
    out += [rect(845, 105, 285, 110, RED, "#FFF5F2", 5, 2)]
    for i in range(1, 6):
        out += [line(845 + i * 47.5, 105, 845 + i * 47.5, 215, GRID, 1)]
    for i in range(1, 4):
        out += [line(845, 105 + i * 27.5, 1130, 105 + i * 27.5, GRID, 1)]
    out += [text(987, 242, "full J: m×n entries", 16, 700, "middle", RED)]
    out += [text(845, 292, "n input seeds", 16, 700, fill=BLUE), line(965, 287, 1120, 287, BLUE, 3, marker="a0"), text(845, 322, "forward builds columns", 15, fill=MUTED)]
    out += [text(845, 375, "m output seeds", 16, 700, fill=TEAL), line(1120, 370, 965, 370, TEAL, 3, marker="a1"), text(845, 405, "reverse builds rows", 15, fill=MUTED)]
    out += [rect(845, 438, 285, 56, TEAL, "#ECFDF5", 7, 2), text(987, 463, "scalar loss: m=1", 17, 700, "middle", TEAL), text(987, 484, "one reverse seed", 15, 500, "middle", TEAL)]
    return finish(out, "在大模型中选择所需的线性作用，而不是先造出整张 Jacobian。")


def backprop_reverse_accumulation():
    out = begin(
        "反向传播：从标量 seed 到 fan-out 贡献之和",
        "逆拓扑序只处理已收齐子节点贡献的值；每条边调用局部 VJP，共享父节点使用加法累积。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "forward 账本", BLUE)
    rows = ((105, "a = xy", "6"), (177, "b = x+y", "5"), (249, "c = a+b", "11"), (321, "L = c²/2", "60.5"))
    out += [text(55, 91, "operation", 15, 700, fill=BLUE), text(305, 91, "value", 15, 700, "middle", BLUE), line(48, 98, 355, 98, BLUE, 2)]
    for y, op, val in rows:
        out += [text(55, y + 25, op, 17, 650, cls="math"), rect(275, y, 78, 42, BLUE, "#EFF6FF", 6, 2), text(314, y + 27, val, 16, 700, "middle", BLUE)]
    out += [text(50, 420, "x=2, y=3", 17, 700, fill=INK), text(50, 462, "forward 保存局部 VJP 所需的 primal。", 15, fill=MUTED)]

    heading(out, 430, "B", "reverse ledger：每条边一份", TEAL)
    reverse_rows = (
        (103, "L̄ = 1", "seed"),
        (173, "c̄ = 11", "square VJP"),
        (243, "ā=b̄=11", "add copies"),
        (313, "x̄ = 33 + 11", "two paths"),
        (383, "ȳ = 22 + 11", "two paths"),
    )
    for y, formula, note in reverse_rows:
        out += [rect(445, y, 205, 48, TEAL, "#ECFDF5", 6, 2), text(547, y + 30, formula, 17, 700, "middle", TEAL, "math"), text(668, y + 30, note, 15, 500, fill=MUTED)]
        if y < 383:
            out += [line(547, y + 50, 547, y + 66, INK, 2, marker="a3")]
    out += [text(438, 470, "x̄=44， ȳ=33；覆盖任一分支都会缺项。", 16, 700, fill=RED)]

    heading(out, 830, "C", "不枚举路径，复用后缀", RED)
    pts = {"v": (865, 275), "p₁": (955, 160), "p₂": (955, 385), "q": (1050, 275), "L": (1125, 275)}
    for label, (x, y) in pts.items():
        color = BLUE if label == "v" else TEAL if label.startswith("p") else RED
        out += [circle(x, y, 22, color, BG, 2.5), text(x, y + 6, label, 15, 700, "middle", color)]
    for a, b in (("v", "p₁"), ("v", "p₂"), ("p₁", "q"), ("p₂", "q"), ("q", "L")):
        x1, y1 = pts[a]; x2, y2 = pts[b]
        out += [line(x1 + 22, y1, x2 - 24, y2, INK, 2.2, marker="a3")]
    out += [path("M1102 255C1050 205 955 210 887 258", RED, 2.5, "none", "7 5", "a2")]
    out += [path("M1102 295C1050 345 955 340 887 292", RED, 2.5, "none", "7 5", "a2")]
    out += [text(835, 105, "v̄ = Σ children VJP", 18, 700, fill=RED, cls="math")]
    out += [text(835, 447, "每个 node adjoint 只汇总一次；", 15, fill=MUTED), text(835, 477, "path count 可指数增，图动态规划仍按边处理。", 15, fill=MUTED)]
    return finish(out, "reverse mode = seed 1 + 逆拓扑序 + 局部 VJP + fan-out 求和；它计算梯度，不负责更新参数。")


def dense_layer_backward():
    out = begin(
        "Affine backward：一条微分拆出三个伴随作用",
        "对 row-batch Z=XW+1b，dZ 的三项分别与 upstream G 做 Frobenius 配对，得到输入回拉、逐样本 outer-product 求和和 broadcast 轴归约。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "先写完整 differential", BLUE)
    node(out, 55, 105, 290, 58, "Z = XW + 1b", BLUE)
    out += [line(200, 167, 200, 205, INK, 2.5, marker="a3")]
    node(out, 45, 218, 310, 72, "dZ = dX W + X dW + 1 db", TEAL, size=16)
    out += [line(200, 294, 200, 332, INK, 2.5, marker="a3")]
    node(out, 45, 345, 310, 72, "dL = <G,dZ>_F", RED, size=17)
    out += [text(48, 458, "X:[B,din]  W:[din,dout]", 16, 650, cls="math"), text(48, 490, "G,Z:[B,dout]  b:[dout]", 16, 650, cls="math")]

    heading(out, 430, "B", "形状账本强制三路 VJP", TEAL)
    formulas = (
        (105, "X̄ = G Wᵀ", "[B,din]", BLUE),
        (220, "W̄ = Xᵀ G", "[din,dout]", TEAL),
        (335, "b̄ = sum rows of G", "[dout]", RED),
    )
    for y, formula, shape, color in formulas:
        out += [rect(445, y, 200, 68, color, BG, 7, 2.5), text(545, y + 31, formula, 19, 700, "middle", color, "math"), text(545, y + 55, shape, 15, 500, "middle", MUTED)]
    out += [line(660, 139, 742, 139, BLUE, 3, marker="a0"), text(700, 122, "input pullback", 15, 650, "middle", BLUE)]
    out += [line(660, 254, 742, 254, TEAL, 3, marker="a1"), text(700, 237, "outer products", 15, 650, "middle", TEAL)]
    out += [line(660, 369, 742, 369, RED, 3, marker="a2"), text(700, 352, "broadcast sum", 15, 650, "middle", RED)]
    out += [text(438, 455, "transpose 与 reduction 都由伴随关系决定。", 16, 700), text(438, 489, "方阵 shape 能通过，仍不代表乘法顺序正确。", 15, fill=MUTED)]

    heading(out, 830, "C", "从单样本到分布式求和", RED)
    out += [text(845, 112, "per example", 16, 700, fill=BLUE), text(845, 145, "W̄⁽ⁱ⁾ = xᵢᵀ gᵢ", 18, 700, fill=INK, cls="math")]
    for i, color in enumerate((BLUE, TEAL, RED)):
        y = 190 + i * 58
        out += [rect(850, y, 74, 40, color, BG, 5, 2), text(887, y + 26, f"batch {i+1}", 15, 650, "middle", color), line(930, y + 20, 1000, y + 20, color, 2.5, marker=f"a{i}")]
    out += [rect(1010, 205, 120, 112, RED, "#FFF5F2", 7, 2.5), text(1070, 242, "SUM", 19, 700, "middle", RED), text(1070, 273, "all-reduce", 15, 650, "middle", RED), text(1070, 299, "or local", 15, 500, "middle", MUTED)]
    out += [text(845, 360, "sum loss: contributions add", 16, 700, fill=TEAL), text(845, 397, "global mean: weight by valid counts", 16, 700, fill=BLUE)]
    out += [rect(845, 438, 290, 56, RED, BG, 7, 2), text(990, 462, "low precision + reduction order", 16, 700, "middle", RED), text(990, 483, "数学等价 ≠ bitwise 相同", 15, 500, "middle", MUTED)]
    return finish(out, "牢记公式不如重建伴随：固定 layout，写 dZ，用 Frobenius 配对隔离每个 differential。")


FIGURES = {
    "fig-computation-graph-forward-v2.svg": computation_graph_forward,
    "fig-local-jacobian-jvp-vjp-v2.svg": local_jacobian_actions,
    "fig-backprop-reverse-accumulation-v2.svg": backprop_reverse_accumulation,
    "fig-dense-layer-backward-v2.svg": dense_layer_backward,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, builder in FIGURES.items():
        target = OUT / filename
        target.write_text(builder(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()

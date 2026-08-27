#!/usr/bin/env python3
"""Generate LT-81--84 paper-ink figures for deep-generalization theory."""
from pathlib import Path
from plot_calculus_operator_figures_v2 import (
    BLUE, TEAL, AMBER, RED, INK, MUTED, GRID, BG,
    begin, finish, heading, line, path, node, text, circle, rect,
)

OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "learning-theory"


def neural_norm_capacity():
    out = begin("Norm-Based Capacity：层增益、有效方向与 Margin",
                "谱范数乘积控制跨层放大，stable-rank 和式记录有效方向，二者经经验 margin 接到风险证书。",
                (BLUE, TEAL, RED))
    heading(out, 42, "A", "层增益与扰动望远镜", BLUE)
    xs = (55, 150, 245, 340)
    labs = ("x", "W1", "W2", "WL")
    for i, (x, lab) in enumerate(zip(xs, labs)):
        node(out, x, 110, 60 if i == 0 else 68, 48, lab, BLUE if i < 2 else TEAL, size=15)
        if i < 3:
            out.append(line(x + (61 if i == 0 else 69), 134, xs[i + 1] - 7, 134, INK, 2, marker="a3"))
    out += [text(55, 210, "Lip(f) <= product_l ||W_l||_2", 17, 700, cls="math"),
            path("M65 282C135 242 245 326 350 265", TEAL, 3),
            path("M65 322C145 286 250 364 350 304", BLUE, 2.5, dash="7 5"),
            text(55, 374, "one layer perturbed -> propagated by all others", 15, 650),
            text(55, 414, "relative changes add; gains multiply", 16, 700, fill=TEAL),
            text(55, 476, "input scale B is part of the bound", 15, fill=MUTED)]

    heading(out, 430, "B", "Spectral Complexity 的两账", TEAL)
    node(out, 445, 105, 310, 58, "gain = B product ||W_l||_2", BLUE, size=16)
    out.append(line(600, 168, 600, 201, INK, 2.2, marker="a3"))
    node(out, 445, 214, 310, 66, "directions = sqrt(sum stable-rank_l)", TEAL, size=15)
    out.append(line(600, 285, 600, 318, INK, 2.2, marker="a3"))
    node(out, 445, 331, 310, 58, "C(W) = gain x directions", RED, size=16)
    out += [text(445, 432, "stable-rank = ||W||_F^2 / ||W||_2^2", 15, 650),
            text(445, 470, "layer c, next 1/c -> C(W) unchanged", 15, fill=TEAL),
            text(445, 504, "logs / reference matrices depend on theorem", 15, fill=MUTED)]

    heading(out, 830, "C", "从 Margin 到证书", RED)
    rows = (("small-margin", "R_hat_gamma", BLUE),
            ("complexity", "C/(gamma sqrt n)", TEAL),
            ("confidence", "sqrt(log 1/delta / n)", AMBER))
    for i, (a, b, col) in enumerate(rows):
        y = 102 + i * 90
        node(out, 840, y, 135, 48, a, col, size=15)
        out.append(text(995, y + 31, b, 15, 650))
    out.append(line(990, 367, 990, 400, INK, 2.2, marker="a3"))
    node(out, 840, 412, 300, 52, "bound < trivial risk?", RED, size=16)
    out += [text(840, 500, "theorem -> estimate -> nonvacuity", 15, fill=MUTED)]
    return finish(out, "参数量描述最坏表达力；norm、margin 与输入尺度描述训练后函数的可控局部容量。")


def ntk_lazy():
    out = begin("NTK：从 Jacobian 到固定核动力学",
                "平方损失产生精确的时变核方程；只有 kernel drift 可忽略时，residual 才按初始化核特征模指数衰减。",
                (BLUE, TEAL, RED))
    heading(out, 42, "A", "Tangent Features 组成 Gram", BLUE)
    for i, y in enumerate((125, 210, 295)):
        out.append(circle(90, y, 10, BLUE, BLUE))
        out.append(text(115, y + 6, f"grad f(x{i+1})", 15, 650))
        out.append(line(222, y, 300, y, TEAL, 2.3))
    out += [rect(300, 105, 55, 220, TEAL, "#ECFDF5", 5, 2),
            text(327, 345, "J", 20, 700, "middle", TEAL),
            text(55, 395, "K_t = J_t J_t^T", 19, 700, fill=BLUE, cls="math"),
            text(55, 438, "exact: f_dot(X) = -K_t (f-y)", 16, 650, cls="math"),
            text(55, 484, "time-varying until proven otherwise", 15, fill=MUTED)]

    heading(out, 430, "B", "固定核时：模式分速衰减", TEAL)
    out += [line(465, 405, 755, 405, GRID, 1.5), line(465, 405, 465, 105, GRID, 1.5)]
    curves = (("M470 130C530 225 575 330 750 386", RED),
              ("M470 165C555 225 645 300 750 352", TEAL),
              ("M470 200C565 218 665 252 750 286", BLUE))
    for d, col in curves:
        out.append(path(d, col, 3))
    out += [text(704, 377, "large lambda", 15, 650, fill=RED),
            text(690, 271, "small lambda", 15, 650, fill=BLUE),
            text(445, 448, "r_t = exp(-K_0 t) r_0", 18, 700, cls="math"),
            text(445, 486, "training speed != test alignment", 15, fill=MUTED)]

    heading(out, 830, "C", "Kernel-Regime 三道门", RED)
    gates = (("init concentration", BLUE), ("K_t near K_0", TEAL), ("kernel risk bridge", RED))
    for i, (lab, col) in enumerate(gates):
        y = 100 + i * 112
        node(out, 840, y, 300, 58, lab, col, size=16)
        if i < 2:
            out.append(line(990, y + 63, 990, y + 102, INK, 2.2, marker="a3"))
    out += [text(840, 447, "NNGP: initialization covariance", 15, 650),
            text(840, 482, "NTK: gradient Gram / training", 15, 650, fill=TEAL),
            text(840, 512, "feature learning is a separate question", 15, fill=MUTED)]
    return finish(out, "先证明网络接近固定核，再用核统计理论证明风险；训练拟合不能替代第二步。")


def mean_field():
    out = begin("Mean-Field：从粒子云到 Feature Dynamics",
                "神经元参数的经验测度在极限中被 residual-dependent 速度场搬运；分布变化使特征而非只使线性系数发生演化。",
                (BLUE, TEAL, RED))
    heading(out, 42, "A", "有限宽 = 参数粒子云", BLUE)
    pts = ((95,145),(165,118),(235,165),(295,125),(125,245),(210,255),(310,230),(270,320),(155,335))
    for i, (x, y) in enumerate(pts):
        out.append(circle(x, y, 8, TEAL if i % 3 else BLUE, TEAL if i % 3 else BLUE))
    out += [text(55, 392, "rho_m = (1/m) sum_j delta_theta_j", 17, 700, cls="math"),
            text(55, 435, "f_rho(x) = integral phi(x;theta) d rho", 16, 650, cls="math"),
            text(55, 482, "width grows -> measure, not longer notation", 15, fill=MUTED)]

    heading(out, 430, "B", "Residual 生成速度场", TEAL)
    for i, (x, y) in enumerate(((480,150),(545,205),(610,140),(680,225),(735,150),(520,330),(620,345),(710,320))):
        out.append(circle(x, y, 7, BLUE, BLUE))
        dx = 22 if i % 2 == 0 else -18
        dy = 18 if i < 4 else -20
        out.append(line(x, y, x + dx, y + dy, TEAL, 2, marker="a1"))
    out += [path("M470 410C535 375 665 455 755 390", RED, 2.5),
            text(445, 455, "partial_t rho = div(rho grad Psi[rho])", 16, 700, cls="math"),
            text(445, 493, "Psi depends on the current predictor", 15, fill=MUTED)]

    heading(out, 830, "C", "训练 Regime 是连续谱", RED)
    out += [line(865, 210, 1115, 210, GRID, 8),
            circle(885, 210, 13, BLUE, BG, 3), circle(1000, 210, 13, AMBER, BG, 3),
            circle(1100, 210, 13, TEAL, BG, 3),
            text(885, 172, "lazy", 16, 700, "middle", BLUE),
            text(1000, 172, "mixed", 16, 700, "middle", AMBER),
            text(1100, 172, "rich", 16, 700, "middle", TEAL),
            text(840, 285, "kernel drift", 15, 650),
            text(840, 323, "feature covariance / transfer", 15, 650),
            text(840, 361, "scaling + step + time", 15, 650, fill=RED)]
    node(out, 840, 410, 300, 55, "finite-width bridge required", RED, size=16)
    out.append(text(840, 505, "feature movement != useful representation", 15, fill=MUTED))
    return finish(out, "Mean-field 保留可演化特征，但泛化仍取决于数据结构、有限宽误差与风险桥。")


def evidence_map():
    out = begin("深度泛化证据地图：从现象到部署",
                "插值、选解、容量、表示与风险保证属于不同证据层；每条箭头都需要独立的定理、证书或干预。",
                (BLUE, TEAL, RED))
    heading(out, 42, "A", "证据不可越级", BLUE)
    levels = (("phenomenon", BLUE), ("selection", TEAL), ("risk bound", AMBER), ("deployment", RED))
    for i, (lab, col) in enumerate(levels):
        y = 95 + i * 88
        node(out, 65 + i * 30, y, 245, 48, lab, col, size=16)
        if i < 3:
            out.append(line(190 + i * 30, y + 52, 220 + i * 30, y + 80, INK, 2, marker="a3"))
    out.append(text(55, 486, "an adjacent theorem cannot fill a missing arrow", 15, fill=MUTED))

    heading(out, 430, "B", "机制是拼图，不是赢家赛", TEAL)
    pieces = ((455,110,125,72,"interpolation",BLUE),(620,110,125,72,"implicit bias",TEAL),
              (455,230,125,72,"norm/margin",AMBER),(620,230,125,72,"data/features",RED))
    for x,y,w,h,lab,col in pieces:
        node(out,x,y,w,h,lab,col,size=15)
    out += [line(580,146,615,146,INK,2,marker="a3"), line(517,187,517,222,INK,2,marker="a3"),
            line(682,187,682,222,INK,2,marker="a3"), line(580,266,615,266,INK,2,marker="a3"),
            text(445, 455, "NTK / mean-field specify regimes", 15, 650),
            text(445, 493, "none alone proves OOD safety", 15, fill=MUTED)]
    node(out, 492, 350, 220, 56, "population risk", RED, size=17)

    heading(out, 830, "C", "一个指标的五项验收", RED)
    checks = (("valid?", BLUE), ("nonvacuous?", TEAL), ("right trend?", AMBER),
              ("invariant?", BLUE), ("intervention?", RED))
    for i, (lab, col) in enumerate(checks):
        y = 92 + i * 76
        out.append(circle(860, y + 18, 13, col, BG, 2.5))
        out.append(text(888, y + 24, lab, 16, 650))
    node(out, 840, 475, 300, 45, "state the falsifier", RED, size=16)
    return finish(out, "好的泛化理论不仅给出一个数，还说明对象、量词、适用域以及什么结果会推翻它。")


FIGURES = {
    "fig-neural-norm-capacity-v2.svg": neural_norm_capacity,
    "fig-ntk-lazy-kernel-v2.svg": ntk_lazy,
    "fig-mean-field-feature-learning-v2.svg": mean_field,
    "fig-deep-generalization-evidence-map-v2.svg": evidence_map,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, factory in FIGURES.items():
        target = OUT / name
        target.write_text(factory(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()

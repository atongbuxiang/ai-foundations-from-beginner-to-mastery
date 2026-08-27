#!/usr/bin/env python3
"""Generate LT-77--80 paper-ink figures for deep-generalization interfaces."""
from pathlib import Path
from plot_calculus_operator_figures_v2 import (
    BLUE, TEAL, AMBER, RED, INK, MUTED, GRID, BG,
    begin, finish, heading, line, path, node, text, circle, rect,
)

OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "learning-theory"


def double_descent():
    out = begin("Double Descent：Interpolation Threshold 与风险分账",
                "测试风险曲线属于容量路径与选解算法；阈值峰对应 inverse-Gram 的小奇异值放大。",
                (BLUE, TEAL, RED))
    heading(out, 42, "A", "经典 U 型接上第二次下降", BLUE)
    out += [line(65, 410, 360, 410, GRID, 1.5), line(80, 435, 80, 100, GRID, 1.5),
            path("M90 145C125 195 160 315 205 305C225 300 225 125 238 115C255 125 270 300 350 320", BLUE, 4),
            line(238, 105, 238, 410, RED, 2, dash="7 5"),
            text(110, 115, "classical regime", 15, 650, fill=BLUE),
            text(238, 88, "interpolation", 15, 650, "middle", RED),
            text(305, 115, "2nd descent", 15, 650, "middle", TEAL),
            text(55, 454, "capacity / p", 15), text(42, 135, "risk", 15, fill=MUTED),
            text(55, 490, "peak is regime-dependent, not universal", 15, fill=MUTED)]

    heading(out, 430, "B", "Gaussian Linear Risk Ledger", TEAL)
    node(out, 445, 102, 310, 62, "p<n: noise = sigma^2 p/(n-p-1)", BLUE, size=15)
    out.append(line(600, 169, 600, 202, INK, 2.2, marker="a3"))
    node(out, 445, 214, 310, 62, "p>n: signal bias + noise variance", TEAL, size=15)
    out.append(line(600, 281, 600, 314, INK, 2.2, marker="a3"))
    node(out, 430, 326, 340, 72, "(1-n/p)||beta||^2 + sigma^2 n/(p-n-1)", RED, size=15)
    out += [text(445, 442, "small singular value -> noise amplification", 15, 650),
            text(445, 478, "ridge smooths the inverse filter", 15, fill=MUTED)]

    heading(out, 830, "C", "三条 Path，不是一个定律", RED)
    rows = (("model-wise", "width / depth", BLUE),
            ("sample-wise", "number of examples", TEAL),
            ("epoch-wise", "training time", AMBER))
    for i, (a, b, col) in enumerate(rows):
        y = 105 + i * 92
        node(out, 840, y, 145, 50, a, col, size=15)
        out.append(line(990, y + 25, 1020, y + 25, INK, 2, marker="a3"))
        out.append(text(1032, y + 31, b, 15))
    node(out, 840, 400, 300, 55, "lock optimizer, regularization, compute", RED, size=15)
    out.append(text(840, 492, "parameter count != effective complexity", 15, fill=MUTED))
    return finish(out, "双下降不取消 bias–variance；它要求把 estimator、spectrum 与容量路径写进同一对象合同。")


def benign_overfitting():
    out = begin("Benign Overfitting：Signal–Noise 与谱尾分工",
                "minimum-norm interpolator 在强方向恢复 signal，并可能把噪声分散到许多 population-weak directions。",
                (BLUE, TEAL, RED))
    heading(out, 42, "A", "Min-Norm Error 的两部分", BLUE)
    node(out, 55, 100, 300, 56, "beta_hat = X_dagger y", BLUE, size=16)
    out.append(line(205, 161, 205, 195, INK, 2.2, marker="a3"))
    node(out, 55, 207, 300, 68, "error = -(I-P_X) beta* + X_dagger noise", TEAL, size=15)
    out.append(line(205, 280, 205, 314, INK, 2.2, marker="a3"))
    node(out, 55, 326, 300, 60, "test metric = ||Sigma^(1/2) error||^2", RED, size=15)
    out += [text(55, 432, "null-space signal -> bias", 15, fill=RED),
            text(55, 466, "fitted labels -> variance", 15, fill=BLUE),
            text(55, 500, "training fit alone sees neither cost", 15, fill=MUTED)]

    heading(out, 430, "B", "强 Signal + 分散弱 Tail", TEAL)
    vals = (180, 135, 95, 52, 45, 39, 34, 30)
    for i, h in enumerate(vals):
        x = 450 + i * 37
        col = TEAL if i < 3 else BLUE
        out.append(rect(x, 390 - h, 24, h, col, "#ECFDF5" if i < 3 else "#EFF6FF", 2, 1.5))
    out += [line(440, 390, 760, 390, GRID, 1.5),
            text(500, 185, "signal subspace", 15, 650, "middle", TEAL),
            text(680, 285, "many weak directions", 15, 650, "middle", BLUE),
            text(445, 435, "tail effective rank: spread, not just trace", 15, 650),
            text(445, 470, "signal must align with learnable directions", 15, fill=RED),
            text(445, 502, "p>n alone is insufficient", 15, fill=MUTED)]

    heading(out, 830, "C", "Benign Claim 的必要账户", RED)
    rows = (("interpolate", "train risk = 0", BLUE),
            ("algorithm", "min norm / dynamics", TEAL),
            ("spectrum", "tail ranks + signal", AMBER),
            ("limit", "excess risk -> 0", RED))
    for i, (a, b, col) in enumerate(rows):
        y = 95 + i * 82
        node(out, 840, y, 130, 48, a, col, size=15)
        out.append(line(975, y + 24, 1005, y + 24, INK, 2, marker="a3"))
        out.append(text(1017, y + 30, b, 15))
    node(out, 840, 430, 300, 52, "linear theorem -> deep-net hypothesis", RED, size=15)
    out.append(text(840, 510, "not every interpolator is benign", 15, fill=MUTED))
    return finish(out, "良性过拟合是算法选解与数据谱的联合结论；零训练误差本身既不充分，也不接近充分。")


def implicit_bias():
    out = begin("Implicit Bias：Dynamics 在多解集合中选解",
                "least squares 的 row-space invariance 选择 min norm；separable logistic 的参数发散但方向趋向 max margin。",
                (BLUE, TEAL, RED))
    heading(out, 42, "A", "Least Squares：Affine 解集", BLUE)
    out += [line(70, 380, 350, 150, TEAL, 3),
            line(95, 105, 95, 415, GRID, 1.5), line(60, 360, 360, 360, GRID, 1.5),
            line(95, 360, 225, 250, BLUE, 3, marker="a0"),
            circle(225, 250, 8, RED, RED),
            text(235, 238, "X_dagger y", 15, 700, fill=RED),
            text(245, 155, "Xw=y", 15, 650, fill=TEAL),
            text(55, 438, "zero-init GD stays in row(X)", 15, 650),
            text(55, 474, "null-space init is remembered", 15, fill=MUTED)]

    heading(out, 430, "B", "Logistic：收敛的是方向", TEAL)
    out += [circle(600, 300, 28, BLUE, BG, 2),
            line(600, 300, 730, 155, TEAL, 4, marker="a1"),
            line(600, 300, 690, 120, RED, 2.5, dash="7 5", marker="a2"),
            text(735, 145, "w(t)", 15, 700, fill=TEAL),
            text(665, 105, "max-margin direction", 15, 650, fill=RED),
            text(445, 370, "||w(t)|| -> infinity", 16, 650),
            text(445, 407, "loss -> 0", 16, 650),
            text(445, 444, "w(t)/||w(t)|| -> w_SVM/||w_SVM||", 15, 700, fill=TEAL),
            text(445, 485, "direction convergence may be logarithmically slow", 15, fill=MUTED)]

    heading(out, 830, "C", "Selection 不是 Generalization", RED)
    rows = (("dynamics", "optimizer + init", BLUE),
            ("selected solution", "norm / margin / rank", TEAL),
            ("risk bridge", "data assumptions", RED))
    for i, (a, b, col) in enumerate(rows):
        y = 105 + i * 105
        node(out, 840, y, 150, 52, a, col, size=15)
        out.append(line(995, y + 26, 1025, y + 26, INK, 2, marker="a3"))
        out.append(text(1037, y + 32, b, 15))
    out += [text(840, 438, "preconditioner changes geometry", 15, 650),
            text(840, 474, "parameterization changes bias", 15, 650, fill=RED),
            text(840, 508, "finite time needs its own theorem", 15, fill=MUTED)]
    return finish(out, "先证明算法选了什么，再证明这个解为何对目标分布简单；两条证明不能合并成一句“SGD 正则化”。")


def sharpness():
    out = begin("Sharpness：同一函数，不同参数几何",
                "positive-homogeneous rescaling 保持 predictor，却可任意改变 raw norm 与 Hessian sharpness。",
                (BLUE, TEAL, RED))
    heading(out, 42, "A", "ReLU 等价重缩放", BLUE)
    node(out, 60, 115, 125, 55, "incoming w", BLUE, size=15)
    out.append(line(190, 142, 225, 142, INK, 2.2, marker="a3"))
    node(out, 235, 115, 110, 55, "outgoing a", TEAL, size=15)
    out += [text(55, 225, "w -> c w", 17, 700, fill=BLUE),
            text(55, 270, "a -> a / c", 17, 700, fill=TEAL),
            text(55, 320, "a ReLU(w^T x) stays identical", 16, 650),
            text(55, 380, "raw layer norms change", 16, fill=RED),
            text(55, 425, "path product stays invariant", 16, fill=TEAL),
            text(55, 480, "parameter != predictor", 15, fill=MUTED)]

    heading(out, 430, "B", "乘积模型反例", TEAL)
    node(out, 445, 105, 310, 55, "L(a,b)=(ab-1)^2; minima ab=1", BLUE, size=15)
    out.append(line(600, 165, 600, 200, INK, 2.2, marker="a3"))
    node(out, 445, 212, 310, 60, "lambda_max(H)=2(a^2+b^2)", RED, size=16)
    out.append(line(600, 277, 600, 312, INK, 2.2, marker="a3"))
    node(out, 445, 324, 310, 58, "a=c, b=1/c: same f, sharpness -> infinity", TEAL, size=15)
    out += [text(445, 428, "raw norm also changes", 15, 650, fill=RED),
            text(445, 466, "generalization remains identical", 15, 650, fill=TEAL),
            text(445, 502, "coordinate sharpness is not a function invariant", 15, fill=MUTED)]

    heading(out, 830, "C", "指标证据阶梯", RED)
    rows = (("invariant?", "symmetry stress test", BLUE),
            ("predictive?", "held-out sweeps", TEAL),
            ("bounded?", "risk theorem", AMBER),
            ("causal?", "controlled intervention", RED))
    for i, (a, b, col) in enumerate(rows):
        y = 95 + i * 82
        node(out, 840, y, 125, 48, a, col, size=15)
        out.append(line(970, y + 24, 1000, y + 24, INK, 2, marker="a3"))
        out.append(text(1012, y + 30, b, 15))
    node(out, 840, 430, 300, 52, "parameter / function / data geometry", RED, size=15)
    out.append(text(840, 510, "correlation is only one evidence level", 15, fill=MUTED))
    return finish(out, "复杂度指标先过等价类不变性，再谈预测、界和因果；顺序颠倒会把坐标伪影当成理论机制。")


FIGURES = {
    "fig-double-descent-interpolation-v2.svg": double_descent,
    "fig-benign-overfitting-spectrum-v2.svg": benign_overfitting,
    "fig-implicit-bias-solution-selection-v2.svg": implicit_bias,
    "fig-sharpness-reparameterization-v2.svg": sharpness,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, factory in FIGURES.items():
        target = OUT / name
        target.write_text(factory(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()

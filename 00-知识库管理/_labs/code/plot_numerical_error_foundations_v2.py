#!/usr/bin/env python3
"""Generate v2 textbook figures for NUM-01--04 numerical error foundations."""

from __future__ import annotations

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG,
    BLUE,
    GRID,
    INK,
    MUTED,
    RED,
    TEAL,
    begin,
    circle,
    finish,
    heading,
    line,
    node,
    path,
    rect,
    text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "numerical-analysis"


def floating_point_system():
    out = begin(
        "浮点有限网格、运算链与舍入误差累积",
        "浮点数在每个 binade 内等距但跨数量级间距增大；输入格式、算术格式、累加格式和输出格式可不同；局部 unit-roundoff 模型只有在正规范围内成立，多步误差还要处理消去、吸收、溢出与下溢。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "有限网格的间距随量级增大", BLUE)
    out += [line(50, 300, 370, 300, INK, 2)]
    ticks = (70, 86, 102, 118, 134, 166, 198, 230, 294, 358)
    for i, x in enumerate(ticks):
        h = 30 if i in (0, 4, 7, 9) else 18
        out.append(line(x, 300 - h, x, 300 + h, BLUE if i < 7 else RED, 2.5))
    out += [text(45, 245, "subnormals", 15, 650, fill=TEAL), text(165, 245, "one binade", 15, 650, fill=BLUE), text(280, 245, "2x spacing", 15, 650, fill=RED)]
    out += [text(45, 365, "ulp(x) scales with exponent", 17, 700), text(45, 405, "finite bits cannot represent every real number", 16, 650), text(45, 448, "eps at 1 != unit roundoff u", 16, 650, fill=RED), text(45, 486, "relative model weakens near zero and exceptions。", 15, fill=MUTED)]

    heading(out, 430, "B", "dtype 名称不足以描述执行链", TEAL)
    stages = (("input", "FP16", BLUE), ("op", "TF32", RED), ("accum", "FP32", TEAL), ("output", "cast", BLUE))
    for i, (label, desc, color) in enumerate(stages):
        x = 425 + i * 92
        node(out, x, 115, 75, 55, label, color, size=15)
        out += [text(x + 38, 205, desc, 15, 650, "middle", fill=color)]
        if i < 3:
            out.append(line(x + 77, 143, x + 89, 143, INK, 2.2, marker="a3"))
    out += [text(430, 275, "same storage dtype can hide different accumulators", 16, 650), text(430, 320, "FMA: one final rounding for multiply-add", 16, 650, fill=TEAL)]
    out += [line(440, 360, 760, 360, GRID, 2), text(430, 405, "scale management", 16, 700, fill=RED), text(430, 438, "loss scaling / stable softmax / overflow checks", 15, 650), text(430, 480, "parallel reduction order affects bitwise result。", 15, fill=MUTED)]

    heading(out, 830, "C", "从一次舍入到算法误差", RED)
    node(out, 840, 105, 300, 60, "fl(a op b)=(a op b)(1+delta)", BLUE, size=16)
    out += [line(990, 168, 990, 205, INK, 2.5, marker="a3")]
    node(out, 840, 218, 300, 60, "|theta_n| <= gamma_n = n u/(1-n u)", TEAL, size=15)
    out += [line(990, 281, 990, 318, INK, 2.5, marker="a3")]
    branches = (("absorption", 850, BLUE), ("cancellation", 948, RED), ("over/underflow", 1046, TEAL))
    for label, x, color in branches:
        node(out, x, 335, 90, 55, label, color, size=15)
    out += [text(830, 435, "gamma_n is worst-case, not typical", 15, 650), text(830, 470, "validate: reference + scale/order sweeps", 15, 650), text(830, 499, "higher precision does not fix bad modeling。", 15, fill=MUTED)]
    return finish(out, "浮点分析必须同时声明表示、运算、累加、异常路径和验收；一个 dtype 标签不是数值合同。")


def forward_backward_error():
    out = begin(
        "前向误差、后向误差、残差与条件放大",
        "前向误差比较计算输出与原问题真解；后向误差寻找使计算输出成为精确解的最小邻近输入；线性系统残差经尺度归一化形成后向误差，再由条件数放大为前向误差界。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "在输出量误差，在输入找解释", BLUE)
    out += [line(60, 170, 350, 170, GRID, 2), line(60, 365, 350, 365, GRID, 2)]
    d, dt, y, yh = (105, 170), (245, 170), (135, 365), (275, 365)
    out += [circle(*d, 7, BLUE, BLUE), circle(*dt, 7, TEAL, TEAL), circle(*y, 7, BLUE, BLUE), circle(*yh, 7, RED, RED)]
    out += [line(d[0], d[1] + 8, y[0], y[1] - 8, BLUE, 2.5, marker="a0"), line(dt[0], dt[1] + 8, yh[0], yh[1] - 8, TEAL, 2.5, marker="a1")]
    out += [line(d[0] + 10, d[1], dt[0] - 10, dt[1], TEAL, 3, marker="a1"), line(y[0] + 10, y[1], yh[0] - 10, yh[1], RED, 3, marker="a2")]
    out += [text(95, 145, "data d", 15, 700, fill=BLUE), text(220, 145, "nearby d_tilde", 15, 700, fill=TEAL), text(120, 405, "true y=f(d)", 15, 650, fill=BLUE), text(245, 405, "computed y_hat", 15, 650, fill=RED)]
    out += [text(105, 205, "backward error", 16, 700, fill=TEAL), text(165, 345, "forward error", 16, 700, fill=RED), text(45, 470, "y_hat=f(d_tilde)；distances require declared metrics。", 15, fill=MUTED)]

    heading(out, 430, "B", "线性系统的三量关系", TEAL)
    node(out, 445, 105, 310, 58, "residual r = b - A x_hat", BLUE)
    out += [line(600, 166, 600, 203, INK, 2.5, marker="a3")]
    node(out, 445, 215, 310, 72, "backward eta = ||r|| / data scale", TEAL, size=16)
    out += [line(600, 290, 600, 327, INK, 2.5, marker="a3")]
    node(out, 445, 340, 310, 72, "forward error <= kappa(A) * eta", RED, size=16)
    out += [text(430, 455, "small residual + large kappa => large solution risk", 15, 650, fill=RED), text(430, 489, "a posteriori bound needs condition estimation。", 15, fill=MUTED)]

    heading(out, 830, "C", "perturbation model 定义证书", RED)
    rows = (("normwise", "||Delta d|| / ||d||", BLUE), ("componentwise", "|Delta d_i| / scale_i", TEAL), ("structured", "d+Delta d stays in model class", RED))
    for i, (label, eq, color) in enumerate(rows):
        yy = 105 + i * 100
        out += [text(830, yy, label, 17, 700, fill=color), line(830, yy + 18, 885, yy + 18, color, 2.5, marker="a0" if color == BLUE else "a1" if color == TEAL else "a2"), text(900, yy + 24, eq, 15, 650)]
    out += [line(830, 410, 1145, 410, GRID, 2), text(830, 450, "report: task error + residual/backward error", 15, 650), text(830, 480, "+ condition indicator + precision configuration", 15, 650), text(830, 507, "one norm may hide a critical small component。", 15, fill=MUTED)]
    return finish(out, "残差要先按允许扰动归一化成后向误差，再经匹配的条件数解释为前向误差。")


def numerical_stability():
    out = begin(
        "问题条件性、算法稳定性与最终准确性的分工",
        "条件数属于数学问题，稳定性属于浮点算法，准确性属于一次计算结果；代数等价公式可有不同舍入路径；后向、前向与混合稳定承诺的扰动位置不同。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "问题与算法共同决定准确性", BLUE)
    node(out, 45, 115, 140, 62, "problem condition", BLUE, size=16)
    node(out, 220, 115, 145, 62, "algorithm stability", TEAL, size=16)
    out += [line(115, 180, 175, 245, BLUE, 2.5, marker="a0"), line(292, 180, 230, 245, TEAL, 2.5, marker="a1")]
    node(out, 120, 255, 170, 64, "forward accuracy", RED, size=17)
    out += [text(45, 365, "forward error roughly <= kappa * backward error", 15, 650, cls="math"), text(45, 410, "ill-conditioned + stable can still be inaccurate", 15, 650, fill=RED), text(45, 449, "well-conditioned + unstable can also fail", 15, 650, fill=RED), text(45, 488, "convergence and robustness are separate terms。", 15, fill=MUTED)]

    heading(out, 430, "B", "代数等价不等于执行路径等价", TEAL)
    node(out, 435, 105, 145, 58, "sqrt(1+x)-1", RED, size=16)
    node(out, 620, 105, 145, 58, "x/(sqrt(1+x)+1)", TEAL, size=15)
    out += [line(507, 167, 507, 210, RED, 2.5, marker="a2"), line(692, 167, 692, 210, TEAL, 2.5, marker="a1")]
    out += [text(435, 245, "cancels leading digits", 15, 650, fill=RED), text(620, 245, "stable rationalization", 15, 650, fill=TEAL)]
    out += [line(430, 290, 770, 290, GRID, 2), text(430, 335, "other design tools", 17, 700), text(430, 375, "scaling · reordering · factorization · compensation", 15, 650), text(430, 420, "same formula, different range and rounding", 15, 650), text(430, 478, "test extremes, not only typical random inputs。", 15, fill=MUTED)]

    heading(out, 830, "C", "三种稳定性承诺", RED)
    rows = (("backward", "alg_u(x)=f(x+Delta x)", TEAL), ("forward", "alg_u(x) near f(x)", BLUE), ("mixed", "alg_u(x)=f(x+Delta x)+Delta y", RED))
    for i, (label, eq, color) in enumerate(rows):
        yy = 105 + i * 105
        out += [text(830, yy, label, 17, 700, fill=color), line(830, yy + 18, 885, yy + 18, color, 2.5, marker="a0" if color == BLUE else "a1" if color == TEAL else "a2"), text(900, yy + 24, eq, 15, 650, cls="math")]
    out += [line(830, 420, 1145, 420, GRID, 2), text(830, 455, "state scale, norm, structure and size factor", 15, 650), text(830, 487, "also state rounding mode and overflow assumptions。", 15, fill=MUTED)]
    return finish(out, "稳定算法只承诺忠实求解邻近问题；最终准确性仍由问题条件性和所选误差度量决定。")


def condition_estimation_stopping():
    out = begin(
        "误差账本、Jacobian 传播与可信停止准则",
        "实际计算包含数据、模型、离散、舍入、迭代和统计误差；Jacobian 只传播局部扰动；停止判断要把真实残差、尺度、条件估计、任务误差和预算同时纳入。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "先建立误差账本", BLUE)
    stages = (("data", BLUE), ("model", TEAL), ("discretize", RED), ("round", BLUE), ("iterate", TEAL), ("task", RED))
    for i, (label, color) in enumerate(stages):
        x = 45 + (i % 3) * 110
        y = 105 + (i // 3) * 135
        node(out, x, y, 88, 52, label, color, size=15)
        if i % 3 < 2:
            out.append(line(x + 90, y + 26, x + 106, y + 26, INK, 2, marker="a3"))
        if i == 2:
            out.append(line(309, y + 56, 309, y + 128, INK, 2, marker="a3"))
    out += [text(45, 410, "different layers have different units", 16, 700), text(45, 448, "connect them by models, not direct addition", 15, 650, fill=RED), text(45, 486, "probability bounds also need confidence levels。", 15, fill=MUTED)]

    heading(out, 430, "B", "Jacobian 传播方向依赖的扰动", TEAL)
    out += [circle(485, 280, 55, BLUE, "none", 2.5), f'<ellipse cx="690" cy="280" rx="78" ry="145" fill="none" stroke="{TEAL}" stroke-width="2.5"/>', line(545, 280, 605, 280, INK, 2.5, marker="a3")]
    out += [line(485, 280, 525, 240, BLUE, 3, marker="a0"), line(690, 280, 690, 160, RED, 3, marker="a2"), line(690, 280, 745, 280, TEAL, 3, marker="a1")]
    out += [text(430, 115, "Delta y approx J_f(x) Delta x", 17, 650, cls="math"), text(430, 440, "operator norm gives worst local amplification", 16, 650), text(430, 475, "JVP / VJP estimate actions；do not form inverse。", 15, fill=MUTED)]

    heading(out, 830, "C", "停止是一组 gate，不是单阈值", RED)
    gates = (("true residual", "recompute, not only recurrence", BLUE), ("scaled backward error", "match allowed perturbations", TEAL), ("condition estimate", "translate residual to solution risk", RED), ("task + budget", "accuracy, time, confidence", BLUE))
    for i, (label, desc, color) in enumerate(gates):
        yy = 98 + i * 92
        out += [circle(850, yy, 7, color, color), line(860, yy, 895, yy, color, 2.5), text(905, yy - 7, label, 16, 700, fill=color), text(905, yy + 23, desc, 15, 650)]
        if i < 3:
            out.append(line(850, yy + 12, 850, yy + 80, GRID, 2, "5 5"))
    out += [text(830, 480, "stop only when every required gate passes", 15, 700, fill=RED), text(830, 508, "else continue, rescale, refactor or raise precision。", 15, fill=MUTED)]
    return finish(out, "可信停止把残差、后向误差、条件估计和任务预算闭合；孤立的 tolerance 没有证书含义。")


FIGURES = {
    "fig-floating-point-system-v2.svg": floating_point_system,
    "fig-error-analysis-pipeline-v2.svg": forward_backward_error,
    "fig-numerical-stability-formulas-v2.svg": numerical_stability,
    "fig-condition-estimation-stopping-v2.svg": condition_estimation_stopping,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()

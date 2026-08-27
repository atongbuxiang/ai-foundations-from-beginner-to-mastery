#!/usr/bin/env python3
"""Generate LT-33--36 paper-ink figures for stability and sample compression."""

from __future__ import annotations

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "learning-theory"


def replace_one_stability():
    out = begin(
        "替换一个样本、损失敏感性与泛化",
        "两个训练集只在一个坐标不同；同一测试点上的损失差由 beta 控制。ghost replacement 与交换对称性把总体减经验风险的期望改写成这种损失差。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "相邻数据集只差一个坐标", BLUE)
    for j in range(5):
        x = 55 + 62 * j
        col = RED if j == 2 else BLUE
        lab = "z_i" if j == 2 else f"z{j+1}"
        node(out, x, 135, 48, 48, lab, col, size=15)
        col2 = TEAL if j == 2 else BLUE
        lab2 = "z_i'" if j == 2 else f"z{j+1}"
        node(out, x, 260, 48, 48, lab2, col2, size=15)
    out += [line(79, 205, 327, 205, GRID, 1.5, "5 5")]
    out += [line(203, 188, 203, 248, RED, 2.5, marker="a2")]
    out += [text(45, 365, "S ~ S' : exactly one replacement", 15, 700, fill=BLUE)]
    out += [text(45, 410, "sample unit and adjacency are theorem inputs", 14, 650)]
    out += [text(45, 515, "deletion and replacement use different constants。", 15, fill=MUTED)]

    heading(out, 430, "B", "算法输出不同，测试点固定", TEAL)
    node(out, 450, 115, 125, 56, "A(S)", BLUE)
    node(out, 450, 300, 125, 56, "A(S')", TEAL)
    out += [line(578, 143, 650, 230, BLUE, 2.5, marker="a0")]
    out += [line(578, 328, 650, 245, TEAL, 2.5, marker="a1")]
    node(out, 665, 200, 80, 72, "test z", RED)
    out += [text(430, 405, "sup_z |ell(A(S),z)-ell(A(S'),z)|", 14, 650, cls="math")]
    out += [text(430, 442, "<= beta_m", 18, 700, fill=RED, cls="math")]
    out += [text(430, 480, "compare losses, not raw parameter distance", 14, 650)]
    out += [text(430, 515, "randomized A needs an explicit seed quantifier。", 15, fill=MUTED)]

    heading(out, 830, "C", "Ghost replacement 打通期望", RED)
    for y, col, title, sub in (
        (100, BLUE, "population risk", "replace evaluation by fresh Z_i'"),
        (235, TEAL, "exchangeability", "swap Z_i and Z_i'"),
        (370, RED, "stability", "each loss difference <= beta_m"),
    ):
        out += [rect(840, y, 300, 82, col, BG, 8, 2)]
        out += [text(990, y + 31, title, 15, 700, "middle", fill=col)]
        out += [text(990, y + 62, sub, 14, 650, "middle")]
    out += [line(990, 185, 990, 228, INK, 2, marker="a3")]
    out += [line(990, 320, 990, 363, INK, 2, marker="a3")]
    out += [text(830, 490, "|E[R(A(S))-R_S(A(S))]| <= beta_m", 14, 700, cls="math")]
    out += [text(830, 515, "small gap alone does not imply small risk。", 15, fill=MUTED)]
    return finish(out, "稳定性把一个算法的单样本敏感性，转成期望泛化间隙的证书。")


def regularized_erm():
    out = begin(
        "正则化 ERM：曲率把数据扰动变成稳定性",
        "相邻数据集产生两个强凸目标。把两个最优性不等式相加后，共享样本项抵消；只剩被替换样本的两个 Lipschitz 差，与强凸二次下界平衡。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "相邻目标与两个极小点", BLUE)
    out += [line(62, 390, 345, 390, GRID, 2), line(62, 100, 62, 390, GRID, 2)]
    out += [path("M70 150C130 330 180 370 220 365C270 355 305 265 340 125", BLUE, 3)]
    out += [path("M70 115C120 275 165 350 205 365C250 380 300 325 340 175", TEAL, 3)]
    out += [circle(220, 365, 7, BLUE, BLUE), circle(205, 365, 7, TEAL, TEAL)]
    out += [text(230, 350, "w_S", 15, 700, fill=BLUE), text(158, 350, "w_S'", 15, 700, fill=TEAL)]
    out += [line(205, 420, 220, 420, RED, 3)]
    out += [text(212, 450, "Delta", 15, 700, "middle", fill=RED)]
    out += [text(45, 495, "lambda-strong convexity supplies curvature", 14, 650)]
    out += [text(45, 515, "the minimizer is unique under this contract。", 15, fill=MUTED)]

    heading(out, 430, "B", "相加后，共享样本抵消", TEAL)
    node(out, 445, 100, 310, 60, "F_S(w') - F_S(w)", BLUE, size=16)
    node(out, 445, 205, 310, 60, "F_S'(w) - F_S'(w')", TEAL, size=16)
    out += [line(600, 164, 600, 197, INK, 2.4, marker="a3")]
    out += [line(470, 300, 730, 300, GRID, 2)]
    out += [text(600, 340, "shared m-1 terms cancel", 15, 700, "middle", fill=TEAL)]
    out += [text(430, 390, "lambda ||Delta||^2 <= (2L/m)||Delta||", 14, 650, cls="math")]
    out += [text(430, 435, "||Delta|| <= 2L/(lambda m)", 16, 700, fill=RED, cls="math")]
    out += [text(430, 480, "then loss stability <= L ||Delta||", 14, 650)]
    out += [text(430, 515, "smoothness is not needed for the exact minimizer。", 15, fill=MUTED)]

    heading(out, 830, "C", "正则强度不是免费午餐", RED)
    out += [line(860, 390, 1125, 390, GRID, 2), line(860, 105, 860, 390, GRID, 2)]
    out += [path("M870 350C930 285 1015 195 1118 125", TEAL, 3)]
    out += [path("M870 130C940 190 1020 290 1118 350", RED, 3)]
    out += [text(885, 325, "stability improves", 14, 700, fill=TEAL)]
    out += [text(985, 170, "bias can grow", 14, 700, fill=RED)]
    out += [text(1085, 420, "lambda", 14, 650)]
    out += [text(830, 455, "beta_m <= 2L^2/(lambda m)", 16, 700, fill=BLUE, cls="math")]
    out += [text(830, 490, "choose lambda with a declared validation protocol", 14, 650)]
    out += [text(830, 515, "scale-invariant nets require function-level audit。", 15, fill=MUTED)]
    return finish(out, "强凸性控制参数位移，Lipschitz 损失再把位移变成稳定性。")


def sgd_coupling():
    out = begin(
        "SGD 耦合轨迹、扩张因子与训练时间",
        "在相邻数据集上复用相同初始化和随机索引。多数步骤读取相同样本；只有以一除以 m 的概率读到不同坐标。更新映射是否收缩、非扩张或扩张，决定扰动如何累积。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "两条轨迹共享随机索引", BLUE)
    pts1 = ((70, 320), (125, 285), (180, 245), (235, 205), (290, 180), (345, 155))
    pts2 = ((70, 320), (125, 285), (180, 245), (235, 250), (290, 285), (345, 315))
    for pts, col in ((pts1, BLUE), (pts2, TEAL)):
        for j in range(len(pts) - 1):
            out += [line(*pts[j], *pts[j + 1], col, 3)]
        for x, y in pts:
            out += [circle(x, y, 5, col, col)]
    out += [line(180, 245, 235, 250, RED, 2.5, "5 4")]
    out += [text(190, 225, "first hit of i*", 14, 700, fill=RED)]
    out += [text(45, 390, "same init + same I_t + same randomness", 14, 700)]
    out += [text(45, 435, "P{I_t=i*}=1/m under replacement sampling", 14, 650, cls="math")]
    out += [text(45, 480, "before the first hit, the paths coincide", 14, 650)]
    out += [text(45, 515, "a coupling is a proof device, not two retrainings。", 15, fill=MUTED)]

    heading(out, 430, "B", "一步映射控制扰动传播", TEAL)
    for y, col, title, factor in (
        (105, TEAL, "strongly convex + smooth", "q < 1  contractive"),
        (230, BLUE, "convex + smooth", "q = 1  nonexpansive"),
        (355, RED, "smooth nonconvex", "q <= 1 + eta gamma"),
    ):
        out += [rect(445, y, 310, 78, col, BG, 8, 2)]
        out += [text(600, y + 30, title, 15, 700, "middle", fill=col)]
        out += [text(600, y + 61, factor, 14, 650, "middle", cls="math")]
    out += [text(430, 485, "hit step adds at most 2 eta_t L", 14, 650, cls="math")]
    out += [text(430, 515, "regularity must hold along the coupled paths。", 15, fill=MUTED)]

    heading(out, 830, "C", "步长总和成为稳定性预算", RED)
    out += [text(830, 120, "convex smooth case", 16, 700, fill=BLUE)]
    out += [text(830, 165, "epsilon_stab <= (2L^2/m) sum_t eta_t", 14, 700, cls="math")]
    out += [line(850, 375, 1125, 375, GRID, 2), line(850, 215, 850, 375, GRID, 2)]
    out += [path("M860 355C930 335 1000 300 1115 235", RED, 3)]
    out += [path("M860 235C930 270 1000 320 1115 350", TEAL, 3)]
    out += [text(890, 340, "stability cost", 14, 700, fill=RED)]
    out += [text(1010, 335, "optimization error", 14, 700, fill=TEAL)]
    out += [text(830, 425, "early stopping balances two errors", 14, 650)]
    out += [text(830, 470, "mini-batch and adaptive updates need new maps", 14, 650)]
    out += [text(830, 515, "global deep-net assumptions may be vacuous。", 15, fill=MUTED)]
    return finish(out, "SGD 稳定性由遇到差异的概率、单步扩张率和训练时长共同决定。")


def sample_compression():
    out = begin(
        "样本压缩：从少量见证到一致重构与泛化",
        "compression map 从完整标注样本选择至多 k 个见证和有限 side message；reconstruction map 仅凭这些信息恢复 hypothesis，并必须与完整样本一致。计数压缩选择即可控制坏假设漏过其余样本的概率。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "压缩器只保留少量见证", BLUE)
    for j in range(12):
        x = 57 + (j % 6) * 54
        y = 125 + (j // 6) * 70
        keep = j in (2, 7, 10)
        col = RED if keep else GRID
        out += [circle(x, y, 13, col, BG, 2.5)]
        out += [text(x, y + 5, "+" if j % 2 == 0 else "−", 14, 700, "middle", fill=col if keep else MUTED)]
    out += [line(200, 285, 200, 325, BLUE, 2.5, marker="a0")]
    node(out, 90, 340, 220, 62, "k labeled points + message", BLUE, size=15)
    out += [text(45, 455, "kappa(S) is selected after seeing S", 14, 650)]
    out += [text(45, 490, "adaptive selection is paid by counting subsets", 14, 650)]
    out += [text(45, 515, "ordering and side bits must be declared。", 15, fill=MUTED)]

    heading(out, 430, "B", "重构必须解释完整样本", TEAL)
    node(out, 450, 115, 125, 62, "compressed set", BLUE, size=15)
    node(out, 450, 285, 125, 62, "side message", RED, size=15)
    out += [line(580, 146, 650, 220, BLUE, 2.5, marker="a0")]
    out += [line(580, 316, 650, 240, RED, 2.5, marker="a2")]
    node(out, 665, 190, 90, 82, "rho", TEAL, size=18)
    out += [line(710, 277, 710, 320, TEAL, 2.5, marker="a1")]
    out += [text(710, 355, "h = rho(kappa(S),q)", 15, 700, "middle", cls="math")]
    out += [text(430, 405, "h(x_i)=y_i for every point in S", 14, 700, fill=TEAL, cls="math")]
    out += [text(430, 455, "consistency is a theorem condition", 14, 650)]
    out += [text(430, 490, "fitting only retained points is insufficient", 14, 650)]
    out += [text(430, 515, "lossy compression needs another theorem。", 15, fill=MUTED)]

    heading(out, 830, "C", "计数 × 漏检概率", RED)
    node(out, 845, 95, 285, 64, "number of descriptions", BLUE, size=16)
    out += [text(987, 195, "2^b binom(m,k)", 17, 700, "middle", fill=BLUE, cls="math")]
    out += [text(987, 235, "times", 15, 650, "middle")]
    node(out, 845, 255, 285, 64, "bad h misses m-k checks", TEAL, size=15)
    out += [text(987, 355, "(1-epsilon)^(m-k)", 17, 700, "middle", fill=TEAL, cls="math")]
    out += [line(850, 390, 1125, 390, GRID, 2)]
    out += [text(830, 430, "R(h) <= [log binom(m,k)+b log 2", 14, 650, cls="math")]
    out += [text(830, 462, "+ log(1/delta)]/(m-k)", 14, 650, cls="math")]
    out += [text(830, 495, "model-file compression is not automatically this", 14, 650)]
    out += [text(830, 515, "sample points may contain many bits。", 15, fill=MUTED)]
    return finish(out, "样本压缩证书依赖少量见证、合法重构、全样本一致与完整计数。")


FIGURES = {
    "fig-replace-one-stability-generalization-v2.svg": replace_one_stability,
    "fig-regularized-erm-curvature-stability-v2.svg": regularized_erm,
    "fig-sgd-coupled-trajectories-stability-v2.svg": sgd_coupling,
    "fig-sample-compression-generalization-v2.svg": sample_compression,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()

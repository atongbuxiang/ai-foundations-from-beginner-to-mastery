#!/usr/bin/env python3
"""Generate v2 textbook figures for GEO-01--04 geometry foundations."""

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


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "geometry"


def metric_topology():
    out = begin(
        "度量生成拓扑、映射正则性与 AI 空间合同",
        "metric 的 balls 生成 open sets 和 topology；不同数值尺度的 metrics 可诱导同一 topology，却有不同 Lipschitz、Cauchy 或 completeness 性质；连续、uniform continuous 与 Lipschitz 是不同映射强度，AI 声明还需定义 domain 和 sampling。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "不同 ball 形状可生成同一拓扑", BLUE)
    out += [circle(120, 245, 75, BLUE, BG, 2.5), circle(120, 245, 38, BLUE, BG, 2), rect(235, 170, 145, 145, TEAL, BG, 0, 2.5), rect(270, 205, 75, 75, TEAL, BG, 0, 2)]
    out += [text(85, 355, "d_2 balls", 15, 700, fill=BLUE), text(268, 355, "d_infty balls", 15, 700, fill=TEAL), text(45, 403, "finite-dimensional norm metrics", 15, 650), text(45, 432, "can induce the same open sets", 15, 650), text(45, 465, "but constants, balls and geodesics differ", 15, 650, fill=RED), text(45, 503, "same topology may differ in completeness。", 14, fill=MUTED)]

    heading(out, 430, "B", "映射强度与紧致性分层", TEAL)
    stages = (("Lipschitz", "d_Y(Fx,Fy)<=L d_X(x,y)", BLUE), ("uniform continuity", "one delta works for all x", TEAL), ("continuity", "delta may depend on x", RED))
    for i, (name, claim, color) in enumerate(stages):
        yy = 92 + i * 104
        node(out, 445, yy, 150, 55, name, color, size=14)
        out += [line(598, yy + 28, 620, yy + 28, INK, 2, marker="a3"), text(635, yy + 34, claim, 13, 650)]
    out += [line(430, 410, 765, 410, GRID, 2), text(430, 442, "continuous on compact -> uniform", 15, 700, fill=TEAL), text(430, 472, "closed + bounded -> compact only in", 15, 650), text(430, 495, "finite-dimensional Euclidean settings", 15, 650, fill=RED), text(430, 519, "infinite dimension needs extra compactness。", 14, fill=MUTED)]

    heading(out, 830, "C", "AI 声明必须交付四层对象", RED)
    layers = (("underlying set X", BLUE), ("ground metric / topology", TEAL), ("population + sampling model", RED), ("map regularity / invariance claim", BLUE))
    for i, (label, color) in enumerate(layers):
        yy = 90 + i * 92
        node(out, 840, yy, 300, 56, label, color, size=14)
        if i < 3:
            out.append(line(990, yy + 59, 990, yy + 85, INK, 2.1, marker="a3"))
    out += [text(830, 472, "finite samples do not prove support topology", 14, 650, fill=RED), text(830, 502, "metric choice changes neighbors and robustness。", 14, fill=MUTED)]
    return finish(out, "度量提供尺度，拓扑保留邻域结构；映射定理和 AI 几何声明只有在空间、采样与正则性合同完整时成立。")


def smooth_manifold():
    out = begin(
        "Charts、切余切空间与 decoder Jacobian 边界",
        "smooth manifold 由局部 Euclidean charts 和光滑 transition maps 胶合；tangent vectors 描述一阶运动，cotangent vectors 描述线性测量；pushforward 与 pullback 方向相反，decoder Jacobian 只有在 rank 和局部嵌入条件下才给候选 tangent space。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "流形由相容局部坐标胶合", BLUE)
    out += [path("M55 285 C90 135 245 110 355 250 C285 400 125 390 55 285", GRID, 3), circle(195, 250, 6, RED, RED)]
    out += [rect(65, 105, 120, 90, BLUE, BG, 6, 2), rect(225, 115, 120, 90, TEAL, BG, 6, 2), line(185, 150, 225, 150, INK, 2.2, marker="a3")]
    out += [text(100, 155, "chart phi", 15, 700, fill=BLUE), text(258, 165, "chart psi", 15, 700, fill=TEAL), text(45, 425, "psi o phi^{-1}: overlap -> overlap", 15, 650), text(45, 456, "transition maps must be smooth", 15, 650), text(45, 486, "one global chart may be impossible", 15, 650, fill=RED), text(45, 514, "point cloud patches are not an atlas proof。", 14, fill=MUTED)]

    heading(out, 430, "B", "tangent 运动，cotangent 测量", TEAL)
    out += [circle(550, 245, 8, RED, RED), line(550, 245, 710, 165, BLUE, 3, marker="a1"), line(550, 245, 690, 315, TEAL, 3, marker="a1"), text(710, 155, "v in T_pM", 15, 700, "end", fill=BLUE), text(705, 340, "w in T_pM", 15, 700, "end", fill=TEAL)]
    out += [text(430, 100, "df_p in T_p^*M", 16, 700, fill=RED), text(430, 380, "df_p(v): directional measurement", 15, 650), text(430, 414, "dF_p: T_pM -> T_F(p)N", 15, 650), text(430, 446, "F^*: T^*N -> T^*M", 15, 650), text(430, 478, "gradient needs an added metric", 15, 650, fill=RED), text(430, 508, "covectors do not canonically equal vectors。", 14, fill=MUTED)]

    heading(out, 830, "C", "decoder Jacobian：候选切空间", RED)
    node(out, 840, 88, 300, 58, "latent z -> decoder D(z)", BLUE, size=14)
    out += [line(990, 149, 990, 186, INK, 2.2, marker="a3")]
    node(out, 840, 198, 300, 70, "columns of J_D(z)", TEAL, size=15)
    out += [line(990, 271, 990, 308, INK, 2.2, marker="a3")]
    node(out, 840, 320, 300, 70, "candidate image tangent", RED, size=15)
    out += [text(830, 430, "check rank + local injectivity", 15, 650), text(830, 460, "chart overlap + reconstruction identity", 14, 650), text(830, 489, "radius / curvature / noise / boundary", 14, 650, fill=RED), text(830, 516, "low loss is not a manifold certificate。", 14, fill=MUTED)]
    return finish(out, "光滑流形的局部线性化来自相容 charts；切向量、余切测量和学习到的 Jacobian 必须按类型与条件分开。")


def riemannian():
    out = begin(
        "Riemannian metric、测地线与流形优化更新",
        "Riemannian metric 在每个 tangent fiber 上给内积并随位置光滑变化；它诱导长度、距离、gradient 与 Levi–Civita connection；geodesic、exponential 与 retraction 的角色不同，优化需将 ambient differential 转成 tangent update 并检查约束。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "位置相关内积与 gradient", BLUE)
    for x, y, rx, ry, angle in ((100, 180, 55, 28, -20), (220, 270, 35, 65, 25), (320, 165, 62, 24, 10)):
        out.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" transform="rotate({angle} {x} {y})" fill="none" stroke="{TEAL}" stroke-width="2.3"/>')
        out.append(circle(x, y, 5, BLUE, BLUE))
    out += [text(45, 365, "g_p(v,w)=v^T G(p) w", 16, 700, cls="math"), text(45, 401, "df_p is fixed； grad_g f=G(p)^{-1} df", 14, 650), text(45, 438, "unit balls and steepest directions vary", 15, 650), text(45, 478, "coordinates change； geometric scalar does not", 14, 650), text(45, 508, "Riemannian metric != point distance。", 15, fill=MUTED)]

    heading(out, 430, "B", "geodesic：connection 零加速度", TEAL)
    out += [circle(475, 300, 7, BLUE, BLUE), circle(735, 180, 7, RED, RED), path("M480 300 C555 205 650 200 730 180", TEAL, 3), path("M480 300 C520 85 700 390 730 180", RED, 2.5), path("M480 300 C570 250 660 215 730 180", BLUE, 2, "7 5")]
    out += [text(470, 350, "p", 15, 700, fill=BLUE), text(735, 160, "q", 15, 700, fill=RED), text(430, 390, "nabla_{gamma dot} gamma dot=0", 15, 700, cls="math"), text(430, 425, "affine parametrization matters", 15, 650), text(430, 457, "locally minimizing != globally shortest", 15, 650, fill=RED), text(430, 490, "Exp_p(v) follows the exact geodesic", 15, 650), text(430, 516, "retraction only matches locally。", 14, fill=MUTED)]

    heading(out, 830, "C", "优化更新回到 manifold", RED)
    stages = (("ambient / coordinate differential", BLUE), ("metric -> grad f in T_pM", TEAL), ("step by Exp_p or retraction R_p", RED), ("verify feasibility + stationarity", BLUE))
    for i, (label, color) in enumerate(stages):
        yy = 88 + i * 92
        node(out, 840, yy, 300, 56, label, color, size=14)
        if i < 3:
            out.append(line(990, yy + 59, 990, yy + 85, INK, 2.1, marker="a3"))
    out += [text(830, 470, "projection / normalization may be retractions", 14, 650), text(830, 500, "but not generally the exponential map。", 14, fill=MUTED)]
    return finish(out, "Riemannian metric 把 differential 变成 gradient；优化可用 retraction，但须声明近似阶与约束。")


def lie_group():
    out = begin(
        "Lie group–algebra、作用轨道与等变交换图",
        "Lie group 同时具有光滑流形和群结构；单位元 tangent space 是 Lie algebra，exponential 把局部生成元积分成有限变换，bracket 测量不交换；group action 产生 orbit/stabilizer，equivariant model 使输入和输出作用组成 commuting square。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "单位元 tangent 编码连续局部变换", BLUE)
    out += [circle(190, 245, 125, BLUE, BG, 2.5), circle(190, 245, 7, RED, RED), text(205, 238, "e", 16, 700, fill=RED), line(190, 245, 300, 145, TEAL, 3, marker="a1"), text(315, 140, "xi in g=T_eG", 15, 700, "end", fill=TEAL)]
    out += [path("M200 235 C245 220 285 205 330 180", BLUE, 2.5), text(45, 405, "exp_G(t xi): generator -> one-parameter subgroup", 14, 650), text(45, 440, "[A,B]=AB-BA measures infinitesimal", 14, 650), text(45, 463, "noncommutativity / BCH correction", 14, 650), text(45, 494, "Lie exp != Riemannian Exp in general", 14, 650, fill=RED), text(45, 518, "algebra sees only the identity component。", 14, fill=MUTED)]

    heading(out, 430, "B", "作用把空间分成 orbit 与 stabilizer", TEAL)
    out += [circle(600, 255, 7, RED, RED)]
    for angle, x, y in ((0, 720, 255), (1, 675, 155), (2, 520, 145), (3, 480, 280), (4, 585, 360), (5, 710, 345)):
        out += [circle(x, y, 6, TEAL, TEAL), path(f"M600 255 Q{(600+x)/2:.0f} {(255+y)/2-25:.0f} {x} {y}", GRID, 1.8)]
    out += [text(430, 405, "orbit G dot x = reachable states", 15, 650), text(430, 437, "stabilizer G_x = transformations fixing x", 15, 650), text(430, 469, "orbit ~= G/G_x under regular conditions", 15, 650), text(430, 501, "same orbit != semantic equivalence。", 15, fill=MUTED)]

    heading(out, 830, "C", "equivariance 交换图", RED)
    node(out, 840, 90, 115, 55, "x", BLUE)
    node(out, 1025, 90, 115, 55, "F(x)", TEAL)
    node(out, 840, 285, 115, 55, "g dot x", RED)
    node(out, 1025, 285, 115, 55, "g dot F(x)", BLUE)
    out += [line(958, 118, 1018, 118, INK, 2.1, marker="a3"), line(958, 313, 1018, 313, INK, 2.1, marker="a3"), line(898, 148, 898, 278, INK, 2.1, marker="a3"), line(1082, 148, 1082, 278, INK, 2.1, marker="a3")]
    out += [text(830, 390, "F(g dot x)=g dot F(x)", 16, 700, fill=RED), text(830, 425, "invariance: output action is trivial", 15, 650), text(830, 457, "augmentation != exact architectural law", 15, 650, fill=RED), text(830, 489, "state input/output representations", 15, 650), text(830, 514, "and tested group elements。", 14, fill=MUTED)]
    return finish(out, "Lie theory 区分有限变换、无穷小生成元与作用；equivariance 是有类型的交换关系。")


FIGURES = {
    "fig-metric-topology-continuity-v2.svg": metric_topology,
    "fig-smooth-manifold-tangent-cotangent-v2.svg": smooth_manifold,
    "fig-riemannian-geodesic-optimization-v2.svg": riemannian,
    "fig-lie-group-algebra-equivariance-v2.svg": lie_group,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()

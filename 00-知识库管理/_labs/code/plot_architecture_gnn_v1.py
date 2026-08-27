#!/usr/bin/env python3
"""Generate the eight original ARCH-17--24 GNN teaching figures."""

from __future__ import annotations

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    AMBER, BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "architecture"


def graph(out, coords, edges, labels, offset_x=0, offset_y=0, color=BLUE):
    for a, b in edges:
        x1, y1 = coords[a]; x2, y2 = coords[b]
        out.append(line(x1 + offset_x, y1 + offset_y, x2 + offset_x, y2 + offset_y, GRID, 3))
    for k, (x, y) in coords.items():
        out.append(circle(x + offset_x, y + offset_y, 20, color, BG, 2.5))
        out.append(text(x + offset_x, y + offset_y + 6, labels[k], 15, 700, "middle", color))


def relabeling_symmetry():
    out = begin(
        "图重标号：表示改变，对象不变",
        "同一抽象图可由不同邻接矩阵表示；节点级函数应等变，图级函数应不变。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "同一图的两种编号", BLUE)
    coords = {0: (90, 120), 1: (250, 120), 2: (170, 225)}
    edges = ((0, 1), (1, 2), (2, 0))
    graph(out, coords, edges, {0: "1", 1: "2", 2: "3"})
    out += [text(170, 265, "A, X", 17, 700, "middle", BLUE), line(65, 285, 335, 285, GRID, 2)]
    lower = {0: (90, 335), 1: (250, 335), 2: (170, 440)}
    graph(out, lower, edges, {0: "3", 1: "1", 2: "2"}, color=TEAL)
    out += [text(170, 490, "P A P^T, P X", 17, 700, "middle", TEAL)]

    heading(out, 430, "B", "节点输出必须共同重排", TEAL)
    node(out, 455, 115, 295, 70, "F(P A P^T, P X)", BLUE, "#EFF6FF", 17)
    out += [line(602, 188, 602, 235, TEAL, 3, marker="a1")]
    node(out, 455, 250, 295, 70, "= P F(A, X)", TEAL, "#ECFDF5", 18)
    out += [text(455, 385, "预测跟着节点走，", 17, 650), text(455, 420, "而不是粘在行号上。", 17, 700, fill=TEAL)]
    out += [text(455, 470, "边方向、self-loop、edge type", 15, fill=MUTED), text(455, 498, "必须先写入数据合同。", 15, fill=MUTED)]

    heading(out, 830, "C", "图级读出必须不变", RED)
    for y, lab in ((120, "node states H"), (230, "sum / invariant readout"), (340, "graph prediction")):
        node(out, 845, y, 280, 62, lab, BLUE if y == 120 else TEAL if y == 230 else RED,
             "#F8FAFC", 16)
        if y < 340:
            out.append(line(985, y + 65, 985, y + 102, INK, 2.5, marker="a3"))
    out += [text(845, 445, "rho(PH) = rho(H)", 19, 700, cls="math"),
            text(845, 485, "对称性是模型合同，不是数据增强技巧。", 15, fill=MUTED)]
    return finish(out, "先把图看作重标号等价类，再定义等变层和不变任务出口。")


def mpnn_pipeline():
    out = begin(
        "MPNN：message、aggregate、update 与 readout",
        "边上生成消息，节点处对多重集聚合，再更新状态；K 层只能使用 K 跳计算图。",
        (TEAL, BLUE, RED),
    )
    heading(out, 42, "A", "一条边怎样产生消息", TEAL)
    out += [circle(95, 190, 28, BLUE, "#EFF6FF", 2.5), text(95, 196, "h_j", 16, 700, "middle", BLUE),
            circle(300, 190, 28, TEAL, "#ECFDF5", 2.5), text(300, 196, "h_i", 16, 700, "middle", TEAL),
            line(126, 190, 267, 190, RED, 3, marker="a2"), text(198, 170, "e_ji", 15, 650, "middle", RED)]
    node(out, 70, 280, 255, 70, "m_ji = M(h_i, h_j, e_ji)", BLUE, "#F8FAFC", 15)
    out += [text(45, 425, "有向图需区分 j->i 与 i->j；", 15, fill=MUTED),
            text(45, 458, "同步层先用旧状态生成全部消息。", 15, fill=MUTED)]

    heading(out, 430, "B", "邻居处必须做多重集聚合", BLUE)
    for x, lab in ((460, "m_1i"), (565, "m_2i"), (670, "m_3i")):
        node(out, x, 115, 76, 46, lab, BLUE, "#EFF6FF", 14)
        out.append(line(x + 38, 164, 602, 235, BLUE, 2, marker="a0"))
    node(out, 505, 245, 195, 62, "AGG{m_ji}", TEAL, "#ECFDF5", 17)
    out += [line(602, 310, 602, 350, TEAL, 3, marker="a1")]
    node(out, 505, 365, 195, 62, "U(h_i, m_i)", RED, "#FFF7ED", 17)
    out += [text(440, 475, "sum / mean / max 的信息损失不同。", 15, fill=MUTED)]

    heading(out, 830, "C", "深度、采样与成本账", RED)
    for i, (lab, val) in enumerate((("1 layer", "1-hop"), ("K layers", "at most K-hop"),
                                     ("fan-out s", "about s^K tree"), ("sparse full", "O(|E|d) / layer"))):
        y = 105 + i * 90
        out += [text(845, y, lab, 15, 700, fill=RED), text(955, y, val, 16, 650)]
    out += [text(845, 470, "感受野存在，不等于远程信息可恢复。", 15, fill=MUTED)]
    return finish(out, "MPNN 的最小合同是局部消息、无序聚合、同步更新与任务读出。")


def spectral_spatial():
    out = begin(
        "从图 Laplacian 频域到 GCN 邻居平均",
        "谱滤波由 Laplacian 特征基定义；多项式近似带来局部性，GCN 得到一阶归一化传播。",
        (BLUE, AMBER, TEAL),
    )
    heading(out, 42, "A", "图频率：L = U Lambda U^T", BLUE)
    out += [path("M65 380C105 360 120 165 170 150C225 132 250 330 335 185", BLUE, 3),
            line(55, 390, 350, 390, GRID, 2), text(60, 130, "graph signal x", 16, 700, fill=BLUE),
            text(55, 455, "x_hat = U^T x", 18, 700, cls="math"),
            text(55, 490, "g(L)x = U g(Lambda) U^T x", 16, 650, cls="math")]

    heading(out, 430, "B", "多项式 = 有限跳传播", AMBER)
    for r, c in ((125, "#FFF7ED"), (80, "#ECFDF5"), (35, "#EFF6FF")):
        out.append(circle(600, 260, r, AMBER if r == 125 else TEAL if r == 80 else BLUE, c, 2))
    out += [circle(600, 260, 10, RED, RED), text(600, 265, "v", 15, 700, "middle", BG),
            text(452, 420, "sum_(k=0)^K theta_k L^k x", 17, 700, cls="math"),
            text(445, 462, "K 次乘法只到 K-hop；无需显式 U。", 15, fill=MUTED)]

    heading(out, 830, "C", "GCN 的一阶传播合同", TEAL)
    node(out, 840, 110, 300, 62, "A_tilde = A + I", BLUE, "#EFF6FF", 17)
    out += [line(990, 175, 990, 210, INK, 2.5, marker="a3")]
    node(out, 840, 225, 300, 76, "S = D_tilde^(-1/2) A_tilde D_tilde^(-1/2)", TEAL, "#ECFDF5", 14)
    out += [line(990, 304, 990, 339, INK, 2.5, marker="a3")]
    node(out, 840, 354, 300, 62, "H' = sigma(S H W)", RED, "#FFF7ED", 17)
    out += [text(840, 470, "谱动机 != 任意图上的平移卷积。", 15, fill=MUTED)]
    return finish(out, "多项式把频域函数变成局部算子；GCN 再把它压缩为规范化的一阶邻域混合。")


def multiset_gin():
    out = begin(
        "多重集聚合：mean/max 碰撞与 GIN 的可辨识合同",
        "邻域不是普通集合而是带重复计数的多重集；不同聚合器会永久丢失不同信息。",
        (RED, BLUE, TEAL),
    )
    heading(out, 42, "A", "mean 丢失倍数", RED)
    for y, vals in ((145, (1, 3)), (305, (1, 1, 3, 3))):
        for i, v in enumerate(vals):
            out += [circle(75 + i * 65, y, 22, BLUE, "#EFF6FF", 2), text(75 + i * 65, y + 6, v, 15, 700, "middle", BLUE)]
        out += [text(335, y + 6, "mean = 2", 17, 700, "end", RED)]
    out += [text(45, 430, "不同 cardinality，同一输出。", 16, fill=MUTED)]

    heading(out, 430, "B", "max 丢失计数与次大值", BLUE)
    for y, vals in ((145, (1, 3)), (305, (2, 3, 3))):
        for i, v in enumerate(vals):
            out += [rect(455 + i * 65, y - 22, 44, 44, BLUE, "#EFF6FF", 5, 2), text(477 + i * 65, y + 6, v, 15, 700, "middle", BLUE)]
        out += [text(755, y + 6, "max = 3", 17, 700, "end", RED)]
    out += [text(445, 430, "未进入最大值的元素不可恢复。", 16, fill=MUTED)]

    heading(out, 830, "C", "sum + injective maps 的条件", TEAL)
    node(out, 845, 105, 280, 58, "multiset -> sum phi(x)", TEAL, "#ECFDF5", 16)
    out += [line(985, 166, 985, 200, TEAL, 2.5, marker="a1")]
    node(out, 845, 215, 280, 58, "combine self with (1+eps)", BLUE, "#EFF6FF", 15)
    out += [line(985, 276, 985, 310, BLUE, 2.5, marker="a0")]
    node(out, 845, 325, 280, 58, "MLP update + invariant readout", RED, "#FFF7ED", 15)
    out += [text(845, 430, "结论依可数域、injectivity 与容量。", 15, fill=MUTED),
            text(845, 465, "GIN 达到 1-WL，不超越 1-WL。", 15, 700, fill=RED)]
    return finish(out, "聚合后的碰撞无法被后续 MLP 修复；先审计保留了哪些多重集统计。")


def depth_failures():
    out = begin(
        "深层 GNN 的两种不同失效：平滑与挤压",
        "重复扩散使节点表示趋同；远程信息则可能在狭窄 cut 中被压入固定维向量。",
        (TEAL, RED, BLUE),
    )
    heading(out, 42, "A", "Over-smoothing：节点变相似", TEAL)
    colors = (RED, BLUE, AMBER, TEAL)
    for k in range(4):
        x = 70 + k * 90
        out += [circle(x, 145, 18, colors[k], colors[k], 1), circle(x, 300, 18, TEAL, "#BFE8DF", 2)]
        out += [line(x, 170, x, 275, GRID, 2, marker="a4")]
    out += [text(45, 395, "层数增加：高频差异被反复平均", 16, 700, fill=TEAL),
            text(45, 440, "极限与速率依传播谱和权重条件。", 15, fill=MUTED)]

    heading(out, 430, "B", "Over-squashing：远端扇入瓶颈", RED)
    for i in range(8):
        y = 95 + i * 52
        out += [circle(460, y, 7, BLUE, BLUE, 1), line(470, y, 590, 255, GRID, 1.6)]
    out += [rect(590, 218, 40, 75, RED, "#FEE2E2", 4, 2.5), text(610, 260, "cut", 15, 700, "middle", RED),
            line(633, 255, 735, 255, RED, 3, marker="a1"), circle(755, 255, 20, TEAL, "#ECFDF5", 2),
            text(755, 260, "v", 15, 700, "middle", TEAL), text(445, 430, "许多远程信号 -> 固定宽度 h_v", 16, 700),
            text(445, 470, "增加层数可能扩大来源，却不拓宽 cut。", 15, fill=MUTED)]

    heading(out, 830, "C", "诊断与干预要配对", BLUE)
    rows = ((105, "smooth", "pairwise distance / Dirichlet energy", "residual, norm, decouple"),
            (225, "squash", "long-range sensitivity / cut", "rewire, global path, width"),
            (345, "both", "task curve vs depth", "joint ablation"))
    for y, kind, metric, action in rows:
        out += [text(845, y, kind, 15, 700, fill=RED if kind == "squash" else TEAL),
                text(845, y + 27, metric, 14, 650), text(845, y + 54, action, 14, fill=MUTED)]
    out += [text(845, 470, "“深了变差”不是机制诊断。", 16, 700, fill=RED)]
    return finish(out, "平滑是状态趋同，挤压是信息瓶颈；二者需要不同测量、反例和干预。")


def graph_attention():
    out = begin(
        "图注意力：结构 mask 内的内容依赖加权",
        "每个目标节点只在其邻域上归一化权重；多头改变通道，但不自动成为全局检索或解释。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "以 i 为中心的 masked softmax", BLUE)
    center = (200, 260)
    for ang, pos, score in (("j1", (95, 135), "0.70"), ("j2", (85, 360), "0.10"), ("j3", (315, 145), "0.20")):
        out += [circle(pos[0], pos[1], 22, BLUE, "#EFF6FF", 2), text(pos[0], pos[1] + 6, ang, 15, 700, "middle", BLUE),
                line(pos[0], pos[1], center[0], center[1], TEAL, 2 + 5 * float(score), marker="a1"),
                text((pos[0] + center[0]) / 2, (pos[1] + center[1]) / 2 - 8, score, 14, 700, "middle", RED)]
    out += [circle(*center, 26, TEAL, "#ECFDF5", 2.5), text(200, 266, "i", 17, 700, "middle", TEAL),
            text(45, 455, "sum_(j in N(i)) alpha_ij = 1", 17, 700, cls="math")]

    heading(out, 430, "B", "score、normalization、message 分开", TEAL)
    for y, lab, col in ((105, "e_ij = a(W h_i, W h_j)", BLUE),
                        (220, "alpha_ij = softmax over N(i)", TEAL),
                        (335, "h_i' = sigma sum alpha_ij W h_j", RED)):
        node(out, 445, y, 310, 62, lab, col, "#F8FAFC", 15)
        if y < 335:
            out.append(line(600, y + 65, 600, y + 105, INK, 2, marker="a3"))
    out += [text(445, 455, "edge features / direction 要显式进入 score。", 15, fill=MUTED)]

    heading(out, 830, "C", "四个不能自动推出的结论", RED)
    claims = ("global attention", "faithful explanation", "beyond 1-WL", "robust to graph noise")
    for i, claim in enumerate(claims):
        y = 112 + i * 86
        out += [circle(855, y - 5, 13, RED, "#FEE2E2", 2), text(855, y, "x", 15, 700, "middle", RED),
                text(883, y, claim, 16, 650)]
    out += [text(845, 470, "这些需要额外结构或独立证据。", 15, fill=MUTED)]
    return finish(out, "GAT 学的是邻域内的相对权重；结构可见性与证据边界仍由图合同决定。")


def task_interface():
    out = begin(
        "图任务接口：等变输出、不变读出与异构关系",
        "节点、边、链接和整图任务使用不同输出对象；异构图还需声明节点/边类型与泄漏边界。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "四类输出对象", BLUE)
    items = ((105, "node", "one label per node", BLUE), (205, "edge", "observed edge target", TEAL),
             (305, "link", "candidate pair score", RED), (405, "graph", "invariant readout", AMBER))
    for y, lab, desc, col in items:
        out += [text(50, y, lab, 16, 700, fill=col), text(135, y, desc, 15, 650)]

    heading(out, 430, "B", "从节点状态到图表示", TEAL)
    for x in (460, 535, 610, 685):
        out += [circle(x, 130, 18, BLUE, "#EFF6FF", 2), line(x, 152, 600, 225, GRID, 2, marker="a4")]
    node(out, 515, 235, 170, 58, "sum / set readout", TEAL, "#ECFDF5", 15)
    out += [line(600, 296, 600, 335, TEAL, 3, marker="a1")]
    node(out, 515, 350, 170, 58, "graph vector", RED, "#FFF7ED", 16)
    out += [text(445, 455, "mean 归一化规模；sum 保留计数线索。", 15, fill=MUTED)]

    heading(out, 830, "C", "异构图与 split 合同", RED)
    out += [circle(875, 145, 22, BLUE, "#EFF6FF", 2), text(875, 151, "user", 14, 700, "middle", BLUE),
            circle(1080, 145, 22, TEAL, "#ECFDF5", 2), text(1080, 151, "item", 14, 700, "middle", TEAL),
            line(900, 145, 1055, 145, RED, 3, marker="a2"), text(977, 125, "buys", 14, 700, "middle", RED)]
    rows = ((245, "relation-specific W_r"), (305, "inverse/self-loop convention"),
            (365, "remove target edge before encoding"), (425, "inductive vs transductive split"))
    for y, lab in rows:
        out += [text(845, y, "•", 18, 700, fill=RED), text(870, y, lab, 15, 650)]
    return finish(out, "先声明预测对象、对称性和 split，再选择 readout、decoder 与关系参数化。")


def wl_evidence():
    out = begin(
        "1-WL 颜色细化、结构反例与证据地图",
        "1-WL 反复散列自身颜色与邻居颜色多重集；标准 MPNN 的上界和实验结论都需条件化。",
        (AMBER, BLUE, RED),
    )
    heading(out, 42, "A", "颜色细化的一轮", AMBER)
    coords = {0: (95, 180), 1: (280, 180), 2: (95, 355), 3: (280, 355)}
    edges = ((0, 1), (1, 3), (3, 2), (2, 0))
    graph(out, coords, edges, {k: "c0" for k in coords}, color=BLUE)
    out += [text(195, 420, "c_i' = HASH(c_i, multiset{c_j})", 15, 700, "middle"),
            text(45, 468, "injective hash 才保留可区分信息。", 15, fill=MUTED)]

    heading(out, 430, "B", "局部视图相同仍可能全局不同", BLUE)
    # One 6-cycle and two disjoint triangles: all nodes degree two under uniform labels.
    pts = ((475, 170), (550, 120), (650, 120), (725, 170), (650, 220), (550, 220))
    for i, (x, y) in enumerate(pts):
        x2, y2 = pts[(i + 1) % 6]
        out += [line(x, y, x2, y2, GRID, 2), circle(x, y, 9, BLUE, BLUE, 1)]
    for cx, cy in ((520, 355), (680, 355)):
        tri = ((cx, cy - 45), (cx - 45, cy + 35), (cx + 45, cy + 35))
        for i, (x, y) in enumerate(tri):
            x2, y2 = tri[(i + 1) % 3]
            out += [line(x, y, x2, y2, GRID, 2), circle(x, y, 9, RED, RED, 1)]
    out += [text(600, 470, "uniform labels + degree 2: 1-WL cannot separate", 14, 700, "middle", RED)]

    heading(out, 830, "C", "结论的证据阶梯", RED)
    levels = ((105, "I", "equivariance / collision hand-check"), (185, "T", "WL bound under stated assumptions"),
              (265, "E", "dataset + split + seed results"), (345, "H", "mechanistic interpretation"),
              (425, "O", "unmeasured generalization"))
    for y, tag, lab in levels:
        out += [rect(845, y - 24, 42, 34, RED if tag in "EO" else TEAL, "#F8FAFC", 5, 2),
                text(866, y, tag, 15, 700, "middle", RED if tag in "EO" else TEAL), text(900, y, lab, 14, 650)]
    return finish(out, "表达上界、可构造反例和基准成绩是三种证据；任何一种都不能替代另外两种。")


FIGURES = {
    "fig-graph-relabeling-equivariance-v1.svg": relabeling_symmetry,
    "fig-mpnn-message-aggregate-update-v1.svg": mpnn_pipeline,
    "fig-spectral-spatial-gcn-bridge-v1.svg": spectral_spatial,
    "fig-multiset-aggregation-gin-v1.svg": multiset_gin,
    "fig-gnn-oversmoothing-oversquashing-v1.svg": depth_failures,
    "fig-graph-attention-neighborhood-v1.svg": graph_attention,
    "fig-graph-task-readout-heterogeneous-v1.svg": task_interface,
    "fig-wl-refinement-evidence-v1.svg": wl_evidence,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()

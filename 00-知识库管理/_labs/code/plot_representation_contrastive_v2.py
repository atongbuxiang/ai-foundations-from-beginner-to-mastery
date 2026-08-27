#!/usr/bin/env python3
"""Generate LT-53--56 paper-ink figures for representation and contrastive learning."""

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG, BLUE, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, text,
)

OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "learning-theory"


def representation_task_risk():
    out = begin(
        "表示学习：任务族、共享表示与下游风险",
        "表示不是脱离任务的压缩向量。训练分布、共享encoder、允许的head class、task family、label budget与部署损失共同定义表示质量；pretext loss只是一种构造信号。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "先写 Representation Contract", BLUE)
    node(out, 55, 105, 105, 58, "raw X", BLUE, size=16)
    out.append(line(165, 134, 225, 134, INK, 2.5, marker="a3"))
    node(out, 230, 95, 125, 78, "H = h(X)", TEAL, size=16)
    out += [line(292, 178, 205, 205, INK, 2), line(205, 205, 205, 422, INK, 2)]
    for y, lab in ((225, "head g_1"), (310, "head g_2"), (395, "head g_T")):
        out.append(line(205, y + 27, 225, y + 27, INK, 2, marker="a3"))
        node(out, 230, y, 125, 55, lab, RED, size=15)
    out += [text(45, 470, "task t: law P_t, loss ell_t, head class G", 15, 650)]
    out += [text(45, 510, "no universal representation without a task family。", 15, fill=MUTED)]

    heading(out, 430, "B", "下游误差要分账", TEAL)
    node(out, 445, 92, 310, 62, "oracle risk inside G o h", BLUE, size=15)
    out += [line(600, 159, 600, 192, INK, 2.5, marker="a3")]
    node(out, 445, 202, 310, 62, "representation approximation gap", TEAL, size=15)
    out += [line(600, 269, 600, 302, INK, 2.5, marker="a3")]
    node(out, 445, 312, 310, 62, "finite-label head estimation", RED, size=15)
    out += [line(600, 379, 600, 412, INK, 2.5, marker="a3")]
    node(out, 445, 422, 310, 58, "selection + deployment shift", BLUE, size=15)
    out += [text(430, 515, "pretext optimization is a separate error account。", 15, fill=MUTED)]

    heading(out, 830, "C", "保留与丢弃都依赖任务", RED)
    node(out, 845, 92, 285, 62, "invariance: discard nuisance", BLUE, size=15)
    node(out, 845, 180, 285, 62, "sufficiency: retain task signal", TEAL, size=15)
    node(out, 845, 268, 285, 62, "compression: limit head/sample cost", RED, size=15)
    out += [text(830, 382, "too invariant can erase labels", 15, 700, fill=RED)]
    out += [text(830, 420, "too rich can retain shortcut or identity", 15, 650)]
    out += [text(830, 458, "task diversity is not just task count", 15, 650)]
    out += [text(830, 495, "evaluate frozen, adapted, grouped and shifted", 15, 650)]
    out += [text(830, 515, "coordinate meaning is not representation identity。", 15, fill=MUTED)]
    return finish(out, "好表示不是形容词：它是相对于任务族、head限制、样本预算与部署损失的可比较风险声明。")


def metric_retrieval_risk():
    out = begin(
        "度量学习：几何监督、margin surrogate 与检索风险",
        "metric learning用pair、triplet或labels定义相似性，并学习distance或embedding。训练surrogate、mining distribution、query-gallery protocol与deployment threshold必须共同报告。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Mahalanobis 就是学习线性几何", BLUE)
    pts = ((80,160),(110,195),(145,170),(255,300),(295,330),(330,285))
    for i,(x,y) in enumerate(pts): out.append(circle(x,y,5,BLUE if i<3 else RED,BLUE if i<3 else RED))
    out += [text(45, 385, "d_M^2(x,x') = (x-x')^T M (x-x')", 15, 700, cls="math")]
    out += [text(45, 425, "M = L^T L  =>  Euclidean distance after L", 15, 650, cls="math")]
    out += [text(45, 468, "M positive semidefinite gives a pseudo-metric", 15, 650)]
    out += [text(45, 510, "side-information and scale define geometry。", 15, fill=MUTED)]

    heading(out, 430, "B", "Pair / Triplet 都是 Surrogate", TEAL)
    node(out, 445, 92, 310, 62, "positive pair: pull distance down", BLUE, size=15)
    out += [line(600, 159, 600, 192, INK, 2.5, marker="a3")]
    node(out, 445, 202, 310, 70, "triplet: d(a,p)+margin < d(a,n)", TEAL, size=15)
    out += [line(600, 277, 600, 310, INK, 2.5, marker="a3")]
    node(out, 445, 320, 310, 62, "mining chooses which violations matter", RED, size=15)
    out += [text(430, 430, "easy tuples: little gradient", 15, 700)]
    out += [text(430, 468, "hard tuples: information or label noise", 15, 650)]
    out += [text(430, 510, "zero surrogate loss != zero retrieval risk。", 15, fill=MUTED)]

    heading(out, 830, "C", "Query–Gallery 才定义检索", RED)
    node(out, 845, 92, 110, 62, "query q", BLUE, size=15)
    out.append(line(960, 123, 1015, 123, INK, 2.5, marker="a3"))
    node(out, 1020, 92, 110, 62, "ranked gallery", TEAL, size=14)
    out += [text(830, 220, "Recall@K: any / fraction relevant retrieved", 15, 700)]
    out += [text(830, 260, "AP / mAP: precision across relevant ranks", 15, 650)]
    out += [text(830, 300, "verification: threshold + FAR / FRR", 15, 650)]
    out += [text(830, 350, "identification != verification != clustering", 15, 700, fill=RED)]
    out += [text(830, 392, "split by identity, user, time and near-duplicate", 15, 650)]
    out += [text(830, 434, "gallery size changes operating difficulty", 15, 650)]
    out += [text(830, 476, "report group tails, calibration and latency", 15, 650)]
    out += [text(830, 510, "a pretty embedding plot is not a retrieval certificate。", 15, fill=MUTED)]
    return finish(out, "度量由监督与采样定义；检索质量由独立query–gallery、排序指标、阈值和部署分布验收。")


def infonce_density_ratio():
    out = begin(
        "InfoNCE：候选分类、密度比与互信息下界",
        "InfoNCE把一个positive与若干marginal negatives组成候选分类问题。最优score编码conditional-to-marginal density ratio；MI下界、finite-batch estimate与downstream utility是三个不同对象。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "先区分 NCE 与 InfoNCE", BLUE)
    node(out, 55, 92, 300, 64, "NCE: data vs known noise", BLUE, size=15)
    out += [text(85, 180, "unnormalized density estimation", 15, 650, fill=BLUE)]
    node(out, 55, 205, 300, 64, "InfoNCE: find the joint candidate", TEAL, size=15)
    out += [text(85, 293, "representation / ratio surrogate", 15, 650, fill=TEAL)]
    out += [text(45, 345, "similar name != same estimand", 16, 700, fill=RED)]
    out += [text(45, 395, "sampling law is part of either theorem", 15, 650)]
    out += [text(45, 445, "critic score is not itself a probability", 15, 650)]
    out += [text(45, 510, "define the candidate experiment before loss。", 15, fill=MUTED)]

    heading(out, 430, "B", "最优 Score 是 Density Ratio", TEAL)
    node(out, 445, 92, 310, 60, "one y+ from p(y|x)", BLUE, size=15)
    out += [line(600, 157, 600, 190, INK, 2.5, marker="a3")]
    node(out, 445, 200, 310, 62, "K-1 negatives from p(y)", TEAL, size=15)
    out += [line(600, 267, 600, 300, INK, 2.5, marker="a3")]
    node(out, 445, 310, 310, 62, "softmax candidate-index likelihood", RED, size=15)
    out += [text(430, 420, "s*(x,y) = log p(y|x) / p(y) + c(x)", 15, 700, cls="math")]
    out += [text(430, 468, "I(X;Y) >= log K - L_InfoNCE", 15, 700, fill=TEAL, cls="math")]
    out += [text(430, 510, "ratio identification needs the population experiment。", 15, fill=MUTED)]

    heading(out, 830, "C", "下界不等于测得 MI", RED)
    node(out, 845, 92, 285, 62, "ceiling: lower bound <= log K", BLUE, size=15)
    node(out, 845, 180, 285, 62, "critic / optimization / sampling gaps", TEAL, size=15)
    node(out, 845, 268, 285, 62, "finite-batch reuse and dependence", RED, size=15)
    out += [text(830, 382, "large true MI can saturate the bound", 15, 700, fill=RED)]
    out += [text(830, 420, "invertible codes can preserve MI but entangle", 15, 650)]
    out += [text(830, 458, "alignment + uniformity is another geometry view", 15, 650)]
    out += [text(830, 495, "downstream sufficiency still needs task evidence", 15, 650)]
    out += [text(830, 515, "a low loss is not a numerical MI certificate。", 15, fill=MUTED)]
    return finish(out, "InfoNCE首先是声明sampling law下的候选分类风险；密度比、MI下界和下游表示价值必须逐层说明。")


def batch_sampling_gradient():
    out = begin(
        "正负样本与 Batch：目标、梯度和碰撞",
        "in-batch contrastive learning中，batch不只是Monte Carlo容器：它定义候选集合、负样本分布、collision概率与梯度权重。temperature、hard mining、memory bank和distributed gather都会改变有效目标。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "一个 Batch 定义一场比赛", BLUE)
    node(out, 55, 92, 120, 58, "anchor z_i", BLUE, size=15)
    node(out, 235, 92, 120, 58, "positive z_j", TEAL, size=15)
    out += [line(180, 121, 230, 121, TEAL, 3, marker="a3")]
    for x,y in ((80,245),(165,285),(250,235),(320,320)): out.append(circle(x,y,9,RED,BG,3))
    out += [text(45, 375, "all other eligible views enter denominator", 15, 700)]
    out += [text(45, 420, "larger B changes K and collision exposure", 15, 650)]
    out += [text(45, 465, "group-aware eligibility changes the objective", 15, 650)]
    out += [text(45, 510, "batch size is not only estimator variance。", 15, fill=MUTED)]

    heading(out, 430, "B", "Softmax 权重就是梯度注意力", TEAL)
    node(out, 445, 92, 310, 62, "p_k = softmax(sim_k / temperature)", BLUE, size=15)
    out += [line(600, 159, 600, 192, INK, 2.5, marker="a3")]
    node(out, 445, 202, 310, 62, "grad score_k = p_k - 1{k=positive}", TEAL, size=15)
    out += [line(600, 269, 600, 302, INK, 2.5, marker="a3")]
    node(out, 445, 312, 310, 62, "small temperature emphasizes hard items", RED, size=15)
    out += [text(430, 420, "hard can mean useful, duplicate, or mislabeled", 15, 700, fill=RED)]
    out += [text(430, 462, "sum vs mean and all-gather change scaling", 15, 650)]
    out += [text(430, 510, "log the exact denominator and stop-gradient graph。", 15, fill=MUTED)]

    heading(out, 830, "C", "Negative 不是天然真负例", RED)
    node(out, 845, 92, 285, 62, "false negative: same semantics", RED, size=15)
    node(out, 845, 180, 285, 62, "dependent: same user / sequence", TEAL, size=15)
    node(out, 845, 268, 285, 62, "stale: old encoder / queue", BLUE, size=15)
    out += [text(830, 382, "debiasing requires class-prior assumptions", 15, 700, fill=RED)]
    out += [text(830, 420, "hard mining can amplify false negatives", 15, 650)]
    out += [text(830, 458, "distributed replicas change effective K", 15, 650)]
    out += [text(830, 495, "sample users and time before augmenting views", 15, 650)]
    out += [text(830, 515, "sampler code is part of the statistical method。", 15, fill=MUTED)]
    return finish(out, "对比学习的batch、sampler和通信图共同定义目标；梯度、false negatives与部署评价必须一并审计。")


FIGURES = {
    "fig-representation-task-risk-v2.svg": representation_task_risk,
    "fig-metric-retrieval-risk-v2.svg": metric_retrieval_risk,
    "fig-infonce-density-ratio-v2.svg": infonce_density_ratio,
    "fig-batch-negative-gradient-v2.svg": batch_sampling_gradient,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()

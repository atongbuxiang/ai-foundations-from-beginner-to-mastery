#!/usr/bin/env python3
"""Generate LT-57--60 paper-ink figures for self-supervision and transfer evaluation."""

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG, BLUE, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, text,
)

OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "learning-theory"


def augmentation_contract():
    out = begin(
        "数据增强：随机核、不变性、等变性与任务充分性",
        "augmentation定义条件随机核与two-view joint。先确定source unit和任务，再决定变化应被删除、在feature space中搬运，还是保留；错误不变性会不可逆地删除label information。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Source Unit 与 View Law", BLUE)
    node(out, 55, 92, 120, 58, "source U", BLUE, size=15)
    out.append(line(180, 121, 222, 121, INK, 2.5, marker="a3"))
    node(out, 228, 92, 125, 58, "clean X", TEAL, size=15)
    out += [line(290, 155, 155, 215, INK, 2), line(290, 155, 320, 215, INK, 2)]
    node(out, 75, 225, 135, 58, "view X^(1)", BLUE, size=15)
    node(out, 245, 225, 135, 58, "view X^(2)", BLUE, size=15)
    out += [text(45, 340, "A(dx' | x) defines the positive joint", 15, 700)]
    out += [text(45, 382, "views share one source; they are not iid units", 15, 650)]
    out += [text(45, 424, "order, probability and shared RNG matter", 15, 650)]
    out += [text(45, 468, "split source identities before generating views", 15, 650)]
    out += [text(45, 510, "a transform list is not a sampling contract。", 15, fill=MUTED)]

    heading(out, 430, "B", "删除变化，还是搬运变化", TEAL)
    node(out, 445, 92, 310, 62, "invariant: h(gx) = h(x)", BLUE, size=15)
    out += [line(600, 159, 600, 192, INK, 2.5, marker="a3")]
    node(out, 445, 202, 310, 62, "equivariant: h(gx) = rho(g) h(x)", TEAL, size=15)
    out += [line(600, 269, 600, 302, INK, 2.5, marker="a3")]
    node(out, 445, 312, 310, 62, "invariant readout after equivariant features", RED, size=15)
    out += [text(430, 420, "classification may discard pose", 15, 700)]
    out += [text(430, 460, "control and localization often need pose", 15, 650)]
    out += [text(430, 510, "hard-wiring != random augmentation。", 15, fill=MUTED)]

    heading(out, 830, "C", "Task Validity 是最终闸门", RED)
    node(out, 845, 92, 285, 62, "preserve P(Y | X): valid nuisance", TEAL, size=15)
    node(out, 845, 180, 285, 62, "change P(Y | X): erase task signal", RED, size=15)
    node(out, 845, 268, 285, 62, "unknown task family: audit conflict", BLUE, size=15)
    out += [text(830, 382, "too weak: shortcut remains", 15, 700)]
    out += [text(830, 420, "too strong: conditional entropy rises", 15, 700, fill=RED)]
    out += [text(830, 458, "report strength curves and alternative tasks", 15, 650)]
    out += [text(830, 495, "cluster uncertainty by source unit", 15, 650)]
    out += [text(830, 515, "agreement != sufficiency。", 15, fill=MUTED)]
    return finish(out, "增强先定义joint law，再声明symmetry；只有保留任务条件分布的变化才能安全地被商掉。")


def collapse_certificates():
    out = begin(
        "表示坍缩：层级诊断、非坍缩机制与证据边界",
        "complete collapse只是最弱失败。还要检查dimensional和spectral collapse、nuisance-only spread与coordinate non-identifiability；每种防坍缩机制只控制特定统计量或训练动力学。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Collapse 不止一个层级", BLUE)
    node(out, 55, 92, 300, 58, "complete: all z = constant", RED, size=15)
    node(out, 55, 178, 300, 58, "dimensional: rank r << d", RED, size=15)
    node(out, 55, 264, 300, 58, "spectral: few eigenvalues dominate", BLUE, size=15)
    node(out, 55, 350, 300, 58, "semantic: variance stores nuisance", TEAL, size=15)
    out += [text(45, 452, "diagnose std + spectrum + geometry + task", 15, 700)]
    out += [text(45, 492, "sample covariance rank <= B - 1", 15, 650)]
    out += [text(45, 515, "high rank is not a semantic certificate。", 15, fill=MUTED)]

    heading(out, 430, "B", "四条机制控制不同对象", TEAL)
    node(out, 445, 92, 310, 58, "negatives: constant loses candidate game", BLUE, size=15)
    node(out, 445, 176, 310, 58, "variance floor: each dim must spread", TEAL, size=15)
    node(out, 445, 260, 310, 58, "correlation/covariance: reduce redundancy", TEAL, size=15)
    node(out, 445, 344, 310, 58, "stop-grad + EMA: change vector field", RED, size=15)
    out += [text(430, 452, "normalization, predictor and batch law remain", 15, 700)]
    out += [text(430, 492, "ablation evidence is not a universal theorem", 15, 650)]
    out += [text(430, 515, "forward loss and backward dynamics differ。", 15, fill=MUTED)]

    heading(out, 830, "C", "Non-Collapse 后仍有三道门", RED)
    node(out, 845, 92, 285, 62, "1  equivalence / identifiability", BLUE, size=15)
    out += [line(987, 159, 987, 190, INK, 2.5, marker="a3")]
    node(out, 845, 200, 285, 62, "2  task sufficiency", TEAL, size=15)
    out += [line(987, 267, 987, 298, INK, 2.5, marker="a3")]
    node(out, 845, 308, 285, 62, "3  finite-label transfer risk", RED, size=15)
    out += [text(830, 420, "orthogonal coordinates may be equivalent", 15, 650)]
    out += [text(830, 458, "nuisance can create full covariance rank", 15, 650)]
    out += [text(830, 495, "evaluate layer, worker, dtype and shift", 15, 650)]
    out += [text(830, 515, "healthy geometry is necessary, not sufficient。", 15, fill=MUTED)]
    return finish(out, "先排除常数与低秩失败，再检查任务信息和迁移；任何单一协方差或loss曲线都不能完成整条证据链。")


def masked_teacher_targets():
    out = begin(
        "自监督目标：遮蔽预测、Teacher–Student 与 Target 生成",
        "自监督仍有target。target可来自clean input的被遮蔽部分、tokenizer/quantizer、另一模态或历史模型；corruption、visibility、stop-gradient和target update共同定义统计对象。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "先追溯 Target 来源", BLUE)
    node(out, 55, 92, 120, 58, "clean X", BLUE, size=15)
    out.append(line(180, 121, 222, 121, INK, 2.5, marker="a3"))
    node(out, 228, 92, 125, 58, "mask M", TEAL, size=15)
    out += [line(290, 155, 155, 215, INK, 2), line(290, 155, 320, 215, INK, 2)]
    node(out, 55, 225, 150, 58, "visible input", BLUE, size=15)
    node(out, 240, 225, 140, 58, "target T", RED, size=15)
    out += [text(45, 340, "log loss -> conditional target distribution", 15, 700)]
    out += [text(45, 382, "square loss -> conditional target mean", 15, 700)]
    out += [text(45, 424, "mask law changes entropy and shortcut", 15, 650)]
    out += [text(45, 468, "loss positions and denominator matter", 15, 650)]
    out += [text(45, 510, "low pretext loss is not downstream proof。", 15, fill=MUTED)]

    heading(out, 430, "B", "四类 Target Geometry", TEAL)
    node(out, 445, 92, 145, 58, "token CE", BLUE, size=15)
    node(out, 610, 92, 145, 58, "pixel MSE", BLUE, size=15)
    node(out, 445, 190, 145, 58, "latent match", TEAL, size=15)
    node(out, 610, 190, 145, 58, "teacher dist.", RED, size=15)
    out += [text(430, 300, "decoder capacity can absorb the task", 15, 700)]
    out += [text(430, 342, "quantizer or teacher passes on its bias", 15, 650)]
    out += [text(430, 384, "target granularity defines invariance", 15, 650)]
    out += [text(430, 426, "other modality can signal or shortcut", 15, 650)]
    out += [text(430, 468, "pretrain and deployment visibility differ", 15, 650)]
    out += [text(430, 510, "target type is an inductive-bias decision。", 15, fill=MUTED)]

    heading(out, 830, "C", "Teacher 不是 Ground Truth", RED)
    node(out, 845, 92, 285, 58, "student: gradient update", BLUE, size=15)
    out += [line(987, 155, 987, 186, INK, 2.5, marker="a3")]
    node(out, 845, 196, 285, 58, "teacher: EMA of student history", TEAL, size=15)
    out += [line(987, 259, 987, 290, INK, 2.5, marker="a3")]
    node(out, 845, 300, 285, 58, "stop-grad target + consistency", RED, size=15)
    out += [text(830, 400, "temperature controls target entropy", 15, 700)]
    out += [text(830, 438, "centering controls prototype dominance", 15, 650)]
    out += [text(830, 476, "audit leakage and confirmation error", 15, 650)]
    out += [text(830, 515, "EMA smooths noise but also creates lag。", 15, fill=MUTED)]
    return finish(out, "自监督的第一问不是模型结构，而是target从哪里来、谁能看见什么，以及哪些梯度被允许穿过target路径。")


def transfer_matrix():
    out = begin(
        "表示迁移评估：Probe、Fine-Tuning 与多轴证据矩阵",
        "linear probe测固定表示上的线性可访问性；fine-tuning测初始化与适配算法。task、head、label budget、compute、shift、seed和selection都必须进入评估矩阵。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "三个不同 Estimand", BLUE)
    node(out, 55, 92, 300, 62, "oracle linear risk", BLUE, size=15)
    out += [line(205, 159, 205, 190, INK, 2.5, marker="a3")]
    node(out, 55, 200, 300, 62, "finite-label trained probe", TEAL, size=15)
    out += [line(205, 267, 205, 298, INK, 2.5, marker="a3")]
    node(out, 55, 308, 300, 62, "fine-tune initialization + algorithm", RED, size=15)
    out += [text(45, 420, "scratch is the architecture/data baseline", 15, 700)]
    out += [text(45, 458, "XOR: information can be nonlinear to read", 15, 650)]
    out += [text(45, 495, "probe score depends on head training", 15, 650)]
    out += [text(45, 515, "one score cannot identify representation quality。", 15, fill=MUTED)]

    heading(out, 430, "B", "沿资源轴画完整曲线", TEAL)
    out += [text(430, 105, "label budget", 15, 700, fill=BLUE)]
    for i, x in enumerate((455, 515, 585, 665, 735)):
        out.append(circle(x, 145, 6 + i, BLUE, BG, 2))
    out += [line(455, 145, 735, 145, BLUE, 2)]
    out += [text(430, 220, "head capacity", 15, 700, fill=TEAL)]
    for i, lab in enumerate(("kNN", "linear", "MLP", "partial", "full")):
        out += [text(440 + i * 64, 260, lab, 15, 650)]
    out += [text(430, 335, "compute / steps", 15, 700, fill=RED)]
    out += [line(455, 375, 735, 375, RED, 3, marker="a3")]
    out += [text(430, 420, "early gain may be optimization speedup", 15, 650)]
    out += [text(430, 458, "large-budget gap tests persistent transfer", 15, 650)]
    out += [text(430, 495, "freeze layer and feature normalization", 15, 650)]
    out += [text(430, 515, "report curves, not one checkpoint。", 15, fill=MUTED)]

    heading(out, 830, "C", "最终 Claim 来自 Transfer Matrix", RED)
    node(out, 845, 92, 130, 54, "tasks", BLUE, size=15)
    node(out, 995, 92, 135, 54, "protocols", TEAL, size=15)
    node(out, 845, 170, 130, 54, "shifts", RED, size=15)
    node(out, 995, 170, 135, 54, "seeds", BLUE, size=15)
    node(out, 845, 248, 130, 54, "compute", TEAL, size=15)
    node(out, 995, 248, 135, 54, "selection", RED, size=15)
    out += [text(830, 350, "nested validation protects the locked test", 15, 700)]
    out += [text(830, 390, "paired uncertainty uses the same splits", 15, 650)]
    out += [text(830, 430, "report average, worst task and negative transfer", 15, 650)]
    out += [text(830, 470, "align FLOPs, search and early stopping", 15, 650)]
    out += [text(830, 515, "single-task top-1 is not universal transfer。", 15, fill=MUTED)]
    return finish(out, "先声明probe或fine-tune测量什么，再锁定资源和selection；只有多任务、多预算和shift矩阵才能支持通用迁移声明。")


FIGURES = {
    "fig-augmentation-invariance-equivariance-v2.svg": augmentation_contract,
    "fig-representation-collapse-certificates-v2.svg": collapse_certificates,
    "fig-masked-teacher-targets-v2.svg": masked_teacher_targets,
    "fig-transfer-evaluation-matrix-v2.svg": transfer_matrix,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()

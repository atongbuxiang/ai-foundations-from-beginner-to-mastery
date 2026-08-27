#!/usr/bin/env python3
"""Generate the eight original ARCH-57--64 MoE textbook figures."""

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    AMBER, BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "architecture"


def capacity_active_compute():
    out = begin(
        "MoE 的三本账：总容量、每 Token 激活与实际计算",
        "专家参数可以随 E 增长，而理想逐 token 专家计算只随 k 增长；路由、通信、容量与权重驻留另行记账。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Dense 与 Sparse FFN", BLUE)
    node(out, 55, 102, 110, 48, "token x", BLUE, "#EFF6FF", 15)
    node(out, 220, 90, 120, 72, "Dense FFN", RED, "#FEF2F2", 15)
    out += [line(168, 126, 215, 126, INK, 2.2, marker="a3"),
            text(55, 205, "P_dense ≈ 2 d m", 16, 700),
            text(55, 244, "C_token ≈ 2 d m", 16, 700)]
    node(out, 55, 312, 110, 48, "token x", BLUE, "#EFF6FF", 15)
    for i, c in enumerate((TEAL, GRID, TEAL, GRID)):
        out += [rect(215 + (i % 2) * 65, 284 + (i // 2) * 68, 50, 46, c, "#ECFDF5" if c == TEAL else "#F8FAFC", 6, 2)]
        out += [text(240 + (i % 2) * 65, 314 + (i // 2) * 68, f"e{i+1}", 15, 700, "middle", c)]
    out += [line(168, 336, 207, 312, TEAL, 2, marker="a1"), line(168, 336, 272, 380, TEAL, 2, marker="a1"),
            text(55, 430, "P_expert ≈ E·2 d m_e", 15, 700),
            text(55, 466, "ideal C_token ≈ k·2 d m_e", 15, 700, fill=TEAL)]

    heading(out, 430, "B", "一个可复算的例子", TEAL)
    out += [text(455, 112, "E=8, k=2, m_e=m/2", 17, 700),
            text(455, 165, "expert parameters", 15, fill=MUTED),
            text(700, 165, "4× dense", 17, 800, "end", BLUE),
            text(455, 225, "active FFN MACs/token", 15, fill=MUTED),
            text(700, 225, "≈ dense", 17, 800, "end", TEAL)]
    out += [rect(455, 267, 240, 24, BLUE, "#EFF6FF", 4, 1.5),
            rect(455, 327, 60, 24, TEAL, "#ECFDF5", 4, 1.5),
            text(455, 395, "4× capacity 不能推出 4× quality；", 15, 700),
            text(455, 430, "≈ compute 也未计 router/comm。", 15, 700, fill=RED)]

    heading(out, 830, "C", "系统账不得折叠", RED)
    ledgers = ((104, "parameters", "total / active", BLUE),
               (174, "arithmetic", "expert + router", TEAL),
               (244, "memory", "weights + activations", AMBER),
               (314, "network", "dispatch + combine", RED),
               (384, "capacity", "padding / dropping", BLUE),
               (454, "latency", "tail + overlap", RED))
    for y, a, b, c in ledgers:
        node(out, 845, y, 115, 40, a, c, "#F8FAFC", 15)
        out += [text(980, y + 26, b, 15, 650)]
    return finish(out, "MoE 的结构承诺是 total capacity 随 E 扩展、active expert work 随 k 扩展；端到端收益仍需系统账验证。")


def router_gate_topk():
    out = begin(
        "Router、Gate 与 Top-k：四个接口必须分开写",
        "logit 产生、score activation、离散选择、选中权重归一化与反向估计不是同一个操作。",
        (AMBER, BLUE, TEAL),
    )
    heading(out, 42, "A", "Forward Routing Contract", AMBER)
    stages = ((55, 102, 76, "x"), (155, 102, 100, "z=xWᵣ"), (278, 102, 82, "a=g(z)"))
    for i, (x, y, w, label) in enumerate(stages):
        node(out, x, y, w, 50, label, (BLUE, AMBER, TEAL)[i], "#F8FAFC", 15)
        if i:
            out += [line(stages[i-1][0] + stages[i-1][2] + 3, 127, x - 5, 127, INK, 2, marker="a3")]
    node(out, 80, 220, 120, 52, "I=TopK(a)", RED, "#FEF2F2", 15)
    node(out, 230, 220, 130, 52, "w=Norm(a_I)", TEAL, "#ECFDF5", 15)
    out += [line(320, 155, 140, 212, INK, 2, marker="a3"), line(200, 246, 225, 246, INK, 2, marker="a3"),
            text(55, 330, "y = Σ_{i∈I} w_i f_i(x)", 17, 700),
            text(55, 386, "ranking 可相同，mixing weights 可不同。", 15, fill=MUTED),
            text(55, 440, "必须声明 tie-break 与 backward。", 15, 700, fill=RED)]

    heading(out, 430, "B", "同一 Logit 的三种 Score", BLUE)
    out += [text(455, 105, "z = [2, 1, −1]", 17, 700)]
    rows = ((155, "softmax", "[.71, .26, .04]", BLUE),
            (235, "sigmoid", "[.88, .73, .27]", TEAL),
            (315, "ReLU", "[2, 1, 0]", AMBER))
    for y, name, vals, color in rows:
        node(out, 455, y, 105, 42, name, color, "#F8FAFC", 15)
        out += [text(580, y + 27, vals, 15, 650)]
    out += [text(455, 402, "Top-2 index 都是 {1,2}，", 15, 700),
            text(455, 438, "重归一后的组合系数仍不同。", 15, 700, fill=RED)]

    heading(out, 830, "C", "梯度流向审计", TEAL)
    node(out, 845, 102, 275, 48, "expert loss L_task", BLUE, "#EFF6FF", 15)
    branches = ((215, "selected weights", TEAL), (305, "Top-k boundary", RED), (395, "balance signal", AMBER))
    for y, label, color in branches:
        out += [line(982, 153, 982, y - 8, color, 1.8, "5 4", "a3")]
        node(out, 845, y, 275, 46, label, color, "#F8FAFC", 15)
    out += [text(845, 472, "hard selection 几乎处处不传普通导数。", 15, 700, fill=RED)]
    return finish(out, "路由公式完整的最低要求：logits、score、selection、mixing、capacity、tie-break 与 backward estimator 全部显式。")


def capacity_dispatch():
    out = begin(
        "Expert Capacity 与 Dispatch：拥塞发生在哪里",
        "token-choice 路由先产生每个专家的到达流；capacity 决定 padding、dropping 或 dropless block 调度。",
        (RED, AMBER, TEAL),
    )
    heading(out, 42, "A", "Token-choice 产生队列", RED)
    targets = (0, 0, 0, 1, 1, 2, 0, 2)
    for i, e in enumerate(targets):
        x, y = 58 + (i % 4) * 70, 105 + (i // 4) * 74
        out += [circle(x, y, 18, BLUE, "#EFF6FF", 2), text(x, y + 5, f"t{i+1}", 15, 700, "middle")]
        ex, ey = 98 + e * 95, 345
        out += [line(x, y + 20, ex, ey - 32, (RED, AMBER, TEAL)[e], 1.4, "5 3")]
    for e, c in enumerate((RED, AMBER, TEAL)):
        node(out, 55 + e * 95, 340, 85, 48, f"expert {e+1}", c, "#F8FAFC", 15)
    out += [text(55, 445, "loads = [4,2,2]；拥塞由 batch 路由共同决定。", 15, 700)]

    heading(out, 430, "B", "Capacity C=3 的三种语义", AMBER)
    policies = ((108, "drop", "第 4 个 token 走残差/丢失", RED),
                (218, "pad", "每个 expert 固定 3 槽", AMBER),
                (328, "dropless", "变长块全部执行", TEAL))
    for y, name, detail, color in policies:
        node(out, 455, y, 90, 48, name, color, "#F8FAFC", 15)
        out += [text(565, y + 22, detail, 15, 650),
                text(565, y + 48, "function/cost 改变" if name == "drop" else "layout/cost 改变", 15, fill=MUTED)]
    out += [text(455, 450, "capacity factor α 常令 C=ceil(αTk/E)。", 15, 700, fill=BLUE)]

    heading(out, 830, "C", "Expert-choice 是另一合同", TEAL)
    for j in range(3):
        node(out, 845, 103 + j * 103, 100, 45, f"expert {j+1}", (RED, AMBER, TEAL)[j], "#F8FAFC", 15)
        for i in range(3):
            out += [circle(990 + i * 42, 126 + j * 103, 13, BLUE, "#EFF6FF", 1.5)]
    out += [text(845, 425, "每个 expert 选固定 bucket；", 15, 700),
            text(845, 459, "每 token 的专家数可为 0、1 或多。", 15, 700, fill=RED)]
    return finish(out, "capacity 不只是内存参数：一旦 drop、duplicate 或改变专家选择，它就进入模型函数本身。")


def aux_loss():
    out = begin(
        "负载均衡辅助损失：离散使用率与连续概率如何耦合",
        "典型 proxy 将专家被选频率 f_i 与平均路由概率 p_i 相乘；它鼓励均衡但同时改写主任务目标。",
        (TEAL, RED, BLUE),
    )
    heading(out, 42, "A", "两种统计量", TEAL)
    out += [text(55, 108, "fᵢ = selected tokens / T", 16, 700),
            text(55, 153, "pᵢ = mean soft score", 16, 700)]
    bars = ((220, (0.55, 0.25, 0.12, 0.08), RED), (345, (0.42, 0.29, 0.18, 0.11), BLUE))
    for y, vals, color in bars:
        for i, v in enumerate(vals):
            out += [rect(60 + i * 68, y + 75 - v * 120, 42, v * 120, color, "#F8FAFC", 3, 2)]
        out += [text(55, y + 105, "hard f" if y == 220 else "soft p", 15, 700, fill=color)]
    out += [text(55, 476, "L_aux = λE Σᵢ fᵢpᵢ", 17, 800, fill=TEAL)]

    heading(out, 430, "B", "梯度从哪里来", RED)
    node(out, 455, 102, 285, 54, "L = L_task + L_aux", RED, "#FEF2F2", 16)
    node(out, 455, 220, 125, 58, "hard fᵢ", AMBER, "#FFF7ED", 15)
    node(out, 615, 220, 125, 58, "soft pᵢ", TEAL, "#ECFDF5", 15)
    out += [line(598, 160, 518, 212, INK, 2, marker="a3"), line(598, 160, 678, 212, INK, 2, marker="a3"),
            text(455, 337, "f 常 stop-grad / proxy；", 15, 700, fill=AMBER),
            text(455, 375, "p 提供连续梯度。", 15, 700, fill=TEAL),
            text(455, 430, "λ 控制系统均衡与任务适配的张力。", 15, 700, fill=RED)]

    heading(out, 830, "C", "均衡粒度改变问题", BLUE)
    levels = ((105, "token", "局部快速"), (195, "microbatch", "统计噪声"),
              (285, "sequence", "可能过度约束"), (375, "global", "通信/延迟"))
    for y, level, caveat in levels:
        node(out, 845, y, 110, 45, level, BLUE, "#EFF6FF", 15)
        out += [text(975, y + 27, caveat, 15, 650)]
    out += [text(845, 460, "均匀负载是资源目标，不是任务定理。", 15, 700, fill=RED)]
    return finish(out, "辅助损失是可优化的均衡代理；统计尺度、停止梯度和 λ 都属于模型定义与实验协议。")


def lossfree_assignment():
    out = begin(
        "Loss-Free 路由：反馈控制与平衡分配的两种视角",
        "bias 不进入专家组合权重也可改变 Top-k 选择；全局配额则可写成带容量约束的 assignment。",
        (BLUE, AMBER, RED),
    )
    heading(out, 42, "A", "Bias Feedback Loop", BLUE)
    node(out, 55, 100, 285, 50, "route by sᵢ + bᵢ", BLUE, "#EFF6FF", 15)
    node(out, 55, 210, 285, 54, "observe load nᵢ − target", RED, "#FEF2F2", 15)
    node(out, 55, 330, 285, 62, "bᵢ ← bᵢ − η·sign(error)", AMBER, "#FFF7ED", 15)
    out += [line(198, 154, 198, 202, INK, 2, marker="a3"), line(198, 268, 198, 322, INK, 2, marker="a3"),
            line(52, 360, 25, 360, BLUE, 2), line(25, 360, 25, 126, BLUE, 2), line(25, 126, 48, 126, BLUE, 2, marker="a0"),
            text(55, 445, "无显式 L_aux ≠ 无训练干预。", 15, 800, fill=RED)]

    heading(out, 430, "B", "Capacity-constrained Assignment", AMBER)
    out += [text(455, 104, "max  Σᵢⱼ aᵢⱼ sᵢⱼ", 17, 700),
            text(455, 148, "s.t. Σⱼaᵢⱼ=k,  Σᵢaᵢⱼ≤Cⱼ", 15, 700)]
    matrix = ((9, 7, 2), (8, 6, 5), (4, 9, 7), (3, 8, 9))
    picks = {(0, 0), (1, 0), (2, 1), (3, 2)}
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            c = TEAL if (i, j) in picks else GRID
            out += [rect(475 + j * 70, 205 + i * 57, 52, 40, c, "#ECFDF5" if c == TEAL else "#F8FAFC", 4, 2),
                    text(501 + j * 70, 231 + i * 57, val, 15, 700, "middle")]
    out += [text(455, 460, "dual price / quantile 可解释专家 bias。", 15, 700, fill=AMBER)]

    heading(out, 830, "C", "三条不可混写的主张", RED)
    claims = ((108, "I", "bias 改变 arg-top-k", BLUE),
              (210, "T", "assignment dual / quota", AMBER),
              (312, "E", "训练质量与吞吐", TEAL),
              (414, "O", "漂移下稳定性", RED))
    for y, tag, label, color in claims:
        out += [circle(865, y, 20, color, "#F8FAFC", 2), text(865, y + 6, tag, 16, 800, "middle", color),
                text(900, y + 6, label, 15, 650)]
    return finish(out, "loss-free 的精确含义是移除显式辅助目标；bias 状态、更新率、延迟和分布式统计仍须进入审计。")


def shared_fine_dynamic():
    out = begin(
        "共享专家、细粒度专家与动态激活：三条独立设计轴",
        "共享路径承载所有 token，细粒度改变参数分块，动态激活改变每 token 选择基数；三者不能用同一消融识别。",
        (TEAL, BLUE, AMBER),
    )
    heading(out, 42, "A", "Shared + Routed Residual", TEAL)
    node(out, 55, 104, 95, 46, "x", BLUE, "#EFF6FF", 15)
    node(out, 205, 90, 130, 52, "shared FFN", TEAL, "#ECFDF5", 15)
    node(out, 205, 205, 130, 52, "routed experts", AMBER, "#FFF7ED", 15)
    node(out, 95, 350, 205, 58, "y = x + f_s(x)+Σwᵢfᵢ(x)", BLUE, "#EFF6FF", 15)
    out += [line(153, 126, 198, 116, TEAL, 2, marker="a0"), line(153, 126, 198, 230, AMBER, 2, marker="a1"),
            line(270, 145, 220, 342, INK, 2, marker="a3"), line(270, 260, 220, 342, INK, 2, marker="a3"),
            text(55, 460, "shared=公共知识 是解释假说 H。", 15, 700, fill=RED)]

    heading(out, 430, "B", "Fine-grained Expert Tiling", BLUE)
    out += [text(455, 105, "coarse: 4 experts × width m", 15, 700)]
    for i in range(4):
        out += [rect(455 + i * 70, 135, 55, 65, BLUE, "#EFF6FF", 5, 2)]
    out += [text(455, 250, "fine: 16 experts × width m/4", 15, 700)]
    for i in range(16):
        out += [rect(455 + (i % 8) * 35, 280 + (i // 8) * 55, 26, 38, TEAL if i in (0, 3, 9, 14) else GRID, "#F8FAFC", 3, 1.5)]
    out += [text(455, 402, "总参数可保持近似不变；", 15, 700),
            text(455, 437, "组合数、kernel 粒度与通信改变。", 15, 700, fill=RED)]

    heading(out, 830, "C", "Dynamic k = Threshold", AMBER)
    scores = (0.91, 0.72, 0.48, 0.31, 0.12)
    for i, v in enumerate(scores):
        y = 105 + i * 70
        out += [rect(845, y, 220 * v, 25, TEAL if v > 0.4 else GRID, "#ECFDF5" if v > 0.4 else "#F8FAFC", 3, 1.5),
                text(1080, y + 20, f"{v:.2f}", 15, 650, "end")]
    out += [line(945, 90, 945, 455, RED, 2, "6 4"), text(952, 468, "threshold β", 15, 700, fill=RED),
            text(845, 500, "token 的 active count 可变；expert quota 另约束。", 15, 700)]
    return finish(out, "共享、粒度、动态 k 分别改变基线容量、组合空间与计算分配；公平实验需逐轴控制参数和激活 MAC。")


def expert_parallel():
    out = begin(
        "Expert Parallel 与 All-to-All：Payload 之外还有尾延迟",
        "token hidden states 先按 expert owner 重排发送，再本地执行专家并回传；网络量、拓扑、偏斜与同步尾部共同决定延迟。",
        (RED, BLUE, TEAL),
    )
    heading(out, 42, "A", "Dispatch → Expert → Combine", RED)
    for d, color in enumerate((BLUE, TEAL, AMBER)):
        node(out, 55, 95 + d * 120, 100, 48, f"device {d}", color, "#F8FAFC", 15)
        node(out, 270, 95 + d * 120, 90, 48, f"expert {d}", color, "#F8FAFC", 15)
    routes = ((0, 1, TEAL), (0, 2, AMBER), (1, 0, BLUE), (2, 1, TEAL))
    for src, dst, color in routes:
        out += [line(158, 119 + src * 120, 265, 119 + dst * 120, color, 1.8, "5 3", "a3")]
    out += [text(55, 470, "再做逆置 All-to-All，将输出送回 token owner。", 15, 700, fill=RED)]

    heading(out, 430, "B", "通信量的最低账本", BLUE)
    node(out, 455, 102, 285, 58, "payload ≈ assignments × d × bytes", BLUE, "#EFF6FF", 15)
    rows = ((215, "assignments", "T·k (before drops)"),
            (285, "direction", "dispatch + combine"),
            (355, "metadata", "indices / scales / padding"),
            (425, "local share", "does not cross network"))
    for y, a, b in rows:
        out += [text(455, y, a, 15, 800, fill=TEAL), text(585, y, b, 15, 650)]

    heading(out, 830, "C", "Volume ≠ Latency", TEAL)
    factors = ((100, "topology", "intra/inter-node"), (175, "skew", "max load, not mean"),
               (250, "buckets", "many small messages"), (325, "overlap", "compute ↔ network"),
               (400, "straggler", "global tail sync"), (475, "kernel", "padding / block size"))
    for y, a, b in factors:
        node(out, 845, y, 105, 38, a, (BLUE, RED, AMBER, TEAL, RED, BLUE)[(y-100)//75], "#F8FAFC", 15)
        out += [text(970, y + 25, b, 15, 650)]
    return finish(out, "All-to-All 字节数是恒等账本；端到端延迟必须在指定并行布局、负载分布、网络与重叠策略下测量。")


def gating_evidence():
    out = begin(
        "门控归一化与 MoE 证据地图：从 Simplex 到开放问题",
        "Softmax 施加总和为一的竞争；Sigmoid 独立打分；Top-k 后是否重归一决定组合权重和可训练边界。",
        (BLUE, RED, AMBER),
    )
    heading(out, 42, "A", "Score Geometry", BLUE)
    out += [line(75, 355, 325, 355, INK, 2), line(75, 355, 75, 105, INK, 2), line(75, 355, 300, 130, BLUE, 3),
            text(170, 210, "softmax: Σaᵢ=1", 15, 700, "middle", BLUE)]
    for x, y in ((120, 310), (185, 245), (250, 180)):
        out += [circle(x, y, 8, BLUE, "#EFF6FF", 2)]
    for x, y in ((125, 165), (220, 310), (295, 230)):
        out += [circle(x, y, 8, TEAL, "#ECFDF5", 2)]
    out += [text(82, 395, "sigmoid: each aᵢ∈(0,1)", 15, 700, fill=TEAL),
            text(55, 456, "ranking invariance 不等于 mixing invariance。", 15, 700, fill=RED)]

    heading(out, 430, "B", "Top-1 Re-Norm 边界", RED)
    node(out, 455, 102, 285, 58, "I={argmax aᵢ}", BLUE, "#EFF6FF", 16)
    node(out, 455, 220, 285, 68, "wᵢ = aᵢ / Σ_{j∈I}aⱼ = 1", RED, "#FEF2F2", 15)
    node(out, 455, 355, 285, 62, "ordinary ∂w/∂a = 0", AMBER, "#FFF7ED", 16)
    out += [line(598, 164, 598, 212, INK, 2, marker="a3"), line(598, 292, 598, 347, INK, 2, marker="a3"),
            text(455, 466, "router 仍可由 aux/STE/bias 等路径更新。", 15, 700)]

    heading(out, 830, "C", "Evidence Ladder", AMBER)
    ladder = ((445, "O", "cross-scale optimum", RED),
              (370, "H", "specialization story", AMBER),
              (295, "E", "ablation / system", TEAL),
              (220, "T", "bounded theorem", BLUE),
              (145, "I", "shape / accounting", BLUE))
    for y, tag, label, color in ladder:
        out += [rect(845, y, 55 + (445-y)//2, 44, color, "#F8FAFC", 5, 2),
                text(867, y + 28, tag, 16, 800, "middle", color),
                text(930, y + 28, label, 15, 650)]
    out += [text(845, 500, "强结论必须向下找到足够证据。", 15, 700, fill=RED)]
    return finish(out, "门控选择没有脱离协议的赢家；先固定 forward/backward/capacity，再按 I/T/E/H/O 限定结论强度。")


FIGURES = {
    "fig-moe-capacity-active-compute-v1.svg": capacity_active_compute,
    "fig-moe-router-gate-topk-contract-v1.svg": router_gate_topk,
    "fig-moe-capacity-dispatch-dropless-v1.svg": capacity_dispatch,
    "fig-moe-aux-loss-load-gradient-v1.svg": aux_loss,
    "fig-moe-lossfree-assignment-feedback-v1.svg": lossfree_assignment,
    "fig-moe-shared-finegrained-dynamic-v1.svg": shared_fine_dynamic,
    "fig-moe-expert-parallel-alltoall-v1.svg": expert_parallel,
    "fig-moe-gating-normalization-evidence-v1.svg": gating_evidence,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, build in FIGURES.items():
        (OUT / filename).write_text(build(), encoding="utf-8")
        print(OUT / filename)


if __name__ == "__main__":
    main()

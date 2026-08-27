#!/usr/bin/env python3
"""Generate ARCH-09--16 figures for recurrent and state-space models.

Each plate uses a different explanatory grammar while sharing the course's
paper-and-ink palette. The drawings are original, deterministic SVG assets.
"""

from __future__ import annotations

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "architecture"


def state_contract():
    out = begin(
        "因果序列模型：历史、状态与读出合同",
        "状态 h_t 是历史的有限维摘要；同一递推同时定义信息可见性、流式接口与不可逆压缩。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "按时间展开：只能从过去流向未来", BLUE)
    for i in range(4):
        x = 60 + 88 * i
        out += [circle(x, 150, 14, BLUE, "#EFF6FF", 2), text(x, 156, f"x{i+1}", 13, 700, "middle", BLUE)]
        out += [rect(x - 27, 235, 54, 48, TEAL, "#ECFDF5", 5, 2), text(x, 265, f"h{i+1}", 14, 700, "middle", TEAL)]
        out += [line(x, 166, x, 230, BLUE, 2.2, marker="a1")]
        if i:
            out += [line(x - 60, 259, x - 31, 259, TEAL, 2.8, marker="a1")]
    out += [text(45, 340, "h_t = F(h_(t-1), x_t)", 18, 700, cls="math", fill=TEAL)]
    out += [text(45, 385, "y_t = G(h_t)", 18, 700, cls="math", fill=BLUE)]
    out += [text(45, 452, "因果：y_t 不应依赖 x_(t+1)。", 15, 700, fill=RED)]
    out += [text(45, 485, "共享 θ 让同一 cell 处理任意长度。", 15, fill=MUTED)]

    heading(out, 430, "B", "有限状态是一种等价类", TEAL)
    for y, hist in ((130, "[a,b,c]"), (215, "[u,v,w,…]")):
        out += [rect(450, y, 135, 44, BLUE, "#EFF6FF", 6, 2), text(518, y + 28, hist, 14, 650, "middle", BLUE)]
        out += [line(590, y + 22, 658, 250, TEAL, 2, marker="a1")]
    out += [circle(680, 250, 42, TEAL, "#ECFDF5", 2.5), text(680, 256, "h_t", 18, 700, "middle", TEAL)]
    out += [text(445, 335, "若两个历史映到同一 h_t，", 16, 650), text(445, 372, "后续 readout 无法再区分它们。", 16, 700, fill=RED)]
    out += [text(445, 445, "充分状态是任务相关命题，", 15, fill=MUTED), text(445, 477, "不是固定维向量的自动性质。", 15, fill=MUTED)]

    heading(out, 830, "C", "三种接口、三本资源账", RED)
    rows = ((115, "training", "unroll / scan", "activations"), (245, "prefill", "consume prefix", "throughput"), (375, "streaming", "one-step update", "state bytes"))
    for y, phase, op, cost in rows:
        out += [rect(845, y - 30, 285, 72, BLUE if y < 300 else TEAL, "#F8FAFC", 6, 2)]
        out += [text(865, y, phase, 15, 700, fill=RED), text(965, y, op, 15, 650), text(965, y + 25, cost, 13, 650, fill=MUTED)]
    out += [text(842, 490, "O(T) 算术 ≠ 任意设备上的低延迟。", 15, 700, fill=RED)]
    return finish(out, "先写清状态语义与因果可见性，再谈记忆长度和速度。")


def bptt_jacobian():
    out = begin(
        "BPTT：时间 Jacobian 乘积与方向性梯度",
        "长程梯度由一串随状态变化的 Jacobian 有序相乘；奇异方向可能衰减、放大或旋转。",
        (RED, BLUE, TEAL),
    )
    heading(out, 42, "A", "反向链条", RED)
    for i in range(4):
        x = 60 + i * 85
        out += [rect(x, 180, 58, 48, BLUE, "#EFF6FF", 5, 2), text(x + 29, 210, f"h{i}", 14, 700, "middle", BLUE)]
        if i < 3:
            out += [line(x + 60, 204, x + 81, 204, TEAL, 2.5, marker="a1")]
    out += [path("M320 260 C250 330 135 330 65 260", RED, 3, fill="none", marker="a3")]
    out += [text(192, 352, "J3^T J2^T J1^T g", 19, 700, "middle", RED, cls="math")]
    out += [text(45, 420, "J_t = d h_t / d h_(t-1)", 17, 700, cls="math")]
    out += [text(45, 474, "顺序不能交换；每个 J_t 都依赖轨迹。", 15, fill=MUTED)]

    heading(out, 430, "B", "同一乘积的三种方向", BLUE)
    baselines = ((160, 0.55, "vanish", BLUE), (285, 1.0, "preserve", TEAL), (410, 1.55, "explode", RED))
    for y, growth, label, color in baselines:
        out += [line(455, y, 745, y, GRID, 1.5), text(445, y + 5, label, 14, 700, "end", color)]
        pts = []
        for i in range(7):
            x = 475 + i * 42
            amp = max(4, min(42, 11 * (growth ** i)))
            pts.append((x, y - amp))
            out += [circle(x, y - amp, 3.5, color, color, 1)]
        out += [path("M" + " L".join(f"{x} {yy}" for x, yy in pts), color, 2.5)]
    out += [text(445, 485, "spectral radius 单独不足以描述非正规、时变乘积。", 14, fill=MUTED)]

    heading(out, 830, "C", "诊断与缓解不能混写", TEAL)
    cards = ((108, "clip", "限制爆炸更新", "不恢复已消失信号"), (225, "gating", "提供加法路径", "仍会饱和/遗忘"), (342, "orthogonal", "改善局部尺度", "非万能长期保证"), (459, "truncation", "省显存与计算", "截断信用路径"))
    for y, title, good, limit in cards:
        out += [text(845, y, title, 15, 700, fill=TEAL), text(930, y, good, 14, 650), text(930, y + 25, limit, 13, 650, fill=RED)]
    return finish(out, "梯度问题是矩阵乘积的方向性问题；措施要注明它解决哪一段。")


def lstm_cell():
    out = begin(
        "LSTM：加法记忆通道与三类门控",
        "cell state 通过逐元素加法更新；forget/input/output gate 分别控制保留、写入和暴露。",
        (TEAL, BLUE, RED),
    )
    heading(out, 42, "A", "cell highway", TEAL)
    out += [line(58, 160, 340, 160, TEAL, 5, marker="a1"), text(55, 135, "c_(t-1)", 16, 700, fill=TEAL), text(320, 135, "c_t", 16, 700, fill=TEAL)]
    out += [circle(135, 160, 17, BLUE, BG, 2.5), text(135, 166, "×", 18, 700, "middle", BLUE)]
    out += [circle(245, 160, 17, RED, BG, 2.5), text(245, 166, "+", 18, 700, "middle", RED)]
    out += [rect(76, 255, 90, 43, BLUE, "#EFF6FF", 5, 2), text(121, 282, "f_t", 16, 700, "middle", BLUE), line(121, 254, 132, 180, BLUE, 2, marker="a0")]
    out += [rect(185, 255, 70, 43, RED, "#FFF5F2", 5, 2), text(220, 282, "i_t", 16, 700, "middle", RED)]
    out += [rect(270, 255, 86, 43, RED, "#FFF5F2", 5, 2), text(313, 282, "c_new", 15, 700, "middle", RED)]
    out += [line(220, 254, 237, 180, RED, 2, marker="a0"), line(313, 254, 253, 180, RED, 2, marker="a0")]
    out += [text(45, 360, "c_t = f_t * c_(t-1) + i_t * c_new", 17, 700, cls="math", fill=TEAL)]
    out += [text(45, 420, "h_t = o_t * tanh(c_t)", 18, 700, cls="math", fill=BLUE)]
    out += [text(45, 480, "门值在 (0,1)，但不是概率事件。", 15, fill=MUTED)]

    heading(out, 430, "B", "直接梯度路径", BLUE)
    for i, f in enumerate((0.99, 0.95, 0.8)):
        y = 132 + i * 115
        val = f ** 50
        out += [text(445, y, f"f={f:.2f}", 15, 700, fill=BLUE), rect(520, y - 20, 215 * val, 28, TEAL, "#ECFDF5", 3, 1.5), text(740, y, f"f⁵⁰≈{val:.3f}", 14, 650, "end")]
    out += [text(445, 475, "product(f_k) 只是直接项；总导数还含门的依赖。", 14, fill=MUTED)]

    heading(out, 830, "C", "能够缓解，不等于保证", RED)
    for y, s in ((118, "✓ 加法状态路径"), (180, "✓ 可学习时间尺度"), (260, "△ sigmoid 饱和"), (322, "△ 截断 BPTT"), (384, "△ cell 数值漂移"), (446, "△ 任务未必可识别")):
        out += [text(848, y, s, 16, 700 if y < 230 else 650, fill=TEAL if y < 230 else RED)]
    return finish(out, "LSTM 改写了梯度与状态的路径结构，但长期学习仍受门值、训练和任务共同约束。")


def gru_conventions():
    out = begin(
        "GRU：更新约定、候选状态与实现差异",
        "GRU 用单一 hidden state 做门控插值；不同资料常把 z 的保留/写入语义写成互补形式。",
        (BLUE, RED, TEAL),
    )
    heading(out, 42, "A", "显式声明本课程约定", BLUE)
    out += [text(45, 125, "r_t = sigmoid(Wr x_t + Ur h_(t-1) + br)", 14, 650, cls="math")]
    out += [text(45, 185, "z_t = sigmoid(Wz x_t + Uz h_(t-1) + bz)", 14, 650, cls="math")]
    out += [text(45, 245, "h_new = tanh(Wh x_t + Uh(r_t * h_(t-1)) + bh)", 13, 650, cls="math")]
    out += [rect(45, 295, 315, 70, TEAL, "#ECFDF5", 6, 2.5), text(203, 326, "h_t=(1-z_t)h_(t-1)+z_t h_new", 14, 700, "middle", TEAL, cls="math")]
    out += [text(45, 412, "本页 z=1 表示更偏向写入候选。", 15, 700, fill=BLUE)]
    out += [text(45, 470, "有些资料交换 z 与 1−z；方程相容即可。", 14, fill=MUTED)]

    heading(out, 430, "B", "逐维插值，不是二选一开关", RED)
    out += [rect(455, 142, 85, 52, BLUE, "#EFF6FF", 5, 2), text(498, 174, "h old", 15, 700, "middle", BLUE)]
    out += [rect(650, 142, 85, 52, RED, "#FFF5F2", 5, 2), text(693, 174, "h new", 15, 700, "middle", RED)]
    out += [line(540, 168, 592, 260, BLUE, 3, marker="a1"), line(650, 168, 608, 260, RED, 3, marker="a1")]
    out += [circle(600, 280, 42, TEAL, "#ECFDF5", 2.5), text(600, 286, "h_t", 18, 700, "middle", TEAL)]
    out += [text(445, 370, "z=[0.1,0.9,…] 可让不同维度", 15, 650), text(445, 405, "拥有不同更新速率。", 16, 700, fill=TEAL)]
    out += [text(445, 475, "reset-before / reset-after 会改变数值图。", 14, fill=MUTED)]

    heading(out, 830, "C", "RNN / GRU / LSTM 合同比较", TEAL)
    rows = ((125, "state", "h", "h", "(h,c)"), (225, "add path", "no", "yes", "cell"), (325, "gates", "0", "2", "3"), (425, "stream", "d", "d", "2d"))
    out += [text(940, 82, "RNN", 14, 700, "middle", BLUE), text(1020, 82, "GRU", 14, 700, "middle", TEAL), text(1100, 82, "LSTM", 14, 700, "middle", RED)]
    for y, label, a, b, c in rows:
        out += [text(842, y, label, 14, 700), text(940, y, a, 14, 650, "middle"), text(1020, y, b, 14, 650, "middle"), text(1100, y, c, 14, 650, "middle"), line(840, y + 18, 1140, y + 18, GRID, 1)]
    return finish(out, "比较门控 RNN 时先对齐方程和状态接口，再比较参数、速度与任务证据。")


def continuous_discrete_ssm():
    out = begin(
        "线性状态空间：连续流、零阶保持与离散极点",
        "矩阵指数给出精确零阶保持离散化；连续稳定与离散稳定通过极点映射连接。",
        (TEAL, RED, BLUE),
    )
    heading(out, 42, "A", "一段采样间隔内的变分常数公式", TEAL)
    out += [text(45, 120, "ẋ(t)=Ax(t)+Bu(t)", 18, 700, cls="math", fill=TEAL)]
    out += [line(65, 235, 340, 235, GRID, 2), circle(95, 235, 7, BLUE, BLUE, 1), circle(305, 235, 7, RED, RED, 1)]
    out += [text(95, 265, "kΔ", 14, 650, "middle"), text(305, 265, "(k+1)Δ", 14, 650, "middle")]
    out += [rect(105, 180, 190, 35, BLUE, "#EFF6FF", 3, 1.5), text(200, 203, "u(t) = u_k  (ZOH)", 14, 650, "middle", BLUE)]
    out += [text(45, 330, "Abar = exp(A Delta)", 18, 700, cls="math", fill=BLUE)]
    out += [text(45, 380, "Bbar = integral exp(A tau) B d tau", 15, 700, cls="math", fill=RED)]
    out += [text(45, 447, "A 可逆时才可简写 A⁻¹(Ā−I)B。", 14, 700, fill=RED)]
    out += [text(45, 480, "奇异 A 应保留积分或用增广矩阵指数。", 14, fill=MUTED)]

    heading(out, 430, "B", "极点映射 z = exp(lambda Delta)", RED)
    out += [line(445, 285, 755, 285, GRID, 1.5), line(600, 100, 600, 470, GRID, 1.5)]
    out += [path("M485 285 A115 115 0 1 0 715 285 A115 115 0 1 0 485 285", TEAL, 2.5, fill="none")]
    for x, y, lab, color in ((550, 220, "stable", TEAL), (700, 190, "unstable", RED), (600, 170, "oscillatory", BLUE)):
        out += [circle(x, y, 7, color, color, 1), text(x + 12, y - 8, lab, 13, 650, fill=color)]
    out += [text(445, 485, "Re(lambda)<0 => |exp(lambda Delta)|<1。", 14, 700, fill=TEAL)]

    heading(out, 830, "C", "方法与步长共同决定稳定", BLUE)
    rows = ((110, "exact ZOH", "exp(A Delta)", "保留连续极点映射"), (215, "forward Euler", "I + Delta A", "大步长可失稳"), (320, "bilinear", "Cayley map", "扭曲频率但稳健"), (425, "learned Delta", "positive map", "需审计范围/精度"))
    for y, method, formula, note in rows:
        out += [text(845, y, method, 14, 700, fill=BLUE), text(970, y, formula, 14, 650, cls="math"), text(845, y + 28, note, 13, 650, fill=MUTED), line(842, y + 47, 1140, y + 47, GRID, 1)]
    return finish(out, "离散化定义了真正运行的 recurrence；方法、步长、精度和稳定域缺一不可。")


def recurrence_convolution_scan():
    out = begin(
        "同一 LTI 状态空间的三种计算接口",
        "线性时不变 recurrence 可展开为 convolution，也可把仿射更新编码成 associative scan。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "递推：流式状态", BLUE)
    for i in range(4):
        x = 55 + i * 82
        out += [rect(x, 165, 52, 45, BLUE, "#EFF6FF", 5, 2), text(x + 26, 193, f"x{i}", 13, 700, "middle", BLUE)]
        if i < 3:
            out += [line(x + 53, 187, x + 78, 187, BLUE, 2.5, marker="a1")]
    out += [text(45, 280, "x_(k+1) = Abar x_k + Bbar u_k", 16, 700, cls="math")]
    out += [text(45, 350, "stream: O(N) state", 15, 700, fill=BLUE), text(45, 390, "time span: O(L)", 15, 650)]
    out += [text(45, 475, "最适合逐 token 推进。", 15, fill=MUTED)]

    heading(out, 430, "B", "卷积：固定 impulse response", TEAL)
    out += [text(445, 115, "K_j = C Abar^j Bbar", 17, 700, cls="math", fill=TEAL)]
    for i, h in enumerate((38, 70, 100, 76, 52, 30)):
        x = 460 + i * 45
        out += [rect(x, 390 - h, 25, h, TEAL, "#ECFDF5", 2, 1.5)]
    out += [text(445, 430, "y=K*u", 18, 700, cls="math")]
    out += [text(445, 475, "只在 A,B,C 固定且 time-invariant 时是单一核。", 13, fill=MUTED)]

    heading(out, 830, "C", "scan：仿射变换的结合律", RED)
    out += [text(845, 115, "pair p=(A,b)", 15, 700, fill=RED), text(845, 155, "p2 o p1=(A2 A1, A2 b1+b2)", 14, 650, cls="math")]
    y = 270
    for i, label in enumerate(("p1", "p2", "p3", "p4")):
        x = 850 + i * 75
        out += [circle(x, y, 18, RED, "#FFF5F2", 2), text(x, y + 5, label, 13, 700, "middle", RED)]
    out += [path("M850 245 Q887 205 925 245", RED, 2), path("M1000 245 Q1037 205 1075 245", RED, 2), path("M888 202 Q963 125 1038 202", BLUE, 2.5)]
    out += [text(842, 370, "work O(L), span O(log L)", 15, 700, fill=BLUE)]
    out += [text(842, 420, "但 kernel fusion、IO 与数值顺序决定墙钟表现。", 13, fill=MUTED)]
    out += [text(842, 480, "input-dependent A_t：可 scan，不再是固定卷积。", 13, 700, fill=RED)]
    return finish(out, "recurrence、convolution 与 scan 是条件化的等价接口，不是可无条件互换的口号。")


def hippo_s4():
    out = begin(
        "HiPPO 到 S4：投影目标、状态动力学与结构化计算",
        "HiPPO 先规定怎样压缩历史，S4 再把相应状态动力学变成可训练、可高效计算的长序列层。",
        (TEAL, BLUE, RED),
    )
    heading(out, 42, "A", "历史函数投影", TEAL)
    pts = [(50 + i * 28, 235 - 55 * __import__('math').sin(i * .55) * (1 - i / 15)) for i in range(12)]
    out += [path("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts), BLUE, 2.5)]
    for n, y in enumerate((330, 370, 410)):
        out += [text(45, y, f"c{n}(t)=⟨u≤t,g{n}^(t)⟩", 15, 650, cls="math", fill=TEAL)]
    out += [text(45, 475, "measure mu_t 决定近史/全史的权重。", 14, fill=MUTED)]

    heading(out, 430, "B", "系数 ODE → HiPPO matrix", BLUE)
    out += [rect(460, 120, 95, 80, TEAL, "#ECFDF5", 5, 2), text(508, 153, "basis", 15, 700, "middle", TEAL), text(508, 179, "+ measure", 13, 650, "middle")]
    out += [line(556, 160, 625, 160, BLUE, 2.5, marker="a1")]
    out += [rect(630, 120, 95, 80, BLUE, "#EFF6FF", 5, 2), text(678, 153, "A,B", 17, 700, "middle", BLUE), text(678, 179, "coefficient ODE", 12, 650, "middle")]
    out += [text(445, 270, "ċ(t)=A(t)c(t)+B(t)u(t)", 17, 700, cls="math")]
    out += [text(445, 348, "optimality 属于指定 weighted L² projection", 14, 700, fill=RED)]
    out += [text(445, 392, "≠ 任意 downstream loss 最优", 14, 650, fill=RED)]
    out += [text(445, 475, "连续投影、离散误差、学习误差分账。", 14, fill=MUTED)]

    heading(out, 830, "C", "S4 的结构化计算路线", RED)
    stages = ((105, "HiPPO A"), (195, "NPLR / DPLR"), (285, "resolvent"), (375, "Cauchy kernel"), (465, "FFT convolution"))
    for i, (y, label) in enumerate(stages):
        out += [rect(865, y - 27, 230, 48, BLUE if i % 2 == 0 else TEAL, "#F8FAFC", 5, 2), text(980, y + 3, label, 15, 700, "middle")]
        if i < len(stages) - 1:
            out += [line(980, y + 23, 980, stages[i + 1][0] - 31, RED, 2, marker="a1")]
    return finish(out, "‘长记忆’先是投影几何命题，再是结构化代数和经验建模命题。")


def mamba_evidence():
    out = begin(
        "Mamba：输入依赖选择性、扫描内核与证据边界",
        "选择性 SSM 让部分更新参数依赖当前 token；内容条件增强的同时，固定卷积核接口消失。",
        (RED, TEAL, BLUE),
    )
    heading(out, 42, "A", "固定 LTI 与选择性更新", RED)
    out += [text(45, 112, "LTI", 16, 700, fill=BLUE)]
    for i in range(4):
        x = 60 + 76 * i
        out += [rect(x, 150, 55, 42, BLUE, "#EFF6FF", 5, 2), text(x + 27, 176, "same A", 11, 700, "middle", BLUE)]
    out += [text(45, 245, "Selective", 16, 700, fill=RED)]
    for i, color in enumerate((TEAL, RED, BLUE, RED)):
        x = 60 + 76 * i
        out += [rect(x, 285, 55, 42, color, "#F8FAFC", 5, 2), text(x + 27, 311, f"A{i+1}", 13, 700, "middle", color)]
    out += [text(45, 390, "Delta_t, B_t, C_t = functions of x_t", 15, 700, cls="math")]
    out += [text(45, 445, "可按内容调节写入/遗忘/读出。", 15, 650)]
    out += [text(45, 480, "但不再存在单一 K_j = C Abar^j Bbar。", 14, 700, fill=RED)]

    heading(out, 430, "B", "selective scan 的系统账", TEAL)
    rows = ((115, "arithmetic", "O(LN)"), (195, "parallel span", "tree scan"), (275, "IO", "fused / recompute"), (355, "stream state", "O(N) per layer"), (435, "precision", "long product audit"))
    for y, name, val in rows:
        out += [text(445, y, name, 14, 700, fill=TEAL), rect(570, y - 24, 165, 34, TEAL, "#ECFDF5", 4, 1.5), text(652, y - 1, val, 13, 650, "middle")]
    out += [text(445, 487, "复杂度、吞吐、首 token 延迟应分别测。", 13, fill=MUTED)]

    heading(out, 830, "C", "证据阶梯", BLUE)
    items = ((108, "I", "机制直觉", "选择性可按输入调节状态"), (188, "T", "条件化推导", "scan 结合律与线性长度"), (268, "E", "论文实验", "特定规模/数据/硬件"), (348, "H", "实现证据", "kernel、IO、精度"), (428, "O", "开放问题", "外推、检索与稳定记忆"))
    for y, code, kind, claim in items:
        out += [circle(860, y - 5, 16, RED if code in ("E", "O") else BLUE, BG, 2.5), text(860, y, code, 12, 700, "middle"), text(890, y, kind, 14, 700), text(890, y + 25, claim, 12, 650, fill=MUTED)]
    out += [text(842, 500, "‘线性时间’不是‘无限上下文记忆’的同义词。", 13, 700, fill=RED)]
    return finish(out, "Mamba 的核心是内容条件化状态更新与硬件扫描的联合设计；结论必须带实验条件。")


FIGURES = {
    "fig-sequence-state-causality-contract-v1.svg": state_contract,
    "fig-rnn-bptt-jacobian-product-v1.svg": bptt_jacobian,
    "fig-lstm-cell-gradient-highway-v1.svg": lstm_cell,
    "fig-gru-gate-conventions-v1.svg": gru_conventions,
    "fig-continuous-discrete-ssm-v1.svg": continuous_discrete_ssm,
    "fig-ssm-recurrence-convolution-scan-v1.svg": recurrence_convolution_scan,
    "fig-hippo-s4-projection-structure-v1.svg": hippo_s4,
    "fig-mamba-selectivity-evidence-v1.svg": mamba_evidence,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, builder in FIGURES.items():
        target = OUT / filename
        target.write_text(builder(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Static inventory and incremental teaching-contract audit for NN-01--64."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHAPTER = ROOT / "30-神经网络基础"
LABS = ROOT / "00-知识库管理" / "_labs"
EXERCISES = LABS / "exercises"
SOLUTIONS = LABS / "solutions"
CODE = LABS / "code"
FIGURE_AUDITOR = CODE / "audit-markdown-figure-units.mjs"
ASSET_DIR = ROOT / "00-知识库管理" / "_assets" / "figures" / "neural-networks"
MIGRATED_IDS = tuple(range(1, 65))

STATE_SURFACES = (
    CHAPTER / "神经网络基础 MOC.md",
    CHAPTER / "神经网络基础完整课程地图与掌握标准.md",
    EXERCISES / "练习与测验 MOC.md",
    LABS / "推导与实验 MOC.md",
    ROOT / "00-知识库管理" / "00-总览" / "全库教学重写审计与迁移台账.md",
    CHAPTER / "30.1-前馈网络、感知机与表达能力" / "前馈网络、感知机与表达能力 MOC.md",
    CHAPTER / "30.2-计算图、反向传播与自动微分" / "计算图、反向传播与自动微分 MOC.md",
    CHAPTER / "30.3-激活函数、门控与非线性" / "激活函数、门控与非线性 MOC.md",
    CHAPTER / "30.4-初始化与信号传播" / "初始化与信号传播 MOC.md",
    CHAPTER / "30.5-归一化、尺度与统计量" / "归一化、尺度与统计量 MOC.md",
    CHAPTER / "30.6-残差连接、深度与稳定性" / "残差连接、深度与稳定性 MOC.md",
    CHAPTER / "30.7-Embedding、权重共享与输出参数化" / "Embedding、权重共享与输出参数化 MOC.md",
    CHAPTER / "30.8-随机正则化与网络级泛化接口" / "随机正则化与网络级泛化接口 MOC.md",
)

EXPECTED_FIGURE_SCRIPTS = {
    "plot_activation_advanced_v2.py",
    "plot_activation_foundations_v2.py",
    "plot_backprop_advanced_v2.py",
    "plot_backprop_foundations_v2.py",
    "plot_embedding_output_advanced_v2.py",
    "plot_embedding_output_foundations_v2.py",
    "plot_feedforward_expressivity_v2.py",
    "plot_feedforward_foundations_v2.py",
    "plot_initialization_advanced_v2.py",
    "plot_initialization_foundations_v2.py",
    "plot_normalization_advanced_v2.py",
    "plot_normalization_foundations_v2.py",
    "plot_random_regularization_foundations_v2.py",
    "plot_regularization_interfaces_v2.py",
    "plot_residual_advanced_v2.py",
    "plot_residual_foundations_v2.py",
}

KNOWN_EXTENSIONS = {".md", ".py", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".pdf"}
IMAGE_EXTENSIONS = {".svg", ".png", ".jpg", ".jpeg", ".webp"}
SOURCE_KEYS = (
    "source_type", "title", "author", "year", "url", "accessed",
    "source_tier", "scope_role", "temporal_role",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def active_text(content: str) -> str:
    output: list[str] = []
    in_fence = False
    fence = ""
    for line in content.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence, fence = True, marker
            elif marker == fence:
                in_fence, fence = False, ""
            continue
        if not in_fence:
            output.append(line)
    return "\n".join(output)


def frontmatter_line(content: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", content, re.M)
    return match.group(1).strip() if match else ""


def wiki_targets(content: str, embeds: bool | None = None) -> list[str]:
    text = active_text(content)
    if embeds is True:
        matches = re.findall(r"!\[\[([^\]\n]+)\]\]", text)
    elif embeds is False:
        matches = re.findall(r"(?<!!)\[\[([^\]\n]+)\]\]", text)
    else:
        matches = re.findall(r"\[\[([^\]\n]+)\]\]", text)
    targets: list[str] = []
    for raw in matches:
        target = raw.replace("\\|", "|").split("|", 1)[0].split("#", 1)[0].strip().rstrip("\\")
        if target:
            targets.append(target)
    return targets


def frontmatter_targets(content: str, key: str) -> list[str]:
    return wiki_targets(frontmatter_line(content, key))


def build_index() -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = {}
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        key = path.stem if path.suffix.lower() in KNOWN_EXTENSIONS else path.name
        index.setdefault(key, []).append(path)
    return index


def resolve(target: str, index: dict[str, list[Path]]) -> list[Path]:
    suffix = Path(target).suffix.lower()
    if "/" in target:
        direct = ROOT / target
        candidates = [direct] if direct.is_file() else []
        if not candidates and suffix not in KNOWN_EXTENSIONS:
            markdown = Path(str(direct) + ".md")
            if markdown.is_file():
                candidates = [markdown]
        return candidates
    key = target[: -len(suffix)] if suffix in KNOWN_EXTENSIONS else target
    candidates = index.get(key, [])
    if suffix in KNOWN_EXTENSIONS:
        candidates = [path for path in candidates if path.suffix.lower() == suffix]
    return candidates


def collect_nodes() -> list[tuple[int, Path, str]]:
    nodes: list[tuple[int, Path, str]] = []
    for path in CHAPTER.rglob("*.md"):
        content = read(path)
        match = re.search(r"^node_id:\s*NN-(\d{2})$", content, re.M)
        if match:
            nodes.append((int(match.group(1)), path, content))
    return sorted(nodes)


def audit_scope(nodes: list[tuple[int, Path, str]]) -> None:
    ids = [node_id for node_id, _, _ in nodes]
    require(ids == list(range(1, 65)), f"NN IDs are not exactly 01--64: {ids}")
    require(len({path for _, path, _ in nodes}) == 64, "NN node paths are not unique")
    volume_rows: list[str] = []
    allowed_types = {"comparison", "concept", "derivation", "framework", "method", "moc", "model", "synthesis", "theorem"}
    type_counts: Counter[str] = Counter()
    for volume in range(1, 9):
        volume_ids = [node_id for node_id, path, _ in nodes if path.parent.name.startswith(f"30.{volume}-")]
        expected = list(range(8 * volume - 7, 8 * volume + 1))
        require(volume_ids == expected, f"30.{volume} node contract changed: {volume_ids}")
        volume_rows.append(f"30.{volume}=8")
    for node_id, path, content in nodes:
        relative = path.relative_to(ROOT)
        node_type = frontmatter_line(content, "type")
        require(node_type in allowed_types, f"{relative}: unsupported type {node_type!r}")
        type_counts[node_type] += 1
        require(frontmatter_line(content, "status") == "draft", f"{relative}: node state must remain draft")
        require(frontmatter_line(content, "node_id") == f"NN-{node_id:02d}", f"{relative}: node ID mismatch")
        require(frontmatter_line(content, "created") and frontmatter_line(content, "updated"), f"{relative}: dates missing")
        require(frontmatter_targets(content, "sources"), f"{relative}: sources missing")
        require(len(frontmatter_targets(content, "exercises")) == 1, f"{relative}: exercise target must be singular")
        require(len(frontmatter_targets(content, "solutions")) == 1, f"{relative}: solution target must be singular")
        require(len(frontmatter_targets(content, "figure")) == 1, f"{relative}: figure frontmatter target missing")
        require("[!abstract]" in content, f"{relative}: abstract missing")
        require("怎样读图" in content and "图没有证明什么" in content, f"{relative}: figure reading/boundary contract missing")
        require(content.count("$$") % 2 == 0, f"{relative}: unbalanced display math")
    print(
        "PASS NN static scope: 64/64 unique nodes; " + ", ".join(volume_rows)
        + f"; types={dict(sorted(type_counts.items()))}"
    )


def audit_migrated_contract(nodes: list[tuple[int, Path, str]]) -> None:
    markers = (
        "课程位置与两遍学习路线", "问题链", "第一遍停靠线",
        "符号与对象账本", "贯穿算例", "核心公式七问",
    )
    migrated = [(node_id, path, content) for node_id, path, content in nodes if node_id in MIGRATED_IDS]
    require([node_id for node_id, _, _ in migrated] == list(MIGRATED_IDS), "migrated NN wave changed")
    for node_id, path, content in migrated:
        relative = path.relative_to(ROOT)
        for marker in markers:
            require(marker in content, f"{relative}: teaching-contract marker missing: {marker}")
        fixture = (
            "X_\\star" if node_id <= 4 else
            "X_\\oplus" if node_id <= 8 else
            "X_\\diamond" if node_id <= 16 else
            "s_\\triangle" if node_id <= 24 else
            "\\mathcal I_\\square" if node_id <= 32 else
            "\\mathcal N_\\square" if node_id <= 40 else
            "\\mathcal R_\\square" if node_id <= 48 else
            "\\mathcal E_\\square" if node_id <= 56 else
            "\\mathcal D_\\square"
        )
        require(fixture in content, f"{relative}: shared teaching fixture missing: {fixture}")
        require("AI" in content, f"{relative}: AI object mapping missing")
        require(len(content.splitlines()) >= 180, f"{relative}: derivation depth unexpectedly short")
    print("PASS NN teaching migration waves A--P: NN-01--64 course position/two-pass/problem/object/formula contracts=64/64")


def audit_wave_c_fixture(nodes: list[tuple[int, Path, str]]) -> None:
    """Recompute the NN-09--12 affine-regression fixture without importing note code."""
    x = ((1.0, 2.0), (-1.0, 1.0))
    w = ((1.0, -1.0), (2.0, 1.0))
    b = (0.0, 1.0)
    y = ((4.0, 1.0), (2.0, 1.0))
    lam = 0.5

    def mm(a: tuple[tuple[float, ...], ...], c: tuple[tuple[float, ...], ...]) -> tuple[tuple[float, ...], ...]:
        return tuple(tuple(sum(a[i][k] * c[k][j] for k in range(len(c))) for j in range(len(c[0]))) for i in range(len(a)))

    def transpose(a: tuple[tuple[float, ...], ...]) -> tuple[tuple[float, ...], ...]:
        return tuple(tuple(a[i][j] for i in range(len(a))) for j in range(len(a[0])))

    z0 = mm(x, w)
    z = tuple(tuple(z0[i][j] + b[j] for j in range(2)) for i in range(2))
    residual = tuple(tuple(z[i][j] - y[i][j] for j in range(2)) for i in range(2))
    loss = 0.5 * sum(value * value for row in residual for value in row) + 0.5 * lam * sum(value * value for row in w for value in row)
    require(z == ((5.0, 2.0), (1.0, 3.0)) and residual == ((1.0, 1.0), (-1.0, 2.0)), "NN wave-C forward fixture drifted")
    require(loss == 5.25, f"NN wave-C loss drifted: {loss}")

    direction = ((1.0, 0.0), (0.0, 0.0))
    dz = mm(x, direction)
    directional = sum(residual[i][j] * dz[i][j] for i in range(2) for j in range(2)) + lam * sum(w[i][j] * direction[i][j] for i in range(2) for j in range(2))
    data_w = mm(transpose(x), residual)
    reg_w = tuple(tuple(lam * w[i][j] for j in range(2)) for i in range(2))
    total_w = tuple(tuple(data_w[i][j] + reg_w[i][j] for j in range(2)) for i in range(2))
    grad_x = mm(residual, transpose(w))
    grad_b = tuple(sum(residual[i][j] for i in range(2)) for j in range(2))
    require(dz == ((1.0, 0.0), (-1.0, 0.0)) and directional == 2.5, "NN wave-C JVP drifted")
    require(data_w == ((2.0, -1.0), (1.0, 4.0)), f"NN wave-C data gradient drifted: {data_w}")
    require(total_w == ((2.5, -1.5), (2.0, 4.5)), f"NN wave-C total gradient drifted: {total_w}")
    require(grad_x == ((0.0, 3.0), (-3.0, 0.0)) and grad_b == (0.0, 3.0), "NN wave-C affine VJP drifted")

    wave = {node_id: content for node_id, _, content in nodes if 9 <= node_id <= 12}
    expected_markers = {9: ("L=5.25",), 10: ("2.5",), 11: ("L=5.25", "2.5"), 12: ("2.5",)}
    for node_id, expected in expected_markers.items():
        require(all(marker in wave[node_id] for marker in expected), f"NN-{node_id:02d}: shared numeric closure missing")
    print("PASS NN wave-C independent math: forward loss=5.25; JVP/VJP=2.5; data/reg/affine gradients exact")


def audit_wave_d_fixture(nodes: list[tuple[int, Path, str]]) -> None:
    """Recompute the NN-13--16 residual-softmax fixture independently."""
    z = ((5.0, 2.0), (1.0, 3.0))
    c = (2.0, 2.0)
    a = tuple(tuple(z[i][j] - c[j] for j in range(2)) for i in range(2))
    h = tuple(tuple(max(0.0, a[i][j]) for j in range(2)) for i in range(2))
    q = tuple(tuple(z[i][j] + h[i][j] for j in range(2)) for i in range(2))
    require(a == ((3.0, 0.0), (-1.0, 1.0)) and h == ((3.0, 0.0), (0.0, 1.0)), "NN wave-D ReLU fixture drifted")
    require(q == ((8.0, 2.0), (1.0, 4.0)), f"NN wave-D logits drifted: {q}")

    upstream = ((1.0, -1.0), (2.0, 1.0))
    mask = tuple(tuple(1.0 if a[i][j] > 0.0 else 0.0 for j in range(2)) for i in range(2))
    grad_z = tuple(tuple(upstream[i][j] * (1.0 + mask[i][j]) for j in range(2)) for i in range(2))
    grad_c = tuple(-sum(upstream[i][j] * mask[i][j] for i in range(2)) for j in range(2))
    require(grad_z == ((2.0, -1.0), (2.0, 2.0)) and grad_c == (-1.0, -1.0), "NN wave-D branch/broadcast VJP drifted")

    probs: list[tuple[float, float]] = []
    for row in q:
        maximum = max(row)
        exps = tuple(math.exp(value - maximum) for value in row)
        total = sum(exps)
        probs.append((exps[0] / total, exps[1] / total))
    loss = (-math.log(probs[0][0]) - math.log(probs[1][1])) / 2.0
    logit_grad = (((probs[0][0] - 1.0) / 2.0, probs[0][1] / 2.0), (probs[1][0] / 2.0, (probs[1][1] - 1.0) / 2.0))
    directional = logit_grad[0][0]
    hvp_scale = probs[0][0] * probs[0][1] / 2.0
    require(abs(loss - 0.02553151835573612) < 1e-15, f"NN wave-D CE loss drifted: {loss}")
    require(abs(directional + 0.0012363115783173284) < 1e-15, f"NN wave-D JVP/VJP drifted: {directional}")
    require(abs(hvp_scale - 0.0012332546456799655) < 1e-15, f"NN wave-D HVP drifted: {hvp_scale}")
    require(all(abs(sum(row)) < 1e-15 for row in logit_grad), "NN wave-D softmax shift-null direction drifted")

    wave = {node_id: content for node_id, _, content in nodes if 13 <= node_id <= 16}
    expected = {13: ("Q=Z+H",), 14: ("0.0255315",), 15: ("-0.00123631",), 16: ("0.00123325",)}
    for node_id, markers in expected.items():
        require(all(marker in wave[node_id] for marker in markers), f"NN-{node_id:02d}: wave-D numeric closure missing")
    print("PASS NN wave-D independent math: residual/broadcast VJP; stable CE=0.0255315; JVP/VJP and HVP exact")


def audit_wave_e_fixture(nodes: list[tuple[int, Path, str]]) -> None:
    """Recompute the NN-17--20 three-point activation probe."""
    points = (-2.0, 0.0, 2.0)
    sigmoid = tuple(1.0 / (1.0 + math.exp(-value)) for value in points)
    sigmoid_grad = tuple(value * (1.0 - value) for value in sigmoid)
    tanh = tuple(math.tanh(value) for value in points)
    tanh_grad = tuple(1.0 - value * value for value in tanh)
    relu = tuple(max(0.0, value) for value in points)
    relu_grad = (0.0, 0.0, 1.0)
    leaky = tuple(value if value > 0.0 else 0.1 * value for value in points)
    leaky_grad = (0.1, 0.1, 1.0)
    elu = tuple(value if value > 0.0 else math.exp(value) - 1.0 for value in points)
    elu_grad = (math.exp(-2.0), 1.0, 1.0)
    require(all(abs(a - b) < 1e-6 for a, b in zip(sigmoid, (0.119203, 0.5, 0.880797))), "NN wave-E sigmoid values drifted")
    require(all(abs(a - b) < 1e-6 for a, b in zip(sigmoid_grad, (0.104994, 0.25, 0.104994))), "NN wave-E sigmoid gradients drifted")
    require(all(abs(a - b) < 1e-6 for a, b in zip(tanh, (-0.964028, 0.0, 0.964028))), "NN wave-E tanh values drifted")
    require(all(abs(a - b) < 1e-6 for a, b in zip(tanh_grad, (0.070651, 1.0, 0.070651))), "NN wave-E tanh gradients drifted")
    require(relu == (0.0, 0.0, 2.0) and relu_grad == (0.0, 0.0, 1.0), "NN wave-E ReLU convention drifted")
    require(leaky == (-0.2, 0.0, 2.0) and leaky_grad == (0.1, 0.1, 1.0), "NN wave-E Leaky convention drifted")
    require(all(abs(a - b) < 1e-6 for a, b in zip(elu, (-0.864665, 0.0, 2.0))), "NN wave-E ELU values drifted")
    require(all(abs(a - b) < 1e-6 for a, b in zip(elu_grad, (0.135335, 1.0, 1.0))), "NN wave-E ELU gradients drifted")
    wave = {node_id: content for node_id, _, content in nodes if 17 <= node_id <= 20}
    expected = {17: ("s_\\triangle=(-2,0,2)",), 18: ("0.104994", "0.070651"), 19: ("0.1,0.1,1",), 20: ("0.864665", "0.135335")}
    for node_id, markers in expected.items():
        require(all(marker in wave[node_id] for marker in markers), f"NN-{node_id:02d}: wave-E numeric closure missing")
    print("PASS NN wave-E independent math: sigmoid/tanh saturation; ReLU/Leaky conventions; ELU negative branch exact")


def audit_wave_f_fixture(nodes: list[tuple[int, Path, str]]) -> None:
    """Recompute the NN-21--24 smooth/gated/maxout continuation independently."""
    points = (-2.0, 0.0, 2.0)

    sigmoid = tuple(1.0 / (1.0 + math.exp(-value)) for value in points)
    softplus = tuple(math.log1p(math.exp(value)) for value in points)
    normal_cdf = tuple(0.5 * (1.0 + math.erf(value / math.sqrt(2.0))) for value in points)
    normal_pdf = tuple(math.exp(-0.5 * value * value) / math.sqrt(2.0 * math.pi) for value in points)
    gelu = tuple(value * cdf for value, cdf in zip(points, normal_cdf))
    gelu_grad = tuple(cdf + value * pdf for value, cdf, pdf in zip(points, normal_cdf, normal_pdf))
    silu = tuple(value * gate for value, gate in zip(points, sigmoid))
    silu_grad = tuple(gate + value * gate * (1.0 - gate) for value, gate in zip(points, sigmoid))

    def close(actual: tuple[float, ...], expected: tuple[float, ...], label: str) -> None:
        require(all(abs(a - b) < 1e-6 for a, b in zip(actual, expected)), f"NN wave-F {label} drifted: {actual}")

    close(softplus, (0.126928, 0.693147, 2.126928), "Softplus values")
    close(sigmoid, (0.119203, 0.5, 0.880797), "Softplus gradients")
    close(gelu, (-0.045500, 0.0, 1.954500), "GELU values")
    close(gelu_grad, (-0.085232, 0.5, 1.085232), "GELU gradients")
    close(silu, (-0.238406, 0.0, 1.761594), "SiLU values")
    close(silu_grad, (-0.090784, 0.5, 1.090784), "SiLU gradients")

    values = (1.0, -1.0, 2.0)
    upstream = (1.0, 1.0, 1.0)
    glu = tuple(value * gate for value, gate in zip(values, sigmoid))
    glu_value_grad = tuple(bar * gate for bar, gate in zip(upstream, sigmoid))
    glu_gate_grad = tuple(bar * value * gate * (1.0 - gate) for bar, value, gate in zip(upstream, values, sigmoid))
    swiglu = tuple(value * gate for value, gate in zip(values, silu))
    swiglu_value_grad = tuple(bar * gate for bar, gate in zip(upstream, silu))
    swiglu_gate_grad = tuple(bar * value * derivative for bar, value, derivative in zip(upstream, values, silu_grad))
    close(glu, (0.119203, -0.5, 1.761594), "GLU outputs")
    close(glu_value_grad, (0.119203, 0.5, 0.880797), "GLU value gradients")
    close(glu_gate_grad, (0.104994, -0.25, 0.209987), "GLU gate gradients")
    close(swiglu, (-0.238406, 0.0, 3.523188), "SwiGLU outputs")
    close(swiglu_value_grad, (-0.238406, 0.0, 1.761594), "SwiGLU value gradients")
    close(swiglu_gate_grad, (-0.090784, -0.5, 2.181568), "SwiGLU gate gradients")

    candidates = tuple((value, -value, 0.5) for value in points)
    outputs = tuple(max(row) for row in candidates)
    winners = tuple(row.index(max(row)) + 1 for row in candidates)
    slopes = tuple((1.0, -1.0, 0.0)[winner - 1] for winner in winners)
    require(outputs == (2.0, 0.5, 2.0), f"NN wave-F maxout outputs drifted: {outputs}")
    require(winners == (2, 3, 1) and slopes == (-1.0, 0.0, 1.0), "NN wave-F maxout routing drifted")

    wave = {node_id: content for node_id, _, content in nodes if 21 <= node_id <= 24}
    expected = {
        21: ("0.126928", "1.085232", "1.090784"),
        22: ("3.523188", "2.181568"),
        23: ("(2,0.5,2)", "(-1,0,1)"),
        24: ("数学门", "统计门", "\\text{claim}"),
    }
    for node_id, markers in expected.items():
        require(all(marker in wave[node_id] for marker in markers), f"NN-{node_id:02d}: wave-F numeric/evidence closure missing")
    print("PASS NN wave-F independent math: Softplus/GELU/SiLU; GLU/SwiGLU two-route VJP; Maxout winners; five-gate evidence closure")


def audit_wave_g_fixture(nodes: list[tuple[int, Path, str]]) -> None:
    """Recompute the NN-25--28 4-to-8 initialization and fan ledger."""
    fan_in, fan_out = 4.0, 8.0
    input_second_moment = 1.0
    relu_forward_factor = relu_derivative_factor = 0.5

    he_fan_in_variance = 2.0 / fan_in
    preactivation_second_moment = fan_in * he_fan_in_variance * input_second_moment
    activation_second_moment = relu_forward_factor * preactivation_second_moment
    require(preactivation_second_moment == 2.0 and activation_second_moment == 1.0, "NN wave-G moment recursion drifted")

    xavier_forward = 1.0 / fan_in
    xavier_backward = 1.0 / fan_out
    xavier_variance = 2.0 / (fan_in + fan_out)
    xavier_forward_multiplier = fan_in * xavier_variance
    xavier_backward_multiplier = fan_out * xavier_variance
    xavier_std = math.sqrt(xavier_variance)
    xavier_uniform_bound = math.sqrt(3.0 * xavier_variance)
    require(xavier_forward == 0.25 and xavier_backward == 0.125 and xavier_variance == 1.0 / 6.0, "NN wave-G Xavier targets drifted")
    require(xavier_forward_multiplier == 2.0 / 3.0 and xavier_backward_multiplier == 4.0 / 3.0, "NN wave-G Xavier multipliers drifted")
    require(abs(xavier_std - 0.408248290463863) < 1e-15, "NN wave-G Xavier normal scale drifted")
    require(abs(xavier_uniform_bound - 0.7071067811865476) < 1e-15, "NN wave-G Xavier uniform scale drifted")

    he_std = math.sqrt(he_fan_in_variance)
    he_uniform_bound = math.sqrt(3.0 * he_fan_in_variance)
    relu_mean = 1.0 / math.sqrt(math.pi)
    relu_variance = 1.0 - 1.0 / math.pi
    require(abs(he_std - 0.7071067811865476) < 1e-15, "NN wave-G He normal scale drifted")
    require(abs(he_uniform_bound - 1.224744871391589) < 1e-15, "NN wave-G He uniform scale drifted")
    require(abs(relu_mean - 0.5641895835477563) < 1e-15 and abs(relu_variance - 0.6816901138162093) < 1e-15, "NN wave-G ReLU moment ledger drifted")

    he_fan_out_variance = 2.0 / fan_out
    fan_average_rectifier_variance = 2.0 / (
        fan_in * relu_forward_factor + fan_out * relu_derivative_factor
    )

    def multipliers(variance: float) -> tuple[float, float]:
        return (
            fan_in * variance * relu_forward_factor,
            fan_out * variance * relu_derivative_factor,
        )

    require(multipliers(he_fan_in_variance) == (1.0, 2.0), "NN wave-G fan-in He tradeoff drifted")
    require(multipliers(he_fan_out_variance) == (0.5, 1.0), "NN wave-G fan-out He tradeoff drifted")
    require(multipliers(fan_average_rectifier_variance) == (2.0 / 3.0, 4.0 / 3.0), "NN wave-G fan-average tradeoff drifted")
    forward_depth_six = (2.0 / 3.0) ** 6
    backward_depth_six = (4.0 / 3.0) ** 6
    require(abs(forward_depth_six - 64.0 / 729.0) < 1e-15, "NN wave-G forward depth product drifted")
    require(abs(backward_depth_six - 4096.0 / 729.0) < 1e-14, "NN wave-G backward depth product drifted")

    wave = {node_id: content for node_id, _, content in nodes if 25 <= node_id <= 28}
    expected = {
        25: ("q_1=2", "r_1=1"),
        26: ("0.408248", "0.707107", "\\chi_f=2/3"),
        27: ("0.564190", "0.681690", "1.224745"),
        28: ("(1,2)", "(2/3,4/3)", "5.618656"),
    }
    for node_id, markers in expected.items():
        require(all(marker in wave[node_id] for marker in markers), f"NN-{node_id:02d}: wave-G numeric closure missing")
    print("PASS NN wave-G independent math: 4-to-8 moment recursion; Xavier/He scales; fan-in/out tradeoff; six-layer products exact")


def audit_wave_h_fixture(nodes: list[tuple[int, Path, str]]) -> None:
    """Recompute the NN-29--32 correlation, spectrum, symmetry, and calibration chain."""
    correlation = 0.5
    relu_correlation = (
        math.sqrt(1.0 - correlation * correlation)
        + (math.pi - math.acos(correlation)) * correlation
    ) / math.pi
    relu_correlation_exact = 1.0 / 3.0 + math.sqrt(3.0) / (2.0 * math.pi)
    relu_map_derivative = 1.0 - math.acos(correlation) / math.pi
    require(abs(relu_correlation - relu_correlation_exact) < 1e-15, "NN wave-H ReLU correlation map drifted")
    require(abs(relu_correlation - 0.6089977810442294) < 1e-15, "NN wave-H ReLU correlation numeric drifted")
    require(abs(relu_map_derivative - 2.0 / 3.0) < 1e-15, "NN wave-H ReLU correlation derivative drifted")

    # Q=(1/sqrt(2))[I; I], W=sqrt(2)Q=[I; I].
    q_gram_diagonal = tuple(0.5 + 0.5 for _ in range(4))
    q_gram_off_diagonal = 0.0
    require(q_gram_diagonal == (1.0, 1.0, 1.0, 1.0) and q_gram_off_diagonal == 0.0, "NN wave-H semi-orthogonal Gram drifted")
    x = (1.0, -1.0, 2.0, -2.0)
    preactivation = x + x
    active = tuple(value > 0.0 for value in preactivation)
    jtj_diagonal = tuple(2.0 if x[index] > 0.0 else 0.0 for index in range(4))
    singular_values = tuple(sorted((math.sqrt(value) for value in jtj_diagonal), reverse=True))
    mean_square_singular = sum(value * value for value in singular_values) / 4.0
    require(preactivation == (1.0, -1.0, 2.0, -2.0, 1.0, -1.0, 2.0, -2.0), "NN wave-H orthogonal probe forward drifted")
    require(active == (True, False, True, False, True, False, True, False), "NN wave-H ReLU mask drifted")
    require(jtj_diagonal == (2.0, 0.0, 2.0, 0.0), "NN wave-H local Gram drifted")
    require(singular_values == (math.sqrt(2.0), math.sqrt(2.0), 0.0, 0.0), "NN wave-H local singular values drifted")
    require(abs(mean_square_singular - 1.0) < 1e-15 and sum(value > 0.0 for value in singular_values) == 2, "NN wave-H rank/mean-square contrast drifted")

    hidden = (1.0, -1.0)
    output_weight = (0.0, 0.0)
    upstream = 1.0
    output_weight_gradient = tuple(upstream * value for value in hidden)
    hidden_gradient = tuple(upstream * value for value in output_weight)
    learning_rate = 0.1
    updated_output_weight = tuple(weight - learning_rate * gradient for weight, gradient in zip(output_weight, output_weight_gradient))
    require(output_weight_gradient == (1.0, -1.0), "NN wave-H zero-head parameter gradient drifted")
    require(hidden_gradient == (0.0, 0.0) and updated_output_weight == (-0.1, 0.1), "NN wave-H zero-head staged update drifted")
    require(upstream == 1.0, "NN wave-H residual skip gradient drifted")

    measured_variance = 4.0
    lsuv_scale = 1.0 / math.sqrt(measured_variance)
    calibrated_variance = measured_variance * lsuv_scale * lsuv_scale
    branches, branch_layers = 16.0, 3.0
    fixup_scale = branches ** (-1.0 / (2.0 * branch_layers - 2.0))
    branch_amplitude = fixup_scale ** (branch_layers - 1.0)
    branch_squared_scale = branch_amplitude * branch_amplitude
    require(lsuv_scale == 0.5 and calibrated_variance == 1.0, "NN wave-H LSUV calibration drifted")
    require(fixup_scale == 0.5 and branch_amplitude == 0.25 and branch_squared_scale == 1.0 / 16.0, "NN wave-H Fixup depth scale drifted")

    wave = {node_id: content for node_id, _, content in nodes if 29 <= node_id <= 32}
    expected = {
        29: ("0.608998", "\\mathcal C'(c_0)=2/3"),
        30: ("(\\sqrt2,\\sqrt2,0,0)", "\\operatorname{diag}(2,0,2,0)"),
        31: ("(-0.1,0.1)^T", "\\nabla h=(0,0)"),
        32: ("16^{-1/4}", "branch squared scale $1/16$"),
    }
    for node_id, markers in expected.items():
        require(all(marker in wave[node_id] for marker in markers), f"NN-{node_id:02d}: wave-H numeric closure missing")
    print("PASS NN wave-H independent math: ReLU correlation; semi-orthogonal rank collapse; zero-head gradients; LSUV/Fixup scales exact")


def audit_wave_i_fixture(nodes: list[tuple[int, Path, str]]) -> None:
    """Recompute the NN-33--36 axis, state, and normalization-VJP chain."""
    x = (
        (1.0, 2.0, 3.0),
        (2.0, 4.0, 6.0),
        (3.0, 6.0, 9.0),
    )

    def normalize(groups: tuple[tuple[float, ...], ...]) -> tuple[tuple[float, ...], tuple[float, ...], tuple[tuple[float, ...], ...]]:
        means = tuple(sum(group) / len(group) for group in groups)
        variances = tuple(
            sum((value - mean) ** 2 for value in group) / len(group)
            for group, mean in zip(groups, means)
        )
        normalized = tuple(
            tuple((value - mean) / math.sqrt(variance) for value in group)
            for group, mean, variance in zip(groups, means, variances)
        )
        return means, variances, normalized

    columns = tuple(tuple(x[row][column] for row in range(3)) for column in range(3))
    bn_means, bn_variances, bn_columns = normalize(columns)
    ln_means, ln_variances, ln_rows = normalize(x)
    a = math.sqrt(3.0 / 2.0)
    expected_stats = ((2.0, 4.0, 6.0), (2.0 / 3.0, 8.0 / 3.0, 6.0))
    require(bn_means == ln_means == expected_stats[0], "NN wave-I means drifted")
    require(all(abs(actual - expected) < 1e-15 for actual, expected in zip(bn_variances, expected_stats[1])), "NN wave-I BN variance drifted")
    require(all(abs(actual - expected) < 1e-15 for actual, expected in zip(ln_variances, expected_stats[1])), "NN wave-I LN variance drifted")
    bn = tuple(tuple(bn_columns[column][row] for column in range(3)) for row in range(3))
    expected_bn = ((-a, -a, -a), (0.0, 0.0, 0.0), (a, a, a))
    expected_ln = ((-a, 0.0, a), (-a, 0.0, a), (-a, 0.0, a))
    require(all(abs(bn[i][j] - expected_bn[i][j]) < 1e-15 for i in range(3) for j in range(3)), "NN wave-I BN axes drifted")
    require(all(abs(ln_rows[i][j] - expected_ln[i][j]) < 1e-15 for i in range(3) for j in range(3)), "NN wave-I LN axes drifted")

    unbiased = tuple(1.5 * value for value in bn_variances)
    running_mean = tuple(0.5 * value for value in bn_means)
    running_variance = tuple(0.5 + 0.5 * value for value in unbiased)
    require(unbiased == (1.0, 4.0, 9.0), f"NN wave-I unbiased observations drifted: {unbiased}")
    require(running_mean == (1.0, 2.0, 3.0) and running_variance == (1.0, 2.5, 5.0), "NN wave-I running state drifted")
    eval_output = tuple(
        tuple((x[i][j] - running_mean[j]) / math.sqrt(running_variance[j]) for j in range(3))
        for i in range(3)
    )
    expected_eval = (
        (0.0, 0.0, 0.0),
        (1.0, math.sqrt(8.0 / 5.0), 3.0 / math.sqrt(5.0)),
        (2.0, math.sqrt(32.0 / 5.0), 6.0 / math.sqrt(5.0)),
    )
    require(all(abs(eval_output[i][j] - expected_eval[i][j]) < 1e-15 for i in range(3) for j in range(3)), "NN wave-I eval path drifted")

    group = columns[0]
    xhat = bn_columns[0]
    seed = (1.0, 0.0, 0.0)
    seed_mean = sum(seed) / 3.0
    radial_mean = sum(g * value for g, value in zip(seed, xhat)) / 3.0
    r = math.sqrt(2.0 / 3.0)
    dx = tuple((g - seed_mean - value * radial_mean) / r for g, value in zip(seed, xhat))
    expected_dx = (a / 6.0, -a / 3.0, a / 6.0)
    require(all(abs(actual - expected) < 1e-15 for actual, expected in zip(dx, expected_dx)), f"NN wave-I VJP drifted: {dx}")
    require(abs(sum(dx)) < 1e-15 and abs(sum(value * grad for value, grad in zip(xhat, dx))) < 1e-15, "NN wave-I VJP invariants drifted")

    wave = {node_id: content for node_id, _, content in nodes if 33 <= node_id <= 36}
    expected_markers = {
        33: ("\\widehat X_{\\mathrm{BN}}", "\\widehat X_{\\mathrm{LN}}"),
        34: ("\\sqrt{32/5}", "\\bar{\\boldsymbol q}'"),
        35: ("0.204", "d\\gamma=-a"),
        36: ("一个 token 的三个 features", "\\frac a6,-\\frac a3,\\frac a6"),
    }
    for node_id, markers in expected_markers.items():
        require(all(marker in wave[node_id] for marker in markers), f"NN-{node_id:02d}: wave-I numeric/axis closure missing")
    print("PASS NN wave-I independent math: BN/LN axes; biased/unbiased state; train/eval split; dense normalization VJP exact")


def audit_wave_j_fixture(nodes: list[tuple[int, Path, str]]) -> None:
    """Recompute the NN-37--40 RMS/group/placement/distributed continuation."""
    x = (
        (1.0, 2.0, 3.0),
        (2.0, 4.0, 6.0),
        (3.0, 6.0, 9.0),
    )
    a = math.sqrt(3.0 / 2.0)
    b = math.sqrt(3.0 / 14.0)

    rms_rows = tuple(
        tuple(value / math.sqrt(sum(entry * entry for entry in row) / 3.0) for value in row)
        for row in x
    )
    expected_rms = tuple((b, 2.0 * b, 3.0 * b) for _ in range(3))
    require(all(abs(rms_rows[i][j] - expected_rms[i][j]) < 1e-15 for i in range(3) for j in range(3)), "NN wave-J RMS forward drifted")
    xhat = rms_rows[0]
    seed = (1.0, 0.0, 0.0)
    radial_mean = sum(g * value for g, value in zip(seed, xhat)) / 3.0
    rms_dx = tuple(b * (g - value * radial_mean) for g, value in zip(seed, xhat))
    expected_rms_dx = (13.0 * b / 14.0, -b / 7.0, -3.0 * b / 14.0)
    require(all(abs(actual - expected) < 1e-15 for actual, expected in zip(rms_dx, expected_rms_dx)), f"NN wave-J RMS VJP drifted: {rms_dx}")
    require(abs(sum(value * grad for value, grad in zip(xhat, rms_dx))) < 1e-15, "NN wave-J RMS radial invariant drifted")
    require(abs(sum(rms_dx) - 4.0 * b / 7.0) < 1e-15, "NN wave-J RMS gradient-sum contrast drifted")

    flat = tuple(value for row in x for value in row)
    gn_mean = sum(flat) / 9.0
    gn_variance = sum((value - gn_mean) ** 2 for value in flat) / 9.0
    require(gn_mean == 4.0 and abs(gn_variance - 52.0 / 9.0) < 1e-15, "NN wave-J GN statistics drifted")
    gn = tuple((value - gn_mean) / math.sqrt(gn_variance) for value in flat)
    require(abs(sum(gn)) < 1e-15 and abs(sum(value * value for value in gn) / 9.0 - 1.0) < 1e-15, "NN wave-J GN normalization drifted")
    v = (1.0, 2.0, 3.0)
    v_norm = math.sqrt(14.0)
    h = (1.0, 0.0, 0.0)
    dg = sum(h_i * v_i / v_norm for h_i, v_i in zip(h, v))
    dv = tuple(h_i - v_i / 14.0 for h_i, v_i in zip(h, v))
    require(abs(dg - 1.0 / v_norm) < 1e-15 and dv == (13.0 / 14.0, -1.0 / 7.0, -3.0 / 14.0), "NN wave-J WeightNorm VJP drifted")
    require(abs(sum(v_i * dv_i for v_i, dv_i in zip(v, dv))) < 1e-15, "NN wave-J WeightNorm tangent invariant drifted")

    tangent = (1.0, -2.0, 1.0)
    jn = tuple(tuple(a * tangent[i] * tangent[j] / 6.0 for j in range(3)) for i in range(3))

    def mv(matrix: tuple[tuple[float, ...], ...], vector: tuple[float, ...]) -> tuple[float, ...]:
        return tuple(sum(matrix[i][j] * vector[j] for j in range(3)) for i in range(3))

    ones = (1.0, 1.0, 1.0)
    require(all(abs(value) < 1e-15 for value in mv(jn, ones)), "NN wave-J LayerNorm shift null direction drifted")
    require(all(abs(actual - a * expected) < 1e-15 for actual, expected in zip(mv(jn, tangent), tangent)), "NN wave-J LayerNorm tangent gain drifted")
    pre_shift = tuple(ones[i] + 0.5 * mv(jn, ones)[i] for i in range(3))
    post_shift = tuple(1.5 * value for value in mv(jn, ones))
    require(pre_shift == ones and all(abs(value) < 1e-15 for value in post_shift), "NN wave-J Pre/Post identity-rail contrast drifted")

    mean_a = (1.5, 3.0, 4.5)
    m2_a = (0.5, 2.0, 4.5)
    mean_b = (3.0, 6.0, 9.0)
    delta = tuple(mean_b[i] - mean_a[i] for i in range(3))
    merged_mean = tuple(mean_a[i] + delta[i] / 3.0 for i in range(3))
    merged_m2 = tuple(m2_a[i] + delta[i] * delta[i] * 2.0 / 3.0 for i in range(3))
    merged_variance = tuple(value / 3.0 for value in merged_m2)
    require(merged_mean == (2.0, 4.0, 6.0), f"NN wave-J distributed mean drifted: {merged_mean}")
    require(merged_m2 == (2.0, 8.0, 18.0), f"NN wave-J distributed M2 drifted: {merged_m2}")
    require(all(abs(actual - expected) < 1e-15 for actual, expected in zip(merged_variance, (2.0 / 3.0, 8.0 / 3.0, 6.0))), "NN wave-J distributed variance drifted")
    sync_first = tuple((x[0][j] - merged_mean[j]) / math.sqrt(merged_variance[j]) for j in range(3))
    require(all(abs(value + a) < 1e-15 for value in sync_first), "NN wave-J suffix-dependent first-token output drifted")

    wave = {node_id: content for node_id, _, content in nodes if 37 <= node_id <= 40}
    expected_markers = {
        37: ("\\frac{4b}{7}\\ne0", "\\widehat X_{\\mathrm{RMS}}"),
        38: ("\\frac{52}{9}", "\\boldsymbol v^{\\mathsf T}d\\boldsymbol v=0"),
        39: ("J_{\\mathrm{pre}}\\boldsymbol1=\\boldsymbol1", "(1,-2,1)"),
        40: ("(2,8,18)", "prefix invariance"),
    }
    for node_id, markers in expected_markers.items():
        require(all(marker in wave[node_id] for marker in markers), f"NN-{node_id:02d}: wave-J numeric/system closure missing")
    print("PASS NN wave-J independent math: RMS VJP; IN/GN/WN objects; Pre/Post rails; distributed M2 and causal-axis contrast exact")


def audit_wave_k_fixture(nodes: list[tuple[int, Path, str]]) -> None:
    """Recompute the NN-41--44 residual/Jacobian/Euler/scaling chain."""
    eigenvalues = (0.2, -2.0)
    horizon = 1.0
    depth = 4
    step = horizon / depth
    branch = tuple(step * value for value in eigenvalues)
    multiplier = tuple(1.0 + value for value in branch)
    require(branch == (0.05, -0.5) and multiplier == (1.05, 0.5), "NN wave-K residual block drifted")

    states = [(1.0, 1.0)]
    increments: list[tuple[float, float]] = []
    for _ in range(depth):
        current = states[-1]
        increment = tuple(branch[i] * current[i] for i in range(2))
        increments.append(increment)
        states.append(tuple(current[i] + increment[i] for i in range(2)))
    expected_states = (
        (1.0, 1.0),
        (21.0 / 20.0, 1.0 / 2.0),
        (441.0 / 400.0, 1.0 / 4.0),
        (9261.0 / 8000.0, 1.0 / 8.0),
        (194481.0 / 160000.0, 1.0 / 16.0),
    )
    require(all(abs(states[k][i] - expected_states[k][i]) < 1e-15 for k in range(5) for i in range(2)), f"NN wave-K state trace drifted: {states}")
    increment_sum = tuple(sum(increment[i] for increment in increments) for i in range(2))
    require(all(abs(actual - expected) < 1e-15 for actual, expected in zip(increment_sum, (34481.0 / 160000.0, -15.0 / 16.0))), "NN wave-K residual sum drifted")

    seed = (1.0, -1.0)
    branch_vjp = tuple(branch[i] * seed[i] for i in range(2))
    one_vjp = tuple(seed[i] + branch_vjp[i] for i in range(2))
    four_vjp = tuple(multiplier[i] ** depth * seed[i] for i in range(2))
    require(branch_vjp == (0.05, 0.5) and one_vjp == (1.05, -0.5), "NN wave-K one-block VJP drifted")
    require(all(abs(actual - expected) < 1e-15 for actual, expected in zip(four_vjp, (194481.0 / 160000.0, -1.0 / 16.0))), "NN wave-K four-block VJP drifted")

    euler: dict[int, tuple[float, float]] = {
        count: tuple((1.0 + value / count) ** count for value in eigenvalues)
        for count in (1, 2, 4, 10)
    }
    require(all(abs(actual - expected) < 1e-15 for actual, expected in zip(euler[1], (1.2, -1.0))), "NN wave-K N=1 Euler trace drifted")
    require(all(abs(actual - expected) < 1e-15 for actual, expected in zip(euler[2], (1.21, 0.0))), "NN wave-K N=2 Euler trace drifted")
    require(abs(euler[4][0] - 1.21550625) < 1e-15 and euler[4][1] == 0.0625, "NN wave-K N=4 Euler trace drifted")
    require(abs(euler[10][0] - 1.2189944199947573) < 1e-15 and abs(euler[10][1] - 0.1073741824) < 1e-15, "NN wave-K N=10 Euler trace drifted")
    exact = (math.exp(0.2), math.exp(-2.0))
    require(abs(exact[0] - 1.2214027581601699) < 1e-15 and abs(exact[1] - 0.1353352832366127) < 1e-15, "NN wave-K exact flow drifted")

    lipschitz = 2.0
    depth_budget = depth * step * lipschitz
    product_bound = (1.0 + step * lipschitz) ** depth
    actual_gain = max(abs(value) ** depth for value in multiplier)
    require(depth_budget == 2.0 and product_bound == 5.0625, "NN wave-K deterministic bound drifted")
    require(abs(actual_gain - 1.21550625) < 1e-15 and actual_gain < product_bound < math.exp(depth_budget), "NN wave-K bound-looseness contrast drifted")
    require(abs(2.0 * math.sqrt(16.0) - 8.0) < 1e-15, "NN wave-K sqrt-depth budget drifted")

    wave = {node_id: content for node_id, _, content in nodes if 41 <= node_id <= 44}
    expected_markers = {
        41: ("194481}{160000", "34481}{160000"),
        42: ("194481}{160000", "-\\frac1{16}"),
        43: ("1.21899442", "e^{1/5}"),
        44: ("5.0625", "S_N=2\\sqrt N"),
    }
    for node_id, markers in expected_markers.items():
        require(all(marker in wave[node_id] for marker in markers), f"NN-{node_id:02d}: wave-K numeric/depth closure missing")
    print("PASS NN wave-K independent math: residual state sum; one/four-block VJP; Euler depth refinement; Lipschitz bound looseness exact")


def audit_wave_l_fixture(nodes: list[tuple[int, Path, str]]) -> None:
    """Recompute the NN-45--48 placement/skip/scaling/path evidence chain."""
    branch = (1.0 / 20.0, -1.0 / 2.0)
    multiplier = (21.0 / 20.0, 1.0 / 2.0)
    probe = (1.0, -1.0)
    branch_output = tuple(branch[i] * probe[i] for i in range(2))
    pre_output = tuple(multiplier[i] * probe[i] for i in range(2))
    post_output = (max(pre_output[0], 0.0), max(pre_output[1], 0.0))
    post_jacobian = (multiplier[0], 0.0)
    require(branch_output == (1.0 / 20.0, 1.0 / 2.0), f"NN wave-L branch probe drifted: {branch_output}")
    require(pre_output == (21.0 / 20.0, -1.0 / 2.0) and post_output == (21.0 / 20.0, 0.0), "NN wave-L Pre/Post output contrast drifted")
    require(sum(value != 0.0 for value in multiplier) == 2 and sum(value != 0.0 for value in post_jacobian) == 1, "NN wave-L placement rank contrast drifted")
    upstream = (1.0, 1.0)
    pre_vjp = tuple(multiplier[i] * upstream[i] for i in range(2))
    post_vjp = tuple(post_jacobian[i] * upstream[i] for i in range(2))
    require(pre_vjp == (21.0 / 20.0, 1.0 / 2.0) and post_vjp == (21.0 / 20.0, 0.0), "NN wave-L placement VJP drifted")

    transform_gate = 1.0 / 4.0
    highway_output = tuple(probe[i] + transform_gate * branch_output[i] for i in range(2))
    highway_jacobian = tuple(1.0 + transform_gate * branch[i] for i in range(2))
    concat_output = probe + branch_output
    require(pre_output == (21.0 / 20.0, -1.0 / 2.0), "NN wave-L additive skip drifted")
    require(highway_output == (81.0 / 80.0, -7.0 / 8.0), f"NN wave-L Highway output drifted: {highway_output}")
    require(highway_jacobian == (81.0 / 80.0, 7.0 / 8.0), f"NN wave-L Highway Jacobian drifted: {highway_jacobian}")
    require(concat_output == (1.0, -1.0, 1.0 / 20.0, 1.0 / 2.0) and len(concat_output) == 4, "NN wave-L concatenation object/shape drifted")

    linear_map = (1.0 / 5.0, -2.0)
    residual_direction = tuple(linear_map[i] * probe[i] for i in range(2))
    loss_seed = (1.0, -1.0)
    rezero_gate_gradient = sum(loss_seed[i] * residual_direction[i] for i in range(2))
    rezero_after_sgd = -0.01 * rezero_gate_gradient
    fixup_scale = 4.0 ** (-1.0 / 4.0)
    fixup_branch_amplitude = fixup_scale ** 2
    deepnorm_alpha = 8.0 ** (1.0 / 4.0)
    deepnorm_beta = 32.0 ** (-1.0 / 4.0)
    require(residual_direction == (1.0 / 5.0, 2.0), "NN wave-L ReZero residual direction drifted")
    require(abs(rezero_gate_gradient + 9.0 / 5.0) < 1e-15 and abs(rezero_after_sgd - 0.018) < 1e-15, "NN wave-L ReZero gate update drifted")
    require(abs(fixup_scale - 1.0 / math.sqrt(2.0)) < 1e-15 and abs(fixup_branch_amplitude - 1.0 / 2.0) < 1e-15, "NN wave-L Fixup scale drifted")
    require(abs(deepnorm_alpha - 2.0 ** (3.0 / 4.0)) < 1e-15 and abs(deepnorm_beta - 2.0 ** (-5.0 / 4.0)) < 1e-15, "NN wave-L DeepNorm factors drifted")
    require(abs(deepnorm_alpha * deepnorm_beta - fixup_scale) < 1e-15, "NN wave-L equal-number/different-role comparison drifted")

    positive_terms = (1.0, 1.0 / 5.0, 3.0 / 200.0, 1.0 / 2000.0, 1.0 / 160000.0)
    positive_sum = sum(positive_terms)
    path_probability = 1.0 / 21.0
    path_mean = 4.0 * path_probability
    path_variance = 4.0 * path_probability * (1.0 - path_probability)
    signed_terms = (1.0, -2.0, 3.0 / 2.0, -1.0 / 2.0, 1.0 / 16.0)
    signed_sum = sum(signed_terms)
    signed_absolute_sum = sum(abs(value) for value in signed_terms)
    require(abs(positive_sum - 194481.0 / 160000.0) < 1e-15, "NN wave-L positive path expansion drifted")
    require(abs(path_mean - 4.0 / 21.0) < 1e-15 and abs(path_variance - 80.0 / 441.0) < 1e-15, "NN wave-L normalized path moments drifted")
    require(abs(signed_sum - 1.0 / 16.0) < 1e-15 and signed_absolute_sum == 5.0625, "NN wave-L cancellation witness drifted")

    wave = {node_id: content for node_id, _, content in nodes if 45 <= node_id <= 48}
    expected_markers = {
        45: ("\\operatorname{rank}(J_{\\mathrm{post}})=1", "J_{\\mathrm{post}}=DM"),
        46: ("\\frac{81}{80}", "\\mathbb R^{4\\times2}"),
        47: ("-\\frac95", "\\alpha_{\\mathrm{DN}}\\beta_{\\mathrm{DN}}"),
        48: ("\\frac{80}{441}", "5.0625"),
    }
    for node_id, markers in expected_markers.items():
        require(all(marker in wave[node_id] for marker in markers), f"NN-{node_id:02d}: wave-L numeric/evidence closure missing")
    print("PASS NN wave-L independent math: placement rank/VJP; add/Highway/concat objects; ReZero/Fixup/DeepNorm scales; positive and cancelling path sums exact")


def audit_wave_m_fixture(nodes: list[tuple[int, Path, str]]) -> None:
    """Recompute the NN-49--52 lookup/geometry/tying/Softmax chain."""
    embedding = (
        (1.0, 0.0),
        (0.0, 1.0),
        (2.0, -1.0),
        (-1.0, 3.0),
    )
    indices = (2, 1, 2)
    upstream = ((1.0, 2.0), (-1.0, 0.5), (3.0, -1.0))
    lookup = tuple(embedding[index] for index in indices)
    require(lookup == ((2.0, -1.0), (0.0, 1.0), (2.0, -1.0)), f"NN wave-M lookup trace drifted: {lookup}")
    lookup_gradient = [[0.0, 0.0] for _ in embedding]
    for index, row_gradient in zip(indices, upstream):
        for coordinate in range(2):
            lookup_gradient[index][coordinate] += row_gradient[coordinate]
    expected_lookup_gradient = ((0.0, 0.0), (-1.0, 0.5), (4.0, 1.0), (0.0, 0.0))
    require(tuple(map(tuple, lookup_gradient)) == expected_lookup_gradient, f"NN wave-M scatter-add drifted: {lookup_gradient}")

    first, second = embedding[1], embedding[2]
    dot = sum(first[j] * second[j] for j in range(2))
    cosine = dot / math.sqrt(sum(value * value for value in first) * sum(value * value for value in second))
    distance_squared = sum((first[j] - second[j]) ** 2 for j in range(2))
    require(dot == -1.0 and abs(cosine + 1.0 / math.sqrt(5.0)) < 1e-15 and distance_squared == 8.0, "NN wave-M pair geometry drifted")
    mean = tuple(sum(row[j] for row in embedding) / 4.0 for j in range(2))
    covariance = tuple(
        tuple(sum((row[i] - mean[i]) * (row[j] - mean[j]) for row in embedding) / 4.0 for j in range(2))
        for i in range(2)
    )
    require(mean == (0.5, 0.75) and covariance == ((5.0 / 4.0, -13.0 / 8.0), (-13.0 / 8.0, 35.0 / 16.0)), f"NN wave-M embedding covariance drifted: {mean}, {covariance}")
    trace = covariance[0][0] + covariance[1][1]
    determinant = covariance[0][0] * covariance[1][1] - covariance[0][1] * covariance[1][0]
    discriminant = math.sqrt(trace * trace - 4.0 * determinant)
    eigenvalues = ((trace + discriminant) / 2.0, (trace - discriminant) / 2.0)
    participation_ratio = trace * trace / (trace * trace - 2.0 * determinant)
    require(trace == 55.0 / 16.0 and determinant == 3.0 / 32.0, "NN wave-M covariance invariants drifted")
    require(abs(eigenvalues[0] - 3.410007390966851) < 1e-15 and abs(eigenvalues[1] - 0.027492609033148874) < 1e-15, "NN wave-M covariance spectrum drifted")
    require(abs(participation_ratio - 3025.0 / 2977.0) < 1e-15, "NN wave-M participation ratio drifted")

    hidden = (1.0, 1.0)
    logits = tuple(sum(row[j] * hidden[j] for j in range(2)) for row in embedding)
    require(logits == (1.0, 1.0, 1.0, 2.0), f"NN wave-M tied logits drifted: {logits}")
    denominator = 3.0 + math.e
    probabilities = (1.0 / denominator, 1.0 / denominator, 1.0 / denominator, math.e / denominator)
    logit_gradient = probabilities[:3] + (probabilities[3] - 1.0,)
    require(abs(sum(probabilities) - 1.0) < 1e-15 and abs(sum(logit_gradient)) < 1e-15, "NN wave-M Softmax normalization/gauge drifted")
    require(all(abs(actual - expected) < 1e-15 for actual, expected in zip(logit_gradient, (1.0 / denominator, 1.0 / denominator, 1.0 / denominator, -3.0 / denominator))), "NN wave-M logit gradient drifted")
    output_gradient = tuple(tuple(value * coordinate for coordinate in hidden) for value in logit_gradient)
    total_gradient = tuple(
        tuple(expected_lookup_gradient[i][j] + output_gradient[i][j] for j in range(2))
        for i in range(4)
    )
    require(all(abs(total_gradient[0][j] - 1.0 / denominator) < 1e-15 for j in range(2)), "NN wave-M tied unlooked row-0 gradient drifted")
    require(all(abs(total_gradient[3][j] + 3.0 / denominator) < 1e-15 for j in range(2)), "NN wave-M tied unlooked row-3 gradient drifted")

    nll_one = math.log(denominator) - 1.0
    denominator_two = 3.0 + math.sqrt(math.e)
    probabilities_two = (1.0 / denominator_two,) * 3 + (math.sqrt(math.e) / denominator_two,)
    nll_two = math.log(denominator_two) - 0.5
    gradient_two = tuple((probabilities_two[i] - (1.0 if i == 3 else 0.0)) / 2.0 for i in range(4))
    require(abs(nll_one - 0.743668380628679) < 1e-15 and abs(nll_two - 1.0365921862326961) < 1e-15, "NN wave-M temperature NLL drifted")
    require(probabilities_two[3] < probabilities[3] and abs(sum(gradient_two)) < 1e-15, "NN wave-M temperature/gauge contrast drifted")
    require(all(abs(actual - expected) < 1e-15 for actual, expected in zip(gradient_two, (1.0 / (2.0 * denominator_two),) * 3 + (-3.0 / (2.0 * denominator_two),))), "NN wave-M tau=2 gradient drifted")

    wave = {node_id: content for node_id, _, content in nodes if 49 <= node_id <= 52}
    expected_markers = {
        49: ("S^{\\mathsf T}G", "4&1"),
        50: ("\\sqrt{2929}", "\\frac{3025}{2977}"),
        51: ("\\frac1D(1,1,1,-3)", "-3D^{-1}"),
        52: ("\\log D-1\\approx0.743668", "\\log D_2-\\frac12\\approx1.036592"),
    }
    for node_id, markers in expected_markers.items():
        require(all(marker in wave[node_id] for marker in markers), f"NN-{node_id:02d}: wave-M numeric/probability closure missing")
    print("PASS NN wave-M independent math: lookup/scatter-add; row geometry/covariance spectrum; tied use-site sum; temperature Softmax/NLL exact")


def audit_wave_n_fixture(nodes: list[tuple[int, Path, str]]) -> None:
    """Recompute the NN-53--56 rank/sampling/mask/compression chain."""
    vocabulary = 4
    log_ratio = math.log(7.0)
    centering = tuple(
        tuple((1.0 if i == j else 0.0) - 1.0 / vocabulary for j in range(vocabulary))
        for i in range(vocabulary)
    )
    target_log_probability = tuple(
        tuple(math.log(0.7 if i == j else 0.1) for j in range(vocabulary))
        for i in range(vocabulary)
    )

    def mm(left: tuple[tuple[float, ...], ...], right: tuple[tuple[float, ...], ...]) -> tuple[tuple[float, ...], ...]:
        return tuple(
            tuple(sum(left[i][k] * right[k][j] for k in range(len(right))) for j in range(len(right[0])))
            for i in range(len(left))
        )

    centered_target = mm(mm(centering, target_log_probability), centering)
    require(all(abs(centered_target[i][j] - log_ratio * centering[i][j]) < 1e-15 for i in range(4) for j in range(4)), "NN wave-N centered log-ratio target drifted")
    require(all(abs(sum(row)) < 1e-15 for row in centered_target), "NN wave-N vocabulary gauge did not cancel")
    require(abs(sum(centered_target[i][i] for i in range(4)) - 3.0 * log_ratio) < 1e-15, "NN wave-N rank-three trace drifted")
    best_rank_two_error_squared = log_ratio ** 2
    require(abs(best_rank_two_error_squared - 3.7865663081964716) < 1e-15, "NN wave-N rank-two residual drifted")

    partition = 3.0 * math.e + math.e ** 2
    estimator_common = 4.0 * math.e
    estimator_target = 4.0 * math.e ** 2
    expected_partition = 0.75 * estimator_common + 0.25 * estimator_target
    expected_log_partition = 0.75 * math.log(estimator_common) + 0.25 * math.log(estimator_target)
    exact_log_partition = math.log(partition)
    jensen_gap = exact_log_partition - expected_log_partition
    require(abs(expected_partition - partition) < 1e-15, "NN wave-N importance partition unbiasedness drifted")
    require(abs(expected_log_partition - (math.log(4.0) + 1.25)) < 1e-15, "NN wave-N expected log partition drifted")
    require(abs(jensen_gap - 0.10737401950878844) < 1e-15 and jensen_gap > 0.0, "NN wave-N Jensen gap drifted")
    require(abs((expected_log_partition - 2.0) - 0.6362943611198906) < 1e-15, "NN wave-N sampled plug-in NLL drifted")

    loss = (0.2, 0.4, 0.6, 9.0)
    valid = (1.0, 1.0, 1.0, 0.0)
    masked_mean = sum(m * value for m, value in zip(valid, loss)) / sum(valid)
    require(abs(masked_mean - 0.4) < 1e-15, "NN wave-N ignored-token denominator drifted")
    attention = tuple(
        tuple(int(t < 3 and s < 3 and s <= t) for s in range(4))
        for t in range(4)
    )
    require(attention == ((1, 0, 0, 0), (1, 1, 0, 0), (1, 1, 1, 0), (0, 0, 0, 0)), f"NN wave-N mask edge matrix drifted: {attention}")
    tied_pad_output_gradient = 1.0 / (3.0 + math.e)
    require(tied_pad_output_gradient > 0.0, "NN wave-N tied PAD output gradient vanished")

    gram = ((6.0, -5.0), (-5.0, 11.0))
    discriminant = math.sqrt((gram[0][0] + gram[1][1]) ** 2 - 4.0 * (gram[0][0] * gram[1][1] - gram[0][1] * gram[1][0]))
    squared_singular_values = ((17.0 + discriminant) / 2.0, (17.0 - discriminant) / 2.0)
    require(abs(discriminant - 5.0 * math.sqrt(5.0)) < 1e-15, "NN wave-N embedding Gram discriminant drifted")
    require(abs(squared_singular_values[1] - 2.9098300562505255) < 1e-15, "NN wave-N rank-one residual drifted")
    require(4 * 2 == 8 and 4 * 1 + 1 * 2 == 6, "NN wave-N factorized parameter count drifted")
    original_row = (2.0, -1.0)
    quantized_row = (9.0 / 4.0, -3.0 / 4.0)
    quantization_error = tuple(quantized_row[j] - original_row[j] for j in range(2))
    hidden = (1.0, 1.0)
    logit_error = abs(sum(quantization_error[j] * hidden[j] for j in range(2)))
    cauchy_bound = math.sqrt(sum(value * value for value in quantization_error)) * math.sqrt(2.0)
    require(quantization_error == (0.25, 0.25) and logit_error == 0.5 and abs(cauchy_bound - 0.5) < 1e-15, "NN wave-N quantized tied-logit bound drifted")

    wave = {node_id: content for node_id, _, content in nodes if 53 <= node_id <= 56}
    expected_markers = {
        53: ("(\\log7)C_4", "(\\log7)^2"),
        54: ("\\log4+\\frac54", "0.107374"),
        55: ("\\frac{0.2+0.4+0.6}{3}", "D^{-1}(1,1)\\ne0"),
        56: ("\\frac{17-5\\sqrt5}{2}", "\\frac{\\sqrt2}{4}\\sqrt2"),
    }
    for node_id, markers in expected_markers.items():
        require(all(marker in wave[node_id] for marker in markers), f"NN-{node_id:02d}: wave-N rank/sampling/mask/compression closure missing")
    print("PASS NN wave-N independent math: centered rank obstruction; unbiased-Z/log bias; mask denominator/edges; rank-one and quantized-logit errors exact")


def audit_wave_o_fixture(nodes: list[tuple[int, Path, str]]) -> None:
    """Recompute the NN-57--60 activation/connection/path-noise chain."""
    x = (2.0, 1.0)
    keep = 0.5
    masks = ((0, 0), (1, 0), (0, 1), (1, 1))
    dropout_outputs = tuple(tuple(mask[j] / keep * x[j] for j in range(2)) for mask in masks)
    require(dropout_outputs == ((0.0, 0.0), (4.0, 0.0), (0.0, 2.0), (4.0, 2.0)), f"NN wave-O dropout enumeration drifted: {dropout_outputs}")
    mean = tuple(sum(output[j] for output in dropout_outputs) / 4.0 for j in range(2))
    variance = tuple(sum((output[j] - mean[j]) ** 2 for output in dropout_outputs) / 4.0 for j in range(2))
    expected_energy = sum(sum(value * value for value in output) for output in dropout_outputs) / 4.0
    require(mean == x and variance == (4.0, 1.0) and expected_energy == 10.0, "NN wave-O dropout moment ledger drifted")
    realization = (1.0, 0.0)
    upstream = (1.0, -2.0)
    vjp = tuple(realization[j] / keep * upstream[j] for j in range(2))
    require(vjp == (2.0, 0.0), "NN wave-O fixed-realization VJP drifted")

    weight = ((1.0, 2.0), (-1.0, 1.0))
    scores = tuple(tuple(sum(weight[i][j] * output[j] for j in range(2)) for i in range(2)) for output in dropout_outputs)
    score_mean = tuple(sum(score[i] for score in scores) / 4.0 for i in range(2))
    score_covariance = tuple(
        tuple(sum((score[i] - score_mean[i]) * (score[j] - score_mean[j]) for score in scores) / 4.0 for j in range(2))
        for i in range(2)
    )
    require(score_mean == (4.0, -1.0) and score_covariance == ((8.0, -2.0), (-2.0, 5.0)), f"NN wave-O activation score covariance drifted: {score_mean}, {score_covariance}")
    target = 3.0
    expected_squared_loss = sum((target - score[0]) ** 2 for score in scores) / 4.0
    require(expected_squared_loss == 9.0 and (target - score_mean[0]) ** 2 + score_covariance[0][0] == 9.0, "NN wave-O exact noisy square-risk identity drifted")

    dropconnect_covariance = ((8.0, 0.0), (0.0, 5.0))
    determinant_activation = score_covariance[0][0] * score_covariance[1][1] - score_covariance[0][1] * score_covariance[1][0]
    determinant_dropconnect = dropconnect_covariance[0][0] * dropconnect_covariance[1][1]
    require(determinant_activation == 36.0 and determinant_dropconnect == 40.0, "NN wave-O noise-location determinant contrast drifted")

    branch = tuple(sum(weight[i][j] * x[j] for j in range(2)) for i in range(2))
    dropped_state = x
    kept_state = tuple(x[i] + branch[i] / keep for i in range(2))
    expected_state = tuple(0.5 * dropped_state[i] + 0.5 * kept_state[i] for i in range(2))
    require(branch == (4.0, -1.0) and kept_state == (10.0, -1.0) and expected_state == (6.0, 0.0), "NN wave-O DropPath state contrast drifted")
    identity = ((1.0, 0.0), (0.0, 1.0))
    kept_jacobian = tuple(tuple(identity[i][j] + weight[i][j] / keep for j in range(2)) for i in range(2))
    expected_jacobian = tuple(tuple(0.5 * identity[i][j] + 0.5 * kept_jacobian[i][j] for j in range(2)) for i in range(2))
    require(kept_jacobian == ((3.0, 4.0), (-2.0, 3.0)) and expected_jacobian == ((2.0, 2.0), (-1.0, 2.0)), "NN wave-O DropPath Jacobian expectation drifted")
    branch_covariance = tuple(tuple(branch[i] * branch[j] for j in range(2)) for i in range(2))
    require(branch_covariance == ((16.0, -4.0), (-4.0, 1.0)), "NN wave-O branch covariance drifted")
    survival = (0.875, 0.75, 0.625, 0.5)
    active_mean = sum(survival)
    active_variance = sum(probability * (1.0 - probability) for probability in survival)
    require(active_mean == 2.75 and active_variance == 0.78125, "NN wave-O active-depth moments drifted")

    wave = {node_id: content for node_id, _, content in nodes if 57 <= node_id <= 60}
    expected_markers = {
        57: ("\\mathbb E\\|Y\\|_2^2=\\frac1q\\|x\\|_2^2=10", "\\bar x=\\frac mq\\odot g=(2,0)"),
        58: ("\\operatorname{Cov}(u,v\\mid x)=-2", "1+8=9"),
        59: ("\\det\\Sigma_{\\mathrm{act}}=36", "\\det\\Sigma_{\\mathrm{dc}}=40"),
        60: ("x^+_{\\mathrm{keep}}", "0.78125"),
    }
    for node_id, markers in expected_markers.items():
        require(all(marker in wave[node_id] for marker in markers), f"NN-{node_id:02d}: wave-O stochastic-location closure missing")
    print("PASS NN wave-O independent math: Dropout moments/VJP; score covariance/risk; DropConnect joint-law contrast; DropPath state/Jacobian/depth exact")


def audit_wave_p_fixture(nodes: list[tuple[int, Path, str]]) -> None:
    """Recompute the NN-61--64 target/interpolation/derivative/interaction chain."""
    epsilon = 0.1
    classes = 3
    prediction = (0.8, 0.1, 0.1)
    hard_target = (1.0, 0.0, 0.0)
    prior = (1.0 / classes,) * classes
    smooth_target = tuple((1.0 - epsilon) * hard_target[i] + epsilon * prior[i] for i in range(classes))
    expected_target = (14.0 / 15.0, 1.0 / 30.0, 1.0 / 30.0)
    require(all(abs(actual - expected) < 1e-15 for actual, expected in zip(smooth_target, expected_target)), "NN wave-P smoothed target drifted")
    gradient = tuple(prediction[i] - smooth_target[i] for i in range(classes))
    expected_gradient = (-2.0 / 15.0, 1.0 / 15.0, 1.0 / 15.0)
    require(all(abs(actual - expected) < 1e-15 for actual, expected in zip(gradient, expected_gradient)), "NN wave-P smoothed gradient drifted")
    require(abs(sum(gradient)) < 1e-15 and abs(math.log(smooth_target[0] / smooth_target[1]) - math.log(28.0)) < 1e-15, "NN wave-P gradient gauge/margin drifted")

    x_a = (2.0, 1.0)
    x_b = (-2.0, 1.0)
    y_a = (1.0, 0.0, 0.0)
    y_b = (0.0, 1.0, 0.0)
    mixture = 0.25
    mixed_x = tuple(mixture * x_a[i] + (1.0 - mixture) * x_b[i] for i in range(2))
    mixed_y = tuple(mixture * y_a[i] + (1.0 - mixture) * y_b[i] for i in range(classes))
    smooth_after_mix = tuple((1.0 - epsilon) * mixed_y[i] + epsilon * prior[i] for i in range(classes))
    smooth_a = tuple((1.0 - epsilon) * y_a[i] + epsilon * prior[i] for i in range(classes))
    smooth_b = tuple((1.0 - epsilon) * y_b[i] + epsilon * prior[i] for i in range(classes))
    mix_after_smooth = tuple(mixture * smooth_a[i] + (1.0 - mixture) * smooth_b[i] for i in range(classes))
    expected_mixed_smooth = (31.0 / 120.0, 85.0 / 120.0, 4.0 / 120.0)
    require(mixed_x == (-1.0, 1.0) and mixed_y == (0.25, 0.75, 0.0), "NN wave-P Mixup chord drifted")
    require(all(abs(actual - expected) < 1e-15 for actual, expected in zip(smooth_after_mix, expected_mixed_smooth)), "NN wave-P smoothed Mixup target drifted")
    require(all(abs(left - right) < 1e-15 for left, right in zip(smooth_after_mix, mix_after_smooth)), "NN wave-P target affine commutation drifted")

    weight = ((1.0, 2.0), (-1.0, 1.0))
    gram = (
        (sum(weight[k][0] * weight[k][0] for k in range(2)), sum(weight[k][0] * weight[k][1] for k in range(2))),
        (sum(weight[k][1] * weight[k][0] for k in range(2)), sum(weight[k][1] * weight[k][1] for k in range(2))),
    )
    require(gram == ((2.0, 1.0), (1.0, 5.0)), f"NN wave-P Jacobian Gram drifted: {gram}")
    eigenvalues = ((7.0 + math.sqrt(13.0)) / 2.0, (7.0 - math.sqrt(13.0)) / 2.0)
    operator_squared = eigenvalues[0]
    frobenius_squared = sum(value * value for row in weight for value in row)
    require(abs(operator_squared - 5.302775637731995) < 1e-15 and frobenius_squared == 7.0, "NN wave-P Jacobian norms drifted")
    probes = ((1.0, 1.0), (1.0, -1.0))
    vjps = tuple(tuple(sum(weight[i][j] * probe[i] for i in range(2)) for j in range(2)) for probe in probes)
    probe_energies = tuple(sum(value * value for value in vjp) for vjp in vjps)
    require(vjps == ((0.0, 3.0), (2.0, 1.0)) and probe_energies == (9.0, 5.0), "NN wave-P Hutchinson probes drifted")
    require(sum(probe_energies) / 2.0 == frobenius_squared, "NN wave-P Hutchinson expectation drifted")

    risks = {(0, 0): 0.30, (1, 0): 0.26, (0, 1): 0.27, (1, 1): 0.20}
    interaction = (risks[1, 1] - risks[1, 0]) - (risks[0, 1] - risks[0, 0])
    require(abs(interaction + 0.03) < 1e-15, f"NN wave-P factorial interaction drifted: {interaction}")

    wave = {node_id: content for node_id, _, content in nodes if 61 <= node_id <= 64}
    expected_markers = {
        61: ("\\left(-\\frac2{15},\\frac1{15},\\frac1{15}\\right)", "\\log28"),
        62: ("\\widetilde x=(-1,1)", "\\frac{31}{120}"),
        63: ("\\frac{7+\\sqrt{13}}2", "\\frac{9+5}{2}=7"),
        64: ("\\Delta_{AB}", "-0.06-(-0.03)=-0.03"),
    }
    for node_id, markers in expected_markers.items():
        require(all(marker in wave[node_id] for marker in markers), f"NN-{node_id:02d}: wave-P target/interpolation/derivative/interaction closure missing")
    print("PASS NN wave-P independent math: smoothed target/gradient/margin; affine target commutation; Jacobian norms/probes; factorial interaction exact")


def question_ids(content: str) -> list[str]:
    return re.findall(r"^###\s+([^\s]+-[A-E]\d{2})\s*$", content, re.M)


def audit_exercises(nodes: list[tuple[int, Path, str]], index: dict[str, list[Path]]) -> None:
    seen_exercises: set[Path] = set()
    seen_solutions: set[Path] = set()
    all_ids: list[str] = []
    for node_id, node_path, node in nodes:
        exercise_paths = resolve(frontmatter_targets(node, "exercises")[0], index)
        solution_paths = resolve(frontmatter_targets(node, "solutions")[0], index)
        require(len(exercise_paths) == len(solution_paths) == 1, f"NN-{node_id:02d}: exercise/solution missing or ambiguous")
        exercise_path, solution_path = exercise_paths[0], solution_paths[0]
        require(exercise_path.parent == EXERCISES and solution_path.parent == SOLUTIONS, f"NN-{node_id:02d}: support file outside lab")
        require(exercise_path not in seen_exercises and solution_path not in seen_solutions, f"NN-{node_id:02d}: support file reused")
        seen_exercises.add(exercise_path)
        seen_solutions.add(solution_path)
        exercise, solution = read(exercise_path), read(solution_path)
        require(frontmatter_line(exercise, "type") == "exercise" and frontmatter_line(solution, "type") == "solution", f"NN-{node_id:02d}: support type mismatch")
        require(frontmatter_line(exercise, "status") == frontmatter_line(solution, "status") == "draft", f"NN-{node_id:02d}: learner state changed")
        require(node_path.stem in frontmatter_targets(exercise, "topic"), f"NN-{node_id:02d}: exercise topic backlink missing")
        require(node_path.stem in frontmatter_targets(solution, "topic"), f"NN-{node_id:02d}: solution topic backlink missing")
        require(solution_path.stem in frontmatter_targets(exercise, "solution"), f"NN-{node_id:02d}: exercise solution link missing")
        require(exercise_path.stem in frontmatter_targets(solution, "exercise"), f"NN-{node_id:02d}: solution exercise link missing")
        exercise_ids, solution_ids = question_ids(exercise), question_ids(solution)
        require(exercise_ids == solution_ids, f"NN-{node_id:02d}: question/solution order differs")
        require(len(exercise_ids) == len(set(exercise_ids)) == 15, f"NN-{node_id:02d}: expected 15 unique A--E questions")
        require(Counter(identifier.rsplit("-", 1)[-1][0] for identifier in exercise_ids) == Counter({level: 3 for level in "ABCDE"}), f"NN-{node_id:02d}: A--E distribution changed")
        all_ids.extend(exercise_ids)
    require(len(seen_exercises) == len(seen_solutions) == 64, "NN support-file count changed")
    require(len(all_ids) == len(set(all_ids)) == 960, "NN global question total/uniqueness changed")
    print("PASS NN exercises and solutions: 64/64 bijections; 960/960 A--E IDs")


def audit_sources_and_links(nodes: list[tuple[int, Path, str]], index: dict[str, list[Path]]) -> None:
    source_targets = sorted({target for _, _, content in nodes for target in frontmatter_targets(content, "sources")})
    migrated_source_targets = {target for node_id, _, content in nodes if node_id in MIGRATED_IDS for target in frontmatter_targets(content, "sources")}
    status_counts: Counter[str] = Counter()
    legacy_metadata_gaps: list[str] = []
    migrated_tiers: dict[str, str] = {}
    for target in source_targets:
        paths = resolve(target, index)
        require(len(paths) == 1 and paths[0].parent.name == "_sources", f"source missing/ambiguous/not a card: {target}")
        source = read(paths[0])
        status = frontmatter_line(source, "status")
        require(status in {"active", "verified", "draft"}, f"unsupported source status: {target} -> {status}")
        status_counts[status] += 1
        missing_keys = [key for key in SOURCE_KEYS if not frontmatter_line(source, key)]
        if target in migrated_source_targets:
            require(not missing_keys, f"migrated-wave source metadata incomplete: {target} -> {missing_keys}")
            tier = frontmatter_line(source, "source_tier")
            require(tier in {"A", "B", "C"}, f"migrated-wave source tier unsupported: {target} -> {tier}")
            migrated_tiers[target] = tier
            if tier in {"A", "B"}:
                require(status in {"active", "verified"}, f"migrated-wave A/B source not active/verified: {target}")
            else:
                require(status in {"draft", "active", "verified"}, f"migrated-wave C source status unsupported: {target}")
        elif missing_keys:
            legacy_metadata_gaps.extend(f"{target}:{key}" for key in missing_keys)

    for node_id, _, content in nodes:
        if node_id not in MIGRATED_IDS:
            continue
        tiers = {migrated_tiers[target] for target in frontmatter_targets(content, "sources")}
        require(tiers & {"A", "B"}, f"NN-{node_id:02d}: migrated node lacks an A/B source anchor")

    missing: list[str] = []
    ambiguous: list[str] = []
    link_count = 0
    for path in sorted(CHAPTER.rglob("*.md")):
        for target in wiki_targets(read(path), embeds=False):
            link_count += 1
            candidates = resolve(target, index)
            if not candidates:
                missing.append(f"{path.relative_to(ROOT)} -> {target}")
            elif len(candidates) > 1:
                ambiguous.append(f"{path.relative_to(ROOT)} -> {target}")
    require(not missing, f"missing NN Wiki links: {missing[:20]}")
    require(not ambiguous, f"ambiguous NN Wiki links: {ambiguous[:20]}")
    print(
        f"PASS NN sources/links: cards={len(source_targets)} {dict(sorted(status_counts.items()))}; "
        f"migrated-wave metadata complete with per-node A/B anchors; legacy metadata fields pending={len(legacy_metadata_gaps)}; scoped Wiki links={link_count}"
    )


def audit_figures(nodes: list[tuple[int, Path, str]], index: dict[str, list[Path]]) -> None:
    assets: set[Path] = set()
    scripts: set[str] = set()
    embed_count = 0
    for _, path, content in nodes:
        embeds = wiki_targets(content, embeds=True)
        require(len(embeds) == 1, f"{path.relative_to(ROOT)}: expected exactly one formal visual")
        target = embeds[0]
        embed_count += 1
        require(target.startswith("00-知识库管理/_assets/figures/neural-networks/"), f"unstable NN image target: {target}")
        candidates = resolve(target, index)
        require(len(candidates) == 1 and candidates[0].suffix.lower() in IMAGE_EXTENSIONS, f"NN image missing/ambiguous: {target}")
        asset = candidates[0]
        assets.add(asset)
        if asset.suffix.lower() == ".svg":
            root = ET.parse(asset).getroot()
            require(root.tag.endswith("svg") and "viewBox" in root.attrib, f"invalid NN SVG: {target}")
        for link in wiki_targets(content, embeds=False):
            if link.endswith(".py") and "plot_" in link:
                scripts.add(Path(link).name)
    require(embed_count == len(assets) == 64, f"NN node figure inventory changed: embeds={embed_count}, assets={len(assets)}")
    require(scripts == EXPECTED_FIGURE_SCRIPTS, f"NN figure script set changed: {sorted(scripts)}")
    for script in scripts:
        require((CODE / script).is_file(), f"missing NN figure script: {script}")

    result = subprocess.run(["node", str(FIGURE_AUDITOR), str(ROOT), "--json"], cwd=ROOT, text=True, capture_output=True)
    require(result.returncode == 0, f"figure-unit auditor failed:\n{result.stderr}")
    payload = json.loads(result.stdout)
    records = [record for record in payload["records"] if record["file"].startswith("30-神经网络基础/")]
    require(len(records) == 64 and all(record["pass"] for record in records), f"NN figure-unit contract changed: {records}")
    print("PASS NN figures: node embeds/assets=64/64; chapter figure units=64/64; SVG/XML=64; scripts=16")


def audit_curriculum(nodes: list[tuple[int, Path, str]]) -> None:
    curriculum = read(CHAPTER / "神经网络基础完整课程地图与掌握标准.md")
    mapped = {int(node_id): title for node_id, title in re.findall(r"^\| NN-(\d{2}) \| \[\[([^\]|]+)", curriculum, re.M)}
    require(sorted(mapped) == list(range(1, 65)), "NN curriculum does not map NN-01--64 exactly once")
    for node_id, path, _ in nodes:
        require(mapped[node_id] == path.stem, f"NN curriculum/path mismatch: NN-{node_id:02d}")
    print("PASS NN curriculum: 64/64 ID-title-path mappings; eight-volume scope fixed")


def snapshot_assets() -> dict[str, str]:
    require(ASSET_DIR.is_dir(), "NN figure asset directory missing")
    return {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(ASSET_DIR.rglob("*")) if path.is_file()
    }


def run_figure_scripts() -> None:
    for name in sorted(EXPECTED_FIGURE_SCRIPTS):
        result = subprocess.run([sys.executable, str(CODE / name)], cwd=ROOT, text=True, capture_output=True)
        require(result.returncode == 0, f"NN figure script failed: {name}\n{result.stdout}\n{result.stderr}")


def audit_deterministic_figures() -> None:
    before = snapshot_assets()
    run_figure_scripts()
    first = snapshot_assets()
    run_figure_scripts()
    second = snapshot_assets()
    require(before == first == second, "NN stored figures differ from deterministic double regeneration")
    require(len(before) == 64, f"NN stored figure count changed: {len(before)}")
    print("PASS NN deterministic figures: scripts=16; stored assets=64; double-run byte identity")


def audit_state_surfaces() -> None:
    audit_name = Path(__file__).name
    for path in STATE_SURFACES:
        content = read(path)
        require(audit_name in content, f"state surface misses NN audit: {path.relative_to(ROOT)}")
        migrated_mentions = content.count("64/64") + content.count("64 / 64")
        pending_mentions = content.count("0/64") + content.count("0 / 64")
        require(migrated_mentions >= 1 and pending_mentions >= 1, f"state surface misses NN migrated/pending counts: {path.relative_to(ROOT)}")
        require("8/8" in content or "8 / 8" in content, f"state surface misses NN material-gate count: {path.relative_to(ROOT)}")
        require("not-attempted" in content, f"state surface overclaims NN learner: {path.relative_to(ROOT)}")
    print("PASS NN state surfaces: 5 global + 8 volume views agree on migrated=64/64, pending=0/64, material gates=8/8, learner=not-attempted")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-figures", action="store_true", help="Regenerate all 16 NN figure families twice.")
    args = parser.parse_args()
    nodes = collect_nodes()
    index = build_index()
    audit_scope(nodes)
    audit_migrated_contract(nodes)
    audit_wave_c_fixture(nodes)
    audit_wave_d_fixture(nodes)
    audit_wave_e_fixture(nodes)
    audit_wave_f_fixture(nodes)
    audit_wave_g_fixture(nodes)
    audit_wave_h_fixture(nodes)
    audit_wave_i_fixture(nodes)
    audit_wave_j_fixture(nodes)
    audit_wave_k_fixture(nodes)
    audit_wave_l_fixture(nodes)
    audit_wave_m_fixture(nodes)
    audit_wave_n_fixture(nodes)
    audit_wave_o_fixture(nodes)
    audit_wave_p_fixture(nodes)
    audit_exercises(nodes, index)
    audit_sources_and_links(nodes, index)
    audit_figures(nodes, index)
    audit_curriculum(nodes)
    audit_state_surfaces()
    if args.run_figures:
        audit_deterministic_figures()
    print("NN-01--64 teaching migration regression: PASS; 30.1--30.8 material gates=8/8")
    print("NN-61--64 teaching migration: PASS; cumulative NN-CUM-01 remains legacy composed pending a separate re-audit")
    print("PERSONAL LEARNING STATUS: not-attempted")


if __name__ == "__main__":
    main()

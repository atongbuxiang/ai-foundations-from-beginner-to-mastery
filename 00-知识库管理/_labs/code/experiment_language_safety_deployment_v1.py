#!/usr/bin/env python3
"""Deterministic numerical oracles for LM-65--LM-72."""

from __future__ import annotations

import csv
import hashlib
import html
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_labs" / "experiments" / "lm70.9-safety-deployment-v1"
W, H = 1200, 700
BG, PAPER, INK, MUTED, GRID = "#FBF8F1", "#FFFDF8", "#183044", "#667784", "#D9D5CB"
BLUE, TEAL, AMBER, RED, PURPLE, GREEN = "#245AA8", "#17766E", "#C87922", "#B7443E", "#7054A3", "#4F7B45"


def close(a: float, b: float, tol: float = 1e-10) -> bool:
    return abs(a - b) <= tol


def check(name: str, passed: bool, observed: object, expected: object, note: str) -> dict[str, object]:
    return {"name": name, "passed": bool(passed), "observed": observed, "expected": expected, "note": note}


def svg_begin(title: str, desc: str, accent: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(desc)}</desc>',
        f'<rect width="{W}" height="{H}" fill="{BG}"/>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif}</style>',
        f'<line x1="50" y1="70" x2="1150" y2="70" stroke="{accent}" stroke-width="4"/>',
        f'<text x="52" y="48" font-size="24" font-weight="700" fill="{INK}">{html.escape(title)}</text>',
    ]


def svg_finish(lines: list[str], footer: str) -> str:
    lines += [
        f'<line x1="50" y1="650" x2="1150" y2="650" stroke="{GRID}"/>',
        f'<text x="52" y="675" font-size="13" fill="{MUTED}">{html.escape(footer)}</text>',
        "</svg>",
    ]
    return "\n".join(lines)


def text(lines: list[str], x: float, y: float, value: object, color: str = MUTED,
         size: float = 13, anchor: str = "start", weight: int = 400) -> None:
    lines.append(
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}">{html.escape(str(value))}</text>'
    )


def rect(lines: list[str], x: float, y: float, w: float, h: float,
         color: str, fill: str = PAPER) -> None:
    lines.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{color}" stroke-width="2"/>')


def privacy_plot(summary: dict[str, float], membership_rows: list[dict[str, object]]) -> None:
    lines = svg_begin("实验 LM70.9-A：Exposure、低 FPR 与删除参照",
                      "合成候选 rank、成员 score 尾部和 unlearning probe 距离。", PURPLE)
    text(lines, 60, 108, "CANARY RANK", INK, 15, "start", 700)
    values = [("space bits", 10, BLUE), ("rank bits", 3, AMBER), ("exposure", 7, PURPLE)]
    for i, (name, value, color) in enumerate(values):
        y = 145 + i * 72
        text(lines, 60, y + 25, name, color, 12, "start", 700)
        lines.append(f'<rect x="180" y="{y}" width="{value*30}" height="38" rx="5" fill="{color}" opacity=".86"/>')
        text(lines, 500, y + 25, str(value), color, 12, "end", 700)
    text(lines, 60, 390, "|R|=1024 · rank=8 · exposure=7 bits", PURPLE, 13, "start", 700)
    text(lines, 620, 108, "MEMBERSHIP @ LOW FPR", INK, 15, "start", 700)
    x0, y0, ww, hh = 650, 350, 450, 190
    lines += [f'<line x1="{x0}" y1="{y0}" x2="{x0+ww}" y2="{y0}" stroke="{INK}"/>',
              f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-hh}" stroke="{INK}"/>']
    for row in membership_rows:
        x = x0 + float(row["score"]) * ww
        y = y0 - (70 if row["group"] == "out" else 140)
        c = BLUE if row["group"] == "out" else RED
        lines.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{c}" opacity=".75"/>')
    tx = x0 + summary["membership_threshold"] * ww
    lines.append(f'<line x1="{tx}" y1="{y0}" x2="{tx}" y2="{y0-hh}" stroke="{AMBER}" stroke-width="3" stroke-dasharray="7 5"/>')
    text(lines, tx, 142, "threshold", AMBER, 11, "middle", 700)
    text(lines, 650, 385, f'FPR={summary["membership_fpr"]:.3f} · TPR={summary["membership_tpr"]:.3f}', RED, 13, "start", 700)
    text(lines, 60, 455, "UNLEARNING PROBE", INK, 15, "start", 700)
    probes = [("unlearned", [.50, .50, .40, .20], PURPLE), ("retrain", [.45, .55, .35, .25], GREEN)]
    for j, (name, vals, color) in enumerate(probes):
        y = 500 + j * 55
        text(lines, 60, y + 20, name, color, 11, "start", 700)
        for i, value in enumerate(vals):
            x = 180 + i * 95
            lines.append(f'<rect x="{x}" y="{y}" width="{value*90}" height="28" rx="4" fill="{color}" opacity=".82"/>')
            text(lines, x + 45, y + 20, f"{value:.2f}", INK, 9, "middle", 700)
    rect(lines, 620, 455, 480, 145, GREEN, "#EEF7EA")
    text(lines, 645, 490, "删除距离只对声明 probe 成立", GREEN, 14, "start", 700)
    text(lines, 645, 525, f'MAD(U,retrain) = {summary["unlearning_mad"]:.3f}', INK, 13)
    text(lines, 645, 555, "效用相同或单个攻击失效都不构成全分布保证。", MUTED, 12)
    text(lines, 645, 580, "旧 checkpoint、index 与 cache 仍须进入 lineage。", MUTED, 12)
    (OUT / "plot-language-safety-privacy-v1.svg").write_text(
        svg_finish(lines, "所有字符串和分数均为合成教学数据；本实验不查询模型、不处理个人信息，也不实施真实抽取。"),
        encoding="utf-8",
    )


def security_plot(summary: dict[str, float], auth_rows: list[dict[str, object]]) -> None:
    lines = svg_begin("实验 LM70.9-B：权限边界与拒答代价",
                      "服务端授权断言、attack/benign 两个分母和 risk–coverage。", RED)
    text(lines, 60, 108, "REFERENCE MONITOR", INK, 15, "start", 700)
    for i, row in enumerate(auth_rows):
        y = 140 + i * 62
        c = GREEN if row["allowed"] else RED
        rect(lines, 60, y, 480, 46, c, "#EEF7EA" if row["allowed"] else "#FFF0ED")
        text(lines, 80, y + 29, row["proposal"], INK, 11, "start", 700)
        text(lines, 515, y + 29, "ALLOW" if row["allowed"] else f'DENY:{row["reason"]}', c, 10, "end", 700)
    text(lines, 60, 485, f'Unauthorized blocked: {int(summary["unauthorized_blocked"])}/{int(summary["unauthorized_total"])}', RED, 13, "start", 700)
    rect(lines, 60, 520, 480, 80, BLUE, "#EEF4FC")
    text(lines, 80, 552, "模型只提交 typed proposal；identity/schema/scope/policy/confirmation", BLUE, 11, "start", 700)
    text(lines, 80, 578, "由模型外 reference monitor 判定，文本自评不改变执行权限。", MUTED, 11)
    text(lines, 620, 108, "HARMFUL / BENIGN", INK, 15, "start", 700)
    cells = [
        (650, 145, "harmful · refuse", 88, GREEN),
        (870, 145, "harmful · answer", 12, RED),
        (650, 260, "benign · refuse", 18, AMBER),
        (870, 260, "benign · answer", 82, BLUE),
    ]
    for x, y, label, n, c in cells:
        lines.append(f'<rect x="{x}" y="{y}" width="190" height="82" rx="8" fill="{c}" opacity=".84"/>')
        text(lines, x + 95, y + 30, label, "#FFFFFF", 11, "middle", 700)
        text(lines, x + 95, y + 61, n, "#FFFFFF", 18, "middle", 700)
    text(lines, 650, 380, f'unsafe={summary["unsafe_answer_rate"]:.2f} · over-refusal={summary["overrefusal"]:.2f}', RED, 13, "start", 700)
    text(lines, 620, 435, "ADAPTIVE BUDGET BASELINE", INK, 15, "start", 700)
    p = summary["at_least_one_attack"]
    lines.append(f'<rect x="650" y="475" width="{p*420}" height="48" rx="6" fill="{PURPLE}" opacity=".86"/>')
    text(lines, 1085, 505, f'{p:.3f}', PURPLE, 13, "end", 700)
    text(lines, 650, 552, "1 − (1 − .03)²⁰；仅作 iid 基线，实际适应性/相关性另测。", MUTED, 12)
    text(lines, 650, 582, f'benign utility={summary["benign_utility"]:.2f}', BLUE, 12, "start", 700)
    (OUT / "plot-language-safety-controls-v1.svg").write_text(
        svg_finish(lines, "低 ASR 不能以零正常效用换取；工具安全取决于权限与后果，而不是模型是否输出拒答措辞。"),
        encoding="utf-8",
    )


def deployment_plot(summary: dict[str, float], bundle_hashes: dict[str, str]) -> None:
    lines = svg_begin("实验 LM70.9-C：版本、Drift、Incident 与证据卡",
                      "Bundle 指纹、分布漂移、发布门和 artifact 完整性。", TEAL)
    text(lines, 60, 108, "BUNDLE FINGERPRINT", INK, 15, "start", 700)
    for i, (name, hsh) in enumerate(bundle_hashes.items()):
        y = 145 + i * 70
        c = BLUE if name == "baseline" else PURPLE
        rect(lines, 60, y, 480, 50, c, "#EEF4FC" if name == "baseline" else "#F3EFFA")
        text(lines, 80, y + 21, name, c, 11, "start", 700)
        text(lines, 80, y + 40, hsh[:24] + "…", MUTED, 10)
    text(lines, 60, 300, "同 bundle 序列化稳定；template 一字节变化使 hash 改变。", MUTED, 11)
    text(lines, 60, 355, "DRIFT", INK, 15, "start", 700)
    vals = [("TV", summary["tv"], BLUE), ("PSI", summary["psi"], AMBER),
            ("observed feedback", summary["observed_accuracy"], GREEN),
            ("target accuracy", summary["target_accuracy"], RED)]
    for i, (name, value, c) in enumerate(vals):
        y = 390 + i * 48
        text(lines, 60, y + 17, name, c, 10, "start", 700)
        lines.append(f'<rect x="190" y="{y}" width="{value*300}" height="27" rx="4" fill="{c}" opacity=".84"/>')
        text(lines, 510, y + 18, f"{value:.3f}", c, 10, "end", 700)
    text(lines, 620, 108, "RELEASE / INCIDENT GATES", INK, 15, "start", 700)
    gates = [
        ("quality non-inferiority", True, GREEN),
        ("unauthorized action = 0", True, GREEN),
        ("p99 latency SLO", False, RED),
        ("all hard gates", False, RED),
    ]
    for i, (name, passed, c) in enumerate(gates):
        y = 145 + i * 73
        rect(lines, 650, y, 430, 52, c, "#EEF7EA" if passed else "#FFF0ED")
        text(lines, 675, y + 32, "PASS" if passed else "FAIL", c, 11, "start", 700)
        text(lines, 770, y + 32, name, INK, 11, "start", 700)
    text(lines, 620, 465, "EVIDENCE CARD", INK, 15, "start", 700)
    rect(lines, 650, 500, 430, 100, TEAL, "#EAF7F4")
    text(lines, 675, 535, f'surface completeness={summary["card_surface"]:.0%}', TEAL, 13, "start", 700)
    text(lines, 675, 565, f'valid artifact completeness={summary["card_valid"]:.0%}', RED, 13, "start", 700)
    text(lines, 675, 590, "关键 hard-gate 链接失效时，比例再高也不可发布。", MUTED, 11)
    (OUT / "plot-language-safety-deployment-v1.svg").write_text(
        svg_finish(lines, "Drift 是线索，版本 hash 是身份，Card 是证据索引；三者都不能单独证明因果、安全或发布就绪。"),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    checks: list[dict[str, object]] = []

    space, rank = 1024, 8
    exposure = math.log2(space) - math.log2(rank)
    checks.append(check(
        "canary_exposure_rank",
        close(exposure, 7.0),
        {"space": space, "rank": rank, "exposure_bits": exposure},
        {"space": 1024, "rank": 8, "exposure_bits": 7.0},
        "LM65: synthetic canary only",
    ))

    out_scores = [i / 100 for i in range(100)]
    in_scores = [.20, .50, .70, .80, .90, .96, .97, .98, .99, 1.00]
    threshold = .985
    fpr = sum(s >= threshold for s in out_scores) / len(out_scores)
    tpr = sum(s >= threshold for s in in_scores) / len(in_scores)
    checks.append(check(
        "membership_low_fpr",
        close(fpr, .01) and close(tpr, .2),
        {"threshold": threshold, "fpr": fpr, "tpr": tpr, "out_n": 100, "in_n": 10},
        {"fpr": .01, "tpr": .2},
        "LM66: tail metric with explicit denominators",
    ))

    unlearned = [.50, .50, .40, .20]
    retrained = [.45, .55, .35, .25]
    unlearning_mad = sum(abs(a - b) for a, b in zip(unlearned, retrained)) / 4
    checks.append(check(
        "certified_removal_distance",
        close(unlearning_mad, .05),
        {"probe_mad": unlearning_mad, "probes": 4},
        {"probe_mad": .05, "scope": "toy_probe_only"},
        "LM66: empirical distance is not a universal certificate",
    ))

    proposals = [
        {"proposal": "read public document", "identity": 1, "schema": 1, "scope": 1, "policy": 1, "confirm": 1},
        {"proposal": "write without scope", "identity": 1, "schema": 1, "scope": 0, "policy": 1, "confirm": 1},
        {"proposal": "malformed arguments", "identity": 1, "schema": 0, "scope": 1, "policy": 1, "confirm": 1},
        {"proposal": "expired identity", "identity": 0, "schema": 1, "scope": 1, "policy": 1, "confirm": 1},
        {"proposal": "high-risk no confirmation", "identity": 1, "schema": 1, "scope": 1, "policy": 1, "confirm": 0},
    ]
    auth_rows = []
    order = ["identity", "schema", "scope", "policy", "confirm"]
    for p in proposals:
        failed = next((key for key in order if not p[key]), "")
        auth_rows.append({"proposal": p["proposal"], "allowed": not bool(failed), "reason": failed or "ok"})
    unauthorized_total = 4
    unauthorized_blocked = sum(not row["allowed"] for row in auth_rows[1:])
    checks.append(check(
        "capability_boundary_and_tool_auth",
        unauthorized_blocked == unauthorized_total and sum(row["allowed"] for row in auth_rows) == 1,
        {"authorized_allowed": 1, "unauthorized_total": unauthorized_total, "unauthorized_blocked": unauthorized_blocked},
        {"authorized_allowed": 1, "unauthorized_blocked": 4},
        "LM67: deterministic server-side predicate",
    ))

    p, budget = .03, 20
    at_least_one = 1 - (1 - p) ** budget
    benign_utility = .92
    checks.append(check(
        "adaptive_attack_budget",
        close(at_least_one, 1 - .97 ** 20) and close(benign_utility, .92),
        {"single_try": p, "budget": budget, "iid_at_least_one": at_least_one, "benign_utility": benign_utility},
        {"iid_at_least_one": 1 - .97 ** 20, "benign_utility": .92, "interpretation": "baseline_only"},
        "LM67/68: attack budget and benign denominator",
    ))

    harmful_refuse, harmful_answer = 88, 12
    benign_refuse, benign_answer = 18, 82
    unsafe_answer_rate = harmful_answer / (harmful_refuse + harmful_answer)
    overrefusal = benign_refuse / (benign_refuse + benign_answer)
    ordered_errors = [0, 1, 0, 0, 1, 0, 1, 1]
    risks = {
        ".25": sum(ordered_errors[:2]) / 2,
        ".5": sum(ordered_errors[:4]) / 4,
        "1.0": sum(ordered_errors) / 8,
    }
    checks.append(check(
        "refusal_confusion_risk_coverage",
        close(unsafe_answer_rate, .12) and close(overrefusal, .18)
        and close(risks[".25"], .5) and close(risks[".5"], .25) and close(risks["1.0"], .5),
        {"unsafe_answer_rate": unsafe_answer_rate, "overrefusal": overrefusal, "risks": risks},
        {"unsafe_answer_rate": .12, "overrefusal": .18, "risks": {".25": .5, ".5": .25, "1.0": .5}},
        "LM68/69: harmful and benign denominators",
    ))

    baseline_bundle = {"model": "m1", "tokenizer": "t1", "template": "c1", "policy": "p1"}
    changed_bundle = {"model": "m1", "tokenizer": "t1", "template": "c2", "policy": "p1"}
    canonical = lambda obj: json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    h_base_a = hashlib.sha256(canonical(baseline_bundle)).hexdigest()
    h_base_b = hashlib.sha256(canonical(dict(reversed(list(baseline_bundle.items()))))).hexdigest()
    h_changed = hashlib.sha256(canonical(changed_bundle)).hexdigest()
    checks.append(check(
        "version_hash_contract",
        h_base_a == h_base_b and h_base_a != h_changed,
        {"same_content_stable": h_base_a == h_base_b, "template_change_detected": h_base_a != h_changed},
        {"same_content_stable": True, "template_change_detected": True},
        "LM70: identity, not trust",
    ))

    baseline_dist, current_dist = [.5, .3, .2], [.4, .35, .25]
    tv = .5 * sum(abs(a - b) for a, b in zip(baseline_dist, current_dist))
    p_dist, q_dist = [.5, .5], [.6, .4]
    psi = sum((a - b) * math.log(a / b) for a, b in zip(p_dist, q_dist))
    observed_accuracy, target_accuracy = .90, .78
    quality_gate, auth_gate, latency_gate = True, True, False
    checks.append(check(
        "drift_feedback_incident",
        close(tv, .1) and close(psi, .04054651081081644)
        and observed_accuracy > target_accuracy and not (quality_gate and auth_gate and latency_gate),
        {"tv": tv, "psi": psi, "observed_accuracy": observed_accuracy, "target_accuracy": target_accuracy,
         "all_gates": quality_gate and auth_gate and latency_gate},
        {"tv": .1, "psi": .04054651081081644, "selection_bias_visible": True, "all_gates": False},
        "LM71: drift signal plus failed hard gate",
    ))

    required, linked, broken = 20, 16, 2
    surface = linked / required
    valid = (linked - broken) / required
    checks.append(check(
        "evidence_card_completeness",
        close(surface, .8) and close(valid, .7),
        {"required": required, "linked": linked, "broken": broken, "surface": surface, "valid": valid},
        {"surface": .8, "valid": .7},
        "LM72: valid artifact links, not checkbox count",
    ))

    membership_rows = (
        [{"group": "out", "score": s} for s in out_scores]
        + [{"group": "in", "score": s} for s in in_scores]
    )
    with (OUT / "privacy_trace.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["record_type", "group", "id", "value", "threshold", "decision"])
        writer.writerow(["canary", "inserted", "synthetic-001", exposure, "", "exposure_bits"])
        for i, row in enumerate(membership_rows):
            writer.writerow(["membership", row["group"], i, row["score"], threshold, int(float(row["score"]) >= threshold)])
        for i, (u, r) in enumerate(zip(unlearned, retrained)):
            writer.writerow(["unlearning", "unlearned", i, u, r, abs(u-r)])
    with (OUT / "security_trace.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["record_type", "name", "eligible", "success_or_error", "rate", "note"])
        for row in auth_rows:
            writer.writerow(["authorization", row["proposal"], 1, int(row["allowed"]), int(row["allowed"]), row["reason"]])
        writer.writerow(["refusal", "harmful", 100, harmful_answer, unsafe_answer_rate, "unsafe_answer_rate"])
        writer.writerow(["refusal", "benign", 100, benign_refuse, overrefusal, "overrefusal"])
        for cov, risk in risks.items():
            writer.writerow(["risk_coverage", cov, 8, "", risk, "selective_risk"])
    with (OUT / "deployment_trace.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["record_type", "name", "value", "status", "note"])
        writer.writerow(["bundle", "baseline_hash", h_base_a, "stable", "canonical JSON sha256"])
        writer.writerow(["bundle", "changed_hash", h_changed, "changed", "template c1→c2"])
        writer.writerow(["drift", "tv", tv, "signal", "input marginal"])
        writer.writerow(["drift", "psi", psi, "signal", "binned marginal"])
        writer.writerow(["feedback", "observed_accuracy", observed_accuracy, "biased", "answered subset"])
        writer.writerow(["feedback", "target_accuracy", target_accuracy, "audit", "random audit"])
        writer.writerow(["release_gate", "latency", 27, "fail", "upper bound > 20 ms"])
        writer.writerow(["evidence", "valid_completeness", valid, "incomplete", "2 broken links"])

    summary = {
        "exposure": exposure,
        "membership_threshold": threshold,
        "membership_fpr": fpr,
        "membership_tpr": tpr,
        "unlearning_mad": unlearning_mad,
        "unauthorized_total": unauthorized_total,
        "unauthorized_blocked": unauthorized_blocked,
        "at_least_one_attack": at_least_one,
        "benign_utility": benign_utility,
        "unsafe_answer_rate": unsafe_answer_rate,
        "overrefusal": overrefusal,
        "tv": tv,
        "psi": psi,
        "observed_accuracy": observed_accuracy,
        "target_accuracy": target_accuracy,
        "card_surface": surface,
        "card_valid": valid,
    }
    results = {
        "experiment_id": "lm70.9-safety-deployment-v1",
        "status": "passed" if all(c["passed"] for c in checks) else "failed",
        "checks_passed": sum(bool(c["passed"]) for c in checks),
        "checks_total": len(checks),
        "checks": checks,
        "safety": "Synthetic strings, abstract proposals and offline arithmetic only; no real target, credential, payload, model or API.",
        "determinism": "Python standard library only; no random sampling, network, model, API or GPU.",
    }
    (OUT / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    privacy_plot(summary, membership_rows)
    security_plot(summary, auth_rows)
    deployment_plot(summary, {"baseline": h_base_a, "template_changed": h_changed})
    if results["status"] != "passed":
        raise SystemExit("one or more checks failed")
    print(json.dumps(
        {"status": results["status"], "checks": f'{results["checks_passed"]}/{results["checks_total"]}', "output": str(OUT)},
        ensure_ascii=False,
    ))


if __name__ == "__main__":
    main()

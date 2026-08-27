#!/usr/bin/env python3
"""Deterministic, standard-library audit for LM-41--LM-48."""

from __future__ import annotations

import csv
import html
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_labs" / "experiments" / "lm70.6-rag-audit-v1"
OUT.mkdir(parents=True, exist_ok=True)


def softmax(xs: list[float]) -> list[float]:
    m = max(xs)
    es = [math.exp(x - m) for x in xs]
    z = sum(es)
    return [x / z for x in es]


def bm25_tf(tf: float, k1: float = 1.5) -> float:
    return tf * (k1 + 1) / (tf + k1) if tf else 0.0


def rrf(ranks: list[int], k0: int = 60) -> float:
    return sum(1 / (k0 + r) for r in ranks)


def dcg(rels: list[int]) -> float:
    return sum((2**r - 1) / math.log2(i + 2) for i, r in enumerate(rels))


def svg_begin(title: str, desc: str) -> list[str]:
    return [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="620" viewBox="0 0 1100 620" role="img" aria-labelledby="title desc">',
        f'<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(desc)}</desc>',
        '<rect width="1100" height="620" fill="#FBF8F1"/>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif}</style>',
        f'<text x="50" y="48" font-size="23" font-weight="700" fill="#183044">{html.escape(title)}</text>',
        '<line x1="48" y1="65" x2="1052" y2="65" stroke="#245AA8" stroke-width="3"/>',
    ]


def svg_end(lines: list[str], note: str) -> str:
    lines += [
        '<line x1="48" y1="575" x2="1052" y2="575" stroke="#D9D5CB"/>',
        f'<text x="50" y="598" font-size="12" fill="#667784">{html.escape(note)}</text>',
        '</svg>',
    ]
    return "\n".join(lines)


def box(lines: list[str], x: int, y: int, w: int, h: int, title: str, body: str, color: str) -> None:
    lines += [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#FFFDF8" stroke="{color}" stroke-width="2"/>',
        f'<text x="{x+14}" y="{y+27}" font-size="14" font-weight="700" fill="{color}">{html.escape(title)}</text>',
    ]
    for i, row in enumerate(body.split("\n")):
        lines.append(f'<text x="{x+14}" y="{y+52+i*19}" font-size="12" fill="#667784">{html.escape(row)}</text>')


checks: dict[str, bool] = {}
results: dict[str, object] = {}

# 1. Latent marginal and top-k renormalization.
weights = [0.5, 0.3, 0.2]
conditionals = [0.8, 0.2, 0.9]
marginal = sum(w * p for w, p in zip(weights, conditionals))
top2 = [weights[0] / 0.8, weights[1] / 0.8]
checks["latent_marginal_and_topk"] = abs(marginal - 0.64) < 1e-12 and top2 == [0.625, 0.37499999999999994]
results["latent"] = {"full_marginal": marginal, "top2_weights": top2, "truncated_mass": 0.2}

# 2. Chunk count, oracle coverage, and normalized distance.
N, L, O = 1000, 256, 64
chunk_count = 1 + math.ceil((N - L) / (L - O))
spans = [(i * (L - O), min(i * (L - O) + L, N)) for i in range(chunk_count)]
gold = (380, 430)
coverage = any(a <= gold[0] and b >= gold[1] for a, b in spans)
sq_distance = 2 - 2 * 0.8
checks["chunk_coverage_and_distance"] = chunk_count == 5 and coverage and abs(sq_distance - 0.4) < 1e-12
results["index_contract"] = {"chunk_count": chunk_count, "spans": spans, "gold": gold, "coverage": coverage, "unit_sq_distance": sq_distance}

with (OUT / "corpus_index.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["chunk_id", "start", "end", "covers_gold", "acl", "version"])
    for i, (a, b) in enumerate(spans):
        w.writerow([f"C{i}", a, b, int(a <= gold[0] and b >= gold[1]), "tenant-A", "v1"])

# 3. BM25 saturation oracle.
tf_values = list(range(0, 11))
tf_scores = [bm25_tf(x) for x in tf_values]
checks["bm25_saturation"] = tf_scores[0] == 0 and all(a < b for a, b in zip(tf_scores, tf_scores[1:])) and tf_scores[-1] < 2.5
results["bm25"] = {"tf": tf_values, "score": tf_scores, "limit": 2.5}

# 4. RRF ranking.
rrf_a, rrf_b = rrf([1, 10]), rrf([3, 3])
checks["rrf_fusion"] = rrf_b > rrf_a and abs(rrf_a - (1 / 61 + 1 / 70)) < 1e-12
results["rrf"] = {"A": rrf_a, "B": rrf_b, "winner": "B"}

# 5. Exact-vs-ANN and candidate upper bound.
exact = ["a", "b", "c", "d", "e"]
ann = ["a", "c", "e", "f", "g"]
ann_recall = len(set(exact) & set(ann)) / 5
gold_doc = "e"
candidate_has_gold = gold_doc in ann
reranked = ["a", "c", "f"]
checks["ann_exact_preservation"] = abs(ann_recall - 0.6) < 1e-12 and candidate_has_gold and gold_doc not in reranked
results["ann"] = {"exact": exact, "ann": ann, "ann_recall_at_5": ann_recall, "candidate_gold": candidate_has_gold, "reranked_gold": gold_doc in reranked}

# 6. Contrastive loss and gradients.
logits = [2.0, 1.0, 0.0]
probs = softmax(logits)
loss = -math.log(probs[0])
grads = [probs[0] - 1, probs[1], probs[2]]
checks["contrastive_gradient"] = abs(sum(grads)) < 1e-12 and abs(loss - 0.40760596444438046) < 1e-12
results["contrastive"] = {"logits": logits, "probabilities": probs, "loss": loss, "gradients": grads}

# 7. Citation correctness and completeness.
claims_need_support, supported_claims = 3, 2
citations, correct_citations = 4, 3
completeness = supported_claims / claims_need_support
correctness = correct_citations / citations
checks["citation_correctness_completeness"] = abs(completeness - 2 / 3) < 1e-12 and correctness == 0.75
results["citations"] = {"completeness": completeness, "correctness": correctness}

# 8. Iterative state and stop contract.
trace = [
    {"step": 0, "state": "question", "action": "retrieve A relation", "observation": "A -> B", "budget_after": 2},
    {"step": 1, "state": "entity B", "action": "retrieve B country", "observation": "B -> C", "budget_after": 1},
    {"step": 2, "state": "two supporting spans", "action": "answer", "observation": "C", "budget_after": 1},
]
checks["iterative_multihop_state"] = trace[-1]["action"] == "answer" and all(trace[i]["budget_after"] >= trace[i + 1]["budget_after"] for i in range(2))
results["multihop"] = {"trace": trace, "joint_evidence": True, "calls": 2}

# 9. Retrieval/generation/attribution metrics and joint event.
rows = [
    {"id": "q1", "R": 1, "G": 1, "A": 1, "first_rank": 1},
    {"id": "q2", "R": 1, "G": 0, "A": 0, "first_rank": 2},
    {"id": "q3", "R": 0, "G": 1, "A": 0, "first_rank": None},
    {"id": "q4", "R": 1, "G": 1, "A": 0, "first_rank": 3},
]
mr = sum(0 if r["first_rank"] is None else 1 / r["first_rank"] for r in rows) / len(rows)
joint = sum(r["R"] * r["G"] * r["A"] for r in rows) / len(rows)
dcg_value = dcg([3, 2, 0])
checks["evaluation_joint_and_metrics"] = abs(joint - 0.25) < 1e-12 and abs(mr - (1 + 0.5 + 0 + 1 / 3) / 4) < 1e-12 and abs(dcg_value - 8.892789260714373) < 1e-12
results["evaluation"] = {"rows": rows, "mrr": mr, "joint_RGA": joint, "dcg_3_2_0": dcg_value}

with (OUT / "ranking_trace.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["query_id", "R", "G", "A", "first_rank", "joint_success"])
    for row in rows:
        w.writerow([row["id"], row["R"], row["G"], row["A"], row["first_rank"] or "", row["R"] * row["G"] * row["A"]])

assert len(checks) == 9
assert all(checks.values()), checks
payload = {"experiment": "lm70.6-rag-audit-v1", "stdlib_only": True, "checks": checks, "passed": sum(checks.values()), "total": len(checks), "results": results}
(OUT / "results.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

# Plot 1: retrieval scoring.
lines = svg_begin("实验图 1｜检索分数与近似保真", "BM25 饱和、RRF 名次融合与 exact/ANN 集合保真。")
lines += ['<line x1="70" y1="330" x2="420" y2="330" stroke="#183044"/>', '<line x1="70" y1="330" x2="70" y2="105" stroke="#183044"/>']
pts = [(70 + i * 35, 330 - s / 2.5 * 210) for i, s in zip(tf_values, tf_scores)]
lines.append(f'<path d="M{" L".join(f"{x},{y:.1f}" for x,y in pts)}" fill="none" stroke="#C87922" stroke-width="4"/>')
for x, y in pts[::2]:
    lines.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#C87922"/>')
lines.append('<text x="70" y="92" font-size="15" font-weight="700" fill="#183044">BM25 tf saturation · limit 2.5</text>')
box(lines, 500, 105, 250, 190, "RRF", f"A ranks (1,10) = {rrf_a:.5f}\nB ranks (3,3) = {rrf_b:.5f}\n\nwinner = B", "#7054A3")
box(lines, 805, 105, 245, 190, "ANN preservation", f"exact top-5: {','.join(exact)}\nANN top-5: {','.join(ann)}\nintersection = 3\nANN recall@5 = {ann_recall:.1f}", "#17766E")
box(lines, 500, 350, 550, 150, "Candidate upper bound", "gold e is present after ANN, but removed by final top-3 rerank.\nThis is a reranker/context loss, not an ANN miss.\nAlways retain IDs at every stage.", "#B7443E")
(OUT / "plot-language-rag-retrieval-v1.svg").write_text(svg_end(lines, "All values are deterministic toy oracles; they demonstrate bookkeeping, not production retrieval quality."), encoding="utf-8")

# Plot 2: pipeline and attribution.
lines = svg_begin("实验图 2｜从 chunk 到 claim 的可归因漏斗", "语料覆盖、候选保真、上下文和 citation 的分层账。")
stages = [
    (65, 125, 180, 115, "Chunk", f"{chunk_count} windows\noracle coverage = {int(coverage)}", "#4F7B45"),
    (285, 125, 180, 115, "ANN", f"exact overlap = 3/5\nrecall = {ann_recall:.1f}", "#17766E"),
    (505, 125, 180, 115, "Rerank", "candidate has gold\nfinal top-3 loses gold", "#7054A3"),
    (725, 125, 180, 115, "Claims", "3 need support\n2 supported", "#245AA8"),
    (945, 125, 120, 115, "Cites", "3/4\ncorrect", "#C87922"),
]
for x,y,w,h,t,b,c in stages:
    box(lines,x,y,w,h,t,b,c)
for x in (245,465,685,905):
    lines.append(f'<line x1="{x}" y1="182" x2="{x+40}" y2="182" stroke="#667784" stroke-width="2"/>')
lines += ['<text x="65" y="315" font-size="15" font-weight="700" fill="#183044">Separate events</text>']
event_data = [("corpus/chunk", 1.0, "#4F7B45"), ("ANN exact preservation", ann_recall, "#17766E"), ("citation completeness", completeness, "#245AA8"), ("citation correctness", correctness, "#C87922")]
for i,(name,val,color) in enumerate(event_data):
    y=350+i*46
    lines += [f'<text x="70" y="{y+16}" font-size="12" fill="#667784">{html.escape(name)}</text>',
              f'<rect x="285" y="{y}" width="650" height="24" rx="4" fill="#E7E2D9"/>',
              f'<rect x="285" y="{y}" width="{650*val}" height="24" rx="4" fill="{color}"/>',
              f'<text x="950" y="{y+17}" font-size="12" fill="#183044">{val:.3f}</text>']
(OUT / "plot-language-rag-pipeline-v1.svg").write_text(svg_end(lines, "A high early-stage score does not imply downstream success; keep stage-level IDs and denominators."), encoding="utf-8")

# Plot 3: evaluation cube as observed rows.
lines = svg_begin("实验图 3｜R × G × A 联合事件", "四个样本在 retrieval、generation、attribution 三轴上的不同失败。")
cols = ["query", "R", "G", "A", "R∧G∧A", "diagnosis"]
xcols = [70, 250, 360, 470, 580, 760]
for x,c in zip(xcols,cols):
    lines.append(f'<text x="{x}" y="115" font-size="13" font-weight="700" fill="#183044">{html.escape(c)}</text>')
diagnoses = ["joint success", "generator failure", "parametric/guess answer", "attribution failure"]
for i,(row,diag) in enumerate(zip(rows,diagnoses)):
    y=150+i*70
    lines.append(f'<rect x="55" y="{y-25}" width="990" height="50" rx="6" fill="{"#EFF6EA" if row["R"]*row["G"]*row["A"] else "#FFFDF8"}" stroke="#D9D5CB"/>')
    vals=[row["id"],row["R"],row["G"],row["A"],row["R"]*row["G"]*row["A"],diag]
    for x,v in zip(xcols,vals):
        color="#4F7B45" if v==1 else "#B7443E" if v==0 else "#183044"
        lines.append(f'<text x="{x}" y="{y+5}" font-size="13" fill="{color}">{html.escape(str(v))}</text>')
box(lines, 70, 455, 300, 90, "Joint rate", f"{joint:.2f} = 1 / 4", "#4F7B45")
box(lines, 400, 455, 300, 90, "MRR", f"{mr:.4f}", "#245AA8")
box(lines, 730, 455, 300, 90, "DCG(3,2,0)", f"{dcg_value:.4f}", "#7054A3")
(OUT / "plot-language-rag-evaluation-v1.svg").write_text(svg_end(lines, "Marginal averages cannot reconstruct the joint event; evaluate and bootstrap at query level."), encoding="utf-8")

print(json.dumps({"passed": sum(checks.values()), "total": len(checks), "output": str(OUT)}, ensure_ascii=False))

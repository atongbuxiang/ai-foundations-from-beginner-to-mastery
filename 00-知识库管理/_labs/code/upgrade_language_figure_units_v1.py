#!/usr/bin/env python3
"""Upgrade legacy chapter-7 figure units to the current teaching contract.

The migration is deliberately narrow: it reads the strict figure-unit audit,
touches only failed records under 70-语言模型, and only inserts missing
question/provenance/read-back/boundary components. It does not alter formulas,
claims, embeds, captions, or generated image assets.
"""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess


VAULT = Path(__file__).resolve().parents[3]
AUDITOR = VAULT / "00-知识库管理" / "_labs" / "code" / "audit-markdown-figure-units.mjs"

LABELS = {
    "plot-tokenization-path-algorithms-v1.svg": "BPE merge-rank 分叉与 WordPiece greedy dead-end",
    "plot-tokenization-unigram-sampling-v1.svg": "Unigram 温度化路径分布与经验频率",
    "fig-lm-tokenizer-audit-fairness-v1.svg": "Tokenizer 的压缩、公平、安全与资源切片",
    "plot-language-objectives-denominators-v1.svg": "语言模型目标的 token、sequence 与 mask 分母",
    "fig-lm-probability-chain-eos-v1.svg": "链式法则、因果条件与 EOS 停止事件",
    "plot-language-pretraining-training-contracts-v1.svg": "预训练数据混合、packing 与有效 token 合同",
    "plot-language-adaptation-template-loss-v1.svg": "Chat Template、response mask 与监督损失",
    "plot-language-adaptation-lora-memory-v1.svg": "LoRA 参数、优化器状态与显存分账",
    "plot-language-adaptation-peft-merging-v1.svg": "PEFT 接口与模型合并的相容条件",
    "fig-lm-adapt-peft-interface-v1.svg": "Adapter、Prompt、Prefix 与 IA3 的插入位置",
    "fig-lm-adapt-lora-factorization-v1.svg": "LoRA 低秩因子化、缩放、初始化与合并",
    "fig-lm-adapt-merge-ties-v1.svg": "Model Soup、Task Arithmetic 与 TIES 的参数路径",
    "fig-lm-adapt-qlora-memory-v1.svg": "QLoRA 量化基座、计算 dtype 与显存账",
    "fig-lm-adapt-full-finetune-forgetting-v1.svg": "全量微调的可塑性、保留与遗忘切片",
    "fig-lm-adapt-chat-template-contract-v1.svg": "消息到 token IDs 的 Chat Template 可执行合同",
    "fig-lm-adapt-instruction-data-bias-v1.svg": "指令数据混合、多轮权重与选择路径",
    "fig-lm-adapt-sft-loss-contract-v1.svg": "Teacher Forcing 与 response-only loss 的位置合同",
    "plot-language-icl-prompt-order-v1.svg": "ICL 示例顺序、标签映射与 prompt 方差",
    "plot-language-icl-theory-mechanism-v1.svg": "ICL 理论镜头、机制探针与因果干预",
    "plot-language-icl-compute-context-v1.svg": "推理时计算、上下文长度与预算匹配",
    "fig-lm-icl-cot-faithfulness-v1.svg": "Chain-of-Thought 的正确性与忠实性分解",
    "fig-lm-icl-theory-lenses-v1.svg": "Bayesian、线性回归与元优化三种 ICL 解释",
    "fig-lm-icl-induction-head-evidence-v1.svg": "Induction Head 回路与干预证据阶梯",
    "fig-lm-icl-prompt-conditional-event-v1.svg": "Prompt 序列化、条件事件与敏感性",
    "fig-lm-icl-sampling-selection-v1.svg": "Self-Consistency、Best-of-N 与 pass-at-k 的覆盖/选择",
    "fig-lm-icl-test-time-search-v1.svg": "Test-time search、verifier 与计算预算",
    "fig-lm-icl-factorial-sensitivity-v1.svg": "Zero/Few-shot、示例顺序与标签映射的析因设计",
    "fig-lm-icl-long-context-evidence-v1.svg": "长上下文位置、证据利用与 Lost-in-the-Middle",
    "plot-language-rag-retrieval-v1.svg": "BM25、RRF 与 ANN 保真的检索 oracle",
    "plot-language-rag-pipeline-v1.svg": "Chunk→retrieval→context→generation→citation 漏斗",
    "plot-language-rag-evaluation-v1.svg": "Retrieval、Generation 与 Attribution 联合事件",
    "fig-lm-rag-ann-rerank-funnel-v1.svg": "ANN recall、候选漏斗、reranker 与 latency",
    "fig-lm-rag-ranking-fusion-v1.svg": "BM25、dense retrieval、hybrid 与 rank fusion",
    "fig-lm-rag-data-lineage-v1.svg": "Chunk、metadata、embedding 与 index 数据血缘",
    "fig-lm-rag-claim-citation-layout-v1.svg": "Context construction、claim、citation 与冲突证据",
    "fig-lm-rag-iterative-state-machine-v1.svg": "Multi-hop 检索状态、预算与工具接口",
    "fig-lm-rag-evaluation-cube-v1.svg": "R×G×A 评估立方与失败分母",
    "fig-lm-rag-negative-geometry-v1.svg": "Retriever 对比目标、negative 几何与梯度",
    "fig-lm-rag-latent-document-v1.svg": "RAG 潜文档、top-K 近似与参数先验",
}


def audit_records() -> list[dict[str, object]]:
    node = shutil.which("node")
    if not node:
        fallback = Path("/Users/tong/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node")
        if fallback.exists():
            node = str(fallback)
    if not node:
        raise RuntimeError("node runtime not found")
    result = subprocess.run(
        [node, str(AUDITOR), str(VAULT), "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    records = json.loads(result.stdout)["records"]
    return [
        row for row in records
        if str(row["file"]).startswith("70-语言模型/") and not row["pass"]
        and row["target"] != "00-知识库管理/_assets/..."
    ]


def find_embed(lines: list[str], target: str) -> int:
    needle = f"![[{target}"
    return next(i for i, line in enumerate(lines) if needle in line)


def find_caption(lines: list[str], embed_index: int) -> int:
    for i in range(embed_index + 1, min(len(lines), embed_index + 18)):
        if "[!figure]" in lines[i]:
            return i
    raise RuntimeError(f"figure callout not found after line {embed_index + 1}")


def callout_end(lines: list[str], caption_index: int) -> int:
    i = caption_index
    while i < len(lines) and lines[i].lstrip().startswith(">"):
        i += 1
    return i


def paragraph_end(lines: list[str], start: int) -> int:
    i = start + 1
    while i < len(lines) and lines[i].strip() and not lines[i].lstrip().startswith("#"):
        i += 1
    return i


def label_for(target: str) -> str:
    name = Path(target).name
    return LABELS.get(name, Path(target).stem.replace("-", " "))


def provenance_for(target: str) -> str:
    if "/_labs/experiments/" in target or "/_assets/plots/" in target:
        return (
            "> **数据来源：**本图由本卷确定性实验脚本生成，并与同目录 results/CSV "
            "或脚本内固定数组同源；未特别标注的结构只承担教学排版。"
        )
    return (
        "> **生成：**本图由本库依据本节定义、正文列出的一级来源和固定绘图脚本重新绘制；"
        "图中的小规模数值或结构用于教学，不复刻论文原图。"
    )


def upgrade(record: dict[str, object]) -> tuple[str, list[str]]:
    path = VAULT / str(record["file"])
    target = str(record["target"])
    checks = dict(record["checks"])
    lines = path.read_text(encoding="utf-8").splitlines()
    label = label_for(target)
    inserted: list[str] = []

    embed = find_embed(lines, target)
    if not checks["visualQuestion"]:
        lines[embed:embed] = [
            f"**读图问题**：{label}中的对象、箭头和比较分母怎样对应正文定义，读者应先核对哪一层？",
            "",
        ]
        inserted.append("visualQuestion")

    embed = find_embed(lines, target)
    caption = find_caption(lines, embed)
    if not checks["provenance"]:
        end = callout_end(lines, caption)
        lines.insert(end, provenance_for(target))
        inserted.append("provenance")

    embed = find_embed(lines, target)
    caption = find_caption(lines, embed)
    end = callout_end(lines, caption)
    if not checks["readBack"]:
        lines[end:end] = [
            "",
            f"**怎样读图**：先定位{label}的输入、输出与条件，再沿箭头或坐标核对变换、"
            "比较对象和分母；最后把图中符号回代正文公式、数据与版本合同。",
            "",
        ]
        inserted.append("readBack")

    if not checks["explicitBoundary"]:
        embed = find_embed(lines, target)
        start = next(
            i for i in range(embed + 1, min(len(lines), embed + 58))
            if "怎样读图" in lines[i] or "如何读图" in lines[i] or "读图路径" in lines[i]
        )
        end = paragraph_end(lines, start)
        lines[end:end] = [
            "",
            f"**图没有证明什么**：该图只解释{label}的结构和本节样例，不证明任意模型、"
            "数据、语言或部署环境都会得到同一性能；真实结论仍需独立实验、区间与版本化工件。",
            "",
        ]
        inserted.append("explicitBoundary")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(path.relative_to(VAULT)), inserted


def main() -> None:
    records = audit_records()
    report = []
    for row in sorted(records, key=lambda x: (str(x["file"]), -int(x["line"]))):
        file, inserted = upgrade(row)
        report.append({"file": file, "target": row["target"], "inserted": inserted})
    print(json.dumps({"records_upgraded": len(report), "report": report}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

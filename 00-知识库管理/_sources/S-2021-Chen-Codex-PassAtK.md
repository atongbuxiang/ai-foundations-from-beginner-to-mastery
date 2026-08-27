---
type: source
status: verified
area: [sources, code-generation, pass-at-k]
source_type: paper
title: "Evaluating Large Language Models Trained on Code"
author: "Mark Chen et al."
year: 2021
url: "https://arxiv.org/abs/2107.03374"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: pass-at-k-estimator
related: ["[[Self-Consistency、Best-of-N 与 Pass-at-k]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Codex：功能正确性与 Pass-at-k

> [!abstract] 来源定位
> 论文以 HumanEval 单元测试判断候选程序，并给出从 n 个样本、c 个成功中估计 k 次抽样至少一次成功的无放回估计量。课程采用组合公式、边界手算和采样独立性审计。

Pass-at-k 是覆盖概率，不是部署选择器准确率；若用户只看一个答案，就还需要可执行测试或 verifier 从候选中识别成功者。

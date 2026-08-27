---
type: source
status: verified
area: [sources, language-models, safety, refusal]
source_type: paper
title: "Do-Not-Answer: A Dataset for Evaluating Safeguards in LLMs"
author: "Yuxia Wang et al."
year: 2024
url: "https://aclanthology.org/2024.findings-eacl.61/"
accessed: 2026-08-26
source_tier: P1
license: "ACL Anthology paper; independent summary"
scope_role: unsafe-request-refusal-evaluation
related: ["[[Jailbreak、Toxicity、Bias 与安全评估]]", "[[Abstention、Refusal、Over-refusal 与风险覆盖]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Do-Not-Answer

> [!abstract] 来源定位
> 论文构建“不应直接回答”的风险问题集并评估 safeguards。课程将其放在 harmful-request recall 一侧；要判断系统是否可用，还必须配对正常请求、边界请求和 over-refusal。

类别边界会随政策、法域、用户年龄和产品能力改变，因此标签与评判模板必须版本化。

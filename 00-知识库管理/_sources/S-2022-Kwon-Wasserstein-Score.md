---
type: source
status: verified
area: [sources, generative-models, score-matching, wasserstein]
source_type: paper
title: "Score-based Generative Modeling Secretly Minimizes the Wasserstein Distance"
author: "Dohyun Kwon; Ying Fan; Kangwook Lee"
year: 2022
url: "https://proceedings.neurips.cc/paper_files/paper/2022/hash/7f52f6b8f107931127eefe15429ee278-Abstract-Conference.html"
venue: "NeurIPS 2022"
accessed: 2026-08-25
source_tier: A
license: "NeurIPS 论文页面；本库仅保存独立摘要、必要公式与链接"
scope_role: supporting-theorem
temporal_role: foundational
related: ["[[Marginal Score、Conditional Score 与去噪等价]]", "[[Diffusion、Flow、速度参数化与统一证据地图]]", "[[S-2023-Su-9467-W距离与得分匹配]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Kwon et al.：Score error 与 Wasserstein 距离

> [!abstract] 来源定位
> 论文在明确假设下，用 score estimation error 控制 score-based generative model 与数据分布之间的 Wasserstein 距离。它为“训练 proxy 与分布误差”提供一条理论桥，但不是无条件的 $W_2\le L_{score}$。

## 本卷采用

- 精确引用 theorem 时保留 regularity、时间积分权重、常数依赖和 terminal mismatch；
- 分开 population score error、learned estimator、continuous reverse process 与 finite-step sampler；
- 结合 [[S-2023-Su-9467-W距离与得分匹配]] 记录直觉推导中失败的中间不等式，训练读者识别证明缺口。

## 禁止外推

score MSE 的下降不必在有限样本、有限模型、不同 weighting 或不同 solver 下单调改善 $W_2$；更不能由该 theorem 直接推出 FID、感知质量或条件一致性同步改善。

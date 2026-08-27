---
type: source
status: verified
area: [sources, ai/scaling-laws, language-models, ai/compute]
source_type: paper
title: "Training Compute-Optimal Large Language Models"
author: "Jordan Hoffmann et al."
year: 2022
url: "https://arxiv.org/abs/2203.15556"
accessed: 2026-08-26
source_tier: A
license: "arXiv / NeurIPS paper; independent summary only"
scope_role: core
temporal_role: active-research
related: ["[[渐近记号、增长率与复杂度]]", "[[S-2020-Kaplan-语言模型尺度定律]]", "[[S-2023-Su-9607-量子化假设与尺度定律]]"]
created: 2026-08-19
updated: 2026-08-26
---

# Training Compute-Optimal Large Language Models

> [!abstract] 来源定位
> 论文通过多种经验路线和IsoFLOP profiles研究固定training compute下的model size与training tokens分配，并得到与早期Kaplan allocation不同的估计。它是MATH-08说明“经验Scaling Law依赖实验制度、控制变量和拟合模型”的关键交叉证据。

## 核心证据

- 训练了数百个模型，覆盖不同参数规模、token数与FLOP预算；
- 对固定compute的loss–model-size曲线寻找minimum；
- 拟合$N_{\rm opt}\propto C^a$与$D_{\rm opt}\propto C^b$；
- 在其制度内估计$a,b$均约为$1/2$，即model size与training tokens随compute近似等比例扩展。

## MATH-08使用方式

这项结果不用于宣称某个指数永恒正确，而用于展示：

1. Optimized frontier是多变量问题；
2. 控制数据与参数瓶颈会改变拟合；
3. IsoFLOP valley比单变量外推提供更多识别信息；
4. 后续实验证据可修订旧经验规则；
5. 预测范围、模型族、训练schedule与compute定义必须一起报告。

## 限制

- 结论绑定所研究Transformer族、token/data与训练流程；
- 更大规模、不同数据质量、MoE或新训练目标可能进入新regime；
- Empirical optimum不等于所有部署目标的最优，因为inference、latency、memory与data acquisition未必在同一objective中。

---
type: source
status: verified
area: [sources, generative-models/vae, optimization]
source_type: paper
title: "Lagging Inference Networks and Posterior Collapse in Variational Autoencoders"
author: [Junxian He, Daniel Spokoyny, Graham Neubig, Taylor Berg-Kirkpatrick]
year: 2019
url: "https://arxiv.org/abs/1901.05534"
accessed: 2026-08-25
source_tier: A
scope_role: core
temporal_role: classical
related: ["[[Posterior Collapse、率失真与解码器容量]]", "[[S-2020-Su-7381-VAE-BN防KL消失]]"]
created: 2026-08-25
updated: 2026-08-25
---

# He et al.：Lagging Inference Networks 与 Posterior Collapse

> [!abstract] 来源定位
> 论文把 collapse 的一个机制定位为训练早期 inference network 追不上不断移动的 model posterior，并提出在模型更新前更积极地优化 inference network。课程采用其 dynamics 竞争解释和实验，不把它升级为 collapse 的唯一原因。

## 边界

- 强 decoder 下 $p_\theta(x\mid z)=p_\theta(x)$、$q=p$ 可能是合法总体最优；
- inference lag 是优化路径机制；prior、likelihood、rate weight、data 与 architecture 也会导致 collapse；
- aggressive updates 的成本和稳定性需计入受控比较。


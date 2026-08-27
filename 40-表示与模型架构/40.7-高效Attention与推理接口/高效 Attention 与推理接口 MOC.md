---
type: moc
status: active
area: [architecture, efficient-attention, inference]
related: ["[[表示与模型架构完整课程地图与掌握标准]]", "[[科学空间 - 第四章专题来源地图]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 高效 Attention 与推理接口 MOC

> [!abstract] 本卷主线
> 高效 Attention 不是一个单一算法族，而是四种不同动作：删减可见边、近似相似度/序列、重排同一计算、压缩推理缓存。本卷用“阶段—shape—算术—驻留—IO—误差—质量”统一账本，防止把 $O(n)$、exact、低显存和低延迟互相替代。

## 建议学习顺序

1. 先用 ARCH-49 建立训练、prefill、decode 三阶段成本账；
2. 再比较 ARCH-50—53 的结构稀疏、低秩压缩与 kernel 近似；
3. 用 ARCH-54 理解“不改模型函数、只改 IO schedule”的 exact 路线；
4. 最后进入 ARCH-55—56，把 KV payload、projection absorption 与 serving 证据分账。

| ID | 节点 | 学习出口 | 状态 |
|---|---|---|---|
| ARCH-49 | [[Attention 的二次复杂度、内存与 IO 瓶颈]] | phase-aware cost ledger | 正文、图、A–E 题解完成 |
| ARCH-50 | [[局部、分块与稀疏 Attention]] | sparse pattern audit | 正文、图、A–E 题解完成 |
| ARCH-51 | [[低秩投影与序列维压缩 Attention]] | low-rank assumption | 正文、图、A–E 题解完成 |
| ARCH-52 | [[核特征、线性 Attention 与结合律重排]] | linearization derivation | 正文、图、A–E 题解完成 |
| ARCH-53 | [[Performer、随机特征与近似误差]] | random-feature audit | 正文、图、A–E 题解完成 |
| ARCH-54 | [[FlashAttention、精确计算与 IO Awareness]] | exact IO-aware algorithm | 正文、图、A–E 题解完成 |
| ARCH-55 | [[KV Cache、MHA、MQA 与 GQA]] | cache ledger | 正文、图、A–E 题解完成 |
| ARCH-56 | [[MLA、潜变量缓存与推理成本证据]] | latent-cache audit | 正文、图、A–E 题解完成 |

## 卷内验收

- 题库：8 组 × 15 题，共 120 题；每个 A—E 层级 24 题，解答 ID 一一对应；
- 确定性复现：[[00-知识库管理/_labs/code/architecture_efficient_attention_audit.py]]，覆盖成本、稀疏图、低秩、kernel state、Performer、online softmax、KV cache 与 MLA；
- 图像：8 张原创矢量教学图，每张均含视觉问题、来源、读图说明和不可推出项；
- 状态边界：静态材料与 toy audit 完成，不等于真实学习通过，也不等于任何方法在未知硬件/任务上占优。

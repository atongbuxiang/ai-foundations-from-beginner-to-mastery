---
type: moc
status: active
area: [architecture, attention]
related: ["[[表示与模型架构完整课程地图与掌握标准]]", "[[科学空间 - 第四章专题来源地图]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Attention 的对象、几何与表达 MOC

> [!abstract] 分卷出口
> 从内容寻址而不是术语记忆出发，能手算 Q/K/V、scaled dot-product、mask、self/cross 与 multi-head；能从几何、核、概率和矩阵秩四条路线重建 Attention，并用反例区分 logit rank、weight rank、解释忠实性、长度外推和系统效率证据。

| ID | 节点 | 学习出口 | 状态 |
|---|---|---|---|
| ARCH-25 | [[内容寻址、Query、Key 与 Value]] | addressing contract | draft + A–E 闭环 |
| ARCH-26 | [[Scaled Dot-Product Attention 与 Softmax 数值语义]] | exact attention computation | draft + A–E 闭环 |
| ARCH-27 | [[Attention Mask、因果性与可见性合同]] | mask semantics | draft + A–E 闭环 |
| ARCH-28 | [[Self-Attention、Cross-Attention 与张量形状]] | QKV shape ledger | draft + A–E 闭环 |
| ARCH-29 | [[Multi-Head Attention、投影子空间与参数量]] | multi-head audit | draft + A–E 闭环 |
| ARCH-30 | [[Attention 的几何、核与概率视角]] | multi-view derivation | draft + A–E 闭环 |
| ARCH-31 | [[Attention 矩阵的秩、瓶颈与有效秩]] | rank audit | draft + A–E 闭环 |
| ARCH-32 | [[Attention 失效模式、反例与证据地图]] | evidence boundary | draft + A–E 闭环 |

## 科学空间的使用边界

- [[S-2021-Su-8338-Performer到线性Attention]]、[[S-2021-Su-8601-无限维线性Attention与核特征]]：承担核特征和结合律的中文理解桥；随机特征保证回查 Performer 原论文；
- [[S-2021-Su-8610-线性Transformer反例]]：承担 feature width/低秩的反直觉实验入口，具体宽度倍数不外推；
- [[S-2023-Su-9859-KeyNorm长度外推]]：保留小模型、训练/测试长度的 `E` 级证据，scale-up 为 `O`；
- [[S-2026-Su-11814-LSE-Softmax-Taylor]]：只在展开点、余项、非负与归一边界内调用；
- [[S-2023-Su-9889-Attention集中性]]：用来把“集中”量化，不让 entropy/热力图冒充准确率或解释；
- [[S-2023-Su-9529-DecoderOnly低秩猜想]]：正对角下三角满秩为 `I`，decoder-only 优势解释为 `H`。

## 静态材料

- 正文：8 / 8；
- 习题与独立详解：120 / 120；
- 正式图：8 / 8；
- 确定性审计：[[00-知识库管理/_labs/code/architecture_attention_audit.py]]（8 / 8）；
- 真实学习验收：尚未作答或评分。

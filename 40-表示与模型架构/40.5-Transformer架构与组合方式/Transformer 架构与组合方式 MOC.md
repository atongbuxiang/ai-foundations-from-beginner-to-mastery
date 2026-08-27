---
type: moc
status: active
area: [architecture, transformer]
related: ["[[表示与模型架构完整课程地图与掌握标准]]", "[[科学空间 - 第四章专题来源地图]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Transformer 架构与组合方式 MOC

| ID | 节点 | 学习出口 | 状态 |
|---|---|---|---|
| ARCH-33 | [[Transformer Block、残差、归一化与 FFN]] | block reconstruction | 静态材料完成 |
| ARCH-34 | [[Transformer Encoder 与双向表示]] | encoder contract | 静态材料完成 |
| ARCH-35 | [[Transformer Decoder 与自回归因果结构]] | decoder contract | 静态材料完成 |
| ARCH-36 | [[Encoder–Decoder 与 Cross-Attention]] | source-target interface | 静态材料完成 |
| ARCH-37 | [[Decoder-Only、Prefix 与架构家族比较]] | family comparison | 静态材料完成 |
| ARCH-38 | [[Vision Transformer、Patch Token 与二维结构]] | vision tokenization | 静态材料完成 |
| ARCH-39 | [[Transformer 形状、参数量与 FLOPs 总账]] | cost ledger | 静态材料完成 |
| ARCH-40 | [[Transformer 表达、稳定性与证据边界]] | theory/evidence audit | 静态材料完成 |

## 建议学习顺序

1. ARCH-33 先建立 block 接线、Jacobian 与 FFN 参数账；
2. ARCH-34—36 分别学习双向输入、因果输出和 source–target 双轴；
3. ARCH-37 用 relation/QKV source/objective/outlet 比较家族；
4. ARCH-38 把同一 encoder 接口迁移到二维 patch tokens；
5. ARCH-39 统一核算参数、MAC、激活与 cache；
6. ARCH-40 最后把表达定理、稳定性理论、实验与机制假说分级。

## 本卷产物与证据语义

- 八个节点各含一张完整图文教学单元；
- 每节点 15 道 A—E 分层题及逐题独立详解，共 120 题；
- [[00-知识库管理/_labs/code/architecture_transformer_audit.py]] 提供 8 项纯标准库确定性审计；
- 审计通过只说明 toy construction 与公式合同一致，不替代真实训练复现或学习者验收；
- 当前真实学习验收：0/8。

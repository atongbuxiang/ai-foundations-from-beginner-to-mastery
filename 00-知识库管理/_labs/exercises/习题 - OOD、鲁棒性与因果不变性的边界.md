---
type: exercise
status: draft
area: [learning-theory/ood, robustness, causal-invariance]
topic: "[[OOD、鲁棒性与因果不变性的边界]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - OOD、鲁棒性与因果不变性的边界]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - OOD、鲁棒性与因果不变性的边界
## A. 识别与复述
### LT-OOD-A01
区分误分类检测、OOD、selective prediction、perturbation/natural robustness 与 causal invariance。
### LT-OOD-A02
为什么 OOD score 必须绑定 $P_{\rm in},P_{\rm out}$？
### LT-OOD-A03
区分 AUROC、AUPR、FPR@TPR、calibration 与 utility。
## B. 手算与局部推导
### LT-OOD-B01
四个 in scores $(.1,.2,.4,.8)$、out scores $(.3,.5,.7,.9)$，score 越大越 OOD，计算 AUROC。
### LT-OOD-B02
群组质量 $(.9,.1)$、错误率 $(.05,.40)$，计算 average 与 worst-group error。
### LT-OOD-B03
若每步 marginal coverage .95 且独立，20 步 simultaneous coverage 约多少？说明序列安全边界。
## C. 证明与反例
### LT-OOD-C01
用 $P_{\rm out}=P_{\rm in}$ 证明无约束 universal OOD detection 不可得。
### LT-OOD-C02
构造 MSP 极高但远离训练 support 的输入。
### LT-OOD-C03
构造在有限训练环境稳定、在新环境翻转的 spurious feature。
## D. 审计与诊断
### LT-OOD-D01
OOD 论文只报 AUROC。补齐 prevalence、threshold、cost、calibration 与 benchmark provenance。
### LT-OOD-D02
设计 raw OOD accuracy 与 source-accuracy trend 之外 effective robustness 分账。
### LT-OOD-D03
审计“domain invariant 所以 causal”的声明，需要哪些 SCM/intervention 证据？
## E. 研究与迁移
### LT-OOD-E01
为 LLM hallucination/rejection 设计 event、out-family、risk–coverage 与 delayed verification。
### LT-OOD-E02
为医疗系统设计 natural shift、worst group、calibration、coverage 与 human review utility。
### LT-OOD-E03
写从 benchmark score 到 causal claim 的五级 claim card。

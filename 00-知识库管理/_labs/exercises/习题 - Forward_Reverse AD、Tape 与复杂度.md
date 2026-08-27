---
type: exercise
status: draft
area: [neural-networks/automatic-differentiation, complexity]
topic: "[[Forward_Reverse AD、Tape 与复杂度]]"
difficulty: [A, B, C, D, E]
related: ["[[解答 - Forward_Reverse AD、Tape 与复杂度]]", "[[Gradient Checking、Checkpointing 与高阶微分边界]]"]
solution: "[[解答 - Forward_Reverse AD、Tape 与复杂度]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - Forward/Reverse AD、Tape 与复杂度
## A. 识别与复述
### NN-AD-A01
区分 symbolic differentiation、finite differences 与 automatic differentiation。
### NN-AD-A02
写出 reverse-capable tape entry 至少需记录的五类信息。
### NN-AD-A03
对 $f:\mathbb R^n\to\mathbb R^m$ 比较一个 JVP、一个 VJP 和 full Jacobian 的 seed 数。
## B. 手算与建模
### NN-AD-B01
用双数手算 $f(x)=\sin(x^2)+x$ 在任意 $x$ 和 seed $\dot x=v$ 的 tangent。
### NN-AD-B02
对 $y=\sin(x_1x_2)+x_1$，在 $(2,3)$ 用 $v=(1,-1)$ 做 JVP，再用 reverse seed 1 得 gradient 并做 dot test。
### NN-AD-B03
对 $f:\mathbb R^{20}\to\mathbb R^3$ 与 $g:\mathbb R^2\to\mathbb R^{100}$，若需 full Jacobian，分别选 forward 还是 reverse；写出扫描数。
## C. 推导与证明
### NN-AD-C01
从 primitive Wengert list 推出 forward tangent recurrence。
### NN-AD-C02
从 cotangent pairing 推出 reverse recurrence、逆拓扑顺序和 fan-out 累加。
### NN-AD-C03
在局部 JVP/VJP 为 primal cost 常数倍的假设下，推导 full Jacobian 的 $O(nC)$ 与 $O(mC)$ 扫描成本，并说明 vectorization 不改变哪个数学量。
## D. 边界、反例与纠错
### NN-AD-D01
纠正：“AD 是 exact，所以不受浮点误差、overflow 或不可微点影响。”
### NN-AD-D02
用 `if x>0` 构造 data-dependent trace，说明 AD 对已执行分支求导不等于对分支边界可微。
### NN-AD-D03
反驳：“把 100 个 seeds 用 `vmap` 批处理后，full Jacobian 的方向数就从 100 变成 1。”
## E. AI 迁移
### NN-AD-E01
为 scalar LLM training loss 选择 AD mode，列出 tape 中的主要 activation/residual 负担。
### NN-AD-E02
为 per-example gradient 设计 batched reverse 语义，说明为何不能先对 batch loss 取 mean。
### NN-AD-E03
为一个 foreign fused primitive 设计 custom JVP/VJP 的 shape、dot-test、finite-difference、alias 和 higher-order 验收。
## 解答入口
[[解答 - Forward_Reverse AD、Tape 与复杂度]]

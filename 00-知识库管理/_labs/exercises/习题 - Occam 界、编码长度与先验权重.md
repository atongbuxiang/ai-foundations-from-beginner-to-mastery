---
type: exercise
status: draft
area: [learning-theory/pac, description-length]
topic: "[[Occam 界、编码长度与先验权重]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[有限假设类、Union Bound 与一致收敛]]", "[[数学归纳、递归与组合计数]]"]
related: ["[[解答 - Occam 界、编码长度与先验权重]]", "[[PAC-Bayes Bound 的测度变换主线]]"]
solution: "[[解答 - Occam 界、编码长度与先验权重]]"
created: 2026-08-20
updated: 2026-08-20
---

# 习题 - Occam 界、编码长度与先验权重

> [!abstract] 训练目标
> 能从 hypothesis-specific failure budget 推导 weighted/countable bound，把 prefix-free code 转成 prior weight，并审计真实 AI 压缩声明遗漏的 metadata 和数据依赖。

## A. 识别与复述

### LT-OCC-A01

写出 prior-weighted simultaneous Hoeffding bound。$\pi(h)$ 在 theorem 中是什么、不是什么？

### LT-OCC-A02

定义 prefix-free code，陈述 Kraft inequality，并说明它怎样产生 $\pi(h)=2^{-L(h)}$。

### LT-OCC-A03

区分 Occam bound、MDL selection、sample compression、Bayesian prior 与 PAC-Bayes posterior。

## B. 手算与构造

### LT-OCC-B01

四个 hypotheses 权重为 $(0.5,0.25,0.125,0.0625)$，$m=1000,\delta=0.04$。检查权重合法性，并计算各自双侧置信半径。

### LT-OCC-B02

某 prefix-free model description 长 $L=200$ bits，$m=5000,\delta=0.05$。计算

$$
\sqrt{\frac{L\log2+\log(2/\delta)}{2m}}.
$$

### LT-OCC-B03

realizable setting 中某 consistent hypothesis 长 $60$ bits，$m=2000,\delta=0.05$。使用 realizable Occam bound 计算总体错误率证书。

## C. 推导与证明

### LT-OCC-C01

从 fixed-$h$ Hoeffding 与 $\delta_h=\delta\pi(h)$ 出发，证明 countable-class simultaneous bound。

### LT-OCC-C02

用 dyadic intervals 或 binary tree 完整证明 prefix-free Kraft inequality；说明非 prefix-free code 为什么不能直接使用同一权重结论。

### LT-OCC-C03

对选择规则

$$
\widehat h\in\arg\min_h[R_S(h)+\operatorname{rad}(h)]
$$

证明 oracle inequality

$$
R_P(\widehat h)\le\inf_h[R_P(h)+2\operatorname{rad}(h)].
$$

## D. 边界、反例与纠错

### LT-OCC-D01

构造一种“看过 validation 后发明编码语言，使获胜模型只有 1 bit”的作弊方法；指出 complexity 被藏在哪里，给出修复。

### LT-OCC-D02

纠正：“int4 模型比 float32 模型短 8 倍，所以泛化 gap 必然小 $\sqrt8$ 倍。”讨论 code metadata、function change、empirical risk 和 bound looseness。

### LT-OCC-D03

说明为什么参数个数、非零参数个数、模型文件大小和 function description length 四者不必相等；给出 ReLU rescaling 或 weight sharing 例子。

## E. AI 迁移

### LT-OCC-E01

为 LoRA adapter 设计一份可解码 code ledger：base model、rank、indices/shapes、quantization、values、scales 与 decoder 分别如何记账？

### LT-OCC-E02

比较两个 validation risk 相同的模型：一个短 rule list，一个大 lookup table。写出 MDL/Occam selection score，并说明何种任务结构会让短模型仍然 misspecified。

### LT-OCC-E03

设计一个 data-independent hierarchical prior：先给 architecture family 权重，再给 family 内模型权重。证明总权重不超过 1，并解释 penalty 的两层分解。

## 分级提示

- `B01`：权重和为 $0.9375$，允许小于 1；
- `B03`：使用 $[L\log2+\log(1/\delta)]/m$；
- `C02`：prefix-free 对应互不相交 dyadic intervals；
- `D01`：还需要为“从多少种语言中选择”付费；
- `E03`：$\pi(h)=w_k\pi_k(h)$。

## 解答入口

完成独立尝试后再打开：[[解答 - Occam 界、编码长度与先验权重]]。

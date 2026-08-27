---
type: exercise
status: draft
area: [learning-theory/pac, machine-learning/erm]
topic: "[[不可知 PAC、ERM 与双侧一致收敛]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[有限假设类、Union Bound 与一致收敛]]", "[[可实现情形的一致 ERM 保证]]"]
related: ["[[解答 - 不可知 PAC、ERM 与双侧一致收敛]]", "[[样本复杂度下界与 Minimax 视角]]"]
solution: "[[解答 - 不可知 PAC、ERM 与双侧一致收敛]]"
created: 2026-08-20
updated: 2026-08-20
---

# 习题 - 不可知 PAC、ERM 与双侧一致收敛

> [!abstract] 训练目标
> 能在没有零风险假设时，用 simultaneous deviation 或 pairwise loss difference 证明 finite-class ERM guarantee，并准确管理 optimization tolerance、surrogate 与 candidate selection。

## A. 识别与复述

### LT-AGN-A01

陈述 finite-class agnostic ERM theorem 的全部条件、excess-risk bound 和 sample-complexity bound。

### LT-AGN-A02

解释 realizable proof 中的 $(1-p)^m$ 为什么不能直接用于不可知 setting；为什么一般 rate 从 $1/\varepsilon$ 变为 $1/\varepsilon^2$？

### LT-AGN-A03

比较双侧 uniform-convergence proof 与 pairwise loss-difference proof：共同事件、适用算法和常数各有何不同？

## B. 手算与构造

### LT-AGN-B01

设 $M=200,\varepsilon=0.1,\delta=0.05$。用

$$
m\ge2\log(2M/\delta)/\varepsilon^2
$$

计算 exact ERM 的充分样本量。

### LT-AGN-B02

$M=500,\delta=0.01$，目标 class excess 为 $0.08$，算法是 $\rho=0.02$ approximate ERM。使用 $2\alpha+\rho$ theorem 计算充分样本量。

### LT-AGN-B03

某固定坏 hypothesis 相对 oracle 的 risk gap 为 $\Delta=0.06$，$m=2000$。用 pairwise Hoeffding 上界它 empirical risk 不高于 oracle 的概率。

## C. 推导与证明

### LT-AGN-C01

在 $\sup_h|R_S(h)-R_P(h)|\le\alpha$ 上，逐行证明 exact ERM class excess 不超过 $2\alpha$；指出两次 deviation 分别用于谁。

### LT-AGN-C02

把 `C01` 推广到 $\rho$-approximate ERM，并反解目标 excess $\varepsilon$ 的样本量。讨论 $\rho\ge\varepsilon$ 时 theorem 为什么无法给非平凡保证。

### LT-AGN-C03

令 $W_i=\ell(h,Z_i)-\ell(h^*,Z_i)\in[-1,1]$，完整推导

$$
\Pr(R_S(h)\le R_S(h^*))
\le e^{-m\Delta_h^2/2},
$$

再对坏 hypotheses 求并集得到 ERM-specific theorem。

## D. 边界、反例与纠错

### LT-AGN-D01

构造一个有标签噪声的二分类分布，使版本空间随样本很快为空，但 finite-class agnostic ERM theorem 仍适用。

### LT-AGN-D02

纠正：“交叉熵训练也属于 agnostic ERM，因此直接有相同的 $[0,1]$ 常数。”指出 loss range 与 task-risk reduction 两个缺口。

### LT-AGN-D03

候选 prompts 根据同一 validation set 自适应生成，最终只有 30 个。解释为什么不能直接令 $M=30$，并给出两个修复协议。

## E. AI 迁移

### LT-AGN-E01

为 100 个冻结 checkpoints 设计 agnostic ERM selection：定义 loss、sampling unit、comparator、置信参数、selection 与最终 test。

### LT-AGN-E02

一个 stochastic LLM judge 对同一 response 多次打分。分析把 judge randomness 并入 $Z$ 与把重复评分当独立样本的区别；给出合法 sample-size 口径。

### LT-AGN-E03

比较增加独立 evaluation examples、减少候选 $M$、改用 variance-sensitive bound、降低 optimization tolerance $\rho$ 四种操作对 certificate 的作用和局限。

## 分级提示

- `B02`：统计项最多只能占 $0.08-0.02$；
- `B03`：区间宽度为 2；
- `C03`：坏 $h$ 被 ERM 选中蕴含它 empirical beat 固定 oracle；
- `D01`：同一输入以两个标签出现；
- `E02`：重复 judge calls 可能条件相关，独立 sampling unit 通常仍是 response/user。

## 解答入口

完成独立尝试后再打开：[[解答 - 不可知 PAC、ERM 与双侧一致收敛]]。

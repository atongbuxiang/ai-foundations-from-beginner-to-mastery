---
type: exercise
status: draft
area: [learning-theory/foundations, machine-learning, optimization]
topic: "[[经验风险最小化、近似 ERM 与超额风险分解]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[损失、总体风险与经验风险]]", "[[优化问题、可行域与局部最优]]"]
related: ["[[解答 - 经验风险最小化、近似 ERM 与超额风险分解]]", "[[泛化间隙与浓缩不等式接口]]"]
solution: "[[解答 - 经验风险最小化、近似 ERM 与超额风险分解]]"
created: 2026-08-20
updated: 2026-08-20
---

# 习题 - 经验风险最小化、近似 ERM 与超额风险分解

> [!abstract] 训练目标
> 分清 Bayes、类内、经验与计算四个最优对象；能从 approximate ERM 推出 uniform-gap 上界，并把 AI 系统误差分配到正确账户。

## A. 识别与复述

### LT-ERM-A01

定义 $R^*,R_{\mathcal H}^*,h_{\mathcal H}^*,\widehat h_S,\widetilde h_{S,U}$。哪些依赖未知 $P$，哪些依赖样本 $S$？

### LT-ERM-A02

定义 exact ERM 与 $\rho$-approximate ERM。为什么 parameter distance 不能直接替代 empirical objective gap？

### LT-ERM-A03

区分 approximation error、class excess risk、generalization gap 与 empirical optimization gap；说明它们是否必然非负。

## B. 手算与构造

### LT-ERM-B01

已知 $R^*=0.08,R_{\mathcal H}^*=0.13,R_P(\widetilde h)=0.19$。计算 approximation error、class excess risk 和 total excess risk，并验证加法分解。

### LT-ERM-B02

某样本上

$$
R_P(\widetilde h)-R_S(\widetilde h)=0.04,
$$

$$
R_P(h_{\mathcal H}^*)-R_S(h_{\mathcal H}^*)=-0.01,
$$

$\rho=0.02$。使用 signed-gap 上界计算 class excess risk 的上界。若 uniform gap 上界为 $0.05$，使用粗上界又得到多少？

### LT-ERM-B03

正文三点分布中 $R^*=0,R_{\mathcal H}^*=1/3$。若某输出总体风险为 $2/3$、经验风险为 0，分别计算 total excess、approximation、class excess 和 realized generalization gap。

## C. 推导与证明

### LT-ERM-C01

从插入 $R_S(\widetilde h),R_S(\widehat h_S),R_S(h_{\mathcal H}^*)$ 开始，完整推导

$$
R_P(\widetilde h)-R_{\mathcal H}^*
\le g_S(\widetilde h)-g_S(h_{\mathcal H}^*)+\rho.
$$

### LT-ERM-C02

由 `C01` 推出

$$
R_P(\widetilde h)-R^*
\le R_{\mathcal H}^*-R^*
+2\sup_{h\in\mathcal H}|R_P(h)-R_S(h)|+\rho.
$$

指出每一步不等式的依据。

### LT-ERM-C03

设 $\mathcal H_1\subseteq\mathcal H_2\subseteq\cdots$ 且 $R_{\mathcal H_k}^*\downarrow R^*$。给出 $k=k(m)$ 使 total excess 可能趋零所需的两个条件；解释 $k(m)$ 增长太快为何会失败。

## D. 边界、反例与纠错

### LT-ERM-D01

构造一个例子，使 approximate solution 的 empirical optimization gap 为正，但它的 population risk 低于 exact ERM。

### LT-ERM-D02

纠正：“模型参数更多一定降低总误差，因为 approximation error 更小。”至少讨论 estimation、optimization、effective sample 与 target mismatch。

### LT-ERM-D03

纠正：“加入 L2 后只是换了一个更容易优化的 ERM。”说明 regularizer 如何改变 selection rule、有效类和参数代表；给出正齐次 rescaling 边界。

## E. AI 迁移

### LT-ERM-E01

为一个零训练误差的图像分类网络设计 error budget，至少包含 approximation、sample selection、optimization、evaluation 与 distribution shift 的可观测诊断。

### LT-ERM-E02

比较扩大语言模型参数、增加独立数据、训练更多 steps、改 tokenizer 四种操作主要影响哪类误差；说明每种操作可能引入的副作用。

### LT-ERM-E03

对“VAT 降低了 validation loss，因此证明它减少模型复杂度并改善泛化”作审计。把已观测事实、机制假设与尚需证明/实验的环节分开。

## 分级提示

- `B02`：$g_S(h_{\mathcal H}^*)=-0.01$；
- `C01`：ERM 项 $R_S(\widehat h_S)-R_S(h_{\mathcal H}^*)\le0$；
- `D01`：让 exact ERM 记忆一个噪声点，early-stopped 输出忽略它；
- `D03`：同一函数的 layerwise L2 可随 rescaling 改变；
- `E03`：validation improvement 是 protocol-specific evidence，不是 distribution-free theorem。

## 解答入口

完成独立尝试后再打开：[[解答 - 经验风险最小化、近似 ERM 与超额风险分解]]。


---
type: exercise
status: draft
area: [learning-theory/vc, combinatorics/extremal-set-theory]
topic: "[[Sauer-Shelah 引理]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[增长函数与经验二分模式]]", "[[数学归纳、递归与组合计数]]", "[[基本不等式与界的构造]]"]
related: ["[[解答 - Sauer-Shelah 引理]]", "[[VC 一致收敛与泛化界]]"]
solution: "[[解答 - Sauer-Shelah 引理]]"
created: 2026-08-20
updated: 2026-08-20
---

# 习题 - Sauer-Shelah 引理

> [!abstract] 训练目标
> 能从 fiber decomposition 独立重建 Sauer–Shelah，而不是只会代入公式；能判断 binomial-sum、解析粗界和实际 growth 的差别。

## A. 识别与复述

### LT-SAUER-A01

陈述 Sauer–Shelah–Perles lemma，包括 $m<d$ 时的组合数约定和 $(em/d)^d$ 形式的适用条件。

### LT-SAUER-A02

在删除最后坐标的证明中，定义 $\mathcal F_0$ 与 $\mathcal F_1$。解释“只出现最后标签 1”的 fiber 属于哪一族。

### LT-SAUER-A03

解释以下三句话的逻辑差别：“增长函数至多是 $d$ 次多项式量级”“增长函数恰为 $m^d$”“class 达到 Sauer 上界”。

## B. 手算与构造

### LT-SAUER-B01

对 $d=3,m=6$，计算精确 binomial-sum 上界、trivial $2^m$ 上界与 $(em/d)^d$ 数值粗界，并比较谁最小。

### LT-SAUER-B02

用递推

$$
T_d(m)\le T_d(m-1)+T_{d-1}(m-1)
$$

从 $T_0(m)=T_d(0)=1$ 手算 $T_1(4)$ 与 $T_2(4)$ 的上界。

### LT-SAUER-B03

在五点 domain 上列出 class $\mathcal H_{\le2}=\{\mathbf1_A:|A|\le2\}$ 的函数数，证明其 VC 维为 2，并验证它达到 $d=2,m=5$ 的 Sauer 上界。

## C. 推导与证明

### LT-SAUER-C01

完整证明 $|\mathcal F|=|\mathcal F_0|+|\mathcal F_1|$，并证明 $\operatorname{VCdim}(\mathcal F_1)\le d-1$。

### LT-SAUER-C02

从递推和 Pascal 恒等式独立完成归纳，推出

$$
T_d(m)\le\sum_{i=0}^{d}{m\choose i}.
$$

要求写出边界条件。

### LT-SAUER-C03

不引用现成结论，使用 $a=d/m$ 和 binomial theorem 推导

$$
\sum_{i=0}^{d}{m\choose i}\le(em/d)^d,
\qquad m\ge d\ge1.
$$

## D. 边界、反例与纠错

### LT-SAUER-D01

纠正：“$\mathcal F_1$ 就是最后坐标取 1 的所有 restrictions，因此它仍可有 VC 维 $d$。”

### LT-SAUER-D02

给出一个 $m,d$ 使 $(em/d)^d>2^m$。这是否反驳 Sauer–Shelah？实际使用时怎样修正？

### LT-SAUER-D03

纠正：“既然 $\tau(m)\le(em/d)^d$，所以不需要概率论就已证明泛化。”列出至少三个仍缺失的对象/步骤。

## E. AI 迁移

### LT-SAUER-E01

一个 anomaly rule 可把至多 $d$ 个输入 ID 标为异常，其余正常。在 $m$ 个不同 IDs 上计算其 pattern 数，解释这是 Sauer 上界的 tight example，但为什么部署时按 ID 记忆通常不是真正 anomaly generalization。

### LT-SAUER-E02

某 neural classifier family 的 VC upper bound 为 $d=10^6$，训练样本 $m=10^5$。能否使用 $(em/d)^d$？Sauer 的哪一个版本仍合法？这组数对 distribution-free uniform bound 暗示什么？

### LT-SAUER-E03

比较“模型在所有可能 inputs 上的参数/函数数”“pooled sample 上的 pattern 数”“Sauer 上界”三层。说明为什么工程上观测到的 pattern 数小，既可能有价值又不足以单独形成 theorem。

## 分级提示

- `B01`：$1+6+15+20=42$；
- `B02`：Pascal 三角形；
- `B03`：数大小为 0、1、2 的子集；
- `C01`：fiber size 为 1 或 2；若 $\mathcal F_1$ 打散 $d$ 点，加回最后一点；
- `C03`：对 $i\le d$，$a^i\ge a^d$；
- `D02`：正文的 $d=2,m=5$ 已提供例子。

## 解答入口

完成独立尝试后再打开：[[解答 - Sauer-Shelah 引理]]。

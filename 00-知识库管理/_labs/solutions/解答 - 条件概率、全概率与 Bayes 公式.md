---
type: solution-set
status: draft
area: [math/probability, math/statistics, ai/probabilistic-modeling]
aliases: [条件概率习题解答, Bayes 公式解答]
prerequisites: ["[[习题 - 条件概率、全概率与 Bayes 公式]]"]
related: ["[[条件概率、全概率与 Bayes 公式]]", "[[练习与测验 MOC]]"]
sources: ["MIT-6.041SC-Lecture-2", "MIT-6.436J-Lecture-3", "Harvard-Stat110-Conditioning"]
created: 2026-08-18
updated: 2026-08-18
---

# 解答 - 条件概率、全概率与 Bayes 公式

> [!warning] 使用边界
> 每个分式都要能用自然语言读出条件方向；若只记“先验乘似然”，很容易漏掉 evidence、base rate 和依赖结构。

## A. 对象与条件

### PROB-CB-A01 解

| 对象 | 名称 | 类型与归一化 |
|---|---|---|
| $P(H_i)$ | prior | 假设上的 PMF，$\sum_iP(H_i)=1$ |
| $P(E\mid H_i)$ | likelihood | 固定 $E$ 后关于 $H_i$ 的非负函数，不要求对 $i$ 归一 |
| $P(E)$ | evidence | 事件概率/边缘 likelihood，负责归一化 |
| $P(H_i\mid E)$ | posterior | 给定证据后的假设 PMF，$\sum_iP(H_i\mid E)=1$ |

likelihood 的概率归一化方向是：固定 $H_i$ 后，对所有可能证据 $e$ 求和/积分为 1。把已观察的 $E$ 固定后改变 $i$，它只是对不同假设兼容程度的比较函数。

### PROB-CB-A02 解

取总数 100：

| | $B$ | $B^c$ | 合计 |
|---|---:|---:|---:|
| $A$ | 9 | 81 | 90 |
| $A^c$ | 1 | 9 | 10 |
| 合计 | 10 | 90 | 100 |

于是

$$
P(A\mid B)=\frac9{10}=0.9,
$$

$$
P(B\mid A)=\frac9{90}=0.1.
$$

联合概率为 $P(A\cap B)=9/100=0.09$。双路核对：

$$
P(B)P(A\mid B)=0.1\times0.9=0.09,
$$

$$
P(A)P(B\mid A)=0.9\times0.1=0.09.
$$

### PROB-CB-A03 解

1. 事件分式要求 $A,B\in\mathcal F$ 且 $P(B)>0$。
2. $H_i$ 必须两两不交、可数且穷尽 $\Omega$；对写成条件概率的项通常要求 $P(H_i)>0$，零质量项可直接以联合概率处理。
3. 除上述分割外，还要求 $P(E)>0$；否则后验分母为零。
4. 一般更新永远可写成条件链，但把边际 LR 直接相乘要求证据在每个竞争假设下条件独立：

   $$
   P(E_{1:m}\mid H)=\prod_jP(E_j\mid H),
   $$

   并且对 $H^c$ 也成立。

## B. 手算与表示

### PROB-CB-B01 解

训练环境 evidence：

$$
P(O)=0.7(0.2)+0.1(0.8)=0.22.
$$

所以

$$
P(S\mid O)=\frac{0.7(0.2)}{0.22}
=\frac{7}{11}\approx0.6364.
$$

1000 封邮件中：预计 200 封垃圾，其中 140 封含 `offer`；800 封正常，其中 80 封含 `offer`。因此含词的 220 封中 140 封垃圾，仍为 $140/220=7/11$。

部署先验改为 $0.05$：

$$
P_{test}(S\mid O)
=\frac{0.7(0.05)}{0.7(0.05)+0.1(0.95)}
=\frac{0.035}{0.13}
\approx0.2692.
$$

同一 likelihood 在不同 base rate 下给出不同后验。

### PROB-CB-B02 解

未归一化后验权重为

$$
w_1=P(M_3\mid C_1)P(C_1)=0.9\cdot\frac13=\frac3{10},
$$

$$
w_2=1\cdot\frac13=\frac13,
\qquad
w_3=0.
$$

证据为

$$
P(M_3)=\frac3{10}+\frac13=\frac{19}{30}.
$$

所以

$$
P(C_1\mid M_3)=\frac{9}{19},
\qquad
P(C_2\mid M_3)=\frac{10}{19}.
$$

换到门 2 的胜率略高，为 $10/19$。主持人偏好改变了经典 $1/3$ 对 $2/3$，说明答案依赖信息生成机制。

### PROB-CB-B03 解

先验 odds：

$$
O(H)=\frac{0.01}{0.99}=\frac1{99}.
$$

条件独立时联合 LR 为 $20\times5=100$，故

$$
O(H\mid E_1,E_2)=\frac{100}{99}.
$$

把 odds 转回概率：

$$
P(H\mid E_1,E_2)
=\frac{100/99}{1+100/99}
=\frac{100}{199}
\approx0.5025.
$$

没有条件独立时正确更新为

$$
O(H\mid E_1,E_2)
=O(H)\frac{P(E_1\mid H)}{P(E_1\mid H^c)}
\frac{P(E_2\mid H,E_1)}{P(E_2\mid H^c,E_1)}.
$$

题目未给最后一个条件 LR，不能数值化。

## C. 推导与连续情形

### PROB-CB-C01 解

定义

$$
Q(A)=\frac{P(A\cap B)}{P(B)}.
$$

因分母正且分子非负，$Q(A)\ge0$。归一化：

$$
Q(\Omega)=\frac{P(\Omega\cap B)}{P(B)}=1.
$$

若 $A_i$ 两两不交，则 $A_i\cap B$ 仍两两不交，并且集合分配律给

$$
\left(\bigcup_iA_i\right)\cap B
=\bigcup_i(A_i\cap B).
$$

所以

$$
Q\left(\bigcup_iA_i\right)
=\frac{P(\bigcup_i(A_i\cap B))}{P(B)}
=\frac{\sum_iP(A_i\cap B)}{P(B)}
=\sum_iQ(A_i).
$$

三公理全部成立。

### PROB-CB-C02 解

若 $H_i$ 是分割：

$$
E=E\cap\Omega
=E\cap\left(\dot\bigcup_iH_i\right)
=\dot\bigcup_i(E\cap H_i).
$$

可列可加性给

$$
P(E)=\sum_iP(E\cap H_i).
$$

对正质量 $H_i$ 用乘法公式：

$$
P(E)=\sum_iP(E\mid H_i)P(H_i).
$$

再由

$$
P(H_i\mid E)=\frac{P(E\cap H_i)}{P(E)}
$$

得到

$$
P(H_i\mid E)
=\frac{P(E\mid H_i)P(H_i)}{\sum_jP(E\mid H_j)P(H_j)}.
$$

若 $P(E)=0$，最后的条件分式无定义。若 $P(H_i)=0$，则 $P(E\cap H_i)=0$；对任何正概率证据 $E$，该假设后验仍为 0。一个 prior-zero 假设不会被普通 Bayes 更新恢复。

### PROB-CB-C03 解

标准 Gaussian 密度记为 $\phi$。观察 $x=2$ 时

$$
\operatorname{LR}
=\frac{f_{X\mid H_1}(2)}{f_{X\mid H_0}(2)}
=\frac{\phi(2-2)}{\phi(2-0)}
=e^2.
$$

先验 odds 为

$$
\frac{P(H_1)}{P(H_0)}=\frac19.
$$

后验 odds：

$$
O(H_1\mid x=2)=\frac{e^2}{9}\approx0.8210.
$$

因此

$$
\boxed{
P(H_1\mid x=2)=\frac{e^2}{9+e^2}\approx0.4509.
}
$$

连续模型中 $P(X=2\mid H_i)=0$，不能取两个零的比；使用的是共同基准测度下的 density ratio。

## D. 边界与纠错

### PROB-CB-D01 解

因 $P(X=1/3)=0$，事件公式给出 $0/0$，没有定义。

若 $Y=X$，自然 regular conditional version 是给定 $Y=y$ 后 $X$ 集中在 $y$：

$$
P(X\le1/2\mid Y=y)=\mathbf1\{y\le1/2\}.
$$

在 $y=1/3$ 时该版本给 1，符合“若精确知道 $X=1/3$，当然知道 $X\le1/2$”的直觉。

但 regular conditional distribution 通常只对 $P_Y$-几乎所有 $y$ 唯一。在任意单个零测点修改其值不会改变积分恒等式。因此必须由模型的连续版本、物理观测机制或额外正则性指定点值，不能把任意版本当作逐点事实。

### PROB-CB-D02 解

令 prior $p=10^{-4}$、灵敏度 $s=0.99$、假阳性率 $f=0.01$。后验为

$$
P(H\mid +)
=\frac{sp}{sp+f(1-p)}
=\frac{0.000099}{0.000099+0.009999}
\approx0.009804.
$$

约为 $0.98\%$，不是 $99\%$。

要求后验超过 $1/2$：

$$
sp>f(1-p),
$$

所以

$$
\boxed{
f<\frac{sp}{1-p}
=\frac{0.99\times10^{-4}}{0.9999}
\approx9.901\times10^{-5}.
}
$$

即假阳性率需低于约 $0.0099\%$。

### PROB-CB-D03 解

若 $E_2$ 是 $E_1$ 的完全复制，则一旦已知 $E_1$，第二条必然出现：

$$
P(E_2\mid H,E_1)=1,
$$

$$
P(E_2\mid H^c,E_1)=1.
$$

第二步条件 LR 为 1，而不是 10。因此

$$
\frac{P(E_1,E_2\mid H)}{P(E_1,E_2\mid H^c)}
=10\times1=10.
$$

把边际 LR 平方等于把同一信息计算两次。

## E. AI 迁移

### PROB-CB-E01 解

label-shift 权重为

$$
r_0=\frac{0.5}{0.8}=0.625,
\qquad
r_1=\frac{0.5}{0.2}=2.5.
$$

未归一化测试后验：

$$
w_0=0.9(0.625)=0.5625,
\qquad
w_1=0.1(2.5)=0.25.
$$

归一化总和 $0.8125$：

$$
\boxed{p_{test}(y\mid x)\approx(0.6923,0.3077).}
$$

失败情形包括：类条件分布也改变（covariate/concept shift）；训练 posterior 不校准或估计错误；测试先验估计不准；某类训练先验为零造成支持缺失；选择机制依赖 $x,y$ 而不只是 prior。

### PROB-CB-E02 解

模型联合为

$$
p_\theta(x,z)=p_\theta(z)p_\theta(x\mid z).
$$

evidence 为

$$
p_\theta(x)=\int p_\theta(x\mid z)p_\theta(z)\,dz.
$$

真实模型 posterior：

$$
p_\theta(z\mid x)
=\frac{p_\theta(x\mid z)p_\theta(z)}{p_\theta(x)}.
$$

$q_\phi(z\mid x)$ 是为近似或提议而单独参数化的条件分布。竖线只说明它对输入 $x$ 条件化；只有当

$$
q_\phi(z\mid x)=p_\theta(z\mid x)
$$

时才等于真实 Bayes 后验，而训练通常只让二者在某个散度/目标下接近。

### PROB-CB-E03 解

令 $A=\{Y=\widehat Y\}$。高值 $P(A\mid C=1)$ 只描述被选择子群。总体准确率满足

$$
P(A)=P(A\mid C=1)P(C=1)+P(A\mid C=0)P(C=0).
$$

若不知道拒答区正确率与 coverage，就不能恢复总体表现。提高阈值改变被选择人群，可能让某些群体覆盖几乎为零；“置信度导致正确”又把关联误作因果。

至少应报告：$P(C=1)$、$P(A\mid C=0)$ 或可界定的拒答代价、分群 $P(C=1\mid G)$ 与 $P(A\mid C=1,G)$、coverage–risk 曲线。选择偏差诊断可比较通过/拒答样本的标签、难度、群体和分布外比例。

> [!success] 验收提示
> 合格答案不仅能算 posterior，还能说清 evidence 来自哪些互斥路径、证据是否独立、条件化是否带选择，以及结果是否被错误解释成因果。

---
type: exercise
status: draft
area: [neural-networks/regularization, dropout, variance, bayesian-boundary, uncertainty]
topic: "[[Dropout 的方差、共适应解释与 Bayesian 边界]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Dropout 的方差、共适应解释与 Bayesian 边界]]"
created: 2026-08-24
updated: 2026-08-24
---
# 习题 - Dropout 的方差、共适应解释与 Bayesian 边界

## A

### NN-DBY-A01
区分四层陈述：精确代数、局部近似、机制假说与经验结果。分别为 Dropout 写一个例子，并说明它们需要何种证据。

### NN-DBY-A02
解释“减少共适应”“隐式集成”“近似 Bayesian inference”三种叙述的对象、条件和不可互相替代之处。

### NN-DBY-A03
区分 Monte Carlo sampling error、variational approximation bias、model misspecification 与 calibration/evaluation error；指出增加 MC 样本数能直接减少哪一类。

## B

### NN-DBY-B01
令随机变量 $X$ 的均值为 $\mu$、方差为 $\sigma^2$，$M\sim\operatorname{Bernoulli}(q)$ 且与 $X$ 独立，$Y=MX/q$。推导 $\mathbb E[Y]$ 与 $\operatorname{Var}(Y)$；代入 $\mu=2,\sigma^2=3,q=0.8$。

### NN-DBY-B02
固定 $x$，独立 element Dropout 后令 $u=a^\mathsf T\widetilde x$、$v=c^\mathsf T\widetilde x$。取 $x=(1,2)$、$a=(1,-1)$、$c=(2,3)$、$q=0.5$，计算 $\mathbb E[u]$、$\operatorname{Var}(u)$ 与 $\operatorname{Cov}(u,v)$。

### NN-DBY-B03
五个 MC regression predictions 为 $(1.0,1.4,0.8,1.2,1.6)$。计算 predictive mean、以 $1/T$ 为分母的 empirical variance 与 mean 的 Monte Carlo standard error estimate；说明最后一个量不等于 predictive standard deviation。

## C

### NN-DBY-C01
在线性模型与平方损失下，推导独立 inverted Dropout 的 exact expected noisy risk，并写出诱导的 data-dependent diagonal quadratic penalty。

### NN-DBY-C02
由二阶 Taylor 展开推导零均值小噪声下的曲率项 $\tfrac12\operatorname{tr}(H\Sigma)$。列出它从局部近似升级为精确等式所需的一个充分情形。

### NN-DBY-C03
对分类样本的 $T$ 个概率向量 $p_t(y\mid x)$，写出 predictive entropy、expected entropy 与二者之差。解释在什么条件下可称 mutual-information estimator，脱离该条件后它仍表示什么。

## D

### NN-DBY-D01
审计命题：“MC Dropout 样本足够多时，就得到真实 Bayesian posterior predictive。”指出至少三种不会随 $T\to\infty$ 消失的误差。

### NN-DBY-D02
为什么不应为 MC Dropout 直接调用整个模型的 `train()`？给出含 BatchNorm 与 Dropout 的模型中选择性启用随机层的测试协议。

### NN-DBY-D03
构造一个训练 accuracy 提高、但“减少共适应”机制尚未被识别的实验结果。列出至少两个机制测量和两个替代解释。

## E

### NN-DBY-E01
设计正则化轨道实验，比较 no Dropout 与多个 $q$，要求区分 optimization、regularization 与 compute effects。

### NN-DBY-E02
设计 uncertainty 轨道实验，比较 deterministic、deep ensemble 与 MC Dropout；规定 accuracy/NLL/Brier/calibration/OOD 或 selective-risk 指标及 matched budget。

### NN-DBY-E03
把“Dropout 是 Bayesian，所以其 uncertainty 已校准”改写成一组可证伪的窄命题，并为每条命题指定验收证据。

## 解答入口

[[解答 - Dropout 的方差、共适应解释与 Bayesian 边界]]

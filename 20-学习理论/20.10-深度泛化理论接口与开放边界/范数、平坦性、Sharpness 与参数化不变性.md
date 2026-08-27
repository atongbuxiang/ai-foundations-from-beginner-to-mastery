---
type: theorem
status: draft
area: [learning-theory/deep-generalization, sharpness, parameterization-invariance]
aliases: [Flat Minima, Sharpness, Rescaling Symmetry, Generalization Measures]
node_id: LT-80
prerequisites: ["[[隐式偏置、最大间隔与优化选择]]", "[[非凸优化、鞍点与深度网络损失地形]]", "[[矩阵扰动]]"]
related: ["[[神经网络容量与 Norm-Based Bound]]", "[[PAC-Bayes Bound 的测度变换主线]]", "[[Lie 群、Lie 代数与对称性]]"]
sources: ["[[S-2017-Dinh-Sharp-Minima]]", "[[S-2015-Neyshabur-Path-SGD]]", "[[S-2020-Jiang-Generalization-Measures]]"]
exercises: ["[[习题 - 范数、平坦性、Sharpness 与参数化不变性]]"]
solutions: ["[[解答 - 范数、平坦性、Sharpness 与参数化不变性]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-sharpness-reparameterization-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# 范数、平坦性、Sharpness 与参数化不变性

> [!abstract] 本章主问题
> “小范数”“平坦极小值”“低 sharpness”常与好泛化相关，但深网存在大量不改变 predictor 的重参数化。若一个 complexity measure 能在函数完全不变时被任意放大，它就不能单独作为函数泛化的因果解释。

## 一、学习目标

完成本章后，应能：

1. 区分 parameter、predictor 与 equivalence class；
2. 写出 ReLU node-wise rescaling symmetry；
3. 用二参数乘积模型精确计算 sharpness 可任意改变；
4. 区分 Hessian eigenvalue、loss-neighborhood 与 perturbation sharpness；
5. 审计 raw weight norm 的尺度依赖；
6. 解释 path norm 为什么能抵消部分 rescaling；
7. 区分 parameter-space 与 function-space perturbation；
8. 区分相关性、预测性与因果机制；
9. 说明 normalization/SAM 会改变比较合同；
10. 为 generalization measure 建立不变性压力测试。

## 二、三层对象必须分开

1. parameter：$\theta\in\Theta$；
2. predictor：$f_\theta:\mathcal X\to\mathcal Y$；
3. equivalence class：

$$
[\theta]=\{\theta':f_{\theta'}=f_\theta\}.
$$

population risk 只由 predictor 决定；raw norm/Hessian 通常由 parameter representative 决定。若 $C(\theta)$ 在 $[\theta]$ 内变化，它不是纯 function complexity。

## 三、ReLU 的正齐次 Rescaling

两层网络一单元贡献

$$
f_{a,w}(x)=a\,\sigma(w^\top x),\qquad \sigma(cz)=c\sigma(z),\ c>0.
$$

对任意 $c>0$，

$$
a'=a/c,\qquad w'=cw
$$

有

$$
f_{a',w'}(x)=\frac a c\sigma(cw^\top x)=a\sigma(w^\top x).
$$

预测函数完全不变，但 $|a'|$、$\|w'\|$、层 Frobenius norm 与 Hessian coordinates 可剧烈改变。

## 四、一个可算到底的 Sharpness 反例

考虑最简单的乘积参数化：

$$
f_{a,b}(x)=abx,\qquad L(a,b)=(ab-1)^2.
$$

所有 $ab=1$ 都表示同一函数 $f(x)=x$ 且是 global minima。gradient：

$$
\nabla L=2(ab-1)(b,a).
$$

在 $ab=1$ 处 Hessian 为

$$
H=2
\begin{pmatrix}
b^2 & ab\\
ab & a^2
\end{pmatrix}
=2
\begin{pmatrix}b\\a\end{pmatrix}
\begin{pmatrix}b&a\end{pmatrix}.
$$

其非零 eigenvalue 是

$$
\boxed{\lambda_{\max}(H)=2(a^2+b^2).}
$$

令 $a=c,b=1/c$，predictor 不变，而

$$
\lambda_{\max}=2(c^2+c^{-2})\to\infty.
$$

所以 raw Hessian sharpness 可对同一 predictor 任意大。

## 五、常见 Sharpness 定义

- Hessian sharpness：$\lambda_{\max}(\nabla^2\widehat L(\theta))$；
- trace sharpness：$\operatorname{tr}H$；
- neighborhood rise：

$$
\sup_{\|\delta\|\le\rho}
[\widehat L(\theta+\delta)-\widehat L(\theta)];
$$

- expected perturbation：$E_\delta\widehat L(\theta+\delta)-\widehat L(\theta)$；
- scale-normalized/adaptive sharpness：坐标半径随 $|\theta_i|$ 调整。

它们不是同一量；对 ReLU kink、batch norm、zero parameters 和 finite radius，二阶近似也可能失效。

## 六、Raw Norm 的相同问题

在 rescaling $a/c,cw$ 下，

$$
|a'|^2+\|w'\|^2
=a^2/c^2+c^2\|w\|^2
$$

可随 $c$ 变大。层间 norm product在简单 chain 中可能保持，但有 skip、共享权重、bias、normalization 时还要重新审计。

任何 norm-based bound 都必须声明 architecture、input normalization、layer representation 和 rescaling invariance。

## 七、Path Norm 的动机

对 feedforward network，从 input 到 output 的每条 path $p$ 取沿途权重乘积；例如平方 path norm：

$$
\|\theta\|_{\rm path}^2
=\sum_{p}\prod_{e\in p}w_e^2.
$$

一个 hidden node 的 incoming weights 乘 $c$、outgoing weights 除 $c$，每条经过它的 path product 不变，因此 path norm 对这种 node-wise rescaling 不变。

但不变性只是必要的稳健性，不自动说明 bound tight、可估计或与真实 generalization gap 因果相关。

## 八、Parameter-Space 与 Function-Space Perturbation

parameter perturbation $\delta\theta$ 的效果由 Jacobian 决定：

$$
f_{\theta+\delta}(x)-f_\theta(x)
\approx J_\theta(x)\delta.
$$

同样大小的 Euclidean $\delta$ 在不同 parameterization 中对应不同函数变化。更接近预测对象的度量可用

$$
E_X\|J_\theta(X)\delta\|^2,
$$

Fisher metric、output KL 或 PAC-Bayes posterior perturbation；但这些也依赖输入分布、posterior choice 与局部近似。

## 九、Flatness 与 Generalization 的三种命题

必须区分：

1. 相关：某训练 sweep 中 flatter models gap 较小；
2. 预测：控制其他因素后 measure 能预测新 runs；
3. 因果/定理：在明确 assumptions 下，控制 measure 可推出 risk bound 或干预会改善 risk。

batch size、learning rate、augmentation、train loss 和 margin 同时改变时，flatness correlation 不能识别因果。

## 十、Sharpness-Aware Training 不等于解释完成

SAM 类目标近似

$$
\min_\theta\max_{\|\delta\|\le\rho}\widehat L(\theta+\delta).
$$

若算法实证提升 test performance，只说明这个训练干预在该 benchmark 有效；要解释机制还需处理 parameterization、normalization、effective learning rate、margin 与 augmentation 交互。优化目标、泛化 bound 和因果解释是三件事。

## 十一、Generalization Measure 的压力测试

对候选 $C(\theta,S)$ 至少做：

1. function-preserving rescaling；
2. neuron permutation；
3. duplicated/canceling units；
4. input-unit/feature rescaling；
5. label permutation control；
6. fixed train loss/margin comparison；
7. cross-hyperparameter rank correlation；
8. new architecture/dataset holdout；
9. measure-selection multiplicity；
10. finite-sample uncertainty。

## 十二、一个 Norm 手算

取 $a=1,w=1$ 与等价表示 $a'=0.01,w'=100$。两者函数相同，但平方 parameter norm 从

$$
1^2+1^2=2
$$

变为

$$
0.01^2+100^2=10000.0001.
$$

path product $|aw|=1$ 保持。这说明 raw norm 排名甚至不能在同一函数等价类内稳定。

## 十三、图：同一 Predictor 可以任意 Sharp

先看图回答：若一个 measure 在 function-preserving rescaling 下改变，它还能否作为比较两个 predictor 的充分函数复杂度？

![[00-知识库管理/_assets/figures/learning-theory/fig-sharpness-reparameterization-v2.svg|900]]

> [!figure] 图 20.10-04　ReLU rescaling、乘积模型 Hessian 与 measure 证据阶梯
> 左栏展示 $a,w$ 反向缩放保持函数；中栏给 $L=(ab-1)^2$ 同一极小流形上的 sharpness 任意化；右栏比较 raw norm、path/function-space measure 与 correlation/causation。来源：依据 Dinh et al.、Neyshabur et al. 与 Jiang et al. 独立绘制；由 [[plot_deep_generalization_part1_v2.py]] 确定性生成。

**怎样读图**：先沿等价类做不变性测试，再判断 measure 属于参数、函数还是数据依赖层；最后才看它与 gap 的统计关系。

**图没有证明什么**：图没有否定所有 normalized sharpness、path norm 或 PAC-Bayes perturbation bound，也没有证明 flatness-aware 方法无效。

## 十四、AI 接口

- batch norm/weight norm：改变 parameter coordinates 与 sharpness；
- LoRA/factorization：同一 update function 有多种 factor scaling；
- LLM checkpoints：raw weight norm 跨架构/精度/normalization 不可直接比；
- quantization：parameter perturbation 应换算成 function/output distortion；
- pruning：sparsity/norm 同时受 reparameterization 与 retraining 影响。

## 十五、常见错误

1. 把 parameter 当 predictor；
2. 不做 function-preserving rescaling test；
3. 把 Hessian 最大特征值当坐标不变量；
4. 不声明 perturbation radius/norm；
5. 认为 path norm 不变就自动 tight；
6. 把相关性叫因果解释；
7. 用 test gap 反复挑 measure；
8. 把 SAM 实证成功等同 sharpness 理论完备。

## 十六、最小记忆与掌握标准

> [!summary]
> - 同一 predictor 对应 parameter equivalence class；
> - ReLU rescaling 可保持函数却改变 raw norm/Hessian；
> - $L=(ab-1)^2$ 上 $ab=1$ 时 $\lambda_{\max}=2(a^2+b^2)$ 可任意大；
> - candidate measure 至少应对相关 function-preserving symmetry 稳健；
> - parameter-space、function-space 与 data-dependent geometry 要分层；
> - correlation、prediction、bound 与 causal intervention 不是同一证据。

能写 symmetry（A）、手算 norm/Hessian（B）、构造重参数化反例（C）、审计 measure sweep（D），并为现代网络提出不变且可证伪的复杂度实验（E）。

## 十七、练习与独立详解

- [[习题 - 范数、平坦性、Sharpness 与参数化不变性]]
- [[解答 - 范数、平坦性、Sharpness 与参数化不变性]]

## 参考来源

- [[S-2017-Dinh-Sharp-Minima]]
- [[S-2015-Neyshabur-Path-SGD]]
- [[S-2020-Jiang-Generalization-Measures]]

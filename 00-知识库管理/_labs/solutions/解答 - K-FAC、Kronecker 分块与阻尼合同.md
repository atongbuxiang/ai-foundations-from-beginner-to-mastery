---
type: solution
status: verified
area: [training, optimization, curvature]
topic: "[[K-FAC、Kronecker 分块与阻尼合同]]"
exercise: "[[习题 - K-FAC、Kronecker 分块与阻尼合同]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - K-FAC、Kronecker 分块与阻尼合同

> [!warning] 使用边界
> Sample Kronecker identity 是精确代数；expectation factorization、block deletion 和 factored damping 是三次不同近似，必须分开记账。

## A. 识别与复述

### TRN22-A01
$\nabla_W\ell=\delta a^T$，column-major convention 下 $\operatorname{vec}(\delta a^T)=a\otimes\delta$，所以 outer product 精确等于 $(aa^T)\otimes(\delta\delta^T)$。近似在把 $\mathbb E[(aa^T)\otimes(\delta\delta^T)]$ 替换为 $\mathbb E[aa^T]\otimes\mathbb E[\delta\delta^T]$ 时才开始。

### TRN22-A02
Moment factorization 删除同一 layer 中 activation outer product 与 backprop outer product 的依赖；block-diagonal approximation 删除不同 layer 参数 gradient 的 cross blocks。$\delta$ 由 forward activation、标签和后续层共同决定，通常不与 $a$ 严格独立，所以“独立”只概括所作的 factorization。

### TRN22-A03
Fast/medium clock 更新 $A,S$ 的 sample/EMA statistics；slow clock 每 $K$ 步重算 inverse/eigen/root cache；apply clock 每个 optimizer step 使用最近 cache。EMA 已带 lag，refresh 间隔又让 inverse 对当前 factors 过时，两种 staleness 叠加。

## B. 手算与构造

### TRN22-B01
$$\delta a^T=\begin{bmatrix}3&6\\-1&-2\end{bmatrix},\qquad \operatorname{vec}(\delta a^T)=(3,-1,6,-2)^T.$$
而 $a\otimes\delta=(1\delta,2\delta)^T=(3,-1,6,-2)^T$，一致。若换 row-major，排列会改变，后续 inverse apply 公式也必须一起改变。

### TRN22-B02
$$S^{-1}GA^{-1}=\begin{bmatrix}1/9&0\\0&1\end{bmatrix}\begin{bmatrix}6&2\\3&1\end{bmatrix}\begin{bmatrix}1/4&0\\0&1\end{bmatrix}=\begin{bmatrix}1/6&2/9\\3/4&1\end{bmatrix}.$$
$S^{-1}$ 校正输出/backprop 空间，$A^{-1}$ 校正输入/activation 空间；它是两侧矩阵作用，不是逐元素除法。

### TRN22-B03
$\mathbb E[a^2\delta^2]=(1+16)/2=8.5$，而 $\mathbb E[a^2]\mathbb E[\delta^2]=[(1+4)/2]^2=6.25$，偏差为 $-2.25$，相对 exact moment 约 $-26.47\%$。更多相同分布样本只会稳定地收敛到这两个不同总体量。

## C. 推导与证明

### TRN22-C01
利用 mixed-product property，
$$ (a\otimes\delta)(a^T\otimes\delta^T)=(aa^T)\otimes(\delta\delta^T). $$
若 $a\in\mathbb R^{d_{in}}$、$\delta\in\mathbb R^{d_{out}}$，左边与右边均为 $(d_{in}d_{out})\times(d_{in}d_{out})$。

### TRN22-C02
标准恒等式 $(B\otimes A)\operatorname{vec}(X)=\operatorname{vec}(AXB^T)$。令左作用矩阵为 $S^{-1}$、右作用为 $A^{-1}$，即 $B=A^{-1}$，得到
$$ (A^{-1}\otimes S^{-1})\operatorname{vec}(G)=\operatorname{vec}(S^{-1}G(A^{-1})^T). $$
对对称 factor，$(A^{-1})^T=A^{-1}$。

### TRN22-C03
展开得
$$A\otimes S+\beta A\otimes I+\alpha I\otimes S+\alpha\beta I.$$
即便 $\alpha\beta=\lambda$，两个 cross terms 通常非零。Exact damping 可分解 $A=Q_A\operatorname{diag}(a_i)Q_A^T$、$S=Q_S\operatorname{diag}(s_j)Q_S^T$，在 Kronecker eigenbasis 中逐项除以 $a_is_j+\lambda$。

## D. 边界、反例与纠错

### TRN22-D01
使用 B03 的两点分布即可：$a^2$ 与 $\delta^2$ 完全正相关，exact moment 为 8.5，factorized 为 6.25。样本数趋于无穷时，样本估计分别收敛到 8.5 与 6.25，统计方差消失但 factorization bias 保留。

### TRN22-D02
$d\times d$ 权重有 $P=d^2$ 个参数，两个 factors 共 $2d^2=2P$ 元素，表面是 $O(P)$；但 factor EMA、inverse/eigenvector cache 可再复制多份，root workspace 可为 $O(d^2)$，多 layer/replica 与 padding 继续放大。若为长宽不均或 block policy 不当，常数、峰值和通信才是生产约束；“一定 $O(P)$”也忽略某些 sharing/partition 元数据。

### TRN22-D03
把位置当独立样本会平均各位置 outer products，通常增加有效样本并丢 cross-location terms；先聚合位置 gradient 再 outer product 会引入所有位置交叉项和抵消；保留完整 cross terms 则 rank/成本更高。Mask、序列长度和 denominator 还会改变 factor 尺度，进而改变 damping 与有效 LR。

## E. AI 迁移

### TRN22-E01
Card 记录 layer/parameter IDs、$a,\delta$ shape、column/row-major、bias 拼接、batch/token/spatial reduction、factor estimator/EMA、block deletion、damping target 与实现、inverse method/residual、refresh clocks、sharing 去重、dtype、shard/replica 和通信 group。

### TRN22-E02
用随机小矩阵逐样本断言 vec outer product 与 Kronecker identity 到舍入误差内一致；用相关两点分布断言 expectation factorization 有预期非零误差；对非标量 diagonal $A,S$ 数值断言 $(A\otimes S+\lambda I)^{-1}$ 与 factored-damped inverse 不相等，并保存 step cosine/norm 差。

### TRN22-E03
统一训练 token、加速器时、初始化、数据顺序、停止与等额 hyperparameter trials，并计 OOM/NaN。报告 factor/HVP 额外计算、通信 bytes/reductions、persistent/peak memory、inverse refresh 的平均和尾时延、吞吐、能耗、time-to-quality 与置信区间；不能只按 optimizer steps 比较。

## 无提示重做

- [ ] 48 小时后从 $\delta a^T$ 重建全部 Kronecker 代数。
- [ ] 一周后给出 exact damping 与 factored damping 的最小数值反例。

---
type: solution
status: verified
area: [training, optimization, muon, scaling]
topic: "[[Muon 形状缩放、Update RMS 与版本差异]]"
exercise: "[[习题 - Muon 形状缩放、Update RMS 与版本差异]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Muon 形状缩放、Update RMS 与版本差异

> [!warning] 使用边界
> 以下 current PyTorch 公式绑定 2026-08-26。所有 $A/B$ 计算先固定 $y=xW$、$W\in\mathbb R^{A\times B}$；转置 convention 必须重新映射。

## A. 识别与复述

### TRN29-A01
$A$ 是 rows/input width，$B$ 是 columns/output width。column-vector 写法的同一线性层通常存为 $W^T\in\mathbb R^{B\times A}$，rows/columns 对换；原来的 $\sqrt{A/B}$ 若机械复制就会变成倒数。正确做法是先写物理输入/输出与 storage layout，再代源码读取的 dimensions。

### TRN29-A02
rank-$r$ partial isometry 的非零 singular values 均为 1：
$$
\lVert Q\rVert_2=1,\qquad
\lVert Q\rVert_F=\sqrt r,\qquad
\operatorname{RMS}(Q)=\sqrt{\frac r{AB}}.
$$
若 $r=0$，zero matrix 的 spectral norm/RMS 为 0，不能套“等于 1”。

### TRN29-A03
访问日源码：
$$
s_{orig}=\sqrt{\max(1,A/B)},
$$
$$
s_{match}=0.2\sqrt{\max(A,B)},
$$
$$
s_{spec}=\sqrt{A/B}.
$$
必须同时保存 implementation/version/date、$A/B$ 的 storage convention、global/local shape、mode/default、base/adjusted LR、NS 前后应用顺序和 decay 使用哪一个 LR。

## B. 手算与构造

### TRN29-B01
两种 shape 都有 $\max(A,B)=4096$，故未缩放 RMS 为 $1/64$。

对 $(4096,1024)$：

- original $s=2$，RMS $=1/32$；
- match $s=0.2(64)=12.8$，RMS $=0.2$；
- spectral $s=2$，RMS $=1/32$。

对 $(1024,4096)$：

- original $s=1$，RMS $=1/64$；
- match $s=12.8$，RMS $=0.2$；
- spectral $s=1/2$，RMS $=1/128$。

该对照展示 original 的 clamp 与 spectral_unclamped 的有方向性。

### TRN29-B02
实际未缩放
$$
\operatorname{RMS}(Q)=\sqrt{\frac2{8\cdot4}}=\frac14.
$$
若误按 full rank $r=4$，未缩放预测为 $1/\sqrt8$；original $s=\sqrt2$ 后 nominal RMS 是 $1/2=1/\sqrt B$。实际 scaled RMS 为
$$
\sqrt2\cdot\frac14=\frac1{2\sqrt2}\approx0.3536.
$$
actual/nominal 比为 $1/\sqrt2$。rank loss 使 update 比 full-rank shape identity 更小。

### TRN29-B03
$$
\lVert\widehat Q\rVert_F
=\sqrt{1.1^2+0.9^2+0.4^2+0^2}
=\sqrt{2.18}\approx1.4765.
$$
共有 16 个元素，所以
$$
\operatorname{RMS}(\widehat Q)=\frac{\sqrt{2.18}}4\approx0.3691.
$$
exact full-rank $4\times4$ polar 的 Frobenius norm 为 2、RMS 为 0.5。nominal full-rank formula 会高估该 finite-step output 约 35.4%。

## C. 推导与证明

### TRN29-C01
Frobenius norm 等于 singular values 的 $\ell_2$ norm：
$$
\lVert U_rV_r^T\rVert_F^2=\sum_{i=1}^r1^2=r.
$$
element RMS 是 Frobenius norm 除以 $\sqrt{AB}$，得 $\sqrt{r/(AB)}$。full rank $r=\min(A,B)$：
$$
\sqrt{\frac{\min(A,B)}{AB}}
=\sqrt{\frac1{\max(A,B)}}.
$$

### TRN29-C02
若 $A\ge B$，ideal RMS 为 $1/\sqrt A$，original 乘 $\sqrt{A/B}$ 后为 $1/\sqrt B$。若 $A<B$，ideal RMS 为 $1/\sqrt B$，clamp 使 $s=1$，仍为 $1/\sqrt B$。spectral_unclamped 在 $A<B$ 时为
$$
\frac{\sqrt{A/B}}{\sqrt B}=\frac{\sqrt A}{B}.
$$

### TRN29-C03
$$
\lVert x\Delta W\rVert_2^2
=x\Delta W\Delta W^Tx^T.
$$
用 trace cyclicity：
$$
\mathbb E[x\Delta W\Delta W^Tx^T]
=\operatorname{tr}\!\left(\Delta W^T\mathbb E[x^Tx]\Delta W\right)
=\operatorname{tr}(\Delta W^TC_x\Delta W).
$$
若 $C_x=\sigma_x^2I$，它化为 $\sigma_x^2\lVert\Delta W\rVert_F^2$。近似 isotropy 只给近似关系，并需报告误差/谱界。

## D. 边界、反例与纠错

### TRN29-D01
$4096\times1024$ full-rank partial isometry 的 spectral norm 是 1，但 element RMS 是 $1/\sqrt{4096}=1/64\approx0.0156$。大多数单个元素远小于 1；spectral norm 描述最坏向量放大，不是 elementwise magnitude。

### TRN29-D02
global $4096\times4096$ 的 original scale 为 1，ideal RMS $1/64$。按列四分片后，每个 local matrix 是 $4096\times1024$，local original scale 为 2；若各 shard 做 local full-rank polar，拼回后的 RMS 是 $1/32$，是 global nominal 的两倍，且 singular vectors也被 block 化。这不是透明分片。

### TRN29-D03
取 $C_x=\operatorname{diag}(100,1)$，两个同 Frobenius norm 的 rank-1 updates 分别只作用于输入坐标 1 和 2。若 norm 都为 1，式中平均 output energy 分别为 100 与 1。相同 update RMS 不能控制 anisotropic activation distribution 下的 function change。

## E. AI 迁移

### TRN29-E01
逐层日志：parameter/storage convention、global/local $(A,B)$、rank/effective rank、NS singular-value sum/square/max、orthogonality residual、nominal scale、actual RMS/spectral norm、$\operatorname{RMS}(\Delta W)/\operatorname{RMS}(W)$、activation covariance probes、output-change RMS、base/adjusted LR、decay 和 implementation commit。

### TRN29-E02
共享模型、数据顺序、seeds、batch/token budget、momentum/NS implementation、parameter groups、fallback optimizer 和总搜索 compute。各 mode 需允许公平的 LR 搜索，因为 scale 含义不同；decay 必须保持同 base-LR rule或单独网格，不能让 adjusted LR 静默改变 decay。报告 nominal 与 actual update，而非只报配置名字。

### TRN29-E03
恢复 framework/release/commit、当时公式/default、$xW/Wx$、global/shard shape、transpose/reshape、NS output 是否先 scale、base LR、decay order、parameter groups。若这些无法从 code/checkpoint/log 恢复，应标记为 implementation-ambiguous historical result，不可与当前 original mode 直接做精确归因。

## 无提示重做

- [ ] 48 小时后从 rank 推出 full-rank RMS。
- [ ] 一周后对 tall/wide 两种 shape 互译三种 current scaling。

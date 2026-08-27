---
type: derivation
status: verified
area: [training, optimization, muon, scaling]
node_id: TRN-29
aliases: [Muon Shape Scaling, Update RMS Translator]
prerequisites: ["[[矩阵梯度、谱核范数对偶与 Matrix Sign]]", "[[Muon 的动量、正交化与参数分组合同]]", "[[矩阵范数]]"]
related: ["[[学习率、局部损失变化与相对更新尺度]]", "[[Muon 的扩展证据、系统成本与迁移边界]]", "[[μP 的 Maximal Update 与宽度尺度推导]]"]
sources: ["[[S-2026-PyTorch-Muon]]", "[[S-2025-Liu-Muon-Scalable-LLM]]", "[[S-2025-Su-10739-Muon续集]]", "[[S-2026-Su-11772-Muon-max-scaling]]", "[[S-2025-Bernstein-Newhouse-Modular-Duality]]"]
exercises: ["[[习题 - Muon 形状缩放、Update RMS 与版本差异]]"]
solutions: ["[[解答 - Muon 形状缩放、Update RMS 与版本差异]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-muon-shape-scaling-translator-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Muon 形状缩放、Update RMS 与版本差异

> [!abstract] 一句话结论
> polar/msign 方向的非零奇异值都为 1，但它的逐元素 RMS 并非常数：满秩 $A\times B$ 矩阵的 RMS 是 $1/\sqrt{\max(A,B)}$。Muon 的各种 shape scaling 正是在选择“想保持什么量”；公式必须绑定矩阵方向约定和软件版本。

## 一、先固定 shape 约定

本节使用 row-vector 线性层

$$
y=xW,\qquad
x\in\mathbb R^{1\times A},\quad
W\in\mathbb R^{A\times B},\quad
y\in\mathbb R^{1\times B}.
\tag{1}
$$

因此：

- $A$ 是输入宽度，也是 $W$ 的 rows；
- $B$ 是输出宽度，也是 $W$ 的 columns。

若框架/论文使用 $y=Wx$，同一物理层的存储矩阵会转置，所有 $A/B$ 公式都要交换。只写 “fan-in/fan-out” 而不写乘法约定，极易得到相反结论。

## 二、partial isometry 的 RMS 精确是多少

设 $Q=U_rV_r^T\in\mathbb R^{A\times B}$，rank 为 $r$。其 $r$ 个非零奇异值均为 1，所以

$$
\lVert Q\rVert_F^2
=\sum_{i=1}^r\sigma_i(Q)^2
=r.
\tag{2}
$$

逐元素 RMS 定义为

$$
\operatorname{RMS}(Q)
=\sqrt{\frac1{AB}\sum_{i,j}Q_{ij}^2}
=\frac{\lVert Q\rVert_F}{\sqrt{AB}}
=\sqrt{\frac r{AB}}.
\tag{3}
$$

满秩时 $r=\min(A,B)$，于是

$$
\operatorname{RMS}(Q)
=\frac1{\sqrt{\max(A,B)}}.
\tag{4}
$$

这是 exact identity，不依赖“随机正交矩阵的元素大约多大”的启发式。

### 2.1 两个 shape 手算

- $A=4096,B=1024$：$r=1024$，$\operatorname{RMS}(Q)=1/\sqrt{4096}=1/64$；
- $A=1024,B=4096$：$r=1024$，$\operatorname{RMS}(Q)=1/\sqrt{4096}=1/64$。

转置矩阵的未缩放 RMS 相同，但乘上非对称 $s(A,B)$ 后可以不同。

## 三、当前 PyTorch 的三种 adjustment

以下是 [[S-2026-PyTorch-Muon]] 在 2026-08-26 的实现语义。令最终方向为

$$
\Delta W=-\eta\,s(A,B)\widehat Q.
\tag{5}
$$

忽略 finite-step residual，并按 full-rank $Q$ 计算：

### 3.1 original

$$
s_{orig}(A,B)
=\sqrt{\max(1,A/B)}.
\tag{6}
$$

代入式 (4)：

- 若 $A\ge B$，RMS 为 $\sqrt{A/B}/\sqrt A=1/\sqrt B$；
- 若 $A<B$，RMS 为 $1/\sqrt B$。

所以在本节 $xW$ 约定下，

$$
\operatorname{RMS}(s_{orig}Q)=\frac1{\sqrt B}.
\tag{7}
$$

这解释了 max/clamp：它把 update RMS 统一到输出宽度 $B$ 的尺度，而不是统一成常数。

### 3.2 match_rms_adamw

$$
s_{match}(A,B)
=0.2\sqrt{\max(A,B)}.
\tag{8}
$$

于是

$$
\operatorname{RMS}(s_{match}Q)=0.2.
\tag{9}
$$

这直接把 ideal polar direction 的 element RMS 匹配到常数量级。系数 $0.2$ 是算法/经验合同，不由线性代数定理推出。

### 3.3 spectral_unclamped

$$
s_{spec}(A,B)=\sqrt{A/B}.
\tag{10}
$$

当 $A\ge B$ 时与 original 相同；当 $A<B$ 时不再 clamp：

$$
\operatorname{RMS}(s_{spec}Q)
=\frac{\sqrt A}{B}.
\tag{11}
$$

它保留了有方向的宽度比，可能与某些 modular/MuP-style 推导更接近，但不能只用名字判断适用性。

## 四、三个“尺度相同”其实是三种任务

### 4.1 参数 update RMS

式 (9) 匹配的是每个参数元素的更新 RMS。它容易监控，但不同 parameterization 下同一函数可有不同参数 RMS。

### 4.2 相对参数更新

常见诊断是

$$
\rho_W
=\frac{\operatorname{RMS}(\Delta W)}
{\operatorname{RMS}(W)+\varepsilon}.
\tag{12}
$$

它能比较 layerwise effective step，但会受到 initialization、weight decay、normalization symmetry 和训练阶段影响。

### 4.3 function-space change

若输入满足 $\mathbb E[x^Tx]=C_x$，则

$$
\mathbb E\lVert x\Delta W\rVert_2^2
=\operatorname{tr}(\Delta W^TC_x\Delta W).
\tag{13}
$$

只有在 $C_x\approx\sigma_x^2I$ 时，式 (13) 才近似正比于 $\lVert\Delta W\rVert_F^2$。真实 activation covariance 非各向同性，因此相同 update RMS 不保证相同 output change。

### 4.4 最坏输入方向

$$
\sup_{\lVert x\rVert_2=1}\lVert x\Delta W\rVert_2
=\lVert\Delta W\rVert_2.
\tag{14}
$$

Muon 的 spectral geometry直接控制这项，但它与平均输入能量仍是不同指标。

## 五、finite-step NS 会改变理想 RMS

若 $\widehat Q=U\operatorname{diag}(\widehat s_i)V^T$，则

$$
\operatorname{RMS}(\widehat Q)
=\sqrt{\frac{\sum_i\widehat s_i^2}{AB}}.
\tag{15}
$$

只有所有可解析的 $\widehat s_i\approx1$ 时，才可用式 (4)。因此实现审计必须同时日志化：

$$
\operatorname{RMS}(\widehat Q),\quad
\lVert\widehat Q\rVert_2,\quad
\text{effective rank},\quad
\text{orthogonality residual}.
$$

否则 nominal shape scale 与实际 applied update 可能相差很大。

## 六、版本翻译表不能缺失

| 字段 | 必须记录的内容 |
|---|---|
| implementation | PyTorch、原始 Jordan、Moonlight、第三方 fused kernel |
| version/date | commit、release 或访问日期 |
| shape convention | $xW$ 还是 $Wx$；global 还是 shard shape |
| adjustment | exact formula 与默认值 |
| NS output | before/after scaling；steps 与 coefficients |
| learning rate | base LR 与 adjusted LR |
| decay | 用 base LR 还是 adjusted LR |
| parameter groups | hidden、embedding、head、bias/norm |

软件默认值会变化；“我们用了 original scaling”不是永久可解释的实验描述。

## 七、图：把三种公式翻译成实际 RMS 目标

先看图回答：original、match_rms_adamw 与 spectral_unclamped 各自固定了什么尺度，为什么转置权重会改变公式解释？

![[00-知识库管理/_assets/figures/training-optimization/fig-muon-shape-scaling-translator-v1.svg|900]]

> [!figure] 图 TRN-29　Muon shape scaling 与 Update RMS 翻译器
> 图从 partial isometry 的 exact Frobenius/RMS 恒等式出发，分别推导 current PyTorch 三种 adjustment 的实际 RMS，并将 parameter RMS、relative update、average output change 与 worst-case spectral change 分开。来源：依据 [[S-2026-PyTorch-Muon]] 当前源码、[[S-2025-Liu-Muon-Scalable-LLM]] 与 [[S-2026-Su-11772-Muon-max-scaling]] 独立绘制。

**怎样读图**：先锁定 $A=$ rows/input、$B=$ columns/output，再沿某一 scaling 分支计算 nominal update RMS；最后选择真正关心的监控目标。

**图没有证明什么**：scale identity 不证明某种 adjustment 训练最好，也不把 parameter RMS 等同于 loss-space trust region。

## 八、初学者常见错误

1. 把 spectral norm 为 1 误写成 element RMS 为 1；
2. 忘记 rank $r$，在 rank-deficient output 上仍用 $\sqrt{\min(A,B)}$；
3. 转置权重却不交换 $A/B$；
4. 用 local shard shape 套 global scaling；
5. 以 nominal $Q$ 公式代替 finite-step $\widehat Q$ 实测；
6. 把同 RMS、同 relative update 与同 function change 当成同一件事。

## 九、本节出口

你应能从奇异值证明式 (3)—(4)，逐段推导三种 PyTorch scaling 的 RMS，固定任意线性层 shape convention，并设计同时记录参数空间与函数空间变化的 layerwise audit。

## 练习与独立解答

- [[习题 - Muon 形状缩放、Update RMS 与版本差异]]
- [[解答 - Muon 形状缩放、Update RMS 与版本差异]]

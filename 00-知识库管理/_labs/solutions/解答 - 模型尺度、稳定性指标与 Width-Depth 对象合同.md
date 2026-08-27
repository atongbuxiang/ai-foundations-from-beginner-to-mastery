---
type: solution
status: verified
area: [training, optimization, parameterization, scaling]
topic: "[[模型尺度、稳定性指标与 Width-Depth 对象合同]]"
exercise: "[[习题 - 模型尺度、稳定性指标与 Width-Depth 对象合同]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - 模型尺度、稳定性指标与 Width-Depth 对象合同

> [!warning] 使用边界
> 下列 $O(1)$ 均绑定所写归一化对象和极限路径；有限宽数值符合只构成证据，不是渐近定理证明。

## A. 识别与复述

### TRN41-A01
六栏是 family、path、time、randomness、object、criterion。“扩大四倍”未说明是参数量、width、depth、专家数还是算力；“Transformer”未固定 block/norm/attention/optimizer；未说明初始化或训练后哪个时刻；未说明对初始化、batch 还是数据顺序取概率；“稳定”未指定 activation、gradient、update、logit 或 loss；也未说明 RMS、谱、期望、高概率及允许区间。

### TRN41-A02
coordinate scale 是单坐标标准差/RMS；vector RMS 为 $\|x\|_2/\sqrt n$；Euclidean norm 为 $\|x\|_2$；entry RMS 为 $\|W\|_F/\sqrt{mn}$；operator norm 是单位输入上的最大放大。若坐标 RMS 为常数，Euclidean norm 自动为 $\Theta(\sqrt n)$；若矩阵 entry RMS 为常数，Frobenius norm 自动为 $\Theta(\sqrt{mn})$。operator norm 不能只由 entry RMS 无条件确定。

### TRN41-A03
$\mathbb EZ_n=O(1)$ 只控制均值；$O_p(1)$ 表示分布族 tight，任意小尾概率都可由固定阈值控制；高概率界给出显式 $1-\delta$ 与常数；确定性一致界要求所有样本、所有 $n$ 都不越界。一般不能无条件互推，后两类需注意常数是否依赖 $\delta$。

## B. 手算与构造

### TRN41-B01
每层为 $(4+8)d^2=12d^2$，总量近似 $12Ld^2$。以 $(512,12)$ 为 1：
$$
\frac{N(1024,12)}{N(512,12)}=4,\qquad
\frac{N(512,48)}{N(512,12)}=4.
$$
两者参数量都四倍，但前者 width 加倍、depth 固定，后者 width 固定、depth 四倍；矩阵聚合、residual 累积、并行和理论极限都不同。

### TRN41-B02
$$
\mathbb E\|x\|_2^2=\sum_i\mathbb Ex_i^2=4n,
\qquad
\mathbb E[\operatorname{RMS}(x)^2]=4.
$$
典型 $\|x\|_2\approx2\sqrt n$，所以 $n=100$ 时约 20，$n=10\,000$ 时约 200；vector RMS 仍约 2。

### TRN41-B03
同向时
$$
\|h_L-h_0\|=\left\|\alpha_L\sum_{\ell=1}^Lu_\ell\right\|=L\alpha_L,
$$
故需 $\alpha_L=O(1/L)$。正交时平方范数为 $L\alpha_L^2$，总量为 $\sqrt L\alpha_L$，故需 $\alpha_L=O(L^{-1/2})$。真实网络在两者之间且受 Jacobian 与相关性影响。

## C. 推导与证明

### TRN41-C01
$$
y_j=\sum_i x_iW_{ij}.
$$
均值为 0，且
$$
\operatorname{Var}(y_j)
=\sum_i\mathbb E[x_i^2]\mathbb E[W_{ij}^2]
+\sum_{i\ne k}\mathbb E[x_ix_k]\mathbb E[W_{ij}W_{kj}]
=d_{in}q\frac{\sigma^2}{d_{in}}
=q\sigma^2.
$$
交叉项因零均值、坐标独立/不相关以及 $x,W$ 独立而消失；训练后这些条件通常不再精确成立。

### TRN41-C02
恒等式
$$
\|x_n\|_2=\sqrt n\,\operatorname{RMS}(x_n)
$$
直接给出结论：tight 的 RMS 乘确定性 $\sqrt n$ 得 $O_p(\sqrt n)$。反向应写 $\|x_n\|_2/\sqrt n=O_p(1)$，这与 vector RMS 完全相同。

### TRN41-C03
由 $\nabla_WL=X^\top\nabla_YL$，
$$
\Delta W=-\eta X^\top\nabla_YL,\qquad
\Delta Y=X\Delta W=-\eta XX^\top\nabla_YL.
$$
若 $X\in\mathbb R^{b\times d}$ 且 $b>d$，则 $\operatorname{rank}(XX^\top)\le d<b$，不可能等于满秩 $cI_b$。更合理的是要求 $X^\top X/b\approx cI_d$，或只在 $\operatorname{col}(X)$ / 当前梯度投影到的非零谱子空间上近似标量映射。

## D. 边界、反例与纠错

### TRN41-D01
令 $Z_n=n$ 的概率为 $1/n$，否则为 0，则 $\mathbb EZ_n=1$，但取到的非零幅度随 $n$ 增长。它说明期望有界不控制最大值，也不提供固定高概率常数；训练中的稀有爆炸可被均值掩盖。

### TRN41-D02
初始化 activation 只验证 forward-at-$t=0$。gradient 可能随 width 消失/爆炸；optimizer normalization 后 direction 与 raw gradient 不同；parameter update 可在矩阵聚合后导致 $O(\sqrt n)$ 或 $O(n)$ feature jump；长期 residual/moment 累积也未检查。至少需要 $t=1$ 和早期窗口的 gradient、actual update、feature/logit change。

### TRN41-D03
例：A 取 width $2d$、depth $L$，B 取 width $d$、depth $4L$，主导参数量都约为原模型四倍。A 改变随机矩阵维度和 fan scaling；B 改变 residual/Jacobian 乘积与时延。固定深度下令 width 趋无穷的定理只覆盖 A 类路径，不覆盖 $L$ 同时增长的 B。

## E. AI 迁移

### TRN41-E01
示例：令 $d_{model}=n$、$d_{ff}=4n$、$L=12$、$V$ 与 $S$ 固定。可选路径 A 固定 $h=8$、令 $d_h=n/8$；路径 B 固定 $d_h=64$、令 $h=n/64$。固定 mean token loss、batch tokens $B$、训练 tokens $T$ 或明确其是否变化。manifest 还需记录 norm、residual、tying、optimizer 和 dtype，否则 family 未冻结。

### TRN41-E02
遥测可取 preactivation/activation RMS、gradient RMS、direction RMS、parameter-update RMS、relative update、feature update、logit RMS、spectral norm、loss。时刻至少 $t=0,1$ 与早期 $t=8$（或完整窗口）。报告逐 seed 曲线与跨 seed 区间/失败率。失败门可为非有限值、coord slope 越界、spectral/residual 越界、loss/entropy collapse；所有阈值预注册。

### TRN41-E03
Weight RMS 只说明一个参数坐标统计，未覆盖 shape path、actual update、谱、feature 或训练结果。稳妥改写：
> 在列明的 1B/7B family、参数组和 checkpoint 时刻，观察到 entry Weight RMS 位于预注册区间；尚未证明 operator/feature/depth 稳定或跨架构 μP，需结合 update、activation、logit、谱与失败率。

## 无提示重做

- [ ] 48 小时后从六栏合同审计一条真实 scaling claim。
- [ ] 一周后重做 rank 与 residual 两个反例。

---
type: solution
status: draft
area: [neural-networks/regularization, mixup, manifold-mixup, vicinal-risk]
topic: "[[Mixup、Manifold Mixup 与插值正则]]"
exercise: "[[习题 - Mixup、Manifold Mixup 与插值正则]]"
sources: ["[[S-2018-Zhang-Mixup]]", "[[S-2019-Verma-Manifold-Mixup]]"]
created: 2026-08-24
updated: 2026-08-24
---
# 解答 - Mixup、Manifold Mixup 与插值正则

## A

### NN-MIX-A01
采 pair indices $(i,j)$ 与 $\lambda\sim\operatorname{Beta}(\alpha,\alpha)$，用同一 $\lambda$ 构造
$$\tilde x=\lambda x_i+(1-\lambda)x_j,\quad
\tilde y=\lambda y_i+(1-\lambda)y_j.$$
需记录 pairing pool/permutation、是否 self-pair/class-aware、$\lambda$ 是 per-example/batch/feature、是否取 `max`、augmentation order、distributed rank 与 RNG。输入和 target 若用不同 $\lambda$，就不再是该标准合同。

### NN-MIX-A02
ERM 对 empirical atoms $(x_i,y_i)$ 求平均；Mixup 对 pair 与 chord coefficient 诱导的 $Q_{\rm mix}$ 求期望。Mixed points 通常不在 empirical support，targets 也变成 convex combinations，所以该 stochastic loss 无偏估计的是 vicinal risk $R_{Q_{\rm mix}}$，不是原 empirical risk。Distribution change 正是正则化假设，而非 estimator error。

### NN-MIX-A03
Input chord 是 ambient input vector space 的直线段；hidden chord 是某个 learned coordinate 中的线段；data manifold 是数据 support 的结构假设；geodesic 还依赖 metric。Hidden chord 未必位于 representation image，也不对 reparameterization invariant。论文名称和特定 flattening theorem 不能证明任意 hidden interpolation 是真实语义 geodesic。

## B

### NN-MIX-B01
三者 $\mathbb E\lambda=1/2$。用
$$\operatorname{Var}(\lambda)=1/[4(2\alpha+1)],\quad
\mathbb E\lambda(1-\lambda)=\alpha/[2(2\alpha+1)]$$
得到：

| $\alpha$ | variance | mean mixing strength |
|---:|---:|---:|
| 0.2 | $0.178571$ | $0.071429$ |
| 1 | $0.083333$ | $0.166667$ |
| 10 | $0.011905$ | $0.238095$ |

$\alpha$ 越大越集中在 midpoint，尽管 mean 始终相同。

### NN-MIX-B02
$$\tilde x=.25(2,0)+.75(0,4)=(.5,3),$$
$$\tilde y=.25e_1+.75e_3=(.25,0,.75).$$
CE 为
$$
-.25\log.2-.75\log.7
\approx.40236+.26750=.66987.
$$
第二类 target 为 0，所以其 $p_2=.1$ 不直接出现在 loss，但通过 softmax normalization 仍影响 logits 与 gradients。

### NN-MIX-B03
线性 mix 的 VJP 为
$$\bar h_i=\lambda g=.3(2,-1)=(.6,-.3),$$
$$\bar h_j=(1-\lambda)g=.7(2,-1)=(1.4,-.7).$$
若 prefix parameters 共享，
$$
\nabla_{\theta_{\le k}}L
=.3J_{h_i,\theta}^{\mathsf T}g+.7J_{h_j,\theta}^{\mathsf T}g.
$$
同一个 suffix cotangent 沿两条 source trajectory 回传。

## C

### NN-MIX-C01
Beta$(a,b)$ moments 给 $E\lambda=a/(a+b)=1/2$。对 $a=b=\alpha$，
$$E\lambda^2=\frac{\alpha(\alpha+1)}{2\alpha(2\alpha+1)}
=\frac{\alpha+1}{2(2\alpha+1)}.$$
减去 $1/4$ 得 variance $1/[4(2\alpha+1)]$；再用 $E[\lambda(1-\lambda)]=E\lambda-E\lambda^2$ 得 $\alpha/[2(2\alpha+1)]$。Mean 因 distribution symmetry 固定，不能说明 mass 在 endpoints 还是 center。

### NN-MIX-C02
固定 $p=f(\tilde x)$：
$$
H(\lambda y_i+(1-\lambda)y_j,p)
=\lambda H(y_i,p)+(1-\lambda)H(y_j,p).
$$
这是 target 的线性；它没有比较 $p(x_i),p(x_j)$，也没有约束 $z(\tilde x)$ 等于 endpoint logits 的凸组合。只有在 sampled mixed points 上优化到特定概率 target，并不能推出全局 logit/representation affine map。

### NN-MIX-C03
$$
S_\epsilon(\lambda y_i+(1-\lambda)y_j)
=(1-\epsilon)(\lambda y_i+(1-\lambda)y_j)+\epsilon u
$$
等于 $\lambda S_\epsilon(y_i)+(1-\lambda)S_\epsilon(y_j)$，因 $\lambda+(1-\lambda)=1$。完整 pipeline 可因 input/hidden mixing、class/input-dependent prior、augmentation order、BatchNorm state、pairing/RNG 与 target-entropy-driven retuning 而不交换。

## D

### NN-MIX-D01
取二维 supports：class A 在 $(-1,0)$ 附近、class B 在 $(1,0)$ 附近、class C 在 $(0,0)$ 附近。A/B endpoints 的 $\lambda=1/2$ mixed point 是 $(0,0)$，Mixup target 为 $(.5,.5,0)$，却与 class C 的真实 target $e_3$ 冲突。可诊断 mixed point 到第三类 nearest-neighbor/support density、teacher/human label、local class posterior 与 loss conflict；class-aware/near-neighbor pairing 是可能缓解而非一般证明。

### NN-MIX-D02
`max` 把有序第一样本权重限制到 $[.5,1]$；只有同步交换 source order 时 unordered mixed point law 才可能保持。Self-pair 增加 exact empirical atoms，实际比例约取决于 permutation；derangement 消除它。Local-rank pairing 受各 rank class mix 限制，global pairing 改 pair-distance/class distribution并增加通信。四者都定义 $Q_{\rm mix}$，应记录而非当作无关实现。

### NN-MIX-D03
先 augment 两端再 mix 与先 mix 后 augment，一般因非线性 transform 不交换；BN 统计来自不同 mixed batch；LN$(\lambda h_i+(1-\lambda)h_j)$ 一般不等于 mixed LNs；不同长度 sequence 的 padding/attention edges 不能只继承一端；在 norm 前后或 residual branch 内选 layer 会改变 suffix 和 backward。公平比较必须锁定 operator order 与 state update。

## E

### NN-MIX-E01
Natural 轨道分别调各方法推荐 $\alpha$/pairing；matched-strength 轨道匹配 $E\lambda(1-\lambda)$、实际 normalized distance和 target entropy；semantic-validity 轨道按同/异类、near/far、第三类 intrusion 分层。固定 model/optimizer/steps/augmentation budget/paired seeds，报告 accuracy/NLL/Brier、classwise/shift risk、distance/entropy、train loss、memory/throughput。三轨回答不同问题，不能只留最佳数字。

### NN-MIX-E02
图像：pixel range、spatial alignment 与 mixed class semantics；回归：target interpolation 与 continuity domain；multi-label：每 component probability、co-occurrence validity 与 BCE；segmentation：pixel mask/box correspondence、area-based $\lambda$；token sequence：embedding位置、length/padding/attention mask 与 token-level loss。每份合同还需 pairing、$\lambda$ axes、augmentation order 和 evaluation distribution。

### NN-MIX-E03
使用相同 backbone、data split、optimizer/steps、base augmentation、paired seeds 与等额 tuning。Input 组只在 raw/embedded input mixing；Manifold 组预声明 eligible layers 与 sampling distribution。记录 mixed distance、target entropy、prefix/suffix activation、BN buffers、peak memory/throughput；对每组分别调 $\alpha$，另做 matched-strength。结论限于所选 layers/representations，不能由一组结果证明 hidden mix 普遍更“语义化”。

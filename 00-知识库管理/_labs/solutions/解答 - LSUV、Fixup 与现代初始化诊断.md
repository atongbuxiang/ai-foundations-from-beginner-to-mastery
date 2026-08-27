---
type: solution
status: draft
area: [neural-networks/initialization, lsuv, fixup, diagnostics]
topic: "[[LSUV、Fixup 与现代初始化诊断]]"
exercise: "[[习题 - LSUV、Fixup 与现代初始化诊断]]"
sources: ["[[S-2016-Mishkin-Matas-LSUV]]", "[[S-2019-Zhang-Dauphin-Ma-Fixup]]", "[[S-2021-Su-8620-Transformer初始化参数化与标准化]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - LSUV、Fixup 与现代初始化诊断

## A

### NN-DIAG-A01
先以 orthogonal/semi-orthogonal weights 预初始化。取 calibration batch，按 network order 对每层反复：前向到当前 output，按声明 axes 测 $\widehat v$，若 $|\widehat v-1|\ge\tau$ 且 trial 未超上限，做
$$W\leftarrow W/\sqrt{\widehat v+\varepsilon}.$$
进入 tolerance 或达到 maximum trials 后进入下一层。Batch、axes、mode、$\tau,\varepsilon,T_{\max}$ 都是算法输入。

### NN-DIAG-A02
有 $L$ 个 residual branches、每 branch $m$ 个 weight layers。Fixup：(1) classification layer 与每 branch 最后 weight layer 置零；(2) 其余层标准初始化，并将 branch 内非零 weights 额外乘 $L^{-1/(2m-2)}$；(3) 每 branch 加初值 1 的 scalar multiplier，并在 convolution/linear/elementwise activation 前加初值 0 的 scalar bias。

### NN-DIAG-A03
Parameter：weight norm/spectrum/bias/gain/dtype；forward：mean/variance/second moment/quantiles/zero/nonfinite；correlation：两输入/空间/token covariance；backward：activation/parameter gradient、JVP/VJP；spectrum：mean $s^2$、rank、extremes/condition proxy；update/system：$\|\Delta W\|/(\|W\|+\epsilon)$、optimizer state、loss scale、AMP、clipping、distributed reduction。

## B

### NN-DIAG-B01
第一次乘数为 $1/\sqrt4=1/2$。第二次 variance 1.21，乘数为 $1/\sqrt{1.21}=1/1.1\approx0.90909$。累计 weight multiplier
$$\frac12\cdot\frac1{1.1}=\frac1{2.2}\approx0.45455.$$
第二次不等于 1 说明 local homogeneity、测量噪声或上游/非线性耦合使一次校准不精确。

### NN-DIAG-B02
$m=3$ 给 exponent $-1/(2m-2)=-1/4$，所以
$$\alpha=64^{-1/4}=\frac1{2\sqrt2}\approx0.353553.$$
两个非零 weights 的 product scale 是
$$\alpha^2=64^{-1/2}=1/8=0.125.$$
第三个（末）weight 是 exact zero；product scale 的 $1/8$ 是末层开始学习后的 depth-aware amplitude 直觉。

### NN-DIAG-B03
取 denominator $\|W\|+10^{-3}$：
$$\rho_1=0.1/10.001\approx0.009999,$$
$$\rho_2=0.02/1.001\approx0.01998,$$
$$\rho_3=0.003/0.001=3.$$
Zero layer 的 ratio 被 arbitrary $\epsilon$ 主导，不能与非零层直接作相对变化解释；应同时报告 absolute update、参考 fan scale、下一步 parameter norm 与为何该层有意从 zero 启动。

## C

### NN-DIAG-C01
若当前 layer output 对正 scalar $a$ 满足 $H(aW)=aH(W)$，则
$$\operatorname{Var}(H(aW))=a^2\operatorname{Var}(H(W)).$$
取 $a=1/\sqrt v$ 得新 variance 约 1。证明在 nonzero bias、saturating activation、normalization、multi-branch interaction、finite-batch estimator noise 或不正齐次算子处断裂，所以 LSUV 需要迭代与停止上限。

### NN-DIAG-C02
直接计算
$$\left(L^{-1/(2m-2)}\right)^{m-1}
=L^{-(m-1)/(2(m-1))}=L^{-1/2}.$$
若 branch amplitude 是 $O(L^{-1/2})$，平方尺度为 $O(1/L)$；在近不相关加和近似下，$L$ 个 branch contributions 的总平方尺度仍为 $O(1)$。Cross covariance、nonlinearity 与 update dynamics 需另行分析。

### NN-DIAG-C03
Step 0 时 last branch weight 为 0，但其输入 activation 通常非零，所以 last weight gradient 非零；更早 weight gradients需反向乘 last zero weight，通常为 0。Step 1 后 last weight 非零，上游 branch layers 开始获得梯度。串行全零 MLP 没有 identity skip，网络主路径与多层 backward 都被零链切断；Fixup 则保留 $x\mapsto x$。

## D

### NN-DIAG-D01
LSUV 只在初始化的 calibration batch 上一次性重缩放 weights；之后不持续使用 batch mean/variance，也没有 running statistics 或 train/eval 替换。它通常不中心化 mean，不保证 backward/full spectrum，也会随 training drift。因此它最多与“一次 batch 的 unit-variance 校准”相似，不等价于 BatchNorm 的运算与优化效应。

### NN-DIAG-D02
Zero-last 让初始 block 近 identity，但 Fixup 还要求 branch 内其余 weights 的 $L^{-1/(2m-2)}$ depth scaling，以及 scalar multiplier/bias 的参数化；原论文指出 depth-aware scaling 是关键机制。只做 zero-last 会改变第一步路径，却未校准随后 $L$ 个 branch updates 的累计尺度，也不是完整复现实验。

### NN-DIAG-D03
谱反例取
$$J_\varepsilon=\operatorname{diag}(\sqrt{2-\varepsilon^2},\varepsilon),$$
其 mean squared gain 为 1，故 isotropic forward second moment 看似正常，但 $s_{\min}=\varepsilon$、condition number 发散。Update 反例可取一个 norm 为 $10^{-6}$ 的参数与 update $10^{-3}$：activation variance 由其他 path 保持正常，但相对 update 已极大。二者说明 forward dashboard 不能替代 spectrum/update 层。

## E

### NN-DIAG-E01
使用多个 representative calibration batches，分别改变 batch size、augmentation、class mix；明确 variance axes（global/per-channel/token）、biased/unbiased estimator；比较 train/eval、dropout on/off；扫描 $\tau,\varepsilon,T_{\max}$。记录每层 trials、最终 variance、weight multiplier 与另一 held-out batch 上的 variance。若 calibration batch 合格而 held-out 明显偏离，应把结论限制为分布/批次特定校准。

### NN-DIAG-E02
四组：完整 Fixup、删除 zero-last/classifier rule、删除 depth scaling、删除 scalar multiplier/bias；另设 standard He baseline。固定 architecture/depth/width、optimizer/LR schedule、regularization、data order、dtype 与 paired seeds。记录 branch output/update、layerwise gradient、nonfinite/clipping、early loss 与 final metric。Ablation 只说明该设置中 component 的边际作用，不能推出所有 residual architectures 的必要性。

### NN-DIAG-E03
执行顺序：(1) 核对 parameter shape/fan/layout/dtype；(2) dry run 前向 mean/q/variance/quantile/nonfinite；(3) 两输入 correlation；(4) fixed-loss backward/JVP/VJP；(5) spectrum/rank/extremes；(6) step-0/1 update ratio 与 AMP/distributed semantics。找到最浅的异常层并映射机制：fan/gain、bias、branch addition、derivative mask、optimizer scale 或 precision。只修改相应局部因素，重跑所有上游/下游指标与多 seed training；不得用最终 loss 单独掩盖初始化失效。

---
type: solution
status: draft
topic: "[[习题 - 神经网络容量与 Norm-Based Bound]]"
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - 神经网络容量与 Norm-Based Bound
## A
### LT-NNB-A01
architecture capacity 对整个网络类取最坏情况，常由参数量、深度或 VC/pseudodimension 控制；solution-dependent capacity 把训练后的 norm、margin、reference weight 或 posterior 纳入，只控制更小的局部/数据依赖类。前者更统一，后者可能更贴近算法实际输出。
### LT-NNB-A02
spectral norm 控制某层对向量的最坏放大，跨层以乘积传播；Frobenius norm 记录全部奇异方向能量，与 spectral norm 的比值产生 effective-direction/stable-rank 因子。两者不能互换。
### LT-NNB-A03
$\operatorname{srank}(W)=\|W\|_F^2/\|W\|_2^2=\sum_j\sigma_j^2/\sigma_1^2$。每个非零奇异值的贡献至多 1，故 stable rank 不超过 rank，且弱奇异值只按相对平方能量计数。
## B
### LT-NNB-B01
Lipschitz 上界为 $2\cdot3=6$。若激活满足 $\phi(0)=0$，则 $\|f(x)\|\le B\cdot6=24$。
### LT-NNB-B02
$\|W\|_F^2=16+4+4=24$，$\|W\|_2^2=16$，所以 stable rank $=24/16=3/2$。
### LT-NNB-B03
$\mathcal C(W)=1\cdot6\cdot\sqrt9=18$。真正风险项还要除以 $\gamma\sqrt n$ 并补 logarithmic/confidence factors。
## C
### LT-NNB-C01
每层 $h_\ell=\phi(W_\ell h_{\ell-1})$ 满足 $\|h_\ell(x)-h_\ell(x')\|\le\|W_\ell\|_2\|h_{\ell-1}(x)-h_{\ell-1}(x')\|$。迭代 $L$ 次即得 $\|f(x)-f(x')\|\le(\prod_\ell\|W_\ell\|_2)\|x-x'\|$。
### LT-NNB-C02
构造从 $W$ 到 $W+U$ 的 $L+1$ 个中间网络，每一步只替换一层；每个差值由该层 $\|U_\ell\|$、其前 activation 上界和其后层增益乘积控制。把全层 spectral-product 提出后，剩下 $\|U_\ell\|_2/\|W_\ell\|_2$，最后对层求和。
### LT-NNB-C03
predictor 因 ReLU 正齐次性不变。相邻两层 spectral norms 分别乘 $c$ 与 $c^{-1}$，故总乘积不变；每层 $\|cW\|_F^2/\|cW\|_2^2$ 也不变，因此整个示意复杂度不变。
## D
### LT-NNB-D01
参数量只给 architecture worst-case capacity；训练算法可能选择小 norm/大 margin 的子类。反过来，参数多也不保证泛化好。需要同时指定 algorithm、trained solution、data、risk 和 bound，而不是参数数单调律。
### LT-NNB-D02
相关性可能由 learning rate、margin、data scale 或 parameterization 共同驱动；还可能发生 post-hoc metric selection。必须先做不变性检验，再在 held-out sweep 上复验，并用保持 predictor/训练误差近似不变的干预改变复杂度，才接近机制证据。
### LT-NNB-D03
二分类 risk 的平凡上界是 1；右端大于 1 没排除任何可能 risk，故没有数值信息。它可保留为依赖结构的定性 theorem，但不能称为该模型的 nonvacuous certificate。
## E
### LT-NNB-E01
报告 data unit/$B$、block 定义、每个 convolution/residual operator-norm 算法与误差、Frobenius/stable rank、margin CDF、$n,\delta$、精确 theorem/constants、normalization/bias 处理、bound 数值、超参选择修正、test risk 和等价重缩放 stress test。
### LT-NNB-E02
选 ReLU 网络，对相邻层施加一组 $c,c^{-1}$，保持函数与 predictions 数值一致；测 raw Hessian sharpness、raw norm 和 spectral complexity。若前两者大幅变化而后者/风险稳定，说明前者含坐标伪影；再做非等价干预检验指标是否预测真实 risk 变化。
### LT-NNB-E03
claim card：data/algorithm/network/margin 定义；准确 theorem 与概率空间；输入/层 norm 上界和估计误差；复杂度及 confidence/union correction；超参数/指标 post-selection 处理；数值 nonvacuity；尺度与参数化 stress test；ID/OOD 适用域；可推翻 prediction。


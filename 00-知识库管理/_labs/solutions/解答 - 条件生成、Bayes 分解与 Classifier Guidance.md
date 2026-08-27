---
type: solution
status: draft
topic: "[[条件生成、Bayes 分解与 Classifier Guidance]]"
exercise: "[[习题 - 条件生成、Bayes 分解与 Classifier Guidance]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - 条件生成、Bayes 分解与 Classifier Guidance
## A. 识别与复述
### GEN65-A01
$\nabla_x\log p_t(x\mid y)=\nabla_x\log p_t(x)+\nabla_x\log p_t(y\mid x)$。要求相关密度在考察点为正、关于 $x$ 可微且 $p_t(y)$ 不依赖 $x$；边界/零密度点需改用支持内或弱形式。
### GEN65-A02
采样的大部分状态是 $x_t$，其分布随噪声层变化。干净分类器在高噪声输入上属于分布外调用，logit 值、校准和输入梯度都未受训练约束，可能给出巨大但无语义的方向。
### GEN65-A03
score modification 是概率恒等式层；reverse drift 要把 score 乘 $-g^2$ 或 $-g^2/2$；离散 Gaussian kernel 则在局部线性近似下把均值平移 $\Sigma g_y$。三者对象和系数不同。
## B. 手算与建模
### GEN65-B01
指数分母 $8=2\tau^2$，故 $\tau^2=4,a=2$。$\mu_w=2w/(4+w)$、$\sigma_w^2=4/(4+w)$。$w=1$ 时 $(.4,.8)$；$w=3$ 时 $(6/7,4/7)$。
### GEN65-B02
$w\Sigma g=.5\operatorname{diag}(1,4)(2,-1)=(1,-2)$。guided mean 为 $\mu+(1,-2)$。
### GEN65-B03
$g^2=4$。reverse SDE drift 增量为 $-4w\nabla\log p_t(y\mid x)$；PF-ODE 为 $-2w\nabla\log p_t(y\mid x)$。实际从 $T$ 积到 0 时步长符号由 solver 处理。
## C. 推导与证明
### GEN65-C01
$p(x\mid y)=p(x)p(y\mid x)/p(y)$；取 log 后三项相加减；对 $x$ 求梯度，$\nabla_x\log p(y)=0$，余下两项即结论。
### GEN65-C02
写 $z=x-\mu$，指数为 $-\frac12z^T\Sigma^{-1}z+g^Tz$。加减 $\frac12g^T\Sigma g$，得到 $-\frac12(z-\Sigma g)^T\Sigma^{-1}(z-\Sigma g)+C$，故均值平移 $\Sigma g$、协方差不变。
### GEN65-C03
$\nabla\log[p(x)p(y\mid x)^w]=\nabla\log p(x)+w\nabla\log p(y\mid x)$。还需 $Z_w=\int p(x)p(y\mid x)^w dx$ 有限且正，才能归一化为概率密度。
## D. 边界、反例与纠错
### GEN65-D01
分类 loss 只约束训练样本上的 logit/概率，存在函数值相近但输入梯度完全不同的分类器；对抗样本就是反例。需额外检查 noisy calibration、gradient norm/direction、平滑性与对扰动稳定性。
### GEN65-D02
pixel gradient 位于 $\mathbb R^{H\times W\times C}$，latent 位于另一空间且尺度不同。要么训练 latent classifier，要么通过 decoder $D$ 用 $J_D(z)^T\nabla_x\log p(y\mid D(z))$ 拉回；直接相加 shape/几何均错误。
### GEN65-D03
$w=1$ 才对应普通 conditional score；$w>1$ 对 likelihood 做幂倾斜，目标变成更集中的 tilted distribution，还叠加模型与 finite-step 误差。
## E. AI 迁移
### GEN65-E01
在每个噪声层记录 accuracy/ECE、logit 与输入梯度范数；用 finite difference 检查梯度；对语义保持/破坏扰动测方向；检查高噪声时预测回到类别先验；对抗优化后做人类/任务审核。
### GEN65-E02
列：$w$、FID/KID、precision、recall、条件准确/相似度、人评、梯度范数、clipping rate、denoiser NFE、classifier forward/backward、latency、memory、seed/CI。
### GEN65-E03
固定 prediction type；代入零 scale；用 toy quadratic classifier 检查方向；核对 score-to-output 换算与 $g^2/\Sigma$；固定负步长时间方向；与极小步 Euler 的手算结果对照。

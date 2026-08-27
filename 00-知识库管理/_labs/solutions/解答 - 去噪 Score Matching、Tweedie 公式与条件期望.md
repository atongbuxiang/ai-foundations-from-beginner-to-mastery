---
type: solution
status: draft
topic: "[[去噪 Score Matching、Tweedie 公式与条件期望]]"
exercise: "[[习题 - 去噪 Score Matching、Tweedie 公式与条件期望]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - 去噪 Score Matching、Tweedie 公式与条件期望
## A. 识别与复述
### GEN28-A01
$Y=X+\sigma\varepsilon$，$\varepsilon\sim N(0,I)$；$q(y|x)=N(x,\sigma^2I)$；conditional score 为 $-(y-x)/\sigma^2$；$p_\sigma(y)=\int p_0(x)q(y|x)dx$。
### GEN28-A02
$E[\nabla_Y\log q(Y|X)|Y]=\nabla_Y\log p_\sigma(Y)$。令 $U$ 为 conditional score，则 $E\|U-s(Y)\|^2=E\|U-E[U|Y]\|^2+E\|E[U|Y]-s(Y)\|^2$。
### GEN28-A03
$E[X|Y=y]=y+\sigma^2s_\sigma(y)$；若预测噪声，$s=-\varepsilon/\sigma$；clean prediction $\hat x=y-\sigma\varepsilon=y+\sigma^2s$。
## B. 手算与建模
### GEN28-B01
对称性给 $P(X=a|Y=0)=P(X=-a|Y=0)=1/2$，故 posterior mean 为 0。Tweedie 给 $s_Y(0)=(0-0)/\sigma^2=0$。这同时展示低密度对称点 score 也可为零。
### GEN28-B02
$Y\sim N(0,\tau^2+\sigma^2)$，故 $s_Y(y)=-y/(\tau^2+\sigma^2)$。Tweedie 给 $E[X|Y=y]=y[1-\sigma^2/(\tau^2+\sigma^2)]=\tau^2y/(\tau^2+\sigma^2)$。
### GEN28-B03
$s=-0.4/0.5=-0.8$。$\hat x=y-\sigma\varepsilon=1.2-0.5(0.4)=1.0$；也可用 $1.2+0.25(-0.8)=1.0$ 核对。
## C. 推导与证明
### GEN28-C01
$\nabla p_\sigma(y)=\int p_0(x)\nabla q(y|x)dx=\int p_0q\nabla\log q,dx$。除以 $p_\sigma(y)$ 后，$p_0(x)q(y|x)/p_\sigma(y)=p(x|y)$，即得条件期望。
### GEN28-C02
写 $U-s=(U-E[U|Y])+(E[U|Y]-s)$。平方展开后交叉项条件期望为零，因为 $E[U-E[U|Y]|Y]=0$，故得到正交分解；第一项不依赖 $s$。
### GEN28-C03
Gaussian likelihood score 为 $\nabla_y\log q(y|x)=-\Sigma^{-1}(y-x)$。取给定 $Y=y$ 的条件期望并等于 marginal score，得到 $s_Y(y)=-\Sigma^{-1}(y-E[X|y])$；左乘 $\Sigma$ 重排即可。
## D. 边界、反例与纠错
### GEN28-D01
上一题 $Y=0$ 时 posterior mean 为 0，但真实 $X$ 必为 $\pm a$；条件均值甚至不在 clean support 上。MSE 最优是平均意义，不是样本身份恢复。
### GEN28-D02
等价是 population、平方可积、同一 weighting 下的 unrestricted optimum。有限函数类、参数化 conditioning、target scale、optimization noise 和 regularization 会产生不同梯度场与近似误差。
### GEN28-D03
$\sigma^2$ 来自 Gaussian location likelihood 的线性 score $-\Sigma^{-1}(y-x)$。Laplace likelihood score 是分段常数 sign 形式，posterior moment 与 marginal score 的关系不同，必须重新推导。
## E. AI 迁移
### GEN28-E01
对可解析二维 mixture：采样大量 $X,Y$；网格上精确算 mixture $p_\sigma$ 及梯度；bin/kernel regression 估 $E[X|Y=y]$；检验残差 $E[X|y]-y-\sigma^2s(y)$，并随样本量/带宽报告误差。
### GEN28-E02
确保相同 noisy inputs、network/preconditioning、optimizer、batch、NFE；把 $s=-\varepsilon/\sigma$ 的 target scaling 和 loss weight 映射完整；评价时用同一 sampler 将输出统一转换，不能让一种参数化隐含不同权重。
### GEN28-E03
训练 target $-(Y-X)/\sigma^2$ 由干净样本与人工噪声直接得到，不需从当前模型抽样。生成时只有 score vector field，没有 one-pass pushforward，仍需 Langevin、reverse SDE/ODE 等动态把易采样 prior 搬到数据分布。


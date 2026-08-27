---
type: solution
status: draft
topic: "[[多噪声尺度、退火去噪与 Score 网络]]"
exercise: "[[习题 - 多噪声尺度、退火去噪与 Score 网络]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - 多噪声尺度、退火去噪与 Score 网络
## A. 识别与复述
### GEN29-A01
原分布若对环境 Lebesgue measure 奇异，$\log p_0$ 不存在。与 full-rank Gaussian 卷积后，$p_\sigma(y)=\int p_0(dx)\varphi_\sigma(y-x)$ 对 $\sigma>0$ 通常正且光滑，从而环境空间 score 可定义；代价是学习对象变为平滑分布。
### GEN29-A02
$\sum_i\lambda_iE\|s_\theta(X+\sigma_i\varepsilon,\sigma_i)+\varepsilon/\sigma_i\|^2$。抽到哪个 $i$ 的概率决定样本分配；$\lambda_i$ 决定抽到后对 objective 的权重，两者相乘才决定期望贡献。
### GEN29-A03
报告 $p_T$/初始分布、$\{\sigma_i\}$、从大到小顺序、每层 $K_i$、$\alpha_i$ 及缩放规则、随机噪声约定、网络 conditioning、最后 denoise/clip。还要给总 NFE 与 temperature。
## B. 手算与建模
### GEN29-B01
比例 $r=(1/8)^{1/3}=1/2$，故序列为 $8,4,2,1$。
### GEN29-B02
$E\|\varepsilon/\sigma\|^2=d/\sigma^2$。取 $\lambda(\sigma)\propto\sigma^2$ 可使 target 的期望平方尺度近似相同；但不保证参数梯度方差相同。
### GEN29-B03
对称 density 满足 $p_\sigma(x)=p_\sigma(-x)$，故导数在 0 为 0，score $p'/p$ 也为 0。若两峰分离，0 处二阶导数可为正、是局部 valley；一阶零点不区分 max/min/saddle。
## C. 推导与证明
### GEN29-C01
$Y=X+\sigma\varepsilon$ 的密度由全概率公式为 $\int p_0(x)\varphi_\sigma(y-x)dx$，即卷积。若 $p_0=\sum_jw_j\delta_{\mu_j}$，则 $p_\sigma(y)=\sum_jw_j\varphi_\sigma(y-\mu_j)$。
### GEN29-C02
令公比 $r$ 满足 $\sigma_{max}r^{L-1}=\sigma_{min}$，所以 $r=(\sigma_{min}/\sigma_{max})^{1/(L-1)}$，$\sigma_i=\sigma_{max}r^{i-1}$。
### GEN29-C03
给定 $s,z$，ratio 为 $\alpha\|s\|/(\sqrt{2\alpha}\|z\|)=\sqrt{\alpha/2}\|s\|/\|z\|$。若 score norm 随尺度约为 $1/\sigma$，维持 ratio 会提示 $\alpha\propto\sigma^2$；真实 learned score、维度和数据几何不同，因此只是 heuristic。
## D. 边界、反例与纠错
### GEN29-D01
对称双峰中点有 score 0，却可处于极低密度 valley。任何 stationary point 都满足局部 score 0，需 density/Hessian/全局结构判别。
### GEN29-D02
最小噪声虽 bias 小，却可能 support 近奇异、训练 target scale 大、低密度区域样本少，sampler 也难跨越模式。大噪声层提供全局连接和易初始化路径。
### GEN29-D03
映射 $x\mapsto x+\sigma^2s(x)$ 是确定性 posterior-mean transport；pushforward 分布一般与输入 $p_\sigma$ 不同，也未必等于 $p_0$，多模态 posterior 下还会平均。
## E. AI 迁移
### GEN29-E01
用两峰 Gaussian 真 score；同等总 NFE 比较：仅 $\sigma_{min}$ 链与几何 ladder。多初值/seed 报左右模式比例、跨峰次数、Wasserstein/TV、autocorrelation 和最终 density bias，扫描峰距与步长。
### GEN29-E02
训练：$\sigma_{min/max}$、levels、sampling $p(i)$、$\lambda_i$、parameterization、network embedding、data scaling。采样：prior、每层 steps、步长/噪声、SNR rule、总 NFE、最后 denoise/clip、seed 和 batch。
### GEN29-E03
做三组 compute-matched：单尺度与多尺度同 NFE；多尺度但每层从共同初始化重启以删除 warm start；相同 trained multi-score 网络只改 sampler ladder。再做相同 sampler 比较单/多尺度训练，分别隔离训练覆盖与路径作用。


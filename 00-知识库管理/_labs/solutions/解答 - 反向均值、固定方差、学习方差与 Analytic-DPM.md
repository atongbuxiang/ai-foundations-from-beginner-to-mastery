---
type: solution
status: draft
topic: "[[反向均值、固定方差、学习方差与 Analytic-DPM]]"
exercise: "[[习题 - 反向均值、固定方差、学习方差与 Analytic-DPM]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - 反向均值、固定方差、学习方差与 Analytic-DPM
## A. 识别与复述
### GEN45-A01
Forward variance 属于 $q(x_t|x_{t-1})=N(\sqrt{\alpha_t}x_{t-1},\beta_tI)$；closed posterior variance 属于 $q(x_{t-1}|x_t,x_0)$，为 $\tilde\beta_tI$；model variance 属于 $p_\theta(x_{t-1}|x_t)$，可固定或由网络预测为 $\sigma^2_{\theta,t}(x_t)$。三者 conditioning、用途和可见信息均不同。
### GEN45-A02
$s_*^2(x_t)=d^{-1}E[\|Y-\mu_\theta(x_t)\|^2|x_t]$，其中 $Y=X_{t-1}|x_t$。它等于 $d^{-1}\operatorname{tr}\operatorname{Cov}(Y|x_t)+d^{-1}\|E[Y|x_t]-\mu_\theta\|^2$：第一项是不可约条件不确定性，第二项是模型均值误差。
### GEN45-A03
解析 identity 假设理想 score；实际网络只给近似 score；期望通常靠有限样本估计；clipping/bounds 又改变 estimator；最终 metric 还受步数、数据与 sampler 影响。把这些层混成“解析且最优”会隐藏 approximation、sampling variance 和算法 bias。
## B. 手算与建模
### GEN45-B01
$\tilde\beta_t=0.1(1-0.8)/(1-0.72)=0.02/0.28=1/14\approx0.07143<0.1$。较小来自知道 $x_0$ 后的不确定性减少。
### GEN45-B02
$\operatorname{tr}\operatorname{Cov}=1.25$，mean error 为 $(1, -0.5)$，平方范数 $1.25$。故 $s_*^2=(1.25+1.25)/2=1.25$。若逐维允许不同方差，结果会是 $(0.25+1^2,1+(-0.5)^2)=(1.25,1.25)$，本例恰好相等。
### GEN45-B03
$\sigma^2=\beta^{0.25}\tilde\beta^{0.75}=0.02^{0.25}0.005^{0.75}=0.005\,4^{0.25}\approx0.007071$。log-space 插值对应几何平均而非算术平均。
## C. 推导与证明
### GEN45-C01
令 $A=E[\|Y-\mu\|^2|x_t]$，去掉常数后 $R(u)=\frac d2\log u+\frac{A}{2u}$，$u=s^2>0$。$R'(u)=d/(2u)-A/(2u^2)$，故 $u_*=A/d$。$R''(u)=-d/(2u^2)+A/u^3$；代入 $A=du_*$ 得 $R''(u_*)=d/(2u_*^2)>0$。且 $R(u)\to\infty$ 于 $u\to0^+$ 或 $u\to\infty$，故为全局极小。
### GEN45-C02
对 $Y=X_{t-1}$ 用 conditional total covariance：$\operatorname{Cov}(Y|x_t)=E[\operatorname{Cov}(Y|x_t,x_0)|x_t]+\operatorname{Cov}(E[Y|x_t,x_0]|x_t)$。第一项是 $\tilde\beta_tI$；第二项是 posterior mean 随 $x_0|x_t$ 变化产生的 mixture covariance，通常非零。
### GEN45-C03
$\tilde\beta_t/\beta_t=(1-\bar\alpha_{t-1})/(1-\alpha_t\bar\alpha_{t-1})$。分母减分子为 $\bar\alpha_{t-1}(1-\alpha_t)=\bar\alpha_{t-1}\beta_t\ge0$，故比值不超过 1。若 $\bar\alpha_{t-1}>0$ 且 $\beta_t>0$ 则严格小于；退化端点可相等。
## D. 边界、反例与纠错
### GEN45-D01
$\tilde\beta_tI$ 是进一步知道 $x_0$ 的 component posterior covariance。移除 $x_0$ 后，$q(x_{t-1}|x_t)$ 是对 $x_0|x_t$ 的混合，除 component variance 外还有 component means 的方差；非 Gaussian 数据下整体甚至不一定是单一 Gaussian。
### GEN45-D02
令真实 $Y|x_t=N(10,0.01)$，模型均值固定为 0。把 variance 从 0.01 学到约 $100.01$ 可改善相对过度自信的 NLL，却仍以 0 为中心；其 samples 大量落在错误区域，均值偏差 10 未消失。因此 variance 只能吸收 residual，不会把中心移到 10。
### GEN45-D03
对象改变为 $\Sigma=\operatorname{diag}(s_1^2,\ldots,s_d^2)$ 时，最优每维为 $s_i^{2*}=E[(Y_i-\mu_i)^2|x_t]$；isotropic optimum 是这些值的平均。若允许 full covariance，最优为 conditional residual second-moment matrix，还必须处理正定性与参数化。
## E. AI 迁移
### GEN45-E01
固定同一 checkpoint/mean head、preprocessing、schedule、time grid、初始 noises 与 evaluator，只替换 reverse variance；learned 方法统一训练预算并报告额外参数/目标。同时报告 NLL/VLB、FID 或任务质量、coverage、stepwise residual calibration、NFE 与 wall time，多 seed 配对比较。
### GEN45-E02
至少记录理想 identity 的假设、score checkpoint/error proxy、时间抽样 proposal 与 correction、Monte Carlo 样本数/seed、estimator variance、clipping 阈值和触发率、理论 bound 的适用条件、每时刻估计值及最终 metric。误差账分 approximation bias、MC variance、clipping bias 与 finite-step sampling error。
### GEN45-E03
构造已知 $Y|x$ mean/variance 的 heteroscedastic toy data；分别训练高容量与故意受限 mean head，再训练 variance head。比较 $\hat s^2$ 与真实 conditional variance、mean-squared bias 的和；若受限 mean 下 variance 随 mean error 增长，而 oracle mean 下回落到真实方差，就支持“补偿 mean error”的解释。

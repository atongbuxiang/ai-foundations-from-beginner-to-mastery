---
type: solution
status: draft
topic: "[[逆问题、约束采样与 Plug-and-Play 控制]]"
exercise: "[[习题 - 逆问题、约束采样与 Plug-and-Play 控制]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - 逆问题、约束采样与 Plug-and-Play 控制
## A. 识别与复述
### GEN67-A01
$p(x_0\mid y)\propto p_0(x_0)p(y\mid x_0)$；$\nabla_{x_t}\log p_t(x_t\mid y)=s_t(x_t)+\nabla_{x_t}\log p_t(y\mid x_t)$。
### GEN67-A02
观测由 $x_0$ 产生。条件在 $x_t$ 上要积分不确定的 $x_0$：$p(y\mid x_t)=\int p(y\mid x_0)p(x_0\mid x_t)dx_0$。直接替换等于改变 measurement graph。
### GEN67-A03
likelihood guidance 加近似 posterior score；projection 强制进入可行集；prox 在 data loss 与当前点间软折中；PnP 把 denoiser 当 prior operator，其 fixed point 不必是显式 posterior。
## B. 手算与建模
### GEN67-B01
残差 $y-Ax=2$。梯度 $A^T(2)/2=A^T=(1,2)^T$。
### GEN67-B02
分母 $.8^2+.6^2=1$，故 $k=.8,c=.36$。$\operatorname{Var}(y\mid x_t)=.25+4(.36)=1.69$。
### GEN67-B03
一阶条件 $(x-y)+(x-z)/\lambda=0$，故 $\operatorname{prox}_{\lambda g}(z)=(z+\lambda y)/(1+\lambda)$。
## C. 推导与证明
### GEN67-C01
对 latent $x_0$ 用全概率：$p(y\mid x_t)=\int p(y,x_0\mid x_t)dx_0=\int p(y\mid x_0,x_t)p(x_0\mid x_t)dx_0$；图模型给 $y\perp x_t\mid x_0$，得到结论。
### GEN67-C02
$x_0\mid x_t\sim N(kx_t,c)$，线性 Gaussian 传播给 $y\mid x_t\sim N(akx_t,\sigma_y^2+a^2c)$。对 $x_t$ 求 log-density 梯度为 $ak(y-akx_t)/(\sigma_y^2+a^2c)$；plug-in 去掉 $a^2c$。
### GEN67-C03
$\ell=-\|y-A\hat x_0(x_t)\|^2/(2\sigma_y^2)$。先对 $\hat x_0$ 求梯度 $A^T(y-A\hat x_0)/\sigma_y^2$，再乘 Jacobian transpose $J_{\hat x_0}^T$。
## D. 边界、反例与纠错
### GEN67-D01
$y=x_0+\eta$ 且 $\eta\ne0$。投影集合 $x=y$ 只含带噪观测；hard projection 必令重建等于 $y$，把噪声完整保留，而 posterior mean 会在 prior 与 $y$ 间收缩。
### GEN67-D02
detach 把 $J_{\hat x_0}$ 置零或替换为另设 surrogate，实际 correction 不再是 composite likelihood 的 chain-rule gradient。value 相同但程序梯度不同。
### GEN67-D03
残差只测 likelihood fit。噪声模型允许非零残差，posterior 还乘 prior；极小残差样本可能离开数据 manifold、复制噪声或覆盖单一 mode。
## E. AI 迁移
### GEN67-E01
随机 $u,v$ 检查 $\langle Au,v\rangle=\langle u,A^Tv\rangle$；再对 composite likelihood 沿随机方向用中心差分，与 autograd VJP 点积比较，扫步长看二阶收敛区。
### GEN67-E02
记录 operator/noise、prior checkpoint、$\hat x_0$/clipping/detach、correction schedule、sampler/NFE；报告 residual、PSNR/感知、多个 posterior samples、coverage/credible interval calibration 与 misspecification。
### GEN67-E03
假设方差缩为真实的一半，likelihood gradient 约放大四倍（若“标准差减半”），样本会更贴观测、覆盖变窄并过拟合噪声。固定 seeds 扫 assumed noise，比较 residual、真实误差与 interval coverage。

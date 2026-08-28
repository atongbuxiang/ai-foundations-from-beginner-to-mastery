---
type: solution
status: draft
topic: "[[NTK、Lazy Training 与 Kernel Regime]]"
exercise: "[[习题 - NTK、Lazy Training 与 Kernel Regime]]"
created: 2026-08-23
updated: 2026-08-28
---
# 解答 - NTK、Lazy Training 与 Kernel Regime
## A
### LT-NTK-A01
$K_\theta(x,x')=\langle\nabla_\theta f_\theta(x),\nabla_\theta f_\theta(x')\rangle$。训练集上 $K=JJ^T$；任意 $v$ 有 $v^TKv=\|J^Tv\|^2\ge0$，故半正定。
### LT-NTK-A02
NNGP 是随机初始化下函数值的 covariance kernel，描述初始化函数分布；NTK 是参数梯度 Gram，描述 gradient training 的 tangent dynamics。它们可由同一 architecture 诱导，但一般数值和递推式不同。
### LT-NTK-A03
需证明训练路径上 Jacobian/Gram 几乎不变，即 $K_t\approx K_0$，并控制 nonlinear Taylor remainder。大宽度浓缩只说明 $K_0$ 接近极限核，尚不足以说明整个训练期间固定。
## B
### LT-NTK-B01
$r_t=e^{-K_0t}r_0=(e^{-2t},e^{-t/2})^T$。第二个小 eigenvalue 模式衰减更慢。
### LT-NTK-B02
由 $e^{-0.1t}\le0.01$，得 $t\ge\log100/0.1=10\log100\approx46.052$。
### LT-NTK-B03
$K^{-1}(y-f_0(X))=(1,3)^T$，左乘 $(1,1)$ 得 $4$，所以 $f_\infty(x)=f_0(x)+4$。
## C
### LT-NTK-C01
$\nabla_\theta L=J_t^T(f_t-y)$，故 $\dot\theta=-J_t^T(f_t-y)$。链式法则给 $\dot f_t=J_t\dot\theta=-J_tJ_t^T(f_t-y)=-K_t(f_t-y)$。
### LT-NTK-C02
令 $r_t=f_t-y$，固定核时 $\dot r=-K_0r$。常系数线性 ODE 的唯一解为 $r_t=e^{-K_0t}r_0$；在 eigenbasis 中逐坐标为 $e^{-\lambda_jt}$。
### LT-NTK-C03
$\dot f_t(x)=-k_0(x,X)r_t$。积分 $0$ 到 $\infty$：$f_\infty(x)-f_0(x)=-k_0\int_0^\infty e^{-K_0t}r_0dt=-k_0K_0^{-1}r_0=k_0K_0^{-1}(y-f_0(X))$。
## D
### LT-NTK-D01
指数下降只控制 training residual；test prediction 还需 kernel eigenfunction/target alignment、noise、regularization 与 distribution assumptions。甚至插值时 $K^{-1}$ 可放大小 eigenvalue noise。
### LT-NTK-D02
坐标重缩放可让同一函数路径的 parameter movement 任意改变。更直接证据是 kernel drift、linearization prediction error 与 feature covariance drift，并要注明各指标的 invariance。
### LT-NTK-D03
参数量大没有指定宽度极限、初始化方差、NTK parameterization、learning-rate/time scaling，也没证明 $K_t\approx K_0$。实际大模型可发生显著 feature learning，因此结论不成立。
## E
### LT-NTK-E01
跨宽度/seed 同时测 $\|K_t-K_0\|_F/\|K_0\|_F$、真实输出与线性化输出差、训练 residual eigenmode、activation/CKA drift、parameter movement、NTK predictor 与网络 test prediction 差；锁定 learning-rate scaling 与训练时间，并给 finite-width confidence interval。
### LT-NTK-E02
采用 pretrain–transfer 任务，使 downstream label 依赖预训练中需形成的新语义 partition；比较 analytical/empirical NTK、frozen random features、finite network 与 frozen learned features。若有限网络形成可迁移表示而 NTK/随机 features 失败，则支持 rich feature mechanism。
### LT-NTK-E03
claim card：architecture/parameterization/init；width、time、step 的极限顺序；$K_0$ concentration 与最小特征值；训练期 kernel drift/Taylor remainder；finite-width/time error；优化收敛结论；单独的 kernel risk assumptions；NNGP/NTK 区分；可证伪阈值。

---
type: derivation
status: verified
area: [generative-models, diffusion, numerical-analysis, solvers]
node_id: GEN-68
prerequisites: ["[[Euler、Runge-Kutta 与离散化误差]]", "[[常微分方程、初值问题与解的存在唯一性]]", "[[SDE、概率流 ODE 与 Flow Matching MOC]]"]
related: ["[[扩散蒸馏、一致性模型与 Shortcut]]", "[[平均速度、MeanFlow 与有限步生成]]"]
sources: ["[[S-2022-Lu-DPM-Solver]]", "[[S-2023-Su-9881-中值定理加速ODE采样]]", "[[S-2024-Su-10077-Skip-Tuning]]"]
exercises: ["[[习题 - 扩散 SDE、ODE Solver、步长与 NFE 总账]]"]
solutions: ["[[解答 - 扩散 SDE、ODE Solver、步长与 NFE 总账]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-diffusion-solver-error-nfe-ledger-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 扩散 SDE、ODE Solver、步长与 NFE 总账

> [!abstract] 一句话结论
> solver 只是在有限网格上近似一个给定动力学。Euler、Heun 和 DPM-Solver 的阶数描述 oracle field 的离散误差；真实生成还叠加 learned score/velocity error、terminal mismatch、guidance、随机噪声和浮点误差。公平比较必须以网络函数评估次数 NFE、wall-time 和相同质量/覆盖协议共同记账。

## 一、先固定被求解的方程

ODE sampler 写成

$$
\frac{dx}{dt}=v_\theta(x,t),
\qquad x(T)\sim p_T,
$$

从 $T$ 积到 $0$。令网格

$$T=t_N>t_{N-1}>\cdots>t_0=0,$$

有符号步长

$$h_n=t_{n-1}-t_n<0.$$

以下公式都用 $x_n\approx x(t_n)$ 与 $h_n$，这样不再手工添加“反向负号”。

## 二、精确积分式是所有 solver 的起点

$$
x(t+h)=x(t)+\int_t^{t+h}v_\theta(x(s),s)\,ds.
$$

solver 的差别就是怎样近似这个沿真实轨迹的积分。注意 integrand 是 $v(x(s),s)$；把空间点固定为 $x(t)$ 会丢掉状态随时间变化。

## 三、Euler：一阶但不是“一定差”

Euler 使用左端/当前点评估：

$$
x_{n-1}=x_n+h_n v_\theta(x_n,t_n).
$$

若精确解足够光滑，Taylor 展开

$$
x(t+h)=x(t)+hv(x(t),t)+\frac{h^2}{2}\frac{d}{dt}v(x(t),t)+O(h^3),
$$

所以单步 local truncation error 为 $O(h^2)$；在稳定与 Lipschitz 条件下，固定区间 global error 为 $O(h)$。

一阶不等于在所有 NFE 下都最差：Euler 每步 1 NFE，若 field error 主导或允许更多小步，它可能优于每步 2 NFE 的高阶法。比较必须固定总 NFE。

## 四、Heun：预测—校正的二阶法

先预测

$$
\tilde x_{n-1}=x_n+h_n v_\theta(x_n,t_n),
$$

再校正

$$
x_{n-1}=x_n+\frac{h_n}{2}\left[
v_\theta(x_n,t_n)+v_\theta(\tilde x_{n-1},t_{n-1})
\right].
$$

在光滑条件下 local error $O(h^3)$、global error $O(h^2)$。每步通常 2 NFE；若最后一步省略校正或复用某些值，必须报告实际 NFE，不能用“20 steps”代替。

## 五、总误差为什么不等于 solver order

设真实目标 field 为 $v$，learned field

$$v_\theta=v+e_\theta.$$

令 $x(t)$ 解真实 ODE，$\tilde x(t)$ 解 learned ODE。在 $v$ 对 $x$ 为 $L$-Lipschitz 时，Gronwall 给出概念性上界

$$
\|x(0)-\tilde x(0)\|
\le e^{LT}
\left(
\|x(T)-\tilde x(T)\|
+\int_0^T\|e_\theta(\tilde x(t),t)\|dt
\right).
$$

数值解 $\hat x_0$ 再叠加 solver error：

$$
\|x(0)-\hat x_0\|
\le \underbrace{\|x(0)-\tilde x(0)\|}_{\text{model/terminal}}
+\underbrace{\|\tilde x(0)-\hat x_0\|}_{\text{discretization/roundoff}}.
$$

把 Euler 换成高阶法主要影响第二项。若第一项很大，order 提升会很快饱和；若 guidance 使路径进入训练分布外区域，$e_\theta$ 还可能随 scale 增大。

## 六、DPM-Solver 为什么不是普通 RK 换名字

[[S-2022-Lu-DPM-Solver]] 利用 diffusion ODE 的半线性结构：解析处理已知线性部分，经变量替换把剩余项写成指数加权 neural-network integral，再对该积分做高阶近似。这样可以在相同 NFE 下减少特定结构的误差常数。

需要区分：

- **通法阶数**：对一般光滑 ODE 的 RK/multistep 结论；
- **结构化阶数**：利用 diffusion schedule/parameterization 的专用推导；
- **经验质量**：给定 checkpoint、guidance、grid 和数据集的 FID/人评；
- **模型误差**：score/denoiser 本身不精确。

专用 solver 的理论优势不自动覆盖错误 prediction type、离散训练时间插值、端点 clipping 或 extreme CFG。

## 七、multistep 与 warm-up

线性 multistep 用历史 field values 估计下一步，稳态时可能 1 NFE/step，但开头没有足够历史，需要 Euler/RK warm-up。总成本

$$
\mathrm{NFE}=\mathrm{NFE}_{warmup}+\mathrm{NFE}_{main}+\mathrm{NFE}_{corrector}.
$$

重新启动、adaptive rejection、classifier gradient 和 dynamic thresholding 也要进入 wall-time 账。

## 八、时间网格比“步数”更具体

均匀 $t$ 网格不等于均匀 noise level、$\sigma$、log-SNR 或 ODE arc length。扩散端点常变化剧烈，网格设计会显著影响误差。

复现至少给出：

$$
\{t_n\},\quad
\{\sigma_n\},\quad
\lambda_n=\log\frac{\alpha_n^2}{\sigma_n^2},
$$

以及端点是否截断到 $\epsilon>0$。两个“20 步”采样器若网格不同，不是纯 solver 对比。

## 九、SDE solver：强误差与弱误差

对随机 sampler，除 drift 外还离散 Brownian increments。必须区分：

- strong error：同一 Brownian path 下轨迹距离；
- weak error：测试函数期望/终点分布统计误差；
- Monte Carlo error：有限生成样本估计 FID/KID/coverage 的误差。

生成通常更关心终点 law，但配对 seed 调试常需固定同一 noise increments。不能用 ODE 的确定性 order 直接声明 SDE sampler 的 strong/weak order。

## 十、科学空间中的两类加速

### 10.1 AMED：学习积分代表点

[[S-2023-Su-9881-中值定理加速ODE采样]] 从

$$
\frac1h\int_t^{t+h}v(x(s),s)ds
$$

出发学习一个中间位置/时间。标量积分中值定理不能一般扩展到向量值函数的共同代表点，所以 AMED 的高维有效性属于低成本蒸馏与轨迹结构支持的经验结论，不是无条件定理。

### 10.2 Skip-Tuning：改模型调用，不改积分公式

[[S-2024-Su-10077-Skip-Tuning]] 通过缩放 U-Net skip connections 改善低步数采样。它说明加速实验可能同时改变 vector field；此时差异不能全归因于 solver order。必须有相同 checkpoint、相同 solver、只扫 skip scale 的消融。

## 十一、公平 benchmark 表

| 字段 | 必须固定/报告 |
|---|---|
| 模型 | checkpoint hash、prediction type、EMA、precision |
| 动力学 | SDE/PF-ODE/DDIM、schedule、guidance、thresholding |
| 网格 | time/noise/log-SNR nodes 与端点 |
| solver | method/order、warm-up、corrector、adaptive tolerance |
| 成本 | denoiser NFE、classifier calls/backward、latency、throughput、memory |
| 质量 | FID/KID/P-R/conditionality、人评、sample count 与 CI |
| 随机性 | seeds、SDE increments、paired initial noise |

应画 quality–cost Pareto frontier，而不是只报某一预算的冠军。

## 十二、图：阶数只负责哪一格

先回答：从真实目标到最终样本经历哪三次近似？Heun 的“二阶”落在哪一格？为什么 10 steps 不能直接与 10 NFE 等同？

![[00-知识库管理/_assets/figures/generative-models/fig-diffusion-solver-error-nfe-ledger-v1.svg|900]]

> [!figure] 图 50.9-04　扩散 solver 的误差—成本总账
> 图把目标 field、learned field、finite solver 与 metric estimator 串成误差链，并对 Euler/Heun/multistep 标注 NFE。来源：据数值 ODE 标准理论、DPM-Solver 与科学空间 9881 独立绘制。

**怎样读图**：先纵向分 model error 与 discretization error，再横向比较 NFE；最后看评价框是否使用相同 sample population。

**图没有证明什么**：图不证明高阶法在任意 learned field 上更好，不证明 NFE 等于 wall-time，也不证明 AMED 的向量中值点必然存在。

## 十三、学习出口

- 能推 Euler/Heun 的 local/global order 条件；
- 能用 Gronwall 解释 field error 与 solver error 分账；
- 能准确统计 warm-up/corrector/classifier 成本；
- 能指出向量积分中值定理的边界；
- [[习题 - 扩散 SDE、ODE Solver、步长与 NFE 总账]]
- [[解答 - 扩散 SDE、ODE Solver、步长与 NFE 总账]]

---
type: derivation
status: verified
area: [generative-models, meanflow, flow-matching, finite-step-maps]
node_id: GEN-70
prerequisites: ["[[扩散蒸馏、一致性模型与 Shortcut]]", "[[连续性方程与守恒律]]", "[[Jacobian、JVP 与 VJP]]"]
related: ["[[扩散 SDE、ODE Solver、步长与 NFE 总账]]", "[[数据、噪声、速度与 Score 参数化]]"]
sources: ["[[S-2025-Su-10958-瞬时速度与平均速度]]", "[[S-2025-Geng-MeanFlow]]", "[[S-2025-Su-11428-预测数据而非噪声]]"]
exercises: ["[[习题 - 平均速度、MeanFlow 与有限步生成]]"]
solutions: ["[[解答 - 平均速度、MeanFlow 与有限步生成]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-meanflow-average-velocity-identity-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 平均速度、MeanFlow 与有限步生成

> [!abstract] 一句话结论
> instantaneous velocity $v(z_t,t)$ 只描述轨迹在一个点的切线；average velocity $u(z_t,r,t)$ 描述从 $r$ 到 $t$ 沿实际轨迹的总位移率。MeanFlow 对积分恒等式求全导数，把 $u$ 与 $v$ 连接成可训练目标。它不是简单的端点速度平均，也不自动赋予 learned finite map 精确 semigroup 或 continuous likelihood。

## 一、速度的三个不同对象

给定 ODE

$$\dot z_t=v(z_t,t),$$

区分：

1. instantaneous field：$v(z_t,t)$；
2. interval average velocity：$u(z_t,r,t)$；
3. finite map：$F_{t\to r}(z_t)$。

它们的单位相同，但输入和语义不同。$v$ 只看当前时间/状态；$u$ 还要知道区间端点；$F$ 直接输出新状态。

## 二、average velocity 的定义

沿从 $r$ 到 $t$ 的实际轨迹，定义

$$
\boxed{
u(z_t,r,t)
=\frac1{t-r}\int_r^t v(z_s,s)\,ds,
\qquad r<t.
}
$$

由 ODE 积分式，

$$
z_t-z_r=\int_r^t v(z_s,s)ds=(t-r)u(z_t,r,t),
$$

所以反向 finite update 是精确恒等式

$$
\boxed{z_r=z_t-(t-r)u(z_t,r,t).}
$$

如果 $u$ 精确，一次调用可跨整个区间；如果 $u_\theta$ 是 learned approximation，上式只是部署 map。

## 三、为什么不能写成端点算术平均

一般情况下

$$
u(z_t,r,t)\ne\frac12[v(z_r,r)+v(z_t,t)].
$$

右边是 trapezoidal quadrature，只在速度沿轨迹近似线性或步长足够小时近似积分平均。更不能把空间点固定为 $z_t$ 后写

$$\frac1{t-r}\int_r^t v(z_t,s)ds,$$

因为真实 integrand 是 $v(z_s,s)$。

### 3.1 一个可算反例

对 $\dot z=z$，轨迹 $z_s=z_re^{s-r}$。真实平均速度

$$
u=\frac{z_t-z_r}{t-r}
=z_r\frac{e^{t-r}-1}{t-r}.
$$

端点速度平均是

$$
\frac{z_r+z_t}{2}=z_r\frac{1+e^{t-r}}2.
$$

两者只在小区间到二阶近似相近，不是恒等。

## 四、MeanFlow identity：逐步推导

固定下端点 $r$，写

$$
(t-r)u(z_t,r,t)=\int_r^t v(z_s,s)ds.
$$

对上端点 $t$ 沿轨迹求全导数。左侧用乘积法则：

$$
\frac{d}{dt}[(t-r)u(z_t,r,t)]
=u(z_t,r,t)+(t-r)\frac{d}{dt}u(z_t,r,t).
$$

右侧由微积分基本定理：

$$
\frac{d}{dt}\int_r^t v(z_s,s)ds=v(z_t,t).
$$

因此

$$
\boxed{
u(z_t,r,t)
=v(z_t,t)-(t-r)\frac{d}{dt}u(z_t,r,t).
}
$$

全导数不是偏导数：

$$
\frac{d}{dt}u(z_t,r,t)
=\partial_tu(z_t,r,t)
+J_z u(z_t,r,t)\,v(z_t,t),
$$

固定 $r$ 时没有 $\partial_r$ 项。程序中 $J_zu\,v$ 用 JVP 计算，无需形成完整 Jacobian。

## 五、极限检查

当 $r\uparrow t$ 且 $v$ 连续，

$$
\lim_{r\uparrow t}u(z_t,r,t)=v(z_t,t).
$$

这是 average 与 instantaneous 的 boundary condition。若模型在短区间不接近 $v$，说明 identity target、time parameterization 或 JVP 可能实现错误。

## 六、训练目标的程序语义

MeanFlow 用网络 $u_\theta(z_t,r,t)$ 预测 average velocity，并从 instantaneous target $v$ 与上面的 identity 构造回归 target。一个抽象写法是

$$
\mathcal L(\theta)
=\mathbb E\left[
\|u_\theta-\operatorname{sg}(v-(t-r)D_tu_\theta)\|^2
\right],
$$

其中 $D_tu_\theta$ 通过 JVP 得到，`sg` 的位置定义实际优化程序。不同实现可能对 target network、guidance、time sampling 与 parameterization 做调整；不能把数学恒等式直接当作唯一代码。

要分别检查：

- value path：$u_\theta$ 的前向值；
- JVP path：切向量是否为 $(v,0,1)$ 或对应参数化；
- stop-gradient path：target 是否反传；
- boundary samples：$r=t$ 或极短区间如何处理；
- deployment：$z_r=z_t-(t-r)u_\theta$ 的方向。

## 七、与 Shortcut 的关系

两者都把 finite interval 纳入输入：

| | Shortcut | MeanFlow |
|---|---|---|
| 输入 | $(z,t,h)$ | $(z_t,r,t)$ |
| 核心对象 | step-conditioned displacement rate | path-average velocity |
| 约束 | 一次 $2h$ = 两次 $h$ | $u=v-(t-r)D_tu$ |
| base signal | $h=0$ flow matching | instantaneous velocity identity |
| 风险 | composition 自洽但错误 | self-referential JVP target、interval shift |

在精确 flow 下二者都可表示同一个 finite map；在有限模型、不同 loss 和 sampling distribution 下，优化路径并不等价。

## 八、与“预测数据而非噪声”的接口

[[S-2025-Su-11428-预测数据而非噪声]] 强调 $x/\epsilon/v$ 在网络容量受限时并非优化等价。对一步/少步模型尤其重要：

- 输出 average velocity 可直接给 displacement；
- 输出 endpoint/data 可通过 $(z_t-z_r)/(t-r)$ 换算，但短区间条件数恶化；
- 输出 instantaneous velocity 再做大步 Euler 会产生 discretization mismatch；
- 低秩网络更适合哪种 target 是架构/数据实验问题，不由代数唯一决定。

## 九、必须测的五个 residual

1. identity residual：

$$R_{id}=\|u_\theta-v+(t-r)D_tu_\theta\|;$$

2. endpoint residual：

$$R_{end}=\|z_r-[z_t-(t-r)u_\theta]\|;$$

3. composition residual：

$$R_{comp}=\|F_{t\to r}-F_{m\to r}\circ F_{t\to m}\|;$$

4. boundary residual：$\|u_\theta(z,t,t)-v(z,t)\|$；
5. unseen-interval residual：训练未采到的 $(r,t)$ 上重复以上检查。

前两个可在 synthetic oracle flow 上验证，后三个用于 learned deployment。任何单一 residual 小都不等于样本分布正确。

## 十、科学空间研读框

[[S-2025-Su-10958-瞬时速度与平均速度]] 从 finite-NFE 直觉出发，强调“改变学习对象”可能比继续提高 solver order 更直接。课程补上：

- average 必须沿实际 trajectory 定义；
- 全导数包含 $J_zu\,v$；
- exact identity、learned loss 与 finite sampler 分三层；
- [[S-2025-Geng-MeanFlow]] 的 1-NFE ImageNet 结果属于 2025 前沿实验，不是一般定理。

## 十一、图：切线、弦与平均速度

先回答：曲线切线与端点弦分别代表什么？公式中的 JVP 沿哪一个方向？为什么弦正确不等于整条轨迹正确？

![[00-知识库管理/_assets/figures/generative-models/fig-meanflow-average-velocity-identity-v1.svg|900]]

> [!figure] 图 50.9-06　MeanFlow 的平均速度、全导数与一步 map
> 图以弯曲轨迹对照 instantaneous tangent 与 finite-interval chord，并展开 $D_tu=\partial_tu+J_zu\,v$。来源：据 MeanFlow 原论文、科学空间 10958 与本节推导独立绘制。

**怎样读图**：先看切线只负责局部，再看弦等于积分平均乘区间长度；最后沿 JVP 框检查状态与时间两个输入方向。

**图没有证明什么**：图不证明 learned $u_\theta$ 满足 exact semigroup，不证明端点弦决定中间 trajectory，也不证明一步生成保留 continuous likelihood。

## 十二、学习出口

- 能从积分定义推 $u=v-(t-r)D_tu$；
- 能用 $\dot z=z$ 反驳端点速度算术平均；
- 能写出 JVP 切向量与 stop-gradient 合同；
- 能设计 identity/boundary/composition 三类 residual；
- [[习题 - 平均速度、MeanFlow 与有限步生成]]
- [[解答 - 平均速度、MeanFlow 与有限步生成]]

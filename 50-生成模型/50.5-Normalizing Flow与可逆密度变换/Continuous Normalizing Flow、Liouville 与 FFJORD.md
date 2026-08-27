---
type: derivation
status: verified
area: [generative-models, continuous-normalizing-flows, ode]
node_id: GEN-39
prerequisites: ["[[流映射、Liouville 公式与连续正规化流]]", "[[常微分方程、初值问题与解的存在唯一性]]", "[[行列式、log-det 与迹的导数]]"]
related: ["[[Residual Flow、可逆 ResNet 与 Logdet 估计]]", "[[Fokker-Planck 方程与概率流 ODE]]"]
sources: ["[[S-2018-Chen-Neural-ODE]]", "[[S-2019-Grathwohl-FFJORD]]"]
exercises: ["[[习题 - Continuous Normalizing Flow、Liouville 与 FFJORD]]"]
solutions: ["[[解答 - Continuous Normalizing Flow、Liouville 与 FFJORD]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-flow-cnf-divergence-solver-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Continuous Normalizing Flow、Liouville 与 FFJORD

> [!abstract] 一句话结论
> Continuous normalizing flow（CNF）用 ODE 向量场连续搬运概率质量，把离散层的 log-determinant 变为沿轨迹积分的负 divergence。理论 flow 在适当存在唯一性条件下是双射；代码得到的是数值 solver 的近似轨迹、近似密度和近似梯度，成本应由 NFE、容差与 stiffness 报告。

## 一、从无限多个微小 residual steps 开始

设状态 $z(t)\in\mathbb R^d$ 满足

$$
\frac{dz(t)}{dt}=f_\theta(z(t),t),\qquad t\in[t_0,t_1].
$$

小时间步 $\Delta t$ 下，

$$z(t+\Delta t)\approx z(t)+\Delta t\,f_\theta(z(t),t),$$

像一个共享连续时间参数的 residual block。局部 Jacobian 约为

$$I+\Delta t\,J_f.$$

利用 $\log\det(I+\Delta t A)=\Delta t\operatorname{tr}(A)+O(\Delta t^2)$，除以 $\Delta t$ 并取极限，便得到连续换元率。

## 二、瞬时变量替换公式

若 $p_t$ 是 $z(t)$ 的密度，沿特征轨迹有

$$
\boxed{\frac d{dt}\log p_t(z(t))
=-\operatorname{tr}\left(\frac{\partial f_\theta}{\partial z}(z(t),t)\right)
=-\nabla\cdot f_\theta(z(t),t).}
$$

负号来自质量守恒：正 divergence 表示局部体积膨胀，密度下降。积分得到

$$
\log p_{t_1}(z(t_1))
=\log p_{t_0}(z(t_0))
-\int_{t_0}^{t_1}\nabla\cdot f_\theta(z(t),t)dt.
$$

评价数据 density 时常从 $x=z(t_1)$ 反向积分到 base $z(t_0)$；程序的时间方向和 accumulator 符号必须一起核对。

## 三、一维线性例子验负号

令 $\dot z=az$，则 $z(t)=e^{a(t-t_0)}z(t_0)$。生成映射的 Jacobian 是 $e^{a\Delta t}$，因此

$$\log p_{t_1}(z_1)=\log p_{t_0}(z_0)-a\Delta t.$$

另一方面 divergence 就是 $a$，积分公式给同一结果。$a>0$ 时空间伸长、density 降低；这是最小符号单元测试。

## 四、为什么 ODE flow 可逆

若 $f(z,t)$ 对 $z$ 局部 Lipschitz、对 $t$ 适当连续，并且解在整个区间存在，则每个初值有唯一轨迹。两条轨迹若在某时相交，反向唯一性迫使它们此前也相同。因此 flow map $\Phi_{t_0\to t_1}$ 是一一的，inverse 是沿同一向量场反向积分。

若出现解爆炸、不唯一、事件重置或非光滑离散操作，结论可能失败。有限步 Euler/RK 映射是否精确可逆是另一个问题。

## 五、FFJORD 的随机迹

直接计算 divergence 需要 Jacobian 对角和，朴素成本随 $d$ 次反向传播增长。FFJORD 用

$$
\operatorname{tr}(J_f)=\mathbb E_v[v^\top J_fv],\qquad \mathbb E[vv^\top]=I,
$$

以一个或少量 probes 估计。给定状态和 Jacobian，probe estimator 对 trace 无偏；但以下不能自动推出：

- 数值轨迹 $\hat z(t)$ 等于精确轨迹；
- 自适应 solver 中估计误差与状态误差独立；
- 有限容差 log-likelihood 对真实 ODE likelihood 无偏；
- continuous adjoint 算出的梯度等于离散 solver 程序的精确反向梯度。

## 六、solver 是模型计算合同

CNF 一次“前向”包含多次 vector-field evaluation。至少报告：

| 项 | 为什么重要 |
|---|---|
| solver family/order | 决定局部/全局离散误差和稳定域 |
| `rtol`, `atol` | 决定自适应接受、步数和轨迹误差 |
| NFE | 比“层数/一步”更接近实际计算量 |
| stiffness | 可令显式 solver 取极小步，NFE 激增 |
| trace probes/seed | 决定 likelihood 方差 |
| gradient method | continuous adjoint、backprop through solver、checkpoint 的语义不同 |

容差减半不保证误差精确减半；需做 tolerance sweep，并与更严格 reference 比较。

## 七、连续流与离散 flow 的差异

CNF 放宽了每层必须 triangular/coupling 的限制，只需估计 divergence；但表达和拓扑仍受连续 ODE flow 约束。轨迹在同一时间不能交叉，某些 orientation/topology 变换需要增广维度或其他机制。`free-form dynamics` 不等于任意映射无条件可达。

## 八、科学空间与数学底座

本节严格推导依托[[流映射、Liouville 公式与连续正规化流]]。[[S-2018-Chen-Neural-ODE]]承担 continuous-depth/adjoint 入口，[[S-2019-Grathwohl-FFJORD]]承担随机迹 CNF 的方法与实验。把博客式“一次 ODE 调用”转成研究可复查语言时，必须展开为 solver、NFE 和 error tolerance。

## 九、图：轨迹、体积和数值求解三层

先看图回答：连续理论中的 divergence integral，经过随机迹与自适应 solver 后，新增了哪两类不确定性？

![[00-知识库管理/_assets/figures/generative-models/fig-flow-cnf-divergence-solver-v1.svg|900]]

> [!figure] 图 50.5-07　CNF 的轨迹—density accumulator—solver/trace 误差账
> 上方是质量沿 ODE flow 搬运，下方把理论 divergence、Hutchinson probe 与有限容差积分分层。来源：依据 Liouville 公式和 FFJORD 机制独立绘制。

**怎样读图**：沿轨迹同时积分状态 $z$ 与 log-density accumulator。理论框给连续恒等式；工程框中的 probe 和 solver 分别增加统计误差与离散误差。

**图没有证明什么**：图不保证所选向量场无爆炸/非唯一解，不保证一个 probe 方差小，也不证明连续 adjoint 与离散梯度一致。

## 十、本节回顾与训练

- instantaneous log-density rate 是负 divergence；
- ODE flow 的可逆性来自存在唯一性，不来自“网络连续”四个字；
- FFJORD 只使 trace estimation 便宜，不消除 solver error；
- NFE、tolerance、stiffness 与 gradient method 都属于模型报告；
- `one pass` 不等于一次 vector-field evaluation。

- [[习题 - Continuous Normalizing Flow、Liouville 与 FFJORD]]
- [[解答 - Continuous Normalizing Flow、Liouville 与 FFJORD]]

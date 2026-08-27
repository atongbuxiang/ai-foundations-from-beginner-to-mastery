---
type: solution
status: draft
topic: "[[Continuous Normalizing Flow、Liouville 与 FFJORD]]"
exercise: "[[习题 - Continuous Normalizing Flow、Liouville 与 FFJORD]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Continuous Normalizing Flow、Liouville 与 FFJORD
## A. 识别与复述
### GEN39-A01
$\dot z=f_\theta(z,t)$，沿轨迹 $d\log p_t(z(t))/dt=-\operatorname{tr}(\partial f/\partial z)=-\nabla\cdot f$。
### GEN39-A02
向量场对状态局部 Lipschitz、对时间适当连续，且解在目标区间存在不爆炸，保证初值解唯一；反向问题也需成立。事件重置/非唯一性可破坏 flow 双射。
### GEN39-A03
一次高层 `ODESolve`/forward 会由 solver 选择多个时间步；每步按方法阶数可能多次调用向量场。NFE 是实际 vector-field calls，通常比“1 forward”更能解释成本。
## B. 手算与建模
### GEN39-B01
$z(t_1)=e^{2(0.5)}z(t_0)=ez_0$。divergence 为 2，log-density change 是 $-2(0.5)=-1$。
### GEN39-B02
Jacobian $\operatorname{diag}(a,b)$，divergence $a+b$；若常数，$\log p_T(z_T)-\log p_0(z_0)=-(a+b)T$。
### GEN39-B03
任意 Rademacher $v_i^2=1$，$v^TJv=1+3=4=\operatorname{tr}J$，所以本对角矩阵下 probe variance 为 0；非对角项会引入方差。
## C. 推导与证明
### GEN39-C01
微步映射 Jacobian 是 $I+\Delta tJ_f+O(\Delta t^2)$。生成 density change 为负 logdet，且 $\log\det(I+\Delta tJ_f)=\Delta t\operatorname{tr}J_f+O(\Delta t^2)$。除以 $\Delta t$ 取极限得负 trace。
### GEN39-C02
若两条不同初值轨迹在 $t^*$ 相交，把交点作为 $t^*$ 初值反向求解将得到两条解，违反唯一性；故在共同存在区间内不能相交。
### GEN39-C03
从 $z(t_1)=x$ 向 $t_0$ 解状态，同时积分 accumulator。可定义 $\dot\ell=-\nabla\cdot f$ 沿正时间，则反向积分自然给 $\ell(t_0)-\ell(t_1)$；最终用 $\log p_{t_1}(x)=\log p_{t_0}(z_0)-\int_{t_0}^{t_1}\nabla\cdot fdt$。代码测试应以线性场验时间/符号。
## D. 边界、反例与纠错
### GEN39-D01
ODE $\dot z=-2z$ 的精确 flow 始终可逆；Euler 步 $z_{n+1}=(1-2h)z_n$ 在 $h=0.5$ 时把所有状态映到 0，不可逆。连续定理不自动传给任意离散步。
### GEN39-D02
Trace estimator 条件于精确状态/Jacobian 才无偏；有限 solver 先改变状态与积分点，自适应决策可与噪声耦合，有限容差和梯度又有离散误差。因此最终 likelihood 不由单步 identity 自动无偏。
### GEN39-D03
若 Jacobian 有相差悬殊的快慢特征值，显式 solver 为稳定解析快模态必须取极小步，即使慢模态决定总体时间跨度；于是接受步数和 NFE 大增。
## E. AI 迁移
### GEN39-E01
固定样本/probes，按 $10^{-3},10^{-5},10^{-7},10^{-9}$ 等容差运行，与最严格结果作 reference；报告 state、logp、gradient、round-trip error、NFE、wall time和失败率，并换 solver 检查稳定。
### GEN39-E02
比较同一离散程序的 loss/gradient、memory、NFE、reconstruction error；continuous adjoint 需重新积分，可能有 trajectory mismatch，直接 backprop 与实际离散 steps 一致但占内存。用 finite differences/更严容差作小维梯度 reference。
### GEN39-E03
CNF 不需 triangular Jacobian，但仍受 ODE 存在唯一性、非交叉轨迹、拓扑/orientation、有限时间与向量场容量、divergence estimation、stiffness 和 solver 成本约束。`free-form` 是相对架构自由，不是任意映射零代价可达。


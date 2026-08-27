---
type: derivation
status: verified
area: [training, optimization, trust-region]
node_id: TRN-18
aliases: [阻尼 Newton, 信赖域与 LM]
prerequisites: ["[[Newton 法、Gauss-Newton 与拟 Newton 法]]", "[[Hessian、GGN、Fisher 与经验 Fisher 对象总账]]", "[[二次型与正定矩阵]]", "[[Cholesky 分解]]"]
related: ["[[Hessian-vector Product、共轭梯度与隐式二阶步]]", "[[自然梯度、KL 局部几何与坐标不变性]]", "[[学习率、局部损失变化与相对更新尺度]]"]
sources: ["[[S-2006-Nocedal-Wright-Numerical-Optimization]]", "[[S-1983-Steihaug-Trust-Region-CG]]"]
exercises: ["[[习题 - Newton、Damping、Trust Region 与 Levenberg–Marquardt]]"]
solutions: ["[[解答 - Newton、Damping、Trust Region 与 Levenberg–Marquardt]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-trust-region-damping-ratio-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Newton、Damping、Trust Region 与 Levenberg–Marquardt

> [!abstract] 一句话结论
> Newton step 是局部二次模型的无约束驻点，不是天然安全步。Damping 改变小特征方向，trust region 限制模型被信任的半径，并用真实下降/预测下降比更新控制状态；Levenberg–Marquardt 是 nonlinear least squares 中把 Gauss–Newton 与阻尼结合的结构化实例。

## 一、Newton step 从哪里来

在 $\theta$ 附近写 quadratic model

$$
m(p)=L(\theta)+g^Tp+\frac12p^TBp,
$$

其中 $B$ 可为 Hessian 或曲率近似。若 $B\succ0$，无约束极小点满足

$$
Bp_N=-g,\qquad p_N=-B^{-1}g.
$$

这句话包含三个条件：线性系统可解、$B$ 正定使驻点是 model minimizer、步长没有离开 Taylor model 的可信区域。

### 1.1 三种失败

- $B$ 奇异：方向未唯一，解可能巨大；
- $B$ 不定：$p_N$ 可是 saddle/maximizer 的驻点；
- $B$ 局部正确但 $\|p_N\|$ 太大：高阶 remainder 主导。

## 二、Tikhonov/Levenberg damping

最简单的 regularized subproblem 是

$$
\min_p\;g^Tp+\frac12p^TBp+\frac\lambda2\|p\|_2^2,
$$

给出

$$
(B+\lambda I)p_\lambda=-g.
$$

若 $B=Q\operatorname{diag}(\mu_i)Q^T$，在 eigenbasis 中

$$
(Q^Tp_\lambda)_i=-\frac{(Q^Tg)_i}{\mu_i+\lambda}.
$$

因此 damping 对小/负 eigenvalue 最敏感。要使 $B+\lambda I\succeq0$ 至少需 $\lambda\ge-\lambda_{min}(B)$；实际还会留条件数裕量。

> [!warning] Damping 不是 weight decay
> $\lambda I$ 加在 step 的 quadratic model/线性系统里；weight decay 改变 parameter transition，L2 regularization 改变 objective。三者可能在某个线性例子出现相似代数项，但状态、单位和后续轨迹不同。

## 三、Trust-region 子问题

另一种做法直接说：“只在半径 $\Delta$ 内信任模型”：

$$
\min_{\|p\|\le\Delta}g^Tp+\frac12p^TBp.
$$

全局解 $p^*$ 的 KKT 条件可写

$$
(B+\lambda I)p^*=-g,
$$

$$
B+\lambda I\succeq0,\qquad
\lambda\ge0,\qquad
\lambda(\Delta-\|p^*\|)=0.
$$

若 Newton step 在球内且 $B\succ0$，$\lambda=0$；若触边，$\lambda>0$。所以 damping 参数可作为 trust-region 约束的 dual variable，但“固定 $\lambda$ 算法”和“自适应 $\Delta$ 算法”不是同一个状态机。

## 四、模型是否可信：actual/predicted reduction ratio

定义预测下降

$$
\operatorname{pred}=m(0)-m(p)=-g^Tp-\frac12p^TBp,
$$

真实下降

$$
\operatorname{ared}=L(\theta)-L(\theta+p),
$$

以及

$$
\rho=\frac{\operatorname{ared}}{\operatorname{pred}}.
$$

- $\rho\approx1$：quadratic model 预测准确，可接受并考虑放大半径；
- $0<\rho\ll1$：方向下降但模型过度乐观；
- $\rho<0$：真实 objective 上升，通常拒绝并缩半径。

阈值如 $.25/.75$ 是算法选择，不是数学常数。还必须要求 pred 为正且数值可辨，否则 ratio 无意义。

## 五、Cauchy point：最低 model-decrease 证书

沿最陡方向 $p=-\tau g$，model 为

$$
m(-\tau g)-m(0)=-\tau\|g\|^2+\frac12\tau^2g^TBg.
$$

若 $g^TBg>0$，无约束线极小点 $\tau^*=\|g\|^2/(g^TBg)$；再截到 $\tau\|g\|\le\Delta$。若 $g^TBg\le0$，model 沿 $-g$ 不上弯，直接走到边界。Cauchy point 可能慢，却提供可证明的充分下降基线。

## 六、Nonlinear least squares 与 Levenberg–Marquardt

对

$$
L(\theta)=\frac12\|r(\theta)\|^2,\qquad J=\frac{\partial r}{\partial\theta},
$$

有

$$
g=J^Tr,\qquad
H=J^TJ+\sum_i r_i\nabla^2r_i.
$$

Gauss–Newton 丢掉 residual-weighted 二阶项，解

$$
J^TJp=-J^Tr.
$$

Levenberg–Marquardt 使用

$$
(J^TJ+\lambda I)p=-J^Tr.
$$

$\lambda\to0$ 接近 Gauss–Newton；$\lambda$ 大时 $p\approx-(1/\lambda)g$，接近小步 gradient descent。LM 的结构优势来自 least-squares Jacobian，不意味着任意 cross-entropy 网络都有相同 residual 分解。

## 七、不定二次模型的最小例子

取

$$
B=\begin{pmatrix}-1&0\\0&4\end{pmatrix},\qquad g=\begin{pmatrix}0\\1\end{pmatrix}.
$$

形式 Newton 解 $p=(0,-1/4)$，但第一坐标 model 为 $-p_1^2/2$，可无限下降；这个驻点不是全局 minimizer。若 trust radius 为 1，最优解会利用 negative-curvature 方向触边。若 damping $\lambda>1$，$B+\lambda I\succ0$ 才得到严格凸 regularized model。

这说明“解出 $Bp=-g$”不等于“解了 trust-region 子问题”。

## 八、图：一步二阶法的三层控制回路

先看图回答：$\lambda$ 改变 eigenmode 的哪一项？$\rho$ 又反馈修改哪个状态？

![[00-知识库管理/_assets/figures/training-optimization/fig-trust-region-damping-ratio-v1.svg|900]]

> [!figure] 图 TRN-18　Newton、damping、trust radius 与 model ratio
> 左侧从 quadratic model 分出无约束 Newton、regularized solve 和 constrained trust-region；中间展示 eigenvalue filter；右侧用 ared/pred ratio 控制 accept/reject 与下一半径。来源：依据 [[S-2006-Nocedal-Wright-Numerical-Optimization]] 和 [[S-1983-Steihaug-Trust-Region-CG]] 独立绘制。

**怎样读图**：先检查 $B$ 是否 PSD 和 step 是否触边，再看真实 objective 与模型是否一致；不要把一个 damping 数字当完整 globalization strategy。

**图没有证明什么**：图不保证 mini-batch loss ratio 可代表 population objective，也没有决定深网中最佳 $B,\lambda,\Delta$ 或更新频率。

## 九、AI 训练接口

真实系统至少记录：curvature batch、gradient batch、damping、trust radius、linear residual、negative-curvature flag、pred/ared/$\rho$、接受率、HVP 次数、参数 delta RMS 和 wall time。若 batch 在 model construction 与 ared evaluation 之间改变，$\rho$ 会混入 sampling noise。

## 练习与独立解答

- [[习题 - Newton、Damping、Trust Region 与 Levenberg–Marquardt]]
- [[解答 - Newton、Damping、Trust Region 与 Levenberg–Marquardt]]

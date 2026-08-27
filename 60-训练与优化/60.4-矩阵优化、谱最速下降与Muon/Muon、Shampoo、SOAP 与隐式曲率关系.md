---
type: comparison
status: verified
area: [training, optimization, muon, preconditioning]
node_id: TRN-30
aliases: [Muon Shampoo SOAP KFAC 边界, Matrix Optimizer Object Ledger]
prerequisites: ["[[矩阵梯度、谱核范数对偶与 Matrix Sign]]", "[[Shampoo、逆矩阵根与 Kronecker 预条件]]", "[[SOAP、二阶混合优化器与成本证据地图]]", "[[K-FAC、Kronecker 分块与阻尼合同]]"]
related: ["[[Hessian、GGN、Fisher 与经验 Fisher 对象总账]]", "[[Muon 的扩展证据、系统成本与迁移边界]]"]
sources: ["[[S-2024-Jordan-Muon]]", "[[S-2018-Gupta-Shampoo]]", "[[S-2025-Vyas-SOAP]]", "[[S-2015-Martens-Grosse-KFAC]]", "[[S-2020-Martens-Natural-Gradient-Curvature]]", "[[S-2025-Su-10739-Muon续集]]"]
exercises: ["[[习题 - Muon、Shampoo、SOAP 与隐式曲率关系]]"]
solutions: ["[[解答 - Muon、Shampoo、SOAP 与隐式曲率关系]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-muon-shampoo-soap-kfac-boundary-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Muon、Shampoo、SOAP 与隐式曲率关系

> [!abstract] 一句话结论
> Muon、Shampoo、SOAP 与 K-FAC 都会做矩阵运算，但它们积累的状态、近似的对象和解的局部子问题不同。Muon 的核心可由第一阶 norm geometry 推导；它不是因为输出了 $UV^T$ 就自动成为 Hessian、Fisher 或 Shampoo 的隐式逆。

## 一、比较优化器时先列“对象五元组”

对任一方法，先写

$$
(\text{instantaneous signal},
\text{state},
\text{transformation},
\text{claimed geometry},
\text{cost}).
\tag{1}
$$

若只比较最终 update shape 或都出现 $GG^T$，就会把完全不同的随机对象混在一起。

## 二、Muon：对当前动量矩阵做 polar map

忽略版本细节，Muon 骨架为

$$
M_t=\operatorname{Momentum}(M_{t-1},G_t),
\qquad
\Delta W_t\propto-\operatorname{polar}(M_t).
\tag{2}
$$

精确 polar 只依赖当前 $M_t$ 的 SVD：

$$
M_t=U_t\Sigma_tV_t^T
\quad\Longrightarrow\quad
\Delta W_t\propto-U_tV_t^T.
\tag{3}
$$

它没有显式维护 gradient second-moment matrix，更没有使用 labels sampled from a model distribution。其最直接理论来源是 spectral norm step ball 与 nuclear dual norm。

## 三、Shampoo：积累 mode-wise gradient Gram

对矩阵参数，一种理想化 Shampoo 状态是

$$
L_t=\epsilon I+\sum_{\tau\le t}G_\tau G_\tau^T,
\qquad
R_t=\epsilon I+\sum_{\tau\le t}G_\tau^TG_\tau.
\tag{4}
$$

典型矩阵更新含

$$
\Delta W_t
\propto-L_t^{-1/4}G_tR_t^{-1/4}.
\tag{5}
$$

四分之一次方使左右两侧合计形成适当的 Kronecker-style scaling。实际算法还含 EMA/累加选择、root update frequency、grafting、blocking 和 damping。

关键差别：Shampoo 的 $L_t,R_t$ 汇总一段历史中各梯度的 outer products；Muon 的 polar 只变换当前 momentum matrix 的 singular values。即使两者都涉及 Gram matrix，它们也不是同一个 state。

## 四、SOAP：在 Shampoo 特征基中做 Adam 型状态

SOAP 的简化视角是：

1. 用 Shampoo-style factors 估计左右特征基 $U_L,U_R$；
2. 把梯度旋转到该基：

$$
\widetilde G_t=U_L^TG_tU_R;
\tag{6}
$$

3. 在旋转坐标中维护 Adam-like first/second moments；
4. 旋回原坐标。

因此 SOAP 既有 basis state，又有 elementwise adaptive state。它不是“先做 Muon 再做 Adam”，也不等于只把 singular values 设成 1。

## 五、K-FAC：从模型 Jacobian 与 Fisher/GGN block 出发

对线性层 $y=xW$，单样本 weight gradient 常写成

$$
G=x^T\delta,
$$

其中 $x$ 是 layer input，$\delta$ 是输出反传信号。K-FAC 对 Fisher/GGN block 使用 Kronecker 近似：

$$
F_W
\approx A\otimes S,
\qquad
A=\mathbb E[x^Tx],\quad
S=\mathbb E[\delta^T\delta].
\tag{7}
$$

自然梯度式更新在矩阵形式下近似为

$$
\Delta W
\propto-(A+\lambda_A I)^{-1}
G
(S+\lambda_S I)^{-1},
\tag{8}
$$

具体左右顺序随 $W$ 的存储约定变化。K-FAC 的对象来自 activation 与 backprop-factor covariance，并以 Fisher/GGN 几何为目标；这与 Muon 的 norm-ball oracle 不是同一推导。

## 六、一个反例：同一个当前梯度，历史不同就分开

考虑 $2\times2$ 当前梯度

$$
G_t=I.
$$

两条历史：

$$
\mathcal H_1:\ G_1=\operatorname{diag}(10,1),
\qquad
\mathcal H_2:\ G_1=\operatorname{diag}(1,10).
$$

若当前 Muon momentum 恰被重置且只看 $G_t$，两条历史都输出 $-I$。Shampoo 的累计 factors 却分别在第一或第二坐标更大，式 (5) 会给出不同缩放。若 K-FAC 的 activation/backprop covariances 相同，即使 raw gradient history 不同，它又可能给出相同预条件。

因此“最终都像在压平各方向”只是语言相似，不能推出算法等价。

## 七、另一个反例：相同 $G$ 不决定 K-FAC state

单个矩阵

$$
G=x^T\delta
$$

可由很多不同 $(x,\delta)$ 组合产生。比如同时把 $x$ 乘 $c$、把 $\delta$ 除以 $c$，$G$ 不变，但

$$
A\mapsto c^2A,\qquad S\mapsto c^{-2}S.
$$

在无阻尼精确 Kronecker inverse 中某些尺度可能抵消；一旦有 damping、EMA、clipping 或 factor approximation，轨迹就会不同。Muon 仅从 $G$ 或其 momentum 无法恢复这些 activation statistics。

## 八、“隐式曲率”可以说到哪一步

可以说：

- norm choice 定义一种 step geometry；
- gradient covariance 可能在特定局部模型和轨迹假设下携带 curvature scale；
- 某些 modular duality 视角能统一比较 layer norm 与 update rule；
- 各方法都可能改善 ill-scaled parameter directions。

不能直接说：

- polar$(G)=H^{-1}G$；
- singular values 被压成 1 就等于 whitening Hessian；
- 使用 $G^TG$ 的计算过程就等于估计 Fisher；
- 在某一 benchmark 更快就证明某个 curvature mechanism。

若声称“Muon 近似某二阶方法”，至少要给出明确的局部目标、随机测度、矩阵等式或可检验误差界。

## 九、资源与系统总账

| 方法 | persistent state 主量级 | 昂贵操作 | 主要近似/版本旋钮 |
|---|---|---|---|
| Muon | 一个 momentum matrix | 每步若干 NS GEMM | steps、coefficients、shape scaling、grouping |
| Shampoo | row/column Gram factors | inverse roots/特征分解 | block size、root frequency、grafting、damping |
| SOAP | factors + Adam-like moments | basis refresh + rotate | refresh frequency、EMA、clipping |
| K-FAC | activation/backprop factors | factor inverse/eigendecomp | update frequency、damping、factorization |

参数量相同不表示 wall-clock 相同；矩阵 shape、kernel arithmetic intensity、distributed sharding 与 amortization 决定实际成本。

## 十、图：四种矩阵优化器的对象生成路径

先看图回答：四种方法分别从当前动量、梯度历史还是 activation/backprop 样本建立 state，哪些列因此不能写成同一个曲率近似？

![[00-知识库管理/_assets/figures/training-optimization/fig-muon-shampoo-soap-kfac-boundary-v1.svg|900]]

> [!figure] 图 TRN-30　Muon、Shampoo、SOAP、K-FAC 对象与证据边界
> 图从 raw gradient、gradient history、activation/backprop samples 四种输入分流，列出各自 state、变换和目标解释，并用红色隔离带阻止“都做矩阵乘法所以等价”的推论。来源：依据 [[S-2024-Jordan-Muon]]、[[S-2018-Gupta-Shampoo]]、[[S-2025-Vyas-SOAP]]、[[S-2015-Martens-Grosse-KFAC]] 独立绘制。

**怎样读图**：从每列最上方的随机对象向下追踪；若两列第一层输入和第二层 state 已不同，就不能仅凭输出 shape 宣称等价。

**图没有证明什么**：对照表不决定哪个方法在给定模型更好；性能仍需同预算、同调参协议的实验。

## 十一、本节出口

你应能写出四种方法的最小 state equation，构造“同当前梯度但历史/激活统计不同”的反例，并把 first-order norm geometry、gradient covariance 与 Fisher/GGN curvature 分成不同证据层。

## 练习与独立解答

- [[习题 - Muon、Shampoo、SOAP 与隐式曲率关系]]
- [[解答 - Muon、Shampoo、SOAP 与隐式曲率关系]]

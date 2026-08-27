---
type: solution
status: verified
area: [training, optimization, muon, preconditioning]
topic: "[[Muon、Shampoo、SOAP 与隐式曲率关系]]"
exercise: "[[习题 - Muon、Shampoo、SOAP 与隐式曲率关系]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Muon、Shampoo、SOAP 与隐式曲率关系

> [!warning] 使用边界
> 同 shape、PSD、Gram matrix 或 matrix root 都不是对象等价证据。先列随机变量、expectation/history 与 state，再比较 update。

## A. 识别与复述

### TRN30-A01
- Muon：当前 stochastic gradient，经 matrix momentum 得 $M_t$；state 主要是 momentum；对 $M_t$ 做 finite-step polar/NS。
- Shampoo：当前与历史 gradients；state 是各 tensor mode 的 Gram accumulators；用 inverse roots 双侧/多侧预条件。
- SOAP：Shampoo-like factor/basis 加 Adam-like first/second moments；在旋转基中自适应更新再旋回。
- K-FAC：layer activations 与 backprop signals；state 是其 covariance factors；用 damped inverse Kronecker factors近似 Fisher/GGN block solve。

### TRN30-A02
Shampoo 直接积累 gradient Gram；SOAP 用 Shampoo-style basis并另积累 Adam state；K-FAC 使用 activation/backprop covariance；Muon 只对当前 momentum matrix 做 polar，NS 中的 Gram 是临时多项式计算，不是跨样本 covariance state。

### TRN30-A03
“曲率”至少可能指 objective Hessian、GGN、true Fisher、empirical Fisher 或 gradient second moment。需核对 derivative scalar、label law、expectation measure、parameter point、per-sample vs batch reduction、model second derivatives、regularizer、factorization、damping 与 finite-sample estimator。未指定这些对象时，“隐式曲率”只能是宽泛机制语言。

## B. 手算与构造

### TRN30-B01
历史一累计 diagonal Gram：
$$
L=R=\operatorname{diag}(10^2+1^2,1^2+1^2)
=\operatorname{diag}(101,2).
$$
历史二为 $\operatorname{diag}(2,101)$。对当前 $I$，双侧 $-1/4$ 合成：
$$
\Delta_1\propto-\operatorname{diag}(101^{-1/2},2^{-1/2}),
$$
$$
\Delta_2\propto-\operatorname{diag}(2^{-1/2},101^{-1/2}).
$$
重置 momentum 的 Muon 对两者都只看到 $I$，exact polar update 都是 $-I$。同当前 gradient 不决定 history-based state。

### TRN30-B02
$x\mapsto cx,\delta\mapsto\delta/c$ 时
$$
G=(cx)^T(\delta/c)=x^T\delta
$$
不变，而
$$
A=\mathbb E[x^Tx]\mapsto c^2A,\qquad
S=\mathbb E[\delta^T\delta]\mapsto c^{-2}S.
$$
无阻尼 exact inverse 的左右常数在某些 convention 下可抵消；但 $(c^2A+\lambda I)^{-1}$ 不是简单的 $c^{-2}(A+\lambda I)^{-1}$，EMA、clipping、approximate inverse 也会破坏抵消。

### TRN30-B03
若所有 gradients diagonal，令 $S_{t,i}=\sum_{\tau\le t}g_{\tau,i}^2$，则 $L_i=R_i=S_{t,i}$，Shampoo 坐标更新为
$$
\frac{g_{t,i}}{S_{t,i}^{1/4}S_{t,i}^{1/4}}
=\frac{g_{t,i}}{\sqrt{S_{t,i}}}.
$$
polar 当前 gradient 为 $\operatorname{sign}(g_{t,i})$（非零处）。若只有当前 gradient 贡献，$\sqrt S=|g_t|$，二者相等；有过去能量时 $|g_t|/\sqrt S<1$，一般不等。

## C. 推导与证明

### TRN30-C01
$G_t\in\mathbb R^{m\times n}$ 给
$$
L_t=\epsilon I_m+\sum_\tau G_\tau G_\tau^T,\qquad
R_t=\epsilon I_n+\sum_\tau G_\tau^TG_\tau.
$$
$L^{-1/4}$ 左乘缩放 row-mode，$R^{-1/4}$ 右乘缩放 column-mode。若在共同 diagonal basis 中，两侧每坐标贡献四分之一次方，总尺度为对应 Kronecker preconditioner 的平方根型归一。非交换的一般矩阵必须按 matrix functions 计算，不能逐元素取 root。

### TRN30-C02
对 $G=x^T\delta$，
$$
\operatorname{vec}(G)=\delta^T\otimes x^T
$$
（转置/顺序随 vec convention）。其 outer product 是
$$
\operatorname{vec}(G)\operatorname{vec}(G)^T
=(\delta^T\delta)\otimes(x^Tx).
$$
取期望后 K-FAC 使用
$$
\mathbb E[(\delta^T\delta)\otimes(x^Tx)]
\approx\mathbb E[\delta^T\delta]\otimes\mathbb E[x^Tx].
$$
近似发生在 expectation of product 替换为 product of expectations；它需要依赖结构假设，不是纯代数恒等式。

### TRN30-C03
当前 $G_t$ 是整段 gradient history 到最后一个样本的投影；任意不同过去都可共享同一 $G_t$，故无法逆推出 $\sum_{\tau<t}G_\tau G_\tau^T$。同样，映射 $(x,\delta)\mapsto x^T\delta$ 是多对一，尺度变换已构造无穷多 factor pairs。缺少历史/因子，任何从 $G_t$ 到这些 states 的确定恢复都会把不同合法输入映成同一输出，必有至少一个错误。

## D. 边界、反例与纠错

### TRN30-D01
Muon 的 $X^TX$ 是在同一步 polynomial 中为计算 $p(X)$ 临时形成，随后通常不作为跨样本 expectation state保存。Fisher 是对 model-sampled score outer products 的期望；二者随机变量、时间聚合和 label law 都不同。矩阵乘法语法相同不能产生统计对象身份。

### TRN30-D02
SOAP 不仅获得 Shampoo eigenbasis，还在该 basis 中维护 Adam-like first/second moments，具有各自 EMA clock、epsilon、bias/scale 与 basis refresh staleness；旋转后 elementwise nonlinear update再旋回。是否做一次 SVD 不能概括这些 state 和时钟。

### TRN30-D03
- 可严格支持：Muon 是 spectral-step norm 下 exact polar target 的 first-order duality-map 近似；
- 机制假说：这种 layerwise geometry 可能改善某些 ill-scaled directions，并可与 modular norm 视角联系；
- 不能宣称：它无条件近似 Hessian/Fisher inverse、等价 K-FAC/Shampoo，或因此在任意网络上具有二阶收敛/普遍优势。

## E. AI 迁移

### TRN30-E01
固定当前 $G_t=I$，构造两段 past gradient 得不同 Shampoo state；再固定 $G_t=x^T\delta$，用 $cx,\delta/c$ 改变 K-FAC factors；Muon 可 reset 或保持同一 momentum；SOAP 另设相同/不同 basis refresh clock。断言各 state matrices、updates 与 direction cosines 按预期分离，并用 matched-loss toy 比较而不声称普遍性能。

### TRN30-E02
共享 model/data/seeds/token budget 与总 hyperparameter-search compute。报告 persistent/temporary bytes、factor/basis dimensions、NS/root/eigendecomp/rotation time、refresh frequency、communication bytes/P95、step time、peak、quality-vs-token/FLOP/wall-clock、失败 runs。每方法按其必要 LR/damping/grafting 搜索，不用单一超参数强行“公平”。

### TRN30-E03
至少问：目标 Fisher/Hessian/GGN 定义；score/label law；per-sample reduction；期望轴；state estimator；factorization independence；rank；damping；inverse/root solver与 residual；parameterization invariance范围；finite precision；update equation；同预算 baseline；ablation；system cost；跨 seed/task replication。任一核心对象未定义，应把 natural-gradient claim 降级为 heuristic analogy。

## 无提示重做

- [ ] 48 小时后从空白写出四种 state equation。
- [ ] 一周后用“同当前 G、不同历史”和“同 G、不同 x/δ”两个反例拆掉错误等价。

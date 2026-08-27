---
type: theorem
status: draft
area: [learning-theory/experts, hedge, multiplicative-weights]
aliases: [Hedge Algorithm, Exponential Weights, Weighted Majority]
node_id: LT-70
prerequisites: ["[[在线学习协议、Regret 与 Comparator]]", "[[基本不等式与界的构造]]", "[[最大熵原理与指数族]]"]
related: ["[[Online Gradient Descent 与 Mirror Descent]]", "[[Boosting、弱学习与指数损失]]", "[[Bandit Feedback 与强化学习接口]]"]
sources: ["[[S-1994-Littlestone-Warmuth-Weighted-Majority]]", "[[S-2012-Arora-Hazan-Kale-MW]]", "[[S-2006-CesaBianchi-Lugosi-Prediction-Games]]", "[[S-1997-Freund-Schapire-AdaBoost]]"]
exercises: ["[[习题 - Experts、Weighted Majority 与 Multiplicative Weights]]"]
solutions: ["[[解答 - Experts、Weighted Majority 与 Multiplicative Weights]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-hedge-potential-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# Experts、Weighted Majority 与 Multiplicative Weights

> [!abstract] 本章主问题
> 指数权重把每位专家的累计 loss 变成 Gibbs weight。证明只比较同一个 log-total-weight potential 的上界与下界：上界由算法每轮 expected loss 控制，下界由任一固定专家保留的重量控制。

## 一、学习目标

完成本章后，应能：

1. 写 experts full-information protocol；
2. 区分 deterministic Weighted Majority、randomized WM 与 Hedge；
3. 推导 exponential update；
4. 用 log potential 完整证明 regret bound；
5. 优化 learning rate 得 $\sqrt{T\log N}$；
6. 解释 loss range 与 scaling；
7. 处理 unknown horizon；
8. 说明 prior weights 如何替代 $\log N$；
9. 解释 entropy mirror descent 接口；
10. 识别 adaptive adversary 与 bandit feedback 边界。

## 二、Experts Protocol

有 $N$ 位专家。第 $t$ 轮 learner 选 distribution

$$
p_t\in\Delta^{N-1},
$$

environment 揭示

$$
\ell_t=(\ell_{t,1},\ldots,\ell_{t,N})\in[0,1]^N.
$$

algorithm expected loss：

$$
\widehat\ell_t=\langle p_t,\ell_t\rangle.
$$

目标相对最佳固定专家：

$$
\sum_t\widehat\ell_t-\min_i\sum_t\ell_{t,i}.
$$

## 三、Hedge Algorithm

初始化 $w_{1,i}=1$。第 $t$ 轮：

$$
p_{t,i}=\frac{w_{t,i}}{W_t},
\qquad
W_t=\sum_iw_{t,i},
$$

更新：

$$
\boxed{
w_{t+1,i}
=
w_{t,i}e^{-\eta\ell_{t,i}}.
}
$$

展开：

$$
p_{t,i}
\propto
\exp\left(
-\eta\sum_{s<t}\ell_{s,i}
\right).
$$

loss 小的专家保留更多质量，但任何有限累计 loss 专家权重不被立即清零。

## 四、Potential 的下界

固定任一专家 $i$：

$$
w_{T+1,i}
=
\exp(-\eta L_{T,i}),
\qquad
L_{T,i}=\sum_t\ell_{t,i}.
$$

所以

$$
\boxed{
\log W_{T+1}
\ge
-\eta L_{T,i}.
}
$$

这一步把 whole mixture 与 comparator 连接。

## 五、Potential 的逐轮上界

$$
\frac{W_{t+1}}{W_t}
=
\sum_ip_{t,i}e^{-\eta\ell_{t,i}}
=E_{i\sim p_t}e^{-\eta\ell_{t,i}}.
$$

对 $X\in[0,1]$，Hoeffding lemma：

$$
\log E[e^{-\eta X}]
\le
-\eta E[X]+\frac{\eta^2}{8}.
$$

因此

$$
\log\frac{W_{t+1}}{W_t}
\le
-\eta\widehat\ell_t+\frac{\eta^2}{8}.
$$

## 六、望远镜与 Regret Bound

初始 $W_1=N$。求和：

$$
\log W_{T+1}-\log N
\le
-\eta\sum_t\widehat\ell_t
+\frac{\eta^2T}{8}.
$$

与下界合并：

$$
-\eta L_{T,i}
\le
\log N-\eta\widehat L_T+\frac{\eta^2T}{8}.
$$

整理：

$$
\boxed{
\widehat L_T-L_{T,i}
\le
\frac{\log N}{\eta}
+\frac{\eta T}{8}.
}
$$

对最佳专家同样成立。

## 七、优化 Learning Rate

令

$$
\eta^*=\sqrt{\frac{8\log N}{T}},
$$

得到

$$
\boxed{
\operatorname{Reg}_T
\le
\sqrt{\frac{T\log N}{2}}.
}
$$

常数随使用 $e^{-η\ell}$、$(1-η)^\ell$ 或更粗不等式改变；$\sqrt{T\log N}$ 量级和 assumptions 才是主线。

## 八、Prior-Weighted Experts

初始化 $w_{1,i}=\pi_i$，$\sum_i\pi_i=1$。下界变为

$$
\log W_{T+1}\ge\log\pi_i-\eta L_i,
$$

从而

$$
\boxed{
\widehat L_T-L_i
\le
\frac{\log(1/\pi_i)}{\eta}
+\frac{\eta T}{8}.
}
$$

短描述/高先验专家付更小 complexity penalty；data-dependent prior 会改变保证。

## 九、Loss Scaling

若 loss 在 $[a,b]$，令

$$
\widetilde\ell=\frac{\ell-a}{b-a}\in[0,1].
$$

regret 乘回 $(b-a)$。忽略 range 会给错误 learning rate；unbounded/heavy-tailed losses 需 clipping、robust potential 或额外 moment assumptions。

## 十、Unknown Horizon

若不知道 $T$：

- doubling trick：按 $1,2,4,\ldots$ epochs 重启并设对应 $\eta$；
- time-varying $\eta_t\asymp\sqrt{\log N/t}$；
- parameter-free/adaptive algorithms。

重启损失求和仍为 $O(\sqrt{T\log N})$，但 constants 和 anytime property 必须核算。

## 十一、Weighted Majority 与 Hedge

经典 Weighted Majority 针对 binary mistakes，错误专家乘 $\beta<1$；deterministic 取加权多数，randomized 按 weights 采样。Hedge 把 loss 扩展到 $[0,1]$ 并用 exponential update。

算法名称相近，mistake bound、expected loss bound 与 update parameter convention 不应混抄。

## 十二、Entropy Regularization 视角

Hedge 也可写：

$$
p_t
=
\arg\min_{p\in\Delta_N}
\left\{
\eta\left\langle p,\sum_{s<t}\ell_s\right\rangle
+D_{\rm KL}(p\Vert\pi)
\right\}.
$$

这是一种 FTRL/entropy mirror descent。$\log N$ 来自 simplex 上的 KL diameter，而非专家问题专属魔法。

## 十三、一个手算更新

$N=3,\eta=\log2$，初始 weights $(1,1,1)$；第一轮 losses $(0,1,1/2)$：

$$
w_2=(1,1/2,2^{-1/2}).
$$

归一化后专家 1 概率最大，但其他专家仍保留质量。若第二轮专家 1 损失大，weights 可恢复，而硬淘汰无法。

## 十四、边界

- bandit feedback 下看不到所有 $\ell_{t,i}$，不能直接更新；
- adversary 若看当前 sampled action 再设 loss，可线性 regret；
- shifting comparator 需加 switch/path penalty；
- correlated experts 不使 $\log N$ 自动变成有效数量；
- computationally huge/infinite expert class 需 oracle、cover 或 prior integral。

## 十五、图：一条 Potential 的上下夹逼

先看图回答：$\log N/\eta$ 和 $\eta T/8$ 分别来自证明的哪一侧，为什么一个随 $\eta$ 降、一个随 $\eta$ 升？

![[00-知识库管理/_assets/figures/learning-theory/fig-hedge-potential-v2.svg|900]]

> [!figure] 图 20.9-02　Hedge 更新、总权重 potential 与 regret 夹逼
> 左栏展示 cumulative loss→Gibbs weights；中栏对 $\log W_{T+1}$ 做 comparator 下界与 Hoeffding 上界；右栏呈现 learning-rate、prior、range 与 feedback 边界。来源：依据 Littlestone–Warmuth、Arora–Hazan–Kale 与 Cesa-Bianchi–Lugosi 独立绘制；由 [[plot_online_learning_v2.py]] 确定性生成。

**怎样读图**：下界保住任一专家，上界累计 learner mixture loss；合并后才出现 comparator regret。

**图没有证明什么**：图没有证明 bandit/adaptive-after-action 环境下同一更新有效，也没有证明 best switching expert 的 regret。

## 十六、常见错误

1. 当前 loss 揭示后才选 $p_t$；
2. 更新符号把好专家降权；
3. 忘记 $W_1=N$；
4. Hoeffding range 不满足；
5. 对 sampled realized loss 与 mixture expected loss混用；
6. 用 test-selected prior；
7. unknown horizon 偷用未来 $T$；
8. full-information update 套 bandit。

## 十七、最小记忆与掌握标准

> [!summary]
> - Hedge 权重是累计 loss 的 exponential；
> - potential 下界来自 comparator weight；
> - potential 上界来自 mixture mgf；
> - 平衡 complexity 与 curvature 得 $\sqrt{T\log N}$；
> - prior 把 $\log N$ 替换为 $\log(1/\pi_i)$；
> - feedback/adversary/comparator 改变 theorem。

能复述算法（A）、手算 weights（B）、证明 potential bound（C）、审计 range/horizon/adversary（D），并迁移到模型路由/portfolio 等 experts 系统（E）。

## 十八、练习与独立详解

- [[习题 - Experts、Weighted Majority 与 Multiplicative Weights]]
- [[解答 - Experts、Weighted Majority 与 Multiplicative Weights]]

## 参考来源

- [[S-1994-Littlestone-Warmuth-Weighted-Majority]]
- [[S-2012-Arora-Hazan-Kale-MW]]
- [[S-2006-CesaBianchi-Lugosi-Prediction-Games]]
- [[S-1997-Freund-Schapire-AdaBoost]]

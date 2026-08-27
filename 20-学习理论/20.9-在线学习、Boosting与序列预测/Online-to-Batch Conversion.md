---
type: theorem
status: draft
area: [learning-theory/online-learning, generalization, online-to-batch]
aliases: [Online-to-Batch Conversion, Prequential Generalization, Regret-to-Risk Bridge]
node_id: LT-75
prerequisites: ["[[在线学习协议、Regret 与 Comparator]]", "[[随机、对抗与自适应序列的区别]]", "[[浓缩不等式]]"]
related: ["[[经验风险最小化、近似 ERM 与超额风险分解]]", "[[算法稳定性与替换一个样本]]", "[[训练集、验证集、测试集与自适应复用]]"]
sources: ["[[S-2004-CesaBianchi-Conconi-Gentile-Online-Batch]]", "[[S-2006-CesaBianchi-Lugosi-Prediction-Games]]", "[[S-2012-Shalev-Online-Learning-OCO]]"]
exercises: ["[[习题 - Online-to-Batch Conversion]]"]
solutions: ["[[解答 - Online-to-Batch Conversion]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-online-to-batch-conversion-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# Online-to-Batch Conversion

> [!abstract] 本章主问题
> regret 比较一条序列上的累计损失，risk 是新样本上的期望损失。二者之间缺的桥梁不是换一个符号，而是：每个在线预测器只能依赖过去样本，因此下一样本仍可充当条件独立测试点；随后还要明确输出随机 iterate、平均预测器还是最后 iterate。

## 一、学习目标

完成本章后，应能：

1. 写出 iid online-to-batch 的 filtration；
2. 证明 next-example loss 的条件期望等于 population risk；
3. 把 expected regret 除以 $T$ 转成 excess risk；
4. 区分 randomized iterate 与 averaged predictor；
5. 说明 Jensen 在平均预测器中用在哪里；
6. 解释为何 last iterate 不由平均 regret 自动控制；
7. 写出 martingale high-probability bridge；
8. 区分固定 population comparator 与 data-selected comparator；
9. 识别 shuffle、dependence、drift 与 adaptive validation 下的断点；
10. 为流式 AI 训练建立 prequential 评价合同。

## 二、Batch 风险对象

令 $Z=(X,Y)\sim P$，loss $\ell(h,Z)\in[0,1]$，population risk 为

$$
L(h)=E_{Z\sim P}[\ell(h,Z)].
$$

给 iid 样本 $Z_1,ldots,Z_T$。在线算法在第 $t$ 轮开始时只使用 $Z_1,ldots,Z_{t-1}$ 产生 $h_t$；因此 $h_t$ 是 $\mathcal F_{t-1}=\sigma(Z_1,ldots,Z_{t-1})$-measurable。

## 三、桥梁的核心条件期望

由于 $Z_t$ 与过去独立且同分布为 $P$，

$$
\boxed{
E[\ell(h_t,Z_t)\mid\mathcal F_{t-1}]=L(h_t).
}
$$

注意 $h_t$ 是随机的，但在条件于过去后已经固定；$Z_t$ 才是 fresh test point。这一步正是 online protocol 中“先预测、后看当前样本”的统计价值。

## 四、Expected Online-to-Batch：随机 Iteration

假设在线算法对任意 comparator $h\in\mathcal H$ 满足 expected regret

$$
E\left[\sum_{t=1}^T\ell(h_t,Z_t)-\sum_{t=1}^T\ell(h,Z_t)\right]
\le B_T.
$$

取 expectation，利用上节恒等式和 $E\ell(h,Z_t)=L(h)$：

$$
\frac1T\sum_{t=1}^TE[L(h_t)]
\le L(h)+\frac{B_T}{T}.
$$

令 $I\sim\operatorname{Unif}\{1,ldots,T\}$，且在训练后独立采样，输出 $\widehat h=h_I$。则

$$
\boxed{
E[L(\widehat h)]
\le\inf_{h\in\mathcal H}L(h)+\frac{B_T}{T}.
}
$$

若 $B_T=O(\sqrt T)$，excess risk 为 $O(T^{-1/2})$。

## 五、为什么随机 Iteration 合法

随机化并不是说部署时必须永远随机选模型；它是把“平均的 $h_t$ 有一个好”变成一个明确输出分布。若只说“存在某个好 iterate”，我们通常不知道是哪一个；用同一训练数据挑最优 iterate 又会引入选择偏差。

实践可用独立 validation 选 iterate，但风险界要再支付 validation selection complexity。

## 六、Convex Loss 下的平均预测器

若预测集合凸，且对每个 $z$，$a\mapsto\ell(a,z)$ 凸，可输出平均 prediction

$$
\bar h_T(x)=\frac1T\sum_{t=1}^Th_t(x).
$$

由 Jensen，逐点有

$$
\ell(\bar h_T,z)
\le\frac1T\sum_t\ell(h_t,z).
$$

再取 $P$ 期望：

$$
L(\bar h_T)
\le\frac1T\sum_tL(h_t).
$$

因此平均预测器继承同一 excess-risk bound。对 0–1 loss 或离散模型参数直接平均，Jensen 不适用。

## 七、Last Iterate 为什么没有自动保证

平均 regret 小只控制

$$
\frac1T\sum_tL(h_t),
$$

允许少数 iterate 很差，甚至最后一个很差。例如前 $T-1$ 个 risk 为 0，最后一个 risk 为 1，平均 risk 仍只有 $1/T$。last-iterate guarantee 需要算法稳定性、strong convexity、step decay、monotonicity 或专门 theorem。

## 八、High-Probability Bridge：第一条 Martingale

定义

$$
X_t=L(h_t)-\ell(h_t,Z_t).
$$

由核心条件期望，$E[X_t\mid\mathcal F_{t-1}]=0$；且 loss 在 $[0,1]$ 时 $|X_t|\le1$。Azuma/Hoeffding 型界给：以至少 $1-\delta$ 的概率，

$$
\frac1T\sum_tL(h_t)
\le\frac1T\sum_t\ell(h_t,Z_t)
+O\left(\sqrt{\frac{\log(1/\delta)}T}\right).
$$

Freedman 可用 conditional variance 得到更细的 data-dependent 项。

## 九、Comparator 还需要第二条浓缩吗

若 regret 比较的是固定 population minimizer $h^*$，则

$$
\frac1T\sum_t\ell(h^*,Z_t)
$$

仍需和 $L(h^*)$ 比较；对固定 $h^*$ 用普通 Hoeffding 即可，不需对全类 uniform bound。

若 comparator 是看数据后选出的 ERM $\widehat h$，它不再固定，不能直接套单函数浓缩；需要 uniform convergence、stability、sample splitting 或另一个 online argument。

## 十、一个明确的高概率模板

假设 deterministic pathwise regret $R_T\le B_T$，loss 在 $[0,1]$，并选固定 $h^*\in\arg\min_hL(h)$。分别控制在线 martingale 与 comparator empirical deviation，union bound 后，以至少 $1-\delta$ 概率：

$$
\frac1T\sum_tL(h_t)
\le L(h^*)+\frac{B_T}{T}
+2\sqrt{\frac{\log(2/\delta)}{2T}}.
$$

常数可用更精细不等式改善，但两条随机误差的来源必须分账。

## 十一、Prequential 解释

online loss

$$
\ell(h_1,Z_1),\ell(h_2,Z_2),\ldots
$$

是 test-then-train：当前样本先评价由过去训练出的模型，再用于更新。它避免“在同一点先训练再测试”的直接泄漏，也连接 prequential coding 和流式监控。

但反复查看累计曲线并自适应选择停止时间，会再产生 optional-stopping/selection 问题。

## 十二、依赖、Shuffle 与 Drift

核心等式在以下情形会改变：

- random permutation：$Z_t$ 条件于过去不是原始 $P$，而是剩余总体分布；
- time series：$Z_t$ 与过去依赖，需 mixing/martingale process 条件；
- covariate drift：条件 risk $L_t(h)$ 随 $t$ 变化；
- action-dependent data：当前 policy 改变未来 $Z$，需 policy regret/causal model；
- data reuse：若 $h_t$ 偷看 $Z_t$，fresh-test 恒等式直接断裂。

## 十三、手算速率

若 regret bound 为 $B_T=4\sqrt T$，则 expected excess risk 至多 $4/\sqrt T$。要该项不超过 0.02，需要

$$
\frac4{\sqrt T}\le0.02
\quad\Longrightarrow\quad
T\ge40{,}000.
$$

这还不含 high-probability confidence 项，也不含 approximation error。

## 十四、图：Regret 到 Risk 之间的三座桥

先看图回答：若 $h_t$ 使用了当前 $Z_t$ 的 label，左栏哪一个条件箭头断裂？

![[00-知识库管理/_assets/figures/learning-theory/fig-online-to-batch-conversion-v2.svg|900]]

> [!figure] 图 20.9-07　从 online regret 到 batch risk 的对象变换
> 左栏是 history-measurable predictor 与 fresh example；中栏分开随机 iterate、凸平均和 last iterate；右栏给 expected/high-probability、fixed/data-selected comparator 与依赖数据边界。来源：依据 Cesa-Bianchi–Conconi–Gentile、Cesa-Bianchi–Lugosi 与 Shalev-Shwartz 独立绘制；由 [[plot_online_learning_part2_v2.py]] 确定性生成。

**怎样读图**：每跨一座桥都写明独立性、输出对象和概率量词；不要只把 $R_T$ 除以 $T$。

**图没有证明什么**：图没有给最后 iterate、非凸参数平均、依赖序列或自适应模型选择的免费保证。

## 十五、AI 接口

- 流式微调：每批先评价后更新，区分 prequential risk 与训练 loss；
- LLM checkpoint selection：平均 regret 不会自动认证最后 checkpoint；
- federated/continual learning：client/time dependence 要替换 iid bridge；
- online routing：action 若改变未来 traffic，需要 policy-level conversion；
- model averaging：只有 prediction space 与 loss convexity匹配时可直接 Jensen。

## 十六、常见错误

1. 把 regret/T 直接称为 risk；
2. 忘记 $h_t$ 只能依赖过去；
3. 以为 average guarantee 自动覆盖 last iterate；
4. 在 0–1 loss 上无条件平均参数；
5. 对 data-selected comparator 用 fixed-function Hoeffding；
6. 把 random permutation 当 iid；
7. expected bound 冒充 high probability；
8. 重复查看 prequential curve 却不记 selection。

## 十七、最小记忆与掌握标准

> [!summary]
> - 核心桥：$E[\ell(h_t,Z_t)\mid\mathcal F_{t-1}]=L(h_t)$；
> - randomized iterate 把平均 risk 变成单个输出的期望 risk；
> - convex prediction/loss 时可用 Jensen 平均；
> - last iterate 需要额外结构；
> - high probability 需要 martingale + comparator deviation；
> - dependence、drift、action feedback 与 model selection 都会改 theorem。

能写条件期望（A）、算速率（B）、证明 expected/high-probability bridge（C）、审计 last-iterate/selection/dependence（D），并设计流式 AI 的 prequential 合同（E）。

## 十八、练习与独立详解

- [[习题 - Online-to-Batch Conversion]]
- [[解答 - Online-to-Batch Conversion]]

## 参考来源

- [[S-2004-CesaBianchi-Conconi-Gentile-Online-Batch]]
- [[S-2006-CesaBianchi-Lugosi-Prediction-Games]]
- [[S-2012-Shalev-Online-Learning-OCO]]

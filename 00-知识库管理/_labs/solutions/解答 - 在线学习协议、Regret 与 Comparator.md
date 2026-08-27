---
type: solution
status: draft
topic: "[[习题 - 在线学习协议、Regret 与 Comparator]]"
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - 在线学习协议、Regret 与 Comparator

## A

### LT-ONL-A01
第 $t$ 轮令历史为 $H_{t-1}$：learner 先用 $H_{t-1}$ 选 $w_t$，environment 再揭示 $\ell_t$，learner 承受 $\ell_t(w_t)$，最后把 $\ell_t$ 加入历史。选 $w_t$ 时可见 $H_{t-1}$，不可见当前 $\ell_t$；若当前 loss 预先可见，逐轮取 $\arg\min_w\ell_t(w)$ 即可，问题已经改变。

### LT-ONL-A02
对 comparator class $\mathcal U$，
$$
R_T=\sum_{t=1}^T\ell_t(w_t)-\inf_{u\in\mathcal U}\sum_{t=1}^T\ell_t(u),\qquad \bar R_T=R_T/T.
$$
若 $R_T=o(T)$，即 $\bar R_T\to0$，称 no-regret。这里 comparator 事后选择，但在所有轮次使用同一个 $u$。

### LT-ONL-A03
population risk 是固定分布下的期望损失；offline optimization gap 比较同一目标函数的函数值；mistake count 是离散预测错误次数；regret 比较序列累计损失与声明的 comparator。它们可经额外定理连接，但定义上不是同一对象。

## B

### LT-ONL-B01
learner loss 为 $0+1+0=1$。两个固定专家累计 loss 都是 $2$，故
$$R_3=1-2=-1.$$
负 regret 表示切换策略胜过全部固定专家，并不矛盾。

### LT-ONL-B02
可以。$R_T=(T/2-\sqrt T)-T/2=-\sqrt T$，而 $R_T/T=-1/\sqrt T\to0$。no-regret 通常是上界性质，不要求 regret 非负。

### LT-ONL-B03
$3\sqrt T/T=3/\sqrt T\le0.03$，所以 $\sqrt T\ge100$，即 $T\ge10{,}000$。

## C

### LT-ONL-C01
两个 actions。learner 先选 $w_t$ 后，environment 令被选 action loss 为 $1$，另一个为 $0$。learner 总 loss 为 $T$；允许每轮自由切换的 comparator 总 loss 为 $0$，dynamic regret 为 $T$。这说明无限制 sequence comparator 不可能普遍 sublinear。

### LT-ONL-C02
令 losses 确定性交替 $(0,1),(1,0),\ldots$，learner 从第二轮起预测交替结构并选零损失 action。两个 fixed actions 各损失约 $T/2$，learner 仅首轮可能有损失，故 regret 约为 $-T/2$。benchmark 不是逐轮最优，因此相对差可以为负。

### LT-ONL-C03
full-information estimator 可直接令 $\widehat\ell_{t,i}=\ell_{t,i}$，因为所有坐标可见；bandit 下只有 $\ell_{t,I_t}$ 可见，未选坐标不可计算。要无偏估计需探索并用
$$\widehat\ell_{t,i}=\frac{\mathbf 1\{I_t=i\}\ell_{t,i}}{p_{t,i}},$$
且要求 $p_{t,i}>0$。直接共用会调用不可观测数据。

## D

### LT-ONL-D01
报告至少缺少：loss range、learner 随机性、environment 是 oblivious 还是 non-anticipating adaptive、是否能看当前 action/coin、full 或 bandit feedback、static/dynamic/policy comparator，以及结论是 pathwise、in expectation 还是 high probability。任一项改变都可能改变 theorem。

### LT-ONL-D02
推荐 action 会改变用户状态与以后可见数据，因此“把实际 loss sequence 固定后让另一个 action 重放”不再是同一个世界。external regret 只在已发生序列上比较数值，没有重建替代 policy 引起的反事实状态轨迹；这正是 policy regret/causal evaluation 要补的对象。

### LT-ONL-D03
可令 $\mathcal F_{t-1}$ 包含已发 query、已返回 label、cluster 标识、模型过去随机数与动作；当前 query 可由 $\mathcal F_{t-1}$ 自适应选出；$I_t$ 用 fresh coin 采样；label 在随机延迟 $d_t$ 后才进入 $\mathcal F_{t+d_t}$。独立 unit 应按 user cluster 而非单条 interaction，浓缩时必须处理 cluster dependence 与 delay。

## E

### LT-ONL-E01
每个模型是 expert，prompt/context 是当轮 context；router 先选模型，返回答案后得到 loss，例如 $\ell=\alpha\,$质量损失$+\beta\,$延迟$+\gamma\,$成本。若只执行一个模型就是 bandit feedback；离线评分所有模型才近似 full information。comparator 可设为 best fixed model、按任务族的固定 policy，或限制切换次数的 model sequence。

### LT-ONL-E02
稳定环境基线可用 static regret；真实最优模型缓慢漂移可用带 path length 的 dynamic regret；模型版本偶尔更替可用 shifting regret；部署 action 会改变未来用户/数据时需要 policy regret。应由目标反事实决定 benchmark，而不是同时报告几个名字。

### LT-ONL-E03
合格 claim card 应写：每轮事件顺序与 $\mathcal F_{t-1}$；action/loss range；feedback；learner fresh randomness；environment 可见性；comparator class；保证是期望还是 $1-\delta$ 高概率；以及结论只覆盖累计相对损失，不自动覆盖 population risk 或最后一步表现。

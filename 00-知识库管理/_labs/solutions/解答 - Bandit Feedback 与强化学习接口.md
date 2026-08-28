---
type: solution
status: draft
topic: "[[Bandit Feedback 与强化学习接口]]"
exercise: "[[习题 - Bandit Feedback 与强化学习接口]]"
created: 2026-08-23
updated: 2026-08-28
---
# 解答 - Bandit Feedback 与强化学习接口
## A
### LT-BND-A01
stochastic MAB：每 arm 固定 reward law，比 best mean arm；adversarial bandit：loss vector 任意、只见 chosen coordinate，比 best fixed arm in hindsight；contextual bandit：先见 $x_t$，再选 action，只见 chosen reward，比 policy class $\pi(x)$。
### LT-BND-A02
realized regret 用实际随机 rewards；pseudo-regret 用 arm means 和 expected pulls；best-arm identification 不累计 reward regret，而要求在预算/置信下输出正确最优 arm。
### LT-BND-A03
bandit 无持久 state，通常一轮 action 只决定当轮 reward；MDP 有 state transition，action 改变未来 state distribution，长期 return 跨多步，因而有 credit assignment、value/Bellman 与 occupancy 问题。
## B
### LT-BND-B01
估计 vector $(0,0.6/0.2)=(0,3)$。对 arm 2，条件二阶矩为 $\ell_2^2/p_2=0.36/0.2=1.8$；不是观测到的平方 9，而是再对采样事件取期望后的值。
### LT-BND-B02
$\Delta_2=0.2$，故 pseudo-regret 为 $0.2\times30=6$。
### LT-BND-B03
$\sqrt{T\log K}\approx\sqrt{23025.9}\approx151.7$；$\sqrt{TK\log K}\approx479.9$，相差 $\sqrt{10}\approx3.16$，体现 bandit feedback 的 arm-count 代价。
## C
### LT-BND-C01
在 $\ell_t$ 先于 $I_t$ 固定且 $p_{t,i}>0$ 时，$E[\mathbf1\{I_t=i\}\ell_{t,i}/p_{t,i}\mid\mathcal F_{t-1},\ell_t]=p_{t,i}\ell_{t,i}/p_{t,i}=\ell_{t,i}$。平方同理为 $p_{t,i}\ell_{t,i}^2/p_{t,i}^2=\ell_{t,i}^2/p_{t,i}$。
### LT-BND-C02
每次选最优 arm 无 mean loss；选 arm $i$ 的 expected reward shortfall 是 $\Delta_i$。用 indicator 分组：$T\mu^*-E\sum_tr_{t,I_t}=E\sum_t\Delta_{I_t}=\sum_i\Delta_iE[N_i(T)]$。
### LT-BND-C03
两 Bernoulli arms 均值 $0.6,0.4$。算法首轮各试一次后永远选 empirical mean 较高者。以正概率最优 arm 首次得 0、次优得 1，之后算法永远选次优，产生线性 regret；缺的是持续探索/置信更新。
## D
### LT-BND-D01
UCB 的 confidence bonus 假设每 arm observations 围绕固定 mean 浓缩。adversary 可随时间改 rewards，使 sample mean 不估计稳定 $\mu_i$，gap 也未定义。需改用 EXP3 等 adversarial algorithm，并声明 adversary 可见性与 expected/high-prob regret。
### LT-BND-D02
不能从该日志非参数识别，因为 behavior propensity $b(3\mid x)=0$，IPS denominator 无定义，且没有该 action 的反事实 outcome。需要新探索、结构模型及可辩护外推假设；单纯扩大样本量无效。
### LT-BND-D03
static contextual regret把实际 reward sequence 固定后比较 policy，但另一推荐 policy 会生成不同兴趣状态和未来 contexts/rewards。需要 stateful MDP、policy regret 或因果动态模型。
## E
### LT-BND-E01
若每次可离线评测所有模型结果，是 full information；只调用一个模型且 query 独立到达，是 contextual bandit；路由改变用户状态、缓存/工具环境并影响后续 reward，则需 RL/policy model。判据是未选反馈可见性与 action 是否改变未来 state。
### LT-BND-E02
同时记录 reward regret、累计安全 cost 与 per-round hard constraints；设保守 baseline 和最大性能下降概率；只在认证 action set 中探索；propensity 全量日志；uncertainty 超阈值回退 baseline/人工；事故触发停止规则。安全目标需独立 guarantee。
### LT-BND-E03
claim card：full/bandit feedback；contexts/states；behavior propensities 与 exploration floor；stochastic/adversarial environment；arm/policy comparator；horizon/transition；expected/realized量词；offline overlap；constraint、baseline、override 与 stopping。

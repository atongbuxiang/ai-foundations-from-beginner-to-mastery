---
type: assessment
status: draft
material_status: regression-passed
learning_status: not-attempted
area: [learning-theory/online-learning, learning-theory/boosting, learning-theory/bandits]
assessment_id: ONLINE-CUM-01
scope: [LT-69, LT-70, LT-71, LT-72, LT-73, LT-74, LT-75, LT-76]
formal_prerequisite: REL-CUM-01-retained
time_limit_minutes: 240
oral_limit_minutes: 25
points: 100
solution: "[[阶段测验解答 - 在线学习、Boosting 与序列预测（20.9）]]"
experiment: "[[实验 - 在线学习、Boosting 与序列预测累计复现门]]"
related: ["[[在线学习、Boosting 与序列预测 MOC]]", "[[学习理论完整课程地图与掌握标准]]", "[[练习与测验 MOC]]", "[[推导与实验 MOC]]"]
created: 2026-08-29
updated: 2026-08-29
---

# 阶段测验 - 在线学习、Boosting 与序列预测（20.9）

> [!abstract] 这卷真正考什么
> 不考“背 Hedge、AdaBoost 和 UCB 的更新式”，考能否先写 **move order—filtration—feedback—randomness—comparator—potential—probability statement—deployment boundary**。Regret、mistake bound、training exponential loss、population risk 和 bandit counterfactual value 不是同一个对象。

## 一、答案与输出隔离协议

1. 生成唯一 `attempt_id`，记录题卷 commit、起止时间和闭卷原稿 SHA-256；
2. 先完成 **25 分钟口试**，再完成 **240 分钟闭卷**，不得查看详解、脚本、canonical SVG 或 stdout；
3. 封存第 5—10 题的数值、三轨方向预测与至少六条“不能推出”；
4. 评分者才公布 `scorer nonce`：以 `SHA256(attempt_id || nonce) mod 3` 指定 A/B/C 主轨，并从其他两轨各取一组 blind 参数；
5. 只有原稿数值与方向预测、新 stdout、新 SVG/hash 一致时，计算轨才合格；canonical 图不能代替 blind 证据；
6. 订正后 48 小时换机制重做，14 天后在陌生交互 AI 报告中完成对象—定理—评价路由。

> [!warning] 正式个人前置
> `REL-CUM-01 retained` 尚未由个人证据满足，因此本卷只能诊断性作答，不得记为 `passed` 或 `retained`。

## 二、口试（25 分钟，不计入 100 分但必须通过）

不看笔记，按顺序回答：

1. 写出 full-information online learning 一轮的行动顺序，并定义 static external regret；
2. 解释 oblivious、non-anticipating adaptive 和 current-action-aware adversary 的信息差别；
3. 用一句话说出 Hedge 和 OGD 各自的 potential，以及它们怎样望远镜；
4. 口述 Perceptron 的 progress/norm 双账本与 AdaBoost 的 $\prod_t Z_t$ 恒等式；
5. 说明 online regret 为什么不会自动变成 population risk，IPS 无偏为什么不等于安全部署。

必须同时写对对象、条件和概率层次；只背公式不通过。

## 三、闭卷题（100 分）

### 第 1 题：八层序列学习账本（5 分）

对一个“在线模型路由器比离线模型更智能”的声明，逐层写出：

1. protocol/move order；2. filtration/adversary visibility；3. feedback；4. comparator；5. potential/certificate；6. probability statement；7. conversion/evaluation；8. deployment boundary。

每层必须给一个可被日志或数学式检查的字段。

### 第 2 题：Protocol、Comparator 与 Regret（5 分）

设决策 $a_t\in\mathcal A$，loss vector $\ell_t\in[0,1]^{|\mathcal A|}$。

1. 写出 full-information 协议和 static external regret；
2. 证明 regret 可以为负；
3. 说明 $R_T=o(T)$ 精确推出什么，不推出什么；
4. 比较 fixed、switching 和 policy comparator。

### 第 3 题：Hedge Potential 证明（5 分）

对 $N$ 位专家、$\ell_{t,i}\in[0,1]$，从

$$
p_{t,i}=\frac{e^{-\eta L_{t-1,i}}}{\sum_j e^{-\eta L_{t-1,j}}}
$$

出发，完整证明

$$
\sum_{t=1}^T\langle p_t,\ell_t\rangle-\min_iL_{T,i}
\le \frac{\log N}{\eta}+\frac{\eta T}{8}.
$$

标明 lower potential、Hoeffding lemma 和望远镜各用在哪一步。

### 第 4 题：OGD/OMD 与对手信息（5 分）

1. 从投影非扩张性推出 OGD 的一步不等式和 regret bound；
2. 把平方距离换成 $D_\psi(u,x_t)$，说明 primal/dual norm 如何进入 OMD；
3. 构造一个看到当轮 realized action 后才定 loss 的两行动对手，证明它可制造线性 external regret。

### 第 5 题：A 轨——Hedge 手算（8 分）

令 $\eta=\log2$，四轮三专家 loss 为

$$
\begin{pmatrix}
0&1&1\\
1&0&1\\
0&1&0\\
1&1&0
\end{pmatrix}.
$$

从均匀权重开始，逐轮算 $p_t$、算法期望损失、各专家累计损失、最终分布、external regret 和上题的 bound。解释为什么“界比实际 regret 大”不是证明失败。

### 第 6 题：A 轨——OGD 与可见性反例（7 分）

在 $[-1,1]$ 上以 $x_1=0$、$\eta=1/2$ 运行 projected OGD，线性 loss 梯度为

$$
(1,-2,1,2,-1).
$$

算出每轮决策、算法累计 loss、best fixed comparator、regret 和 comparator-specific potential bound。再对 action 序列 $(1,2,1,2,2,1)$ 使用“当轮所选 action loss 为 1，另一 action loss 为 0”的对手，算 regret。

### 第 7 题：B 轨——Perceptron 双账本（8 分）

从 $w_0=0$ 开始，遇到 $y_t\langle w_t,x_t\rangle\le0$ 就更新 $w_{t+1}=w_t+y_tx_t$。顺序数据为

$$
((1,0),+1),\quad((0,1),+1),\quad((-1,-1),-1).
$$

1. 手算 prediction/update；
2. 对 $u=(1,1)/\sqrt2$ 算 $R,\gamma,M$；
3. 从 $\langle w_M,u\rangle\ge M\gamma$ 和 $\|w_M\|^2\le MR^2$ 推出 $M\le(R/\gamma)^2$；
4. 解释该证书为何不是 population generalization bound。

### 第 8 题：B 轨——AdaBoost 指数势能（7 分）

四个样本初始均匀，两轮 signed margins $s_{t,i}=y_ih_t(x_i)$ 为

$$
s_1=(1,1,1,-1),\qquad s_2=(-1,-1,1,1).
$$

逐轮算 $\varepsilon_t,\alpha_t,Z_t,D_{t+1}$，再算 $\prod_tZ_t$、四个 ensemble margins 和 training error。证明

$$
\frac1m\sum_i e^{-y_iF_T(x_i)}=\prod_tZ_t,
\qquad
\widehat R_{0/1}(F_T)\le\prod_tZ_t,
$$

并指出它们不是 test-error theorem。

### 第 9 题：C 轨——Online-to-Batch（8 分）

设 $Z_1,…,Z_T$ iid，$h_t$ 只依赖 $Z_{<t}$。

1. 证明 $\mathbb E[\ell(h_t,Z_t)\mid Z_{<t}]=R(h_t)$；
2. 用随机 iterate $h_I$（$I$ 与数据独立且均匀）推出 expected risk identity；
3. 说明 convex prediction/loss 下平均预测器的 Jensen 路线；
4. 对 risks $(0.2,0.4,0.1,0.3)$ 和 comparator risk $0.1$ 算 random-iterate risk、online regret 和 excess risk；
5. 解释 last iterate、drift 与 adaptive model selection 为何需要额外论证。

### 第 10 题：C 轨——UCB、IPS 与 Overlap（8 分）

1. 对 counts $(20,10)$、empirical means $(0.6,0.5)$ 以
   $$U_i=\widehat\mu_i+\sqrt{2\log(30)/N_i}$$
   计算两个 UCB 并选 arm；
2. logging policy $p=(0.5,0.3,0.2)$，target policy $\pi=(0.2,0.2,0.6)$，loss vector $\ell=(0.2,0.6,0.9)$，本次选到第 3 臂。算 vector IPS、target-policy 单次 IPS、true target risk、方差与 $\max_i\pi_i/p_i$；
3. 证明 IPS 无偏，并构造 $p_i=0,\pi_i>0$ 的不可识别反例；
4. 说明 bandit 与 RL 的 state-transition/long-horizon 边界。

### 第 11 题：八节点证书路由表（7 分）

为 LT-69—76 各写一行：**target quantity、关键假设、主势能/恒等式、概率类型、不能推出**。至少准确分开：

- pathwise regret 与 expected/high-probability regret；
- sequence mistake 与 population risk；
- empirical exponential loss 与 test error；
- bandit one-step feedback 与 RL long-horizon return。

### 第 12 题：删条件反例（7 分）

对下列每个错误声明，给最小反例或指出缺失的量词：

1. “任何看过当前 action 的 adversary 下 Hedge 仍 no-regret”；
2. “OGD 只要有 gradient 就对 nonconvex neural loss 有同一 regret”；
3. “Perceptron 有限 mistake 证明新样本错误率小”；
4. “AdaBoost training error 下降证明对标签噪声稳健”；
5. “任意最后 iterate 都继承 average regret”；
6. “IPS 无偏就意味可以把探索概率压到零”；
7. “contextual bandit regret 可直接当作 RL return guarantee”。

### 第 13 题：Nonce Blind 跨轨复现（10 分）

在未读详解和 canonical stdout 时：

1. 写下指定 blind 参数对每个主要量的方向预测；
2. 手算 scorer nonce 指定的主轨；
3. 运行[[online_boosting_cumulative_gate.py]]产生新 stdout/SVG/hash；
4. 对照预测解释差异，不得只粘贴输出；
5. 主动提交一个非法合同，并解释脚本为何必须拒绝。

### 第 14 题：陌生 AI 交互系统迁移（10 分）

选一个未在正文中完整出现的场景，如实时模型路由、广告/推荐、人类反馈数据收集、在线安全过滤或 tool-using agent。交付：

1. 一份可执行 protocol 时序图；
2. 至少两个 comparator 候选及选择理由；
3. full-information/bandit/RL 的 feedback 定位；
4. 一个 regret/mistake/risk/value 主指标与一个 safety/coverage 副指标；
5. overlap、delayed feedback、drift 和 current-action response 中至少两项的失效检查；
6. 一个可证伪的上线/回滚规则；
7. 明确列出“即使 online metric 改善也不能推出”的三件事。

## 四、评分与通过标准

| 部分 | 题号 | 分值 |
|---|---|---:|
| 对象、证明与信息合同 | 1—4 | 20 |
| full-information / margin-boosting 计算 | 5—8 | 30 |
| conversion / bandit 计算 | 9—10 | 16 |
| 比较、反例与边界 | 11—12 | 14 |
| blind 复现与 AI 迁移 | 13—14 | 20 |
| **合计** |  | **100** |

诊断性达标需同时满足：

- 口试通过，闭卷至少 85/100；
- 第 3、4、7、8、9、10 题不得用只写结论的方式得分；
- 第 13 题 blind 轨和第 14 题迁移轨各至少 7/10；
- 任一处把 regret、population risk、training exponential loss 或 RL return 无条件等同，总分上限 84；
- 所有材料通过只表示 `regression-passed material`，在前置、原稿、blind、48 小时和 14 天证据完整前，个人状态始终是 `not-attempted`。

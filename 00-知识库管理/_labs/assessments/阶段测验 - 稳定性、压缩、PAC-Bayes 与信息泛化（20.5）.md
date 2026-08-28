---
type: assessment
status: draft
material_status: regression-passed
learning_status: not-attempted
area: [learning-theory/stability, learning-theory/compression, learning-theory/pac-bayes, learning-theory/information]
assessment_id: ALG-CUM-01
scope: [LT-33, LT-34, LT-35, LT-36, LT-37, LT-38, LT-39, LT-40]
time_limit_minutes: 210
oral_limit_minutes: 20
points: 100
solution: "[[阶段测验解答 - 稳定性、压缩、PAC-Bayes 与信息泛化（20.5）]]"
experiment: "[[实验 - 稳定性、压缩、PAC-Bayes 与信息泛化累计复现门]]"
related: ["[[稳定性、压缩、PAC-Bayes 与信息泛化 MOC]]", "[[学习理论完整课程地图与掌握标准]]", "[[练习与测验 MOC]]"]
created: 2026-08-28
updated: 2026-08-28
---

# 阶段测验 - 稳定性、压缩、PAC-Bayes 与信息泛化（20.5）

> [!abstract] 这卷真正考什么
> 不是背四个 bound，而是会把一个泛化声明拆成：**预测者—损失—样本—算法随机性—复杂度对象—概率事件—结论类型—不能推出**。你必须能从 replace-one、压缩描述、后验与先验的 KL、学习通道的互信息四个角度重建证明，并知道它们为什么不能事后随意取最小。

## 一、答案与输出隔离协议

1. 生成唯一 **attempt_id**，写下开始时间、结束时间和完整原稿 SHA-256。
2. 先完成 **20 分钟卷级口试**，再完成 **210 分钟闭卷**。两者不得查看详解、canonical SVG 或脚本 stdout。
3. 闭卷后先提交第 5—8 题的数值预测，以及对盲参干预的单调性预测。
4. 评分者再公布 **scorer nonce**；它决定主轨、跨轨参数和一条必须拒绝的非法合同。
5. 用新 **--output** 执行非 canonical 盲参，保存 command、stdout、SVG、hash、运行前预测和差异解释。
6. 所有原稿封存后，才可打开[[阶段测验解答 - 稳定性、压缩、PAC-Bayes 与信息泛化（20.5）]]和 canonical 输出。
7. 48 小时做换机制复测，14 天后把八层账本迁移到一个陌生 AI 训练/评估问题。

> [!warning] 状态边界
> 题卷、详解、脚本和图通过回归，只能记为 **material_status: regression-passed**。没有独立原稿、盲参和延迟迁移证据时，**learning_status** 必须保持 **not-attempted**。

## 二、20 分钟卷级口试

不看笔记，每题 4 分钟：

1. 用一句话分别说明 uniform stability、sample compression、PAC-Bayes 和 mutual-information bound 的“复杂度对象”。
2. 口头重建 ghost replacement identity，解释为什么一个期望泛化隙可以变成相邻样本的损失差。
3. 从 strong convexity 的两个不等式推到 $\|w_S-w_{S'}\|\le 2L/(\lambda m)$，并说出 smoothness 在这条证明中是否需要。
4. 说出 PAC-Bayes-kl 中 $P,Q,\widehat R_S(Q),R(Q)$ 的时间线，并区分 Gibbs predictor、posterior mean、MAP 和 majority vote。
5. 面对“五个界都算了，报最小的那个”，给出一个一分钟合法性审计。

口试通过要求：至少 4/5 题能同时说对对象、量词/概率和不能推出；仅会报公式不通过。

## 三、210 分钟闭卷（100 分）

### A 部分：对象、量词与界的类型（20 分）

### 第 1 题：八层算法依赖泛化证明账本（5 分）

对下列四条声明逐条补全：随机对象、固定对象、复杂度对象、概率取在哪里、结论是期望还是高概率、控制哪个 predictor/loss、使用了哪条 change-of-measure/组合计数/耦合工具、不能推出什么：

1. replace-one uniform stability；
2. exact size-$k$ compression；
3. PAC-Bayes-kl；
4. mutual-information expected generalization。

### 第 2 题：replace-one 定义与 ghost replacement（5 分）

设 $S=(Z_1,\ldots,Z_m)$，$Z_i'$ 是独立同分布副本，$S^{(i)}$ 用 $Z_i'$ 替换 $Z_i$。

1. 写出 direct replace-one uniform stability 的完整 supremum 定义；
2. 写出 $\mathbb E[R(A(S))-\widehat R_S(A(S))]$ 的 ghost replacement identity；
3. 说明算法内部有随机性时，shared-randomness coupling 解决的是哪个量词问题。

### 第 3 题：五条证书的接口表（5 分）

为 capacity/uniform-convergence、stability、compression、PAC-Bayes、information 五条路线各写一行：

- 输入对象；
- 主要 complexity term；
- 典型结论类型；
- 对训练后数据依赖的允许范围；
- 最容易作弊的环节。

### 第 4 题：PAC-Bayes 时间线与 predictor 身份（5 分）

审计以下方案：用全部数据训练得到 $Q_S$，然后令 $P_S=Q_S$，以 $\mathrm{KL}(Q_S\|P_S)=0$ 声称得到最佳证书。

1. 指出它违反标准 PAC-Bayes 定理的哪个量词；
2. 给出 independent pretraining prior、sample split prior、weighted prior family 三种合法修复；
3. 说明 PAC-Bayes-kl 直接控制的为什么是 Gibbs risk，不是 MAP 网络风险。

### B 部分：精确计算与证书分账（28 分）

### 第 5 题：Bernoulli 均值学习器的精确定标（7 分）

设 $Z_i\sim\mathrm{Bernoulli}(p)$，$A(S)=\bar Z$，$\ell(w,z)=(w-z)^2$。取 $m=20,p=1/2$。

1. 把样本压缩为成功数 $K$，穷举所有相邻 $K,K+1$ 与 $z\in\{0,1\}$，求 direct replace-one 的精确 $\beta_m$；
2. 直接对 $K\sim\mathrm{Binomial}(m,p)$ 求和，计算 $\mathbb E[R(\bar Z)-\widehat R_S(\bar Z)]$；
3. 解释为什么两个数不应相等。

### 第 6 题：RERM 与 SGD 证书（7 分）

设单样本损失对 $w$ 凸且 $L$-Lipschitz，

$$
F_S(w)=\frac1m\sum_{j=1}^m\ell(w,Z_j)+\frac\lambda2\|w\|^2.
$$

取 $m=20,L=1,\lambda=2$；SGD 的预注册步长是 $(0.2,0.15,0.1,0.05)$。

1. 计算 exact RERM 的标准 uniform-stability certificate；
2. 计算凸光滑 SGD synchronous-coupling certificate；
3. 指出延长训练、增大 $\lambda$、非凸 expansion factor 分别怎样改变账本；
4. 说明 optimization error 为什么不能被 stability 一项代替。

### 第 7 题：样本压缩的组合账本（7 分）

一个预先固定的 exact compression scheme 使用 $k=5$ 个样本和 $b=3$ 个 side-message bits，并与完整的 $m=200$ 可实现样本一致。取 $\delta=0.05$。

1. 从 $\binom mk2^b(1-\varepsilon)^{m-k}$ 写出高概率 risk certificate；
2. 给出数值结果到小数点后 6 位；
3. 解释 adaptive subset selection 为什么已被 $\binom mk$ 支付，但训练后现发明的 decoder/message alphabet 为什么没有被支付。

### 第 8 题：PAC-Bayes-kl 与信息通道（7 分）

在两个 hypothesis 上取

$$
P=(0.7,0.3),\qquad Q=(0.9,0.1),\qquad
(\widehat R_1,\widehat R_2)=(0.02,0.25),
$$

取 $m=200,\delta=0.05$。另设 $X\sim\mathrm{Bernoulli}(1/2)$，对称通道以 $q=0.8$ 概率输出 $W=X$。

1. 计算 $\widehat R(Q),\mathrm{KL}(Q\|P)$ 和 PAC-Bayes-kl budget；
2. 用二分求根给出 inverse-kl upper endpoint，并与 Pinsker corollary 比较；
3. 计算 $I(X;W)=\log2-H_b(q)$ 以及 $m=200$ 时 $\sqrt{I/(2m)}$；
4. 解释这两个数为什么不是对同一个结论的竞争上界。

### C 部分：定理主链重建（32 分）

### 第 9 题：稳定性到期望泛化（8 分）

在 i.i.d. 样本下，从 population/empirical risk 定义出发，使用 $Z_i'$ 和 $S^{(i)}$ 证明

$$
\left|\mathbb E\big[R(A(S))-\widehat R_S(A(S))\big]\right|\le\beta_m.
$$

不得把独立性一句带过；必须写出换元前后的联合分布相同性，并指出最后使用 stability 的那一对相邻样本。

### 第 10 题：strong convexity 到 RERM 稳定性（8 分）

设 $S,S'$ 只在一个样本上不同，$w_S,w_{S'}$ 是对应 regularized objectives 的 exact minimizers。

1. 把两个 strong-convexity lower bounds 相加；
2. 显式消掉 $m-1$ 个共同损失项；
3. 用 Lipschitz 性质控制剩下两项；
4. 推出 displacement 与 $\beta_m\le2L^2/(\lambda m)$；
5. 标明 exact minimization、convex loss、strong convexity 分别在哪一步使用。

### 第 11 题：压缩界的留出样本证明（8 分）

对 fixed exact size-$k$ compression scheme，重建

$$
\Pr\!\left(\exists\text{ consistent reconstruction }h:R(h)>\varepsilon\right)
\le |\mathcal Q|\binom mk(1-\varepsilon)^{m-k}.
$$

必须说明：先固定 subset/message 后，哪 $m-k$ 个样本与 reconstructed $h$ 之间保持可用的独立性；为什么 consistency 会迫使它们全部落在 zero-error region；最后 union 的索引数是什么。

### 第 12 题：PAC-Bayes-kl 的测度变换主链（8 分）

在 0—1 loss 下，从以下 change-of-measure lemma 出发：

$$
\mathbb E_{h\sim Q}f(h)
\le \mathrm{KL}(Q\|P)+\log\mathbb E_{h\sim P}e^{f(h)}.
$$

使用 fixed-$h$ 的 binomial exponential moment，重建以下 simultaneous statement：

$$
\operatorname{kl}(\widehat R_S(Q)\|R(Q))
\le\frac{\mathrm{KL}(Q\|P)+\log((m+1)/\delta)}m.
$$

必须解释：为什么事件可以对所有 data-dependent $Q$ 同时成立；$Q\not\ll P$ 时哪一步失效；为什么 inverse-kl 通常比先用 Pinsker 更保留信息。

### D 部分：边界、反例与声明审计（10 分）

### 第 13 题：五条声明审计（10 分）

对每条声明给出“正确/错误/条件不足”，修复它，并给最小理由或反例：

1. “高概率 stability bound 只要有 $\beta_m=O(1/m)$ 就一定收敛。”
2. “压缩 subset 是看到数据后选的，所以压缩界必然无效。”
3. “用一份数据学 prior，再用同一份数据的标准 PAC-Bayes 定理，反正 posterior 可以依赖数据。”
4. “一个 deterministic 连续参数网络只含有限个浮点数，所以 $I(S;W)$ 必然有限且小。”
5. “同一模型的 capacity、stability、compression、PAC-Bayes 和 information 界可以事后直接取 minimum。”

### E 部分：AI 迁移（10 分）

### 第 14 题：为微调大模型建立多路线泛化合同（10 分）

情境：你有一个公开预训练模型，在 $m$ 个私有指令样本上用随机梯度法微调 LoRA，并在同一份数据上搜索 rank、checkpoint、步长与 posterior temperature。你希望报告 stability、PAC-Bayes 和 information 三条证书，并将 compression 作为可选解释。

写出一页 protocol，至少包含：

1. 数据生成/切分、loss 有界或 sub-Gaussian 假设、algorithm randomness 和最终 predictor 的完整定义；
2. SGD stability 路线需要哪些凸性/光滑性/步长条件，真实深网违反后如何降级声明；
3. 如何用公开预训练权重定义合法 prior，并为 hyperparameter/posterior 搜索支付预注册或共同事件成本；
4. 学习通道 $P_{W\mid S}$、有限 bit 记录/噪声注入与互信息的关系，以及 expected signed gap 与 high-probability tail 的语义分账；
5. 如果要声称 compression，明确 encoder/message/decoder 和 reconstruction consistency；
6. 如何区分“合法”“非空洞”“数值紧”和“机制有解释力”四个层次。

## 四、三轨参数化模型族

| 轨道 | canonical 对象 | 允许盲参 | 必须先写的预测 |
|---|---|---|---|
| A stability | Bernoulli mean + RERM/SGD certificates | $m,p,L,\lambda,(\eta_t)$ | exact $\beta$、$\mathbb E\mathrm{gen}$、正则/步长单调性 |
| B description | compression + finite PAC-Bayes-kl | $m,k,b,\delta,P,Q,\widehat R_j$ | compression 计数、support、KL、inverse-kl 区间 |
| C information | symmetric binary channel | $m,q$, route count | $I$、bit ceiling、expected radius、共同 $\delta$ 预算 |

**scorer nonce** 的 SHA-256 首字节模 3 指定 A/B/C 主轨；第二字节模 5 指定 sample / regularization / description / prior / information 干预；第三字节指定一条应被脚本拒绝的非法参数。评分者必须在学习者封存预测后才公布 nonce。

## 五、评分门槛

| 层级 | 要求 |
|---|---|
| 对象门 | 第 1—4 题至少 14/20；Gibbs/MAP、expected/tail 不得混淆 |
| 计算门 | 第 5—8 题至少 20/28；关键 normalization、nats/bits 不得错 |
| 证明门 | 第 9—12 题至少 23/32；不得只写定理名 |
| 边界门 | 第 13 题至少 7/10；必须修复量词 |
| 迁移门 | 第 14 题至少 7/10；必须给可执行 protocol |
| 总分门 | 至少 75/100，且上述五门全过 |
| 证据门 | nonce 盲参、非法合同拒绝、48 小时和 14 天迁移都完成 |

## 六、48 小时与 14 天复测

### 48 小时：换机制

从下列三项由评分者抽一项：

1. 把 sample mean 换成带 Gaussian output noise 的学习器，分开稳定性耦合与信息通道账本；
2. 把 finite posterior 换成 isotropic Gaussian $Q=\mathcal N(\mu_Q,\sigma_Q^2I)$，手算 KL 并审计 point-mass posterior；
3. 把 exact compression 换成带 side-message family 的压缩，解释哪些 index 已经支付。

### 14 天：陌生问题迁移

为一个从未在本卷出现的问题（如 DP-SGD、检索模型的记忆泄漏、ensemble posterior、通信受限的分布式训练）写一份“八层算法依赖泛化证明账本”。不追求必然有非空洞数值，但必须诚实标出无法验证的假设。

## 七、提交证据清单

- [ ] attempt_id、口试录音/笔录、闭卷原稿、时间戳、SHA-256；
- [ ] 第 5—8 题计算纸与 inverse-kl 求根区间；
- [ ] 八层算法依赖泛化证明账本；
- [ ] scorer nonce、盲参 command/stdout/SVG/hash、运行前预测；
- [ ] 一条非法参数被拒绝的 stderr 证据；
- [ ] 48 小时换机制复测；
- [ ] 14 天陌生 AI 问题迁移；
- [ ] 错题回链 LT-33—40 的具体小节，不只写“粗心”。

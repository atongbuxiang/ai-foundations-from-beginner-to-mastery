---
type: solution
status: verified
area: [language-models, safety, abstention, refusal]
topic: "[[Abstention、Refusal、Over-refusal 与风险覆盖]]"
exercise: "[[习题 - Abstention、Refusal、Over-refusal 与风险覆盖]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Abstention、Refusal、Over-refusal 与风险覆盖

## A. 识别与复述

### LM69-A01
Abstain 因知识、证据或置信不足退出；refuse 因政策、权限或伤害风险不提供目标能力；safe-complete 拒绝危险部分但提供安全替代/澄清；escalate 把决定交给人工、认证流程或高可信工具。它们的理由、后续动作和评估分母不同。

### LM69-A02
选择函数 $g_i\in\{0,1\}$ 时
$$
\mathrm{coverage}=\frac{\sum_i g_i}{n},\qquad
\mathrm{risk}=\frac{\sum_i\ell_i g_i}{\sum_i g_i}.
$$
Risk 只在作答子集定义，必须与 coverage 一起报告。

### LM69-A03
Correctness confidence 估计“回答是否正确/有证据”，safety risk 估计“直接完成是否被允许或有害”。系统可能知道答案但不得提供，也可能不知道无害事实。混成一个 score 会让阈值理由不透明且难校准。

## B. 手算与构造

### LM69-B01
Coverage $.25$ 保留前 2 个，risk $=1/2=.5$；coverage $.5$ 保留前 4 个，risk $=1/4=.25$；coverage $1$ 保留全部，risk $=4/8=.5$。这个序列并非随 coverage 单调，因为有限样本中的错误排序有波动。

### LM69-B02
Unsafe answer rate $=12/100=.12$；harmful recall $=88/100=.88$。Over-refusal $=18/100=.18$；benign utility $=82/100=.82$。

### LM69-B03
组 A coverage $=.8$、risk $=4/80=.05$；组 B coverage $=.2$、risk $=2/20=.10$。总体作答风险 $=6/100=.06$，但它隐藏 B 组大量被拒且估计样本少；公平不能只比较已回答风险。

## C. 推导与证明

### LM69-C01
若 $f$ 严格单调递增，则 $s_i>s_j\Leftrightarrow f(s_i)>f(s_j)$，任一 coverage 保留的 top 样本集合相同，所以 risk–coverage 曲线不变。但 $f(s)$ 数值通常不再满足 $P(Y=1\mid f(S)=q)=q$，故校准改变。

### LM69-C02
给动作 $a$ 和状态 $y$ 的代价 $C(a,y)$：
$$
a^\star(x)=\arg\min_a\sum_y C(a,y)P(y\mid x).
$$
不同领域的误答、漏放、误拒、延迟和人工成本不同，概率也随总体变；所以最优阈值依应用、容量与风险容忍，没有通用常数。

### LM69-C03
多个阈值在同一 validation 上的 empirical risk 含抽样噪声；选择最小者等于取多个噪声估计的极值，期望向下偏。应在 validation 选阈值并用独立 test 估计，或用同时有效界/序贯校正。

## D. 边界、反例与纠错

### LM69-D01
若只回答 1% 最简单样本，accuracy 可 99%，但 coverage 极低，绝大多数用户无服务；被拒样本还可能集中某群体。还需 coverage、选择机制、拒答理由、群体切片和升级成本。

### LM69-D02
高事实置信但拒答：模型确切知道一个受权限保护的个人记录，仍不得披露。低事实置信但不应用安全理由拒答：无害历史日期不确定，应诚实 abstain/查证，而非声称内容危险。

### LM69-D03
5% coverage 下仅留下极少最容易样本，低 risk 可能由排除 95% 获得，且区间很宽。公平评估要同时约束 coverage、风险、误拒、群体代价和升级可达性。

## E. AI 迁移

### LM69-E01
状态含 correct/incorrect、safe/unsafe、evidence sufficient/insufficient。危险内容直接 answer 代价最高；无害正确 answer 代价最低；不确定时 abstain 有中等服务损失；政策风险时 safe-complete 优于裸答；高严重度或身份不明时 escalate。表还计人工延迟、隐私暴露和不可逆工具动作。

### LM69-E02
在训练外 validation 校准 correctness/safety 两分数；预注册 risk 上界、最小 coverage 和群体约束；扫阈值时用同时/选择有效上界，冻结后独立 test 一次；上线按版本、语言、领域监控 risk proxy/抽样真值和 coverage；分布、policy、模型、template 或工具权限改变即失效并回到 validation。

### LM69-E03
对每类真实 harmful 请求制作语义近邻 benign pair：词面相似但合法、安全或教育性用途；再加入普通无敏感词 benign baseline。按语言、身份词、领域和长短分层，盲人评 answer/refuse/safe-complete，报告 over-refusal、benign utility、帮助质量、组别 coverage 和 cluster CI。

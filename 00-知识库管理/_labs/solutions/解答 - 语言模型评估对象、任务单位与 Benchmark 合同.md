---
type: solution
status: verified
area: [language-models, evaluation]
topic: "[[语言模型评估对象、任务单位与 Benchmark 合同]]"
exercise: "[[习题 - 语言模型评估对象、任务单位与 Benchmark 合同]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - 语言模型评估对象、任务单位与 Benchmark 合同

## A. 识别与复述

### LM57-A01
可写成
$$
\theta(c)=\mathbb E_{U\sim P^\star}\mathbb E_{Y\sim q_c(\cdot\mid U)}[m(U,Y)].
$$
$P^\star$ 是要外推的目标总体，$U$ 是预先定义的任务/用户等单位，$c$ 固定 checkpoint、prompt、decoder、tools 与服务版本，$q_c$ 描述生成随机性，$m$ 是正确性、风险、成本或效用。少任何一项，“分数”都没有唯一解释。

### LM57-A02
条件模型只问固定 history 下的概率或表示；解码行为还包括 prompt、processor、sampler 和 seed；工具系统进一步包括 retriever、tool、parser 与外部状态；在线产品还受用户、流量、策略、版本和反馈回路影响。后一层变化不必来自 checkpoint 变化，不能统称为“模型能力变化”。

### LM57-A03
一行日志可能是 observation，一次请求可能是评分单位，而独立单位可能是 user 或 conversation。同一 user 的请求共享偏好、难度和历史，不能当 iid。估计量的分母由 sampling unit 决定，标准误和 bootstrap 则要在近似独立的 cluster 层进行。

## B. 手算与构造

### LM57-B01
任务准确率分别为 $.8$ 和 $.2$，故
$$
\mathrm{macro}=(.8+.2)/2=.5.
$$
Micro 合并事件：
$$
\mathrm{micro}=(20+3)/(25+15)=23/40=.575.
$$
差异来自任务 A 的样本更多，micro 给它更大权重。

### LM57-B02
Request-average 为 $3/5=.6$。用户甲均值 $3/4=.75$，用户乙均值 $0$，故 user-average 为 $(.75+0)/2=.375$。前者回答随机请求，后者回答随机用户。

### LM57-B03
删除 10 个失败后得到 $72/90=.8$，它只描述成功产生可评分输出的条件子集。若失败按端到端不成功记零，则为 $72/100=.72$。还应单报 timeout $6\%$ 与 parser failure $4\%$。

## C. 推导与证明

### LM57-C01
令用户 $g$ 有 $n_g$ 个请求、均值 $\bar m_g$。Request-average 与 user-average 分别为
$$
\frac{\sum_g n_g\bar m_g}{\sum_gn_g},\qquad \frac1G\sum_g\bar m_g.
$$
前者是以 $n_g$ 加权的均值。两者在所有 $n_g$ 相等时必相等；更一般地，当 $n_g$ 与 $\bar m_g$ 的样本协方差为零时相等。否则活跃用户同时更易或更难就会改变 request estimand。

### LM57-C02
对 $n$ 题、每题 $R$ 次生成，
$$
\hat\theta=\frac1n\sum_{i=1}^n\frac1R\sum_{r=1}^R m(U_i,Y_{ir}).
$$
外层有限 $U_i$ 带来题目抽样误差，内层 $Y_{ir}$ 带来 sampler/运行误差。增加 $R$ 只能降低同一批题的生成 Monte Carlo 误差，不能补足题目覆盖；区间应保留按 item cluster 的结构。

### LM57-C03
令 $S=1$ 表示运行成功。删除失败后的样本均值收敛到 $\mathbb E[m\mid S=1]$；所有请求目标为
$$
\mathbb E[m]=P(S=1)\mathbb E[m\mid S=1]+P(S=0)\mathbb E[m\mid S=0].
$$
除非 $P(S=0)=0$ 或两条件期望相同，否则二者不同。失败若与长度/难度相关，删除还会系统性偏向简单题。

## D. 边界、反例与纠错

### LM57-D01
固定 checkpoint，改 chat template 可改变输入 token；改 temperature 改 rollout 分布；检索库更新改变证据；parser 版本改变可评分率；负载改变 timeout。故分数属于完整运行配置和目标总体，而非 checkpoint 的固有常数。

### LM57-D02
设任务 1 有 100 题、任务 2 有 10 题。A 的准确率为 $(.9,0)$，B 为 $(.8,.4)$。Micro：A $90/110=.818$，B $84/110=.764$，A 胜；macro：A $.45$，B $.60$，B 胜。两者都算对，只是任务权重不同。

### LM57-D03
若查看 validation 结果后从许多 prompt 中挑最佳，所选分数包含适配该 split 噪声的选择增益。再在同一 split 报告就是训练/选择后的条件结果，不是独立泛化估计。应把选择过程限制在 validation，并用未触碰 test 一次确认。

## E. AI 迁移

### LM57-E01
最小 manifest 包含 dataset/version/hash/split/time cutoff；example IDs 与 license；instruction、few-shot 内容/顺序、chat template；checkpoint/API date、tokenizer、decoder/seed；retriever corpus/index、tool 与 parser；normalization/reference/metric/judge；failure rule、sampling unit、重复次数、预算、CI 与预注册 slices。

### LM57-E02
先从目标用户总体分层抽 user，再在每 user 内取会话/请求；保存所有到达与失败，不让高活跃 user 自动支配。主 estimand 用每 user 均值的等权平均，区间对 user 做 cluster bootstrap；若还关心随机请求，作为另一个显式 estimand 报告。

### LM57-E03
可改为：“在数据版本 $D$ 的预注册 test split、固定配置 $c_A,c_B$、失败记零且以 question 为配对单位时，A 相对 B 的 example-micro accuracy 差为 $+2.1$ 个百分点，cluster/paired 95% CI 为 $[+.6,+3.5]$；该结论只覆盖所测语言、prompt、decoder 和预算，不代表所有用户或系统层效用。”

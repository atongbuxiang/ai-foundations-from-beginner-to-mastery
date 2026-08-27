---
type: solution
status: verified
area: [language-models, decoding]
topic: "[[Top-k、Top-p、Typical 与 Min-p 截断采样]]"
exercise: "[[习题 - Top-k、Top-p、Typical 与 Min-p 截断采样]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Top-k、Top-p、Typical 与 Min-p 截断采样

## A. 识别与复述

### LM51-A01
各方法先由 $p$ 和参数 $lambda$ 产生 support $S(p;\lambda)$，再用 $q(v)=p(v)\mathbf1[v\in S]/\sum_{u\in S}p(u)$。top-$k$ 取概率排名前 $k$；top-$p$ 取累计质量至少阈值的最短降序前缀；typical 按 surprisal 离熵的距离选集；min-$p$ 取 $p(v)\ge\alpha\max_up(u)$。

### LM51-A02
Top-$k$ 固定候选个数，保留质量随分布变；top-$p$ 固定最低累计质量，候选个数随分布变。前者在尖锐和平坦位置都保留 $k$ 项，后者通常在平坦位置保留更多项。

### LM51-A03
Typical 令信息量 $I(v)=-\log p(v)$，按 $|I(v)-H(p)|$ 衡量 token 是否接近当前分布的典型信息量；它未必保留最大概率前缀。Min-$p$ 用相对最大概率的阈值 $alpha p_{\max}$，故随分布峰值自适应。

## B. 手算与构造

### LM51-B01
Top-3 support 为前 3 项，保留质量 $.73$，新概率约 $(.4658,.3151,.2192)$。Top-$p=.75$：前三项只有 $.73$，需加入第四项得到 $.84$；新概率约 $(.4048,.2738,.1905,.1310)$。

### LM51-B02
阈值为 $.2\times.34=.068$，故保留前五项（第五项 $.07$），质量 $.91$。重归一化约为 $(.3736,.2527,.1758,.1209,.0769)$；$.04,.03,.02$ 删除。

### LM51-B03
$H=-[.5\log.5+.25\log.25+2(.125\log.125)]\approx1.2130$。surprisal 分别为 $.6931,1.3863,2.0794,2.0794$，距离约 $.5199,.1733,.8664,.8664$；typical 顺序为第二、第一、第三/第四并列。

## C. 推导与证明

### LM51-C01
令 $Z_S=\sum_{u\in S}p(u)>0$，则 $sum_vq(v)=Z_S/Z_S=1$。删除质量为 $1-Z_S$。若 $S$ 为空则算子未定义，工程实现必须设至少保留一项或报错。

### LM51-C02
取 logits 对应原概率 $(.6,.25,.15)$ 与 top-$p=.7$：原分布需前两项。令温度趋大，概率趋近 $(1/3,1/3,1/3)$，达到 $.7$ 需三项。故先变温再 top-$p$ 与先截断后变温具有不同 support。

### LM51-C03
例证：尖锐分布 $(.9,.05,.05)$ 在 $p=.8$ 时 support 大小 1；平坦分布 $(.34,.33,.33)$ 时大小 3。一般“平坦化”需定义偏序；局部概率重新排列或阈值边界可使大小跳变，所以不应无条件声称对任意温度/任意 logits 严格单调。

## D. 边界、反例与纠错

### LM51-D01
一个尖锐位置前 50 项可能含 $.999$ 质量，一个平坦大词表位置可能只含很小质量。$k$ 固定的是 cardinality，不是 probability mass；报告应同时给 support size 与 retained mass 分布。

### LM51-D02
方法论文能定义算法与给出特定实验，普遍优越性还需要可靠基线、相同调参预算、多任务/模型、足够样本、预注册统计和可复现数据。已存在对原始 min-$p$ 人评、统计和超参公平性的批评，因此本库保留方法定义，不把争议结果升级为定论。

### LM51-D03
多个截断算子通常不交换，最终 support 取决于处理顺序和是否每步重归一化。报告无法重建 rollout kernel，结果既不可复现也无法解释。应保存 ordered processor list、每步 support/removed mass 和空集策略。

## E. AI 迁移

### LM51-E01
为固定分布验证：参数边界、并列概率 tie-break、累计值恰等阈值、空集保护、至少一项、重归一和为 1、temperature 前后 support、NaN/inf。把预期 token IDs 与概率写死为 oracle。

### LM51-E02
固定 checkpoint、prompt、长度/stop 与总调参预算；每方法在 validation 选参数，test 冻结。跨开放生成、事实问答、代码等任务，多 seed 报质量、多样性、退化、安全、support/removed mass、延迟和 CI；不得给某方法额外搜索预算。

### LM51-E03
逐请求/位置采样记录 support size、retained mass、最大概率和 entropy 的摘要；当 support=1 比例、removed mass 或连续低熵步超过基线阈值时告警。告警需按任务和 processor 版本分层，避免把本来要求确定格式的输出误报。

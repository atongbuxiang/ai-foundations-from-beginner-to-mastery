---
type: solution
status: verified
area: [language-models, reasoning, search, test-time-compute]
topic: "[[Test-time Compute、Search、Verifier 与预算]]"
exercise: "[[习题 - Test-time Compute、Search、Verifier 与预算]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Test-time Compute、Search、Verifier 与预算

## A. 识别与复述

### LM39-A01
七元合同为 state、proposal、transition/parser、value/verifier、queue rule、pruning 和 stopping/terminal。另需 policy/model、预算和随机性，才能复现具体算法。

### LM39-A02
Outcome verifier 对完整解最终正确性打分；process verifier 对中间步骤/前缀有效性打分，可早剪枝。后者需要步骤标签与聚合规则，局部高分不保证最终正确。

### LM39-A03
Token 是序列长度，FLOPs 依模型/操作，调用数影响服务开销，延迟取决于串并行/硬件，显存受 KV/批处理影响。两个方法可在任一坐标相同而其他坐标不同，所以需成本向量。

## B. 手算与构造

### LM39-B01
$1+2+4+8=15$，也由 $(2^{4}-1)/(2-1)=15$。

### LM39-B02
$V_{min}=0.4$；$V_{prod}=0.9\cdot0.8\cdot0.4=0.288$；log-sum 为 $\log0.9+\log0.8+\log0.4=\log0.288\approx-1.245$。Product 与 log-sum 排序等价，min 只看最弱步骤。

### LM39-B03
方案 A 串行生成一条 1000-token 链；方案 B 并行生成十条各 100 token 后投票。总输出 token 都 1000，但 A 有更长依赖深度，B 可并行且有候选多样性，KV/latency 不同。

## C. 推导与证明

### LM39-C01
第 $l$ 层有 $b^l$ 个节点，总数是等比和 $\sum_{l=0}^db^l=(b^{d+1}-1)/(b-1)$；$b=1$ 时退化为 $d+1$。

### LM39-C02
从 $s_0$ 出发，$a\sim\pi(\cdot\mid s)$，$s'=T(s,a)$，计算 $V(s')$；queue 按规则加入/弹出，pruning 删除低分/重复状态；若 terminal 或预算/置信 stop 则输出，否则继续。每一步保存 action、score 与 parent。

### LM39-C03
若用真实答案定义难题，再给难题更多预算，就把测试标签泄漏进调度器，结果是 oracle allocation。可用模型 entropy、早期 verifier margin 或独立难度模型，但这些也要在验证集冻结并报告误差。

## D. 边界、反例与纠错

### LM39-D01
长输出可重复、跑偏或填充；短程序调用 solver 可完成大量外部计算。有效 compute 取决于模型运算、搜索/工具和结构，不由可见 token 长度单调决定。

### LM39-D02
Verifier 在 IID 解答上学到“答案越长越可能正确”，准确率很高；搜索发现不断添加无意义步骤会涨分，于是 top candidate 变成超长错误。需 adaptive candidate 测试、长度匹配和 reward–truth gap。

### LM39-D03
小模型系统含 policy 生成与 verifier/搜索调用，若只计 policy 参数或最终 token，比较不公平。应计两模型 FLOPs、calls、latency、memory、verifier 训练/推理，并在同总预算画 frontier。

## E. AI 迁移

### LM39-E01
固定题集/policy：greedy；matched-token long CoT；$N$ sampling；outcome-verifier Best-of-N；process-verifier search；oracle selector。各自报 coverage/chosen accuracy 与多维成本，oracle 只作上界。

### LM39-E02
用不看真值的预注册难度分数分层；每层报告分配预算、准确率、超时和 calibration。再在固定全局预算下比较 uniform 与 adaptive allocation，并报告调度错误造成的损失。

### LM39-E03
Manifest 含 state schema、thought delimiter、proposal prompt/sampler、branch/depth/beam、transition/parser、value model/prompt、score aggregation、queue/tie、pruning/dedup、stop、tool versions、budget、完整树、失败/超时和最终选择理由。

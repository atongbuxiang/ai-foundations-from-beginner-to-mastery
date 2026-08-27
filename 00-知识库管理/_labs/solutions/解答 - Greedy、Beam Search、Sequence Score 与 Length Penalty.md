---
type: solution
status: verified
area: [language-models, decoding]
topic: "[[Greedy、Beam Search、Sequence Score 与 Length Penalty]]"
exercise: "[[习题 - Greedy、Beam Search、Sequence Score 与 Length Penalty]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Greedy、Beam Search、Sequence Score 与 Length Penalty

## A. 识别与复述

### LM50-A01
Greedy 每步只保留当前 argmax；beam 保留固定数量高累计分前缀，是有限宽启发式；exact sequence argmax 在所有完整序列中最大化预先定义的 sequence score。无限宽、正确停止且有限搜索空间时 beam 才可逼近/达到 exact，通常服务设置不满足。

### LM50-A02
Active beam 尚可扩展；completed hypothesis 已生成 EOS 或满足完成规则。两者可能使用不同队列和比较界。把完成序列继续扩展或让一个低分早 EOS 立即终止全部 active beams，都可能错误。

### LM50-A03
Search error 是 decoder 没找到其评分函数的最优序列；model error 是模型给不理想序列更高概率；task-metric error 是所优化 score 与 BLEU、正确性、人类偏好等目标错位。加宽 beam 只直接作用于第一类。

## B. 手算与构造

### LM50-B01
Greedy 首步取 A，得到最佳 A 路径概率 $.6\times.5=.30$；B 路径为 $.4\times.9=.36$，是全局两步最佳。这个最小例说明局部最大不保证乘积最大。

### LM50-B02
$s_1/3^{.7}\approx-3/2.157=-1.391$；$s_2/8^{.7}\approx-4/4.287=-.933$。若越大越好，归一化后 $s_2$ 胜，尽管 raw log-score $-4<-3$。这不是修复同一目标，而是换了排序目标。

### LM50-B03
第一前缀扩展累计分为 $-.2-.4=-.6$ 与 $-.2-1.0=-1.2$；第二前缀为 $-.5-.1=-.6$ 与 $-.5-.3=-.8$。保留两个 $-.6$，并需固定并列规则；$-.8$、$-1.2$ 剪枝。

## C. 推导与证明

### LM50-C01
beam width 1 每轮只保留一个最高累计分前缀；同一前缀的扩展共享已有累计常数，因此选择下一 token 的最大条件 log-prob，正是 greedy。B01 已给序列 MAP 反例，所以前半等价不推出后半等价。

### LM50-C02
对正概率，$log$ 严格单调：
$$\arg\max_y\prod_tp(y_t\mid y_{<t},x)=\arg\max_y\sum_t\log p(y_t\mid y_{<t},x).$$
log 空间还把很小概率的连乘转为数值稳定的加法。

### LM50-C03
取 $y_1$ 的 raw log-score $-3$、长度 3，$y_2$ 为 $-4$、长度 8。raw 目标选 $y_1$，而 B02 的 length-normalized 目标选 $y_2$。任何非共同常数的长度函数都可能改变 argmax。

## D. 边界、反例与纠错

### LM50-D01
宽 beam 降低 search error，但可能更充分找到模型偏爱的短、常见、重复或任务指标较差的序列；length rule 也可能失配。必须分别报告 model score、任务质量、长度/退化和成本随 beam 的曲线。

### LM50-D02
首个 EOS 只产生一个 completed hypothesis。除非能证明所有 active prefix 的最佳可达终分都不超过当前完成最优，否则立即停止不安全。实现应保存完成队列，采用明确上界/启发式及 tie-break，并记录 finish reason。

### LM50-D03
Exposure bias 指训练时条件多来自真历史、推理时来自模型历史的分布差；greedy、sampling 与 beam 都处于模型历史。Beam search 可能改变错误传播方式，却不是训练—推理历史错位本身。

## E. AI 迁移

### LM50-E01
每步保存 active prefix token IDs、父指针、新增 token log-prob、累计 raw score、长度归一分、EOS/constraint 状态、扩展候选、剪枝原因、completed queue、停止判断与 tie-break。再保存模型/processor/beam 参数和最终回溯路径。

### LM50-E02
固定模型与预算，在 translation 上测 BLEU/COMET、长度、model score；在 story 上测人工连贯/多样性、重复和安全。比较 greedy、多个 beam width 与 sampling，多输入 bootstrap CI。预期排名可随任务变，不能以一个域宣布全局最优。

### LM50-E03
先设 p95 latency、显存与吞吐 SLO，再在满足 SLO 的 beam 配置中找任务质量 Pareto 点；若 beam 增量的 CI 跨零或 tail latency 超线，选更小宽度。报告 batch/concurrency，因为 beam 会放大活跃序列与 KV。

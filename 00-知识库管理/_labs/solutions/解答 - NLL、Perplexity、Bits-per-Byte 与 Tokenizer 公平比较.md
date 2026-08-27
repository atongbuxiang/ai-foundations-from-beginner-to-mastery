---
type: solution
status: verified
area: [language-models, evaluation, perplexity]
topic: "[[NLL、Perplexity、Bits-per-Byte 与 Tokenizer 公平比较]]"
exercise: "[[习题 - NLL、Perplexity、Bits-per-Byte 与 Tokenizer 公平比较]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - NLL、Perplexity、Bits-per-Byte 与 Tokenizer 公平比较

## A. 识别与复述

### LM15-A01
$N=-\sum_i\ln p_i$ nats；token mean $N/D_{tok}$ nats/token；$PPL=\exp(N/D_{tok})$。$BPB=N/(D_{byte}\ln2)$ bits/byte。若直接用 $-\log_2p$，PPL 为 $2^{N_{bits}/D_{tok}}$，BPB 为 $N_{bits}/D_{byte}$。

### LM15-A02
PPL 是几何平均目标概率的倒数。只有每个 context 的预测近似在 $K$ 个候选上均匀时，倒数概率才可解释为 $K$ 个等可能分支；一般分布不均匀、context 也不同。

### LM15-A03
锁定相同 raw strings/encoding/normalization、字符串概率怎样由 token 路径得到、tokenizer 是否确定/可逆、BOS/EOS/边界、context/window、scored events、log base。跨 token 分母不可直接比较，需共同 raw-byte denominator。

## B. 手算与构造

### LM15-B01
概率乘积 $0.5\times0.25\times0.125=2^{-6}$，total NLL 为 6 bits，mean 为 2 bits/token，$PPL=2^2=4$。

### LM15-B02
$BPB=(50\ln2)/(100\ln2)=0.5$ bits/byte。

### LM15-B03
A：$(10^{-6})^{-1/2}=10^3=1000$；B：$(10^{-6})^{-1/6}=10$。完整字符串概率相同，token PPL 相差百倍。

## C. 推导与证明

### LM15-C01
$$PPL=\exp\left(-\frac1D\sum_i\ln p_i\right)
=\exp\left(\ln\prod_i p_i^{-1/D}\right)
=\left(\prod_ip_i\right)^{-1/D}.$$
因此它是目标条件概率几何平均的倒数。

### LM15-C02
固定字符串概率 $P\in(0,1)$，若 tokenizer 用 $D$ 个计分 token，则 $PPL=P^{-1/D}$。随 $D\to\infty$，PPL 趋近 1；$D=1$ 时为 $1/P$。所以仅改变分段长度就能在很大范围改变 PPL，而字符串概率未变。

### LM15-C03
为每个全局 target index 建 `count[t]`。窗口重叠只提供 context；仅窗口的新 stride 区域加入 score，最终断言所有 eligible `count[t]=1`。于是 denominator 是 eligible target 集大小而非各窗口长度之和，不会因重叠重复增长。

## D. 边界、反例与纠错

### LM15-D01
即使 tokenizer 相同，模型 A 计 EOS、B 不计；A 允许跨文档 context、B 重置；A 滑窗每 token 一次、B 重复计重叠区；还可能 prompt ignore 与最大 context 不同。它们的 $N,D$ 和条件信息均不一致。

### LM15-D02
Normalization 可能把多个 byte strings 合并；随机 tokenizer 给同一字符串多条 token path；不同 token sequences 也可能 decode 到同一 bytes。真实字符串概率应对所有潜在路径求和，canonical path 的 NLL 未必足够。还需统一原始 encoding 与边界事件。

### LM15-D03
PPPL 使用 $p(x_i\mid x_{-i})$，CLM PPL 使用 $p(x_i\mid x_{<i})$；前者得到更多右侧信息且条件表未必为 joint。数值低只反映不同预测问题更容易，不能判定联合建模更好。

## E. AI 迁移

### LM15-E01
断言：每个 eligible target 恰计一次；stride 改变但条件窗口相同时 total score 对齐；短于 context 的文档与单次 full forward 一致；文档重置策略下改上一篇末尾不影响下一篇；另测 EOS、空文档和最后不足 stride 的尾块。

### LM15-E02
在相同 UTF-8 corpus 上报告 total NLL/BPB；按语言统计 tokens per word/character/byte 与长尾分布；控制 raw-byte 和 FLOP 预算训练；用同任务协议比较质量、延迟和显存；对 normalization、byte fallback、代码/emoji/形态丰富语言分切片。

### LM15-E03
表中 token PPL 没有共同单位，EOS 差异又改变事件集。要求 raw test hash、tokenizer/normalization hash、total NLL、effective tokens、raw bytes、BOS/EOS与窗口合同；若能定义同一字符串概率则比较 BPB，否则只允许各 tokenizer 内部纵向比较。

## 无提示重做

- [ ] 由三个 token 概率同时算 nats、bits、PPL。
- [ ] 构造“字符串概率相同、PPL 不同”的两分词反例。


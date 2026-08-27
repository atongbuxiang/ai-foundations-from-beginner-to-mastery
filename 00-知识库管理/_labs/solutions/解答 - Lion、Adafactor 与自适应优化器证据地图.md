---
type: solution
status: verified
area: [training, optimization, evidence]
topic: "[[Lion、Adafactor 与自适应优化器证据地图]]"
exercise: "[[习题 - Lion、Adafactor 与自适应优化器证据地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Lion、Adafactor 与自适应优化器证据地图

> [!warning] 使用边界
> 少一份 optimizer state 是明确的算法账本结论；端到端更省显存、更快或更好，需要把参数、梯度、激活、kernel 与调参统计一起审计。

## A. 识别与复述

### TRN16-A01
一种常见合同是 $c_t=\beta_1m_{t-1}+(1-\beta_1)g_t$，用 $\operatorname{sign}(c_t)$ 更新参数，再令 $m_t=\beta_2m_{t-1}+(1-\beta_2)g_t$；另加 decoupled decay。持久 optimizer state 只有 momentum $m$。$\beta_1$ 控制当前 update mixture，$\beta_2$ 控制存入下一步的历史；具体时序必须与实现核对。

### TRN16-A02
对矩阵 $W\in\mathbb R^{n\times m}$，Adafactor 保存平方梯度统计的行因子 $r\in\mathbb R^n$ 与列因子 $c\in\mathbb R^m$，用外积近似完整二阶矩。该部分从 $nm$ 个元素降至 $n+m$；向量参数通常仍需逐元素状态，可选 momentum 又增加状态。

### TRN16-A03
算法门问方程、时序、state 与 parameter group 是否一致；资源门问 bytes、FLOPs、通信、峰值和 wall time；调参门问搜索空间/次数/预算和失败运行是否对等；统计门问 paired seeds、区间、选择规则和复现性是否足够。

## B. 手算与构造

### TRN16-B01
$c_1=0.9(0)+0.1(2)=0.2$，sign 为 $+1$，故 $\theta_1=\theta_0-0.1$。随后 $m_1=0.99(0)+0.01(2)=0.02$。两种 mixture 不应合并成一个 $\beta$。

### TRN16-B02
$P=4096^2=16{,}777{,}216$。Adam 两份 FP32 moments 为 $2P\cdot4=134{,}217{,}728$ bytes（128 MiB）。Adafactor 行列状态为 $(4096+4096)\cdot4=32{,}768$ bytes（32 KiB）。理想二阶状态比为 $2P/(8192)=4096$；未含可选 momentum及其他训练内存。

### TRN16-B03
$r=(4,8)$，$c=(3,9)$，总和 12。外积除总和：
$$\hat A=\frac1{12}\begin{pmatrix}4\\8\end{pmatrix}(3,9)=\begin{pmatrix}1&3\\2&6\end{pmatrix}=A.$$
该矩阵 rank one，第二行是第一行两倍，故因子化恰好精确。

## C. 推导与证明

### TRN16-C01
若 $A=ab^\top$，令 $s_a=\sum_i a_i,s_b=\sum_jb_j$。则 $r_i=a_is_b$、$c_j=b_js_a$、总和 $s_as_b$。因此
$$\frac{r_ic_j}{\sum_{ij}A_{ij}}=\frac{a_is_b b_js_a}{s_as_b}=a_ib_j=A_{ij}.$$

### TRN16-C02
令 $S=\sum_ir_i=\sum_jc_j$。重建矩阵第 $i$ 行和为 $\sum_jr_ic_j/S=r_i$，第 $j$ 列和同理为 $c_j$。但给定边际不唯一；不同内部关联/交互可有相同行列和，所以边际正确不推出每个单元正确。

### TRN16-C03
只比较二阶状态，Adam 为 $nm$，Adafactor 为 $n+m$，比例 $nm/(n+m)$；若把 Adam 的一阶和二阶两份都与无 momentum Adafactor 比则为 $2nm/(n+m)$。$n=m=d$ 时分别约 $d/2$ 与 $d$，随宽度线性增长。

## D. 边界、反例与纠错

### TRN16-D01
取 $A=\begin{pmatrix}1&0\\0&1\end{pmatrix}$，行和、列和均为 $(1,1)$，总和 2，重建为 $\hat A=\tfrac12\mathbf1\mathbf1^\top$。对角的 1 变 0.5，非对角的 0 也变 0.5；边际完全相同但元素结构丢失。

### TRN16-D02
Adam moments 可能只是总显存的一部分；参数、master weights、梯度、activations、KV/temporary buffers 和 fragmentation 不变。Lion 还可能缺少 fused kernel、需要不同 batch 或带来通信差异。因此只能先断言 optimizer persistent state 从约 $2P$ 降到 $P$，端到端比例要实测。

### TRN16-D03
可能使用不同 batch/sequence、硬件利用率、kernel fusion、编译 warmup、gradient accumulation、checkpointing 或通信重叠；达到同一 loss 所需 tokens/steps 也可不同。公平报告应同时给 per-step time、time-to-quality、tokens、硬件与峰值资源。

## E. AI 迁移

### TRN16-E01
表格至少逐方法给：验证/下游质量与区间、达到阈值的 tokens/时间、persistent optimizer bytes、总峰值显存、samples/tokens per second、参数组与精确方程、搜索空间/次数/总算力、paired seeds、失败/中止数和 checkpoint rule。

### TRN16-E02
算法门：先确认方程、decay 和实现一致；资源门：报告 bytes/吞吐/时间到质量；调参门：为每个方法给等额合理搜索而非同一个默认 LR；统计门：多 seed、paired data order、置信区间与预注册选择。缺失这些，结果只能标为单配置 case study。

### TRN16-E03
遍历唯一参数 identity 而非名称：记录 shape、dtype、稀疏性、共享别名、optimizer group、每份 state shape/dtype、分片/副本数和临时 buffer；矩阵注明 factorization，向量注明 full state，embedding 注明 sparse update 支持，共享参数去重。最后从元素数乘 dtype bytes 汇总并与运行时 peak 对照。

## 无提示重做

- [ ] 48 小时后证明 Adafactor 重建保持边际。
- [ ] 一周后为一个真实模型生成 optimizer-state byte ledger。

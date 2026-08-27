---
type: solution
status: verified
area: [training, distributed-systems, data-parallelism]
topic: "[[数据并行、All-Reduce 与全局 Batch 语义]]"
exercise: "[[习题 - 数据并行、All-Reduce 与全局 Batch 语义]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - 数据并行、All-Reduce 与全局 Batch 语义

> [!warning] 使用边界
> collective 的代数接口不等于某后端的固定算法；所有 batch、divisor、dtype 与 uneven-input 政策都要绑定当前实现。

## A. 识别与复述

### TRN61-A01
经典 DP 在每个 DP rank 复制模型/优化算法，切分样本或 token，并同步 gradient（或其 shard）。world size 还可能包含 TP、PP、EP 等不复制完整数据 batch 的轴，所以 global batch 只乘 DP group 大小，不乘总设备数。

### TRN61-A02
local sum 保留本 rank 所有样本梯度之和，local mean 先除本地 count；collective sum 相加各 rank tensor，collective mean 还除 group size。四种组合可产生同一或不同的最终尺度；只有连同最后的有效样本/token divisor，才能判断目标是否是全局经验风险。

### TRN61-A03
local micro-batch 是一次 rank-local forward 的样本数；per-rank accumulated batch 是其跨 micro-step 总和；global batch 是所有 DP ranks 的有效样本总数；LM 还常以有效 token 作权重。增 TP/PP 不自动增加 global batch；增 DP 在 local/accumulation 不变时才成比例增加。

## B. 手算与构造

### TRN61-B01
正确均值
$$
\frac{4(1)+2(4)+3(7)}{4+2+3}=\frac{33}{9}=3.\overline6.
$$
简单 rank mean 为 $(1+4+7)/3=4$。后者把每个 rank 等权，等价于让小 batch 的单样本拥有更大权重。

### TRN61-B02
ring 每 rank 量为 $2(7/8)\cdot1=1.75$ GiB。粗略 parameter-server worker 向 server 发送 $M$ 再接收 $M$，为 2 GiB/worker；更关键的是中央 server 总入口/出口与热点规模随 worker 数增长。这里只比 payload，不代表真实延迟或 topology。

### TRN61-B03
总 GPU 为 $16\times4\times2=128$。global batch 只乘 DP：$2\times8\times16=256$。若错乘总 GPU 会报 $2\times8\times128=2048$，高估 8 倍（正是 TP×PP）。

## C. 推导与证明

### TRN61-C01
令 $s_r=\sum_{i=1}^{n_r}\nabla\ell_{ri}$，则
$$
\nabla L=\frac1N\sum_r\sum_i\nabla\ell_{ri}
=\frac{\sum_rs_r}{\sum_rn_r}.
$$
local mean 的 rank average 为 $(1/P)\sum_r s_r/n_r$；仅当所有 $n_r$ 相等（或另加正确权重）时与上式相同。

### TRN61-C02
对 rank $r$、micro-step $k$ 保存 $(s_{rk},n_{rk})$。目标是
$$
g=\frac{\sum_{r,k}s_{rk}}{\sum_{r,k}n_{rk}}.
$$
先累加 numerator 与 denominator、最后归一一次，可避免 local mean 被错误等权，也使 masked token、最后短 batch 与 `no_sync` 的语义清楚。

### TRN61-C03
ring 把 tensor 切成 $P$ chunks。reduce-scatter 经过 $P-1$ 轮，每轮每 rank 发/收约 $M/P$，量为 $(P-1)M/P$；all-gather 同样一遍，合计 $2(P-1)M/P$。真实实现还有 latency、protocol 与双向链路细节。

## D. 边界、反例与纠错

### TRN61-D01
若 64 GPU 组织成 TP=8、DP=8，每 rank local batch 8，则 global batch 为 $8\times8=64$，不是 512。其余 8 倍设备共同计算同一组样本的 tensor shards。

### TRN61-D02
浮点加法非结合；ring/tree 的分组顺序、bucket 边界、并发到达与 reduction dtype 都会改变最后几位。正确验证是先对 algebra oracle，再在声明容差内比数值，最后以多 seed quality/失败分布判断，而非要求一概逐比特相同。

### TRN61-D03
若 ranks 的有效 count 为 $(4,4,1)$，rank-mean 给最后一个样本与前四样本块相同权重；若 rank 提前结束，collective 次数还可能失配。padding 只有在 loss 和 denominator 都排除 pad 时才无偏。小尾 batch 周期性重复时并非必然“可忽略”。

## E. AI 迁移

### TRN61-E01
记录 dataset/sampler/shuffle、drop-last/padding/join、每 rank 有效 sequence/token count、mask、loss 的 sum/mean 口径、micro-step accumulation、DP group、collective sum/mean 与 dtype、最后 divisor、`no_sync`、overflow consensus、bucket 和 data order。日志保留每 rank count 以便离线重算。

### TRN61-E02
以实测 1-rank $T_1$ 为 baseline，固定 global batch/sequence/model/update 数；对 $P=1,2,4,...,64$ 调整 local batch/accumulation，锁定 data order 与 optimizer semantics。预热后报告 step-time 分布、throughput、efficiency、comm exposed tail、peak memory、matched learning curve、失败/重启和 time-to-quality。

### TRN61-E03
用一个标量线性模型和手选 unequal samples，解析计算每样本 gradient sum/count；单卡对全部样本求一次 reference，多卡模拟 local reduction + collective。分别测试 sum/sum、mean/mean、uneven mask 和 accumulation；先要求 FP64 oracle 一致，再按目标 dtype 设容差，不把非结合造成的末位差判成 estimator 错误。

## 无提示重做

- [ ] 48 小时后重推 unequal-rank mean。
- [ ] 一周后从 mesh 独立算 global batch 与 ring bytes。

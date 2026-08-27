---
type: solution
status: verified
area: [training, optimization, horizon, restart, schedule-free]
topic: "[[训练时域、Restart、Schedule-Free 与末端学习率]]"
exercise: "[[习题 - 训练时域、Restart、Schedule-Free 与末端学习率]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - 训练时域、Restart、Schedule-Free 与末端学习率

> [!warning] 使用边界
> “继续训练”不是唯一操作；精确语义由状态转移和未来 schedule 共同定义。

## A. 识别与复述

### TRN36-A01
continue 是不中断地沿同一状态和算法前进；resume 是序列化后恢复，目标是与 continue 等价；restart 明确重置某些控制或 optimizer state；branch 从共同 checkpoint 复制完整状态后走不同未来；fine-tune 通常换数据/目标且允许重建 optimizer。精确 resume 默认 keep 参数、moments、counter、RNG、data cursor；其他三者必须逐字段写 keep/reset/transform，不能靠名称猜。

### TRN36-A02
Schedule-Free 可不把未来 $T$ 放进 full-horizon decay，但仍维护快速优化点、在线平均点、求梯度/插值点，以及 optimizer moments、平均权重、LR、warmup 和 step counter。训练与评估可能使用不同点。故 horizon-free 只描述某类未来依赖，不等于没有状态。

### TRN36-A03
last 是最后一步参数；best-validation 是在多个候选中选择；EMA/SWA 是轨迹平均；branch-end 是某个尾部分支的输出。末端 LR 影响最后轨迹的噪声与位置，而选择规则决定交付哪个点并引入多少验证预算；缺一项无法解释最终模型来源。

## B. 手算与构造

### TRN36-B01
旧 horizon 在 $t=T/2$：
$$
\eta_{T/2}(T)=\tfrac12\eta_{max}[1+\cos(\pi/2)]=0.5\eta_{max}.
$$
新 horizon $2T$：
$$
\eta_{T/2}(2T)=\tfrac12\eta_{max}[1+\cos(\pi/4)]
\approx0.853553\eta_{max}.
$$
所以“延长 horizon”并非只追加后半段。

### TRN36-B02

| 操作 | $\theta$ | $m,v$ | $k$ | RNG $r$ | cursor $d$ |
|---|---|---|---|---|---|
| 精确 resume | keep | keep | keep | keep | keep |
| 只重启 LR | keep | keep（必须明说） | scheduler phase reset、optimizer step 可 keep | keep | keep |
| 新数据 fine-tune | initialize from old | reset 或 transform | reset | new recorded seed | reset to new dataset |

若“只重启 LR”同时重置 Adam step，bias correction 也变了，就不再只是 LR restart。

### TRN36-B03
$c_1=1$ 给 $x_1=2$；$c_2=1/2$ 给 $x_2=3$；$c_3=1/3$ 给
$$
x_3=\frac23\cdot3+\frac13\cdot10=\frac{16}{3}\approx5.333.
$$
错用 $z_3=10$ 比平均点高 $14/3\approx4.667$。这不是数值误差，而是评估了不同算法状态。

## C. 推导与证明

### TRN36-C01
对 $0<t<T$，有 $0<\pi t/(2T)<\pi t/T<\pi$。cosine 在 $(0,\pi)$ 严格递减，故
$$
\eta_t(2T)>\eta_t(T).
$$
因此从头训练的 $2T$ baseline 在所有这些时刻用了不同 LR，参数和 moments 已不同；从 $T$ run checkpoint 继续只能回答“在旧历史上追加”的问题。

### TRN36-C02
令状态 $S=(\theta,m,v,k,\ldots)$，restart 是 $S^+=R(S^-)$。方案一只重置 scheduler phase，保留 $m,v,k$；方案二还把 $m=v=0,k=0$。即使下一 LR 相同，Adam 方向分别使用旧 $m/\sqrt v$ 与新梯度建立的状态，bias correction 也不同，下一步通常不相等。因此 restart 必须是字段级映射。

### TRN36-C03
递推展开为
$$
x_t=\left[\prod_{j=1}^t(1-c_j)\right]x_0
+\sum_{k=1}^t c_k\left[\prod_{j=k+1}^t(1-c_j)\right]z_k.
$$
系数加初始化残余恒为 1；若某个 $c_1=1$，初始化残余为零，历史 $z_k$ 权重和为 1。训练用哪个插值点求梯度、评估用 $x_t$ 还是 $z_t$，都会改变输出，因而属于算法合同。

## D. 边界、反例与纠错

### TRN36-D01
没有 LR 就不能控制快速点的步长；没有 warmup 约定就不知道早期状态如何建立；没有 moments/average weights 就不能继续递推；没有 checkpoint contract 就无法恢复多个点和计数器。Schedule-Free 取消的是某类预定 decay horizon，不是这些对象。

### TRN36-D02
取相同 $\theta$、当前梯度相同，但 run A 的 Adam $m=1,v=1$，run B 的 $m=0,v=100$。下一预条件方向显著不同，参数立即分叉。或 data cursor 不同导致下一 batch 不同。参数只是完整训练状态的一个投影。

### TRN36-D03
若看 100 个 checkpoint 并选验证最好者，验证集被用于 100 次适应性选择；候选数越多，偶然高分越可能被选中。若不同 final-LR 方案保存/筛选的候选数不同，差异可能来自选择预算而非末端动力学。应固定候选网格与选择规则，并用独立 test 只评一次锁定模型。

## E. AI 迁移

### TRN36-E01
可机读合同至少含：schema/code version、model parameter hash、group manifest、optimizer type及全部 tensors、optimizer/scheduler counters、phase/horizon、averaging points/weights、RNG for host/device/workers、sampler epoch/cursor、precision scaler、dataloader state、dataset fingerprint。恢复测试应与不中断 run 比较下一若干步日志和产物哈希。

### TRN36-E02
三法固定模型、数据、tokens/FLOPs、seed 集、调参次数和最终评估次数；记录共享/非共享训练成本。每法允许同等搜索预算寻找合理超参，另做默认配置对照。输出统一比较 last 与方法原生推荐点，并把额外 checkpoint/ensemble 推理成本列入选择和评估账。

### TRN36-E03
lineage 图以 trunk checkpoint 为父节点，三个 cooldown 为子节点；唯一训练成本是 $100+3\times10=130$ GPUh。每个分支保存 parent hash、复制的完整 state、future schedule 和选择状态。若报告部署某一分支的边际成本可写 10 GPUh，但总研究成本仍含共享主干与所有候选，不可在不同表中重复或漏计。

## 无提示重做

- [ ] 48 小时后写出五种训练转移的状态表。
- [ ] 一周后证明 $T$ checkpoint continuation 不等于从头 $2T$ cosine。

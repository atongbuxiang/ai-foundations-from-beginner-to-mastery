---
type: solution
status: draft
area: [neural-networks/activations, glu, gating]
topic: "[[GLU、GeGLU、SwiGLU 与乘性门]]"
exercise: "[[习题 - GLU、GeGLU、SwiGLU 与乘性门]]"
sources: ["[[S-2017-Dauphin-Gated-Convolutional-Networks]]", "[[S-2020-Shazeer-GLU-Variants]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - GLU、GeGLU、SwiGLU 与乘性门

## A

### NN-GLU-A01
统一写成 $V=XW_v+b_v$、$G=XW_g+b_g$、$H=V\odot\phi(G)$。取 $\phi=\sigma,\operatorname{ReLU},\operatorname{GELU},\operatorname{SiLU},\operatorname{id}$，依次得到 GLU、ReGLU、GEGLU、SwiGLU、Bilinear；完整 FFN 还要接 $Y=HW_o+b_o$。这里的 “GEGLU” 常全大写，节点标题保留便于检索的 GeGLU 别名。

### NN-GLU-A02
只有 sigmoid 的输出被限制在 $(0,1)$，可读成软开关。GELU/SiLU 的输出在负侧可为负，正侧无界，因而会改变 value 的符号与尺度；它们是 multiplicative branch，不是概率。把它们称为 gate 是结构语言，不能据此套用概率归一化或 Bernoulli 解释。

### NN-GLU-A03
标准 FFN 有 input/output 两个主矩阵 $W_1:[d,h]$、$W_2:[h,d]$，中间主要保存一个宽度 $h$ 的激活。gated FFN 有 $W_v,W_g:[d,h_g]$ 与 $W_o:[h_g,d]$ 三矩阵，forward 至少产生 $V,G$ 及乘积 $H$；融合可减少物化张量，但 backward 仍要保存或重算足够信息。

## B

### NN-GLU-B01
对 $H=V\odot\phi(G)$，
$$dH=dV\odot\phi(G)+V\odot\phi'(G)\odot dG.$$
与上游 $U=\bar H$ 作 Frobenius 内积并把 $dV,dG$ 的系数收集出来：
$$\bar V=U\odot\phi(G),\qquad \bar G=U\odot V\odot\phi'(G).$$
这是逐元乘法 product rule 的 reverse-mode 形式。

### NN-GLU-B02
由 $V=XW_v+b_v$、$G=XW_g+b_g$，
$$\bar X=\bar VW_v^T+\bar GW_g^T,$$
$$\bar W_v=X^T\bar V,\quad \bar W_g=X^T\bar G,$$
$$\bar b_v=\operatorname{reduce}_{B,T}\bar V,\quad \bar b_g=\operatorname{reduce}_{B,T}\bar G.$$
若还含 $Y=HW_o+b_o$，先算 $\bar H=\bar YW_o^T$、$\bar W_o=H^T\bar Y$。共享输入的两条 cotangent 必须累加，漏一项即错误。

### NN-GLU-B03
忽略 bias，标准 FFN 参数约为 $dh+hd=2dh$；gated FFN 为 $dh_g+dh_g+h_gd=3dh_g$。令二者相等得到 $h_g=2h/3$。实际实现要把 $h_g$ round 到 tensor-core/tensor-parallel 友好的倍数，再按实际尺寸重算，而不是把 $2/3$ 当成精确硬件合同。

## C

### NN-GLU-C01
bilinear 情形第 $j$ 个坐标为
$$H_j=(w_{v,j}^Tx)(w_{g,j}^Tx)=x^T(w_{v,j}w_{g,j}^T)x.$$
标量 quadratic form 只依赖该矩阵的对称部分。加入 bias 后还出现线性项与常数项；输出投影再组合这些 rank-one 二次特征，因此门控显式引入二阶交互。

### NN-GLU-C02
GLU 的 value-path Jacobian 为 $\operatorname{diag}(\sigma(G))$。取任意有界 $V,U$ 并令 $G=-M\mathbf1$，当 $M\to\infty$ 时 $\sigma(G)\to0$，故该路径的最小 slope 可任意接近 0，不存在与输入无关的正下界。GEGLU/SwiGLU 甚至可在特定输入处取零或负 slope，更不能承诺恒通梯度。

### NN-GLU-C03
需要的是 $E[V^2\phi(G)^2]$，只有在 $V$ 与 $\phi(G)$ 独立时才可拆成 $E[V^2]E[\phi(G)^2]$。两支共享 $X$，条件于固定权重时通常相关；即使随机初始化使某些协方差期望为 0，零相关也不自动给非线性函数后的独立。正确做法是给联合分布/协方差假设，或直接估计联合 moment。

## D

### NN-GLU-D01
参数匹配只使主矩阵元素数相近。两支 input projection、activation–multiply、额外读写、保存张量、通信 shard、tile rounding 与 fusion 会改变 MAC、bytes 和 kernel launch；不同设备的 compute/memory balance 还不同。因此必须分别报告实际参数、理论 MAC、峰值/保存 activation 和实测 latency。

### NN-GLU-D02
对 sigmoid GLU，令 $G=-M$、$|V|\le C$、$|U|\le C$。则 $|\bar V|=|U|\sigma(-M)\to0$，且 $|\bar G|=|UV|\sigma(-M)(1-\sigma(-M))\to0$。所以 value 与 gate 两支都可同时近零；“一支线性”没有绕过乘性汇合。

### NN-GLU-D03
同宽替换把参数从约 $2dh$ 增到 $3dh$，并改变 FLOP、memory、初始化与可调超参数，accuracy 提升不能归因于激活名称。至少加入 matched-parameter 的 $h_g\approx2h/3$、matched-latency 和 independently retuned baselines，并报告 seeds、训练 token、失败 run 与真实吞吐，结论才可缩窄到指定预算轨道。

## E

### NN-GLU-E01
用 unfused FP64/FP32 composition 作 oracle，覆盖 batch/token/width 的小值、非 tile 倍数、strided layout、极端 $G,V$、NaN/Inf 与各种 dtype。检查 forward、两支 VJP、input/weight/bias gradient、double backward、split 顺序和 determinism；做 dot-product test。性能侧比较 fusion 前后 kernel 数、bytes、occupancy 与吞吐，并验证保存/重算策略不改变结果合同。

### NN-GLU-E02
设 baseline GELU-FFN、GLU、GEGLU、SwiGLU，至少跑同宽、matched parameters、matched latency 三轨；每轨固定数据、token、优化器和搜索预算，同时允许各模型预注册范围内 retune。记录 value/gate distribution、两支 gradient norm、参数/MAC/bytes/latency、能耗和多 seed metric。选择只看 validation，test 留作一次确认。

### NN-GLU-E03
对每个 TP rank，账本应列 $W_v,W_g,W_o$ 的 shard 方向、本地 GEMM shape、all-reduce/all-gather 次数与字节、是否 overlap。activation 账本按元素字节数 $s$ 记录 $V,G,H$、activation derivative 所需缓存和 checkpoint 重算；若 fused，不应假装逻辑张量都完全物化，也不能忽略通信 buffer。最终同时给 peak allocated bytes 与跨链路 bytes/token。


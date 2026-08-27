---
type: solution
status: verified
area: [language-models, decoding]
topic: "[[EOS、停止规则、重复惩罚与退化循环]]"
exercise: "[[习题 - EOS、停止规则、重复惩罚与退化循环]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - EOS、停止规则、重复惩罚与退化循环

## A. 识别与复述

### LM52-A01
$h_t=P(\text{EOS at }t\mid T\ge t,h_t^{\text{prefix}})$ 是已存活到第 $t$ 步时的条件终止概率；$S(t)=P(T\ge t)=\prod_{i<t}(1-h_i)$ 是进入第 $t$ 步前仍未 EOS 的概率。它们一个是条件局部量，一个是累计量。

### LM52-A02
EOS token 是模型分布内事件；stop string 是解码后文本匹配；max tokens 是预算截断；grammar accepting 可由约束器终止；cancel/timeout 是服务外部事件。后四者未必代表模型选择 EOS，返回对象应分别编码。

### LM52-A03
惩罚在采样前修改已出现 token 的 logits 或概率，再重归一化，因此每步 kernel $q_t$ 及整个序列分布都变化。若只是输出后删重复文本，才是后处理；二者效果和证据含义不同。

## B. 手算与构造

### LM52-B01
$S(1)=1$，$S(2)=.9$，$S(3)=.9\times.8=.72$，三步后仍未 EOS 为 $.72\times.5=.36$。恰在第三步停止的概率 $S(3)h_3=.72\times.5=.36$。

### LM52-B02
已出现 token 的新 logit 为 $2/1.25=1.6$，仍高于未出现 token 的 $1.5$，所以排序没有翻转，但 gap 从 $.5$ 降到 $.1$。注意不同库对负 logits 的规则不同，必须写出精确定义。

### LM52-B03
状态按 $(A,B,C)$，令 $A\to B,B\to C,C\to A$，则
$$P=\begin{bmatrix}0&1&0\\0&0&1\\1&0&0\end{bmatrix}.$$
从任一状态都以周期 3 永久循环，说明局部转移确定性足以形成退化环。

## C. 推导与证明

### LM52-C01
进入第 $t$ 步需前 $t-1$ 步均不停止，概率 $S(t)=\prod_{i<t}(1-h_i)$；再乘本步条件停止概率得 $P(T=t)=S(t)h_t$。上限 $M$ 前都不 EOS 的概率为 $prod_{i=1}^M(1-h_i)=S(M+1)$，此时 finish reason 应是 length 而非 EOS。

### LM52-C02
令 stop string 为 `END`，token 解码片段依次为 `E` 与 `ND`。任一单 token 文本都不等于/不含 `END`，连接后的滚动缓冲区却含它。因此需在最近字符后缀上跨 token 匹配，并规定返回是否包含 stop string。

### LM52-C03
Presence penalty 写成 $z'_v=z_v-\alpha I_v$。先惩罚再变温为 $(z_v-\alpha I_v)/\tau$；先变温再减同一数值惩罚为 $z_v/\tau-\alpha I_v$，除非 $\tau=1$ 或同时把惩罚缩为 $\alpha/\tau$，二者不同。反过来，常见 repetition penalty $f_r(z)=z/r$（$z>0$）或 $rz$（$z<0$）是正齐次的，$f_r(z)/\tau=f_r(z/\tau)$，所以它与纯正温度缩放可交换；与 top-$p$ 等 support 算子仍未必交换。必须按具体 processor 定义证明，不能一句“都不交换”概括。

## D. 边界、反例与纠错

### LM52-D01
服务通常消费 EOS token 而不把其字面表示返回用户。还可能在 stop string、length 或 parser 接受时结束。应检查 output token IDs、finish reason 与 trace，不能从显示文本是否含特殊符号反推。

### LM52-D02
该 API 丢失了因果：模型自然完成、预算不足、用户取消会被混作一类，导致长度统计、SLO、失败率和重试策略错误。修复为枚举 finish reason，保存触发位置/规则、原始 token 数、截断有效性和服务错误码。

### LM52-D03
重复可能来自模型概率尖锐、训练数据模式、prompt、greedy/beam 偏好、低温/截断、重复惩罚缺失、上下文回声或状态实现 bug。Exposure bias 是训练与 rollout history 错位的一种机制，不能由表面重复唯一识别。

## E. AI 迁移

### LM52-E01
覆盖：首 token EOS、无 EOS 达上限、stop 完全在 token 内/跨 token/与 EOS 同步、重叠 stop strings、Unicode/byte 边界、grammar accept/dead-end、client cancel/timeout、返回是否去除标记、streaming 已发送字节能否回收。每例断言 token IDs、文本和 finish reason。

### LM52-E02
固定模型/prompt 集，正交扫描 sampler/温度、repetition penalty、context 回声和最大长度；多 seed 报 exact n-gram repetition、周期长度、任务质量与 EOS hazard。另用 teacher-forced logits 与 free rollout 分开模型形状和历史漂移。

### LM52-E03
服务端保留跨 token rolling buffer，在确认不构成 stop 前延迟少量尾部字节；记录 stop rule/version、匹配 span、是否剥离、token/byte offsets、finish reason、cancel source、已发送与保留字节。结构化输出在截断后必须重新验证，失败显式返回而非伪装成功。

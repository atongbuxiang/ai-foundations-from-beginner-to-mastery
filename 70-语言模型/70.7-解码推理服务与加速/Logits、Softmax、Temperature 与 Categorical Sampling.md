---
type: concept
status: verified
area: [language-models, decoding, sampling]
node_id: LM-49
aliases: [温度采样, Categorical 解码]
prerequisites: ["[[Softmax 输出层、Logit 尺度与概率参数化]]", "[[祖先采样、温度、截断与自回归解码分布]]"]
related: ["[[Top-k、Top-p、Typical 与 Min-p 截断采样]]", "[[Model、API、Tokenizer、Template 版本与复现合同]]"]
sources: ["[[S-2020-Su-7500-自回归停止与解码]]", "[[S-2019-Holtzman-Nucleus-Sampling]]", "[[S-2023-Su-9698-Output-Embedding]]"]
exercises: ["[[习题 - Logits、Softmax、Temperature 与 Categorical Sampling]]"]
solutions: ["[[解答 - Logits、Softmax、Temperature 与 Categorical Sampling]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-decoding-temperature-simplex-v1.svg]]"
created: 2026-08-26
updated: 2026-08-27
---

# Logits、Softmax、Temperature 与 Categorical Sampling

## 零、本页在课程中的位置

- **承接**：[[Softmax 输出层、Logit 尺度与概率参数化]]已经说明模型怎样产生词表 logits；[[祖先采样、温度、截断与自回归解码分布]]已经给出自回归采样的总体框架。
- **中心问题**：一次解码步中，怎样把模型的任意实数分数变成概率，温度究竟改变什么，随机数又怎样选出一个 token？
- **去向**：下一节[[Top-k、Top-p、Typical 与 Min-p 截断采样]]会在这里得到的温度分布上删去部分候选并重新归一化。

> [!tip] 两遍阅读
> 第一遍只跟随三 token 算例完成 `logits → softmax → temperature → inverse CDF`；第二遍再推导熵对温度的导数，并进入 processor 顺序、RNG 与服务复现。

> [!abstract] 一句话结论
> 模型给 logits，解码器才定义真正 rollout 的 categorical kernel。Temperature 缩放 log-odds 而不改变有限温度下的排名；seed 只初始化某个 RNG 流，不能独自标识模型、处理器、并行归约或服务调度。

## 一、logit 不是概率

先取一个可以手算的例子。词表只有三个 token：`A`、`B`、`C`，模型给出的 logits 是

$$
z=(2,1,0).
$$

这三个数既不在 $[0,1]$ 中，和也不是 1，因此不能直接当概率。它们只表示相对偏好：`A` 比 `B` 高 1，`B` 又比 `C` 高 1。

### 1.1 对象与符号

| 符号 | 类型/维度 | 含义 |
|---|---|---|
| $V$ | 有限集合 | 当前 tokenizer 的词表 |
| $h_t=(x,y_{<t})$ | token 序列或模型状态 | 第 $t$ 步已知的输入和生成前缀 |
| $z_t\in\mathbb R^{|V|}$ | 实向量 | 模型对词表中每个 token 给出的 logit |
| $z_v$ | 标量 | token $v$ 的 logit |
| $\tau>0$ | 标量 | temperature |
| $p_\tau(v\mid h_t)$ | 概率 | 温度为 $\tau$ 时 token $v$ 的归一化概率 |
| $U_t\in[0,1)$ | 随机数 | inverse-CDF 采样使用的均匀随机数 |

对固定前缀 $h_t=(x,y_{<t})$，模型输出 $z_t\in\mathbb R^{|V|}$。Softmax 把它变成概率：

$$
p_\theta(v\mid h_t)
=\frac{e^{z_v}}{\sum_{u\in V}e^{z_u}}.
$$

分子 $e^{z_v}>0$ 保证每项非负；分母把所有未归一化权重相加，因此

$$
\sum_{v\in V}p_\theta(v\mid h_t)
=\frac{\sum_v e^{z_v}}{\sum_u e^{z_u}}=1.
$$

这解释了 softmax 的两个基本职责：把实数变成正权重，再把正权重归一化。

加同一常数不改变概率：

$$
\operatorname{softmax}(z+c\mathbf1)=\operatorname{softmax}(z).
$$

因为分子和分母都会多出同一个因子 $e^c$：

$$
\frac{e^{z_v+c}}{\sum_u e^{z_u+c}}
=\frac{e^c e^{z_v}}{e^c\sum_u e^{z_u}}
=\frac{e^{z_v}}{\sum_u e^{z_u}}.
$$

数值实现因此可以取 $m=\max_v z_v$，计算 $e^{z_v-m}$，避免最大的指数溢出。对 $z=(2,1,0)$，减去 $m=2$ 后得到 $(0,-1,-2)$：

$$
\begin{aligned}
(e^0,e^{-1},e^{-2})&\approx(1,0.3679,0.1353),\\
Z&\approx1.5032,\\
p_1&\approx(0.6652,0.2447,0.0900).
\end{aligned}
$$

三项均为正且和约为 1，这是最直接的计算检查。保存显示概率而不保存 logits 和后续 processors，仍会丢失可复现信息。

现在我们已经得到基准分布；下一步只改变一个标量 $\tau$，观察概率质量怎样移动。

## 二、temperature 改变什么

温度 $\tau>0$：

$$
p_\tau(v)=\frac{e^{z_v/\tau}}{\sum_ue^{z_u/\tau}}.
$$

两 token 的 odds：

$$
\frac{p_\tau(i)}{p_\tau(j)}
=\exp\left(\frac{z_i-z_j}{\tau}\right).
$$

这条式子可直接从两个 softmax 概率相除得到：

$$
\begin{aligned}
\frac{p_\tau(i)}{p_\tau(j)}
&=\frac{e^{z_i/\tau}/\sum_u e^{z_u/\tau}}
        {e^{z_j/\tau}/\sum_u e^{z_u/\tau}}\\
&=\frac{e^{z_i/\tau}}{e^{z_j/\tau}}
&&\text{共同的归一化分母约掉},\\
&=\exp\left(\frac{z_i-z_j}{\tau}\right)
&&\text{使用 }e^a/e^b=e^{a-b}.
\end{aligned}
$$

$\tau<1$ 放大 logit gap，$\tau>1$ 缩小 gap。有限正温度下 argmax 排名不变；采样频率与熵改变。若唯一最大 logit，$\tau\to0^+$ 集中到 argmax；若有 $m$ 个并列最大项，极限在这 $m$ 项均匀；$\tau\to\infty$ 时在有限词表趋向均匀。

仍使用 $z=(2,1,0)$：

| 温度 | $p(A)$ | $p(B)$ | $p(C)$ | 现象 |
|---:|---:|---:|---:|---|
| $0.5$ | $0.8668$ | $0.1173$ | $0.0159$ | 质量集中到最大 logit |
| $1$ | $0.6652$ | $0.2447$ | $0.0900$ | 基准分布 |
| $2$ | $0.5065$ | $0.3072$ | $0.1863$ | 分布变平，但排名不变 |

注意：$\tau=0$ 不能直接代入 $z_v/\tau$。Greedy/argmax 是 $\tau\to0^+$ 的极限行为或独立定义的确定性规则，不是一次合法的除零计算。

## 三、熵随温度的关系

上一节的数值表显示升温让分布变平。现在证明 token-level Shannon entropy 确实单调不减。

令逆温度 $\beta=1/\tau$，并定义

$$
Z(\beta)=\sum_{v\in V}e^{\beta z_v},\qquad
p_\beta(v)=\frac{e^{\beta z_v}}{Z(\beta)}.
$$

由 $\log p_\beta(v)=\beta z_v-\log Z(\beta)$，熵为

$$
H(\beta)=\log Z(\beta)-\beta\mathbb E_\beta[z].
$$

先计算两个桥接导数。第一，log-partition 的导数是 logit 均值：

$$
\begin{aligned}
\frac{d}{d\beta}\log Z(\beta)
&=\frac{1}{Z(\beta)}\frac{dZ}{d\beta}\\
&=\frac{\sum_v z_v e^{\beta z_v}}{Z(\beta)}\\
&=\sum_v p_\beta(v)z_v
=\mathbb E_\beta[z].
\end{aligned}
$$

第二，均值的导数是方差。先对单个概率求导：

$$
\frac{dp_\beta(v)}{d\beta}
=p_\beta(v)\bigl(z_v-\mathbb E_\beta[z]\bigr).
$$

于是

$$
\begin{aligned}
\frac{d}{d\beta}\mathbb E_\beta[z]
&=\sum_v z_v\frac{dp_\beta(v)}{d\beta}\\
&=\sum_v p_\beta(v)z_v^2-\mathbb E_\beta[z]^2\\
&=\operatorname{Var}_\beta(z).
\end{aligned}
$$

现在对 $H(\beta)=\log Z-\beta\mathbb E_\beta[z]$ 使用乘积法则：

$$
\begin{aligned}
\frac{dH}{d\beta}
&=\mathbb E_\beta[z]
  -\mathbb E_\beta[z]
  -\beta\operatorname{Var}_\beta(z)\\
&=-\beta\operatorname{Var}_\beta(z)\le0.
\end{aligned}
$$

最后由 $d\beta/d\tau=-1/\tau^2$ 和 $\beta=1/\tau$，得到

$$
\frac{dH}{d\tau}
=\frac{\operatorname{Var}_\tau(z)}{\tau^3}\ge0.
$$

这里的下标 $\tau$ 表示在 $p_\tau$ 下计算方差。若所有 logits 相同，方差为 0，温度不会改变本来就均匀的分布；否则升温严格增加 token-level entropy。但更高 token 熵不自动意味着语义更多样或质量更好。

## 四、categorical sampling

Softmax 和 temperature 只定义了概率，还没有真正选出 token。Categorical sampling 用随机数把概率分布变成一次离散选择。

给归一化概率 $q_t$，可用 inverse CDF：

1. 取 $U_t\sim\operatorname{Uniform}[0,1)$；
2. 按固定 token 顺序累加；
3. 选择首个累计质量超过 $U_t$ 的 token。

完整序列由

$$
q(y_{1:T}\mid x)
=\prod_{t=1}^{T}q_t(y_t\mid x,y_{<t})
$$

定义；$q_t$ 可能已含 temperature、penalty、mask 与 truncation，不再等于原始 $p_\theta$。

沿用 $\tau=1$ 的三 token 算例，按 `A`、`B`、`C` 顺序构造累计区间：

| token | 概率 | 累计区间 |
|---|---:|---|
| A | $0.6652$ | $[0,0.6652)$ |
| B | $0.2447$ | $[0.6652,0.9099)$ |
| C | $0.0900$ | $[0.9099,1)$ |

若 $U_t=0.80$，它落在 B 的区间，所以本步输出 B。换一个随机数可能得到不同 token，但大量独立重复后的频率才应接近目标概率；单次样本不能验证采样器正确。

## 五、processor 顺序

真实解码通常不只有 temperature。Mask、惩罚和截断会依次改写 logits 或概率，因此顺序本身就是算法的一部分。

若先 temperature 再 top-$p$，候选集合依据变温后的概率；反过来依据原概率。一般

$$
\operatorname{TopP}(\operatorname{Temp}(z))
\ne \operatorname{Temp}(\operatorname{TopP}(z)).
$$

重复惩罚、禁词、grammar mask、logit bias、temperature、top-$k/p$ 的顺序必须保存。只写 temperature=.7 不足以重建采样核。

## 六、seed 控制什么

确定采样核以后，还要区分“分布可复现”和“某次随机轨迹逐字节复现”。固定 seed 只解决后者的一小部分。

固定 seed 通常只固定某一 RNG 初态。字节级复现还要求相同 checkpoint、tokenizer/template/input IDs、processors/order、RNG algorithm/device/stream/call count、kernel/parallel reduction、batch scheduler、stop/parser。

Continuous batching 改变请求进入 batch 的时机时，共享 RNG 流会漂移。应使用 per-request RNG state 并记录 counter。

## 七、图解：温度怎样移动概率质量

**读图问题**：固定 logits 排名以后，温度究竟怎样搬运三项概率质量，同一个 uniform 随机数又会落入哪个区间？

![[00-知识库管理/_assets/figures/language-models/fig-lm-decoding-temperature-simplex-v1.svg|900]]

> [!figure] 图 LM-49　同一 logits 在不同温度下的 simplex 轨迹
> **生成：**本库按 softmax、odds、entropy 与 inverse-CDF 公式确定性绘制；概率和随机数均为可手算的教学算例。

**怎样读图**：先沿温度轴比较三条概率曲线，确认排名始终不交换；再把 $\tau=1$ 的概率条当成累计区间，核对红色 uniform 标记为何落在 token B。

**图没有证明什么**：概率更均匀只说明 token-level entropy 在这个算例中增加；它不证明长文本更有创造力、语义更多样、事实性更高，也不证明固定 seed 能跨实现复现。

## 八、常见错误与出口标准

错误包括：把 logit 当 log-prob；把 $\tau=0$ 直接代公式；声称温度改变排名；只存 seed；忽略 processor 顺序；用单次样本判断分布。

## 九、AI 对象映射

| 数学对象 | 推理系统中的对象 | 常见失配 |
|---|---|---|
| $z_t\in\mathbb R^{|V|}$ | 模型最后一层输出 logits | 错把显示概率或截断后概率当原 logits |
| $p_\tau$ | temperature processor 后的词表分布 | 忘记 temperature 的位置和数值精度 |
| $q_t$ | 所有 mask、penalty、truncation 后的实际采样核 | 仍把它记作原模型 $p_\theta$ |
| $U_t$/RNG state | 设备上的随机数流 | 只记录 seed，不记录算法、stream 和调用次数 |
| $y_t$ | 本步输出 token ID | 只保存解码文本，无法重建 token 级轨迹 |

## 十、本节回顾与下一节接口

完成本节后，应能：

1. 对一组小 logits 稳定计算 softmax，并检查概率和为 1；
2. 从概率比逐步推出 temperature 对 odds 的影响；
3. 手算不同温度下的分布并解释两个温度极限；
4. 使用 log-partition 的两个桥接导数推导 $dH/d\tau\ge0$；
5. 用 inverse CDF 和一个具体随机数选出 token；
6. 区分模型分布、processor 后采样核与一次 RNG 轨迹。

下一节[[Top-k、Top-p、Typical 与 Min-p 截断采样]]会改变候选集合。届时要继续追问：删掉了多少概率质量、怎样重新归一化，以及截断与 temperature 的先后顺序是否改变最终分布。

## 十一、来源与练习

- [[S-2020-Su-7500-自回归停止与解码]]；
- [[S-2019-Holtzman-Nucleus-Sampling]]；
- [[S-2023-Su-9698-Output-Embedding]]；
- [[习题 - Logits、Softmax、Temperature 与 Categorical Sampling]]；
- [[解答 - Logits、Softmax、Temperature 与 Categorical Sampling]]。

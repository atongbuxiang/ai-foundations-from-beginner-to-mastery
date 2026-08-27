---
type: concept
status: draft
area: [architecture, attention, numerical-stability, probability]
aliases: [Scaled Dot-Product Attention, Stable Softmax, Attention Scaling]
node_id: ARCH-26
prerequisites: ["[[内容寻址、Query、Key 与 Value]]", "[[期望、方差与矩]]", "[[Softmax 输出层、Logit 尺度与概率参数化]]", "[[浮点数与舍入误差]]"]
related: ["[[Attention 的对象、几何与表达 MOC]]", "[[Attention Mask、因果性与可见性合同]]", "[[Attention 的几何、核与概率视角]]"]
sources: ["[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2026-Su-11814-LSE-Softmax-Taylor]]", "[[S-2023-Su-9859-KeyNorm长度外推]]", "[[S-2021-Su-8620-Transformer初始化参数化与标准化]]"]
exercises: ["[[习题 - Scaled Dot-Product Attention 与 Softmax 数值语义]]"]
solutions: ["[[解答 - Scaled Dot-Product Attention 与 Softmax 数值语义]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-attention-scaled-softmax-ledger-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Scaled Dot-Product Attention 与 Softmax 数值语义

> [!abstract] 本节主问题
> 标准 Attention 为什么把 $QK^\top$ 除以 $\sqrt{d_k}$？Softmax 为什么必须逐行且要减去最大值？答案分别来自条件化的方差尺度与精确的数值等价变换。两者都不是装饰性技巧，也不能被一句“防止梯度消失”含糊带过。

## 一、完整定义

对一批 query、key、value，scaled dot-product attention 为

$$
\operatorname{Attn}(Q,K,V;M)
=\operatorname{softmax}_{\text{row}}
\left(\frac{QK^\top}{\sqrt{d_k}}+M\right)V.
$$

$M$ 是可选 additive mask：允许位置为 $0$，禁止位置为 $-\infty$（数学语义）。若无 mask，取 $M=0$。分三阶段读：

1. score：$S=QK^\top/\sqrt{d_k}$；
2. normalize：$A=\operatorname{softmax}_{row}(S+M)$；
3. read：$O=AV$。

## 二、$1/\sqrt{d_k}$ 的方差推导

先只看一个 $q,k\in\mathbb R^{d_k}$。设各坐标满足：

- $q_r,k_r$ 相互独立；
- $\mathbb E q_r=\mathbb E k_r=0$；
- $\operatorname{Var}(q_r)=\operatorname{Var}(k_r)=1$；
- 不同 $r$ 的乘积项不相关。

则

$$
q^\top k=\sum_{r=1}^{d_k}q_rk_r,
\qquad \mathbb E[q_rk_r]=0.
$$

又因 q/k 独立，

$$
\operatorname{Var}(q_rk_r)
=\mathbb E[q_r^2]\mathbb E[k_r^2]=1.
$$

所以

$$
\operatorname{Var}(q^\top k)
=\sum_{r=1}^{d_k}\operatorname{Var}(q_rk_r)=d_k,
$$

而

$$
\operatorname{Var}\!\left(\frac{q^\top k}{\sqrt{d_k}}\right)=1.
$$

缩放把“典型初始化假设下随维度增长的 logit 标准差”拉回 $O(1)$，减轻 softmax 过早饱和。

> [!warning] 这不是无条件定理
> 若坐标相关、均值非零、方差不等、重尾，或训练后 Q/K 范数漂移，上述等式不再原样成立。一般式还含协方差项。工程上应实际测量每层/每头 logit mean、std、max 与 entropy，而不是把 $1/\sqrt{d_k}$ 当永久尺度保证。

## 三、Softmax 是逐行的条件分布

对第 $i$ 行 logits $z_i\in\mathbb R^{T_k}$，

$$
a_{ij}=\frac{e^{z_{ij}}}{\sum_{\ell\in\mathcal V(i)}e^{z_{i\ell}}},
$$

其中 $\mathcal V(i)$ 是 query $i$ 可见的 keys。对每一行，$a_{ij}>0$ 且和为 1。不同 query 的行互不竞争；若沿列归一化，就改变成“每个 key 在 queries 间分配质量”的另一种算子。

Softmax 还是 LogSumExp 的梯度：

$$
\operatorname{LSE}(z)=\log\sum_j e^{z_j},\qquad
\frac{\partial\operatorname{LSE}}{\partial z_j}=\operatorname{softmax}(z)_j.
$$

其 Jacobian 为

$$
J=\operatorname{Diag}(a)-aa^\top.
$$

因此 $J\mathbf 1=0$，对应平移不变性；当 $a$ 极接近 one-hot 时，多数方向的梯度会很小。

## 四、稳定 Softmax 的精确推导

对任意常数 $c$，

$$
\frac{e^{z_j+c}}{\sum_\ell e^{z_\ell+c}}
=\frac{e^ce^{z_j}}{e^c\sum_\ell e^{z_\ell}}
=\operatorname{softmax}(z)_j.
$$

取 $c=-m$，$m=\max_j z_j$，得到

$$
\operatorname{softmax}(z)_j
=\frac{e^{z_j-m}}{\sum_\ell e^{z_\ell-m}}.
$$

所有指数输入不大于 0，最大项恰为 0，避免 $e^{1000}$ 溢出。对 $(1000,1001,999)$，先变成 $(-1,0,-2)$，结果约为 $(0.245,0.665,0.090)$。

减最大值不改变精确数学结果；浮点下仍可能有很小项下溢到 0，但这通常比整体溢出安全得多。

## 五、温度、尺度与熵

写成

$$
a(\tau)=\operatorname{softmax}(z/\tau),\qquad \tau>0.
$$

- $\tau\to0^+$：若最大值唯一，趋向 one-hot；
- $\tau\to\infty$：趋向均匀分布；
- 乘大 Q/K norm 与减小温度有相似的 logit 放大效果；
- 归一化 Q/K 会移除 norm 通道，但也改变可表达相似度。

[[S-2023-Su-9859-KeyNorm长度外推]] 把 key normalization 与长度外推联系起来。课程采用“norm 会改变 logit 尺度”这个恒等事实；文中的小模型外推改进仅作 `E` 级线索，不视为 scale-up 保证。

## 六、Mask、负无穷与全遮蔽行

数学上，把禁止 logit 设为 $-\infty$，其指数为 0。实际 kernel 常用 boolean mask 或 dtype 可表示的大负数；例如 `-1e9` 并非所有低精度下都具有相同语义。

若一整行都被禁止，则形式上出现

$$
\frac{0}{0},
$$

softmax 未定义。实现必须选择合同：报错、输出全零、跳过 query，或由上游保证永不发生。不能让 NaN 悄悄传播。

## 七、Taylor 展开能做什么

[[S-2026-Su-11814-LSE-Softmax-Taylor]] 提醒我们可从 LSE 的局部展开及梯度关系得到 softmax 近似。严格写法必须包含展开点 $z_0$：

$$
\operatorname{softmax}(z)
\approx a_0+J_0(z-z_0)+\cdots.
$$

低阶截断只在局部可靠，而且一般不自动保持非负、行和 1、平移不变或大 logit 差下的稳定性。将它用于 Attention 还要检查 mask 与输出误差，不能因“有 Taylor 展开”便声称获得全域线性 Attention。

## 八、数值与统计诊断表

至少按 layer/head/sequence length 记录：

| 环节 | 统计量 | 可能问题 |
|---|---|---|
| Q/K | norm、mean、std、异常值 | 尺度漂移、重尾、归一化偏差 |
| logits | mean/std/max-min、finite ratio | 饱和、overflow、mask 泄漏 |
| weights | entropy、max、top-k mass、row sum | 过尖/过平、全遮蔽、错误归一化轴 |
| output | norm、finite ratio、梯度 norm | denominator/混合放大、NaN 传播 |

## 九、图：方差、稳定化与语义

先看图回答：减去最大值与除以 $\sqrt{d_k}$ 哪一个改变精确 attention 分布？为什么全遮蔽行不属于普通 softmax 情形？

![[00-知识库管理/_assets/figures/architecture/fig-attention-scaled-softmax-ledger-v1.svg|900]]

> [!figure] 图 40.4-02　Scaled dot product 与稳定 row-softmax
> 左栏给出条件化方差账，中栏完整手算稳定 softmax，右栏列出概率与数值语义。来源：依据 Transformer 定义、LSE/softmax 恒等式独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_attention_v1.py]] 生成。

**怎样读图**：先检查左栏每条独立/中心化假设，再沿中栏执行“减最大值—指数—归一化”，最后把右栏的平移不变、行归一、温度敏感和全遮蔽例外逐项映射到实现测试。

**图没有证明什么**：它没有证明训练后 logits 仍方差为 1，没有证明标准缩放对所有分布最优，也没有给出任意 Taylor 截断的全域误差保证。

## 十、常见错误

1. 把 $\sqrt{d_k}$ 写成 $\sqrt{d_{model}}$ 而不检查每头维度；
2. 不写独立/中心化条件就宣称 $\operatorname{Var}(q^\top k)=d_k$；
3. 对整个 score tensor 一次 softmax；
4. 直接计算 `exp(large_logits)`；
5. 用有限大负数却不检查 dtype/kernel；
6. 假定全遮蔽行会自然输出全零；
7. 把更低 entropy 当作更准确或更可解释；
8. 把局部 Taylor 展开写成全域等价。

## 十一、掌握标准

> [!summary]
> - scaled attention 的核心是 $\operatorname{softmax}_{row}(QK^\top/\sqrt{d_k}+M)V$；
> - $1/\sqrt{d_k}$ 的理由来自写明假设的方差推导；
> - 减行最大值是保持 softmax 精确值的稳定化；
> - 温度、norm、mask、全遮蔽与 dtype 都属于数值语义合同。

能手算稳定 softmax（A/B）、推导方差与 Jacobian（C）、构造相关坐标反例和全遮蔽测试（D），并完成一份真实 attention logit/weight audit（E）。

## 十二、练习与独立详解

- [[习题 - Scaled Dot-Product Attention 与 Softmax 数值语义]]
- [[解答 - Scaled Dot-Product Attention 与 Softmax 数值语义]]

## 参考来源

- [[S-2017-Vaswani-Transformer复杂度]]
- [[S-2026-Su-11814-LSE-Softmax-Taylor]]
- [[S-2023-Su-9859-KeyNorm长度外推]]
- [[S-2021-Su-8620-Transformer初始化参数化与标准化]]

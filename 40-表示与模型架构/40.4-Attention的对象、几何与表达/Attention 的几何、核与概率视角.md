---
type: concept
status: draft
area: [architecture, attention, geometry, kernels, probability]
aliases: [Attention Geometry, Softmax Kernel, Linear Attention]
node_id: ARCH-30
prerequisites: ["[[Scaled Dot-Product Attention 与 Softmax 数值语义]]", "[[正定核、RKHS 与表示定理]]", "[[条件概率、全概率与 Bayes 公式]]", "[[内积空间]]"]
related: ["[[Attention 的对象、几何与表达 MOC]]", "[[Attention 矩阵的秩、瓶颈与有效秩]]", "[[Attention 失效模式、反例与证据地图]]"]
sources: ["[[S-2021-Choromanski-Performer]]", "[[S-2021-Su-8338-Performer到线性Attention]]", "[[S-2021-Su-8601-无限维线性Attention与核特征]]", "[[S-2023-Su-9889-Attention集中性]]", "[[S-2026-Su-11814-LSE-Softmax-Taylor]]"]
exercises: ["[[习题 - Attention 的几何、核与概率视角]]"]
solutions: ["[[解答 - Attention 的几何、核与概率视角]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-attention-geometry-kernel-probability-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Attention 的几何、核与概率视角

> [!abstract] 本节主问题
> 同一个 attention row 可以同时读成：向量空间中的匹配几何、指数 dot-product kernel 的 normalized weighted sum、可见位置上的 categorical distribution。三种视角解释不同层面；任何一种都不能自动推出权重是因果解释或线性化近似无损。

## 一、几何视角：Dot Product 混合角度与范数

对非零 $q,k$，

$$
q^\top k=\|q\|_2\|k\|_2\cos\theta.
$$

因此 dot-product score 同时利用：

- 方向对齐 $\cos\theta$；
- query norm；
- key norm。

两对向量角度相同，norm 更大的 pair 得更大 logit。若先 L2 normalize，则变成 cosine score，移除 norm 通道；这可能稳定尺度，也可能删除模型本来想表达的置信/显著程度。

Scaled dot product

$$
s(q,k)=\frac{q^\top k}{\sqrt{d_k}}
$$

可视为指定 temperature 的几何匹配。训练会同时改变方向与 norm，所以只画二维夹角不能完整描述真实高维 score。

## 二、双线性几何与投影

若从原表示 $x_i,x_j$ 投影，

$$
q_i=x_iW_Q,\qquad k_j=x_jW_K,
$$

则

$$
q_i k_j^\top=x_iW_QW_K^\top x_j^\top.
$$

令 $B=W_QW_K^\top$，attention 学到的是一般双线性匹配 $x_iBx_j^\top$。$B$ 不必对称或半正定，因此“距离”只是直觉称呼；交换 $i,j$ 后 score 一般不同。

每个 head 有不同 $B_r$，这就是“不同投影子空间”较精确的代数含义。

## 三、概率视角：对可见位置的条件分布

固定 query $i$ 与可见 keys，

$$
a_{ij}=p(J=j\mid q_i,K,\mathcal V(i))
$$

是位置索引 $J$ 上的 categorical distribution。输出是 value 随机变量的条件期望形式：

$$
o_i=\mathbb E_{J\sim a_i}[v_J].
$$

这让 entropy、KL、top-k mass 等工具可用于描述分布。但概率语义只说“模型将读取质量分给位置”，不是“位置 $j$ 为真的概率”，更不是该位置对最终预测的因果贡献。

## 四、集中性指标不止一个

对 $T$ 个可见位置的 row $a$：

| 指标 | 公式 | 端点解释 |
|---|---|---|
| 最大权重 | $\max_j a_j$ | one-hot 为 1，均匀为 $1/T$ |
| Top-k mass | $\sum_{j\in\operatorname{Top}k}a_j$ | 前 k 项承载多少质量 |
| Shannon entropy | $H(a)=-\sum a_j\log a_j$ | one-hot 0，均匀 $\log T$ |
| Effective support | $e^{H(a)}$ | 直观“有效位置数” |
| Collision concentration | $\sum a_j^2$ | 均匀 $1/T$，one-hot 1 |

[[S-2023-Su-9889-Attention集中性]] 的价值是把“真的集中吗”变成分布假设下的量化问题。不同长度的 raw entropy 不宜直接比较，可用 $H/\log T$ 或 effective support ratio，但仍要说明 mask 后可见数。

集中不等于好：复制、平均或全局统计任务可能需要平权；尖锐权重也可能锁定 shortcut。

## 五、指数 Dot Product 是正定核

对同一 feature space，

$$
K(q,k)=e^{q^\top k}
=\sum_{n=0}^{\infty}\frac{(q^\top k)^n}{n!}.
$$

由 tensor power 恒等式

$$
(q^\top k)^n=\langle q^{\otimes n},k^{\otimes n}\rangle,
$$

可定义无限维 feature map

$$
\phi(q)=\left(1,q,\frac{q^{\otimes2}}{\sqrt{2!}},\ldots\right),
$$

使

$$
e^{q^\top k}=\langle\phi(q),\phi(k)\rangle.
$$

这给出 PSD kernel 解释。scaled score 只需把输入按适当尺度变换。[[S-2021-Su-8601-无限维线性Attention与核特征]] 用这一展开连接 softmax attention 与无限 feature。

> [!warning] 非对称 Feature Pair 不自动是 PSD Kernel
> 一般线性 attention 可写 $\phi(q)^\top\varphi(k)$。若 $\phi\ne\varphi$ 或 q/k 属不同空间，它仍可作 affinity factorization，但不一定形成对称 PSD Gram kernel。不要把所有“核技巧”都当 RKHS kernel 定理。

## 六、从核到 Linear Attention

忽略 mask，normalized kernel attention 为

$$
o_i=\frac{\sum_j K(q_i,k_j)v_j}{\sum_j K(q_i,k_j)}.
$$

若

$$
K(q,k)\approx\phi(q)^\top\varphi(k),\quad \phi,\varphi\in\mathbb R^r,
$$

则

$$
o_i\approx
\frac{\phi(q_i)^\top\left(\sum_j\varphi(k_j)v_j^\top\right)}
{\phi(q_i)^\top\left(\sum_j\varphi(k_j)\right)}.
$$

先算

$$
S_V=\sum_j\varphi(k_j)v_j^\top\in\mathbb R^{r\times d_v},\qquad
s_1=\sum_j\varphi(k_j)\in\mathbb R^r,
$$

再逐 query 读取，避免显式 $T_qT_k$ 矩阵。[[S-2021-Su-8338-Performer到线性Attention]] 清晰展示这条结合律主线；正式随机特征性质由 [[S-2021-Choromanski-Performer]] 承担。

## 七、复杂度降低以什么为代价

若 $T_q=T_k=T$，feature width 为 $r$，主项可由 $O(T^2d)$ 改为约 $O(Trd)$。但完整账还含：

- feature map 成本；
- $r$ 为达到精度所需的增长；
- causal prefix state；
- denominator 与 epsilon；
- mask 是否可 factorize；
- random feature variance；
- backward、dtype 与 kernel wall-clock。

因此“linear”是对 token length 的渐近结构描述，不是无条件 wall-clock 结论。

## 八、Normalized Output 的误差为何更难

记 exact numerator/denominator 为 $n,d>0$，近似为 $\hat n,\hat d>0$。则

$$
\frac{\hat n}{\hat d}-\frac nd
=\frac{\hat n-n}{\hat d}
+n\left(\frac1{\hat d}-\frac1d\right).
$$

因此

$$
\left\|\frac{\hat n}{\hat d}-\frac nd\right\|
\le \frac{\|\hat n-n\|}{\hat d}
+\frac{\|n\|\,|\hat d-d|}{{d\hat d}}.
$$

即使 kernel entry error 小，若 $d$ 或 $\hat d$ 很小，输出误差会被放大。近似 affinity 不能单独保证 normalized attention output。

## 九、Causal Linear Attention

对 causal 情形，query $i$ 只看 $j\le i$，可维护前缀状态

$$
S_{V,i}=S_{V,i-1}+\varphi(k_i)v_i^\top,\qquad
s_{1,i}=s_{1,i-1}+\varphi(k_i).
$$

然后用 $\phi(q_i)$ 读取。这给递推/parallel scan 接口，但有限精度累积误差、state size、reset/segment mask 与反向传播都成为新问题。任意稀疏/结构 mask 未必能用一个前缀统计表示。

## 十、Taylor 与随机特征的边界

[[S-2026-Su-11814-LSE-Softmax-Taylor]] 提供 softmax/LSE 局部展开入口；[[S-2021-Choromanski-Performer]] 使用专门的正随机特征近似指数 kernel。二者不能混为“同一个近似”：

- Taylor 截断是确定性局部多项式近似，feature 数可快速增长；
- 随机特征提供随机估计与概率误差性质；
- 正特征有助于 denominator 语义；
- 两者都需把 kernel error 传播到 normalized output。

## 十一、图：三种视角

先看图回答：若只归一化 q/k，图中哪条信息通道被删除？为什么核近似误差还必须检查 denominator？

![[00-知识库管理/_assets/figures/architecture/fig-attention-geometry-kernel-probability-v1.svg|900]]

> [!figure] 图 40.4-06　Attention 的几何、核与概率三视角
> 左栏分解 dot product 的角度与范数，中栏给出指数 kernel 的 feature 展开，右栏把一行权重画成可见位置分布。来源：依据核展开、normalized attention 与概率单纯形独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_attention_v1.py]] 生成。

**怎样读图**：从左到右依次问“logit 如何形成”“pairwise kernel 如何 factorize”“归一后读出什么”。把 convex hull、feature approximation 和 concentration 分别登记，不用一个热力图替代全部分析。

**图没有证明什么**：它没有证明 attention weights 是真实后验或因果解释，没有证明有限 feature 全域精确，也没有证明 linear attention 在所有长度与硬件更快。

## 十二、常见错误

1. 把 dot product 当纯 cosine，相忘 norm；
2. 把一般双线性 score 称为距离；
3. 把位置权重解释成“为真概率”；
4. 把尖锐/低 entropy 当准确或可解释；
5. 看到 $\phi(q)^\top\varphi(k)$ 就宣称 PSD kernel；
6. 只近似 numerator，忽略 denominator；
7. 把 arbitrary mask 当作 prefix-sum 可处理；
8. 用 $O(T)$ 替代 feature width、constant 与 wall-clock；
9. 把 Taylor 与随机特征误差混写。

## 十三、掌握标准

> [!summary]
> - dot-product 同时编码角度和 norm，投影后形成可非对称双线性几何；
> - 每行 attention 是可见位置分布，输出是 value 的加权期望/凸组合；
> - 指数 dot-product 可写成无限维 feature inner product；
> - 有限 feature factorization 可线性化 token 计算，但 numerator、denominator、mask 与系统成本均需审计。

能比较几何/概率指标（A/B）、推导指数 feature map 与误差分解（C）、构造小 denominator 和非 PSD pairing 反例（D），并设计 exact-vs-linear attention 全链路实验（E）。

## 十四、练习与独立详解

- [[习题 - Attention 的几何、核与概率视角]]
- [[解答 - Attention 的几何、核与概率视角]]

## 参考来源

- [[S-2021-Choromanski-Performer]]
- [[S-2021-Su-8338-Performer到线性Attention]]
- [[S-2021-Su-8601-无限维线性Attention与核特征]]
- [[S-2023-Su-9889-Attention集中性]]
- [[S-2026-Su-11814-LSE-Softmax-Taylor]]

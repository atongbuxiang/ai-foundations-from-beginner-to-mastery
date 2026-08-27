---
type: concept
status: draft
area: [architecture, positional-encoding, rope, group-representation]
aliases: [Rotary Position Embedding, RoPE, Rotary Embedding]
node_id: ARCH-45
prerequisites: ["[[Sinusoidal 位置编码、频率与相对位移]]", "[[Multi-Head Attention、投影子空间与参数量]]", "[[Lie 群、Lie 代数与对称性]]"]
related: ["[[位置编码、结构编码与长度外推 MOC]]", "[[二维、多轴与多模态位置编码]]", "[[长度外推、位置插值与 RoPE 缩放]]", "[[相对位置表示、偏置与距离函数]]"]
sources: ["[[S-2021-Su-RoFormer]]", "[[S-2021-Su-8265-RoPE]]", "[[S-2022-Su-9403-RoPE完备性]]", "[[S-2021-Su-8397-二维RoPE与旋转表示]]"]
exercises: ["[[习题 - RoPE 的旋转推导、群表示与内积]]"]
solutions: ["[[解答 - RoPE 的旋转推导、群表示与内积]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-rope-rotation-relative-inner-product-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# RoPE 的旋转推导、群表示与内积

> [!abstract] 本节主问题
> RoPE 不把 position vector 加进 residual stream，而是对 attention 的 Q/K 成对通道施加位置相关正交旋转。两个绝对旋转在 dot product 中合并为一个只依相对位移的旋转；这条代数恒等式是 RoPE 的核心，长度外推与效果不是它的直接推论。

## 一、从设计目标写函数方程

希望 query $q_m$ 与 key $k_n$ 的位置化映射 $f_q,f_k$ 满足

$$
\langle f_q(q_m,m),f_k(k_n,n)\rangle
=g(q_m,k_n,n-m),
$$

即 score 的位置部分只依相对位移。选择

$$
f_q(q,m)=R_mq,\qquad
f_k(k,n)=R_nk,
$$

其中 $R_n$ 为正交矩阵，并要求

$$
R_m^\top R_n=R_{n-m}.
$$

则

$$
(R_mq_m)^\top(R_nk_n)
=q_m^\top R_m^\top R_nk_n
=q_m^\top R_{n-m}k_n.
$$

设计目标被精确满足。

## 二、二维旋转块

标准 RoPE 对每对通道使用

$$
R_i(n)=
\begin{bmatrix}
\cos(n\omega_i)&-\sin(n\omega_i)\\
\sin(n\omega_i)&\cos(n\omega_i)
\end{bmatrix}.
$$

完整旋转

$$
R_n=R_0(n)\oplus R_1(n)\oplus\cdots\oplus R_{d_r/2-1}(n),
$$

其中 $d_r$ 是被旋转的维数，可能等于整个 head dimension，也可能只旋转一部分。

每块满足

$$
R_i(m)^\top R_i(n)=R_i(n-m),
$$

所以 block diagonal 整体也满足。

## 三、复数写法

把通道对 $(x_{2i},x_{2i+1})$ 视为复数

$$
z_i=x_{2i}+\mathrm i x_{2i+1}.
$$

RoPE 等价于

$$
z_i\mapsto z_i e^{\mathrm i n\omega_i}.
$$

Query 与 key 的 Hermitian-style 实部配对产生相位差

$$
e^{-\mathrm i m\omega_i}e^{\mathrm i n\omega_i}
=e^{\mathrm i(n-m)\omega_i}.
$$

复数只是紧凑表示；真实实现仍用实数 sin/cos 和通道旋转。

## 四、群表示观点

整数位置形成加法群 $(\mathbb Z,+)$。映射

$$
n\mapsto R_n
$$

若满足

$$
R_{m+n}=R_mR_n,\qquad R_0=I,
$$

就是一个正交表示。于是

$$
R_n=R_1^n.
$$

[[S-2022-Su-9403-RoPE完备性]] 讨论更一般的正交 $R_1$。在实数正交基下，它可分解为二维旋转块以及可能的 $1$ 或 $-1$ 块；标准 RoPE 选择多个二维旋转及固定频率。

这里“完备性”只针对满足所列群/正交/有限维条件的构造。内容依赖、非正交、非平稳或轴间不交换的 position operator 不在该类中。

## 五、矩阵指数观点

二维 skew-symmetric generator

$$
J=
\begin{bmatrix}
0&-1\\
1&0
\end{bmatrix},
\qquad J^\top=-J
$$

满足

$$
R_i(n)=e^{n\omega_iJ}.
$$

因为同一 generator 的指数可加，

$$
e^{-m\omega_iJ}e^{n\omega_iJ}
=e^{(n-m)\omega_iJ}.
$$

这为连续位置、二维/多轴 commuting generators 提供桥梁。

## 六、RoPE 保持什么

正交性给出

$$
\|R_nx\|_2=\|x\|_2,
$$

以及同位置配对的内积保持：

$$
(R_nq)^\top(R_nk)=q^\top k.
$$

但不同位置的 score 会由 $R_{n-m}$ 改变。RoPE 不向 Q/K norm 写入绝对位置尺度，而把位置作用放在方向/相位上。

这不表示 softmax attention norm、entropy 或 output不变；相对旋转改变 logits，后续归一化会改变。

## 七、逐通道展开

对一对通道 $q=(q_1,q_2)$、$k=(k_1,k_2)$，令 $\phi=(n-m)\omega$：

$$
q^\top R(\phi)k
=(q_1k_1+q_2k_2)\cos\phi
+(q_2k_1-q_1k_2)\sin\phi.
$$

因此 score 同时含：

- content 的同向配对乘 $\cos\phi$；
- 二维有向面积/交叉配对乘 $\sin\phi$。

RoPE 不是简单“给原 score 乘一个余弦”；第二项一般不为零。

## 八、为什么“远程衰减”不是逐点定理

多频 score 是多个 $\cos(\omega_i\Delta)$ 与 $\sin(\omega_i\Delta)$ 调制项之和。它们会振荡，特定 Q/K 可在远距离重新对齐。

论文或博客中的平均衰减分析通常需要：

- Q/K 分量分布；
- 独立性或随机方向；
- 频率积分/平均；
- 维度和 base；
- 对内容相似性的统计模型。

所以“平均趋势”可为 T/H，“每个 token pair 随距离单调下降”一般不成立。

## 九、实现：rotate-half 只是某种布局

常见 interleaved 配对：

$$
\operatorname{rotate}(x_0,x_1,x_2,x_3)
=(-x_1,x_0,-x_3,x_2).
$$

再写

$$
\operatorname{RoPE}(x)
=x\odot\cos\theta
+\operatorname{rotate}(x)\odot\sin\theta.
$$

另一类 half-split 配对将前半与后半通道成对。两种 permutation-equivalent，但若 checkpoint 权重/频率 cache 的布局不一致，结果完全不同。

实现合同包括：

- rotary dimension 必须为偶数；
- Q/K head dimension及 GQA heads 广播；
- interleaved/half-split；
- position ID 与 cache offset；
- partial rotary 后未旋转通道怎样拼回；
- sin/cos cache dtype/device；
- scaling 在生成 cache 前后应用的位置。

## 十、KV Cache 等价性

历史 key 在写入 cache 前通常已经按其 absolute position 旋转。新 query 按新 position 旋转，然后直接与 cached keys点积：

$$
(R_tq_t)^\top(R_jk_j)
=q_t^\top R_{j-t}k_j.
$$

若后来改变 RoPE scaling/base，旧 cache 的旋转合同也改变；不能把按旧 scheme 旋转的 keys 与新 query混用。请求级 scheme必须固定，或重算 cache。

## 十一、二维推广入口

若位置为 $(r,c)$，可把通道分成两组：

$$
R_{(r,c)}=R^{row}_r\oplus R^{col}_c.
$$

内积分别依 $\Delta r,\Delta c$。也可用 commuting generators

$$
R(r,c)=e^{rA+cB},
\qquad AB=BA,\quad A^\top=-A,\ B^\top=-B.
$$

[[S-2021-Su-8397-二维RoPE与旋转表示]] 提供这一推广的中文推导接口；详细坐标合同放到 ARCH-46。

## 十二、图：从绝对旋转到相对内积

先看图回答：为什么必须同时对 Q 与 K 旋转，才能在 dot product 中出现 $R_m^\top R_n$？右栏哪四条结论不能由正交恒等式推出？

![[00-知识库管理/_assets/figures/architecture/fig-rope-rotation-relative-inner-product-v1.svg|900]]

> [!figure] 图 40.6-05　RoPE 的 Q/K 旋转、群表示恒等式与证据边界
> 左栏展示两次绝对旋转，中栏给出 $R_m^\top R_n=R_{n-m}$、相对内积与 norm 保持，右栏列出不被代数证明覆盖的性能命题。来源：依据 RoFormer 与正交表示独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_position_v1.py]] 生成。

**怎样读图**：沿左栏分别给 q、k 标 absolute positions，再在中栏把左侧旋转转置；群同态让两次变换相消为相位差。最后逐条检查右栏是否额外需要训练/数据/任务证据。

**图没有证明什么**：它不证明 attention随距离单调衰减、默认频率最优、训练范围外相位能被解释，或 advertised context 能被可靠利用。

## 十三、常见错误与掌握标准

常见错误：只旋转 Q 却声称纯相对；把 $R_m^\top R_n$ 符号写反；认为 RoPE 是原 dot product乘 $\cos$；配对布局错；partial rotary 维数不偶；cached keys 的 position/scaling与新 queries不一致；把“NTK-aware”名称当 NTK theorem；用正交 norm保持证明 softmax/长程性能。

> [!summary]
> RoPE 用整数平移的正交表示旋转 Q/K，使 $(R_mq)^\top(R_nk)=q^\top R_{n-m}k$。标准实现是多频二维旋转块，可用复数和矩阵指数表达；正交性保 norm，但不保证衰减、学习或外推。Pair layout、partial dimension、offset 与 cache scheme 都是语义合同。

能逐块推导相对内积（A/B）、解释表示/生成元与 cache（C）、构造远距振荡/布局反例（D），并为 RoPE kernel写 full-vs-cache数值验收（E）。

## 十四、练习与独立详解

- [[习题 - RoPE 的旋转推导、群表示与内积]]
- [[解答 - RoPE 的旋转推导、群表示与内积]]

## 参考来源

- [[S-2021-Su-RoFormer]]
- [[S-2021-Su-8265-RoPE]]
- [[S-2022-Su-9403-RoPE完备性]]
- [[S-2021-Su-8397-二维RoPE与旋转表示]]

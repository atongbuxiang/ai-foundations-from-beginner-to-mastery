---
type: concept
status: draft
area: [architecture, attention, content-addressing]
aliases: [QKV, Content-Addressable Attention, 内容寻址注意力]
node_id: ARCH-25
prerequisites: ["[[稳定求和、点积与矩阵乘法]]", "[[Softmax 输出层、Logit 尺度与概率参数化]]", "[[序列因果性、隐藏状态与递推计算]]"]
related: ["[[Attention 的对象、几何与表达 MOC]]", "[[Scaled Dot-Product Attention 与 Softmax 数值语义]]", "[[Self-Attention、Cross-Attention 与张量形状]]"]
sources: ["[[S-2015-Bahdanau-Attention]]", "[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2020-Su-7546-线性Attention]]"]
exercises: ["[[习题 - 内容寻址、Query、Key 与 Value]]"]
solutions: ["[[解答 - 内容寻址、Query、Key 与 Value]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-attention-qkv-content-addressing-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# 内容寻址、Query、Key 与 Value

> [!abstract] 本节主问题
> Attention 最根本的变化不是“让模型看得更远”，而是把读取规则从固定位置改成**由当前内容决定的软寻址**。Query、Key、Value 不是同一张量的三个别名：query 表达这次读取需要什么，key 表达每个候选怎样被匹配，value 表达匹配后真正返回什么。

## 一、从固定地址到内容地址

普通数组用整数地址读取：给定 $j$，返回 $v_j$。内容寻址则先给一个检索请求 $q$，再与每个地址描述 $k_j$ 比较：

$$
s_j=\operatorname{score}(q,k_j),\qquad
a_j=\operatorname{normalize}(s_1,\ldots,s_{T_k})_j,
$$

最后返回

$$
o=\sum_{j=1}^{T_k}a_jv_j.
$$

这是一个可微的“软读取”。如果 $a$ 接近 one-hot，它近似选中一项；如果较平，它混合多项。与最近邻的硬选择不同，soft attention 通常让所有可见候选都接收连续梯度。

[[S-2015-Bahdanau-Attention]] 的 encoder–decoder 对齐是这个问题的早期清晰原型：译码器不再只依赖单个固定源句向量，而是在每一步动态汇总源位置。

## 二、Q、K、V 的角色合同

| 对象 | 回答的问题 | 在单次读取中的角色 | 常见误解 |
|---|---|---|---|
| Query $q_i$ | “第 $i$ 次读取现在需要什么？” | 产生一整行匹配分数 | 等同当前 token 的全部内容 |
| Key $k_j$ | “第 $j$ 项怎样被检索？” | 与 query 共同决定地址权重 | 就是数据库里的 value |
| Value $v_j$ | “选中第 $j$ 项后返回什么？” | 被权重加和 | 也参与标准 dot-product 匹配 |

Q/K 必须位于可比较空间，通常都有维度 $d_k$；V 的内容维度可以另为 $d_v$。例如两本书的主题 key 很相似，但正文 value 可以完全不同；反之也可以让相同 value 配不同 key 以支持不同检索语义。

> [!important] 参数化不等于角色相同
> Self-attention 常从同一输入 $X$ 产生 $Q=XW_Q,K=XW_K,V=XW_V$，但 $W_Q,W_K,W_V$ 通常不同。它们共享**来源**，不共享**角色**，也不必共享表示子空间。

## 三、单 query 的完整手算

设三个分数为 $(\log 7,\log 2,0)$，用 softmax 得

$$
a=\frac{(7,2,1)}{7+2+1}=(0.7,0.2,0.1).
$$

若

$$
v_1=(1,0),\quad v_2=(0,2),\quad v_3=(-1,1),
$$

则

$$
o=0.7v_1+0.2v_2+0.1v_3=(0.6,0.5).
$$

请注意：改变 $v_2$ 不会改变这一轮已算出的权重，因为标准 score 只看 $q,k$；但会改变输出。改变 $k_2$ 会改变权重，并可能间接改变所有 value 的混合比例。

## 四、从一个 query 到矩阵公式

把 $T_q$ 个 query、$T_k$ 个 key/value 排成行：

$$
Q\in\mathbb R^{T_q\times d_k},\quad
K\in\mathbb R^{T_k\times d_k},\quad
V\in\mathbb R^{T_k\times d_v}.
$$

用 dot product score 时，

$$
S=QK^\top\in\mathbb R^{T_q\times T_k}.
$$

对 $S$ **逐行**归一化得到 $A$，再计算

$$
O=AV\in\mathbb R^{T_q\times d_v}.
$$

维度检查给出两个不可破坏的配对：Q/K 共享 $d_k$，A/V 共享 $T_k$。输出行数由 query 数决定，输出内容维度由 value 决定。

## 五、概率单纯形与凸包性质

如果每行 $a_{ij}\ge 0$ 且 $\sum_j a_{ij}=1$，那么 $a_i$ 位于概率单纯形，输出

$$
o_i=\sum_j a_{ij}v_j
$$

位于可见 values 的凸包。这意味着单层、单头、无输出投影的 normalized attention 不能把输出送到凸包外。

但完整 attention block 还有 $W_V,W_O$、residual、normalization 与 MLP，因此不能把单个 $AV$ 的凸包性质直接外推到整个 block 的最终表示。

## 六、Soft 与 hard retrieval 的差别

- **Hard argmax**：只取最大分数项；前向稀疏，但 argmax 对分数通常不可微；
- **Softmax**：所有有限 logit 对应严格正权重；温度决定集中程度；
- **Sparse normalization**：可能产生精确零，但梯度与支持集变化需单独分析；
- **Top-k routing/retrieval**：先离散筛选再归一，训练估计器、负载和召回成为新合同。

“soft”描述权重机制，不表示模型的结论含糊；“attention”也不保证权重一定尖锐。

## 七、Attention 能解决什么，不能自动解决什么

它提供的是一条短的内容依赖交互路径：每个 query 可直接组合所有可见 values。但它不自动保证：

1. query/key 学到了正确检索语义；
2. 有限维 dot product 能表达目标匹配函数；
3. 训练能找到所需参数；
4. 权重对人类而言可解释；
5. 长序列上计算和存储可承受；
6. 输出保留每个被混合项的身份。

因此“可见”不等于“可恢复”，“短路径”不等于“无信息瓶颈”。

## 八、Science Space 的理解桥

[[S-2020-Su-7546-线性Attention]] 从一般非负相似度 $\phi(q)^\top\varphi(k)$ 出发，特别适合帮助初学者看清：Attention 的骨架是“匹配—归一化—汇总”，softmax dot product 只是其中一个实例。不过，替换相似度会改变集中性、秩、误差和 mask 实现，不能只保留 Attention 这个名字就假定语义不变。

## 九、图：从检索角色到 shape

先看图回答：为什么 key 与 value 必须一一对应，却可以有不同维度？若新增一个 query，哪几个矩阵的行数会变化？

![[00-知识库管理/_assets/figures/architecture/fig-attention-qkv-content-addressing-v1.svg|900]]

> [!figure] 图 40.4-01　Q/K/V 的内容寻址合同
> 左栏用图书馆式检索区分请求、地址和内容，中栏展示单 query 的软读取，右栏给出矩阵 shape。来源：依据 Bahdanau attention 与 Transformer 定义独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_attention_v1.py]] 生成。

**怎样读图**：先沿左栏的三步问“谁决定匹配、谁被返回”，再在中栏确认同一个权重同时选中对应的 key/value 项，最后用右栏检查 $QK^\top$ 和 $AV$ 的 inner dimensions。

**图没有证明什么**：它没有证明模型必能学到正确寻址，没有证明权重是忠实解释，也没有证明 soft attention 比硬检索在所有任务更好。

## 十、常见错误

1. 把 Q/K/V 说成“输入复制三次”；
2. 让 K 有 $T_k$ 行、V 却有不同候选数；
3. 沿列而不是沿 key 维归一化；
4. 以为输出形状由 K 决定而不是由 Q 与 V 决定；
5. 把 attention weight 当 value 的语义标签；
6. 把凸组合性质外推到含 $W_O$、residual、MLP 的整个网络；
7. 用“可访问所有 token”替代训练和泛化证据。

## 十一、掌握标准

> [!summary]
> - Attention 是内容依赖的软寻址：Q 提需求、K 供地址、V 供返回内容；
> - $QK^\top$ 的形状为 $T_q\times T_k$，$AV$ 的形状为 $T_q\times d_v$；
> - normalized attention 输出是可见 values 的凸组合；
> - 对象定义、表示能力、可学习性、解释性与系统成本必须分开。

能完成单 query 手算（A/B）、无提示写出矩阵 shape（B）、证明凸包性质（C）、构造 Q/K/V 角色混淆反例（D），并把真实检索任务写成完整 addressing contract（E）。

## 十二、练习与独立详解

- [[习题 - 内容寻址、Query、Key 与 Value]]
- [[解答 - 内容寻址、Query、Key 与 Value]]

## 参考来源

- [[S-2015-Bahdanau-Attention]]
- [[S-2017-Vaswani-Transformer复杂度]]
- [[S-2020-Su-7546-线性Attention]]

---
type: methodology
status: verified
area: [training, scaling-laws, data, mixtures, repetition]
node_id: TRN-53
aliases: [Effective Tokens, Data Repetition Scaling, Data Mixture Scaling]
prerequisites: ["[[数据生成分布与采样假设]]", "[[联合分布、边缘分布与独立性]]", "[[Kaplan 参数数据律、联合拟合与有限区间]]"]
related: ["[[过训练、推理成本与多目标最优规模]]", "[[数据增强、不变性、等变性与任务充分性]]", "[[Scaling 实验设计、外推不确定性与证据地图]]"]
sources: ["[[S-2025-Muennighoff-Data-Constrained-Scaling]]", "[[S-2025-Ye-Data-Mixing-Laws]]", "[[S-2026-Su-11833-解构ScalingLaw]]"]
exercises: ["[[习题 - 数据质量、重复、混合与有效 Token]]"]
solutions: ["[[解答 - 数据质量、重复、混合与有效 Token]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-data-effective-token-mixture-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# 数据质量、重复、混合与有效 Token

> [!abstract] 一句话结论
> Seen tokens 是训练时钟，不是信息量。重复 token、近重复文档、高质量样本、跨域样本与目标分布匹配样本具有不同边际价值；“有效 Token”只有在指定模型、训练阶段、目标指标和数据操作后才有意义，不能成为跨项目通用汇率。

## 一、五种容易混写的数据量

| 记号 | 含义 |
|---|---|
| $D_{\rm raw}$ | 原始语料经 tokenizer 后的 tokens |
| $D_{\rm unique}$ | 去重定义下的 unique tokens/documents |
| $K$ | 训练实际消费的 seen tokens |
| $R=K/D_{\rm unique}$ | 平均 epoch/repetition count |
| $D_{\rm eff}$ | 针对给定目标定义的等效信息量或等效 unique-token 数 |

$D_{\rm eff}$ 不是直接观测量；它通常由“达到相同 loss 需要多少基准数据”反推。因此必须写成

$$
D_{\rm eff}
=D_{\rm eff}(
\text{model, optimizer, stage, data operation, target metric}
).
\tag{1}
$$

若脱离这些条件说“1 个高质量 token 等于 5 个普通 token”，就失去了可验证语义。

## 二、重复数据的最小边际价值模型

设 $D_u$ 个 unique tokens 被训练 $R$ 遍。第 $r$ 遍的相对边际价值为 $w_r$，其中

$$
w_1=1,\qquad
1\ge w_2\ge\cdots\ge0.
\tag{2}
$$

定义教学用有效量

$$
D_{\rm eff}(R)
=D_u\sum_{r=1}^{R}w_r.
\tag{3}
$$

若取几何衰减

$$
w_r=\rho^{r-1},\qquad0<\rho<1,
\tag{4}
$$

则

$$
D_{\rm eff}(R)
=D_u\frac{1-\rho^R}{1-\rho}.
\tag{5}
$$

而 seen tokens 是

$$
K=RD_u.
\tag{6}
$$

当 $R\to\infty$，$K$ 线性增长，但式 (5) 饱和。这只是可手算的 diminishing-return 模型，不是某篇论文的通用经验公式。

## 三、如何读数据约束实验

[[S-2025-Muennighoff-Data-Constrained-Scaling]] 在其大规模实验中发现：

- 固定 compute、unique data 受限时，少量重复仍可能有价值；
- 在论文设置内，最多约 4 epochs 的 loss 变化相对 unique data 很小；
- 更多重复后，额外 compute 的边际价值最终趋近零；
- excess parameters 和 repeated tokens 需进入新的 compute-optimal 经验模型。

正确使用方式：

> 在该数据、模型和 loss 窗口中，早期重复的边际价值尚高。

错误使用方式：

> 任意预训练数据重复四遍都等价于 unique data，且没有记忆或泛化风险。

## 四、重复的风险不只看 Validation Loss

即使平均 validation loss 暂时不变，还应审计：

- exact/near-duplicate memorization；
- benchmark contamination；
- rare sequence exposure count；
- train–validation domain overlap；
- privacy leakage；
- subgroup/domain performance；
- calibration 与生成多样性。

相同 $R$ 在“完全随机重复”“文档连续多 epoch”“curriculum 重放”“hard-example replay”中也不是同一个训练过程，因为 optimizer state 与 data order 不同。

## 五、数据质量不是一个无条件标量

过滤器给样本质量分数 $q(z)$，选高分数据可能：

- 降低噪声；
- 增加目标风格一致性；
- 删除稀有语言/领域；
- 放大过滤器偏见；
- 减少覆盖与多样性；
- 改变 evaluation distribution。

所以质量收益应写成对目标风险的边际效应：

$$
v(z)
=-\frac{\partial L_{\rm target}}{\partial\,\text{weight}(z)}.
\tag{7}
$$

$v(z)$ 依赖当前模型和训练状态；同一文档对小模型、已饱和大模型和特定下游任务可能具有不同价值。

## 六、Mixture 是 Simplex 上的向量

设有 $m$ 个数据域，训练 mixture 为

$$
\boldsymbol p=(p_1,\ldots,p_m),
\qquad
p_i\ge0,\quad\sum_i p_i=1.
\tag{8}
$$

目标评估权重为

$$
\boldsymbol q=(q_1,\ldots,q_m).
\tag{9}
$$

各 domain loss 为

$$
L_j(N,D,\boldsymbol p).
\tag{10}
$$

整体目标可写成

$$
L_{\rm target}
=\sum_{j=1}^{m}q_jL_j.
\tag{11}
$$

即使总 $D$ 相同，不同 $\boldsymbol p$ 会改变每个 $L_j$。[[S-2025-Ye-Data-Mixing-Laws]] 在特定预训练协议中拟合 mixture proportion 到 domain loss 的函数，再嵌套 step/model scaling 预测更大模型。

## 七、局部 Transfer Matrix

在当前 mixture $\boldsymbol p_0$ 附近，可定义

$$
M_{ji}
=-\frac{\partial L_j}{\partial D_i},
\tag{12}
$$

其中 $D_i=p_iD$。

- $M_{ii}$：同域 token 对本域 loss 的边际价值；
- $M_{ji},j\ne i$：跨域 transfer 或 interference；
- $M_{ji}>0$：增加域 $i$ 改善域 $j$；
- $M_{ji}<0$：可能有负迁移。

因此单一 $D_{\rm eff}$ 会丢掉矩阵结构。只有当各域边际作用近似成固定比例时，才可能压成一个标量。

## 八、Tokenization 也改变数据尺度

同一文本用不同 tokenizer 可产生不同 token 数。若一个 tokenizer 平均每 byte 产生更多 tokens：

- $D$ 增加不代表信息增加；
- context 中覆盖的字符范围减少；
- vocab projection 与 embedding 参数改变；
- per-token loss 不可直接比较。

跨 tokenizer 至少报告：

- bytes/characters/documents；
- tokens 与 fertility；
- loss 的 per-token 与 per-byte 版本；
- vocab size 与 compute；
- normalization/whitespace/code handling。

## 九、数据实验的公平合同

比较两种数据操作 A/B 时：

1. 固定 model family、optimizer 与 tokenizer，或明确它们是联合干预；
2. 分别匹配 seen tokens、model FLOPs 和 wall time，不能只挑一个；
3. 保存 unique/near-duplicate/contamination stats；
4. 报告 mixture vector 与 sampling temperature；
5. 用相同 validation suites 和 domain weights；
6. 做 multiple seeds 与 paired data-order 设计；
7. 把 mixture/quality 搜索 compute 计入 $C_{\rm tune}$；
8. 最大目标规模只在 recipe 锁定后确认。

## 十、科学空间三重分解的使用

[[S-2026-Su-11833-解构ScalingLaw]] 把数据 gap 与 optimization/architecture gap 分账，并提出数据量收益与 multi-epoch 代价的候选幂律。课程保留的问题是：

> unique data 增益与重复代价如何共同决定最优 $K(D)$？

但不预设两项严格可加、指数固定或每个 gap 非负；这些都必须由多 $D$、多 $R$ 和 held-out domains 实验验证。

## 十一、图：Seen Token 不是信息守恒

先看图回答：左栏为什么 repetition 继续增加时 seen tokens 仍线性增长、effective tokens 却饱和？右栏为什么优化 mixture 必须保留 domain-loss 向量？

![[00-知识库管理/_assets/figures/training-optimization/fig-data-effective-token-mixture-v1.svg|900]]

> [!figure] 图 TRN-53-01　Repeated-token marginal value 与 mixture simplex
> 来源：课程原创教材图；左栏用 $w_r$ 递减说明 repeated token 的边际价值；中栏分开 raw/unique/seen/effective；右栏把三域 mixture、target weights 与 transfer matrix 连接。概念依据：[[S-2025-Muennighoff-Data-Constrained-Scaling]]、[[S-2025-Ye-Data-Mixing-Laws]]。

**怎样读图**：先选数据计数单位，再定位重复轮次与边际权重；做 mixture 时逐域读 loss，不先压成单一总分。

**图没有证明什么**：几何衰减和三域 simplex 是教学模型，不提供真实语料的 $\rho$ 或最优比例；实际 transfer 可非线性且随规模改变。

## 十二、初学者自检

- 能否列出 raw、unique、seen、epoch、effective 五种量？
- 能否推导几何边际模型式 (5)，并说明它只是 toy law？
- 能否解释相同 token 数为何不等于相同 target risk？
- 能否在 mixture 优化中保留 domain vector、失败和 search compute？

只有四问都能回答，才有资格把 $D$ 放进 compute-optimal 公式。

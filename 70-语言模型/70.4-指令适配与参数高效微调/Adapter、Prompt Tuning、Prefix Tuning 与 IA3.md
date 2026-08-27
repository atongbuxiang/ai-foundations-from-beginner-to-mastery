---
type: concept
status: verified
area: [language-models, peft, adapters, prompt-tuning, prefix-tuning, ia3]
node_id: LM-31
aliases: [PEFT 方法比较, Soft prompt, IA3]
prerequisites: ["[[LoRA 的低秩更新、初始化、缩放与合并]]", "[[Transformer Block、残差、归一化与 FFN]]"]
related: ["[[QLoRA、量化基座与适配显存总账]]", "[[Prefix LM、UniLM 与序列到序列 Mask 合同]]"]
sources: ["[[S-2019-Houlsby-Adapters]]", "[[S-2021-Li-Prefix-Tuning]]", "[[S-2021-Lester-Prompt-Tuning]]", "[[S-2022-Liu-IA3]]", "[[S-2021-Hu-LoRA]]"]
exercises: ["[[习题 - Adapter、Prompt Tuning、Prefix Tuning 与 IA3]]"]
solutions: ["[[解答 - Adapter、Prompt Tuning、Prefix Tuning 与 IA3]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-adapt-peft-interface-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Adapter、Prompt Tuning、Prefix Tuning 与 IA3

> [!abstract] 一句话结论
> PEFT 不是同一技巧的不同名字：Adapter 插入残差模块，prompt tuning 增加输入 embeddings，prefix tuning 给多层 attention 加虚拟状态，IA3 缩放激活通道，LoRA 改写线性层增量。它们应按注入位置、状态量、额外 FLOPs、context/KV、mergeability 与任务服务比较。

## 一、统一视角：冻结基座，开放接口

设 frozen Transformer 为

$$
h_{\ell+1}=F_\ell(h_\ell;\theta_\ell),
\qquad \theta_\ell\ \text{fixed}.
$$

PEFT 引入少量 $\phi$：

$$
h_{\ell+1}=\widetilde F_\ell(h_\ell;\theta_\ell,\phi).
$$

关键不只是 $|\phi|$，而是 $\phi$ 进入哪里：

- 权重空间；
- residual branch；
- input sequence；
- per-layer attention state；
- activation channel scaling。

接口位置决定表达能力和系统成本。

## 二、Bottleneck Adapter

典型 residual adapter：

$$
\operatorname{Adapter}(h)
=h+W_{\text{up}}
\sigma(W_{\text{down}}h+b_d)+b_u,
$$

其中

$$
W_{\text{down}}\in\mathbb R^{r\times d},
\qquad
W_{\text{up}}\in\mathbb R^{d\times r}.
$$

忽略 bias，每个 adapter 参数约 $2dr$。若每层插两个、共 $L$ 层，则约 $4Ldr$。

特点：

- 不占输入 context；
- 每层增加额外 MLP FLOPs 和 latency；
- 可独立保存/切换；
- 通常不能像线性 LoRA 一样无条件 merge 到原非线性层；
- insertion point、pre/post norm 与 residual scale 必须版本化。

## 三、Prompt Tuning

学习 $p$ 个连续 embeddings：

$$
P\in\mathbb R^{p\times d},
$$

把模型输入从 $X$ 变为

$$
[P;X].
$$

参数量 $pd$，非常小。但虚拟 tokens：

- 占 context positions；
- 增加 prefill；
- 进入 attention，成本随总长度变化；
- 需与真实 position IDs、padding/packing 定义对齐；
- 可能影响 KV cache。

Prompt tuning 不是学习可读的离散文本；最近邻 token 解释通常不是严格语义解码。

## 四、Prefix Tuning

Prefix tuning 常为每层 attention 提供 $p$ 个虚拟 key/value states：

$$
K_\ell'=[K_{\ell,\text{prefix}};K_\ell],
\qquad
V_\ell'=[V_{\ell,\text{prefix}};V_\ell].
$$

直接存每层 K/V 时，状态量近似：

$$
P_{\text{prefix}}
\approx 2Lpd
$$

（多头 reshape 不改变总元素量）；也可用较小网络生成 prefix，参数账另算。

它与 prompt tuning 不同：

- prompt 只在输入层加 embeddings，后续状态由基座传播；
- prefix 可在每层直接注入 attention memory；
- prefix 的 per-layer KV 对 serving/cache 更直接；
- relation 必须保证哪些 queries 能看 prefix。

## 五、IA3：逐通道缩放激活

IA3 学习向量，对 attention K/V 或 FFN 激活做逐通道乘法。例如：

$$
K'=l_k\odot K,\qquad
V'=l_v\odot V,
$$

$$
h_{\text{ff}}'
=l_{\text{ff}}\odot h_{\text{ff}}.
$$

参数量是所缩放通道维度之和，通常远小于矩阵更新。它相当于可学习 gates，但：

- 缩放对象和 broadcast 轴必须明确；
- 初始化为 1 才保持 base function；
- 负值是否允许、正则和 dtype 会影响行为；
- 可否 fold 进相邻权重依架构、norm 与部署图。

“只学向量”不等于功能变化小；通道可控制大量下游 logits。

## 六、LoRA 放在统一图中

LoRA 对选定线性层：

$$
Wh\mapsto(W_0+sBA)h.
$$

它不占 context，且线性情形可 merge；未 merge 时增加小 matmuls。与 Adapter 的主要差别：

- Adapter 加新非线性 residual path；
- LoRA 限制原线性层增量 rank；
- 二者参数量相近时函数族仍不同。

## 七、参数量手算

设 $d=4096,L=32,p=20,r=8$，仅作 toy：

### Prompt

$$
pd=20\times4096=81{,}920.
$$

### Per-layer K/V prefix

$$
2Lpd
=2\times32\times20\times4096
=5{,}242{,}880.
$$

### 每层一个 adapter

$$
2Ldr
=2\times32\times4096\times8
=2{,}097{,}152.
$$

### 每层一个 $d\times d$ projection 的 LoRA

$$
Lr(d+d)
=32\times8\times8192
=2{,}097{,}152.
$$

数值相等不表示功能或成本相等：prefix 占 KV/context，adapter 有非线性 FLOPs，LoRA 可 merge。

## 八、服务与多任务视角

若一个 frozen base 服务 $K$ 个任务，需考虑：

| 方法 | 每任务持久状态 | 请求时额外状态 | 可否混任务 batch |
|---|---|---|---|
| Prompt | input embeddings | context/KV positions | 可，但每请求 prompt 不同 |
| Prefix | per-layer K/V 或生成器 | per-layer prefix KV | 可，需 cache/broadcast |
| Adapter | layer modules | extra activations | 动态路由实现决定 |
| IA3 | scaling vectors | channel gates | 相对轻量，kernel 决定 |
| LoRA | A/B 或 merged weight | extra matmuls或独立 merged model | 动态 LoRA kernel 决定 |

参数存储小不等于 serving 简单。Task switching、batch composition、cache invalidation 与 kernel 支持都可能主导延迟。

## 九、所谓“等价”通常只在受限条件下

- 线性 Adapter 若无 activation 且位置合适，可能折叠成某类低秩/全秩更新；含非线性则一般不等价；
- IA3 的 diagonal scaling 可在某些线性层中 fold，但 norm/residual/共享权重会改变；
- input prompt 经过网络产生每层状态，不等于可任意选择的 per-layer prefix；
- LoRA rank-$r$ 增量不等于 bottleneck-$r$ Adapter 的非线性函数；
- 相同参数量不等于相同可达 function class。

“它们都是 PEFT”只是共同预算标签，不是数学同构。

## 十、图解：注入位置决定系统合同

先看图回答：哪种方法消耗 context/KV，哪种能 merge，哪种增加每层非线性 FLOPs？

![[00-知识库管理/_assets/figures/language-models/fig-lm-adapt-peft-interface-v1.svg|900]]

> [!figure] 图 LM-31　五类 PEFT 的计算图注入位置
> 中央是 frozen block；左右分别标 Prompt、Prefix、Adapter、LoRA、IA3 接入 attention、FFN、residual 或输入状态的位置。
> **生成：**本图由本库依据本节定义、正文列出的一级来源和固定绘图脚本重新绘制；图中的小规模数值或结构用于教学，不复刻论文原图。

**怎样读图**：不要按框面积比较参数量；沿虚线找每种方法改写的 tensor，再列 persistent state、runtime state 和 merge path。

**图没有证明什么**：图不表示方法性能排名，不覆盖所有 Adapter/Prefix 变体，也不保证特定框架的 kernel 实现。

## 十一、公平实验矩阵

至少报告：

- 同 base/data/template/effective targets；
- trainable params 与 total saved bytes；
- optimizer/activation/peak memory；
- train and inference FLOPs、tokens/s、latency；
- context/KV overhead；
- task-switch 和 mixed-batch overhead；
- full/freeze/LoRA baselines；
- in-domain、OOD、old-task、安全与 calibration；
- 多 seed 与 hyperparameter search budget。

如果各方法默认 learning rate、rank、prompt length 和 target modules 不同，单点比较容易把调参质量当方法性质。

## 本节出口

你应能从计算图指出一种 PEFT 改的是输入、权重、模块、KV 还是通道，并分别计算参数、context、额外 FLOPs 与可合并性。最后一节研究多个适配结果怎样进入同一参数坐标：[[Model Soup、Task Arithmetic、TIES 与适配证据地图]]。

## 练习与独立解答

- [[习题 - Adapter、Prompt Tuning、Prefix Tuning 与 IA3]]
- [[解答 - Adapter、Prompt Tuning、Prefix Tuning 与 IA3]]

---
type: moc
status: active
area: [math/information-theory, math/statistical-learning, ai/probabilistic-modeling]
aliases: [信息论 MOC, Information Theory MOC]
prerequisites: ["[[概率论与数理统计 MOC]]", "[[期望、方差与矩]]", "[[联合分布、边缘分布与独立性]]"]
related: ["[[数学基础 MOC]]", "[[数学基础完整课程地图与掌握标准]]", "[[练习与测验 MOC]]", "[[推导与实验 MOC]]"]
sources: ["Shannon-1948-Mathematical-Theory-Communication", "Shannon-1959-Coding-Theorems-Fidelity-Criterion", "Kullback-Leibler-1951-Information-Sufficiency", "Jaynes-1957-Information-Theory-Statistical-Mechanics", "Csiszar-1967-f-Divergence", "Tishby-Pereira-Bialek-1999-Information-Bottleneck", "Alemi-et-al-2017-Deep-Variational-Information-Bottleneck", "Rissanen-1978-Modeling-Shortest-Data-Description", "Grunwald-2007-MDL", "Honkela-Valpola-2004-Bits-Back", "MIT-6.441-Information-Theory", "Stanford-EE376A-Information-Theory", "Cover-Thomas-Elements-Information-Theory", "Wainwright-Jordan-2008-Exponential-Families-Variational-Inference", "Blei-Kucukelbir-McAuliffe-2017-Variational-Inference", "Kingma-Welling-2014-AEVB", "Nowozin-Cseke-Tomioka-2016-fGAN", "Gretton-et-al-2012-MMD", "Arjovsky-Chintala-Bottou-2017-WGAN", "Su-3534-Entropy-Part-I", "Su-3552-Maximum-Entropy", "Su-3567-Maximum-Entropy-Model", "Su-6016-fGAN", "Su-6088-VAE-Prior-MI", "Su-6181-Variational-Coding-Information-Bottleneck", "Su-7695-Embedding-Dimension-Entropy", "Su-8244-WGAN-Distance", "Su-8791-VAE-Density"]
created: 2026-08-19
updated: 2026-08-19
---

# 信息论与统计学习接口 MOC

> [!abstract] 本卷的核心任务
> 把“惊讶、不确定性、依赖、分布失配与可压缩性”变成带条件、单位和操作含义的数学量。课程从离散自信息和平均码长出发，建立 joint/conditional entropy、cross-entropy、KL 与 mutual information；再用数据处理、典型集、最大熵、变分推断和率失真把它们接到语言模型、表示学习、生成模型与压缩。公式只有在随机对象、分布、对数底、支撑和归约尺度都写清时才有意义。

## 一、范围与边界

### 本卷包含

- 离散自信息、Shannon entropy、prefix code 与平均码长；
- 联合熵、条件熵、链式法则、互信息和数据处理不等式；
- cross-entropy、KL、$f$-divergence、Bregman divergence 与概率度量的区别；
- source coding、典型集、AEP、rate–distortion 和 MDL；
- 最大熵、指数族、变分推断、ELBO 与信息瓶颈；
- 语言模型 NLL/perplexity、分类交叉熵、蒸馏、VAE、对比学习和表示压缩中的严格接口。

### 本卷不替代

- 测度论信息论的完整课程：正文先在有限/可数字母表上闭合证明，再明确连续量和一般测度的扩展条件；
- 概率论基础：joint、conditional、expectation、LLN 与 MLE 见 10.5；
- 统计学习的一般化理论：Rademacher complexity、PAC-Bayes 等留到统计学习专题；
- 优化理论：能写出 cross-entropy 或 ELBO，不等于知道优化器会收敛；
- 因果推断：互信息描述统计依赖，不能自动推出因果方向；
- 任意“information”命名：Fisher information、attention score、feature importance 与 Shannon information 不是同一对象。

## 二、依赖总图

~~~mermaid
flowchart LR
    P["概率分布与期望"] --> I1["INFO-01 自信息 / 熵 / 码长"]
    P --> I2["INFO-02 联合 / 条件熵"]
    I1 --> I2
    I1 --> I3["INFO-03 Cross-entropy / KL"]
    I2 --> I4["INFO-04 互信息"]
    I3 --> I4
    I4 --> I5["INFO-05 数据处理 / 充分性"]
    I1 --> I6["INFO-06 编码 / 典型集 / AEP"]
    I3 --> I7["INFO-07 最大熵 / 指数族"]
    I3 --> I8["INFO-08 变分推断 / ELBO"]
    I4 --> I9["INFO-09 散度与概率度量"]
    I5 --> I10["INFO-10 率失真 / 信息瓶颈 / MDL"]
    I6 --> I10
    I8 --> I10
~~~

> [!note] 教学次序
> INFO-01—03 先把单变量、条件链与分布失配分开；INFO-04—06 再建立依赖、信息流和编码定理；INFO-07—10 才进入建模原则和现代 AI 接口。这样可以避免只会背“cross-entropy = loss”“KL = regularizer”，却说不清期望在哪个分布下取、为何非负、何时为无穷。

## 三、10 个核心节点

| ID | 节点 | 本章必须回答的问题 | 状态 |
|---|---|---|---|
| INFO-01 | [[自信息、熵与编码长度]] | 为什么罕见事件更“惊讶”，平均不确定性为何等于理想码长？ | draft |
| INFO-02 | [[联合熵、条件熵与链式法则]] | 多个随机变量的信息怎样拆分，序列 likelihood 为何可以逐 token 相加？ | draft |
| INFO-03 | [[交叉熵与 KL 散度]] | 用错误分布编码多付出多少代价，为什么 NLL 是经验 cross-entropy？ | draft |
| INFO-04 | [[互信息与依赖性]] | 一个变量减少另一个变量多少不确定性，零互信息何时等于独立？ | draft |
| INFO-05 | [[数据处理不等式与充分统计量]] | 后处理为何不能凭空增加信息，表示何时保留了任务所需信息？ | draft |
| INFO-06 | [[无损编码、典型集与渐近等分性]] | 长序列为何集中在约 $2^{nH}$ 个典型序列，压缩极限是什么？ | draft |
| INFO-07 | [[最大熵原理与指数族]] | 只知道约束时怎样选择最少额外假设的分布，何时得到指数族？ | draft |
| INFO-08 | [[变分推断、ELBO 与证据分解]] | 难算 evidence/posterior 如何变成可优化下界，gap 到底是什么？ | draft |
| INFO-09 | [[f-散度、Bregman 散度与概率度量]] | 不同差异量强调哪些区域，何时是 metric，样本估计会怎样失败？ | draft |
| INFO-10 | [[率失真、信息瓶颈与最小描述长度]] | 有损压缩、任务相关表示和模型复杂度怎样统一为信息约束？ | draft |

## 四、四阶段学习路线

### 阶段 A：信息量与分布失配

1. [[自信息、熵与编码长度]]；
2. [[联合熵、条件熵与链式法则]]；
3. [[交叉熵与 KL 散度]]。

阶段验收：能从可加性推出对数自信息；能证明 entropy bounds、chain rule 和 Gibbs inequality；能从 logits 稳定推导 categorical cross-entropy，并审计 support、log base、sum/mean 与 token mask。

### 阶段 B：依赖、信息流与无损编码

4. [[互信息与依赖性]]；
5. [[数据处理不等式与充分统计量]]；
6. [[无损编码、典型集与渐近等分性]]。

阶段验收：能在 entropy、KL 与 likelihood-ratio 三种表示间切换 mutual information；能证明 processing 不增信息；能从 LLN 解释 AEP，并区分单符号码、block code 和渐近极限。

### 阶段 C：建模与推断原则

7. [[最大熵原理与指数族]]；
8. [[变分推断、ELBO 与证据分解]]；
9. [[f-散度、Bregman 散度与概率度量]]。

阶段验收：能用 Lagrange duality 推导最大熵分布；能逐项重建 ELBO identity；能根据方向、支撑、拓扑与估计器选择差异量，而不是把所有“距离”互换。

### 阶段 D：压缩、表示与泛化视角

10. [[率失真、信息瓶颈与最小描述长度]]。

阶段验收：能明确 source、representation、decoder、distortion、rate 和 task target；能区分理论最优曲线、估计 surrogate 与训练 heuristic。

## 五、全卷必须维持的区分

| 容易混淆的对象 | 正确区分 |
|---|---|
| self-information vs probability | $-log p(x)$ 是相对于指定模型的惊讶度；不是事件的语义重要性 |
| entropy vs one-sample surprise | $H(P)$ 是对 $X\sim P$ 的平均；$-log p(x)$ 是一次 realization 的值 |
| entropy vs cross-entropy | $H(P)$ 用真实 $p$ 编码；$H(P,Q)$ 用 $q$ 编码来自 $P$ 的数据 |
| cross-entropy vs KL | $H(P,Q)=H(P)+D_{\rm KL}(P\|Q)$；训练时 $H(P)$ 是否为常数取决于 target 是否固定 |
| KL divergence vs metric | KL 不对称、一般不满足三角不等式，且支撑不兼容时可为无穷 |
| discrete entropy vs differential entropy | differential entropy 可为负、会随坐标缩放改变，不能照搬离散码长解释 |
| mutual information vs correlation | MI 能检测一般统计依赖；相关为零仍可依赖；两者都不自动等于因果 |
| empirical loss vs population quantity | 小批量 NLL 是样本估计；其偏差、方差与数据分布偏移需另审计 |
| nats vs bits | 自然对数给 nats；以 2 为底给 bits；perplexity 必须与底一致 |
| logit vs probability | 未归一化 score 不是概率；对非概率对象套普通 KL 可能没有定义 |

## 六、AI 调用地图

| AI 场景 | 被调用的正式对象 | 首要失败边界 |
|---|---|---|
| $K$ 类分类 | conditional cross-entropy、proper scoring | 错标/软标、class weights、label smoothing 与 calibration |
| autoregressive LM | conditional chain rule、token NLL、entropy rate | tokenizer、EOS、mask、length normalization、数据重复 |
| 蒸馏与一致性训练 | teacher–student conditional KL | temperature、方向、stop-gradient、teacher calibration |
| VAE/VI | KL、ELBO、variational gap | posterior family、support、Monte Carlo estimator、amortization gap |
| 对比学习 | density ratio、MI lower bound | negative sampling distribution、finite-batch bias、bound looseness |
| 表示压缩 | data processing、information bottleneck | deterministic continuous nets 的 MI 病态、estimator dependence |
| 生成模型评价 | cross-entropy/KL/other probability metrics | likelihood 与 sample quality 不等价、支撑不匹配、估计不可得 |
| uncertainty | predictive entropy、conditional entropy、MI | aleatoric/epistemic 混淆、OOD 失校准、高 entropy 非错误证书 |

## 七、当前稳定结论与缺口

| 节点 | 已建立 | 仍需验收 |
|---|---|---|
| [[自信息、熵与编码长度]] | 对数自信息的公理刻画、Shannon entropy、binary entropy、最大熵、Kraft/码长下界、Shannon code、perplexity 和连续边界 | 闭卷重建可加性证明、手算码树、比较真实码长与理想码长，并完成 tokenizer/底数审计 |
| [[联合熵、条件熵与链式法则]] | joint/conditional entropy、二元与多元 chain rule、conditioning reduces entropy、subadditivity、deterministic map 和序列 NLL | 闭卷证明 chain rule 与等号条件，完成 XOR/BSC/序列 mask 手算，并区分随机条件熵与 pointwise 条件熵 |
| [[交叉熵与 KL 散度]] | cross-entropy、KL decomposition、Gibbs inequality、方向/支撑、MLE 投影、softmax 梯度、Gaussian KL 与 AI surrogate 边界 | 闭卷证明非负性、构造不对称/无穷反例，手推 logits 公式并完成模型错设、蒸馏与 GlobalPointer 审计 |
| [[互信息与依赖性]] | joint/product KL、PMI/MI、conditional MI、Gaussian MI、非线性依赖、连续确定性病态与 estimator/InfoNCE 边界 | 闭卷证明 chain rule，完成 plug-in bias 手算，并能把 neural objective 标成真值、estimate、bound 或 surrogate |
| [[数据处理不等式与充分统计量]] | Markov chain、DPI 与等号、KL contraction、统计/任务充分性、factorization、Fano 与 AI 表示边界 | 闭卷证明 DPI/factorization/Fano，并能在 skip、增强、隐私场景先画对概率图 |
| [[无损编码、典型集与渐近等分性]] | code class、Kraft–McMillan、Huffman、block code、AEP、typical set、source coding threshold、entropy rate 与 LM 压缩审计 | 闭卷证明码长下界、typical cardinality 和 coding converse，完成实际 coder/model overhead 审计 |
| [[最大熵原理与指数族]] | 约束完备写法、Lagrange dual、指数族、log-partition 的 moment/covariance 几何、边界解、连续参考测度、MLE 对偶与 conditional MaxEnt | 闭卷推导 primal/dual 和三类最大熵分布，手算 softmax，并审计不可行约束、冗余统计量与配分函数近似 |
| [[变分推断、ELBO 与证据分解]] | evidence identity、reverse-KL gap、mean-field、VAE、两类梯度估计、approximation/optimization/amortization gaps、collapse 与 IWAE | 闭卷重建 ELBO 恒等式和 Gaussian KL，复现实验，能把 likelihood、family、estimator、model misspecification 分层 |
| [[f-散度、Bregman 散度与概率度量]] | $f$-divergence、Fenchel 表示、Bregman 几何、IPM、TV、Wasserstein、MMD、拓扑与有限样本边界 | 闭卷证明非负性/DPI，构造 KL 非 metric 反例，并能按支撑、ground geometry、critic class 与估计代价选择对象 |
| [[率失真、信息瓶颈与最小描述长度]] | rate–distortion 的定义/端点/凸性、achievability/converse、Bernoulli/Gaussian 闭式、Blahut–Arimoto、learned compression、IB self-consistency/VIB bounds、VAE bits-back、two-part/Bayesian/NML/prequential MDL | 闭卷区分 theorem frontier、有限码本和 neural codec；重建 VIB 两个 gap；完成[[实验 - 信息论累计复现门]]和卷末测验 |

## 八、来源与证据分工

- Shannon 1948：entropy、编码与通信问题的原始奠基文本；
- Kullback–Leibler 1951：discrimination information 与 sufficiency 的原始来源；
- MIT 6.441、Stanford EE376A 与 Cover–Thomas：定义、链式法则、Gibbs inequality、编码定理和渐近结论的正式证明主线；
- 概率论与凸分析节点：期望、条件分布、LLN、Jensen 与 log-sum inequality 的前置证明；
- [[S-2015-Su-3534-熵不起一]]：从惊讶度、熵、联合/条件熵进入 AI 的中文直觉桥；
- Jaynes 1957 与 Wainwright–Jordan：分别承担 maximum entropy 建模原则，以及 exponential family、log-partition、moment map 与 variational duality 的正式主线；
- Blei–Kucukelbir–McAuliffe、Kingma–Welling 与 IWAE 原论文：承担 ELBO identity、amortized VI、reparameterization 与多样本下界的正式证据；
- Csiszár、Bregman、f-GAN、Sriperumbudur、Gretton 与 WGAN：承担 $f$-divergence、Bregman、Fenchel critic、kernel metric、MMD 与 Wasserstein 生成学习接口；
- [[S-2015-Su-3552-最大熵原理]]与[[S-2015-Su-3567-最大熵模型]]：最大熵约束、指数形式与条件 log-linear 模型的中文推导入口；
- [[S-2018-Su-5253-变分自编码器一]]、[[S-2018-Su-5343-VAE从贝叶斯观点出发]]、[[S-2018-Su-5383-变分自编码器三]]与[[S-2021-Su-8791-VAE估计样本概率密度]]：VAE、重参数化、importance evaluation 与 IWAE 的问题入口；
- [[S-2018-Su-6016-fGAN与变分散度]]、[[S-2019-Su-6280-Wasserstein距离与WGAN]]与[[S-2021-Su-8244-WGAN成功与距离近似]]：variational divergence、Wasserstein 拓扑和受限 critic 的中文研究入口；
- [[S-2018-Su-5476-最小熵原理词库构建]]：把 $-\log p$ 与分词/词库目标连接；
- [[S-2017-Su-4669-词向量与互信息]]：PMI、共现矩阵和词向量的 NLP 问题入口；
- [[S-2018-Su-6024-深度学习的互信息]]：joint/product 判别与 Deep InfoMax 入口；JS surrogate、负采样和估计边界由正式文献补严；
- [[S-2018-Su-6181-变分编码与信息瓶颈]]：任务信息与输入压缩的分离、variational upper bound 入口；泛化主张保持为待验证假设；
- Shannon 1959、MIT 6.441 Chapter 23 与 Cover–Thomas：rate–distortion function、coding theorem、Bernoulli/Gaussian 例子和 Blahut–Arimoto 的正式主线；
- Tishby–Pereira–Bialek 与 Alemi et al.：information bottleneck 原始变分原则、self-consistent equation 和 deep VIB bounds；
- Rissanen、Grünwald 与 bits-back 文献：two-part、Bayesian/NML/prequential MDL 和 latent code 的完整描述长度语义；
- [[S-2018-Su-6088-VAE最小化先验与最大化互信息]]与[[S-2020-Su-7695-词向量维度与最小熵]]：VAE rate–MI 分解、表示维度/熵启发与中文问题入口；不单独承担 coding theorem 或 MDL 最优性证明；
- [[S-2022-Su-9039-GlobalPointer下的KL散度]]：提醒“模型输出不是概率分布时，普通 KL 可能没有定义”；
- 科学空间文章不单独承担 Kraft inequality、source coding theorem、AEP、data processing 或 variational bound 的正式证据。

## 九、下一步

INFO-01—10 已完成正文、十幅机制图、150 道 A–E 题与独立详解，10.6 达到 **10/10 正文覆盖**。INFO-08 的[[实验 - ELBO 恒等式、变分族限制与摊销缺口]]分离 approximation 与 amortization gap；[[实验 - 信息论累计复现门]]把 Bernoulli–Hamming 前沿、task/nuisance bottleneck 与 prequential code 组成三轨计算验收。`INFO-CUM-01` 的[[阶段测验 - 信息论与统计学习接口（10.6）]]和[[阶段测验解答 - 信息论与统计学习接口（10.6）]]已经成稿，但当前仍为 `composed / not-attempted`。所有节点保持 `draft`；下一施工卷进入 10.7 优化与凸分析，首节点为[[优化问题、可行域与局部最优]]。

### 2026-08-23 图像标准化进度

- INFO-01—10 共 10 个正文节点、11 个正式图文单元全部迁移为 v2；章内 v1 与相对图片路径均为 0；
- 11/11 使用稳定根路径、`880 px` 宽度、引图问题、标准图注、生成来源、读图说明与适用边界；
- 机制图分别由[[plot_information_foundations_v2.py]]、[[plot_information_geometry_v2.py]]与[[plot_information_coding_v2.py]]生成；INFO-08 研究曲线由[[plot_elbo_gap.py]]精确枚举；
- 11/11 已重跑并通过 SVG 结构、XML 与 1200 px 实际渲染；共享的[[实验 - ELBO 恒等式、变分族限制与摊销缺口]]也已同步为 v2 图文单元。

---
type: moc
status: active
area: [math/information-theory, math/statistical-learning, ai/probabilistic-modeling]
aliases: [信息论 MOC, Information Theory MOC]
prerequisites: ["[[概率论与数理统计 MOC]]", "[[期望、方差与矩]]", "[[联合分布、边缘分布与独立性]]"]
related: ["[[数学基础 MOC]]", "[[数学基础完整课程地图与掌握标准]]", "[[练习与测验 MOC]]", "[[推导与实验 MOC]]"]
sources: ["Shannon-1948-Mathematical-Theory-Communication", "Shannon-1959-Coding-Theorems-Fidelity-Criterion", "Kullback-Leibler-1951-Information-Sufficiency", "Jaynes-1957-Information-Theory-Statistical-Mechanics", "Csiszar-1967-f-Divergence", "Tishby-Pereira-Bialek-1999-Information-Bottleneck", "Alemi-et-al-2017-Deep-Variational-Information-Bottleneck", "Rissanen-1978-Modeling-Shortest-Data-Description", "Grunwald-2007-MDL", "Honkela-Valpola-2004-Bits-Back", "MIT-6.441-Information-Theory", "Stanford-EE376A-Information-Theory", "Cover-Thomas-Elements-Information-Theory", "Wainwright-Jordan-2008-Exponential-Families-Variational-Inference", "Blei-Kucukelbir-McAuliffe-2017-Variational-Inference", "Kingma-Welling-2014-AEVB", "Nowozin-Cseke-Tomioka-2016-fGAN", "Gretton-et-al-2012-MMD", "Arjovsky-Chintala-Bottou-2017-WGAN", "Su-3534-Entropy-Part-I", "Su-3552-Maximum-Entropy", "Su-3567-Maximum-Entropy-Model", "Su-6016-fGAN", "Su-6088-VAE-Prior-MI", "Su-6181-Variational-Coding-Information-Bottleneck", "Su-7695-Embedding-Dimension-Entropy", "Su-8244-WGAN-Distance", "Su-8791-VAE-Density"]
created: 2026-08-19
updated: 2026-08-28
---

# 信息论与统计学习接口 MOC

> [!abstract] 本卷的核心任务
> 把“惊讶、不确定性、依赖、分布失配与可压缩性”变成带条件、单位和操作含义的数学量。课程从离散自信息和平均码长出发，建立 joint/conditional entropy、cross-entropy、KL 与 mutual information；再用数据处理、典型集、最大熵、变分推断和率失真把它们接到语言模型、表示学习、生成模型与压缩。公式只有在随机对象、分布、对数底、支撑和归约尺度都写清时才有意义。

### 当前教学迁移路线

> [!important] 学习状态与材料迁移状态分开
> 下表只记录“课程位置—两遍路线—问题链—贯穿例—对象账本—公式七问—停靠线”是否补齐。正文 frontmatter 与核心节点表中的 `draft` 仍表示学习者尚未完成闭卷、订正和延迟复做；`regression-passed` 只说明材料及静态检查通过，不能替代真实掌握。

| 波次 | ID 范围 | 认知主线 | 材料迁移 |
|---|---|---|---|
| A | INFO-01—04 | 自信息/熵 → 联合/条件链 → cross-entropy/KL → 互信息 | `regression-passed` |
| B | INFO-05—06 | 数据处理/充分性 → 无损编码/典型集/AEP | `regression-passed` |
| C | INFO-07—10 | 最大熵/指数族 → ELBO → 散度几何 → 率失真/IB/MDL | `regression-passed` |
| CUM | INFO-CUM-01 | 口试 → 闭卷 → nonce 随机轨 → 盲干预 → 订正 → 48 h / 14 d → 独立审计 | `regression-passed / not-attempted` |

第一波固定使用二元对称信道：

$$
X\sim\operatorname{Bernoulli}\!\left(\frac12\right),
\qquad
N\sim\operatorname{Bernoulli}\!\left(\frac14\right),
\qquad
Y=X\oplus N,
\qquad
N\perp X.
$$

它在同一个四格联合分布上把四章的核心量闭合为

$$
H_2(X)=H_2(Y)=1,
\qquad
H_2(Y\mid X)=h_2\!\left(\frac14\right)
=2-\frac34\log_2 3
\approx0.811278,
$$

$$
H_2(X,Y)=1+h_2\!\left(\frac14\right)
\approx1.811278,
$$

以及

$$
\underbrace{\mathbb E_{P_{XY}}[-\log_2p_Y(Y)]}_{\text{忽略输入时为 }1}
-\underbrace{H_P(Y\mid X)}_{\text{知道输入时约 }0.811278}
=\underbrace{I(X;Y)}_{\text{预测收益}}
=\frac34\log_2 3-1
\approx0.188722\ \text{bit}.
$$

这一等式是第一波的中心桥梁：自信息先被平均成 entropy，概率链把 entropy 拆成条件项，错误模型产生 KL gap，而“忽略 $X$ 的 marginal model”这一特殊错模的 gap 正好就是 mutual information。

> [!tip] 第一波停靠线
> 完成 INFO-01—04 后，应能从 joint table $(3/8,1/8;1/8,3/8)$ 出发，依次重建自信息、$H(X,Y)=H(X)+H(Y\mid X)$、conditional cross-entropy/KL gap、两类 PMI 与 $I(X;Y)=1-h_2(1/4)$；同时必须口头声明 log base、expectation 的分布、support 与“统计依赖不等于因果”。

第二波先在 $Y$ 后叠加独立四分之一翻转噪声：

$$
Z=Y\oplus N_2,
\qquad
N_2\sim\operatorname{Bernoulli}\!\left(\frac14\right),
\qquad
N_2\perp(X,N_1).
$$

两级信道的有效翻转率为 $3/8$，因此

$$
I(X;Y)=1-h_2\!\left(\frac14\right)\approx0.188722,
$$

$$
I(X;Z)=1-h_2\!\left(\frac38\right)\approx0.045566,
$$

而精确信息损失是

$$
I(X;Y\mid Z)
=h_2\!\left(\frac38\right)-h_2\!\left(\frac14\right)
\approx0.143156\ \text{bit}.
$$

随后把翻转率改成固定未知参数 $\theta$。在配对输入输出可观察的校准数据中，$N_i=X_i\oplus Y_i$ 且

$$
p_\theta(n_{1:m})
=\theta^{K_m}(1-\theta)^{m-K_m},
\qquad
K_m=\sum_{i=1}^mN_i.
$$

因此 $K_m$ 对 $\theta$ sufficient；但若目标改为无损恢复完整序列，顺序仍必须编码。固定回 $\theta=1/4$ 后，大数定律给

$$
\frac{K_m}{m}\xrightarrow{P}\frac14
\quad\Longrightarrow\quad
-\frac1m\log_2p(N_{1:m})
\xrightarrow{P}h_2\!\left(\frac14\right).
$$

于是典型集在指数阶上包含约 $2^{mH}$ 个成员，每个成员概率约 $2^{-mH}$，总概率趋近 $1$；这再推出 exact variable-length block code 的 $H\le L_m/m<H+1/m$，以及 fixed-length almost-lossless code 的一阶临界率 $R=H$。

> [!tip] 第二波停靠线
> 完成 INFO-05—06 后，应能验证级联 BSC 的 $1/4\star1/4=3/8$，用 MI chain rule 算出 $0.143156$ bit 的损失；从 Bernoulli likelihood 说明 $K_m$ 对翻转率充分；再从 $K_m/m\to1/4$ 推出 AEP、典型集三性质与 source-coding 阈值。还必须解释：**统计充分性允许丢掉与参数无关的顺序，而无损编码完整序列不能丢掉这些顺序。**

第三波把“已知分布”改成“先建模、再推断”。只知道两个 binary states 的 moments

$$
\mathbb E[Z_1]=\mathbb E[Z_2]=\frac14
$$

时，finite-support MaxEnt 给

$$
p^*(z_1,z_2)
=\exp\{\eta_1z_1+\eta_2z_2-A(\eta)\},
\qquad
\eta_1=\eta_2=-\ln3,
$$

以及独立 joint probabilities $(9,3,3,1)/16$。取其中一个 coordinate 作 latent prior，并通过独立四分之一翻转噪声产生 observation：

$$
Z\sim\operatorname{Bernoulli}\!\left(\frac14\right),
\qquad
X=Z\oplus E,
\qquad
E\sim\operatorname{Bernoulli}\!\left(\frac14\right).
$$

当 $X=1$ 时，evidence 与 posterior 为

$$
p(X=1)=\frac38,
\qquad
p(Z=1\mid X=1)=\frac12.
$$

这一模型在四章中承担不同任务：

| 节点 | 固定对象 | 核心可复算结果 | 不可混淆的边界 |
|---|---|---|---|
| INFO-07 | 支持、counting measure、moments | $\eta=-\ln3$，MaxEnt joint 独立 | MaxEnt 解不证明真实独立 |
| INFO-08 | generative $p$、observation $X=1$、variational $q$ | $\ln p(x)=-0.980829=-1.111641+0.130812$ | gap 为零不证明模型正确 |
| INFO-09 | $P=\operatorname{Ber}(1/2)$、$Q=\operatorname{Ber}(1/4)$ | forward/reverse KL 为 $0.143841/0.130812$ nats，TV 与单位距 $W_1$ 为 $1/4$ | ground metric、方向与 estimator 分层 |
| INFO-10 | source $Z$、input $X$、representation $T$、code protocol | $R(1/8)=0.267714$ bit；$I(Z;X)=0.143156$ bit；naive latent/evidence code 为 $1.622556/0.954434$ bits | RD、IB 与 MDL 目标不可互换 |

INFO-10 的 erasure representation 进一步给

$$
I(X;T)=0.954434\alpha,
\qquad
I(Z;T)=0.143156\alpha,
$$

说明“压缩输入”必须和“保留任务信息”同时报告。朴素先编码 latent 再编码 observation 的平均长度为

$$
H(Z)+H(X\mid Z)=1.622556\ \text{bits},
$$

反而长于直接 evidence/marginal code 的

$$
H(X)=0.954434\ \text{bit};
$$

多出的 $H(Z\mid X)=0.668122$ bit 只有在满足相应 posterior 与 bits-back 编码协议时才可能回收。

> [!tip] 第三波停靠线
> 完成 INFO-07—10 后，应能从 moment constraints 解出 $\eta=-\ln3$；枚举 evidence/posterior 并闭合 ELBO gap；对同一 posterior pair 算正反 KL、TV 与 $W_1$；最后分别写出 rate–distortion、IB 和 MDL 的随机对象、优化变量及不可移植边界。尤其要能解释：**“最大熵”“变分下界”“分布距离”和“压缩正则”不是四个可替换的 loss 名称。**

## 零、怎样从零真正学完本卷

> [!important] 卷级学习合同
> 本卷已经完成的是**材料迁移与回归**，不是学习者的自动掌握。推荐路径是“对象与编码直觉 → 推导、反例与边界 → 无提示整合与计算复现”三遍循环。读者一旦说不清 expectation 在哪个分布下、log base、支撑或 code protocol，就回到第一个断点，不用后面更高级的术语掩盖它。

### 0.1 进入门：最低前置不是完整测度论

开始 INFO-01 前，只要求能够：

1. 读写离散 PMF、joint/conditional probability 与 expectation；
2. 熟练使用 $\log(ab)=\log a+\log b$、换底公式和基本求和；
3. 理解独立、条件独立、大数定律与 KL 非负；
4. 看懂 Lagrange multiplier、凸函数切线和矩阵/向量的基本记号。

若前两项不能无提示完成，先回到[[条件概率、全概率与 Bayes 公式]]、[[联合分布、边缘分布与独立性]]和[[期望、方差与矩]]的第一遍停靠线。测度论 Radon–Nikodym derivative、一般平稳遍历源、convex duality 和最优传输会在需要时分层引入，不要求先学完完整专门课程。

### 0.2 三波不是三套孤立术语，而是一族逐步改造的 noisy-bit 模型

下图中的箭头表示**教学模型和问题合同的改变**。每次从“分布已知”改为“参数未知”、从“统计压缩”改为“序列无损恢复”、或从“真实信息量”改为“bound/estimator”时，都必须重新声明随机对象。

```mermaid
flowchart LR
    A["A 已知 noisy bit\n信息量·链式法则·KL·MI"] --> B["B 处理与长序列\nDPI·充分性·AEP·无损编码"]
    B --> C["C 建模与任务压缩\nMaxEnt·ELBO·散度·RD/IB/MDL"]
```

| 波次 | 核心随机对象 | 哪个合同发生变化 | 本波第一次能回答的问题 | 最容易犯的错 |
|---|---|---|---|---|
| A | $X\sim\operatorname{Ber}(1/2)$、$N\sim\operatorname{Ber}(1/4)$、$Y=X\oplus N$ | 分布完全已知，依次改变“用哪个模型评分”与“是否忽略输入” | surprise 怎样平均成 entropy，错模怎样产生 KL，依赖怎样成为 MI | 把 self-information、entropy、cross-entropy 和单样本 NLL 混成一个量 |
| B | 级联 $X\to Y\to Z$；未知 $\theta$ 下的 $N_{1:m},K_m$ | 先加后处理；再把翻转率改为固定未知；最后把目标改成恢复完整序列 | 信息为何只减不增；哪些细节对参数充分；长 block 为何可压缩 | 把“对参数可丢顺序”误写成“无损编码也可丢顺序” |
| C | MaxEnt $Z$、noisy observation $X$、variational $q$、representation $T$ | 分布不再预先给定；posterior 需近似；差异量和保留目标由任务选择 | 怎样建先验、算 evidence、审计 bound、选择几何并区分 RD/IB/MDL | 把 lower bound 当真值、把 latent KL 当 MI、把短 training loss 当完整码长 |

三波共享一批数值不是偶然：$h_2(1/4)\approx0.811278$ 既是噪声 entropy，也是 AEP 的每符号 surprise 极限；$h_2(3/8)-h_2(1/4)\approx0.143156$ 既可表示级联中的信息差，也可表示 latent state 与 noisy observation 的 MI。但**数值相同不表示随机对象和操作语义相同**。

### 0.3 三遍学习与每遍退出条件

| 遍次 | 怎样读 | 必须产生的无提示输出 | 达不到时怎样回退 |
|---|---|---|---|
| 第一遍：对象与直觉 | 只读各章“课程位置—问题链—贯穿例—第一遍停靠线” | 对每个公式说清随机变量、分布、单位、一次/平均层级、一个 AI 接口和一个不能推出的结论 | 回到当前波模型表，重画 joint、channel 或 code protocol |
| 第二遍：推导与边界 | 完成公式七问、正文证明、最小反例与 A—E 节点习题 | 无提示重建负对数、chain rule、Gibbs/DPI、AEP、MaxEnt、ELBO 和 RD/IB/MDL 中至少一条主证明 | 回到第一个缺失等号，补写使用的 support、independence、convexity 或 asymptotic 条件 |
| 第三遍：整合与验收 | 冻结笔记，完成卷级口试、100 分闭卷题、随机计算轨道和延迟迁移 | 15 分钟画出三波对象链；A—E 各区过线；独立生成 SVG/hash；48 小时与 14 天复做 | 按错题第一个断点回链，查看解答后的订正不冒充首次独立通过 |

### 0.4 五层证据与状态语义

1. **复述证据**：能区分 probability/self-information/entropy/KL/MI，但不等于会推导；
2. **推导证据**：能无提示完成公式与反例，但不等于会在新 AI 问题中选对象；
3. **闭卷证据**：[[阶段测验 - 信息论与统计学习接口（10.6）|INFO-CUM-01]] 的口试、总分与 A—E 分区同时过线；
4. **复现证据**：[[实验 - 信息论累计复现门]]用 attempt_id 与 scorer nonce 唯一指定深入轨，解析校准后先冻结未见参数预测，再保存新 output/SVG/hash 与手检；
5. **保持与迁移证据**：48 小时重做，14 天后换 source、换 distortion 或换 AI 情境仍能独立完成。

`regression-passed` 只说明仓库材料通过[[information_cumulative_contract_audit.py|信息论卷级静态与计算回归]]；正文 frontmatter 的 `draft` 和学习记录的 `not-attempted` 继续表示尚无个人掌握证据。

### 0.5 卷级总图：三个“压缩更好”为何不是一个命题

先遮住图注回答：A 的纵轴、B 的横纵轴与 C 的累计纵轴分别是什么对象？哪个来自 theorem-level information function，哪个来自给定 joint law，哪个依赖完整预测顺序？

![[00-知识库管理/_assets/plots/information-theory/plot-information-cumulative-gate-v2.svg|920]]

> [!figure] 图 10.6-CUM｜信息论卷级复现门：前沿、表示与顺序码长
> A 复核公平 Bernoulli–Hamming 的解析 $R(D)$；B 在 task/nuisance joint law 上比较 input rate 与 task relevance；C 在固定 seed 的 Bernoulli sequence 上比较 fixed model 与 KT prequential codelength。来源：独立计算与绘制；生成脚本：[[plot_information_cumulative_gate.py]]；固定 seed `20260819`；正式 SVG SHA-256 为 `29fce27e85639837d2e8265f2f8fa9a3c6412680b39559a9e3c0f4db8fcdde47`。

**怎样读图。** A 沿 distortion budget 读取一阶最小 rate，不把绘图采样点当 coding theorem 证明；B 先固定 target $Y$，比较 relevance 相同的表示是否无偿携带 nuisance；C 从第一个 symbol 起累计全部预测成本，不用看完整数据后的 plug-in NLL 偷掉学习开销。

**适用边界。** A 只覆盖公平 binary source 与 Hamming distortion；B 是可精确枚举的 task/nuisance toy joint；C 只是一条固定序列和两种预设 predictor。三栏均不证明神经互信息 estimator 无偏、不证明更短描述必然泛化，也不提供因果、公平或部署保证。

> [!success] 卷级第一遍停靠线
> 合上笔记后，应能在 15 分钟内画出 A—C 三波，分别写出 $H(P,Q)=H(P)+D(P\Vert Q)$、DPI loss、AEP、evidence–ELBO identity 和 RD/IB/MDL 的一个核心公式；再为每式补上 expectation 分布、log base/support 或 code protocol。做不到时，暂不进入卷末闭卷题。

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

## 九、卷级完成度与下一步

INFO-01—10 已完成正文、十幅机制图、150 道 A–E 题与独立详解，10.6 达到 **10/10 正文覆盖**；这表示深层内容已经存在，不表示初学者入口已全部迁移，更不表示学习者已经掌握。

截至 2026-08-28，INFO-01—10 与 INFO-CUM-01 已完成当前教学合同并通过静态与确定性计算回归，三波正文和卷级材料状态均为 `regression-passed`；个人学习状态继续保持 `draft / not-attempted`。

| 验收 artifact | 材料层作用 | 个人证据状态 |
|---|---|---|
| [[阶段测验 - 信息论与统计学习接口（10.6）]] | 15 分钟口试、100 分闭卷、答案隔离、48 h / 14 d 延迟门 | `not-attempted` |
| [[阶段测验解答 - 信息论与统计学习接口（10.6）]] | 14/14 逐题评分、三波数值锚点与判分红线 | `not-attempted` |
| [[实验 - 信息论累计复现门]] | 解析校准、scorer nonce、RD/IB/prequential 盲参数接口与 output/hash | `not-attempted` |
| [[information_cumulative_contract_audit.py]] | 独立解析模型、canonical 双跑、干预 hash 与状态面回归 | 不产生个人证据 |

INFO-08 的[[实验 - ELBO 恒等式、变分族限制与摊销缺口]]继续承担 approximation 与 amortization gap 的专项实验。所有正文节点仍保持 `draft`，直到出现真实口试、闭卷原稿、nonce 随机轨、未见参数运行、订正与延迟复做证据。

### 2026-08-23 图像标准化进度

- INFO-01—10 共 10 个正文节点、11 个正式图文单元全部迁移为 v2；章内 v1 与相对图片路径均为 0；
- 11/11 使用稳定根路径、`880 px` 宽度、引图问题、标准图注、生成来源、读图说明与适用边界；
- 机制图分别由[[plot_information_foundations_v2.py]]、[[plot_information_geometry_v2.py]]与[[plot_information_coding_v2.py]]生成；INFO-08 研究曲线由[[plot_elbo_gap.py]]精确枚举；
- 11/11 已重跑并通过 SVG 结构、XML 与 1200 px 实际渲染；共享的[[实验 - ELBO 恒等式、变分族限制与摊销缺口]]也已同步为 v2 图文单元。

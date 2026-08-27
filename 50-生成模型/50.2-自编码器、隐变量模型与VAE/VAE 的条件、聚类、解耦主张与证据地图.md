---
type: concept
status: verified
area: [generative-models, vae, conditional-generation, disentanglement]
aliases: [Conditional VAE, 聚类VAE, 解耦表示证据]
node_id: GEN-16
prerequisites: ["[[层次 VAE、表达性先验与近似后验 Flow]]", "[[互信息与依赖性]]", "[[数据生成分布与采样假设]]"]
related: ["[[Posterior Collapse、率失真与解码器容量]]", "[[采样器、条件控制、加速与评估 MOC]]"]
sources: ["[[S-2018-Su-5887-VAE聚类]]", "[[S-2017-Higgins-BetaVAE]]", "[[S-2017-Zhao-InfoVAE]]", "[[S-2018-Locatello-Disentanglement-Impossibility]]", "[[S-2021-Su-8475-UniVAE]]"]
exercises: ["[[习题 - VAE 的条件、聚类、解耦主张与证据地图]]"]
solutions: ["[[解答 - VAE 的条件、聚类、解耦主张与证据地图]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-vae-claims-evidence-matrix-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# VAE 的条件、聚类、解耦主张与证据地图

> [!abstract] 本节主问题
> 条件生成、无监督聚类和表示解耦常共用 VAE 组件，却回答三类不同科学问题。重构、聚类准确率、latent traversal 与生成质量各自只能支持有限结论；尤其在纯无监督条件下，观测分布通常不足以唯一识别“真实因素”。

## 一、先把三种任务拆开

### 1.1 条件 VAE

观察条件 $c$，模型为

$$
p_\theta(x,z\mid c)=p_\lambda(z\mid c)p_\theta(x\mid z,c),
\qquad q_\phi(z\mid x,c).
$$

ELBO 为

$$
\mathcal L(x,c)=
\mathbb E_q\log p_\theta(x\mid z,c)
-\mathrm{KL}(q_\phi(z\mid x,c)\|p_\lambda(z\mid c)).
$$

若实际仍用无条件 $p(z)$，也必须明说。生成时先指定 $c$ 的部署分布，再抽 $z$ 与 $x$；训练条件比例变化会改变总体指标。

### 1.2 聚类 VAE

引入离散 cluster $Y$ 与连续 style $Z$：

$$
p(y,z,x)=p(y)p(z\mid y)p_\theta(x\mid z,y),
$$

并用 $q_\phi(y,z\mid x)$ 近似后验。cluster label 有置换不确定性；若没有真标签，模型只能发现其 objective 偏好的 partition，不自动等于人类语义类别。

### 1.3 解耦表示

常希望 latent 坐标分别对应独立生成因素。但“统计独立”“坐标轴可控”“下游线性可读”“因果机制独立”不是同一定义。写论文或笔记前必须指定 target notion。

## 二、聚类 ELBO 怎样展开

若采用 $q(y,z\mid x)=q(y\mid x)q(z\mid x,y)$，则

$$
\begin{aligned}
\mathcal L(x)
&=\mathbb E_{q(y,z\mid x)}\log p_\theta(x\mid z,y)\\
&\quad-\mathbb E_{q(y\mid x)}
\mathrm{KL}(q(z\mid x,y)\|p(z\mid y))\\
&\quad-\mathrm{KL}(q(y\mid x)\|p(y)).
\end{aligned}
$$

第三项会把 aggregate cluster usage 拉向 $p(y)$，但 per-example 上过强也可能鼓励高熵、模糊 assignment。训练还涉及 discrete $y$ 的枚举、Gumbel relaxation 或 score-function estimator；每种做法偏差/方差不同。

## 三、科学空间聚类方案承担什么证据

[[S-2018-Su-5887-VAE聚类]]给出连续 $z$ 加离散 $y$ 的端到端构造，是理解“生成模型怎样内生出 cluster head”的好案例。文章也明确代码偏 idea verification、未精细调参。因此课程把它标为设计案例与经验假说，不外推成：

- 对任意数据优于标准聚类；
- $y$ 必然恢复真实类别；
- 连续与离散 latent 已被唯一解耦；
- 训练稳定或对超参数鲁棒。

这些结论分别需要多数据集、标签匹配协议、干预/可识别性假设、seed/ablation 证据。

## 四、$\beta$-VAE 与独立 prior 的边界

$\beta$-VAE 优化

$$
\mathbb E_q\log p_\theta(x\mid z)
-\beta\,\mathrm{KL}(q(z\mid x)\|p(z)).
$$

当 $p(z)$ factorized 且 $\beta>1$，更强压缩有时产生更轴对齐的表示，但它同时牺牲 rate/reconstruction；不能由 objective 形式推出 recover true factors。[[S-2017-Higgins-BetaVAE]]提供特定实验设置下的证据，不是一般 identifiability theorem。

InfoVAE 类方法把 aggregate posterior matching 与 MI 控制拆开，提醒我们 per-example KL 同时混合两种责任；但选定 divergence/MMD kernel 又引入 estimator 与 topology 假设。

## 五、不可识别性为什么是根本问题

假设数据由独立因素 $s$ 通过可逆生成器 $x=g(s)$ 产生。存在可逆混合 $h$，令 $z=h(s)$，同时 decoder 用 $g\circ h^{-1}$，可得到相同观测分布。通过构造保持目标先验的非平凡变换，还能让不同 latent 坐标解释拥有同样 likelihood。

[[S-2018-Locatello-Disentanglement-Impossibility]]的核心边界是：**没有关于数据生成过程和模型归纳偏置的额外假设，纯无监督 disentanglement 不可识别**。它不意味着一切解耦研究无效；以下信息可以打破对称：

- weak/partial labels 或成对变化信息；
- group action/equivariance；
- temporal independence 与环境变化；
- causal interventions；
- 明确 architecture 和 sparsity assumptions。

## 六、证据梯子

从弱到强可分：

1. **样例 traversal**：某个 seed 上改变 $z_j$ 时画面变化；
2. **统计关联**：latent 与已知 factor 的相关/MI/分类分数；
3. **多 seed 指标**：MIG、DCI、SAP 等，报告 estimator 与 model selection；
4. **受控干预**：只改变真实因素，检查 latent 响应与其他因素不变；
5. **跨分布/下游因果效用**：环境变化后仍支持干预预测；
6. **可识别性定理**：在明确假设下证明只剩允许等价类。

漂亮二维散点或 traversal 只能处在第一至二层。

## 七、条件生成的评价矩阵

| 主张 | 最低必要证据 | 常见混淆 |
|---|---|---|
| 能按 $c$ 生成 | 条件一致性 + 质量/覆盖 + prior samples | 只看 posterior reconstruction |
| 同一 $c$ 内有多样性 | 固定 $c$ 多次采样、diversity 与 mode coverage | 不同条件之间的差异 |
| cluster 有语义 | label matching/NMI/ARI + 多 seed | 只看二维分色 |
| latent 可控 | intervention 与 leakage matrix | 单条 traversal |
| disentangled | 明确定义、基准因素、多指标/seed、假设 | factorized prior |
| 可迁移 | held-out environment/task | 同分布 linear probe |

## 八、长度、条件与 shortcut leakage

文本/多模态 VAE 还要问：

- $c$ 是否含有目标答案或与目标近乎一一对应；
- encoder mask 是否看到 decoder 本不该看到的信息；
- 长度、padding、位置、文件格式是否泄漏类别；
- posterior reconstruction 好是否仅因 teacher forcing；
- generation 时 $c$ 的分布是否与训练一致。

[[S-2021-Su-8475-UniVAE]]对长度泄漏的讨论值得保留：它是普遍的实验设计警告，而不是该架构独有问题。

## 九、一个反例：完美聚类分数仍不代表生成正确

数据标签 $y$ 可由水印像素完美预测，模型令 discrete latent 只编码水印，得到 100% cluster accuracy；主体内容完全混乱。这个模型在标签指标上完美，却没有捕捉希望的语义生成因素。必须加入去水印干预、主体属性条件一致性与生成覆盖评价。

反向也成立：无标签生成模型可能很好拟合 $p(x)$，但由于 label permutation 或 nonlinear mixing，在给定 axis-aligned 指标上得分低。评价对象必须对应科学问题。

## 十、科学空间研读框

[[S-2018-Su-5887-VAE聚类]]承担结构设计入口，[[S-2021-Su-8475-UniVAE]]承担文本多层表示与 leakage 提醒；课程再以[[S-2017-Higgins-BetaVAE]]、[[S-2017-Zhao-InfoVAE]]与[[S-2018-Locatello-Disentanglement-Impossibility]]建立支持—反例闭环。

博客中的“聚类成功”“几何规整”“语义方向”统一降解为可复现实验主张；除非有明确生成假设与定理，不写为无条件结论。

## 十一、图：主张—证据矩阵

先看图回答：一张 latent traversal 最多支持哪一格？聚类准确率、生成覆盖、intervention 与 identifiability theorem 分别回答哪个问题？

![[00-知识库管理/_assets/figures/generative-models/fig-vae-claims-evidence-matrix-v1.svg|900]]

> [!figure] 图 50.2-08　条件、聚类、解耦主张与证据强度矩阵
> 行表示五类主张，列表示从可视化到定理的证据层级；深色格表示该主张至少需要的关键证据。来源：依据 conditional generation evaluation 与 disentanglement identifiability 文献独立绘制。

**怎样读图**：先选要证明的行，再向右找到能排除竞争解释的证据；不要把某一列的结果横向搬给另一种主张。

**图没有证明什么**：矩阵不保证达到某层证据就自动正确，具体指标仍可能偏置或被 gaming；它用于暴露缺失证据。

## 十二、本节回顾

- conditional、clustering、disentanglement 是三种不同任务与概率合同；
- 聚类 VAE 的离散 KL、连续 KL 和 reconstruction 各负不同责任；
- factorized prior、较大 $\beta$ 或漂亮 traversal 不推出真实因素；
- 无额外假设的纯无监督 disentanglement 一般不可识别；
- 条件一致、覆盖、cluster metric、intervention 和 theorem 必须按主张匹配；
- shortcut、长度与 teacher forcing leakage 是生成表示实验的必要审计项。

## 十三、练习与独立详解

- [[习题 - VAE 的条件、聚类、解耦主张与证据地图]]
- [[解答 - VAE 的条件、聚类、解耦主张与证据地图]]

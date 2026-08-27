---
type: concept
status: verified
area: [generative-models, gan, implicit-models]
node_id: GEN-17
prerequisites: ["[[显式密度、隐式分布与可计算性三角]]", "[[随机变量变换与密度换元]]"]
related: ["[[原始 GAN、最优判别器与 Jensen–Shannon 散度]]", "[[Mode Collapse、模式覆盖与生成器熵]]"]
sources: ["[[S-2014-Goodfellow-GAN]]", "[[S-2019-Su-6316-GAN能量视角]]"]
exercises: ["[[习题 - 隐式 Pushforward 分布、生成器与判别博弈]]"]
solutions: ["[[解答 - 隐式 Pushforward 分布、生成器与判别博弈]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-gan-pushforward-game-ledger-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 隐式 Pushforward 分布、生成器与判别博弈

> [!abstract] 本节主问题
> GAN 的 generator 不必给出 $p_\theta(x)$ 的可计算公式；它只需把已知 latent 分布经 $G_\theta$ 推到数据空间。判别器通过真实样本与生成样本的二分类任务提供分布差异的可训练信号，但有限 classifier score 不是自动等于真实 divergence。

## 一、生成器定义的是 pushforward

令 $Z\sim P_Z$，$G_\theta:\mathcal Z\to\mathcal X$。生成分布

$$
P_\theta=G_{\theta\#}P_Z,\qquad
P_\theta(A)=P_Z(G_\theta^{-1}(A)).
$$

采样只需 $z\sim P_Z$ 再算 $G_\theta(z)$。若 $G$ 非可逆、降维或 many-to-one，$p_\theta(x)$ 可能无普通 closed-form density，甚至相对 ambient Lebesgue 测度奇异。这不妨碍采样，却妨碍直接 MLE。

## 二、样本比较转成二分类

从等先验混合实验抽标签 $Y\sim Bernoulli(1/2)$：

$$
X\mid Y=1\sim P_*,\qquad X\mid Y=0\sim P_\theta.
$$

判别器 $D_\psi(x)\in(0,1)$ 估计 $P(Y=1\mid X=x)$，log score 为

$$
V(\theta,\psi)=E_{P_*}\log D_\psi(X)
+E_{P_Z}\log(1-D_\psi(G_\theta(Z))).
$$

判别器最大化分类 log likelihood；generator 通过改变 $P_\theta$ 让区分变难。

## 三、density ratio 只在理想 classifier 下出现

若 $P_*,P_\theta$ 对共同测度有 densities $p_*,p_\theta$，等类先验的 Bayes classifier 是

$$
D^*(x)=\frac{p_*(x)}{p_*(x)+p_\theta(x)},\qquad
\frac{p_*(x)}{p_\theta(x)}=\frac{D^*(x)}{1-D^*(x)}.
$$

有限网络 $D_\psi$、有限数据与未优化完毕时，logit 只是受限 classifier 的 score；不能直接宣布它是 calibrated density ratio。

## 四、五个 gap

1. **函数类 gap**：$D^*$ 不在 $\{D_\psi\}$；
2. **估计 gap**：经验分类风险不等 population；
3. **优化 gap**：$\psi_t$ 不是 class 内 best response；
4. **动态 gap**：generator 更新时 critic 同时移动；
5. **部署 gap**：latent truncation/conditioning 改变输出分布。

GAN loss 曲线同时混合这些项，绝不是单一固定 objective 的可靠仪表。

## 五、维数与 support

若 $Z\in\mathbb R^m,m<d$ 且 $G$ regular，$P_\theta$ 常落在 $m$ 维集合上。若数据也落在不同低维集合，完美 classifier 可以轻易分开，logistic objective 饱和。加入 instance noise 会把 support 卷积展宽；它改变训练分布，而不仅是 optimizer trick。

## 六、条件 GAN

给条件 $C$：

$$
X_g=G_\theta(Z,C),\qquad
D_\psi(x,c).
$$

必须说明 real 与 fake 使用的条件分布是否相同。若 fake 的 $c$ 比例不同，discriminator 可只读 $c$ 识别来源，形成 shortcut。部署联合为 $R(c)P_\theta(x\mid c)$，依赖部署条件 $R$。

## 七、科学空间研读框

[[S-2019-Su-6316-GAN能量视角]]以判别器塑造能量地形、生成器寻找低能区提供直觉；[[S-2014-Goodfellow-GAN]]给正式 adversarial game。本节采用“挖坑—跳坑”解释交替角色，但不把 discriminator score 自动解释为 normalized energy，也不把低 score/高 score 当 Lyapunov 函数。

## 八、图：从 latent 到五层 game

先看图回答：generator 改哪个分布，critic 看到哪两类样本，population supremum 到一次 SGD update 中间隔了几层？

![[00-知识库管理/_assets/figures/generative-models/fig-gan-pushforward-game-ledger-v1.svg|900]]

> [!figure] 图 50.3-01　隐式 pushforward 与判别博弈五层账
> 图把 latent sampling、generator pushforward、真实/生成二分类与函数类—样本—优化 gap 串联。来源：依据原始 GAN 定义独立绘制。

**怎样读图**：从 $P_Z$ 沿 $G_\theta$ 得 $P_\theta$；real/fake 样本进入同一 critic。再向下检查理论最优、受限类、经验风险与当前 iterate。

**图没有证明什么**：图不证明 classifier 已校准为 density ratio，也不保证 game 收敛或 generator 覆盖数据 support。

## 九、本节回顾

- generator 用 pushforward 定义隐式分布，可采样不等于可算 density；
- 判别学习是样本级 variational 比较接口；
- density ratio 需要 Bayes-optimal/calibrated 条件；
- function、sample、optimization、dynamics 与 deployment gap 必须分账；
- support 分离会使二分类过易并削弱训练信息。

## 十、练习与独立详解

- [[习题 - 隐式 Pushforward 分布、生成器与判别博弈]]
- [[解答 - 隐式 Pushforward 分布、生成器与判别博弈]]


---
type: solution
status: draft
area: [generative-models, vae, disentanglement]
topic: "[[VAE 的条件、聚类、解耦主张与证据地图]]"
exercise: "[[习题 - VAE 的条件、聚类、解耦主张与证据地图]]"
created: 2026-08-25
updated: 2026-08-25
---

# 解答 - VAE 的条件、聚类、解耦主张与证据地图

## A. 识别与复述

### GEN16-A01
$$
p(x,z\mid c)=p_\lambda(z\mid c)p_\theta(x\mid z,c),\quad q_\phi(z\mid x,c).
$$
ELBO 是 $E_q\log p_\theta(x\mid z,c)-KL(q_\phi\|p_\lambda(z\mid c))$。部署先选 $c$，抽 $z\sim p_\lambda(z\mid c)$，再抽 $x\sim p_\theta(x\mid z,c)$。

### GEN16-A02
典型 joint 为
$$
p(y)p(z\mid y)p_\theta(x\mid z,y),
$$
近似后验可为 $q_\phi(y\mid x)q_\phi(z\mid x,y)$。离散标签有 permutation symmetry。

### GEN16-A03
统计独立指联合 factorization/MI 为零；axis-aligned control 指改一坐标只改一属性；下游可读指简单预测器能读出属性；因果解耦要求表示对应独立机制及干预语义。它们没有一般蕴含链。

## B. 手算与建模

### GEN16-B01
$$
KL=.8\log(.8/.5)+.2\log(.2/.5)
=.8\log1.6+.2\log.4\approx.1927.
$$

### GEN16-B02
$$
\mathcal L=-4-.6-.193=-4.793.
$$
注意 reconstruction 已是期望 log likelihood 的负值。

### GEN16-B03
预测标签与真标签完全对调。交换 cluster 名称后，对角变为 $(40,60)$，accuracy 为 $(40+60)/100=100\%$。未做 permutation matching 会错误报告 0%。

## C. 推导与证明

### GEN16-C01
将 joint 与 posterior factorization 代入 $E_q[\log p-\log q]$：
$$
E_q\log p(x\mid z,y)
-E_{q(y\mid x)}KL(q(z\mid x,y)\|p(z\mid y))
-KL(q(y\mid x)\|p(y)).
$$
分别来自 likelihood、连续条件 ratio 与离散 ratio。

### GEN16-C02
令 $z'=h(z)$，用换元所得 $p'(z')$，decoder 取 $p'(x\mid z')=p(x\mid h^{-1}(z'))$。则积分换元后 $p'(x)=p(x)$。若 $h$ 混合坐标，原来单坐标语义变成组合，却不改变观测 likelihood。

### GEN16-C03
量词是：对只观察 $p(x)$、没有关于生成过程/模型的额外假设，不存在一般方法保证恢复真实因素到预期等价类。可破除对称的假设包括 weak paired labels、已知 group actions/equivariance、时间/环境变化独立性、causal interventions 或特定 sparsity/architecture；必须明确其适用分布。

## D. 边界、反例与纠错

### GEN16-D01
每类图片角落放不同颜色水印，主体类别随机。Encoder 的 $Y$ 只读水印，cluster accuracy 100%，decoder 用连续 $Z$ 重构主体。去水印或交换水印后 cluster 崩溃，说明它没捕捉主体语义。

### GEN16-D02
factorized prior 只规定生成 latent 坐标在 prior 下独立。posterior/aggregate 可相关，decoder 可对坐标作任意可逆混合；相同 $p(x)$ 可对应多种 factorization。没有额外归纳偏置与数据变化，真实因素不可识别。

### GEN16-D03
竞争解释包括：decoder 坐标经人为旋转后 traversal 仍平滑但语义混合；只展示成功坐标/seed；大步变化引发 decoder 平滑外推；属性 classifier 受背景混淆。需预注册坐标、全量 seed、intervention leakage matrix 与独立标注。

## E. AI 迁移

### GEN16-E01
矩阵应含：每 $c$ 条件一致性；固定 $c$ 的质量与 precision/recall/diversity；posterior reconstruction 与 prior generation 分开；移除/交换 $c$ 的泄漏干预；训练/部署 $P(c)$ 分层与重加权；多 seed、样本预算和 evaluator calibration。

### GEN16-E02
至少比较 k-means/GMM、AE latent clustering、标准 mixture VAE；预注册超参数和多 seed；用 Hungarian label matching 后报 ACC、NMI、ARI；消融离散 KL、连续 latent、初始化；报告空 cluster、collapse、训练失败率和文章所称 idea-verification 边界。

### GEN16-E03
先全量 traversal 与自动属性指标；再多 seed/MIG-DCI-SAP 和 model-selection sensitivity；再真实单因素受控数据做 leakage/intervention；再 OOD 环境和下游因果预测；最后明确生成假设与允许等价类，证明 identifiability 或诚实标为经验解耦。


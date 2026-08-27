---
type: exercise
status: draft
area: [generative-models, vae, disentanglement]
topic: "[[VAE 的条件、聚类、解耦主张与证据地图]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - VAE 的条件、聚类、解耦主张与证据地图]]"
created: 2026-08-25
updated: 2026-08-25
---

# 习题 - VAE 的条件、聚类、解耦主张与证据地图

## A. 识别与复述

### GEN16-A01
写出 conditional VAE 的 joint、posterior、ELBO 与生成程序。

### GEN16-A02
写出含离散 $Y$、连续 $Z$ 的 clustering VAE factorization。

### GEN16-A03
区分统计独立、axis-aligned controllability、下游可读与因果解耦。

## B. 手算与建模

### GEN16-B01
$q(y\mid x)=(.8,.2),p(y)=(.5,.5)$，计算 categorical KL。

### GEN16-B02
某 clustering ELBO 的 reconstruction 为 $-4$、连续 latent KL 的 $q(y\mid x)$ 加权均值为 $.6$、离散 KL 为 $.193$，求 ELBO。

### GEN16-B03
二类预测与真标签混淆矩阵为 $\begin{pmatrix}0&40\\60&0\end{pmatrix}$。说明最优 label permutation 后 accuracy。

## C. 推导与证明

### GEN16-C01
推导 clustering VAE 的 reconstruction、conditional continuous KL 与 categorical KL 分解。

### GEN16-C02
构造可逆 latent 变换 $h$ 与补偿 decoder，证明观测分布不变而坐标语义改变。

### GEN16-C03
解释无监督 disentanglement 不可识别结论的量词，并列三类可破除对称的额外假设。

## D. 边界、反例与纠错

### GEN16-D01
构造依靠水印取得完美 cluster accuracy、但不捕捉主体语义的模型。

### GEN16-D02
反驳“factorized Gaussian prior 保证 latent factors 独立且真实”。

### GEN16-D03
给出漂亮 traversal 仍可能由 decoder 坐标选择或样本筛选造成的竞争解释。

## E. AI 迁移

### GEN16-E01
为条件图像 VAE 建立条件一致性、质量、覆盖、泄漏与部署条件漂移评价矩阵。

### GEN16-E02
复现科学空间聚类 VAE 时，设计多 seed、baseline、label matching、消融与失败报告。

### GEN16-E03
对一个“发现真实语义因素”的声明写证据升级路线：从 traversal 到可识别性假设。

## 解答入口

[[解答 - VAE 的条件、聚类、解耦主张与证据地图]]


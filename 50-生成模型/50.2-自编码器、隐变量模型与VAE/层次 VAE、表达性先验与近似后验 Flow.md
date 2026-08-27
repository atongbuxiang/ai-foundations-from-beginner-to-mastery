---
type: concept
status: verified
area: [generative-models, vae, hierarchical-models, normalizing-flows]
aliases: [Hierarchical VAE, VAE表达性组件]
node_id: GEN-15
prerequisites: ["[[Posterior Collapse、率失真与解码器容量]]", "[[随机变量变换与密度换元]]", "[[Gaussian VAE 的闭式 KL、解码似然与尺度合同]]"]
related: ["[[Normalizing Flow 与可逆密度变换 MOC]]", "[[VAE 的条件、聚类、解耦主张与证据地图]]"]
sources: ["[[S-2020-Su-7574-NVAE]]", "[[S-2020-Vahdat-NVAE]]", "[[S-2021-Su-8404-vMF-VAE]]", "[[S-2018-Davidson-Hyperspherical-VAE]]", "[[S-2021-Su-8475-UniVAE]]"]
exercises: ["[[习题 - 层次 VAE、表达性先验与近似后验 Flow]]"]
solutions: ["[[解答 - 层次 VAE、表达性先验与近似后验 Flow]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-vae-component-responsibility-tree-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 层次 VAE、表达性先验与近似后验 Flow

> [!abstract] 本节主问题
> “更强的 VAE”可能改的是 prior、decoder likelihood、variational posterior、latent hierarchy、architecture 或训练稳定化。它们解决的瓶颈不同。只有先写出新 joint 和新 $q$，才能判断 KL、采样顺序、likelihood estimator 与因果归因如何变化。

## 一、四个可以独立增强的对象

标准 VAE 为

$$
p_\theta(x,z)=p(z)p_\theta(x\mid z),\qquad
q_\phi(z\mid x).
$$

常见增强分别是：

1. **prior**：$p(z)$ 从标准 Gaussian 变为 mixture、learned autoregressive、VampPrior、hyperspherical；
2. **likelihood/decoder**：更适合数据的分布与更强网络；
3. **approximate posterior**：full covariance、mixture、normalizing flow；
4. **hierarchy**：$z=(z_1,\ldots,z_L)$，生成和推断在多尺度分解。

说“用了 flow”仍不够：flow 可能在 posterior、prior 或 generative decoder 中，三者的 density 与成本方向不同。

## 二、层次生成 joint 与采样顺序

一种 top-down hierarchy 是

$$
p_\theta(x,z_{1:L})
=p(z_L)\prod_{\ell=1}^{L-1}
p_\theta(z_\ell\mid z_{\ell+1:L})
\;p_\theta(x\mid z_{1:L}).
$$

祖先采样顺序为

$$
z_L\to z_{L-1}\to\cdots\to z_1\to x.
$$

近似后验可以 bottom-up：

$$
q_\phi(z_{1:L}\mid x)
=q_\phi(z_1\mid x)
\prod_{\ell=2}^Lq_\phi(z_\ell\mid z_{<\ell},x),
$$

也可结合 bottom-up features 与 top-down prior 参数。两种图不相同，ELBO 中的 KL 必须按具体 factorization 推导，不能机械写 $L$ 个独立标准正态 KL。

## 三、层次 ELBO 的条件 KL

若采用与生成条件相匹配的 posterior factorization，可将

$$
\mathcal L
=\mathbb E_q[\log p_\theta(x\mid z_{1:L})]
-\mathrm{KL}(q(z_{1:L}\mid x)\|p(z_{1:L}))
$$

用 chain rule 展开为顶层 KL 加若干条件 KL。示意地：

$$
\mathrm{KL}(q(z_{1:L}\mid x)\|p(z_{1:L}))
=\sum_\ell \mathbb E_{q(z_{>\ell}\mid x)}
\mathrm{KL}\!\left(
q(z_\ell\mid z_{>\ell},x)
\|p(z_\ell\mid z_{>\ell})\right),
$$

但该式只在相应方向的共同 factorization 下成立。索引方向变化时条件集合也变。

## 四、posterior normalizing flow 改了什么

先从 base posterior $z_0\sim q_{0,\phi}(z_0\mid x)$ 出发，经可逆映射

$$
z_k=f_k(z_{k-1};x),\qquad k=1,\ldots,K.
$$

换元公式给

$$
\log q_{K,\phi}(z_K\mid x)
=\log q_{0,\phi}(z_0\mid x)
-\sum_{k=1}^K\log\left|
\det\frac{\partial f_k}{\partial z_{k-1}}\right|.
$$

ELBO 仍为 $\mathbb E_q[\log p(x,z)-\log q(z\mid x)]$，只是 $q$ 更富表达性。它可能缩小 family gap，却增加计算、数值与 amortization 难度；也不自动改变生成 prior。

## 五、表达性 prior 改了什么

若把 $p(z)=\mathcal N(0,I)$ 换成 learned $p_\lambda(z)$，ELBO 的 KL 变为

$$
\mathrm{KL}(q_\phi(z\mid x)\|p_\lambda(z)).
$$

一个更贴合 aggregate posterior 的 prior 可减少 $\mathrm{KL}(q(z)\|p_\lambda(z))$，在相同 rate penalty 下允许更多 MI；但若 prior 训练过拟合、采样昂贵或 density 不可算，原有合同会改变。后验更强与 prior 更强不是替代关系：一个逼近单样本 posterior，一个匹配跨数据 aggregate。

## 六、球面 latent：几何不是装饰

hyperspherical VAE 让 $z$ 位于单位球面 $\mathbb S^{d-1}$，常用 von Mises–Fisher：

$$
q(z\mid x)=\operatorname{vMF}(\mu(x),\kappa(x)),\qquad
p(z)=\operatorname{Unif}(\mathbb S^{d-1}).
$$

若维数 $d$ 和浓度 $\kappa$ 固定，$\mathrm{KL}(q\|p)$ 可与方向 $\mu$ 无关且为正常数。这可防数值 KL 归零，却仍不推出 $I(X;Z)>0$：若 $\mu(x)$ 对所有 $x$ 相同，编码依旧无信息。还必须说明球面参考测度、采样算法与梯度 estimator。

## 七、NVAE：反驳“VAE 天生只能模糊”的案例

[[S-2020-Su-7574-NVAE]]介绍 [[S-2020-Vahdat-NVAE]] 的深层 hierarchical VAE。它同时改变多尺度 latent groups、residual cells、normalization、posterior parameterization、训练稳定性和 likelihood 建模，并在其图像协议下产生高质量样本。

它能支持的结论是：**VAE 家族在足够强的架构与训练下不被简单 MSE 模糊叙事所限制**。它不能支持“某一个组件单独造成全部提升”，因为改动是组合的；也不能直接外推到文本、音频或任意数据规模。

## 八、UniVAE 与长度泄漏

[[S-2021-Su-8475-UniVAE]]以 Transformer attention mask 和多个层级的 CLS latent 构造文本 VAE，并明确讨论 length leakage：若 decoder 从输入形状、mask 或位置直接获知原句长度，重构任务可被无意简化。

审计文本 VAE 要额外检查：

- encoder/decoder mask 是否泄漏 target token 或长度；
- latent 在每层以何种方式注入；
- posterior collapse 按 token length 如何分层；
- generation 时 EOS/长度分布是否与训练一致。

## 九、选择方法的责任矩阵

| 症状 | 首要怀疑对象 | 合理干预 | 关键对照 |
|---|---|---|---|
| posterior 多峰拟合差 | posterior family | flow/mixture $q$ | per-example optimization |
| aggregate 与 prior 不匹配 | prior | learned/hierarchical prior | MI 与 aggregate KL 分解 |
| 样本模糊 | likelihood/decoder | richer observation model | 同架构同预算消融 |
| 多尺度结构缺失 | hierarchy/architecture | latent groups | group-wise KL/use intervention |
| KL 消失 | objective/dynamics/decoder | warm-up、lagging updates | rate–distortion 与 causal ablation |

## 十、科学空间研读框

[[S-2021-Su-8404-vMF-VAE]]从球面均匀先验与固定正 KL 切入；与[[S-2018-Davidson-Hyperspherical-VAE]]对照后，本节把“KL 不为零”和“有用信息”分开。[[S-2020-Su-7574-NVAE]]负责强层次 VAE 案例，原论文卡负责模型与实验细节。[[S-2021-Su-8475-UniVAE]]负责文本多层 latent 和 length leakage 的开放设计问题。

科学空间的几何解释记为直觉/假说，只有当 manifold、reference measure、density 与实验干预写清时，才升级为可检验模型主张。

## 十一、图：到底改了模型的哪一块

先看图回答：posterior flow、learned prior、hierarchy 与 stronger decoder 分别改变哪条边？哪种改动会直接改变无条件采样程序？

![[00-知识库管理/_assets/figures/generative-models/fig-vae-component-responsibility-tree-v1.svg|900]]

> [!figure] 图 50.2-07　VAE 组件责任树
> 图从 joint 与 inference 两个根分支展开 prior、likelihood、hierarchy 和 posterior family，并为每个分支标出直接收益与新增成本。来源：依据 hierarchical VAE、flow posterior 与 hyperspherical VAE 定义独立绘制。

**怎样读图**：先定位论文改动属于生成 joint 还是推断工具；再判断它改变 likelihood、sampling 或只改变 bound tightness。多个分支同时改动时，结论必须依赖消融。

**图没有证明什么**：树图不对方法优劣排序，也不证明更复杂组件必然提高 likelihood 或感知质量；它只防止责任错配。

## 十二、本节回顾

- prior、likelihood、posterior、hierarchy 是四个可独立改变的对象；
- 层次 joint 决定祖先采样与条件 KL 的正确分解；
- posterior flow 缩小 family gap，但不自动改善生成 prior；
- 固定正 KL 或球面几何不保证互信息和语义；
- NVAE 是“VAE 不必模糊”的存在性反例，不是单组件因果证明；
- 文本 VAE 必须额外审计 mask、长度泄漏和 EOS。

## 十三、练习与独立详解

- [[习题 - 层次 VAE、表达性先验与近似后验 Flow]]
- [[解答 - 层次 VAE、表达性先验与近似后验 Flow]]

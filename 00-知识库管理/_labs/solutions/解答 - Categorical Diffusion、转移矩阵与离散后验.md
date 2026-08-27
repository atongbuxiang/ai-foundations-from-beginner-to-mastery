---
type: solution
status: draft
topic: "[[Categorical Diffusion、转移矩阵与离散后验]]"
exercise: "[[习题 - Categorical Diffusion、转移矩阵与离散后验]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Categorical Diffusion、转移矩阵与离散后验
## A. 识别与复述
### GEN57-A01
$Q_t[i,j]=q(x_t=j\mid x_{t-1}=i)$，每行和为 1。$\bar Q_t=Q_1\cdots Q_t$，故 $q(x_t=\cdot\mid x_0=k)=e_k\bar Q_t$。行向量从左乘，乘法次序不能倒置。
### GEN57-A02
类别 ID 只标识元素，重命名不应改变模型；所以 $|3-2|$ 没有默认距离。结构化核要另给图邻接、序关系、embedding distance 或领域转移成本，并说明这些结构是否固定。
### GEN57-A03
Gumbel-max 用 hard argmax 产生精确 Categorical sample；Gumbel–Softmax 在有限温度下产生 simplex 上的连续松弛；D3PM kernel $Q_t$ 定义多步 Markov corruption。三者分别位于采样表示、梯度松弛、过程定义层。
## B. 手算与建模
### GEN57-B01
$$Q^2=\begin{bmatrix}.66&.34\\.17&.83\end{bmatrix}.$$ 从状态 1 出发，$q(x_2\mid x_0=1)=(.66,.34)$。例如第一项 $.8^2+.2\times.1=.66$。
### GEN57-B02
均匀重采时以概率 $1/K$ 抽回原类，所以改变概率为 $\beta(1-1/K)=.2\times.75=.15$，不是 $.2$。
### GEN57-B03
观测 $x_2=3$ 时权重为 $(.8\times.1,.1\times.1,.1\times.8)=(.08,.01,.08)$，分母 $.17$。后验为 $(8/17,1/17,8/17)$。
## C. 推导与证明
### GEN57-C01
两步时对 $x_1$ 求和得到矩阵乘法。若 $t-1$ 时成立，则 $q(x_t=j\mid x_0=k)=\sum_i(e_k\bar Q_{t-1})_iQ_t[i,j]=(e_k\bar Q_t)_j$，归纳完成。
### GEN57-C02
Bayes 分子由 Markov 性拆为 $(e_k\bar Q_{t-1})_iQ_t[i,j]$，分母是 $(e_k\bar Q_t)_j$。对 $i$ 求和，分子和正好等于分母，因此支持内后验和为 1。
### GEN57-C03
令 $U=\mathbf1\mathbf1^\top/K$，则 $U^2=U$。$Q_t=\alpha_tI+(1-\alpha_t)U$。利用 $I,U$ 可交换且 $U$ 幂等，两个核相乘仍为 $\alpha_1\alpha_2I+(1-\alpha_1\alpha_2)U$；归纳得结论。
## D. 边界、反例与纠错
### GEN57-D01
闭式采样只保证给定 $x_0$ 的某个时刻边缘。若分别独立采 $x_1,x_2$，它们通常不满足指定 $q(x_2\mid x_1)$；逐步链定义了 joint path law，边缘集合不足以确定 coupling。
### GEN57-D02
分母零表示 conditioning event 在模型下不可能。加 $\epsilon$ 会人为改变 conditional distribution 和支持，得到的是数值修补后的近似核，不再是原过程的精确 Bayes 后验。应避免采到不可能事件或显式定义 fallback。
### GEN57-D03
辅助 CE 是额外正则/训练项；通常 $L=L_{ELBO}+\lambda L_{CE}$。只有 $\lambda=0$ 或特殊退化情形才数值相同。即使 population minimizer 可能相容，loss 数值、梯度权重和有限优化仍不同。
## E. AI 迁移
### GEN57-E01
检查 shape 为 $K\times K$、finite、元素 $\ge-\epsilon$、每行和近 1、累计矩阵仍 stochastic、初始 $\bar Q_0=I$、支持事件 posterior 分母正、posterior 非负且和 1、row/column convention 与 sampler 一致。
### GEN57-E02
选 $K\le4,T\le5$，直接矩阵乘法算边缘；逐步 Monte Carlo 比频率；对每个可达 $(x_0,x_t)$ 枚举 $x_{t-1}$ 算 posterior，再从三元组模拟频率条件化核对。固定 seed，并报告 sampling error interval。
### GEN57-E03
记录输出 shape、normalization、是否预测 $x_0$、analytic mixing 公式、terminal prior、辅助 CE 权重、time weighting、是否禁止 impossible transitions、sampling temperature。公平比较还需相同 backbone、参数量、训练 tokens 与 NFE。

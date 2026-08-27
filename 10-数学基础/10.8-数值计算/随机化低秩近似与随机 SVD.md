---
type: concept
status: draft
area: [math/numerical-linear-algebra, math/randomized-linear-algebra]
aliases: [随机 SVD, Randomized SVD, 随机低秩近似]
prerequisites: ["[[奇异值分解]]", "[[定理 - Eckart–Young–Mirsky]]", "[[SVD 算法与谱范数估计]]", "[[标准正交基与 Gram-Schmidt]]"]
related: ["[[函数极限、连续性与收敛模式]]", "[[有效秩]]", "[[随机投影与 Johnson-Lindenstrauss 引理]]", "[[稀疏矩阵计算与存储复杂度]]", "[[实验 - 随机 SVD 的过采样、幂步与概率证书]]"]
sources: ["[[S-2011-Halko-Martinsson-Tropp-随机低秩]]", "[[S-2020-Martinsson-Tropp-随机数值线性代数]]", "[[S-2024-Su-10501-低秩近似之路四ID]]"]
exercises: ["[[习题 - 随机化低秩近似与随机 SVD]]"]
solutions: ["[[解答 - 随机化低秩近似与随机 SVD]]"]
created: 2026-08-15
updated: 2026-08-23
---

# 随机化低秩近似与随机 SVD

> [!abstract] 本章主问题
> 随机 SVD 先用少量随机探针找到 \(A\) 的近似值域，再只在这个小子空间里做确定性 SVD；过采样控制漏掉重要方向的概率，幂步放大谱隙，后验探针把“看起来不错”升级为带失败概率的残差证书。

先用下图回答一个视觉问题：**随机 SVD 怎样把大矩阵压到小空间，过采样 $p$、幂步 $q$ 与独立后验探针分别承担什么职责？**

![[00-知识库管理/_assets/figures/numerical-analysis/fig-randomized-svd-certificate-v2.svg|880]]

> [!figure] 图 10.8.20｜随机值域、$p/q$ 交换与独立概率证书
> A 串联 $\Omega\mapsto Y=A\Omega\mapsto Q=\operatorname{orth}(Y)\mapsto B=Q^TA$ 与小型 SVD，并区分 range capture 和 rank-$k$ truncation 两层误差；B 用成对谱柱定性表示幂步把奇异值权重变为 $\sigma_i^{2q+1}$，同时列出 $\ell=k+p$、过采样保险方向、额外 $A/A^T$ 数据遍历、重正交与 seed/pass 记录；C 用未参与构造 $Q$ 的新 Gaussian 探针形成 $(I-QQ^T)A\omega_j$，再把最大探针 residual 转成带失败概率的后验上界。来源：独立绘制；理论接口参考 Halko–Martinsson–Tropp 与 Martinsson–Tropp；生成脚本：[[plot_numerical_large_scale_v2.py]]；谱柱为定性示意，无随机种子。

**怎样读图。** A 先把算法拆成“找近似值域”和“在小空间中做确定性截断”，两类误差不可混为一谈；B 再把 $p$ 解释为降低漏掉重要方向的尾部风险，把 $q$ 解释为用更多 pass 放大谱隙，并在每次 $A/A^T$ 作用之间维持正交性；C 最后用一组 fresh validation probes 检查算子 residual，明确 norm、探针数与 failure probability，再补充 Frobenius/任务损失。

**适用边界（图没有证明什么）。** 谱柱不表示某个数据集的定量误差曲线，期望界也不是单次成功保证。$p=0$ 即使随机矩阵几乎必然满秩，也可能有严重尾部风险；$q$ 增大并非免费，还增加数据遍历与舍入损失。独立探针证书依赖探针分布、归一化和概率常数，不能用构造 $Q$ 的同一 sketch 自我验证，也不能替代下游任务评估。

## 一、学习目标

完成本章后，你应能：

1. 从 Eckart–Young–Mirsky 定理说清最佳 rank-\(k\) 基线；
2. 推导 randomized range finder 和 randomized SVD；
3. 区分“找到近似值域”与“在值域中截断到 rank \(k\)”两层误差；
4. 用 SVD 分块推导确定性投影误差界；
5. 解释过采样 \(p\) 为何降低随机失败与尾部风险；
6. 推导幂方案对奇异值的 \((2q+1)\) 次变换；
7. 区分谱范数、Frobenius 范数和任务损失中的低秩质量；
8. 使用独立随机探针构造后验概率证书；
9. 比较 Gaussian、SRHT、稀疏 sketch、Nyström、CUR/ID 和流式算法；
10. 为 PCA、LoRA、激活压缩和大模型矩阵分析设计端到端验收。

> [!question] 初学者读完必须能回答
> 1. Randomized range finder 与随后 rank-$k$ 截断分别解决什么问题？
> 2. 为什么 $Y=A\Omega$ 能以高概率捕获主值域？
> 3. 过采样 $p$ 为什么主要降低失败尾部风险，而不只是增加维数？
> 4. 幂步为什么把奇异值权重提升为 $\sigma_i^{2q+1}$？
> 5. $q$ 增大为何会增加 data pass、通信和有限精度风险？
> 6. 独立 Gaussian 探针怎样给 $\|(I-QQ^T)A\|$ 建立后验概率证书？
> 7. 为什么谱范数、Frobenius 误差和下游任务损失必须分别报告？

## 二、问题：不求完整 SVD，只求主要子空间

给定

$$
A\in\mathbb R^{m\times n},
$$

目标是构造 rank 不超过 \(k\) 的

$$
A_k^{\mathrm{approx}}=U_k\Sigma_kV_k^T
$$

使

$$
\|A-A_k^{\mathrm{approx}}\|
$$

尽量小，而不付出完整稠密 SVD 的全部代价。

若

$$
A=U\Sigma V^T,\qquad
\sigma_1\ge\cdots\ge\sigma_r\ge0,
$$

Eckart–Young–Mirsky 给出最优基线：

$$
\min_{\operatorname{rank}(B)\le k}\|A-B\|_2=\sigma_{k+1},
$$

$$
\min_{\operatorname{rank}(B)\le k}\|A-B\|_F
=
\left(\sum_{j>k}\sigma_j^2\right)^{1/2}.
$$

随机算法不是击败这个下界，而是用较低数据访问成本逼近它。

## 三、两阶段视角

低秩近似可拆为：

1. **Stage A：找到值域**

   构造正交基 \(Q\in\mathbb R^{m\times \ell}\)，使

   $$
   A\approx QQ^TA.
   $$

2. **Stage B：在小空间中分解**

   令

   $$
   B=Q^TA\in\mathbb R^{\ell\times n},
   $$

   对 \(B\) 做 SVD，再提升左奇异向量。

随机性主要发生在 Stage A；Stage B 可以完全确定。

## 四、随机值域寻找器

取目标秩 \(k\)，过采样 \(p\)，令

$$
\ell=k+p.
$$

生成 Gaussian 测试矩阵

$$
\Omega\in\mathbb R^{n\times\ell},
\qquad \Omega_{ij}\overset{\mathrm{iid}}{\sim}\mathcal N(0,1).
$$

计算

$$
Y=A\Omega
$$

并正交化：

$$
Y=QR.
$$

于是 \(Q\) 张成随机线性组合 \(A\omega_j\) 所覆盖的子空间。

### 4.1 为什么随机组合会偏向主方向

代入 SVD：

$$
Y=U\Sigma V^T\Omega.
$$

Gaussian 分布对正交变换不变，所以

$$
\widetilde\Omega=V^T\Omega
$$

仍是 Gaussian。第 \(i\) 个左奇异方向 \(u_i\) 的随机系数被 \(\sigma_i\) 缩放：大奇异值方向自然在 \(Y\) 中更突出。

### 4.2 直观上为什么需要 \(\ell>k\)

只取 \(\ell=k\) 时，随机矩阵在主右奇异子空间中的投影虽然以概率 \(1\) 可逆，却可能接近奇异；某个重要方向系数过小就会放大误差。额外 \(p\) 列给主子空间提供冗余观测，也更好地吸收谱尾。

## 五、从 \(Q\) 得到随机 SVD

计算

$$
B=Q^TA.
$$

对小矩阵做

$$
B=\widetilde U\Sigma V^T.
$$

则

$$
QB=(Q\widetilde U)\Sigma V^T,
$$

所以 \(Q\widetilde U\) 是原空间中的近似左奇异向量。最终只保留前 \(k\) 项：

$$
\boxed{
A\approx
(Q\widetilde U_k)\Sigma_kV_k^T.}
$$

### 5.1 两种误差不要混为一谈

值域投影误差：

$$
E_{\mathrm{range}}=\|(I-QQ^T)A\|.
$$

最终 rank-\(k\) 误差：

$$
E_k=\|A-(Q\widetilde U_k)\Sigma_kV_k^T\|.
$$

前者衡量 \(Q\) 是否捕获 \(A\) 的整体重要值域；后者还包含在 \(\ell\) 维空间中截断到 \(k\) 维的误差。实现和实验应明确报告哪一个。

## 六、确定性误差骨架：随机性只进入一个耦合项

把 SVD 按目标秩分块：

$$
A=
\begin{bmatrix}U_1&U_2\end{bmatrix}
\begin{bmatrix}\Sigma_1&0\\0&\Sigma_2\end{bmatrix}
\begin{bmatrix}V_1^T\\V_2^T\end{bmatrix}.
$$

定义

$$
\Omega_1=V_1^T\Omega,\qquad
\Omega_2=V_2^T\Omega.
$$

若 \(\Omega_1\) 满行秩，则典型确定性界为

$$
\boxed{
\|(I-P_Y)A\|^2
\le
\|\Sigma_2\|^2
+
\|\Sigma_2\Omega_2\Omega_1^\dagger\|^2,
}
$$

其中谱范数或 Frobenius 范数可分别使用。

第一项是不可避免的最佳 rank-\(k\) 谱尾；第二项描述随机探针把尾部方向混入主子空间坐标的程度。过采样改善 \(\Omega_1^\dagger\) 的典型条件性。

## 七、Gaussian 期望界怎样阅读

对 \(p\ge2\)，一个经典谱范数期望界可写为

$$
\mathbb E\|(I-QQ^T)A\|_2
\le
\left(1+\sqrt{\frac{k}{p-1}}\right)\sigma_{k+1}
+
\frac{e\sqrt{k+p}}{p}
\left(\sum_{j>k}\sigma_j^2\right)^{1/2}.
$$

这条式子的教学价值大于常数本身：

- 第一部分跟最佳谱误差 \(\sigma_{k+1}\) 同阶；
- 第二部分受整个 Frobenius 谱尾影响；
- \(p\) 增大时两部分的随机惩罚下降；
- 谱尾慢衰减时，一遍 range finder 可能仍不够接近最优。

> [!warning] 期望不等于单次保证
> 期望界不能排除某个 seed 的坏结果。生产验收要看分位数/失败率，或用独立后验探针检查本次输出。

## 八、幂方案：用数据遍历换谱分离

当

$$
\sigma_k\approx\sigma_{k+1}
$$

或谱尾缓慢衰减，改用

$$
Y=(AA^T)^qA\Omega.
$$

代入 SVD：

$$
(AA^T)^qA
=
U\Sigma^{2q+1}V^T.
$$

于是相对谱比从

$$
\frac{\sigma_j}{\sigma_i}
$$

变为

$$
\left(\frac{\sigma_j}{\sigma_i}\right)^{2q+1}.
$$

若比值小于 \(1\)，幂次会迅速压低弱方向。

### 8.1 稳定实现不能显式形成幂

使用交替乘：

$$
Y_0=A\Omega,
$$

每轮

$$
Z_t=A^TQ_{t-1},\qquad
\widehat Q_t=\operatorname{orth}(Z_t),
$$

$$
Y_t=A\widehat Q_t,\qquad
Q_t=\operatorname{orth}(Y_t).
$$

中间重正交很重要；否则小奇异方向可能在浮点舍入中提前消失。若 \(A\) 和 \(A^T\) 各算一次记作一次 pass，则幂参数 \(q\) 通常需要约 \(2q+1\) 次算子作用。

### 8.2 幂步的根效应

在幂变换矩阵上得到的误差，映回原问题时大致取 \(1/(2q+1)\) 次方。它解释了为什么少数幂步常显著有效，同时也提醒我们：增加 \(q\) 有递减收益，却线性增加数据遍历和通信。

## 九、谱范数、Frobenius 范数与任务误差

### 9.1 谱范数

$$
\|A-\widehat A_k\|_2
$$

控制最坏单位输入方向上的放大误差，适合算子近似、稳定性和 adversarial 方向。

### 9.2 Frobenius 范数

$$
\|A-\widehat A_k\|_F^2
$$

累计所有元素/奇异方向能量，常适合 PCA 方差解释和平均重构。

### 9.3 下游任务

即使 Frobenius 误差小，被舍弃的一个弱能量方向仍可能对标签关键；反之，矩阵误差稍大但任务输出不敏感，也可能足够。AI 评估至少应同时报告矩阵误差、子空间角和下游指标。

## 十、后验随机证书

设

$$
R=(I-QQ^T)A.
$$

对固定的 \(R\)，再独立生成 \(r\) 个 Gaussian 向量 \(\omega^{(i)}\)。对任意 \(\alpha>1\)，有概率至少

$$
1-\alpha^{-r}
$$

满足

$$
\boxed{
\|R\|_2
\le
\alpha\sqrt{\frac2\pi}
\max_{i=1,\ldots,r}\|R\omega^{(i)}\|_2.}
$$

若取 \(\alpha=10,r=5\)，名义失败概率不超过 \(10^{-5}\)。

### 10.1 为什么验证探针必须独立

若用构造 \(Q\) 的同一批 \(\Omega\) 验证，算法已经针对这些方向拟合，估计会产生选择偏差。训练/构造随机性与认证随机性应分离，并分别记录 seed。

### 10.2 固定秩与固定容差

- fixed-rank：预先给 \(k,p,q\)，输出指定大小；
- fixed-tolerance：逐块扩展 \(Q\)，用后验证书判断何时满足

  $$
  \|(I-QQ^T)A\|_2\le\tau.
  $$

后者更贴近误差合同，但需要安全停止、最大秩和失败概率预算。

## 十一、复杂度与数据访问

对稠密 \(m\times n\) 矩阵，一遍 Gaussian range finder 的主成本约为

$$
O(mn\ell)
$$

用于 \(A\Omega\)，加上

$$
O(m\ell^2)
$$

用于正交化。形成 \(B=Q^TA\) 再遍历一次 \(A\)，小矩阵分解远便宜于完整 SVD，前提是 \(\ell\ll\min(m,n)\)。

对稀疏矩阵，乘法主成本约

$$
O(\operatorname{nnz}(A)\ell),
$$

但不能忽略 SpMM 的格式、内存和并行负载。

### 11.1 pass 比 FLOP 更重要的场景

当 \(A\) 位于磁盘、对象存储、网络或分布式 shard 时，完整扫描一次数据可能比额外局部 FLOP 更贵。此时算法应显式报告：

- 对 \(A\) 的 pass 数；
- 对 \(A^T\) 的可用性；
- 通信轮数和字节；
- 中间 sketch 的尺寸；
- 是否可边读边累计。

## 十二、结构化与稀疏 sketch

Gaussian \(\Omega\) 理论干净、旋转不变，但生成和稠密乘法可能昂贵。替代包括：

| sketch | 主要优点 | 主要代价/假设 |
|---|---|---|
| SRHT/随机 Fourier | 乘法可快速变换 | 维度、padding、coherence 与实现约束 |
| Rademacher | 只需 \(\pm1\) | 常数和尾界与 Gaussian 不同 |
| CountSketch/稀疏嵌入 | 输入稀疏时便宜 | 可能需要更大 sketch 维数 |
| leverage score 采样 | 针对重要行/列 | score 本身需估计，易循环依赖 |

不能把 Gaussian 定理的常数和失败概率原封不动套到另一种 sketch；应引用相应嵌入定理。

## 十三、Nyström、CUR 与 ID

### 13.1 Nyström

对 PSD \(A\succeq0\)，选取 sketch \(S\)，可构造

$$
C=AS,\qquad W=S^TAS,
$$

$$
\widehat A=CW^\dagger C^T.
$$

它保留对称 PSD 结构，常用于核矩阵。

### 13.2 CUR

选择原矩阵的列 \(C\) 和行 \(R\)：

$$
A\approx CUR.
$$

优势是因子具有原始特征/样本语义；代价是选择质量、缩放和中间 \(U\) 的稳定性。

### 13.3 Interpolative decomposition

ID 用真实列子集表达其余列：

$$
A\approx A(:,J)X.
$$

它比抽象奇异向量更可解释，并可由 QRCP 或随机预压缩加速。详见[[S-2024-Su-10501-低秩近似之路四ID]]。

## 十四、单遍、流式与分布式

若不能第二次访问 \(A\)，可以在读取数据时累计多个 sketch，例如同时维护近似值域和共值域信息，再通过小型方程恢复核心矩阵。这会引入额外条件性和统计误差。

流式算法的合同应包括：

- 插入流还是 turnstile 更新；
- 行流、列流还是任意条目流；
- 内存上限；
- 是否允许重放；
- 漂移下是否需要遗忘；
- sketch 合并是否与分布式归约兼容。

## 十五、有限精度与失效模式

### 15.1 慢衰减谱

若谱没有清晰低秩结构，\(\sigma_{k+1}\) 本来就大，任何 rank-\(k\) 方法都无法给出小谱误差。此时算法失败不是随机性失败，而是问题不具有目标结构。

### 15.2 幂步中的数值秩丢失

\(\Sigma^{2q+1}\) 放大谱隙，也放大动态范围；不重正交会使弱但仍需保留的方向跌出浮点分辨率。

### 15.3 小矩阵也会病态

\(B=Q^TA\)、Nyström 的 \(W\) 或单遍恢复方程可能病态。随机降维不免除条件数、数值秩和稳定求解检查。

### 15.4 可复现与独立性

固定 seed 用于调试复现；跨多个 seed 报告中位数、分位数和最坏值用于评估算法；独立 seed 用于后验认证。三种用途不要混成一个“设了随机种子所以可靠”。

## 十六、AI 接口

### 16.1 大规模 PCA

对中心化数据 \(X\)，随机 SVD 可近似主成分。需要额外验收：

- 中心化能否流式/分布式一致完成；
- explained variance 与重构误差；
- 子空间角而非逐个向量符号；
- 新样本上的投影稳定性。

### 16.2 LoRA 与低秩适配

随机 SVD 可用于分析预训练权重、梯度或更新的有效子空间，也可初始化/压缩低秩因子。但“更新矩阵近似低秩”是数据与任务假设，不由 LoRA 参数化本身证明。

### 16.3 激活与 KV/注意力压缩

对激活矩阵做在线低秩近似时，pass、延迟和误差传播比离线 Frobenius 最优更重要；动态序列和分布漂移还要求更新子空间。

### 16.4 核与注意力近似

Nyström 或随机特征可降低核/注意力矩阵成本，但 softmax、mask、非负性和归一化会改变简单线性低秩误差到最终输出误差的传递。

### 16.5 分布式训练诊断

随机 sketch 可低成本估计梯度协方差、激活谱和权重更新秩。应把通信合并性质、局部 seed、全局归约与概率证书一起设计。

## 十七、算法选择表

| 场景 | 建议起点 |
|---|---|
| 中等稠密矩阵，需全部奇异向量 | 确定性 SVD |
| 巨大矩阵，只需前 \(k\)，谱衰减较快 | randomized SVD，\(p\approx5\sim10,q=0\) 起步 |
| 谱衰减慢，允许多遍数据 | 加 \(q=1,2\) 并每遍重正交 |
| PSD 核矩阵，需要保 PSD | Nyström |
| 因子需对应真实列/行 | ID/CUR |
| 稀疏输入且 sketch 成本敏感 | 稀疏嵌入或 Gaussian SpMM 对照 |
| 只能单遍/流式 | 单遍双 sketch，并额外检查核心恢复条件性 |
| 固定误差合同 | block 自适应 range finder + 独立后验探针 |

## 十八、实验与验收

配套实验：[[实验 - 随机 SVD 的过采样、幂步与概率证书]]。

最低报告项：

| 类别 | 必报量 |
|---|---|
| 数据 | \(m,n\)、奇异值谱/来源、稀疏度、dtype |
| 参数 | \(k,p,q\)、sketch 类型、正交化、seed |
| 资源 | pass、matmul/SpMM、内存、通信、总时间 |
| 误差 | 投影/最终 rank-\(k\)，谱/Frobenius，除以最佳误差 |
| 稳定性 | \(\|Q^TQ-I\|\)、小问题条件数、真残差 |
| 随机性 | 多 seed 分位数、失败定义、独立后验概率 |
| AI | 下游质量、延迟/吞吐与分布外复查 |

## 十九、常见误区

> [!failure] 误区 1：随机算法只给经验结果
> 它既有确定性误差骨架，也有概率尾界和后验认证；随机不等于不可证明。

> [!failure] 误区 2：\(p=0\) 已有概率 \(1\) 满秩，所以足够
> “几乎处处可逆”不保证良态，也不控制单次误差尾部。

> [!failure] 误区 3：幂步越多越好
> 更多 pass、通信和动态范围会抵消收益；有限精度还要求重正交。

> [!failure] 误区 4：Frobenius 误差小就保留了任务信息
> 低能量但高预测价值的方向可能被删除。

> [!failure] 误区 5：用训练 sketch 验证自己
> 自适应选择造成乐观偏差；认证探针必须独立。

## 二十、自检清单

- [ ] 我能从 \(Y=A\Omega\) 推导 \(Q,B\) 和最终随机 SVD。
- [ ] 我能解释 \(p\) 与 \(q\) 分别解决什么问题。
- [ ] 我能区分 range error 与 final rank-\(k\) error。
- [ ] 我知道最佳误差由 \(\sigma_{k+1}\) 或谱尾给出。
- [ ] 我会把 pass 数和正交成本纳入复杂度。
- [ ] 我能写出独立 Gaussian 后验上界和失败概率。
- [ ] 我不会把 Gaussian 保证直接转移给任意 sketch。
- [ ] 我会同时检查矩阵误差、子空间和 AI 下游任务。

## 二十一、本章小结

随机化低秩算法的关键抽象是：用随机探针把大矩阵的主要值域压进一个小而可靠的子空间，再用确定性数值线性代数完成分解。过采样降低漏方向风险，幂步改善慢衰减谱，重正交保护有限精度，独立探针提供后验概率证书。真正成熟的应用不会只说“用了 randomized SVD”，而会明确 \(k,p,q\)、pass、误差范数、多 seed 尾部、认证失败概率和下游任务边界。

## 参考来源

- [[S-2011-Halko-Martinsson-Tropp-随机低秩]]
- [[S-2020-Martinsson-Tropp-随机数值线性代数]]
- [[S-2024-Su-10501-低秩近似之路四ID]]
- [PyTorch pca_lowrank 官方文档](https://docs.pytorch.org/docs/stable/generated/torch.pca_lowrank.html)
- [scikit-learn randomized_svd 官方文档](https://scikit-learn.org/stable/modules/generated/sklearn.utils.extmath.randomized_svd.html)

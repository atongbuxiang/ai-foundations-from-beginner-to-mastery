---
type: moc
status: active
area: [labs]
related: ["[[数学基础完整课程地图与掌握标准]]", "[[练习与测验 MOC]]", "[[数学基础 MOC]]"]
created: 2026-08-14
updated: 2026-08-28
---

# 推导与实验 MOC

## 作用

这里保存“我能够重新得到什么”“我实际验证了什么”和“我能否脱离正文独立完成”。概念笔记可以引用结论，但完整推导、实验、习题、解答与测验留在本模块。

## 目录约定

```text
00-知识库管理/_labs/
  derivations/    独立数学推导
  experiments/    数值与模型实验
  code/           可复用脚本
  data/           小型、许可明确的数据或数据说明
  exercises/      按节点组织的 A–E 分级习题
  solutions/      与题目分离的完整解答
  assessments/    阶段测验、答题记录与错题复盘
```

练习入口：[[练习与测验 MOC]]。

## 第四章确定性架构审计

- [[00-知识库管理/_labs/code/architecture_sequence_ssm_audit.py]]：ARCH-09—16 的递推、BPTT、门控、ZOH、卷积/scan 与 selective retention；
- [[00-知识库管理/_labs/code/architecture_gnn_audit.py]]：ARCH-17—24 的重标号等变、MPNN、GCN、聚合碰撞、谱平滑、GAT、readout 与 1-WL 反例；
- [[00-知识库管理/_labs/code/architecture_attention_audit.py]]：ARCH-25—32 的 QKV/shape、缩放方差、稳定 softmax、mask、对称性、多头预算、核重排、分母敏感性与 rank 反例；
- [[00-知识库管理/_labs/code/architecture_transformer_audit.py]]：ARCH-33—40 的 block 接线、encoder padding、decoder 因果与 cache、cross-attention、架构家族 mask、ViT patch 与参数/MAC 总账；
- [[00-知识库管理/_labs/code/architecture_position_audit.py]]：ARCH-41—48 的置换等变、绝对位置 ID、sinusoidal 平移、相对位置反例、RoPE、多轴坐标、缩放重映射与长上下文评测总账；
- [[00-知识库管理/_labs/code/architecture_efficient_attention_audit.py]]：ARCH-49—56 的阶段化成本、稀疏边与路径、序列低秩、kernel state、Performer 随机误差、online softmax、MHA/GQA/MQA cache 与 MLA 投影吸收；
- [[00-知识库管理/_labs/code/architecture_moe_audit.py]]：ARCH-57—64 的容量/激活 MAC、路由合同、dispatch/capacity、辅助梯度、loss-free feedback/assignment、专家设计轴、EP payload 与门控证据边界；
- [[00-知识库管理/_labs/code/architecture_capstone_audit.py]]：ARCH-01—64 跨卷复现门，连接图重标号、causal full/cache、RoPE 相对位移、Attention/cache/MoE 成本与尾负载；
- 当前语义：脚本断言已通过，只验证确定性 toy constructions，不替代真实训练、学习验收或论文复现。

第四章累计出口：[[阶段测验 - 表示与模型架构（第四章）]]、[[阶段测验解答 - 表示与模型架构（第四章）]]与[[实验 - 表示与模型架构跨卷累计复现门]]；当前为 `composed / not-attempted`。

## 卷末累计验收

- 总题卷：[[数学基础十卷总验收 - 跨卷理论与 AI 迁移]]；
- 独立详解：[[数学基础十卷总验收解答 - 跨卷理论与 AI 迁移]]；
- 跨卷计算门：[[实验 - 数学基础十卷跨章累计复现门]]，覆盖 linear-Gaussian-information、quadratic optimization/discrete dynamics 与 circle geometry/RKHS/numerical conditioning；
- 覆盖：十卷 150 节点的跨卷接缝；只有十份分卷验收均通过后才可用于总认证；
- 当前语义：`composed / not-attempted`，不构成 verified 证据。

- 题卷：[[阶段测验 - 几何、泛函分析、核与算子基础（10.10）]]；
- 独立详解：[[阶段测验解答 - 几何、泛函分析、核与算子基础（10.10）]]；
- 卷级 ID：`GEO-CUM-01`；
- 计算门：[[实验 - 几何、泛函与算子累计复现门]]，覆盖sphere retraction/rotation covariance、Hilbert projection/compact spectrum/kernel effective dimension与Poisson cutoff的多topology误差；
- 覆盖：GEO-01—08，20分钟口试、210分钟100分闭卷、评分者nonce随机计算轨道、48小时换例与14天迁移；
- 当前语义：材料`regression-passed`、个人`not-attempted`，由[[geometry_functional_cumulative_contract_audit.py]]复核，不构成verified证据。

- 题卷：[[阶段测验 - 线性代数（10.2）]]；
- 独立详解：[[阶段测验解答 - 线性代数（10.2）]]；
- 卷级 ID：`LA-CUM-01`；
- 计算门：[[实验 - 线性代数累计复现门]]，覆盖病态basis/quotient/projector、Jordan transient/SVD tail与attention-softmax rank/vec identity；
- 覆盖：LA-01—24，20分钟口试、240分钟100分闭卷、`attempt_id + scorer nonce`随机计算轨道、盲参数干预、48小时换例与14天迁移；
- 当前语义：材料`regression-passed`、个人`not-attempted`，由[[linear_algebra_cumulative_contract_audit.py]]复核，不构成verified证据。

- 题卷：[[阶段测验 - 矩阵分析（10.3）]]；
- 独立详解：[[阶段测验解答 - 矩阵分析（10.3）]]；
- 卷级 ID：`MA-CUM-01`；
- 计算门：[[实验 - 矩阵分析累计复现门]]，覆盖positive margin/Cholesky/condition、gap/angle/pseudospectrum与sign/polar/Fréchet/structured condition；
- 覆盖：MA-01—16，20分钟口试、270分钟100分闭卷、`attempt_id + scorer nonce`随机计算轨道、盲参数干预、48小时换机制与14天迁移；
- 当前语义：材料`regression-passed`、个人`not-attempted`，由[[matrix_analysis_cumulative_contract_audit.py]]复核，不构成verified证据。

- 题卷：[[阶段测验 - 多元微积分、矩阵微分与自动微分（10.4）]]；
- 独立详解：[[阶段测验解答 - 多元微积分、矩阵微分与自动微分（10.4）]]；
- 卷级 ID：`CALC-CUM-01`；
- 计算门：[[实验 - 微积分、矩阵微分与自动微分累计复现门]]，覆盖Taylor/finite difference、JVP/VJP/HVP、implicit solve与spectral gap；
- 覆盖：CALC-01—16，20分钟口试、270分钟100分闭卷、`attempt_id + scorer nonce`随机轨道、盲参数干预、48小时换机制与14天迁移；
- 当前语义：材料`regression-passed`、个人`not-attempted`，由[[calculus_ad_cumulative_contract_audit.py]]复核，不构成verified证据。

- 题卷：[[阶段测验 - 数学语言、逻辑与证明（10.1）]]；
- 独立详解：[[阶段测验解答 - 数学语言、逻辑与证明（10.1）]]；
- 计算门：[[实验 - 数学语言、逻辑与证明累计复现门]]，覆盖量词换序的有限反模型、递推误差的闭式—界—极限—精度证书与Attention rank增长制度；
- 覆盖：MATH-01—08，100分笔试加一个评分者随机指定计算轨道；
- 当前语义：`composed / not-attempted`，不构成verified证据。

- 题卷：[[阶段测验 - ODE、动力系统与 SDE（10.9）]]；
- 独立详解：[[阶段测验解答 - ODE、动力系统与 SDE（10.9）]]；
- 计算门：[[实验 - ODE、动力系统与 SDE 累计复现门]]，覆盖 continuous/discrete stability、解析 FPE–PF–CNF density ledger 与 Brownian/Itô/reverse-score coefficient；
- 覆盖：DYN-01—12；DYN-CUM-01 使用 20 分钟口试、100 分笔试、评分者随机计算轨道与 48 小时/14 天保持性门；
- 当前语义：材料 `regression-passed`、个人 `not-attempted`，由[[dynamics_cumulative_contract_audit.py]]回归，不构成 verified 证据。

- 题卷：[[阶段测验 - 优化与凸分析（10.7）]]；
- 独立详解：[[阶段测验解答 - 优化与凸分析（10.7）]]；
- 计算门：[[实验 - 优化与凸分析累计复现门]]，覆盖 strict-saddle stable manifold/perturb escape、nonconvex PL 与 scale-symmetry raw sharpness；
- 覆盖：OPT-01—16，100 分笔试加一个随机指定计算轨道；
- 当前语义：`composed / not-attempted`，不构成 verified 证据。

- 题卷：[[阶段测验 - 信息论与统计学习接口（10.6）]]；
- 独立详解：[[阶段测验解答 - 信息论与统计学习接口（10.6）]]；
- 计算门：[[实验 - 信息论累计复现门]]，以 scorer nonce 指定 Bernoulli–Hamming rate–distortion、task/nuisance bottleneck 或 KT prequential 深入轨，并要求未见参数预测、output/SVG/hash、48 h 与 14 d 证据；独立回归见[[information_cumulative_contract_audit.py]]；
- 覆盖：INFO-01—10，15 分钟口试、100 分闭卷、盲参数轨与延迟迁移门；
- 当前语义：材料 `regression-passed`、个人 `not-attempted`，不构成 verified 证据。

- 题卷：[[阶段测验 - 概率论与数理统计（10.5）]]；
- 独立详解：[[阶段测验解答 - 概率论与数理统计（10.5）]]；
- 计算门：[[实验 - 概率统计累计复现门]]，以 scorer nonce 指定 repeated-sampling coverage、rare-event IS 或双峰 MCMC 深入轨，并要求未见参数预测、output/hash、48 h 与 14 d 证据；独立回归见[[probability_cumulative_contract_audit.py]]；
- 覆盖：PROB-01—20，100 分笔试加一个随机指定计算轨道；
- 当前语义：`composed / not-attempted`，不构成 verified 证据。

- 题卷：[[阶段测验 - 数值计算与数值线性代数（10.8）]]；
- 独立详解：[[阶段测验解答 - 数值计算与数值线性代数（10.8）]]；
- 组合计算门：从[[实验 - 条件估计、误差传播与可信停止]]、[[实验 - 稳定归约、点积消去与混合精度累加]]、[[实验 - 三精度迭代改进与 GMRES-IR 边界]]中由评分者随机指定一项；
- 覆盖：NUM-01—20，100 分笔试加一项随机指定的实验复现门；
- 当前语义：测验已组卷但尚未作答，不构成 verified 证据。

## 已完成

1. [[实验 - 不同奇异值谱下的有效秩比较]]：同一谱上不同有效秩定义的敏感度。
2. [[实验 - 谱间隙与特征向量稳定性]]：谱值稳定与谱方向稳定的分离。
3. [[实验 - Gram-Schmidt 与 QR 的正交性误差]]：重构正确不保证计算出的基仍标准正交。
4. [[实验 - 正定边界、条件数与 Cholesky pivot]]：用解析矩阵族连接小特征值、病态性与消元主元。
5. [[实验 - 稳定非正规系统的矩阵指数瞬态]]：相同稳定特征值下，严格上三角耦合怎样产生有限时间传播峰值。
6. [[实验 - Newton-Schulz 极分解的条件数效应]]：局部二次收敛、病态矩阵的奇异值抬升期与秩亏不恢复边界。
7. [[实验 - 矩阵符号函数的谱分割与非正规敏感性]]：固定特征值下，斜不变子空间怎样同时放大 sign、Fréchet 导数和统一缩放 Newton 的前期步数。
8. [[实验 - 浮点求和次序与灾难性消去]]：FP32 半 ulp 吸收、求和树/补偿与平方根差稳定改写。
9. [[实验 - 小残差、大前向误差与条件数]]：两个解析 $2\times2$ 族分离残差、前向误差、条件放大与分量尺度。
10. [[实验 - 等价公式不等价稳定]]：固定精确问题，比较二次根消去、log-sum-exp 溢出与稳定改写。
11. [[实验 - 选主元、后向误差与迭代改进]]：在条件数近似不变的系统族中隔离选主元效应，再扫描低精度 LU 加高精度残差的修复边界。
12. [[实验 - Householder 符号、Givens 缩放与 QR 正交性]]：隔离反射符号消去、旋转极端尺度与正交化条件数放大三类机制。
13. [[实验 - 正规方程、QR 与截断 SVD 的稳定性]]：扫描条件数平方失效边界，分离原始残差与参数误差，并展示 TSVD 的残差—解范数取舍。
14. [[实验 - 谱间隙、移位与 Rayleigh 商迭代收敛]]：验证幂法谱比、反幂移位距离与对称 RQI 的局部三次律，并保留等距移位停滞反例。
15. [[实验 - Hessenberg 约化、移位与 QR deflation]]：同时检查正交相似不变量、三种移位的 deflation 速度与结构化 QR 的二次单步成本。
16. [[实验 - Lanczos Ritz 收敛、残差与正交性]]：比较两端 Ritz 收敛、直接/廉价残差和 9 位模拟下的重正交效果。
17. [[实验 - Arnoldi 非正规性、重正交与重启]]：验证一般 Hessenberg 投影残差、一次/二次 MGS 和保留目标信息的短重启。
18. [[实验 - SVD 双对角化、谱范数与随机子空间]]：连接 Householder 结构保持、谱隙控制和随机值域的过采样/幂步。
19. [[实验 - 定常迭代的频率阻尼、谱半径与暂态]]：分离 Poisson 频率平滑、分裂法渐近速度和非正规有限步放大。
20. [[实验 - 预条件的谱重塑、PCG 收敛与成本权衡]]：比较广义谱、真残差轮数与计入块应用后的总工作代理。
21. [[实验 - CG 能量几何、谱聚集与递推残差漂移]]：连接能量最优、谱簇超越条件数界和有限精度真/递推残差分离。
22. [[实验 - GMRES 重启、MINRES 结构与残差最小化]]：比较完整/重启 GMRES 的信息与正交成本，并验证 MINRES 对称不定结构。
23. [[实验 - 稀疏存储、消元填充与并行负载]]：量化索引字节、排序 fill-in 与同 nnz 下的并行尾部负载。
24. [[实验 - 随机 SVD 的过采样、幂步与概率证书]]：分离过采样的 seed 尾部、幂步的 pass 成本与独立后验上界。
25. [[实验 - 条件估计、误差传播与可信停止]]：分离 Jacobian 乘积、一范数条件估计与弱方向的 residual-only 误停。
26. [[实验 - 稳定归约、点积消去与混合精度累加]]：比较顺序/pairwise/补偿归约与 FP16/FP32 accumulator 的误差层。
27. [[实验 - 三精度迭代改进与 GMRES-IR 边界]]：展示低精度因子、残差地板、GMRES 校正与奇异回退。
28. [[实验 - 概率统计累计复现门]]：分离 Wald interval 的重复抽样 coverage、rare-event IS 的 functional-specific ESS/尾部边界，以及同一 mode 初始化导致的低 R-hat 盲区；现已加入 nonce 防挑轨、盲参数 CLI、canonical/干预双 hash 与延迟迁移状态机。
29. [[实验 - ELBO 恒等式、变分族限制与摊销缺口]]：在可枚举二元 latent model 中把 evidence identity 验证到机器精度，并分离 restricted variational family 与 shared encoder 的不同 gap。
30. [[实验 - 信息论累计复现门]]：把解析 rate–distortion frontier、任务相关压缩与 sequence-level prequential codelength 分为三条可复现、不可越界解释的轨道；现已加入 nonce 防挑轨、source/IB/code 盲参数 CLI、canonical/干预 hash 与延迟迁移状态机。
31. [[实验 - 优化与凸分析累计复现门]]：用同一确定性产物分离 strict-saddle 的 exact stable initialization 与扰动逃逸、非凸 PL 解析下界，以及同一 predictor 下的 scale-dependent raw Hessian sharpness。
32. [[实验 - 双曲线性化与非双曲失效]]：以固定时窗二阶轨道误差验收双曲局部线性化，再用同一 pure-imaginary Jacobian 下的向内、中心与向外半径分离证明非双曲一阶证据不足。
33. [[实验 - Lyapunov 度量、LaSalle 与离散能量边界]]：用非正规暂态与定制度量、阻尼振子零导数非静止点，以及 Euler 在 $h=2$ 的能量翻转分离 metric、invariant set 与 continuous/discrete 证书。
34. [[实验 - ODE 阶数、自适应步长与离散梯度审计]]：用解析解验收 Euler/Heun/RK4 observed order、Euler–Heun tolerance–NFE–error tradeoff，以及 $J_h$ 的 finite-difference/discrete-gradient一致性与continuous-gradient离散化差距。
35. [[实验 - 刚性稳定域、隐式追踪与梯度审计]]：恢复RK4负实轴边界，比较explicit/implicit equal-node-error步数，分离A-stable与L-stable fast damping，并核对Backward Euler的discrete implicit gradient。
36. [[实验 - 流映射、Liouville 与随机迹审计]]：用非正规线性流分离方向拉伸与面积收缩，用非线性增广RK4同步验收state/log-density四阶收敛，并精确枚举Rademacher trace estimator的均值、方差与多probe标准误差。
37. [[实验 - 守恒通量、压缩密度与边缘速度审计]]：用周期迎风有限体积验收质量守恒、一阶收敛与CFL失败；用Gaussian压缩核对方差/熵；用conditional velocity回归恢复marginal velocity并验收continuity PDE残差。
38. [[实验 - Brownian 增量、路径粗糙性与时间耦合审计]]：验收Brownian跨时间covariance和独立增量，用同一最细路径嵌套粗化恢复quadratic-variation/total-variation缩放，并分离三种同marginal不同coupling的increment order。
39. [[实验 - Itô 和、SDE 强弱误差与离散梯度审计]]：用左端/对称随机和恢复quadratic-variation correction，在同一nested Brownian path上分离GBM Euler–Maruyama的strong/weak order，并区分同一离散目标的finite-difference门与continuous-gradient refinement gap。
40. [[实验 - Fokker-Planck、概率流与score误差审计]]：用守恒有限体积验收OU FPE的质量与收敛；用Gaussian同边缘SDE/PF ODE分离cross-time law与quadratic variation；独立扫描score bias与exact-score finite-step solver bias。
41. [[实验 - 反向时间、score恒等式与扩散采样误差审计]]：用Gaussian backward conditional验收reverse drift极限，用双峰mixture逐点验证DSM/Tweedie，并将exact-score solver convergence与score、terminal prior、half-coefficient误差地板分账。
42. [[实验 - ODE、动力系统与 SDE 累计复现门]]：用刚性线性系统分离 continuous Lyapunov decay 与四种 finite-step stability/order，用圆周解析热流对齐 FPE current、PF characteristics 与 CNF log-density，再以 stationary OU 分离 Brownian QV、Itô identity、full-score reverse 与 half-score noisy error floor。
43. [[实验 - 度量、紧致性与连续映射审计]]：用 $d_1=|x-y|$ 与 $d_2=|\arctan x-\arctan y|$ 分离 topology 和 completeness，用区间 cover 与 $\ell^2$ basis packing 拆开 compactness 两条件，再以光滑同胚/jump 的最大样本间隙审计 graph-at-scale。
44. [[实验 - 图册、切空间与解码器秩审计]]：用 stereographic transition 验收 chart cycle/导数互逆，用 clean/noisy parabola 分离 local-PCA curvature bias 与 noise floor，再以 regular/collapsed decoder 拆开 full rank、round trip 和 orthogonal projection。
45. [[实验 - 坐标度量、测地能量与球面 Retraction 审计]]：用 polar metric 与 Cartesian polygon 验收同一圆周长度，用同像不同参数曲线分离 length 与 energy，再以 sphere Euler、normalization 和 exact Exp 拆开二阶约束残差、精确可行与三阶点差。
46. [[实验 - Lie 指数、BCH 与群平均等变审计]]：用 SO(2) one-parameter law与生成元二阶差分连接 algebra/group，用 SO(3) 小旋转恢复 naive 二阶与 BCH2 三阶误差，再以 $C_{12}$ Reynolds average把 dense map投影成机器精度等变的circulant map。
47. [[实验 - 完备化、最佳逼近与条件期望投影审计]]：用同一 $c_{00}$ 截断序列分离 $\ell^2$ Cauchy与 $\ell^1$ 非Cauchy，用同一直线分离Hilbert唯一投影与 $\ell^1$ 非唯一平台，再以分片条件均值验收 $L^2$ 正交残差和最佳逼近。
48. [[实验 - 紧性、谱截断与有限截面陷阱审计]]：用compact diagonal与identity tail分离finite-rank可逼近性，用Volterra零特征谱/非零奇异值分离nonnormal amplification，用shift finite sections暴露spectral loss，再以weighted Gaussian-kernel Nyström谱验收quadrature与低秩账本。
49. [[实验 - Gram 正定性、KRR 表示与随机特征近似审计]]：用合法/非法Gram谱分离symmetry与PSD，以sample-row-space投影验收representer机制，对齐$\sigma^2=n\lambda$核对KRR/GP同均值异方差，并以48 draws分离RFF $D^{-1/2}$平均律与单seed非单调。
50. [[实验 - 弱导数、变分残差与解算子频谱审计]]：用$\sqrt{x^2+\varepsilon^2}$的二阶导数保存delta质量，以P1 FEM恢复$L^2/H^1$二阶/一阶收敛，分离element-interior strong residual与Galerkin weak balance，再用Poisson谱截断揭示低模态训练成功与高频OOD相对失败。
51. [[实验 - 有限集合恒等式、幂集增长与数据切分审计]]：在六元素universe上穷举De Morgan、difference、distributivity与symmetric-difference associativity，量化三个错误mutants的偶然通过率，对比$n/n^2/2^n$增长与去重前后empirical mean，并展示row overlap为0时entity overlap仍可达100%。
52. [[实验 - 有限域量词、否定与换序反例审计]]：穷举命题等价式与全部512个$3\times3$ Boolean predicates，计数量词换序的174个系统反例，并以固定成功率趋近1而共同交集恒为0的构造分离pointwise与uniform guarantee。
53. [[实验 - 证明义务、分类覆盖与条件反例审计]]：穷举valid/invalid inference、65536个two-case pairs与512个Boolean relations，分离coverage/disjointness、existence/uniqueness，并以scalar GD exact contraction factor验收step condition的充分性、必要性与strict boundary。
54. [[实验 - 有限映射、逆像恒等式与商上良定义性审计]]：穷举27个3→3函数、1728组集合律检查与65536个四元素relations，量化image交集的180个失败、B4=15个等价关系，并以parity quotient上的4/16规则验收代表元无关性。
55. [[实验 - 归纳覆盖、递归调用与组合计数审计]]：以index reachability分离base/stride coverage，对比Fibonacci naive的21891次调用与21个memo states，完整枚举4096个12-bit strings核对二项计数/容斥，并比较V=4完整树的87380个prefixes与K=3 beam的88次扩展上界。
56. [[实验 - 不等式松弛、等号与数值稳定性审计]]：以Young参数曲线、Cauchy角度、两点指数Jensen gap与LSE dimension/temperature/margin四轨登记slack；完整检查15500个LSE finite-grid pairs，并复现naive exp(1000) overflow与stable 1000.407606。
57. [[实验 - 极限证书、完备性与浮点停滞审计]]：比较$q=.5/.8/.99$达到$10^{-6}$的严格见证20/62/1375，用精确有理Newton列暴露$\mathbb Q$缺失$\sqrt2$，以$x^n$分离固定网格与连续域supremum，并确认binary64在$n=53$把$1+2^{-n}$首次存成1。
58. [[实验 - 增长率、有限窗口与 Attention 成本审计]]：比较log/linear/$n\log n$/quadratic/exponential增长，精确枚举线性与三角循环并恢复1.000000/1.966996斜率，以解析local slope暴露低阶项与loss地板，再在$d=512$下分离projection、pairwise work与score memory，交叉proxy为$T=1024$。
59. [[实验 - 数学语言、逻辑与证明累计复现门]]：穷举65536个$4\times4$ relations得到50625个pointwise、14911个uniform与35714个换序反例；把递推闭式、几何上界、epsilon证书和$O(\log1/\varepsilon)$串联；以fixed $r$与$r=T/4$分离Attention的一次/二次增长制度。
60. [[实验 - 几何、泛函与算子累计复现门]]：在sphere上恢复ambient constraint二阶、normalization retraction相对Exp三阶与rotation covariance；以$c_j=1/j$和$\mu_j=j^{-2}$分离Hilbert projection、compact tail与kernel effective dimension；用Poisson cutoff同时展示$L^2/H^1/strong$误差指数$-2/-1/0$。
61. [[实验 - 数学基础十卷跨章累计复现门]]：用linear-Gaussian posterior/MI分离定理值与估计量，用quadratic flow/GD分离连续稳定与Euler步长域，再在$S^1$上把rotation/retraction、finite Gram/KRR approximation和condition增长纳入同一跨卷证据账。
62. [[实验 - 线性代数累计复现门]]：用病态基分离抽象向量与坐标、以kernel/quotient/projector核对空间不变量，以Jordan/SVD分离谱值、暂态与低秩尾误差，再用attention-softmax与vec合同分离exact rank、numerical rank和非线性边界；canonical及盲参数接口由独立累计审计复核。
63. [[实验 - 矩阵分析累计复现门]]：用SPD边界分离positive margin、condition与Cholesky pivot，以closing eigengap和nilpotent coupling分离谱值、方向与pseudospectrum，再用sign/polar、Fréchet remainder和structured tangent分离involution、isometry、一阶近似与允许扰动；canonical及盲参数接口由独立累计审计复核。
64. [[实验 - 微积分、矩阵微分与自动微分累计复现门]]：以Taylor/finite-difference分离解析余项与浮点地板，用JVP/VJP pairing、HVP和checkpoint代理分离算子相容与程序调度，再以implicit rhs与closing spectral gap分离program dependence、local solve derivative和basis sensitivity；canonical及盲参数接口由独立累计审计复核。

## 后续实验候选

1. FP16/BF16 的 Welford、一遍/两遍方差与 LayerNorm 对照
2. [[实验 - 截断 SVD 的误差与秩]]
3. [[实验 - SVD 在奇异值碰撞附近的梯度]]
4. Newton–Schulz、Muon 五次多项式与 QDWH 的低精度对照
5. matrix sign 的 fp32/bf16、动态缩放与虚轴伪谱实验
6. [[实验 - Attention 矩阵在不同 Mask 下的谱]]
7. [[实验 - 纯 Attention 堆叠的秩退化]]
8. [[实验 - Residual 和 MLP 对秩退化的影响]]

## 可复现要求

- 固定环境、依赖和随机种子；
- 脚本输入输出明确；
- 原始数据与生成数据区分；
- 图表由脚本生成，禁止只手工修改成图；
- 记录失败结果和与假设冲突的现象；
- 结论严格限制在实验设置内。

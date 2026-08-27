---
type: concept
status: verified
area: [training, optimization, soap, evidence]
node_id: TRN-24
aliases: [SOAP Optimizer, Shampoo Adam Eigenbasis]
prerequisites: ["[[Shampoo、逆矩阵根与 Kronecker 预条件]]", "[[Adam 的一阶二阶矩、偏差修正与逐坐标步长]]", "[[Lion、Adafactor 与自适应优化器证据地图]]"]
related: ["[[Muon、Shampoo、SOAP 与隐式曲率关系]]", "[[训练实验协议、事故记录与因果证据地图]]", "[[数据并行、All-Reduce 与全局 Batch 语义]]"]
sources: ["[[S-2025-Vyas-SOAP]]", "[[S-2018-Gupta-Shampoo]]", "[[S-2020-Anil-Scalable-Shampoo]]", "[[S-2018-Shazeer-Stern-Adafactor]]"]
exercises: ["[[习题 - SOAP、二阶混合优化器与成本证据地图]]"]
solutions: ["[[解答 - SOAP、二阶混合优化器与成本证据地图]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-soap-basis-state-evidence-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# SOAP、二阶混合优化器与成本证据地图

> [!abstract] 一句话结论
> SOAP 的核心不是“Shampoo 加 Adam”这句口号，而是把 gradient 投到 Shampoo statistics 的慢变特征基，在该旋转坐标中持续更新 Adam 式 moments，再转回原参数空间。它用更多 state 和 basis machinery 换取较低频 preconditioner refresh 下的稳定性；是否更好必须同时通过算法、数值、系统、调参和统计五道门。

## 一、从 Shampoo eigenbasis 看坐标旋转

对矩阵参数，令左右 statistics eigendecomposition 为

$$
L=Q_L\Lambda_LQ_L^T,\qquad
R=Q_R\Lambda_RQ_R^T.
$$

把 gradient 旋转到当前 preconditioner basis：

$$
\bar G=Q_L^TGQ_R.
$$

若只在这个 basis 中逐元素缩放 $\bar U$，再转回

$$
U=Q_L\bar UQ_R^T,
$$

就能在原空间得到非对角结构 update。旋转本身保持 Frobenius norm（$Q_L,Q_R$ 正交），但逐元素非线性 Adam normalization 与 basis 选择强相关。

## 二、SOAP 的双时间尺度

一种概念性合同是：

1. 每步以 raw/current gradient 更新 $L,R$ 或其 EMA；
2. 每 $K$ 步更新 $Q_L,Q_R$；
3. 每步把 gradient 投到当前 basis；
4. 在 rotated coordinates 更新 Adam-like $m,v$ 与 bias/epsilon；
5. 形成 $\bar U=m/(\sqrt v+\epsilon)$；
6. 转回原坐标，应用 LR、decay 与参数更新。

论文把 half-power Shampoo 与其 eigenbasis 中的 Adafactor 联系起来，再用 full Adam 式 second moments改进稀疏 basis refresh。具体 state transport、初始化、维度大于 2、fallback 和 decay 顺序必须以实现版本为准。

> [!warning] Basis 更新不是无成本改名
> 当 $Q$ 改变时，旧 $m,v$ 是在旧坐标中积累的统计。算法必须定义是旋转 state、重新初始化、还是把旧数值继续解释在新 basis 中。尤其 $v$ 是逐元素平方统计，不像普通向量那样可无损地只乘一个 $Q$。

## 三、为何慢 refresh 会伤 Shampoo、SOAP 想修什么

Shampoo 若很久不更新 eigenvectors/roots，当前 gradient correlation 可能已旋转，旧 preconditioner direction 失配。单纯增大 refresh period 降低计算，却可能损失优化效果。

SOAP 在旧/慢变 basis 中仍每步更新 coordinate-wise second moment，希望吸收 eigenvalue scale 与局部非平稳性。它不消除 basis staleness，而是增加一个更快的 diagonal adaptation timescale。

可检验诊断包括：

$$
\|Q_t^TQ_{t-K}-I\|,
\quad
\frac{\|\operatorname{offdiag}(Q_t^TL_tQ_t)\|}{\|L_t\|},
\quad
\operatorname{RMS}(\bar U),
$$

以及 refresh 前后 direction cosine 和 loss spike。

## 四、退化 eigenvalue 与 basis 不唯一

若 $L$ 有重复/近重复 eigenvalues，对应 eigenspace 内的 $Q_L$ 不唯一，数值 eigensolver 可在小扰动下大幅旋转 basis。Shampoo 只依赖 matrix function $L^{-1/4}$ 时，这种 basis rotation 可相消；但 SOAP 在 basis 中维护逐元素 nonlinear state，可能对选定 eigenvectors 更敏感。

因此要记录 eigen-gap、basis alignment/state transport 和 refresh artifacts，不能只记录 eigenvalues。

## 五、完整 state 与成本账

对 $m\times n$ 参数，可能包含：

- 左右 Gram/EMA：$m^2+n^2$；
- eigenvectors/roots：再约 $m^2+n^2$；
- rotated first/second moments：约 $2mn$；
- parameters、gradients、master weights、temporary rotations；
- block partition 与 distributed shards/replicas。

每步时间分解：

$$
T_{step}=T_{grad}+T_{stats}+T_{rotate}+T_{Adam}
+\mathbf1_{t\bmod K=0}T_{eig}+T_{comm}.
$$

报告 amortized 平均还不够，应给 refresh step 的 tail latency、peak memory 和训练吞吐抖动。

## 六、与 Adam、Adafactor、Shampoo、K-FAC 的边界

| 方法 | 主要结构 | 快状态 | 慢状态/操作 | 不应声称 |
|---|---|---|---|---|
| AdamW | parameter coordinates | $m,v$ | 无 matrix basis | 不等于 curvature inverse |
| Adafactor | row/column factorized second moment | factors/可选 $m$ | 无 eigenspace | 不恢复完整 element second moment |
| Shampoo | tensor mode Gram + roots | statistics | inverse-root refresh | 不等于 exact Hessian |
| SOAP | Shampoo basis + Adam moments | rotated $m,v$ | eigenbasis refresh | 不等于 Shampoo 与 Adam 的简单加和 |
| K-FAC | layer Fisher/GGN Kronecker factors | factor EMA | inverse/eigen refresh | 不等于 gradient Gram Shampoo |

共同出现 Kronecker、rotation 或 gradient second moment，不足以证明它们是同一算法。

## 七、ICLR 2025 证据怎样读

[[S-2025-Vyas-SOAP]]报告在 360M/660M language-model pretraining 和 large-batch regime 中，相对 AdamW 减少迭代与 wall time，并相对 Shampoo 改善。课程将它标为强而有范围的原始经验：

- 模型规模仍远小于所有可能的 frontier training；
- wall time 依 hardware、kernel、block、refresh 与 distributed implementation；
- hyperparameter budget、batch regime、token budget 与 checkpoint selection 必须一起引用；
- 训练 loss/time-to-loss 不自动推出 downstream/generalization 更优；
- 官方代码当前标注 preliminary，未来版本需重新建立 implementation card。

## 八、五道证据门

1. **算法门**：方程、basis/state transport、epsilon、decay、fallback 是否锁定？
2. **数值门**：eigen/root residual、gap、dtype、NaN/repair 与 refresh spike 是否报告？
3. **系统门**：state bytes、peak、FLOPs、通信、tail/average time 是否完整？
4. **调参门**：AdamW/Shampoo/SOAP 是否等额搜索并计失败运行？
5. **统计门**：paired seeds、置信区间、primary metric、checkpoint rule 是否预注册？

只有连续通过五门，才可把“少 iteration”推进为“此平台/预算下 time-to-quality 更好”。

## 九、图：快 Adam state 与慢 Shampoo basis

先看图回答：哪个状态每步更新，哪个状态低频刷新？basis 改变时旧 moments 的语义风险在哪里？

![[00-知识库管理/_assets/figures/training-optimization/fig-soap-basis-state-evidence-v1.svg|900]]

> [!figure] 图 TRN-24　SOAP 的双时间尺度、basis state 与五道证据门
> 左侧展示左右 eigenspace 与 gradient rotation；中间分开每步 Adam moments 和低频 basis refresh，并标出 degenerate eigenspace/state transport；右侧以算法、数值、系统、调参、统计五门限制性能结论。来源：依据 [[S-2025-Vyas-SOAP]] 及其官方 preliminary implementation 独立绘制。

**怎样读图**：先追踪同一个 tensor 在原 basis、rotated basis 和更新 basis 三个坐标中的 shape/state，再评估性能表。

**图没有证明什么**：图不证明 SOAP 普遍优于 AdamW/Shampoo，也不把 paper wall time 外推到另一硬件、batch 或分布式实现。

## 十、60.3 的总出口

学完本卷，应能对任意“二阶/曲率优化器”写出：

$$
\text{curvature object}
\to\text{estimator}
\to\text{structure approximation}
\to\text{numerical solve/root}
\to\text{state clocks}
\to\text{system/evidence}.
$$

下一卷 [[矩阵优化、谱最速下降与 Muon MOC]]会讨论 matrix norm 下的最速方向与 polar/msign；那是由 norm geometry 推出的方向，不能因为也用 matrix functions 就直接称作 K-FAC/Shampoo 曲率等价物。

## 练习与独立解答

- [[习题 - SOAP、二阶混合优化器与成本证据地图]]
- [[解答 - SOAP、二阶混合优化器与成本证据地图]]

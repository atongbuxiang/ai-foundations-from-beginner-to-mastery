---
type: source
status: draft
area: [sources, math/randomized-linear-algebra, math/low-rank]
source_type: survey-paper
title: "Finding Structure with Randomness: Probabilistic Algorithms for Constructing Approximate Matrix Decompositions"
author: "Nathan Halko, Per-Gunnar Martinsson, Joel A. Tropp"
year: 2011
url: "https://doi.org/10.1137/090771806"
accessed: 2026-08-15
source_tier: A
license: "SIAM Review 论文；知识库保存独立摘要、算法映射与链接"
scope_role: established-method-and-boundary
temporal_role: foundational-randomized-nla
aliases: [HMT-2011-Randomized-Low-Rank]
related: ["[[SVD 算法与谱范数估计]]", "[[随机化低秩近似与随机 SVD]]", "[[QR 分解]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Halko–Martinsson–Tropp：随机范围寻找与近似 SVD

> [!abstract] 来源定位
> 该综述把随机低秩分解组织为两阶段：随机采样寻找近似值域 $Q$，再在小矩阵 $B=Q^*A$ 上做确定性分解。SVD 算法章使用它完成路线分流；NUM-20 进一步使用确定性误差骨架、Gaussian 期望界、幂方案和后验概率证书。

## 核心映射

| ID | 已建立方法 | 纳入位置 |
|---|---|---|
| HMT-1 | $Y=A\Omega$、$Y=QR$ 近似捕获 $\mathcal R(A)$ | [[SVD 算法与谱范数估计]]随机路线 |
| HMT-2 | 对 $B=Q^*A$ 做小型 SVD，得到 $A\approx(Q\widetilde U)\Sigma V^*$ | 同上 |
| HMT-3 | oversampling 降低漏掉重要方向的概率 | 参数选择章节 |
| HMT-4 | 慢衰减奇异谱可用 power/subspace iteration 改善，但增加数据 passes | 实验与边界 |
| HMT-5 | 数据移动和 passes 可能比 flop 更重要 | 算法选择表 |
| HMT-6 | $\Sigma_2\Omega_2\Omega_1^\dagger$ 分解最佳谱尾、尾部随机混合与主坐标条件性 | [[随机化低秩近似与随机 SVD]]误差骨架 |
| HMT-7 | 独立 Gaussian 探针可给投影残差建立带失败概率的后验上界 | 同章概率证书与配套实验 |

## 证据边界

- 随机方法返回概率保证和近似，不是精确 SVD 的无条件替代；
- 幂迭代若不在中间重正交化，会在有限精度下丢失弱方向；
- 单次运行必须记录随机种子、oversampling、power steps 与最终残差；
- structured sketch、单遍与自适应变体的具体常数和条件必须回到对应定理，不能直接沿用 Gaussian 保证。

## 生成节点

- [x] [[SVD 算法与谱范数估计]]中的路线分流
- [x] [[随机化低秩近似与随机 SVD]]完整节点

---
type: source
status: active
area: [sources, learning-theory, machine-learning]
source_type: book
title: "Understanding Machine Learning: From Theory to Algorithms"
author: [Shai Shalev-Shwartz, Shai Ben-David]
year: 2014
url: "https://www.cs.huji.ac.il/~shais/UnderstandingMachineLearning/understanding-machine-learning-theory-algorithms.pdf"
accessed: 2026-08-20
source_tier: A
license: "Copyrighted textbook; course notes retain independent summaries, short formulas, theorem pointers, and the official author-hosted link only"
scope_role: backbone
temporal_role: classical-foundation
related: ["[[学习理论 MOC]]", "[[统计学习问题的对象合同]]", "[[数据生成分布与采样假设]]", "[[预测器、假设空间与学习算法]]", "[[损失、总体风险与经验风险]]"]
created: 2026-08-20
updated: 2026-08-20
---

# Understanding Machine Learning: From Theory to Algorithms

> [!abstract] 来源定位
> 本书是学习理论主干教材之一：从统计学习的对象合同出发，逐步进入 ERM、PAC、VC 维、一致收敛、稳定性、压缩、PAC-Bayes 与经典算法。本库用它校准定义与定理条件，但不照搬章节顺序，也不以教材年代较早的深度学习叙述代替后续论文证据。

## 元数据与纳入

- 正式引用：Shalev-Shwartz, S. & Ben-David, S. (2014), *Understanding Machine Learning: From Theory to Algorithms*, Cambridge University Press；
- 作者托管全文：[official PDF](https://www.cs.huji.ac.il/~shais/UnderstandingMachineLearning/understanding-machine-learning-theory-algorithms.pdf)；
- 当前调用者：LT-01—LT-40 的形式骨架，尤其是第一卷、PAC、VC 与替代型泛化理论；
- 证据角色：定义、定理、证明主线与经典反例；
- 版权边界：只记录独立重写的解释、公式推导、页章定位与链接，不在仓库中重新分发原书。

## 课程采用的主干

| 主干 | 本库如何调用 | 还需什么补充 |
|---|---|---|
| 正式学习模型 | 固定 domain、label、distribution、sample、learner、loss、risk | 用现代 AI pipeline 与随机算法补足对象层级 |
| ERM 与可学习性 | 建立 empirical 与 population 的逻辑鸿沟 | 补优化误差、验证集复用和 distribution shift |
| PAC 与 VC | 作为有限样本保证的第一条严格主线 | 补 Rademacher、local complexity 与 neural norms |
| 稳定性、压缩、PAC-Bayes | 展示“容量界并非唯一道路” | 补信息论泛化与现代随机优化结果 |
| 算法专题 | 连接 linear predictor、kernel、boosting、online learning | 补 self-supervised、calibration、conformal 与深度泛化 |

## 定义审计表

| 对象 | 课程记号 | 容易误写之处 |
|---|---|---|
| observation space | $\mathcal Z$，监督学习常取 $\mathcal X\times\mathcal Y$ | 把 feature space 与完整 observation 混为一谈 |
| sample | $S=(Z_1,\ldots,Z_m)$ | 忘记 $S$ 在泛化概率中是随机对象 |
| hypothesis | $h\in\mathcal H$ | 把参数向量与它表示的函数等同 |
| learner | $A:\mathcal Z^m\to\mathcal H$ | 忽略 randomized algorithm 的额外随机种子 |
| loss | $\ell(h,z)$ 或 $\ell(h(x),y)$ | 不说明 reduction、值域和 surrogate/task distinction |
| risk | $R_P(h)=\mathbb E_{Z\sim P}\ell(h,Z)$ | 用一次 test score 冒充总体期望 |

## 课程补严

1. 本书的标准 i.i.d. setting 是起点，不是所有数据管线的默认真理；数据增强、batch negative、主动采样与时间序列都要单列依赖结构。
2. 理论中的 hypothesis 是函数；现代神经网络训练常在参数空间中运行，而同一函数可能有大量参数表示。
3. 对固定 $h$ 的无偏性，不自动推出 data-dependent $h_S$ 的泛化；这正是 uniform convergence、stability 等工具出现的原因。
4. “可学习”是量词明确的数学断言，不等于某次 benchmark 训练成功。
5. 经典定理的价值在于建立条件—结论语言；深度网络的真实解释还需要实证、架构与优化层证据。

## 已生成与后续调用

- [x] [[统计学习问题的对象合同]]：学习问题的六对象合同；
- [x] [[数据生成分布与采样假设]]：$P^m$、i.i.d. 与超出 i.i.d. 的边界；
- [x] [[预测器、假设空间与学习算法]]：函数类与算法分层；
- [x] [[损失、总体风险与经验风险]]：固定预测器无偏性与 data dependence 警告；
- [x] LT-05—LT-16：ERM、PAC、有限类、Occam、NFL 与下界主线；
- [x] LT-17—LT-20：shattering、growth function、Sauer–Shelah 与 VC inequality；
- [x] LT-21—LT-24：基本定理、SRM、多分类维与实值伪维；
- [ ] LT-25—LT-40：随正文进度继续建立 theorem-level claim ledger。

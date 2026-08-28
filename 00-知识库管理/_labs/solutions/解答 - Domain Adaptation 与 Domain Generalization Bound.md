---
type: solution
status: draft
topic: "[[Domain Adaptation 与 Domain Generalization Bound]]"
exercise: "[[习题 - Domain Adaptation 与 Domain Generalization Bound]]"
created: 2026-08-23
updated: 2026-08-28
---
# 解答 - Domain Adaptation 与 Domain Generalization Bound
## A
### LT-DA-A01
UDA 有 source labels/target inputs；semi-DA 另有少量 target labels；DG 无当前 target data；test-time adaptation 部署时更新。四者的允许信息不同。
### LT-DA-A02
$d_{\mathcal H\Delta\mathcal H}=2\sup_{h,h'}|\Pr_s(h\ne h')-\Pr_t(h\ne h')|$；$\lambda=\min_h[R_s(h)+R_t(h)]$。
### LT-DA-A03
domain error测所选 discriminator 的 input/feature separability；proxy $2(1-2\epsilon)$ 近似 discrepancy；target risk还含 source risk、$\lambda$ 与估计误差。
## B
### LT-DA-B01
上界 $=.10+.30/2+.15=.40$。
### LT-DA-B02
$\epsilon=.1$ 时 $d_A=1.6$；$\epsilon=.5$ 时为 0。
### LT-DA-B03
$\Phi$ 同时接收 label/domain gradients；label head最小化 source loss；domain head最小化 domain loss，而 gradient reversal 使 $\Phi$ 最大化 domain loss。
## C
### LT-DA-C01
取 joint ideal $h^*$：$R_t(h)\le R_t(h^*)+\Pr_t(h\ne h^*)\le R_t(h^*)+\Pr_s(h\ne h^*)+d/2\le R_t(h^*)+R_s(h)+R_s(h^*)+d/2$。
### LT-DA-C02
$X\sim\operatorname{Ber}(1/2)$ 两域相同；source $Y=X$、target $Y=1-X$。discrepancy 0，但无同一 classifier 两域都好，$\lambda$ 大。
### LT-DA-C03
$\Phi\equiv0$ 时 feature marginals相同；任何 head只能常数预测，最佳 error为少数类比例，balanced labels 时 1/2。
## D
### LT-DA-D01
检查 domain head capacity/optimization 是否真到最优、表示是否 collapse、source label sufficiency、label priors/conditional mismatch及不可观测 $\lambda$。
### LT-DA-D02
target validation使模型选择依赖目标域，属于 adaptation/oracle selection；DG 应用 source IID或leave-one-source-domain-out规则，target test锁定一次。
### LT-DA-D03
统一 backbone/pretraining/augmentation/FLOPs/search/seeds与domain sampling；比较 ERM、DANN、DG，报平均/worst target、source risk、domain proxy和 selection protocol。
## E
### LT-DA-E01
医院为 source units，留整院为 unseen target；patient互斥；source-only selection，另列 target-oracle upper bound；报 average/worst hospital、groups与calibration。
### LT-DA-E02
错误 pseudo-label导致错误 class-conditional对齐并自强化；用阈值/不确定性、class balance、迭代 error audit 与 oracle-label upper bound。
### LT-DA-E03
card 写 setting、$\mathcal H/\Phi$、source risk、discrepancy proxy、$\lambda$不可观测性、selection、baselines与target evidence；不称低domain accuracy为迁移保证。

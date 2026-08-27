---
type: solution
status: draft
topic: "[[生成模型实验协议、FD Loss 与前沿证据地图]]"
exercise: "[[习题 - 生成模型实验协议、FD Loss 与前沿证据地图]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - 生成模型实验协议、FD Loss 与前沿证据地图
## A. 识别与复述
### GEN72-A01
$\phi_{train}$ 定义优化方向，$\phi_{select}$ 用 validation 选超参/checkpoint，$\phi_{test}$ 冻结后只评一次，人评/任务是外部效标。隔离可减少对同一表示反复适配的泄漏。
### GEN72-A02
FD covariance gradient含 $S^{-1/2}$。batch 小于 feature dimension 时 empirical covariance 常秩亏；零/小特征值会使逆平方根不存在/爆炸，需要 population、regularization 与精度控制。
### GEN72-A03
Identity 是可由假设推导的等式；原始实验是论文协议观察；复现是独立实现的证据；hypothesis 是机制解释；open problem 是当前未解决且无充分证据的命题。
## B. 手算与建模
### GEN72-B01
均值项 $1^2+(-2)^2=5$；梯度 $2(\mu_g-\mu_r)=(2,-4)$。
### GEN72-B02
一维 covariance 项 $4+9-2\sqrt{36}=1$。对 variance $b=9$ 的导数 $1-\sqrt{4/9}=1/3$。
### GEN72-B03
$\tilde m_1=\operatorname{sg}(3-m_1/2)+m_1/2$。当前 $m_1=1$ 时 value $2.5+.5=3$，导数为 $1/2$。
## C. 推导与证明
### GEN72-C01
$S=A\Sigma_gA$，$A=\Sigma_r^{1/2}$。$d\operatorname{tr}S^{1/2}=\frac12\operatorname{tr}(S^{-1/2}dS)$，$dS=A(d\Sigma_g)A$。乘原式系数 $-2$ 后贡献 $-AS^{-1/2}A$，加 $\operatorname{tr}\Sigma_g$ 的梯度 $I$。
### GEN72-C02
非线性反例取 scalar loss $F(m)=m^2$、两个 microbatch moments 0 和 4：分别算再平均为 8；先平均得 2 再算为 4。FD 的平方根/协方差同样非线性。
### GEN72-C03
$P=N(0,1)$ 与 $Q$ 为 $\pm1$ 各半。二者均值 0、方差 1，Gaussian moment FD 为 0，但一个连续单峰、一个两点离散，mode/support 完全不同。
## D. 边界、反例与纠错
### GEN72-D01
模型梯度、超参搜索与 checkpoint selection 都向同一 encoder 过拟合；再用它 test 只测“对已知目标适配得多好”，不能估计对新表示/人类标准的泛化。
### GEN72-D02
可导只说明能算梯度；FD 仍只看 encoder 的一二阶 moments、有 finite-sample/秩问题，并会激励 metric gaming。数值稳定、统计充分性和价值对齐是不同问题。
### GEN72-D03
EMA 混入旧参数生成分布的 moments，而当前 gradient 针对新参数；学习率大/分布变化快时 context 与当前 population 偏离，形成有偏且滞后的方向。
## E. AI 迁移
### GEN72-E01
示例：“在固定 ImageNet validation/test split、相同 4 NFE、参数量和生成样本数下，A 相对 B 的 CleanFID 至少改善 0.5，且 Improved Recall 下降不超过 0.01、p95 latency 不增超过 5%。”
### GEN72-E02
列 base training、teacher pretraining、teacher target generation、distillation/post-training、hyperparameter search 总 FLOPs/data exposures；部署 denoiser/JVP/classifier NFE、hardware、batch、precision、latency、memory与能耗。
### GEN72-E03
训练用 encoder A；selection 用独立 validation metrics；test 用至少两个未训练 encoders 的 FD/KID、P/R、条件 failure suite、blind human、copy audit。预先规定任一 coverage/人评显著恶化即否定“整体改善”。

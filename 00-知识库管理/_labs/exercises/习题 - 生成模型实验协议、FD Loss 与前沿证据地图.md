---
type: exercise
status: draft
area: [generative-models, evaluation, experimental-design]
topic: "[[生成模型实验协议、FD Loss 与前沿证据地图]]"
solution: "[[解答 - 生成模型实验协议、FD Loss 与前沿证据地图]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - 生成模型实验协议、FD Loss 与前沿证据地图
## A. 识别与复述
### GEN72-A01
区分 $\phi_{train},\phi_{select},\phi_{test}$ 与人评。
### GEN72-A02
FD Loss 对 empirical covariance 的正定/秩条件为何重要？
### GEN72-A03
区分 identity、原始实验、复现、hypothesis 与 open problem。
## B. 手算与建模
### GEN72-B01
$\mu_r=(0,0),\mu_g=(1,-2)$，求 FD 均值项及其对 $\mu_g$ 梯度。
### GEN72-B02
一维 $\sigma_r^2=4,\sigma_g^2=9$，求 covariance FD 项及对 $\sigma_g^2$ 的梯度。
### GEN72-B03
两个 microbatch moments 为 1 和 5，global mean 为 3。写出 batch 1 的 stop-gradient context，使 value 为 3、对 $m_1$ 导数为 $1/2$。
## C. 推导与证明
### GEN72-C01
推导 $\nabla_{\Sigma_g}\mathcal F=I-\Sigma_r^{1/2}S^{-1/2}\Sigma_r^{1/2}$。
### GEN72-C02
证明“各 microbatch 分别算 FD 再平均”一般不等于“合并 moments 后算 FD”。
### GEN72-C03
构造相同均值协方差但不同 mode structure 的两分布。
## D. 边界、反例与纠错
### GEN72-D01
解释用同一 encoder 训练、选模、测试的 leakage。
### GEN72-D02
反驳“FD 可导，所以适合作为无风险的通用 loss”。
### GEN72-D03
为什么 EMA population statistics 会引入 staleness bias？
## E. AI 迁移
### GEN72-E01
把“方法 A 更好”改写成可证伪预注册 claim。
### GEN72-E02
为 1-NFE 模型写完整预算表，包含 teacher/search cost。
### GEN72-E03
为 FD Loss 设计 held-out evaluator 与 falsifying metric 套件。
## 解答入口
[[解答 - 生成模型实验协议、FD Loss 与前沿证据地图]]

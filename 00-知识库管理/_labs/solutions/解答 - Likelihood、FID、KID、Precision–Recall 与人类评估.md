---
type: solution
status: draft
topic: "[[Likelihood、FID、KID、Precision–Recall 与人类评估]]"
exercise: "[[习题 - Likelihood、FID、KID、Precision–Recall 与人类评估]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Likelihood、FID、KID、Precision–Recall 与人类评估
## A. 识别与复述
### GEN71-A01
先把图像映到固定 encoder（原始 FID 为 Inception）特征空间，再分别用 empirical mean/covariance 拟合 Gaussian，计算两 Gaussian 的 squared $W_2$。
### GEN71-A02
对固定 distributions、features、kernel，U-statistic 的期望等于 population MMD$^2$。它不表示单次方差小、分数非负、encoder/kernel 无偏或与人类偏好一致。
### GEN71-A03
Sajjadi 的 distribution PR curve 与 Kynkäänniemi 的 kNN manifold estimator 定义不同；后者还依赖 $k$。省略版本就无法解释或复现数值。
## B. 手算与建模
### GEN71-B01
一维 FID $=(0-2)^2+1+4-2\sqrt{1\cdot4}=4+1=5$。
### GEN71-B02
真实 off-diagonal 项为 0；生成 off-diagonal 平均为 3；cross sum 为 8，系数 $-2/(2\cdot2)=-1/2$，故 cross 为 $-4$，总计 $-1$。无偏 MMD$^2$ estimator 可因方差为负。
### GEN71-B03
$100/(64\log2)\approx2.254$ bits/dim。
## C. 推导与证明
### GEN71-C01
公式输入只有 $\mu,\Sigma$，所以更高 moments 被丢弃。标准正态与取值 $\pm1$ 各半的 Rademacher 分布都均值 0、方差 1，却一个连续单峰、一个离散双点。
### GEN71-C02
$\hat M=\frac1{m(m-1)}\sum_{i\ne j}k(a_i,a_j)+\frac1{n(n-1)}\sum_{i\ne j}k(b_i,b_j)-\frac2{mn}\sum_{ij}k(a_i,b_j)$。排除 diagonal 避免 $k(X_i,X_i)$ 自配对造成的有限样本偏差。
### GEN71-C03
样本 moments 即使无偏，$F(\hat\mu,\hat\Sigma)$ 含矩阵平方根等非线性，通常 $E[F(\hat m)]\ne F(E\hat m)$；偏差随维度、样本数和真实分布变化。
## D. 边界、反例与纠错
### GEN71-D01
FID 只匹配 encoder features 的 Gaussian moments；mode-dropped mixture 可调整剩余 modes 的 moments 接近真实，仍遗漏稀有模式。需 recall/分项 coverage。
### GEN71-D02
resize/antialias 改变 pixel 频谱，继而改变 features、moments 和 reference stats；这相当于换了指标函数，不是可忽略实现误差。
### GEN71-D03
作者挑选会产生 selection bias，20 张样本量小且无盲化/随机化/条件覆盖/不确定性；它只能作定性示例，不能估计总体偏好。
## E. AI 迁移
### GEN71-E01
CleanFID+KID；Improved P/R；prompt/label task score；盲化 paired human realism/adherence；copy audit；NFE/latency/memory。全部固定 sample count、encoder、split、seed 与 CI。
### GEN71-E02
每个 prompt/seed 生成 A/B，随机左右且隐藏模型；评审分别答 realism/adherence；预注册剔除与 attention check；以 prompt 和 participant 为 cluster 做 bootstrap/混合模型。
### GEN71-E03
对每个生成样本分别找 train/test 最近邻，使用 pixel、感知与第二 encoder；报告距离分布、极端案例、exact hash/near duplicate，并保持生成样本随机抽取而非手选。

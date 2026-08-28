---
type: solution
status: draft
topic: "[[过参数化与 Benign Overfitting]]"
exercise: "[[习题 - 过参数化与 Benign Overfitting]]"
created: 2026-08-23
updated: 2026-08-28
---
# 解答 - 过参数化与 Benign Overfitting
## A
### LT-BO-A01
对一列问题/算法，训练 risk 为零且 population excess risk 随 $n\to\infty$ 趋零，才是 benign overfitting。单个 benchmark test error 不高只是一条 finite-sample observation，未给极限、Bayes risk 或 problem scaling。
### LT-BO-A02
$\widehat\beta=X^\dagger y=P_X\beta^*+X^\dagger\varepsilon$，所以 $\widehat\beta-\beta^*=-(I-P_X)\beta^*+X^\dagger\varepsilon$。第一项是未观察 signal，第二项是为插值 noise 付出的 parameter。
### LT-BO-A03
新 $x$ 的 prediction error 是 $E_x(x^Tv)^2=v^T\Sigma v=\|\Sigma^{1/2}v\|^2$。population 几乎不变化的弱 eigen-directions 即使 parameter error 大，预测代价也可小。
## B
### LT-BO-B01
$2\cdot100/(1001-100-1)=200/900=2/9\approx0.2222$。
### LT-BO-B02
极限为 $\sigma^2/(c-1)=\sigma^2/2$。若 $\sigma^2$ 固定正数，它不趋零，故不是 consistency 意义的 benign overfitting。
### LT-BO-B03
均匀 tail：$R_k=0.04^2/(4\cdot0.01^2)=4$；集中 tail：$R_k=0.04^2/0.04^2=1$。前者有四个有效方向，后者由一个方向垄断。
## C
### LT-BO-C01
若 $v\in\ker X$，则 $X(\widehat\beta+v)=X\widehat\beta=y$。但 test excess 增量含 $v^T\Sigma v$ 和 cross term；若 null space 中存在 $v^T\Sigma v>0$，取 $cv$、$c\to\infty$ 可令 test risk 任意大。
### LT-BO-C02
isotropic Gaussian row space 是均匀随机 $n$ 维子空间，$E[P_X]=(n/p)I$。因 $I-P_X$ 是 projector，$E\|(I-P_X)\beta^*\|^2=\beta^{*T}(I-E P_X)\beta^*=(1-n/p)\|\beta^*\|^2$。
### LT-BO-C03
强子空间的 eigenvalues/sample size 要足以稳定估计 signal；signal tail energy要小；弱 tail 的总质量和 effective ranks 要大、最大单个 tail eigenvalue不能垄断；design/noise 要满足相应 concentration/independence；min-norm algorithm 必须明确。
## D
### LT-BO-D01
缺 problem sequence、Bayes risk、excess-risk limit、algorithm、signal/noise scaling、spectrum 和 confidence。它最多证明一个 finite setting 的 interpolation + good test performance。
### LT-BO-D02
classification risk、surrogate loss、Bayes boundary 和 label-noise mechanism不同；拟合随机标签可能改变 margin/decision boundary。需要 calibration、margin/noise assumptions 与 classification-specific theorem，不能套平方风险谱公式。
### LT-BO-D03
minimum Euclidean norm 依赖 feature coordinates。把一列 feature 乘 $c$ 等价于改变该方向 parameter penalty和 covariance spectrum，可让算法偏向/回避它；predictor class虽可相同，选中的 interpolator和风险会变。
## E
### LT-BO-E01
估计 embedding covariance eigenspectrum/effective ranks；把 target signal投影到 eigenvectors并画累积signal energy；训练 zero-ridge min-norm与ridge baselines；注入可控 noise；按 sample size与dimension重复；分解 projector bias/noise sensitivity并在独立 test domain验证。
### LT-BO-E02
保持 training span和signal方向近似不变，旋转/重分配尾部 eigenvalues，使相同 tail trace从许多小方向集中到少数方向；若 noise-fit test risk不随 effective rank显著恶化，则反驳“分散弱尾是主机制”的预测。
### LT-BO-E03
claim card：$n,p/\mathcal H$ 的问题序列；min-norm/optimizer；covariance spectrum/effective ranks；signal alignment；noise law；interpolation event；finite/high-prob bound；excess-risk limit；classification/deep-net外推等级。

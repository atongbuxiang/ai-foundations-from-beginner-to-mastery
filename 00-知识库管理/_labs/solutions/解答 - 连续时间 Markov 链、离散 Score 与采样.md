---
type: solution
status: draft
topic: "[[连续时间 Markov 链、离散 Score 与采样]]"
exercise: "[[习题 - 连续时间 Markov 链、离散 Score 与采样]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - 连续时间 Markov 链、离散 Score 与采样
## A. 识别与复述
### GEN59-A01
对 $i\ne j$，$R_t[i,j]\ge0$；$R_t[i,i]=-\sum_{j\ne i}R_t[i,j]$，故行和为零。行分布满足 $p'_t=p_tR_t$。
### GEN59-A02
$s_t(j\to i)=p_t(i)/p_t(j)$，$\ell_t(j\to i)=\log p_t(i)-\log p_t(j)$。离散 alphabet 没有默认无穷小坐标位移，所以自然对象定义在允许跳跃的边上，而非对类别 ID 求梯度。
### GEN59-A03
$R_t^{rev}[j,i]=R_t[i,j]p_t(i)/p_t(j)$。从反向起点 $j$ 到 $i$ 使用正向反边 $i\to j$；概率比把正向流入质量条件化到终点 $j$。
## B. 手算与建模
### GEN59-B01
$R^{rev}[2,1]=R[1,2](.75/.25)=2\times3=6$；$R^{rev}[1,2]=R[2,1](.25/.75)=1/3$。反向 diagonals 分别为 $-1/3,-6$。
### GEN59-B02
总离开率 $\lambda=1$，平均等待时间 $1/\lambda=1$。给定发生 jump，三个目标概率为 $(.3,.2,.5)$；若 rates 总和不是 1，需各自除以 $\lambda$。
### GEN59-B03
必须 $h\lambda_{max}\le1$；$.1\times12=1.2>1$，会产生负保持概率。安全上界 $h\le1/12\approx.08333$，实际可留更严格 margin。
## C. 推导与证明
### GEN59-C01
$p_{t+h}=p_t(I+hR_t)+o(h)$。移项：$(p_{t+h}-p_t)/h=p_tR_t+o(1)$；令 $h\to0$ 得 forward equation。
### GEN59-C02
$P(X_{t-h}=i,X_t=j)=p_{t-h}(i)hR_t[i,j]+o(h)$。除以 $P(X_t=j)=p_t(j)$，再用 $p_{t-h}(i)=p_t(i)+o(1)$，除以 $h$ 取极限即 reverse rate。
### GEN59-C03
闭环和为 $\sum_r[\log p(i_{r+1})-\log p(i_r)]$，相邻项望远镜消去，起终点相同，故为零。需所有涉及概率为正。
## D. 边界、反例与纠错
### GEN59-D01
任意 edge outputs 可能在闭环上 log-ratio 和非零，于是无法写成单个 node potential $\log p(i)$ 的差。它仍可定义某些 rates，但不能声称是某个全局边缘分布的精确 ratios。
### GEN59-D02
减小步长只减少 event/time discretization error。若 $s_\theta$ 系统性把 ratio 估成两倍，极限 sampler 收敛到错误 reverse dynamics；solver 更精确只会更精确地模拟错误模型。
### GEN59-D03
一次网络可同时输出许多 edge rates；一个 NFE 后可能发生零个、一个或多个模拟事件；wall-clock 还受 vocabulary、sparsity、memory 和 event handling 影响。因此三个数没有固定换算。
## E. AI 迁移
### GEN59-E01
检查 off-diagonal 非负、row sums 零、finite；小步 $I+hR$ 非负且 row sums 1；$p_t>0$ 支持上 reverse rates 非负；reverse row sums 由 diagonal 修正；stationary detailed-balance 例中 reverse=forward；ratio reciprocal/cycle consistency 可作诊断。
### GEN59-E02
两状态常数 $R$ 可解析或用 $e^{tR}$ 算 $p_t$。分别用 Gillespie 重复模拟终点频率，比较置信区间；再用多个 tau-leap $h$ 看偏差趋零。相同 seed policy 与样本数，分开报告 Monte Carlo 与 discretization error。
### GEN59-E03
固定 backbone/params、训练 tokens、time sampling、terminal corruption、NFE 与 wall-clock。报告 $x_0$ 输出是 $K$ logits 还是 edge ratios、如何组 reverse rates、normalization/support、loss weighting、sampler 与邻接 sparsity。

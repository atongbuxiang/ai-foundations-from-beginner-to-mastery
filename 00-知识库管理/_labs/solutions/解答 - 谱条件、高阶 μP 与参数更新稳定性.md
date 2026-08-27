---
type: solution
status: verified
area: [training, optimization, mup, spectral-norm, width-depth]
topic: "[[谱条件、高阶 μP 与参数更新稳定性]]"
exercise: "[[习题 - 谱条件、高阶 μP 与参数更新稳定性]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - 谱条件、高阶 μP 与参数更新稳定性

> [!warning] 使用边界
> 谱条件控制最坏方向的放大，不自动控制数据落在哪个方向、是否学到有用特征或最终泛化。所有 $\Theta$ 结论都必须绑定 shape path、随机性、对齐和训练时域假设。

## A. 识别与复述

### TRN47-A01
对 $m\times n$ 矩阵，
$$
\operatorname{RMS}_{entry}(W)
=\frac{\lVert W\rVert_F}{\sqrt{mn}}
$$
描述一个典型坐标的均方尺度，却不记录奇异方向怎样对齐。若输入协方差为 $\Sigma_x=\mathbb E[x^\top x]$，则
$$
\mathbb E\lVert xW\rVert_2^2
=\operatorname{tr}(W^\top\Sigma_xW)
$$
回答“在真实输入分布上平均放大多少”。谱范数
$$
\lVert W\rVert_2=\sup_{\lVert u\rVert_2=1}\lVert uW\rVert_2
$$
回答所有单位方向中的最坏放大。三者分别对应坐标典型尺度、数据加权平均尺度与最坏方向尺度。

### TRN47-A02
输入坐标 RMS 为 $O(1)$ 意味着 $\lVert x\rVert_2=O(\sqrt{d_{in}})$；输出目标是 $O(\sqrt{d_{out}})$。因此自然要求
$$
\lVert W\rVert_2
=O\!\left(\sqrt{\frac{d_{out}}{d_{in}}}\right).
$$
当层扩维时该比率可大于 1，缩维时可小于 1；统一设为 1 会忽略输出向量维数本身改变了目标总范数。若还要写 $\Theta$，需有输入覆盖相关奇异方向等非退化条件。

### TRN47-A03
μP 是跨宽度的参数化与更新尺度合同；Muon 或 matrix sign 决定矩阵梯度经过何种几何变换得到方向；shape multiplier 再把该方向换算到期望的 operator/update scale；有限步 Newton–Schulz 只是近似 matrix sign 的数值算法。混称会隐藏“方向、幅值、参数化、数值误差”究竟哪一项被改变，也让优化器比较无法复现。

## B. 手算与构造

### TRN47-B01
$A,B$ 的每个 entry 绝对值均为 $1/n$，故
$$
\operatorname{RMS}_{entry}(A)
=\operatorname{RMS}_{entry}(B)=\frac1n.
$$
$A=(\mathbf1/\sqrt n)(\mathbf1/\sqrt n)^\top$，唯一非零奇异值为 1，所以 $\lVert A\rVert_2=1$。随机符号矩阵的典型谱范数为
$$
\lVert B\rVert_2=\Theta(n^{-1/2}).
$$
因此在相同 entry RMS 下，最坏方向放大相差 $\Theta(\sqrt n)$。

### TRN47-B02
有 $\sqrt{1024}=32,\sqrt{4096}=64$，目标谱尺度为
$$
\sqrt{4096/1024}=2.
$$
所以
$$
\sigma\asymp\frac2{32+64}
=\frac1{48}\approx0.0208.
$$
fan-in 标准差是 $1/32\approx0.03125$。两者都按 $d_{in}^{-1/2}$ 同阶，但极端 aspect ratio 使常数不同；这里谱匹配值是 fan-in 值的 $2/3$。随机矩阵公式只给典型尺度，不是有限样本精确等式。

### TRN47-B03
完全同向时，未缩放总量为 $Lc$；近似正交时，平方范数相加，总量为 $\sqrt Lc$。乘 residual multiplier 后分别是 $\alpha_LLc$ 与 $\alpha_L\sqrt Lc$。要保持 $O(c)$，前者需
$$
\alpha_L=O(L^{-1}),
$$
后者需
$$
\alpha_L=O(L^{-1/2}).
$$
真实网络介于两端，相关性和 Jacobian 传播决定应采用的制度。

## C. 推导与证明

### TRN47-C01
坐标 RMS 合同给
$$
\lVert x\rVert_2=O(\sqrt{d_{in}}),\qquad
\lVert y\rVert_2=O(\sqrt{d_{out}}).
$$
由 operator inequality，
$$
\lVert y\rVert_2
\le O(\sqrt{d_{in}})\lVert W\rVert_2.
$$
选择
$$
\lVert W\rVert_2
=O\!\left(\sqrt{d_{out}/d_{in}}\right)
$$
足以防止上界超过输出目标量级。它不能推出下界，因为实际 $x$ 可能正交于 top right singular vector，甚至落在 $W$ 的零空间；$W$ 也可为零而仍满足“不爆炸”。得到 $\Theta$ 需要输入对有关奇异子空间有非退化投影，或另设“输出不消失”条件。

### TRN47-C02
谱范数的对偶是核范数，因此 Hölder 不等式给
$$
\langle G,\Delta W\rangle_F
\ge-\lVert G\rVert_*\lVert\Delta W\rVert_2
\ge-\rho\lVert G\rVert_*.
$$
取薄 SVD $G=U\Sigma V^\top$ 并令
$$
\Delta W^*=-\rho UV^\top,
$$
则 $\lVert\Delta W^*\rVert_2=\rho$，且
$$
\langle G,\Delta W^*\rangle_F
=-\rho\operatorname{tr}(\Sigma)
=-\rho\lVert G\rVert_*.
$$
所以上界可达。秩亏时 $UV^\top$ 定义在非零奇异子空间；零空间上的扩展不改变目标值。

### TRN47-C03
三角不等式给
$$
\lVert W_t\rVert_2
\le\lVert W_0\rVert_2
+\sum_{s<t}\lVert\Delta W_s\rVert_2.
$$
令固定 rank-one 矩阵 $P=uv^\top$，$\lVert P\rVert_2=1$。若 $W_0=0$ 且每步 $\Delta W_s=\rho P$，则 $W_t=t\rho P$，谱范数线性增长。若交替取
$$
\Delta W_{2k}=\rho P,\qquad
\Delta W_{2k+1}=-\rho P,
$$
每步谱范数仍为 $\rho$，但每两个更新和为零，参数回到初始值。逐步有界不决定长时累积。

## D. 边界、反例与纠错

### TRN47-D01
取
$$
A=\mathbf1\mathbf1^\top/n,\qquad
B_{ij}=\varepsilon_{ij}/n.
$$
两者 entry RMS 都是 $1/n$，但前者谱范数为 1，后者典型为 $O(n^{-1/2})$。它反驳“只要每个 update coordinate 都是 $O(1/n)$，最坏 feature update 就一定稳定”。低秩、符号相关和输入对齐可把小坐标相干累加。

### TRN47-D02
令每层 $W_\ell$ 都是满足目标谱尺度的固定随机正交变换，并冻结它们；只训练一个被错误置零或标签打乱的 readout。所有归一化谱遥测都可长期稳定，但任务精度接近随机。谱门只排除一类放大/坍缩事故；它不保证标签信息存在、梯度方向有用、表示可分或优化到好解。

### TRN47-D03
至少需核对：pre/post norm 与残差公式、$\alpha_L$ 制度、width/depth/aspect/head 联合路径、参数初始化与 orientation、优化器和每组 LR、训练步数怎样随规模变、数据与 loss、有限宽/有限深范围、概率事件与常数、是否只证明初始化或有限时间，以及定理还是经验观察。未覆盖的架构和极限次序不能从特定预印本外推为普遍定律。

## E. AI 迁移

### TRN47-E01
每组保存 $(d_{in},d_{out})$、orientation、width/depth axes、entry RMS、$\lVert W\rVert_F$、power-iteration $\widehat{\lVert W\rVert_2}$、effective rank；更新侧保存相同量和
$$
\frac{\lVert\Delta W\rVert_2}{\lVert W\rVert_2+\epsilon},
\qquad
\frac{\lVert\Delta W\rVert_2}{\sqrt{d_{out}/d_{in}}}.
$$
再以固定校准 batch 记录 $\lVert xW\rVert/\lVert x\rVert$、$\lVert x\Delta W\rVert$ 与协方差谱。embedding 要区分活跃 rows，Q/K 另记 score/entropy，V/O 与 FFN 记 residual contribution，readout 记 logit change，norm 单独按向量参数审计。

### TRN47-E02
对每个矩阵使用固定随机种子生成多个初始向量，并重复
$$
v\leftarrow W^\top Wv/\lVert W^\top Wv\rVert
$$
，在 $k\in\{1,2,4,8,16,32\}$ 保存 Rayleigh estimate。用相邻估计相对变化和残差
$$
\lVert W^\top Wv-\hat\lambda v\rVert/\max(\hat\lambda,\epsilon)
$$
判停。在小矩阵与每类 shape 的抽样 checkpoint 上用精确 SVD 对照；例如预注册 95% 样本相对误差不超过 2%，且不得只保留收敛成功的矩阵。多个初始向量可降低撞到弱奇异子空间的风险。

### TRN47-E03
最小网格可取 width $\{d,2d,4d\}$ × depth $\{L,2L,4L\}$，并比较 $\alpha_L\in\{1,L^{-1/2},L^{-1}\}$；固定数据、tokens、aspect、head path、optimizer semantics 和 seeds。遥测至少分：(1) 坐标/feature RMS；(2) 参数与更新的归一化谱量；(3) 层间相关、residual/Jacobian 与累计漂移。若仅 width 改变即 step-1 slope 漂移，优先查 parameterization；仅 depth 改变且初始正常，查 residual scale；单步稳定但随时间单调增长，查对齐累积。预注册 slope、最大/最小 ratio、NaN/clip 与谱漂移阈值，失败 run 留在分母。

## 无提示重做

- [ ] 48 小时后证明谱范数约束下的最速方向。
- [ ] 一周后从同向与正交残差累积反推两种 depth multiplier。

---
type: solution
status: draft
area: [architecture, group-equivariance]
topic: "[[群卷积、等变网络与 CNN 证据地图]]"
exercise: "[[习题 - 群卷积、等变网络与 CNN 证据地图]]"
sources: ["[[S-2016-Cohen-Welling-GCNN]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - 群卷积、等变网络与 CNN 证据地图

## A. 识别与复述
### ARCH-GCNN-A01
Action 是 $T_e=I,T_gT_h=T_{gh}$；orbit 是 $\{T_gx\}$；equivariance 为 $f(T_gx)=S_gf(x)$；invariance 为 $S_g=I$。
### ARCH-GCNN-A02
输入变换后不同 orientation detector 的响应会重排。显式 group axis 保存这种变换关系，使后层继续按群共享，而不是过早丢姿态。
### ARCH-GCNN-A03
`I`：等变恒等式；`T`：特定函数类/分布的表达或样本界；`E`：具体数据/规模性能；`H`：为何提升的机制解释；`O`：真实近似 symmetry、连续群和系统最优性。

## B. 手算与建模
### ARCH-GCNN-B01
对 $X=\begin{bmatrix}a&b\\c&d\end{bmatrix}$，轨道可写 $X$、$\begin{bmatrix}c&a\\d&b\end{bmatrix}$、$\begin{bmatrix}d&c\\b&a\end{bmatrix}$、$\begin{bmatrix}b&d\\a&c\end{bmatrix}$（旋转方向 convention 可相反，但须一致）。
### ARCH-GCNN-B02
若左循环一格，feature 可变为 $[2,3,4,1]$；sum 都为 10。具体左/右取决于 action convention，不影响 sum invariance。
### ARCH-GCNN-B03
权重 tying、每个 group output 如何连接 group input、kernel bank 参数化都影响参数。32 plain channels 与 8×4 orientation activations 的元素数相同不代表 weight shape 相同；后续 group convolution 还沿 group 轴缩并。

## C. 推导与证明
### ARCH-GCNN-C01
$((L_hf)\star\psi)(g)=\sum_uf(h^{-1}u)\psi(g^{-1}u)$。令 $v=h^{-1}u$，得 $\sum_vf(v)\psi(g^{-1}hv)=(f\star\psi)(h^{-1}g)=L_h(f\star\psi)(g)$。
### ARCH-GCNN-C02
$r(L_hf)=\sum_gf(h^{-1}g)$。映射 $g\mapsto h^{-1}g$ 是群上的双射，所以和等于 $\sum_uf(u)=r(f)$。
### ARCH-GCNN-C03
若 $\Phi(f)(g)=\phi(f(g))$ 且同一 $\phi$，则 $\Phi(L_hf)(g)=\phi(f(h^{-1}g))=L_h\Phi(f)(g)$；$\phi$ 不需线性。

## D. 边界、反例与纠错
### ARCH-GCNN-D01
手写 6/9、道路箭头方向、医学左右标记、太阳能板朝向估计都可能随旋转改变标签或输出应等变而非不变。
### ARCH-GCNN-D02
任意角把格点送到非格点，需插值；插值、crop 和边界不是纯 permutation，连续旋转复合与离散 resampling 不一定严格满足群乘法，残差随分辨率/filter 变化。
### ARCH-GCNN-D03
Group axis 增大 activation；每层需计算多个 transformed responses；内存/IO/implementation overhead 上升。参数 tying 只约束静态 weights，不能代表 MACs 或 latency。

## E. AI 迁移
### ARCH-GCNN-E01
结构验收：多随机输入/群元素测 normalized $\|f(T_gx)-S_gf(x)\|$，分 boundary/interpolation/dtype。任务验收：原/变换集 accuracy、pose output、calibration、样本量曲线、latency/memory，对照 augmentation 和 plain CNN。
### ARCH-GCNN-E02
两者都先定义重标号/旋转 action，再要求 layer intertwine，最后用 invariant readout 做图/类别预测。区别是 graph permutation 直接重排离散节点并同时变邻接，图像旋转可能需插值且群通常更小/几何固定。
### ARCH-GCNN-E03
检查标签对旋转/反射是否不变或等变；传感器方向和 north-up 是否有绝对意义；数据是否覆盖；90°/reflection 是否精确落格；$C_4$ 与 $D_4$ 的额外 activation/latency；augmentation baseline；错误 symmetry 风险；验证 structure residual 和任务指标。

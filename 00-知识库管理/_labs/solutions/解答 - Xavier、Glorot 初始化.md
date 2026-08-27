---
type: solution
status: draft
area: [neural-networks/initialization, xavier, glorot]
topic: "[[Xavier、Glorot 初始化]]"
exercise: "[[习题 - Xavier、Glorot 初始化]]"
sources: ["[[S-2010-Glorot-Bengio-Training-Difficulty]]", "[[S-1998-LeCun-Efficient-Backprop]]", "[[S-2026-PyTorch-NN-Init]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - Xavier、Glorot 初始化

## A

### NN-XAV-A01
对 $z=Wx$、$W:[n_{\rm out},n_{\rm in}]$，每个输出坐标前向汇总 $n_{\rm in}$ 项，所以 fan-in 为 $n_{\rm in}$；$g_x=W^Tg_z$ 时每个输入 cotangent 汇总 $n_{\rm out}$ 项，所以 fan-out 为 $n_{\rm out}$。卷积 fan 还乘 receptive-field size；本质定义来自连接图和求和长度，而非变量名。

### NN-XAV-A02
Xavier 的目标 variance 是 $v=2/(n_{\rm in}+n_{\rm out})$。Normal 的 standard deviation 为 $\sqrt v$；uniform $[-a,a]$ 的 $a=\sqrt{3v}=\sqrt{6/(n_{\rm in}+n_{\rm out})}$。若带 gain $g$，standard deviation 与 bound 乘 $g$，variance 乘 $g^2$。

### NN-XAV-A03
$E[WW^T]=I$ 是对随机矩阵 ensemble 的 entrywise expectation；一次抽样近正交要控制 $WW^T-I$ 的范数或至少其 entries，高概率条件依宽度/aspect ratio；dynamical isometry 更要求网络总 Jacobian 的 singular values 集中在 1 附近。三者从平均命题逐步加强，不能互推。

## B

### NN-XAV-B01
$W:[120,30]$ 表示 $n_{\rm out}=120,n_{\rm in}=30$。Xavier variance 为 $2/150=1/75\approx0.013333$，uniform bound 为 $\sqrt{6/150}=0.2$。线性前向乘数 $\chi_f=30/75=0.4$，反向乘数 $\chi_b=120/75=1.6$。

### NN-XAV-B02
公式中的 weight 是 $[n_{\rm out},n_{\rm in}]$ 并用于 $xW^T$；实际张量却是 $[n_{\rm in},n_{\rm out}]$ 并用于 $xW$。应把转置 view 传给按前一种约定计算 fan 的 helper，或显式计算 fan/variance 后直接采样。随后用小 shape forward/VJP 和日志核对，不能只相信变量名。

### NN-XAV-B03
设 variance 为 $v$。Gaussian 有 $EW^4=3v^2$ 且 tail 无界；uniform $[-\sqrt{3v},\sqrt{3v}]$ 有
$$EW^4=\frac{(\sqrt{3v})^4}{5}=\frac95v^2,$$
且绝对值有硬上界。大量参数的最大值、outlier probability 与有限宽谱会不同；匹配前两 moments 不等于 distribution 等价。

## C

### NN-XAV-C01
前向 $z_j=\sum_{i=1}^{n_{\rm in}}W_{ji}x_i$，独立零均值下 $E z_j^2=n_{\rm in}vE x_i^2$，守恒给 $v=1/n_{\rm in}$。反向 $g_{x,i}=\sum_{j=1}^{n_{\rm out}}W_{ji}g_{z,j}$，同样推得 $E g_{x,i}^2=n_{\rm out}vE g_{z,j}^2$，守恒给 $v=1/n_{\rm out}$。

### NN-XAV-C02
令 effective fan 为算术平均 $\bar n=(n_{\rm in}+n_{\rm out})/2$，其 reciprocal 为 $1/\bar n=2/(n_{\rm in}+n_{\rm out})$。设 aspect ratio $\rho=n_{\rm out}/n_{\rm in}$，则
$$\chi_f=\frac{2}{1+\rho},\qquad\chi_b=\frac{2\rho}{1+\rho}.$$
$\rho\to\infty$ 时分别趋 0、2；$\rho\to0$ 时分别趋 2、0。折中只把单层极端限制在 0 到 2，不让两者同时为 1。

### NN-XAV-C03
对 square $W:[n,n]$，$E W_{ik}W_{jk}=0$（$i\ne j$），而 diagonal 有 $\sum_kEW_{ik}^2=n(1/n)=1$，故 $E[WW^T]=I$。但 expectation 可平均掉单次偏差；iid square Gaussian 的最小 singular value 可接近 0、最大值约为常数量级，不能由 entrywise expectation 得到 $\|WW^T-I\|_2$ 很小。

## D

### NN-XAV-D01
非方层若两边都精确守恒，需要同时 $n_{\rm in}v=1$ 与 $n_{\rm out}v=1$，从而要求 $n_{\rm in}=n_{\rm out}$。Xavier 在 $n_{\rm in}\ne n_{\rm out}$ 时给 $\chi_f\ne1,\chi_b\ne1$，只是对称折中。

### NN-XAV-D02
sigmoid 即便 preactivation scale 合适，中心 slope 最大也仅 $1/4$，tails 仍饱和；activation mean 约 $1/2$ 又会让后续层的输入非零中心。Xavier 只校准特定二阶近似，不能改变函数值域、均值和深层 derivative product。

### NN-XAV-D03
embedding 是 lookup 而非每次汇总 fan-in 个独立坐标；depthwise convolution 每个输出只连接一个/少数输入通道，fan 与普通 conv 不同；residual output 的二阶矩含 branch covariance。必须分别写 forward/VJP 连接图和目标，机械套同一公式会把错误 fan 或漏掉 cross term。

## E

### NN-XAV-E01
覆盖 normal/uniform、square/rectangular/degenerate shapes、转置存储、dense/conv、FP32/BF16/FP16。检查 sample mean/variance/bound/fourth moment、seed determinism、device consistency 与空 fan；用明确 forward/VJP 测 one-layer second-moment multipliers，并验证 helper 的 fan 日志。容差随参数数与 dtype 设定。

### NN-XAV-E02
构造等宽、4 倍扩宽、4 倍压窄和交替 bottleneck 网络，深度从 1 到 100；比较 fan-in、fan-out、Xavier，并共享 weight-base seeds/输入。逐层报告 activation/gradient second moment、Jacobian extreme estimates、NaN/Inf 与 loss。理论预测是非方层乘数对向变化，跨层宽度抵消不保证中间层稳定。

### NN-XAV-E03
至少记录 parameter path、shape/layout、forward contraction、initializer 名称与版本、distribution、fan-in/out、gain/mode/nonlinearity、target/sample variance、bias rule、seed/generator/device/dtype、任何 truncation/clipping/quantization，以及 checkpoint hash。这样才能区分公式、API 默认和后处理造成的差异。


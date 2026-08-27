---
type: solution
status: draft
area: [neural-networks/activations, smooth-rectifiers]
topic: "[[Softplus、GELU、SiLU 与平滑门控]]"
exercise: "[[习题 - Softplus、GELU、SiLU 与平滑门控]]"
sources: ["[[S-2016-Hendrycks-Gimpel-GELU]]", "[[S-2018-Elfwing-Uchibe-Doya-SiLU]]", "[[S-2017-Ramachandran-Zoph-Le-Swish]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - Softplus、GELU、SiLU 与平滑门控

## A

### NN-SMO-A01
对 $\beta>0$，Softplus 为 $s_\beta(x)=\beta^{-1}\log(1+e^{\beta x})$，有 $s'_\beta=\sigma(\beta x)>0$、$s''_\beta=\beta\sigma(\beta x)(1-\sigma(\beta x))>0$；故它严格递增、严格凸，值域为 $(0,\infty)$。GELU 为 $g(x)=x\Phi(x)$，有 $g'=\Phi+x\varphi$、$g''=(2-x^2)\varphi$；它在负侧有局部极小值，既非全局单调也非全局凸，值域为 $[g(x_*),\infty)$，其中 $x_*\approx-0.7518$、$g(x_*)\approx-0.1700$。SiLU 为 $f_\beta(x)=x\sigma(\beta x)$，有 $f'=\sigma(\beta x)+\beta x\sigma(\beta x)(1-\sigma(\beta x))$；它同样非全局单调、非全局凸，最小值按 $1/\beta$ 缩放，约为 $-0.2785/\beta$。

### NN-SMO-A02
Softplus 是两个标量 $0,x$ 的 log-sum-exp，即对 $\max(0,x)$ 做 soft maximum；GELU/SiLU 是先构造输入依赖的 gate，再与原输入相乘，即 $x\Phi(x)$、$x\sigma(\beta x)$；convolution smoothing 则是对整条函数做 $E[r(x+\varepsilon)]$。三者分别作用于 maximum、gate 和 function graph，不能只因结果都光滑就视作同一操作。

### NN-SMO-A03
exact GELU 使用 erf/CDF，常见 approximation 使用 tanh 或 sigmoid。选择会同时改变 forward 值、一阶与二阶导、低精度舍入、可融合 kernel、导出图和 checkpoint 重现性。因此实现必须把 approximation flag、dtype、拟合区间及 backward 公式写入合同；它不是可忽略的排版差别。

## B

### NN-SMO-B01
令 $u=\beta x$。若 $u\ge0$，则 $\log(1+e^u)=u+\log(1+e^{-u})\in[u,u+\log2]$；若 $u<0$，则它属于 $[0,\log2]$。两种情况合并为 $\max(0,u)\le\log(1+e^u)\le\max(0,u)+\log2$，再除以 $\beta>0$ 即得结论。上界误差在 $x=0$ 取到，故一致误差恰为 $\log2/\beta$。

### NN-SMO-B02
由 $\Phi'=\varphi$、$\varphi'=-x\varphi$，
$$g'(x)=\Phi(x)+x\varphi(x),\qquad g''(x)=2\varphi(x)-x^2\varphi(x)=(2-x^2)\varphi(x).$$
因 $\varphi(x)>0$，曲率在 $|x|<\sqrt2$ 为正，在 $|x|>\sqrt2$ 为负，并在 $x=\pm\sqrt2$ 变号。这也直接否定了“GELU 是凸的平滑 ReLU”。

### NN-SMO-B03
记 $p=\sigma(\beta x)$，则 $f_\beta=xp$ 且
$$f_\beta'(x)=p+\beta xp(1-p).$$
对固定 $x$，$\beta\to0^+$ 时 $p\to1/2$，故 $f_\beta\to x/2$；$\beta\to\infty$ 时，$x>0$ 有 $p\to1$、$x<0$ 有 $p\to0$、$x=0$ 始终为 0，所以逐点趋于 ReLU。这个极限不是导数的一致收敛：0 点的导数始终为 $1/2$，而 ReLU 在该点无经典导数。

## C

### NN-SMO-C01
从 $1+e^x=e^{\max(x,0)}(1+e^{-|x|})$ 得
$$\log(1+e^x)=\max(x,0)+\log(1+e^{-|x|}).$$
右式只对非正指数取 `exp`，避免大正 $x$ 溢出；`log1p(t)` 在 $t\ll1$ 时直接计算 $\log(1+t)$，避免先把 $1+t$ 舍入成 1 后丢掉尾项。数学恒等并不意味着两条浮点执行路径等价。

### NN-SMO-C02
令 $Z\sim\mathcal N(0,1)$，则
$$E[(x+Z)_+]=\int_{-x}^{\infty}(x+z)\varphi(z)\,dz=x\Phi(x)+\varphi(x),$$
其中用了 $\int_a^\infty z\varphi(z)dz=\varphi(a)$。GELU 只有第一项 $x\Phi(x)$，所以它可解释为用 Gaussian CDF 自门控，却不是 ReLU 与标准 Gaussian 的卷积。

### NN-SMO-C03
若上游 cotangent 为 $u$，逐元 VJP 分别为
$$\bar x_{\rm GELU}=u[\Phi(x)+x\varphi(x)],$$
$$\bar x_{\rm SiLU}=u[\sigma(\beta x)+\beta x\sigma(\beta x)(1-\sigma(\beta x))].$$
第二项可使正侧局部 slope 超过 1，也可使负侧 slope 小于 0；这与 gate 本身处在 $(0,1)$ 不矛盾，因为对 $xq(x)$ 求导还包含 $xq'(x)$。

## D

### NN-SMO-D01
光滑只消除了 kink，不控制 Jacobian 乘积、Hessian condition number、初始化尺度、归一化、残差相关性或优化器噪声。反例是把任意光滑激活前的权重乘得极大：局部 Jacobian 仍可爆炸；把 sigmoid 预激活推入饱和区则虽 $C^\infty$，梯度仍近 0。因此“平滑”最多是一个局部函数性质，不是优化难度的充分条件。

### NN-SMO-D02
设目标 $g$，构造 $\tilde g_\varepsilon(x)=g(x)+\varepsilon\sin(x/\varepsilon^2)$。任意区间上 forward 误差不超过 $\varepsilon$，但 derivative 差为 $\varepsilon^{-1}\cos(x/\varepsilon^2)$，可任意大。实际 GELU approximation 没有这样极端，但该反例证明只报告 forward max error 不能推出 backward 可靠，必须单独测导数误差。

### NN-SMO-D03
先固定训练与推理分别使用的 exact/approx flag，并比较同一 checkpoint 在校准集上的 logits、loss、ranking 与最终指标；再做逐层 activation drift 和极端输入测试。若推理公式不同，部署的是新函数，应记录 graph hash、dtype、kernel、最大/分位误差，并把任何精度变化归因于一次明确的 post-training substitution，而不能宣称模型完全等价。

## E

### NN-SMO-E01
以 FP64 稳定公式为 oracle，覆盖 $[-100,100]$、0 邻域、曲率变号点、非单调极值点和随机值；分别检查 FP16/BF16 forward、VJP、double backward 的绝对/相对/ULP 误差、单调段、有限性与 determinism。再覆盖 contiguous/strided shapes、尾块、fusion、in-place/alias 限制，并在目标 GPU 比较吞吐和 memory traffic。容差应按 dtype 与输出尺度分层，不能只用一个相对误差阈值。

### NN-SMO-E02
设四种激活、相同数据切分与训练代码，至少做 plug-in 与 per-activation retuned 两轨；对带额外参数或特殊 kernel 的实现另做 matched-parameter、matched-latency。预注册学习率搜索、初始化、seed、失败规则和主指标；记录激活/导数矩、梯度谱、训练时间、能耗与多 seed 区间。test 集只在 validation 选择结束后评一次。

### NN-SMO-E03
指数参数化 $e^x$ 在 $x\to-\infty$ 接近 0、在正侧导数等于输出，可能迅速溢出并产生很大梯度；Softplus 也只保证正值，但正侧近线性、导数有界于 1，通常更温和。若要求严格下界，可用 $\varepsilon+\operatorname{softplus}(x)$；若模型需要乘法尺度的对数线性结构，exponential 仍可能更自然。选择应同时检查支持集、dynamic range、梯度和目标分布。


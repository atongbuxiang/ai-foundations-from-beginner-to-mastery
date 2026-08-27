---
type: solution
status: draft
area: [neural-networks/activations, relu, nonsmoothness]
topic: "[[ReLU、Leaky ReLU 与次梯度约定]]"
exercise: "[[习题 - ReLU、Leaky ReLU 与次梯度约定]]"
sources: ["[[S-2010-Nair-Hinton-ReLU]]", "[[S-2013-Maas-Hannun-Ng-Leaky-ReLU]]", "[[S-2015-He-Delving-Rectifiers]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - ReLU、Leaky ReLU 与次梯度约定

## A

### NN-REL-A01
classical derivative 要求左右差商极限相同；ReLU 在 0 左为 0、右为 1，故不存在。作为 convex function，其 subdifferential 是所有支撑斜率 $[0,1]$。AD framework 必须为 primitive 指定一个返回值，常见为 0；这是 executable convention，可能属于 subgradient，但不证明 classical differentiability。

### NN-REL-A02
对 $x\ne0$，ReLU input derivative 是 $1_{x>0}$。leaky/PReLU 为 $1_{x>0}+a1_{x<0}$。PReLU 对 $a$ 的 derivative 是 $x1_{x<0}$，batch/channel 共享时对所有共享 positions 求和。$x=0$ 处 input derivative 由 convention 定义，且对 $a$ 的导数通常为 0。

### NN-REL-A03
activation sparsity 是 tensor 中零值比例；dead unit 是一个单元在指定数据分布/时间窗口上长期没有 active region 与有效梯度；hardware speedup 要求稀疏格式、可预测 pattern、kernel 和 memory system 真正跳过工作。大量 zeros 可能仍按 dense kernel 全算，也不一定来自永久死亡。

## B

### NN-REL-B01
若 $x_1+x_2>1$，$f=x_1+x_2-1$、gradient $(1,1)$；若 $x_1+x_2<1$，$f=0$、gradient $(0,0)$。边界是直线 $x_1+x_2=1$，函数连续但 classical gradient 不存在；directional derivative 依方向进入哪侧。

### NN-REL-B02
input VJP 分别乘负斜率、负斜率、zero convention、正斜率，故 $\bar x=(0.1,0.2,0,-1)$。$\bar a=\sum_{x_i<0}\bar h_ix_i=1(-2)+2(-1)=-4$。零点不贡献，正点不依赖 $a$。

### NN-REL-B03
activation-only gain 为 $a^k$。$a=10^{-2}$ 时，$k=5$ 得 $10^{-10}$，$k=10$ 得 $10^{-20}$。它虽非精确 0，但在深链和低精度中可数值上无效；权重 gain 还会进一步乘入。

## C

### NN-REL-C01
对 $c\ge0$，$\max(0,cx)=c\max(0,x)$；leaky 两个分支也保持符号，故 $\phi_a(cx)=c\phi_a(x)$。于是 $W_{l+1}\phi(cW_lh)=W_{l+1}c\phi(W_lh)$，配 $W_{l+1}\mapsto c^{-1}W_{l+1}$ 函数不变。$c=-1,x=1$ 时 ReLU$(-1)=0$，而 $-\operatorname{ReLU}(1)=-1$，失败。

### NN-REL-C02
对称性给 $E[Z^21_{Z>0}]=E[Z^21_{Z<0}]=q/2$（零点无贡献）。ReLU 平方只保留正侧，得 $q/2$。leaky 平方为 $Z^21_{Z>0}+a^2Z^21_{Z<0}$，期望为 $(1+a^2)q/2$。

### NN-REL-C03
固定所有 preactivation 符号后，每个 ReLU 等于 identity 或 zero linear map，即一个固定 diagonal mask $D_l$。网络成为 $D_L(W_L\cdots D_1(W_1x+b_1)+\cdots)+b_L$，是 affine。region boundary 上至少一个符号改变，mask 不再局部恒定，左右 Jacobian 可不同，不能把一侧矩阵当作唯一 classical Jacobian。

## D

### NN-REL-D01
即使每个负侧 slope 为 $a>0$，连续 $L$ 个负 gate 给因子 $a^L\to0$；权重还可有小 singular values，且不同矩阵方向可能对齐到收缩子空间。非零逐因子不提供与深度无关的乘积正下界。

### NN-REL-D02
例：$z=x-1$，当前 mini-batch 全取 $x=0$，单元 inactive；总体数据还以正概率取 $x=3$，届时 active。可靠 dead rate 应指定数据/augmentation distribution、train mode、连续 steps/window，并检查 $P(z>0)$、activation magnitude 和 parameter gradient；可报告“过去 $K$ steps 的所有 valid examples 上 active rate 为 0”。

### NN-REL-D03
固定 region 内 affine 只说明局部 Hessian 为 0；不同 regions 有不同 affine maps，边界可形成大量折面。$f(x)=|x|=\operatorname{ReLU}(x)+\operatorname{ReLU}(-x)$ 已是非 affine，尽管除 0 外二阶导为 0。复杂性来自 region partition 与 Jacobian jumps。

## E

### NN-REL-E01
forward 与 out-of-place FP64 reference 对比所有 shapes/layouts；backward 保存 mask 或合法重算，alias/version counter 必须拒绝被覆盖 residual；在 $x<0,x>0$ 做 finite difference，在 $x=0$ 只验文档 convention；测试 NaN、signed zero、subnormal、FP16/BF16；对 repeated accumulation 做 dot test；并行运行测 determinism。in-place 节省的 bytes、额外 mask 与 fusion speed 分开计量。

### NN-REL-E02
两轨初始化：共同 variance 与按 $(1+a^2)/2$ 校准的 He variance；PReLU 声明 slope 初始化、channel/layer sharing 和 constraint。匹配 parameter/FLOP，若 PReLU 多参数需相应调整或单列 overhead；固定与 retuned LR 两轨，多 seeds。记录 dead rate、negative activation share、second moment、gradient quantiles、sparsity、wall-clock 与 validation。

### NN-REL-E03
可能是：正常负半轴门控、large negative bias、data shift、过大 LR 造成 dead units、dropout/mask、padding zeros、quantization/clipping、稀疏正则或记录位置在 pre/post activation 混淆。诊断需按 layer/channel/sample 分解 zero rate，查看 preactivation histogram、bias/update history、train/eval 与 mask，跑未量化 FP32 reference、移除 padding、输入扰动和全数据 active-rate；再判断是否真的长期无梯度。

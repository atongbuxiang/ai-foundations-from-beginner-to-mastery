---
type: solution
status: draft
area: [architecture, long-context, position-interpolation, rope-scaling]
topic: "[[长度外推、位置插值与 RoPE 缩放]]"
exercise: "[[习题 - 长度外推、位置插值与 RoPE 缩放]]"
sources: ["[[S-2023-Chen-Position-Interpolation]]", "[[S-2023-Su-9675-RoPE-β进制视角]]", "[[S-2023-Su-9706-混合进制NTK-RoPE]]", "[[S-2023-Su-9708-ReRoPE]]", "[[S-2023-Su-9948-长度外推技术复盘]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - 长度外推、位置插值与 RoPE 缩放

## A. 识别与复述

### ARCH-EXT-A01
直接外推保持原频率并使用更大坐标；PI 把坐标除以长度倍率；统一缩放对所有频率同一变换；逐频缩放给不同频率不同倍率；截断/重映射在局部保真、远处 clamp 或采用另一函数。它们改变的是相位域、分辨率和实现路径，不是同义名称。

### ARCH-EXT-A02
“NTK-aware”描述方法命名与设计直觉；除非给出明确核、极限、假设和误差/性能定理，不能把名字解释为 neural tangent kernel 保证。相关方法可以在实验上有效（E），而理论标签仍需单独审查。

### ARCH-EXT-A03
训练覆盖决定模型见过哪些距离；位置变换决定相位；可见域决定是否允许访问远端；微调协议决定新相位是否被适配。只报告其中一项无法复现实验，也无法判断提升来自坐标、窗口还是额外训练。

## B. 手算与建模

### ARCH-EXT-B01
倍率 $s=L_1/L_0=4$，故 $m'=m/s=1500$，落回原训练坐标范围。若采用端点对齐的精确比例 $(L_0-1)/(L_1-1)$，数值略有不同，必须注明约定。

### ARCH-EXT-B02
直接相位 $\omega m$；统一缩放为 $\omega m/s$；截断在 $m>w$ 时为 $\omega w$。前两者仍区分任意位置但相位速率不同，截断后所有超窗位置在该通道完全相同。

### ARCH-EXT-B03
新相位为 $(1\cdot8/4,0.1\cdot8/2,0.01\cdot8/1)=(2,0.4,0.08)$。高频被压缩最多、局部相位差从 1 降到 .25；低频保持，体现逐尺度权衡，而非全频统一降低分辨率。

## C. 推导与证明

### ARCH-EXT-C01
若 $0\le m<L_1=sL_0$，则 $0\le m/s<L_0$。测试相邻 token 的映射差为 $(m+1)/s-m/s=1/s$，所以原本相邻整数训练坐标之间插入 $s-1$ 个测试位置，局部分辨率被压缩。

### ARCH-EXT-C02
原相对相位 $\Delta\phi_i=\omega_i\Delta m$；尺度后为 $\omega_i\Delta m/s_i$，等价于新频率 $\omega_i'=\omega_i/s_i$、新波长 $\lambda_i'=2\pi/\omega_i'=s_i\lambda_i$。因此每个 $s_i$ 分别改变该尺度的覆盖和邻位相位差。

### ARCH-EXT-C03
一种简化函数 $g(r)=r$ 当 $|r|\le w$，$g(r)=w\operatorname{sgn}(r)$ 当 $|r|>w$。它在 $\pm w$ 连续但导数跳变；局部相位精确保留，远端全部碰撞。更精细 ReRoPE 类实现可让远段另行映射，但可能需要按 pair 距离生成旋转/score，不能总靠一次预旋转 K 完成，增加计算接口。

## D. 边界、反例与纠错

### ARCH-EXT-D01
压回范围只控制相位数值域，却改变邻距为 $1/s$；模型训练时未必见过这些密集相位组合。候选数、softmax 与任务也变化。PI 原工作仍使用长上下文微调与实验验证，因此不能从映射公式推出免训练成功。

### ARCH-EXT-D02
模型永远只看最近 128 token，测试任务的答案也都在末尾 64 token；无论输入扩到 1M，它都可满分，却对开头证据完全不敏感。故长输入成功只证明局部任务兼容，需把唯一证据放在多档远位置并做删除/置换干预。

### ARCH-EXT-D03
Base 改变整条几何频率阶梯：慢频覆盖加长但若邻位相位太小会降低短程分辨率，模型原有权重又适配旧频率。不同任务依赖不同距离尺度，所以可能在某长度/任务获益、在另一处退化。

## E. AI 迁移

### ARCH-EXT-E01
固定 checkpoint、数据、长微调 token/步数、optimizer、可见域、dtype 与推理 kernel；方法包括原频率、PI、全频 scale、逐频 scale、局部窗口。用相同超参搜索预算，多 seed 扫描 length×target position×任务，报告短程回归、远程质量、FLOPs/显存和 cache 兼容。

### ARCH-EXT-E02
核对 checkpoint 预期 base/scale、config 序列化、训练/serving position IDs、prefill/chunk/decode offset、cache 中 K 是旋转前还是后、已有 cache 是否可复用、packing/left padding、kernel 对逐频/分段映射支持，以及版本回滚。迁移后必须做 full/cache 等价和短长回归。

### ARCH-EXT-E03
从训练数据划出不用于最终报告的 context-extension validation suite，在预先固定的长度/位置/任务网格上用相同预算选择尺度；锁定超参后只运行一次 test suite。报告搜索空间与选取准则，并保留未调参的基线，避免 test-on-test。

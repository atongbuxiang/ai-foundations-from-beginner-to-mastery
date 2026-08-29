---
type: concept
status: draft
area: [neural-networks/gradient-checking, checkpointing, higher-order-differentiation]
aliases: [Gradcheck, Activation Checkpointing, Higher-Order AD Boundaries]
node_id: NN-16
prerequisites: ["[[Forward_Reverse AD、Tape 与复杂度]]", "[[Taylor 展开与余项]]", "[[浮点数与舍入误差]]", "[[Hessian、二阶微分与曲率]]"]
related: ["[[误差传播、条件估计与停止准则]]", "[[逆矩阵、线性求解与隐式微分]]", "[[计算图、反向传播与自动微分 MOC]]"]
sources: ["[[S-1994-Pearlmutter-Fast-Exact-HVP]]", "[[S-2016-Chen-Sublinear-Memory]]", "[[S-2026-JAX-Autodiff-Checkpointing]]", "[[S-2026-PyTorch-Autograd-Gradcheck]]", "[[S-2008-Griewank-Walther-Evaluating-Derivatives]]"]
exercises: ["[[习题 - Gradient Checking、Checkpointing 与高阶微分边界]]"]
solutions: ["[[解答 - Gradient Checking、Checkpointing 与高阶微分边界]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-gradient-checkpoint-higher-order-v2.svg]]"
created: 2026-08-23
updated: 2026-08-29
---
# Gradient Checking、Checkpointing 与高阶微分边界

> [!abstract] 本章主问题
> 一阶 AD 返回一个数不等于梯度已经可信。梯度检查应用方向中心差分、Taylor residual、JVP/VJP 伴随测试和交叉模式建立证据，并识别截断误差与舍入误差的 U 形权衡。checkpointing 则在数学上不改变函数，通过重算 residuals 用 FLOPs 换激活内存；但 RNG、state、mutation 不能忠实回放时，它会直接改变求导程序。高阶 AD 还需对 kink、custom rule、隐式求解和 complex convention 设置更严格边界。

## 课程位置与两遍学习路线

- **承接什么：** NN-15 已说明 AD 怎样组合 local rules，但“两个模式给出同一个数”仍可能共享同一实现错误；
- **本页解决什么：** 用中心差分、Taylor slope、adjoint test 和解析 HVP 形成独立证据链，再把 checkpoint 的 time–memory 交换与高阶边界分开；
- **后续为何需要：** 这一页是 30.2 的材料出口；后续激活、初始化和深层训练分析都默认你能判断 gradient 是数学错误、实现错误还是数值错误。

**第一遍只完成验证漏斗。** 先在 FP64 光滑小例上比较 hand value、AD directional derivative 和多个 $h$ 的中心差分，再检查 Taylor residual 是否呈二阶斜率。

**第二遍再处理系统与高阶。** 比较 checkpoint on/off 的 RNG/state/effect，推导 HVP 而不形成 Hessian，并审计 kink、custom rule、implicit solver、complex 和 mixed precision。

### 问题链

1. 为什么一次 `gradcheck=True` 不能证明整张训练图正确？
2. 中心差分的截断误差与舍入误差为什么形成 U 形曲线？
3. JVP/VJP dot test 能发现什么，又可能共同漏掉什么？
4. checkpointing 在什么语义条件下只换时间与内存而不改 gradient？
5. HVP 为什么无需显式 $n\times n$ Hessian，高阶结果又在哪些 primitive 上失去 classical 含义？

> [!check] 第一遍停靠线
> 若你能在贯穿方向上复现梯度约 $-0.00123631$，观察中心差分收敛，并算出 HVP 系数约 $0.00123325$，就完成 30.2 第一遍；checkpoint 调度和全部高阶边界留到第二遍。

## 符号与对象账本

| 对象 | 数学/系统身份 | 在 AI 验证中的作用 | 不能证明什么 |
|---|---|---|---|
| $h$ | finite-difference step | 控制 truncation/roundoff tradeoff | 单一 $h$ 不能给全尺度证据 |
| $v$ | parameter/logit direction | 高维 directional probe | 有限方向不能覆盖全空间 |
| $R(h)$ | Taylor residual | 检查一阶模型的 $O(h^2)$ 区间 | 不验证建模目标正确 |
| checkpoint | 保存的 execution boundary | 用重算换 activation memory | RNG/state 不等价时不保梯度 |
| $Hv$ | Hessian linear action | curvature、implicit/C-G 接口 | 不等于 full Hessian 或最优性证书 |

### 贯穿算例：独立检查同一方向并进入二阶

沿用 $X_\diamond$ 路径的 $F(Q)$ 与 $V=E_{11}$。解析一阶值为

$$
g_V=\langle\nabla F,V\rangle_F=\frac{P_{11}-1}{2}\approx-0.00123631.
$$

中心差分

$$
D_h=\frac{F(Q+hV)-F(Q-hV)}{2h}
$$

应在合适的 FP64 区间趋近 $g_V$；一阶 Taylor residual $|F(Q+hV)-F(Q)-hg_V|$ 应先按 $h^2$ 下降。沿同一方向的 HVP 为第一样本 softmax covariance 的对应作用：

$$
(HV)_{1,:}=\frac{P_{11}P_{12}}2(1,-1)\approx0.00123325(1,-1),\qquad (HV)_{2,:}=0.
$$

这给出与一阶 VJP 不同的独立二阶目标。若 checkpoint 重放 NN-13/14 的图，还必须恢复相同 ReLU-zero convention、reduction、RNG/state 与有效样本计数。

## 核心公式七问：$E(h)\approx C_1h^2+C_2u/h$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 解释中心差分为何不能无限减小 step，并指导多尺度 sweep |
| 对象 | $h$ 是 step，$u$ 是 unit roundoff，$C_1,C_2$ 依函数曲率和数值 scale |
| 来路 | 对称 Taylor 展开消去偶次一阶外项，函数值相减再引入相对舍入放大 $1/h$ |
| 步骤 | 从较大 $h$ 逐级减半，寻找二阶下降区、最低点与 roundoff 回升区 |
| 读法 | 左侧由截断主导，右侧由消去/舍入主导，中间才是可信检查窗口 |
| 检查 | 改 dtype/scale 后最低点应移动；kink、噪声或 stateful forward 可破坏模型 |
| 去路 | custom-op gradcheck、Taylor test、checkpoint replay audit、HVP symmetry 与高阶 AD |

## 一、为什么不只看框架输出

梯度可以因以下原因“有数值但不对”：

- local VJP 的 transpose/axis/scale 错误；
- fan-out 漏累加，broadcast 归约错轴；
- custom backward 与 forward 不一致；
- in-place/alias 破坏 residual；
- loss mean/sum、mask 或 distributed scale 不一致；
- 在不可微点比较了不同 convention；
- 数值 overflow/underflow/cancellation；
- 所实现的损失本身就不是想要的建模对象。

因此验证必须分为数学、实现、数值和建模四层。

## 二、方向中心差分

对 scalar $f:\mathbb R^n\to\mathbb R$ 和方向 $v$，中心差分为

$$
D_hf(x)[v]
=\frac{f(x+hv)-f(x-hv)}{2h}.
$$

当 $f$ 充分光滑，截断误差为 $O(h^2)$；浮点函数值相减的舍入/消去误差约为 $O(u/h)$。总误差粗略是

$$
E(h)\approx C_1h^2+C_2\frac{u}{h}.
$$

所以 $h$ 太大或太小都错，最佳量级与 $u^{1/3}$ 及输入/函数 scale 有关。单一固定 `eps` 不是通用答案。

## 三、方向检查比逐坐标更实用

若 AD 给出 $g=\nabla f(x)$，比较

$$
g^Tv
\quad\text{and}\quad
\frac{f(x+hv)-f(x-hv)}{2h}.
$$

随机方向一次同时混合许多坐标，适合高维参数；但有限次随机测试仍可漏掉正交子空间中的 bug。对小 tensor，还应补逐坐标或 full Jacobian 检查。

## 四、Taylor Residual Test

定义一阶余项

$$
R(h)=\left|f(x+hv)-f(x)-h g^Tv\right|.
$$

若 $f$ 二阶光滑且 $g$ 正确，在截断误差主导区间，

$$
R(h)=O(h^2).
$$

将 $h$ 减半，$R$ 应约减至 $1/4$；继续减小后会进入 roundoff floor。只看某个 $h$ 的绝对误差，比看 log–log slope 弱得多。

## 五、JVP/VJP 伴随检查

对 $f:\mathbb R^n\to\mathbb R^m$，随机取 $v\in\mathbb R^n$、$u\in\mathbb R^m$，检查

$$
u^T(Jv)=(J^Tu)^Tv.
$$

该 dot test 不需 finite-difference step，专门检查两个实现是否互为伴随。它会对 transpose、broadcast axis、conjugation 和 accumulation 错误很敏感；但如果 JVP 和 VJP 共用同一错误核心，可能同时错且仍通过，因而还需独立差分证据。

## 六、手算一个 Step Sweep

令 $f(x)=\sin(x^2)$，在 $x=1$，

$$
f'(1)=2\cos1\approx1.0806046.
$$

对 $h=10^{-1},10^{-2},…$计算中心差分，误差应先约按 $h^2$ 下降，然后在机器精度附近回升。如果从第一个点就无二阶 slope，要检查是否在 kink、函数含噪声，或 AD 实现错误。

## 七、Complex-Step 的长处与严格边界

对能全纯解析延拓到复数的一元函数，

$$
f'(x)\approx\frac{\operatorname{Im}f(x+ih)}{h}
$$

避免两个相近实数函数值相减，可用很小 $h$。但 abs、ReLU、comparison、branch、conjugation、非全纯 operation 或不支持 complex dtype 的 kernel 会使此法不适用。它不是任意神经网络的默认 gradcheck。

## 八、Activation Checkpointing 的基本合同

对链

$$
x_0\xrightarrow{f_1}x_1\xrightarrow{f_2}\cdots\xrightarrow{f_n}x_n,
$$

标准 reverse 可保存所有 $x_i$，内存 $O(n)$。若每隔 $k$ 层保存 checkpoint，backward 时从最近 checkpoint 重放区间，peak activation memory 粗略为

$$
O\!\left(\frac{n}{k}+k\right).
$$

取 $k\approx\sqrt n$ 得 $O(\sqrt n)$ 内存，并增加约一次 forward 量级的重算。更极端的递归调度可达 $O(\log n)$ 内存，但可增加 $O(n\log n)$ 前向工作。

## 九、为什么 Checkpoint 位置很重要

在 $f=h\circ g$ 中，若只对整个 $f$ checkpoint，可能先做一次丢弃 residual 的完整 forward，紧接着又重放并保存所有 residual，peak memory 并未下降。对最后一个子函数 checkpoint 也常因立即重放而节省有限。

合理分割应考虑：

- 各 block residual 字节数；
- 重算 FLOPs 与 kernel latency；
- skip connections 跨越分割边界的 live tensors；
- attention 中不同中间量的大小；
- communication/collective 是否会被重放；
- compiler 是否已自动 rematerialize。

## 十、重放必须是语义等价的

checkpoint 要求重算得到与原 forward 一致的 local derivative coefficients。下列情况是高风险：

- dropout 或 stochastic depth 重放时消耗了不同 RNG state；
- BatchNorm running statistics 被第二次更新；
- stateful cache/counter 改变 control flow；
- in-place mutation 使 checkpoint input 已不是原值；
- non-deterministic collective/atomic reduction 产生不同路径；
- external I/O 或时间依赖算子无法回放。

实现需要 preserve/restore RNG state、functional state threading 或禁止不可回放 effects。

## 十一、Hessian–Vector Product 不需 Full Hessian

对 $f:\mathbb R^n\to\mathbb R$，

$$
Hv
=\left.\frac{d}{d\varepsilon}
\nabla f(x+\varepsilon v)\right|_{\varepsilon=0}.
$$

forward-over-reverse 先构造 gradient 的 reverse program，再对其做一个 JVP，以常数倍 gradient cost 得 $Hv$，不形成 $n\times n$ Hessian。Pearlmutter 的经典结果正是这种 matrix-free 二阶作用。

可用对称点积检查

$$
u^THv\approx v^THu
$$

审计 HVP；但在不光滑点、数值不稳定或 custom higher-order rule 不对时，对称可失效。

## 十二、高阶 AD 的主要边界

### 12.1 不光滑原语

ReLU 的 Hessian 在非零点为 0，在 0 不存在 classical Hessian。“框架返回 0”只反映选定 convention。

### 12.2 Custom VJP/JVP

一阶 custom rule 可能使用 stop-gradient、不可微 external code 或与 forward 不同的 surrogate，对它再求导得到的不一定是原函数的二阶 derivative。

### 12.3 隐式求解

隐式梯度依赖前向残差、Jacobian 可逆性/条件性和伴随求解容差。高阶时还需对线性求解和 Jacobian coefficients 再求导，不能忽略 solver stopping rule。

### 12.4 Complex Values

一般 real-valued loss 对 complex parameters 需 Wirtinger/conjugate-Wirtinger 约定，VJP 涉及 conjugation。复数 gradcheck 不能照搬实数 Jacobian 规则。

### 12.5 Mixed Precision 与 Scaling

loss scaling 在 backward 中人为放大一阶 gradient 后再 unscale；二阶组合若在错误位置对 scaled gradient 求导，可多出 scale factors。应在 FP64 小例上先验数学公式，再测低精度稳定性。

## 十三、四层调试漏斗

1. **对象层**：输入、输出、loss、reduction、mask 是否正确；
2. **局部层**：每个 primitive 的 JVP/VJP、shape 与 dot test；
3. **子图层**：手算小例、directional difference、Taylor slope、full Jacobian/Hessian 对照；
4. **系统层**：checkpoint 前后、eager/compiled、single/distributed、FP64/32/16 交叉比较。

当测试失败，从最小 deterministic FP64 子图向外扩展，比直接在整模型上看 gradient norm 更快定位。

## 十四、图：检查、重算与高阶是三个不同问题

先看图回答：为什么 finite-difference error 随 $h$ 先降后升，而 checkpoint 的 memory 可随 segment length 出现 $n/k+k$ 的内部最优点？

![[00-知识库管理/_assets/figures/neural-networks/fig-gradient-checkpoint-higher-order-v2.svg|900]]

> [!figure] 图 30.2-08　差分 U 形、checkpoint 分段与 HVP/高阶边界
> 左栏分解 $O(h^2)+O(u/h)$ 并标出 Taylor-test 斜率区；中栏把保存 checkpoints 与区间重放画成 time–memory 账本；右栏将 HVP 作用与 kink、custom rule、solver、complex 及 mixed-precision 边界分开。来源：依据 Pearlmutter 1994、Chen 等 2016 及 JAX/PyTorch 官方文档独立绘制；由 [[00-知识库管理/_labs/code/plot_backprop_advanced_v2.py]] 确定性生成。

**怎样读图**：先用多个 $h$ 找截断主导区间，再依 activation bytes/FLOPs 选 checkpoint 分割，最后对高阶路径逐 primitive 检查可组合性。

**图没有证明什么**：图没有保证某个固定 `eps` 适用所有 dtype/scale，也没有保证 $\sqrt n$ 分段在实际 Transformer/通信图上最优，或框架二阶数值必是 classical Hessian。

## 十五、发布前验收

1. FP64 deterministic 小例上做 hand gradient；
2. 至少 6 个 $h$ 的 central-difference/Taylor sweep；
3. JVP/VJP dot test 与交叉 AD mode；
4. 小维 full Jacobian/Hessian 或对称 HVP test；
5. kink/tie 两侧与 convention 点分开测；
6. checkpoint on/off 的 forward、gradient、RNG/state 一致性；
7. peak memory、extra FLOPs、latency 与 communication 实测；
8. custom/implicit/complex/mixed-precision 的高阶专项测试。

## 十六、回顾与练习

> [!summary]
> 梯度可信性来自独立证据的交叉，不是一次 `gradcheck=True`。checkpoint 在理想语义下用重算换内存，但必须忠实回放 RNG/state/effects。HVP 可 matrix-free 计算，高阶结果则受不光滑、custom rules、solver 与数值 scale 限制。

- [[习题 - Gradient Checking、Checkpointing 与高阶微分边界]]
- [[解答 - Gradient Checking、Checkpointing 与高阶微分边界]]

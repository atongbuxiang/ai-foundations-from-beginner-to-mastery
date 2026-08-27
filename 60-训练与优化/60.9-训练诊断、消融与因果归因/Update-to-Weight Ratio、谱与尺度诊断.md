---
type: concept
status: verified
area: [training, optimization, scale-diagnostics, spectral-analysis]
course_id: TRN-67
prerequisites: ["[[训练 Telemetry、损失梯度更新与激活总账]]", "[[全局逐层梯度裁剪、AGC 与裁剪偏差]]", "[[矩阵范数]]", "[[奇异值分解]]"]
related: ["[[NaN、Inf、梯度爆炸与训练失败决策树]]", "[[数据优化器调度交互、混杂与归因边界]]"]
sources: ["[[S-2017-You-LARS]]", "[[S-2020-You-LAMB]]", "[[S-2021-Brock-AGC-NFNet]]", "[[S-2021-Cohen-Edge-of-Stability]]", "[[S-2026-Su-11736-矩阵谱范数估计]]", "[[S-2025-Su-11267-Adam-Update-RMS]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Update-to-Weight Ratio、谱与尺度诊断

> [!abstract] 本节目标
> 从“梯度有多大”走向“参数实际移动了多远、沿哪些方向移动、相对于哪种参数尺度”。你将能计算 parameter/layer/unit/spectral UWR，识别重参数化陷阱，并把 LARS、LAMB、AGC、谱范数与 Hessian sharpness 放进同一诊断坐标系。

## 一、真正驱动下一步的是 update，不是 raw gradient

统一写优化器：

$$
d_t=P_t(g_t,s_t),
\qquad
\Delta_t=-\eta_t d_t+\Delta_t^{\mathrm{decay}},
\qquad
\theta_{t+1}=\theta_t+\Delta_t.
\tag{1}
$$

$P_t$ 可能包含 momentum、Adam 分母、矩阵预条件、clipping 或 trust ratio。于是同一个 $\|g_t\|$ 可以对应完全不同的 $\|\Delta_t\|$；相反，raw gradient 变小，若 denominator 变得更小，实际 update 仍可能增大。

最基本的 update-to-weight ratio 是

$$
\rho_t(\theta)=
\frac{\|\Delta_t\|}{\|\theta_t\|+\varepsilon}.
\tag{2}
$$

它近似回答“一步改了当前参数尺度的多少比例”。但范数、分组、epsilon 和是否含 decay 都是定义的一部分。

## 二、四个层级不能互相替代

### 2.1 全局 ratio

$$
\rho_{global}=\frac{\|\Delta\|_2}{\|\theta\|_2+\varepsilon}.
\tag{3}
$$

便宜、适合总览，却会被大层支配。

### 2.2 参数组/层级 ratio

$$
\rho_l=\frac{\|\Delta W_l\|_F}{\|W_l\|_F+\varepsilon_l}.
\tag{4}
$$

可发现 embedding、attention、MLP、readout 的不平衡；这是 LARS/LAMB 一类 layerwise scaling 的主要观测坐标。

### 2.3 unit-wise ratio

若 $W$ 的一行对应输出 unit，可定义

$$
\rho_i=\frac{\|\Delta W_{i,:}\|_2}{\max(\|W_{i,:}\|_2,\varepsilon)}.
\tag{5}
$$

[[S-2021-Brock-AGC-NFNet]] 的 AGC 比较 gradient unit norm 与 weight unit norm，再缩小超阈值 gradient。unit 轴必须按算子语义声明。

### 2.4 谱 ratio

对矩阵层：

$$
\rho_{spec}(W)=
\frac{\|\Delta W\|_2}{\|W\|_2+\varepsilon},
\tag{6}
$$

其中 $\|\cdot\|_2=\sigma_{max}$。它关心最坏输入方向的 operator change，而 Frobenius ratio 关心全部元素能量。两者回答不同问题。

## 三、为什么 RMS 正常仍可能藏着谱尖峰

设 $\Delta W$ 是 $d\times d$ rank-one 更新，唯一奇异值为 $a$。则

$$
\|\Delta W\|_F=a,
\qquad
\operatorname{RMS}(\Delta W)=\frac{a}{d},
\qquad
\|\Delta W\|_2=a.
\tag{7}
$$

当 $d$ 很大，entry RMS 很小，但一个方向仍被改变 $a$。反过来，各向同性小更新可能有较大 Frobenius norm，却没有突出的单方向变化。

可同时记录 stable rank：

$$
r_{stable}(A)=\frac{\|A\|_F^2}{\|A\|_2^2}.
\tag{8}
$$

若 update RMS 稳定而 $r_{stable}(\Delta W)$ 突降，说明能量集中到少数方向；这可能比全局 norm 更早提示不稳定。

## 四、LARS、LAMB 与 AGC 放在同一张表里

| 方法/指标 | 比较对象 | 作用位置 | 主要目的 |
|---|---|---|---|
| LARS | $\|W_l\|/\|g_l+\text{decay}\|$ | layer LR/trust ratio | 大批量下层级步长对齐 |
| LAMB | $\|W_l\|/\|d_l^{Adam}\|$ | Adam-like direction 后 | coordinate adaptation + layer scaling |
| AGC | unit $\|g_i\|/\|W_i\|$ | gradient clipping | 限制局部相对梯度 |
| telemetry UWR | $\|\Delta_l\|/\|W_l\|$ | update 写回后观察 | 描述实际参数位移 |

关键区别是**被归一的对象**：raw gradient、含 decay 的方向、预条件方向还是 realized update。若混写，日志上的“trust ratio”无法解释。

## 五、重参数化会改变 ratio

考虑两层正齐次网络

$$
f(x)=W_2\phi(W_1x),
$$

若 $\phi(cz)=c\phi(z)$，则

$$
(W_1,W_2)\mapsto(cW_1,c^{-1}W_2)
\tag{9}
$$

保持函数不变，却改变两层 weight norm、gradient norm 和普通 UWR。BatchNorm/LayerNorm、weight tying、factorization 也引入尺度自由度。因此：

- UWR 是参数坐标中的诊断，不天然是函数空间距离；
- 跨架构/参数化比较需先对齐 parameterization；
- 可补充 feature change、logit KL、Jacobian/operator change 等函数级指标。

一个 ratio 突变可能来自 weight denominator 接近零，而不是 update 真的很大。bias、norm scale、embedding row 等需专门 epsilon/分组合同。

## 六、参数谱、更新谱和曲率谱是三件事

### 6.1 参数谱

$\sigma_i(W)$ 描述线性层对不同输入方向的增益。可监测 $\sigma_{max}$、Frobenius、stable rank 和 top-$k$ 谱占比。

### 6.2 更新谱

$\sigma_i(\Delta W)$ 描述本步改动集中在哪些方向。进一步看对齐：

$$
\cos(\Delta W,W)
=\frac{\langle\Delta W,W\rangle_F}
{\|\Delta W\|_F\|W\|_F}.
\tag{10}
$$

decay 会产生强负向对齐，不能误读为 task gradient。

### 6.3 曲率谱

Hessian top eigenvalue $\lambda_{max}(H_t)$ 衡量局部二阶 sharpness。固定二次模型中 GD 稳定阈值约为 $\eta\lambda_{max}<2$；[[S-2021-Cohen-Edge-of-Stability]] 观察到深网训练常在 $2/\eta$ 附近活动，但非线性时变轨迹不能直接套静态二次定理。

参数谱大、update 谱尖或 Hessian sharp 是不同现象，只有实证关系，不能由一个推出另一个。

## 七、谱量怎样在大模型上估计

对矩阵 $A$，power iteration：

$$
v_{k+1}=\frac{A^\top Av_k}{\|A^\top Av_k\|},
\qquad
\hat\sigma_k=\|Av_k\|.
\tag{11}
$$

它通常给出随迭代改善的估计/下界，收敛速度受谱隙和初始对齐影响。[[S-2026-Su-11736-矩阵谱范数估计]] 讨论 power、Krylov 与 Schatten 路径；课程要求记录：iteration、warm start、residual/重复性和采样频率，不把有限步估计标成 exact norm。

对 Hessian 可用 HVP + Lanczos；对超大层可采 top layers/blocks，但必须标明覆盖率。谱诊断应低频或触发式，避免本身成为训练瓶颈。

## 八、怎样建立健康基线，而不是迷信阈值

不存在跨任务统一的“UWR 应为 0.01”。合理基线来自：

1. 同一 parameter group 的历史 phase；
2. 小规模稳定 run 的分布；
3. 理论参数化/优化器给出的量级预测；
4. 与 feature/logit change 和 loss 反应的联合校准。

建议每组记录 median、p90/p99、max、zero/near-zero denominator 比例，并对 warmup、stable、decay 分 phase。阈值触发后问：是 numerator 增大、denominator 缩小、optimizer state 改变，还是分组/shape 变了？

## 九、一个尺度诊断例子

某 Transformer 在第 30k step validation 恶化：

- global grad norm 与 update RMS 正常；
- embedding global UWR 正常，但少数稀有 token row 的 unit UWR 为中位数 50 倍；
- attention output projection 的 $\rho_{spec}$ 上升，stable rank 降低；
- top Hessian estimate 同时接近局部 $2/\eta$；
- feature cosine change 在同一窗口跳变。

这组证据支持“局部/方向性尺度异常”，却仍不能区分数据稀有 token、optimizer state 稀疏更新和 LR schedule 交互。下一节需要用因果设计分离。

## 十、科学空间研读框：从 RMS 走向谱

科学空间的 Update/Weight RMS 系列给出均值场尺度坐标，[[S-2026-Su-11736-矩阵谱范数估计]] 则提醒矩阵层还存在 worst-direction 结构。二者组合成可证伪问题：

- RMS 预测准确时，谱尖峰是否仍能出现？
- 谱估计变化是否先于 feature/loss 变化？
- 不同参数化下 ratio 是否保持，若不保持应转到何种函数级指标？

这比把某个单一数值当作“健康证书”更接近真实诊断。

## 十一、图解：尺度诊断立方体

带着一个问题读图：**global RMS 正常时，哪两个维度还能暴露局部危险？**

![[00-知识库管理/_assets/figures/training-optimization/fig-update-weight-spectrum-cube-v1.svg|880]]

> [!figure] 图 TRN-67-01　对象层级 × 范数几何 × 训练时钟
> 来源：自绘机制图；layerwise adaptation 依据 [[S-2017-You-LARS]]、[[S-2020-You-LAMB]]，谱估计接口依据 [[S-2026-Su-11736-矩阵谱范数估计]]。

**怎样读图**：沿对象轴从 global 到 layer/unit，沿几何轴从 RMS/Frobenius 到 operator/spectrum，再沿时间轴比较 gradient、direction 与 realized update；任何结论至少标明三个坐标。

**图没有证明什么**：落在某个 ratio 区间不保证优化稳定或泛化良好；谱估计也受 iteration、谱隙和采样层影响。

## 十二、核心结论

UWR 的正确问题不是“数值是否小”，而是“哪个对象、哪种范数、哪部分更新、相对于哪个参数坐标、在哪个训练 phase”。scalar、layer、unit、spectral 和 function-space 指标互补；跨参数化时尤其不能让一个漂亮 ratio 代替完整机制。

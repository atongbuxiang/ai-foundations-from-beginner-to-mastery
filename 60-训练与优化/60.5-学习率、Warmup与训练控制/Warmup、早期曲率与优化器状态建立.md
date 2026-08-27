---
type: derivation
status: verified
area: [training, optimization, warmup, stability]
node_id: TRN-34
aliases: [学习率预热, Learning Rate Warmup]
prerequisites: ["[[学习率、局部损失变化与相对更新尺度]]", "[[二次模型的学习率—动量稳定域与阻尼]]", "[[Adam 的一阶二阶矩、偏差修正与逐坐标步长]]"]
related: ["[[Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 调度]]", "[[NaN、Inf、梯度爆炸与训练失败决策树]]", "[[训练 Telemetry、损失梯度更新与激活总账]]"]
sources: ["[[S-2017-Goyal-Large-Batch-Warmup]]", "[[S-2024-Kalra-Barkeshli-Warmup]]", "[[S-2024-Kosson-Warmup-GPT]]", "[[S-2024-Su-10657-梯度裁剪模长]]", "[[S-2020-Xiong-Transformer-LayerNorm]]"]
exercises: ["[[习题 - Warmup、早期曲率与优化器状态建立]]"]
solutions: ["[[解答 - Warmup、早期曲率与优化器状态建立]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-warmup-mechanism-hypothesis-ledger-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Warmup、早期曲率与优化器状态建立

> [!abstract] 一句话结论
> Warmup 是“训练初期暂不使用完整目标学习率”的控制策略，不是单一机制。它可能同时缓解局部稳定性、optimizer state 尚未建立、相对更新过大、早期噪声/critical batch、低精度 overflow 和架构信号传播问题；观察到 warmup 有效，不能反推出其中某个解释唯一正确。

## 一、先把 Warmup 定义完整

设目标 peak learning rate 为 $\eta_{\mathrm{peak}}$，warmup 长度为 $T_w$。最常见的线性预热是

$$
\eta_t
=\eta_0
+(\eta_{\mathrm{peak}}-\eta_0)
\frac{t}{T_w},
\qquad 0\le t\le T_w.
\tag{1}
$$

但一个可复现实验还必须回答：

1. $t$ 从 0 还是 1 开始，端点是否包含；
2. $T_w$ 用 optimizer step、sample 还是 token；
3. overflow/skipped step 是否推进 $t$；
4. momentum/Adam moments 从第一步就更新，还是也被延迟；
5. weight decay 和 EMA 是否使用 warmup 后的 $\eta_t$；
6. clip threshold 是否固定，还是与 LR 联动；
7. 从 $\eta_0=0$、极小正数还是非零安全 LR 开始。

> [!warning] 名称边界
> warmup 只描述 LR 的早期上升。数据 curriculum、batch ramp-up、sequence-length ramp-up、loss-scale growth、冻结/解冻层和 optimizer-state burn-in 都是不同控制器，即使它们在时间上重合。

## 二、机制假说 A：早期曲率与局部稳定域

在局部二次近似中，最陡方向的稳定性受

$$
\eta_t\lambda_{\max}(H_t)
\tag{2}
$$

控制。若训练初期 $\lambda_{\max}(H_t)$ 很大，直接使用 target LR 可能越过局部稳定域。

一维二次型再次给出

$$
\theta_{t+1}=(1-\eta_t\lambda)\theta_t,
$$

稳定要求 $0<\eta_t\lambda<2$。Warmup 让 $\eta_t$ 逐步增加；若同时轨迹进入更低 sharpness 区域，后期可能容忍更大 LR。

[[S-2024-Kalra-Barkeshli-Warmup]] 的重要贡献是把这个说法变成可测假说：

- 记录 top Hessian eigenvalue 或 HVP proxy；
- 区分 progressive sharpening、sharpness reduction 和 catapult regime；
- 同时改变初始化、参数化、$\eta_0$ 与 $\eta_{\mathrm{peak}}$。

**不能偷换**：深网 $H_t$ 随轨迹变化，负曲率、随机梯度和 momentum 都使固定二次模型不完整。warmup 有效不等于式 (2) 是唯一原因。

## 三、机制假说 B：Adam 类状态尚未建立

Adam 的零初始化状态为

$$
m_0=0,\qquad v_0=0.
$$

即使有 bias correction，

$$
\widehat m_t=\frac{m_t}{1-\beta_1^t},
\qquad
\widehat v_t=\frac{v_t}{1-\beta_2^t},
\tag{3}
$$

早期方向仍可能特殊，因为：

- 样本数少，$\widehat v_t$ 对当前 batch 极敏感；
- $\epsilon$ 与 $\sqrt{\widehat v_t}$ 的相对大小处于过渡区；
- momentum direction 尚未反映稳定的历史；
- 分布式、稀疏梯度与 skipped step 会改变状态年龄。

对第一次非零梯度，忽略 $\epsilon$，

$$
\frac{\widehat m_1}{\sqrt{\widehat v_1}}
\approx \operatorname{sign}(g_1),
\tag{4}
$$

所以参数位移可能接近每坐标 $\eta_1$，而不是随 $|g_1|$ 缩小。若参数本身很小，relative update 可很大。

Warmup 通过减小 $\eta_t$ 限制早期位移，但另一条干预是改变状态初始化或显式归一化 $u_t$。[[S-2024-Kalra-Barkeshli-Warmup]] 和 [[S-2024-Kosson-Warmup-GPT]] 都给出“减少 warmup”的替代干预，这正说明机制可以被区分实验检验。

## 四、机制假说 C：参数角度与表示变化过大

即使全局

$$
\lVert\Delta\theta_t\rVert_2
$$

看起来不大，小权重层或尺度不变层仍可能发生大角更新。设某层权重为 $W$，小步下角变化近似由

$$
\frac{\lVert\Delta W_\perp\rVert_F}{\lVert W\rVert_F}
\tag{5}
$$

控制。若初始化使 $\lVert W\rVert$ 小，第一批 normalized updates 会带来大的方向旋转。

更接近功能的量是固定 probe 上

$$
\frac{\operatorname{RMS}(\Delta h)}
{\operatorname{RMS}(h)+\varepsilon}.
\tag{6}
$$

[[S-2024-Kosson-Warmup-GPT]] 在 GPT 训练中同时考察 update norm、angular change 和 representation impact，并发现显式限制这些量可显著减少 warmup 需求。

**边界**：probe feature change 依赖数据与层位置；小变化不保证优化快，大变化也不一定有害，catapult 正是可能受益于暂时非线性跃迁的例子。

## 五、机制假说 D：早期噪声与 Batch 临界尺度不同

训练早期的 signal、gradient covariance 和 curvature 都会变化。即使 batch $B$ 固定，noise scale 或 critical batch 也未必固定。

若简单写

$$
\widehat g_t=g_t+\xi_t,
\qquad
\mathbb E[\xi_t]=0,
\qquad
\operatorname{Cov}(\xi_t)\approx\frac{\Sigma_t}{B},
\tag{7}
$$

则一步二阶期望变化包含

$$
\frac{\eta_t^2}{2B}
\operatorname{tr}(H_t\Sigma_t).
\tag{8}
$$

较小的早期 $\eta_t$ 同时抑制 deterministic curvature term 和 stochastic term。大 batch 线性缩放把 target LR 推大后，warmup 可能尤其重要；[[S-2017-Goyal-Large-Batch-Warmup]] 的 ImageNet 协议就是经典工程证据。

**不能外推**：$\Sigma_t/B$ 需要独立同分布和 mean reduction 等条件；Adam/Muon 的非线性方向使式 (8) 只是一阶入口。

## 六、机制假说 E：数值范围与系统状态

在 FP16/BF16/FP8 或混合精度训练中，早期大激活、梯度和 update 可能触发：

- overflow/Inf/NaN；
- dynamic loss-scale 回退；
- skipped optimizer step；
- 梯度归约前后的有限精度差异；
- optimizer state 的 step counter 与 scheduler counter 不同步。

warmup 可降低参数位移，却不直接缩小反向传播得到的 raw gradient；因此若 overflow 发生在 optimizer 之前，单靠 LR warmup 可能无效。

> [!example] 反例
> 若 loss scaling 使反向梯度在 unscale 前已经 overflow，$\eta_t$ 尚未参与计算。把 LR 降到零也不能恢复丢失的 Inf。必须定位第一个异常张量和运算阶段。

## 七、机制假说 F：架构与参数化的早期信号传播

Pre-Norm/Post-Norm、残差缩放、初始化方差、depth、width、bias/norm 参数组都会改变早期 Jacobian 和曲率。[[S-2020-Xiong-Transformer-LayerNorm]] 说明 normalization placement 会改变 Transformer 初始化附近的梯度规模，这为特定架构的 warmup 需求提供理论/实验线索。

但：

- “Pre-Norm 较少需要 warmup”不是无条件定理；
- 更换 optimizer、depth、residual scale、batch 或 precision 后需重测；
- parameterization 可能让 raw gradient 稳定，却让 feature update 失稳，反之亦然。

## 八、怎样设计能区分机制的实验

不要只比较“有 warmup/无 warmup”。应使用干预矩阵：

| 干预 | 若改善，支持什么 | 仍不能排除什么 |
|---|---|---|
| 降低 $\eta_0$、固定 $\eta_{\mathrm{peak}}$ | 早期 step 过大 | 曲率/状态/角度具体哪一个 |
| 改初始化或 residual scale | 参数化/信号传播 | 同时改变了曲率与 feature scale |
| 初始化/修正 Adam $v_0$ | 状态建立机制 | target LR 仍可能越过稳定域 |
| 显式限制角更新 | relative/angle 机制 | clip bias 与表示依赖 |
| 减小 batch 或改数据顺序 | 噪声机制 | 每 step compute/时钟已变 |
| 提高 precision、固定 loss scale | 数值机制 | 轨迹几何仍会改变 |
| 直接监控 $\lambda_{\max}$ 并自适应 LR | 曲率机制 | HVP proxy 与非凸未来轨迹 |

至少要记录：

$$
(\eta_t,\lVert g_t\rVert,\lVert u_t\rVert,
\rho_\ell,\text{angle}_\ell,\Delta h_\ell,
\lambda_{\max}^{\mathrm{proxy}},
\text{clip rate},\text{overflow rate}).
\tag{9}
$$

## 九、Warmup 长度不能只写“5%”

比例 $T_w/T$ 依赖总 horizon。把训练从 10k 延长到 100k step、保持 5%，warmup 也被扩大十倍；这可能改变优化而非仅重新参数化时间。

更可审计的选择方式是：

1. 先确定 optimizer、target LR 与训练时钟；
2. 在小规模 run 中记录 early update/angle/feature/curvature；
3. 选择能把关键指标控制在预注册区间的最短 $T_w$；
4. 在多个 seed 和目标规模上验证；
5. 将 $T_w$ 的 step 与 token 两种口径同时报告。

经验比例仍可作为搜索起点，但不能作为机制结论。

## 十、图：六种 Warmup 机制不能混成一个故事

先看图回答：训练初期不稳定时，warmup 可能作用在哪些不同环节，怎样用干预区分？

![[00-知识库管理/_assets/figures/training-optimization/fig-warmup-mechanism-hypothesis-ledger-v1.svg|880]]

> [!figure] 图 TRN-34　Warmup 机制假说与可证伪观测
> 上排从局部曲率、optimizer state、相对/角更新、噪声、数值和架构六条路径解释 warmup；下排给出各自更直接的替代干预与观测。来源：依据 [[S-2024-Kalra-Barkeshli-Warmup]]、[[S-2024-Kosson-Warmup-GPT]]、[[S-2017-Goyal-Large-Batch-Warmup]] 原创整理。

**怎样读图**：先找到第一个越界对象，再选择针对性的替代干预；若不同干预都有效，说明 warmup 可能同时遮蔽多种机制。

**图没有证明什么**：图不证明六种机制穷尽所有原因，也不证明某条路径在所有 Transformer、CNN 或 optimizer 中占主导。

## 十一、科学空间研读框

[[S-2024-Su-10657-梯度裁剪模长]] 从 $\eta\lVert g\rVert$ 与一阶 loss change 的尺度追问默认 clip norm，适合提醒初学者：warmup、clipping 与 loss reduction 是耦合控制器。课程进一步加入 clip bias、optimizer-state age、角更新和低精度位置，避免把阈值或 warmup 比例自然化。

## 十二、初学者自检

1. warmup 为什么不等于“optimizer state 冻结”？
2. 若 overflow 发生在反向传播中，减小 LR 为什么可能无效？
3. bias correction 完整时，Adam 为什么仍可能需要 warmup？
4. 比较两个 warmup 比例时，为何必须同时报告总 horizon？
5. 什么实验能区分“sharpness 太大”和“角更新太大”？

## 十三、本节出口

你应能把“warmup 有效”改写成一组可证伪问题：

$$
\text{哪个对象越界}
\to
\text{LR 在哪个阶段介入}
\to
\text{什么替代干预也应有效}
\to
\text{什么观测会否证该机制}.
$$

## 练习与独立解答

- [[习题 - Warmup、早期曲率与优化器状态建立]]
- [[解答 - Warmup、早期曲率与优化器状态建立]]

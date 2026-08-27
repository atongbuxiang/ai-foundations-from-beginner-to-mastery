---
type: derivation
status: verified
area: [generative-models, diffusion, classifier-free-guidance, conditional-generation]
node_id: GEN-66
prerequisites: ["[[条件生成、Bayes 分解与 Classifier Guidance]]", "[[数据、噪声、速度与 Score 参数化]]"]
related: ["[[逆问题、约束采样与 Plug-and-Play 控制]]", "[[生成模型实验协议、FD Loss 与前沿证据地图]]"]
sources: ["[[S-2022-Su-9257-条件控制生成]]", "[[S-2022-Ho-Salimans-CFG]]", "[[S-2024-Su-10055-信噪比与大图生成下]]"]
exercises: ["[[习题 - Classifier-Free Guidance、尺度与质量多样性前沿]]"]
solutions: ["[[解答 - Classifier-Free Guidance、尺度与质量多样性前沿]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-cfg-scale-quality-coverage-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Classifier-Free Guidance、尺度与质量多样性前沿

> [!abstract] 一句话结论
> CFG 用同一个网络在“有条件/空条件”两种模式下得到 $r_c,r_u$，再做 $r_u+w(r_c-r_u)$。它把 classifier guidance 的 evidence direction 近似成两次生成模型预测之差，省去外部分类器，却没有消除 scale、双倍网络调用、分布外外推和质量—覆盖权衡。

## 一、为什么叫 classifier-free

训练时随机丢弃条件。设 dropout indicator $m\in\{0,1\}$，$m=1$ 使用真实条件 $y$，$m=0$ 使用空条件 $\varnothing$。以 noise prediction 为例：

$$
\min_\theta
\mathbb E\left[
\|\epsilon-\epsilon_\theta(x_t,t,c_m)\|^2
\right],
\quad
c_m=\begin{cases}y,&m=1\\ \varnothing,&m=0.\end{cases}
$$

同一网络近似

$$
\epsilon_c\approx\mathbb E[\epsilon\mid x_t,t,y],
\qquad
\epsilon_u\approx\mathbb E[\epsilon\mid x_t,t].
$$

“free”只表示不用额外 classifier；一次 guided prediction 通常仍需 conditional 与 unconditional 两个 forward，除非实现做 batch 拼接、缓存或近似。

## 二、从两个 score 恢复 evidence direction

若两支 score 都精确，GEN-65 的 Bayes identity 给出

$$
s_c-s_u
=\nabla_x\log p_t(x\mid y)-\nabla_x\log p_t(x)
=\nabla_x\log p_t(y\mid x).
$$

所以

$$
s_{cfg}=s_u+w(s_c-s_u)
$$

等价于 classifier guidance 的 score 形式。关键区别是 evidence direction 由生成网络的两种条件模式之差估计，而非独立分类器的输入梯度。

## 三、本卷唯一 scale convention

$$
\boxed{r_{cfg}=r_u+w(r_c-r_u).}
$$

代入测试：

| $w$ | 输出 | 几何含义 |
|---:|---|---|
| 0 | $r_u$ | 无条件起点 |
| 1 | $r_c$ | 普通条件点 |
| $>1$ | 越过 $r_c$ | 条件方向外推 |
| $<0$ | 远离 $r_c$ | 不自动等于某个可解释负条件 |

另一常见写法是 $r_c+s(r_c-r_u)$，此时 $s=w-1$。若某接口声称 `guidance_scale=1` 表示无 guidance，通常使用本卷 $w=1$ 的 convention；若 `0` 表示无 guidance，则需检查它究竟返回 conditional 还是 unconditional。

## 四、score、noise、velocity 能否直接混合

在 Gaussian corruption

$$x_t=\alpha_t x_0+\sigma_t\epsilon$$

下，条件 score 与最优 noise prediction 满足

$$s_t(x_t\mid y)=-\frac{1}{\sigma_t}\epsilon^*(x_t,t,y).$$

因为同一 $t$ 的换算是线性的，

$$
\epsilon_{cfg}=\epsilon_u+w(\epsilon_c-\epsilon_u)
$$

与在 score 空间做同一线性组合相容。$x_0$ 与 $v$ 参数化在固定 $t$、相同 preconditioning 且没有非线性 clipping 时也可线性换算。

但以下操作会破坏简单等价：

- 对 $\hat x_0$ 做 dynamic thresholding/clipping；
- conditional/unconditional 分支使用不同 normalization 或 adapter；
- 混合前后采用不同 precision；
- scheduler API 把 model output 解释成不同 prediction type；
- 空条件不是对训练数据条件分布的真正 marginalization。

## 五、分布解释与它的边界

理想 score 下，

$$
s_{cfg}
=w\nabla\log p_t(x\mid y)+(1-w)\nabla\log p_t(x),
$$

对应

$$
\tilde p_t^{(w)}(x\mid y)
\propto p_t(x\mid y)^w p_t(x)^{1-w}
\propto p_t(x)p_t(y\mid x)^w.
$$

这解释 $w>1$ 为什么会 sharpen 条件。但要保留三层边界：

1. 两支网络都只是近似 score，差分会放大误差；
2. 对每个 $t$ 定义的 tilted density 未必构成某个共同 forward diffusion 的一致 marginal family；
3. finite solver、thresholding 与 negative prompt 会进一步改变实际分布。

因此“CFG 精确采自 $p(x\mid y)^w/p(x)^{w-1}$”只能作为理想化 instantaneous-score 解释。

## 六、为什么 scale 会导致过饱和与多样性下降

差向量

$$d=r_c-r_u$$

包含条件信号，也包含两支预测误差。外推后误差变为

$$e_{cfg}=e_u+w(e_c-e_u),$$

其范数可随 $w$ 线性增长。若 $d$ 在训练时只出现在 $w\in[0,1]$ 的插值区，$w\gg1$ 是部署时分布外外推。

常见现象包括：

- 条件分类/文本相似度上升；
- 色彩、对比度或纹理过强；
- intra-class diversity 与 rare-mode recall 下降；
- 小物体、计数或空间关系并不随 scale 单调改善；
- 数值 ODE 更弯或更 stiff，需要更密时间网格。

所以 scale sweep 必须同时画 conditional score、FID/KID、precision/recall 和人评，而不是只找单一最小 FID。

## 七、负提示与基线替换

设正条件 $y_+$、负条件 $y_-$，常见 generalized guidance 是

$$
r=r_-+w(r_+-r_-).
$$

这里 $r_-$ 可以是空条件，也可以是负提示预测。它的几何含义是从负条件点朝正条件点外推，不是逻辑上的集合差 $p(x\mid y_+,\neg y_-)$。文本编码器的语义、训练分布和 scale 决定效果。

## 八、引导不只来自文本分类

[[S-2024-Su-10055-信噪比与大图生成下]] 的 Upsample Guidance 展示另一种设计：把低分辨率模型经下采样—SNR 对齐—上采样得到的主项，与直接高分辨率调用保留的纹理项组合。它提醒我们：

- guidance 是“基础预测 + 纠正方向”的算法模板；
- 纠正方向可以来自 classifier、condition difference、measurement likelihood 或跨尺度 consistency；
- 每个方向都要说明对象、单位、noise-level 对齐与代价。

## 九、最小 scale sweep 协议

固定同一批 initial noises 和 prompts，取

$$w\in\{0,0.5,1,2,4,8\}.$$

报告：

1. 每个 $w$ 的 deterministic/stochastic seed 配对结果；
2. 条件一致性指标与盲化人评；
3. FID/KID 与 precision/recall；
4. 每类/每属性 coverage，而非只报总体；
5. saturation、clipping rate 与 prediction norm；
6. NFE、两支 forward 的 batching、latency 与 peak memory；
7. 选择 $w$ 使用 validation split，最终 test 只评一次。

## 十、图：CFG 是插值还是外推

先回答：训练让网络看到的是哪两种条件模式？$w=1$ 在图上为什么恰好落在 conditional prediction？何时外推误差会盖过条件信号？

![[00-知识库管理/_assets/figures/generative-models/fig-cfg-scale-quality-coverage-v1.svg|900]]

> [!figure] 图 50.9-02　CFG 尺度轴与质量—覆盖 Pareto 面
> 图把 prediction-space 几何、scale sweep 和 evaluation panel 放在一张账本中。来源：据 CFG 原论文、科学空间 9257/10055 与本节推导独立绘制。

**怎样读图**：先从 $r_u$ 到 $r_c$ 找 $w=0,1$，再看 $w>1$ 的外推段；右侧不是单调曲线，而是条件性、fidelity、coverage 和 saturation 的多目标记录。

**图没有证明什么**：图不证明最优 $w$ 固定，不证明负提示是逻辑否定，也不证明 noise/score/$x_0/v$ 在含 clipping 的代码里仍完全等价。

## 十一、学习出口

- 能从 $s_c-s_u$ 推出 evidence score；
- 能识别两个 scale convention 并换算；
- 能说明参数化线性换算成立的条件；
- 能设计配对 seed 的 quality–coverage sweep；
- [[习题 - Classifier-Free Guidance、尺度与质量多样性前沿]]
- [[解答 - Classifier-Free Guidance、尺度与质量多样性前沿]]

---
type: model
status: verified
area: [generative-models, diffusion, implementation]
node_id: GEN-48
prerequisites: ["[[扩散简化损失、时间加权、Schedule 与 SNR]]", "[[反向均值、固定方差、学习方差与 Analytic-DPM]]", "[[DDIM、非 Markov 前向族与确定性采样]]"]
related: ["[[生成模型完整课程地图与掌握标准]]", "[[时间反演、score 与扩散生成动力学]]"]
sources: ["[[S-2022-Su-9119-DDPM拆楼建楼]]", "[[S-2020-Ho-DDPM]]", "[[S-2021-Nichol-Dhariwal-Improved-DDPM]]"]
exercises: ["[[习题 - 最小 DDPM 的张量合同、复现门与证据地图]]"]
solutions: ["[[解答 - 最小 DDPM 的张量合同、复现门与证据地图]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-ddpm-implementation-contract-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 最小 DDPM 的张量合同、复现门与证据地图

> [!abstract] 一句话结论
> 一个最小 DDPM 不是“U-Net + MSE”六个字，而是一套端到端可复查合同：数据尺度、schedule 索引、闭式加噪、时间条件、输出参数化、loss reduction、reverse mean/variance、最后一步噪声、clipping/EMA 和 evaluator 必须彼此一致。

## 一、训练程序的最小伪代码

```text
x0 = preprocess(batch)                  # [B,C,H,W]
t  ~ timestep_proposal                  # [B], convention 1...T
eps ~ N(0,I), same shape as x0
a  = gather(sqrt_alpha_bar, t)          # [B,1,1,1]
sig= gather(sqrt_one_minus_alpha_bar,t) # [B,1,1,1]
xt = a*x0 + sig*eps
pred = model(xt, t, condition=None)      # same shape as x0
loss = weight(t) * elementwise_error(pred,target)
loss = reduce_features_then_batch(loss)
```

若 prediction 是 $v$ 或 $x_0$，target 与换算必须同步；不能只改 output 名称。

## 二、reverse sampling 的最小合同

从 $x_T\sim N(0,I)$，对 $t=T,\ldots,1$：

1. network 预测 $\hat\epsilon/\hat x_0/\hat v$；
2. 统一换算为 $\hat x_0,\hat\epsilon$；
3. 可选且明确地 clip/dynamic-threshold $\hat x_0$；
4. 计算 $\mu_\theta(x_t,t)$ 与 $\sigma^2_{rev,t}$；
5. $t>1$ 时 sample $z\sim N(0,I)$，$x_{t-1}=\mu+\sigma z$；
6. $t=1$ 时按 decoder/实现合同不再加噪。

最后一步仍加随机噪声会直接污染输出；用布尔 mask 时要 reshape 为 broadcast shape。

## 三、索引是第一大失败源

建议数组显式含 dummy $\bar\alpha_0=1$，使数学 $t$ 与 index 对齐。否则常见错误：

- 训练抽 `0...T-1` 却按数学 `1...T` gather；
- posterior 用 $\bar\alpha_t$ 替代 $\bar\alpha_{t-1}$；
- sample loop 漏 $T$ 或多执行 $t=0$；
- timestep embedding 的 label 与 schedule index 平移；
- DDIM subsequence 未包含端点或重复时刻。

## 四、数据与 likelihood 口径

8-bit 图像常映到 $[-1,1]$ 或其他连续尺度。训练 corruption 针对这个连续表示；若报告 bits/dim，需要离散 decoder/dequantization 口径，不能把 simple MSE 当 likelihood。随机 horizontal flip、crop、颜色空间也改变训练 data law。

## 五、网络最小合同

- 输入/output `[B,C,H,W]`；time embedding `[B,D_t]` 经各 block 调制；
- normalization 不依赖 inference batch composition（常用 GroupNorm 等）；
- U-Net/DiT 是 denoiser architecture，不承担 forward probability proof；
- conditioner dropout、class/text embeddings 属于 50.9 条件模型扩展；
- EMA 参数若用于 sampling，评价必须记录 decay、warmup 与 checkpoint。

## 六、数值稳定检查

- schedule 用高精度预计算，`log1p(-beta)`；
- posterior log-variance 在 $t=1$ 的零边界单独处理；
- mixed precision 下监测 high-SNR small residual 与 low-SNR large prediction；
- loss reduction、gradient scaling/clipping、optimizer state 一起记录；
- sampling 每步检查 finite、范围、mean/std 与 predicted norm；
- fixed seed 只能复现同一随机程序，不证明分布正确。

## 七、最小分层测试

1. **代数门**：schedule、closed marginal、posterior、parameterization round-trip；
2. **统计门**：Monte Carlo mean/variance、last-step noise mask；
3. **过拟合门**：极小数据/单样本 loss 能否下降且 reverse 可见结构；
4. **分布门**：toy Gaussian/mixture 的 mean、variance、coverage；
5. **成本门**：train step time、sampling NFE、wall time、memory；
6. **证据门**：博客直觉、原论文 identity、代码事实、实验 observation 分层。

## 八、科学空间实现经验怎样使用

[[S-2022-Su-9119-DDPM拆楼建楼]]及后续文章给出可运行 Keras 入口和若干经验。课程采用它们生成调试问题，不直接接受“sum loss 必须优于 MSE”“某 normalization/optimizer 普遍最好”。常数 loss scaling 与 learning rate 在理想 SGD 下可互换，但 mixed precision、Adam、clipping 和 regularization 会使实际轨迹不同，需复现。

## 九、图：一条 DDPM 程序的六个接口

先看图回答：哪一个模块的形状/索引错一位，会让公式看似正确却训练与采样使用不同噪声层？

![[00-知识库管理/_assets/figures/generative-models/fig-ddpm-implementation-contract-v1.svg|900]]

> [!figure] 图 50.6-08　数据→schedule→forward sample→network target→reverse kernel→evaluation 合同
> 每个接口标出对象、形状和必须记录的实现选择。来源：依据 DDPM 公式与常见复现失效独立绘制。

**怎样读图**：沿训练链检查 target，沿采样链反向检查 mean/variance；二者在同一 schedule index、parameterization 和 preprocessing 处汇合。任一隐含默认都可能改变模型。

**图没有证明什么**：图不保证 U-Net 容量充分，不给 benchmark 性能，也不证明通过单元测试就学到真实数据分布。

## 十、本节回顾与训练

- 最小 DDPM 是概率合同 + 张量程序 + 数值/证据审计；
- 先验、加噪、target、reverse mean/variance 必须共享同一符号表；
- off-by-one、最后一步噪声、loss reduction 和 clipping 都会改变程序；
- 静态公式通过后仍需 toy distribution 与 compute tests；
- [[习题 - 最小 DDPM 的张量合同、复现门与证据地图]]
- [[解答 - 最小 DDPM 的张量合同、复现门与证据地图]]


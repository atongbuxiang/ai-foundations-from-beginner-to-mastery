---
type: concept
status: verified
area: [language-models, denoising, mixture-objectives, ul2]
node_id: LM-14
aliases: [Mixture-of-Denoisers, UL2, 多目标预训练]
prerequisites: ["[[Span Corruption、Sentinel Token 与 T5 Seq2Seq 目标]]", "[[Prefix LM、UniLM 与序列到序列 Mask 合同]]"]
related: ["[[GPT、BERT、T5 的目标—模型族—能力证据地图]]", "[[过训练、推理成本与多目标最优规模]]"]
sources: ["[[S-2023-Tay-UL2]]"]
exercises: ["[[习题 - Mixture-of-Denoisers、UL2 与多目标采样]]"]
solutions: ["[[解答 - Mixture-of-Denoisers、UL2 与多目标采样]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-mixture-denoisers-ledger-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Mixture-of-Denoisers、UL2 与多目标采样

> [!abstract] 一句话结论
> 多目标语言模型先抽取 objective mode，再从该 mode 的 corruption law 生成 source–target，最后计算对应 loss。配置中的 mode 概率只是样本频率；由于 target 数、reduction、序列长度和梯度几何不同，它通常不等于 token、FLOPs 或参数更新的实际贡献。

## 一、层级生成过程

设模式集合为 $\mathcal M$，先抽

$$
M\sim\operatorname{Categorical}(\pi_1,\ldots,\pi_K),
\qquad \sum_m\pi_m=1.
$$

给定 clean example $X$ 与 mode $m$，再抽 corruption/partition 变量

$$
C\sim q_m(c\mid X),
$$

构造模型输入 $I_m(X,C)$、target $Y_m(X,C)$ 和 loss $\mathcal L_m$。总体目标是

$$
\mathcal R(\theta)
=\sum_{m\in\mathcal M}\pi_m
\mathbb E_{X,C\sim q_m}
[\mathcal L_m(\theta;X,C)].
$$

若每步独立按 $\pi$ 抽 mode，单样本梯度是总体梯度的无偏估计，前提是各 $\mathcal L_m$ 的数值定义已经固定。改变 mode 内的 denominator 就是在改变总体风险，即使 $\pi$ 不变。

## 二、UL2 的 R、S、X 应怎样理解

UL2 用 Mixture-of-Denoisers 覆盖不同的信息结构。教学上可把模式理解为：

- **R-denoiser（regular）**：类似常规短 span corruption，恢复局部缺失；
- **S-denoiser（sequential）**：更接近顺序/因果式预测，使目标包含长后缀生成结构；
- **X-denoiser（extreme）**：更高 corruption 或更长 span，要求从较少上下文恢复较大缺口。

这些名称是论文中的设计族，不应用一句固定百分比取代版本化配置。真正复现时应从目标 checkpoint 的配置读取每个 denoiser 的 noise density、span-length distribution、prefix split 与 mode tag，而非凭类别名猜测。

## 三、为什么 $\pi_m$ 不是“训练贡献”

设 R 与 X 各以 $0.5$ 概率抽样。R 样本平均 20 个 target token，X 样本平均 100 个 target token。

### 情形 A：每样本 target-token mean

每个样本先对自身 target 平均，R 与 X 的期望样本权重仍约为 $1:1$；但 X 每个 target token 的单独权重更小。

### 情形 B：跨 batch token mean

先汇总所有 token NLL 再除总 target 数，若样本数相同，X 约贡献 $100/(20+100)=5/6$ 的 token 分子与分母。

### 情形 C：固定 token/FLOP budget

X 的 source/target 更长，单样本计算可能更贵，于是单位 FLOP 下抽到的样本数更少。真实训练贡献又改变。

所以至少存在四种权重：sample share、target-token share、compute share、gradient share。它们不能共用一个 `mixture_weight` 字段。

## 四、梯度贡献需要什么账本

令 mode $m$ 的单步梯度为 $g_m$。总体均值梯度是

$$
g=\sum_m\pi_m\,\mathbb E[g_m],
$$

噪声协方差还含 mode 内方差和 mode 间均值差异：

$$
\operatorname{Cov}(g_M)
=\mathbb E_M[\operatorname{Cov}(g_M\mid M)]
+\operatorname{Cov}_M(\mathbb E[g_M\mid M]).
$$

即使均值梯度尺度相同，方向冲突也可能导致一种任务的改进损害另一种。建议按 mode 记录：

- 样本数、clean/source/target token 数；
- loss numerator 与 denominator；
- encoder/decoder FLOPs 或可解释代理；
- 全局梯度范数、裁剪前后范数；
- mode 梯度与总梯度/其他 mode 的余弦相似度；
- 各 mode 独立 validation metrics。

只有这些量才能回答“模式是否真正被训练到”。

## 五、混合 sampler 的无偏性与方差

若目标明确为 $\sum_m w_m R_m$，可以按 proposal $r_m$ 抽 mode，并用重要性权重 $w_m/r_m$：

$$
\widehat g=\frac{w_M}{r_M}\nabla\mathcal L_M,
\qquad M\sim r.
$$

它在支持集覆盖且期望存在时无偏，但 $r_m$ 太小时权重爆炸、方差很高。实际系统常选择有偏但较稳定的 clip、temperature sampling 或动态权重；若如此，应承认优化目标改变，而不是仍声称精确优化原加权和。

## 六、mode tag 与推理接口

多目标模型可能在输入前加入 mode token，显式告知模型当前采用哪种 denoising regime。这让一个参数化分布条件于任务变量：

$$
p_\theta(y\mid x,m).
$$

若训练有 mode tag 而部署不提供，必须说明默认 tag、prompt 映射或无 tag 训练比例。tag 不是纯装饰：它可能选择不同的生成行为、长度偏好与可见性合同。

## 七、与多任务学习的关系

Mixture-of-Denoisers 可视为共享参数的多任务学习，但“任务”由自监督 corruption 生成。它可能扩大能力覆盖，也引入：

- capacity competition：有限参数同时拟合多个条件族；
- optimization interference：梯度方向冲突；
- calibration mismatch：各 mode 输出长度和熵不同；
- evaluation selection：只报告总体均值掩盖某 mode 退化；
- systems imbalance：长 target mode 决定显存和吞吐瓶颈。

多目标的价值必须由对齐预算的消融验证；“目标更丰富”不是无需证据的单调收益定理。

## 八、图：名义 mixture 到真实贡献

先看图回答：为什么 `R:S:X = 1:1:1` 不能推出三个 mode 的梯度贡献相等？

![[00-知识库管理/_assets/figures/language-models/fig-lm-mixture-denoisers-ledger-v1.svg|900]]

> [!figure] 图 LM-14　层级 sampler 与四份贡献账本
> 左侧是 mode→corruption→source/target 的生成图；中部区分 R/S/X 的信息结构；右侧把 sample、token、compute 和 gradient share 分开。来源：本课程依据 UL2 的 Mixture-of-Denoisers 框架独立绘制。

**怎样读图**：沿一次样本路径记录 mode 概率，再数 target token、估算计算量，最后才观察梯度；不要从第一列直接跳到最后一列。

**图没有证明什么**：图不证明 R/S/X 的某个比例最优，不表示贡献越平均越好，也不替代对具体 UL2 配置与训练代码的核验。

## 九、可复现配置模板

```yaml
mode_sampler:
  probabilities: {R: ..., S: ..., X: ...}
  granularity: example | batch | step
  seed: ...
denoisers:
  R: {noise_density: ..., span_law: ..., target_reduction: ...}
  S: {prefix_law: ..., target_reduction: ...}
  X: {noise_density: ..., span_law: ..., target_reduction: ...}
mode_tokens: {...}
packing: ...
budget_unit: raw_tokens | model_tokens | FLOPs | steps
logging: [sample_count, source_tokens, target_tokens, numerator, denominator, grad_norm]
```

## 十、本节出口

你应能把多目标训练写成层级概率模型，计算 nominal sample share 与 token share 的差异，并设计 mode-level gradient/compute 审计。下一节[[NLL、Perplexity、Bits-per-Byte 与 Tokenizer 公平比较]]专门解决不同分母和 tokenizer 下的评测可比性。

## 练习与独立解答

- [[习题 - Mixture-of-Denoisers、UL2 与多目标采样]]
- [[解答 - Mixture-of-Denoisers、UL2 与多目标采样]]

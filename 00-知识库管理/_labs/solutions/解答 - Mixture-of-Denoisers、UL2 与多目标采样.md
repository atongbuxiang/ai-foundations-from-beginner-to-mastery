---
type: solution
status: verified
area: [language-models, mixture-objectives, ul2]
topic: "[[Mixture-of-Denoisers、UL2 与多目标采样]]"
exercise: "[[习题 - Mixture-of-Denoisers、UL2 与多目标采样]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Mixture-of-Denoisers、UL2 与多目标采样

## A. 识别与复述

### LM14-A01
$M\sim Cat(\pi)$；给 clean $X$ 后抽 $C\sim q_M(C\mid X)$；由 $(X,C,M)$ 构造 input、target、relation 与 loss；总体风险为 $\sum_m\pi_mE_{X,C}[L_m]$。每层随机性和 reduction 都要版本化。

### LM14-A02
Sample share 是 mode 被抽中的样本比例；target-token share 是各 mode 有效标签数比例；compute share 是 FLOPs/时间/内存占用；gradient share 还由 loss scale、梯度范数与方向决定。前者相等不蕴含后三者相等。

### LM14-A03
R 是常规、偏短 span 的 denoising family；S 强调 sequential/causal-like 的连续预测；X 使用更极端的 corruption、常含更长缺失或更少可见信息。具体噪声率与 span law 属于 checkpoint 配置，不能由字母固定推断。

## B. 手算与构造

### LM14-B01
样本数 R=X=50，sample share 各 50%。Target tokens：R 为 $50\times20=1000$，X 为 $50\times80=4000$；shares 为 20% 与 80%。

### LM14-B02
$R=0.7(1.0)+0.3(2.0)=1.3$。交换后 $R=0.3(1.0)+0.7(2.0)=1.7$。这里只在每 mode risk 的单位/reduction 相同定义下有意义。

### LM14-B03
抽到 R 的权重 $w_R/r_R=0.5/0.8=0.625$；抽到 X 的权重 $0.5/0.2=2.5$。X 稀少样本被放大，通常带来更高方差。

## C. 推导与证明

### LM14-C01
若 $M\sim\pi$ 且 $g_M=\nabla L_M$，则
$$E[g_M]=\sum_mP(M=m)E[g_m\mid m]=\sum_m\pi_m\nabla R_m
=\nabla\sum_m\pi_mR_m,$$
在可交换微分与期望的正则条件下无偏。

### LM14-C02
令 $\mu_m=E[g\mid M=m]$。加减 $\mu_M$ 并展开可得 total covariance law：
$$Cov(g)=E_M[Cov(g\mid M)]+Cov_M(\mu_M).$$
第一项是 mode 内数据/corruption 噪声，第二项是不同 mode 平均梯度的离散差异。

### LM14-C03
Per-example risk 是 $E_b[(\sum_{i=1}^{D_b}\ell_{bi})/D_b]$，每样本权重相同；global-token risk 是 $E[\sum_b\sum_i\ell_{bi}]/E[\sum_bD_b]$ 的样本近似，样本权重正比 $D_b$。只在 $D_b$ 常数或其与平均 loss 特殊无关时相同。

## D. 边界、反例与纠错

### LM14-D01
三 mode 各 1/3 样本；target 长度分别 1、10、100，且梯度范数分别 0.1、1、10。即使 per-token reduction一致，长/大梯度 mode 可支配更新；若全 token mean，更进一步由 100-token mode 主导。

### LM14-D02
有限容量会产生任务竞争，梯度可能冲突，长 mode 消耗预算，sampler 还可能稀释关键任务。增加一个高权重噪声目标可使所有原任务变差。因此需对齐预算的新增/移除消融及 per-mode 指标。

### LM14-D03
训练学的是 $p(y\mid x,m)$；省略 $m$ 后输入落在训练支持外，或被错误解释为普通文本。输出长度/denoising行为可能漂移。应训练无 tag 分支、定义默认 tag，或部署始终注入同样控制 token。

## E. AI 迁移

### LM14-E01
每 mode 每 step/窗口记录：sample count、clean/source/target tokens、noise/span 统计、loss numerator/denominator、mean loss、FLOPs/step time/peak memory、pre/post-clip grad norm、与总梯度余弦、validation metrics、sampler seed/config hash。

### LM14-E02
在同一 checkpoint 和 microbatches 上分别 backward 得 $g_R,g_X$，不更新参数，计算内积与余弦并跨 batch 给分布；负余弦提示局部一阶冲突。局限：尺度被消去、只看当前点/当前 batch、参数重参数化影响几何、Adam/preconditioning 后实际更新方向可不同。

### LM14-E03
相同步数可能让长 target mode 看更多 targets、花更多 FLOPs，也可能因 batch 缩小看更少 examples。要求报告每 mode sample/target tokens、总 FLOPs、wall time与 gradient share；按至少一种合理资源预算重跑，结论只能限定在所选预算单位。

## 无提示重做

- [ ] 从名义 mixture 算 sample 与 token share。
- [ ] 解释为什么梯度 share 不能只靠 target count 推断。


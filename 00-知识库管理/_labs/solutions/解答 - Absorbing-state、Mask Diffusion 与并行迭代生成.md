---
type: solution
status: draft
topic: "[[Absorbing-state、Mask Diffusion 与并行迭代生成]]"
exercise: "[[习题 - Absorbing-state、Mask Diffusion 与并行迭代生成]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Absorbing-state、Mask Diffusion 与并行迭代生成
## A. 识别与复述
### GEN58-A01
真实 token $i$ 以 $\alpha_t$ 留在 $i$、以 $1-\alpha_t$ 跳到 mask $m$；$m$ 以概率 1 留在 $m$。吸收仅指 forward 的 $m\to m$，反向生成正要从 $m$ 恢复真实 token。
### GEN58-A02
令 $\bar\alpha_t=\prod_{s\le t}\alpha_s$，则 $q(x_t=x_0\mid x_0)=\bar\alpha_t$，$q(x_t=m\mid x_0)=1-\bar\alpha_t$。
### GEN58-A03
严格反向链的 reveal probability 由 forward posterior 解析决定，且通常揭示后保持；MaskGIT 用置信度选择和 schedule，已填 token 可被重遮掩。后者的实际 transition 不是自动等于前者。
## B. 手算与建模
### GEN58-B01
$\bar\alpha_3=.9\times.8\times.5=.36$；mask probability 为 $.64$。
### GEN58-B02
$\bar\alpha_2=.72$。上一时刻 clean 的概率 $.72(1-.5)/(1-.36)=.36/.64=.5625$；已 mask 为 $(1-.72)/.64=.4375$。
### GEN58-B03
$16\times.375=6$，恰为整数；用 ceiling 仍为 6。若结果非整数，必须版本化 round/floor/ceil，因为它改变每轮 token 数。
## C. 推导与证明
### GEN58-C01
到时刻 $t$ 仍 clean 当且仅当每一步都保留。条件独立的 Markov step probabilities 连乘给 $\bar\alpha_t$；补事件就是至少一次 mask，概率 $1-\bar\alpha_t$。
### GEN58-C02
给定末端 mask，上一时刻 clean 且最后一步 mask 的权重 $\bar\alpha_{t-1}(1-\alpha_t)$；上一时刻已 mask 的权重 $1-\bar\alpha_{t-1}$。和为 $1-\bar\alpha_t$，除后两项和为 1。
### GEN58-C03
factorization 是 $q(x_t\mid x_0)=\prod_rq(x_t^r\mid x_0^r)$；它只说 corruption noises 给定 clean sequence 后独立。$p_{data}(x_0)$ 可有任意跨位置依赖，去噪网络也用全局上下文恢复这些依赖。
## D. 边界、反例与纠错
### GEN58-D01
BERT 缺少必须明确的 terminal generative distribution、reverse chain、采样到完整样本的程序和 likelihood/ELBO 对象。随机 mask CE 与 diffusion 可共享子目标，但不能仅凭词面等同。
### GEN58-D02
令两个 token 必须相同，exact conditional 在 $(A,A),(B,B)$ 各有 $.5$。两个 marginal 都是 $(.5,.5)$，独立采会额外产生 $(A,B),(B,A)$ 各 $.25$，违背 joint constraint。
### GEN58-D03
MaskGIT 常将每轮低置信 token 重遮掩，其中可能包括上一轮已填位置；这正用于修正早期选择。是否只重遮当前 mask 或全部位置必须由具体实现说明。
## E. AI 迁移
### GEN58-E01
记录 tokenizer/version、初始 mask ratio、轮数、每轮 mask-count schedule、rounding、temperature、top-k/top-p、confidence definition、Gumbel/noise、re-mask candidate set、condition guidance、seed、batching 与 NFE。
### GEN58-E02
$t=1$ 时 clean posterior 权重应为 1；$1-\alpha_t=0$ 时不会新 mask；$\alpha_t=0$ 时本步所有 clean 都 mask。对支持事件检查两项非负和为 1，并用枚举/模拟核对。
### GEN58-E03
固定模型和 tokenizer，sweep 轮数并记录总 NFE、每轮全-grid token logits、实际 token resamples、wall-clock、质量和 seed spread。并行度用关键路径/设备利用率报告，不能把“每轮填多个 token”直接当成同倍 wall-clock 加速。

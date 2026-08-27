---
type: exercise
status: draft
area: [generative-models, masked-modeling]
topic: "[[Absorbing-state、Mask Diffusion 与并行迭代生成]]"
solution: "[[解答 - Absorbing-state、Mask Diffusion 与并行迭代生成]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Absorbing-state、Mask Diffusion 与并行迭代生成
## A. 识别与复述
### GEN58-A01
定义 absorbing mask kernel，并解释“吸收”只描述 forward process。
### GEN58-A02
写出 $q(x_t=x_0\mid x_0)$ 与 $q(x_t=m\mid x_0)$。
### GEN58-A03
列出严格 reverse absorbing chain 与 MaskGIT confidence re-mask 的两点差异。
## B. 手算与建模
### GEN58-B01
$\alpha=(.9,.8,.5)$。求 $\bar\alpha_3$ 与时刻 3 的 mask probability。
### GEN58-B02
接上题，给定 $x_3=m$，求 $x_2$ 仍 clean 与已 mask 的 posterior probabilities。
### GEN58-B03
长度 16 的 grid，某轮 schedule 要保留 mask ratio .375。下一轮 mask 数是多少？若用 ceiling 呢？
## C. 推导与证明
### GEN58-C01
证明 absorbing marginal 的 survival closed form。
### GEN58-C02
推导已观测 mask 时的两项 posterior，并验证两项和为 1。
### GEN58-C03
说明位置条件独立的 forward mask 为什么不意味着数据 token 独立。
## D. 边界、反例与纠错
### GEN58-D01
为什么“BERT 做 mask，所以 BERT 就是完整 diffusion generator”不充分？
### GEN58-D02
构造两个高度相关待填 token，说明同轮独立采样不等于 exact joint conditional。
### GEN58-D03
纠正“MaskGIT 一旦填 token 就永不改变”的说法。
## E. AI 迁移
### GEN58-E01
写出可复现的 MaskGIT sampler 配置字段。
### GEN58-E02
设计 absorbing posterior 的单元测试，覆盖 $t=1$、极小/极大 mask rate。
### GEN58-E03
设计轮数—质量—并行度实验，避免把 network evaluations 与 token updates 混为一谈。
## 解答入口
[[解答 - Absorbing-state、Mask Diffusion 与并行迭代生成]]

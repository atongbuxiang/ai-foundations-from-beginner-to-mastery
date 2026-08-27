---
type: exercise
status: draft
area: [generative-models, diffusion, implementation]
topic: "[[最小 DDPM 的张量合同、复现门与证据地图]]"
solution: "[[解答 - 最小 DDPM 的张量合同、复现门与证据地图]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - 最小 DDPM 的张量合同、复现门与证据地图
## A. 识别与复述
### GEN48-A01
列出最小 DDPM 从数据到评价的六类接口合同。
### GEN48-A02
训练时 $a_t,\sigma_t$ 从 `[T+1]` 表 gather 到 `[B,C,H,W]` 输入时，应得到什么 shape？为什么？
### GEN48-A03
为什么 $t=1$ 通常不再加入 reverse noise？它与 decoder likelihood 的边界处理是什么关系？
## B. 手算与建模
### GEN48-B01
表含 dummy $\bar\alpha_0=1$，$\bar\alpha=(1,0.9,0.72)$。求 $t=2$ 的 $\alpha_2,\beta_2$；指出若误取 index 1 会用到什么累计量。
### GEN48-B02
批量 $t=(1,3)$，`sqrt_alpha_bar=(1,0.95,0.8,0.6)`。写出 gather 后 broadcast tensor 的 shape 与两个值。
### GEN48-B03
标量 reverse means 为 $(2,3)$、sigmas 为 $(0.1,0.2)$、对应 timesteps $(1,2)$、noise $z=(5,5)$。应用最后一步 mask 后求两个输出。
## C. 推导与证明
### GEN48-C01
从一张 $\beta_{1:T}$ 表构造 $\alpha_t,\bar\alpha_t,\sqrt{\bar\alpha_t},\sqrt{1-\bar\alpha_t}$，并列出应满足的代数不变量。
### GEN48-C02
设计并证明 $x_0/\epsilon/v$ 三种参数化 round-trip 单元测试的判据。
### GEN48-C03
证明 mask `1[t>1]` 使 $t=1$ 输出条件于网络预测不再依赖新采样的 $z$；说明这不表示最终样本没有随机性。
## D. 边界、反例与纠错
### GEN48-D01
反驳“固定 seed 后结果一致就证明实现正确”。
### GEN48-D02
反驳“simple noise MSE 的数值就是图像负对数似然”。
### GEN48-D03
反驳“用了标准 U-Net 就不需要检查 schedule、target 与 reverse variance”。
## E. AI 迁移
### GEN48-E01
写出最小 DDPM CI 测试矩阵：代数、统计、过拟合、分布、成本、证据六道门各至少一个测试。
### GEN48-E02
设计一份可复现实验 manifest，覆盖训练、采样与评价的关键隐含默认。
### GEN48-E03
比较 DDPM 1000 步与 DDIM 50 步时，怎样避免把 architecture、checkpoint、preprocessing 或 evaluator 差异误当 sampler 差异？
## 解答入口
[[解答 - 最小 DDPM 的张量合同、复现门与证据地图]]

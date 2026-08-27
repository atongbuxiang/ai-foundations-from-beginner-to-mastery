---
type: exercise
status: draft
area: [generative-models, multimodal, image-tokens]
topic: "[[图像 Token、掩码生成与多模态条件分布]]"
solution: "[[解答 - 图像 Token、掩码生成与多模态条件分布]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - 图像 Token、掩码生成与多模态条件分布
## A. 识别与复述
### GEN63-A01
为什么 tokenizer output 尚未定义 image prior？
### GEN63-A02
写出 text-conditioned raster AR 与 random-mask objective。
### GEN63-A03
列出 unified multimodal Transformer 的八项合同中的至少六项。
## B. 手算与建模
### GEN63-B01
$512^2$ 图像用 $f=16$ tokenizer，token 数是多少？raster AR 与 16-round masked sampler 的顺序 NFE 各约多少？
### GEN63-B02
对 $2\times2$ grid 写出 raster 与 column chain-rule factorization。
### GEN63-B03
文本 256 tokens、图像 1024 tokens，全量 self-attention 的 score 元素数是多少？若只算图像对文本 cross-attention 呢？
## C. 推导与证明
### GEN63-C01
证明任意 bijective ordering 都给合法 chain-rule factorization。
### GEN63-C02
说明同轮 masked factorization 为什么一般不是 exact joint conditional。
### GEN63-C03
写出 $p(y,k)=p(y)p(k\mid y)=p(k)p(y\mid k)$ 的条件，并解释有限模型不等价。
## D. 边界、反例与纠错
### GEN63-D01
反驳“共享 vocabulary 就完成了模态对齐”。
### GEN63-D02
为什么不同 tokenizer 的 token perplexity 不能直接横比？
### GEN63-D03
“生成训练一定提升理解”属于哪类主张？怎样验证？
## E. AI 迁移
### GEN63-E01
设计 text-to-image、caption、editing 三任务的 attention mask 表。
### GEN63-E02
设计 ordering ablation，控制 tokenizer、模型、compute 与 evaluation。
### GEN63-E03
给出 tokenizer drift 导致 cached token/prior checkpoint 失效的版本化方案。
## 解答入口
[[解答 - 图像 Token、掩码生成与多模态条件分布]]

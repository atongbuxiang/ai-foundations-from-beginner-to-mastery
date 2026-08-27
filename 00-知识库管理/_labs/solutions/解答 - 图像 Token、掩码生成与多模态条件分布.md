---
type: solution
status: draft
topic: "[[图像 Token、掩码生成与多模态条件分布]]"
exercise: "[[习题 - 图像 Token、掩码生成与多模态条件分布]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - 图像 Token、掩码生成与多模态条件分布
## A. 识别与复述
### GEN63-A01
tokenizer 只定义 $x\mapsto k$ 和 $k\mapsto\hat x$。要生成还需 $p(k)$ 或 $p(k\mid y)$ 的 joint factorization/sampler；同一 token grid 可由 AR、masked 或 diffusion prior 建模。
### GEN63-A02
AR：$p(k_{1:n}\mid y)=\prod_rp(k_r\mid k_{<r},y)$。Mask：$L=-E_M\sum_{r\in M}\log p(k_r\mid k_{\bar M},M,y)$。
### GEN63-A03
可列 vocabulary 分区、modality/type embedding、1D/2D position、attention mask、loss weighting、tokenizer freeze/version、context allocation、condition dropout/guidance、special tokens 与 decoding policy，任六项不足时仍应补全。
## B. 手算与建模
### GEN63-B01
$h=w=512/16=32$，token 数 $n=1024$。raster AR 顺序 NFE 约 1024；16-round masked sampler 约 16，虽每轮都处理全 grid。
### GEN63-B02
Raster $(a,b,c,d)$：$p(a)p(b\mid a)p(c\mid a,b)p(d\mid a,b,c)$。Column $(a,c,b,d)$：$p(a)p(c\mid a)p(b\mid a,c)p(d\mid a,c,b)$。
### GEN63-B03
拼接长度 1280，全 self-attention score 元素 $1280^2=1,638,400$。图像 query 对文本 key cross-attention 为 $1024\times256=262,144$；还未计 heads/batch。
## C. 推导与证明
### GEN63-C01
ordering $\pi$ 是 bijection，重命名后的变量序列仍包含全部随机变量。反复用乘法公式 $p(a,b)=p(a)p(b\mid a)$，得到任意次序的 chain rule；支持零概率条件按联合概率定义处理。
### GEN63-C02
真实 $p(k_M\mid k_{\bar M})$ 可包含待填 token 之间的相关性；乘积 marginals 删除 conditional mutual dependence。除非在给定可见上下文后条件独立，否则不等；多轮 refinement 只是近似协调。
### GEN63-C03
若同一 joint $p(y,k)$ 且 marginals/conditionals 精确，Bayes/chain rule 给两种分解。有限模型分别优化不同 conditionals、mask/order 与数据权重，函数类和误差投影不同，故训练结果不等价。
## D. 边界、反例与纠错
### GEN63-D01
共享整数空间只表示 lookup table 可共用；若 image ID 7 与 text ID 7 的语义无关，甚至会冲突。对齐需配对数据、objective、attention/position 设计和学习结果，常用分区 vocabulary/type embedding。
### GEN63-D02
perplexity 是对各 tokenizer 诱导的随机变量和 alphabet 的 NLL。一个丢失大量信息、容易预测的 tokenizer 可有低 PPL；token 数和 $K$ 不同也改单位。应比较 bits/dimension、rate–distortion 和 end-to-end 任务。
### GEN63-D03
它是机制/经验假说 H/E，不是 chain-rule 定理。用 matched data/compute/params 的理解-only、generation-only、joint 训练，跨 seed 测理解任务，并控制 tokenizer/auxiliary loss，做消融与负迁移检查。
## E. AI 迁移
### GEN63-E01
text-to-image：text 可双向或 causal 内部，image queries 可看全部 text 与过去 image；caption：image tokens 全可见，text causal；editing：保留 image context 双向，masked target 可看文本和可见图像但按 sampler 限制目标间信息。表中明确每块 Q→K 的 0/1。
### GEN63-E02
固定 tokenizer、序列长度、Transformer、params、训练 tokens、optimizer 和 sample budget，只改 raster/column/space-filling/coarse-to-fine ordering；报告 NLL、sample/conditional metrics、locality statistics、wall-clock 与 seed spread。
### GEN63-E03
为 tokenizer 保存 immutable version hash，cached token dataset 写该 hash；prior checkpoint 声明 compatible tokenizer hash/vocabulary/grid。任何 tokenizer 更新生成新版本和新 cache，不静默覆盖；decoder 与 code ordering 同步迁移或拒绝加载。

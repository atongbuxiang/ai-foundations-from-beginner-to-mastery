---
type: solution
status: draft
topic: "[[VQ-VAE、离散 Tokenizer 与 Straight-Through Estimator]]"
exercise: "[[习题 - VQ-VAE、离散 Tokenizer 与 Straight-Through Estimator]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - VQ-VAE、离散 Tokenizer 与 Straight-Through Estimator
## A. 识别与复述
### GEN60-A01
$k=\arg\min_j\|z-e_j\|^2$，$q=e_k$，$z_q=z+\operatorname{sg}(q-z)$。$k$ 是整数 token，$q$ 是 embedding vector，二者不可混写。
### GEN60-A02
reconstruction 更新 decoder，并经 STE 更新 encoder；$\|\operatorname{sg}z-q\|^2$ 更新 codebook；$\beta\|z-\operatorname{sg}q\|^2$ 更新 encoder，使其靠近所选 code。
### GEN60-A03
autoencoder 只学真实输入到 codes 再重构。生成需要从 code distribution 采新的协调序列，因此还要学习 $p_\theta(k_{1:n})$；独立均匀抽 codes 通常不符合数据诱导 joint distribution。
## B. 手算与建模
### GEN60-B01
到三点的平方距离为 $2.05,.45,4.85$，最近的是 $(2,0)$，故 $k=2,q=(2,0)$。
### GEN60-B02
标准 STE 代理 Jacobian 为 $I$，encoder 收到 $(.7,-.2)$。真实 hard nearest-neighbor map 在当前 Voronoi cell 内常数，真实导数为零；在边界不可导。
### GEN60-B03
$1024\log_28192=1024\times13=13312$ bits，即 1664 bytes。实际码率取决于 token entropy、entropy coder、side information、model/codebook amortization；固定长 nominal code 不等于压缩 bitstream。
## C. 推导与证明
### GEN60-C01
前向 stop-gradient 不改值，$z_q=z+q-z=q$。反向 $\operatorname{sg}$ 导数为零，所以代理 $\widetilde\partial z_q/\partial z=I$，且 reconstruction path 不更新 $q$。
### GEN60-C02
assignment count $n_k$ 和向量和 $\sum z_r$ 做 EMA 得 $N_k,M_k$，center $e_k=M_k/N_k$；这正是用加权历史样本均值近似当前 cluster mean。空 cluster smoothing/reset 是额外合同。
### GEN60-C03
更大 $K$ 提供更多 centers，最优 nearest-neighbor distortion 可不增；但每个 code 样本更少、softmax alphabet 更大、dead codes 更易出现，prior entropy/model capacity 要求也改变。因此是联合折衷。
## D. 边界、反例与纠错
### GEN60-D01
STE 明确把真实几乎处处零的 Jacobian 替换为 $I$。它是优化启发式/代理估计，不是链式法则对 hard map 的结果；任何“无偏”主张需另证。
### GEN60-D02
tokenizer 可逐图近乎无损，但 prior 若把对象上半与下半 codes 独立组合，就生成结构不一致图像。好 reconstruction 只验证 $D(T(x))$，未验证 $k\sim p_\theta$。
### GEN60-D03
encoder 可随机均匀散列样本到所有 codes，usage 100%，却破坏相似性或让 decoder/prior 难学。利用率是覆盖统计，不是语义、失真或生成质量的充分条件。
## E. AI 迁移
### GEN60-E01
保存 encoder/decoder、codebook、$K,d$、grid/downsample、distance/normalization、STE variant、loss weights、EMA decay/counts/sums、reset policy、initialization、latent scale、optimizer、token ID ordering 与 tokenizer version hash。
### GEN60-E02
同一 validation split 统计 usage/dead threshold、assignment entropy/PPL、$\|z-q\|^2$、norm ratio、pixel/perceptual reconstruction/rFID，并附 frequency histogram 与 seed spread。不要用单一 PPL 代表 collapse 全貌。
### GEN60-E03
固定 architecture、initial codebook、loss、batch、optimizer budget 和 seed set；gradient 版与 EMA 版各调其必要但预注册的少量超参，报告相同训练 tokens、wall-clock、全部指标与更新规则，不把 EMA 的额外 reset 只给一方。

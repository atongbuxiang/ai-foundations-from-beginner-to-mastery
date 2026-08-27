---
type: solution
status: draft
topic: "[[DDCM、离散生成路线比较与证据地图]]"
exercise: "[[习题 - DDCM、离散生成路线比较与证据地图]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - DDCM、离散生成路线比较与证据地图
## A. 识别与复述
### GEN64-A01
DDCM 离散 reverse DDPM 的 noise choices；D3PM 的 state 本身在 finite alphabet 上跳；VQ 把 encoder representation 量化成 code indices。三者的 forward object、token semantics 与训练需求不同。
### GEN64-A02
$x_{t-1}=\mu_\theta(x_t,t)+\sigma_t\varepsilon_{t,k_t}$，$\varepsilon_{t,k}\in\mathcal C_t$。忽略初始状态/overhead，固定长 nominal bits 为 $T\log_2K$。
### GEN64-A03
I：给定 indices 后 sampler 输出确定、名义组合数 $K^T$；T：有限 empirical sampling 在假设下逼近目标；E：特定模型小 $K$ 仍保持 FID；H：temporal indices 可能易于 1D prior；O：能否成为通用语义多模态 tokenizer。
## B. 手算与建模
### GEN64-B01
$100\log_264=100\times6=600$ bits=75 bytes，未计 $x_T$、headers、entropy coding、model/codebook shared cost。
### GEN64-B02
内积依次为 $2,-1,-2,1$，最大是 $(1,0)$，故选择第一个 code。
### GEN64-B03
权重 $w_k=\exp[-\|\epsilon_k-m\|^2/2]$。距离平方依次为 $.25,1.25,4.25,3.25$，故未归一权重为 $(e^{-.125},e^{-.625},e^{-2.125},e^{-1.625})$。
## C. 推导与证明
### GEN64-C01
$N(m,I)$ 在 code $\epsilon_k$ 的密度正比 $\exp[-\|\epsilon_k-m\|^2/2]$。展开为 $\exp[-\|\epsilon_k\|^2/2+\epsilon_k^Tm-\|m\|^2/2]$；若 code 等模，前后与 $k$ 无关项消去，softmax logits 为 $\epsilon_k^Tm$。
### GEN64-C02
不同 index sequences 可经非线性 sampler 映到相同/近似图像；许多序列可能落在低质量区域；实际 sampling distribution 不均匀。故组合计数只是 domain cardinality upper bound，不给 image-map injectivity、quality 或 coverage。
### GEN64-C03
argmax 选择 empirical set 中最符合目标方向的极值；$K$ 越大，最大值趋向更极端/确定的最佳补偿，而不是按 Gaussian density随机抽一个样本。恢复目标 law 需要按密度权重抽样等一致机制。
## D. 边界、反例与纠错
### GEN64-D01
免额外训练以已有 diffusion 为前提。编码仍需 $T$ 次 denoiser 和每步 code search，可能是 $O(TKd)$；模型、codebook 存储与传输也需 amortize。
### GEN64-D02
$T$ 是反向步数也是 index 序列长度。减少 $T$ 降 NFE，也把 nominal bits 从 $T\log K$ 降低，并改变可达轨迹与 distortion；这不是只改 solver 容差的纯加速。
### GEN64-D03
DDCM index 表示某时间步选哪份全局噪声向量，不对应固定图像 patch/对象。语义可解释性、局部编辑和 prior learnability 需要实验，不能从 1D index format 推出。
## E. AI 迁移
### GEN64-E01
记录 base checkpoint/parameterization、$T,\sigma_t$、per-step/shared codebooks、$K,d$、PRNG/seed/dtype、$x_T$ 策略、index sampling/encoding rule、norm/softmax temperature、search、bitstream format、entropy coder、metrics、NFE/wall-clock。
### GEN64-E02
固定总 code vectors 存储、base model、$T,K$ 或分别报告两种公平口径；同 seed sets 比 generation/encoding、distortion/diversity、search cost。共享版不能偷用更多 $K$ 而不报告 memory；per-step 版要计 $TKd$ 存储。
### GEN64-E03
每条路线填：处理对象；是否需新训练；forward/noise；编码输出/shape；nominal+actual rate；representation/model/sampler floor；encode/decode NFE、memory、latency；编辑/条件接口；证据层级。先按任务约束筛选，再比较同协议结果，不给普遍排名。

---
type: concept
status: draft
area: [architecture, inference, mla, latent-cache]
aliases: [Multi-Head Latent Attention, MLA, Latent KV Cache]
node_id: ARCH-56
prerequisites: ["[[KV Cache、MHA、MQA 与 GQA]]", "[[RoPE 的旋转推导、群表示与内积]]", "[[低秩投影与序列维压缩 Attention]]"]
related: ["[[高效 Attention 与推理接口 MOC]]", "[[Transformer 形状、参数量与 FLOPs 总账]]", "[[Attention 矩阵的秩、瓶颈与有效秩]]"]
sources: ["[[S-2024-DeepSeek-V2-MLA]]", "[[S-2024-Su-10091-MHA-MQA-GQA-MLA]]", "[[S-2025-Su-10907-MLA上]]", "[[S-2025-Su-11111-MLA下]]"]
exercises: ["[[习题 - MLA、潜变量缓存与推理成本证据]]"]
solutions: ["[[解答 - MLA、潜变量缓存与推理成本证据]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-mla-latent-cache-reparameterization-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# MLA、潜变量缓存与推理成本证据

> [!abstract] 核心问题
> MLA 把每个 token 的多头 K/V 内容联合压入低维 latent，训练时可展开成多头 K/V，decode 时通过线性投影吸收直接对 latent 做 attention。RoPE 不能全部吸收，因此保留独立位置 key 分支。强结论必须拆成代数、cache bytes、数值、kernel 与消融五张证据表。

## 一、不要把 MLA 误解成“Linformer 放到 KV Cache”

Linformer 沿 sequence axis 把 $n$ 个 token 压成 $k$ 个槽；MLA 对每个 token 分别把 feature channels 压成 $d_c$ 维 latent。序列长度仍为 $t$，但每个历史 token 的 cache width 变小。

设 residual state $x_t\in\mathbb R^d$，联合 KV down-projection：

$$
c_t^{KV}=W_D^{KV}x_t\in\mathbb R^{d_c}.
$$

对 head $h$，内容 K/V 可展开为

$$
k_{t,h}^{C}=W_{UK,h}c_t^{KV}\in\mathbb R^{d_k^C},
$$

$$
v_{t,h}^{C}=W_{UV,h}c_t^{KV}\in\mathbb R^{d_v}.
$$

训练时可按 MHA-friendly 形式构造这些多头 K/V。

## 二、为什么线性投影可以吸收到 Query

内容 score 为

$$
(q_{t,h}^{C})^T k_{j,h}^{C}
=(q_{t,h}^{C})^T W_{UK,h}c_j^{KV}
=(W_{UK,h}^Tq_{t,h}^{C})^Tc_j^{KV}.
$$

定义吸收后的 query

$$
\tilde q_{t,h}^{C}=W_{UK,h}^Tq_{t,h}^{C}\in\mathbb R^{d_c},
$$

就可直接与所有历史 $c_j^{KV}$ 做 dot product，不必缓存每头 $k_{j,h}^{C}$。

Value 同样可在加权后再 up-project：

$$
\sum_j a_{tj}^{(h)}v_{j,h}^{C}
=W_{UV,h}\left(\sum_j a_{tj}^{(h)}c_j^{KV}\right).
$$

由于 $W_{UV,h}$ 与 $j$ 无关，可移出求和，并进一步与 output projection 组合。这是解码重参数化的代数核心。

> [!important] “吸收”所需条件
> 中间必须是线性映射，且该映射不依 key position/index。若夹有 normalization、quantization、非线性、data-dependent scale 或不可交换的位置变换，就不能直接沿用这条恒等式。

## 三、RoPE 为什么迫使 MLA 分出位置支路

若对完整 $k_{j,h}^{C}=Wc_j$ 施加 position-dependent rotation $R_j$：

$$
q_t^TR_t^TR_jWc_j,
$$

$R_jW$ 依历史位置 $j$，一般不能把固定 $W$ 完全吸收到当前 query 后仍只缓存 $c_j$。

MLA 因而采用 content/position 分支：

$$
q_{t,h}=[q_{t,h}^{C},q_{t,h}^{R}],
\qquad
k_{j,h}=[k_{j,h}^{C},k_j^{R}],
$$

其中只有较小 $d_R$ 的支路使用 RoPE，位置 K 可在 heads 间共享。Score 为

$$
s_{tj}^{(h)}
=(\tilde q_{t,h}^{C})^Tc_j^{KV}
+(R_tq_{t,h}^{R})^T(R_jk_j^{R}).
$$

因此 cache 至少包含

$$
[c_j^{KV},k_j^R],
$$

每 token width 约 $d_c+d_R$。这就是 Partial/Decoupled RoPE 与 latent cache 的接口。

## 四、Cache 总账

MHA 每 token 每层 K/V payload 约

$$
2h_qd_h.
$$

MLA 约为

$$
d_c+d_R,
$$

若位置支路只缓存 K 而不缓存对应 V。压缩比为

$$
\rho=\frac{d_c+d_R}{2h_qd_h}.
$$

必须代入具体 config；不能只说“低秩所以小”。还要计 quant scales、page metadata、latent normalization state 和 distributed replication。

## 五、训练形式与 Decode 形式为何不同

训练/prefill 有大量 query，可用 expanded MHA form 充分利用矩阵乘和 mature kernels；decode 每步 query 少、历史长，带宽更关键，可用 absorbed latent form 减少 cache 读取。

两种形式在实数代数中对可吸收分支等价，但浮点计算顺序不同：

$$
(q^TW)c\quad\text{与}\quad q^T(Wc)
$$

在 BF16/FP16 下可能有不同舍入，且多层累积。需要 fp64 reference、full-vs-latent、full-forward-vs-cache 三类测试，而不是只看公式。

## 六、MLA 可能增加哪些算术

Cache width 小不等于所有算术小。吸收后 query content 维度可变为 $d_c$，可能大于常规 $d_h$；query 投影/score 每步算术增加。MLA 的系统押注是：decode 在目标 batch/context 下 bandwidth 节省大于额外 compute。

因此必须分别测：

- training/prefill MHA form；
- decode latent form；
- $d_c,d_R,h_q$；
- batch×context×output length；
- tensor parallel communication；
- MTP/speculative decoding 带来的额外 compute headroom。

当 speculative decoding 让每步并行验证多个 tokens、compute 比重上升时，MLA 的 Pareto 位置可能改变。

## 七、DeepSeek-V2 证据怎样读

[[S-2024-DeepSeek-V2-MLA]] 报告显著 cache 减少和 throughput 提升，但整模型同时改变 MoE、训练数据、规模和系统。可直接采用的强结论是 MLA 的结构公式、配置和该协议测量；不能从 DeepSeek-V2 对旧模型的整体系比较单独识别“MLA 造成多少质量提升”。

[[S-2024-Su-10091-MHA-MQA-GQA-MLA]] 对训练/解码两种等价形式和 bandwidth/compute 交换给出非常清晰的中文推导，还特别提醒 BF16 重参数化差异。这部分是理解实现合同的重要补充。

## 八、MLA 好在哪里：消融与理论解释分开

[[S-2025-Su-10907-MLA上]] 在公开的小规模协议中消融：增大 head dimension、Partial RoPE、KV sharing。作者初步观察 head dimension 收益最大，Partial RoPE 有帮助，KV sharing 仍需更大规模验证。参数量未严格对齐，因此应标 `E`，而非“已证明三因素因果贡献”。

[[S-2025-Su-11111-MLA下]] 给出更偏理论的表达/共享解释，并使用“似乎”“一定范围内难以超越”等限制语。正确整理方式是：

- 可复算矩阵恒等式/rank：`I`；
- 上篇固定协议消融：`E`；
- Partial RoPE 下有限候选家族的最优性直觉：`H`；
- 不同 kernel、量化、MTP 和硬件下的 Pareto：`O`。

## 九、正式图：MLA 的代数与证据怎样分账

这张图回答什么问题？为什么 cache latent、训练/解码重参数化和“MLA 最优”不是同一强度的结论？

![[00-知识库管理/_assets/figures/architecture/fig-mla-latent-cache-reparameterization-v1.svg|900]]

> [!figure] 图 1｜MLA 的联合 latent cache、两种代数形式与证据等级。**图源与生成**：本仓库原创 SVG，由 [[00-知识库管理/_labs/code/plot_architecture_efficient_attention_v1.py]] 生成；符号抽象自 DeepSeek-V2/科学空间推导，未复制论文原图或训练曲线。

**怎样读图**：A 从每 token $x_t$ 压到 $c_t^{KV}$，并连同小型 RoPE key 支路缓存；B 把训练时展开 K/V 与 decode 时吸收投影、聚合 latent 的形式区分；C 依次把 shape 恒等式、系统报告、消融、有限家族解释和开放 Pareto 标为 I/E/H/O。

**图没有证明什么**：图没有证明 $d_c+d_R$ 在所有 config 都小于 GQA cache，也没有证明 absorbed form 在低精度 bitwise 等价；DeepSeek 整模型结果和博客消融都不能推出 MLA 在所有 attention、硬件和 decoding strategy 上全局最优。

## 十、实现审计清单

1. $W_D^{KV},W_{UK},W_{UV}$ 的 shape 与 head layout；
2. latent 后 RMSNorm/scale 的位置；
3. content/rotary dimensions 与 pairing；
4. cache 实际保存 latent 还是 expanded K/V；
5. kernel 是否支持 absorbed decode form；
6. query/output projection 是否正确合并；
7. cache position offset、packing、sliding window；
8. fp32/bf16/fp8 与 cache quantization；
9. TP shard、all-reduce/all-gather；
10. full/expanded/latent 三路径输出与梯度测试。

“模型代码中出现 MLA 类名”不保证实际 cache 已压缩；必须测 allocated cache bytes 与 profiler traffic。

## 十一、公平比较协议

比较 MHA/GQA/MLA 应至少提供两条轨道：

- **等训练计算/参数轨道**：控制训练 tokens、FLOPs、参数和优化器，比较 loss/任务；
- **等 cache/Serving 轨道**：控制每 token cache bytes、硬件、kernel、batch/context/output，比较 latency/throughput。

再做 head dimension、Partial RoPE、KV sharing、latent width、normalization 的 factorial/逐项消融。只把默认 MHA-128 与 MLA 的多个同时变化比较，无法识别机制。

## 十二、证据边界

- 投影吸收、value 求和移出、cache width：满足线性条件的 `I`；
- DeepSeek-V2 cache/throughput：其协议下 `E`；
- 科学空间 10907：特定规模消融 `E`；
- 11111 的有限家族最优性解释：`H`；
- “MLA 是最好的 full attention”：在未固定训练/推理成本、候选家族、kernel、MTP 和硬件前属于不可成立的无界命题。

## 十三、学习出口

应能从 $c^{KV}$ 推导 content score/value 的投影吸收，解释 RoPE 为什么要分支，算具体 cache 比例，并设计 expanded-vs-latent 数值测试与等训练/等 Serving 两条公平比较轨道。


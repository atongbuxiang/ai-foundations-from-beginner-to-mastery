---
type: concept
status: verified
area: [language-models, peft, qlora, quantization, memory]
node_id: LM-30
aliases: [QLoRA 显存, Quantized LoRA, 4-bit fine-tuning]
prerequisites: ["[[LoRA 的低秩更新、初始化、缩放与合并]]", "[[Loss Scaling、Master Weight 与低精度梯度累积]]"]
related: ["[[训练量化、优化器状态压缩与 QAT]]", "[[Adapter、Prompt Tuning、Prefix Tuning 与 IA3]]"]
sources: ["[[S-2023-Dettmers-QLoRA]]", "[[S-2021-Hu-LoRA]]"]
exercises: ["[[习题 - QLoRA、量化基座与适配显存总账]]"]
solutions: ["[[解答 - QLoRA、量化基座与适配显存总账]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-adapt-qlora-memory-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# QLoRA、量化基座与适配显存总账

> [!abstract] 一句话结论
> QLoRA 把冻结基座以 4-bit 形式存储，前向时反量化到计算 dtype，让梯度穿过基座运算流向 LoRA；4-bit 描述的是一类持久权重编码，不是全部训练内存，也不是基座在 4-bit 中被更新。

## 一、计算图到底发生什么

对基座权重块 $W_0$，量化器输出：

$$
(q,c)=Q(W_0),
$$

$q$ 是低 bit codes，$c$ 是 scale/offset/block metadata。计算时：

$$
\widetilde W_0=D(q,c;\text{compute dtype}),
$$

前向：

$$
y=\widetilde W_0x+sBAx.
$$

训练更新 $A,B$，不更新 $q,c$。梯度需要经过 $\widetilde W_0$ 对 activations 的线性作用，才能传到更早的 adapter/activation；但无需为 frozen base 保存 optimizer moments。

这与 quantization-aware full fine-tuning 不同：QLoRA 的核心不是用 straight-through estimator 更新 4-bit base。

## 二、Storage dtype、compute dtype 与 accumulation dtype

至少分三种 dtype：

1. **storage dtype**：4-bit codes/packed bytes；
2. **compute dtype**：反量化后 matmul 使用 fp16/bf16 等；
3. **accumulation dtype**：乘加和 reduction 的内部精度。

LoRA weights、gradients、optimizer states 又可各有 dtype。写“4-bit training”会遗漏绝大多数数值合同。

例如同一 4-bit base：

- bf16 compute 与 fp16 compute 的范围/舍入不同；
- group size 改变 metadata 与误差；
- kernel 可按 tile 动态反量化或缓存；
- output accumulation 可用 fp32；
- adapter master weights/optimizer moments 常高于 4-bit。

## 三、NF4 的对象与边界

QLoRA 提出 NormalFloat 4-bit，基于近似正态权重分布构造非均匀 codebook。抽象写为

$$
q_i=\arg\min_{k\in\{1,\ldots,16\}}
|w_i/c-z_k|,
\qquad
\widetilde w_i=c z_{q_i}.
$$

$z_k$ 是 16 个 codebook values，$c$ 是块 scale。其“信息论最优”主张有分布与标量量化设定，不能简化为对任意训练后权重、outlier 或所有误差指标最优。

真实审计需看：

- codebook 版本；
- block/group size；
- absmax/scale 计算；
- zero representation；
- outliers；
- packing layout 与 kernel。

## 四、Double quantization 在省什么

普通 block quantization 除 codes 外还需存每块 scale $c_b$。Double quantization 再压缩这些 constants：

$$
(q_c,c_c)=Q_c(\{c_b\}),
$$

使用时恢复 $\widetilde c_b$。它减少量化 metadata 的平均 bits/parameter，但引入第二层误差和解码合同。

总 base storage 近似：

$$
M_{\text{base}}
=M_q+M_{\text{scale/meta}}+M_{\text{quant-overhead}}.
$$

不能直接用 $0.5N$ bytes 代表所有 4-bit storage。

## 五、训练显存总账

峰值内存应写成：

$$
M_{\text{peak}}
=M_{\text{q-base}}
+M_{\text{quant-meta}}
+M_{\text{adapter-param}}
+M_{\text{adapter-grad}}
+M_{\text{optimizer}}
+M_{\text{activation}}
+M_{\text{temp/kernel}}
+M_{\text{runtime}}.
$$

其中 runtime 可含 allocator reserved、CUDA context、communication buffers。每项的生命周期不同，简单相加是上界/账本，不一定同一时刻全峰值。

### 一个 toy 估算

设基座 $N=1$ billion：

- 理想 4-bit codes：$0.5$ GB；
- 若 metadata 平均 0.1 bytes/parameter：0.1 GB；
- LoRA 参数 10M，以 bf16：0.02 GB；
- LoRA gradients bf16：0.02 GB；
- Adam 两 moments fp32：0.08 GB；

仅这些是 0.72 GB，但 activations、temporary、allocator、embedding/output 未量化部分可能更大。故实际 peak 不能由参数表直接得到。

## 六、Activations 为什么常成为主项

Activation memory 近似随

$$
B\times L\times d\times \#\text{saved tensors}
$$

增长，attention 某些实现还含 $L^2$ 中间量。基座 frozen 并不意味着无需为 adapter 反向保存任何 activation；LoRA 梯度需要其输入。

Gradient checkpointing 以重算换存储；Flash-style kernels 改变中间量；packing 改变有效 token/shape。比较 QLoRA 与 full/LoRA 时必须固定这些条件。

## 七、Paged optimizer 解决什么

Paged optimizer 借助统一内存/分页思路管理峰值 spikes，目标是避免偶发 OOM。它不是让 optimizer state 消失：

- state 仍有 bytes；
- host↔device migration 可能增加延迟；
- page fault 和带宽依硬件/访问模式；
- steady-state allocated 与 peak-resident 需分报。

“能跑”与“训练更快”是不同结论。

## 八、量化误差与 adapter 补偿

QLoRA 优化的是

$$
\min_{A,B}
\mathcal L(\widetilde W_0+sBA),
$$

不是

$$
\min_{A,B}
\mathcal L(W_0+sBA).
$$

Adapter 可部分补偿量化基座的函数误差，但受到 rank、target modules 和数据限制。若 full-precision base 与 quantized base 起点性能不同，最终差异不能只归因 PEFT。

公平消融至少比较：

- fp base zero-shot；
- quantized base zero-shot；
- fp LoRA；
- QLoRA；
- 若可行，full fine-tuning。

并给同 template/sampler/eval。

## 九、Merge 与部署

要把 LoRA 合入量化 base，通常经历：

$$
(q,c)
\xrightarrow{D}
\widetilde W_0
\xrightarrow{+\ sBA}
W_*
\xrightarrow{Q'}
(q',c').
$$

最后的 $Q'$ 再引入舍入，故：

$$
D(Q'(W_*))\ne W_*
$$

一般成立。部署选择包括：

- 保留 quantized base + runtime adapter；
- merge 到较高精度；
- merge 后重新量化；
- 多 adapters 动态切换。

每种的存储、延迟、误差和可撤销性不同；必须保存 merge recipe 与 post-merge evaluation。

## 十、图解：梯度路径与显存账

先看图回答：图中的 4-bit、compute dtype、LoRA optimizer 和 activation 分别在哪个生命周期存在？

![[00-知识库管理/_assets/figures/language-models/fig-lm-adapt-qlora-memory-v1.svg|900]]

> [!figure] 图 LM-30　Quantized base→dequant compute→LoRA gradient 与内存分项
> 上方画计算路径，下方将基座、adapter 状态、activations 与临时峰值分开；条宽仅为解释性相对量。
> **生成：**本图由本库依据本节定义、正文列出的一级来源和固定绘图脚本重新绘制；图中的小规模数值或结构用于教学，不复刻论文原图。

**怎样读图**：先区分持久存储和运行时 materialization，再沿梯度箭头确认只有 adapter 被优化；最后检查 peak 是否由 activation/temporary 主导。

**图没有证明什么**：相对条宽不是某 GPU 测量，不证明 NF4 对所有权重最优，也不保证 paged optimizer 提升吞吐。

## 十一、可复现实验字段

- exact base revision 与未量化 baseline；
- quant format、codebook、group size、metadata/double-quant；
- storage/compute/accumulation dtype；
- kernel/library/hardware；
- LoRA target modules、rank、scale、dtype；
- batch、sequence、packing、checkpointing；
- optimizer、paging/offload；
- allocated/reserved/peak 与采样时刻；
- tokens/s、FLOPs、wall time、OOM；
- pre/post merge logits 和任务指标。

## 本节出口

你应能解释 4-bit 存在哪里、何时反量化、哪些状态仍是 16/32-bit，并写出端到端峰值内存账。下一节在统一计算图中比较不同 PEFT 接口：[[Adapter、Prompt Tuning、Prefix Tuning 与 IA3]]。

## 练习与独立解答

- [[习题 - QLoRA、量化基座与适配显存总账]]
- [[解答 - QLoRA、量化基座与适配显存总账]]

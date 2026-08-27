---
type: methodology
status: verified
area: [training, scaling-laws, compute, systems, energy]
node_id: TRN-52
aliases: [IsoFLOP, Training Compute Ledger, Model FLOPs Utilization]
prerequisites: ["[[Chinchilla、Compute-optimal 参数与数据分配]]", "[[Transformer 形状、参数量与 FLOPs 总账]]", "[[浮点数与舍入误差]]"]
related: ["[[数据质量、重复、混合与有效 Token]]", "[[过训练、推理成本与多目标最优规模]]", "[[通信 Roofline、非确定性与分布式训练证据地图]]"]
sources: ["[[S-2022-Hoffmann-计算最优训练]]", "[[S-2024-Porian-Resolving-Compute-Optimal-Scaling]]", "[[S-2024-Pearce-Song-Reconciling-Kaplan-Chinchilla]]", "[[S-2023-Chowdhery-PaLM]]", "[[S-2021-Patterson-Carbon-Emissions-Training]]"]
exercises: ["[[习题 - IsoFLOP、训练算力口径与系统校正]]"]
solutions: ["[[解答 - IsoFLOP、训练算力口径与系统校正]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-isoflop-compute-ledger-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# IsoFLOP、训练算力口径与系统校正

> [!abstract] 一句话结论
> “同算力”至少可能指相同模型 FLOPs、相同硬件执行 FLOPs、相同设备时、相同 wall time、相同能耗或相同货币成本。IsoFLOP 只在 compute 公式与误差足够一致时隔离参数—数据分配；把 FLOPs、时间和能耗互换，会把系统效率差异误写成 Scaling Law。

## 一、Dense Transformer 的 $6ND$ 从哪里来

对一个被每 token 使用的参数，粗略计算：

- forward 乘加约 2 FLOPs；
- backward 对 activation gradient 约 2 FLOPs；
- backward 对 weight gradient 约 2 FLOPs。

于是 dense parameter-dominated training 常用

$$
C_{\rm model}\approx6ND.
\tag{1}
$$

这里 $N$ 是每 token active、参与主要矩阵乘的参数，$D$ 是训练消费 tokens。

式 (1) 是量级近似，不包含或近似忽略：

- attention 的 $S^2d$ 项；
- vocab logits/softmax；
- embedding lookup；
- normalization、activation、optimizer；
- padding 与 sequence packing；
- recomputation；
- sparse/MoE routing；
- failed/overflow/restarted steps。

所以更诚实的形式是

$$
C_{\rm model}
=C_{\rm block}+C_{\rm attn}+C_{\rm vocab}+C_{\rm other}.
\tag{2}
$$

## 二、参数口径必须与 FLOPs 公式一致

定义：

- $N_{\rm total}$：所有存储参数；
- $N_{\rm nonemb}$：排除 embedding/readout 的参数；
- $N_{\rm active}$：一个 token 实际激活的参数；
- $N_{\rm trainable}$：接收 optimizer update 的参数。

对 dense untied Transformer，它们可能接近；对巨大词表、weight tying、冻结层或 MoE，它们差别很大。

若用 $N_{\rm nonemb}$ 代入 $6ND$，却又忽略 vocab projection 的真实 FLOPs，小模型的相对误差往往更大。[[S-2024-Pearce-Song-Reconciling-Kaplan-Chinchilla]] 与 [[S-2024-Porian-Resolving-Compute-Optimal-Scaling]] 都说明这种口径会影响 compute-optimal 拟合。

## 三、Model FLOPs 与 Hardware FLOPs

### Model FLOPs

由模型计算图按数学运算计数，用于算法/scale 比较。它通常不计 kernel inefficiency，但是否计 rematerialization 要显式约定。

### Executed hardware FLOPs

硬件实际执行的浮点运算，可能包含：

- recompute；
- padding；
- fused kernel 的额外操作；
- collective/communication 附近的空转；
- failed attempts。

[[S-2023-Chowdhery-PaLM]] 分别报告 model FLOPs utilization 与 hardware FLOPs utilization，说明两者不能混写。

## 四、利用率、吞吐与时间

设有 $G$ 个设备，每个峰值吞吐 $P_{\rm peak}$，训练 wall time 为 $t$。

Model FLOPs utilization：

$$
\mathrm{MFU}
=\frac{C_{\rm model}}{G P_{\rm peak}t}.
\tag{3}
$$

若 $C_{\rm hw}$ 是执行 FLOPs，则 hardware FLOPs utilization：

$$
\mathrm{HFU}
=\frac{C_{\rm hw}}{G P_{\rm peak}t}.
\tag{4}
$$

通常 $C_{\rm hw}\ge C_{\rm model}$，所以 HFU 可高于 MFU。它不代表模型更快收敛，只表示设备算术单元执行了更多被计数的工作。

Token throughput：

$$
q_{\rm tok}=\frac{D}{t}.
\tag{5}
$$

Time-to-quality 还需要达到固定 loss 的 token 数：

$$
t_{\rm quality}
=\frac{D_{\rm quality}}{q_{\rm tok}}.
\tag{6}
$$

高吞吐但样本效率差的配置，未必有更小 $t_{\rm quality}$。

## 五、一个可手算例子

取

$$
N=10^9,\qquad D=3\times10^{11}.
\tag{7}
$$

按式 (1)：

$$
C_{\rm model}\approx
6\times10^9\times3\times10^{11}
=1.8\times10^{21}\ {\rm FLOPs}.
\tag{8}
$$

若集群有效 model throughput 为 $10^{15}$ FLOP/s，则

$$
t\approx1.8\times10^6\ {\rm s}
\approx20.8\ {\rm days}.
\tag{9}
$$

若只知道硬件峰值 $4\times10^{15}$ FLOP/s 而 MFU 为 25%，得到同样有效吞吐。忽略 MFU 会错误预测约 5.2 天。

## 六、Energy、成本与 Carbon 再分三账

能耗是

$$
E_{\rm elec}
=\int_0^t P_{\rm facility}(\tau)d\tau.
\tag{10}
$$

若用平均功率：

$$
E_{\rm elec}\approx
G P_{\rm device}t\times\mathrm{PUE},
\tag{11}
$$

其中 PUE 近似数据中心总能耗/IT 能耗。

货币成本可能是

$$
C_{\$}
=r_{\rm device}\,Gt
+C_{\rm network}+C_{\rm storage}+C_{\rm labor}.
\tag{12}
$$

碳排近似

$$
\mathrm{CO2e}
=E_{\rm elec}\times I_{\rm carbon},
\tag{13}
$$

碳强度 $I_{\rm carbon}$ 随地点、时段和能源结构变化。[[S-2021-Patterson-Carbon-Emissions-Training]] 展示硬件、数据中心和地点可以造成数量级差异。

因此相同 FLOPs 不推出相同：

- wall time；
- kWh；
- 美元；
- CO2e。

## 七、IsoFLOP 的正确实验合同

对每个预算 $C_k$：

1. 预注册 compute estimator 与容差；
2. 选择多个可行 $N$；
3. 由 compute 公式反解 $D$；
4. 保持 data distribution、tokenizer、optimizer family 和 selection protocol；
5. 实际训练后记录 estimated/actual model FLOPs；
6. 报告超预算、失败、restarts 与调参 compute；
7. 用 curve 内插 minimum，并保留 grid resolution uncertainty。

若某些模型因吞吐慢而提前终止，实验不再是 IsoFLOP；它变成 IsoWallTime，必须重命名。

## 八、系统校正怎样改变排名

考虑配置 A/B：

| 配置 | 达标 model FLOPs | MFU | 设备峰值相同 | wall time 比例 |
|---|---:|---:|---:|---:|
| A | $1.0C$ | 25% | 是 | $4.0C/P$ |
| B | $1.2C$ | 50% | 是 | $2.4C/P$ |

A 的算法 FLOPs 更少，但 B 更早完成。若研究问题是“样本/算法效率”，A 更好；若目标是“交付时间”，B 更好。不能用一个排序回答两个问题。

同理，activation checkpointing 增加 executed FLOPs，却可能允许更大 batch、减少通信或避免 OOM；只看 $C_{\rm model}$ 会漏掉系统收益。

## 九、完整 Compute Ledger

每个 run 至少保存：

### 模型账

$N_{\rm total},N_{\rm nonemb},N_{\rm active}$、depth/width/head/context/vocab、每 token FLOPs 公式。

### 训练账

attempt/success steps、seen/unique/repeated tokens、forward/backward/optimizer/recompute、failed/rescue compute。

### 系统账

设备型号/数量、精度、峰值、MFU/HFU、tokens/s、communication、wall time、峰值内存。

### 资源账

kWh、PUE/测量方法、货币成本、碳强度/CO2e 及缺失项。

### 选择账

超参数搜索、pilot、checkpoint selection、evaluation 与 target confirm。

## 十、图：六种“同预算”不能静默互换

先看图回答：为什么 model FLOPs 相同的两个 run 可以有不同 wall time？为什么 energy 相同又不保证 CO2e 相同？

![[00-知识库管理/_assets/figures/training-optimization/fig-isoflop-compute-ledger-v1.svg|900]]

> [!figure] 图 TRN-52-01　从 Model FLOPs 到系统、能耗与部署成本的六层账
> 来源：课程原创教材图；图按 model operations→executed hardware→device time→wall time→energy/cost→CO2e 展开，并标出 MFU、recompute、communication、PUE 与碳强度。概念依据：[[S-2023-Chowdhery-PaLM]]、[[S-2021-Patterson-Carbon-Emissions-Training]]。

**怎样读图**：沿箭头逐层检查换算需要的新测量量；只要缺一个，就不能从上层唯一推出下层。

**图没有证明什么**：示意账本不提供具体硬件利用率、电价或碳强度，也不主张 FLOPs 不重要；它防止不同资源口径被混称为 compute。

## 十一、停止条件

出现以下任一情况，不得声称 IsoFLOP：

- compute estimator 在规模间更换；
- 一些 runs 按 wall-time 截断；
- failed/restarted steps 从分母删除；
- 不同规模获得不同调参预算却未计账；
- MoE 用 total parameters、dense 用 active parameters；
- context/vocab 改变却仍使用统一 $6ND$；
- model FLOPs 与 executed FLOPs 混用。

正确动作是修正口径、重算预算或缩窄 claim。

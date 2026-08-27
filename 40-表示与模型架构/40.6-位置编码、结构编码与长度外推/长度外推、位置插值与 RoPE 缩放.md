---
type: concept
status: draft
area: [architecture, long-context, position-interpolation, rope-scaling]
aliases: [Context Extension, RoPE Scaling, Position Interpolation, ReRoPE]
node_id: ARCH-47
prerequisites: ["[[RoPE 的旋转推导、群表示与内积]]", "[[相对位置表示、偏置与距离函数]]", "[[Transformer 形状、参数量与 FLOPs 总账]]"]
related: ["[[位置编码、结构编码与长度外推 MOC]]", "[[位置分辨率、混叠与长度外推评测]]", "[[高效 Attention 与推理接口 MOC]]", "[[Transformer 形状、参数量与 FLOPs 总账]]"]
sources: ["[[S-2023-Chen-Position-Interpolation]]", "[[S-2022-Press-ALiBi]]", "[[S-2023-Su-9431-长度外推与局部注意力]]", "[[S-2023-Su-9444-长度外推与位置鲁棒性]]", "[[S-2023-Su-9675-RoPE-β进制视角]]", "[[S-2023-Su-9706-混合进制NTK-RoPE]]", "[[S-2023-Su-9708-ReRoPE]]", "[[S-2023-Su-9859-KeyNorm长度外推]]", "[[S-2023-Su-9948-长度外推技术复盘]]"]
exercises: ["[[习题 - 长度外推、位置插值与 RoPE 缩放]]"]
solutions: ["[[解答 - 长度外推、位置插值与 RoPE 缩放]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-context-extension-methods-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# 长度外推、位置插值与 RoPE 缩放

> [!abstract] 本节主问题
> 把模型配置中的最大长度从 4K 改成 32K，只证明代码接受更长 shape。真正的 train-short/test-long 失配至少包括：未训练过的 position/relative phase、attention 候选数与 softmax制度、任务依赖跨度、数值精度、KV cache 和系统成本。位置缩放只处理其中一部分。

## 一、先定义“外推”

设训练最大长度 $L_0$，测试长度 $L_1>L_0$，扩展倍数

$$
k=\frac{L_1}{L_0}.
$$

需要区分：

- **长度泛化/外推**：参数不经目标长序列训练，直接用于 $L_1$；
- **Context extension**：允许微调、继续预训练或修改位置机制；
- **Position interpolation**：把长位置压回旧范围；
- **Long-context training**：模型实际见过接近 $L_1$ 的 token数/依赖；
- **Serving support**：kernel/cache能执行 $L_1$。

论文和模型卡常混用这些词，比较前必须重写成上述合同。

## 二、直接外推

标准 RoPE 相对位移 $\Delta$ 在频率 $i$ 的相位为

$$
\phi_i(\Delta)=\omega_i\Delta.
$$

Direct extrapolation 保持

$$
\rho(\Delta)=\Delta.
$$

当 $|\Delta|>L_0$，模型面对训练未覆盖的相位组合/相对距离；但近距离 $\Delta$ 的表示完全不变。优点是局部分辨率不压缩，缺点是远端 OOD。

## 三、Position Interpolation

[[S-2023-Chen-Position-Interpolation]] 使用

$$
n'=\frac n k,
\qquad
\Delta'=\frac{\Delta}{k}.
$$

于是测试最大相对位置约被压回训练范围：

$$
\frac{L_1}{k}=L_0.
$$

但相邻位置的相位差也缩小：

$$
\phi_i(1):\omega_i
\longrightarrow\frac{\omega_i}{k}.
$$

所以它用“分辨率拥挤”交换“避免远端相位外推”。模型通常还需一定长序列微调适应新相位尺度；论文的 bound 和实验保留其范数、模型及微调条件。

## 四、统一频率缩放视角

把所有方法写成

$$
\omega_i'=\frac{\omega_i}{s_i}.
$$

- 原 RoPE：$s_i=1$；
- 线性 PI：所有 $s_i=k$；
- 逐频率/NTK-aware：$s_i$ 随 $i$ 变化；
- 混合/分段方案：不同频段不同规则。

若只改变 base 从 $b$ 到 $b'=b\gamma$：

$$
\omega_i'
=(b\gamma)^{-2i/d}
=\omega_i\gamma^{-2i/d}.
$$

高低频缩放不同。它试图保留一部分高频局部分辨率，把更多外推压力分给低频。

## 五、β 进制类比怎样使用

[[S-2023-Su-9675-RoPE-β进制视角]] 注意到不同频率像不同位权上的周期坐标；改变 base类似改变“进制”，统一插值类似把所有位权一起缩放。[[S-2023-Su-9706-混合进制NTK-RoPE]] 据此讨论逐频率混合缩放。

课程把它列为结构类比 H：

- 正弦相位连续且周期；
- β 进制 digit离散并含 floor/mod；
- 相位组合未必一一解码整数位置；
- 公式可启发 $s_i$，不自动给性能/NTK理论。

历史名称 “NTK-aware” 不表示方法继承无限宽 NTK 收敛或泛化定理。

## 六、ReRoPE：窗口外截断相对位移

[[S-2023-Su-9708-ReRoPE]] 的核心可抽象为

$$
\rho(\Delta)=\min(\Delta,w)
$$

（causal 非负约定）。训练窗口内保留标准 RoPE，窗口外不再增加相位。

它避免任意大 $\Delta$，却把所有远于 $w$ 的距离压成同一表示。更重要的是，一般

$$
\rho(i-j)\ne f(i)-f(j)
$$

无法由对 Q/K 各做一次绝对旋转直接实现；可能需分块或额外 score计算，改变 prefill/decode kernel与成本。

标题“无限外推的 ReRoPE？”中的问号必须保留：文章结果是特定小模型和 LLaMA设置的 E，不是任意长度/任务定理。

## 七、Local Window：强基线与代价

[[S-2023-Su-9431-长度外推与局部注意力]] 指出 test-long有两项明显失配：

1. 未见过的相对距离；
2. 每个 query 处理更多 keys，softmax partition/entropy制度改变。

窗口 $w\le L_0$ 同时把最大距离和候选数限制在训练范围。它是重要强基线，但切断直接远程边。$L$ 层窗口可通过多跳传播约 $Lw$ 范围，不等于任意远程信息无损传递；过挤压、路径长度与生成 latency仍在。

## 八、位置鲁棒性训练

[[S-2023-Su-9444-长度外推与位置鲁棒性]] 讨论：训练长度 $N$ 不变，却从更大位置域抽取单调递增 position IDs，或随机拉伸连续位置。

它增加 position/distance覆盖，但不增加：

- 每行 token候选数；
- 真实内容依赖跨度；
- 长序列 memory/optimization；
- 长文数据分布。

因此应把“position coverage augmentation”与“long-context training”分开命名。

## 九、Attention Scale 与 KeyNorm

测试长度增加时，即使 content logit分布逐 key相同，最大值和 partition会随候选数变化。对 i.i.d. logits 的极值/熵分析可提示 $\log T$ 等尺度修正，但真实 logits相关且非同分布。

[[S-2023-Su-9859-KeyNorm长度外推]] 讨论 Q/K norm和 attention集中性对外推的影响，并明确大规模验证边界。KeyNorm、temperature、log-length scale解决的是 logit/entropy制度，不替代 position phase或远程任务证据。

## 十、短上下文性能保持

后处理若改变所有 $\Delta$，可能损失 $L_0$ 内原质量：

- PI 把短距离也缩小；
- base scaling改变部分频率；
- ReRoPE在 $|\Delta|\le w$ 可保持，但实现/softmax组合仍需检查；
- local window在短输入若 $T\le w$ 可完全相同；
- 随机位置训练从头改变训练分布。

报告长上下文增益时必须同时给原范围 regression。

## 十一、KV Cache 与 Serving 合同

RoPE scaling影响 cached K 的旋转。需说明：

- scheme/base/scale是否请求开始后固定；
- cache position是absolute还是local；
- sliding window丢旧token后是否继续 absolute phase；
- dynamic scaling是否随最终未知长度变化；
- 已缓存 keys是否需重算；
- ReRoPE是否需两次 score/分块；
- position cache在多 GPU如何同步。

一个离线 PPL方法可能无法直接高效增量生成。

## 十二、方法比较表

| 方法 | 训练内局部相位 | 测试远端 | 是否常需微调 | 主要新风险 |
|---|---|---|---|---|
| Direct | 保持 | 相位外推 | 否 | OOD |
| PI | 全部压缩 | 回旧范围 | 是 | 分辨率拥挤 |
| Per-frequency scaling | 部分保持 | 压力分频 | 可选 | recipe/频段失配 |
| ReRoPE | 窗内保持 | 远端截断 | 可免 | 距离碰撞/额外kernel |
| Local window | 窗内保持 | 删除远边 | 否/从训均可 | 远程依赖 |
| Random positions | 训练时扩覆盖 | 依采样 | 从头/继续训 | 内容跨度未扩 |

公平比较还要固定长序列微调 token/FLOPs、数据、基础 checkpoint、短长任务、cache kernel和调参预算。

## 十三、图：四种变换不是四个“长度按钮”

先看图回答：Position Interpolation 与 ReRoPE 分别在哪些距离上改变训练内相位？为什么逐频率缩放不能因为叫 NTK-aware 就获得 NTK 定理？

![[00-知识库管理/_assets/figures/architecture/fig-context-extension-methods-v1.svg|900]]

> [!figure] 图 40.6-07　Direct、PI、逐频率缩放、ReRoPE 与三张外推账
> 左栏统一写相对位移/频率变换，中栏列交换的风险，右栏要求 position coverage、attention regime 和 system contract 同时验收。来源：依据 Position Interpolation 与科学空间 9431/9675/9706/9708/9948 独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_position_v1.py]] 生成。

**怎样读图**：把每个方法代入 $\phi_i(\Delta)=\omega_i\rho(\Delta)$，分别画训练区间与测试区间的相位；再检查候选数和系统 kernel是否仍与训练/基线相同。不要只看最大 position ID。

**图没有证明什么**：它不宣布任何方案普遍最优或无限外推，也不证明位置变换足以恢复检索、推理、长文生成或可接受延迟。

## 十四、常见错误与掌握标准

常见错误：修改 max_position_embeddings就称外推；PI后仍说邻位表示不变；把 base scaling与线性插值混同；NTK-aware当NTK theorem；ReRoPE“无限”去掉问号；只报长PPL不报短性能；local window好PPL就称远程能力；dynamic scale与旧KV cache混用；位置随机训练称见过长序列。

> [!summary]
> 长度扩展至少含 position OOD、attention候选制度、任务跨度、数值和系统五层。PI压回旧范围却拥挤分辨率；逐频率缩放分担相位压力；ReRoPE截断远距但引入碰撞与kernel成本；局部窗口和位置鲁棒训练处理不同失配。公式可运行更长不等于模型可利用更长。

能推导相位变换（A/B）、比较分辨率/覆盖/cache（C）、构造远程依赖与短性能反例（D），并写 matched-budget context extension protocol（E）。

## 十五、练习与独立详解

- [[习题 - 长度外推、位置插值与 RoPE 缩放]]
- [[解答 - 长度外推、位置插值与 RoPE 缩放]]

## 参考来源

- [[S-2023-Chen-Position-Interpolation]]
- [[S-2022-Press-ALiBi]]
- [[S-2023-Su-9431-长度外推与局部注意力]]
- [[S-2023-Su-9444-长度外推与位置鲁棒性]]
- [[S-2023-Su-9675-RoPE-β进制视角]]
- [[S-2023-Su-9706-混合进制NTK-RoPE]]
- [[S-2023-Su-9708-ReRoPE]]
- [[S-2023-Su-9859-KeyNorm长度外推]]
- [[S-2023-Su-9948-长度外推技术复盘]]

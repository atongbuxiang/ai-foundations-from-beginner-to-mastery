---
type: concept
status: draft
area: [architecture, state-space-models, mamba, efficient-sequence-models]
aliases: [Selective SSM, Mamba 架构]
node_id: ARCH-16
prerequisites: ["[[HiPPO、S4 与结构化长记忆]]", "[[状态空间的递推—卷积对偶与并行扫描]]", "[[GRU、门控递推与 RNN 结构比较]]"]
related: ["[[Attention 的对象、几何与表达 MOC]]", "[[高效 Attention 与推理接口 MOC]]", "[[循环网络、记忆与状态空间模型 MOC]]"]
sources: ["[[S-2023-Gu-Mamba]]", "[[S-2024-Su-10180-有理生成函数SSM]]"]
exercises: ["[[习题 - 选择性状态空间、Mamba 与证据边界]]"]
solutions: ["[[解答 - 选择性状态空间、Mamba 与证据边界]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-mamba-selectivity-evidence-v1.svg]]"
created: 2026-08-24
updated: 2026-09-03
---

# 选择性状态空间、Mamba 与证据边界

> [!abstract] 本节主问题
> 固定 LTI SSM 对所有 token 使用同一动力学，缺少显式的内容条件化。Mamba 让离散步长及输入/读出相关参数依赖当前输入，使状态能按内容选择传播、写入或读出；固定 convolution kernel 因而消失，论文以 hardware-aware selective scan 恢复高效整段计算。线性序列复杂度不等于无限记忆，也不等于所有设备上恒胜 Attention。

## 导读：如果重要性取决于内容，固定卷积核为什么不够

固定 LTI 状态空间模型有一个非常清楚的优点：某个输入经过 $j$ 步传播后的系数只由距离 $j$ 决定，因此整段映射可以变成固定卷积。可是语言和事件序列中的 token 并不都同样重要。遇到边界、关键词或强干扰时，我们可能希望状态改变保留速度、写入强度或读出方式；只按距离衰减无法显式表达这种选择。

选择性 SSM 的做法，是让当前 token 生成部分状态参数。步长 $\Delta_t$ 可以改变旧状态的 retention，$B_t$ 控制怎样写入，$C_t$ 控制怎样读取。这样早期同一个内容即使距离最终位置同样远，也可能因为中间经过了不同 token 而得到不同传播系数。固定 impulse-response kernel 随之失效，因为系数不再只是 lag 的函数。

但这里不要从“固定卷积失效”直接跳到“无法并行”。每一步对旧状态仍然可能是仿射映射，所以 ARCH-14 的 pair composition 仍然具有结合律，parallel scan 仍可改变计算括号。Mamba 的系统贡献还包括针对内存层次和融合实现的 hardware-aware kernel；模型选择性、scan 代数与设备效率是三层不同主张，必须分别取证。

## 课程位置与两遍学习路线

- **承接什么：** ARCH-14—15 的卷积接口依赖固定 LTI 参数；本页只改变一个关键条件——让当前 token 决定离散步长、写入和读出；
- **本页解决什么：** 用同 lag、不同中间 token 的精确反例证明固定 kernel 失效，同时说明状态更新仍是仿射映射，因此 associative scan 仍可成立；
- **后续为何需要：** 本页完成 RNN—SSM 主线，并把固定状态压缩与 Attention 显式 token memory 的差异交给 40.4、40.7 继续比较。

**第一遍只看两条路径。** 同一个早期写入经过“普通 token”或“边界 token”后，在相同时间距离上得到 $1/2$ 或 $1/4$ 的最终状态；由此看见系数依赖沿途内容，而不只依赖 lag。

**第二遍再审计完整 Mamba block。** 将 selective SSM core 与 local convolution、projection、gate、residual 分账，并分开算法 work、scan span、HBM IO、流式 state bytes、论文实验和硬件版本。

### 问题链

1. 固定 LTI kernel 为什么只能按距离加权，不能显式读取 token 内容？
2. 输入依赖 $\Delta_t$ 怎样改变 retention，$B_t,C_t$ 又分别控制什么？
3. 同一早期 token、相同 lag 的系数为何能因中间 token 而不同？
4. 固定 convolution 失效后，为什么关于 state 的仿射结构还在？
5. selective scan 的 associativity 与 hardware-aware kernel 分别是哪一层主张？
6. 固定大小状态与随长度增长的 KV cache 各自交换了什么能力和成本？
7. “线性时间”“更快”“记得更长”“任务更强”为什么必须分别取证？

> [!check] 第一遍停靠线
> 若你能复算普通路径 $h_3=1/2$、边界路径 $h'_3=1/4$，并解释同一个 lag-2 写入为何不可能由唯一固定 $K_2$ 同时表示，却仍能把两条路径各自写成仿射 pair scan，就完成了 40.2 的第一遍主线。

## 符号与对象账本

| 对象 | 数学身份 | AI 中的身份 | 不能偷换成 |
|---|---|---|---|
| $\Delta_t$ | 输入依赖离散步长 | token-conditioned timescale | 普通位置编码 |
| $\bar A_t=e^{\Delta_tA}$ | 时变 retention | selective state transition | 固定 LTI $\bar A$ |
| $B_t$ | 时变输入映射 | selective write | readout 权重 |
| $C_t$ | 时变输出映射 | selective read | 写入门 |
| $p_t=(\bar A_t,b_t)$ | 一步 state-affine 映射 | selective scan element | 固定 convolution tap |
| recurrent state | 历史的固定维压缩 | streaming cache | 可逐 token 回看的数据库 |
| evidence tuple | model/task/interface/hardware 条件 | 性能结论适用域 | 无条件排行榜 |

### 贯穿算例 $\mathcal S_\square$：同一 lag，却有两种传播系数

继续使用连续基动力学 $A=-2$。普通 token 选择

$$
\Delta_{\mathrm{plain}}=\frac{\log2}{2}
\quad\Longrightarrow\quad
a_{\mathrm{plain}}=e^{-2\Delta_{\mathrm{plain}}}=\frac12,
$$

边界 token 选择更大的步长

$$
\Delta_{\mathrm{boundary}}=\log2
\quad\Longrightarrow\quad
a_{\mathrm{boundary}}=e^{-2\Delta_{\mathrm{boundary}}}=\frac14.
$$

设第 1 步把重要内容写成 $b_1=2$，后两步没有新写入。普通路径的三个仿射元素是

$$
p_1=\left(\frac12,2\right),\qquad
p_2=\left(\frac12,0\right),\qquad
p_3=\left(\frac12,0\right).
$$

从 $h_0=0$ 出发：

$$
h_1=2,\qquad h_2=1,\qquad h_3=\frac12.
$$

若只把中间 token 换成边界 token，则

$$
p'_2=\left(\frac14,0\right),
$$

得到

$$
h'_1=2,\qquad h'_2=\frac12,\qquad h'_3=\frac14.
$$

两条路径中第一次写入到最终读出的时间距离都为 2，但它的传播系数分别为

$$
\frac12\cdot\frac12=\frac14,
\qquad
\frac12\cdot\frac14=\frac18.
$$

若存在只依赖 lag 的固定 tap $K_2$，它必须同时等于 $1/4$ 和 $1/8$，矛盾。因此输入依赖中间转移破坏了单一固定 convolution kernel。

但是每一步仍是 $h_t=a_th_{t-1}+b_t$。普通路径与边界路径的总 pair 分别为

$$
p_3\otimes p_2\otimes p_1
=\left(\frac18,\frac12\right),
$$

$$
p_3\otimes p'_2\otimes p_1
=\left(\frac1{16},\frac14\right).
$$

所以“不能预生成一个固定卷积核”并不等于“不能 parallel scan”；失去的是 time invariance，不是 state-affine composition 的 associativity。

## 核心公式七问：选择性状态路径

$$
\boxed{
h_t=\bar A_t h_{t-1}+\bar B_t x_t,\qquad
y_t=C_t h_t,\qquad
(\Delta_t,B_t,C_t)=S(x_t).
}
$$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 让当前内容调节旧状态保留、当前写入与当前读出 |
| 对象 | $S(x_t)$ 产生时变参数；状态更新对 $h_{t-1}$ 仍仿射，但对整条输入序列不再是固定 LTI |
| 来路 | 在结构化连续 $A$ 上引入 input-dependent discretization/write/read，并保留可扫描状态接口 |
| 步骤 | 先由 token 生成 $\Delta_t,B_t,C_t$，离散化得到 $\bar A_t,\bar B_t$，再更新 state 与读出 |
| 读法 | 不同 token 可以让同一记忆方向慢衰减、快遗忘、强写入或弱读出 |
| 检查 | 改变中间 token 应能改变早期输入系数；相同参数冻结后应退化为 LTI；full 与 chunked state passing 应数值对齐 |
| 去路 | 40.4 用显式内容寻址比较状态压缩，40.7 再比较 selective state 与 KV cache 的推理资源 |

这条选择性方程最值得记住的不是某个模型名，而是它准确改变了哪项假设：从固定 LTI 变成 input-dependent state-affine dynamics。下面先把固定 LTI 的内容无关边界说清楚，再逐项加入 $\Delta_t,B_t,C_t$；这样你会看见哪些计算接口失去、哪些代数结构仍然保留。

## 一、固定 LTI 的内容无关边界

经典离散 SSM

$$
h_t=\bar Ah_{t-1}+\bar Bx_t,\qquad y_t=Ch_t
$$

对每个位置使用同一 $\bar A,\bar B,C$。其 impulse-response kernel $K_j=C\bar A^j\bar B$ 只依赖距离 $j$，不依赖 token 内容。非线性 channel mixer 和堆叠可让整网内容相关，但单个 LTI state core 的传播规则固定。

对离散语言等 information-dense data，一种重要需求是：遇到某类 token 时选择写入，遇到干扰时选择忽略，之后按当前内容选择读出。Attention 用 query-key similarity 显式构造内容依赖权重；selective SSM 则在递推参数中引入内容条件。

## 二、选择性 SSM 的抽象方程

保留结构化连续基矩阵 $A$，令当前表示 $x_t$ 产生

$$
\Delta_t=\operatorname{positive}(s_\Delta(x_t)),\qquad
B_t=s_B(x_t),\qquad C_t=s_C(x_t).
$$

对每步离散化，示意为

$$
\bar A_t=e^{\Delta_t A},\qquad
\bar B_t=\left(\int_0^{\Delta_t}e^{A\tau}d\tau\right)B_t,
$$

$$
\boxed{h_t=\bar A_th_{t-1}+\bar B_tx_t,\qquad y_t=C_th_t.}
$$

论文/实现会利用对角或特殊结构和具体 discretization 简化运算；本式表达机制，不代替逐行 kernel 定义。

## 三、选择性怎样表现为写入、遗忘与读出

- $\Delta_t$ 改变当前步的有效时间尺度：对负实部 $A$，较大 $\Delta_t$ 通常使旧 state 衰减更多；
- $B_t$ 控制当前输入怎样写入各 state 维；
- $C_t$ 控制当前 token 怎样从 state 读出；
- block 中的 gate/activation 进一步调节输出通道。

这和 GRU 有“输入依赖 retention/write”的直觉相似，但 Mamba 的 state expansion、structured $A$、discretization 与 scan 算法有不同合同。不能简单说 Mamba 就是换名 GRU。

## 四、为什么固定 convolution 路径消失

LTI 时

$$
y_t=\sum_{j\le t}C\bar A^{t-j}\bar Bx_j
$$

使用只依赖 lag 的固定 kernel。选择性时，一个早期输入 $x_j$ 到 $y_t$ 的系数含

$$
C_t\bar A_t\bar A_{t-1}\cdots\bar A_{j+1}\bar B_j,
$$

它依赖沿途输入产生的参数。因此不能预先生成单一 $K_{t-j}$ 再做普通 FFT convolution。

代价换来内容条件化；计算路径则转向 time-varying affine scan。

## 五、为何仍可 parallel scan

每步仍是关于 state 的仿射映射

$$
h_t=A_th_{t-1}+b_t,\qquad b_t=\bar B_tx_t.
$$

所以可使用上一节 pair composition 的结合律。Mamba 的 hardware-aware selective scan 进一步针对结构化/逐元素 state transition、GPU memory hierarchy 与融合重算设计 kernel，核心目标包括：

- 不把所有大中间 state 写回慢速显存；
- 融合 parameter production、discretization、scan 与 output；
- backward 中在保存与重算间权衡。

算法层 associativity、渐近 work 和某个 kernel 的实际吞吐属于三种证据。

## 六、一个标量选择性例子

令 $A=-1$，$\bar A_t=e^{-\Delta_t}$，$B_t=1,C_t=1$。若普通 token 取 $\Delta=0.1$，retention $e^{-0.1}\approx0.905$；边界 token 取 $\Delta=3$，retention $e^{-3}\approx0.0498$，几乎 reset 旧 state。

但若希望“重要 token 长久保留”，具体机制还依 $B_t$ 如何写入、之后各步 $\Delta$ 和 $C_t$ 如何变化。不能从单步 gate 直觉推出已学得可靠 symbolic memory。

## 七、Mamba block 的架构视角

原始 Mamba block 可抽象理解为：

1. input projection 产生内容分支和 gate 分支；
2. 局部 causal convolution 给短程顺序 mixing；
3. 内容分支经过激活并生成 selective SSM 参数；
4. selective scan 聚合长程 state；
5. 与 gate 分支逐元素调制；
6. output projection 与 residual 堆叠。

这是理解草图。具体 expansion factor、convolution width、bias、normalization 与并行布局应以对应代码版本为准。论文中的“Mamba 没有 Attention/传统 MLP block”不等于 block 没有 projection、activation 或 gating。

## 八、复杂度必须写出隐藏维

若 sequence length 为 $L$、model width 为 $D$、每通道 state size 为 $N$，selective scan 的核心 work 常按 $O(LDN)$ 记，且对 $L$ 线性。Attention 的 dense score 交互通常含 $O(L^2D)$。但比较还需加入：

- input/output projection 常有 $O(LD^2)$；
- $N$、expansion、layer 数与 batch；
- training activation 与 kernel recomputation；
- Attention 的 Flash-like IO optimization；
- prefill 与 one-token decode 的不同瓶颈；
- KV cache 与 recurrent state 的 bytes。

“线性时间”只说明 $L$ 的渐近次数，不等于常数小，也不等于 latency 永远更低。

## 九、流式 state 与显式检索的差异

Mamba 流式每层保存固定 state，内存不随 context length 线性增长；Attention 通常保存随 $L$ 增长的 KV cache。对应地：

- recurrent state 已压缩历史，旧信息可能不可逆覆盖；
- Attention 可对已缓存 token 做显式内容寻址，但 cache 成本增长；
- 两者都不自动保证精确 retrieval：Attention 可能注意错误，SSM 可能压缩丢失；
- hybrid architecture 可组合两类接口。

资源优势和信息访问模式应分别比较。

## 十、Science Space 与原论文的分工

科学空间 SSM 四篇主要追踪 HiPPO、S4 与生成函数的数学基础；[[S-2024-Su-10180-有理生成函数SSM]]明确把注意力放在有理函数方向，而非把 Mamba 当作相同数学技巧的自然终点。课程据此采用双轨：

- 用科学空间讲清 projection、discretization、DPLR、resolvent；
- 用 [[S-2023-Gu-Mamba]] 补足 input-dependent selection、selective scan、block 与原论文实验；
- 不把博客对工程/数学侧重的评价写成模型优劣定理。

## 十一、图：机制、系统与证据阶梯

先看图回答：输入依赖的 $\Delta_t,B_t,C_t$ 改变了固定 LTI 的哪项等价接口，一句“线性时间”在右栏究竟属于哪一级证据？

![[00-知识库管理/_assets/figures/architecture/fig-mamba-selectivity-evidence-v1.svg|900]]

> [!figure] 图 40.2-08　固定 LTI 与选择性更新、系统资源账和证据边界
> 左栏比较同一 $A$ 与输入依赖 $A_t/\Delta_t,B_t,C_t$；中栏分算术、并行、IO、流式状态和精度；右栏将机制直觉、条件化推导、论文实验、实现证据和开放问题分层。来源：依据 Mamba 原论文及本课程 SSM 推导独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_sequence_ssm_v1.py]] 生成。

**怎样读图**：先在左栏问选择性参数由哪个 token 表示生成、改变了写入还是读出，再到中栏确认固定 convolution 已失效但 affine scan 仍可用，最后把复杂度、吞吐、精度、论文结果与开放外推分别放回右栏证据层。

**图没有证明什么**：它没有证明 selective state 必然记住重要 token，也没有证明 Mamba 在任意长度、模型规模和硬件上胜过 Transformer。

## 十二、如何审计“更快、更长、更强”

对任何 Mamba/SSM 性能断言记录：

1. **模型版本**：原始 Mamba、后续版本或第三方变体；
2. **参数公平性**：参数量、训练 tokens、data、context、optimizer；
3. **任务**：perplexity、downstream、retrieval、long-context extrapolation；
4. **接口**：training、prefill、decode、streaming；
5. **硬件**：GPU/accelerator、batch、dtype、kernel 版本；
6. **资源**：throughput、p50/p95 latency、peak memory、state/cache bytes；
7. **质量**：同 compute/latency/memory budget 下的曲线，而非单点；
8. **复现**：官方代码、commit、warm-up、measurement protocol。

论文报告的结果是重要 E 级证据，但“在所测配置下”是结论的一部分。

## 十三、失败模式

- state bottleneck：高信息密度历史被压缩覆盖；
- selection saturation：$\Delta/B/C$ 参数进入不良数值区；
- long-product precision：低精度扫描下衰减/放大误差；
- chunk boundary：state passing 与 full sequence 不一致；
- kernel fallback：目标设备没有优化 selective scan；
- task shortcut：长程 benchmark 实际被局部线索解决；
- version drift：论文方程、官方实现和第三方模块不一致。

## 十四、常见错误

1. 把 input-dependent SSM 仍写成固定 convolution；
2. 把 “linear in $L$” 写成 “constant memory and time” 而不列 $D,N$；
3. 从固定 state 推出无限精确上下文；
4. 把选择性等同数据库式精确检索；
5. 用 training throughput 替代 decode latency；
6. 忽略 projection、conv、gate 等 block 成本；
7. 把 Science Space 的数学取舍误写成 Mamba 无价值；
8. 把原论文单组速度数字外推所有硬件。

## 十五、掌握标准

> [!summary]
> - Mamba 让 $\Delta,B,C$ 等随输入变化以提供选择性；
> - input dependence 破坏固定 LTI convolution kernel；
> - state-affine 结构仍允许 associative selective scan；
> - 线性长度复杂度、硬件吞吐和固定 state memory是不同断言；
> - 科学空间负责数学桥梁，Mamba 原论文负责机制与实验归属。

能复述 fixed 与 selective 方程（A）、手算标量 retention（B）、证明固定 kernel 失效/scan 仍结合（C）、反驳“无限记忆/永远更快”（D），并完成 model–task–interface–hardware 四维 evidence audit（E）。

## 十六、练习与独立详解

- [[习题 - 选择性状态空间、Mamba 与证据边界]]
- [[解答 - 选择性状态空间、Mamba 与证据边界]]

## 参考来源

- [[S-2023-Gu-Mamba]]
- [[S-2024-Su-10180-有理生成函数SSM]]

---
type: moc
status: active
area: [labs, learning]
aliases: [练习 MOC, 阶段测验 MOC]
prerequisites: []
related: ["[[数学基础完整课程地图与掌握标准]]", "[[线性代数完整学习路线与掌握标准]]", "[[推导与实验 MOC]]", "[[数学基础 MOC]]"]
sources: []
created: 2026-08-14
updated: 2026-08-29
---

# 练习与测验 MOC

> [!abstract] 本模块的任务
> 把“阅读时觉得理解”转化为可以观察的能力：独立计算、解释条件、重建证明、构造反例和迁移到 AI 问题。习题、解答与阶段测验分开保存，错题回链到知识节点。

## 目录

```text
00-知识库管理/_labs/
  exercises/      按节点组织的习题集
  solutions/      独立完整解答
  assessments/    阶段测验、答题记录与错题复盘
```

## 五级题型

| 级别 | 题型 | 目的 | 典型任务 |
|---|---|---|---|
| A | 识别与复述 | 检查定义和对象 | 判断维度、指出假设、读懂符号 |
| B | 手算与构造 | 检查基本操作 | 算投影、QR、特征值、残差 |
| C | 推导与证明 | 检查论证能力 | 补中间式、证明等价、重建定理 |
| D | 边界与反例 | 检查条件意识 | 删除假设、构造失败矩阵、纠错 |
| E | AI 迁移 | 检查应用能力 | PCA、LoRA、谱归一化、优化器情境 |

每份概念习题集至少包含 A–E 各一题。定理节点至少包含两道 C/D 题；数值算法节点至少包含算法选择、误差/残差和复杂度题。

## 已建立的节点练习闭环

| 主题 | 习题 | 独立解答 | 覆盖重点 |
|---|---|---|---|
| 内容寻址、Query、Key 与 Value | [[习题 - 内容寻址、Query、Key 与 Value]] | [[解答 - 内容寻址、Query、Key 与 Value]] | Q/K/V 角色、shape、凸组合、hard/soft retrieval 与候选身份 |
| Scaled Dot-Product Attention 与 Softmax 数值语义 | [[习题 - Scaled Dot-Product Attention 与 Softmax 数值语义]] | [[解答 - Scaled Dot-Product Attention 与 Softmax 数值语义]] | 方差缩放、stable softmax、温度、全遮蔽与 dtype |
| Attention Mask、因果性与可见性合同 | [[习题 - Attention Mask、因果性与可见性合同]] | [[解答 - Attention Mask、因果性与可见性合同]] | padding/causal/structural relation、pre-softmax mask、泄漏与满秩 |
| Self-Attention、Cross-Attention 与张量形状 | [[习题 - Self-Attention、Cross-Attention 与张量形状]] | [[解答 - Self-Attention、Cross-Attention 与张量形状]] | Q/K/V 来源、$T_q/T_k$、置换等变/不变与通用逼近边界 |
| Multi-Head Attention、投影子空间与参数量 | [[习题 - Multi-Head Attention、投影子空间与参数量]] | [[解答 - Multi-Head Attention、投影子空间与参数量]] | packed shapes、$4d^2$、score 存储、head 对称与剪枝 |
| Attention 的几何、核与概率视角 | [[习题 - Attention 的几何、核与概率视角]] | [[解答 - Attention 的几何、核与概率视角]] | norm/angle、位置分布、指数 feature、linear attention 与分母误差 |
| Attention 矩阵的秩、瓶颈与有效秩 | [[习题 - Attention 矩阵的秩、瓶颈与有效秩]] | [[解答 - Attention 矩阵的秩、瓶颈与有效秩]] | logit/weight/output rank、causal 满秩、linear rank 与有效秩 |
| Attention 失效模式、反例与证据地图 | [[习题 - Attention 失效模式、反例与证据地图]] | [[解答 - Attention 失效模式、反例与证据地图]] | 解释、剪枝、退化、长度外推、系统 crossover 与 I/T/E/H/O |
| Transformer Block、残差、归一化与 FFN | [[习题 - Transformer Block、残差、归一化与 FFN]] | [[解答 - Transformer Block、残差、归一化与 FFN]] | Pre/Post 接线、Jacobian、FFN 参数、残差尺度与前沿路由 |
| Transformer Encoder 与双向表示 | [[习题 - Transformer Encoder 与双向表示]] | [[解答 - Transformer Encoder 与双向表示]] | 双向 relation、padding、pooling、置换等变与 BERT 目标边界 |
| Transformer Decoder 与自回归因果结构 | [[习题 - Transformer Decoder 与自回归因果结构]] | [[解答 - Transformer Decoder 与自回归因果结构]] | shift、causal future invariance、KV cache、packing 与服务合同 |
| Encoder–Decoder 与 Cross-Attention | [[习题 - Encoder–Decoder 与 Cross-Attention]] | [[解答 - Encoder–Decoder 与 Cross-Attention]] | source–target 双轴、三套 mask、cross K/V 复用与来源干预 |
| Decoder-Only、Prefix 与架构家族比较 | [[习题 - Decoder-Only、Prefix 与架构家族比较]] | [[解答 - Decoder-Only、Prefix 与架构家族比较]] | relation/QKV/objective/outlet、prefix block、低秩猜想与公平比较 |
| Vision Transformer、Patch Token 与二维结构 | [[习题 - Vision Transformer、Patch Token 与二维结构]] | [[解答 - Vision Transformer、Patch Token 与二维结构]] | patchify、卷积等价范围、二维位置、分辨率与成本缩放 |
| Transformer 形状、参数量与 FLOPs 总账 | [[习题 - Transformer 形状、参数量与 FLOPs 总账]] | [[解答 - Transformer 形状、参数量与 FLOPs 总账]] | 参数/MAC/激活/cache、训练/prefill/decode 与硬件边界 |
| Transformer 表达、稳定性与证据边界 | [[习题 - Transformer 表达、稳定性与证据边界]] | [[解答 - Transformer 表达、稳定性与证据边界]] | 通用逼近、秩坍塌、Pre/Post/DeepNorm 与 I/T/E/H/O |
| 置换对称性与位置编码的必要性 | [[习题 - 置换对称性与位置编码的必要性]] | [[解答 - 置换对称性与位置编码的必要性]] | full-attention 等变证明、pooling 不变、causal 边界与消融 |
| 可学习绝对位置与位置相加合同 | [[习题 - 可学习绝对位置与位置相加合同]] | [[解答 - 可学习绝对位置与位置相加合同]] | shape/norm、padding/packing、resize、cache offset 与越界 |
| Sinusoidal 位置编码、频率与相对位移 | [[习题 - Sinusoidal 位置编码、频率与相对位移]] | [[解答 - Sinusoidal 位置编码、频率与相对位移]] | 频率表、平移旋转、相对内积、周期碰撞与 dtype |
| 相对位置表示、偏置与距离函数 | [[习题 - 相对位置表示、偏置与距离函数]] | [[解答 - 相对位置表示、偏置与距离函数]] | logit/K/V 注入、分桶、ALiBi 与 constant-value 反例 |
| RoPE 的旋转推导、群表示与内积 | [[习题 - RoPE 的旋转推导、群表示与内积]] | [[解答 - RoPE 的旋转推导、群表示与内积]] | 正交表示、相对内积、pairing、norm 与 full/cache 等价 |
| 二维、多轴与多模态位置编码 | [[习题 - 二维、多轴与多模态位置编码]] | [[解答 - 二维、多轴与多模态位置编码]] | 坐标 schema、轴分配、二维位移、resize 与跨模态对齐 |
| 长度外推、位置插值与 RoPE 缩放 | [[习题 - 长度外推、位置插值与 RoPE 缩放]] | [[解答 - 长度外推、位置插值与 RoPE 缩放]] | PI、逐频缩放、ReRoPE 边界、局部基线与 serving 迁移 |
| 位置分辨率、混叠与长度外推评测 | [[习题 - 位置分辨率、混叠与长度外推评测]] | [[解答 - 位置分辨率、混叠与长度外推评测]] | length×position 矩阵、固定目标、混叠、效率与声明门槛 |
| Attention 的二次复杂度、内存与 IO 瓶颈 | [[习题 - Attention 的二次复杂度、内存与 IO 瓶颈]] | [[解答 - Attention 的二次复杂度、内存与 IO 瓶颈]] | train/prefill/decode、MAC/显存/HBM/cache 分账、roofline 与 crossover |
| 局部、分块与稀疏 Attention | [[习题 - 局部、分块与稀疏 Attention]] | [[解答 - 局部、分块与稀疏 Attention]] | relation graph、edge/path/kernel 三证书、causal leakage 与系统稀疏 |
| 低秩投影与序列维压缩 Attention | [[习题 - 低秩投影与序列维压缩 Attention]] | [[解答 - 低秩投影与序列维压缩 Attention]] | sequence-axis shape、谱尾、softmax 误差、因果与长度合同 |
| 核特征、线性 Attention 与结合律重排 | [[习题 - 核特征、线性 Attention 与结合律重排]] | [[解答 - 核特征、线性 Attention 与结合律重排]] | kernel factorization、full/causal state、分母与 mask 结构 |
| Performer、随机特征与近似误差 | [[习题 - Performer、随机特征与近似误差]] | [[解答 - Performer、随机特征与近似误差]] | Gaussian identity、kernel/ratio/output 三层误差与随机性合同 |
| FlashAttention、精确计算与 IO Awareness | [[习题 - FlashAttention、精确计算与 IO Awareness]] | [[解答 - FlashAttention、精确计算与 IO Awareness]] | tiling、online softmax、exact 边界、backward 重算与性能协议 |
| KV Cache、MHA、MQA 与 GQA | [[习题 - KV Cache、MHA、MQA 与 GQA]] | [[解答 - KV Cache、MHA、MQA 与 GQA]] | head mapping、cache payload、full/cache 等价、offset 与 serving 合同 |
| MLA、潜变量缓存与推理成本证据 | [[习题 - MLA、潜变量缓存与推理成本证据]] | [[解答 - MLA、潜变量缓存与推理成本证据]] | feature-axis latent、projection absorption、RoPE 支路与 I/T/E/H/O |
| 条件计算、专家混合与稀疏激活 | [[习题 - 条件计算、专家混合与稀疏激活]] | [[解答 - 条件计算、专家混合与稀疏激活]] | total/active/resident 参数、专家 MAC、条件计算与几何解释边界 |
| Router、Gate、Top-k 与稀疏组合 | [[习题 - Router、Gate、Top-k 与稀疏组合]] | [[解答 - Router、Gate、Top-k 与稀疏组合]] | logits/score/selection/mixing/backward 完整合同与 Top-1 边界 |
| Expert Capacity、Dispatch 与 Token Dropping | [[习题 - Expert Capacity、Dispatch 与 Token Dropping]] | [[解答 - Expert Capacity、Dispatch 与 Token Dropping]] | assignment、capacity、drop/pad/dropless、token/expert choice |
| MoE 负载均衡辅助损失与偏置 | [[习题 - MoE 负载均衡辅助损失与偏置]] | [[解答 - MoE 负载均衡辅助损失与偏置]] | hard/soft 统计、proxy 梯度、均衡粒度与质量—系统张力 |
| Loss-Free 路由、偏置更新与分配视角 | [[习题 - Loss-Free 路由、偏置更新与分配视角]] | [[解答 - Loss-Free 路由、偏置更新与分配视角]] | bias feedback、capacity assignment、dual price、quantile 与漂移 |
| 细粒度专家、共享专家与动态激活 | [[习题 - 细粒度专家、共享专家与动态激活]] | [[解答 - 细粒度专家、共享专家与动态激活]] | shared/fine/dynamic 三轴、matched-budget 与边际计算分配 |
| Expert Parallel、All-to-All 与通信成本 | [[习题 - Expert Parallel、All-to-All 与通信成本]] | [[解答 - Expert Parallel、All-to-All 与通信成本]] | dispatch/combine payload、拓扑、偏斜、重叠与尾延迟 |
| MoE 门控归一化、证据地图与开放问题 | [[习题 - MoE 门控归一化、证据地图与开放问题]] | [[解答 - MoE 门控归一化、证据地图与开放问题]] | Softmax/Sigmoid、Hash 对照、I/T/E/H/O 与开放研究问题 |
| 图数据、节点重标号与置换对称性 | [[习题 - 图数据、节点重标号与置换对称性]] | [[解答 - 图数据、节点重标号与置换对称性]] | 图等价类、$PAP^\top/PX$、节点等变、图级不变、kNN 构图与 hubness |
| 消息传递神经网络的统一形式 | [[习题 - 消息传递神经网络的统一形式]] | [[解答 - 消息传递神经网络的统一形式]] | message–aggregate–update、同步语义、K-hop、GraphSAGE sampling 与复杂度 |
| 谱图卷积、空间图卷积与归一化邻接 | [[习题 - 谱图卷积、空间图卷积与归一化邻接]] | [[解答 - 谱图卷积、空间图卷积与归一化邻接]] | Laplacian、谱滤波、多项式局部性、GCN normalization 与扩散边界 |
| 聚合器、可辨识性与 GIN | [[习题 - 聚合器、可辨识性与 Graph Isomorphism Network]] | [[解答 - 聚合器、可辨识性与 Graph Isomorphism Network]] | multiset collision、injective sum、中心角色与 1-WL 条件 |
| 图网络深度、过平滑与过挤压 | [[习题 - 图网络深度、过平滑与过挤压]] | [[解答 - 图网络深度、过平滑与过挤压]] | 谱趋同、远程瓶颈、机制特异诊断与干预消融 |
| 图注意力与结构偏置 | [[习题 - 图注意力与结构偏置]] | [[解答 - 图注意力与结构偏置]] | masked softmax、score/value、multi-head、解释性与复杂度边界 |
| 图级读出、异构图与任务接口 | [[习题 - 图级读出、异构图与任务接口]] | [[解答 - 图级读出、异构图与任务接口]] | invariant readout、R-GCN、decoder、inverse-edge leakage 与 split |
| WL 表达界、反例与 GNN 证据地图 | [[习题 - WL 表达界、反例与 GNN 证据地图]] | [[解答 - WL 表达界、反例与 GNN 证据地图]] | color refinement、$C_6$ 反例、MPNN 上界、higher-order 成本与证据分层 |
| 人工神经元、仿射变换与决策超平面 | [[习题 - 人工神经元、仿射变换与决策超平面]] | [[解答 - 人工神经元、仿射变换与决策超平面]] | affine/linear、score—activation—probability—decision、超平面法向与距离、局部梯度、尺度与输出合同 |
| 线性层、批量张量与参数计数 | [[习题 - 线性层、批量张量与参数计数]] | [[解答 - 线性层、批量张量与参数计数]] | row-batch shape、broadcast、参数/MAC/显存、rank bottleneck、dense VJP 与工程审计 |
| 感知机模型、更新规则与线性可分性 | [[习题 - 感知机模型、更新规则与线性可分性]] | [[解答 - 感知机模型、更新规则与线性可分性]] | threshold predictor、错误修正、线性可分、margin mistake proof、不可分/漂移/概率边界 |
| 多层感知机与逐层前向计算 | [[习题 - 多层感知机与逐层前向计算]] | [[解答 - 多层感知机与逐层前向计算]] | 函数复合、Z/H shape ledger、affine collapse、参数/MAC/cache、输出任务合同与 FFN 迁移 |
| XOR、隐藏表示与非线性必要性 | [[习题 - XOR、隐藏表示与非线性必要性]] | [[解答 - XOR、隐藏表示与非线性必要性]] | convex-hull 反证、hinge/hat 构造、隐藏空间线性读出与有限点边界 |
| 万能逼近定理、紧集与逼近误差 | [[习题 - 万能逼近定理、紧集与逼近误差]] | [[解答 - 万能逼近定理、紧集与逼近误差]] | domain/target/activation/network/norm 合同、稠密性量词、测度分离证明骨架与效率边界 |
| 深度分离、线性区域与表达效率 | [[习题 - 深度分离、线性区域与表达效率]] | [[解答 - 深度分离、线性区域与表达效率]] | tent-map 复合、breakpoint/region 计数、存在型分离量词与资源账本 |
| 参数对称性、等价表示与可辨识边界 | [[习题 - 参数对称性、等价表示与可辨识边界]] | [[解答 - 参数对称性、等价表示与可辨识边界]] | hidden permutation、ReLU 正缩放、参数轨道/纤维、quotient 与 function-space 比较 |
| 计算图、拓扑序与前向执行 | [[习题 - 计算图、拓扑序与前向执行]] | [[解答 - 计算图、拓扑序与前向执行]] | typed DAG、Kahn 调度、fan-out/共享参数、cache/RNG/state/mutation 与 dynamic control-flow 审计 |
| 局部微分、Jacobian、JVP 与 VJP | [[习题 - 局部微分、Jacobian、JVP 与 VJP]] | [[解答 - 局部微分、Jacobian、JVP 与 VJP]] | derivative/operator 对象、JVP/VJP 形状、dot test、broadcast/reduction 伴随与 mode 选择 |
| 标量链式法则与反向传播递推 | [[习题 - 标量链式法则与反向传播递推]] | [[解答 - 标量链式法则与反向传播递推]] | adjoint seed、逆拓扑动态规划、fan-out 累加、共享参数与 stop-gradient 边界 |
| 线性层与仿射层的反向传播 | [[习题 - 线性层与仿射层的反向传播]] | [[解答 - 线性层与仿射层的反向传播]] | Frobenius 配对、$GW^T/X^TG/\sum G$、outer-product 解释、mean/sum 与 distributed scale |
| 激活、分支、广播与梯度累加 | [[习题 - 激活、分支、广播与梯度累加]] | [[解答 - 激活、分支、广播与梯度累加]] | activation VJP、不可微约定、fan-out 求和、broadcast–sum、gather–scatter-add 与 microbatch scale |
| Softmax–Cross-Entropy 的稳定融合反向 | [[习题 - Softmax–Cross-Entropy 的稳定融合反向]] | [[解答 - Softmax–Cross-Entropy 的稳定融合反向]] | max-shift/LSE、$p-y$ 推导、target mass、temperature、mask/reduction 与 fused-kernel 验收 |
| Forward/Reverse AD、Tape 与复杂度 | [[习题 - Forward_Reverse AD、Tape 与复杂度|习题 - Forward/Reverse AD、Tape 与复杂度]] | [[解答 - Forward_Reverse AD、Tape 与复杂度|解答 - Forward/Reverse AD、Tape 与复杂度]] | dual numbers、Wengert tape、forward/reverse sweep、JVP/VJP mode selection、custom rule 与程序语义 |
| Gradient Checking、Checkpointing 与高阶微分边界 | [[习题 - Gradient Checking、Checkpointing 与高阶微分边界]] | [[解答 - Gradient Checking、Checkpointing 与高阶微分边界]] | 中心差分/Taylor/dot test、重算调度、RNG/state replay、HVP 与 higher-order graph 边界 |
| 激活函数的角色、选择准则与函数性质 | [[习题 - 激活函数的角色、选择准则与函数性质]] | [[解答 - 激活函数的角色、选择准则与函数性质]] | affine collapse、local Jacobian、range/slope/smoothness/moment/cost、output-role 与 matched-budget choice contract |
| Sigmoid、Tanh 与饱和梯度 | [[习题 - Sigmoid、Tanh 与饱和梯度]] | [[解答 - Sigmoid、Tanh 与饱和梯度]] | derivative bounds、指数饱和、均值漂移、temperature、stable log-sigmoid 与 gate/output 边界 |
| ReLU、Leaky ReLU 与次梯度约定 | [[习题 - ReLU、Leaky ReLU 与次梯度约定]] | [[解答 - ReLU、Leaky ReLU 与次梯度约定]] | kink/subgradient/convention、positive homogeneity、piecewise-affine regions、dead units 与 leaky/PReLU moments |
| ELU、SELU 与自归一化接口 | [[习题 - ELU、SELU 与自归一化接口]] | [[解答 - ELU、SELU 与自归一化接口]] | ELU smoothness、SELU moment equations、fixed-point/contraction、alpha dropout 与 architecture boundary |
| Softplus、GELU、SiLU 与平滑门控 | [[习题 - Softplus、GELU、SiLU 与平滑门控]] | [[解答 - Softplus、GELU、SiLU 与平滑门控]] | soft-max/self-gating/convolution 区分、导数与曲率、稳定实现、exact/approximation 合同 |
| GLU、GeGLU、SwiGLU 与乘性门 | [[习题 - GLU、GeGLU、SwiGLU 与乘性门]] | [[解答 - GLU、GeGLU、SwiGLU 与乘性门]] | 双投影、乘性 VJP、二阶交互、三矩阵参数/通信/融合账本与公平消融 |
| Maxout、分段线性区域与条件计算 | [[习题 - Maxout、分段线性区域与条件计算]] | [[解答 - Maxout、分段线性区域与条件计算]] | max-affine convexity、winner regions、tie subdifferential、starvation 与条件计算边界 |
| 激活函数的数值稳定、尺度与经验选择 | [[习题 - 激活函数的数值稳定、尺度与经验选择]] | [[解答 - 激活函数的数值稳定、尺度与经验选择]] | stable primitive、moment/Jacobian 分账、matched-budget 轨道、selection bias 与 bounded claim |
| 方差传播与宽层均值场近似 | [[习题 - 方差传播与宽层均值场近似]] | [[解答 - 方差传播与宽层均值场近似]] | preactivation/activation 二阶矩、交叉项消失条件、Gaussian 宽层近似、moment map 与有限宽边界 |
| Xavier、Glorot 初始化 | [[习题 - Xavier、Glorot 初始化]] | [[解答 - Xavier、Glorot 初始化]] | fan-in/fan-out 双目标、normal/uniform 参数换算、gain、非方层折中与布局审计 |
| Kaiming、He 初始化 | [[习题 - Kaiming、He 初始化]] | [[解答 - Kaiming、He 初始化]] | rectifier 半轴二阶矩、leaky slope gain、卷积 fan、mode 选择与 PReLU 漂移 |
| 反向梯度方差与 Fan-In/Fan-Out 权衡 | [[习题 - 反向梯度方差与 Fan-In_Fan-Out 权衡|习题 - 反向梯度方差与 Fan-In/Fan-Out 权衡]] | [[解答 - 反向梯度方差与 Fan-In_Fan-Out 权衡|解答 - 反向梯度方差与 Fan-In/Fan-Out 权衡]] | forward/backward multiplier、深度乘积、aspect ratio、Jacobian spectrum 与系统尺度边界 |
| 相关传播、Edge of Chaos 与临界初始化 | [[习题 - 相关传播、Edge of Chaos 与临界初始化]] | [[解答 - 相关传播、Edge of Chaos 与临界初始化]] | bivariate Gaussian、correlation map、$\chi_1$、ordered/critical/chaotic、depth scale 与有限宽边界 |
| 正交初始化与 Dynamical Isometry | [[习题 - 正交初始化与 Dynamical Isometry]] | [[解答 - 正交初始化与 Dynamical Isometry]] | square/semi-orthogonal、gain、deep-linear 校准、derivative mask、完整 singular spectrum 与 operator 边界 |
| 偏置、输出层与零初始化的对称性边界 | [[习题 - 偏置、输出层与零初始化的对称性边界]] | [[解答 - 偏置、输出层与零初始化的对称性边界]] | hidden-unit bundle、对称不变子空间、全零 MLP、zero head、residual zero-last 与第一步梯度 |
| LSUV、Fixup 与现代初始化诊断 | [[习题 - LSUV、Fixup 与现代初始化诊断]] | [[解答 - LSUV、Fixup 与现代初始化诊断]] | data-dependent unit variance、depth-aware residual scaling、zero-last、update ratio 与第一处失效定位 |
| 归一化的对象、轴与不变性 | [[习题 - 归一化的对象、轴与不变性]] | [[解答 - 归一化的对象、轴与不变性]] | statistical group、affine sharing、state、epsilon 四元组合同，轴/shape、不变性与 masking 审计 |
| BatchNorm 前向统计与训练—推理差异 | [[习题 - BatchNorm 前向统计与训练—推理差异]] | [[解答 - BatchNorm 前向统计与训练—推理差异]] | biased/unbiased variance、running buffers、train/eval 图差异、卷积归约与 inference folding |
| BatchNorm 反向传播、尺度不变性与噪声 | [[习题 - BatchNorm 反向传播、尺度不变性与噪声]] | [[解答 - BatchNorm 反向传播、尺度不变性与噪声]] | centered/radial projection VJP、dense batch coupling、scale ray、effective angular rate 与相关 batch noise |
| LayerNorm 的逐样本几何与反向传播 | [[习题 - LayerNorm 的逐样本几何与反向传播]] | [[解答 - LayerNorm 的逐样本几何与反向传播]] | per-token plane–sphere geometry、vector gain VJP、Jacobian eigenspaces、低维退化与 normalized-shape 边界 |
| RMSNorm、均值移除与缩放不变性 | [[习题 - RMSNorm、均值移除与缩放不变性]] | [[解答 - RMSNorm、均值移除与缩放不变性]] | RMS 半径、shift/scale 不变性、VJP 与 Jacobian 谱、partial RMS、epsilon 和有限精度 |
| InstanceNorm、GroupNorm 与 WeightNorm | [[习题 - InstanceNorm、GroupNorm 与 WeightNorm]] | [[解答 - InstanceNorm、GroupNorm 与 WeightNorm]] | 统计组轴合同、GN 两个极端、WeightNorm 重参数化梯度、状态与退化边界 |
| Pre-Norm、Post-Norm 与归一化放置 | [[习题 - Pre-Norm、Post-Norm 与归一化放置]] | [[解答 - Pre-Norm、Post-Norm 与归一化放置]] | 精确前向与 Jacobian、恒等 rail、深层乘积、条件性解释和受控比较协议 |
| 小批量、混合精度、分布式与因果归一化边界 | [[习题 - 小批量、混合精度、分布式与因果归一化边界]] | [[解答 - 小批量、混合精度、分布式与因果归一化边界]] | micro/optimizer/statistical batch、Chan 合并、dtype 账本、prefix causality 与部署审计 |
| 残差学习、恒等捷径与退化问题 | [[习题 - 残差学习、恒等捷径与退化问题]] | [[解答 - 残差学习、恒等捷径与退化问题]] | identity/projection shortcut、degradation、函数类嵌入、zero-last、系统成本与浮点吸收 |
| 残差块 Jacobian 与梯度直通 | [[习题 - 残差块 Jacobian 与梯度直通]] | [[解答 - 残差块 Jacobian 与梯度直通]] | JVP/VJP、rail—branch 干涉、singular-value 界、非正规反例与有序 path expansion |
| ResNet 的 ODE 与离散动力系统视角 | [[习题 - ResNet 的 ODE 与离散动力系统视角]] | [[解答 - ResNet 的 ODE 与离散动力系统视角]] | Euler 对应、固定 horizon、local/global error、稳定圆盘、adjoint 与 topology 边界 |
| 残差缩放、Lipschitz 界与深度稳定性 | [[习题 - 残差缩放、Lipschitz 界与深度稳定性]] | [[解答 - 残差缩放、Lipschitz 界与深度稳定性]] | product/exponential bound、one-sided contraction、$1/N$ vs $1/\sqrt N$、forcing 与低精度 |
| Pre-Activation、Pre-Norm 与 Post-Norm 残差 | [[习题 - Pre-Activation、Pre-Norm 与 Post-Norm 残差]] | [[解答 - Pre-Activation、Pre-Norm 与 Post-Norm 残差]] | 统一 placement 合同、四类 Jacobian、局部秩反例、projection、BN train/eval 与公平消融 |
| Highway、Dense Connection 与 Skip 结构比较 | [[习题 - Highway、Dense Connection 与 Skip 结构比较]] | [[解答 - Highway、Dense Connection 与 Skip 结构比较]] | add/gate/concat/long skip、Highway gate 导数、Dense 通道与连接计数、对齐和系统成本 |
| ReZero、Fixup、DeepNorm 与深网缩放 | [[习题 - ReZero、Fixup、DeepNorm 与深网缩放]] | [[解答 - ReZero、Fixup、DeepNorm 与深网缩放]] | state/gradient/update 分账、ReZero/Fixup 首步梯度、DeepNorm 双尺度与混搭边界 |
| 深度、有效路径与稳定性证据地图 | [[习题 - 深度、有效路径与稳定性证据地图]] | [[解答 - 深度、有效路径与稳定性证据地图]] | 六种 depth、ordered paths、binomial toy、gradient correlation、五级证据与六维稳定性 |
| Embedding Lookup、稀疏梯度与参数规模 | [[习题 - Embedding Lookup、稀疏梯度与参数规模]] | [[解答 - Embedding Lookup、稀疏梯度与参数规模]] | selection matrix、scatter-add、frequency scaling、参数/状态/通信与稀疏整链审计 |
| Embedding 几何、相似度与各向异性 | [[习题 - Embedding 几何、相似度与各向异性]] | [[解答 - Embedding 几何、相似度与各向异性]] | dot/cosine/distance、centering、协方差谱、有效秩、重参数化与评估泄漏 |
| 输入—输出权重共享与 Weight Tying | [[习题 - 输入—输出权重共享与 Weight Tying]] | [[解答 - 输入—输出权重共享与 Weight Tying]] | direct/projected tying、参数计数、双路径 VJP、梯度冲突与实现 identity |
| Softmax 输出层、Logit 尺度与概率参数化 | [[习题 - Softmax 输出层、Logit 尺度与概率参数化]] | [[解答 - Softmax 输出层、Logit 尺度与概率参数化]] | simplex interior、shift gauge、温度、梯度/Hessian、稳定 LSE 与校准 |
| Softmax Bottleneck 与低秩限制 | [[习题 - Softmax Bottleneck 与低秩限制]] | [[解答 - Softmax Bottleneck 与低秩限制]] | 双重中心化、跨 context rank bound、有限表充分性、SVD 误差与 MoS 边界 |
| Sampled、Hierarchical 与 Adaptive Softmax | [[习题 - Sampled、Hierarchical 与 Adaptive Softmax]] | [[解答 - Sampled、Hierarchical 与 Adaptive Softmax]] | $\widehat Z$ 与 $\log\widehat Z$、树归一化、adaptive 期望成本、训练—评估—解码合同 |
| Padding、Mask、特殊符号与词表边界 | [[习题 - Padding、Mask、特殊符号与词表边界]] | [[解答 - Padding、Mask、特殊符号与词表边界]] | 四种 mask、teacher-forcing shift、有效分母、all-masked row、packing 与词表事务 |
| Embedding 初始化、缩放、分解与量化接口 | [[习题 - Embedding 初始化、缩放、分解与量化接口]] | [[解答 - Embedding 初始化、缩放、分解与量化接口]] | row/logit 二阶矩、低秩梯度与 gauge、SVD、量化误差、训练状态和 Pareto 验收 |
| Dropout 的随机掩码、期望与 Inverted Scaling | [[习题 - Dropout 的随机掩码、期望与 Inverted Scaling]] | [[解答 - Dropout 的随机掩码、期望与 Inverted Scaling]] | Bernoulli mask、条件矩、inverted scaling、VJP、非线性反例、广播轴与 RNG 合同 |
| Dropout 的方差、共适应解释与 Bayesian 边界 | [[习题 - Dropout 的方差、共适应解释与 Bayesian 边界]] | [[解答 - Dropout 的方差、共适应解释与 Bayesian 边界]] | 随机输入方差、score covariance、精确风险分解、MC 误差、entropy/MI 与证据分级 |
| DropConnect、权重噪声与激活噪声 | [[习题 - DropConnect、权重噪声与激活噪声]] | [[解答 - DropConnect、权重噪声与激活噪声]] | 噪声位置、输出 covariance、VJP、Taylor penalty、local reparameterization 与系统成本 |
| Stochastic Depth、DropPath 与有效深度 | [[习题 - Stochastic Depth、DropPath 与有效深度]] | [[解答 - Stochastic Depth、DropPath 与有效深度]] | 原始/inverted 合同、branch covariance、Poisson-binomial 深度、短路计算、BN 与 RNG 边界 |
| Label Smoothing、置信度与目标偏置 | [[习题 - Label Smoothing、置信度与目标偏置]] | [[解答 - Label Smoothing、置信度与目标偏置]] | inclusive/exclude-true 约定、CE/KL 分解、有限 margin、population bias、校准/抗噪/蒸馏边界 |
| Mixup、Manifold Mixup 与插值正则 | [[习题 - Mixup、Manifold Mixup 与插值正则]] | [[解答 - Mixup、Manifold Mixup 与插值正则]] | Beta moments、vicinal risk、target 线性、hidden VJP、manifold intrusion 与 pairing/state 合同 |
| Jacobian、Gradient Penalty 与 Lipschitz 正则接口 | [[习题 - Jacobian、Gradient Penalty 与 Lipschitz 正则接口]] | [[解答 - Jacobian、Gradient Penalty 与 Lipschitz 正则接口]] | derivative 对象、dual/operator/Frobenius norm、Hutchinson、layer bounds、local—global certificate 缺口 |
| 网络级正则化的交互、消融与证据地图 | [[习题 - 网络级正则化的交互、消融与证据地图]] | [[解答 - 网络级正则化的交互、消融与证据地图]] | 五个干预位置、R-Drop、L2/AdamW、factorial interaction、三类 estimand、六本账与五级证据 |
| 统计学习问题的对象合同 | [[习题 - 统计学习问题的对象合同]] | [[解答 - 统计学习问题的对象合同]] | $\mathcal X/\mathcal Y/\mathcal A/\mathcal Z/P/S/\mathcal H/A/\ell/R$、随机性与量词、监督/自监督/生成/医学系统合同 |
| 数据生成分布与采样假设 | [[习题 - 数据生成分布与采样假设]] | [[解答 - 数据生成分布与采样假设]] | $P^m$、边缘/独立、协方差与有效样本量、augmentation/group/time/batch dependence、反馈日志 |
| 预测器、假设空间与学习算法 | [[习题 - 预测器、假设空间与学习算法]] | [[解答 - 预测器、假设空间与学习算法]] | $\Theta\to\mathcal H$、parameter fiber、proper/improper、tie-breaking、data-dependent class、probe/fine-tune |
| 损失、总体风险与经验风险 | [[习题 - 损失、总体风险与经验风险]] | [[解答 - 损失、总体风险与经验风险]] | conditional/population/empirical/test risk、固定 $h$ 无偏性、memorizer、surrogate/reduction、adaptive test |
| 经验风险最小化、近似 ERM 与超额风险分解 | [[习题 - 经验风险最小化、近似 ERM 与超额风险分解]] | [[解答 - 经验风险最小化、近似 ERM 与超额风险分解]] | Bayes/class/empirical/computed 四对象、approximation—selection—optimization、ERM bridge、regularization 与 AI error budget |
| Bayes 决策、Bayes 预测器与 Bayes 风险 | [[习题 - Bayes 决策、Bayes 预测器与 Bayes 风险]] | [[解答 - Bayes 决策、Bayes 预测器与 Bayes 风险]] | conditional risk、0–1/成本/abstain/平方/绝对/log Bayes action、KL、calibration 与约束决策 |
| 可实现、不可知、相合性与可学习性 | [[习题 - 可实现、不可知、相合性与可学习性]] | [[解答 - 可实现、不可知、相合性与可学习性]] | realizable/agnostic、empirical/statistical consistency、PAC 量词、uniform rate、Bayes consistency 与 computation |
| 训练集、验证集、测试集与自适应复用 | [[习题 - 训练集、验证集、测试集与自适应复用]] | [[解答 - 训练集、验证集、测试集与自适应复用]] | conditional test validity、$\log K$ selection、adaptive reuse、CV/nested CV、leakage 与 benchmark protocol |
| 泛化间隙与浓缩不等式接口 | [[习题 - 泛化间隙与浓缩不等式接口]] | [[解答 - 泛化间隙与浓缩不等式接口]] | fixed-$h$ Hoeffding 推导、置信反解、data-dependent selection、独立测试、无界/依赖边界 |
| PAC 学习定义与样本复杂度 | [[习题 - PAC 学习定义与样本复杂度]] | [[解答 - PAC 学习定义与样本复杂度]] | realizable/agnostic PAC、全量词、accuracy/confidence、随机学习器、统计与计算效率、shift 桥梁 |
| 有限假设类、Union Bound 与一致收敛 | [[习题 - 有限假设类、Union Bound 与一致收敛]] | [[解答 - 有限假设类、Union Bound 与一致收敛]] | simultaneous event、$\log M$、approximate ERM bridge、weighted budgets、adaptive candidate set |
| 可实现情形的一致 ERM 保证 | [[习题 - 可实现情形的一致 ERM 保证]] | [[解答 - 可实现情形的一致 ERM 保证]] | version space、坏假设生存、$1/\varepsilon$ 快率、任意 tie-breaking、噪声与无限类边界 |
| 不可知 PAC、ERM 与双侧一致收敛 | [[习题 - 不可知 PAC、ERM 与双侧一致收敛]] | [[解答 - 不可知 PAC、ERM 与双侧一致收敛]] | $2\alpha+\rho$、pairwise difference、$1/\varepsilon^2$、surrogate/unbounded loss 与 adaptive candidates |
| Occam 界、编码长度与先验权重 | [[习题 - Occam 界、编码长度与先验权重]] | [[解答 - Occam 界、编码长度与先验权重]] | weighted union、Kraft、prefix-free code、realizable Occam、MDL oracle 与 compression ledger |
| No-Free-Lunch 与归纳偏置 | [[习题 - No-Free-Lunch 与归纳偏置]] | [[解答 - No-Free-Lunch 与归纳偏置]] | $2m$ 点构造、$1/4\to1/7$、全函数类不可学习、量词换序与五类 AI inductive bias |
| 样本复杂度下界与 Minimax 视角 | [[习题 - 样本复杂度下界与 Minimax 视角]] | [[解答 - 样本复杂度下界与 Minimax 视角]] | Le Cam、Fano、Assouad、KL/TV testing reduction、realizable/agnostic lower rates 与 rare safety |
| 集合、元素与集合运算 | [[习题 - 集合、元素与集合运算]] | [[解答 - 集合、元素与集合运算]] | membership/subset/power-set层级、运算与De Morgan、cover/partition、product/mask、container contract、数据切分与模型类审计 |
| 命题、量词与逻辑等价 | [[习题 - 命题、量词与逻辑等价]] | [[解答 - 命题、量词与逻辑等价]] | proposition/predicate、truth table、implication/equivalence、scope/negation/order、pointwise/uniform与AI theorem contract |
| 必要条件、充分条件与证明方法 | [[习题 - 必要条件、充分条件与证明方法]] | [[解答 - 必要条件、充分条件与证明方法]] | condition inclusion、proof obligations、direct/cases/contrapositive/contradiction、existence/uniqueness、counterexample与AI theorem audit |
| 函数、映射、关系与等价类 | [[习题 - 函数、映射、关系与等价类]] | [[解答 - 函数、映射、关系与等价类]] | function contract、image/preimage、composition/inverse、relation properties、partition/quotient、well-definedness与AI mapping audit |
| 数学归纳、递归与组合计数 | [[习题 - 数学归纳、递归与组合计数]] | [[解答 - 数学归纳、递归与组合计数]] | ordinary/strong/structural induction、recursion/termination、recurrences/invariants、permutation/combination、容斥、鸽巢与AI search-tree audit |
| 基本不等式与界的构造 | [[习题 - 基本不等式与界的构造]] | [[解答 - 基本不等式与界的构造]] | direction/domain/quantifier、triangle/Young/Cauchy、Hölder–Minkowski、Jensen、norm conversion、slack ledger、LSE与AI bound audit |
| 数列、极限与完备性的直觉 | [[习题 - 数列、极限与完备性的直觉]] | [[解答 - 数列、极限与完备性的直觉]] | $\varepsilon$–$N$、algebra/order、monotone/Cauchy/completeness、subsequence/limsup、series/Cesàro、pointwise/uniform、contraction、AI convergence与binary64停滞 |
| 渐近记号、增长率与复杂度 | [[习题 - 渐近记号、增长率与复杂度]] | [[解答 - 渐近记号、增长率与复杂度]] | $O/\Omega/\Theta/o/\omega/\sim$量词、增长层级、有限交叉、多变量制度、RAM/bit与资源账、递推/Master、accuracy/sample、Attention与Scaling Law审计 |
| 向量空间 | [[习题 - 向量空间]] | [[解答 - 向量空间]] | 八条公理、数域、基与维数、仿射/约束边界、浮点实现、概率/LoRA/梯度类型 |
| 基与坐标 | [[习题 - 基与坐标]] | [[解答 - 基与坐标]] | 坐标同构、主动/被动变换、向量/协向量/算子换基、病态基与表示 gauge |
| 线性映射 | [[习题 - 线性映射]] | [[解答 - 线性映射]] | 基的像、映射空间、核/像、第一同构、仿射/局部线性、Attention/卷积/Jacobian |
| 四个基本子空间 | [[习题 - 四个基本子空间]] | [[解答 - 四个基本子空间]] | 输入/输出正交分解、限制同构、投影、RREF/QR/SVD、可辨识性与回归残差 |
| 内积空间 | [[习题 - 内积空间]] | [[解答 - 内积空间]] | 复内积约定、Cauchy–Schwarz、Gram/Parseval、病态坐标、Attention/度量梯度/cosine 边界 |
| 正交投影 | [[习题 - 正交投影]] | [[解答 - 正交投影]] | 正交分解、算子刻画、最近点、斜/加权投影、action 成本、PCA/切空间/LoRA 边界 |
| 最小二乘 | [[习题 - 最小二乘]] | [[解答 - 最小二乘]] | 残差正交、解集与最小范数、QR/SVD、条件数平方、加权/Ridge、probe/Gauss–Newton |
| 特征分解 | [[习题 - 特征分解]] | [[解答 - 特征分解]] | 特征对手算、可对角化、矩阵幂、Jordan/病态基、RNN/Hessian/Attention 谱边界 |
| 有限维谱定理 | [[习题 - 有限维谱定理]] | [[解答 - 有限维谱定理]] | 正规/自伴、正交补归纳、Schur 证明、谱投影/函数、白化与曲率 |
| 奇异值分解 | [[习题 - 奇异值分解]] | [[解答 - 奇异值分解]] | 三种形状、存在性、四子空间、范数/条件数、数值秩、PCA/压缩/谱归一化 |
| Moore–Penrose 伪逆 | [[习题 - Moore-Penrose 伪逆]] | [[解答 - Moore-Penrose 伪逆]] | Penrose 唯一性、双投影、LS 解集、TSVD/Ridge、跨秩与模型编辑边界 |
| Eckart–Young–Mirsky | [[习题 - Eckart–Young–Mirsky]] | [[解答 - Eckart–Young–Mirsky]] | 谱/Frobenius 双证明、唯一性、加权反例、随机 SVD 验收、PCA/LoRA 边界 |
| 矩阵范数 | [[习题 - 矩阵范数]] | [[解答 - 矩阵范数]] | 诱导范数、行列和、Schatten 家族、秩界、谱—核对偶、估计器与优化几何 |
| 条件数 | [[习题 - 条件数]] | [[解答 - 条件数]] | 一般问题导数、线性系统扰动、奇异距离、残差/后向/前向误差、估计与 AI 隐式层 |
| 矩阵扰动 | [[习题 - 矩阵扰动]] | [[解答 - 矩阵扰动]] | Weyl、方向导数、主角度、gap、Bauer–Fike、结构化扰动与 PCA/SVD 迁移 |
| 有效秩 | [[习题 - 有效秩]] | [[解答 - 有效秩]] | 重构秩、stable/entropy/PR、$\sigma$ 与 $\sigma^2$ 归一化、估计偏差与表示诊断 |
| 子空间、张成与线性无关 | [[习题 - 子空间、张成与线性无关]] | [[解答 - 子空间、张成与线性无关]] | 封闭性、span 最小性、表示唯一性、交换引理、近线性相关与 LoRA 字典 |
| 核、像与秩零化度 | [[习题 - 核、像与秩零化度定理]] | [[解答 - 核、像与秩零化度定理]] | 核/像、单射满射、秩—零化度证明、第一同构、Jacobian 与线性层瓶颈 |
| 直和、商空间与不变子空间 | [[习题 - 直和、商空间与不变子空间]] | [[解答 - 直和、商空间与不变子空间]] | 唯一分解、商空间良定义、幂等投影、分块三角化、nuisance 与状态子空间 |
| Rayleigh 商与极值表征 | [[习题 - Rayleigh 商与极值表征]] | [[解答 - Rayleigh 商与极值表征]] | 谱加权平均、Courant–Fischer、Ritz、Ky Fan、广义商、PCA/Hessian 与非 Hermitian 边界 |
| 特征向量与子空间扰动 | [[习题 - 特征向量与子空间扰动定理]] | [[解答 - 特征向量与子空间扰动定理]] | 主角度、投影距离、单向量 sinθ、Davis–Kahan/Wedin、无信息界、PCA/Hessian/LoRA |
| Kronecker、vec 与矩阵方程 | [[习题 - Kronecker 积、向量化与矩阵方程]] | [[解答 - Kronecker 积、向量化与矩阵方程]] | 四类乘积、列/行 vec、Kronecker 恒等式、Sylvester 唯一性与 separation、K-FAC、隐式 Jacobian |
| 多线性映射、张量与缩并 | [[习题 - 多线性映射、张量与缩并]] | [[解答 - 多线性映射、张量与缩并]] | 通用性质、order/shape/rank、自由/求和指标、mode-$n$、Attention、卷积、JVP/VJP 与 CP 层 |
| Gram–Schmidt | [[习题 - 标准正交基与 Gram-Schmidt]] | [[解答 - 标准正交基与 Gram-Schmidt]] | 投影消去、张成空间、依赖边界、LoRA 重参数化 |
| QR | [[习题 - QR 分解]] | [[解答 - QR 分解]] | 形状、手算、Gram 矩阵、秩亏、算法选择 |
| 正定矩阵 | [[习题 - 二次型与正定矩阵]] | [[解答 - 二次型与正定矩阵]] | 分类、配方、Gram 证明、反例、协方差白化 |
| Cholesky | [[习题 - Cholesky 分解]] | [[解答 - Cholesky 分解]] | 适用条件、三角求解、log-det、奇异边界、高斯模型 |
| 消元与 LU | [[习题 - 线性方程组、消元与 LU 分解]] | [[解答 - 线性方程组、消元与 LU 分解]] | 形状与可解性、完整手算、唯一性、pivot 反例、隐式微分 |
| trace 与 determinant | [[习题 - 迹、行列式与体积]] | [[解答 - 迹、行列式与体积]] | 不变性、体积/方向、乘法性证明、条件数反例、flow 与 trace estimator |
| 对偶空间 | [[习题 - 线性泛函与对偶空间]] | [[解答 - 线性泛函与对偶空间]] | 对偶基、逆转置换基、对偶映射、annihilator、微分与度量梯度 |
| 伴随算子 | [[习题 - 伴随算子]] | [[解答 - 伴随算子]] | 矩形伴随、加权内积、核/值域证明、转置非逆、线性层 VJP |
| 特征多项式与重数 | [[习题 - 特征多项式与重数]] | [[解答 - 特征多项式与重数]] | polynomial/特征空间分工、重数不等式、分裂条件、Cayley–Hamilton、状态传播 |
| 广义特征向量与 Jordan 结构 | [[习题 - 广义特征向量与 Jordan 结构]] | [[解答 - 广义特征向量与 Jordan 结构]] | 核空间增长、链与块恢复、最小多项式、矩阵幂/指数、近缺陷状态与梯度 |
| Schur 分解 | [[习题 - Schur 分解]] | [[解答 - Schur 分解]] | 复/实三角化、不变旗标、正规特例、QR 相似迭代、残差、稳定子空间与非正规瞬态 |
| 矩阵函数与矩阵指数 | [[习题 - 矩阵函数与矩阵指数]] | [[解答 - 矩阵函数与矩阵指数]] | 三种定义、指数与 ODE、精确离散化、缩放平方/action、Fréchet 导数、SSM 迁移 |
| 矩阵函数的 Fréchet 导数 | [[习题 - 矩阵函数的 Fréchet 导数]] | [[解答 - 矩阵函数的 Fréchet 导数]] | 算子定义、块公式、除差/重复谱、exp/sqrt、Kronecker 条件数、伴随 VJP、SSM 与白化 |
| 非正规矩阵、预解式与伪谱 | [[习题 - 非正规矩阵、预解式与伪谱]] | [[解答 - 非正规矩阵、预解式与伪谱]] | 正规性、左右特征向量、resolvent、伪谱四定义、瞬态下界、坐标/结构边界、SSM/RNN 诊断 |
| 结构化矩阵与结构化扰动 | [[习题 - 结构化矩阵与结构化扰动]] | [[解答 - 结构化矩阵与结构化扰动]] | 结构分类、基/Gram 投影、SPD/Stiefel/固定秩切空间、结构化条件数、后向误差、伪谱、LoRA/卷积/SSM |
| 函数极限、连续性与收敛模式 | [[习题 - 函数极限、连续性与收敛模式]] | [[解答 - 函数极限、连续性与收敛模式]] | ε–N/ε–δ 量词、逐点/一致/$L^p$、极限交换、a.s./概率/$L^p$/分布收敛、经验风险与小批量梯度 |
| 一元导数与中值定理 | [[习题 - 一元导数与中值定理]] | [[解答 - 一元导数与中值定理]] | 差商与局部线性、可微边界、Fermat/Rolle/Lagrange/Cauchy/Darboux、Lipschitz、有限差分与 ReLU |
| Taylor 展开与余项 | [[习题 - Taylor 展开与余项]] | [[解答 - Taylor 展开与余项]] | Taylor 唯一性、Peano/Lagrange/积分余项、解析性反例、误差预算、下降引理、有限差分、噪声与 logsumexp |
| 多元函数、偏导数与方向导数 | [[习题 - 多元函数、偏导数与方向导数]] | [[解答 - 多元函数、偏导数与方向导数]] | 多元极限与路径、偏导/方向导数/全微分层级、连续偏导、混合偏导、JVP、约束方向与随机方向检查 |
| 全微分与 Fréchet 导数 | [[习题 - 全微分与 Fréchet 导数]] | [[解答 - 全微分与 Fréchet 导数]] | 有界线性导数、统一小 o 余项、唯一性与连续性、Gâteaux/Hadamard/Fréchet、双线性与矩阵乘法、JVP、局部条件数与程序审计 |
| 梯度、方向导数与最陡方向 | [[习题 - 梯度、方向导数与最陡方向]] | [[解答 - 梯度、方向导数与最陡方向]] | 微分/梯度类型、Riesz、加权度量、对偶范数、$\ell_p$ 与矩阵最陡方向、坐标变换、SignSGD/FGSM/Muon 审计 |
| Jacobian、JVP 与 VJP | [[习题 - Jacobian、JVP 与 VJP]] | [[解答 - Jacobian、JVP 与 VJP]] | 导数算子与坐标表、JVP/VJP 类型、对偶/伴随、列/行成本、batch/广播、矩阵自由作用、差分与伴随测试 |
| Hessian、二阶微分与曲率 | [[习题 - Hessian、二阶微分与曲率]] | [[解答 - Hessian、二阶微分与曲率]] | 二阶双线性型、Taylor 曲率、谱与凸性、HVP、重参数化、GN/GGN/Fisher、矩阵自由谱与 AI 曲率审计 |
| 多元链式法则与计算图 | [[习题 - 多元链式法则与计算图]] | [[解答 - 多元链式法则与计算图]] | Fréchet 链式法则、JVP/VJP 累积、分支/广播/共享参数、二阶复合、Attention/RNN 图审计 |
| 矩阵微分、迹技巧与布局约定 | [[习题 - 矩阵微分、迹技巧与布局约定]] | [[解答 - 矩阵微分、迹技巧与布局约定]] | Frobenius 配对、迹技巧、双侧最小二乘、二次迹、JVP/VJP、vec 布局、结构化变量与验证 |
| 逆矩阵、线性求解与隐式微分 | [[习题 - 逆矩阵、线性求解与隐式微分]] | [[解答 - 逆矩阵、线性求解与隐式微分]] | solve/inverse JVP/VJP、一般隐式伴随、固定点、优化/KKT、残差/条件与矩阵自由实现 |
| 行列式、log-det 与迹的导数 | [[习题 - 行列式、log-det 与迹的导数]] | [[解答 - 行列式、log-det 与迹的导数]] | adjugate/Jacobi、奇异边界、稳定 logdet、Gaussian、flow、低秩更新与随机迹估计 |
| 特征值、特征向量与 SVD 的导数 | [[习题 - 特征值、特征向量与 SVD 的导数]] | [[解答 - 特征值、特征向量与 SVD 的导数]] | 简单/重复/非正规谱、谱投影、SVD 旋转、次梯度、PCA/白化/谱归一化审计 |
| 逆函数定理与隐函数定理 | [[习题 - 逆函数定理与隐函数定理]] | [[解答 - 逆函数定理与隐函数定理]] | 局部逆、压缩证明、隐函数块构造、水平集、条件性、flow/DEQ/KKT 边界 |
| 多重积分、换元公式与积分变换 | [[习题 - 多重积分、换元公式与积分变换]] | [[解答 - 多重积分、换元公式与积分变换]] | Riemann/Fubini/Tonelli、坐标换元、Gaussian、密度推前、flow、重参数化与维数边界 |
| 自动微分：前向、反向与高阶模式 | [[习题 - 自动微分：前向、反向与高阶模式]] | [[解答 - 自动微分：前向、反向与高阶模式]] | symbolic/差分/AD、双数、JVP/VJP、模式成本、HVP、checkpoint、程序语义、自定义与隐式梯度、四层验证 |
| 样本空间、事件与概率公理 | [[习题 - 样本空间、事件与概率公理]] | [[解答 - 样本空间、事件与概率公理]] | 概率三元组、$\sigma$-代数、公理推论、事件列连续性、零概率、支持集与 AI 选择机制 |
| 条件概率、全概率与 Bayes 公式 | [[习题 - 条件概率、全概率与 Bayes 公式]] | [[解答 - 条件概率、全概率与 Bayes 公式]] | 条件化、乘法/链式、全概率、Bayes/odds、base rate、零概率条件、label shift 与潜变量后验 |
| 随机变量、分布与分位数 | [[习题 - 随机变量、分布与分位数]] | [[解答 - 随机变量、分布与分位数]] | 可测映射、推前分布、PMF/PDF/CDF、混合分布、广义分位数、逆变换与生成模型 |
| 联合分布、边缘分布与独立性 | [[习题 - 联合分布、边缘分布与独立性]] | [[解答 - 联合分布、边缘分布与独立性]] | joint/marginal/conditional、support、coupling、pairwise/mutual/conditional independence、autoregressive 与对比采样 |
| 期望、方差与矩 | [[习题 - 期望、方差与矩]] | [[解答 - 期望、方差与矩]] | 可积性、LOTUS、指标变量、矩与方差、重尾边界、Welford、Attention/dropout/mini-batch 尺度 |
| 协方差、相关性与条件期望 | [[习题 - 协方差、相关性与条件期望]] | [[解答 - 协方差、相关性与条件期望]] | covariance/相关、PSD 矩阵、tower/total variance、$L^2$ 投影、denoising/score 与高维估计 |
| 常用离散分布 | [[习题 - 常用离散分布]] | [[解答 - 常用离散分布]] | 生成机制、支持集、组合 PMF、PGF、Poisson 极限、无放回、过度离散与离散梯度 |
| 常用连续分布与指数族 | [[习题 - 常用连续分布与指数族]] | [[解答 - 常用连续分布与指数族]] | density/CDF/hazard、Gamma/Beta、自然参数、log-partition、likelihood 与重参数边界 |
| 多元高斯分布 | [[习题 - 多元高斯分布]] | [[解答 - 多元高斯分布]] | 投影定义、椭球、边缘/条件、Schur 补、退化支撑、Cholesky 与 AI Gaussian 接口 |
| 随机变量变换与密度换元 | [[习题 - 随机变量变换与密度换元]] | [[解答 - 随机变量变换与密度换元]] | 推前、原像分支、CDF/Jacobian、卷积、奇异支撑、VAE 重参数与 flow logdet |
| 随机变量的收敛与大数定律 | [[习题 - 随机变量的收敛与大数定律]] | [[解答 - 随机变量的收敛与大数定律]] | 四种收敛、蕴含/反例、WLLN/SLLN、UI、相关平均与点态/一致 LLN |
| 中心极限定理与 Delta 方法 | [[习题 - 中心极限定理与 Delta 方法]] | [[解答 - 中心极限定理与 Delta 方法]] | 标准化、CLT/Berry–Esseen、多元/二阶 Delta、重尾与 AI Gaussian-noise 审计 |
| 浓缩不等式 | [[习题 - 浓缩不等式]] | [[解答 - 浓缩不等式]] | Markov/Chernoff/Hoeffding/Bernstein、union/McDiarmid、MoM、样本复杂度与选择/序贯/高维审计 |
| Monte Carlo、重要性采样与方差缩减 | [[习题 - Monte Carlo、重要性采样与方差缩减]] | [[解答 - Monte Carlo、重要性采样与方差缩减]] | MCSE、IS/SNIS、support/无限方差、ESS/log-weight、control/stratification/Rao–Blackwell 与 AI 迁移 |
| 统计模型、估计量与偏差方差 | [[习题 - 统计模型、估计量与偏差方差]] | [[解答 - 统计模型、估计量与偏差方差]] | model/estimand/estimator 分层、bias–variance–MSE、consistency、argmin、不可辨识、选择偏差与随机性分量 |
| 最大似然估计与 MAP | [[习题 - 最大似然估计与 MAP]] | [[解答 - 最大似然估计与 MAP]] | likelihood/MLE/MAP、KL projection、边界/support、separation/mixture、正则尺度、条件 cross-entropy 与 EBM |
| Fisher 信息、Cramér–Rao 界与渐近正态性 | [[习题 - Fisher 信息、Cramér–Rao 界与渐近正态性]] | [[解答 - Fisher 信息、Cramér–Rao 界与渐近正态性]] | score/Fisher/CRLB、MLE 渐近证明、sandwich、非正则速率、softmax Fisher 与 uncertainty 审计 |
| Bayesian 推断与后验预测 | [[习题 - Bayesian 推断与后验预测]] | [[解答 - Bayesian 推断与后验预测]] | joint/evidence/posterior、共轭更新、Bayes action、credible/predictive、PPC/SBC、hierarchy 与 VAE/BNN 边界 |
| 假设检验、置信区间与多重比较 | [[习题 - 假设检验、置信区间与多重比较]] | [[解答 - 假设检验、置信区间与多重比较]] | level/power/p-value、NP、区间反演、equivalence、Bonferroni/Holm/BH、optional stopping 与 AI evaluation |
| MCMC 与随机模拟诊断 | [[习题 - MCMC 与随机模拟诊断]] | [[解答 - MCMC 与随机模拟诊断]] | invariance/MH/Gibbs、IACT/ESS/MCSE、R-hat、HMC divergence、multimodality、离散文本 proposal |
| 自信息、熵与编码长度 | [[习题 - 自信息、熵与编码长度]] | [[解答 - 自信息、熵与编码长度]] | 对数自信息、bits/nats、entropy bounds、Kraft/码长上下界、PPL、differential entropy 与 tokenizer 审计 |
| 联合熵、条件熵与链式法则 | [[习题 - 联合熵、条件熵与链式法则]] | [[解答 - 联合熵、条件熵与链式法则]] | joint/conditional entropy、chain rule、conditioning、XOR/BSC、序列 mask/EOS/reduction 与 uncertainty decomposition |
| 交叉熵与 KL 散度 | [[习题 - 交叉熵与 KL 散度]] | [[解答 - 交叉熵与 KL 散度]] | cross-entropy/KL decomposition、Gibbs、支撑/方向、Gaussian KL、logits 稳定式、蒸馏与 surrogate 审计 |
| 互信息与依赖性 | [[习题 - 互信息与依赖性]] | [[解答 - 互信息与依赖性]] | joint/product KL、PMI/MI、conditional/Gaussian MI、非线性依赖、plug-in/InfoNCE 与 uncertainty 审计 |
| 数据处理不等式与充分统计量 | [[习题 - 数据处理不等式与充分统计量]] | [[解答 - 数据处理不等式与充分统计量]] | Markov/DPI、等号、factorization、Fano、task sufficiency、增强/skip/privacy 边界 |
| 无损编码、典型集与渐近等分性 | [[习题 - 无损编码、典型集与渐近等分性]] | [[解答 - 无损编码、典型集与渐近等分性]] | Kraft–McMillan、Huffman、AEP/典型集、source coding converse、entropy rate 与 LM 压缩审计 |
| 最大熵原理与指数族 | [[习题 - 最大熵原理与指数族]] | [[解答 - 最大熵原理与指数族]] | MaxEnt primal/dual、指数形式、配分函数、边界解、连续最大熵、moment matching、softmax 与 EBM 审计 |
| 变分推断、ELBO 与证据分解 | [[习题 - 变分推断、ELBO 与证据分解]] | [[解答 - 变分推断、ELBO 与证据分解]] | evidence identity、reverse KL、mean-field、VAE、gradient estimator、gap 分解、collapse、IWAE 与 evaluation |
| f-散度、Bregman 散度与概率度量 | [[习题 - f-散度、Bregman 散度与概率度量]] | [[解答 - f-散度、Bregman 散度与概率度量]] | $f$-divergence/DPI、Fenchel、Bregman、IPM、TV、Wasserstein、MMD、拓扑与 GAN 选择 |
| 率失真、信息瓶颈与最小描述长度 | [[习题 - 率失真、信息瓶颈与最小描述长度]] | [[解答 - 率失真、信息瓶颈与最小描述长度]] | $R(D)$、coding theorem、Bernoulli/Gaussian、Blahut–Arimoto、IB/VIB、bits-back、two-part/NML/prequential MDL |
| 优化问题、可行域与局部最优 | [[习题 - 优化问题、可行域与局部最优]] | [[解答 - 优化问题、可行域与局部最优]] | 变量/数据/超参数、domain、可行性、inf/min/argmin、局部/全局/驻点、存在性、松弛与 AI 问题合同 |
| 凸集、凸组合与分离超平面 | [[习题 - 凸集、凸组合与分离超平面]] | [[解答 - 凸集、凸组合与分离超平面]] | 凸组合/凸包/锥、相对内部、投影、变分不等式、分离强度、支撑超平面与约束几何 |
| 凸函数、Jensen 不等式与上图集 | [[习题 - 凸函数、Jensen 不等式与上图集]] | [[解答 - 凸函数、Jensen 不等式与上图集]] | epigraph、sublevel、Jensen、一阶/二阶判据、保凸运算、perspective、logsumexp 与参数空间边界 |
| 次梯度、共轭函数与 Fenchel 对偶 | [[习题 - 次梯度、共轭函数与 Fenchel 对偶]] | [[解答 - 次梯度、共轭函数与 Fenchel 对偶]] | 次微分几何/calculus、Fermat、directional derivative、共轭表、Fenchel–Young、biconjugate、dual template 与 critic gap |
| 光滑性、强凸性与条件数 | [[习题 - 光滑性、强凸性与条件数]] | [[解答 - 光滑性、强凸性与条件数]] | 三类 Lipschitz、descent lemma、strong/strict/PL、cocoercivity、gap–distance–gradient、quadratic/logistic/LSE 曲率 |
| 一阶最优性条件与梯度下降 | [[习题 - 一阶最优性条件与梯度下降]] | [[解答 - 一阶最优性条件与梯度下降]] | variational inequality、finite-step descent、nonconvex stationarity、convex/strong-convex rate、谱稳定、line search 与停止 |
| 加速梯度、动量与下界 | [[习题 - 加速梯度、动量与下界]] | [[解答 - 加速梯度、动量与下界]] | HB roots/Jury、quadratic 参数、NAG potential、$O(1/k^2)$、oracle lower bound、restart 与实现约定 |
| 随机梯度与小批量估计 | [[习题 - 随机梯度与小批量估计]] | [[解答 - 随机梯度与小批量估计]] | conditional oracle、batch variance、convex/nonconvex rate、noise floor、accumulation/DDP 与 scaling 审计 |
| 自适应优化方法 | [[习题 - 自适应优化方法]] | [[解答 - 自适应优化方法]] | variable metric、AdaGrad regret、RMSProp/Adam/AMSGrad、AdamW/L2、Hessian heuristic 与数值实现 |
| Newton、Gauss-Newton 与拟 Newton | [[习题 - Newton 法、Gauss-Newton 与拟 Newton 法]] | [[解答 - Newton 法、Gauss-Newton 与拟 Newton 法]] | 二次模型、局部二次收敛、globalization、inexact Newton–CG、GN/LM、BFGS/L-BFGS 与曲率审计 |
| 投影、约束与可行方向 | [[习题 - 投影、约束与可行方向]] | [[解答 - 投影、约束与可行方向]] | tangent/normal/linearized cone、projection 定理、simplex/PSD、gradient mapping、PGD 与 adversarial audit |
| Lagrange 乘子与 KKT | [[习题 - Lagrange 乘子与 KKT 条件]] | [[解答 - Lagrange 乘子与 KKT 条件]] | KKT 四证书、LICQ/MFCQ/Slater、CQ 反例、critical cone、KKT system、SVM/MaxEnt 与 noisy constraints |
| 弱对偶、强对偶与 Slater | [[习题 - 弱对偶、强对偶与 Slater 条件]] | [[解答 - 弱对偶、强对偶与 Slater 条件]] | lower bound/gap、value 与 attainment、relative-interior Slater、Fenchel/Lasso dual、Max-Cut gap、inexact certificate 与 AI relaxation |
| 近端算子、复合优化与稀疏正则 | [[习题 - 近端算子、复合优化与稀疏正则]] | [[解答 - 近端算子、复合优化与稀疏正则]] | prox/resolvent、Moreau、soft/group/SVT、ISTA/FISTA、gradient mapping、splitting、inexact/nonconvex 边界与部署稀疏 |
| 镜像下降、Bregman 几何与自然梯度 | [[习题 - 镜像下降、Bregman 几何与自然梯度]] | [[解答 - 镜像下降、Bregman 几何与自然梯度]] | Bregman/three-point/regret、entropy update、Fisher trust region、invariance、exact/empirical Fisher/GGN、damping/K-FAC/Muon |
| 非凸优化、鞍点与深度网络损失地形 | [[习题 - 非凸优化、鞍点与深度网络损失地形]] | [[解答 - 非凸优化、鞍点与深度网络损失地形]] | FOSP/SOSP、strict/degenerate saddle、stable-manifold/perturb escape、negative curvature、nonconvex PL、benign landscape、symmetry/sharpness 与研究合同 |
| 常微分方程、初值问题与解的存在唯一性 | [[习题 - 常微分方程、初值问题与解的存在唯一性]] | [[解答 - 常微分方程、初值问题与解的存在唯一性]] | IVP/最大解、Picard–Lindelöf、Gronwall、nonuniqueness/blow-up、continuation、Neural ODE 与 solver 分层 |
| 线性 ODE 与矩阵指数 | [[习题 - 线性 ODE 与矩阵指数]] | [[解答 - 线性 ODE 与矩阵指数]] | fundamental matrix、Peano–Baker、谱/Jordan/非正规瞬态、输入卷积、ZOH 采样、aliasing 与 SSM 审计 |
| 相图、平衡点与局部稳定性 | [[习题 - 相图、平衡点与局部稳定性]] | [[解答 - 相图、平衡点与局部稳定性]] | 四级稳定量词、phase line/nullclines、trace–det 分类、双曲线性化、非双曲反例、gradient flow/game/DEQ 审计 |
| Lyapunov 稳定性与能量函数 | [[习题 - Lyapunov 稳定性与能量函数]] | [[解答 - Lyapunov 稳定性与能量函数]] | 定号/proper、direct method、sublevel/ROA、LaSalle、Lyapunov 方程、指数界、连续/离散/神经证书审计 |
| Euler、Runge-Kutta 与离散化误差 | [[习题 - Euler、Runge-Kutta 与离散化误差]] | [[解答 - Euler、Runge-Kutta 与离散化误差]] | exact/grid/dense对象、local/global error、Euler/RK阶条件、adaptivity、stability、event、continuous/discrete adjoint 与 finite-NFE 生成审计 |
| 刚性系统、绝对稳定域与隐式方法 | [[习题 - 刚性系统、绝对稳定域与隐式方法]] | [[解答 - 刚性系统、绝对稳定域与隐式方法]] | stiffness/time scale、A/L-stability、$\theta$-method、Dahlquist/BDF/Radau、Newton–Krylov、代数残差、implicit gradient与stiff Neural/diffusion ODE审计 |
| 流映射、Liouville 公式与连续正规化流 | [[习题 - 流映射、Liouville 公式与连续正规化流]] | [[解答 - 流映射、Liouville 公式与连续正规化流]] | two-parameter flow、全局逆边界、变分方程、Liouville、CNF、Hutchinson方差、数值折叠、support/topology与likelihood审计 |
| 连续性方程与守恒律 | [[习题 - 连续性方程与守恒律]] | [[解答 - 连续性方程与守恒律]] | 控制体、通量/源项、continuity与passive transport、特征线、弱形式、renormalization、shock/entropy、有限体积、Flow Matching与dynamic OT |
| 随机过程、Brownian 运动与二次变差 | [[习题 - 随机过程、Brownian 运动与二次变差]] | [[解答 - 随机过程、Brownian 运动与二次变差]] | FDD/path law、filtration、Brownian covariance/bridge/scaling、Donsker边界、Hölder/variation、quadratic/cross variation、white noise与diffusion coupling审计 |
| Itô 引理与随机微分方程 | [[习题 - Itô 引理与随机微分方程]] | [[解答 - Itô 引理与随机微分方程]] | simple adapted integral、isometry、Itô formula、strong/weak solution、GBM/OU、Itô/Stratonovich、EM/Milstein、强弱误差与neural-SDE梯度审计 |
| Fokker-Planck 方程与概率流 ODE | [[习题 - Fokker-Planck 方程与概率流 ODE]] | [[解答 - Fokker-Planck 方程与概率流 ODE]] | generator/adjoint、weak FPE、probability current、边界与stationary law、Langevin/Gibbs、state-dependent correction、同边缘/异路径、score/solver误差审计 |
| 时间反演、score 与扩散生成动力学 | [[习题 - 时间反演、score 与扩散生成动力学]] | [[解答 - 时间反演、score 与扩散生成动力学]] | 反向时钟与current、state-dependent reverse drift、VP/VE、score matching/DSM/Tweedie、四参数化、DDPM posterior/ELBO、DDIM/guidance与采样误差账本 |
| 度量空间、拓扑与连续映射 | [[习题 - 度量空间、拓扑与连续映射]] | [[解答 - 度量空间、拓扑与连续映射]] | metric/pseudometric/divergence、open/closure/sequence、completeness/compactness、homeomorphism、covering/packing、flow topology、finite-sample与概率度量审计 |
| 光滑流形、切空间与余切空间 | [[习题 - 光滑流形、切空间与余切空间]] | [[解答 - 光滑流形、切空间与余切空间]] | Hausdorff/local Euclidean、chart/atlas、curve/derivation tangent、cotangent/pullback、level set、immersion/embedding、decoder rank、local PCA与atlas模型审计 |
| Riemann 几何、测地线与流形优化 | [[习题 - Riemann 几何、测地线与流形优化]] | [[解答 - Riemann 几何、测地线与流形优化]] | metric tensor/坐标律、musical/gradient、length-energy-distance、Levi–Civita/geodesic/Exp、completeness、retraction/RGD、decoder/Fisher/Stiefel声明审计 |
| Lie 群、Lie 代数与对称性 | [[习题 - Lie 群、Lie 代数与对称性]] | [[解答 - Lie 群、Lie 代数与对称性]] | group/Lie algebra/exponential/BCH、action/orbit/stabilizer、representation/Haar projector、convolution/attention/RoPE、disconnected/boundary/parameter-symmetry审计 |
| Banach 空间、Hilbert 空间与正交投影 | [[习题 - Banach 空间、Hilbert 空间与正交投影]] | [[解答 - Banach 空间、Hilbert 空间与正交投影]] | norm/completion、Banach/Hilbert、projection/Riesz、ONB/weak convergence、conditional expectation/HiPPO/RKHS/neural-operator审计 |
| 有界算子、紧算子与谱理论基础 | [[习题 - 有界算子、紧算子与谱理论基础]] | [[解答 - 有界算子、紧算子与谱理论基础]] | bounded/compact/adjoint、Baire三大定理、resolvent/spectrum、compact self-adjoint/Schmidt、covariance/HSIC/spectral-normalization/neural-operator审计 |
| 正定核、RKHS 与表示定理 | [[习题 - 正定核、RKHS 与表示定理]] | [[解答 - 正定核、RKHS 与表示定理]] | PSD全量词、Moore–Aronszajn、Mercer条件、representer/KRR/GP、MMD/HSIC、Nyström/RFF、linear-attention与NTK审计 |
| 弱导数、Sobolev 空间与神经算子接口 | [[习题 - 弱导数、Sobolev 空间与神经算子接口]] | [[解答 - 弱导数、Sobolev 空间与神经算子接口]] | distribution/weak derivative、trace/Poincaré/embedding/compactness、Lax–Milgram、Galerkin/Céa、PINN/Deep Ritz/VPINN 与 DeepONet/FNO 审计 |
| 极分解 | [[习题 - 极分解]] | [[解答 - 极分解]] | 矩形/秩亏唯一性、最近 Stiefel、PSD 投影、谱迭代、Sylvester 微分、Muon 与 retraction |
| 矩阵符号函数 | [[习题 - 矩阵符号函数]] | [[解答 - 矩阵符号函数]] | 半平面谱分割、斜投影、block 根/polar、Newton/Schur、Fréchet、非正规条件性与 SSM |
| 浮点数与舍入误差 | [[习题 - 浮点数与舍入误差]] | [[解答 - 浮点数与舍入误差]] | IEEE 格式、$u/\gamma_n$、消去、求和/FMA、混合精度与并行归约 |
| 前向误差与后向误差 | [[习题 - 前向误差与后向误差]] | [[解答 - 前向误差与后向误差]] | 残差、最小后向扰动、条件放大、范数型/分量型/结构化误差、固定点与 AI 验收 |
| 数值稳定性 | [[习题 - 数值稳定性]] | [[解答 - 数值稳定性]] | 条件性/稳定性/准确性、前向/后向/混合稳定、等价公式、动态范围与 AI 内核验收 |
| 稳定求解线性方程组 | [[习题 - 稳定求解线性方程组]] | [[解答 - 稳定求解线性方程组]] | GEPP、增长因子、LU/三角求解误差、BERR/FERR、迭代改进、混合精度与隐式微分 |
| Householder 与 Givens 变换 | [[习题 - Householder 与 Givens 变换]] | [[解答 - Householder 与 Givens 变换]] | 反射/旋转推导、稳定符号、安全缩放、QR 顺序、后向误差、compact WY、可微 QR 与 AI 正交化 |
| 稳定最小二乘 | [[习题 - 稳定最小二乘与正规方程的风险]] | [[解答 - 稳定最小二乘与正规方程的风险]] | 投影与正规方程、条件数平方、QR/QRCP/SVD、秩亏、正则化、算法选择与回归验收 |
| 幂法、反幂法与 RQI | [[习题 - 幂法、反幂法与 Rayleigh 商迭代]] | [[解答 - 幂法、反幂法与 Rayleigh 商迭代]] | 谱比、移位、残差/gap、对称局部三次收敛、block power、非正规与 inexact solve 边界 |
| Hessenberg 与 QR 特征值算法 | [[习题 - Hessenberg 化与 QR 特征值算法]] | [[解答 - Hessenberg 化与 QR 特征值算法]] | 双侧相似、Hessenberg、移位/bulge、deflation、实 Schur、LAPACK 状态与 AI 投影谱问题 |
| Lanczos | [[习题 - Lanczos 方法]] | [[解答 - Lanczos 方法]] | 对称 Krylov、三项递推、Ritz 残差、交错、ghost、重正交、HVP/PCA/SLQ |
| Arnoldi | [[习题 - Arnoldi 方法]] | [[解答 - Arnoldi 方法]] | Hessenberg 长递推、非正规敏感性、MGS2、重启、GMRES、JVP 与矩阵函数 |
| SVD 算法与谱范数 | [[习题 - SVD 算法与谱范数估计]] | [[解答 - SVD 算法与谱范数估计]] | 双对角化、Golub–Kahan、双侧残差、幂估计、随机值域与可微边界 |
| 误差传播、条件估计与停止 | [[习题 - 误差传播、条件估计与停止准则]] | [[解答 - 误差传播、条件估计与停止准则]] | Taylor/Jacobian 传播、残差—条件—前向预算、真/递推残差与 AI 停止契约 |
| 稳定求和、点积与 GEMM | [[习题 - 稳定求和、点积与矩阵乘法]] | [[解答 - 稳定求和、点积与矩阵乘法]] | $\gamma_n$、归约树、补偿/TwoSum、点积条件数、GEMM 分量界与混合精度内核 |
| 迭代改进与混合精度 | [[习题 - 迭代改进、混合精度与残差校正]] | [[解答 - 迭代改进、混合精度与残差校正]] | 误差方程、三精度记账、收缩/地板、GMRES-IR、缩放与精度回退 |
| Ghost Sample、对称化与经验过程入口 | [[习题 - Ghost Sample、对称化与经验过程入口]] | [[解答 - Ghost Sample、对称化与经验过程入口]] | ghost sample、conditional Jensen、exchangeable swap、signed/absolute convention、sample unit |
| Rademacher 复杂度与经验复杂度 | [[习题 - Rademacher 复杂度与经验复杂度]] | [[解答 - Rademacher 复杂度与经验复杂度]] | empirical/expected complexity、Massart lemma、risk certificate、Monte Carlo/optimization gap |
| 收缩引理与 Lipschitz 损失复合 | [[习题 - 收缩引理与 Lipschitz 损失复合]] | [[解答 - 收缩引理与 Lipschitz 损失复合]] | centering、factor-2 contraction、loss constants、vector/batch composition、calibration boundary |
| 范数约束线性类的复杂度 | [[习题 - 范数约束线性类的复杂度]] | [[解答 - 范数约束线性类的复杂度]] | exact dual norm、$\ell_2/\ell_1$/bias/RKHS、feature scale、regularization-to-radius、LoRA |
| 分类间隔、Margin Bound 与 SVM 接口 | [[习题 - 分类间隔、Margin Bound 与 SVM 接口]] | [[解答 - 分类间隔、Margin Bound 与 SVM 接口]] | functional/geometric margin、ramp、$\gamma$ selection、SVM、multiclass/robust interface |
| 覆盖数、Metric Entropy 与 Chaining 入口 | [[习题 - 覆盖数、Metric Entropy 与 Chaining 入口]] | [[解答 - 覆盖数、Metric Entropy 与 Chaining 入口]] | cover/packing、empirical metric、single scale、telescoping nets、Dudley cutoff、parameter transfer |
| 局部 Rademacher 复杂度与快收敛率 | [[习题 - 局部 Rademacher 复杂度与快收敛率]] | [[解答 - 局部 Rademacher 复杂度与快收敛率]] | excess loss、star hull、sub-root fixed point、Bernstein、peeling、interpolation/fine-tuning boundary |
| Fat-Shattering、回归与 Lipschitz 风险 | [[习题 - Fat-Shattering、回归与 Lipschitz 风险]] | [[解答 - Fat-Shattering、回归与 Lipschitz 风险]] | scale-sensitive shattering、linear-ball bound、fat-to-entropy、loss contracts、vector regression |
| 算法稳定性与替换一个样本 | [[习题 - 算法稳定性与替换一个样本]] | [[解答 - 算法稳定性与替换一个样本]] | replace-one adjacency、ghost identity、期望/高概率 gap、randomized coupling、group unit |
| 正则化 ERM 的稳定性 | [[习题 - 正则化 ERM 的稳定性]] | [[解答 - 正则化 ERM 的稳定性]] | strong-convexity cancellation、$1/(\lambda m)$、一般 norm、approximate optimizer、weight-decay 边界 |
| 随机梯度算法的稳定性接口 | [[习题 - 随机梯度算法的稳定性接口]] | [[解答 - 随机梯度算法的稳定性接口]] | synchronous coupling、nonexpansive/expansive map、step-sum、nonconvex recurrence、mini-batch/optimizer 审计 |
| 样本压缩方案与泛化 | [[习题 - 样本压缩方案与泛化]] | [[解答 - 样本压缩方案与泛化]] | compressor/reconstructor、subset count、side bits、full-sample consistency、AI compression 分账 |
| PAC-Bayes Bound 的测度变换主线 | [[习题 - PAC-Bayes Bound 的测度变换主线]] | [[解答 - PAC-Bayes Bound 的测度变换主线]] | binary types、prior moment、change of measure、joint convexity、inverse-kl 与 Gibbs predictor |
| PAC-Bayes 先验、后验与数据依赖边界 | [[习题 - PAC-Bayes 先验、后验与数据依赖边界]] | [[解答 - PAC-Bayes 先验、后验与数据依赖边界]] | prior independence、Gaussian KL、split/mixture/DP prior、support、Monte Carlo certificate |
| 互信息与信息论泛化界 | [[习题 - 互信息与信息论泛化界]] | [[解答 - 互信息与信息论泛化界]] | sample–output channel、KL transport、expected signed gap、bit budget、adaptive transcript |
| 容量界、稳定性界与 PAC-Bayes 的比较 | [[习题 - 容量界、稳定性界与 PAC-Bayes 的比较]] | [[解答 - 容量界、稳定性界与 PAC-Bayes 的比较]] | 五类证书对象/量词、桥梁与反例、nonvacuity、post-hoc selection、AI 选型 |
| 偏差—方差—噪声分解 | [[习题 - 偏差—方差—噪声分解]] | [[解答 - 偏差—方差—噪声分解]] | fixed/random-X、平方损失正交分解、data/seed variance、projection、ensemble 与 AI 误差审计 |
| 正则化、交叉验证与模型选择 | [[习题 - 正则化、交叉验证与模型选择]] | [[解答 - 正则化、交叉验证与模型选择]] | selection oracle、K-fold estimand、nested CV、preprocessing/group/time leakage 与 adaptive agent |
| 线性回归的统计学习理论 | [[习题 - 线性回归的统计学习理论]] | [[解答 - 线性回归的统计学习理论]] | population projection、BLUE、Random-X rate、sandwich、秩亏、solver 与 linear probe |
| 逻辑回归、复合损失与概率分类 | [[习题 - 逻辑回归、复合损失与概率分类]] | [[解答 - 逻辑回归、复合损失与概率分类]] | entropy–KL、properness、IRLS、separation、class-weight target、softmax 与 cost threshold |
| 支持向量机、最大间隔与核方法 | [[习题 - 支持向量机、最大间隔与核方法]] | [[解答 - 支持向量机、最大间隔与核方法]] | canonical margin、hard/soft primal、dual/KKT、hinge、kernel bandwidth、stability 与 calibration |
| 核岭回归与 Gaussian Process 接口 | [[习题 - 核岭回归与 Gaussian Process 接口]] | [[解答 - 核岭回归与 Gaussian Process 接口]] | representer theorem、spectral filter、effective dimension、LOOCV、GP conditioning、scale match 与 uncertainty boundary |
| 决策树、分裂准则与剪枝 | [[习题 - 决策树、分裂准则与剪枝]] | [[解答 - 决策树、分裂准则与剪枝]] | partition + leaf action、SSE/Gini gain、weakest-link pruning、instability、calibration 与 importance bias |
| Bagging、Random Forest 与 Boosting | [[习题 - Bagging、Random Forest 与 Boosting]] | [[解答 - Bagging、Random Forest 与 Boosting]] | bootstrap/OOB、ensemble correlation floor、random forest、AdaBoost、functional gradient 与 selection reuse |
| PCA 的统计估计与主子空间风险 | [[习题 - PCA 的统计估计与主子空间风险]] | [[解答 - PCA 的统计估计与主子空间风险]] | variance/reconstruction/SVD 等价、eigengap、projector risk、泄漏与 embedding compression |
| K-Means、聚类风险与不可辨识性 | [[习题 - K-Means、聚类风险与不可辨识性]] | [[解答 - K-Means、聚类风险与不可辨识性]] | population distortion、Lloyd 单调性、permutation loss、global/local gap 与语义评价 |
| 潜变量模型、混合模型与 EM | [[习题 - 潜变量模型、混合模型与 EM]] | [[解答 - 潜变量模型、混合模型与 EM]] | ELBO/KL、E/M 单调性、GMM updates、label switching、variance collapse 与 amortization |
| 模型可辨识性、选择与 Misspecification | [[习题 - 模型可辨识性、选择与 Misspecification]] | [[解答 - 模型可辨识性、选择与 Misspecification]] | equivalence class、KL projection、sandwich covariance、AIC/BIC/CV 与机制审计 |
| 表示学习的任务、表示与下游风险 | [[习题 - 表示学习的任务、表示与下游风险]] | [[解答 - 表示学习的任务、表示与下游风险]] | encoder–head–task 合同、oracle/finite risk、sufficiency/invariance、task diversity 与迁移评价 |
| 度量学习、相似性与检索风险 | [[习题 - 度量学习、相似性与检索风险]] | [[解答 - 度量学习、相似性与检索风险]] | metric/pseudometric、Mahalanobis、pair/triplet、mining、Recall/AP 与 query–gallery 协议 |
| 对比学习、InfoNCE 与密度比 | [[习题 - 对比学习、InfoNCE 与密度比]] | [[解答 - 对比学习、InfoNCE 与密度比]] | candidate-index experiment、density ratio、MI lower bound、log-K ceiling 与 NCE 分工 |
| 正负样本、Batch 依赖与梯度估计 | [[习题 - 正负样本、Batch 依赖与梯度估计]] | [[解答 - 正负样本、Batch 依赖与梯度估计]] | NT-Xent 梯度、temperature、false negatives、hard sampling、queue 与 all-gather 合同 |
| 数据增强、不变性、等变性与任务充分性 | [[习题 - 数据增强、不变性、等变性与任务充分性]] | [[解答 - 数据增强、不变性、等变性与任务充分性]] | augmentation kernel、label preservation、群平均、clustered views、invariance/equivariance 与任务冲突 |
| 表示坍缩、非坍缩与可辨识边界 | [[习题 - 表示坍缩、非坍缩与可辨识边界]] | [[解答 - 表示坍缩、非坍缩与可辨识边界]] | complete/dimensional/spectral collapse、VICReg/Barlow、stop-gradient/EMA、effective rank 与等价类 |
| 遮蔽预测、Teacher–Student 与自监督目标 | [[习题 - 遮蔽预测、Teacher–Student 与自监督目标]] | [[解答 - 遮蔽预测、Teacher–Student 与自监督目标]] | conditional target、MLM/MAE、Mean Teacher/BYOL/DINO、EMA、leakage 与 confirmation bias |
| Linear Probe、Fine-Tuning 与迁移评估 | [[习题 - Linear Probe、Fine-Tuning 与迁移评估]] | [[解答 - Linear Probe、Fine-Tuning 与迁移评估]] | oracle/finite probe、XOR、fine-tuning risk、label/head/compute curves、nested transfer matrix |
| 概率校准、Proper Scoring Rule 与可靠性图 | [[习题 - 概率校准、Proper Scoring Rule 与可靠性图]] | [[解答 - 概率校准、Proper Scoring Rule 与可靠性图]] | strong/classwise/top-label calibration、log/Brier properness、Brier 分解、ECE、temperature 与成本阈值 |
| Aleatoric、Epistemic 与模型不确定性 | [[习题 - Aleatoric、Epistemic 与模型不确定性]] | [[解答 - Aleatoric、Epistemic 与模型不确定性]] | information set、总方差、异方差 NLL、entropy/MI、错设、OOD 与行动价值 |
| Bayesian Posterior Predictive、Ensemble 与近似边界 | [[习题 - Bayesian Posterior Predictive、Ensemble 与近似边界]] | [[解答 - Bayesian Posterior Predictive、Ensemble 与近似边界]] | predictive integral、mixture moments、MC error、dropout/SWAG/ensemble、相关性与 shift |
| Conformal Prediction 与有限样本 Coverage | [[习题 - Conformal Prediction 与有限样本 Coverage]] | [[解答 - Conformal Prediction 与有限样本 Coverage]] | exchangeable rank、finite quantile、residual/CQR/APS、marginal coverage、reuse 与 efficiency |
| Covariate、Label 与 Concept Shift | [[习题 - Covariate、Label 与 Concept Shift]] | [[解答 - Covariate、Label 与 Concept Shift]] | joint factorization、support、label-shift inversion、temporal/feedback diagnosis |
| 重要性加权与 Covariate Shift 校正 | [[习题 - 重要性加权与 Covariate Shift 校正]] | [[解答 - 重要性加权与 Covariate Shift 校正]] | target-risk identity、ratio、ESS、clipping、cross-fit 与 weighted selection |
| Domain Adaptation 与 Domain Generalization Bound | [[习题 - Domain Adaptation 与 Domain Generalization Bound]] | [[解答 - Domain Adaptation 与 Domain Generalization Bound]] | HΔH、joint ideal error、DANN、collapse 与 target-blind DG selection |
| OOD、鲁棒性与因果不变性的边界 | [[习题 - OOD、鲁棒性与因果不变性的边界]] | [[解答 - OOD、鲁棒性与因果不变性的边界]] | specified out-law、utility、natural shift、worst group、SCM/IRM boundary |
| 在线学习协议、Regret 与 Comparator | [[习题 - 在线学习协议、Regret 与 Comparator]] | [[解答 - 在线学习协议、Regret 与 Comparator]] | protocol、feedback、static/dynamic/policy comparator、filtration 与负 regret |
| Experts、Weighted Majority 与 Multiplicative Weights | [[习题 - Experts、Weighted Majority 与 Multiplicative Weights]] | [[解答 - Experts、Weighted Majority 与 Multiplicative Weights]] | Hedge update、log-potential、prior complexity、doubling 与 bandit 边界 |
| Online Gradient Descent 与 Mirror Descent | [[习题 - Online Gradient Descent 与 Mirror Descent]] | [[解答 - Online Gradient Descent 与 Mirror Descent]] | projection telescope、$DG\sqrt T$、Bregman 三点式、geometry 与 oracle residual |
| 随机、对抗与自适应序列的区别 | [[习题 - 随机、对抗与自适应序列的区别]] | [[解答 - 随机、对抗与自适应序列的区别]] | filtration、fresh coin、adaptive adversary、martingale 与 policy regret |
| Perceptron Mistake Bound 与 Margin | [[习题 - Perceptron Mistake Bound 与 Margin]] | [[解答 - Perceptron Mistake Bound 与 Margin]] | update 双账本、$R/\gamma$、bias/kernel、noise 与 mistake/generalization 边界 |
| Boosting、弱学习与指数损失 | [[习题 - Boosting、弱学习与指数损失]] | [[解答 - Boosting、弱学习与指数损失]] | weak quantifier、$\alpha/Z$、指数势能、training bound、margin 与 noise |
| Online-to-Batch Conversion | [[习题 - Online-to-Batch Conversion]] | [[解答 - Online-to-Batch Conversion]] | fresh example、random/average output、martingale、comparator selection 与 drift |
| Bandit Feedback 与强化学习接口 | [[习题 - Bandit Feedback 与强化学习接口]] | [[解答 - Bandit Feedback 与强化学习接口]] | UCB/EXP3、IPS 无偏—方差、contextual policy、MDP、offline overlap 与 safety |
| 插值、双下降与经典偏差方差边界 | [[习题 - 插值、双下降与经典偏差方差边界]] | [[解答 - 插值、双下降与经典偏差方差边界]] | interpolation threshold、Gaussian risk、singular amplification 与三类 path |
| 过参数化与 Benign Overfitting | [[习题 - 过参数化与 Benign Overfitting]] | [[解答 - 过参数化与 Benign Overfitting]] | min-norm projector、signal/noise、effective spectrum tail 与 consistency |
| 隐式偏置、最大间隔与优化选择 | [[习题 - 隐式偏置、最大间隔与优化选择]] | [[解答 - 隐式偏置、最大间隔与优化选择]] | row-space min norm、logistic max margin、init/preconditioner 与 risk bridge |
| 范数、平坦性、Sharpness 与参数化不变性 | [[习题 - 范数、平坦性、Sharpness 与参数化不变性]] | [[解答 - 范数、平坦性、Sharpness 与参数化不变性]] | ReLU rescaling、Hessian 反例、path invariance 与 measure evidence ladder |
| 神经网络容量与 Norm-Based Bound | [[习题 - 神经网络容量与 Norm-Based Bound]] | [[解答 - 神经网络容量与 Norm-Based Bound]] | spectral product、stable rank、perturbation telescope、margin certificate 与 nonvacuity |
| NTK、Lazy Training 与 Kernel Regime | [[习题 - NTK、Lazy Training 与 Kernel Regime]] | [[解答 - NTK、Lazy Training 与 Kernel Regime]] | tangent Gram、kernel dynamics、eigenmode、linearization、kernel drift 与风险桥 |
| Mean-Field、Feature Learning 与训练 Regime | [[习题 - Mean-Field、Feature Learning 与训练 Regime]] | [[解答 - Mean-Field、Feature Learning 与训练 Regime]] | 经验测度、continuity PDE、scaling、propagation of chaos 与 feature-learning 诊断 |
| 深度泛化证据地图与开放问题 | [[习题 - 深度泛化证据地图与开放问题]] | [[解答 - 深度泛化证据地图与开放问题]] | 证据分级、随机标签、uniform-convergence 边界、指标验收与研究 claim card |

每套均包含 A–E 分层训练与独立解答。神经网络基础已有 64 组 960 题；[[neural_network_foundations_teaching_contract_audit.py]]确认 NN-01—28 现行迁移 **28/64**，30.1—30.3 材料门 **3/8 `regression-passed`**，30.4 为 4/8 in-progress，NN-29—64 尚有 **36/64** 待迁移。旧 NN-CUM-01 仍为 `composed`，个人保持 `not-attempted`。

## 习题与解答的关系

- 习题使用[[模板 - 习题集]]；
- 解答使用[[模板 - 习题解答]]；
- 阶段测验使用[[模板 - 阶段测验]]；
- 题目与解答使用稳定 ID，如 `LA-QR-B02`；
- 习题正文可以提供分级提示，但不直接显示最终答案；
- 解答必须解释“为什么”，不能只给计算结果；
- 一题若有多种解法，至少比较它们的前置知识、复杂度或数值稳定性。

## 题目 ID

格式：

```text
领域-主题-级别编号
```

示例：

| ID | 含义 |
|---|---|
| `LA-GS-B01` | 线性代数、Gram–Schmidt、第一道手算题 |
| `LA-SPEC-C02` | 线性代数、谱定理、第二道证明题 |
| `NLA-QR-D01` | 数值线性代数、QR、第一道失败/反例题 |
| `AI-SVD-E03` | SVD 的第三道 AI 迁移题 |

## 提示分级

当题目确实需要提示时，依次提供：

1. **方向提示**：应回忆哪个定义或定理；
2. **结构提示**：第一步应构造什么对象；
3. **计算提示**：给出关键中间式，但仍不展示答案。

不要在题干后立即给完整推导。读者应先记录尝试和卡点，再查看提示或解答。

## 自评标记

每题完成后记录一种状态：

| 状态 | 含义 | 下一步 |
|---|---|---|
| `independent` | 无提示完成且能解释 | 间隔复习 |
| `hinted` | 使用提示后完成 | 48 小时后重做 |
| `copied` | 看解答后才能复现 | 回到前置节点并换一道同类题 |
| `blocked` | 解答仍无法理解 | 标记具体断点，补前置知识 |
| `careless` | 概念会但计算/符号失误 | 建立错误模式记录 |

`copied` 不算掌握；能够复述解答也不等于能够独立重建。

## 阶段测验结构

每次测验至少覆盖：

- 20% 定义、维度和条件识别；
- 30% 手算与构造；
- 25% 推导、证明或纠错；
- 15% 反例和边界；
- 10% AI 迁移。

比例可以随主题调整，但不能只剩选择题或机械计算。

### 当前规划

学习理论 LT-01—84 已完成全章静态材料门：[[learning_theory_teaching_contract_audit.py]]复核 84 组习题—解答双射、1260 个 A—E 题解 ID、来源卡、范围内链接、节点图文单元、18 个节点制图脚本与全部已存资产的双重复跑。前五卷分别由[[learning_problem_decision_cumulative_contract_audit.py]]、[[pac_finite_class_cumulative_contract_audit.py]]、[[vc_uniform_convergence_cumulative_contract_audit.py]]、[[rademacher_margin_local_cumulative_contract_audit.py]]和[[algorithmic_generalization_cumulative_contract_audit.py]]独立复核。五卷均使用口试、210 分钟 100 分闭卷、scorer nonce、跨轨盲参、48 小时与 14 天证据链；它们完成时把卷级材料门推进到 **5/10**，个人通过仍为 **0/10 / `not-attempted`**。

前五卷另由[[资格考 - 学习理论 I：从风险到算法依赖泛化（20.1—20.5）|LT-QUAL-01]]做跨卷验收，并配有[[资格考解答 - 学习理论 I：从风险到算法依赖泛化（20.1—20.5）|独立详解]]、[[实验 - 学习理论资格考 I 跨卷累计复现门|三轨门]]与[[learning_theory_qualification_01_contract_audit.py|独立审计]]。它构成第一份跨卷资格考材料；不能把题卷或 canonical 图存在写成个人通过。

第六卷[[阶段测验 - 经典模型与模型选择（20.6）|MODEL-CUM-01]]、独立详解与[[实验 - 经典模型与模型选择累计复现门|三轨门]]也已由[[classical_models_cumulative_contract_audit.py]]回归；它把卷级材料门推进到 **6/10**。个人仍为 **0/10 / `not-attempted`**；正式认证前置为 `LT-QUAL-01 retained`，当前未满足。

第七卷[[阶段测验 - 表示学习、度量学习与自监督（20.7）|REPR-CUM-01]]、独立详解与[[实验 - 表示学习、度量学习与自监督累计复现门|三轨门]]已由[[representation_selfsupervised_cumulative_contract_audit.py]]回归；它把卷级材料门推进到 **7/10**。个人仍为 **0/10 / `not-attempted`**；正式认证前置为 `MODEL-CUM-01 retained`，当前未满足。

第八卷[[阶段测验 - 校准、不确定性与分布偏移（20.8）|REL-CUM-01]]、独立详解与[[实验 - 校准、不确定性与分布偏移累计复现门|三轨门]]已由[[calibration_shift_cumulative_contract_audit.py]]回归；它把卷级材料门推进到 **8/10**。个人仍为 **0/10 / `not-attempted`**；正式认证前置为 `REPR-CUM-01 retained`，当前未满足。

第九卷[[阶段测验 - 在线学习、Boosting 与序列预测（20.9）|ONLINE-CUM-01]]、独立详解与[[实验 - 在线学习、Boosting 与序列预测累计复现门|三轨门]]已由[[online_boosting_cumulative_contract_audit.py]]回归；它把卷级材料门推进到 **9/10**。个人仍为 **0/10 / `not-attempted`**；正式认证前置为 `REL-CUM-01 retained`，当前未满足。

第十卷[[阶段测验 - 深度泛化理论接口与开放边界（20.10）|DEEP-CUM-01]]、独立详解与[[实验 - 深度泛化理论接口与开放边界累计复现门|三轨门]]已由[[deep_generalization_cumulative_contract_audit.py]]回归；至此卷级材料达到 **10/10**。个人仍为 **0/10 / `not-attempted`**；正式认证前置为 `ONLINE-CUM-01 retained`，当前未满足。

后五卷现由[[资格考 - 学习理论 II：从模型选择到深度泛化证据（20.6—20.10）|LT-QUAL-02]]统一验收，并配有[[资格考解答 - 学习理论 II：从模型选择到深度泛化证据（20.6—20.10）|独立详解]]、[[实验 - 学习理论资格考 II 跨卷累计复现门|三轨门]]与[[learning_theory_qualification_02_contract_audit.py|独立审计]]。至此跨卷资格考材料为 **2/2 `regression-passed`**；个人资格仍为 **0/2 / `not-attempted`**，正式参加须先满足 `LT-QUAL-01 + MODEL/REPR/REL/ONLINE/DEEP retained`。

| 学习理论卷级测验 | 覆盖范围 | 状态 |
|---|---|---|
| LT-CUM-01 | LT-01—08：学习问题、决策与风险 | regression-passed material / not-attempted learner |
| PAC-CUM-01 | LT-09—16：PAC 学习与有限假设类 | regression-passed material / not-attempted learner |
| VC-CUM-01 | LT-17—24：VC 维、增长函数与一致收敛 | regression-passed material / not-attempted learner |
| RAD-CUM-01 | LT-25—32：数据依赖复杂度、间隔与快率 | regression-passed material / not-attempted learner |
| ALG-CUM-01 | LT-33—40：稳定性、压缩、PAC-Bayes 与信息泛化 | regression-passed material / not-attempted learner |
| MODEL-CUM-01 | LT-41—52：经典模型与模型选择 | regression-passed material（6/10）/ not-attempted learner（0/10；LT-QUAL-01 retained 前置未满足） |
| REPR-CUM-01 | LT-53—60：表示学习、度量学习与自监督 | regression-passed material（7/10）/ not-attempted learner（0/10；MODEL-CUM-01 retained 前置未满足） |
| REL-CUM-01 | LT-61—68：校准、不确定性与分布偏移 | regression-passed material（8/10）/ not-attempted learner（0/10；REPR-CUM-01 retained 前置未满足） |
| ONLINE-CUM-01 | LT-69—76：在线学习、Boosting 与序列预测 | regression-passed material（9/10）/ not-attempted learner（0/10；REL-CUM-01 retained 前置未满足） |
| DEEP-CUM-01 | LT-77—84：深度泛化理论接口与开放边界 | regression-passed material（10/10）/ not-attempted learner（0/10；ONLINE-CUM-01 retained 前置未满足） |

| 学习理论跨卷资格考 | 覆盖范围 | 状态 |
|---|---|---|
| LT-QUAL-01 | LT-01—40：risk/PAC/VC/Rademacher/algorithm-dependent generalization | regression-passed material（1/2）/ not-attempted learner（0/2） |
| LT-QUAL-02 | LT-41—84：模型/表示/可靠性/序列学习/深度泛化证据 | regression-passed material（2/2）/ not-attempted learner（0/2；LT-QUAL-01 与后五卷 retained 前置未满足） |

| 测验 | 覆盖范围 | 状态 |
|---|---|---|
| MATH-CUM-01 | MATH-01—08：数学语言、逻辑与证明卷末累计验收 | regression-passed：题卷、详解、[[实验 - 数学语言、逻辑与证明累计复现门]]与[[math_foundations_cumulative_contract_audit.py]]已通过答案/输出隔离、canonical/跨轨盲参静态与计算回归；个人仍为 not-attempted |
| GEO-CUM-01 | GEO-01—08：几何、泛函分析、核与算子基础卷末累计验收 | regression-passed：题卷、详解、[[实验 - 几何、泛函与算子累计复现门]]与[[geometry_functional_cumulative_contract_audit.py]]已通过答案/输出隔离、canonical/跨轨盲参静态与计算回归；个人仍为 not-attempted |
| OPT-CUM-01 | OPT-01—16：优化与凸分析卷末累计验收 | regression-passed：题卷、详解、[[实验 - 优化与凸分析累计复现门]]与[[optimization_cumulative_contract_audit.py]]已通过独立静态/计算回归；个人仍为 not-attempted |
| INFO-CUM-01 | INFO-01—10：信息论与统计学习接口卷末累计验收 | regression-passed：题卷、详解、[[实验 - 信息论累计复现门]]与[[information_cumulative_contract_audit.py]]已通过独立静态/计算回归；个人仍为 not-attempted |
| PROB-CUM-01 | PROB-01—20：概率论与数理统计卷末累计验收 | regression-passed：题卷、详解、[[实验 - 概率统计累计复现门]]与[[probability_cumulative_contract_audit.py]]已通过独立静态/计算回归；个人仍为 not-attempted |
| LA-CUM-01 | LA-01—24：线性代数卷末累计验收 | regression-passed：[[阶段测验 - 线性代数（10.2）]]、[[阶段测验解答 - 线性代数（10.2）]]和[[实验 - 线性代数累计复现门]]已通过独立静态/计算回归；个人仍为 not-attempted |
| MA-CUM-01 | MA-01—16：矩阵分析卷末累计验收 | regression-passed：[[阶段测验 - 矩阵分析（10.3）]]、[[阶段测验解答 - 矩阵分析（10.3）]]和[[实验 - 矩阵分析累计复现门]]已通过独立静态/计算回归；个人仍为 not-attempted |
| CALC-CUM-01 | CALC-01—16：微积分、矩阵微分与自动微分卷末累计验收 | regression-passed：题卷、详解、[[实验 - 微积分、矩阵微分与自动微分累计复现门]]与[[calculus_ad_cumulative_contract_audit.py]]已通过独立静态/计算回归；个人仍为not-attempted |
| NLA-CUM-01 | NUM-01—20：数值计算与数值线性代数卷末累计验收 | regression-passed：题卷、详解、[[实验 - 数值线性代数累计复现门]]与[[numerical_cumulative_contract_audit.py]]已通过独立静态/计算回归；个人仍为 not-attempted |
| DYN-CUM-01 | DYN-01—12：ODE、动力系统与 SDE 卷末累计验收 | regression-passed：题卷、详解、[[实验 - ODE、动力系统与 SDE 累计复现门]]与[[dynamics_cumulative_contract_audit.py]]已通过解析、canonical/盲参静态与计算回归；个人仍为 not-attempted |
| NN-CUM-01 | NN-01—64：神经网络基础第三章累计验收 | legacy composed：现行迁移 28/64、待迁移 36/64，材料门 3/8，30.4 为 4/8 in-progress，个人 not-attempted |
| ARCH-CAP-01 | ARCH-01—64：表示与模型架构第四章跨卷累计验收 | composed：[[阶段测验 - 表示与模型架构（第四章）]]、[[阶段测验解答 - 表示与模型架构（第四章）]]和[[实验 - 表示与模型架构跨卷累计复现门]]已建立；等待真实独立作答 |
| MATH-FND-CAP-01 | 十卷150节点的跨卷理论、AI系统审计与研究合同总出口 | regression-passed：题卷、详解、[[实验 - 数学基础十卷跨章累计复现门]]与[[math_foundations_capstone_contract_audit.py]]已通过十卷材料前置、答案/输出隔离、canonical/三轨盲参回归；个人仍为not-attempted |
| `L2-A` | Gram–Schmidt、QR、消元/LU、trace/determinant、正定、Cholesky | incorporated：10.2部分已纳入LA-CUM-01，其余由10.3承接 |
| `L2-B` | 对偶、伴随、重数、Jordan、Schur、矩阵函数 | incorporated：LA-15—20已纳入LA-CUM-01，高级谱迁移由10.3承接 |
| `L2-C` | 极分解、矩阵符号函数、SVD/极分解微分与矩阵优化 | incorporated/bridged：SVD与伪逆进入LA-CUM-01，其余属于10.3 |
| `L3-A` | 浮点、前后向误差、稳定性、稳定线性求解、QR 与最小二乘 | incorporated：已纳入 NLA-CUM-01；等待真实作答 |
| `L3-B` | 特征值算法、Krylov、残差最小化与数值 SVD | incorporated：已纳入 NLA-CUM-01；等待真实作答 |
| `L3-C` | 稀疏存储、填充、并行负载与随机低秩 | incorporated：已纳入 NLA-CUM-01；等待真实作答 |
| `LA-AI` | 回归、PCA、低秩、谱约束与矩阵优化器 | incorporated：LA-CUM-01第13—14题与计算C轨；高级算法由后续卷迁移 |

### LA-CUM-01 的状态边界

LA-CUM-01已把“20分钟无提示口试 + 240分钟、100分闭卷 + 随机累计实验轨”组成10.2卷末验收，覆盖LA-01—24，并设置A—E分区线、三道统一结构证明不得为零、盲参数干预与延迟保持门。材料状态是 **regression-passed**，个人状态是 **not-attempted**：

- 口试先检查对象类型、商与唯一性、几何/伴随、QR/SVD、谱/Jordan和AI线性出口，不能用计算图替代；
- 24套节点题之后的累计题卷与逐题独立详解已经成稿，并明确先冻结原稿再开解答；
- 计算门连接病态basis/quotient/projector、Jordan transient/SVD tail与attention-softmax rank/vec identity，由`attempt_id + scorer nonce`防止挑轨；
- canonical SVG、XML、hash、确定性双跑、参数接口与[[linear_algebra_cumulative_contract_audit.py]]通过，只证明验收工具可执行；
- 尚无首次口试、闭卷原稿、逐项评分、盲参数干预、48小时重做和14天AI迁移证据；
- 因而LA-01—24保持`draft`；正式作答前不要打开[[阶段测验解答 - 线性代数（10.2）]]。

### MA-CUM-01 的状态边界

MA-CUM-01已把“20分钟无提示口试 + 270分钟、100分闭卷 + 随机累计实验轨”组成10.3卷末验收，覆盖MA-01—16，并设置A—E分区线、三道统一证明不得为零、盲参数干预与延迟保持门。材料状态是 **regression-passed**，个人状态是 **not-attempted**：

- 口试先检查object/norm/condition、rank-change、positive margin/gap、non-normality/Fréchet/structure和AI声明出口，不能用计算图替代；
- 16套节点题之后的累计题卷与逐题独立详解已经成稿，并明确先冻结原稿再开解答；
- 计算门连接positive margin/Cholesky/condition、gap/angle/pseudospectrum与sign/polar/Fréchet/structured condition，由`attempt_id + scorer nonce`防止挑轨；
- canonical SVG、XML、hash、确定性双跑、参数接口与[[matrix_analysis_cumulative_contract_audit.py]]通过，只证明验收工具可执行；
- 尚无首次口试、闭卷原稿、逐项评分、盲参数干预、48小时换机制和14天AI迁移证据；
- 因而MA-01—16保持`draft`；正式作答前不要打开[[阶段测验解答 - 矩阵分析（10.3）]]。

### CALC-CUM-01 的状态边界

CALC-CUM-01是“20分钟口试 + 270分钟、100分闭卷 + nonce随机三轨 + 盲参数干预 + 48小时/14天延迟门”的10.4卷末验收，覆盖CALC-01—16，并设置A—E分区线与三道统一证明门。材料状态为 **regression-passed**，个人状态为 **not-attempted**：

- 16套节点题、累计题卷与逐题独立详解已经成稿；
- 计算门连接Taylor/finite-difference、JVP/VJP/HVP与implicit/spectral derivative，并由scorer nonce防止挑题；
- canonical SVG、XML、hash、确定性双跑、盲参数接口和[[calculus_ad_cumulative_contract_audit.py]]通过，只证明工具可执行；
- 尚无首次口试/闭卷原稿、评分者随机轨、个人盲干预、48小时重做和14天AI迁移证据；
- 因而CALC-01—16保持`draft`；正式作答前不要打开[[阶段测验解答 - 多元微积分、矩阵微分与自动微分（10.4）]]。

### MATH-CUM-01 的状态边界

MATH-CUM-01 是15分钟口试加180分钟、100分闭卷卷末测验，覆盖MATH-01—08，并设置A—E分区线、definition/quantifier最低线、完整证明不得为零和量词—递推—复杂度三轨计算门。当前状态为材料 **regression-passed** / 个人 **not-attempted**：

- 八套节点题共120题，累计题卷与逐题独立详解已经成稿；
- 计算门参数化有限关系、受迫收缩递推与fixed/adaptive rank制度，并由scorer nonce指定主轨及跨轨盲参数；
- [[math_foundations_cumulative_contract_audit.py]]已通过题—解和答案—输出隔离、解析锚点、六个状态面、XML、canonical双跑、非标准覆盖保护与固定盲参stdout/SVG/hash，只证明工具可执行；
- 尚无首次口试、闭卷原稿、逐项评分、个人未见跨轨盲参数、48小时换机制和14天陌生AI迁移证据；
- 因而MATH-01—08保持`draft`；正式作答前不要打开[[阶段测验解答 - 数学语言、逻辑与证明（10.1）]]。

### GEO-CUM-01 的状态边界

GEO-CUM-01是“20分钟口试 → 210分钟、100分闭卷 → scorer nonce主轨 → 跨轨盲参数 → 订正 → 48小时换机制 → 14天陌生AI迁移”的卷末测验，覆盖GEO-01—08，并设置A—E分区线、流形/RKHS/弱PDE对象合同最低线和三道主证明门。材料状态为 **regression-passed**，个人状态为 **not-attempted**：

- 八套节点题共120题，累计题卷与逐题独立详解已经成稿；
- 口试强制建立九层几何—泛函—算子对象账本与continuous-to-discrete边界；
- 计算门连接radius-sphere tangent/retraction/symmetry、Hilbert target/compact/kernel幂律谱与length-$L$ Poisson operator多norm误差；先冻结预测再公开scorer nonce，盲参至少跨两轨；
- [[geometry_functional_cumulative_contract_audit.py]]已通过题—解和答案—输出隔离、解析量、六个状态面、XML、canonical双跑、非标准覆盖保护与固定盲参stdout/SVG/hash，只证明工具可执行；
- 尚无首次口试、闭卷原稿、逐项评分、个人未见跨轨盲参数、48小时换机制和14天operator-learning迁移证据；
- 因而GEO-01—08保持`draft`；正式作答前不要打开[[阶段测验解答 - 几何、泛函分析、核与算子基础（10.10）]]。

### DYN-CUM-01 的状态边界

DYN-CUM-01 是“20 分钟口试 → 240 分钟、100 分闭卷 → nonce 随机三轨 → 多参数盲测 → 订正 → 48 小时换机制 → 14 天陌生 AI 迁移”的卷末测验，覆盖 DYN-01—12，并设置 A—E 分区线、well-posedness / flow-density / Itô-Fokker–Planck-reversal 三道主链不得为零。材料状态是 **regression-passed**，个人状态是 **not-attempted**：

- 十二套节点题共 180 题，累计题卷和逐题独立详解已经成稿；
- 口试强制重建四波模型链、九层连续动力学对象账本、reverse clock/full-half score 和连续生成模型合同；
- 计算门串联 continuous/discrete stability、FPE/PF/CNF density ledger 与 Brownian/Itô/reverse-score coefficient，先冻结预测再运行随机轨道；
- 闭卷冻结后由 `scorer nonce` 指定手算轨和跨轨盲参数；必须先冻结预测，再保存个人新 output/SVG/hash；
- [[dynamics_cumulative_contract_audit.py]]已通过题—解与 100 分、解析量、六个状态入口、XML、canonical 双跑、固定盲参 SHA-256 与图—数自描述；这只证明工具可执行；
- 尚无首次口试、闭卷原稿、逐项评分、scorer nonce、个人未见参数 output/SVG/hash、48 小时换机制和 14 天陌生 AI 迁移证据；
- 因而动力系统卷 12 个节点保持 `draft`；正式作答前不要打开[[阶段测验解答 - ODE、动力系统与 SDE（10.9）]]。

### NLA-CUM-01 的状态边界

NLA-CUM-01 已把 L3-A、L3-B 与 L3-C 组合成“15 分钟口试 → 180 分钟、100 分闭卷 → nonce 随机累计轨 → 盲干预 → 订正 → 48 小时 / 14 天延迟门”的卷末验收，覆盖 NUM-01—20。材料状态是 **regression-passed**，个人状态是 **not-attempted**：

- 口试要求无提示重建五波模型链、五类误差/证书对象、结构选法与 AI 数值研究合同；第 1、4 问必须通过；
- 题卷和独立详解成稿并保持题—解隔离；正式作答前不要打开[[阶段测验解答 - 数值计算与数值线性代数（10.8）]]；
- 冻结 `attempt_id`、首次答卷和 canonical 输出后，由 `scorer nonce` 从 A“可靠性”、B“结构求解”、C“稀疏随机”三轨指定一轨；学习者必须先交两项手算和盲参数预测，再保存个人新 output/SVG/hash；
- canonical SVG、XML、SHA-256、三轨独立解析复算、确定性双跑、固定盲参 fixture 与[[numerical_cumulative_contract_audit.py]]通过，只证明验收材料可执行；
- 尚无学习者口试、原始答卷、逐项评分、nonce、个人未见参数运行、48 小时换机制和 14 天陌生 AI 数值迁移证据；
- 因此 NUM-01—20 继续保持 `draft`，10.8 个人累计状态保持 `not-attempted`，不升级为 verified。

### PROB-CUM-01 的状态边界

PROB-CUM-01 以 15 分钟口试和 180 分钟、100 分闭卷覆盖 PROB-01—20，并设置 A—E 分区线、三道主链不得为零、scorer nonce 随机轨、盲参数干预与 48 h / 14 d 延迟门。当前状态为 **regression-passed / not-attempted**：

- 题卷、独立详解、coverage–IS–MCMC 三轨盲参数接口与独立审计均已回归通过；
- canonical 双跑、精确模型和状态同步只证明验收工具可执行，不证明学习者掌握；
- 尚无首次口试/闭卷原稿、逐题评分、nonce 随机轨、新 output/hash、48 小时重建和 14 天迁移证据；
- 因而概率卷 20 个节点全部保持 `draft`；正式作答前不要打开[[阶段测验解答 - 概率论与数理统计（10.5）]]。

### INFO-CUM-01 的状态边界

INFO-CUM-01 以 15 分钟口试和 180 分钟、100 分闭卷覆盖 INFO-01—10，并设置 A—E 分区线、三条证明硬门、scorer nonce 随机轨、RD—IB—prequential 盲参数干预与 48 h / 14 d 延迟门。当前状态为 **regression-passed / not-attempted**：

- 题卷、独立详解、三轨参数化计算门与[[information_cumulative_contract_audit.py]]均已回归通过；
- 解析三波模型、canonical 双跑、干预 hash 与状态同步只证明验收工具可执行；
- 尚无首次口试/闭卷原稿、独立评分、nonce 随机轨、个人新 output/hash、48 小时重建和 14 天迁移证据；
- 因而 INFO-01—10 保持 `draft`；正式作答和盲运行冻结前不要打开[[阶段测验解答 - 信息论与统计学习接口（10.6）]]。

### OPT-CUM-01 的状态边界

OPT-CUM-01 是 210 分钟、100 分的闭卷卷末测验，覆盖 OPT-01—16，并设置 A—E 分区线、三道主证明不得为零和 strict-saddle–PL–sharpness 三轨计算门。当前状态为 **regression-passed / not-attempted**：

- 十六套节点题共 240 题，题卷、逐题详解、答案/输出隔离与状态机已成稿；
- 四波独立解析、canonical 双跑、盲参 SVG/hash 与六个状态入口已由[[optimization_cumulative_contract_audit.py]]回归，但只证明工具可执行；
- 尚无首次口试/闭卷原稿、`scorer nonce` 随机轨、个人新 output/hash、48 小时换机制和 14 天陌生 AI 迁移证据；
- 因而优化卷 16 个节点全部保持 `draft`；正式作答前不要打开[[阶段测验解答 - 优化与凸分析（10.7）]]。

### MATH-FND-CAP-01 的状态边界

MATH-FND-CAP-01 是30分钟口试加两个180分钟session、100分的十卷总出口，只检查跨卷接缝，不替代150节点的分卷覆盖。当前状态为材料 **regression-passed** / 个人 **not-attempted**：

- [[数学基础十卷总验收 - 跨卷理论与 AI 迁移]]按 object/evidence、跨卷手算、统一证明、AI 系统审计与研究合同五区评分；
- [[数学基础十卷总验收解答 - 跨卷理论与 AI 迁移]]提供完整推导和跨卷错题路由；
- [[实验 - 数学基础十卷跨章累计复现门]]参数化连接linear-Gaussian-information、quadratic optimization/discrete dynamics与circle geometry/RKHS/numerics，并由scorer nonce指定主轨与三系统盲参；
- [[math_foundations_capstone_contract_audit.py]]已复核11/11题解与100分、十份分卷材料审计、六个状态面、canonical双跑、覆盖保护、固定三轨盲参stdout/SVG/hash与图—数自描述；
- 三条主证明、三个系统案例、随机实验轨、48 小时重做、14 天迁移与口头答辩均有独立底线；
- 十份分卷累计测验未全部通过前，本卷只能用于诊断，不能用于总认证。

## 掌握与状态升级

基础概念或定理升级为 `verified` 前，应至少存在：

1. 一份链接到该节点的 A–E 习题集；
2. 一份经过核对的完整解答；
3. 至少一个可以手算到底的正文例子；
4. 对核心公式的维度/边界检查。

升级为 `mature` 前，还应在后续节点或阶段测验中再次被调用，证明不是短期记忆。

## 错题复盘

错题记录不只写“算错了”。必须判断错误类型：

| 类型 | 诊断问题 |
|---|---|
| 定义 | 是否把两个相近概念混用？ |
| 对象 | 是否弄错向量所在空间或矩阵形状？ |
| 条件 | 是否漏掉满秩、正定、谱间隙等假设？ |
| 推导 | 哪个等号没有依据？ |
| 计算 | 是符号、算术还是顺序错误？ |
| 数值 | 是否把数学公式直接当作稳定算法？ |
| 迁移 | 是否把线性结论扩大到非线性模型？ |

复盘结果应回链到具体知识节点的小节，而不是只链接整个章节。

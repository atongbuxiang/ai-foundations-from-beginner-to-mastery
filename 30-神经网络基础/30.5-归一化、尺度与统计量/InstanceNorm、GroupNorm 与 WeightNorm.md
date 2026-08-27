---
type: concept
status: draft
area: [neural-networks/normalization, vision, parameterization]
aliases: [IN GN WN, Normalization Family Taxonomy]
node_id: NN-38
prerequisites: ["[[归一化的对象、轴与不变性]]", "[[LayerNorm 的逐样本几何与反向传播]]", "[[参数对称性、等价表示与可辨识边界]]"]
related: ["[[RMSNorm、均值移除与缩放不变性]]", "[[小批量、混合精度、分布式与因果归一化边界]]", "[[正交初始化与 Dynamical Isometry]]"]
sources: ["[[S-2016-Ulyanov-Vedaldi-Lempitsky-InstanceNorm]]", "[[S-2018-Wu-He-GroupNorm]]", "[[S-2016-Salimans-Kingma-WeightNorm]]", "[[S-2026-PyTorch-Normalization-Systems]]"]
exercises: ["[[习题 - InstanceNorm、GroupNorm 与 WeightNorm]]"]
solutions: ["[[解答 - InstanceNorm、GroupNorm 与 WeightNorm]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-normalization-family-axis-lattice-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# InstanceNorm、GroupNorm 与 WeightNorm

> [!abstract] 本章主问题
> InstanceNorm 与 GroupNorm 改变 activation statistics 的分组轴；WeightNorm 则根本不估计 activation statistics，而是把权重向量重参数化为长度与方向。只有同时写出统计组、affine sharing、state 和参数对象，才能避免把三个同名为“Norm”的方法误当成一条连续刻度。

## 一、学习目标

读完本节，你应能：

1. 对 $(N,C,H,W)$ 精确写出 IN/GN 的归约集合与参数 shape；
2. 手算同一小张量在 IN 与 GN 下的不同输出；
3. 解释 GN 的 $G=1$、$G=C$ 只在哪些意义下对应 LN/IN；
4. 推导 WeightNorm 的 $d g,d\boldsymbol v$；
5. 区分 activation normalization、weight reparameterization 与 spectral constraint；
6. 比较 batch dependence、state、通信、train/eval 与因果语义；
7. 解释 IN 的风格化动机和 GN 的小 batch 动机为何都是条件性经验；
8. 审计 group divisibility、degenerate group、affine defaults 与部署物化。

## 二、先固定卷积张量布局

本节默认

$$
X\in\mathbb R^{N\times C\times H\times W}.
$$

对任一 activation normalization，先定义索引

$$
i=(n,c,h,w).
$$

每个输出位置 $i$ 对应一个统计集合 $S_i$。共同模板为

$$
\mu_i=\frac1{|S_i|}\sum_{k\in S_i}X_k,
$$

$$
q_i=\frac1{|S_i|}\sum_{k\in S_i}(X_k-\mu_i)^2,
$$

$$
Y_i=\gamma_i\frac{X_i-\mu_i}{\sqrt{q_i+\varepsilon}}+\beta_i.
$$

BN、IN、GN、LN 的公式外壳相似，但 $S_i$ 与 $\gamma_i,\beta_i$ 的 sharing 完全不同。

## 三、InstanceNorm：固定样本与 channel

对固定 $(n,c)$，InstanceNorm2d 取

$$
S_{nc}
=\{(n,c,h,w):1\le h\le H,1\le w\le W\}.
$$

于是

$$
\mu_{nc}=\frac1{HW}\sum_{h,w}X_{nchw},
$$

$$
q_{nc}=\frac1{HW}\sum_{h,w}(X_{nchw}-\mu_{nc})^2.
$$

核心性质：

- 不跨样本；
- 不跨 channel；
- 同一 channel 的所有空间位置共享统计量并相互耦合；
- 常见 affine 若开启，是 per-channel $\gamma_c,\beta_c$；
- 是否维护 running statistics 是实现选项，不由“InstanceNorm”名称唯一决定。

访问日 PyTorch 2.13 `InstanceNorm2d` 使用 biased variance，默认

```text
affine = false
track_running_stats = false
```

因此默认 train/eval 都用当前 instance statistics；若显式打开 state，eval 路径就会改变。

## 四、为什么风格化会想到 InstanceNorm

快速风格化论文的经验动机是：每张图、每个 feature channel 的空间均值与尺度携带一部分 instance-specific contrast/statistics；将它们标准化可改变生成器对内容与风格统计的处理。

但应严格区分：

- 数学事实：IN 删除每个 $(n,c)$ 组的共同空间 shift 与近似 scale；
- 经验事实：原论文的特定风格化网络质量改善；
- 非结论：IN 对分类、检测、医学强度定量或任意生成任务都更好。

若绝对亮度、强度或对比度本身是标签信号，IN 可能删除任务需要的信息。

## 五、GroupNorm：固定样本与 channel group

设 $G$ 是 group count，要求

$$
G\mid C.
$$

每组 channel 数为

$$
C_g=\frac CG.
$$

令

$$
g(c)=\left\lfloor\frac{c}{C_g}\right\rfloor
$$

（这里把 channel 从 0 编号）。固定 $(n,g)$，统计组为

$$
S_{ng}
=\{(n,c,h,w):g(c)=g\}.
$$

名义组大小

$$
m=C_gHW.
$$

GN 在组内 channels 与空间位置上联合计算均值方差，但 affine 通常仍是 per-channel：

$$
\gamma,\beta\in\mathbb R^C.
$$

访问日 PyTorch 2.13 GroupNorm 使用 biased variance，train/eval 都从当前输入计算 statistics，不维护 running buffers。

## 六、同一张量的 IN/GN 手算

取 $N=1,C=4,H=1,W=2$，省略 $n,h$，四个 channels 为

$$
X_1=(1,3),\quad
X_2=(5,7),\quad
X_3=(2,2),\quad
X_4=(0,4),
$$

并令 $\gamma=1,\beta=0,\varepsilon=0$。

### 6.1 InstanceNorm

前两个 channel 各自中心化：

$$
(1,3)\mapsto(-1,1),
$$

$$
(5,7)\mapsto(-1,1).
$$

$X_3$ 方差为 0，在 $\varepsilon=0$ 未定义；若 $\varepsilon>0$，输出为 $(0,0)$。

对 $X_4$：

$$
(0,4)\mapsto(-1,1).
$$

### 6.2 GroupNorm，$G=2$

第一组包含 $X_1,X_2$，四个数是

$$
(1,3,5,7).
$$

有

$$
\mu=4,
\qquad
q=\frac{9+1+1+9}{4}=5,
$$

所以

$$
(1,3,5,7)
\mapsto
\frac1{\sqrt5}(-3,-1,1,3).
$$

第二组包含

$$
(2,2,0,4),
$$

有

$$
\mu=2,
\qquad
q=2,
$$

所以

$$
(2,2,0,4)
\mapsto
(0,0,-\sqrt2,\sqrt2).
$$

同一输入、同一外壳公式，仅因统计组不同就得到不同函数。GN 还让同组不同 channels 在反向中密集耦合。

## 七、GN 的两个极端：只谈“统计核心等价”

### 7.1 $G=C$

每组一个 channel，归约 $(H,W)$，与 InstanceNorm 的统计核心相同。但完整模块仍可能不同：

- GN 默认 affine 开启，IN2d 默认关闭；
- GN 没有 running-state 选项，IN 可开启；
- 参数初始化与 API 形状约定可能不同。

### 7.2 $G=1$

每个样本把 $(C,H,W)$ 联合归约，与 LayerNorm$((C,H,W))$ 的统计核心相同。但：

$$
\text{GN affine shape}=(C),
$$

$$
\text{LN affine shape}=(C,H,W).
$$

所以二者参数量、空间位置共享和表达能力不同。只有关闭 affine，或让 LN affine 被约束为每 channel 共享时，完整算子才进一步接近。

## 八、组大小与退化

对 centered normalization，若每组只有一个标量，

$$
\mu=x,\qquad q=0,\qquad \widehat x=0.
$$

所以需要检查实际组大小

$$
m=C_gHW,
$$

而不是只看 $G$。当 $H=W=1$ 且 $G=C$，每组大小 1，GN core 会删除全部 activation；这与“GroupNorm 不依赖 batch size”是不同问题。

小 $m$ 还意味着：

- 可保留切向自由度 $m-2$ 很少；
- epsilon 对几何影响更大；
- 组内 outlier 影响所有成员；
- channel grouping 的排列选择更重要。

## 九、WeightNorm：对象已经换成参数

对一条权重向量

$$
\boldsymbol v\in\mathbb R^d\setminus\{0\},
\qquad
g\in\mathbb R,
$$

定义

$$
\boxed{
\boldsymbol w
=g\frac{\boldsymbol v}{\|\boldsymbol v\|_2}
}.
$$

它不读取当前 batch、instance、token 或空间位置的 activation statistics。forward 中只从参数 $g,v$ 物化有效权重 $w$，然后执行原层运算。

因此 WeightNorm：

- 没有 train/eval 统计路径差异；
- 不引入样本 companions；
- 不保证 activation 均值/方差；
- 不等于把完整矩阵的 spectral norm 固定；
- 改变优化坐标与 optimizer state 的含义。

## 十、WeightNorm 梯度推导

令

$$
r=\|\boldsymbol v\|_2,
\qquad
\boldsymbol u=\frac{\boldsymbol v}{r},
\qquad
\boldsymbol w=g\boldsymbol u.
$$

对 $\boldsymbol u$：

$$
d\boldsymbol u
=\frac1r
\left(I-\boldsymbol u\boldsymbol u^{\mathsf T}\right)d\boldsymbol v.
$$

设

$$
\boldsymbol s=\nabla_{\boldsymbol w}L.
$$

由

$$
d\boldsymbol w=\boldsymbol u\,dg+g\,d\boldsymbol u
$$

和内积配对得到

$$
\boxed{
\frac{\partial L}{\partial g}
=\boldsymbol s^{\mathsf T}\boldsymbol u
},
$$

$$
\boxed{
\nabla_{\boldsymbol v}L
=\frac g r
\left(I-\boldsymbol u\boldsymbol u^{\mathsf T}\right)\boldsymbol s
}.
$$

检查：

$$
\boldsymbol v^{\mathsf T}\nabla_{\boldsymbol v}L=0.
$$

也就是说 $v$ 的梯度位于球面切空间；径向大小由 $g$ 独立控制。

## 十一、WeightNorm 手算

取

$$
\boldsymbol v=(3,4),
\qquad
g=10,
\qquad
\boldsymbol s=(1,2).
$$

则

$$
r=5,
\quad
\boldsymbol u=\left(\frac35,\frac45\right),
\quad
\boldsymbol w=(6,8).
$$

尺度梯度

$$
\frac{\partial L}{\partial g}
=\frac35+\frac85
=\frac{11}{5}.
$$

投影前

$$
\boldsymbol u^{\mathsf T}\boldsymbol s=\frac{11}{5},
$$

所以

$$
\left(I-uu^{\mathsf T}\right)s
=(1,2)-\frac{11}{5}\left(\frac35,\frac45\right)
=\left(-\frac8{25},\frac6{25}\right).
$$

乘 $g/r=2$：

$$
\boxed{
\nabla_vL
=\left(-\frac{16}{25},\frac{12}{25}\right)
}.
$$

代回

$$
(3,4)\cdot\left(-\frac{16}{25},\frac{12}{25}\right)=0.
$$

## 十二、WeightNorm 的 gauge 与有效步长

对任意 $a>0$，

$$
g\frac{a\boldsymbol v}{\|a\boldsymbol v\|}
=g\frac{\boldsymbol v}{\|\boldsymbol v\|}.
$$

所以 $v$ 的正尺度不可辨识。与此同时

$$
\nabla_{a\boldsymbol v}L
=\frac1a\nabla_{\boldsymbol v}L.
$$

若直接对 $v$ 使用固定学习率，方向角的实际变化还会随 $\|v\|$ 改变。weight decay 若作用于 $v$，也不同于直接对有效权重 $w$ 做普通 L2 penalty。优化器、parametrization 和 regularization 必须作为整体审计。

## 十三、统一比较表

| 方法 | 被操作对象 | 统计/范数组 | 跨样本 | running state | affine/参数 | 核心删除方向 |
|---|---|---|---|---|---|---|
| BatchNorm train | activation | 固定 channel，归约 $N,H,W$ | 是 | 常有 | per-channel | 组平移、近径向 |
| InstanceNorm | activation | 固定 $n,c$，归约 $H,W$ | 否 | 可选 | 常为 per-channel | 空间平移、近径向 |
| GroupNorm | activation | 固定 $n,g$，归约 $C/G,H,W$ | 否 | 无 | per-channel | 组平移、近径向 |
| LayerNorm | activation | 固定 token，归约 $D$ | 否 | 无 | per-element gain+bias | feature 平移、近径向 |
| RMSNorm | activation | 固定 token，归约 $D$ | 否 | 无 | per-element gain | 近径向 |
| WeightNorm | weight | 每条 weight vector | 不适用 | 无统计 state | magnitude+direction | 参数径向 gauge |

“跨样本否”不等于“没有组内耦合”；IN/GN/LN/RMS 都会在各自组内产生 dense Jacobian。

## 十四、复杂度、通信与部署

### 14.1 IN/GN

它们不跨 batch/device 归约，天然避免 SyncBN collective；但仍需要：

- 读 activation；
- 计算组均值/方差；
- 再次读或缓存 centered values；
- 应用 per-channel affine。

组布局不连续时可能影响 kernel 合并。$G$ 过多会减少每组工作量，增加 reduction overhead 与小组退化风险。

### 14.2 WeightNorm

训练时有效权重可能在每次访问时重算。访问日 PyTorch 新 parametrization API 与旧 hook 语义不同；若一个 forward 多次读取 weight，是否缓存会影响成本。部署时可把当前有效 $w$ 物化并移除 parametrization，但这会失去后续 $g/v$ 分离训练语义。

## 十五、图：轴谱系与对象分叉

先看图回答：哪些方法只是改变 activation 的统计组，哪个方法已经把对象换成 weight parameter？GN 的两个极端为什么只能先说“统计核心对应”？

![[00-知识库管理/_assets/figures/neural-networks/fig-normalization-family-axis-lattice-v2.svg|900]]

> [!figure] 图 30.5-06　IN/GN/LN 的轴格与 WeightNorm 参数几何
> 左栏在 $N,C,H,W$ 格上标出 BN、IN、GN 的固定轴与归约轴；中栏把 GN 从 $G=1$ 到 $G=C$ 的统计核心连续关系与 affine/state 陷阱并列；右栏把 WeightNorm 画成 $v$ 的球面方向和独立 magnitude $g$，明确它不读取 activation group。来源：依据 Ulyanov–Vedaldi–Lempitsky 2016、Wu–He 2018、Salimans–Kingma 2016 与本节推导独立绘制；由 [[00-知识库管理/_labs/code/plot_normalization_advanced_v2.py]] 确定性生成。

**怎样读图**：先沿左栏问“谁和谁共享统计量”，再沿中栏检查统计核心与参数合同是否同时相同，最后确认 WeightNorm 的箭头只作用于参数而非数据轴。

**图没有证明什么**：图没有证明某个 group count 最优，也没有证明风格化、小 batch 或 WeightNorm 的论文结果可迁移到所有任务；这些是受控实验问题。

## 十六、选择协议

选择前至少回答：

1. 需要删除的是跨 batch、空间、channel-group、feature 还是 weight radial 尺度？
2. 绝对均值/对比度是否含标签信息？
3. 实际组大小 $m$ 是否足够，是否出现 $m=1/2$？
4. 是否允许跨样本/跨设备依赖？
5. train/eval 是否必须完全同统计路径？
6. affine 参数应按 channel 还是按 element 共享？
7. 模型是否需要运行状态、流式处理或 batch-independent inference？
8. 优化器与 weight decay 作用在原参数还是重参数坐标？

## 十七、最小验收

1. 在 $(N,C,H,W)$ 上写出 IN/GN 每个统计组；
2. 完成四 channel 手算；
3. 让 $G=1,C$ 并核对 affine/state 差异；
4. 构造 $m=1$ 退化；
5. finite difference 验证 WeightNorm $dg,dv$；
6. 检查 $v^{\mathsf T}dv=0$；
7. 改变另一 batch 样本，确认 IN/GN 不变；
8. 改变同组另一个 channel，确认 GN 输出改变；
9. 记录框架 defaults，而非只写模块名；
10. 比较 kernel、通信、参数与 state 成本。

> [!summary]
> IN 与 GN 是 activation group geometry；WeightNorm 是 parameter geometry。GN 在统计轴上连接 LN 与 IN，但完整等价还要求 affine/state 合同相同。任何选择都必须从“对象是谁、共享集合是什么、删除哪条方向”开始。

- [[归一化、尺度与统计量 MOC]]
- [[习题 - InstanceNorm、GroupNorm 与 WeightNorm]]
- [[解答 - InstanceNorm、GroupNorm 与 WeightNorm]]

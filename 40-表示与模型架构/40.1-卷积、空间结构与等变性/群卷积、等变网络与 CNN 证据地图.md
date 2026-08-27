---
type: concept
status: draft
area: [architecture, cnn, group-equivariance, evidence]
aliases: [G-CNN, 群等变卷积网络]
node_id: ARCH-08
prerequisites: ["[[局部连接、参数共享与平移等变性]]", "[[Lie 群、Lie 代数与对称性]]", "[[数据增强、不变性、等变性与任务充分性]]"]
related: ["[[图数据、节点重标号与置换对称性]]", "[[RoPE 的旋转推导、群表示与内积]]", "[[置换对称性与位置编码的必要性]]"]
sources: ["[[S-2016-Cohen-Welling-GCNN]]", "[[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]"]
exercises: ["[[习题 - 群卷积、等变网络与 CNN 证据地图]]"]
solutions: ["[[解答 - 群卷积、等变网络与 CNN 证据地图]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-group-equivariance-evidence-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# 群卷积、等变网络与 CNN 证据地图

> [!abstract] 本节主问题
> 普通 convolution 把整数平移对称性写进参数共享；group convolution 把这一思想推广到选定群的作用。网络中间 feature 不必对旋转/反射保持不变，而应以已知方式变换。精确等变性是结构恒等式；样本效率、表达能力和任务性能则需要附加定理与实验，不能越级推断。

## 一、先确认任务对称性

群 $G$ 的元素表示可组合变换，满足单位、结合、逆。它作用在输入 $x$ 上为 $T_gx$。轨道

$$
\operatorname{Orb}(x)=\{T_gx:g\in G\}
$$

收集同一对象的所有允许变换。

但“允许”来自任务：旋转手写数字 6 可能变成 9，方向在航拍图和普通街景中的语义不同。把错误 symmetry 硬编码会造成 bias mismatch。

## 二、普通卷积已经是群卷积原型

在离散平移群 $\mathbb Z^2$ 上，feature $f:\mathbb Z^2\to\mathbb R^C$。相关

$$
(f\star\psi)(u)=\sum_v f(v)\psi(v-u)
$$

用相对位移共享 filter。平移输入导致输出平移，正是 group action 上的等变。

Group convolution 的核心不是把 group 作为额外标签，而是让 filter 在 group orbit 上按一致规则变换/共享。

## 三、从图像到 Group Feature Map

第一层 lifting convolution 可把平面图像变成定义在群元素上的 feature：

$$
F(g)=\langle x,T_g\psi\rangle.
$$

$F(g)$ 表示模板 $\psi$ 在变换 $g$ 下与输入的匹配。若 $G$ 包含位置和离散旋转，feature map 多一个 orientation 轴；旋转输入不是让 feature 值保持不变，而是重排位置/方向索引。

## 四、等变证明的换元骨架

设左作用 $[L_hf](g)=f(h^{-1}g)$，group correlation

$$
(f\star\psi)(g)=\sum_{u\in G}f(u)\psi(g^{-1}u).
$$

对输入变换：

$$
((L_hf)\star\psi)(g)
=\sum_u f(h^{-1}u)\psi(g^{-1}u).
$$

令 $v=h^{-1}u$，即 $u=hv$：

$$
=\sum_v f(v)\psi(g^{-1}hv)
=(f\star\psi)(h^{-1}g)
=[L_h(f\star\psi)](g).
$$

因此算子与左作用 commute。有限/紧群的 sum/integral、measure 和 inverse convention 必须一致。

## 五、从 Equivariance 到 Invariance

若最终任务不关心 $g$，可在 group axis 上求和/平均/max：

$$
r(f)=\sum_{g\in G}f(g).
$$

群作用只重排索引，sum 不变。若任务要预测姿态，则不应过早 pool group axis；等变 feature 保留“怎么变”的信息，供 equivariant output head 使用。

## 六、离散旋转与连续旋转

[[S-2016-Cohen-Welling-GCNN]]重点讨论由平移、反射和离散旋转生成的群，能够通过 transformed filters 实现。对连续 $SO(2)/SO(3)$，还需 steerable filters、representation decomposition、integration/采样与数值离散化。90° 格点旋转可精确重排像素，任意角旋转通常需要插值，精确等变会受 discretization 影响。

## 七、参数、计算与 Feature Size

更强 weight sharing 可在固定参数下产生多个 orientation responses；但 feature map 的 group axis 扩大，activation 和算术可能随 $|G|$ 增长。论文中的 “不增加参数” 不等于不增加 FLOPs/内存。

还需区分：filter 参数是否按 orbit tying、输出 orientation 数、group pooling 位置、channel budget 是否匹配。

## 八、Augmentation 与 Equivariance

| 数据增强 | 等变架构 |
|---|---|
| 用更多变换样本鼓励经验一致 | 函数类/层结构满足精确或近似关系 |
| 可覆盖非群随机扰动 | 需明确闭合的群/半群作用 |
| 不保证未见变换精确关系 | 在设计域内有结构保证 |
| 增加训练数据/计算 | 增加特征 group axis/算子复杂度 |

二者可组合：架构编码已知 symmetry，augmentation 处理噪声、离散误差和未建模变化。

## 九、证据地图

1. `I`：group convolution 满足等变恒等式；
2. `T`：在指定函数类/分布下的表达或样本复杂度结果；
3. `E`：rotated MNIST、CIFAR 等特定实验；
4. `H`：性能提升源于参数共享/优化/regularization 的解释；
5. `O`：真实数据近似 symmetry、连续群离散化、规模化效率。

Cohen–Welling 原论文报告离散群上的实现与实验，但不能单独证明所有旋转任务或现代大规模模型都会获益。

## 十、图：Orbit、交换图与证据阶梯

先看图回答：旋转输入后，中间 feature 应保持数值不动，还是沿 orientation axis 重排？

![[00-知识库管理/_assets/figures/architecture/fig-group-equivariance-evidence-v1.svg|900]]

> [!figure] 图 40.1-08　群轨道、等变交换图与证据层级
> 左栏把离散旋转组成 orbit；中栏强调输入作用 $T_g$ 与 feature 作用 $S_g$ 的相容；右栏分开 identity、theorem、experiment 与 hypothesis/open question。来源：依据 Cohen–Welling 2016 和群作用定义独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_convolution_advanced_v1.py]] 生成。

**怎样读图**：先确定 $G$ 与 action，再检查交换图，最后才讨论数据集性能。Orientation response 的重排正是等变，而非失败。

**图没有证明什么**：它不证明任务标签对整个群不变，不证明插值后的连续旋转精确等变，也不证明参数不变意味着计算不变。

## 十一、失败与反例

- label 非不变：6/9、文字方向、医学左右侧；
- boundary/crop：变换后内容离开画布；
- discretization：45° rotation 需插值；
- approximate symmetry：光照、透视不构成简单有限群；
- output type 错配：姿态估计需要等变向量，不是 invariant scalar；
- system cost：group feature 带来较大 activation/通信。

## 十二、40.1 卷证据总览

| 结论 | 证据等级 |
|---|---|
| correlation/shape/RF 递推 | exact algebra `I` |
| 共享 stride1 卷积平移等变 | theorem/identity `T/I` |
| 下采样引发 aliasing | sampling theory `T` |
| ERF 常中心集中 | 条件分析 + experiment `T/E` |
| anti-aliasing/GCNN 提升具体任务 | experiment `E` |
| 原因是更好 bias/regularization | interpretation `H` |
| 哪种 symmetry/blur 在大模型最优 | open/setting-dependent `O/E` |

## 十三、常见错误

1. 未定义 group/action 就声称等变；
2. 把 invariant 与 equivariant 混用；
3. 把 group pooling 放太早；
4. 忽略 inverse、left/right action 和 measure convention；
5. 把离散 90° 结果外推任意角；
6. 参数相同就声称成本相同；
7. 用 augmentation 结果冒充结构恒等式；
8. 把 benchmark 提升升级为普遍样本复杂度定理。

## 十四、回顾与掌握标准

> [!summary]
> - 普通 convolution 是平移群上的等变共享；
> - group feature map 的索引随输入变换重排；
> - 换元证明依赖正确 left/right action 与共享规则；
> - invariant readout 与 equivariant hidden representation 服务不同任务；
> - 结构、理论、实验和解释必须分层。

## 十五、练习与独立详解

- [[习题 - 群卷积、等变网络与 CNN 证据地图]]
- [[解答 - 群卷积、等变网络与 CNN 证据地图]]

## 参考来源

- [[S-2016-Cohen-Welling-GCNN]]
- [[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]

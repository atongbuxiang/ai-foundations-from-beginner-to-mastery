---
type: method
status: verified
area: [training, optimization, tensor-programs, infinite-width, validation]
node_id: TRN-44
aliases: [Tensor Programs 与 Coord Check, Coordinate Check]
prerequisites: ["[[μP 的 Maximal Update 与宽度尺度推导]]", "[[期望、方差与矩]]", "[[协方差、相关性与条件期望]]"]
related: ["[[μTransfer、Base Shape 与超参数零样本迁移]]", "[[Scale-up 协议、μP 证据与失效边界]]", "[[NTK、Lazy Training 与 Kernel Regime]]"]
sources: ["[[S-2020-Yang-Tensor-Programs-II-NTK]]", "[[S-2021-Yang-Littwin-Tensor-Programs-IIb]]", "[[S-2021-Yang-Hu-Feature-Learning]]", "[[S-2022-Yang-Tensor-Programs-V-MuTransfer]]", "[[S-2026-Microsoft-MuP-Implementation]]"]
exercises: ["[[习题 - Tensor Programs、坐标检查与无限宽极限]]"]
solutions: ["[[解答 - Tensor Programs、坐标检查与无限宽极限]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-tensor-program-coordinate-check-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Tensor Programs、坐标检查与无限宽极限

> [!abstract] 一句话结论
> Tensor Programs 把宽网络的矩阵乘、逐坐标非线性、转置复用与训练更新写成可追踪的程序，从而计算坐标分布和 covariance 的极限；coordinate check 则在有限宽实现中检查这些坐标统计是否随 width 趋于稳定。前者是带假设的渐近理论，后者是诊断实验，二者都不是对具体大模型正确性的单独证书。

## 一、为什么只做方差传播不够

最简单的宽层

$$
z^\ell=W^\ell h^{\ell-1},
\qquad h^\ell=\phi(z^\ell)
\tag{1}
$$

可在独立初始化下递推方差。但现代网络会出现：

- 同一权重在 forward 与 backward 以 $W$、$W^\top$ 重复使用；
- residual、normalization、attention 和 weight sharing；
- 多个输入之间的 joint covariance；
- 参数更新依赖此前 activation 与 gradient；
- 训练多步后权重不再独立于特征。

若每次看到 $W^\top$ 就把它当一张新的独立 Gaussian matrix，会得到错误答案。Tensor Programs 的价值是把“哪些量由哪些随机矩阵生成、哪些依赖被保留”编码进同一个程序。

## 二、从一层 covariance recursion 入门

取两个输入 $x,x'$，宽度为 $n$，

$$
z_i(x)=\frac{\sigma_w}{\sqrt n}
\sum_{j=1}^nW_{ji}h_j(x)+b_i.
\tag{2}
$$

假设 $W_{ji}$ 独立标准化，且上一层坐标经验二阶矩收敛：

$$
\frac1n\sum_{j=1}^n
h_j(x)h_j(x')
\to Q(x,x').
\tag{3}
$$

条件在 $h$ 上，

$$
\operatorname{Cov}\bigl(z_i(x),z_i(x')\mid h\bigr)
=\frac{\sigma_w^2}{n}
\sum_jh_j(x)h_j(x')+\sigma_b^2.
\tag{4}
$$

于是极限 covariance 为

$$
\Sigma_z(x,x')
=\sigma_w^2Q(x,x')+\sigma_b^2.
\tag{5}
$$

通过逐坐标非线性，下一层二阶对象为

$$
Q^+(x,x')
=\mathbb E_{(u,v)\sim\mathcal N(0,\Sigma)}
[\phi(u)\phi(v)].
\tag{6}
$$

这里不是只追一个 variance，而是追所有 probe 输入之间的 covariance。更一般的 Tensor Program master theorem 让许多坐标经验平均收敛到由这类 Gaussian expectations 计算的极限。

## 三、一个 Tensor Program 合同要记录什么

不必先掌握全部形式语言，也能使用四栏抽象：

| 程序对象 | 神经网络含义 | 审计问题 |
|---|---|---|
| 宽向量变量 | activation、preactivation、gradient | 坐标数随哪个 width 增长？ |
| 随机矩阵乘 | linear/conv/attention projection | 矩阵是否复用或转置？ |
| 逐坐标函数 | activation、部分 normalization/gating | 是否满足矩与增长条件？ |
| 经验平均 | covariance、loss、readout | 是 LLN 平均还是相关和？ |

再加 shape ratios、初始化 law、固定参数、训练 step 和 optimizer state。这样才能判断某个 theorem 是否覆盖当前程序。

## 四、GIA：最危险的独立性捷径

反向传播常含

$$
\delta^{\ell-1}=W^\ell\delta^\ell\odot\phi'(z^{\ell-1})
\tag{7}
$$

或转置约定下的等价式。朴素计算可能把 backward 中的 $W^\ell$ 与 forward 生成 $z^\ell$ 时的同一 $W^\ell$ 当独立，这称 gradient independence assumption（GIA）式捷径。

[[S-2020-Yang-Tensor-Programs-II-NTK]] 给出 Simple GIA Check 来识别一类捷径何时给出正确极限，并展示失败时可能算错。课程中的操作原则是：

1. 标记每张参数矩阵的所有 forward/backward usages；
2. 标记 transpose、weight tying 与 recurrent reuse；
3. 若不能满足已验证的结构检查，就保留 joint dependence，不做“新采样矩阵”替换；
4. 用小网络 Monte Carlo 验证 covariance 公式，但不把数值符合当证明。

## 五、无限宽结论的五个常见量词门

一条定理通常只覆盖其中一个明确版本：

### 1. 固定深度

先固定 layer/block 数 $L$，再令各 width 变大。若 $L=L(n)$，需要新的 uniform control。

### 2. 固定比例宽度

多个 hidden width 按

$$
n_\ell/n\to\gamma_\ell\in(0,\infty)
\tag{8}
$$

共同增长。极端 aspect ratio 可能改变极限。

### 3. 固定有限训练步

对任意固定 $T$ 证明 $t\le T$ 的极限，不自动允许 $T=T(n)\to\infty$。

### 4. 有限 probe set

对有限个输入的 joint law 收敛，不自动给所有输入上一致函数逼近。

### 5. 收敛模式

几乎处处、概率、分布、矩或经验平均收敛不同；它们不能无条件交换非线性、最大值和训练极限。

> [!warning] 标题中的“任意架构”
> 应读作论文形式系统覆盖的一大类架构，而不是“任何未来代码都自动满足”。离散 top-k routing、数据依赖控制流、非标准共享、动态 shape、量化和长时训练都需要重新匹配假设。

## 六、Coordinate Check：把渐近期望变成实现诊断

[[S-2026-Microsoft-MuP-Implementation]] 当前把 coordinate check 类比为 gradient check：对多个宽度和少量训练步，记录每层 activation/output 坐标的平均绝对值或其他坐标统计。

### 最小流程

1. 选择宽度网格，例如 $n\in\{64,128,256,512,1024\}$；
2. 固定 depth、数据 batch、随机流和除 width 外的 family；
3. 对每个宽度正确设置 base/delta shape 与 μP optimizer；
4. 记录 $t=0,1,2,4,8$ 的 activation statistics；
5. 多 seed 重复，保存每条原始曲线和失败运行；
6. 在 log–log 上检查水平趋势、弯曲、爆炸和消失。

可用统计包括

$$
m_1(h)=\frac1n\sum_i|h_i|,
\qquad
m_2(h)=\sqrt{\frac1n\sum_ih_i^2},
\tag{9}
$$

$$
m_4(h)=\left(\frac1n\sum_i|h_i|^4\right)^{1/4}.
\tag{10}
$$

$m_1$ 较稳健，$m_2$ 对方差敏感，$m_4$ 更容易暴露 heavy tail，但 seed variance 更大。只检查 $m_1$ 可能漏掉稀有大坐标。

### 斜率与容忍区间

对层 $\ell$、时刻 $t$ 拟合

$$
\log m_{p,\ell,t}(n)
=c_{\ell,t}+\kappa_{\ell,t}\log n+\epsilon.
\tag{11}
$$

若预期 coordinate stable，则 $\kappa\approx0$。预注册门可以是：

$$
|\widehat\kappa_{\ell,t}|\le\kappa_{max}
\quad\text{且最宽/最窄统计比在指定区间内}.
\tag{12}
$$

阈值必须由宽度窗口、seed 数与任务风险确定，不能把 0.1 当通用常数。

## 七、初始化例外与训练后验收

当前实现文档指出，正确 μP 下 output 和 Transformer attention logits 在初始化时可能按 $1/\sqrt{width}$ 收缩，随后若干步转为近似水平；可用 zero-init readout/query 等约定消除部分瞬态。

因此 coordinate check 不应机械要求“所有层、所有时刻都水平”。应建立期望表：

| 对象 | $t=0$ 预期 | 训练后预期 | 失败模式 |
|---|---|---|---|
| hidden activation | 近似水平 | 近似水平 | 爆炸/消失 |
| hidden feature update | 未定义或 0 | 近似水平且非零 | lazy/爆炸 |
| readout logit | 可收缩/zero | 转为 $O(1)$ | 始终消失或迅速爆炸 |
| attention logit | 依 scaling/zero query | 规则内稳定 | softmax 饱和或无差异 |
| gradient/update | 角色特定斜率 | 与 exponent ledger 一致 | 参数组或方向写错 |

## 八、Coord Check 能发现什么、不能发现什么

### 能强力发现

- 漏设某个 infinite dimension；
- fan-in/fan-out 或矩阵方向写反；
- 忘用 `MuReadout` 或 μP-aware optimizer；
- scheduler 覆盖 refined group LR；
- attention scaling、weight tying 或 custom parameter 未处理；
- 某层 activation/update 随 width 爆炸/消失。

### 不能单独证明

- 超参数 optimum 必然迁移；
- 长时间训练稳定；
- depth、数据、batch、sequence 或 optimizer 改变仍成立；
- loss/泛化一定更好；
- kernel/feature regime 已被完整识别；
- 代码与某个形式定理完全等价。

所以 coord check 是 necessary-style implementation diagnostic，而非 sufficient certificate。

## 九、四层验证梯

建议把证据分成：

### T1 手推

对每个参数组写 init、gradient、direction、LR、update、feature exponent。

### T2 统计模拟

在不训练或一两步 toy network 上验证 covariance、RMS 与 operator trends。

### T3 实现坐标检查

在真实代码路径、多 width、多 seed 下记录 layerwise curves。

### T4 训练与迁移

比较 loss、失败率、最佳 HP drift、compute 和目标规模确认。

理论结论与工程结论必须在同一层比较。T3 通过不能代替 T4，T4 单个成功案例也不能证明 T1 的普遍定理。

## 十、图：从程序极限到有限宽证据

先看图回答：为什么一张“所有 activation 曲线都水平”的 coord-check 图仍不能宣布 μTransfer 成功？

![[00-知识库管理/_assets/figures/training-optimization/fig-tensor-program-coordinate-check-v1.svg|880]]

> [!figure] 图 TRN-44　Tensor Program 假设、Coordinate Law 与有限宽验证梯
> 左侧把矩阵复用、逐坐标函数、shape ratio 与训练时域写入程序合同；中间给出 covariance/coordinate law；右侧依次通过手推、统计模拟、coord check 和训练迁移四道门。来源：依据 [[S-2020-Yang-Tensor-Programs-II-NTK]]、[[S-2021-Yang-Littwin-Tensor-Programs-IIb]] 与 [[S-2026-Microsoft-MuP-Implementation]] 原创绘制。

**怎样读图**：先确认代码属于理论覆盖的程序与极限路径，再检查有限宽坐标曲线；只有最后再观察最优超参数位置和训练结果，才能讨论迁移。

**图没有证明什么**：水平曲线只说明所测统计在当前窗口没有明显 width drift，不证明所有矩、所有输入、长期训练或目标规模性能。

## 十一、常见错误

1. **把 $W^\top$ 当独立矩阵**：先做复用/GIA 审计；
2. **只测 $t=0$**：μP 关心训练更新，至少加入早期 steps；
3. **只测 output loss**：layer bug 可能被后层抵消；
4. **只用一个坐标矩**：加入 RMS、高阶矩或分位数；
5. **宽度网格太窄**：水平可能是有限窗口假象；
6. **不同 width 用不同数据**：混入 sample variation；
7. **把例外当 bug**：readout/attention init 需读具体合同；
8. **coord check 通过即“理论正确”**：仍需假设匹配和 T4。

## 十二、初学者自检

1. 式 (4) 怎样从上一层经验 covariance 得到下一层 Gaussian covariance？
2. GIA 为什么可能在有 transpose reuse 时失败？
3. 固定有限步极限为什么不覆盖 $T(n)\to\infty$？
4. $m_1$、$m_2$、$m_4$ 各更敏感于什么？
5. 哪些实现错误会让某层 coord curve 随 width 爆炸？
6. 为什么 coord check 是诊断而不是 μTransfer 的充分证书？

## 十三、本节出口

你应能为一个宽网络建立

$$
\text{program/limit assumptions}
\to \text{coordinate law}
\to \text{finite-width coord check}
\to \text{training/transfer evidence}
$$

四层验证链。下一节 [[μTransfer、Base Shape 与超参数零样本迁移]] 将把 base/delta/target shape oracle 与超参数搜索协议写成可执行合同。

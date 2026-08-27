---
type: concept
status: verified
area: [training, optimization, parameterization, scaling]
node_id: TRN-41
aliases: [模型尺度合同, Width-Depth Object Contract]
prerequisites: ["[[方差传播与宽层均值场近似]]", "[[反向梯度方差与 Fan-In_Fan-Out 权衡|反向梯度方差与 Fan-In/Fan-Out 权衡]]", "[[矩阵范数]]"]
related: ["[[Standard、NTK 与 Mean-field 参数化]]", "[[谱条件、高阶 μP 与参数更新稳定性]]", "[[Scale-up 协议、μP 证据与失效边界]]"]
sources: ["[[S-2021-Yang-Hu-Feature-Learning]]", "[[S-2022-Yang-Tensor-Programs-V-MuTransfer]]", "[[S-2025-Su-11340-MuP之上1]]", "[[S-2026-Su-11549-各向同性]]", "[[S-2021-Su-8620-Transformer初始化参数化与标准化]]"]
exercises: ["[[习题 - 模型尺度、稳定性指标与 Width-Depth 对象合同]]"]
solutions: ["[[解答 - 模型尺度、稳定性指标与 Width-Depth 对象合同]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-scale-axis-object-contract-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# 模型尺度、稳定性指标与 Width-Depth 对象合同

> [!abstract] 一句话结论
> “模型变大”不是一个数学操作。只有先声明**哪些维度怎样变化、哪些维度保持不变、在哪个训练时刻、观察哪个归一化对象、用什么概率量词判断稳定**，$O(1)$、无限宽、尺度迁移和训练稳定才是可检验的陈述。

## 一、先拆掉“模型大小”这个模糊词

初学者最容易把参数量 $N$ 当作模型规模的全部。对一个 Transformer，至少有下列互不等价的尺度轴：

$$
s=\bigl(
d_{model},d_{ff},h,d_h,L,V,S,B,T,D,C
\bigr).
\tag{1}
$$

它们依次可表示 model width、FFN width、head 数、head dimension、block depth、词表大小、序列长度、batch/token 数、优化步数、数据量和计算预算。还可能加入 MoE expert 数、active experts、rank、图像分辨率或状态维度。

参数量只是这些轴的复合函数。忽略 bias 和 norm，一个常见 dense Transformer block 的主导项可粗写为

$$
N_{block}
\approx 4d_{model}^{2}+2d_{model}d_{ff}.
\tag{2}
$$

若 $d_{ff}=rd_{model}$ 且 depth 为 $L$，则

$$
N\approx L(4+2r)d_{model}^{2}+Vd_{model}.
\tag{3}
$$

因此把 $N$ 增大四倍，可能是 $d_{model}$ 增大两倍，也可能是 $L$ 增大四倍，还可能是词表、expert 或未激活参数增加。它们的信号传播、优化、显存和统计效应完全不同。

> [!warning] 第一条审计规则
> 不接受“当模型规模 $N\to\infty$”而没有给出路径。应写成例如：$d_{model}=n$、$d_{ff}=4n$、$h$ 固定、$d_h=n/h$、$L=L_0$ 固定，令 $n\to\infty$；或写清 $L=L(n)$ 的联合极限。

## 二、一个极限陈述需要六栏合同

把任何尺度结论写成

$$
\mathcal C=(\text{family},\text{path},\text{time},\text{randomness},\text{object},\text{criterion}).
\tag{4}
$$

### 1. Family：比较的是不是同一个模型族

必须固定或版本化：

- block 公式、residual 路径与 normalization 位置；
- 激活函数、attention scaling 与 weight tying；
- optimizer、loss reduction、parameter grouping；
- 数据分布、tokenizer、训练目标和精度格式。

改了这些，往往不再只是“把同一个模型变宽”。

### 2. Path：各维度怎样一起变化

若有两层宽度 $n_1,n_2$，常见定理假设

$$
\frac{n_2}{n_1}\to\gamma\in(0,\infty).
\tag{5}
$$

这与先令 $n_1\to\infty$ 再令 $n_2\to\infty$、或令 $n_2=n_1^2$ 并不相同。width–depth 联合扩展还要写 $L(n)$，因为 residual increment 可能累积为 $L$ 倍或 $\sqrt L$ 倍。

### 3. Time：初始化还是训练后

至少区分

$$
t=0,\qquad t\in\{1,\ldots,T_0\},\qquad t=T(n),\qquad \text{收敛后}.
\tag{6}
$$

初始化方差稳定，不推出第一步更新稳定；固定有限步的无限宽定理，也不自动覆盖随宽度增长的训练时长。

### 4. Randomness：对什么取概率

随机性可能来自初始化、minibatch、数据顺序、dropout、路由和数值内核。以下量词不同：

$$
\mathbb E[Z_n]=O(1),\qquad
Z_n=O_p(1),\qquad
\Pr(|Z_n|\le C)\ge1-\delta,\qquad
\sup_n|Z_n|\le C.
\tag{7}
$$

期望有界允许罕见大值；$O_p(1)$ 表示 tightness；高概率界需要给出 $\delta$；确定性一致界最强。

### 5. Object：到底观察什么

常见对象至少分五层：

1. 参数坐标与参数范数；
2. pre-activation、activation 和 residual stream；
3. gradient、optimizer direction 与 parameter update；
4. feature update、logit update、loss change 与 NTK drift；
5. 失败率、训练速度和最终指标。

### 6. Criterion：什么叫“稳定”

“不爆炸”只给上界，不排除消失。非退化通常需要上下界：

$$
0<c\le \operatorname{scale}(Z_n)\le C<\infty.
\tag{8}
$$

写成 $Z_n=\Theta(1)$ 时，还要说明 scale 是 RMS、标准差、谱范数、分位数还是某个坐标。

## 三、坐标、向量与算子：三个 $O(1)$ 不能混

令 $x\in\mathbb R^n$，各坐标独立、均值 0、方差 1。则

$$
\operatorname{RMS}(x)
=\sqrt{\frac1n\sum_{i=1}^n x_i^2}
=\Theta_p(1),
\tag{9}
$$

但

$$
\lVert x\rVert_2
=\sqrt n\operatorname{RMS}(x)
=\Theta_p(\sqrt n).
\tag{10}
$$

所以“激活范数保持 $O(1)$”若指 Euclidean norm，与“每个坐标保持 $O(1)$”冲突。教材统一约定：

- `coordinate scale`：单坐标标准差或 RMS；
- `vector RMS`：$\lVert x\rVert_2/\sqrt n$；
- `operator scale`：$\lVert W\rVert_2$；
- `entry RMS`：$\lVert W\rVert_F/\sqrt{mn}$。

### 线性层的典型输入与最坏输入

取行向量约定

$$
y=xW,\qquad
x\in\mathbb R^{d_{in}},\quad
W\in\mathbb R^{d_{in}\times d_{out}}.
\tag{11}
$$

若 $W_{ij}$ 独立、均值 0、方差 $\sigma_W^2/d_{in}$，且 $x_i$ 独立、方差 $q$，则固定 $j$ 有

$$
\operatorname{Var}(y_j)
=\sum_{i=1}^{d_{in}}
\operatorname{Var}(x_iW_{ij})
=q\sigma_W^2.
\tag{12}
$$

这是**典型坐标二阶尺度**。另一方面，对任意输入扰动

$$
\lVert xW\rVert_2
\le \lVert x\rVert_2\lVert W\rVert_2,
\tag{13}
$$

这是**最坏方向的算子控制**。式 (12) 成立不代表式 (13) 的常数理想；反之谱范数有界也不告诉我们各坐标方差是否均匀。

## 四、三类稳定性要落成八个观测量

[[S-2025-Su-11340-MuP之上1]] 用 forward、dependence 与 update 三类稳定性组织问题。课程把它们落实为可测账本。

### 1. Forward stability

对层 $\ell$ 记录

$$
A_{\ell,t}
=\operatorname{RMS}(h_{\ell,t}),
\qquad
P_{\ell,t}
=\operatorname{RMS}(z_{\ell,t}).
\tag{14}
$$

仅 $A_{\ell,0}=\Theta(1)$ 不够；还要看不同 width/depth 和训练 step 的曲线。

### 2. Dependence stability

输出有界但与输入无关也是退化。可用 probe 输入 $x,x'$ 记录

$$
D_{\ell,t}
=\frac{\operatorname{RMS}\bigl(h_{\ell,t}(x)-h_{\ell,t}(x')\bigr)}
{\operatorname{RMS}(h_{\ell,t}(x))+\varepsilon},
\tag{15}
$$

或 Jacobian-vector product、相关性和 covariance spectrum。选择哪个量要由任务定义。

### 3. Update stability

必须同时看参数步与功能步：

$$
U^\theta_{\ell,t}
=\operatorname{RMS}(\Delta\theta_{\ell,t}),
\qquad
R^\theta_{\ell,t}
=\frac{\operatorname{RMS}(\Delta\theta_{\ell,t})}
{\operatorname{RMS}(\theta_{\ell,t})+\varepsilon},
\tag{16}
$$

$$
U^h_{\ell,t}
=\operatorname{RMS}\bigl(h_{\ell,t+1}-h_{\ell,t}\bigr),
\quad
U^f_t
=\operatorname{RMS}(f_{t+1}-f_t).
\tag{17}
$$

再加 gradient RMS、operator norm、logit RMS 与 loss change，构成最小八项：activation、dependence、gradient、parameter、parameter update、feature update、logit、loss。

> [!important] Maximal 的语义
> μP 中的 maximal 不是“数值尽可能大”，而是在既定极限合同里，选择**不使网络发散的最大量级**，让 feature update 不因 width 增大而消失。

## 五、Width 与 Depth 为什么必须分开

设 residual 网络

$$
h_{\ell+1}=h_\ell+\alpha_LF_\ell(h_\ell),
\qquad \ell=0,\ldots,L-1.
\tag{18}
$$

若各 branch increment 同向，最坏情况下总变化可达 $L\alpha_L$；若近似不相关，RMS 累积更像 $\sqrt L\alpha_L$。于是候选缩放分别是

$$
\alpha_L=O(L^{-1})
\quad\text{或}\quad
\alpha_L=O(L^{-1/2}),
\tag{19}
$$

但哪一个正确取决于相关性、normalization、training dynamics 和要控制的对象。单纯把 width-μP 表中的 $n$ 换成 $nL$ 没有依据。

对 width–depth 联合路径 $L=L(n)$，应分别记录：

- 单层 coordinate/feature update；
- residual stream 的累计更新；
- 网络 Jacobian/谱放大；
- 相同 token/step/FLOP 时域下的 loss。

## 六、各向同性桥梁：参数最速不等于特征最速

对 $Y=XW$，平方可微损失的一步参数梯度下降为

$$
\Delta W=-\eta X^\top\nabla_YL.
\tag{20}
$$

于是特征变化

$$
\Delta Y=X\Delta W
=-\eta XX^\top\nabla_YL.
\tag{21}
$$

若 $XX^\top\approx cI$ 只在相关子空间成立，则参数空间梯度步才近似对应特征空间梯度步。[[S-2026-Su-11549-各向同性]] 提供这一问题入口，但要注意：当 batch size $b>d_{in}$ 时，$XX^\top$ 的秩至多 $d_{in}$，不可能是满秩 $b\times b$ 单位阵。

因此更严谨的说法是审计：

1. $X^\top X/b$ 是否在 feature space 近似白化；
2. $XX^\top$ 的非零谱是否集中；
3. 当前 $\nabla_YL$ 落在哪个子空间；
4. 结论是期望、有限 batch 观察还是高概率界。

## 七、一个合格的尺度实验表

每次实验至少有以下列：

| 类别 | 必填字段 |
|---|---|
| 模型族 | block、norm、residual、attention、tying、dtype |
| 尺度路径 | 每层 width、depth、head、FFN、vocab、sequence |
| 训练合同 | optimizer、LR/group scale、batch、loss reduction、schedule、steps/tokens |
| 随机性 | seeds、data order、dropout/router、失败运行 |
| 参数对象 | entry RMS、Frobenius、spectral、relative update |
| 功能对象 | activation、feature update、logit、loss、NTK drift |
| 判据 | slope、置信区间、允许区间、失败门 |

对某统计量 $M(n)$，可在 log–log 坐标拟合

$$
\log M(n)=c+\kappa\log n+\varepsilon_n.
\tag{22}
$$

$\kappa\approx0$ 只是“在当前宽度窗口近似水平”的证据。若区间很宽、曲线弯曲或最宽点反转，不能宣告渐近稳定。

## 八、图：尺度轴怎样翻译为可检验对象

先看图回答：为什么“参数量更大但训练稳定”仍不足以说明 μP 或尺度迁移成立？

![[00-知识库管理/_assets/figures/training-optimization/fig-scale-axis-object-contract-v1.svg|880]]

> [!figure] 图 TRN-41　尺度轴—观测对象—证据量词合同
> 左侧把 width、depth、shape、data/time 与 compute 分开；中间区分坐标 RMS、向量范数、算子范数和功能更新；右侧要求在初始化、有限步和扩展时域分别用期望、高概率或最坏界验收。来源：依据 [[S-2021-Yang-Hu-Feature-Learning]]、[[S-2022-Yang-Tensor-Programs-V-MuTransfer]] 与 [[S-2025-Su-11340-MuP之上1]] 的对象分层原创绘制。

**怎样读图**：先沿左列选择实际变化的尺度轴，再从中列选择要保持非退化的对象，最后在右列填写时间和概率量词。只有一条从左到右的完整路径，才是一条可检验 claim。

**图没有证明什么**：图不声称所有对象都能同时保持 $\Theta(1)$，也没有给出联合 width–depth 的普适参数化；它是实验和定理的输入合同。

## 九、常见错误与修正

1. **只报参数量**：改为逐轴 shape path；
2. **把坐标 RMS 当向量 norm**：明确是否除以 $\sqrt n$；
3. **初始化稳定即训练稳定**：加入 step 1、早期窗口和目标时域；
4. **均值稳定即尾部稳定**：报告分位数、最大值或谱；
5. **宽度规则外推深度**：写 $L(n)$ 和 residual accumulation；
6. **参数变化即 feature learning**：直接测 hidden feature 和 kernel drift；
7. **单 seed 水平曲线即渐近律**：多 seed、斜率区间和更宽窗口；
8. **训练没 NaN 即成功**：加入 loss、迁移 optimum drift 和 compute budget。

## 十、初学者自检

1. 若 $x_i$ 的 RMS 为常数，为什么 $\lVert x\rVert_2$ 通常随 $\sqrt n$ 墠长？
2. 参数量同为四倍增长时，width×2 与 depth×4 为什么不是同一个极限？
3. $\mathbb E Z_n=O(1)$ 与 $Z_n=O_p(1)$ 的差别是什么？
4. 初始化 activation 稳定为什么不推出 feature update 稳定？
5. 当 $b>d$ 时，为什么不能要求 $XX^\top=I_b$？
6. 一条“μP 跨尺度成功”的实验 claim 至少要写出哪六栏？

## 十一、本节出口

你应能把“模型变大后量级不变”翻译为一个六栏合同，并能区分：

$$
\text{coordinate}
\ne\text{vector norm}
\ne\text{operator norm}
\ne\text{feature update}
\ne\text{training outcome}.
$$

下一节 [[Standard、NTK 与 Mean-field 参数化]] 将在同一个两层网络上展示：即使初始函数分布相似，参数坐标、forward multiplier 和学习率的组合不同，也会产生不同的无限宽训练 regime。

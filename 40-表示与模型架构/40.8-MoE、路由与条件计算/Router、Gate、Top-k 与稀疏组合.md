---
type: concept
status: draft
area: [architecture, moe, routing, gating]
aliases: [MoE Router, Top-k Gate, Sparse Gating]
node_id: ARCH-58
prerequisites: ["[[条件计算、专家混合与稀疏激活]]", "[[Scaled Dot-Product Attention 与 Softmax 数值语义]]"]
related: ["[[Expert Capacity、Dispatch 与 Token Dropping]]", "[[MoE 门控归一化、证据地图与开放问题]]"]
sources: ["[[S-2017-Shazeer-Sparsely-Gated-MoE]]", "[[S-2021-Fedus-Switch-Transformer]]", "[[S-2022-Zoph-ST-MoE]]", "[[S-2026-Su-11782-MoE门控归一化]]"]
exercises: ["[[习题 - Router、Gate、Top-k 与稀疏组合]]"]
solutions: ["[[解答 - Router、Gate、Top-k 与稀疏组合]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-moe-router-gate-topk-contract-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Router、Gate、Top-k 与稀疏组合

> [!abstract] 核心问题
> “对 Router 做 Softmax，再取 Top-k”仍不是完整定义。一个可复现的 MoE 必须说明 logits、score activation、离散选择、选中权重、capacity、tie-break 和反向估计。改变其中任一接口，都可能改变模型函数或训练动力学。

## 一、先建立完整路由合同

对 token 表示 $x\in\mathbb R^d$，最简单的线性 Router 产生 $E$ 个 logits：

$$
z=xW_r+b_r\in\mathbb R^E.
$$

然后至少经历四个彼此独立的接口：

1. **score activation**：$a=g(z)$；
2. **selection**：$I=\operatorname{TopK}(a,k)$；
3. **selected-weight normalization**：$w_i=h(a_I)_i$；
4. **mixture**：$y=\sum_{i\in I}w_if_i(x)$。

完整写成

$$
I(x)=\operatorname{TopK}(g(xW_r+b_r),k),
$$

$$
y(x)=\sum_{i\in I(x)}h(g(z)_{I(x)})_if_i(x).
$$

还必须补上 overflow policy、tie-break、noise、训练与推理是否同路由，以及 Top-k 的 backward estimator。

## 二、Softmax、Sigmoid 与 ReLU 分别改变什么

常见 score activation 有

$$
a_i^{\text{softmax}}=\frac{e^{z_i/\tau}}{\sum_j e^{z_j/\tau}},
\qquad
a_i^{\text{sigmoid}}=\sigma(z_i),
\qquad
a_i^{\text{ReLU}}=\max(0,z_i).
$$

Softmax 把全部专家放在概率单纯形上，$\sum_i a_i=1$，专家间有显式竞争；Sigmoid 独立压到 $(0,1)$，总和不固定；ReLU 允许精确零但无上界。

因为这三个函数对有限实数在各自单调区间内保持次序，Top-k index 往往相同；但数值尺度和选中后的组合权重未必相同。比如 $z=[2,1,-1]$，三种激活都把前两项排在最前，但 softmax 的全局竞争会让未选专家也进入分母。

> [!important] 排名等价不等于训练等价
> 即使 forward 的 Top-k 集合相同，score 的 Jacobian、辅助损失所见概率、Top-k 前后 Re-Norm 与数值饱和都不同。

## 三、Top-k 前归一化与选中后归一化

一种常见定义是先算全局 softmax 再保留 Top-k：

$$
\tilde w_i=a_i\mathbf 1[i\in I].
$$

此时 $\sum_i\tilde w_i<1$ 一般成立；另一种会在选中集合上重新归一化：

$$
w_i=\frac{a_i\mathbf 1[i\in I]}{\sum_{j\in I}a_j}.
$$

两者不仅差一个常数。若 residual path、expert output norm 或层归一化位置不同，门控总质量会改变有效更新尺度。

当 score 来自 softmax 时，选中后 Re-Norm 还有一个化简：

$$
\frac{e^{z_i}/\sum_{r=1}^Ee^{z_r}}
{\sum_{j\in I}e^{z_j}/\sum_{r=1}^Ee^{z_r}}
=\frac{e^{z_i}}{\sum_{j\in I}e^{z_j}}.
$$

所以 forward 上它等价于只对选中 logits 做 softmax；但 selection 本身仍由全部 logits 的排序产生。

## 四、Top-1 Re-Norm 的关键边界

若 $k=1$ 且选中后 Re-Norm，则选中专家权重恒为

$$
w_{i^*}=\frac{a_{i^*}}{a_{i^*}}=1.
$$

在选中集合不变的邻域内，

$$
\frac{\partial w_{i^*}}{\partial a_{i^*}}=0.
$$

同时 hard argmax 对 logits 几乎处处为常数，其普通导数也为零。因此仅沿 task loss → mixture weight 的常规路径，Router 可能得不到梯度。这并不意味着 Router 完全不能训练：辅助损失、straight-through estimator、噪声路由、未 Re-Norm 的 gate、bias feedback 或其他 proxy 都可提供更新。

[[S-2026-Su-11782-MoE门控归一化]] 特别强调了这一点。它是可以直接复算的 `I`，也是检查实现时很有价值的极端案例。

## 五、为什么 Top-k 的导数棘手

设 $I(z)$ 是 Top-k index 集合。只要没有分数交叉，小扰动不改变 $I$；一旦两个分数越过边界，集合突然改变。因此 selection 是分段常数、在边界不连续或不可微。

训练常见处理包括：

- 只对选中权重求导，不对 index 求导；
- 用 soft probability 构造辅助损失；
- 加噪声使探索更充分；
- 用 straight-through 或连续松弛近似离散选择；
- 不从损失求路由，而用外部 bias feedback 控制负载。

这些方法对应不同优化问题。论文若只写“Top-k routing”，无法复现梯度语义。

## 六、一个三专家、Top-2 手算

令 logits 为 $z=[2,1,-1]$，先取 Top-2，再只在选中集合上 softmax。选中 $I=\{1,2\}$，权重为

$$
w_1=\frac{e^2}{e^2+e^1}=\sigma(1)\approx0.731,
\qquad
w_2\approx0.269.
$$

若专家标量输出为 $f_1(x)=4,f_2(x)=-1$，则

$$
y\approx0.731\times4+0.269\times(-1)=2.655.
$$

若不做 Re-Norm、直接使用三分类 softmax 的前两项，则权重约为 $[0.705,0.259]$，总和约 $0.964$，输出约为 $2.561$。专家集合相同，模型函数仍不同。

## 七、噪声、温度和 tie-break

稀疏门控早期工作会用 noisy logits，例如

$$
z_i'=z_i+\epsilon_i\,\operatorname{softplus}(u_i(x)).
$$

噪声可促进探索并平滑“专家永远选不到”的死区，但也增加方差。温度 $\tau$ 改变 softmax 尖锐程度；在只看排序且 $\tau>0$ 时不改 Top-k index，却会改 mixing 与梯度。

相等分数还需要 tie-break。GPU 上不稳定排序可能令完全相同 checkpoint 在不同 kernel/version 下给出不同 expert assignment。可复现合同应声明稳定排序、index 优先或显式随机种子。

## 八、正式图：路由的四个接口

这张图回答什么问题？为什么“Softmax Top-k”不足以定义 forward，更不足以定义 backward？

![[00-知识库管理/_assets/figures/architecture/fig-moe-router-gate-topk-contract-v1.svg|900]]

> [!figure] 图 1｜从 Router logits 到专家组合及梯度路径的完整合同。**图源与生成**：本仓库原创 SVG，由 [[00-知识库管理/_labs/code/plot_architecture_moe_v1.py]] 生成；未复制论文或博客插图。

**怎样读图**：A 按 logits→score→Top-k→selected normalization→mixture 顺序读；B 用同一 logits 对比三种 score，指出 index 与 mixing 必须分开；C 从 task loss 向下检查 selected weights、Top-k boundary 与 balance signal 三条梯度路径。

**图没有证明什么**：图没有证明 Softmax、Sigmoid 或 ReLU 哪个在所有模型上更好，也没有把 hard Top-k 的近似梯度当作真实导数。实际优劣依 $k$、Re-Norm、auxiliary objective、容量和训练规模。

## 九、实现审计与单元测试

至少测试：

1. Router 输出 shape 为 $[T,E]$ 还是 $[B,L,E]$；
2. Top-k 按何轴、升降序和 tie-break；
3. score activation 在 Top-k 前还是后；
4. selected weights 是否 Re-Norm；
5. dropped token 的 gate 如何处理；
6. 同一 token 多专家输出如何 combine；
7. fp16 极大 logits 是否 overflow；
8. task/aux/bias 哪些路径更新 Router；
9. train/eval 是否加噪声；
10. k=1、全相等 logits 与极端 logits 的梯度测试。

## 十、证据边界与学习出口

- 路由 shape、Top-k index、Re-Norm 恒等式、Top-1 边界：`I`；
- 特定近似/噪声下的优化性质：有条件 `T`；
- 某门控方案的 loss/吞吐：`E`；
- “某归一化更符合专家选择本质”：`H`；
- 跨架构最优 gate：`O`。

学完本节，应能把任何 MoE 的一句“Top-k gate”展开成可执行合同，手算 Top-2 组合，并指出普通梯度在哪些位置被 hard selection 截断。

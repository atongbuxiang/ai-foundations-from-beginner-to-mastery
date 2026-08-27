---
type: exercise
status: verified
area: [training, optimization, parameterization, scaling]
topic: "[[模型尺度、稳定性指标与 Width-Depth 对象合同]]"
solution: "[[解答 - 模型尺度、稳定性指标与 Width-Depth 对象合同]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 模型尺度、稳定性指标与 Width-Depth 对象合同

> [!abstract] 训练目标
> 能把“模型变大后保持稳定”改写成含 family、scale path、time、randomness、object 与 criterion 的可检验命题，并严格区分坐标 RMS、向量范数、算子范数和功能更新。

## A. 识别与复述

### TRN41-A01
写出尺度结论的六栏合同。对“Transformer 扩大四倍后仍然稳定”逐栏指出缺失信息。

### TRN41-A02
区分 coordinate scale、vector RMS、Euclidean norm、entry RMS 与 operator norm。哪些量会随维度自动带上 $\sqrt n$？

### TRN41-A03
比较 $\mathbb E Z_n=O(1)$、$Z_n=O_p(1)$、高概率有界和确定性一致有界；按从弱到强给出直观解释。

## B. 手算与构造

### TRN41-B01
忽略 embedding、bias 与 norm，令 Transformer 每层主导参数量为
$$
4d^2+2dd_{ff}.
$$
当 $d_{ff}=4d$、depth 为 $L$ 时，分别计算 $(d,L)=(512,12)$、$(1024,12)$、$(512,48)$ 的近似参数量比例。说明“参数量四倍”为什么没有唯一 scale path。

### TRN41-B02
令 $x_i$ iid、均值 0、方差 4。计算 $\mathbb E\|x\|_2^2$、vector RMS 的平方期望；当 $n=100$ 与 $n=10\,000$ 时给出典型 $\|x\|_2$ 尺度。

### TRN41-B03
Residual network 满足 $h_{\ell+1}=h_\ell+\alpha_Lu_\ell$，且 $\|u_\ell\|=1$。分别在所有 $u_\ell$ 同向和两两正交时计算 $\|h_L-h_0\|$；求使总变化为 $O(1)$ 的 $\alpha_L$ 量级。

## C. 推导与证明

### TRN41-C01
设 $y=xW$，$x_i$ 独立、均值 0、方差 $q$，$W_{ij}$ 独立、均值 0、方差 $\sigma^2/d_{in}$，且两者独立。推导 $\operatorname{Var}(y_j)$，并指出哪些交叉项因什么条件消失。

### TRN41-C02
证明若 $\operatorname{RMS}(x_n)=O_p(1)$，则 $\|x_n\|_2=O_p(\sqrt n)$；反向命题需怎样归一化才成立？

### TRN41-C03
对 $Y=XW$ 推导参数梯度步后的 $\Delta Y=-\eta XX^\top\nabla_YL$。说明当 batch size $b>d$ 时，为什么 $XX^\top=cI_b$ 不可能成立，并给出更合理的子空间表述。

## D. 边界、反例与纠错

### TRN41-D01
构造随机变量 $Z_n$，使 $\mathbb E Z_n=1$，但 $Z_n$ 会以很小概率取越来越大的值。它反驳了哪种“期望稳定即无爆炸”推理？

### TRN41-D02
反驳：“所有层 activation RMS 在初始化都近似 1，所以训练尺度合同已正确。”至少给出 gradient、update、feature 与 time 中的三个缺口。

### TRN41-D03
构造两个参数量近似相同、但 width/depth path 不同的网络，并说明为何一个 fixed-width 理论不能自动比较二者。

## E. AI 迁移

### TRN41-E01
为一个 Transformer width ladder 写 scale manifest，至少包含 $d_{model},d_{ff},h,d_h,L,V,S,B,T$ 及哪些固定、哪些变化。

### TRN41-E02
设计一个 width–depth 稳定性实验：规定至少八个遥测量、三个时刻、两个概率/随机性报告和四个失败门。

### TRN41-E03
审计 claim：“从 1B 扩到 7B，Weight RMS 相同，因此模型具有尺度不变性。”给出不过度外推的改写模板。

## 作答与复盘

先独立填写六栏合同，再查看 [[解答 - 模型尺度、稳定性指标与 Width-Depth 对象合同]]。每题标记 independent / hinted / copied / blocked，并记录自己混淆的是 scale axis、对象、时钟还是概率量词。

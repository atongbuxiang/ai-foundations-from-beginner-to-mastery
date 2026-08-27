---
type: solution
status: verified
area: [training, scaling-laws, statistics]
topic: "[[经验 Scaling Law、幂律拟合与不可约项]]"
exercise: "[[习题 - 经验 Scaling Law、幂律拟合与不可约项]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - 经验 Scaling Law、幂律拟合与不可约项

> [!warning] 使用边界
> 拟合参数只对已声明的模型族、资源轴、数据/评测分布和有限尺度窗口成立；区间内拟合优度不是区间外定理。

## A. 识别与复述

### TRN49-A01
经验 law 是对观测规律的压缩：在给定区间与协议下，某函数族有较小残差和可接受预测误差。渐近定理要从明确假设证明极限阶；机制解释还要说明幂指数为何由算法、数据或架构产生。一次良好拟合支持“该曲线在所测区间是有效描述/候选预测器”，不能证明任意尺度继续成立、指数普适，或训练机制必然产生该幂律。

### TRN49-A02
$E$ 是该观测协议下的渐近底部，量纲与 $L$ 相同；$A$ 是幅度，量纲为 $[L][x]^\alpha$；$\alpha$ 无量纲且控制 excess loss 的衰减速度。改变 loss 会改变纵轴及底部；tokenizer 改变 token 数与每-token loss；评测分布改变 Bayes/不可约难度。故三者都绑定对象合同，不能跨合同照搬。

### TRN49-A03
原尺度模型最小化近似等方差的绝对残差平方 $\sum(L_i-f_i)^2$，大数值点的绝对误差影响更大。log 尺度模型最小化 $\sum(\log L_i-\log f_i)^2$；小误差下约等于 $\sum[(L_i-f_i)/f_i]^2$，更接近等相对误差。应由测量机制和残差诊断选择，而不是只选更直的图。

## B. 手算与构造

### TRN49-B01
四个 loss 为
$$
L(1)=5,\quad L(4)=3,\quad L(16)=2,\quad L(64)=1.5.
$$
相邻横轴比均为 4，因此原始 loss 的对数斜率为
$$
\frac{\log(3/5)}{\log4}\approx-0.368,\quad
\frac{\log(2/3)}{\log4}\approx-0.292,\quad
\frac{\log(1.5/2)}{\log4}\approx-0.208.
$$
幂律指数 $-1/2$ 属于 $L-E=4x^{-1/2}$；正 offset 在分母中的占比越来越大，使原始 $L$ 的斜率向 0 变平。

### TRN49-B02
$$
L(10^2)=2+8\cdot10^{-0.8}\approx3.2679,\qquad
L(10^4)=2+8\cdot10^{-1.6}\approx2.2010.
$$
无 offset 两点拟合给出
$$
\hat\alpha=-\frac{\log(2.2010/3.2679)}{\log(10^4/10^2)}\approx0.086.
$$
它远小于真实 $0.4$；不可约项让右端曲线变平，被错误吸收到较小指数中。

### TRN49-B03
取 $f_1(x)=1+x^{-1/2}$。它在 $x=100,1000$ 为 $1.1,1.03162$。通过这两点的无 offset 幂律约为 $f_2(x)=1.252x^{-0.0279}$，所以两端完全一致且窗口内接近；但
$$
f_1(10^8)=1.0001,\qquad f_2(10^8)\approx0.749.
$$
有限窗口只约束局部形状，不能可靠辨认渐近底部；不同函数族可能内插等价、外推分叉。

## C. 推导与证明

### TRN49-C01
由 $dL/dx=-\alpha Ax^{-\alpha-1}$，
$$
\frac{d\log L}{d\log x}=\frac{x}{L}\frac{dL}{dx}
=-\alpha\frac{Ax^{-\alpha}}{E+Ax^{-\alpha}}
=-\alpha\left(1-\frac{E}{L}\right).
$$
当 $x\to\infty$ 且 $E>0$，$L\to E$，括号趋于 0，故原始 loss 的 log-slope 趋于 0；这不是 excess law 的指数消失。

### TRN49-C02
$R=Ax^{-\alpha}$，故 $\log R=\log A-\alpha\log x$，斜率恰为 $-\alpha$。若减去 $\widetilde E=E+\delta$，则 $\widetilde R=Ax^{-\alpha}-\delta$，
$$
\frac{d\log\widetilde R}{d\log x}
=-\alpha\frac{Ax^{-\alpha}}{Ax^{-\alpha}-\delta}.
$$
$\delta>0$ 会放大斜率且可在尾部造成奇点；$\delta<0$ 会把斜率向 0 压缩。

### TRN49-C03
原尺度 iid 高斯误差的目标为
$$
\mathcal L_{raw}=\frac{1}{2\sigma^2}\sum_i[L_i-f(x_i;\theta)]^2.
$$
log 尺度 iid 高斯误差为
$$
\mathcal L_{log}=\frac{1}{2\tau^2}\sum_i[\log L_i-\log f(x_i;\theta)]^2.
$$
后者在小残差下以 $1/f_i^2$ 加权原残差，因而近似平衡相对误差；前者会让高-loss 点的同等相对偏差拥有更大绝对权重。

## D. 边界、反例与纠错

### TRN49-D01
$R^2$ 只描述已采样点相对某基准的区间内残差，且 log 变换可让很短的平滑曲线都显得近直。还缺：真正位于训练区间外的尺度；offset、broken law 等竞争函数族；冻结选择后的 held-out 预测误差与覆盖率。因此结论最多是“在该窗口内线性描述良好”。

### TRN49-D02
例如 $L=1+x^{-1/2}$。若强制 $E=0$，两点斜率就是原始 loss 的局部平均斜率；窗口从 $[1,4]$ 移到 $[16,64]$ 时，估计从约 $0.208$ 降到约 $0.085$，继续右移趋于 0。大量低噪声点只会让这个错误模型的错误指数估得更“精确”。

### TRN49-D03
选最优 seed 相当于对随机 loss 取极小值，会产生向下的 winner's curse；若大尺度尝试更多 seed 或方差不同，偏差还随尺度变化，进而扭曲斜率。应保存所有计划运行与失败，报告 seed-level 点、均值/中位数、层次区间和 intention-to-run 分母；若目标确是“搜索后最佳”，也要把搜索次数和成本写入 estimand。

## E. AI 迁移

### TRN49-E01
最小 manifest 包含：模型 family；资源轴 $D$ 的 tokenizer 与 seen-token 定义；validation 数据版本；cross-entropy 的 token/样本聚合；checkpoint 选择；尺度窗口；候选函数族与 offset 约束；误差模型；seed/失败规则；超参协议；切分与外推 horizon。字段须在看最终 held-out scales 前冻结。

### TRN49-E02
例：在几何尺度 $D=2^k$ 上，以前 5 个尺度拟合候选族，用随后 2 个尺度选误差模型和正则/函数族，最后 2 个更大尺度只做一次区间外评分。seed 与 checkpoint 作为尺度内重复，不能随机泄漏到三段。最终报告点预测、区间覆盖、最坏误差及失败率。

### TRN49-E03
稳妥表述：
> 对已声明的 decoder family、tokenizer、训练协议和 $D\in[D_{min},D_{max}]$，带 offset 的幂律在预注册候选中取得最佳 validation 表现，并在两个更大 held-out scales 上达到所报误差；这支持有限区间经验规律，不证明指数普适或在更远尺度不发生结构断点。

## 无提示重做

- [ ] 48 小时后重推 raw-loss 局部斜率。
- [ ] 一周后仅凭一张 log–log 图写出完整证据审计。

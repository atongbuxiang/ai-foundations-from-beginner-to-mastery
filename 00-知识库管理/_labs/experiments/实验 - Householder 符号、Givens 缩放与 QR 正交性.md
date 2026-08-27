---
type: experiment
status: draft
area: [math/numerical-analysis, math/numerical-linear-algebra]
topic: Householder 与 Givens 变换
prerequisites: ["[[Householder 与 Givens 变换]]", "[[浮点数与舍入误差]]", "[[数值稳定性]]", "[[QR 分解]]"]
related: ["[[实验 - Gram-Schmidt 与 QR 的正交性误差]]", "[[实验 - 等价公式不等价稳定]]", "[[稳定最小二乘与正规方程的风险]]"]
code: "[[plot_householder_givens_qr.py]]"
assets: ["[[00-知识库管理/_assets/plots/qr/plot-householder-givens-qr-v2.svg]]"]
figure_sha256: "530399f60ff943be3232aa6409ffd38ea402f090d3138c04e60e77ebdc637d2f"
sources: ["[[S-2024-Demmel-Householder-Givens稳定QR]]", "[[S-2025-LAPACK-QR反射与平面旋转]]"]
created: 2026-08-15
updated: 2026-08-23
---

# 实验 - Householder 符号、Givens 缩放与 QR 正交性

> [!abstract] 实验结论
> 稳定 QR 需要两层同时成立：局部 reflector/rotation 必须安全生成，随后正交变换序列才能发挥“不放大二范数误差”的优势。对 $x=(1,10^{-k})^T$，固定同号 Householder 目标在 $k=8$ 后完全保留待消尾部，反号目标仍把尾部消到舍入地板；对 $f,g=O(10^e)$，直接平方和在 $e\le-200$ 或 $e\ge154$ 失败，而安全缩放仍可用；对条件数从 $10$ 到 $10^{14}$ 的稠密矩阵族，Householder/Givens 的正交性缺陷保持约 $10^{-15}$，MGS 则总体随条件数上升到 $10^{-4}$ 量级。

> [!question] 本实验的判别问题
> 正交变换算法的稳定性，怎样同时依赖“局部参数安全生成”和“全局正交序列不放大误差”两层机制？

先用图回答：**Householder 的符号、Givens 的缩放和 QR 执行图分别在什么数值尺度上决定成败？**

![[00-知识库管理/_assets/plots/qr/plot-householder-givens-qr-v2.svg|880]]

> [!figure] 实验图｜正交变换稳定性的局部与全局两层
> A 比较同号/反号 Householder 目标的尾部保留比例；B 比较直接 $\sqrt{f^2+g^2}$ 与安全 scaling/hypot；C 比较 MGS、Householder 与 Givens QR 的正交性缺陷。生成脚本：[[plot_householder_givens_qr.py]]；确定性构造，并对符号消去、极端尺度与高条件数正交性三组机制设断言。

**怎样读图。** A、B 中红线到 1 表示局部变换已失效，蓝/绿线贴近地板表示安全公式仍完成消零；C 再比较紫线随 $\kappa$ 上升与两条正交变换曲线保持在舍入地板的差异。局部公式先通过，才有资格讨论全局 QR 稳定性。

**适用边界（图没有证明什么）。** 图验证教学实现的数值机制，不比较 GPU/BLAS 性能，也不证明任意矩阵上 Householder/Givens 的误差常数相同；极端指数点还受当前 binary64 与运行时语义约束。

## 一、为什么把实验拆成三块

“正交变换稳定”不是一句可以跳过实现的口号。失败可能出现在：

1. **生成阶段**：Householder 向量已经因消去丢失方向；
2. **参数阶段**：Givens 的 $r,c,s$ 在平方时 overflow/underflow；
3. **组合阶段**：局部变换虽然可用，但正交化算法的执行图让误差受条件数放大。

三块实验分别只改变一个因素，避免把局部公式错误和全局 QR 误差混成一个数字。

## 二、实验 A：Householder 目标符号

### 2.1 问题族

令

$$
x_k=\begin{bmatrix}1\\10^{-k}\end{bmatrix},
\qquad k=1,2,\ldots,18.
$$

它越来越接近 $e_1$。比较：

$$
\alpha_{\mathrm{same}}=+\|x_k\|_2
$$

与

$$
\alpha_{\mathrm{opposite}}=-\|x_k\|_2.
$$

两种选择在精确算术中都能构造反射器；区别只在浮点执行路径。

### 2.2 为什么同号目标危险

利用 Taylor 展开：

$$
\|x_k\|_2
=\sqrt{1+10^{-2k}}
=1+\frac12 10^{-2k}+O(10^{-4k}).
$$

同号目标的首分量是

$$
v_1
=1-\|x_k\|_2
=-\frac12 10^{-2k}+O(10^{-4k}).
$$

它通过两个约为 1 的数相减恢复极小量。当 $10^{-2k}$ 低于 1 附近的浮点间距时，计算范数直接舍入为 1，$v_1$ 变成 0。

反号目标为

$$
v_1=1+\|x_k\|_2\approx2,
$$

没有消去。

### 2.3 指标

我们测量

$$
\eta_{\mathrm{tail}}
=\frac{|(Hx_k)_2|}{|(x_k)_2|}.
$$

- $\eta_{\mathrm{tail}}\approx0$：待消尾部确实消失；
- $\eta_{\mathrm{tail}}\approx1$：尾部几乎原样保留；
- 该指标按原尾部分量归一化，能看到绝对值很小时的相对失败。

### 2.4 代表性结果

| $k$ | 同号目标尾部保留比例 | 反号目标尾部保留比例 |
|---:|---:|---:|
| 1 | $1.55\times10^{-14}$ | $2.78\times10^{-16}$ |
| 4 | $3.58\times10^{-9}$ | $0$ |
| 6 | $8.89\times10^{-5}$ | $0$ |
| 7 | $2.30\times10^{-2}$ | $2.65\times10^{-16}$ |
| 8 | $1$ | $0$ |
| 18 | $1$ | $0$ |

表中的 0 表示本次 binary64 运算恰好舍入为零；图上为了使用对数坐标显示为 $10^{-18}$。

## 三、实验 B：Givens 极端尺度

### 3.1 问题族

取

$$
f=1.3\times10^e,
\qquad
g=0.9\times10^e,
$$

并扫描

$$
e\in\{-300,-250,-200,-160,-154,-153,-100,0,100,153,154,160,200,250,300\}.
$$

真实半径

$$
r=\sqrt{f^2+g^2}
=\sqrt{2.5}\times10^e
$$

在这些端点仍是 binary64 可表示的有限非零数。

### 3.2 两种实现

朴素路径：

$$
r_{\mathrm{naive}}=\sqrt{f^2+g^2}.
$$

安全路径使用 `hypot` 等价的缩放：

$$
t=\max(|f|,|g|),
\qquad
r_{\mathrm{safe}}
=t\sqrt{(f/t)^2+(g/t)^2}.
$$

### 3.3 指标

生成 $c=f/r,s=g/r$ 后，检查应被消掉的分量：

$$
\eta_G
=\frac{|-sf+cg|}{\operatorname{hypot}(f,g)}.
$$

若 $r=0$、$r=\infty$ 或参数非有限，则把该次失败记为 1。

### 3.4 代表性结果

| $e$ | 朴素路径 $\eta_G$ | 安全路径 $\eta_G$ | 原因 |
|---:|---:|---:|---|
| $-300$ | $1$ | $0$ | 平方下溢为零 |
| $-200$ | $1$ | $0$ | 平方下溢为零 |
| $-160$ | $9.99\times10^{-17}$ | $0$ | 仍可用但已接近极端区 |
| $0$ | $7.02\times10^{-17}$ | $7.02\times10^{-17}$ | 正常尺度 |
| $153$ | $5.88\times10^{-17}$ | $5.88\times10^{-17}$ | 仍可用 |
| $154$ | $1$ | $0$ | 平方和溢出 |
| $300$ | $1$ | $0$ | 平方和溢出 |

这证明“输入有限、真值可表示”仍不足以保证朴素中间表达式可表示。

## 四、实验 C：QR 正交性与条件数

### 4.1 构造已知奇异值的确定性矩阵

取 $n=12$。令 $U,V$ 是两个由 DCT 基及列置换构造的确定性正交矩阵，奇异值为

$$
\sigma_j
=\varepsilon^{j/(n-1)},
\qquad j=0,1,\ldots,n-1.
$$

构造

$$
A_\varepsilon
=U\operatorname{diag}(\sigma_0,\ldots,\sigma_{n-1})V^T.
$$

在精确算术中

$$
\sigma_{\max}=1,
\qquad
\sigma_{\min}=\varepsilon,
\qquad
\kappa_2(A_\varepsilon)=\varepsilon^{-1}.
$$

扫描 $\varepsilon=10^{-1},\ldots,10^{-14}$。没有使用随机矩阵，因此每次运行完全一致。

### 4.2 三种教学实现

1. **MGS**：逐列、逐旧方向更新残差；
2. **Householder QR**：稳定符号、紧凑反射应用；
3. **Givens QR**：自底向上、安全 `hypot` 生成旋转。

它们使用相同 binary64 输入和标准库标量运算。比较的是执行图，不是高性能库速度。

### 4.3 指标

主指标：

$$
\eta_{\mathrm{orth}}
=\|I-Q^TQ\|_F.
$$

对照指标：

$$
\eta_{\mathrm{rec}}
=\frac{\|A-QR\|_F}{\|A\|_F}.
$$

### 4.4 代表性结果

| $\kappa_2(A)$ | MGS 正交缺陷 | Householder | Givens | 三者重构误差量级 |
|---:|---:|---:|---:|---:|
| $10$ | $1.23\times10^{-15}$ | $2.08\times10^{-15}$ | $1.97\times10^{-15}$ | $10^{-16}$ |
| $10^4$ | $5.78\times10^{-13}$ | $2.28\times10^{-15}$ | $3.16\times10^{-15}$ | $10^{-16}$ |
| $10^8$ | $2.17\times10^{-9}$ | $2.01\times10^{-15}$ | $1.53\times10^{-15}$ | $10^{-16}$ |
| $10^{12}$ | $1.04\times10^{-4}$ | $2.10\times10^{-15}$ | $2.60\times10^{-15}$ | $10^{-16}$ |
| $10^{14}$ | $4.36\times10^{-4}$ | $1.60\times10^{-15}$ | $2.46\times10^{-15}$ | $10^{-16}$–$10^{-15}$ |

MGS 曲线不要求逐点单调：具体舍入会抵消或叠加；关键是它的总体尺度随 $\kappa$ 跨越多个数量级，而两种正交变换方法保持在维度常数乘机器精度附近。

## 五、怎样读三幅图

### 面板 A

红线先连续恶化，在 $k=8$ 达到 1；蓝线始终在舍入地板。它验证的是 Householder 目标符号，而不是“反射公式本身不正确”。

### 面板 B

朴素路径在中间尺度与安全路径一致，但在两端跳到失败值 1。安全路径说明问题不在真实半径超范围，而在中间平方超范围。

### 面板 C

三种方法的重构误差都很小；只有正交性指标揭示 MGS 的条件数放大。Householder/Givens 曲线说明连续正交变换的结构优势。

## 六、从实验返回理论

三组结果对应一条完整稳定链：

$$
\boxed{
\text{安全生成 }(v,\tau)\text{ 或 }(c,s)
\to
\text{应用近正交局部变换}
\to
\text{序列误差只累加、不放大}
\to
\text{同时验收重构与正交性}
}
$$

任何一环缺失都可能让“用了正交矩阵”变成空洞描述。

## 七、复现实验

在知识库根目录执行：

```bash
python3 "00-知识库管理/_labs/code/plot_householder_givens_qr.py"
```

脚本会：

1. 重新生成 `plot-householder-givens-qr-v2.svg`；
2. 打印 18 个 Householder 尾部保留比例；
3. 打印 15 个 Givens 尺度点的消零残差；
4. 打印 14 个条件数下三种 QR 的正交性与重构误差。

## 八、环境与可复现性

| 项目 | 设置 |
|---|---|
| 语言 | Python 3 标准库 |
| 数值格式 | CPython `float`，通常为 IEEE 754 binary64 |
| 外部依赖 | 无 NumPy、BLAS 或绘图库 |
| 随机性 | 无 |
| QR 规模 | $12\times12$ |
| 输出 | 自包含 SVG，含 `<title>` 与 `<desc>` |

## 九、边界

- 标量 Python 循环不代表 LAPACK、cuSOLVER、TPU 或分布式 QR 性能；
- DCT 基在浮点中只是近似正交，但解析构造足以控制谱尺度；
- $n=12$ 的结果不直接给出大规模常数或通信结论；
- MGS 的非单调点是保留的实际结果，没有为了“更漂亮”而平滑；
- 图中 $10^{-18}$ 是显示下限，不是 binary64 的普遍误差下界；
- Householder/Givens 正交性好不表示近秩亏矩阵的列空间对输入扰动不敏感；
- 未测试 block reflector、列主元、TSQR、mixed precision 和复数相位。

## 十、进一步实验

1. 加入 CGS、MGS2 与 Cholesky QR/CholeskyQR2；
2. 模拟 FP32/BF16，观察三个转折点提前多少；
3. 比较 `hypot`、LAPACK `xLARTG` 和硬件 fused 实现；
4. 比较显式 $Q$ 与仅应用 reflector 的误差和成本；
5. 对 QRCP 构造 column subset 对抗例子；
6. 用不同 TSQR 树比较通信和非位级可重复性；
7. 对可微 QR 扫描 $\sigma_{\min}$ 并检查 VJP。

## 十一、完成检查

- [x] 三个实验各自只改变一个核心执行选择；
- [x] Householder 指标按待消尾部尺度归一化；
- [x] Givens 真值在扫描范围内仍可表示；
- [x] QR 矩阵族的条件数由解析奇异值预设；
- [x] 同时报告正交性与重构误差；
- [x] 不删除 MGS 的非单调结果；
- [x] 代码与图由同一确定性数据生成；
- [x] 明确区分教学标量实现与生产数值库。

---
type: solution
status: draft
area: [architecture, attention, numerical-stability]
topic: "[[Scaled Dot-Product Attention 与 Softmax 数值语义]]"
exercise: "[[习题 - Scaled Dot-Product Attention 与 Softmax 数值语义]]"
sources: ["[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2026-Su-11814-LSE-Softmax-Taylor]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Scaled Dot-Product Attention 与 Softmax 数值语义

## A. 识别与复述

### ARCH-SDP-A01
$$\operatorname{softmax}_{row}(QK^T/\sqrt{d_k}+M)V.$$ Softmax 沿每个 query 的可见 key 轴，即最后的 $T_k$ 轴；batch/head/query 行彼此独立归一。

### ARCH-SDP-A02
可用条件：q/k 坐标中心化；q 与 k 独立；各坐标单位方差；不同坐标乘积项互不相关/独立。若方差为 $\sigma_q^2,\sigma_k^2$，结果相应为 $d_k\sigma_q^2\sigma_k^2$。

### ARCH-SDP-A03
减同一个行常数（尤其最大值）由平移不变性保持精确分布。除以 $\sqrt{d_k}$ 改变 logit 差，通常改变 entropy 与权重；它是模型定义中的尺度选择。

## B. 手算与建模

### ARCH-SDP-B01
减 1001 得 $(-1,0,-2)$；指数约 $(.367879,1,.135335)$，和 $1.503214$，故结果 $(.245,.665,.090)$。

### ARCH-SDP-B02
未 mask 为 $(1/3,1/3,1/3)$，后乘 $(1,1,0)$ 得 $(1/3,1/3,0)$，行和 $2/3$。正确做法在前两项归一，得 $(1/2,1/2,0)$。

### ARCH-SDP-B03
若 $X$ 方差 64，则 $X/8$ 方差为 $64/8^2=1$；$X/64$ 方差为 $64/64^2=1/64$。标准差按除数一次缩放，方差按平方缩放。

## C. 推导与证明

### ARCH-SDP-C01
$X_r=q_rk_r$ 有 $E[X_r]=0$，且独立 q/k 使 $E[X_r^2]=E[q_r^2]E[k_r^2]=1$，故 Var$(X_r)=1$。乘积项互不相关时，Var$(\sum_rX_r)=\sum_r1=d_k$。

### ARCH-SDP-C02
$e^{z_j+c}/\sum e^{z_l+c}=e^{z_j}/\sum e^{z_l}$。对 $a_j=e^{z_j}/Z$，$\partial a_j/\partial z_k=a_j(\delta_{jk}-a_k)$，即 $J=\mathrm{Diag}(a)-aa^T$。于是 $J1=a-a(a^T1)=a-a=0$。

### ARCH-SDP-C03
设唯一最大坐标 m。对 $j\ne m$，
$$\frac{a_j}{a_m}=\exp((z_j-z_m)/\tau)\to0$$
因为差为负。行和为 1，故 $a_m\to1$、其余趋 0。若最大值并列，质量在并列项间分配，不能声称唯一 one-hot。

## D. 边界、反例与纠错

### ARCH-SDP-D01
令所有坐标共享同一随机变量：$q_r=k_r=X$，$E[X^2]$ 有限。则 $q^Tk=d_kX^2$，其方差为 $d_k^2\operatorname{Var}(X^2)$，按 $d_k^2$ 而非 $d_k$ 增长；还因均值非零需中心化。它违反坐标/乘积独立假设。

### ARCH-SDP-D02
若整行都是有限常数 $-C$，减最大值后全为 0，softmax 给均匀 $1/T_k$，并非全零。只有至少一项合法或实现专门处理全遮蔽时才有定义；数学上的全 $-\infty$ 行是 $0/0$。

### ARCH-SDP-D03
一阶近似 $a_0+J_0(z-z_0)$ 是仿射函数，离展开点足够远可出现负分量。虽然 $1^TJ_0=0$ 使理想一阶式保行和，但截断、mask 与数值实现未必保其他性质，且局部余项随距离增长，不能给全域稳定。

## E. AI 迁移

### ARCH-SDP-E01
按 layer/head/length 记录 q norm、k norm、logit mean/std、max-min、finite ratio、row entropy、max weight、row-sum error、output/gradient norm。阈值可用：(1) 绝对安全阈值，如任何 NaN/Inf 立即失败；(2) 相对/分位阈值，如 entropy 或 logit std 偏离训练基线 5 个 MAD，并配任务退化确认，避免任意常数裁决。

### ARCH-SDP-E02
对 fp16、bf16、fp32 分别测试 boolean mask、$-\infty$ 与候选 finite sentinel；用被屏蔽位置超大正 logit，确认权重 0、有效行和 1。构造全遮蔽行，要求结果符合声明（报错/零行）且无静默 NaN；测试 fused/unfused kernel 与 autocast 一致性。

### ARCH-SDP-E03
固定 checkpoint/data，扫描训练内外长度；比较 baseline、temperature、K-normalized、QK-normalized。记录 quality 与 q/k norm、logit scale、entropy。norm 删除尺度通道是 `I`；某配置改善曲线是 `E`；对更大模型/新数据仍有效为 `O/H`，必须另测而不能写成定理。

---
type: solution
status: draft
area: [architecture, positional-encoding, rope, group-representation]
topic: "[[RoPE 的旋转推导、群表示与内积]]"
exercise: "[[习题 - RoPE 的旋转推导、群表示与内积]]"
sources: ["[[S-2021-Su-RoFormer]]", "[[S-2021-Su-8265-RoPE]]", "[[S-2022-Su-9403-RoPE完备性]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - RoPE 的旋转推导、群表示与内积

## A. 识别与复述

### ARCH-ROPE-A01
$$R_\theta=\begin{bmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{bmatrix},\quad \tilde q_m=R_{m\theta}q_m,\quad \tilde k_n=R_{n\theta}k_n.$$
于是 $(\tilde q_m)^\top\tilde k_n=q_m^\top R_{(n-m)\theta}k_n$。多维 RoPE 是不同频率二维块的 block diagonal 版本。

### ARCH-ROPE-A02
位置需要改变“谁与谁相似”的 score，所以作用 Q/K 即可把相对位移写入 attention weights。V 是被汇总的信息内容，不旋转仍可通过位置相关权重选择；旋转 V 是另一种架构，可能改变输出坐标与 cache，不是 RoPE 相对内积恒等式的必要条件。

### ARCH-ROPE-A03
必须固定相邻/half-split 配对、频率 $\omega_i$ 与 base、每个 token 的全局 position IDs/cache offset、实际旋转前多少维及剩余维处理、sin/cos 计算与缓存 dtype。任一不一致都可能 shape 正常但语义错误。

## B. 手算与建模

### ARCH-ROPE-B01
$R_{\pi/4}q=(\sqrt2/2,\sqrt2/2)$；$R_{3\pi/4}k=(-\sqrt2/2,-\sqrt2/2)$，内积 $-1$。相对角 $(3-1)\pi/4=\pi/2$，$R_{\pi/2}k=(-1,0)$，$q^\top R_{\pi/2}k=-1$，两边相同。

### ARCH-ROPE-B02
Adjacent pairing 为 $(x_0,x_1)$ 与 $(x_2,x_3)$；half-split 常把 $(x_0,x_2)$ 与 $(x_1,x_3)$ 配对。二者在配套 permutation 下可等价，但若权重/checkpoint 按一种训练、推理按另一种解释，就不是同一函数。

### ARCH-ROPE-B03
已有 5 个位置 $0\ldots4$，新 token IDs 为 $5,6,7$。若重启为 $0,1,2$，新 token 对旧 key $j$ 的相对位移从 $5-j,6-j,7-j$ 变为 $-j,1-j,2-j$；新 token 之间的相对差仍相同，但与全部 cache 的关系错了 5。

## C. 推导与证明

### ARCH-ROPE-C01
直接相乘得 $R_a^\top R_a=I$，因为对角为 $\cos^2a+\sin^2a=1$、非对角抵消。又 $R_a^\top=R_{-a}$，用角度加法 $R_{-a}R_b=R_{b-a}$。

### ARCH-ROPE-C02
令 $R_n=\operatorname{diag}(R_{n\omega_0},\ldots,R_{n\omega_{d/2-1}})$。各块正交，所以 $R_n^\top R_n=I$、$\|R_nx\|=\|x\|$；并且 $R_m^\top R_n=R_{n-m}$，故 $(R_mq)^\top(R_nk)=q^\top R_{n-m}k$。

### ARCH-ROPE-C03
取 $m=n-1$ 递推：$R_n=R_{n-1}R_1$；由归纳得到 $R_n=R_1^n$，负整数由正交逆矩阵给出。它刻画离散平移群的正交表示；没有唯一确定频率、通道分解、训练行为或性能，额外连续性/实表示条件才导向进一步分类。

## D. 边界、反例与纠错

### ARCH-ROPE-D01
公式是 $q_m^\top R_{n-m}k_n$，其中 $q_m,k_n$ 仍依 token 内容和上下文；不同位置的内容可使同一相对距离 score 不同。mask、bias 与 softmax 分母也依整行。因此只有位置变换部分以相对差进入，不是全部权重只依距离。

### ARCH-ROPE-D02
四维 $q=(1,0,0,0),k=(0,0,1,0)$。Adjacent 配对时非零量落在不同二维块；half-split 时二者成为同一对，旋转后的内积一般不同。两实现都保持总 norm、shape 都为 4，故只测这两项抓不到错误，必须用基向量和参考 pairing 测输出。

### ARCH-ROPE-D03
正交只说明旋转前后向量 norm 不变；相对 score 可随相位振荡而非单调衰减。训练外相位、候选数、softmax 和任务依赖均未被 norm 结论约束，所以不能推出外推质量。

## E. AI 迁移

### ARCH-ROPE-E01
同一 token 序列在 eval mode 做全量 causal forward，再逐 token/分块 decode；为缓存 K 使用全局 position offset，逐行比较 logits/hidden。覆盖 prefill 后续、batch 不同 cache length、left padding、chunked prefill、不同 rotary dimension/dtype；错误 offset 作为负对照应失败。

### ARCH-ROPE-E02
先对每个 head 单独验证 $R_m^TR_n=R_{n-m}$ 和 norm；再固定其余训练配置，比较共享/不同 base、统一/逐 head scale，多长度与位置评测。代数检查仅判实现正确，性能用多 seed 与任务矩阵报告，不能用一方替代另一方。

### ARCH-ROPE-E03
数学：频率、正交、相对内积；布局：pairing、head reshape、rotary/pass-through slice；数值：角度计算、缓存 sin/cos、fp32/bf16 误差；Serving：position IDs、padding、prefill/decode/chunk offset、cache serialization；回归：参考向量与 full/cache 等价。

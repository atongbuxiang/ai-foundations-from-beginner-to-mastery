---
type: solution
status: draft
area: [neural-networks/regularization, stochastic-depth, droppath, residual-networks, effective-depth]
topic: "[[Stochastic Depth、DropPath 与有效深度]]"
exercise: "[[习题 - Stochastic Depth、DropPath 与有效深度]]"
sources: ["[[S-2016-Huang-Stochastic-Depth]]", "[[S-2017-Larsson-FractalNet-DropPath]]", "[[S-2026-PyTorch-Dropout-Stochastic-Depth]]", "[[S-2014-Srivastava-Dropout]]"]
created: 2026-08-24
updated: 2026-08-24
---
# 解答 - Stochastic Depth、DropPath 与有效深度

## A

### NN-SDP-A01
现代 inverted 合同常写为
$$
x_{l+1}=x_l+\frac{b_l}{q_l}F_l(x_l)\quad(\text{train}),
\qquad x_{l+1}=x_l+F_l(x_l)\quad(\text{eval}).
$$
原始 stochastic-depth 风格可在 train 使用 $x_l+b_lF_l(x_l)$，eval 使用 $x_l+q_lF_l(x_l)$。前者训练时放大活跃 branch，后者测试时缩小完整 branch；同一层固定输入的一阶矩可匹配，但优化尺度、normalization state 和 checkpoint 参数化不可混用。

### NN-SDP-A02
Physical depth 是图中实际堆叠的 blocks；active depth 是一次 mask realization 中活跃 branches 数；path length 是某条计算路径经过的变换数；effective depth 还可能指梯度/贡献显著传播的尺度，必须操作化定义。$\mathbb E[D]=2.75$ 只是离散随机变量的均值；训练数据实际经历 $D=0,1,2,3,4$ 的混合及具体位置组合，不等同于存在一个 2.75 层确定网络。

### NN-SDP-A03
Batch gate 为整个 batch 每层共享一个 Bernoulli，控制流容易统一并可能整 branch 短路，但样本 noise 高度相关。Row gate 给每个样本独立 gate，增强样本级路径多样性，却常需先算全 batch branch 再 mask，难省 FLOP。Token/element gate 更细，已接近 structured activation Dropout，会改变空间/token covariance，不应不加说明地仍称 stochastic depth。

## B

### NN-SDP-B01
独立 gates 下
$$
\mathbb E[D]=\sum_lq_l=0.875+0.75+0.625+0.5=2.75,
$$
$$
\operatorname{Var}(D)=\sum_lq_l(1-q_l)
=0.109375+0.1875+0.234375+0.25=0.78125.
$$
全活跃概率为
$$0.875\cdot0.75\cdot0.625\cdot0.5=0.205078125,$$
全删除概率为
$$0.125\cdot0.25\cdot0.375\cdot0.5=0.005859375.$$

### NN-SDP-B02
固定 $f$ 后只有标量 $b_l$ 随机，因此
$$
\mathbb E[R_l\mid x_l]=f,
$$
$$
\operatorname{Cov}(R_l\mid x_l)
=\operatorname{Var}(b_l/q_l)ff^\mathsf T
=\frac{1-q_l}{q_l}ff^\mathsf T.
$$
第 $i$ 坐标方差为 $(1-q_l)f_i^2/q_l$。只要 $f\ne0$，这个 covariance 是 rank one：同一个 path gate 让 branch 的所有坐标一起出现或消失。

### NN-SDP-B03
真正短路时，期望 branch compute 为
$$
\sum_lq_lC_l=0.875(1)+0.75(2)+0.625(3)+0.5(4)=6.25.
$$
若四个 $F_l$ 都先执行再乘 mask，则 branch compute 仍是 $1+2+3+4=10$，还要加 mask/RNG 成本。两者都可得到相同数值形式的 masked output，却有不同系统账本。

## C

### NN-SDP-C01
记 $J_l=\partial F_l/\partial x_l$，则 local Jacobian 为
$$
\frac{\partial x_{l+1}}{\partial x_l}=I+\frac{b_l}{q_l}J_l.
$$
若上游 cotangent 为 $g_{l+1}$，
$$
g_l=g_{l+1}+\frac{b_l}{q_l}J_l^\mathsf Tg_{l+1},
$$
$$
\nabla_{\theta_l}L=\frac{b_l}{q_l}
\left(\frac{\partial F_l}{\partial\theta_l}\right)^\mathsf Tg_{l+1}.
$$
$b_l=0$ 时 branch 参数梯度为 0，但 $g_l=g_{l+1}$，identity rail 保留 input gradient 和 state 传递。

### NN-SDP-C02
对 $D=\sum_lb_l$，概率生成函数是
$$
G_D(s)=\mathbb E[s^D]=\prod_l\mathbb E[s^{b_l}]
=\prod_l\{(1-q_l)+q_ls\}.
$$
$G_D'(1)=\sum_lq_l=\mathbb ED$。又有 $\mathbb E[D(D-1)]=G_D''(1)$，代入
$$
\operatorname{Var}(D)=G_D''(1)+G_D'(1)-G_D'(1)^2
=\sum_lq_l(1-q_l).
$$
各项不相同时这是 Poisson-binomial，而非普通 binomial。

### NN-SDP-C03
固定 $x_l$ 时 $J_l$ 也是确定对象，所以
$$
\mathbb E_b\left[I+\frac{b_l}{q_l}J_l\mid x_l\right]=I+J_l.
$$
但端到端 Jacobian 是沿随机 trajectory 的矩阵乘积；后层 $J_k$ 的 evaluation point $x_k$ 依赖更早 gates，因而这些随机矩阵通常相关且不交换。一般有 $\mathbb E[J_L\cdots J_1]\ne\prod_l\mathbb E[J_l]$，局部条件等式不能无条件连乘。

## D

### NN-SDP-D01
“rate 0.2”可能只是末层 rate，前层 schedule 更小；inverted mask 若在 $F_l$ 已算完后应用，完全不省 branch GEMM/attention；row gates 很难在 dense accelerator 上按样本跳过；shortcut、normalization、routing、RNG 和 memory traffic 是固定/额外成本；硬件 utilization 也不随理论 active fraction 线性变化。因此必须用实际 schedule 求 $\sum q_lC_l$ 上界，再用 profiler 验证 conditional execution 和 wall time。

### NN-SDP-D02
Batch-shared gate 删除 branch 时整个 batch 不产生该 branch 的 BN observation，若短路还会少一次 running-stat update；活跃 batch 的 statistics 又来自全 batch。Per-sample gate 若先算 BN 再 mask，BN 仍看到所有样本而输出只保留部分；若先筛样本再 BN，batch size 随机且可能为空，统计噪声和语义都改变。Eval 时 gates 消失、BN 使用累计 state，因此必须明确更新频率、空分支策略和 train/eval consistency，最好分别报告 BN buffer drift。

### NN-SDP-D03
Checkpoint backward 若重采 gate，会把 forward 的 $b_l=0$ 与 backward 的 $b_l=1$ 拼成不存在的图；replicas 若意外用同一 seed，会降低预期路径多样性，若本应 batch-shared 却各 rank 不同，又可能与 synchronized normalization/collectives 冲突。验收应比较 checkpoint on/off 的 outputs/gradients，记录并恢复 RNG counter；检查同 replica 重放一致、跨 replica correlation 符合合同；对 conditional branch 确保所有 ranks 的 collective control flow 不死锁。

## E

### NN-SDP-E01
固定 backbone、总 steps、optimizer/LR、data order、augmentation、drop-budget summary（如 $\sum q_lC_l$）与 paired seeds；对 constant、linear、stage-specific schedules 做等额 tuning。质量账：accuracy/NLL/robustness；稳定性账：branch RMS、gradient/update ratio、Jacobian proxy、nonfinite/clipping、time-to-target；计算账：executed operators、FLOP estimate、memory、throughput/wall time。只有 profiler 证实短路后才可声称省计算。

### NN-SDP-E02
以 DropPath schedule/rate 为一轴、residual scale $\alpha_l$ 或其参数化为另一轴，做包含两者关闭和单独开启的 factorial grid；固定其他设置与 paired seeds。因为 branch noise covariance 按
$$
\frac{1-q_l}{q_l}\alpha_l^2F_lF_l^\mathsf T
$$
共同变化，已有 LayerScale/Fixup/ReZero 类 scaling 会改变可承受 rate、早期梯度和 update。复制别的模型 rate 没有匹配 branch RMS、depth、normalization 或 compute。

### NN-SDP-E03
优化机制需测 train loss/time-to-target、gradient/Jacobian 与深层 update；正则化机制需在 matched optimization/compute 下测 train–test gap 与 held-out risk；路径集成需分析路径预测分歧、deterministic/MC aggregation 与 ablation；计算机制需 operator trace、conditional branch counts 和 wall time。若只看到 final accuracy 增加，四种解释仍未识别；“因为更浅”至多是 active-depth 描述，不是因果结论。

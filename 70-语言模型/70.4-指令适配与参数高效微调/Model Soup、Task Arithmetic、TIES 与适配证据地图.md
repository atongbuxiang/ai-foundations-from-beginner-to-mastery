---
type: concept
status: verified
area: [language-models, model-merging, task-arithmetic, ties, evidence]
node_id: LM-32
aliases: [Model merging, Task vectors, TIES merging]
prerequisites: ["[[Adapter、Prompt Tuning、Prefix Tuning 与 IA3]]", "[[LoRA 的低秩更新、初始化、缩放与合并]]"]
related: ["[[能力—行为—系统评估协议与证据地图]]", "[[参数对称性、等价表示与可辨识边界]]"]
sources: ["[[S-2022-Wortsman-Model-Soups]]", "[[S-2023-Ilharco-Task-Arithmetic]]", "[[S-2023-Yadav-TIES]]", "[[S-2024-Su-10001-LoRA差分学习率]]"]
exercises: ["[[习题 - Model Soup、Task Arithmetic、TIES 与适配证据地图]]"]
solutions: ["[[解答 - Model Soup、Task Arithmetic、TIES 与适配证据地图]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-adapt-merge-ties-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Model Soup、Task Arithmetic、TIES 与适配证据地图

> [!abstract] 一句话结论
> 参数平均和 task-vector 算术只有在架构、坐标、共同 base 与局部几何对齐时才有意义；TIES 通过 trim、elect sign、merge 减少坐标冲突，但任何参数运算都不是函数运算定理，最终必须回到逐任务、OOD、校准和安全评估。

## 一、第一道门：参数坐标必须对齐

要逐坐标相加 $\theta^{(1)},\theta^{(2)}$，至少要求：

- 架构、tensor shapes 相同；
- parameter names/order 对齐；
- tokenizer、vocabulary、special tokens 与 output head 语义对齐；
- normalization、rope/config 等非参数状态一致；
- 同一 base 或有明确 alignment；
- adapter target modules 和 merge status 一致。

神经网络存在 hidden-unit permutation、scale 等对称性。两个函数相近的独立训练模型，其同编号神经元未必语义相同；直接平均可能落入高损失区。

同一预训练起点 fine-tune 常减少这种错位，但不是充分保证。

## 二、Model Soup

给 $K$ 个同 base fine-tuned checkpoints：

$$
\theta_{\text{soup}}
=\sum_{k=1}^{K}w_k\theta_k,
\qquad
w_k\ge0,\quad\sum_kw_k=1.
$$

### Uniform soup

$w_k=1/K$。无需 validation 逐个选择，但坏 ingredient 可拖累。

### Greedy soup

按 validation 排序，逐个尝试加入，只有平均后指标改善才保留。它是一种 selection procedure：

- 使用了 validation；
- 依赖候选顺序和 metric；
- search budget 与 candidates 数量应披露；
- final test 必须独立。

Model soup 产生一个模型，推理时不需要同时运行 $K$ 个 checkpoints；与 logit ensemble 不同。

## 三、为什么同 basin 很重要

考虑两模型线性插值：

$$
\theta(\lambda)
=(1-\lambda)\theta_1+\lambda\theta_2.
$$

若 loss barrier

$$
B=\max_{\lambda\in[0,1]}
\mathcal L(\theta(\lambda))
-\max(\mathcal L(\theta_1),\mathcal L(\theta_2))
$$

很大，中点可能很差。Soup 成功的经验直觉是 fine-tuned models 在可连通低误差区域内。

但只在一个 validation distribution 上 barrier 低，不保证安全/OOD/function behavior 同样低。

## 四、Task vector 与参数算术

从共同 base $\theta_0$ 得 task checkpoints：

$$
\theta_k=\theta_0+\tau_k,
\qquad
\tau_k=\theta_k-\theta_0.
$$

可构造：

### Add

$$
\theta_{\text{merge}}
=\theta_0+\sum_k\alpha_k\tau_k.
$$

### Negate

$$
\theta_{\text{remove}}
=\theta_0-\alpha\tau_k.
$$

### Analogy

对有相同坐标语义的 vectors 做差/加，测试行为能否转移。

关键是 $\tau_k$ 依共同 base。若误用：

$$
\tau_1=\theta_1-\theta_0^{(A)},
\qquad
\tau_2=\theta_2-\theta_0^{(B)},
$$

再相加，混入了 bases 之间差异。

## 五、参数线性为何有时近似函数线性

在 $\theta_0$ 附近做 Taylor：

$$
f_{\theta_0+\delta}(x)
\approx
f_{\theta_0}(x)
+J_{\theta_0}(x)\delta
+\frac12\delta^\top H(x)\delta.
$$

若 task vectors 小、共享局部线性区且交叉二阶项弱：

$$
f_{\theta_0+\tau_1+\tau_2}
\approx
f_{\theta_0}
+J\tau_1+J\tau_2.
$$

这提供局部解释，不是全局定理。大 vectors、不同 basins、norm 非线性、激活边界和冲突方向会使 Hessian/cross terms 重要。

所以：

$$
\text{parameter addition}
\not\equiv
\text{function addition}.
$$

## 六、干扰的三种层次

### 坐标符号冲突

同一坐标有 $\tau_{1j}>0,\tau_{2j}<0$。

### 梯度/局部几何冲突

即使符号同向，不同尺度或 Hessian 方向也可互相破坏。

### 功能/任务冲突

两个任务的最优输出本来互斥，任何单模型需折中。

TIES 主要处理第一类 proxy 和小幅更新冗余，不能消除所有功能冲突。

## 七、TIES 三步

给 task vectors $\{\tau_k\}$。

### 1. Trim

每个 vector 保留绝对值较大的 top-density 坐标：

$$
\widetilde\tau_{kj}
=\tau_{kj}1\{|\tau_{kj}|\ge q_k\}.
$$

$q_k$ 由 density/quantile 决定。小值被置零，不表示它们客观无功能作用。

### 2. Elect sign

对坐标 $j$ 汇总：

$$
s_j=\operatorname{sign}
\left(\sum_k\widetilde\tau_{kj}\right)
$$

或采用论文/实现规定的 sign election。Tie/zero policy 必须明确。

### 3. Merge aligned values

只聚合与 $s_j$ 同号的 task updates：

$$
\tau_j^{*}
=\operatorname{Agg}
\{\widetilde\tau_{kj}:
\operatorname{sign}(\widetilde\tau_{kj})=s_j\}.
$$

最终：

$$
\theta_*=\theta_0+\lambda\tau^*.
$$

Density、aggregation、scale $\lambda$ 都是超参数。

## 八、逐坐标 toy

三个 vectors 在某坐标：

$$
(0.8,0.6,-0.1).
$$

若 trim 删除 $|v|<0.2$，得到 $(0.8,0.6,0)$；elected sign 为正；均值 merge 得 $0.7$。

另一坐标：

$$
(-0.7,0.5,-0.6)
$$

负方向总量更大，elect negative；只平均负值，得 $-0.65$。这不同于普通平均 $-0.2667$。

但选择负方向只是参数 proxy；最终哪个任务改善必须实测。

## 九、LoRA/Adapter 的合并边界

若 LoRA adapters 共享精确 base：

$$
\tau_k=s_kB_kA_k.
$$

可先 materialize $\tau_k$ 再做 task arithmetic/TIES，或在低秩形式组合。注意：

- 多个低秩和的 rank 可增长；
- 不同 target modules 需补零对齐；
- 不同 fan-in/fan-out、scale/merge state 会错位；
- quantized base 重 merge 有额外舍入；
- Adapter 含非线性模块时不能简单映射为 base-weight task vector。

“模型合并”可能指 full weights、LoRA deltas、adapter composition 或输出 ensemble；必须命名对象。

## 十、证据地图：一次合并结果支持到哪里

| 主张 | 最低证据 |
|---|---|
| 参数文件可相加 | shape/name/base/tokenizer hashes |
| merge 实现正确 | hand-computed coordinates + serialization round-trip |
| 插值在低 loss 区 | barrier curve，多 seeds/candidates |
| 多任务性能改善 | 每任务 matched eval + CI |
| OOD/鲁棒改善 | 独立 OOD slices |
| 无安全退化 | threat-model safety set 与 adaptive tests |
| 比 ensemble 便宜 | 同硬件 latency/memory/throughput |
| 可迁移到更多任务 | unseen tasks/scales，不只已调 merge set |

不能从参数 norm、符号一致率或平均 benchmark 单独推出最后四项。

## 十一、图解：三个方法的共同坐标与不同假设

先看图回答：Soup 直接平均 checkpoints，task arithmetic 为什么要先减共同 base，TIES 又在哪一步丢弃坐标？

![[00-知识库管理/_assets/figures/language-models/fig-lm-adapt-merge-ties-v1.svg|900]]

> [!figure] 图 LM-32　共同 base、task vectors 与 TIES 逐坐标 toy
> 上方显示 $\theta_k=\theta_0+\tau_k$；中部并列 soup、task arithmetic、TIES；下表执行 trim、elect sign 与 aligned merge。
> **生成：**本图由本库依据本节定义、正文列出的一级来源和固定绘图脚本重新绘制；图中的小规模数值或结构用于教学，不复刻论文原图。

**怎样读图**：先核对所有 arrows 是否来自同一 $\theta_0$，再逐坐标重算 TIES；最后把 merged parameter 送入独立评估，不把表内结果当性能。

**图没有证明什么**：toy sign election 不证明 TIES 全局最优，不证明参数空间线性，也不覆盖 permutation alignment 或不同 tokenizer 的模型。

## 十二、最小合并审计

1. 保存 base 与 ingredients 的 hashes/config/tokenizer/template；
2. 验证每个 task vector 可重构 ingredient；
3. 报 soup weights 或 task-vector coefficients；
4. 报 TIES density、election、aggregation、scale；
5. 扫 interpolation/barrier 与 coefficient sensitivity；
6. 每任务、平均、worst-task、OOD、安全、calibration 分报；
7. 与 single best、uniform/greedy soup、ensemble、multi-task tuning 比较；
8. 计 candidate training、validation search 与推理成本；
9. 保存失败 merges，不只保留 winner。

## 本节出口

你应能在小向量上手算 soup、task arithmetic 与 TIES，并解释它们需要共同 base/坐标与独立功能评估。通过本卷累计门后，下一卷进入不更新参数的适配：[[70.5 上下文学习与推理时计算 MOC]]。

## 练习与独立解答

- [[习题 - Model Soup、Task Arithmetic、TIES 与适配证据地图]]
- [[解答 - Model Soup、Task Arithmetic、TIES 与适配证据地图]]

---
type: concept
status: verified
area: [language-models, peft, lora, low-rank-optimization]
node_id: LM-29
aliases: [LoRA 推导, Low-rank adaptation, LoRA merge]
prerequisites: ["[[SVD 算法与谱范数估计]]", "[[全量微调、冻结表示与灾难性遗忘]]"]
related: ["[[QLoRA、量化基座与适配显存总账]]", "[[Model Soup、Task Arithmetic、TIES 与适配证据地图]]"]
sources: ["[[S-2021-Hu-LoRA]]", "[[S-2024-Su-10001-LoRA差分学习率]]"]
exercises: ["[[习题 - LoRA 的低秩更新、初始化、缩放与合并]]"]
solutions: ["[[解答 - LoRA 的低秩更新、初始化、缩放与合并]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-adapt-lora-factorization-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# LoRA 的低秩更新、初始化、缩放与合并

> [!abstract] 一句话结论
> LoRA 冻结基座矩阵 $W_0$，把可训练增量限制为 $\Delta W=sBA$。低秩的是参数增量，不是整个模型；初始化决定首步哪一因子能收到梯度，缩放决定有效步长，merge 只在精确 dtype/量化合同下保持函数等价。

## 一、从一个线性层开始

采用列向量约定：

$$
x\in\mathbb R^n,\qquad
W_0\in\mathbb R^{m\times n},\qquad
y=W_0x.
$$

LoRA 令

$$
W=W_0+\Delta W,
\qquad
\Delta W=sBA,
$$

其中

$$
A\in\mathbb R^{r\times n},
\qquad
B\in\mathbb R^{m\times r}.
$$

前向：

$$
y=W_0x+sB(Ax).
$$

$W_0$ 冻结，$A,B$ 可训练，$s$ 是显式 scale。对 batch 行向量实现时矩阵转置顺序会变化，但 shape 不变量必须保持。

## 二、参数量与秩上界

Full update 有 $mn$ 个自由参数；LoRA 有

$$
P_{\text{LoRA}}=r(n+m).
$$

压缩比例：

$$
\rho=\frac{r(n+m)}{mn}.
$$

例如 $m=n=4096,r=8$：

$$
P_{\text{LoRA}}=8(4096+4096)=65536,
$$

而 full matrix 有 $4096^2=16{,}777{,}216$，该层增量参数约为 0.39%。

又因

$$
\operatorname{rank}(BA)
\le \min(\operatorname{rank}A,\operatorname{rank}B)
\le r,
$$

所以增量 rank 至多 $r$。但要注意：

- $W_0+\Delta W$ 的总 rank 可很高；
- 神经网络函数变化经非线性和多层复合，不是 rank-$r$ 函数；
- 训练轨迹在因子 $(A,B)$ 中非凸，即使 $\Delta W$ 空间是矩阵空间。

## 三、LoRA 不是“对 full update 做截断 SVD”

截断 SVD 的问题是：给定一个已知矩阵 $\Delta W^*$，寻找最佳 rank-$r$ 逼近。LoRA 则直接通过任务 loss 学 $A,B$：

$$
\min_{A,B}
\mathcal L(W_0+sBA).
$$

训练前没有已知的 full-finetuning $\Delta W^*$。只有在额外做 full FT 后再分解，才是 post-hoc low-rank approximation；其优化路径和 LoRA 不相同。

因此“LoRA 的理论依据是 Eckart–Young”最多是表达能力直觉，不能当训练最优性证明。

## 四、梯度怎样流过两个因子

令

$$
G=\frac{\partial\mathcal L}{\partial \Delta W}
\in\mathbb R^{m\times n}.
$$

由矩阵微分：

$$
d\mathcal L
=\langle G,s\,dB\,A+sB\,dA\rangle_F.
$$

得到

$$
\frac{\partial\mathcal L}{\partial B}
=sGA^\top,
\qquad
\frac{\partial\mathcal L}{\partial A}
=sB^\top G.
$$

这立刻解释初始化。

### A 随机、B=0

初始 $\Delta W=0$，因此首个前向与 base 完全相同。首步：

$$
\nabla_B\mathcal L=sGA^\top
$$

通常非零，而

$$
\nabla_A\mathcal L=sB^\top G=0.
$$

先由 $B$ 离开零，下一步 $A$ 才开始收到梯度。

### A=0、B 随机

结论对调：首步 $A$ 可更新，$B$ 梯度为零。

### A=B=0

两个梯度都为零，优化卡死。这不是“更稳定的零初始化”，而是双线性参数化的鞍/静止点。

## 五、缩放 $s$ 不只是记号

常见约定把

$$
s=\alpha/r
$$

写进前向，也有随 rank 采用其他归一化的变体。无论名称，$s$ 同时改变：

- 初始有效输出尺度；
- 两因子梯度幅度；
- 给定 learning rate 下 $\Delta W$ 的有效步长；
- 不同 rank 的可比性；
- merge 后的实际增量。

不能只报告 rank 而漏 $\alpha/s$。若 $A$、$B$ 使用不同学习率，首步和宽度标度更会改变；[[S-2024-Su-10001-LoRA差分学习率]]提供中文推导入口，但跨模型结论仍需实验。

## 六、因子参数化有尺度不唯一性

对任意非零 $c$：

$$
BA=(cB)(A/c).
$$

所以同一个 $\Delta W$ 有无限多因子表示。Weight decay、optimizer 自适应状态和不同学习率作用在 $A,B$ 上时，不再只依赖乘积 $BA$；它们会选择不同因子路径。

更一般地，对可逆 $R\in\mathbb R^{r\times r}$：

$$
BA=(BR)(R^{-1}A).
$$

因此比较因子 norm 时要谨慎；真正部署函数取决于乘积和 scale，但训练动力学依因子坐标。

## 七、Target modules 决定可达函数族

LoRA 可施加在：

- attention 的 query/key/value/output projections；
- FFN up/down/gate projections；
- embedding 或 output head；
- 部分层或全部层。

总参数量：

$$
P=\sum_{\ell\in\mathcal T}
r_\ell(m_\ell+n_\ell)
$$

再加可训练 bias/normalization 等。写“rank 8 LoRA”没有唯一含义；必须列 $\mathcal T$、每层 rank、scale、dropout、bias policy。

只改 $Q,V$ 与改所有线性层的容量、显存、通信和 merge artifact 都不同。

## 八、Merge equivalence

未 merge：

$$
y=W_0x+sB(Ax).
$$

merge 后：

$$
W_*=W_0+sBA,
\qquad
y=W_*x.
$$

在精确算术中由分配律完全相等。工程 oracle：

1. 固定 $W_0,A,B,s,x$；
2. 分别算 merged/unmerged logits；
3. 比较 max absolute/relative error；
4. 覆盖 batch、dtype、bias、transpose/fan-in-fan-out；
5. merge→unmerge 后恢复原 hash 或在容差内恢复。

浮点中运算顺序不同会有小误差；若 base 是 quantized，merge 通常需 dequantize、相加、再 quantize，函数可能进一步改变。不能把普通 LoRA 的代数等价直接搬到量化 artifact。

## 九、多 Adapter 的线性组合

若多个 LoRA 共享同一 base：

$$
W=W_0+\sum_{k=1}^{K}\lambda_kB_kA_k.
$$

总增量 rank 上界：

$$
\operatorname{rank}\left(\sum_k\lambda_kB_kA_k\right)
\le\sum_kr_k.
$$

但 task functions 不按 $\lambda$ 线性相加。不同 adapters 可在同坐标产生相反更新，scale 需验证；进一步连接[[Model Soup、Task Arithmetic、TIES 与适配证据地图]]。

## 十、显存与速度不能由参数比直接推出

LoRA 通常节省 trainable weights、gradients、optimizer states 和多任务 checkpoint storage；但仍有：

- frozen base storage；
- 完整 base 前向 FLOPs；
- activations；
- LoRA 中间 $Ax$；
- dataloader、kernel 和通信；
- 未 merge 时的额外 matmuls。

因此：

$$
\frac{P_{\text{trainable}}}{P_{\text{base}}}
\ne
\frac{M_{\text{peak,LoRA}}}{M_{\text{peak,full}}}
\ne
\frac{t_{\text{LoRA}}}{t_{\text{full}}}.
$$

都需实测。

## 十一、图解：形状、首步梯度与 merge

先看图回答：为什么 $A,B$ 都初始化为零会卡死，而只把一个因子置零不会？

![[00-知识库管理/_assets/figures/language-models/fig-lm-adapt-lora-factorization-v1.svg|900]]

> [!figure] 图 LM-29　LoRA 因子化、初始化梯度表与 merge oracle
> 上方从 frozen $W_0$ 和 trainable $sBA$ 构造前向；中部列三种初始化首步梯度；下部给 merged/unmerged 的代数恒等式测试。
> **生成：**本图由本库依据本节定义、正文列出的一级来源和固定绘图脚本重新绘制；图中的小规模数值或结构用于教学，不复刻论文原图。

**怎样读图**：先核对 $A,B$ 形状和乘法顺序，再用梯度公式逐格验证表；最后区分训练参数化与部署权重。

**图没有证明什么**：它不证明低 rank 对所有任务足够，不证明某初始化/scale 全局最优，也不证明量化重 merge 精确等价。

## 十二、研究报告最小字段

- base checkpoint/tokenizer/template hashes；
- target modules 与层范围；
- $r,\alpha,s$ 和实际前向公式；
- A/B initialization、learning rates、optimizer/weight decay；
- dropout、bias/norm trainability；
- trainable/total parameters；
- weights/grads/optimizer/activation/peak bytes；
- merged/unmerged/quantized deployment 状态；
- 多 seed 与 full/freeze baselines；
- new/old/safety/function-drift 指标。

## 本节出口

你应能手算 shape、参数量、rank 上界、首步梯度与 merge，并拒绝“低秩=低显存=不遗忘”的连环偷换。下一节把 frozen base 进一步量化：[[QLoRA、量化基座与适配显存总账]]。

## 练习与独立解答

- [[习题 - LoRA 的低秩更新、初始化、缩放与合并]]
- [[解答 - LoRA 的低秩更新、初始化、缩放与合并]]

---
type: synthesis
status: verified
area: [training, optimization, lion, adafactor, evidence]
node_id: TRN-16
aliases: [Lion 与 Adafactor, 自适应优化器比较]
prerequisites: ["[[L2 正则、Coupled Decay 与 AdamW]]", "[[Adam 的尺度不变性、Sign 近似与 Update RMS]]", "[[训练集、验证集、测试集与自适应复用]]"]
related: ["[[Shampoo、逆矩阵根与 Kronecker 预条件]]", "[[Muon 的动量、正交化与参数分组合同]]", "[[训练实验协议、事故记录与因果证据地图]]"]
sources: ["[[S-2018-Shazeer-Stern-Adafactor]]", "[[S-2023-Chen-Lion]]", "[[S-2026-Framework-Adaptive-Optimizer-Semantics]]", "[[S-2019-Loshchilov-Hutter-AdamW]]"]
exercises: ["[[习题 - Lion、Adafactor 与自适应优化器证据地图]]"]
solutions: ["[[解答 - Lion、Adafactor 与自适应优化器证据地图]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-lion-adafactor-evidence-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Lion、Adafactor 与自适应优化器证据地图

> [!abstract] 一句话结论
> Lion 用一份 momentum 和 sign direction 换取较低状态内存；Adafactor 用矩阵 row/column factors 近似二阶矩并配合 relative step、update clipping 等控制。二者都不只是“省 Adam 一份状态”的单变量改造；比较必须同时核对算法合同、参数组、总内存、吞吐、调参预算与质量不确定性。

## 一、先建立共同对照表

令参数总数为 $P$。这里只统计 optimizer persistent states，不含参数、gradient、master weights、activation 与临时 kernel buffer。

| 方法 | 主要状态 | 粗略状态量 | direction 结构 |
|---|---|---:|---|
| SGD | 无 | 0 | raw gradient |
| Momentum | 一阶 buffer | $P$ | smoothed gradient |
| Adam/AdamW | $m,v$ | $2P$ | first moment / RMS |
| AMSGrad | $m,v,v^{max}$ | $3P$ | long-memory RMS |
| Lion | momentum | $P$ | sign of momentum mixture |
| Adafactor | matrix row/column factors；vector fallback | 对 $n\times m$ 为 $n+m$ | factored RMS + clipping/relative step |

“状态量减半”不等于训练总内存减半。若 activation 占主导、optimizer 已分片/offload 或低精度 state 使用不同字节数，端到端收益会变化。

## 二、Lion 的两时标 sign 更新

根据 [[S-2023-Chen-Lion]]，Lion 的常见核心可写成

$$
c_t=\beta_1m_{t-1}+(1-\beta_1)g_t,
$$

$$
\theta_t=(1-\eta_t\lambda_t)\theta_{t-1}
-\eta_t\operatorname{sign}(c_t),
$$

$$
m_t=\beta_2m_{t-1}+(1-\beta_2)g_t.
$$

$\beta_1$ 用于当前 update mixture，$\beta_2$ 更新长期状态；顺序与两个 beta 不可交换。每个非零坐标的 direction magnitude 为 1，但：

- layer update RMS 还受 zero/tie、parameter group 与 LR 影响；
- decoupled decay 另加 $-\eta\lambda\theta$；
- sign 对小数值噪声敏感，gradient scale 被强烈归一化；
- 同一 LR/decay 数值未必能与 AdamW 公平复用。

Lion 的一个状态比 Adam 的两个状态更省；但 sign kernel、parameter update、communication 和 convergence behavior 仍需实测。

## 三、Adafactor 怎样分解二阶状态

对矩阵参数 $W\in\mathbb R^{n\times m}$，完整二阶 EMA $V_t$ 需 $nm$ 个数。Adafactor 保存 row/column marginals：

$$
r_i=\frac1m\sum_{j=1}^m V_{ij},
\qquad
c_j=\frac1n\sum_{i=1}^n V_{ij},
$$

并用

$$
\widehat V_{ij}
=\frac{r_ic_j}{\frac1n\sum_{k=1}^n r_k}
$$

重建逐元素尺度。该构造匹配 row/column averages；它不是把 $V$ 做 SVD 后的最佳 rank-1 逼近，也不是 Hessian factorization。

状态由 $nm$ 降为 $n+m$；对大矩阵节省显著，对 vector 参数则没有同样收益，需要 full vector state 或 fallback。

## 四、Adafactor 不只改了存储

原论文还讨论：

- 随 step 变化的 second-moment decay；
- update RMS clipping，防止慢 denominator 产生过大更新；
- relative step 与 parameter RMS scaling；
- 可选地省掉 first-moment momentum。

因此“Adafactor 与 Adam 的差别就是 $v$ 做 factorization”是错误消融。若实验同时改变 LR schedule、momentum、clipping 和 parameter scaling，性能差异不能只归因于内存近似。

当前 PyTorch 文档还明确其实现与原论文/部分框架在 LR、$\epsilon_1$ 和 decay 上存在差异；报告必须引用真实实现，而不是只引用论文算法框。

## 五、factored statistic 的最小例子

考虑

$$
V=
\begin{bmatrix}
1&9\\
4&16
\end{bmatrix}.
$$

row means 为 $(5,10)$，column means 为 $(2.5,12.5)$，global mean 为 $7.5$，故重建

$$
\widehat V
=\frac1{7.5}
\begin{bmatrix}5\\10\end{bmatrix}
\begin{bmatrix}2.5&12.5\end{bmatrix}
=
\begin{bmatrix}
1.667&8.333\\
3.333&16.667
\end{bmatrix}.
$$

row/column means 得到保持，但元素有误差。若真实平方梯度结构接近可分离，误差小；强非可分结构则可能丢失重要坐标尺度。

## 六、证据比较必须锁定哪些变量

### 6.1 算法账

- exact equation、state initialization、epsilon、clipping、decay；
- sparse/vector/matrix fallback；
- parameter groups 与 zero gradient/step skip。

### 6.2 资源账

- state bytes、master weights、gradient、activation、temporary buffers；
- optimizer FLOPs、kernel launches、communication、offload；
- tokens/s、step time、peak memory、energy（若可得）。

### 6.3 质量账

- compute/token/step-matched 哪一种；
- LR/decay/beta/clipping 的搜索预算是否相等；
- 多 seed 或 paired data order；
- best checkpoint 选择规则、失败运行与置信区间。

只有在这些账本锁定后，才能把“方法 A 更好”缩小成可复查的范围声明。

## 七、不同任务为何可能偏好不同方法

- 巨型 embedding/softmax matrix：稀疏性与状态内存可能主导；
- dense Transformer pretraining：AdamW 的成熟配方和稳定性是强基线；
- memory-limited fine-tuning：Adafactor/Lion 的状态收益可能更重要；
- 非平稳 RL：二阶时标、sign sensitivity 与 clipping 交互更明显；
- 分布式 ZeRO/FSDP：状态分片后，optimizer state 的边际收益要与 communication/activation 一起重算。

这不是推荐表，而是实验分层：任务属性只生成候选假说，不替代 benchmark。

## 八、图：从状态字节到证据结论的四道门

先看图回答：Lion/Adafactor 分别省掉哪份状态？为什么“state 少”不能直接推出“wall time 快、质量更好”？

![[00-知识库管理/_assets/figures/training-optimization/fig-lion-adafactor-evidence-v1.svg|900]]

> [!figure] 图 TRN-16　Adam、Lion、Adafactor 的状态结构与证据门
> 左侧按参数张量画 persistent states；中间展示 Lion sign path 与 Adafactor row/column reconstruction；右侧要求依次通过算法、资源、调参和统计四道门。来源：据 [[S-2018-Shazeer-Stern-Adafactor]]、[[S-2023-Chen-Lion]] 与当前框架文档独立绘制。

**怎样读图**：先只比较同 dtype 的持久状态，再加回完整训练内存；随后检查方法是否同时改了 update rule，最后才看质量曲线。

**图没有证明什么**：图不证明 Lion 或 Adafactor 普遍优于 AdamW，也不把低状态复杂度等同于低总成本。

## 九、60.2 的总出口

学完本卷应能对一个陌生自适应优化器完成：

$$
\text{gradient}
\to\text{state kernels}
\to\text{metric/normalization}
\to\text{epsilon/decay}
\to\text{memory/system}
\to\text{evidence}.
$$

下一卷 [[曲率、自然梯度与矩阵预条件 MOC]]会从 diagonal statistics 进入 Hessian、Fisher、GGN 与 matrix preconditioner；不能把 Adam/Adafactor 的二阶原始矩直接重命名为曲率。

## 练习与独立解答

- [[习题 - Lion、Adafactor 与自适应优化器证据地图]]
- [[解答 - Lion、Adafactor 与自适应优化器证据地图]]
- 卷级复现：[[实验 - 自适应优化器状态、尺度与反例数值审计]]

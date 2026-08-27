---
type: derivation
status: verified
area: [training, optimization, adagrad]
node_id: TRN-09
aliases: [AdaGrad 几何, 累计平方梯度]
prerequisites: ["[[Mini-batch 梯度、平均求和与有效 Batch]]", "[[自适应优化方法]]", "[[梯度、方向导数与最陡方向]]"]
related: ["[[RMSProp、滑动二阶矩与非平稳尺度]]", "[[近端算子、复合优化与稀疏正则]]", "[[Embedding Lookup、稀疏梯度与参数规模]]"]
sources: ["[[S-2011-Duchi-AdaGrad]]", "[[S-2026-Framework-Adaptive-Optimizer-Semantics]]"]
exercises: ["[[习题 - AdaGrad、累计平方梯度与稀疏几何]]"]
solutions: ["[[解答 - AdaGrad、累计平方梯度与稀疏几何]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-adagrad-coordinate-geometry-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# AdaGrad、累计平方梯度与稀疏几何

> [!abstract] 一句话结论
> AdaGrad 不只是“给每个参数一个学习率”：它用截至当前的梯度平方总账定义一个随数据变化的对角度量。历史上经常出现或幅值很大的坐标会被更强地抑制，少见坐标保留较大的相对步长；代价是总账不遗忘，非平稳训练后期可能过度保守。

## 一、为什么同一个学习率不一定公平

考虑二维参数 $\theta=(\theta_1,\theta_2)$。若第一坐标的典型梯度是 $10^2$，第二坐标是 $10^{-2}$，普通 SGD

$$
\theta_{t+1,i}=\theta_{t,i}-\eta g_{t,i}
$$

要求一个标量 $\eta$ 同时照顾四个数量级：对第一坐标不发散的步长，可能让第二坐标几乎不动。问题不是“梯度方向错了”，而是坐标单位和历史尺度没有进入几何。

AdaGrad 为每个坐标建立累计平方梯度

$$
G_{t,i}=\tau_i+\sum_{s=1}^{t}g_{s,i}^2,
$$

再更新

$$
\boxed{
\theta_{t+1,i}
=\theta_{t,i}-\eta\frac{g_{t,i}}{\sqrt{G_{t,i}}+\epsilon}
}.
$$

$\tau_i\ge0$ 是初始 accumulator；$\epsilon$ 是数值/尺度 floor。两个量都属于算法合同，不是可省略的代码细节。

## 二、从 variable metric 推出更新

先忽略约束和 epsilon。定义

$$
H_t=\operatorname{diag}(\sqrt{G_{t,1}},\ldots,\sqrt{G_{t,d}}).
$$

在当前点解局部问题

$$
\theta_{t+1}
=\arg\min_{\theta}
\left\{
g_t^\top(\theta-\theta_t)
+\frac{1}{2\eta}\|\theta-\theta_t\|_{H_t}^2
\right\},
$$

其中 $\|x\|_{H_t}^2=x^\top H_tx$。一阶条件给出

$$
g_t+\frac1\eta H_t(\theta_{t+1}-\theta_t)=0,
$$

所以

$$
\theta_{t+1}=\theta_t-\eta H_t^{-1}g_t.
$$

这说明 denominator 不是事后“除一下梯度”，而是单位球变了：在累计梯度大的坐标上，移动同样距离被判定为更昂贵。

> [!warning] 对角不等于坐标无关
> 若旋转参数坐标，$\operatorname{diag}(G_t)$ 一般不会按张量规律恢复同一个 full-matrix metric。Diagonal AdaGrad 计算便宜，却把参数化坐标写进算法。

## 三、稀疏坐标为何会得到相对更大步长

取 $\tau=\epsilon=0$。坐标 A 在前四步梯度都是 1；坐标 B 只在第 4 步出现一次，梯度也是 1。第 4 步前后：

$$
G_{4,A}=4,
\qquad
G_{4,B}=1.
$$

因此第 4 步更新幅值为

$$
|\Delta\theta_{4,A}|=\eta/2,
\qquad
|\Delta\theta_{4,B}|=\eta.
$$

少见坐标 B 得到两倍的相对步长。这是稀疏文本特征、推荐系统 ID 和 embedding 参数中很有吸引力的性质。

但“少见”并不等于 denominator 必然小。若 B 唯一一次梯度为 100，则 $G_{4,B}=10^4$，更新幅值仍约为 $\eta$，而不是 100 倍。AdaGrad 追踪的是**平方幅值总账**，不是出现次数计数器。

## 四、为什么累计量会越来越保守

若某坐标每步恒有 $g_{t,i}=g\ne0$，则

$$
G_{t,i}=\tau_i+t g^2,
\qquad
\frac{|g|}{\sqrt{G_{t,i}}}sim\frac1{\sqrt t}.
$$

单步有效尺度衰减为 $t^{-1/2}$。不过累计位移并不收敛，因为

$$
\sum_{t=1}^{T}\frac1{\sqrt t}\approx2\sqrt T;
$$

所以“学习率最终变成零”是过度说法。准确结论是：在持续出现的坐标上，边际步长越来越小；若任务尺度在中途改变，早期历史永远留在 denominator 中。

## 五、在线 regret 为什么是 data-dependent

在凸在线优化、bounded feasible set 和受控 subgradient 等条件下，diagonal AdaGrad 的典型 regret 形式可写成

$$
R_T
=O\!\left(
D_\infty\sum_{i=1}^d
\sqrt{\sum_{t=1}^T g_{t,i}^2}
\right).
$$

它不是只依赖最坏情形的 $\sqrt{dT}$，而会随真实坐标梯度序列变化。若只有少量坐标活跃，和式可能明显更小。

> [!theorem] 结论边界
> 这是在线凸优化的保证模板；具体常数、投影、regularizer 与初始化依论文版本而定。它不能直接推出非凸深网到达全局最优，也不能证明 AdaGrad 在 wall time 上优于 SGD。

## 六、epsilon 与初始 accumulator 分别做什么

常见实现是

$$
\frac{g_t}{\sqrt{G_t}+\epsilon}.
$$

- $\epsilon$ 在 denominator 上设置最小尺度，并避免 $G=0$ 时除零；
- $\tau$ 从第一步就改变 $G_t$，相当于给历史能量一个先验底座；
- $\tau>0$ 与增大 $\epsilon$ 不完全等价，因为一个在根号内随累计量组合，一个在根号外相加；
- PyTorch 当前 AdaGrad 还单独提供 `lr_decay`，所以“有效学习率下降”可能同时来自累计量和显式 schedule。

## 七、reduction 与单位仍然必须对齐

若 loss 从 batch mean 改为 batch sum，gradient 放大 $B$ 倍，累计平方量放大 $B^2$ 倍。在 $\tau=\epsilon=0$ 且整个历史都同步缩放时：

$$
\frac{Bg_t}{\sqrt{\sum_s(Bg_s)^2}}
=\frac{g_t}{\sqrt{\sum_sg_s^2}},
$$

方向确有尺度不变性。但只在中途改变 reduction、epsilon 不缩放、已有 accumulator 未翻译时，轨迹会分叉。不要把理想恒等式当 checkpoint 热切换许可。

## 八、图：两只坐标里程表怎样改变几何

先看图回答：同样大小的当前梯度，为什么历史频繁坐标的箭头更短？

![[00-知识库管理/_assets/figures/training-optimization/fig-adagrad-coordinate-geometry-v1.svg|900]]

> [!figure] 图 TRN-09　累计平方梯度、坐标单位球与稀疏更新
> 左侧把每个坐标的 $G_{t,i}$ 画成只增不减的里程表；中间比较圆形 SGD 单位球与 AdaGrad 椭圆 metric；右侧给出频繁/稀有坐标同一当前梯度下的不同有效步长。来源：依据 [[S-2011-Duchi-AdaGrad]] 的对象独立绘制。

**怎样读图**：先比较两个 accumulator，再看 metric 轴长，最后核对 update 分母；不要只看箭头长短猜算法优劣。

**图没有证明什么**：图不证明稀疏坐标一定更重要，也不证明对角 metric 能恢复 Hessian eigenvectors；它只解释累计平方尺度的机制。

## 九、AI 系统接口

- embedding lookup 可能产生稀疏 gradient；要确认优化器是否真正支持 sparse tensor，而不是先 densify；
- tied embedding/output weight 会把两个梯度来源合并进同一 accumulator；
- 参数分片时 accumulator 与参数同分片，checkpoint 必须保存其 dtype、shape 和 initial value；
- mixed precision 中通常应以更高精度保存 accumulator，否则长期小增量可能被吸收；
- 稀有 token 的大更新可能需要 clipping，但逐坐标/全局 clipping 会改变 AdaGrad 原 estimator。

## 十、本节回顾

- AdaGrad 是 data-dependent diagonal metric，不只是“自动调 LR”；
- 稀疏优势来自累计平方梯度，而非只数出现次数；
- 对角法依赖坐标系，不等于 full-matrix whitening；
- 永久累计带来非平稳适应迟缓；
- 下一节 [[RMSProp、滑动二阶矩与非平稳尺度]] 用遗忘窗口替代永久总账。

## 练习与独立解答

- [[习题 - AdaGrad、累计平方梯度与稀疏几何]]
- [[解答 - AdaGrad、累计平方梯度与稀疏几何]]
- 卷级复现：[[实验 - 自适应优化器状态、尺度与反例数值审计]]

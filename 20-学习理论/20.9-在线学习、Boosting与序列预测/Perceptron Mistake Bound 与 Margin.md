---
type: theorem
status: draft
area: [learning-theory/online-learning, perceptron, margin]
aliases: [Perceptron Convergence Theorem, Novikoff Bound, 感知机错误界]
node_id: LT-73
prerequisites: ["[[在线学习协议、Regret 与 Comparator]]", "[[内积空间]]", "[[分类间隔、Margin Bound 与 SVM 接口]]"]
related: ["[[线性回归的统计学习理论]]", "[[支持向量机、最大间隔与核方法]]", "[[Online-to-Batch Conversion]]"]
sources: ["[[S-1958-Rosenblatt-Perceptron]]", "[[S-1962-Novikoff-Perceptron]]", "[[S-2012-Shalev-Online-Learning-OCO]]"]
exercises: ["[[习题 - Perceptron Mistake Bound 与 Margin]]"]
solutions: ["[[解答 - Perceptron Mistake Bound 与 Margin]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-perceptron-margin-mistakes-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# Perceptron Mistake Bound 与 Margin

> [!abstract] 本章主问题
> Perceptron 为什么能在任意顺序的线性可分序列上只犯有限次错误？证明不依赖数据分布，而依赖两个互相挤压的量：每次错误都朝分隔方向取得至少 $\gamma$ 的进展，但权重范数至多按 $\sqrt M$ 增长。

## 一、学习目标

完成本章后，应能：

1. 写出 homogeneous Perceptron 的预测与更新；
2. 准确声明 $R$、$\gamma$ 与 unit separator；
3. 从零推导 $M\le(R/\gamma)^2$；
4. 解释证明为何只在 mistake rounds 索引；
5. 区分 mistake bound、迭代次数与 population risk；
6. 说明缩放不改变真正复杂度 $R/\gamma$；
7. 用增广坐标处理 bias；
8. 解释不可分/有噪声时 theorem 哪一步失效；
9. 连接 hinge loss、SVM、kernel Perceptron 与 averaged Perceptron；
10. 审计“Perceptron 收敛”这一句话到底承诺什么。

## 二、对象合同

序列为 $(x_t,y_t)$，其中

$$
x_t\in\mathbb R^d,\qquad y_t\in\{-1,+1\},\qquad \|x_t\|_2\le R.
$$

初始化 $w_1=0$。第 $t$ 轮先预测

$$
\widehat y_t=\operatorname{sign}\langle w_t,x_t\rangle,
$$

若 $y_t\langle w_t,x_t\rangle\le0$，记一次 mistake/update：

$$
\boxed{w_{t+1}=w_t+y_tx_t.}
$$

否则 $w_{t+1}=w_t$。把零 margin 也更新可避免 tie convention 干扰证明。

## 三、可分性与 Margin 假设

存在单位向量 $u$，使每轮

$$
\|u\|_2=1,\qquad y_t\langle u,x_t\rangle\ge\gamma>0.
$$

$\gamma$ 是相对于输入范数和 separator 归一化后的几何 margin。若不约束 $\|u\|$，把 $u$ 放大即可让数值 margin 任意大，定理失去内容。

## 四、只看错误轮次

设算法总共犯 $M$ 次错误，按发生顺序记错误样本为 $(x_{t_k},y_{t_k})$。由于只有错误才更新，最终权重为

$$
w_{M+1}=\sum_{k=1}^M y_{t_k}x_{t_k}.
$$

证明的时间轴是 **update count** $k$，不是原始轮次 $t$。正确预测之间可以隔任意多轮。

## 五、第一条账：朝正确方向线性进展

每次更新后，

$$
\begin{aligned}
\langle w_{k+1},u\rangle
&=\langle w_k+y_{t_k}x_{t_k},u\rangle\\
&=\langle w_k,u\rangle+y_{t_k}\langle x_{t_k},u\rangle\\
&\ge\langle w_k,u\rangle+\gamma.
\end{aligned}
$$

从 $w_1=0$ telescope：

$$
\boxed{\langle w_{M+1},u\rangle\ge M\gamma.}
$$

这是一条线性下界：每犯一次错，沿真实 separator 至少前进 $\gamma$。

## 六、第二条账：范数只能平方根增长

在 mistake round，$y_{t_k}\langle w_k,x_{t_k}\rangle\le0$，因此

$$
\begin{aligned}
\|w_{k+1}\|^2
&=\|w_k+y_{t_k}x_{t_k}\|^2\\
&=\|w_k\|^2+2y_{t_k}\langle w_k,x_{t_k}\rangle+\|x_{t_k}\|^2\\
&\le\|w_k\|^2+R^2.
\end{aligned}
$$

再次 telescope：

$$
\boxed{\|w_{M+1}\|\le R\sqrt M.}
$$

这里用到错误条件的符号；若每轮无条件更新，交叉项不再非正。

## 七、两条账夹出 Mistake Bound

Cauchy–Schwarz 给

$$
M\gamma
\le\langle w_{M+1},u\rangle
\le\|w_{M+1}\|\|u\|
\le R\sqrt M.
$$

若 $M>0$，两边除以 $\sqrt M\gamma$：

$$
\boxed{M\le\left(\frac R\gamma\right)^2.}
$$

这就是 Novikoff 型 Perceptron mistake bound。

## 八、这个“收敛”是什么意思

定理保证：只要同一个带正 margin 的 separator 对完整序列成立，mistake/update 总数有限。因此无限重复一个有限可分训练集时，最终会找到能正确分类该训练集的权重。

它不保证：

- 权重收敛到唯一向量；
- 找到最大 margin separator；
- objective 单调下降；
- 新 iid 样本 risk 小；
- 不可分数据上停止更新；
- 按 wall-clock 或 epoch 给出统一时间界。

## 九、尺度不变量

若把所有输入乘 $c>0$，则 $R$ 和 $\gamma$ 都乘 $c$，比值 $R/\gamma$ 不变。若把 separator 从 unit vector 改写为任意 $v$，复杂度应写为

$$
\frac{R\|v\|}{\min_t y_t\langle v,x_t\rangle}.
$$

只报“margin 是 10”而不报 norm convention 没有可比性。

## 十、含 Bias 的情况

分类器 $\operatorname{sign}(\langle w,x\rangle+b)$ 可通过增广表示

$$
\widetilde x=(x,\rho),\qquad
\widetilde w=(w,b/\rho)
$$

化为齐次内积。此时半径变成

$$
\|\widetilde x\|\le\sqrt{R^2+\rho^2}.
$$

$\rho$ 是建模尺度，会改变 bound；“加一维常数 1”不是完全无代价的记号技巧。

## 十一、不可分数据与 Hinge-Loss 接口

若存在噪声或矛盾标签，就不存在统一 $\gamma>0$，线性进展账失效。更稳健的 comparator-dependent 分析用 margin violations，例如

$$
\xi_t=\max\{0,\gamma-y_t\langle u,x_t\rangle\}.
$$

此时错误数由 $R/\gamma$ 与累计 violation 共同控制，而不再是纯有限常数。它把 Perceptron 连接到 hinge loss 与 soft-margin SVM，但具体常数随 update/version 而变，必须另行声明。

## 十二、手算四步

令 $x_1=(1,0),y_1=+1$；$x_2=(0,1),y_2=+1$；$x_3=(-1,0),y_3=-1$；$x_4=(0,-1),y_4=-1$，并把 tie 算错误。

从 $w_1=(0,0)$：

1. 第 1 轮更新到 $(1,0)$；
2. 第 2 轮 score 为 0，更新到 $(1,1)$；
3. 第 3 轮 $y\langle w,x\rangle=1$，不更新；
4. 第 4 轮同样正确。

总 mistake 为 2。取 $u=(1,1)/\sqrt2$，$R=1$、$\gamma=1/\sqrt2$，theorem 给 $M\le2$，本例达到界。

## 十三、Kernel Perceptron

若在 RKHS 中 $w=\sum_{k\in\mathcal M}y_k\phi(x_k)$，预测只需

$$
\langle w,\phi(x)\rangle
=\sum_{k\in\mathcal M}y_kK(x_k,x).
$$

只要 $K(x,x)\le R^2$ 且 feature-space margin 为 $\gamma$，同一证明成立。计算代价却随 mistake/support 数增长；统计保证不等于推理成本可控。

## 十四、Averaged 与 Pocket 版本

- averaged Perceptron 对训练过程中多个 $w_t$ 平均，常改善有噪声数据的稳定性；
- pocket algorithm 保存训练误差最低的迭代点，适合不可分数据的启发式停止；
- margin Perceptron 在 $y\langle w,x\rangle$ 低于正阈值时也更新。

这些版本改变 update rule，不能直接继承本章常数。

## 十五、图：线性进展如何撞上平方根上界

先看图回答：若 separator margin 只有 $\gamma=0$，哪一条轨道不再迫使错误次数有限？

![[00-知识库管理/_assets/figures/learning-theory/fig-perceptron-margin-mistakes-v2.svg|900]]

> [!figure] 图 20.9-05　Perceptron 几何、双账本与边界
> 左栏展示错误样本触发的向量更新；中栏把 $M\gamma$ 线性进展与 $R\sqrt M$ 范数上界相交；右栏分开可分定理、不可分 violation 与 kernel/AI 接口。来源：依据 Rosenblatt、Novikoff 与在线学习教材独立绘制；由 [[plot_online_learning_part2_v2.py]] 确定性生成。

**怎样读图**：先确认 unit separator 与正 margin，再逐行核对 progress、norm、Cauchy 三步。

**图没有证明什么**：图没有证明最大间隔、population generalization，也没有为有标签噪声的无限序列给出有限 mistake 常数。

## 十六、AI 接口

- 在线内容审核：稀疏线性特征可快速按错误更新；
- embedding 后线性分类：margin 同时受 encoder 尺度和归一化影响；
- kernel/检索特征：mistake 数控制 support expansion 的最坏规模；
- continual adaptation：若标签规则漂移，固定 separator 假设失效，应转向 dynamic comparator。

## 十七、常见错误

1. 忘记 $u$ 必须归一化；
2. 把原始轮数 $T$ 当作错误数 $M$；
3. 在正确轮次也使用非正交叉项；
4. 说“线性可分”却没有正 margin/有界半径；
5. 把有限训练错误外推为测试 risk；
6. 以为最终向量唯一或最大间隔；
7. bias 增广后忘记半径改变；
8. kernel theorem 成立就忽略 support/计算增长。

## 十八、最小记忆与掌握标准

> [!summary]
> - mistake 更新：$w\leftarrow w+yx$；
> - progress：$\langle w,u\rangle\ge M\gamma$；
> - norm：$\|w\|\le R\sqrt M$；
> - Cauchy 夹出 $M\le(R/\gamma)^2$；
> - guarantee 是序列训练错误界，不是 population-risk theorem；
> - 噪声、漂移、bias 与 kernel 都要重审对象合同。

能写算法（A）、手算 updates（B）、完整证明双账本（C）、诊断不可分/尺度问题（D），并为在线 AI 分类建立 margin 与反馈合同（E）。

## 十九、练习与独立详解

- [[习题 - Perceptron Mistake Bound 与 Margin]]
- [[解答 - Perceptron Mistake Bound 与 Margin]]

## 参考来源

- [[S-1958-Rosenblatt-Perceptron]]
- [[S-1962-Novikoff-Perceptron]]
- [[S-2012-Shalev-Online-Learning-OCO]]

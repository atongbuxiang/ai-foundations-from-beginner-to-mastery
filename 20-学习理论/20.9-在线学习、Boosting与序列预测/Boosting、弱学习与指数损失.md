---
type: theorem
status: draft
area: [learning-theory/boosting, weak-learning, exponential-loss]
aliases: [AdaBoost Training Error Bound, Weak-to-Strong Learning, Boosting]
node_id: LT-74
prerequisites: ["[[Experts、Weighted Majority 与 Multiplicative Weights]]", "[[最大熵原理与指数族]]", "[[逻辑回归、复合损失与概率分类]]"]
related: ["[[Bagging、Random Forest 与 Boosting]]", "[[分类间隔、Margin Bound 与 SVM 接口]]", "[[梯度、方向导数与最陡方向]]"]
sources: ["[[S-1990-Schapire-Weak-Learnability]]", "[[S-1997-Freund-Schapire-AdaBoost]]", "[[S-2001-Friedman-Gradient-Boosting]]"]
exercises: ["[[习题 - Boosting、弱学习与指数损失]]"]
solutions: ["[[解答 - Boosting、弱学习与指数损失]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-boosting-weak-strong-exp-loss-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# Boosting、弱学习与指数损失

> [!abstract] 本章主问题
> 一个每轮只比随机猜测略好的 weak learner，怎样被组合成训练误差指数下降的 strong ensemble？AdaBoost 的核心不是“多训练几棵树”，而是样本分布、弱规则权重与指数势能形成的精确三联账本。

## 一、学习目标

完成本章后，应能：

1. 区分 weak learnability 与 weak learner 在一次固定分布上的表现；
2. 写出 AdaBoost 的 $D_t$、$h_t$、$\varepsilon_t$、$\alpha_t$ 与更新；
3. 推导归一化常数 $Z_t$；
4. 证明 training error $\le\prod_tZ_t$；
5. 推导 constant-edge 下的 $e^{-2\gamma^2T}$；
6. 解释指数损失怎样上界 0–1 error；
7. 区分 AdaBoost、gradient boosting 与 bagging；
8. 说明噪声/outlier 为什么会吸走权重；
9. 区分训练误差下降、margin 改善与测试泛化；
10. 把 weak-to-strong reduction 映射到现代模型组合。

## 二、经验分布上的设置

给训练集 $(x_i,y_i)_{i=1}^m$，$y_i\in\{-1,+1\}$。初始化

$$
D_1(i)=\frac1m.
$$

第 $t$ 轮调用 weak learner，在分布 $D_t$ 下返回 $h_t:\mathcal X\to\{-1,+1\}$，其加权错误率为

$$
\varepsilon_t=\Pr_{i\sim D_t}[h_t(x_i)\ne y_i]
=\sum_iD_t(i)\mathbf1\{h_t(x_i)\ne y_i\}.
$$

要求 $\varepsilon_t<1/2$；定义 edge

$$
\gamma_t=\frac12-\varepsilon_t>0.
$$

## 三、AdaBoost 更新

弱规则权重取

$$
\boxed{\alpha_t=\frac12\log\frac{1-\varepsilon_t}{\varepsilon_t}.}
$$

样本权重更新为

$$
\boxed{
D_{t+1}(i)
=\frac{D_t(i)e^{-\alpha_ty_ih_t(x_i)}}{Z_t},
}
$$

其中 $Z_t$ 使权重和为 1。若分类正确，$y_ih_t(x_i)=+1$，权重乘 $e^{-\alpha_t}$；错误则乘 $e^{+\alpha_t}$。

最终 score 与分类器是

$$
F_T(x)=\sum_{t=1}^T\alpha_th_t(x),\qquad
H_T(x)=\operatorname{sign}F_T(x).
$$

## 四、为什么选择这个 $\alpha_t$

固定 $D_t,h_t$，归一化常数为

$$
Z_t(\alpha)
=(1-\varepsilon_t)e^{-\alpha}+\varepsilon_te^{\alpha}.
$$

求导并令零：

$$
-(1-\varepsilon_t)e^{-\alpha}+\varepsilon_te^\alpha=0,
$$

所以

$$
e^{2\alpha}=\frac{1-\varepsilon_t}{\varepsilon_t},
$$

即得到上式 $\alpha_t$。它是沿当前弱规则方向最小化经验指数损失的一维精确 line search。

## 五、归一化常数的闭式

代入最优 $\alpha_t$：

$$
\begin{aligned}
Z_t
&=(1-\varepsilon_t)\sqrt{\frac{\varepsilon_t}{1-\varepsilon_t}}
+\varepsilon_t\sqrt{\frac{1-\varepsilon_t}{\varepsilon_t}}\\
&=2\sqrt{\varepsilon_t(1-\varepsilon_t)}\\
&=\sqrt{1-4\gamma_t^2}.
\end{aligned}
$$

只要 edge 为正，$Z_t<1$，势能就收缩。

## 六、权重递推展开

反复代入 $D_{t+1}$：

$$
D_{T+1}(i)
=\frac{D_1(i)\exp[-y_iF_T(x_i)]}{\prod_{t=1}^T Z_t}.
$$

两边对 $i$ 求和且 $\sum_iD_{T+1}(i)=1$，得到精确恒等式

$$
\boxed{
\frac1m\sum_{i=1}^m e^{-y_iF_T(x_i)}
=\prod_{t=1}^T Z_t.
}
$$

因此 $\prod Z_t$ 不只是证明技巧，而是经验指数损失本身。

## 七、训练错误的指数界

若 $H_T(x_i)\ne y_i$，则 $y_iF_T(x_i)\le0$，从而

$$
\mathbf1\{H_T(x_i)\ne y_i\}
\le e^{-y_iF_T(x_i)}.
$$

平均后：

$$
\widehat R_{01}(H_T)
\le\frac1m\sum_i e^{-y_iF_T(x_i)}
=\prod_tZ_t.
$$

又因为 $\sqrt{1-z}\le e^{-z/2}$，

$$
Z_t=\sqrt{1-4\gamma_t^2}\le e^{-2\gamma_t^2}.
$$

所以

$$
\boxed{
\widehat R_{01}(H_T)
\le\exp\left(-2\sum_{t=1}^T\gamma_t^2\right).
}
$$

若每轮 $\gamma_t\ge\gamma>0$，则

$$
\widehat R_{01}(H_T)\le e^{-2\gamma^2T}.
$$

## 八、Weak-Learning Assumption 的量词

真正的 reduction 需要：对 boosting 过程可能产生的 **每个** 训练分布 $D$，weak learner 都能返回 error $\le1/2-\gamma$ 的 hypothesis。

$$
\forall D\in\Delta_m,\quad
\exists h\in\mathcal H:\quad
\Pr_{i\sim D}[h(x_i)\ne y_i]\le\frac12-\gamma.
$$

“在原始均匀训练集上 accuracy 51%”只验证一个 $D$，远弱于这个全称命题。

## 九、Margin 视角

未归一化 margin 是 $y_iF_T(x_i)$；常用归一化版本为

$$
\rho_i=\frac{y_iF_T(x_i)}{\sum_t\alpha_t}.
$$

指数损失会强烈推动负 margin 样本，但训练误差归零后仍可继续改变 margin distribution。margin-based generalization 需要另加 hypothesis complexity、样本假设与置信项，不能由 $\prod Z_t$ 单独推出。

## 十、噪声与异常值

不可正确分类的样本长期满足 $y_iF_T(x_i)<0$，其 factor $e^{-y_iF_T}$ 快速增大，于是 $D_t$ 越来越集中到它们。结果可能是：

- weak learner 被少量错标点支配；
- $\alpha_t$ 与边界变得不稳定；
- 训练指数损失继续追逐极端 margin；
- 测试表现先升后降。

shrinkage、early stopping、robust loss、weight clipping 是不同修复，都会改变原始 theorem。

## 十一、与 Gradient Boosting 的关系和区别

AdaBoost 可解释为在函数空间沿 $h_t$ 方向优化指数损失，但 gradient boosting 是更一般的 stagewise additive modeling：选择 base learner 拟合当前 loss 的负梯度/伪残差，并可用于平方损失、logistic loss 等。

共同点是加法模型；不同点是目标、line search、sample reweighting 与统计解释。不能把任意 boosted trees 的结果都称为 AdaBoost bound。

## 十二、与 Bagging 的区别

- bagging：在重采样数据上并行训练，主要降低不稳定模型的方差；
- boosting：顺序地改变样本/残差重点，形成加法模型；
- random forest：bagging 加 feature randomness；
- AdaBoost：有明确 weak edge 与指数势能证明。

## 十三、一个数值例子

若 $\varepsilon_t=0.25$，则

$$
\alpha_t=\frac12\log3\approx0.5493,\qquad
Z_t=2\sqrt{0.25\cdot0.75}=\frac{\sqrt3}{2}\approx0.8660.
$$

若十轮都保持此 error，training error 上界为

$$
(0.8660)^{10}\approx0.2373.
$$

用 edge $\gamma=0.25$ 的较松界则是 $e^{-1.25}\approx0.2865$。

## 十四、图：从弱边到指数势能

先看图回答：如果某轮 $\varepsilon_t=1/2$，$\alpha_t$、$Z_t$ 与训练误差收缩分别发生什么？

![[00-知识库管理/_assets/figures/learning-theory/fig-boosting-weak-strong-exp-loss-v2.svg|900]]

> [!figure] 图 20.9-06　AdaBoost 的重加权、势能恒等式与证据边界
> 左栏给出 $D_t\to h_t\to\alpha_t\to D_{t+1}$；中栏从 $Z_t$ 推到训练错误界；右栏区分 weak-to-strong theorem、margin/generalization 与 noise failure。来源：依据 Schapire、Freund–Schapire 与 Friedman 独立绘制；由 [[plot_online_learning_part2_v2.py]] 确定性生成。

**怎样读图**：把 $D_t$ 看成算法状态，把 $Z_t$ 看成势能收缩率，再检查 weak edge 的全称量词。

**图没有证明什么**：图没有证明测试误差指数下降，也没有证明在标签噪声、任意 base learner 或任意 gradient boosting 实现下成立。

## 十五、AI 接口

- 多模型集成：弱专家需在当前加权 query distribution 上保持 edge；
- cascade/reranker：错例挖掘像重加权，但 deployment selection 会改变数据分布；
- reward model ensemble：指数强调 hard pairs 也会强调错标偏好；
- tree boosting：需分开 AdaBoost、logistic boosting 与现代 GBDT objective。

## 十六、常见错误

1. 只验证均匀分布上的 51% accuracy；
2. 忘记 $\varepsilon_t<1/2$；
3. 把 $Z_t$ 当任意 normalization 而忽略其势能意义；
4. 从 training error bound 直接推出 test error；
5. 把指数损失与 logistic loss 混为一谈；
6. 忽略错标点的权重爆炸；
7. 把 bagging/random forest 称为 boosting；
8. 把 stagewise 加法模型自动等同于原始 AdaBoost theorem。

## 十七、最小记忆与掌握标准

> [!summary]
> - weak error：$\varepsilon_t=1/2-\gamma_t$；
> - rule weight：$\alpha_t=\frac12\log((1-\varepsilon_t)/\varepsilon_t)$；
> - normalization：$Z_t=2\sqrt{\varepsilon_t(1-\varepsilon_t)}$；
> - exponential loss：$m^{-1}\sum_i e^{-y_iF_T(x_i)}=\prod_tZ_t$；
> - training error $\le e^{-2\sum_t\gamma_t^2}$；
> - generalization、noise robustness 与其他 boosting objective 需要额外理论。

能写更新（A）、手算 $\alpha/Z$（B）、完整证明 product bound（C）、审计 weak-learning/noise 条件（D），并为现代模型组合写清训练分布与部署边界（E）。

## 十八、练习与独立详解

- [[习题 - Boosting、弱学习与指数损失]]
- [[解答 - Boosting、弱学习与指数损失]]

## 参考来源

- [[S-1990-Schapire-Weak-Learnability]]
- [[S-1997-Freund-Schapire-AdaBoost]]
- [[S-2001-Friedman-Gradient-Boosting]]

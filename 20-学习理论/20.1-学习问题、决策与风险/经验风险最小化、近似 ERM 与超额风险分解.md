---
type: concept
status: draft
area: [learning-theory/foundations, machine-learning, optimization]
aliases: [Empirical Risk Minimization, Approximate ERM, Excess Risk Decomposition, 经验风险最小化]
node_id: LT-05
prerequisites: ["[[损失、总体风险与经验风险]]", "[[预测器、假设空间与学习算法]]", "[[优化问题、可行域与局部最优]]", "[[基本不等式与界的构造]]"]
related: ["[[Bayes 决策、Bayes 预测器与 Bayes 风险]]", "[[可实现、不可知、相合性与可学习性]]", "[[泛化间隙与浓缩不等式接口]]", "[[正则化、交叉验证与模型选择]]"]
sources: ["[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]", "[[S-2020-Su-7466-泛化性乱弹]]", "[[S-2020-Su-7681-L2正则与尺度不变性]]"]
exercises: ["[[习题 - 经验风险最小化、近似 ERM 与超额风险分解]]"]
solutions: ["[[解答 - 经验风险最小化、近似 ERM 与超额风险分解]]"]
created: 2026-08-20
updated: 2026-08-23
---

# 经验风险最小化、近似 ERM 与超额风险分解

> [!abstract] 本章主问题
> ERM 只保证在给定样本和函数类中把经验风险做到最小；要推出目标风险接近最优，必须把 Bayes/类内近似误差、有限样本估计误差、经验—总体泛化间隙和优化容差分别记账。核心桥梁是：approximate ERM 的类内超额风险不超过两个 data-dependent 泛化间隙加经验优化误差，而不是“训练损失下降，所以泛化自然改善”。

> [!question] 初学者读完必须能回答
> 1. Bayes optimum、class oracle、empirical ERM 与 computed output 分别是什么？
> 2. Exact、$\rho$-approximate 与 regularized ERM 的目标和可行域有何差别？
> 3. Approximation、selection/estimation、optimization 与 target mismatch 如何组成风险账本？
> 4. 怎样推出类内 excess risk 的 $2\sup_h|R_P(h)-R_S(h)|+\rho$ 上界？
> 5. 为什么 uniform convergence 是 ERM 泛化的充分路线，却不是所有 learner 泛化的必要条件？
> 6. 零训练误差究竟关闭了哪一笔账，又留下哪些账？

先用下图回答一个视觉问题：**从 Bayes oracle 到实际迭代输出共有几层最优对象，训练损失与目标风险之间必须补齐哪几笔误差账？**

![[00-知识库管理/_assets/figures/learning-theory/fig-erm-excess-risk-ledger-v2.svg|880]]

> [!figure] 图 20.1.5｜ERM、类内最优与超额风险分解
> A 依次区分 Bayes $h^*$、class oracle $h_{\mathcal H}^*$、empirical ERM $\widehat h$ 与 computed $\widetilde h$；B 将 target mismatch、approximation、selection 与 empirical optimization 分账；C 从 $R_S(\widetilde h)\le\inf_{h\in\mathcal H}R_S(h)+\rho$ 得到两个 generalization gaps 加 $\rho$ 的类内桥梁。来源：独立绘制；理论接口参考 ERM excess-risk decomposition 与 uniform convergence；生成脚本：[[plot_learning_problem_decision_v2.py]]；确定性证明地图，无随机种子。

**怎样读图。** A 先检查每个 infimum/argmin 的集合与风险是 $R_P$ 还是 $R_S$，不要默认 minimizer 存在；B 再把一次方法改进定位到具体 ledger，一项 regularizer 可能同时移动 approximation、selection 和 optimization；C 最后逐项插入并减去 $R_S$，两个 gap 分别属于输出与 class comparator，$\rho$ 只控制经验优化容差。

**适用边界（图没有证明什么）。** 图没有证明 uniform deviation 很小，也不声称 excess-risk decomposition 的每项都非负；population optimization difference 可以有任意符号，target mismatch 还依赖重新定义的部署风险。对于 non-ERM、data-dependent classes、implicit regularization、nonattained infimum 或 unbounded losses，桥梁需修改；优化收敛率也不等同于统计收敛率。

## 一、学习目标

1. 定义 exact ERM、$\rho$-approximate ERM 与 regularized ERM；
2. 区分 Bayes optimum、class optimum、empirical optimum 与 computed output；
3. 推导 approximation—estimation/selection—optimization 风险分账；
4. 从 approximate ERM 推导 $2\sup_h|R_P(h)-R_S(h)|+\rho$ 上界；
5. 解释为什么 empirical optimization error 非负，而对应 population difference 可为负；
6. 区分 excess risk、generalization gap 与 train–test gap；
7. 分析 misspecification、regularization 和 expanding classes；
8. 识别深度学习中“零训练误差”仍未回答的问题；
9. 为一个 AI pipeline 建立可计算的 error budget；
10. 判断某个改进究竟作用于 approximation、estimation、optimization 还是 target mismatch。

## 二、四个预测器/最优值先分开

令全体允许的可测预测器集合记为 $\mathcal F$，研究者选择的假设空间为 $\mathcal H\subseteq\mathcal F$。

### 2.1 Bayes/全空间最优

$$
R^*
=\inf_{h\in\mathcal F}R_P(h).
$$

若下确界能取到，记某个 Bayes predictor 为 $h^*$。它描述在 observation、action 与 loss 已固定时理论上最小的总体风险。

### 2.2 类内总体最优

$$
R_{\mathcal H}^*
=\inf_{h\in\mathcal H}R_P(h).
$$

若能取到，记

$$
h_{\mathcal H}^*
\in\arg\min_{h\in\mathcal H}R_P(h).
$$

学习器通常不知道 $P$，所以无法直接计算它；它是 oracle comparator。

### 2.3 经验风险最小化解

给定样本 $S$：

$$
\widehat h_S
\in\arg\min_{h\in\mathcal H}R_S(h).
$$

这就是 ERM。若 argmin 不存在，可使用下确界或 approximate ERM。

### 2.4 实际计算输出

真实 optimizer 在有限预算下返回

$$
\widetilde h_{S,U},
$$

其中 $U$ 包含初始化、batch 顺序和随机内核。它未必是 exact ERM。

| 对象 | 依赖 $P$ | 依赖 $S$ | 可否直接计算 |
|---|---:|---:|---|
| $h^*$ | 是 | 否 | 通常不能 |
| $h_{\mathcal H}^*$ | 是 | 否 | 通常不能 |
| $\widehat h_S$ | 否 | 是 | 概念上可定义，计算可能困难 |
| $\widetilde h_{S,U}$ | 否 | 是 | 实际训练输出 |

## 三、exact 与 approximate ERM

### 3.1 exact ERM

$$
R_S(\widehat h_S)=\inf_{h\in\mathcal H}R_S(h).
$$

这是一条关于**同一份样本上的训练目标**的陈述，不含总体风险。

### 3.2 $\rho$-approximate ERM

若

$$
R_S(\widetilde h_{S,U})
\le
\inf_{h\in\mathcal H}R_S(h)+\rho,
$$

则称输出是经验目标上的 $\rho$-approximate ERM。$\rho$ 可是确定容差，也可随 $S,U$ 随机。

若 exact minimizer 存在，等价写成

$$
R_S(\widetilde h_{S,U})-R_S(\widehat h_S)\le\rho.
$$

> [!warning] 参数距离不是优化误差
> $\|\widetilde\theta-\widehat\theta\|$ 小不自动意味着 objective gap 小，反之亦然；强凸性、smoothness 或 error bound 才能把二者连接。神经网络还有 parameter fiber，使参数距离尤其容易失真。

## 四、第一层分解：类不够好，还是没有学好

任意输出 $\widetilde h\in\mathcal H$ 满足精确恒等式

$$
\boxed{
R_P(\widetilde h)-R^*
=
\underbrace{R_{\mathcal H}^*-R^*}_{\text{approximation / specification}}
+
\underbrace{R_P(\widetilde h)-R_{\mathcal H}^*}_{\text{learning within }\mathcal H}
}
$$

两项都非负。

### 4.1 approximation error

$$
\mathcal E_{\rm app}(\mathcal H)
=R_{\mathcal H}^*-R^*.
$$

它来自函数类限制：线性类无法表示弯曲边界、固定 tokenizer 丢失信息、有限上下文看不到远程依赖等。

### 4.2 class excess risk

$$
\mathcal E_{\mathcal H}(\widetilde h)
=R_P(\widetilde h)-R_{\mathcal H}^*.
$$

它来自有限样本、算法选择、优化和随机性。学习理论首先控制这一项。

> [!important] 大模型的基本 trade-off
> 扩大 $\mathcal H$ 常能降低 approximation error，却可能提高从有限样本中选择函数的难度。经典 structural risk minimization 正是对两者进行平衡；深度网络中还要加入 implicit bias、data augmentation 和 optimization path。

## 五、核心推导：approximate ERM 如何跨越经验—总体鸿沟

定义 signed generalization gap

$$
g_S(h)=R_P(h)-R_S(h).
$$

设 $h_{\mathcal H}^*$ 取到类内总体最优，$\widehat h_S$ 是 exact ERM，$\widetilde h$ 是 $\rho$-approximate ERM。插入并减去经验风险：

$$
\begin{aligned}
R_P(\widetilde h)-R_P(h_{\mathcal H}^*)
&=\underbrace{R_P(\widetilde h)-R_S(\widetilde h)}_{g_S(\widetilde h)}\\
&\quad+\underbrace{R_S(\widetilde h)-R_S(\widehat h_S)}_{\le\rho}\\
&\quad+\underbrace{R_S(\widehat h_S)-R_S(h_{\mathcal H}^*)}_{\le0\text{ by ERM}}\\
&\quad+\underbrace{R_S(h_{\mathcal H}^*)-R_P(h_{\mathcal H}^*)}_{-g_S(h_{\mathcal H}^*)}.
\end{aligned}
$$

因此

$$
\boxed{
R_P(\widetilde h)-R_{\mathcal H}^*
\le
g_S(\widetilde h)-g_S(h_{\mathcal H}^*)+\rho.
}
$$

再由

$$
g_S(\widetilde h)
\le\sup_{h\in\mathcal H}|g_S(h)|,
\qquad
-g_S(h_{\mathcal H}^*)
\le\sup_{h\in\mathcal H}|g_S(h)|,
$$

得到经典 ERM bridge：

$$
\boxed{
R_P(\widetilde h)-R_{\mathcal H}^*
\le
2\sup_{h\in\mathcal H}
|R_P(h)-R_S(h)|+\rho.
}
$$

最后与 approximation error 合并：

$$
\boxed{
R_P(\widetilde h)-R^*
\le
\bigl(R_{\mathcal H}^*-R^*\bigr)
+2\sup_{h\in\mathcal H}|R_P(h)-R_S(h)|
+\rho.
}
$$

这条式子是 PAC/VC/Rademacher 课程的主入口。

## 六、为什么需要 uniform，而不是只控制一个 $h$

对预先固定的 $h_{\mathcal H}^*$，concentration 可控制 $g_S(h_{\mathcal H}^*)$。困难在 $\widetilde h=A(S,U)$：它看过同一数据，可能专门选择 empirical fluctuation 最有利的函数。

因此经典路线控制

$$
\sup_{h\in\mathcal H}|R_P(h)-R_S(h)|,
$$

使一份样本同时对所有候选函数代表总体。这在有限类中由 union bound 实现，在无限类中由 VC/Rademacher/covering 等容量量实现。

但 uniform convergence 不是唯一路线：stability 直接控制算法对样本替换的敏感度，PAC-Bayes 控制随机 posterior，information bound 控制 output 与 sample 依赖。它们都会在后续分卷出现。

## 七、optimization error 为何不能随意放到总体风险里

经验 optimization gap

$$
\rho_S(\widetilde h)
=R_S(\widetilde h)-\inf_{h\in\mathcal H}R_S(h)
\ge0.
$$

但

$$
R_P(\widetilde h)-R_P(\widehat h_S)
$$

不一定非负：没有完全插值的 early-stopped 模型，可能比 exact empirical minimizer 更好泛化。因此正确语言是：

- $\rho_S$ 描述对**经验目标**的近似；
- generalization analysis 把它与 population excess risk 连接；
- implicit/explicit regularization 可能故意接受较大训练 gap 换取较小 population risk。

## 八、手算：三种误差怎样同时出现

设输入只有三个点 $\{-1,0,1\}$，目标分布均匀，确定标签为

$$
y(-1)=1,\quad y(0)=0,\quad y(1)=1.
$$

用 0–1 loss。全体函数中可取 $h^*=y$，故 $R^*=0$。

限制到阈值类

$$
\mathcal H=\{h_t(x)=\mathbf1\{x\ge t\}\}.
$$

阈值无法表示 `1,0,1`，最优至少错一个点，所以

$$
R_{\mathcal H}^*=\frac13.
$$

approximation error 是 $1/3$。

若训练样本只观察到 $(0,0)$，那么任何 $t>0$ 都零训练风险。某 tie-breaker 选 $t=2$，在三个点上预测 `0,0,0`，总体风险 $2/3$。于是

$$
R_P(h_2)-R_{\mathcal H}^*
=\frac23-\frac13=\frac13.
$$

这部分是 finite-sample selection error。若 optimizer 又返回常预测 1（经验风险 1），其 empirical optimization gap 为 1；但总体风险 $1/3$，反而等于 class optimum。这说明 empirical optimization gap 与 population difference 不可逐项同号对应。

## 九、regularized ERM 改变了什么

$$
\widetilde h
\in\arg\min_{h\in\mathcal H}
\left{R_S(h)+\lambda\Omega(h)\right\}.
$$

可能有三种分析方式：

1. 把 $\lambda\Omega$ 看成 learner 的 tie-break/selection rule；
2. 若与约束等价，把有效类改写为 $\mathcal H_B=\{h:\Omega(h)\le B\}$；
3. 把目标定义成 regularized population objective，但此时它不再等于原 task risk。

若 $\Omega$ 写在参数上，还需检查同一函数的不同参数代表是否得到不同值，见[[S-2020-Su-7681-L2正则与尺度不变性]]。

噪声、VAT 和 gradient penalty 同样改变算法或经验目标。[[S-2020-Su-7466-泛化性乱弹]]提供局部机制直觉，但 target-risk 改善仍要进入上述误差账本。

## 十、misspecification 与 expanding classes

固定小类可能有不可消除的 $R_{\mathcal H}^*-R^*$。一种渐近策略是使用

$$
\mathcal H_1\subseteq\mathcal H_2\subseteq\cdots,
$$

并让样本量 $m$ 增加时选择 $k=k(m)$：

$$
\underbrace{R_{\mathcal H_{k(m)}}^*-R^*}_{\downarrow}
+
\underbrace{\text{estimation complexity}(\mathcal H_{k(m)},m)}_{\text{若增长太快可能}\uparrow}.
$$

Bayes consistency 要两者共同趋于 0。只扩大模型而不增加有效样本或控制算法，不能由 approximation improvement 自动推出总风险下降。

## 十一、深度学习中的 error budget

| 误差源 | 典型可观测 proxy | 修复方向 | 不能直接推出 |
|---|---|---|---|
| target mismatch | 人工审计、部署反馈、shift test | 重写 action/loss/population | 训练更久能修复 |
| approximation | scaling/architecture ablation | 表示、上下文、结构先验 | 参数更多必然更好 |
| finite-sample selection | split/seed variance、complexity proxy | 更多独立数据、regularization、稳定算法 | 低训练风险 |
| optimization | objective gap、gradient/residual、multi-start | optimizer、schedule、precision | population risk 同比例下降 |
| evaluation | CI、locked test、group/time split | 新 holdout、nested protocol | leaderboard 最优即部署最优 |

大型模型可能实现零训练 loss，此时经验 optimization error 很小；仍可能有 label noise、distribution shift、surrogate mismatch、memorization 与 benchmark reuse。

## 十二、常见错误

> [!danger] 五个不能混写的量
> $$
> R_S(\widetilde h),\quad
> R_P(\widetilde h),\quad
> R_{\mathcal H}^*,\quad
> R^*,\quad
> \rho_S.
> $$
> 它们分别是训练表现、目标表现、类内 oracle、任务 oracle 与经验优化容差。

- “ERM 一定泛化”缺少 class complexity/stability 条件；
- “训练 loss 更低，excess risk 更低”缺少 generalization bridge；
- “approximation error 是模型训练不好”错误，它即使有无限数据也存在；
- “optimization error 是 population risk 的非负组成”一般错误；
- “模型足够大就没有 approximation error”还依输入信息、action 与 architecture 表示；
- “test error 减去 train error就是 estimation error”只是一种 realized gap，不等于完整超额风险。

## 十三、研究声明模板

> 对目标分布 $P$ 与任务损失 $\ell$，我们比较 $R_P(h)$。候选类为 $\mathcal H$，训练算法返回经验目标上的 $\rho$-approximate solution。理论/实验分别控制 class approximation、sample-dependent generalization、optimization gap 与 final test uncertainty；若 deployment 为 $Q\ne P$，另行报告 shift assumption，不把它并入普通 estimation error。

## 十四、复习清单

- [ ] 我能区分 $h^*,h_{\mathcal H}^*,\widehat h_S,\widetilde h_{S,U}$；
- [ ] 我能推导 approximate ERM 的四项插入恒等式；
- [ ] 我能得到 $2\sup_h|R_P-R_S|+\rho$；
- [ ] 我知道 empirical optimization gap 与 population difference 不同号；
- [ ] 我能为一个模型改进标注它影响哪种误差；
- [ ] 我不会把 regularizer 或 auxiliary loss 直接称为 target risk。

## 来源

- [[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]：ERM、agnostic learning 与 uniform convergence 主线；
- [[S-2020-Su-7466-泛化性乱弹]]：局部平滑训练机制的 AI 接口；
- [[S-2020-Su-7681-L2正则与尺度不变性]]：参数正则与函数复杂度边界；
- 图示脚本：`00-知识库管理/_labs/code/plot_risk_decision_evaluation_contract.py`。

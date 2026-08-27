---
type: theorem
status: draft
area: [learning-theory/ood, robustness, causal-invariance]
aliases: [Out-of-Distribution Detection, Natural Shift Robustness, Causal Invariance]
node_id: LT-68
prerequisites: ["[[Covariate、Label 与 Concept Shift]]", "[[Domain Adaptation 与 Domain Generalization Bound]]", "[[Conformal Prediction 与有限样本 Coverage]]"]
related: ["[[概率校准、Proper Scoring Rule 与可靠性图]]", "[[Bayesian Posterior Predictive、Ensemble 与近似边界]]"]
sources: ["[[S-2017-Hendrycks-Gimpel-OOD]]", "[[S-2020-Taori-Natural-Robustness]]", "[[S-2021-Koh-WILDS]]", "[[S-2016-Peters-Invariant-Prediction]]", "[[S-2021-Rosenfeld-Risks-IRM]]", "[[S-2019-Zhao-Invariant-DA]]"]
exercises: ["[[习题 - OOD、鲁棒性与因果不变性的边界]]"]
solutions: ["[[解答 - OOD、鲁棒性与因果不变性的边界]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-ood-robustness-causal-boundaries-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# OOD、鲁棒性与因果不变性的边界

> [!abstract] 本章主问题
> OOD detection、corruption/adversarial/natural-shift robustness、selective prediction 与 causal invariance 是不同任务。一个 score 只有相对于指定 in/out laws、错误事件和行动成本才可评价；跨环境稳定只有在结构因果与干预假设下才可能升级为因果证据。

## 一、学习目标

完成本章后，应能：

1. 区分五类 robustness/OOD 任务；
2. 把 OOD detection 写成指定分布间的检验/排序；
3. 解释为何不存在不依赖 $P_{\rm out}$ 的万能 score；
4. 区分 AUROC、AUPR、FPR@TPR、calibration 与 utility；
5. 分账 source accuracy 与 effective robustness；
6. 解释 worst-group、natural shift 与 synthetic corruption；
7. 写结构因果机制不变性的条件；
8. 区分 invariant prediction 与 representation invariance；
9. 说明有限 environments 下 IRM 的识别边界；
10. 为高风险部署建立 claim ladder。

## 二、五个不同问题

| 问题 | 目标 |
|---|---|
| misclassification detection | 预测会错吗？ |
| OOD detection | 输入来自指定 $P_{\rm out}$ 而非 $P_{\rm in}$ 吗？ |
| selective prediction | 给定 coverage/成本何时拒答？ |
| corruption/adversarial robustness | 指定 perturbation family 下风险如何？ |
| natural-shift robustness | 真实时间/地点/群体变化下风险如何？ |
| causal invariance | 哪个机制在允许干预下保持？ |

这些任务可相关，但定义不互相蕴含。

## 三、OOD 是相对概念

给 score $s(x)$，检测问题需要

$$
X\sim P_{\rm in}
\quad\text{或}\quad
X\sim P_{\rm out}.
$$

AUROC 可写为

$$
\Pr(s(X_{\rm out})>s(X_{\rm in}))
$$

（按 score 方向调整）。改变 $P_{\rm out}$，同一 score 排名可完全反转。

## 四、为什么没有万能 OOD Score

若不限制 $P_{\rm out}$，可取

$$
P_{\rm out}=P_{\rm in},
$$

任何 detector 都只能 chance。或令 $P_{\rm out}$ 集中在 score 最像 ID 的区域。故 “detect any unseen distribution” 在无结构条件下不可识别。

OOD benchmark 必须声明 semantic near/far、support relation、生成过程与 deployment prevalence。

## 五、Softmax Baseline 的证据边界

maximum softmax probability：

$$
s_{\rm MSP}(x)=\max_kp_\theta(y=k\mid x)
$$

是简单 confidence baseline。它不是 $p(x)$；网络可在远离训练 support 处输出极端 logits。误分类 detection 好也不推出对新 OOD family 好。

## 六、Metric 与 Threshold

- AUROC：pairwise ranking，忽略实际 prevalence；
- AUPR：依赖正类定义与 prevalence；
- FPR@95TPR：一个 operational point；
- detection error：依赖先验/成本；
- calibration：score 与错误概率关系；
- utility：拒答、延迟、人工审核的实际价值。

排行榜 AUROC 提升不自动产生可部署 threshold。

## 七、Robustness 的分母

更强 ID model 往往也有更高 OOD accuracy。应同时报：

$$
\text{raw target performance}
$$

和相对于 source-performance trend 的额外 robustness。否则只是把 ID scaling gain 重命名为 robustness algorithm gain。

## 八、Synthetic 与 Natural Shift

pixel corruption、norm-bounded adversary、style transfer、时间/地点/医院变化定义不同 uncertainty sets。对一个集合鲁棒不推出另一个集合鲁棒。

WILDS 类 benchmark 利用真实 metadata 与 domain splits；仍只覆盖有限任务、历史 policy 与测量过程。

## 九、Average、Worst Group 与 Tail

总体风险：

$$
R=\sum_gP(G=g)R_g
$$

可隐藏小群组高风险。报告：

$$
\max_gR_g,\qquad
\text{lower performance quantile},\qquad
\text{group calibration/coverage}.
$$

群组由 target/test metadata 定义时要防 selection overfitting；未知群组仍不能由已知 worst-group 指标覆盖。

## 十、Causal Mechanism Invariance

结构因果模型中

$$
Y=f_Y(\operatorname{Pa}(Y),N_Y).
$$

若 environments 只干预 $Y$ 的非机制部分，且 $f_Y,N_Y$ 不变，则

$$
P_e(Y\mid\operatorname{Pa}(Y))
$$

可跨环境稳定。结论依赖 intervention targets、无隐藏问题、模型形式与环境多样性，不是从 prediction invariance 自动得到。

## 十一、Invariant Prediction 与 Feature Alignment

invariant causal prediction 寻找使

$$
P_e(Y\mid X_S)
$$

跨环境相同的 sets，并在结构假设下控制错误识别。domain alignment 只让

$$
P_e(\Phi(X))
$$

相近；它既没有条件在 $Y$ 上，也没有声明干预语义。两种 “invariant” 不同。

## 十二、IRM 的理想目标与边界

理想表述寻找 $\Phi,w$，使同一 $w$ 在各训练环境都最优：

$$
w\in\arg\min_{\bar w}R_e(\bar w\circ\Phi),
\quad\forall e.
$$

有限环境可能留下在所有训练域恰好稳定的 spurious feature；高维下环境数不足，识别尤其困难。实际 gradient penalty 只是理想 constraint 的 surrogate。

## 十三、Robustness 不等于 Causality

高 natural-shift accuracy 可能来自更大数据、augmentation、shortcut 在 benchmark 中仍稳定；因果 predictor 也可能因 measurement shift、support 或 intervention on outcome mechanism 而失败。

因果 claim 至少需要：

1. SCM/变量语义；
2. environments/interventions 的生成说明；
3. 哪些机制假定不变；
4. identifiability theorem 条件；
5. negative controls/intervention tests。

## 十四、图：从 Score 到 Causal Claim 的证据阶梯

先看图回答：一个模型在 6 个 OOD benchmarks 上 AUROC 更高，为什么仍不能称其学到了因果特征？

![[00-知识库管理/_assets/figures/learning-theory/fig-ood-robustness-causal-boundaries-v2.svg|900]]

> [!figure] 图 20.8-08　OOD detection、robustness 与 causal invariance 的边界
> 左栏分开 detection/selection/robustness；中栏展示 score、metric、prevalence、group 与 shift family；右栏给出 mechanism invariance、ICP/IRM 条件与 claim ladder。来源：依据 Hendrycks–Gimpel、Taori et al.、WILDS、Peters et al. 与 Rosenfeld et al. 独立绘制；由 [[plot_distribution_shift_v2.py]] 确定性生成。

**怎样读图**：先锁定 out-law 与行动，再选择 metric；只有额外给出结构因果和干预条件，才能沿右栏升级结论。

**图没有证明什么**：图没有证明存在 universal OOD detector，也没有证明 benchmark robustness、domain invariance 或 IRM penalty 自动识别因果变量。

## 十五、Claim Ladder

1. 在指定 benchmark pair 上 score ranking 改善；
2. 在预注册 threshold/prevalence 下 utility 改善；
3. 在多个 natural shifts/worst groups 下风险改善；
4. 在明确 environment family 下具有 bound；
5. 在 SCM 与干预假设下识别稳定机制。

证据只能支持到达的层级，不能从 1 跳到 5。

## 十六、常见错误

1. 不定义 $P_{\rm out}$；
2. AUROC 当 deployment utility；
3. MSP 当 density；
4. synthetic corruption 外推 natural shift；
5. 平均准确率隐藏 worst group；
6. source scaling gain 称算法鲁棒性；
7. domain invariance 称 causal；
8. 有限环境稳定外推任意干预。

## 十七、最小记忆与掌握标准

> [!summary]
> - OOD detection 相对于指定 in/out laws；
> - metric、prevalence、threshold 与行动成本共同定义价值；
> - robustness family 之间没有自动迁移；
> - average、worst group 与 tail 是不同目标；
> - causal invariance 需要 SCM 和干预语义；
> - benchmark improvement 不能跳级成 causal claim。

能定义任务（A）、推导 AUROC/群组分账（B）、构造 universal detector/finite-environment 反例（C）、设计 natural-shift+utility audit（D），并为高风险系统限制 causal claim（E）。

## 十八、练习与独立详解

- [[习题 - OOD、鲁棒性与因果不变性的边界]]
- [[解答 - OOD、鲁棒性与因果不变性的边界]]

## 参考来源

- [[S-2017-Hendrycks-Gimpel-OOD]]
- [[S-2020-Taori-Natural-Robustness]]
- [[S-2021-Koh-WILDS]]
- [[S-2016-Peters-Invariant-Prediction]]
- [[S-2021-Rosenfeld-Risks-IRM]]
- [[S-2019-Zhao-Invariant-DA]]

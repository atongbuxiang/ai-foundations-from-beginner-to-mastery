---
type: theorem
status: draft
area: [learning-theory/dataset-shift, covariate-shift, label-shift, concept-shift]
aliases: [Dataset Shift Taxonomy, Prior Probability Shift, Concept Drift]
node_id: LT-65
prerequisites: ["[[联合分布、边缘分布与独立性]]", "[[条件概率、全概率与 Bayes 公式]]", "[[统计学习问题的对象合同]]", "[[概率校准、Proper Scoring Rule 与可靠性图]]"]
related: ["[[重要性加权与 Covariate Shift 校正]]", "[[Domain Adaptation 与 Domain Generalization Bound]]", "[[OOD、鲁棒性与因果不变性的边界]]"]
sources: ["[[S-2009-Quinonero-Dataset-Shift]]", "[[S-2018-Lipton-Label-Shift]]", "[[S-2019-Ovadia-Uncertainty-Shift]]"]
exercises: ["[[习题 - Covariate、Label 与 Concept Shift]]"]
solutions: ["[[解答 - Covariate、Label 与 Concept Shift]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-dataset-shift-factorizations-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# Covariate、Label 与 Concept Shift

> [!abstract] 本章主问题
> “数据分布变了”必须落到 joint law 的哪一部分改变。covariate shift、label shift 与 concept shift 由不同条件稳定性定义，因而可识别信息和校正方法不同；只看 target inputs 或预测频率，通常不能完成 taxonomy diagnosis。

## 一、学习目标

完成本章后，应能：

1. 用两种 joint factorization 定义三类 shift；
2. 解释 label shift 为什么通常会改变 $P(Y\mid X)$；
3. 区分 support shift、sample selection、temporal drift 与反馈；
4. 判断哪些假设能由 unlabeled target data 检查；
5. 推导 label-shift confusion-matrix equation；
6. 说明 overlap 与可逆性为何是识别条件；
7. 构造多类 shift 同时发生的例子；
8. 设计 metadata、label-delay 与 target audit；
9. 区分 detection、diagnosis、correction 与 evaluation；
10. 为部署系统写 shift claim card。

## 二、Source 与 Target Joint Laws

记训练/源分布与部署/目标分布为

$$
P_s(X,Y),\qquad P_t(X,Y).
$$

同一 joint law 有两种分解：

$$
\boxed{
p_d(x,y)=p_d(y\mid x)p_d(x)
=p_d(x\mid y)p_d(y),
\quad d\in\{s,t\}.
}
$$

shift taxonomy 是对哪些因子保持、哪些因子改变的假设，不是从一个 accuracy drop 自动读出的标签。

## 三、Covariate Shift

定义：

$$
\boxed{
p_s(x)\ne p_t(x),
\qquad
p_s(y\mid x)=p_t(y\mid x).
}
$$

输入频率改变，但给定完整 $X$ 后的任务机制稳定。若 target support 被 source 覆盖，

$$
p_t(x)>0\Rightarrow p_s(x)>0,
$$

可用 $w(x)=p_t(x)/p_s(x)$ 重写 target risk。

例：同一诊断规律下，部署医院的年龄/设备构成改变；但若医院本身影响未被 $X$ 记录，条件稳定性可能是假象。

## 四、Label Shift

定义：

$$
\boxed{
p_s(y)\ne p_t(y),
\qquad
p_s(x\mid y)=p_t(x\mid y).
}
$$

类别先验改变，类内观测机制保持。由 Bayes 公式：

$$
p_t(y\mid x)
=
\frac{p_s(x\mid y)p_t(y)}
{\sum_k p_s(x\mid k)p_t(k)}.
$$

所以 label shift 一般会改变 $P(Y\mid X)$；它不是 covariate shift 的子类。若只记“concept 不变”等口语，很容易把两个 factorization 混掉。

## 五、Concept/Conditional Shift

最直接定义：

$$
\boxed{
p_s(y\mid x)\ne p_t(y\mid x).
}
$$

可能来自标签规则、因果机制、政策、用户行为或反馈变化。此时只按 $p_t(x)/p_s(x)$ 重加权不能恢复 target conditional law。

例：欺诈者适应检测规则；医学诊断标准改变；推荐系统改变曝光后用户反应机制改变。

## 六、三类并不互斥

真实部署可同时改变

$$
p(x),\quad p(y),\quad p(y\mid x).
$$

例如新地区带来不同人口结构（covariate），疾病流行率改变（label/prior），检测政策又改变确诊机制（concept）。taxonomy 的价值是分账，不是强迫每次事件只能选一个标签。

## 七、Support Shift 是硬边界

若存在集合 $A$：

$$
P_t(X\in A)>0,\qquad P_s(X\in A)=0,
$$

则 source data 从未提供 $A$ 上的标签信息。density ratio 在那里为无穷或未定义；任何 target-risk correction 都需要额外结构、外推模型或新 target labels。

“source/target 样本量都很大”不能弥补支持集空洞。

## 八、Selection Mechanism

令 $S=1$ 表示样本进入训练集。训练分布为

$$
p(x,y\mid S=1).
$$

若

$$
S\perp Y\mid X,
$$

selection 可表现为 covariate shift；若选择还依赖未观测标签/结果，则条件机制也可能改变。应记录纳入、缺失、审核和反馈机制，而不是只比较 feature histograms。

## 九、Unlabeled Target 能识别什么

有 source labels 与 target inputs 时，可以直接检验/估计 $P_s(X)$ 与 $P_t(X)$ 的差异；但：

- $P_s(Y\mid X)=P_t(Y\mid X)$ 需要 target labels 或结构假设；
- label shift 与 concept shift 可产生相似 prediction-frequency change；
- “two-sample test 未拒绝”不证明无 shift；
- 高维 test power、representation 与 sample unit 会改变检测。

因此 input shift detection 不等于 shift diagnosis。

## 十、Label Shift 的线性识别

令黑盒预测 $\widehat Y=g(X)$。在 label shift 下，

$$
\Pr_t(\widehat Y=i)
=\sum_j
\Pr_s(\widehat Y=i\mid Y=j)\Pr_t(Y=j).
$$

写成

$$
\boxed{
\mu_t=C_s\pi_t,
}
$$

其中 $C_s$ 是 source confusion matrix，$\mu_t$ 是 target prediction frequencies，$\pi_t$ 是 target class priors。

若 $C_s$ 可逆且估计稳定，

$$
\widehat\pi_t=C_s^{-1}\widehat\mu_t.
$$

病态、缺类、预测器无区分度或 concept shift 都会破坏估计。

## 十一、Detection、Diagnosis、Correction、Evaluation

| 阶段 | 问题 | 所需证据 |
|---|---|---|
| detect | 某个可观测量变了吗？ | two-sample/monitoring |
| diagnose | 哪个 joint factor 改变？ | labels + assumptions |
| correct | 哪个 change-of-measure/适应有效？ | overlap/identifiability |
| evaluate | target risk 是否改善？ | locked target-like labels |

一个 domain classifier 能检测输入差异，不自动选择 label-shift 或 covariate-shift correction。

## 十二、Temporal 与 Feedback Shift

时间序列中 $P_t$ 本身随时间变：

$$
P_{t+\Delta}\ne P_t.
$$

预测又可能改变行动 $A$，行动影响后续 $X,Y$：

$$
\widehat Y\to A\to (X_{\rm future},Y_{\rm future}).
$$

随机打乱 train/test 会泄漏未来并隐藏 drift。需要 time split、label-delay accounting、policy logging 与 pre/post intervention 分层。

## 十三、图：Joint Factorization 决定校正接口

先看图回答：为什么观察到 target predicted-positive rate 增加，不能单独断定 label shift？

![[00-知识库管理/_assets/figures/learning-theory/fig-dataset-shift-factorizations-v2.svg|900]]

> [!figure] 图 20.8-05　Covariate、label 与 concept shift 的因子分账
> 左栏展示两种 joint factorization；中栏对三类 shift、support 与可观测证据分层；右栏给出 detection→diagnosis→correction→evaluation。来源：依据 Quiñonero-Candela et al.、Lipton–Wang–Smola 与 Ovadia et al. 独立绘制；由 [[plot_distribution_shift_v2.py]] 确定性生成。

**怎样读图**：先选 factorization，再声明稳定因子；只有进入右栏并获得相应 target evidence，才能选择校正。

**图没有证明什么**：图没有证明 shift types 互斥，也没有证明 unlabeled target inputs 足以验证 conditional stability。

## 十四、AI 接口

- LLM：topic/time/user changes、知识截止与反馈式数据生成分开；
- 医疗：医院、人群、测量、诊断标准与治疗政策分开；
- 推荐：曝光 policy 同时改变 observed covariates 与 labels；
- 视觉：sensor/corruption、location、class prevalence 与 annotation rule 分开。

## 十五、常见错误

1. 把所有 shift 称为 covariate shift；
2. 认为 label shift 保持 $P(Y\mid X)$；
3. 从 prediction frequency 直接诊断 label shift；
4. 忽略 support mismatch；
5. 用 input two-sample test 证明 conditional invariance；
6. shift correction 后仍用 source test；
7. 随机打乱 temporal data；
8. 忽略 model-driven feedback。

## 十六、最小记忆

> [!summary]
> - shift taxonomy 来自 joint-law factorization；
> - covariate shift 保持 $P(Y\mid X)$；
> - label shift 保持 $P(X\mid Y)$，通常改变 posterior；
> - concept shift 改变任务条件机制；
> - overlap、confusion invertibility 与 target labels 决定可识别性；
> - detection 不等于 diagnosis，更不等于 correction 有效。

## 十七、掌握标准

### A. 定义
能用概率等式定义三类 shift 与 support condition。
### B. 推导
能推导 label-shift Bayes 更新和 confusion-matrix equation。
### C. 反例
能构造多类 shift 重叠、prediction-frequency 误诊与 support failure。
### D. 实验
能设计 time/group metadata monitoring 与 delayed-label target audit。
### E. 迁移
能为实际系统把 shift 类型映射到证据、校正和不可声明结论。

## 十八、练习与独立详解

- [[习题 - Covariate、Label 与 Concept Shift]]
- [[解答 - Covariate、Label 与 Concept Shift]]

## 参考来源

- [[S-2009-Quinonero-Dataset-Shift]]
- [[S-2018-Lipton-Label-Shift]]
- [[S-2019-Ovadia-Uncertainty-Shift]]

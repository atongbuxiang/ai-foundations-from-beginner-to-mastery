---
type: theorem
status: draft
area: [learning-theory/uncertainty, aleatoric, epistemic, heteroscedasticity]
aliases: [Data Uncertainty, Model Uncertainty, Uncertainty Decomposition]
node_id: LT-62
prerequisites: ["[[协方差、相关性与条件期望]]", "[[期望、方差与矩]]", "[[联合熵、条件熵与链式法则]]", "[[Bayesian 推断与后验预测]]", "[[概率校准、Proper Scoring Rule 与可靠性图]]"]
related: ["[[Bayesian Posterior Predictive、Ensemble 与近似边界]]", "[[Conformal Prediction 与有限样本 Coverage]]", "[[OOD、鲁棒性与因果不变性的边界]]", "[[模型可辨识性、选择与 Misspecification]]"]
sources: ["[[S-2021-Hullermeier-Waegeman-Uncertainty]]", "[[S-2017-Kendall-Gal-Uncertainties]]", "[[S-2023-Wimmer-Aleatoric-Epistemic]]"]
exercises: ["[[习题 - Aleatoric、Epistemic 与模型不确定性]]"]
solutions: ["[[解答 - Aleatoric、Epistemic 与模型不确定性]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-aleatoric-epistemic-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# Aleatoric、Epistemic 与模型不确定性

> [!abstract] 本章主问题
> “不确定”不是单一物理量。aleatoric uncertainty 描述在给定信息与模型后，结果仍有随机性；epistemic uncertainty 描述学习者对条件规律、参数或函数的知识不足。二者的数学分解必须绑定信息集、模型层级与不确定性度量，不能把一张图中的两种颜色当成数据里天然存在的两个真值标签。

## 一、学习目标

完成本章后，应能：

1. 说明 uncertainty 必须先绑定预测对象、信息集与行动；
2. 区分 observation noise、label ambiguity、parameter、model-form、approximation 与 shift uncertainty；
3. 用全方差公式推导 aleatoric/epistemic variance decomposition；
4. 推导 heteroscedastic Gaussian NLL，并解释均值—方差耦合；
5. 推导分类 predictive entropy 的 expected-entropy + mutual-information 分解；
6. 说明该熵分解为什么不是模型无关的唯一 taxonomy；
7. 解释“更多数据会降低 epistemic”成立所需的条件；
8. 区分 OOD、misspecification 与高 epistemic score；
9. 设计 calibration、coverage、selective risk 与 shift 多轴评估；
10. 为视觉、医疗、LLM 与科学建模建立 uncertainty claim card。

## 二、先写 Uncertainty Contract

任何“不确定性”陈述先回答：

1. 随机对象是什么：标签、连续响应、未来轨迹、文本答案还是参数？
2. 条件信息是什么：$X=x$、训练数据 $D$、模型类 $\mathcal M$、传感器集合？
3. 谁不知道：真实系统、Bayesian agent、ensemble algorithm 还是人类决策者？
4. 用什么 functional：方差、熵、区间宽度、集合大小、尾部风险？
5. 为哪个行动服务：预测、拒答、采样、探索还是资源分配？

没有这五项，“模型很不确定”只是语义不完整的句子。

## 三、生成随机性与知识不足

设真实数据规律为

$$
Y\mid X=x\sim P^*(\cdot\mid x).
$$

即使完全知道 $P^*$，若它不是点质量，未来 $Y$ 仍不可确定。这是给定 $X=x$ 的生成随机性。

但学习者只有数据

$$
D=\{(X_i,Y_i)\}_{i=1}^n
$$

和模型族 $\{P_\theta\}$，不知道哪一个条件规律合适。对 $\theta$ 或函数的剩余不确定性属于知识状态。

### 3.1 “不可约”是相对于信息集

若只观察低分辨率图像，目标边界可能模糊；加入更清晰传感器 $Z$ 后，

$$
\operatorname{Var}(Y\mid X,Z)
$$

可能小于 $\operatorname{Var}(Y\mid X)$。因此 aleatoric 不是宇宙级不可约常数，而是对当前观测、任务和标签定义条件化后的剩余随机性。

## 四、一张更完整的 Taxonomy

| 层级 | 典型问题 | 数学位置 | 可能缓解 |
|---|---|---|---|
| observation noise | 测量本身有噪声吗？ | $P(Y\mid X,\theta)$ | 更好传感器/重复测量 |
| label ambiguity | 标注规则或事件定义含糊吗？ | annotation law | 重定义任务/多标注者 |
| parameter uncertainty | 同一模型族哪些参数可信？ | $q(\theta\mid D)$ | 更多有信息数据 |
| function uncertainty | 哪些预测函数与数据相容？ | distribution over $f$ | 覆盖新输入区域 |
| model-form uncertainty | 模型族是否错了？ | $\mathcal M$ 之外 | 扩充/比较模型 |
| approximation uncertainty | 推断/优化近似是否不足？ | $q\ne p(\theta\mid D)$ | 更好算法/计算 |
| distribution shift | 部署规律是否改变？ | $P_t\ne P_s$ | 监控/适应/稳健设计 |

把最后四项全部压成“epistemic variance”会丢掉失败原因和可操作方案。

## 五、Hierarchical Predictive Model

给定训练数据 $D$，设学习者对参数的分布为

$$
\Theta\mid D\sim q(\theta\mid D),
$$

并规定

$$
Y_*\mid X_*=x,\Theta=\theta
\sim P_\theta(\cdot\mid x).
$$

预测分布是 mixture：

$$
q(y_*\mid x,D)
=
\int P_\theta(y_*\mid x)q(\theta\mid D)\,d\theta.
$$

只有先定义这个层级模型，后面的 “within-model” 与 “between-model” 才有精确含义。

## 六、总方差分解

记

$$
\mu_\theta(x)
=E[Y_*\mid x,\theta],
\qquad
\sigma_\theta^2(x)
=\operatorname{Var}(Y_*\mid x,\theta).
$$

全方差公式给出

$$
\boxed{
\operatorname{Var}(Y_*\mid x,D)
=
\underbrace{E_{\Theta\mid D}[\sigma_\Theta^2(x)]}_{\text{within-model}}
+
\underbrace{\operatorname{Var}_{\Theta\mid D}[\mu_\Theta(x)]}_{\text{between-model}}.
}
$$

### 6.1 逐步推导

令 $m(x)=E[Y_*\mid x,D]$。加减 $\mu_\Theta(x)$：

$$
Y_*-m
=
\bigl(Y_*-\mu_\Theta\bigr)
+
\bigl(\mu_\Theta-m\bigr).
$$

平方取期望。交叉项为

$$
E\!\left[
(Y_*-\mu_\Theta)(\mu_\Theta-m)\mid x,D
\right]=0,
$$

因为给定 $\Theta$ 后第一因子的条件期望为零。于是得到两项分解。

### 6.2 解释边界

第一项常被称为 aleatoric，第二项常被称为 epistemic；但这个命名只对当前 $q(\theta\mid D)$ 与 likelihood 成立。错设 likelihood 可把系统误差错误吸收到任何一项。

## 七、一个数值例子

两个等权模型：

$$
\mu_1=0,\quad \mu_2=2,
\qquad
\sigma_1^2=\sigma_2^2=1.
$$

mixture mean：

$$
m=\frac{0+2}{2}=1.
$$

within variance：

$$
\frac{1+1}{2}=1.
$$

between variance：

$$
\frac{(0-1)^2+(2-1)^2}{2}=1.
$$

总 predictive variance 为 $2$。若两个模型都把自身 observation variance 报为 0，mixture 仍因模型均值分歧而有方差 1。

## 八、Heteroscedastic Gaussian Regression

模型输出

$$
\mu_\theta(x),\qquad s_\theta(x)=\log\sigma_\theta^2(x),
$$

并设

$$
Y\mid x,\theta\sim
\mathcal N(\mu_\theta(x),e^{s_\theta(x)}).
$$

忽略常数，单样本 NLL：

$$
\boxed{
\ell(x,y)
=
\frac12 e^{-s_\theta(x)}
\bigl(y-\mu_\theta(x)\bigr)^2
+
\frac12s_\theta(x).
}
$$

第一项允许高预测方差降低大残差惩罚，第二项阻止方差无穷增大。

### 8.1 对 $s$ 的局部最优

固定残差 $r=y-\mu$：

$$
\frac{\partial\ell}{\partial s}
=-\frac12e^{-s}r^2+\frac12.
$$

令其为零得到

$$
e^s=r^2.
$$

单样本下模型可用大方差解释大残差；总体条件风险下，理想方差对应给定 $x$ 的条件平方残差。若均值错设，所谓 aleatoric variance 会吸收 bias。

## 九、Homoscedastic、Heteroscedastic 与 Heavy Tail

- homoscedastic：$\sigma^2(x)=\sigma^2$；
- heteroscedastic：$\sigma^2(x)$ 随输入改变；
- heavy-tailed：Gaussian 方差可能不足以表达 rare extreme events；
- multimodal：单一均值—方差不能表示多个可能未来。

把所有结构都压成 $\sigma^2(x)$ 会使 uncertainty 数字看似合理但生成分布错误。应结合 residual diagnostics、PIT、tail score 与 coverage。

## 十、分类中的 Predictive Entropy 分解

设成员概率

$$
p_\theta(y\mid x),
$$

mixture 概率

$$
\bar p(y\mid x,D)
=E_{\Theta\mid D}[p_\Theta(y\mid x)].
$$

predictive entropy：

$$
H(\bar p)
=-\sum_y\bar p_y\log\bar p_y.
$$

在层级模型中，

$$
\boxed{
H(Y_*\mid x,D)
=
E_{\Theta\mid D}
[H(Y_*\mid x,\Theta)]
+
I(Y_*;\Theta\mid x,D).
}
$$

第一项是成员内部平均 entropy，第二项是标签与模型参数之间的 mutual information，也等于

$$
E_{\Theta\mid D}
D_{\mathrm{KL}}
\bigl(p_\Theta(\cdot\mid x)\Vert\bar p(\cdot\mid x)\bigr).
$$

## 十一、为什么 Entropy/MI 不是唯一答案

上述恒等式代数上正确，但语义上仍依赖：

1. $q(\theta\mid D)$ 是否有意义；
2. 不同 $\theta$ 是否只是同一函数的参数对称；
3. likelihood entropy 是否真的对应 data noise；
4. 模型族错设是否被 posterior 表达；
5. 类别数、label semantics 与 entropy scale；
6. ensemble members 是否为 posterior samples；
7. 关心的是平均不确定、尾部风险还是行动代价。

因此 MI 可以作为 disagreement measure，但不能无条件宣称是“真实 epistemic uncertainty”。

## 十二、更多数据会怎样

理想的 well-specified、可辨识 Bayesian regular setting 中，数据覆盖 $x$ 附近且 $n\to\infty$ 时，posterior 可集中：

$$
q(\theta\mid D)\Rightarrow\delta_{\theta^*},
$$

于是 between-model variance 可趋近 0，而真实 observation variance 保留。

但以下情况会失败：

- $x$ 位于训练支持集之外；
- 参数/函数不可辨识；
- 模型错设；
- posterior approximation collapse；
- 标签定义随时间改变；
- 数据量增加但没有覆盖相关方向；
- optimization 只到一个 mode。

“epistemic 必随样本数单调下降”不是无条件有限样本定理。

## 十三、OOD 与 Epistemic 不是同义词

OOD 是相对于参考分布的关系；epistemic 是相对于学习者知识状态的概念。可能出现：

- OOD 但任务简单，模型一致且预测正确；
- in-distribution rare subgroup 上模型高度分歧；
- 所有成员在 OOD 上一致地过度自信；
- 仅像素距离远但语义机制相同；
- 输入近似训练数据但 label mechanism 已改变。

所以 entropy、ensemble variance、density score 与 distance score 都需要独立的 failure-detection benchmark。

## 十四、Uncertainty 不能由 Accuracy 单独验证

完整评估至少包括：

1. proper scores：NLL、Brier、CRPS；
2. calibration：reliability、coverage；
3. sharpness/efficiency：entropy、interval width、set size；
4. selective prediction：risk–coverage curve；
5. ranking：error detection AUROC/AUPRC；
6. shift severity curves；
7. subgroup/temporal performance；
8. decision utility 与 abstention cost。

没有 “epistemic ground-truth label” 时，应通过可证伪后果评估，而不是只看热力图是否“像边界”。

## 十五、图：不确定性是一套层级条件分解

先看图回答：若两个模型给出相同均值但不同方差，或不同均值但各自方差很小，二者的风险来源相同吗？

![[00-知识库管理/_assets/figures/learning-theory/fig-aleatoric-epistemic-v2.svg|900]]

> [!figure] 图 20.8-02　Aleatoric、epistemic 与 model/shift uncertainty
> 左栏从 information set 区分生成随机性与知识不足；中栏给出总方差和 entropy/MI 分解；右栏展示 likelihood 错设、approximation、OOD 与 decision evaluation 的边界。来源：依据 Hüllermeier–Waegeman、Kendall–Gal 与 Wimmer et al. 独立绘制；确定性 SVG，由 [[plot_calibration_uncertainty_v2.py]] 生成。

**怎样读图**：先确定随机对象与条件信息，再选择方差或 entropy 分解；最后检查模型错设和 shift 是否被所选层级遗漏。

**图没有证明什么**：图没有证明 aleatoric 与 epistemic 在任意数据集中可唯一辨识，也没有证明 ensemble disagreement 是 OOD 或错误的可靠检测器。

## 十六、AI 接口

### 16.1 视觉与自动驾驶

图像模糊、遮挡可进入 observation model；新天气、传感器故障、地图更新属于不同 shift。按像素预测 variance 不能替代轨迹级安全 coverage。

### 16.2 医疗

生理随机性、测量误差、诊断标准冲突和医院 shift 必须分层。把少数群体数据不足误标为“病情 aleatoric”会掩盖可改善的不公平。

### 16.3 LLM

token entropy、不同采样答案的分歧、事实未知与题目歧义不是同一对象。自一致性只测 sampling/procedure 下的 variation，不自动识别知识边界。

### 16.4 Active Learning

若 query score 只选高 aleatoric 点，新增标签可能没有价值；理想 acquisition 还应考虑可缩减性、覆盖、成本与 batch redundancy。

## 十七、常见错误

1. 不声明随机对象与条件信息；
2. 把 aleatoric 当绝对不可约；
3. 把所有模型分歧叫 posterior epistemic；
4. 把 entropy/MI 分解当唯一 taxonomy；
5. 忽略 likelihood misspecification；
6. 认为更多 MC samples 会修复近似偏差；
7. 把 OOD 与高 epistemic 画等号；
8. 只用 accuracy 验证 uncertainty；
9. 在训练数据上展示 uncertainty heatmap；
10. 不报告 shift、subgroup 与 action cost。

## 十八、最小记忆

> [!summary]
> - uncertainty 必须绑定对象、信息集、模型与行动；
> - 总方差分成成员内随机性和成员间均值分歧；
> - heteroscedastic likelihood 可学习输入依赖噪声，但也会吸收 bias；
> - predictive entropy = expected entropy + MI 只在已声明层级模型下解释；
> - model-form、approximation 与 shift 不能自动被一个 epistemic 数字覆盖；
> - 评价要同时看 proper score、calibration、coverage、sharpness 与 utility。

## 十九、掌握标准

### A. 定义

能建立 uncertainty contract，并区分七类来源。

### B. 推导

能逐步推导总方差、Gaussian heteroscedastic NLL 与 entropy/MI 恒等式。

### C. 反例

能构造 OOD 但低 disagreement、in-distribution 但高 disagreement 及错设均值导致 variance 膨胀的例子。

### D. 实验

能在合成异方差数据上分开 calibration、interval width 与 shift detection，报告模型/推断近似。

### E. 迁移

能为高风险 AI 系统把不确定性来源映射到传感、数据、模型、推断和行动层缓解方案。

## 二十、练习与独立详解

- [[习题 - Aleatoric、Epistemic 与模型不确定性]]
- [[解答 - Aleatoric、Epistemic 与模型不确定性]]

## 参考来源

- [[S-2021-Hullermeier-Waegeman-Uncertainty]]
- [[S-2017-Kendall-Gal-Uncertainties]]
- [[S-2023-Wimmer-Aleatoric-Epistemic]]

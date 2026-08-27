---
type: concept
status: verified
area: [language-models, evaluation, calibration, uncertainty]
node_id: LM-60
aliases: [语言模型校准, Selective Generation]
prerequisites: ["[[概率校准、Proper Scoring Rule 与可靠性图]]", "[[语言模型评估对象、任务单位与 Benchmark 合同]]"]
related: ["[[Pass-at-k、Best-of-N、采样估计与选择偏差]]", "[[Abstention、Refusal、Over-refusal 与风险覆盖]]"]
sources: ["[[S-2007-Gneiting-Raftery-Proper-Scoring]]", "[[S-2017-Guo-Calibration]]", "[[S-2017-Geifman-Selective-Classification]]", "[[S-2023-Kuhn-Semantic-Uncertainty]]", "[[S-2023-Su-9632-NBCE]]"]
exercises: ["[[习题 - Proper Scoring、Calibration、ECE 与 Selective Generation]]"]
solutions: ["[[解答 - Proper Scoring、Calibration、ECE 与 Selective Generation]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-eval-calibration-risk-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Proper Scoring、Calibration、ECE 与 Selective Generation

> [!abstract] 一句话结论
> 校准必须先定义事件：token 正确、答案等价类正确、claim 被支持或工具成功。Proper score 奖励诚实概率，ECE 是依赖分箱的摘要，risk–coverage 评价置信度排序能否用拒答换风险；三者不能互相替代。

## 一、概率必须对应事件

二元事件 $Y\in\{0,1\}$ 可是“最终答案正确”。系统报告 confidence $C\in[0,1]$。校准定义为

$$
\Pr(Y=1\mid C=c)=c.
$$

开放文本没有天然单一“答案概率”。Token sequence probability 随长度相乘，paraphrase 又把同一意义分散到多条字符串。必须声明：

- exact string event；
- normalized answer equivalence class；
- semantic cluster；
- atomic claim support；
- tool success 或用户满意。

对一个事件校准不推出对另一个事件校准。

## 二、Brier 与 log score

以 loss 越小越好，Brier loss：

$$
\ell_{\rm Brier}(q,y)=(q-y)^2.
$$

若真实事件概率为 $p$，

$$
\mathbb E_p[(q-Y)^2]
=p(1-p)+(q-p)^2,
$$

在 $q=p$ 唯一最小。Log loss

$$
\ell_{\log}(q,y)=-y\log q-(1-y)\log(1-q)
$$

的期望 regret 是 Bernoulli KL，也在 $q=p$ 唯一最小。Strict propriety 是总体期望性质；有限 test 上某个失真预测器可能偶然分更低。

Accuracy 只看阈值后的决定，无法区分信心 .51 与 .99；proper score 同时奖励判对与概率质量。

## 三、ECE 的定义与盲区

把样本按 confidence 分进 bins $B_m$：

$$
\operatorname{acc}(B_m)=\frac1{|B_m|}\sum_{i\in B_m}y_i,
\quad
\operatorname{conf}(B_m)=\frac1{|B_m|}\sum_{i\in B_m}c_i,
$$

$$
\operatorname{ECE}
=\sum_m\frac{|B_m|}{n}
\left|\operatorname{acc}(B_m)-\operatorname{conf}(B_m)\right|.
$$

ECE 依 bin 数、边界、等宽/等频、空 bin 与样本量；同一 bin 内过/欠置信可相互抵消。ECE 不是 proper score，两个模型的 ECE 排名也可能随 binning 反转。应同时画 reliability diagram、样本计数和置信区间，并报告 Brier/log loss。

## 四、Temperature scaling

分类 logits $z$ 用验证集拟合 $T>0$：

$$
q_T(y\mid x)=\operatorname{softmax}(z(x)/T).
$$

正温度保持 argmax，通常不改变 top-1 accuracy，却可改变 confidence 和 NLL。$T$ 只能在 validation 拟合；同一 $T$ 对新领域、长文本或 API 漂移无自动保证。

语言模型 generation temperature 改 rollout 分布；post-hoc calibration temperature 改用于报告概率的 logits。二者目的不同，不能用同一参数名混写。

## 五、语义不确定性

从模型采样字符串 $y_j$，用等价关系聚成意义类 $G_1,\ldots,G_K$。若能估计每类质量

$$
P(G_k\mid x)=\sum_{y\in G_k}P(y\mid x),
$$

semantic entropy 为

$$
H_{\rm sem}(x)=-\sum_kP(G_k\mid x)\log P(G_k\mid x).
$$

实践只观察有限样本，并用 NLI/LLM 聚类近似等价关系。采样温度、样本数、cluster 顺序与 judge error 都要进入不确定性账。多个措辞一致不等于事实正确，只表示样本质量集中在一个意义。

## 六、Selective generation

置信度 $s_i$ 超过阈值 $\tau$ 才回答。Coverage 与 selective risk：

$$
\operatorname{coverage}(\tau)
=\frac1n\sum_i\mathbf1[s_i\ge\tau],
$$

$$
\operatorname{risk}(\tau)
=\frac{\sum_i\ell_i\mathbf1[s_i\ge\tau]}
{\sum_i\mathbf1[s_i\ge\tau]}.
$$

阈值扫过得到 risk–coverage curve。只报告“回答样本准确率 99%”而不报 coverage 可能意味着几乎全部拒答。AURC 也要说明风险定义和积分离散化。

校准与排序分开：一个单调变换可破坏数值校准但保持所有阈值排序；反之总体校准不保证每个 subgroup 的排序有效。

## 七、条件证据与置信

加入 context/RAG 后，confidence 的对象可能变为 $P(Y=1\mid x,z)$。NBCE 一类方法提醒长 context 的条件概率会受位置与依赖近似影响，但“概率变高”不等于证据真实或校准改善。至少分开：

- closed-book confidence；
- evidence answerability/retrieval；
- answer correctness；
- claim support/attribution；
- abstention decision。

## 八、图解：可靠性图、proper loss 与风险覆盖

**读图问题**：同一组 confidence 怎样同时产生 reliability bins、Brier/log loss 和 risk–coverage 曲线，为什么三幅图回答的不是同一个问题？

![[00-知识库管理/_assets/figures/language-models/fig-lm-eval-calibration-risk-v1.svg|900]]

> [!figure] 图 LM-60　Probability quality—calibration—selective decision 三联图
> **生成：**本库按二元事件、ECE、Brier 与 risk–coverage 定义绘制教学样本；点数和区间不来自真实模型。

**怎样读图**：左侧看概率损失是否奖励真实 $p$，中间逐 bin 比较 accuracy/confidence 与样本量，右侧沿阈值降低 coverage，检查风险是否随拒答稳定下降及哪些群体被优先拒绝。

**图没有证明什么**：可靠性曲线贴近对角线不证明模型准确、排序优秀或 subgroup 公平；低 selective risk 也不证明整体安全，因为它可能以低覆盖或偏向性拒答换得。

## 九、常见错误与出口标准

错误包括：token probability 当答案 confidence；ECE 不写 bins；test 拟合温度；只报 ECE 不报 proper score；多样措辞当高不确定；risk 不报 coverage；总体校准替代 subgroup。

完成本节后，应能定义事件，推导 Brier propriety，手算 ECE，解释 temperature scaling，构造 semantic class，并画带分母和 group slice 的 risk–coverage 曲线。

## 十、来源与练习

- [[S-2007-Gneiting-Raftery-Proper-Scoring]]；
- [[S-2017-Guo-Calibration]]；
- [[S-2017-Geifman-Selective-Classification]]；
- [[S-2023-Kuhn-Semantic-Uncertainty]]；
- [[S-2023-Su-9632-NBCE]]；
- [[习题 - Proper Scoring、Calibration、ECE 与 Selective Generation]]；
- [[解答 - Proper Scoring、Calibration、ECE 与 Selective Generation]]。

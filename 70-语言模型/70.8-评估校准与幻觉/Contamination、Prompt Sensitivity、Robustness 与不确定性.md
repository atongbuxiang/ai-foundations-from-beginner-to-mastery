---
type: concept
status: verified
area: [language-models, evaluation, contamination, robustness]
node_id: LM-63
aliases: [Benchmark 污染与稳健性, Prompt 敏感性]
prerequisites: ["[[语言模型评估对象、任务单位与 Benchmark 合同]]", "[[Benchmark 污染、时间截止与成员重叠审计]]"]
related: ["[[能力—行为—系统评估协议与证据地图]]", "[[Model、API、Tokenizer、Template 版本与复现合同]]"]
sources: ["[[S-2024-Oren-BlackBox-Contamination]]", "[[S-2024-Sclar-Prompt-Sensitivity]]", "[[S-2020-Brown-GPT3-Contamination]]", "[[S-2024-Li-Open-Contamination]]", "[[S-2024-Hsieh-RULER]]"]
exercises: ["[[习题 - Contamination、Prompt Sensitivity、Robustness 与不确定性]]"]
solutions: ["[[解答 - Contamination、Prompt Sensitivity、Robustness 与不确定性]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-eval-contamination-robustness-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Contamination、Prompt Sensitivity、Robustness 与不确定性

> [!abstract] 一句话结论
> Benchmark 分数可能同时受训练暴露、记忆利用、prompt 格式、样本构成、decoder seed 与版本漂移影响。污染检测、稳健性实验和置信区间分别回答不同问题；“未发现重叠”与“换一个 prompt 仍高分”都不是能力纯净性的证明。

## 一、污染至少有六种

1. test item 原文进入 pretraining；
2. reference answer/solution/explanation 泄漏；
3. paraphrase、翻译、截图/OCR 版本进入训练；
4. benchmark 模板、标签映射或 canonical order 泄漏；
5. post-training、tool index、prompt cache 接触 test；
6. 反复在公开榜单上调参形成 test feedback。

Exact n-gram overlap 只能覆盖其中一部分。时间 cutoff 有用，但网页发布日期、抓取日期、模型训练截止与 post-training date 必须分开。

## 二、Exposure、memorization 与 exploitation

定义事件：

- $E$：训练/适配数据含 benchmark 信息；
- $M$：模型参数/系统可表现出记忆痕迹；
- $X$：评测时实际利用该信息提高结果。

$E$ 不必然导致 $M$；$M$ 不必然在当前 prompt 被利用；异常高分也不证明 $E$。因此报告 overlap/detector、memorization probe、clean/dirty score gap 与 causal removal 时不能互相替代。

清洗后分数下降也可能因清洗样本更难；需要匹配难度、预注册阈值和 sensitivity analysis。

## 三、黑箱 canonical-order 检验

Oren 等利用零假设：若 benchmark 未以 canonical 顺序暴露，示例顺序在某种 exchangeability 条件下不应使 canonical ordering 有系统更高 likelihood。以随机 permutations 构造 null distribution，得到 p-value/精确假阳控制。

审计问题：

- 模型 API 是否给可比较 likelihood；
- exchangeability 与 tokenization 是否成立；
- permutation 数与检验 power；
- 多 benchmark/多模型 multiplicity；
- 拒绝零假设支持何种污染机制。

不拒绝可能是无污染，也可能是样本小、模型弱、顺序未记住或 API 精度不足。

## 四、Prompt 是实验因子

设 item $i$、prompt variant $p$、seed $s$ 的分数

$$
y_{ips}=\mu+\alpha_i+\beta_p
+(\alpha\beta)_{ip}+\epsilon_{ips}.
$$

Prompt mean、best prompt、worst prompt 与随机 prompt 期望是不同 estimands。若在 test variants 中选最高：

$$
\max_p\hat\theta_p
$$

有 winner's curse。应在 validation 选模板，或在 test 报预先定义的多模板均值/worst-case/variance。

“语义不变”的格式变体需人工确认：选项顺序改变可能改变标签先验，few-shot 顺序也可能改变真正的条件信息。

## 五、Robustness 的三种聚合

对扰动集合 $\mathcal T(x)$：

$$
R_{\rm avg}=\mathbb E_{t\sim\pi}m(t(x)),
\quad
R_{\rm worst}=\min_{t\in\mathcal T}m(t(x)),
\quad
\Delta=m(x)-R_{\rm avg}.
$$

Average 依部署扰动分布 $\pi$；worst-case 依攻击/搜索预算；drop 依原 prompt 基线。三者不能混称 robustness。适应性攻击者若看到系统，可比固定变体找到更坏 prompt，必须记录预算。

## 六、不确定性与独立单位

题目、模板、seed、judge 形成交叉/嵌套结构。简单 bootstrap 所有输出会假装它们 iid。常见策略：

- 比较模型时按 item 做 paired bootstrap；
- 同一来源/用户成簇时 cluster bootstrap；
- prompt 是希望外推的随机族时，分层重采 item 与 prompt；
- API 日间漂移时按 run/day blocking；
- 报 effect size 与 CI，不只报 p-value。

若同时看许多任务/slices/prompts，要预注册 primary family 或用多重比较控制；探索性发现必须标记并在新集复验。

## 七、版本与回归

动态 API 的“同名模型”可能改变权重、template、安全策略或工具。时间序列需保留：

- raw requests/responses；
- model snapshot/API date；
- prompt/token IDs；
- decoder/judge/retriever versions；
- benchmark snapshot；
- environment 与 failure trace。

不可重放旧模型时，只能复核保存的输出评分，不能重建当时的生成分布。

## 八、图解：污染路径与方差分解

**读图问题**：训练暴露怎样经过记忆与评测利用影响分数，prompt、item、seed 与版本的波动又为何不能被一个总体误差条掩盖？

![[00-知识库管理/_assets/figures/language-models/fig-lm-eval-contamination-robustness-v1.svg|900]]

> [!figure] 图 LM-63　Exposure→memorization→exploitation 与 item×prompt×seed 方差板
> **生成：**本库按污染事件链、canonical-order null 与分层评估设计绘制；热图值和 permutation 为教学数据。

**怎样读图**：先沿左侧三事件链定位检测器能支持哪一步，再在右侧按 item、prompt、seed 和 run/day 分解变化；底部将 average、worst-case 与 clean/dirty gap 分开报告。

**图没有证明什么**：发现高 overlap 不证明模型靠记忆作答，黑箱检验不拒绝也不证明无污染；教学方差板更不能代替真实多模板、多 seed、跨时间采样与 cluster-aware CI。

## 九、常见错误与出口标准

错误包括：exact match 清零就称无污染；污染比例等同分数增益；best test prompt；扰动平均当 worst-case；输出当 iid；CI 不含模型/API 漂移；多切片挑显著项。

完成本节后，应能构造污染六分法和 E/M/X 事件，解释 permutation null，设计 prompt factorial，选择正确重采样单位，并写出带版本、multiplicity 与适应性预算的稳健性协议。

## 十、来源与练习

- [[S-2024-Oren-BlackBox-Contamination]]；
- [[S-2024-Sclar-Prompt-Sensitivity]]；
- [[S-2020-Brown-GPT3-Contamination]]；
- [[S-2024-Li-Open-Contamination]]；
- [[S-2024-Hsieh-RULER]]；
- [[习题 - Contamination、Prompt Sensitivity、Robustness 与不确定性]]；
- [[解答 - Contamination、Prompt Sensitivity、Robustness 与不确定性]]。

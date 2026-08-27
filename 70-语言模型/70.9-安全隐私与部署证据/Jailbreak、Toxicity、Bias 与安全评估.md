---
type: concept
status: verified
area: [language-models, safety, jailbreak, toxicity, bias, red-teaming]
node_id: LM-68
aliases: [语言模型安全评估, 红队与伤害评估]
prerequisites: ["[[Prompt Injection、Indirect Injection 与 Tool-RAG 威胁模型]]", "[[LLM-as-a-Judge、Pairwise Preference、位置与长度偏差]]"]
related: ["[[Abstention、Refusal、Over-refusal 与风险覆盖]]"]
sources: ["[[S-2025-NIST-Adversarial-ML]]", "[[S-2020-Gehman-RealToxicityPrompts]]", "[[S-2022-Parrish-BBQ]]", "[[S-2024-Mazeika-HarmBench]]", "[[S-2024-Wang-Do-Not-Answer]]", "[[S-2024-NIST-GenAI-Profile]]"]
exercises: ["[[习题 - Jailbreak、Toxicity、Bias 与安全评估]]"]
solutions: ["[[解答 - Jailbreak、Toxicity、Bias 与安全评估]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-safety-redteam-risk-matrix-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Jailbreak、Toxicity、Bias 与安全评估

> [!abstract] 一句话结论
> Jailbreak 是攻击过程，toxicity 与 bias 是特定可测行为，harm 是结合用户、情境、能力与后果的系统事件；可信安全评估必须同时测危险请求漏放、正常请求误拒、群体切片、攻击适应性和真实工具后果。

## 一、不要把“安全”压成一个词

至少分四层：

1. **policy violation**：输出是否违反某版明确政策；
2. **content property**：毒性、仇恨、欺骗、隐私、危险性等标签；
3. **system action**：是否调用工具、传播内容或改变状态；
4. **realized harm**：特定主体在情境中实际遭受的损失。

一段尖锐但用于批判分析的文本可能被 toxicity classifier 高分；礼貌的错误医疗建议也可能低毒却高危。指标必须绑定事件。

## 二、Jailbreak 是有预算的攻击

给定模型系统 $f_v$、政策 $\pi_v$ 和目标行为 $g$，攻击者在预算 $B$ 内选择提示序列 $a_{1:B}$。攻击成功事件为

$$
J=\mathbf1[
\exists t\le B:\ 
\operatorname{harm}(f_v(a_t),g,\pi_v)=1
].
$$

报告必须包括：

- 攻击者是否知道系统 prompt/防御；
- 是否可多轮、改写、观察拒绝理由；
- 查询、token、人工与计算预算；
- 成功由规则、分类器、LLM judge 还是人评决定；
- 是否要求真正完成有害能力，还是只出现关键词；
- 模型、模板、policy、tool 权限和日期。

Best-of-many 红队与单次用户风险不是同一 estimand。

## 三、Toxicity：测量器也是模型

设分类器输出 $q(x)$，阈值 $\tau$ 后得到 toxic label。完整误差包括语境、引用、方言、身份词、语言和长度。应保存：

$$
\operatorname{FPR}_g,\quad
\operatorname{FNR}_g,\quad
\Pr(q>\tau\mid \text{prompt slice}=g)
$$

以及人工复核样本。生成评估还依 sampler：每提示生成 $k$ 个，报告平均毒性、最大毒性或至少一次超过阈值，分别回答不同问题。

## 四、Bias：歧义与证据条件

BBQ 类设计区分：

- ambiguous context：证据不足，模型应表达不确定；
- disambiguated context：证据足够，模型应按事实回答；
- target/non-target group：检查错误方向。

偏见分数应与任务准确率联合报告。若模型对所有群体都拒答，偏见表面下降但效用也消失。总体均值还可能隐藏交叉群体和语言差异。

## 五、二乘二拒答矩阵

把请求真值简化为 harmful/benign，把系统行为简化为 refuse/answer：

|  | 系统拒答 | 系统回答 |
|---|---:|---:|
| harmful | 安全命中 $R_h$ | 漏放 $A_h$ |
| benign | 过度拒答 $R_b$ | 正常完成 $A_b$ |

可定义

$$
\operatorname{harmful\ recall}=\frac{R_h}{R_h+A_h},
\qquad
\operatorname{benign\ utility}=\frac{A_b}{A_b+R_b}.
$$

但“回答”仍要分安全改写、有限帮助和完整有害完成；“拒答”也要分解释性拒答、空响应与错误分类。

## 六、红队矩阵与统计单位

覆盖轴至少包括：

- harm category × severity；
- direct × obfuscated × multi-turn × indirect；
- base/instruct/system policy；
- language/dialect/region；
- closed text × RAG × tool/agent；
- novice × expert/adaptive attacker；
- normal load × repeated attempts。

同一 base prompt 的多个变体相关，应以 prompt family 为 cluster。报告每 family 是否至少一个成功、每 query 成功率和攻击成本，不能把数千近似变体当独立样本缩窄区间。

## 七、缓解措施与残余风险

训练时数据/偏好优化、推理时 policy model、输入/输出分类器、工具权限、人工确认和事后监控各解决不同环节。评估采用 adaptive loop：

1. 冻结当前防御和可见信息；
2. 在预算内生成/选择变体；
3. 用独立判定与人工锚点评分；
4. 记录新攻击族，不回填 test；
5. 防御更新后建新版本 test；
6. 报旧/新攻击迁移与 benign regression。

安全不是一次性 benchmark，而是版本化对抗过程。

## 八、图解：行为、攻击与后果矩阵

**读图问题**：怎样把 prompt 类型、攻击预算、内容标签、拒答误差与工具后果放在同一评估设计里，又不把它们压成一个总分？

![[00-知识库管理/_assets/figures/language-models/fig-lm-safety-redteam-risk-matrix-v1.svg|900]]

> [!figure] 图 LM-68　红队覆盖矩阵、拒答混淆矩阵与残余风险
> **生成：**本库以抽象 harm categories 和无害示例绘制；不包含攻击载荷或伤害性内容。

**怎样读图**：先沿攻击面和群体切片检查覆盖，再用 harmful/benign 两个分母读漏放与误拒，最后把模型输出接到实际系统权限和 severity。

**图没有证明什么**：矩阵有格子不代表覆盖充分；classifier/judge 标签不等于真实伤害，固定攻击集通过也不覆盖适应性对手。

## 九、常见错误与出口标准

错误包括：toxicity 等于 harm；关键词等于 jailbreak success；不写政策版本；只测英语；只报最坏例或平均值；攻击变体当独立；模型 judge 无人类锚点；安全提高不报 over-refusal；模型拒答却工具已执行。

完成后应能写 jailbreak threat model，区分 content/property/action/harm，计算拒答矩阵指标，构造按群体与攻击族分层的红队协议，并说明为何需要独立判定和 adaptive test。

## 十、来源与练习

- [[S-2025-NIST-Adversarial-ML]]；
- [[S-2020-Gehman-RealToxicityPrompts]]；
- [[S-2022-Parrish-BBQ]]；
- [[S-2024-Mazeika-HarmBench]]；
- [[S-2024-Wang-Do-Not-Answer]]；
- [[S-2024-NIST-GenAI-Profile]]；
- [[习题 - Jailbreak、Toxicity、Bias 与安全评估]]；
- [[解答 - Jailbreak、Toxicity、Bias 与安全评估]]。

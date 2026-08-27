---
type: concept
status: verified
area: [language-models, safety, abstention, refusal, selective-prediction]
node_id: LM-69
aliases: [拒答与风险覆盖, Over-refusal]
prerequisites: ["[[Proper Scoring、Calibration、ECE 与 Selective Generation]]", "[[Jailbreak、Toxicity、Bias 与安全评估]]"]
related: ["[[线上监控、Drift、反馈回路与 Incident 记录]]"]
sources: ["[[S-2017-Geifman-Selective-Classification]]", "[[S-2022-Kadavath-Know-What-Know]]", "[[S-2024-Rottger-XSTest]]", "[[S-2024-Wang-Do-Not-Answer]]", "[[S-2026-Muhamed-RefusalBench]]"]
exercises: ["[[习题 - Abstention、Refusal、Over-refusal 与风险覆盖]]"]
solutions: ["[[解答 - Abstention、Refusal、Over-refusal 与风险覆盖]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-safety-refusal-risk-coverage-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Abstention、Refusal、Over-refusal 与风险覆盖

> [!abstract] 一句话结论
> Abstention 因“不会/证据不足”退出，refusal 因“即使会也不应直接做”受政策约束；二者都要与正常完成、有限安全帮助和人工升级一起评价，并用 risk–coverage、代价矩阵和群体切片防止“全拒绝即最安全”。

## 一、四种动作而非二元拒答

对请求 $x$，系统动作可写为

$$
a(x)\in
\{\text{answer},\text{abstain},\text{refuse},
\text{safe-complete},\text{escalate}\}.
$$

- **answer**：直接完成；
- **abstain**：因知识/证据/置信不足不作实体断言；
- **refuse**：因政策、权限或风险不提供目标能力；
- **safe-complete**：拒绝危险部分，同时给安全替代、澄清或高层信息；
- **escalate**：交人工、认证流程或高可信工具。

一个“抱歉我不能”字符串不足以判断行为。模型可能表面拒绝却在后文给出完整内容，也可能错误声称安全原因而掩盖知识不足。

## 二、任务真值也是多维的

令

- $Y_c$：若作答，内容是否正确；
- $Y_s$：直接完成是否允许/安全；
- $Y_e$：证据是否充分；
- $Y_u$：用户任务是否有可接受的安全替代。

最优动作是条件决策

$$
a^\star(x)
=\arg\min_a
\mathbb E[C(a,Y_c,Y_s,Y_e,Y_u)\mid x].
$$

代价矩阵由应用决定：医疗误答、低风险百科误答、危险能力漏放与无害问题误拒的代价不相同。不能用同一阈值服务所有领域。

## 三、Selective risk 与 Coverage

先考虑只在 score $s(x)\ge\tau$ 时回答。选择函数 $g_\tau(x)$ 为 0/1：

$$
\operatorname{coverage}(\tau)
=\frac1n\sum_i g_\tau(x_i),
$$

$$
\operatorname{risk}(\tau)
=\frac{\sum_i\ell_i g_\tau(x_i)}
{\sum_i g_\tau(x_i)}.
$$

阈值升高通常降低 coverage；若 score 能排序错误，risk 应下降。可是 safety refusal 的 score 可能表示“风险高”，方向相反。应把 correctness confidence $s_c$ 与 harmfulness/policy risk $s_h$ 分开：

$$
\text{answer only if }s_c\ge\tau_c
\ \land\ s_h\le\tau_h.
$$

## 四、拒答混淆矩阵与效用

对 harmful/benign 标签：

$$
\operatorname{unsafe\ answer\ rate}
=\Pr(\text{answer}\mid\text{harmful}),
$$

$$
\operatorname{overrefusal}
=\Pr(\text{refuse}\mid\text{benign}).
$$

还应测 safe-completion quality、事实正确、帮助程度、解释是否泄露敏感细节、人工升级延迟与用户放弃率。XSTest 类 benign-sensitive set 用于发现表面关键词触发的误拒；Do-Not-Answer 类 harmful set 检查漏放。两个分母缺一不可。

## 五、为什么 verbal confidence 不等于拒答依据

模型说“我有 90% 把握”是一个生成文本事件。它可受措辞、示例、温度和模型版本影响。必须在独立 validation 上把 score 映射到目标事件，再在 test/线上监控。

同样，policy classifier 的概率不是“真实伤害概率”。它只在其标签定义与总体下有校准含义。一个输入可同时低事实置信、高安全风险，此时应拒答或升级；也可高事实置信但政策禁止，仍应拒答。

## 六、阈值选择与统计保证

若目标是“已回答样本错误风险不超过 $r_0$”，在 validation 对每个阈值计算风险上置信界 $U_R(\tau)$，选择

$$
\tau^\star
=\arg\max_\tau \operatorname{coverage}(\tau)
\quad\text{s.t.}\quad U_R(\tau)\le r_0.
$$

冻结阈值后只在独立 test 评一次。多个阈值的选择带来 selection bias，应使用独立 split、校正或序贯有效方法。线上分布漂移后，历史保证不能自动延续。

## 七、群体覆盖与被选择人群

总体 risk 低可能因为系统主要拒绝某些语言、方言、领域或新用户。至少报告

$$
\operatorname{coverage}_g,\quad
\operatorname{risk}_g,\quad
\operatorname{overrefusal}_g.
$$

若某组 coverage 太低，其风险估计也因样本少而不稳定。公平目标可能是最小覆盖、风险上限或代价约束，必须公开选择而非隐含在阈值里。

## 八、图解：两个 score、五种动作与三条曲线

**读图问题**：correctness confidence 与 safety risk 怎样共同决定回答、拒答、有限帮助或升级，risk 降低是否以某些群体 coverage 崩塌为代价？

![[00-知识库管理/_assets/figures/language-models/fig-lm-safety-refusal-risk-coverage-v1.svg|900]]

> [!figure] 图 LM-69　双阈值决策面、risk–coverage 与 over-refusal 切片
> **生成：**本库用合成请求分数绘制；标签不代表真实政策或用户群体。

**怎样读图**：左侧先按 safety risk 切拒答，再按 correctness confidence 切 abstain；中间同时读 risk 与 coverage；右侧比较组别 coverage/误拒，而不是只看总体。

**图没有证明什么**：二维 score 不能穷尽真实情境，validation 阈值也不能保证未知分布；低风险可能来自极低覆盖。

## 九、常见错误与出口标准

错误包括：不会与不允许混为一谈；拒答字符串即安全；只测 harmful prompts；全部拒答赢 benchmark；用 token probability 直接阈值；test 选阈值；不报 coverage；只报总体不报群体；升级无容量/SLO。

完成后应能构造多动作代价矩阵，手算 risk–coverage 与误拒率，设计 correctness/safety 双阈值，在独立 split 选阈值并报告群体 coverage、区间和升级成本。

## 十、来源与练习

- [[S-2017-Geifman-Selective-Classification]]；
- [[S-2022-Kadavath-Know-What-Know]]；
- [[S-2024-Rottger-XSTest]]；
- [[S-2024-Wang-Do-Not-Answer]]；
- [[S-2026-Muhamed-RefusalBench]]；
- [[习题 - Abstention、Refusal、Over-refusal 与风险覆盖]]；
- [[解答 - Abstention、Refusal、Over-refusal 与风险覆盖]]。

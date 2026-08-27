---
type: concept
status: verified
area: [language-models, deployment, monitoring, drift, incidents]
node_id: LM-71
aliases: [语言模型线上监控, LLM Incident]
prerequisites: ["[[Model、API、Tokenizer、Template 版本与复现合同]]", "[[Covariate、Label 与 Concept Shift]]"]
related: ["[[语言模型研究协议、Model-Data-System Card 与证据地图]]"]
sources: ["[[S-2009-Quinonero-Dataset-Shift]]", "[[S-2015-Sculley-Hidden-Technical-Debt]]", "[[S-2017-Breck-ML-Test-Score]]", "[[S-2020-Perdomo-Performative-Prediction]]", "[[S-2026-Google-SRE-Postmortem]]", "[[S-2023-NIST-AI-RMF]]"]
exercises: ["[[习题 - 线上监控、Drift、反馈回路与 Incident 记录]]"]
solutions: ["[[解答 - 线上监控、Drift、反馈回路与 Incident 记录]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-safety-monitoring-incident-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# 线上监控、Drift、反馈回路与 Incident 记录

> [!abstract] 一句话结论
> 线上监控不是把离线 accuracy 每小时再算一遍，而是监视输入、路由、检索、模型行为、工具后果、用户选择和版本共同形成的动态系统；告警必须连接 SLO、分母、负责人、回滚与 incident 证据，否则只是仪表盘装饰。

## 一、先写服务目标而非指标清单

一个 SLI 是测量，例如“安全策略漏放率”；SLO 是时间窗内目标，例如“7 天滚动上置信界不超过阈值”。写成

$$
\operatorname{SLI}_{w,g}
=\frac{\sum_{i\in(w,g)}\mathbf1[\text{bad event}_i]}
{\sum_{i\in(w,g)}\mathbf1[\text{eligible}_i]}.
$$

必须声明 window $w$、slice $g$、eligible 分母、延迟标签、失败/缺失和上置信界。平均 latency 正常不代表 p99 正常；总体安全率正常不代表高风险语言切片正常。

## 二、五层监控

1. **traffic/input**：语言、领域、长度、用户/来源、拒绝/截断；
2. **retrieval/tool**：hit、来源 freshness、citation、tool error/permission denial；
3. **model behavior**：answer/refuse/abstain、置信、格式、重复、policy events；
4. **system outcome**：任务完成、人工升级、状态变更、用户纠错；
5. **impact/reliability**：伤害事件、投诉、成本、latency、availability。

Token 分布漂移容易算，但不一定对应风险；真实伤害标签重要却稀疏且延迟。应组合 leading 与 lagging indicators。

## 三、Shift 的条件分解

训练/基线分布 $P_0(X,Y)$ 与线上 $P_t(X,Y)$ 可有：

- covariate shift：$P_t(X)\ne P_0(X)$；
- label/prior shift：$P_t(Y)\ne P_0(Y)$；
- concept shift：$P_t(Y\mid X)\ne P_0(Y\mid X)$；
- policy/measurement shift：标签定义或 judge 本身改变；
- system shift：model/template/retriever/tool/traffic routing 改变。

仅观察 $X$ 通常不能识别 concept shift。API 版本改变与用户分布改变同时发生时，更不能把输出漂移归因某一层。

## 四、简单 Drift 指标与盲区

离散分布总变差

$$
\operatorname{TV}(P,Q)
=\frac12\sum_j|p_j-q_j|.
$$

Population Stability Index

$$
\operatorname{PSI}(P,Q)
=\sum_j(p_j-q_j)\log\frac{p_j}{q_j}
$$

需平滑零 bin，且依分箱。Embedding 距离、分类器 two-sample test 或 MMD 也只是表示层差异。检测到 drift 不等于质量下降；未检测到也可能漏掉罕见高危 slice。阈值应由历史误报成本、风险和检测延迟决定。

## 五、反馈回路与选择偏差

部署策略 $\theta_t$ 改变用户和可观察数据：

$$
P_{t+1}(X,Y)=\mathcal D(\theta_t,P_t).
$$

例如系统拒答后没有答案正确标签；满意用户不反馈；推荐输出改变后续查询；人工只复核高风险样本。于是 observed labels 满足选择事件 $O=1$，而

$$
\Pr(Y\mid X,O=1)\ne\Pr(Y\mid X).
$$

需要随机审计样本、探索流量、反事实日志或可辩护的加权/因果设计，不能直接把用户点赞当总体正确率。

## 六、Canary rollout 与变更归因

新 bundle 先在小 cohort 上运行，按用户或组织稳定随机，避免同一会话跨版本污染。比较 paired/cluster outcomes、guardrail metrics 与 SLO。设硬门：

$$
\text{promote}=
\mathbf1[
\Delta Q_L>-\delta
\land U(R_{\rm safety})<r_0
\land U(L_{99})<\ell_0].
$$

若多个组件同时变，变更日志记录 bundle diff；紧急回滚优先恢复服务，不在事故中强求完整因果识别。

## 七、Incident 不是“坏例截图”

最小记录：

- impact：谁受影响、多少请求、严重度与不确定性；
- detection：首信号、为何现有控制未更早发现；
- timeline：发布、首坏事件、告警、缓解、恢复；
- trigger 与 contributing conditions；
- evidence：request IDs、版本、日志、重放与反事实；
- mitigation/rollback 与验证；
- action items：owner、期限、验收测试；
- communication、数据保留与主体通知。

Blameless 指从系统条件学习，不等于取消责任、证据或截止时间。“root cause”若无干预证据，应写成最有支持的机制假说。

## 八、图解：监控环、反馈环与事故时间线

**读图问题**：离线基线怎样进入线上 SLO，反馈选择又如何使仪表盘偏离真实总体，事故证据怎样闭环到下一版测试？

![[00-知识库管理/_assets/figures/language-models/fig-lm-safety-monitoring-incident-v1.svg|900]]

> [!figure] 图 LM-71　五层 SLI、反馈选择、告警—回滚—复盘闭环
> **生成：**本库依据 dataset shift、performative prediction 与 SRE postmortem 结构绘制。

**怎样读图**：上层从 traffic 到 impact 保留分母和版本；中部标出策略改变可观察标签；下部时间线把 first bad event、detect、mitigate、recover 与行动项验证连接起来。

**图没有证明什么**：相关时间线不自动识别根因；drift 指标稳定不保证 rare harm 为零，告警触发也不表示告警阈值最优。

## 九、常见错误与出口标准

错误包括：无 SLO 的 dashboard；只监 token 均值；坏请求从分母删除；点赞当真值；拒答样本无标签；变更无 cohort；告警无 owner/runbook；incident 只贴截图；回滚后不验证；行动项“加强测试”无验收。

完成后应能定义五层 SLI/SLO、手算 TV/PSI、画反馈选择因果图、设计 canary gate，并写含影响、时间线、证据、回滚与可验证行动项的 postmortem。

## 十、来源与练习

- [[S-2009-Quinonero-Dataset-Shift]]；
- [[S-2015-Sculley-Hidden-Technical-Debt]]；
- [[S-2017-Breck-ML-Test-Score]]；
- [[S-2020-Perdomo-Performative-Prediction]]；
- [[S-2026-Google-SRE-Postmortem]]；
- [[S-2023-NIST-AI-RMF]]；
- [[习题 - 线上监控、Drift、反馈回路与 Incident 记录]]；
- [[解答 - 线上监控、Drift、反馈回路与 Incident 记录]]。

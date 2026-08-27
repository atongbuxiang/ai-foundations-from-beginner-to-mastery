---
type: solution
status: verified
area: [language-models, deployment, monitoring, drift, incidents]
topic: "[[线上监控、Drift、反馈回路与 Incident 记录]]"
exercise: "[[习题 - 线上监控、Drift、反馈回路与 Incident 记录]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - 线上监控、Drift、反馈回路与 Incident 记录

## A. 识别与复述

### LM71-A01
SLI 是观测量及口径；SLO 是指定时间窗/切片的目标；alert 是证据越过触发条件后的操作信号；release gate 是上线前/晋级时的多指标决策规则。同一 SLI 可服务不同 SLO/alert，alert 触发不等于已识别根因。

### LM71-A02
例：traffic 为中文请求占比；RAG/tool 为来源 freshness 违规率；behavior 为 abstention/refusal rate；outcome 为经人工核验的任务完成率；impact 为严重安全事件率或受影响用户数。各层都需 eligible 分母、版本和 slice。

### LM71-A03
Covariate 是 $P(X)$ 变；label/prior 是 $P(Y)$ 变；concept 是 $P(Y\mid X)$ 变；measurement/policy 是标签定义、judge 或采集机制变；system shift 是 model/template/retriever/tool/routing 等执行对象变。它们可同时发生。

## B. 手算与构造

### LM71-B01
$$
\mathrm{TV}=\tfrac12(|.5-.4|+|.3-.35|+|.2-.25|)
=\tfrac12(.2)=.1.
$$

### LM71-B02
$$
(.5-.6)\log(.5/.6)+(.5-.4)\log(.5/.4)
\approx(-.1)(-.1823)+(.1)(.2231)=.04054.
$$

### LM71-B03
错误剔除 parser failure 时，分母 $1950$，SLI $=14/1950\approx.00718$。若 failure 预注册为坏事件，坏事件 $64$、分母 $2000$，SLI $=.032$。失败处理会改变结论，必须事前固定。

## C. 推导与证明

### LM71-C01
给相同 $P_t(X)$，可构造两世界：世界 A 的 $P_t(Y\mid X)=P_0(Y\mid X)$，世界 B 将某 slice 的标签概率反转。两世界边际输入完全相同但 concept 不同，因此仅从 $X$ 不可识别条件机制变化。

### LM71-C02
模型对低 confidence 输入拒答；只有被回答样本产生用户正确/错误反馈，于是观察事件 $O=1$ 依 score，也依潜在难度/错误 $Y$。故 $P(Y\mid X,O=1)$ 是被策略选择的容易子集，不代表所有请求。需随机人工审计部分拒答或探索流量。

### LM71-C03
逐请求随机使同一用户会话跨版本，前序回答改变后续输入，产生 interference 和体验混合；工具状态也可能交叉。按用户/组织稳定分配保持 cluster 一致，分析用 cluster unit，更接近完整系统 treatment。

## D. 边界、反例与纠错

### LM71-D01
大 drift、质量不降：节日导致请求主题改变，但模型在新主题同样准确。小 drift、高危上升：总体 token/embedding 几乎不变，仅极罕见高权限工具请求的授权检查失效，严重事件增加。平均距离对 rare severity 不敏感。

### LM71-D02
点赞者是选择样本；UI、提示请求点赞、回答长度、拒答策略和用户组成都可变。模型可能过滤掉不满用户使剩余点赞率上升。需固定采集、随机/加权审计、任务真值、版本 cohort 和负反馈缺失分析。

### LM71-D03
时间先后只支持关联。同期可能有流量、数据源、policy、工具或外部服务变化；坏例也可能早已存在但检测延迟。应做 bundle diff、日志/重放、cohort 对照和回滚再现；紧急时可先回滚而不宣称已证根因。

## E. AI 迁移

### LM71-E01
例一：7 天滚动、各语言 slice 的有效有引用答案中，人工支持失败率 95% 上界低于门；failure 计坏事件。例二：1 小时窗 write-tool 未授权执行为 0，eligible 为所有提案；任何事件立即 page security owner。例三：每日 p99 端到端 latency 低于 SLO 且人工升级队列 95% 等待低于容量门；owner 分别为 serving/on-call。

### LM71-E02
Alert 保存 snapshot 和 request IDs；确认指标/分母/监控本身；按 severity 限权、停 tool 或 rollback；保护用户和通知责任人；冻结日志、bundle、流量切片、依赖状态；用安全 replay 验证恢复；建立 incident channel/timeline；之后区分 trigger/contributors，行动项经 test 验收。

### LM71-E03
行动项示例：“平台 owner 在 2026-09-15 前让所有 write-tool 请求经过不可绕过的 scope check；验收为 CI 中 30 个 schema/identity/expiry 反例全部被拒、正常集完成率非劣于 -1%，staging 故障注入能触发告警/回滚；security reviewer 签字。”它关注控制缺口而不归咎个人，同时责任与完成证据明确。

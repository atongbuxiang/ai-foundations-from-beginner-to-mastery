---
type: concept
status: verified
area: [language-models, research-protocol, documentation, evidence, governance]
node_id: LM-72
aliases: [语言模型证据卡, Model Data System Card]
prerequisites: ["[[能力—行为—系统评估协议与证据地图]]", "[[线上监控、Drift、反馈回路与 Incident 记录]]"]
related: ["[[语言模型完整课程地图与掌握标准]]"]
sources: ["[[S-2019-Mitchell-Model-Cards]]", "[[S-2021-Gebru-Datasheets]]", "[[S-2022-Pushkarna-Data-Cards]]", "[[S-2013-W3C-PROV-DM]]", "[[S-2023-NIST-AI-RMF]]", "[[S-2024-NIST-GenAI-Profile]]", "[[S-2023-OpenAI-GPT4-System-Card]]", "[[S-2024-NIST-SSDF-GenAI]]"]
exercises: ["[[习题 - 语言模型研究协议、Model-Data-System Card 与证据地图]]"]
solutions: ["[[解答 - 语言模型研究协议、Model-Data-System Card 与证据地图]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-safety-evidence-card-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# 语言模型研究协议、Model-Data-System Card 与证据地图

> [!abstract] 一句话结论
> 一项可信结论应是“主张—适用域—测量—工件—责任—版本”的可追溯图，而不是一张漂亮的 Model Card；Model、Data 与 System Card 分别记录对象，研究协议预注册比较，PROV 连接血缘，线上 SLO/incident 再检验部署中的剩余风险。

## 一、Card 不是结论本身

文档有三种常被混淆的功能：

1. **description**：对象是什么、如何产生；
2. **evidence index**：哪些实验支持哪些主张；
3. **governance interface**：谁批准、谁监控、何时失效。

Card 写得完整只能提高透明度；若原始输出缺失、样本不代表、judge 有偏或线上版本已变，它不会把弱证据变强。

## 二、Model、Data、System 三种对象

| Card | 核心对象 | 最小问题 |
|---|---|---|
| Model | weights/tokenizer/template/adapter | intended use、训练目标、能力/限制、切片、版本 |
| Data | raw/processed/tokenized corpus | 来源、许可、主体、采集、清洗、dedup、删除、维护 |
| System | model + prompt + RAG + tools + policy + humans | 数据流、权限、SLO、threat model、监控、incident |

同一模型进入不同工具系统会有不同安全边界；同一数据集经不同 tokenizer/filters 也不是同一训练对象。

## 三、研究主张的标准形

把主张写为

$$
C=(O,I,P,M,\Delta,U,V),
$$

其中 $O$ 是对象，$I$ 是干预/比较，$P$ 是目标总体，$M$ 是测量协议，$\Delta$ 是 effect/threshold，$U$ 是不确定性，$V$ 是有效版本/时段。

例：“在中文客服请求总体、固定模板和工具权限下，候选 bundle 相对基线的任务完成率非劣于 $-2\%$，且高危漏放率 95% 上界低于门限。”这比“新模型更安全更好”可证伪得多。

## 四、最小预注册协议

1. research question、estimand 与决策；
2. treatment/control bundle 与唯一差异；
3. population、sampling/cluster unit、inclusion/exclusion；
4. data/time cutoff、privacy 与许可；
5. prompt/decoder/retrieval/tool/judge；
6. primary/secondary metrics、failure denominator；
7. sample size、seeds、CI、multiplicity；
8. attack model、预算、自适应性与 stop；
9. safety/privacy/latency/cost hard gates；
10. artifact schema、复现命令、保留/访问规则；
11. exploratory 与 confirmatory 分离；
12. owner、reviewer、有效期与失效触发。

## 五、证据图与 PROV

用 Entity–Activity–Agent 表示：

- Entity：数据 snapshot、prompt、token IDs、checkpoint、raw output、score、card；
- Activity：过滤、训练、生成、评分、部署、回滚；
- Agent：作者、服务、reviewer、组织。

一条主张边应能反向追到 per-unit raw data：

$$
\text{claim}
\leftarrow\text{estimate/CI}
\leftarrow\text{scores}
\leftarrow\text{raw traces}
\leftarrow\text{versioned bundle/data}.
$$

只保存 PDF 表格会使重新评分、改 judge、failure analysis 和删除请求无法执行。

## 六、证据强度与更新

对每个 claim 记录：

- supporting、contradicting、unknown evidence；
- internal demo、benchmark、independent replication、online evidence；
- 适用模型/版本/人群/语言/时间；
- 已知混杂、选择、测量误差；
- 最近复核日与 invalidation triggers；
- owner 和下一实验。

新模型、template、policy、retriever corpus、tool permission、judge 或目标总体变化都可触发失效。旧 Card 保留，不静默改写历史。

## 七、Govern–Map–Measure–Manage 接口

- **Govern**：角色、审批、风险容忍、审计与文档；
- **Map**：用途、主体、系统边界、资产、威胁和影响；
- **Measure**：benchmark、red team、隐私、校准、SLO 与不确定性；
- **Manage**：优先级、控制、发布、监控、事件与退出。

这四类不是线性打勾，而是版本闭环。NIST Profile 可补充风险条目，但每个控制仍需本系统证据。

## 八、图解：从主张到 Model–Data–System 证据闭环

**读图问题**：一个发布主张怎样回溯到数据、模型、系统和原始运行，又怎样被线上 drift 或 incident 反向更新？

![[00-知识库管理/_assets/figures/language-models/fig-lm-safety-evidence-card-v1.svg|900]]

> [!figure] 图 LM-72　Claim ledger、PROV 血缘、三类 Card 与治理环
> **生成：**本库综合 Model Cards、Datasheets/Data Cards、PROV 与 AI RMF 绘制；卡片字段为课程最小合同。

**怎样读图**：中心 claim 连接适用域、估计/区间、raw artifacts 和 owner；上方分开 Model/Data/System 三类对象；下方让上线 SLO 与 incident 回写证据状态和下一版实验。

**图没有证明什么**：血缘图完整不保证输入真实、实验无偏或控制有效；标准映射也不是认证。

## 九、卷终出口标准

错误包括：Card 当宣传；模型卡替代系统卡；来源只列 URL；没有 raw outputs；安全结果无 threat model；负结果不记录；厂商报告当独立复现；版本变了不失效；action 无 owner。

完成后应能写一条可证伪 claim，构造 Model/Data/System 三卡，画 PROV 证据图，把研究预注册、release gate、线上 SLO、incident 与下一版复验连接起来，并明确未知和剩余风险。

## 十、来源与练习

- [[S-2019-Mitchell-Model-Cards]]；
- [[S-2021-Gebru-Datasheets]]；
- [[S-2022-Pushkarna-Data-Cards]]；
- [[S-2013-W3C-PROV-DM]]；
- [[S-2023-NIST-AI-RMF]]；
- [[S-2024-NIST-GenAI-Profile]]；
- [[S-2023-OpenAI-GPT4-System-Card]]；
- [[S-2024-NIST-SSDF-GenAI]]；
- [[习题 - 语言模型研究协议、Model-Data-System Card 与证据地图]]；
- [[解答 - 语言模型研究协议、Model-Data-System Card 与证据地图]]。

---
type: solution
status: verified
area: [language-models, research-protocol, documentation, evidence]
topic: "[[语言模型研究协议、Model-Data-System Card 与证据地图]]"
exercise: "[[习题 - 语言模型研究协议、Model-Data-System Card 与证据地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - 语言模型研究协议、Model-Data-System Card 与证据地图

## A. 识别与复述

### LM72-A01
Description 记录对象/产生方式；evidence index 把每条主张链接到实验、raw artifact 与限制；governance interface 指定 owner、审批、有效期、SLO、事件和更新责任。三者合一仍不等于证据有效。

### LM72-A02
Model Card 面向权重、tokenizer、template/adapter 的用途、性能与限制；Data Card 面向数据来源、主体、许可、处理、删除与维护；System Card 面向模型加 prompt、RAG、tools、policy、humans 后的权限、threat model、SLO 和 incident。

### LM72-A03
Entity 是可标识产物，如 corpus snapshot/checkpoint/raw output；Activity 是产生/使用实体的过程，如过滤、训练、生成、评分；Agent 是负责人或服务，如数据团队、训练 job、reviewer。PROV 关系记录由谁经何活动使用/生成何实体。

## B. 手算与构造

### LM72-B01
示例：“对 2026-Q3 中文客服请求总体，在固定 tool scopes、template t7 和同一 1000 用户 cluster test 上，bundle v18 相对 v17 的任务完成率差值 95% CI 下界高于 -2%，且严重未授权动作率的 95% 上界低于 0.1%；结论仅适用于这两个 bundle 与评估时段。”它可被数据否证。

### LM72-B02
Claim 行：claim_id、文字、适用域、threshold、version。Estimate 行：estimand、point、CI、unit、method。Scores 行：per-unit URI、metric/judge version、failure。Raw 行：request/output/tool/source hashes 与 access。Bundle/data 行：manifest IDs、content hashes、PROV parents、许可/时间。每行还带 owner/timestamp。

### LM72-B03
表面完成率 $=16/20=80\%$。有效 artifact 为 $16-2=14$，有效链接完成率 $=14/20=70\%$。若失效字段是关键 hard gate，即使 70% 也可能整体不可发布，不能只看比例。

## C. 推导与证明

### LM72-C01
字段可以完整但内容虚假、样本偏、指标无效、攻击预算不足、链接指向错误 artifact 或控制未执行。完整性只提高可检查性；安全还要求对目标 threat model 的有效测量、实现验证和线上证据。

### LM72-C02
Template 改变 role 序列化、special tokens、上下文长度和模型行为，因此对象从 $F(W,T,C_0,\ldots)$ 变为 $F(W,T,C_1,\ldots)$。旧 claim 的 treatment、指标分布和安全边界不再相同；weights 不变不足以保持系统等价。

### LM72-C03
若实验结果 $E$ 只有在支持 claim 时才进入 card，条件分布 $P(E\mid\text{published})$ 向有利结果偏，而读者观察不到失败运行和选择次数，效应被高估、区间失真。需预注册 primary、保存全部 runs/negative/contradicting evidence。

## D. 边界、反例与纠错

### LM72-D01
官方文件是发布方的一手自述，能准确说明其流程/声明，却可能缺少数据、受商业限制且未由独立团队复验。证据层应标 vendor official example，并把复现、外部审计和线上证据分开。

### LM72-D02
Model Card 正确描述 text-only 模型及限制；部署却给它自动支付工具和长期 credential，没有 reference monitor。模型层陈述仍真，但 System Card 若声称低 blast radius 就错，因为权限边界和动作后果改变。

### LM72-D03
无法证明某时点发布者看到了什么、复现旧决策、关联 incident 到受影响版本、审计 claim 演化、执行旧数据删除/许可追踪，也无法识别字段被事后改写。应 immutable version + supersedes link。

## E. AI 迁移

### LM72-E01
Model：identity/weights/tokenizer/template/adapter、objective、intended/forbidden use、quality/safety/privacy slices、limits。Data：sources/license/subjects/time、parse/filter/dedup/mix/tokenize、provenance/delete/maintenance。System：architecture/dataflow/trust/permissions、prompt/RAG/tools/humans、threat model、eval/gates、SLO/monitoring/incident/rollback、owners/expiry。

### LM72-E02
Govern：指定 owner、reviewer、风险容忍和记录；Map：画用途、主体、资产、数据流、威胁；Measure：预注册 quality/safety/privacy/latency、红队和 CI；Manage：按 gates 决定 canary、控制/剩余风险、监控/rollback/incident。线上事件回到 Map/Measure，不是一次线性打勾。

### LM72-E03
条目含 claim_id/可证伪文字；对象 bundle、总体、版本/时段；supporting artifacts 与 effect/CI；contradicting runs；unknown slices/assumptions；decision 与 residual risk；owner/reviewer；expiry；invalidation triggers（model/template/policy/tool/data/judge/traffic 变化或 incident）；next test、status 与 immutable history。

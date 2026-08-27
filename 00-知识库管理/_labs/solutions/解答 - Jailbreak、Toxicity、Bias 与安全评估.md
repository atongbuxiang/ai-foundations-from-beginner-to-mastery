---
type: solution
status: verified
area: [language-models, safety, jailbreak, bias, red-teaming]
topic: "[[Jailbreak、Toxicity、Bias 与安全评估]]"
exercise: "[[习题 - Jailbreak、Toxicity、Bias 与安全评估]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Jailbreak、Toxicity、Bias 与安全评估

## A. 识别与复述

### LM68-A01
Policy violation 是相对某版规则的标签；content property 描述文本属性如毒性/偏见；system action 是工具、发送或状态改变；realized harm 还结合主体、暴露、严重度与情境。前两者是测量代理，不能自动等同后果。

### LM68-A02
至少写模型/模板/policy 版本；攻击者知识与可控输入；查询/迭代/token/人工预算；成功 oracle 与人评规则；工具权限和实际后果。还应写语言/总体、sampler、prompt family cluster 与时间。

### LM68-A03
分类器概率是其训练标签和分布下的输出，受阈值、语境、引用、方言、身份词和语言影响；真实伤害还依受众、用途、传播和动作能力。除非对明确 harm event 在目标总体独立校准，否则两者不是同一概率。

## B. 手算与构造

### LM68-B01
Harmful recall $=102/120=.85$；unsafe answer rate $=18/120=.15$。Benign utility $=(300-42)/300=.86$；over-refusal $=42/300=.14$。

### LM68-B02
Query-micro ASR $=(1+4+10)/(5+20+100)=15/125=.12$。Family-macro 先算 $.2,.2,.1$，再平均为 $1/6\approx.1667$。变体多的第三族在 micro 中权重更大。

### LM68-B03
用抽象 group A/B × ambiguous/disambiguated：歧义时检查无证据是否偏向某组或能否表达未知；消歧时检查有证据的任务准确率。再对 target/non-target 方向成对，防止总体准确掩盖偏差方向。抽象设计不需复述任何伤害文本。

## C. 推导与证明

### LM68-C01
同族变体共享 base intent、生成策略和模型薄弱点，错误相关。把 $m$ 个变体当 iid 会把标准误错误缩为约 $1/\sqrt m$；有效独立单位更接近 family。可按 family cluster bootstrap，并同时报每 query 和每 family 至少一次成功。

### LM68-C02
Harmful recall 只在 harmful 分母上奖励拒答。策略“对所有请求拒答”使每个 harmful 请求均拒答，因此 recall=1，达到最大；该目标没有 benign utility 约束，所以不能排除无用解。

### LM68-C03
每 prompt 生成 $k$ 个，mean toxicity 估计随机一次生成的平均属性；max 或“至少一次越阈值”估计攻击者/用户从多次采样中遇到极端输出的风险。$k$ 增大时 max 自然上升，两者不能直接比较且必须写 sampler/budget。

## D. 边界、反例与纠错

### LM68-D01
低 toxicity、高 harm：礼貌而自信地给出关键事实错误并触发高风险决定。高 toxicity score、低 harm：研究者在受控环境引用一句带身份词的攻击样本并明确批判它，分类器因关键词高分。语境和后果不能由词面单独决定。

### LM68-D02
99% 绑定固定数据、已知攻击、某语言、某 judge、某 policy 和查询预算；可能有 contamination、over-refusal、rare severe failure、工具权限变化和自适应攻击。上线还需 benign utility、群体切片、攻击迁移、SLO、canary、回滚和 incident 响应。

### LM68-D03
内容层可记“文本拒答”，但系统动作层必须记“执行成功”，若动作未授权则安全事件失败。最终后果不能由自然语言外观覆盖；参考监视器应在执行前阻断，日志表明控制顺序存在缺陷。

## E. AI 迁移

### LM68-E01
矩阵轴：语言/方言 × harm category/severity × direct/obfuscated/multi-turn/indirect × text-only/read-tool/write-tool × novice/expert-adaptive × single/repeated budget。每格写 eligible 分母、prompt-family 数、success oracle、人工锚点、ASR、benign paired utility、CI 与版本；空格显式标 gap。

### LM68-E02
随机抽各类别、严重度、语言和边界样本，由两名盲评者按固定 rubric 独立标注并仲裁；隐藏系统名和版本，随机 answer/order；judge 做 AB/BA 或标签顺序交换，报告 flip、tie、parse failure、与人类一致率和每 slice confusion matrix。人类分歧保留，不强行制造单真值。

### LM68-E03
冻结 v0 防御和攻击可见信息；固定回归集只做一次；adaptive 队伍在预注册预算寻找新失败；独立判定并建攻击族；更新防御为 v1，同时锁定 benign set；用旧攻击迁移、新攻击 held-out、群体和工具后果比较；发布前做 canary/rollback gate；新发现进入 v2 数据，所有版本保留。

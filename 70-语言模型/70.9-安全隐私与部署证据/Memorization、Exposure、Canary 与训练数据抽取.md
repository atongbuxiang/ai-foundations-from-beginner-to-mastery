---
type: concept
status: verified
area: [language-models, privacy, memorization, extraction]
node_id: LM-65
aliases: [语言模型记忆与抽取, Canary Exposure]
prerequisites: ["[[预训练语料来源、许可、隐私与文档单位合同]]", "[[Contamination、Prompt Sensitivity、Robustness 与不确定性]]"]
related: ["[[Membership、隐私攻击、数据删除与 Unlearning 边界]]"]
sources: ["[[S-2019-Carlini-Secret-Sharer]]", "[[S-2021-Carlini-Training-Data-Extraction]]", "[[S-2023-Carlini-Quantifying-Memorization]]", "[[S-2023-Nasr-Scalable-Extraction]]"]
exercises: ["[[习题 - Memorization、Exposure、Canary 与训练数据抽取]]"]
solutions: ["[[解答 - Memorization、Exposure、Canary 与训练数据抽取]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-safety-memorization-exposure-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Memorization、Exposure、Canary 与训练数据抽取

> [!abstract] 一句话结论
> “训练过”“模型偏好”“逐字记住”“能被攻击者抽取”和“造成隐私伤害”是五个不同事件；Exposure 用受控候选空间中的排序测稀有 canary 是否异常可猜，但真实风险还必须乘上访问能力、查询预算、核验规则、敏感性和主体影响。

## 一、初学者入口：模型为什么会复现训练文本

语言模型通过降低训练 token 的负对数似然学习规律。常见短语被赋予较高概率可能是合理泛化；一条只出现过几次的长随机串若也被高概率复现，更像实例级记忆。二者没有天然清晰的单阈值边界，因为“罕见”取决于参考总体、tokenizer、上下文和匹配规则。

先区分五个事件：

1. **inclusion**：记录确实进入某版训练数据；
2. **influence/memorization**：加入它改变了模型对它或邻域的行为；
3. **verbatim reproduction**：输出与记录满足预先声明的逐字或近似匹配；
4. **extractability**：规定攻击者在预算内找得到它；
5. **harm**：输出泄露了受保护信息并对主体造成影响。

它们通常相关，却没有逻辑等价。例如知道一段公开诗句不构成训练数据成员证明；模型内部受一条记录影响也可能无法从黑盒接口抽取。

## 二、Canary：用合成秘密建立已知真值

Canary 是训练前人工构造并插入的合成字符串。安全实验必须满足：

- 不是真实密码、邮箱、电话或身份证；
- 从已知随机分布 $\mathcal R$ 生成；
- 记录插入次数、位置、上下文模板与去重过程；
- 留有同分布但未插入的 control；
- 预注册攻击可见的前缀和候选空间。

若 canary 为“代号是 483-917”，且六位数字均可能，则候选空间大小可以是 $|\mathcal R|=10^6$。若实验者事后只保留容易猜中的一小组，Exposure 的分母已被污染。

## 三、Rank 与 Exposure 的推导

给定上下文 $x$，对每个候选 $r\in\mathcal R$ 定义模型损失

$$
\ell(r)=-\log P_\theta(r\mid x).
$$

按损失从小到大排序，canary $r^\star$ 的秩为

$$
\operatorname{rank}(r^\star)
=1+\sum_{r\ne r^\star}\mathbf 1[\ell(r)<\ell(r^\star)],
$$

并声明 tie 规则。Exposure 定义为

$$
\operatorname{exposure}(r^\star)
=\log_2|\mathcal R|-\log_2\operatorname{rank}(r^\star)
=\log_2\frac{|\mathcal R|}{\operatorname{rank}(r^\star)}.
$$

直觉上，随机顺序中平均要搜索约整个空间；若 canary 排第 $2^{10}$、空间为 $2^{30}$，exposure 为 $20$ bits，表示排序把穷举规模从约 $2^{30}$ 缩到约 $2^{10}$。这不是“泄露了 20 位真实秘密”的通用定理；它是该候选空间、该 scoring oracle 下的排序压缩。

## 四、从 Exposure 到可抽取性

实际攻击者未必能枚举并读取精确 token likelihood。把攻击写为算法 $A$：

$$
\Pr\!\left[A^{\mathcal O_\theta}(x;B,K)\in M(z)\right],
$$

其中 $\mathcal O_\theta$ 是接口，$B$ 是查询/计算预算，$K$ 是先验知识，$M(z)$ 是预注册匹配集合。完整报告至少要给：

- 白盒 logits、top-$k$ logits 或仅文本黑盒；
- 前缀是否已知，能否多轮适应；
- 生成条数、重排成本、去重与停止规则；
- exact、normalized、substring 或语义匹配；
- 候选如何确认来自训练而非公开常识；
- 每个成功的敏感性与人工复核流程。

“采样 100 万条后找到一条”与“一次正常请求即复现”是完全不同风险。

## 五、记忆率不是一个模型常数

经验上，重复、模型容量、训练轮数、上下文长度和样本稀有度都可影响逐字记忆。可写条件风险

$$
m(k,L,d)=
\Pr(\text{match}\mid
\text{repeat}=k,\ \text{prefix length}=L,\ \text{domain}=d).
$$

只报总体 $\bar m$ 会掩盖高重复个人记录切片。比较两模型时还要控制 tokenizer、训练 token、数据版本、dedup 和攻击预算；更大模型同时用了不同数据时，不能把差异全归因于参数量。

## 六、测量误差与替代解释

逐字重合可能来自：训练语料、后训练数据、RAG、工具返回、系统提示、用户上下文或公开网页。应做 source ablation 和时间核验。相反，未抽取到也可能因为：

- 未知正确前缀；
- API 截断 logits 或安全过滤；
- 搜索预算太小；
- 样本存在但 tokenizer/格式不同；
- 模型记忆为特征影响而非逐字序列。

所以“无成功抽取”只给给定协议下的上界证据。

## 七、防御与治理闭环

1. 数据入口：许可/隐私审查、敏感检测、dedup、主体请求；
2. 训练：最小必要数据、访问控制、受控 canary audit；
3. 模型：必要时研究正则、隐私训练或重训，但逐项验证效用；
4. 服务：输出过滤、速率限制、异常批量采样监控；
5. 响应：定位数据与模型 lineage，禁用受影响版本，评估删除/重训；
6. 证据：保存 canary manifest、攻击预算、负结果、版本和置信区间。

过滤器不是隐私证明，速率限制也不消除单次高危复现。

## 八、图解：从训练包含到隐私伤害

**读图问题**：Canary rank 怎样变成 exposure，而 exposure 为什么仍必须经过接口、预算、核验与伤害四道门才形成部署结论？

![[00-知识库管理/_assets/figures/language-models/fig-lm-safety-memorization-exposure-v1.svg|900]]

> [!figure] 图 LM-65　候选排序、Exposure bits 与风险漏斗
> **生成：**本库依据 canary/exposure 定义绘制合成候选；数值不来自真实模型，不包含真实秘密。

**怎样读图**：左侧比较插入 canary 与未插入 control 的损失秩；中间把 rank 映射为搜索空间压缩；右侧逐层检查攻击接口、预算、匹配核验和主体伤害，任一层缺失都不能称为完整隐私泄露证据。

**图没有证明什么**：高 exposure 不保证黑盒抽取，低 exposure 不保证无其他提示可泄露；玩具候选空间也不估计真实个人数据的基率。

## 九、常见错误与出口标准

常见错误：把公开复述当训练成员证明；不写候选空间；把 loss 当攻击成功；只报最好 canary；事后改匹配规则；忽略查询成本；把未抽取写成安全；把污染检测与隐私攻击混为一谈。

完成后应能手算 rank/exposure，设计 inserted/control canary 实验，写清黑白盒访问、预算与匹配规则，并对“记忆—抽取—伤害”给出分层结论。

## 十、来源与练习

- [[S-2019-Carlini-Secret-Sharer]]；
- [[S-2021-Carlini-Training-Data-Extraction]]；
- [[S-2023-Carlini-Quantifying-Memorization]]；
- [[S-2023-Nasr-Scalable-Extraction]]；
- [[习题 - Memorization、Exposure、Canary 与训练数据抽取]]；
- [[解答 - Memorization、Exposure、Canary 与训练数据抽取]]。

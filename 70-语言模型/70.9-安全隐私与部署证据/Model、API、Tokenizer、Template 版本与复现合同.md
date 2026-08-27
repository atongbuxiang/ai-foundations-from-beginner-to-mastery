---
type: concept
status: verified
area: [language-models, reproducibility, versioning, deployment]
node_id: LM-70
aliases: [语言模型版本合同, API 复现合同]
prerequisites: ["[[指令、消息、Chat Template 与任务序列化合同]]", "[[能力—行为—系统评估协议与证据地图]]"]
related: ["[[线上监控、Drift、反馈回路与 Incident 记录]]", "[[语言模型研究协议、Model-Data-System Card 与证据地图]]"]
sources: ["[[S-2026-HuggingFace-Chat-Templates]]", "[[S-2026-HuggingFace-Tokenizer-Special-Tokens]]", "[[S-2026-PyTorch-Reproducibility]]", "[[S-2021-Pineau-ML-Reproducibility]]"]
exercises: ["[[习题 - Model、API、Tokenizer、Template 版本与复现合同]]"]
solutions: ["[[解答 - Model、API、Tokenizer、Template 版本与复现合同]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-safety-version-contract-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Model、API、Tokenizer、Template 版本与复现合同

> [!abstract] 一句话结论
> “模型名相同”不是同一实验对象；可复现的语言模型运行由权重、tokenizer、chat template、系统/开发者提示、decoder、API 语义、retriever/tools、policy、judge、环境和时间共同决定，任何不可固定组件都应被当作随机/漂移因素而非隐藏常量。

## 一、输出是配置束的函数

把一次运行写为

$$
y=F(
W,T,C,P,D,R,G,J,E,t,\xi),
$$

其中：

- $W$：权重 snapshot/adapter/quantization；
- $T$：tokenizer vocab、normalizer、special tokens；
- $C$：chat template 与 role 序列化；
- $P$：system/developer/user prompt 与 policy；
- $D$：decoder、seed、sample budget、stop；
- $R$：retriever、corpus、index、reranker；
- $G$：tools、schema、权限与依赖服务；
- $J$：parser、metric、judge；
- $E$：代码、框架、驱动、硬件、区域；
- $t$：时间与外部世界 snapshot；
- $\xi$：未控随机性/并发。

只写“用了某某模型”相当于在方程中省略大多数自变量。

## 二、Tokenizer 与 Template 是可执行语义

同一 messages 经不同 template 会产生不同 token IDs：

$$
z=\operatorname{Tokenize}_T(
\operatorname{Render}_C(m_{1:k})).
$$

是否添加 generation prompt、是否继续 final message、special token 是否重复、system role 如何回退，都可能改变概率分布。最小工件包括：

- tokenizer 仓库 revision 与文件哈希；
- chat template 原文/哈希；
- special-token map；
- render 后字符串；
- token IDs 与 attention/loss masks；
- tokenize 参数和库版本。

“文本看起来相同”不保证 token 序列相同。

## 三、Model 版本不只是 checkpoint 文件

记录 base weights、adapter 顺序、merge 状态、量化算法/校准集、context 配置、rope scaling、generation config 和安全 head。内容寻址可定义 bundle 指纹

$$
h_{\rm run}
=H(h_W\Vert h_T\Vert h_C\Vert h_P\Vert h_D
\Vert h_R\Vert h_G\Vert h_J\Vert h_E).
$$

哈希证明字节身份，不证明文件正确、安全或来源可信；还需签名、权限和 provenance。

## 四、API 的“版本”可能不可见

托管 API 可能在同一公开名字下更新权重、路由、过滤器、系统层、量化或区域基础设施。应尽量保存：

- provider、endpoint、显式 snapshot/version；
- request/response ID、timestamp、region；
- 完整允许保存的 request 参数与响应字段；
- usage、finish reason、tool calls、safety labels；
- 多次重复 probe 的分布；
- provider changelog/状态页快照。

若无法固定，就诚实声明“按某时段服务分布复验”，不能承诺 bitwise replay。

## 五、四级复现

| 级 | 目标 |
|---|---|
| R0 工件复算 | 从保存 raw outputs 重新计算指标 |
| R1 同栈重放 | 同代码/权重/环境重跑，容许声明的数值差 |
| R2 独立重实现 | 依据协议另写实现得到统计相容结果 |
| R3 外部复验 | 新环境/模型版本/数据时段检验结论迁移 |

Bitwise equality 最强但常非必要；任务结论复现更重要，却需预先声明容差、效应阈值和统计单位。相反，只复算同一 CSV 不能验证生成系统。

## 六、确定性、容差与随机性

固定 seed 只控制已接入该 RNG 的随机源。并发 batch、GPU kernel、低精度、collective 顺序、外部检索和 API 路由仍可能变化。为连续指标定义容差，例如

$$
|\hat\theta_{\rm replay}-\hat\theta_{\rm original}|
\le\epsilon_{\rm numeric}
$$

或比较效应区间/排序。生成文本不宜只做逐字相等，可保存 token trace，并按预注册任务事件统计。

## 七、变更检测与 Release Gate

每次候选版本与基线做：

1. bundle manifest diff；
2. tokenizer/template golden tests；
3. deterministic toy probes；
4. paired quality/safety/privacy/latency suite；
5. canary cohort 与 rollback；
6. 线上 SLO/incident guard；
7. 新证据卡与旧版本可访问性审计。

一次只改一个组件最好；若供应商一次改变多个隐藏组件，结论应写为“service bundle 变化”，不要虚构模型权重因果。

## 八、图解：从消息到线上输出的版本 DAG

**读图问题**：一个聊天回答沿哪些版本化实体生成，哪一层变化会使旧结论失效？

![[00-知识库管理/_assets/figures/language-models/fig-lm-safety-version-contract-v1.svg|900]]

> [!figure] 图 LM-70　消息序列化、模型系统 bundle 与内容寻址 DAG
> **生成：**本库按 Hugging Face 模板合同、框架复现边界和实验 provenance 绘制。

**怎样读图**：沿 messages→rendered text→token IDs→model/sampler→tool/system→score 保存每个实体哈希；红色变更边触发受影响测试，而不是无差别全量或完全不测。

**图没有证明什么**：哈希完整不代表依赖可信；API 内部组件不可见时，DAG 只能记录可观察合同和时间窗口。

## 九、常见错误与出口标准

错误包括：只写模型家族；latest 当版本；不存 template；文本相同即 token 相同；只存聚合分；seed 等于确定性；升级 tokenizer 不重测；API 漂移归因权重；无法重放却称完全复现。

完成后应能列出运行 bundle、生成内容指纹、设计 golden serialization test、区分四级复现，并为 API 隐藏漂移写可观察 probe 与结论边界。

## 十、来源与练习

- [[S-2026-HuggingFace-Chat-Templates]]；
- [[S-2026-HuggingFace-Tokenizer-Special-Tokens]]；
- [[S-2026-PyTorch-Reproducibility]]；
- [[S-2021-Pineau-ML-Reproducibility]]；
- [[习题 - Model、API、Tokenizer、Template 版本与复现合同]]；
- [[解答 - Model、API、Tokenizer、Template 版本与复现合同]]。

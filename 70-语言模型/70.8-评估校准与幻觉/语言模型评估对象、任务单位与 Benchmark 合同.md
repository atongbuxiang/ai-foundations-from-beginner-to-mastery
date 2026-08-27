---
type: concept
status: verified
area: [language-models, evaluation, benchmarks]
node_id: LM-57
aliases: [语言模型评估对象, Benchmark 合同]
prerequisites: ["[[70.7 解码推理服务与加速 MOC]]", "[[数据版本、Provenance、有效 Token 与证据地图]]"]
related: ["[[Contamination、Prompt Sensitivity、Robustness 与不确定性]]", "[[能力—行为—系统评估协议与证据地图]]"]
sources: ["[[S-2023-Liang-HELM]]", "[[S-2024-Hsieh-RULER]]", "[[S-2024-Sclar-Prompt-Sensitivity]]"]
exercises: ["[[习题 - 语言模型评估对象、任务单位与 Benchmark 合同]]"]
solutions: ["[[解答 - 语言模型评估对象、任务单位与 Benchmark 合同]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-eval-estimand-pipeline-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# 语言模型评估对象、任务单位与 Benchmark 合同

> [!abstract] 一句话结论
> 分数之前先写 estimand：对哪个总体、哪个模型—解码器—系统对象、在哪种 prompt/工具/负载下，以什么采样单位和失败规则求什么期望。Benchmark 文件名不是 estimand，排行榜单元格也不是模型的固有常数。

## 一、把问题写成期望

设任务单元 $U\sim P^\star$，配置 $c$ 包含 checkpoint、prompt/template、decoder、retriever/tools 与 server，输出 $Y\sim q_c(\cdot\mid U)$，评分为 $m(U,Y)$。一个基本 estimand 是

$$
\theta(c)=\mathbb E_{U\sim P^\star}
\mathbb E_{Y\sim q_c(\cdot\mid U)}[m(U,Y)].
$$

这句话包含四个决定：

1. **目标总体** $P^\star$：未来用户、某领域题目、某语言，还是公开 test split；
2. **被评对象** $c$：raw model、固定 decoder、RAG/tool 系统或在线产品；
3. **随机性**：每题一次确定性输出，还是对 sampler 的多次期望；
4. **效用** $m$：正确、偏好、风险、成本或多指标向量。

若只在有限 benchmark $u_1,\ldots,u_n$ 上评一次，

$$
\hat\theta=\frac1n\sum_{i=1}^nm(u_i,y_i)
$$

只是特定样本、特定运行对目标期望的估计。它同时含有限题目误差和生成随机误差。

## 二、四种常被混写的对象

| 对象 | 固定什么 | 可变什么 | 典型问题 |
|---|---|---|---|
| 条件模型分布 | checkpoint/tokenizer/history | next-token 随机变量 | logits/NLL 是否正确 |
| 解码行为 | 模型、prompt、processors/sampler | seed/sample | 该 decoder 的期望任务质量 |
| 工具系统 | 模型+decoder+retriever/tools | 外部状态、调用轨迹 | 端到端成功与最早失败层 |
| 在线产品 | 全系统版本 | 用户、时间、负载、反馈 | 实际 SLO、风险和效用 |

“模型 A 得 80 分”若没有说明是哪一层，无法复现。工具更新可在不改模型的情况下改变系统分数；temperature 改动也可在 checkpoint 不变时改变行为。

## 三、sampling unit 决定分母

任务可能按 token、claim、answer、question、document、conversation、user 或 request 计数。若一个用户贡献 100 个请求，另一个只贡献 1 个，把 101 请求当独立样本会让前者支配均值并低估相关性。

设 user $g$ 有 $n_g$ 个请求：

$$
\hat\theta_{\rm request}
=\frac{\sum_g\sum_{i=1}^{n_g}m_{gi}}{\sum_g n_g},
\qquad
\hat\theta_{\rm user}
=\frac1G\sum_g\frac1{n_g}\sum_i m_{gi}.
$$

两者回答不同问题。前者是随机请求平均，后者是随机用户平均。必须预先选择；标准误也要按独立 cluster 重采样，而非把同用户请求当 iid。

## 四、macro、micro 与 strata

Macro 先算每任务/语言/类别分数再等权平均；micro 把所有基本事件合并后再算。类别大小不同时二者不同。

若任务 $j$ 有 $n_j$ 个二元事件和正确数 $c_j$：

$$
\operatorname{Macro}=\frac1J\sum_j\frac{c_j}{n_j},
\qquad
\operatorname{Micro}=\frac{\sum_jc_j}{\sum_jn_j}.
$$

Macro 给每任务同权，micro 给每事件同权。不能挑分数较高的一种而不披露。还应报告语言、长度、领域、时间、难度、安全群体等预注册 slices；slice 太多则要控制多重比较与小样本不确定性。

## 五、失败与缺失不是清洗噪声

Parser error、timeout、refusal、empty output、tool error、OOM 与内容违规都可能是被评系统行为。若从分母删除，得到的是

$$
\mathbb E[m\mid \text{run succeeded}],
$$

而不是所有请求上的 $\mathbb E[m]$。至少同时报告：

- 总到达/总题数；
- 各 finish/failure reason；
- missingness 是否与难题、长度、群体有关；
- 主分析中失败记零、单列或 censor 的预注册规则；
- sensitivity analysis。

## 六、Benchmark manifest

一个可复现 benchmark 运行至少包含：

| 层 | 字段 |
|---|---|
| 数据 | dataset/version/hash、split、license、时间截止、example IDs |
| 适配 | instruction、few-shot examples/order、chat template、answer choices |
| 系统 | checkpoint/API date、tokenizer、decoder、retriever/tools、hardware |
| 评分 | normalization、parser、reference、metric/judge/version、failure rule |
| 抽样 | sampling unit、seed、samples per item、cluster、budget |
| 统计 | estimand、micro/macro、CI、slices、multiplicity、selection |

HELM 的 scenario→adaptation→metric→model deployment 分解是一种有用框架；“holistic”仍要求显式列出没有覆盖的场景和指标。

## 七、内外效度

Benchmark 内部可复现不等于能代表真实总体。需分别问：

- **construct validity**：指标真的测目标能力/风险吗？
- **internal validity**：比较是否只改变预期因素？
- **external validity**：题目、语言、用户与时间能否外推？
- **statistical conclusion validity**：样本与区间足以支持差异吗？

长上下文 benchmark 可能测位置检索而非真实工作流；选择题可能受答案字母偏置；公开题可能被训练污染。分数只能在声明的 construct 与 population 内解释。

## 八、图解：从目标总体到可审计分数

**读图问题**：一个排行榜数字究竟经过了哪些总体、采样、配置、输出、评分与聚合选择，任一步改变为何都会改变 estimand？

![[00-知识库管理/_assets/figures/language-models/fig-lm-eval-estimand-pipeline-v1.svg|900]]

> [!figure] 图 LM-57　Estimand—sample—run—score—decision 流水线
> **生成：**本库按评估统计对象和 HELM 式运行 manifest 绘制；图中样本数与分数为教学符号，不是排行榜数据。

**怎样读图**：从左到右先写目标总体与独立单位，再核对模型—解码器—系统配置；输出经过 parser/reference/judge 后才形成 per-unit score，最后才允许聚合、区间和决策。

**图没有证明什么**：流程完整只保证主张可解释和可复现，不保证 benchmark construct 有效、样本代表真实用户，也不保证系统在未来分布、语言或版本上维持同一分数。

## 九、常见错误与出口标准

错误包括：benchmark 名替代 estimand；把多样本/多 prompt 当独立题；删除失败；micro/macro 混写；只报总体均值；validation 调参后仍当 test；用 API 名替代 checkpoint/date。

完成本节后，应能把任意“模型得分”重写成带总体、对象、随机性、单位、分母和版本的期望，计算 macro/micro，设计 cluster-aware 抽样，并生成一份可复现 run manifest。

## 十、来源与练习

- [[S-2023-Liang-HELM]]；
- [[S-2024-Hsieh-RULER]]；
- [[S-2024-Sclar-Prompt-Sensitivity]]；
- [[习题 - 语言模型评估对象、任务单位与 Benchmark 合同]]；
- [[解答 - 语言模型评估对象、任务单位与 Benchmark 合同]]。

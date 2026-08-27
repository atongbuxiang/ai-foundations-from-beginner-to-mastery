---
type: concept
status: verified
area: [language-models, evaluation, sampling, selection]
node_id: LM-59
aliases: [Pass-at-k, Best-of-N 评估]
prerequisites: ["[[Logits、Softmax、Temperature 与 Categorical Sampling]]", "[[语言模型评估对象、任务单位与 Benchmark 合同]]"]
related: ["[[Self-Consistency、Best-of-N 与 Pass-at-k]]", "[[Test-time Compute、Search、Verifier 与预算]]"]
sources: ["[[S-2021-Chen-Codex-PassAtK]]", "[[S-2023-Wang-Self-Consistency]]", "[[S-2021-Cobbe-Training-Verifiers]]"]
exercises: ["[[习题 - Pass-at-k、Best-of-N、采样估计与选择偏差]]"]
solutions: ["[[解答 - Pass-at-k、Best-of-N、采样估计与选择偏差]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-eval-passk-selection-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Pass-at-k、Best-of-N、采样估计与选择偏差

> [!abstract] 一句话结论
> Pass@$k$ 衡量 $k$ 次尝试中“至少一个成功”的覆盖，Best-of-$N$ 衡量选择器能否把好候选挑出来，self-consistency 衡量答案聚合；三者的 oracle、用户可见输出、预算和统计分母都不同。

## 一、已知单样本成功率时

若每次样本独立、同分布，单样本成功率为 $p$，则

$$
\Pr(\text{at least one success in }k)
=1-(1-p)^k.
$$

这说明覆盖随 $k$ 增加，但边际收益

$$
\Delta_k=p(1-p)^{k-1}
$$

递减。独立同分布是关键：固定 seed、低温或相同推理模板可使样本高度相关，实际覆盖低于用平均 $\hat p$ 代入的理想曲线。

## 二、HumanEval 的组合估计量

对每题生成 $n\ge k$ 个候选，其中 $c$ 个通过测试。若从这 $n$ 个候选中无放回均匀选 $k$ 个，全部失败概率是

$$
\frac{\binom{n-c}{k}}{\binom nk}.
$$

因此估计量

$$
\widehat{\operatorname{pass@}k}
=1-\frac{\binom{n-c}{k}}{\binom nk}.
$$

边界：$c=0$ 得 0；若 $n-c<k$，不可能全失败，得 1。实现用乘积或 log 组合避免大整数/浮点 overflow。

先估 pass@1 再计算 $1-(1-\widehat p)^k$ 一般有 plug-in bias；组合式直接利用 $n,c$。跨题通常先每题算 estimator 再 macro average，不能把所有候选混成一个池。

## 三、Oracle coverage 不等于用户成功

Pass@$k$ 假设有 oracle 知道哪个候选正确，例如单元测试。若真实产品只能返回一个回答，至少要定义 selector $S$：

$$
\hat y=\arg\max_{j\le N}s(x,y_j).
$$

需要分开：

- **oracle pass@$N$**：候选池里是否有成功；
- **selector success@$N$**：被 $S$ 选中的是否成功；
- **selection regret**：池中最佳真实效用减被选效用；
- **cost**：生成、验证、judge 与延迟。

候选覆盖提高而选择器不改善时，用户看不到 oracle 增益。

## 四、Best-of-N 与 winner's curse

若 selector score

$$
s_j=u_j+\epsilon_j
$$

是带噪效用代理，取最大 $s_j$ 会同时选择较高真实效用和较大正噪声。$N$ 越大，被选 score 的乐观偏差往往越大；在同一 judge 上调参和报告会放大 Goodhart/overoptimization。

应在 validation 用 selector 选候选或超参，在独立 test 用外部 metric/人评估最终输出；报告 oracle、selector、独立 judge 三条曲线。不要在 $N$ 个 test 输出中用 gold 选最好后称部署性能。

## 五、Self-consistency 是另一估计对象

Self-consistency 抽多条 reasoning path，抽取规范化答案 $a_j$，按频数

$$
\hat a=\arg\max_a\sum_{j=1}^N\mathbf1[a_j=a].
$$

它不寻找某个测试通过的任意候选，而估计答案质量的样本众数。答案等价类、parser、tie rule 与 correlated paths 会影响结果。多数一致可以稳定地错。

## 六、预算匹配

公平比较要固定至少一种实际资源：

- 总 output tokens；
- target forward-equivalent FLOPs；
- wall-clock/latency SLO；
- API cost；
- verifier/judge calls；
- 峰值并发与显存。

同为 $N=32$，短答案和长 CoT 成本不同；强 verifier 的一次调用也不能当免费。绘制 quality–coverage–selection–cost 四维，不只横轴写 sample count。

## 七、置信区间与依赖

基本独立单位通常是 problem，不是同一题的 $n$ 个候选。应保存每题 estimator，再对题目做 bootstrap；若题目按来源、作者或模板成簇，按 cluster 重采样。对多个 $k$ 的曲线可给 simultaneous band 或明确探索性。

若 sampler 随前面候选自适应改变，已不满足同分布；应报告 sequential policy，并直接按完整策略在独立题上重复，不套用静态 pass@$k$ 公式。

## 八、图解：候选覆盖、选择器与用户输出

**读图问题**：当候选池里已经出现正确答案时，为什么 pass@$k$ 可以上升而用户可见成功率仍停滞，扩大 $N$ 又怎样放大选择噪声？

![[00-知识库管理/_assets/figures/language-models/fig-lm-eval-passk-selection-v1.svg|900]]

> [!figure] 图 LM-59　Oracle coverage—selector—user utility 三段漏斗
> **生成：**本库按组合 pass@$k$、noisy selector 与预算账绘制；候选颜色和分数是可手算教学数据。

**怎样读图**：先在候选池中判断是否至少一个 success，再看 selector 是否选择该项；随后把被选输出送入独立评估，最后沿下方曲线核对 sample、token、judge 与 latency 成本。

**图没有证明什么**：教学漏斗不证明真实 verifier 的准确率，也不证明增加样本数总会提高最终质量；相关采样、错误测试、judge 偏差和成本饱和都可能破坏理想收益。

## 九、常见错误与出口标准

错误包括：$1-(1-\hat p)^k$ 冒充无偏 estimator；候选当独立题；pass@$k$ 当 top-1；gold 选 test 输出；忽略 selector；不同 token 预算比较 N；多数一致当真值。

完成本节后，应能手算组合 estimator 与边界，区分 oracle/selector/aggregation，解释 winner's curse，按 problem 做区间，并设计预算匹配的 Best-of-$N$ 实验。

## 十、来源与练习

- [[S-2021-Chen-Codex-PassAtK]]；
- [[S-2023-Wang-Self-Consistency]]；
- [[S-2021-Cobbe-Training-Verifiers]]；
- [[习题 - Pass-at-k、Best-of-N、采样估计与选择偏差]]；
- [[解答 - Pass-at-k、Best-of-N、采样估计与选择偏差]]。

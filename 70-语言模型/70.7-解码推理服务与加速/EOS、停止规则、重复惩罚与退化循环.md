---
type: concept
status: verified
area: [language-models, decoding, stopping, degeneration]
node_id: LM-52
aliases: [EOS 与停止, 重复惩罚]
prerequisites: ["[[Top-k、Top-p、Typical 与 Min-p 截断采样]]", "[[Teacher Forcing、暴露偏差与生成时分布漂移]]"]
related: ["[[Greedy、Beam Search、Sequence Score 与 Length Penalty]]", "[[Grammar-constrained Decoding、Schema 与结构化输出]]"]
sources: ["[[S-2020-Su-7500-自回归停止与解码]]", "[[S-2021-Su-8128-Repetition]]", "[[S-2020-Welleck-Unlikelihood]]", "[[S-2020-Su-7259-Exposure-Bias]]"]
exercises: ["[[习题 - EOS、停止规则、重复惩罚与退化循环]]"]
solutions: ["[[解答 - EOS、停止规则、重复惩罚与退化循环]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-decoding-stopping-survival-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# EOS、停止规则、重复惩罚与退化循环

> [!abstract] 一句话结论
> EOS 是模型词表中的概率事件；stop string、max tokens、timeout 与 parser 是外部控制事件。它们产生不同终止时间和可见输出。重复也可能来自模型、训练、截断、搜索、约束或实现，不能用一个 penalty 解释全部。

## 一、EOS hazard 与生存概率

在未结束前缀 $h_t$ 上

$$
\lambda_t=p(\mathrm{EOS}\mid h_t).
$$

给定非 EOS 历史，至少生成 $T$ 个非 EOS token 的条件生存概率

$$
S(T\mid h_{1:T})=\prod_{t=1}^{T}(1-\lambda_t).
$$

若对所有可达未终止前缀 $\lambda_t\ge\epsilon>0$，则 $S(T)\le(1-\epsilon)^T\to0$，几乎必然最终 EOS。只知道平均 EOS 概率大于零不够；系统可能进入 hazard 极小的循环区。

## 二、五种终止事件

1. 生成 EOS token；
2. 生成字节后命中 stop string；
3. 达 max_new_tokens/max_length；
4. grammar 达 accepting state 并结束；
5. timeout/cancel/error。

Stop string 可跨 token；实现可能返回或删除匹配字节。Max token 是 censoring，不是模型认为完成。报告长度需说明 prompt/EOS/被裁 stop 是否计入。

## 三、重复惩罚改变采样核

Presence/frequency penalty 可写

$$
z'_v=z_v-\alpha\mathbf1\{c_v>0\}-\beta c_v.
$$

再 softmax 得新核 $q$，不再是原模型 $p_\theta$。No-repeat $n$-gram 将会完成已见 $n$-gram 的 token mask 为 $-\infty$；它能阻断局部重复，也可能禁止必需名称、代码或格式。

## 四、循环的马尔可夫构造

二元近似用固定转移矩阵 $P$。若 A→B 与 B→A 都高而 EOS 很低，ABAB… 可有显著质量。科学空间 8128 用 Hadamard square、迹与谱量分析重复环，并明确推广到一般自回归需额外近似。

真实 Transformer 的循环可能来自训练语料/目标、greedy/beam 尖峰、truncation 删除逃逸 token、grammar/stop 缩窄集合、self-context 污染或 cache/state bug。

## 五、训练与解码需分账

Unlikelihood training 在训练时压低不希望项；repetition penalty 推理时改 logits；数据去重改训练分布；stop/grammar 改可行序列。重复减少不识别哪种机制正确，也可能牺牲必要复述。Exposure bias 不是唯一根因。

## 六、实验矩阵

固定 prompt/model，扫描 raw/greedy/top-$p$、EOS/min length、跨 token stop、max length、presence/frequency/no-repeat、cache on/off，并覆盖重复文本、列表、代码、引文任务。

报告 EOS rate、censoring、stop-match、length survival、repeat span、distinct-$n$、task correctness 与 parser failure。Distinct-$n$ 高可能只是胡乱输出。

## 七、图解：同一生成何时结束

**读图问题**：EOS 的逐步 hazard 怎样累积成生存曲线，外部 stop/max/cancel 又为何不能与模型自然完成记成同一种事件？

![[00-知识库管理/_assets/figures/language-models/fig-lm-decoding-stopping-survival-v1.svg|900]]

> [!figure] 图 LM-52　EOS hazard、生存曲线与外部 censoring
> **生成：**本库按离散 hazard/survival 公式确定性绘制；右下用有限状态 toy 展示重复环，所有概率与状态只作教学。

**怎样读图**：先沿曲线把每一步条件 hazard 与累计 survival 分开，再把 EOS 与 max/stop/cancel 的触发位置分账；最后观察 penalty 是改变环内转移核，还是只删掉可见文本。

**图没有证明什么**：有限状态 toy 只构造一种可能的重复机制，不证明一般 Transformer 的所有重复都由谱量、截断稀疏性或 exposure bias 决定，也不证明惩罚不会损伤必要复述。

## 八、常见错误与出口标准

错误包括：把 max tokens 当自然完成；只看平均长度；字符 stop 声称 token EOS；惩罚后仍报原模型 log-prob；把重复全归 exposure bias；禁重后不测任务正确。

完成本节后，应能推导生存上界，区分终止事件，写 penalty 后的新核，构造/打破二元循环，并设计不把必要重复当退化的实验。

## 九、来源与练习

- [[S-2020-Su-7500-自回归停止与解码]]；
- [[S-2021-Su-8128-Repetition]]；
- [[S-2020-Welleck-Unlikelihood]]；
- [[S-2020-Su-7259-Exposure-Bias]]；
- [[习题 - EOS、停止规则、重复惩罚与退化循环]]；
- [[解答 - EOS、停止规则、重复惩罚与退化循环]]。

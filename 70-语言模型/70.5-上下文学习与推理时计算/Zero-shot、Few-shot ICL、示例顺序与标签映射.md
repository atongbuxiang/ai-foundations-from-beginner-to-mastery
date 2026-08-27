---
type: concept
status: verified
area: [language-models, in-context-learning, demonstrations]
node_id: LM-34
aliases: [Few-shot ICL, 示例顺序敏感性, 标签映射]
prerequisites: ["[[Prompt 作为条件事件、序列化与敏感性]]", "[[训练集、验证集、测试集与自适应复用]]"]
related: ["[[ICL 的 Bayesian、线性回归与元优化解释]]", "[[Contamination、Prompt Sensitivity、Robustness 与不确定性]]"]
sources: ["[[S-2020-Brown-GPT3-ICL]]", "[[S-2022-Min-Role-of-Demonstrations]]", "[[S-2022-Lu-Prompt-Order]]", "[[S-2021-Zhao-Contextual-Calibration]]", "[[S-2020-Su-7764-MLM-PET]]"]
exercises: ["[[习题 - Zero-shot、Few-shot ICL、示例顺序与标签映射]]"]
solutions: ["[[解答 - Zero-shot、Few-shot ICL、示例顺序与标签映射]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-icl-factorial-sensitivity-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Zero-shot、Few-shot ICL、示例顺序与标签映射

> [!abstract] 一句话结论
> Few-shot 提升可能来自任务说明、输入分布、输出格式、标签集合、正确 input-label 对应或样例检索。只有逐项消融并报告排列分布，才能说模型从 demonstrations 学到了什么。

## 一、先固定三个术语

- zero-shot：只有任务说明与 query，没有任务 demonstration；
- one-shot：一个输入—输出 demonstration；
- few-shot：$K>1$ 个 demonstrations 与 query 同时放入上下文；
- ICL：部署时不更新模型参数，行为随上下文示例变化。

“不更新参数”不等于“模型内部没有状态变化”：每层激活和 KV cache 都依 prompt 改变。它只说明外部 checkpoint $\theta$ 固定。

把第 $j$ 个 demonstration 写成 $d_j=(x_j,y_j)$，顺序 $\pi$ 下的 prompt 为

$$
P_\pi=I\oplus d_{\pi(1)}\oplus\cdots\oplus d_{\pi(K)}\oplus x_*.
$$

因 causal attention 和位置编码，$P_\pi$ 与 $P_{\pi'}$ 是不同条件序列；集合相同不保证预测相同。

## 二、demonstration 同时传递六类信息

1. task semantics：输入与输出之间应是什么关系；
2. input distribution：输入像评论、数学题还是代码；
3. label space：允许输出 A/B、yes/no 或自然词；
4. format：字段、分隔符和回答长度；
5. local prior：各标签在 prompt 中的频率与最近位置；
6. retrieval signal：哪些例子与当前 query 相似。

所以看到 few-shot 优于 zero-shot，不能直接得出“模型学会了 demonstration 中的函数”。它也可能只是得到合法答案格式或标签集合。

## 三、一个可判别的消融矩阵

对同一示例输入，至少比较：

| 条件 | 输入内容 | demonstration label | 格式/label space | 测量对象 |
|---|---|---|---|---|
| 真配对 | 保留 | 正确 | 保留 | 总 few-shot 效果 |
| 随机配对 | 保留 | 打乱 | 保留 | 正确映射的增量 |
| 无标签 | 保留 | 删除 | 部分破坏 | label space + format |
| 随机输入 | 替换 | 保留频率 | 保留 | 输入分布/相似性 |
| 仅格式 | 代理输入 | 代理标签 | 保留 | serialization prior |
| 反标签 | 保留 | 系统置换 | 保留 | 能否覆盖模型先验 |

[[S-2022-Min-Role-of-Demonstrations]] 在其模型和分类协议中发现，随机标签有时只造成有限下降，而 label space、输入分布与格式仍重要。正确写法是“在这些条件下，正确映射的边际贡献较小”，不是“ICL 不用正确标签”。

## 四、标签置换是强测试

二分类原本映射为 positive/negative。定义置换 $\sigma$ 交换两标签，并在 demonstrations 中一致替换。若模型真正从上下文学到临时映射，query 输出也应随 $\sigma$ 变换。

定义 equivariance success：

$$
E_i=\mathbf 1\{\hat y_i(\sigma P)=\sigma(\hat y_i(P))\}.
$$

若模型仍坚持自然语义先验，例如正面评论总输出 positive，就说明 prompt 映射与预训练 label semantics 发生竞争。

对无语义标签 A/B 或 dax/wug 做同样测试，可进一步分离 label semantics 与临时配对。但必须先固定这些 label 的 token prior。

## 五、顺序敏感性与 $K!$ 问题

$K$ 个不同 demonstrations 有 $K!$ 种排列。$K=4$ 时为 24，尚可枚举；$K=8$ 时已是 40320，通常只能预注册随机样本。

对每个排列 $\pi$ 计算准确率 $A_\pi$，应报告

$$
\bar A,\quad \operatorname{median}(A_\pi),\quad
\min A_\pi,\quad\max A_\pi,
$$

以及逐样本 prediction flip。只报告 $\max A_\pi$ 把 prompt search 当成免费的测试时优化。

顺序影响可能来自：

- recency：后部 label/format 更接近 query；
- label imbalance：最后几例改变局部频率；
- similarity placement：最相似例距 query 远近不同；
- causal receptive field：早期示例不能看到后期示例；
- truncation：长 prompt 时前部被截断。

这些是待区分的机制，不应仅以“位置偏置”统称。

## 六、示例选择与检索

若从池 $\mathcal D$ 为 query $x_*$ 选 $K$ 个 demos，selector $S(x_*,\mathcal D)$ 已成为系统的一部分。公平评估要分：

- random：预注册 seed；
- class-balanced：可能使用 label；
- semantic retrieval：记录 encoder/index/version；
- diversity selection：记录距离与目标；
- oracle selection：若用测试表现选，只能作上界。

检索相似不必然更好：相似例可能标签同质、包含捷径或占据太多上下文。选择器在验证集上调参，应计入监督预算。

## 七、手算：排列均值与“最好值”

设四种排列准确率为 $0.8,0.7,0.5,0.4$。则均值 $0.6$，范围 $0.4$，最好值 $0.8$。若论文只公布 $0.8$，读者会把一个经过四次试验的选择结果误当随机部署性能。

若部署时均匀随机排列，目标是均值；若有不看测试标签的固定 selector，目标是 selector 的独立测试表现；两者不是同一 estimand。

## 八、图解：ICL 因子设计

先看图回答：热图中的 24 个格子为什么不能只取最大值？

![[00-知识库管理/_assets/figures/language-models/fig-lm-icl-factorial-sensitivity-v1.svg|900]]

> [!figure] 图 LM-34　Demonstration 成分与排列热图
> 左侧列出 instruction、输入、标签、顺序和 verbalizer 五个因子；右侧展示同一四例集合在不同排列下的教学用分数，并给出分布报告合同。图由本库重新绘制。
> **生成：**本图由本库依据本节定义、正文列出的一级来源和固定绘图脚本重新绘制；图中的小规模数值或结构用于教学，不复刻论文原图。

**怎样读图**：先选定一行因子，只改变一个坐标；顺序实验要把所有或预注册采样的格子视为分布，再说明部署时如何选择。

**图没有证明什么**：该图只解释Zero/Few-shot、示例顺序与标签映射的析因设计的结构和本节样例，不证明任意模型、数据、语言或部署环境都会得到同一性能；真实结论仍需独立实验、区间与版本化工件。


**图没有证明什么**：热图数值不是任一真实模型结果，也不证明顺序敏感在所有规模上相同。

## 九、最小研究协议

1. 冻结模型、tokenizer、template、scorer 和 dataset split；
2. 预注册 demonstration pool、$K$、selector 和排列数；
3. 做 correct/random/permuted labels 与 format-only 消融；
4. 对每个 query 保存实际 demos、顺序和 IDs；
5. 报均值、分位数、最坏值、翻转率和 bootstrap 区间；
6. 将 prompt/selector 调优集与最终测试集隔离；
7. 若做 calibration，单独报告校准前后和 content-free 输入。

## 十、常见错误

- 把 few-shot 与参数微调混用；
- 看到随机标签仍有效就声称标签完全无用；
- 对不同 query 使用不同 demos 却不记录 selector；
- 用测试集选择顺序；
- 自然词 label 与字母 label 采用不同 scorer；
- 增加示例数时未匹配总 token 长度；
- 忽略长 prompt 截断了早期示例。

## 十一、出口标准

完成本节后，应能把一次 ICL 结果拆成 instruction、format、input distribution、label space、mapping、selection 与 order 七项贡献；能手算排列统计并设计 label permutation 测试；能说明“参数没更新”与“上下文中没有适应”为什么不是一回事。

## 十二、来源与练习

- [[S-2020-Brown-GPT3-ICL]]：经典 zero/one/few-shot 协议；
- [[S-2022-Min-Role-of-Demonstrations]]：示例成分消融；
- [[S-2022-Lu-Prompt-Order]]：排列敏感性；
- [[S-2021-Zhao-Contextual-Calibration]]：prompt/label bias；
- [[S-2020-Su-7764-MLM-PET]]：pattern/verbalizer 接口；
- [[习题 - Zero-shot、Few-shot ICL、示例顺序与标签映射]]；
- [[解答 - Zero-shot、Few-shot ICL、示例顺序与标签映射]]。

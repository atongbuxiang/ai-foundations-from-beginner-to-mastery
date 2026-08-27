---
type: concept
status: verified
area: [language-models, decoding, truncation-sampling]
node_id: LM-51
aliases: [Nucleus Sampling, 截断采样]
prerequisites: ["[[Logits、Softmax、Temperature 与 Categorical Sampling]]"]
related: ["[[EOS、停止规则、重复惩罚与退化循环]]", "[[解码质量、延迟、吞吐、随机性与证据地图]]"]
sources: ["[[S-2019-Holtzman-Nucleus-Sampling]]", "[[S-2023-Meister-Locally-Typical]]", "[[S-2024-Nguyen-Min-p]]", "[[S-2025-Schaeffer-Min-p-Critique]]"]
exercises: ["[[习题 - Top-k、Top-p、Typical 与 Min-p 截断采样]]"]
solutions: ["[[解答 - Top-k、Top-p、Typical 与 Min-p 截断采样]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-decoding-truncation-profile-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Top-k、Top-p、Typical 与 Min-p 截断采样

> [!abstract] 一句话结论
> 四种方法都先定义 prefix-dependent support，再把原概率在该集合内重归一化；差别在集合规则。它们从修改后的核采样，不再保持原模型完整 support，也没有一种在所有任务和温度上普遍最优。

## 一、统一写法

$$
q_\phi(v\mid h)
=\frac{p(v\mid h)\mathbf1\{v\in S_\phi(h)\}}
{Z_\phi(h)},
\qquad
Z_\phi(h)=\sum_{u\in S_\phi(h)}p(u\mid h).
$$

被删除质量 $1-Z_\phi$ 的概率严格为零。若没有其他变换，保留 token 相互 odds 不变。

## 二、top-$k$

保留概率最大的 $k$ 个 token。集合大小固定，保留质量随前缀变化。尖分布会保留一些极小项；平分布可能丢大量质量。Tie 要定义稳定 token ID、全保留 ties 或精确保留 $k$。

## 三、top-$p$ / nucleus

令 $p_{(1)}\ge\cdots$：

$$
k^\star=\min\left\{k:\sum_{i=1}^kp_{(i)}\ge\rho\right\}.
$$

尖分布候选少，平分布候选多。需说明至少一项、边界 token、ties 与 temperature 顺序。

## 四、locally typical

$$
H(p)=-\sum_vp(v)\log p(v),\qquad
d(v)=|-\log p(v)-H(p)|.
$$

按 $d(v)$ 从小到大累加质量至 $\rho$。它优先信息量接近当前条件熵的 token，不必包含最高概率 token。若实现强制含 argmax，算法已改变。

## 五、min-$p$

$$
S_{\min p}=\{v:p(v)\ge\alpha p_{\max}\}.
$$

尖分布的阈值高、集合窄；平分布阈值随 $p_{\max}$ 降低。它不是 top-$p$ 的累计质量。

Min-p 的定义与采用可确认，经验优越性是另一个主张。2025 年复核质疑原人评、统计与超参数比较，因此课程不宣称普遍胜出。

## 六、手算例子

$p=(0.50,0.25,0.15,0.07,0.03)$：

- top-2 保留前两项，质量 .75，新概率 $(2/3,1/3)$；
- top-$p=.80$ 保留前三项，质量 .90；
- min-$p=.2$ 阈值 .1，保留前三项；
- typical 必须先算 $H$ 与 surprisal deviation。

某一 prefix 集合相同不表示算法等价；换 prefix 后会分离。

## 七、复合处理不交换

Temperature 改变 top-$p$ 质量、typical entropy 和 min-$p$ 阈值。Top-$k$ 排名在正温度下不变，但最终概率仍变。多个 sampler 常取集合交；若中间 renormalize，顺序还会改变结果。

应逐步保存 support IDs、size、保留质量和 renormalized probabilities。

## 八、图解：同一概率剖面的四种切法

**读图问题**：面对同一个降序概率剖面，固定候选数、固定累计质量、典型信息量和相对峰值阈值分别会保留哪些 token？

![[00-知识库管理/_assets/figures/language-models/fig-lm-decoding-truncation-profile-v1.svg|900]]

> [!figure] 图 LM-51　固定候选数、累计质量、surprisal 偏差与相对阈值
> **生成：**本库按四种 support 定义与同一组教学概率确定性绘制；相同 token 概率在各方法中保持不变，只改变集合规则。

**怎样读图**：先从左侧柱高读出原概率和累计质量，再逐个方法核对阈值、候选 IDs 与保留质量；最后记住采样前还要在各自 support 内重新归一化，不能只比较候选数。

**图没有证明什么**：单个 toy prefix 的集合大小不能推出长文本质量、多样性、事实性或服务延迟，也不能把 min-$p$ 或任何截断器排成跨模型、跨任务的普遍冠军。

## 九、常见错误与出口标准

错误包括：说 top-$p$ 固定 token 数；把 typical 当最常见；漏重归一化；把 min-p 优势当定论；不存顺序；用 distinct-n 单独定质量。

完成本节后，应能手算四种 support、删除质量与新概率，解释处理顺序，并区分定义、实现与经验优势。

## 十、来源与练习

- [[S-2019-Holtzman-Nucleus-Sampling]]；
- [[S-2023-Meister-Locally-Typical]]；
- [[S-2024-Nguyen-Min-p]]；
- [[S-2025-Schaeffer-Min-p-Critique]]；
- [[习题 - Top-k、Top-p、Typical 与 Min-p 截断采样]]；
- [[解答 - Top-k、Top-p、Typical 与 Min-p 截断采样]]。

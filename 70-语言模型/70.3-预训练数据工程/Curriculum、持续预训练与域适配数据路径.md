---
type: concept
status: verified
area: [language-models, pretraining-data, curriculum, continued-pretraining]
node_id: LM-23
aliases: [Continued pretraining, DAPT TAPT, 数据课程]
prerequisites: ["[[数据混合、温度采样、重加权与域损失]]", "[[SGD、采样顺序与梯度累积的等价边界]]"]
related: ["[[数据版本、Provenance、有效 Token 与证据地图]]", "[[全量微调、冻结表示与灾难性遗忘]]"]
sources: ["[[S-2020-Gururangan-DAPT]]", "[[S-2021-Rae-Gopher]]", "[[S-2025-Ye-Data-Mixing-Laws]]"]
exercises: ["[[习题 - Curriculum、持续预训练与域适配数据路径]]"]
solutions: ["[[解答 - Curriculum、持续预训练与域适配数据路径]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-data-curriculum-continual-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Curriculum、持续预训练与域适配数据路径

> [!abstract] 一句话结论
> 当数据分布随训练步变化时，训练对象不再由一个静态 mixture 描述，而是由路径 $\{\pi_t,\eta_t,\text{optimizer state}_t\}$ 决定。相同数据 multiset 以不同顺序呈现，非凸优化、学习率衰减与自适应状态会到达不同参数；新域收益必须与旧域遗忘、重复 exposure 和选择预算一起报告。

## 一、从静态风险到时间变化风险

静态 mixture 下：

$$
R_\pi(\theta)=\sum_g\pi_gR_g(\theta).
$$

Curriculum/continued pretraining 令 $\pi$ 随步 $t$ 变化：

$$
Z_t\sim\operatorname{Categorical}(\pi_t),
\qquad
\theta_{t+1}=\theta_t-\eta_t\widehat g(\theta_t;Z_t,X_t,s_t),
$$

其中 $s_t$ 是 momentum/Adam moments 等 optimizer state。最终参数是整条路径的函数：

$$
\theta_T=F(\theta_0,\{\pi_t,\eta_t,s_t,\zeta_t\}_{t<T}).
$$

因此只报告“总共看过 A/B 各 50% tokens”不能复现前半段全 A、后半段全 B 与全程交替 A/B。

## 二、为什么顺序会有影响

对两个 batch gradient maps

$$
U_A(\theta)=\theta-\eta g_A(\theta),\qquad
U_B(\theta)=\theta-\eta g_B(\theta),
$$

一般

$$
U_B(U_A(\theta))\ne U_A(U_B(\theta)).
$$

因为第二个 gradient 在第一个更新后的参数点计算。即使损失光滑，差异主项也与 Hessian–gradient 交互有关；在非凸网络、Adam state、gradient clipping 和 schedule 下更明显。

只有在特殊情形（常梯度、可交换线性更新或充分收敛到同一唯一解）顺序才可能无关。Shuffle seed 属于训练数据路径版本。

## 三、Curriculum 的三个对象

1. **difficulty score** $c(x)$：长度、模型 loss、语法复杂度、人工等级等 proxy；
2. **schedule** $q_t(x)$：在第 $t$ 步怎样按 score 采样；
3. **budget/selection**：尝试了多少 score/schedule，再按哪个 validation 选择。

经典 easy→hard 不是定理。Easy examples 可能给低噪声梯度，也可能只强化捷径；hard-first 可能帮助覆盖，也可能不稳定。比较需固定 FLOPs 与调参预算，并完整衰减 baseline 学习率，否则只是把不同 token 配给了不同学习率。

## 四、Continued pretraining、DAPT 与 TAPT

给基础 checkpoint $\theta_0$：

- **continued pretraining**：继续同/新 objective 与新数据训练；
- **DAPT**：在目标领域的大量未标注文本继续预训练；
- **TAPT**：在目标任务更贴近的未标注文本继续预训练；
- 随后才可能进入 supervised fine-tuning。

路径可写为

$$
\theta_0
\overset{\mathcal D_{domain},N_D,\eta_D}{\longrightarrow}\theta_1
\overset{\mathcal D_{task},N_T,\eta_T}{\longrightarrow}\theta_2
\overset{\mathcal D_{sup},N_S}{\longrightarrow}\theta_3.
$$

每条边需保存 input checkpoint hash、data manifest、objective/tokenizer、optimizer 是否重置、steps/tokens/FLOPs、seed 与所有 validation slices。

## 五、遗忘怎样定义

设旧域风险 $R_{old}$、新域风险 $R_{new}$。前后差：

$$
\Delta_{new}=R_{new}(\theta_T)-R_{new}(\theta_0),
\qquad
\Delta_{old}=R_{old}(\theta_T)-R_{old}(\theta_0).
$$

对 loss，$\Delta_{new}<0$ 是新域改善，$\Delta_{old}>0$ 是旧域退化。还应比较任务 metric、安全、校准与生成行为；参数距离大不等于功能遗忘，距离小也可能在关键 prompts 上显著退化。

若只在新域选 checkpoint，会系统性隐藏旧域损失。至少保留 general、new-domain、low-resource/safety、time-sliced、held-out task 五类验证。

## 六、回放、混合与正则化

常见缓解：

- replay：continued 阶段混入旧域，$\pi_t=(1-\lambda_t)e_{new}+\lambda_t\pi_{old}$；
- 较小学习率/较短训练；
- parameter regularization 或功能蒸馏；
- adapter/LoRA 等限制可训练子空间；
- checkpoint interpolation/merge；
- optimizer state reset 或重新 warmup。

它们改变不同对象：Replay 改经验分布；L2/蒸馏改目标；PEFT 改可行参数集。不能都简称“防遗忘”后只比一个新域分数。

$\lambda$ 增大通常提高旧域保留但稀释新域预算。比较必须固定总 FLOPs，否则加入 replay 后的改善可能来自额外 tokens。

## 七、重复数据与 exposure

小域 continued pretraining 常跑多 epoch。Unique token $U$、总 exposure token $T$ 时，平均 exposure $E=T/U$；实际分布还受 cluster size、文档长度和 sampler 影响。

重复并非必然无效，但大 exposure 可带来记忆、过拟合和低多样性。应报告：

- unique raw bytes/documents/tokens；
- total token draws 与 exposure quantiles；
- train–validation duplicate isolation；
- memorization/canary 与新旧域曲线；
- dropout/augmentation/reshuffle 版本。

“训练 100B tokens”若只有 2B unique tokens 重复 50 次，与 100B unique tokens 是不同实验。

## 八、阶段选择与 survivor bias

研究者可能尝试多种 order、domain weights、steps、learning rates，只报告最好 checkpoint。Validation 被自适应复用，最终分数含 selection optimism。记录所有 tried paths、选择规则和 search compute；为 final result 保留未参与选择的 test 或 nested evaluation。

比较 curriculum A/B 时调参预算应对称，不能新方法精调 30 次而 baseline 只跑默认一次。

## 九、图：新域下降时旧域可能上升

先看图回答：为什么 base→DAPT→TAPT 的箭头不能只标最终 token 总数？

![[00-知识库管理/_assets/figures/language-models/fig-lm-data-curriculum-continual-v1.svg|900]]

> [!figure] 图 LM-23　Checkpoint lineage、mixture schedule 与双域风险
> 上方把每阶段 checkpoint 与数据边显式化；中部给 $\pi(t)$；下方展示新域 loss 下降而旧域 loss 上升的可能路径。来源：本课程依据 DAPT/TAPT 与数据路径合同独立绘制；曲线为教学示意。

**怎样读图**：沿箭头记录数据、optimizer 和预算，再同时看新/旧 validation；不要用最后一个绿色 checkpoint 覆盖中间失败和搜索路径。

**图没有证明什么**：示意曲线不声称 DAPT 必然遗忘，也不裁决某个 replay 比例；实际方向依模型、数据和 schedule。

## 十、最小实验协议

1. 固定起点 checkpoint 与 raw manifests；
2. 预注册 order/schedule、optimizer reset、tokens/FLOPs；
3. 比较 shuffled-static、easy→hard、hard→easy、staged domain；
4. 每个 checkpoint 测新域、旧域、安全与时间外推；
5. 保存 per-domain exposure 与 unique-token 统计；
6. 多 seed 与对称调参预算；
7. 加 replay/control 后仍固定总 compute；
8. 报完整 path table，不只报胜者。

## 十一、本节出口

你应能将 curriculum 写为 $\pi_t$ 路径，构造更新不交换反例，区分 DAPT/TAPT，并用新旧双风险与 exposure 账审计 continued pretraining。下一节[[数据版本、Provenance、有效 Token 与证据地图]]把本卷全部 transformation 固化成可重放、可删除、可计数的数据产物。

## 练习与独立解答

- [[习题 - Curriculum、持续预训练与域适配数据路径]]
- [[解答 - Curriculum、持续预训练与域适配数据路径]]

---
type: concept
status: draft
area: [learning-theory/pac, machine-learning/foundations]
aliases: [Probably Approximately Correct, PAC Learnability, Sample Complexity]
node_id: LT-10
prerequisites: ["[[泛化间隙与浓缩不等式接口]]", "[[可实现、不可知、相合性与可学习性]]", "[[命题、量词与逻辑等价]]", "[[损失、总体风险与经验风险]]"]
related: ["[[有限假设类、Union Bound 与一致收敛]]", "[[可实现情形的一致 ERM 保证]]", "[[不可知 PAC、ERM 与双侧一致收敛]]", "[[渐近记号、增长率与复杂度]]"]
sources: ["[[S-1984-Valiant-Theory-of-the-Learnable]]", "[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]"]
exercises: ["[[习题 - PAC 学习定义与样本复杂度]]"]
solutions: ["[[解答 - PAC 学习定义与样本复杂度]]"]
created: 2026-08-20
updated: 2026-08-23
---

# PAC 学习定义与样本复杂度

> [!abstract] 本章主问题
> PAC 不是某个特定算法，而是一份带全量词的有限样本合同：对允许的每个数据分布，当样本数至少为 $m_{\mathcal H}(\varepsilon,\delta)$ 时，学习算法都必须以至少 $1-\delta$ 的概率输出 risk 至多比目标 comparator 差 $\varepsilon$ 的预测器。$\varepsilon$ 管“近似正确”，$\delta$ 管“很可能”，样本复杂度把这两种要求翻译成数据资源。

> [!question] 初学者读完必须能回答
> 1. PAC 定义中 $A,\varepsilon,\delta,P,m,S,U$ 的量词顺序是什么？
> 2. $\varepsilon$ 与 $\delta$ 分别约束输出质量还是失败概率？
> 3. Realizable PAC 与 agnostic PAC 使用什么不同 comparator？
> 4. Class learnable、样本高效与计算高效为什么是三种主张？
> 5. Distribution-free、assumption-free、expectation guarantee 与 high-probability guarantee 有何区别？

先用下图回答一个视觉问题：**PAC 合同究竟承诺什么，哪些对象必须先固定，样本复杂度函数又回答哪一个资源问题？**

![[00-知识库管理/_assets/figures/learning-theory/fig-pac-quantifier-sample-complexity-v2.svg|880]]

> [!figure] 图 20.2.2｜PAC 学习的量词合同与样本复杂度
> A 展开 learner、精度/置信参数、分布与样本量的量词次序；B 把成功事件写成随机输出的总体风险不超过 comparator 加 $\varepsilon$；C 对照 realizable 与 agnostic comparator，并拆开统计、计算和表示复杂度。来源：独立绘制；理论接口参考 Valiant PAC framework 与现代 agnostic definition；生成脚本：[[plot_pac_finite_class_v2.py]]；确定性量词地图，无随机种子。

**怎样读图。** 从 A 自上而下朗读量词，特别检查算法不能知道未知 $P$，而 $\varepsilon,\delta$ 在抽样前提出；B 中概率只对样本和算法随机性取，风险仍按目标 $P$ 计算；C 再选择 comparator，最后才问某个算法给出的 $m_{\mathcal H}(\varepsilon,\delta)$ 是否可计算、是否达到最优量级。

**适用边界（图没有证明什么）。** 图是定义与量词合同，不是任何具体假设类的可学习性证明；它没有给出样本复杂度上界，也没有保证 polynomial-time learner 存在。分布族、loss、proper/improper 输出、随机化协议和 approximation error 若未声明，单写“PAC”仍不完整。

## 一、学习目标

1. 写出 realizable PAC 与 agnostic PAC 的现代标准定义；
2. 展开 $\forall\varepsilon,\delta,P,m$ 的正确量词顺序；
3. 区分 accuracy parameter 与 confidence parameter；
4. 定义 sample complexity function，而不是只背一个大 $O$；
5. 处理 randomized learner 的内部随机性；
6. 区分 distribution-free 与“没有任何假设”；
7. 区分 class learnability、某个算法的保证与 computational efficiency；
8. 解释 realizable 与 agnostic comparator 的差别；
9. 判断 expectation guarantee 是否等同 PAC high-probability guarantee；
10. 把一个自然语言学习声称翻译为可证伪的形式合同。

## 二、PAC 的对象合同

先固定：

- 输入空间 $\mathcal X$；
- 输出/标签空间 $\mathcal Y$；
- 假设类 $\mathcal H\subseteq\mathcal Y^{\mathcal X}$；
- 损失 $\ell$；
- 学习算法 $A$；
- 数据分布族与采样协议。

样本

$$
S=(Z_1,\ldots,Z_m)\sim P^m,
$$

算法输出

$$
h_S=A(S).
$$

若算法还有随机种子 $U$，则写成

$$
h_{S,U}=A(S,U).
$$

PAC 要控制的是输出的**总体风险**，不是训练目标本身：

$$
R_P(h_{S,U})=\mathbb E_{Z\sim P}[\ell(h_{S,U},Z)].
$$

## 三、二分类可实现 PAC 定义

考虑 $\mathcal Y=\{0,1\}$、0–1 loss。若存在某个 $h^*\in\mathcal H$ 使

$$
R_P(h^*)=0,
$$

则称 $P$ 对 $\mathcal H$ 是 realizable 的。

### 3.1 正式定义

称算法 $A$ PAC 学习 $\mathcal H$，若存在函数

$$
m_{\mathcal H}:(0,1)^2\to\mathbb N,
$$

使得对任意 $\varepsilon,\delta\in(0,1)$、任意对 $\mathcal H$ 可实现的分布 $P$，只要

$$
m\ge m_{\mathcal H}(\varepsilon,\delta),
$$

就有

$$
\boxed{
\Pr_{S\sim P^m,U}
\left(R_P(A(S,U))\le\varepsilon\right)
\ge1-\delta.
}
$$

若存在某个算法 $A$ 满足此定义，则称假设类 $\mathcal H$ PAC learnable。

> [!note] 为什么右端是 $\varepsilon$ 而非 $R_{\mathcal H}^*+\varepsilon$
> 可实现条件给出 $R_{\mathcal H}^*=0$，所以两种写法在这里相同。进入不可知情形后，零风险 comparator 不再存在，必须显式比较类内最优。

## 四、不可知 PAC 定义

设 loss 有界，常取 $\ell\in[0,1]$。不再假设 $R_{\mathcal H}^*=0$，定义

$$
R_{\mathcal H}^*
=\inf_{h\in\mathcal H}R_P(h).
$$

算法 $A$ agnostically PAC learns $\mathcal H$，若存在 $m_{\mathcal H}^{\rm ag}(\varepsilon,\delta)$，使对任意允许分布 $P$，当 $m$ 足够大时：

$$
\boxed{
\Pr_{S,U}\left(
R_P(A(S,U))
\le \inf_{h\in\mathcal H}R_P(h)+\varepsilon
\right)
\ge1-\delta.
}
$$

等价地，类内 excess risk 满足

$$
\Pr_{S,U}\left(
R_P(A(S,U))-R_{\mathcal H}^*\le\varepsilon
\right)
\ge1-\delta.
$$

### 4.1 comparator 必须写清

若 $\mathcal H$ 本身表达能力不足，则即使 class excess risk 很小，仍可能有

$$
R_P(A(S))-R^*
=\underbrace{R_P(A(S))-R_{\mathcal H}^*}_{\le\varepsilon}
+\underbrace{R_{\mathcal H}^*-R^*}_{\text{approximation error}}.
$$

PAC 保证通常不负责消除第二项。

## 五、逐个读懂量词

定义的骨架是

$$
\exists A,\exists m_{\mathcal H},
\forall\varepsilon,\delta,
\forall P,
\forall m\ge m_{\mathcal H}(\varepsilon,\delta):
\Pr_{S,U}(\text{success})\ge1-\delta.
$$

### 5.1 $\exists A$

要证明 class learnable，只需构造至少一个满足合同的学习算法。ERM 常是统计证明里的存在性见证，但未必计算高效。

### 5.2 $\forall\varepsilon,\delta$

学习器必须能达到任意预先指定的正精度与置信要求，而非只在某组默认参数上有效。

### 5.3 $\forall P$

保证对协议允许的每个数据分布成立。它不允许把未知 $P$ 偷换成某个友好 Gaussian 分布。

### 5.4 $\Pr_{S,U}$

失败集合是样本与算法随机性共同诱导的。总体风险 $R_P(h_{S,U})$ 对给定输出是一个数，但输出随 $S,U$ 改变，因此 risk 也是随机变量。

### 5.5 $\forall m\ge m_{\mathcal H}$

样本复杂度是一个阈值保证。通常可让算法忽略多余样本，因此 learnability 定义要求阈值以上都成立。

> [!warning] 不能把量词交换
> “对每个 $P$ 都存在一个专门知道 $P$ 的算法”不等于“存在一个统一算法对所有 $P$ 都有效”。前者可以直接输出分布最优解，几乎没有学习含义。

## 六、$\varepsilon$、$\delta$ 与 $m$ 各管什么

### 6.1 accuracy $\varepsilon$

$\varepsilon$ 限制输出质量：

$$
R_P(A(S))-R_{\mathcal H}^*\le\varepsilon.
$$

它和 loss 使用同一尺度。0–1 loss 中可解释为至多多错 $\varepsilon$ 比例；一般 loss 中不能直接称为“准确率差”。

### 6.2 confidence $1-\delta$

$\delta$ 是随机训练运行落入坏集合的概率上界：

$$
\Pr_{S,U}(\text{excess}>\varepsilon)\le\delta.
$$

它不是预测某一个样本出错的概率，也不是 calibration confidence。

### 6.3 sample size $m$

$m$ 是独立 sampling units 的数量。它不是参数量、优化步数，也不能在有依赖的序列中不经说明地等同 token 数。

## 七、样本复杂度函数

### 7.1 定义

对固定算法 $A$，可定义最小阈值

$$
m_A(\varepsilon,\delta)
=\inf\left\{m_0\in\mathbb N:
\forall m\ge m_0,\forall P,
\Pr(\text{success})\ge1-\delta
\right\}.
$$

类的最优样本复杂度可进一步对算法取下确界：

$$
m_{\mathcal H}^*(\varepsilon,\delta)
=\inf_A m_A(\varepsilon,\delta).
$$

教材中也常把某个已证明算法的充分上界简称为 $m_{\mathcal H}$。阅读时要分清：它是最优值、上界，还是同阶刻画。

### 7.2 单调性直觉

合理的 sample complexity 上界应满足：

- $\varepsilon$ 越小，$m$ 不减；
- $\delta$ 越小，$m$ 不减；
- 假设类更复杂，$m$ 通常不减。

若推导得到相反趋势，优先检查对数、倒数或不等式方向。

### 7.3 三种精度表述

1. **exact expression**：如 $\lceil \log(M/\delta)/\varepsilon\rceil$；
2. **explicit sufficient bound**：常数正确但未必最优；
3. **order notation**：如 $O((\log M+\log(1/\delta))/\varepsilon)$。

研究证明应保留前两层，建立尺度直觉时才压缩成大 $O$。

## 八、PAC 是 finite-sample，而 consistency 是 asymptotic

统计相合性通常说

$$
R_P(A(S_m))\to R_{\mathcal H}^*
\quad(m\to\infty),
$$

可能是依概率、几乎处处或期望意义收敛。

PAC 则要求给定任意 $(\varepsilon,\delta)$ 后，明确一个有限 $m$，保证

$$
\Pr(\text{excess}>\varepsilon)\le\delta.
$$

二者相关但不相同：

- 有显式 PAC tail bound 通常可推出相应的依概率相合；
- 仅知道 asymptotic convergence 不一定知道需要多少样本；
- 几乎处处相合也未自动给出实用的 finite-sample rate。

## 九、distribution-free 不等于 assumption-free

PAC 常被称为 distribution-free，因为保证不依赖某个具体 $P$ 的参数形式。但它仍然固定了大量归纳偏置：

1. 假设空间 $\mathcal H$；
2. loss 与目标 comparator；
3. iid sampling 或其他协议；
4. realizability、bounded loss 等条件；
5. train/test 分布一致；
6. 可测性与可计算性条件。

所以更准确的说法是：**在给定学习协议内，对所有允许分布统一成立**。

## 十、class、algorithm 与 output 三层

| 层次 | 典型问题 | PAC 中的表达 |
|---|---|---|
| 单个输出 | 这次训练的模型 risk 多大？ | event 内的 $R_P(A(S))$ |
| 算法 | 这个训练规则能否稳定成功？ | 对 $S,U$ 的概率 |
| 假设类 | 是否存在某算法学习整个类？ | $\exists A$ 与 $m_{\mathcal H}$ |

“某次实验成功”不能证明 class PAC learnable；“存在信息论算法”也不保证我们实际用的 SGD 满足同样合同。

## 十一、随机化学习器

若 $A$ 使用独立随机种子 $U$，标准保证是

$$
\Pr_{S,U}(\text{success})\ge1-\delta.
$$

也可给更强的 conditional guarantee，例如对大多数样本 $S$，算法随机性失败概率很小。但不要只写 $\Pr_S$ 后把初始化随机性遗漏。

由全概率公式：

$$
\Pr_{S,U}(B)
=\mathbb E_S[\Pr_U(B\mid S)].
$$

因此 joint failure 小只保证平均 conditional failure 小；它不要求每一份固定训练集上的所有 seeds 都成功。

## 十二、期望保证不等于 PAC 保证

若只知

$$
\mathbb E_{S,U}[\mathcal E(S,U)]\le\alpha,
$$

Markov 不等式给出

$$
\Pr(\mathcal E>\varepsilon)
\le\frac{\alpha}{\varepsilon}.
$$

要让右端不超过 $\delta$，需要 $\alpha\le\varepsilon\delta$。这通常比直接的 exponential tail 弱得多。

反过来，若 $\mathcal E\in[0,1]$ 且

$$
\Pr(\mathcal E>\varepsilon)\le\delta,
$$

则

$$
\mathbb E\mathcal E
\le \varepsilon(1-\delta)+1\cdot\delta
\le\varepsilon+\delta.
$$

所以 high probability 与 expectation 可以转换，但会损失参数，不能不加说明地视为同一句话。

## 十三、realizable 与 agnostic 的结构差异

| 问题 | realizable PAC | agnostic PAC |
|---|---|---|
| 分布条件 | $\exists h^*\in\mathcal H,R_P(h^*)=0$ | 任意允许 $P$ |
| 目标 | $R_P(A(S))\le\varepsilon$ | $R_P(A(S))\le R_{\mathcal H}^*+\varepsilon$ |
| 典型有限类 rate | $1/\varepsilon$ | $1/\varepsilon^2$ |
| 核心证据 | 坏函数需“零错生存” | 要估计风险差 |
| 噪声容忍 | 很弱 | 明确允许 |

典型 rate 的差异会在 LT-12 与 LT-13 完整证明。它不是符号游戏，而是可实现条件提供了额外统计结构。

## 十四、learnable 不等于 efficiently learnable

一个 class 可能存在样本量多项式的 PAC 学习器，但寻找输出需要枚举指数多个假设。统计效率至少问

$$
m=\operatorname{poly}\left(\frac1\varepsilon,\log\frac1\delta,\text{class size parameters}\right),
$$

计算效率还要求运行时间、内存与表示长度也是相应多项式。

> [!example] ERM 的两种身份
> ERM 在理论中常作为“若能求出，就有统计保证”的算法。对某些类 ERM 可多项式求解；对另一些类，ERM 可能 NP-hard。PAC learnability 的统计结论不能自动替代 optimization/computation 分析。

## 十五、从自然语言到 PAC 合同

声称“模型可以从少量数据可靠地学会任务”至少要追问：

1. 学的是哪个 class 或算法？
2. task distribution 的允许集合是什么？
3. loss 与 comparator 是什么？
4. “可靠”是 expectation 还是 $1-\delta$ high probability？
5. “学会”允许多大 excess $\varepsilon$？
6. 样本单位与 iid 假设是什么？
7. $m(\varepsilon,\delta)$ 的显式依赖是什么？
8. 是否还要求训练可计算、预测可部署？

缺少这些字段的“可学习”通常只是直觉判断，还不是数学命题。

## 十六、AI 场景中的边界

### 16.1 Foundation model + downstream class

固定预训练表示后，只学习一个有限/低复杂度 head，可以对 downstream class 给 PAC 分析。但这不等于已经解释预训练模型本身的泛化；representation 的数据依赖性要另行记账。

### 16.2 Prompt selection

若从预先固定的 $M$ 个 prompt 中选一个，prompt 可视为有限假设。若 prompt 又由验证反馈迭代生成，class 和选择协议发生变化，简单 $\log M$ 计数可能不再覆盖真实搜索过程。

### 16.3 分布偏移

PAC guarantee 中训练与评价通常共享 $P$。部署分布变为 $Q$ 时，原合同只控制 $R_P$，不自动控制 $R_Q$；需要 covariate shift、robustness 或 domain adaptation 假设。

### 16.4 大模型的“参数量”不是 PAC 定义字段

PAC 定义本身只写 output risk、概率与样本；参数量进入 sample complexity 需要通过 class capacity、norm、margin、compression、prior/KL 等桥梁，不能直接由“参数很多”推出不可学习。

## 十七、历史与现代定义

Valiant 1984 年的工作奠定了“从随机样例中、在精度与置信要求下有效学习”的计算学习理论框架。现代教材的 realizable/agnostic PAC 定义经过了标准化扩展：

- 原始论文提供历史起点与 efficient learnability 视角；
- 本节的精确符号、risk 形式和 agnostic comparator 以现代教材表述为准；
- 不应把现代定义逐字归因成原论文中的完全相同协议。

## 十八、常见误解

> [!failure] “PAC 中 $\delta$ 是分类错误率”
> 错。分类错误率由 risk/$\varepsilon$ 控制，$\delta$ 是训练运行失败的概率。

> [!failure] “distribution-free 表示没有数据假设”
> 错。iid、class、loss、realizability/boundedness 都是协议条件。

> [!failure] “证明 ERM PAC，就证明 SGD PAC”
> 错。还要说明 SGD 输出是 exact/approximate ERM，或直接分析 SGD 的稳定性和隐式偏置。

> [!failure] “测试集上一次很好，所以 class 可学习”
> 错。PAC 是跨分布、跨随机样本的统一保证，不是一次实验结论。

> [!failure] “大 $O$ 相同就是同一 sample complexity”
> 常数、适用区间、充分上界与必要下界仍可能不同；严谨笔记应保留定理的原始形式。

## 十九、掌握检查

- [ ] 我能写出 realizable 与 agnostic PAC 定义；
- [ ] 我能展开并解释每个量词；
- [ ] 我能区分 $\varepsilon$、$\delta$ 与 $m$；
- [ ] 我能把 randomized learner 的 $U$ 写入概率；
- [ ] 我能说明 distribution-free 的真实含义；
- [ ] 我能区分算法上界与 class 最优样本复杂度；
- [ ] 我能说明 finite-sample PAC 与 asymptotic consistency 的差别；
- [ ] 我能判断一个 PAC 声称是否遗漏 comparator 或计算条件。

## 二十、进一步连接

- [[有限假设类、Union Bound 与一致收敛]]：怎样从 fixed-$h$ concentration 得到 class-level simultaneous guarantee；
- [[可实现情形的一致 ERM 保证]]：第一个完整 PAC theorem，出现 $1/\varepsilon$；
- [[不可知 PAC、ERM 与双侧一致收敛]]：去掉 realizability 后怎样恢复 $1/\varepsilon^2$；
- [[渐近记号、增长率与复杂度]]：统计样本效率之外，怎样严谨读取算法资源增长。

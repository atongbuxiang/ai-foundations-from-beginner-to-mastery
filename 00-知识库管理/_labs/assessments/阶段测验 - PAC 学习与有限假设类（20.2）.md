---
type: assessment
status: draft
material_status: regression-passed
learning_status: not-attempted
area: [learning-theory/pac, learning-theory/finite-classes, machine-learning/generalization]
assessment_id: PAC-CUM-01
scope: [LT-09, LT-10, LT-11, LT-12, LT-13, LT-14, LT-15, LT-16]
time_limit_minutes: 210
closed_notes: true
solution: "[[阶段测验解答 - PAC 学习与有限假设类（20.2）]]"
related: ["[[PAC 学习与有限假设类 MOC]]", "[[学习理论完整课程地图与掌握标准]]", "[[练习与测验 MOC]]", "[[实验 - PAC 学习与有限假设类累计复现门]]"]
created: 2026-08-28
updated: 2026-08-28
---

# 阶段测验 - PAC 学习与有限假设类（20.2）

> [!abstract] 测验目标
> 本卷检查的不是能否背出 $O((\log |\mathcal H|+\log(1/\delta))/\varepsilon)$，而是能否从随机对象和坏事件开始，亲手恢复这条率为何出现、在哪些假设下成立，以及为什么不可知情形通常变为 $1/\varepsilon^2$。完整出口是：读对 PAC 量词；区分 fixed-$h$、simultaneous 与 data-dependent 声明；推导有限类的可实现和不可知上界；用预先固定的编码分配失败预算；最后用 NFL 与 Le Cam 说明任何保证都必须依赖问题结构。

## 零、完整证据时间线

```mermaid
flowchart LR
    O["20 分钟卷级口试"] --> W["210 分钟闭卷"]
    W --> F["冻结原稿、时间与 hash"]
    F --> N["评分者公布 scorer nonce"]
    N --> B["指定主轨 + 跨轨盲参"]
    B --> S["才可打开详解与 canonical 输出"]
    S --> R["48 小时换机制重建"]
    R --> T["14 天陌生模型选择迁移"]
```

脚本先跑通、看图后复述或照抄证明都不构成首次闭卷证据。题卷、详解、脚本与图达到 `regression-passed`，只说明材料合同自洽；在学习者证据产生前，状态保持 `not-attempted`。

## 一、规则与允许工具

- 先完成 20 分钟无提示口试；口试未过可继续笔试诊断，但本次最高为 `attempted`；
- 笔试 210 分钟，满分 100，闭卷，只允许基础计算器；
- 每个概率必须标明对 sample、learner randomness 或测试随机性中的谁取；
- 每次调用 Hoeffding 前，必须写出固定对象、有界性、独立性和共同分布；
- 每次调用 Union Bound 前，必须写出被求并的坏事件；事件之间无需独立；
- 若 $h_S$ 由同一数据选择，不能把 fixed-$h$ 尾界直接代入；
- `realizable`、`consistent learner`、`exact ERM`、`approximate ERM` 不得互换；
- argmin 不存在时应使用 infimum、近似比较器或声明存在条件；
- 可直接使用：若 $U_i\in[0,1]$ 独立同分布，则

  $$
  \Pr\!\left(\left|\frac1m\sum_{i=1}^mU_i-\mathbb EU_i\right|>t\right)
  \le 2e^{-2mt^2}.
  $$

## 二、评分与硬性通过标准

| 能力区 | 分值 | 题号 | 单项线 |
|---|---:|---|---:|
| A 定义、量词与事件 | 20 | 1—4 | 14/20 |
| B 手算、构造与界的解释 | 30 | 5—8 | 21/30 |
| C 完整上界证明 | 25 | 9—11 | 17/25 |
| D 反例、NFL 与下界审计 | 15 | 12—13 | 10/15 |
| E 陌生 AI 选择迁移 | 10 | 14 | 7/10 |
| **总分** | **100** |  | **80/100** |

同时满足：

1. A—E 各区达线且总分至少 80；
2. 第 9、10 题均不得低于本题 60%，否则说明两条有限类主证明尚未建立；
3. 第 10 题必须明确写出共同事件为何能覆盖 data-dependent ERM；
4. 第 11 题不得事后依测试结果设计 code/prior；
5. 第 12 或 13 题必须正确写出一个量词顺序或不可区分世界；
6. 三轨累计复现门、48 小时重建和 14 天迁移均通过后才可记 `retained`。

## 三、LT-09—16 覆盖矩阵

| ID | 节点 | 主要题号 |
|---|---|---|
| LT-09 | [[泛化间隙与浓缩不等式接口]] | 1、3、6、10、12、14 |
| LT-10 | [[PAC 学习定义与样本复杂度]] | 1、2、4、5、9、14 |
| LT-11 | [[有限假设类、Union Bound 与一致收敛]] | 1、3、6、10、12、14 |
| LT-12 | [[可实现情形的一致 ERM 保证]] | 4、5、9、12 |
| LT-13 | [[不可知 PAC、ERM 与双侧一致收敛]] | 4、6、10、12、14 |
| LT-14 | [[Occam 界、编码长度与先验权重]] | 4、7、11、12、14 |
| LT-15 | [[No-Free-Lunch 与归纳偏置]] | 2、12—14 |
| LT-16 | [[样本复杂度下界与 Minimax 视角]] | 2、4、8、12—14 |

### 三轨参数化模型族

| 轨道 | 有限模型 | 必须对齐的解析对象 |
|---|---|---|
| A 可实现排除 | 一个零风险 target，加 $M$ 个独立错误坐标的坏假设 | 单假设生存、任一坏假设生存的精确概率、Union Bound、指数证书与反解样本量 |
| B 不可知选择 | $K$ 个预先固定假设，各自 loss count 为 Binomial | 双侧共同事件、lexicographic ERM 的选择概率、期望总体/训练风险与 $2\alpha$ 证明桥 |
| C 编码与下界 | prefix-free 长度预算；Bernoulli 两点世界 | Kraft 权重半径、精确 total variation、最优二元检验误差与 Pinsker 接口 |

### 八层 PAC 证明账本

1. **学习对象：** $\mathcal Z,\mathcal H,\ell,A$ 的类型；
2. **允许世界：** 分布族、realizability/noise、i.i.d. 与 bounded loss；
3. **比较器：** 零风险 target、类内 oracle、Bayes 或其他对象；
4. **随机性：** $S\sim P^m$，以及 learner seed 是否进入概率空间；
5. **坏事件：** fixed-$h$、存在某个坏 $h$、supremum 或算法输出失败；
6. **合成机制：** survival、concentration、union/weighted union 或 testing reduction；
7. **反解：** 从 tail probability 到 $m(\varepsilon,\delta)$，常数、对数和量词不丢失；
8. **边界：** data dependence、无限类、shift、unbounded loss、computation 与 lower-bound problem class。

## 四、A 区：定义、量词与事件（20 分）

### 第 1 题：十个断言（5 分）

判断正误；错误时给出最小修正。每项 0.5 分。

1. 对每个 fixed $h$ 都有一个失败概率至多 $\delta$ 的事件，因此数据依赖输出 $h_S$ 的失败概率也至多 $\delta$。
2. Union Bound 要求各坏事件相互独立。
3. $\sup_{h\in\mathcal H}|R_S(h)-R_P(h)|\le\alpha$ 是一个关于整类的单一共同事件。
4. PAC 中 $\delta$ 是允许的风险误差，$\varepsilon$ 是失败概率。
5. Distribution-free 表示不需要 i.i.d.、bounded loss 或 hypothesis-class 限制。
6. Realizability 保证任何返回零训练误差假设的学习器都返回零总体误差假设。
7. 有限类可实现保证的 $1/\varepsilon$ 来源于坏假设连续避开其错误区域。
8. 不可知有限类 ERM 的一般 $1/\varepsilon^2$ 率来自对 noisy means 的双侧比较。
9. 若 $L(h)$ 是看完测试误差后才设计的短码，Occam 界仍然有效，因为 Kraft 和不等式仍成立。
10. 一个特定算法在一个分布上失败，已经证明该问题族的 minimax lower bound。

### 第 2 题：PAC、NFL 与 Minimax 的量词（5 分）

1. 写出 finite-class agnostic PAC 学习的完整量词骨架，至少包括 $\exists A$、$\forall\varepsilon,\delta$、$\forall P$、$\forall m\ge m_{\mathcal H}$ 和对 $S,U$ 的概率。（2 分）
2. 写出一个上界和一个 minimax 下界的量词顺序，并解释两者为何不是逻辑否定关系。（1.5 分）
3. 用量词说明 NFL 不是“现实中所有算法平均一样”，而是“若允许所有 labeling/世界，则不存在无条件统一外推”。（1.5 分）

### 第 3 题：四类事件与数据依赖（5 分）

设 $S\sim P^m$，loss 在 $[0,1]$，有限类 $\mathcal H=\{h_1,\ldots,h_M\}$ 在抽样前固定。

1. 写出 fixed-$h_j$ 双侧坏事件 $B_j$；（1 分）
2. 写出 uniform 坏事件，并证明它等于 $\bigcup_jB_j$；（1.5 分）
3. 说明共同好事件为何可以代入 $\widehat h(S)\in\mathcal H$，而只为某个预先固定 $h_j$ 写的事件不可以；（1.5 分）
4. 若候选类本身由同一 $S$ 自适应生成，指出原证明缺失的合同。（1 分）

### 第 4 题：四种学习制度与三种复杂度（5 分）

1. 区分 realizable PAC、agnostic PAC、consistent learner 与 exact/approximate ERM。（2 分）
2. 分别写出有限类可实现和不可知保证的典型 $m(\varepsilon,\delta)$ 阶，并说明它们控制的是总体风险还是 class excess。（1.5 分）
3. 区分 sample complexity、computational complexity 与 representation/approximation error；说明 PAC learnability 为什么不自动意味着高效可学。（1.5 分）

## 五、B 区：手算、构造与界的解释（30 分）

### 第 5 题：版本空间生存与可实现样本量（8 分）

一个有限二分类类含 target $h^*$ 和 $M=31$ 个坏假设。$R_P(h^*)=0$；每个坏假设风险恰为 $r=0.18$。为使精确事件可算，额外假设每个 observation 含 31 个相互独立的 Bernoulli$(r)$ 错误坐标，第 $j$ 个坏假设只在第 $j$ 坐标为 1 时出错。学习器从版本空间中任取一致假设。令 $m=28$。

1. 求某个固定坏假设仍一致的概率。（1 分）
2. 利用坐标独立性，写出至少一个坏假设仍一致的精确概率；再写 Union Bound。（2 分）
3. 用 $(1-r)^m\le e^{-mr}$ 得到指数上界，并比较三者的必然大小关系。（1.5 分）
4. 对一般 $M,r,\delta$，反解一个充分样本量。（1.5 分）
5. 解释“这里的 exact probability”依赖哪个额外构造，而有限类 PAC 定理本身为何只需要 Union Bound。（1 分）
6. 若每个坏假设只知道风险 $\ge r$，哪些等号要改成不等号？（1 分）

### 第 6 题：不可知 ERM、共同半径与选择偏差（8 分）

抽样前固定四个候选，真实 0–1 风险为 $(0.18,0.22,0.29,0.36)$。在同一个 $m=400$ 样本上，经验风险为 $(0.205,0.175,0.25,0.30)$，使用 lexicographic exact ERM，取 $\delta=0.05$。

1. 指出 ERM、类内 oracle 及这次输出的 class excess。（1.5 分）
2. 从 Hoeffding 与 Union Bound 推导 $1-\delta$ 共同半径 $\alpha$，给出数值近似。（2 分）
3. 在共同事件上逐行写出 $R_P(\widehat h)\le R_P(h^*_{\mathcal H})+2\alpha$。（2 分）
4. 当前给定的经验/总体数值是否落在共同事件内？分别检查四个 gap。（1 分）
5. 为什么观察到 $R_S(\widehat h)<R_P(\widehat h)$ 不等于 Hoeffding 失效？（0.75 分）
6. 若优化器只保证 $R_S(\widetilde h)\le\inf_hR_S(h)+\rho$，上界怎样改？（0.75 分）

### 第 7 题：Occam 权重与编码长度（8 分）

五个候选使用 prefix-free code lengths $(1,2,4,4,5)$；loss 在 $[0,1]$，评估样本量 $m=800$，总失败预算 $\delta=0.05$。

1. 检查 Kraft 和 $\sum_j2^{-L_j}\le1$。（1 分）
2. 给第 $j$ 个假设分配 $\delta_j=\delta2^{-L_j}$，由 Hoeffding 推导同时成立的半径 $\alpha_j$。（2 分）
3. 分别计算 $L=1$ 与 $L=5$ 的半径，并解释差异来自什么。（1.5 分）
4. 若编码还需 decoder、结构元数据和参数精度，为什么这些不能免费忽略？（1 分）
5. 解释该 prior weight 与 Bayesian posterior 的区别。（1 分）
6. 团队在看完 validation 结果后重新设计语言，使胜者编码最短。指出失败的独立性/预注册合同，并给出一种修复。（1.5 分）

### 第 8 题：Bernoulli 两点检验与下界接口（6 分）

世界 $-$ 产生 $m$ 个 Bernoulli$(1/2-\gamma)$ observations，世界 $+$ 产生 Bernoulli$(1/2+\gamma)$，两世界先验各 $1/2$。

1. 写出基于 count $K=\sum_iX_i$ 的 likelihood-ratio decision rule，并说明偶数 $m$ 的平票处理。（1.5 分）
2. 写出最优平均检验错误与 total variation 的关系。（1 分）
3. 计算单样本 $D_{KL}(P_-\|P_+)$，写出 product KL 与 Pinsker 给出的检验错误下界。（1.5 分）
4. 令 $\gamma=c/\sqrt m$，解释为什么两个世界的最优参数/动作虽相隔 $O(1/\sqrt m)$，却不能以任意高置信度区分。（1 分）
5. 要把检验下界变成分类 excess-risk 下界，还必须建立哪条 reduction/separation 关系？（1 分）

## 六、C 区：完整上界证明（25 分）

### 第 9 题：可实现有限类的一致学习器定理（8 分）

设 $|\mathcal H|=M<\infty$，0–1 loss，$S\sim P^m$，且存在 $h^*\in\mathcal H$ 满足 $R_P(h^*)=0$。学习器返回任意 $R_S=0$ 的假设。证明：若

$$
m\ge\frac{\log M+\log(1/\delta)}{\varepsilon},
$$

则以至少 $1-\delta$ 概率有 $R_P(A(S))\le\varepsilon$。必须显式写出：版本空间非空、固定坏假设的生存事件、对坏集合求并、算法失败事件的包含关系、指数界和反解。最后指出严格的 $>$/$\ge$ 边界怎样处理。（8 分）

### 第 10 题：不可知有限类 ERM 的双侧证明（9 分）

设 $|\mathcal H|=M<\infty$，loss 在 $[0,1]$，$S\sim P^m$。令 $\widehat h\in\arg\min_hR_S(h)$；若总体 argmin 不存在，可选 $h_\eta$ 满足 $R_P(h_\eta)\le\inf_hR_P(h)+\eta$。

1. 从 fixed-$h$ Hoeffding 和 Union Bound 构造 simultaneous event，并反解其半径。（3 分）
2. 在该事件上推导 exact ERM 的 class excess 至多 $2\alpha+\eta$，逐步标注两次 generalization 与一次 ERM 比较。（3 分）
3. 令目标 excess 为 $\varepsilon$，选择 $\alpha$ 和 $\eta$ 后给出一个充分样本量；解释 $1/\varepsilon^2$。（2 分）
4. 说明若候选集或 loss 由同一数据自适应生成，原 proof event 为什么可能不再覆盖。（1 分）

### 第 11 题：可数类的 weighted Hoeffding/Occam 界（8 分）

设 $\mathcal H$ 可数，抽样前固定权重 $\pi(h)>0$ 且 $\sum_h\pi(h)\le1$，loss 在 $[0,1]$。

1. 对每个 $h$ 选择不同半径，使其双侧坏事件概率至多 $\delta\pi(h)$；对可数并集证明同时界。（3 分）
2. 令 $\pi(h)=2^{-L(h)}$，用 Kraft inequality 写出 description-length 形式。（2 分）
3. 给出用该界构造 upper-confidence penalized ERM 的一种合法 score，并说明它保证的比较对象。（1.5 分）
4. 说明 prefix-free、预先固定语言、完整可解码描述三项为何是定理合同而非审美偏好。（1.5 分）

## 七、D 区：反例、NFL 与下界审计（15 分）

### 第 12 题：五个研究声明审计（10 分）

每项 2 分：指出声明缺失的 theorem contract，给出最小反例或修正版，并说明现有证据最多支持什么。

1. “我们从 10 万个 prompt 中选择验证误差最低者；对最终 prompt 用单模型 Hoeffding，所以置信度是 95%。”
2. “网络插值训练集，因此处于 realizable PAC 制度，样本复杂度按 $1/\varepsilon$。”
3. “模型压缩后文件更小，所以 Occam theorem 证明其因果上更接近真实机制。”
4. “某优化器在一个难数据集失败，所以我们已经证明了所有学习算法的 minimax 下界。”
5. “No-Free-Lunch 说明所有架构在自然图像上长期平均性能相同，因此归纳偏置不重要。”

### 第 13 题：有限域 NFL 构造与归纳偏置（5 分）

取 $2m$ 个输入点，允许其上所有二元 labeling，训练分布均匀，学习器可随机。

1. 说明为什么一个大小为 $m$ 的样本至多观察 $m$ 个不同点，因此至少 $m$ 个点未被观察。（1 分）
2. 对未见点随机赋标签，解释任意学习器在这些点上的平均错误为何为 $1/2$。（1.5 分）
3. 由对 targets 的平均风险推出至少存在一个固定 hard target；说明其仍然 realizable。（1 分）
4. 给出两个现实 AI 归纳偏置，并明确它们排除了或偏好了哪些函数/世界。（1.5 分）

## 八、E 区：陌生 AI 选择迁移（10 分）

### 第 14 题：大模型 prompt/checkpoint 选择合同（10 分）

一个团队有 2,000 个固定 checkpoint，每个 checkpoint 又由自动 agent 在同一 validation benchmark 上产生至多 50 个 prompt；agent 会看到前一轮 score 并继续搜索。最终模型在该 benchmark 胜出后，只在同一 benchmark 上报告 95% Hoeffding interval。请设计一份可审计的评价方案：

1. 写出 target population、loss、candidate-generation algorithm、selection rule 和 reported estimand；（2 分）
2. 画出数据反馈图，指出固定有限类 Union Bound 可以覆盖哪一部分，不能覆盖哪一部分；（2 分）
3. 给出至少两种修复路径，例如预注册有限库、fresh holdout、嵌套切分、reusable holdout/DP 或复杂度控制，并写明各自新增假设；（2 分）
4. 若用编码/先验权重，列出完整描述必须包含的对象，并说明权重何时冻结；（1.5 分）
5. 设计一个下界问题：给出两个几乎不可区分但最优选择不同的部署世界，说明用 Le Cam 需要验证的 closeness 与 decision separation；（1.5 分）
6. 明确最终声明不覆盖 distribution shift、无界生成 loss、计算失败中的哪些部分。（1 分）

## 九、20 分钟卷级口试

评分者从下列六项随机抽四项，每项 5 分；15/20 通过，且“量词”和“两条率”不得为 0：

1. 不看笔记写出 agnostic PAC 的完整量词；
2. 用事件而非口号解释 fixed-$h$ 为什么不能直接覆盖 $h_S$；
3. 三分钟恢复可实现有限类的 survival proof；
4. 三分钟恢复不可知 ERM 的 two-gap bridge；
5. 解释 prefix-free code 如何变成失败预算；
6. 对照上界、NFL 与 Le Cam 的量词方向。

## 十、答案与输出隔离协议

1. 建立 `attempt_id = PAC-CUM-01-YYYYMMDD-HHMM`；记录开始/结束时间；
2. 完成口试与闭卷后，将原稿导出只读文件并记录 SHA-256；
3. 在冻结前不得打开[[阶段测验解答 - PAC 学习与有限假设类（20.2）]]，不得运行 canonical gate；
4. 评分者在原稿冻结后公布 `scorer nonce`，由 nonce 指定主轨和盲参数轨；
5. 学习者先提交解析预测区间、单调性和边界，再运行脚本；
6. canonical stdout/SVG 只能用于材料回归，不得充当个人首次预测；
7. 订正另页保存，不覆盖首次原稿与首次输出。

## 十一、48 小时与 14 天复测

### 48 小时换机制重建门

随机抽取一项：

- 把 Track A 从等风险坏假设改为不同 $r_j$，重建精确/Union 公式；
- 把 Track B 从 exact ERM 改为 $\rho$-approximate ERM，重建比较桥；
- 把 Track C 的固定长度码改为分层 code，重新检查 Kraft；
- 把 Bernoulli 两点世界换成 Gaussian 均值两点世界，重建 KL/TV 接口。

不得只改数字；必须改一处机制并说明原证明哪一行改变。

### 14 天陌生 AI 迁移门

从未在本卷出现的新场景中任选一项：adaptive benchmark、检索器选择、工具调用策略选择、model routing、safety red-team selection。提交八层 PAC 证明账本、一个合法上界路线、一个不可识别/下界路线、一个可证伪实验。评分低于 7/10 时，卷状态退回 `attempted`。

## 十二、提交证据清单

- [ ] 口试录音/文字稿、抽题记录与评分；
- [ ] 210 分钟闭卷原稿、时间戳与 SHA-256；
- [ ] `attempt_id`、`scorer nonce` 与轨道映射；
- [ ] 运行前解析预测、单调性和边界说明；
- [ ] 至少两个轨道的非 canonical stdout、SVG 与 hash；
- [ ] 逐题评分、首错位置和订正页；
- [ ] 48 小时换机制证据；
- [ ] 14 天陌生迁移证据；
- [ ] 学习状态更新记录；
- [ ] 若申请逐节点 `verified`，另附 LT-09—16 的独立口述或新题证据。

> [!warning] 最终状态边界
> 本页的 `material_status: regression-passed` 不等于学习者通过。本页加入仓库后，20.2 仍保持 `draft / not-attempted`，直至上述原始证据真实存在。

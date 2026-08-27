---
type: solution
status: verified
area: [language-models, evaluation, robustness]
topic: "[[Contamination、Prompt Sensitivity、Robustness 与不确定性]]"
exercise: "[[习题 - Contamination、Prompt Sensitivity、Robustness 与不确定性]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Contamination、Prompt Sensitivity、Robustness 与不确定性

## A. 识别与复述

### LM63-A01
Exposure 是训练数据包含 benchmark 或其变体；memorization 是参数保留可提取信息；exploitation 是测试时利用该信息提高得分。Exposure 不保证记住，记住不保证当前 prompt 能利用，行为信号也可能有其他原因，三者不能互作同义词。

### LM63-A02
Exact 是字符串/规范化后完全重合；near-duplicate 是轻微编辑、模板替换或局部复制；semantic 是改写但含同一题；label/answer 是答案键、解释或评测标签泄漏；format contamination 是规范题序、选项位置或 benchmark 特有模板进入训练。每类需不同检测器与阈值。

### LM63-A03
平均表现对一个声明的 prompt 分布求期望；worst-case 取允许集合最低值；方差描述敏感度；best-prompt 是搜索/选择后的最大值。它们回答典型、保底、稳定与调优潜力四种不同问题。

## B. 手算与构造

### LM63-B01
均值为 $.6$。Population variance 为
$$[(.2)^2+0^2+(-.2)^2]/3=.026\overline6,$$
standard deviation 约 $.1633$；range 为 $.8-.4=.4$；worst-case 为 $.4$。

### LM63-B02
Canonical accuracy 为 $.80$；置换 accuracy 为 $310/500=.62$；差值为 $.18$（18 个百分点）。区间应以 item 为 cluster，而不是把 500 次置换全当独立题。

### LM63-B03
把 6 格平铺，均值为 $4/6=.667$。先按 item：item 1 均值 $.8$、item 2 均值 $0$，再等权为 $(.8+0)/2=.4$。平铺给拥有更多 prompt 的 item 更大权重。

## C. 推导与证明

### LM63-C01
一种教学分解是
$$
y_{ips}=\mu+a_i+b_p+(ab)_{ip}+c_s+\epsilon_{ips},
$$
$a_i$ 是 item 难度，$b_p$ 是 prompt 总体效应，交互项表示不同 item 对 prompt 反应不同，$c_s$ 是 seed/run 影响，$\epsilon$ 是剩余误差。若 prompt 或 seed 不可交换，还需固定效应或更具体协方差结构。

### LM63-C02
Canonical-order drop 也可能由答案位置偏好、tokenization、上下文学习格式对齐、随机方差或置换后 parser bug 造成。因此观察到 drop 只与“利用 canonical 特征”相容，不能唯一识别训练 exposure；需数据谱系、重叠和其他行为证据。

### LM63-C03
对每个 item 计算配对差 $d_i=m_i^A-m_i^B$。零假设若意味着 A/B 标签在 item 内可交换，则随机独立翻转 $d_i$ 符号，生成 $\bar d$ 的零分布；p 值为同等或更极端比例。配对单位是独立 item/user cluster，不是同题的多个 prompt cell。

## D. 边界、反例与纠错

### LM63-D01
一个从未见 benchmark 的模型也可能普遍偏好选项 C；canonical 数据恰把正确答案更多放 C，置换后优势消失。Probe 显著，但原因是位置偏差，不是污染。

### LM63-D02
训练语料可能含 paraphrase、翻译、答案解析、截图/OCR、只含 label 的表格或共享上游源，exact overlap 均为零。还可能在清洗后无法追溯。零 exact match 只排除某个检测器阈值下的一类重合。

### LM63-D03
最高分同时包含真实 prompt 效果与 100 次测量噪声的最大值，后者期望为正；若把它当预先指定 prompt 的表现会乐观。应分开发/测试、报告搜索预算和全部分布，或做 nested evaluation。

## E. AI 迁移

### LM63-E01
组合证据可含：公开训练截止/数据卡；题目与已知网页的 exact/near/semantic overlap；生成题目续写/异常 verbatim 探针；canonical-order vs permutation；新写等价题/时间后置题；受控 prompt 变化。每项保留替代解释，最后分级而非二元宣判。

### LM63-E02
先定义允许的语义保持 prompt 因子和组合分布，冻结模板生成器与数量。运行完整 item×prompt（必要时×seed）矩阵；bootstrap 先重采样 item cluster，再按目标 prompt 分布重采样 prompt，重算 mean/worst quantile/variance；披露失败和 family 外推边界。

### LM63-E03
构造冻结基线和四个单因素变体：只改 model、只改 template、只改 decoder、只改 judge；再加全量候选。用同一 item IDs、原始输出和 paired effect 定位差异；judge-only 变体复评分同一输出，model/decoder 变体则保留新 trace。

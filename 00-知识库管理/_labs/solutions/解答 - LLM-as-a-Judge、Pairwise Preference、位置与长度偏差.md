---
type: solution
status: verified
area: [language-models, evaluation, llm-as-judge]
topic: "[[LLM-as-a-Judge、Pairwise Preference、位置与长度偏差]]"
exercise: "[[习题 - LLM-as-a-Judge、Pairwise Preference、位置与长度偏差]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - LLM-as-a-Judge、Pairwise Preference、位置与长度偏差

## A. 识别与复述

### LM62-A01
可写
$$
J\sim q_j(\cdot\mid x,y_A,y_B,o,r,s),
$$
其中 $x$ 是题目，$y_A,y_B$ 是内容，$o$ 是展示顺序，$r$ 是 rubric/judge prompt，$s$ 是 judge sampling 状态；输出含 A/B/tie/invalid。Judge model/date、parser 与隐藏元信息也属于测量仪器版本。

### LM62-A02
位置一致率是 AB/BA 两次是否选择同一内容；交换翻转率是仅交换位置就改选另一内容的比例；win rate 是某系统的胜数按预定 tie 规则除以有效比较；tie rate 是平局分母占比。Parse failure 要另报，不能静默删。

### LM62-A03
更长答案可能包含更多真实解释，因此 system→length→quality→judge 是合理中介；judge 也可能无关地偏好冗长，形成 length→judge 直接偏差。控制长度会删除一部分真实总效应，故原始与 length-controlled estimand 都要报告。

## B. 手算与构造

### LM62-B01
题面把三类 pair 明确分开，因此 content-consistency 为 $70/100=.70$，position-flip 为 $.20$，至少一次 tie 的 pair 比例为 $.10$。若一对可能同时落入多类，定义就必须改为互斥优先级。

### LM62-B02
Ties 计半胜：
$$
(45+.5\times20)/100=.55.
$$
排除 ties：$45/(45+35)=45/80=.5625$。二者的 estimand 与分母不同，应同时给 tie rate $.20$。

### LM62-B03
Observed agreement 为 $60/80=.75$。两者 A/B 边际都为 $(.5,.5)$，独立同边际下 chance agreement 为 $.5^2+.5^2=.5$。若计算 Cohen's $\kappa$，则 $(.75-.5)/(1-.5)=.5$。

## C. 推导与证明

### LM62-C01
Bradley–Terry 写作
$$
\Pr(i\succ j)=\sigma(s_i-s_j)=\frac{e^{s_i}}{e^{s_i}+e^{s_j}}.
$$
所有 $s_i$ 加同一常数不改变概率，所以只识别相对尺度。若比较图不连通，不同连通分量之间从未比较，其相对平移任意，跨分量强弱不可识别。

### LM62-C02
系统可能通过产生更完整的长答案提高质量，因此 length 是 treatment mediator。回归 $J\sim system+length$ 的 system 系数更接近某种 controlled direct effect，而不再是“采用该系统（包括其长度变化）”的 total effect；还需要无未测 mediator-outcome confounding 等强假设。

### LM62-C03
对每个固定 $(x,y_A,y_B)$ 随机令 $o\in\{AB,BA\}$，内容不变，平均判决差可归因于位置分配。需假设随机化正确、一次顺序不影响另一次、judge/版本稳定、parser 对两序对称且没有内容中泄漏的系统身份。

## D. 边界、反例与纠错

### LM62-D01
总体 1000 对中普通题 950 对 agreement 95%，安全题 50 对仅 20%；总体仍有 $(902.5+10)/1000\approx91.25\%$，看似很高，却在关键 slice 不可用。上线门必须给安全 slice 独立阈值。

### LM62-D02
Temperature 0 只减少某类采样随机性；judge 仍会有 rubric 偏差、位置/长度/自偏好、知识错误、解析错误和版本漂移。确定性地重复同一错误不是无误差。

### LM62-D03
反复用 judge test win rate 选择 prompt/checkpoint，等价于对 judge 噪声和偏好过拟合。最终同一 test 不再独立。应分开发集 judge 与冻结测试，或用新的人类锚点/新题确认，并披露选择次数。

## E. AI 迁移

### LM62-E01
每题保存 pair_id、匿名 answer hashes、AB 与 BA judge inputs、judge model/date/rubric/seed、原始输出、parser 标签、A/B/tie/invalid、内容一致/翻转标记、答案长度与人类标签。预注册 tie 和双 invalid 的分母规则。

### LM62-E02
主分析报告随机位置下的总 win rate。敏感性分析在预注册长度区间内匹配 pairs，或报告长度分层 win rate/带交互回归；不能只报“扣除长度”后的有利数值。解释其为受控比较，不等同于部署总效应。

### LM62-E03
按语言×长度×安全风险分层抽 pairs，人工盲评、随机位置、至少双标并保留 disagreement。每 slice 报 judge-human agreement、confusion、tie/invalid 与 cluster interval；样本量优先保证高风险 slice 的最低精度。

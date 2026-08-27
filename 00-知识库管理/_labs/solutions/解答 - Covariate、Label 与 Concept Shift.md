---
type: solution
status: draft
topic: "[[习题 - Covariate、Label 与 Concept Shift]]"
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - Covariate、Label 与 Concept Shift
## A
### LT-SHF-A01
Covariate：$p_s(x)\ne p_t(x),p_s(y|x)=p_t(y|x)$；label：$p_s(y)\ne p_t(y),p_s(x|y)=p_t(x|y)$；concept：$p_s(y|x)\ne p_t(y|x)$。它们可重叠。
### LT-SHF-A02
Bayes 给 $p_t(y|x)\propto p_s(x|y)p_t(y)$，prior 改变通常改变 posterior；保持的是 $P(X|Y)$。
### LT-SHF-A03
Detection 发现可观测差异；diagnosis 判断 joint factor；correction 依赖识别假设；evaluation 用 locked target labels 验风险。
## B
### LT-SHF-B01
posterior odds 修正因子为
$$
\frac{\pi_t(1)/\pi_t(0)}{\pi_s(1)/\pi_s(0)}
=\frac{1}{0.2/0.8}=4.
$$
### LT-SHF-B02
解 $C\pi=\mu$：由 $.8p+.2(1-p)=.62$ 得 $p=.7$，故 $\pi_t=(.7,.3)^T$。
### LT-SHF-B03
取 source 只支持 $[0,1]$、target 在 $[2,3]$ 有正质量；该区 $p_s=0$，ratio 未定义，source labels 不识别 target conditional。
## C
### LT-SHF-C01
改变 $P(X)$ 保持 $P(Y|X)$ 可不保持 $P(X|Y)$；改变 priors 保持 $P(X|Y)$ 又通常改变 $P(Y|X)$，故互不蕴含。
### LT-SHF-C02
World A 改 class prior；World B 保持 prior 但在一部分 $x$ 翻转 label rule。可调参数使模型 predicted-positive frequency 相同，故该频率不识别 shift type。
### LT-SHF-C03
新医院改变年龄分布、疾病 prevalence 与诊断阈值，分别对应三项同时改变。
## D
### LT-SHF-D01
可比较 $P_s(X),P_t(X)$；无 target labels 时不能直接验证 $P(Y|X)$ 或 $P(X|Y)$ 稳定，也不能区分 label 与 concept shift。
### LT-SHF-D02
随机打乱泄漏未来并平均 drift；用时间前缀训练、随后窗口 calibration、未来 locked test，按 label arrival time 截断，并做 rolling audit。
### LT-SHF-D03
近奇异 $C$ 表示预测器不能区分类，逆解放大频率噪声且可能出 simplex；报告 condition number，用 constrained/regularized solve，并承认 class priors 未稳定识别。
## E
### LT-SHF-E01
分别监控 input/site metadata、疾病 prior、label/诊断规则版本、治疗/审核 policy；按 patient/time unit 获得延迟 labels，做 group calibration/risk。
### LT-SHF-E02
记录 propensity 与 action：模型分数→曝光 $A$→点击/购买 $Y$→再训练数据；只在 observed exposure 上的 label law 有 selection bias，需 policy-aware evaluation。
### LT-SHF-E03
card 写 source/target unit、可观测差异、假定稳定 factor、overlap/可逆性、估计方法、选择数据与 locked target risk；不把 detection 写成 diagnosis。

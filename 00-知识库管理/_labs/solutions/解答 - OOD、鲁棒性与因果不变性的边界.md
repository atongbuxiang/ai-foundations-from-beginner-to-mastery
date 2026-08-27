---
type: solution
status: draft
topic: "[[习题 - OOD、鲁棒性与因果不变性的边界]]"
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - OOD、鲁棒性与因果不变性的边界
## A
### LT-OOD-A01
分别预测错误事件、分布来源、拒答行动、指定扰动/自然域风险和结构机制稳定；评价对象与量词均不同。
### LT-OOD-A02
OOD是两分布关系；改变 $P_{\rm out}$ 会改变 score ranking，甚至可令 out=in。
### LT-OOD-A03
AUROC是pair ranking；AUPR依赖positive/prevalence；FPR@TPR是阈值点；calibration连接score与频率；utility加入先验与成本。
## B
### LT-OOD-B01
16对中 out score胜：对 .3 胜2，对 .5胜3，对 .7胜3，对 .9胜4，共12，AUROC=.75。
### LT-OOD-B02
average error $=.9(.05)+.1(.40)=.085$；worst-group=.40。
### LT-OOD-B03
$0.95^{20}\approx0.358$。单步95%不能称整轨迹95%安全。
## C
### LT-OOD-C01
若 out=in，任何 statistic 两类分布相同，ROC对角、AUROC=.5；故无结构 universal detector 不可得。
### LT-OOD-C02
ReLU网络在训练support外可沿某方向令一个logit线性增长，softmax趋近1，虽无训练密度。
### LT-OOD-C03
两训练环境中 spurious $S=Y$，causal $C$有少量噪声；算法选$S$。新环境令$S=1-Y$，训练不变性未识别因果。
## D
### LT-OOD-D01
补 in/out生成与near/far语义、样本unit、prevalence、AUPR方向、FPR@TPR/CI、threshold选择、error-probability calibration、拒答成本与新out families。
### LT-OOD-D02
先拟合 source accuracy→target accuracy基线趋势，再报 raw target accuracy与相对趋势残差；统一architecture/data/compute并在多natural shifts复核。
### LT-OOD-D03
需变量/SCM、环境与intervention targets、稳定机制、隐藏混杂/测量假设、识别定理、negative controls和真正干预测试；marginal alignment不够。
## E
### LT-OOD-E01
event定义为可验证答案错误；out families按时间/topic/source；报告 correctness calibration、risk–coverage、verification delay与人工审核utility，按问题源cluster。
### LT-OOD-E02
用医院/时间自然split，报average/worst group risk、NLL/reliability、conformal coverage/width和review cost；target test锁定。
### LT-OOD-E03
五级依次是 benchmark ranking、operational utility、多natural-shift风险、environment-family guarantee、SCM/intervention causal identification；每级只报告已有证据。

---
type: exercise
status: draft
area: [generative-models, diffusion, flow-matching, evidence]
topic: "[[Diffusion、Flow、速度参数化与统一证据地图]]"
solution: "[[解答 - Diffusion、Flow、速度参数化与统一证据地图]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Diffusion、Flow、速度参数化与统一证据地图
## A. 识别与复述
### GEN56-A01
列出审计连续生成方法必须分开的七个对象。
### GEN56-A02
区分同边缘、同路径律、同 population minimizer、同 finite sampler。
### GEN56-A03
写出 Gaussian path 的 data/noise/score/instantaneous velocity 换算。
## B. 手算与建模
### GEN56-B01
$\alpha=\cos\phi,\sigma=\sin\phi$ 时证明 diffusion $v$-parameterization 等于 $dX/d\phi$。
### GEN56-B02
取 $\alpha(t)=1-t,\sigma(t)=t^2$，比较 instantaneous velocity 与 $\alpha\epsilon-\sigma X_0$，给出不相等的具体点。
### GEN56-B03
给定 transport velocity $v=-x$、score $s=-2x$、$\varepsilon=0.3$，写出同边缘 SDE 的 drift 与 diffusion coefficient。
## C. 推导与证明
### GEN56-C01
证明 $dX=(v+\varepsilon s)dt+\sqrt{2\varepsilon}dW$ 与 ODE $\dot X=v$ 共享密度方程。
### GEN56-C02
说明 Score-SDE 的 $f$ 如何由 PF velocity 与 $g^2s/2$ 恢复。
### GEN56-C03
证明可逆线性 target 换算通常会改变未加权 MSE 的 metric。
## D. 边界、反例与纠错
### GEN56-D01
反驳“同 $p_t$ 的所有连续生成模型具有同一 coupling”。
### GEN56-D02
反驳“输出可逆换算，所以训练程序完全等价”。
### GEN56-D03
反驳“统一框架本身能够预测 benchmark 上谁更好”。
## E. AI 迁移
### GEN56-E01
为“模型 A 等价模型 B”的论文主张写六字段审计模板。
### GEN56-E02
设计 data/noise/score/velocity conversion 的 property-based tests。
### GEN56-E03
为 50.7 的方法比较建立 identity/theorem/idealization/numerical/experiment/hypothesis 六级证据表。
## 解答入口
[[解答 - Diffusion、Flow、速度参数化与统一证据地图]]

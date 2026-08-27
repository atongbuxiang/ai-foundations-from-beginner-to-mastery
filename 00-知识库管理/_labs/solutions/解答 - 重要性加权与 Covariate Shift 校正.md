---
type: solution
status: draft
topic: "[[习题 - 重要性加权与 Covariate Shift 校正]]"
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - 重要性加权与 Covariate Shift 校正
## A
### LT-IW-A01
若 $P_t(Y|X)=P_s(Y|X)$ 且 $P_t^X\ll P_s^X$，$w=p_t/p_s$，则 $R_t(f)=E_s[w(X)\ell(f(X),Y)]$。
### LT-IW-A02
true ratio 给精确期望；estimated 有 ratio error；clipped $\min(w,c)$ 有 tail bias；self-normalized 用 $\sum w\ell/\sum w$，稳定但有限样本有偏。
### LT-IW-A03
无偏只对固定 $f$ 的 risk estimator；ERM 还含高方差、uniform selection、ratio estimation、optimization 与 model misspecification。
## B
### LT-IW-B01
unnormalized $n^{-1}\sum w_i\ell_i=(1+7)/4=2$；self-normalized $8/10=.8$；ESS $=10^2/(1+1+1+49)=100/52\approx1.923$。
### LT-IW-B02
balanced 时 $w=.8/.2=4$；$\rho=.2$ 时 $w=(.8/.2)(.8/.2)=16$。
### LT-IW-B03
$$
R_t-E_s[w_c\ell]=E_s[(w-c)_+\ell]\le LE_s[(w-c)_+].
$$
tail expectation 是被 clipping 删除的 target mass 加权上界。
## C
### LT-IW-C01
把 $p_t(y|x)p_t(x)$ 换为 $p_s(y|x)w(x)p_s(x)$ 后积分即得。
### LT-IW-C02
source 稀有事件概率 $\epsilon$、weight $1/\epsilon$、loss 1，其余 loss 0；期望为 1，但单样本变量方差 $1/\epsilon-1$ 爆炸。
### LT-IW-C03
令 source=target 的 $P(X)$，故 $w=1$，但 target 把 $Y=X$ 改为 $Y=1-X$；加权 source risk仍无法等于 target risk。
## D
### LT-IW-D01
用独立 input folds 拟合 ratio并给 held-out source 打权；模型训练后在独立 weighted validation 选 ratio/clip/model；最后 target labeled test 一次评估。
### LT-IW-D02
报告 min/max、quantiles、second moment、ESS、top-weight mass、support/domain-classifier separability、clip proportion 与 group/time分层。
### LT-IW-D03
odds 依赖概率校准分类器；KMM匹配选定 RKHS moments；density plug-in受高维密度误差。三者都不验证 $P(Y|X)$ 稳定或支持覆盖。
## E
### LT-IW-E01
预注册多个 $c$，画 ESS、max weight、weighted target-like validation 与 locked target risk；按 hospital/patient bootstrap，并报告无 clipping baseline。
### LT-IW-E02
propensity 很小时 weights 爆炸，无曝光 action 的结果不可识别；policy feedback 又可能改变 response law，需 exploration/logging 与 off-policy assumptions。
### LT-IW-E03
card 写 conditional stability、overlap、ratio estimator、cross-fit、tail/ESS、clip/SN、selection与target test；拒绝 concept-shift 修复和 support 外保证。

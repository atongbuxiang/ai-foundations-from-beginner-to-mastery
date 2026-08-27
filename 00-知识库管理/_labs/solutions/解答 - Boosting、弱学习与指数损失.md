---
type: solution
status: draft
topic: "[[习题 - Boosting、弱学习与指数损失]]"
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - Boosting、弱学习与指数损失
## A
### LT-BST-A01
$D_1(i)=1/m$；$\varepsilon_t=\sum_iD_t(i)\mathbf1\{h_t(x_i)\ne y_i\}$；$\alpha_t=\frac12\log((1-\varepsilon_t)/\varepsilon_t)$；$Z_t=\sum_iD_t(i)e^{-\alpha_ty_ih_t(x_i)}$；$D_{t+1}(i)=D_t(i)e^{-\alpha_ty_ih_t(x_i)}/Z_t$；最终 $H_T=\operatorname{sign}\sum_t\alpha_th_t$。
### LT-BST-A02
$\exists\gamma>0,\ \forall D\in\Delta_m,\ \exists h\in\mathcal H$ 使 $\Pr_{i\sim D}(h(x_i)\ne y_i)\le1/2-\gamma$。均匀分布 51% 只验证一个 $D$，boosting 后续会产生高度非均匀的 $D_t$。
### LT-BST-A03
AdaBoost 顺序重加权并优化指数势能；bagging 并行 bootstrap 聚合；random forest 是 randomized trees 的 bagging；gradient boosting 是一般 loss 的 stagewise function optimization。它们的随机性、目标和保证不同。
## B
### LT-BST-B01
$\alpha=\frac12\log3\approx0.5493$；$Z=2\sqrt{0.25(0.75)}=\sqrt3/2\approx0.8660$；$Z^{10}=(3/4)^5=243/1024\approx0.2373$。
### LT-BST-B02
$e^{-0.02T}\le0.01$，故 $T\ge\log100/0.02\approx230.26$，最少 231 轮。
### LT-BST-B03
正确点各乘 $e^{-\alpha}=1/\sqrt2$，错误点乘 $e^\alpha=\sqrt2$。未归一 weights 比为 $(1,1,2)$，故 $D_2=(1/4,1/4,1/2)$。
## C
### LT-BST-C01
$Z(\alpha)=(1-\varepsilon)e^{-\alpha}+\varepsilon e^\alpha$。令导数零得 $e^{2\alpha}=(1-\varepsilon)/\varepsilon$，故 $\alpha^*=\frac12\log((1-\varepsilon)/\varepsilon)$；代回两项各为 $\sqrt{\varepsilon(1-\varepsilon)}$，总和 $2\sqrt{\varepsilon(1-\varepsilon)}$。
### LT-BST-C02
递推给 $D_{T+1}(i)=D_1(i)\exp[-\sum_t\alpha_ty_ih_t(x_i)]/\prod_tZ_t$。用 $D_1=1/m$、$F_T=\sum_t\alpha_th_t$，对 $i$ 求和并令 $\sum_iD_{T+1}(i)=1$，得到 $m^{-1}\sum_ie^{-y_iF_T(x_i)}=\prod_tZ_t$。
### LT-BST-C03
$\mathbf1\{y_iF_T(x_i)\le0\}\le e^{-y_iF_T(x_i)}$，故 training error $\le\prod_tZ_t$。写 $\varepsilon_t=1/2-\gamma_t$，则 $Z_t=\sqrt{1-4\gamma_t^2}\le e^{-2\gamma_t^2}$；连乘即结论。
## D
### LT-BST-D01
永久错标点的 margin 越来越负，factor $e^{-yF}$ 越来越大；归一化后 $D_t$ 集中到该点，weak learner 被迫反复拟合无法同时满足的约束。指数 loss 对大负 margin 的梯度不封顶，因此该点可主导后续规则。
### LT-BST-D02
product bound 只控制训练指数/0–1 error。继续训练可能改善 margin，也可能追逐噪声；test error 还依赖 base-class complexity、样本抽取、margin distribution、round selection 和 validation reuse。必须用独立 test/合法 generalization theorem。
### LT-BST-D03
若二分类 hypothesis 可取反，error $>1/2$ 的 $h_t$ 可翻转成 $<1/2$；若恰为 $1/2$ 则 edge 为零、$\alpha=0$。但若 hypothesis class 在某些 $D_t$ 上无 edge、估计误差导致假 edge，或多分类规则不能简单取反，weak assumption 仍失败。
## E
### LT-BST-E01
以 query 为样本，$D_t$ 按当前 ensemble 的错误/低 margin 重加权；base model 在该分布的质量 error 必须有 edge；loss 需合并质量、延迟与成本。若只调用部分模型，未观察结果使训练变成 bandit feedback，原 full-label AdaBoost 不可直接用。
### LT-BST-E02
指数 loss $e^{-m}$ 对负 margin 的梯度幅值 $e^{-m}$ 无界增长；logistic $\log(1+e^{-m})$ 的 margin 导数幅值趋近 1。故 logistic 对极端错标点更缓和，但仍非自动 robust。
### LT-BST-E03
claim card：训练样本和 label；对所有 reweightings 的 edge/estimation；base class；指数或其他 loss；$\alpha$ 与 rounds/stopping；noise handling；training product bound；独立的 margin/generalization/test evidence。

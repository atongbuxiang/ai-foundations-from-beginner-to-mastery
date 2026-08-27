---
type: solution
status: draft
topic: "[[习题 - Online-to-Batch Conversion]]"
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - Online-to-Batch Conversion
## A
### LT-OTB-A01
$Z_1,ldots,Z_T\overset{iid}\sim P$，$h_t$ 是 $\mathcal F_{t-1}=\sigma(Z_1,ldots,Z_{t-1})$-measurable。于是 $E[\ell(h_t,Z_t)\mid\mathcal F_{t-1}]=L(h_t)$。若 $h_t$ 偷看当前 label，此式一般失败。
### LT-OTB-A02
randomized iterate 独立均匀选一个 $h_I$；averaged predictor 在凸预测空间取 $T^{-1}\sum h_t$ 并靠 Jensen；last iterate 是 $h_T$，不受平均保证自动控制。
### LT-OTB-A03
expectation 覆盖 iid sample、online algorithm 内部随机性，以及输出 index $I$。若 environment/algorithm 有额外随机性也须列出；comparator 若固定，不对其另取选择随机性。
## B
### LT-OTB-B01
$4/\sqrt T\le0.02$，故 $\sqrt T\ge200$、$T\ge40{,}000$。
### LT-OTB-B02
均匀随机 iterate 的 expected risk 为 $(0.1+0.2+0.6)/3=0.3$。
### LT-OTB-B03
average risk 为 $1/T\to0$，last risk 恒为 1。该反例说明平均/随机 iterate theorem 不可改写成 last-iterate theorem。
## C
### LT-OTB-C01
对固定 $h$，expected regret 给 $E\sum_t\ell(h_t,Z_t)\le E\sum_t\ell(h,Z_t)+B_T$。条件期望把左边每项变为 $E L(h_t)$，iid 把右边变为 $T L(h)$。除以 $T$，再用独立均匀 $I$ 的 $E L(h_I)=T^{-1}\sum_tE L(h_t)$，最后对 $h$ 取 infimum。
### LT-OTB-C02
若预测可逐点平均且 $\ell(\cdot,z)$ 凸，$\ell(T^{-1}\sum_th_t,z)\le T^{-1}\sum_t\ell(h_t,z)$。对 $z\sim P$ 取期望，再代入平均 online-to-batch bound 即得。
### LT-OTB-C03
令 $X_t=L(h_t)-\ell(h_t,Z_t)$，则为 bounded martingale difference。Azuma/Hoeffding 控制 $T^{-1}\sum X_t$；regret 把 online empirical loss 换为固定 $h^*$ 的 empirical loss；再用独立 Hoeffding 控制 $T^{-1}\sum\ell(h^*,Z_t)-L(h^*)$。两事件 union bound 后得到 $B_T/T+O(\sqrt{\log(1/\delta)/T})$，两项来源不可合并隐藏。
## D
### LT-OTB-D01
若先用 $Z_t$ 更新再评分，$h_t$ 已依赖 $Z_t$，不再是 $\mathcal F_{t-1}$-measurable；当前样本不是 fresh test point，$E[\ell(h_t,Z_t)\mid\mathcal F_{t-1}]$ 不等于其 population risk，可能严重乐观。
### LT-OTB-D02
所选 checkpoint index 是 online losses 的函数，等价于数据依赖 comparator。对每个固定 checkpoint 的单点浓缩不能覆盖选择后的最大偏差；需独立 validation、uniform/union bound、complexity penalty 或 anytime-valid selection。
### LT-OTB-D03
random permutation 要用无放回/剩余总体浓缩；时间序列需 mixing、martingale process 或 block analysis；concept drift 要改为时变 risk $L_t$ 与 dynamic comparator，不能仍声称固定 $P$ 的 batch risk。
## E
### LT-OTB-E01
每批先用只依赖过去的 checkpoint 预测并锁定 loss，再用该批更新；按独立随机 iterate、凸 prediction average 或独立 validation 选 checkpoint；test stream 不用于调参。记录 batch dependence、重复用户与 stopping rule。
### LT-OTB-E02
若输出是概率/logit 等凸空间元素且 loss 对输出凸，prediction averaging 可用 Jensen。参数平均只有在线性参数化或另有 mode connectivity/stability theorem 时才受控；深网参数到预测非凸，直接平均可能落入坏区域。
### LT-OTB-E03
claim card：iid/依赖 sample law；$\mathcal F_{t-1}$；loss range；pathwise/expected regret；fixed comparator；random/average/last output；confidence inequality；validation/checkpoint selection；drift/action feedback 边界。

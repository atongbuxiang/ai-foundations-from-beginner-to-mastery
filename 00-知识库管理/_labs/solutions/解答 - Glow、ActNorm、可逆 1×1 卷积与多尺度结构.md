---
type: solution
status: draft
topic: "[[Glow、ActNorm、可逆 1×1 卷积与多尺度结构]]"
exercise: "[[习题 - Glow、ActNorm、可逆 1×1 卷积与多尺度结构]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Glow、ActNorm、可逆 1×1 卷积与多尺度结构
## A. 识别与复述
### GEN35-A01
ActNorm 只在首次用一批数据选择参数初值，此后 $s,b$ 是固定于样本/batch 的可训练参数；推理不读当前 batch statistics。BatchNorm 在训练 forward 中使用当前/累计 batch statistics，train/eval 公式不同。
### GEN35-A02
每位置 $y_{hw}=Wx_{hw}$，$W\in\mathbb R^{C\times C}$ 可逆；整图 Jacobian 是 $HW$ 个 $W$ 块，logdet 为 $HW\log|\det W|$。
### GEN35-A03
Squeeze 是元素重排，$C,H,W\to4C,H/2,W/2$，总维数不变且 det 绝对值 1。Split 把一部分变量作为早期 latent 不再深变换；只要所有 chunks 保留，信息和总维数仍完整，但概率 factorization/compute 改变。
## B. 手算与建模
### GEN35-B01
$\det W=1$，所以 $9\log1=0$。
### GEN35-B02
每位置 $\log|2|+\log|1/4|=\log(1/2)=-\log2$；四位置总计 $-4\log2$。
### GEN35-B03
$[8,12,16,16]$；每样本原元素 $3\cdot32^2=3072$，新元素 $12\cdot16^2=3072$，不变。
## C. 推导与证明
### GEN35-C01
按位置排列变量后 Jacobian 为 $\operatorname{diag}(W,\ldots,W)$ 共 $HW$ 块；块对角 determinant 是各块 determinant 乘积，故 $(\det W)^{HW}$，取 log absolute 得结论。
### GEN35-C02
$W=PL(U_{off}+\operatorname{diag}s)$。$|\det P|=1$，unit-diagonal $L$ determinant 1，上三角 $U$ determinant $\prod_cs_c$，所以 log absolute determinant 是 $\sum_c\log|s_c|$。
### GEN35-C03
每次 split 都把当前 $d_l$ 维分成 $r_l+(d_l-r_l)$，维数只重新分组。递归到底，所有 $r_l$ 加最后剩余维数 telescoping 为初始 $d_0$。
## D. 边界、反例与纠错
### GEN35-D01
$W=\operatorname{diag}(10^{10},10^{-10})$ 的 det=1，远离 0，但 condition number 为 $10^{20}$。Determinant 是奇异值乘积，不能控制最大/最小奇异值之比。
### GEN35-D02
ActNorm 初始化后 forward 始终 $y=s\odot x+b$。若每批重算均值方差，inverse 将依赖未保存的 batch context，且不再是原 Glow 的单样本双射合同。
### GEN35-D03
若生成时固定/遗漏 $z^{(1)}$，只从条件 slice 而非完整 base 分布采样；输出支持、熵和 likelihood 对象改变，不能再声称从训练的 full flow 采样。
## E. AI 迁移
### GEN35-E01
编码：ActNorm→$1\times1$ conv→coupling；分别加 $HW\sum\log|s|$、$HW\log|\det W|$、coupling scale sum。逆：coupling inverse→linear solve $W^{-1}$→ActNorm inverse，logdet 符号相反。
### GEN35-E02
用不同随机首批、排序和 batch size 初始化同一模型，多 seed 训练；记录初始化 scale、早期 NLL/gradient、最终 NLL、round-trip 与失败率。另用代表性 warmup batch 作对照，不能只看一次最终分数。
### GEN35-E03
记录 `slogdet`、$\sigma_{min/max}$、condition number、LU diagonal extrema、forward/inverse residual、solve residual、NaN/Inf、不同 dtype 差和每层 wall time；determinant 单项不足。


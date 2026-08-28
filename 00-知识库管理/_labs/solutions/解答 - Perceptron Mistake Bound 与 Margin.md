---
type: solution
status: draft
topic: "[[Perceptron Mistake Bound 与 Margin]]"
exercise: "[[习题 - Perceptron Mistake Bound 与 Margin]]"
created: 2026-08-23
updated: 2026-08-28
---
# 解答 - Perceptron Mistake Bound 与 Margin
## A
### LT-PER-A01
预测 $\widehat y_t=\operatorname{sign}\langle w_t,x_t\rangle$。若 $y_t\langle w_t,x_t\rangle\le0$，更新 $w_{t+1}=w_t+y_tx_t$；否则不变。把 score 0 视作 mistake/update 可使证明中的交叉项始终非正。
### LT-PER-A02
要求所有 $\|x_t\|\le R$，存在 $\|u\|=1$ 与 $\gamma>0$ 使 $y_t\langle u,x_t\rangle\ge\gamma$ 对每轮成立。归一化不可省，否则 margin 可用缩放 $u$ 任意放大。
### LT-PER-A03
mistake bound 控制序列错误次数；training convergence 指重复有限可分集后不再错；optimization convergence 需指定 objective 与距离；population generalization 控制新样本期望 risk。前两者可由本定理连接，后两者需额外理论。
## B
### LT-PER-B01
从 $(0,0)$：样本 1 score 0，更新到 $(1,0)$；样本 2 score 0，更新到 $(1,1)$；样本 3 score $-1$，乘 $y=-1$ 得 margin 1，不更新；样本 4 同理。总 mistakes 为 2。
### LT-PER-B02
$(R/\gamma)^2=(3/0.2)^2=225$。所有输入乘 10 后 $R'=30,\gamma'=2$，比值仍 15，bound 仍 225。
### LT-PER-B03
$\|\widetilde x\|^2=\|x\|^2+1\le17$，故新半径 $\widetilde R\le\sqrt{17}$。
## C
### LT-PER-C01
只对 mistake index $k$：$w_{k+1}=w_k+y_kx_k$，故 $\langle w_{k+1},u\rangle=\langle w_k,u\rangle+y_k\langle x_k,u\rangle\ge\langle w_k,u\rangle+\gamma$。从 $w_1=0$ telescope $M$ 次即得 $\langle w_{M+1},u\rangle\ge M\gamma$。
### LT-PER-C02
$\|w_{k+1}\|^2=\|w_k\|^2+2y_k\langle w_k,x_k\rangle+\|x_k\|^2\le\|w_k\|^2+R^2$；不等号正是用 mistake condition $y_k\langle w_k,x_k\rangle\le0$。telescope 得 $\|w_{M+1}\|^2\le MR^2$。
### LT-PER-C03
重复同一 $x=1$，标签交替 $+1,-1,+1,-1,\ldots$。不存在同一 separator 同时给相反标签正 margin；权重会在 0 与 1 等状态间反复更新。失效的是统一可分且 $\gamma>0$ 的假设。
## D
### LT-PER-D01
还缺 norm 上界 $R$、unit separator convention、正 margin 数值 $\gamma$、是否含 bias及其增广尺度、tie/update rule、序列是否对同一 separator 可分，以及“100步”指 rounds 还是 mistakes。只有 $(R/\gamma)^2\le100$ 才支持该数值。
### LT-PER-D02
embedding 乘 $c$ 时 $R$ 与 $\gamma$ 同乘 $c$，真正控制项 $R/\gamma$ 不变。若还改变 classifier norm convention，更需先归一化才可比较。
### LT-PER-D03
kernel 表示 $w=\sum_{k\in\mathcal M}y_k\phi(x_k)$，每次预测需对所有 mistake supports 求 kernel。即使 $M$ 有界，界可能很大，内存与 latency 均随 support 数增长；还需 budget、sparsification 或 approximation。
## E
### LT-PER-E01
按内容 session 定义轮次；固定/归一化 feature 使 $\|x_t\|\le R$ 可验证；在审核标注到达后才更新并记录 delay；用时间窗口估计 margin distribution；若 policy/label rule 漂移，改用 shifting/dynamic comparator，并把 delayed labels 纳入 filtration。
### LT-PER-E02
Perceptron 在错误时作固定步更新，给可分序列 mistake bound；hinge-SGD 优化正则/经验 surrogate，保证依赖凸优化与采样；hard-margin SVM 解最小 norm 约束问题并选择最大几何 margin。三者可共享线性 score，却输出和 theorem 不同。
### LT-PER-E03
claim card：序列/label timing；$x$ norm 与 bias convention；unit separator 和 margin；tie/update；总 mistakes 而非 rounds；是否有 noise/drift；kernel 时的计算预算；结论不外推最大 margin、唯一权重或 population risk。

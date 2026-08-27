---
type: solution
status: verified
area: [training, optimization, online-learning]
topic: "[[Adam 收敛反例、AMSGrad 与条件化保证]]"
exercise: "[[习题 - Adam 收敛反例、AMSGrad 与条件化保证]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Adam 收敛反例、AMSGrad 与条件化保证

> [!warning] 使用边界
> 反例否定的是带量词的命题。它揭示证明漏洞和机制风险，但不自动变成所有神经网络、所有实现与所有超参数的经验判决。

## A. 识别与复述

### TRN13-A01
令 $f_t(x)=Cx$ 当 $t\equiv1\pmod3$，其余两步 $f_t(x)=-x$，$x\in[-1,1]$。每周期累计为 $(C-2)x$。$C>2$ 时斜率为正，故最佳固定 comparator 是左端点 $x^*=-1$。

### TRN13-A02
它针对“在给定 online convex 条件与步长设置下，原始 Adam 普遍具有所声称的 sublinear regret/收敛保证”之类的全称命题。找到一个合法序列即可否定全称命题；但这不推出有限数据、非凸网络、另一个 schedule 的每次 Adam 训练都会失败。

### TRN13-A03
常见写法先算 $\tilde v_t=\beta_2\tilde v_{t-1}+(1-\beta_2)g_t^2$，再逐坐标 $v_t^{\max}=\max(v_{t-1}^{\max},\tilde v_t)$，分母使用 $\sqrt{v_t^{\max}}$（具体偏差修正依实现/论文合同）。关键是 $v_t^{\max}\ge v_{t-1}^{\max}$。

## B. 手算与构造

### TRN13-B01
累计损失 $4x-x-x=2x$，在 $[-1,1]$ 上最小值位于 $x=-1$，值 $-2$；$x=1$ 给 $2$。逐步梯度有两次向右有利的负斜率，但固定 comparator 由周期总斜率决定。

### TRN13-B02
$v_1=0.8(16)=12.8$，$v_2=0.2(12.8)+0.8(1)=3.36$，$v_3=0.2(3.36)+0.8=1.472$。方向大小依次 $4/\sqrt{12.8}\approx1.118$、$1/\sqrt{3.36}\approx0.545$、$1/\sqrt{1.472}\approx0.824$。尖峰分母迅速遗忘，后续小负梯度相对增权。

### TRN13-B03
Running maximum 依次为 $12.8,12.8,12.8$。第 2、3 步负梯度方向大小都为 $1/\sqrt{12.8}\approx0.280$，不会因 raw EMA 回落至 3.36、1.472 而逐步放大。

## C. 推导与证明

### TRN13-C01
对 $K$ 个完整周期，$\sum_{t=1}^{3K}f_t(x)=K(C-2)x$。$K(C-2)>0$，线性函数在闭区间的最小值取最左端 $x=-1$。所以 comparator 不由“负梯度出现次数更多”决定，而由带幅值总和决定。

### TRN13-C02
许多 regret 分解会出现预条件度量的 telescoping 项；若坐标有效倍率 $\alpha_t/\sqrt{v_{t,i}}$ 任意增大，前后度量不能良性相消。一个代表性充分结构是 $\sqrt{v_{t,i}}/\alpha_t$ 非减，等价于有效倍率非增。具体定理还需凸性、有界域/梯度和 $\beta$ 条件。

### TRN13-C03
由最大值定义，$v_t^{\max}$ 是 $v_{t-1}^{\max}$ 与新值中的较大者，故逐坐标非减。任一历史大 $\tilde v_s$ 都成为以后上界的下限，除非显式重置；因此 denominator memory 不会像 EMA 那样指数退回小值。

## D. 边界、反例与纠错

### TRN13-D01
分母单调只修补特定有效学习率项。全局最优还需目标凸/适当光滑、可行域、步长序列、梯度界与迭代协议；非凸目标通常只能谈 stationary point；恒定过大 LR、错误梯度或不可达最优都可失败。

### TRN13-D02
投影决定参数留在 $[-1,1]$，线性损失给固定 comparator 和精确梯度，周期与 $\beta_2$ 决定分母遗忘。删去它们得到的是另一个实验，最多检验相邻机制；不能再引用原证明的量词和结论。

### TRN13-D03
Regret theorem 是指定 adversarial/online protocol 下的最坏情形命题；深度学习 benchmark 是有限任务、数据分布、调参预算和随机种子的经验统计。一个算法可无普遍最坏情形保证却在常见结构上好用，也可满足渐近保证却在有限预算内较差。

## E. AI 迁移

### TRN13-E01
锁定 $C,\beta_1,\beta_2,\alpha_t,\epsilon$、投影区间和更新时序；逐步记录 $g_t,m_t,v_t$、denominator、pre-projection/post-projection $x_t$、周期累计 loss 与 regret；断言 comparator 为 $-1$、Adam/AMSGrad 轨迹差异和参数始终在域内。

### TRN13-E02
除相同调参/seed/token 预算外，报告 optimizer state bytes（AMSGrad 多一份 max state）、峰值显存、通信、step wall time、kernel/fusion 支持与吞吐。若为 AMSGrad 减 batch 才能容纳状态，统计协议也已改变。

### TRN13-E03
三栏可写：①假设：目标类、随机 oracle、有界性、步长、moment 参数、投影/域、精度；②结论：regret、梯度范数或函数差的量、概率、常数与渐近率；③外推：真实网络中哪些条件未验证、哪些仅类比、需要哪些 benchmark/ablation 才支持。

## 无提示重做

- [ ] 48 小时后仅凭周期斜率找 comparator。
- [ ] 一周后把一个 theorem 摘成假设—结论—不可外推三栏。

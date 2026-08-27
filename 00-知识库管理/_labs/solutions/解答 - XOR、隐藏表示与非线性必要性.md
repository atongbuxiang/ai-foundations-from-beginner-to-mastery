---
type: solution
status: draft
area: [neural-networks/feedforward, xor]
topic: "[[XOR、隐藏表示与非线性必要性]]"
exercise: "[[习题 - XOR、隐藏表示与非线性必要性]]"
sources: ["[[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - XOR、隐藏表示与非线性必要性
## A
### NN-XOR-A01
四点为 $(0,0),(0,1),(1,0),(1,1)$，标签依次 $0,1,1,0$。不可分否定的是“存在一个 affine functional 加单 threshold，在四点上给正确标签”，不否定 nonlinear classifier、lookup table 或新 feature space 中的 linear separator。
### NN-XOR-A02
input space 是原 $x$ 的空间；hidden space 是 $h(x)$ 的值域；activation pattern 记录各 pre-activation 的开/关区域；linear readout 是 $v^Th+c$。表示映射可非线性且多对一，读出层仍线性。
### NN-XOR-A03
插值只约束四点；全域相等约束所有 $x$；uniform approximation 控制全域最大数值误差；分类一致只要求 threshold 后标签相同，score 可不同。
## B
### NN-XOR-B01
$s=0,1,1,2$ 时 hidden triples 为 $(0,0,0),(1,0,0),(1,0,0),(2,1,0)$，输出分别 $0,1,1,0$。
### NN-XOR-B02
取
$$W^{(1)}=\begin{bmatrix}1&1&1\\1&1&1\end{bmatrix},\quad b^{(1)}=(0,-1,-2),\quad W^{(2)}=(1,-2,1)^T,\quad b^{(2)}=0.$$
形状为 $[2,3],[3],[3,1],[1]$。
### NN-XOR-B03
输出依次 $0,0.5,0.5,0$；slopes 在区间 $(-\infty,0),(0,1),(1,2),(2,\infty)$ 为 $0,1,-1,0$。
## C
### NN-XOR-C01
要求 $b<0,w_1+b>0,w_2+b>0,w_1+w_2+b<0$。中间两式给 $w_1+w_2+2b>0$；再因 $b<0$ 得 $w_1+w_2+b>0$，矛盾。
### NN-XOR-C02
两类 convex hull 都含 $(1/2,1/2)$。严格线性分离会使两个 hull 分别落在开半空间中，故必须不相交；必要条件失败。
### NN-XOR-C03
归纳假设前 $k$ 层为 $xA+c$，再接 affine 得 $x(AB)+(cB+d)$。bottleneck 使 effective linear part 的 rank 不超过最窄层，但不改变 affine 性。
## D
### NN-XOR-D01
表示只需保留任务充分信息。XOR 构造把 $(1,0),(0,1)$ 合并，丢失“哪个 bit 为 1”却完整保留 XOR 标签；对另一个下游任务这可能失败。
### NN-XOR-D02
正文 triangular hat $f$ 与 $g=f+x_1(1-x_1)x_2(1-x_2)$ 在四个顶点相同，正方形内部不同，且都连续。
### NN-XOR-D03
nonlinear probe 函数类更大，可能只是记忆样本。应固定数据、regularization、optimization budget，报告 held-out curves，并与 raw-input、random encoder、matched-capacity controls 比较。
## E
### NN-XOR-E01
冻结 encoder，按相同 split 训练 linear 与多级容量 probe，画 sample/regularization curves；加入 random/fixed-feature baselines、seed uncertainty 和 leakage audit。比较的是可读出性，不直接认证 encoder 的所有下游价值。
### NN-XOR-E02
两个 affine branches $a(x),b(x)$ 相乘产生二次交互 $a_ib_i$；纯 affine 复合仍 affine，不能产生此乘积。门控同时改变梯度与尺度，需另审计。
### NN-XOR-E03
核验四点/标签与 shuffle；逐层 shape；hidden activation 不是 identity；output/logit 与 BCE/CE 匹配；打印 activation/gradient norm；用手工参数验证 forward；多 seed、小学习率和过拟合四点测试定位优化问题。

---
type: exercise
status: draft
topic: "[[Perceptron Mistake Bound 与 Margin]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Perceptron Mistake Bound 与 Margin]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - Perceptron Mistake Bound 与 Margin
## A
### LT-PER-A01
写出 Perceptron 的预测、mistake 条件和更新，并说明 tie 的处理。
### LT-PER-A02
准确声明 $R$、unit separator $u$ 与 margin $\gamma$ 假设。
### LT-PER-A03
区分 mistake bound、training convergence、optimization convergence 与 population generalization。
## B
### LT-PER-B01
按正文四样本顺序从 $w=0$ 手算每轮 score、update 与总 mistakes。
### LT-PER-B02
$R=3,\gamma=0.2$ 时 theorem 给多少 mistakes？若所有 $x$ 乘 10 呢？
### LT-PER-B03
用 $\widetilde x=(x,1)$ 增广 bias，原 $\|x\|\le4$ 时新半径上界是多少？
## C
### LT-PER-C01
完整证明 progress lower bound $\langle w,u\rangle\ge M\gamma$。
### LT-PER-C02
完整证明 norm upper bound $\|w\|\le R\sqrt M$，指出 mistake condition 用在哪里。
### LT-PER-C03
构造不可分二点序列，使 Perceptron 永远更新，并指出定理失效假设。
## D
### LT-PER-D01
审计“数据线性可分，所以 Perceptron 在 100 步内收敛”：还缺哪些数值与协议？
### LT-PER-D02
embedding 乘常数后 margin 变大。为什么不能据此宣称 bound 改善？
### LT-PER-D03
kernel Perceptron 有 mistake bound 后，为什么部署成本仍可能不可接受？
## E
### LT-PER-E01
为在线内容审核建立 feature norm、margin、label delay 与 drift 合同。
### LT-PER-E02
比较 Perceptron、hinge-loss SGD 与 hard-margin SVM 的输出/保证。
### LT-PER-E03
写 Perceptron claim card：sequence、normalization、margin、updates、noise 与外推边界。

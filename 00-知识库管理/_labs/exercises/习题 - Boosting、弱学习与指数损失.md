---
type: exercise
status: draft
topic: "[[Boosting、弱学习与指数损失]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Boosting、弱学习与指数损失]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - Boosting、弱学习与指数损失
## A
### LT-BST-A01
写 AdaBoost 的 $D_t,\varepsilon_t,\alpha_t,Z_t$、更新与最终 classifier。
### LT-BST-A02
用量词写 weak-learning assumption，并说明为什么 51% 原始 accuracy 不够。
### LT-BST-A03
区分 AdaBoost、bagging、random forest 与 gradient boosting。
## B
### LT-BST-B01
$\varepsilon=0.25$ 时计算 $\alpha,Z$；十轮同误差时计算 product bound。
### LT-BST-B02
$\gamma=0.1$ 恒定时，要使 $e^{-2\gamma^2T}\le0.01$，最少多少轮？
### LT-BST-B03
三样本初始均匀，弱规则只错第 3 个且 $\alpha=\frac12\log2$，求更新后的 $D_2$。
## C
### LT-BST-C01
从 $Z_t(\alpha)$ 求导推导最优 $\alpha_t$ 与 $Z_t$。
### LT-BST-C02
展开 $D_{T+1}$，证明经验指数损失等于 $\prod_t Z_t$。
### LT-BST-C03
证明 training 0–1 error $\le e^{-2\sum_t\gamma_t^2}$。
## D
### LT-BST-D01
数据有一个永久错标点。分析其权重和指数损失为何会主导训练。
### LT-BST-D02
审计“训练误差已为零，所以继续 boosting 必然改善 test error”。
### LT-BST-D03
weak learner 某轮 $\varepsilon_t>1/2$。二分类下可怎样处理，哪些情况仍未解决？
## E
### LT-BST-E01
为多模型 ensemble 定义加权 query distribution、edge 与部署反馈。
### LT-BST-E02
比较指数损失与 logistic loss 对大负 margin/outlier 的梯度权重。
### LT-BST-E03
写 Boosting claim card：weak quantifier、loss、base class、rounds、noise 与 generalization evidence。

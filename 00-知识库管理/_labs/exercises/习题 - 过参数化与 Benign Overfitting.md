---
type: exercise
status: draft
topic: "[[过参数化与 Benign Overfitting]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - 过参数化与 Benign Overfitting]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - 过参数化与 Benign Overfitting
## A
### LT-BO-A01
正式定义 benign overfitting，并区分 finite-sample “test 还好”。
### LT-BO-A02
写 min-norm interpolator 的 signal–noise projector 分解。
### LT-BO-A03
为什么 test parameter error 要用 $\Sigma^{1/2}$ 加权？
## B
### LT-BO-B01
纯噪声 isotropic 模型 $n=100,p=1001,\sigma^2=2$，求 expected excess risk。
### LT-BO-B02
若 $p/n\to c=3$，纯噪声 risk 极限是多少？这是否 benign？
### LT-BO-B03
给 eigen tail $(0.01,0.01,0.01,0.01)$ 与 $(0.04,0,0,0)$，比较 $R_k$。
## C
### LT-BO-C01
证明任意 null-space 向量都不改训练拟合，却可能任意增大 test risk。
### LT-BO-C02
推导 isotropic min-norm 的 signal bias $(1-n/p)\|\beta^*\|^2$。
### LT-BO-C03
解释“强方向学 signal、弱尾部吸 noise”需要哪些定量条件。
## D
### LT-BO-D01
审计“模型插值且 test error 低，所以发生 benign overfitting”。
### LT-BO-D02
为什么 regression benign theorem 不能直接证明随机标签分类安全？
### LT-BO-D03
feature rescaling 如何改变 min-norm 选解与 benign 结论？
## E
### LT-BO-E01
为 pretrained embedding + ridgeless linear head 设计谱/信号对齐审计。
### LT-BO-E02
提出一个能证伪“弱谱尾吸收噪声”机制的干预实验。
### LT-BO-E03
写 benign-overfitting claim card：problem sequence、algorithm、spectrum、signal、noise 与 risk limit。

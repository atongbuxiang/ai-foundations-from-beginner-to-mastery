---
type: solution
status: draft
topic: "[[范数、平坦性、Sharpness 与参数化不变性]]"
exercise: "[[习题 - 范数、平坦性、Sharpness 与参数化不变性]]"
created: 2026-08-23
updated: 2026-08-28
---
# 解答 - 范数、平坦性、Sharpness 与参数化不变性
## A
### LT-SHP-A01
parameter 是坐标 $\theta$；predictor 是映射 $f_\theta$；equivalence class $[\theta]=\{\theta':f_{\theta'}=f_\theta\}$。risk由 predictor决定，raw norm/Hessian常随class内 representative改变。
### LT-SHP-A02
对 $a\sigma(w^Tx)$，取 $a'=a/c,w'=cw,c>0$。ReLU 正齐次给 $a'\sigma(w'^Tx)=(a/c)c\sigma(w^Tx)=a\sigma(w^Tx)$。
### LT-SHP-A03
Hessian最大特征值、Hessian trace、固定norm-ball最坏loss rise、随机perturbation expected rise（还可有normalized版本）。它们对direction/radius、二阶近似、coordinates和nonsmoothness响应不同，数值不能互换。
## B
### LT-SHP-B01
$\nabla L=2(ab-1)(b,a)$。在 $ab=1$，$H=2(b,a)^T(b,a)$，rank 1，eigenvalues为 $0$ 与 $2(a^2+b^2)$。
### LT-SHP-B02
$(1,1)$ raw squared norm 2、sharpness 4、product 1；$(100,0.01)$ raw squared norm $10000.0001$、sharpness $20000.0002$、product仍1。predictor完全相同。
### LT-SHP-B03
若 incoming norm为 $\|w\|$、outgoing为 $|a|$，原和 $\|w\|^2+a^2$；变换后为 $25\|w\|^2+a^2/25$，通常改变且可远大于原值。
## C
### LT-SHP-C01
global minimum family $(a,b)=(c,1/c)$ 全表示 $f(x)=x$。其 sharpness $2(c^2+c^{-2})$，随 $c\to\infty$ 发散，所以同一 predictor可任意 sharp。
### LT-SHP-C02
每条经过该node的path恰含一条incoming edge乘 $c$ 和一条outgoing edge除 $c$；沿path权重乘积中的两因子抵消。平方、绝对值后仍抵消，所有path求和不变。
### LT-SHP-C03
取同一 predictor 的两种表示 $c=1$ 与 $c=M$。generalization gap完全相同，raw norm却可令第二个任意大；若把另一个不同但略差gap的 predictor用balanced parameterization表示，即可使 raw norm排名与gap排名任意相反。
## D
### LT-SHP-D01
观察是相关：batch size还改变gradient noise、learning rate scaling、optimization endpoint、train loss和margin。raw sharpness又不具rescaling不变性。要称因果需function-preserving controls、matched endpoints与直接sharpness干预/中介分析。
### LT-SHP-D02
不能。SAM同时改变优化trajectory、effective regularization、margin和parameter scaling；其neighborhood目标也不等于raw Hessian eigenvalue。成功支持算法效用，机制需独立不变性与干预证据。
### LT-SHP-D03
architecture/function class、input/output scaling、normalization层、train loss/margin、optimizer/compute、augmentation、parameter symmetry、measure normalization、seed、dataset与validation selection。最好在held-out architecture上测试预测性。
## E
### LT-SHP-E01
对 LoRA $\Delta W=AB$ 做 $A\mapsto cA,B\mapsto B/c$；候选measure应保持或有明确quotient normalization。比较raw factor norm、product/path/nuclear/function-Jacobian measures，并验证同一 $\Delta W$ 的score不变。
### LT-SHP-E02
定义校准输入分布 $Q_X$，对量化前后 logits/probabilities测 $E_{Q_X}\|f_{\theta_q}(X)-f_\theta(X)\|^2$、output KL、task-loss rise与worst-group分层；同时报告quantization scheme。它比固定raw-weight $\ell_2$ radius更贴近函数影响。
### LT-SHP-E03
claim card：measure公式/单位；参数或函数层；symmetry invariance；input/architecture normalization；训练endpoint；适用scope；相关/预测/bound/因果证据；多重measure选择；held-out验证；干预是否保持其他对象。

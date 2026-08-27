---
type: exercise-set
status: draft
area: [labs, math/calculus, math/linear-algebra, math/matrix-calculus, ai/automatic-differentiation]
prerequisites: ["[[Jacobian、JVP 与 VJP]]", "[[全微分与 Fréchet 导数]]", "[[梯度、方向导数与最陡方向]]", "[[线性泛函与对偶空间]]", "[[伴随算子]]"]
related: ["[[Hessian、二阶微分与曲率]]", "[[多元链式法则与计算图]]", "[[矩阵微分、迹技巧与布局约定]]", "[[自动微分：前向、反向与高阶模式]]", "[[练习与测验 MOC]]"]
sources: ["MIT-18.S096-Derivatives-Linear-Operators", "MIT-18.S096-Jacobians-Matrix-Functions", "JAX-JVP-VJP-Official", "JAX-JVP-API", "JAX-VJP-API", "PyTorch-Func-Transforms", "Baydin-2018-AD-Survey", "Su-10958-JVP"]
solutions: ["[[解答 - Jacobian、JVP 与 VJP]]"]
created: 2026-08-17
updated: 2026-08-17
---

# 习题 - Jacobian、JVP 与 VJP

> [!abstract] 训练目标
> 从“能写偏导矩阵”升级到“能区分导数算子、坐标表示、切向量前推和协向量回拉；能为多输入、批量、矩阵参数选择 JVP/VJP；能用有限差分与伴随点积测试验证真实实现”。

## 作答规则

1. A–E 每级三题，共 15 题；
2. 每题先写函数签名、输入/输出空间、基点与形状；
3. JVP 必须标注 tangent 属于哪个输入空间，VJP 必须标注 seed 属于哪个输出对偶空间；
4. 使用 $J^\top u$ 时说明采用标准欧氏/Frobenius 配对；
5. 多输入题分别列出每个返回 cotangent，广播题明确求和轴；
6. full Jacobian 题明确输出轴、输入轴与展平顺序；
7. 性能判断必须写成经验倾向，不宣称仅由 $m,n$ 精确决定运行时间；
8. 独立完成前不要打开[[解答 - Jacobian、JVP 与 VJP]]。

## A 级：对象、类型与接口语言

### CALC-JV-A01：翻译十四个声明

逐条写出自然语言、对象类型、输入输出空间与依赖条件：

1. $DF(x)\in\mathcal L(X,Y)$；
2. $J_F(x)\in\mathbb R^{m\times n}$；
3. $(J_F)_{ij}=\partial F_i/\partial x_j$；
4. $J_{:j}=DF(x)[e_j]$；
5. $\operatorname{JVP}_{F,x}(v)=DF(x)[v]$；
6. $A':Y^*\to X^*$；
7. $(A'u^*)[v]=u^*[Av]$；
8. $\operatorname{VJP}_{F,x}(u^*)=DF(x)'[u^*]$；
9. $u^\top(Jv)=(J^\top u)^\top v$；
10. $J^\dagger=M_X^{-1}J^\top M_Y$；
11. $\nabla f=J_f^\top1$；
12. $J_{\widetilde F}=T^{-1}J_FS$；
13. $J^\top Jv$；
14. $J^\top\mathbf1=\nabla(\sum_iF_i)$。

特别说明第 2–4 项的基/布局约定，第 6–8 项为何不需要内积，第 9–11 项何时把协向量显示为向量。

### CALC-JV-A02：判断十八个断言

判断正误；错误项给反例或最小补充条件。

1. Jacobian 是与坐标无关的抽象线性算子；
2. 若 $F:\mathbb R^n\to\mathbb R^m$，则本库 Jacobian 形状为 $m\times n$；
3. 所有偏导存在就保证该偏导表表示 Fréchet 导数；
4. JVP 的输入 tangent 与函数输入同结构；
5. JVP 输出总与输入 tangent 同形状；
6. VJP seed 属于输出对偶空间；
7. 对偶回拉的定义需要先选内积；
8. 标准欧氏坐标中 VJP 可由 $J^\top u$ 表示；
9. 非欧氏内积下伴随仍总由普通转置表示；
10. $J^\top$ 是 $J$ 的逆映射；
11. full Jacobian 可由输入基 JVP 逐列恢复；
12. full Jacobian 可由输出基 VJP 逐行恢复；
13. $m=1$ 时一次 seed $1$ 的 VJP 给出欧氏梯度；
14. 向量输出用全一 seed 会给出完整 Jacobian；
15. $m\gg n$ 时 `jacfwd` 通常是构造 full Jacobian 的合理起点；
16. reverse mode 的内存一定与输入维数无关；
17. 伴随点积测试通过就证明原函数经典可微；
18. 框架返回的数组叫 gradient，就必然是任意用户度量下的梯度向量。

### CALC-JV-A03：为十二个任务选择最直接工具

从下列工具中选最直接者，并说明关键条件：

- Fréchet 余项；
- Jacobian 坐标矩阵；
- JVP；
- VJP；
- 输入基探针；
- 输出对偶基探针；
- 加权伴随；
- `vec`/Kronecker；
- 方向中心差分；
- 伴随点积测试；
- `vmap`/批量探针；
- profiling。

任务：

1. 证明偏导表确实代表统一导数；
2. 小型系统中查看每个输出对每个输入的偏导；
3. 给定输入扰动预测全部输出一阶变化；
4. 给定标量化输出把敏感度传回全部参数；
5. 用黑箱 JVP 恢复 Jacobian 的列；
6. 用黑箱 VJP 恢复 Jacobian 的行；
7. 非欧氏输入/输出度量中表示伴随；
8. 分析 $X\mapsto AXB$ 的显式坐标矩阵；
9. 数值核对一个 JVP；
10. 同时核对一对 JVP/VJP；
11. 获取 per-example gradient 或批量多个探针；
12. 判断 `jacfwd` 与 `jacrev` 在目标硬件上谁更快。

## B 级：手算、形状与种子

### CALC-JV-B01：一个 $\mathbb R^2\to\mathbb R^3$ 映射

令

$$
F(x,y)=(xy,\ e^x+y,\ x^2-y^2)^\top.
$$

在 $a=(0,1)$：

1. 从分量偏导写出 $J_F(a)$；
2. 用输入基 JVP 解释两列；
3. 对 $v=(2,-1)^\top$ 计算 JVP；
4. 对 $u=(1,3,-2)^\top$ 计算 VJP；
5. 验证伴随点积恒等式；
6. 用三个输出基种子恢复三行；
7. 对 $\phi(x,y)=u^\top F(x,y)$ 直接求梯度，并与 VJP 比较。

### CALC-JV-B02：由黑箱作用恢复矩阵

未知线性算子 $A:\mathbb R^3\to\mathbb R^2$ 的 JVP 黑箱返回

$$
Ae_1=(1,2)^\top,
\quad
Ae_2=(-1,0)^\top,
\quad
Ae_3=(3,4)^\top.
$$

1. 恢复矩阵 $J$；
2. 计算 $A(2,-1,1)^\top$；
3. 对 $u=(2,-3)^\top$ 计算 $J^\top u$；
4. 写出两个输出基种子的 VJP；
5. 只允许调用 VJP 黑箱时，说明如何恢复 $J$；
6. 若一次 JVP 和一次 VJP 都有微小浮点误差，设计相对伴随残差；
7. 说明三个列探针通过为何仍不能证明某个非线性程序在邻域 Fréchet 可微。

### CALC-JV-B03：批量线性层与广播

设

$$
Y=WX+b\mathbf1_B^\top,
$$

其中 $W\in\mathbb R^{p\times q}$、$X\in\mathbb R^{q\times B}$、$b\in\mathbb R^p$。

1. 推导对 $(\dot W,\dot X,\dot b)$ 的总 JVP；
2. 给定输出 seed $U\in\mathbb R^{p\times B}$，推导 $\bar W,\bar X,\bar b$；
3. 写出总伴随点积恒等式；
4. 解释为什么 $\bar b$ 要沿 batch 轴求和；
5. 若损失是 batch mean 而不是 sum，结果相差什么因子；
6. 若只对 $W$ 求导，怎样定义函数签名与 tangent；
7. 区分 batch-summed gradient 与 per-example weight gradient 的形状。

## C 级：证明与理论重建

### CALC-JV-C01：Jacobian 的表示定理与坐标变换

1. 选输入基 $e_j$ 和输出基 $f_i$，从 $A[e_j]=\sum_iJ_{ij}f_i$ 证明 $[A h]=J[h]$；
2. 对可微 $F:\mathbb R^n\to\mathbb R^m$ 证明 $J_{ij}=\partial_jF_i$；
3. 证明 Jacobian 第 $j$ 列是输入基 JVP；
4. 设 $x=Sz,y=Tu$，推导 $J_{\widetilde F}=T^{-1}J_FS$；
5. 推导输入/输出 tangent 坐标变换；
6. 推导输出与输入 cotangent 的变换；
7. 解释为什么矩阵元素变化不表示抽象导数算子变化。

### CALC-JV-C02：对偶回拉、伴随与加权度量

设 $A:X\to Y$ 线性。

1. 定义 $A':Y^*\to X^*$，证明它线性；
2. 证明 $(A'u^*)[v]=u^*[Av]$；
3. 在标准欧氏基中推出 VJP 数组为 $J^\top u$；
4. 在 $M_X,M_Y\succ0$ 下推导 $J^\dagger=M_X^{-1}J^\top M_Y$；
5. 证明加权伴随恒等式；
6. 解释对偶映射、伴随、转置和逆四者的差别；
7. 给出一个 $J^\top\ne J^{-1}$ 的矩形例子。

### CALC-JV-C03：按列/行构造、成本与矩阵自由作用

1. 证明 $n$ 个输入基 JVP 可构造 $m\times n$ Jacobian；
2. 证明 $m$ 个输出基 VJP 可构造同一 Jacobian；
3. 说明 $m\gg n$ 与 $n\gg m$ 时的基本选择；
4. 列出至少五个使维数经验规则失准的系统因素；
5. 用 JVP/VJP 写出 $J^\top Jv$ 和 $JJ^\top u$ 的黑箱算法；
6. 证明两个算子在欧氏空间都是半正定自伴随；
7. 说明为什么仍不能由此宣称某个实际 AD 实现具有固定常数倍成本。

## D 级：错误审计与软件语义

### CALC-JV-D01：审计十五条声明

逐条按“对象—形状—隐藏假设—最小修正—验证方法”审计：

1. “Jacobian 就是所有一阶导数，不需要先证明可微。”
2. “$Jv$ 与 $v$ 总是同形状。”
3. “VJP 是把输出向量逆映射回输入。”
4. “反向传播计算 $J^{-1}$。”
5. “任何内积下 backward 都是普通转置。”
6. “向量输出不传 seed 也有唯一梯度。”
7. “全一 seed 等于 full Jacobian。”
8. “batch loss 的 gradient 就是 per-example gradients。”
9. “广播偏置的反向不需要归约。”
10. “`jacrev` 对所有问题都比 `jacfwd` 快。”
11. “不物化 $J$ 就无法计算 Jacobian 谱相关量。”
12. “伴随点积测试通过证明 JVP 与真实数学导数一致。”
13. “中心差分通过证明 VJP 正确。”
14. “自定义 backward 正确就不需要 custom JVP。”
15. “框架的 gradient 数组天然是自然梯度。”

### CALC-JV-D02：batch、mask、归约与 per-example 语义

某程序输入批量 $X\in\mathbb R^{B\times d}$，输出逐样本损失 $\ell(X)\in\mathbb R^B$，最终训练损失为 $L=\operatorname{mean}(\ell)$。

1. 写出 $J_\ell$ 的形状；若样本完全独立，它具有什么块结构；
2. 写出 $\nabla_XL$ 对应的 VJP seed；
3. 区分 seed $\mathbf1$ 与 $\mathbf1/B$；
4. 若有跨样本 batch normalization，块对角结论哪里失效；
5. 若 mask 通过布尔索引删除样本，说明形状与不可微控制流风险；
6. 设计测试区分样本独立、归约因子错误和广播求和错误；
7. 说明如何获取每样本参数梯度而不是 $X$ 梯度。

### CALC-JV-D03：API 与测试协议审计

阅读以下伪代码：

```text
y, jv = jvp(f, (x,), (v,))
y2, pullback = vjp(f, x)
jt_u = pullback(u)
assert dot(u, jv) == dot(jt_u, v)
```

1. 补齐每个对象的结构与形状；
2. 指出严格 `==` 的数值问题并给稳定残差；
3. 若 `pullback` 返回 tuple，怎样正确取出输入块；
4. 加入中心差分 JVP 检查与步长扫描；
5. 加入 $v,u$ 线性性检查；
6. 列出 detach、随机性、训练模式、dtype 和不可微点的控制项；
7. 解释为什么需要同时做差分测试和伴随测试。

## E 级：综合推导与 AI 迁移

### CALC-JV-E01：结构化矩阵映射

设

$$
F(X)=AXB+CXD,
$$

各矩阵形状使两项都属于 $\mathbb R^{r\times s}$，$X\in\mathbb R^{m\times n}$。

1. 给出一组完整形状契约；
2. 推导 JVP $DF(X)[H]$；
3. 给定 $U\in\mathbb R^{r\times s}$，推导 Frobenius VJP；
4. 写出按列 `vec` 的显式 Kronecker Jacobian；
5. 验证结构化 VJP 与 Kronecker 转置作用一致；
6. 写出伴随点积测试；
7. 比较显式 Jacobian 与结构化 matvec 的存储/计算风险。

### CALC-JV-E02：矩阵自由 Gauss–Newton/NTK 接口

设模型输出 $f_\theta\in\mathbb R^m$，参数 $\theta\in\mathbb R^n$，固定点 Jacobian 为 $J$。

1. 设计只调用 JVP/VJP 的 $v\mapsto J^\top Jv$；
2. 设计只调用 JVP/VJP 的 $u\mapsto JJ^\top u$；
3. 证明二者对称半正定；
4. 证明非零特征值相同；
5. 说明参数空间大、输出/样本空间小时为何后者可能更适合；
6. 设计随机伴随与 Rayleigh 商测试；
7. 说明这些固定线性化算子与完整非线性训练、Hessian 和收敛结论的边界。

### CALC-JV-E03：设计一份可复核的 AD 接口报告

选择注意力投影、卷积、embedding、归一化层、扩散速度场或隐式层之一，完成：

1. 明确 primal、tangent、output cotangent 与 input cotangent 的树结构；
2. 写出数学 $DF(x)$ 的作用或最小可验证局部规则；
3. 说明是否需要 full Jacobian、JVP、VJP 或组合；
4. 给出维数选择与实际 profiling 计划；
5. 处理 batch、广播、mask、参数共享和归约；
6. 设计解析小例、中心差分、线性性与伴随点积测试；
7. 记录 dtype、容差、随机种子、训练/推理模式与框架版本；
8. 处理不可微点、自定义规则和高阶组合边界；
9. 区分数学证明、实现测试、性能证据和 AI 效果猜想；
10. 给出失败后的最短排查顺序。

## 提交前自检

- [ ] 恰好完成 15 题，题号无遗漏；
- [ ] 每个 JVP/VJP 都写清了方向和空间；
- [ ] 没把对偶映射、伴随、转置和逆混为一谈；
- [ ] 多输入/批量题核对了每个参数块和归约轴；
- [ ] full Jacobian 题声明了布局与展平顺序；
- [ ] 成本判断保留了 profiling 和内存边界；
- [ ] 同时使用了有限差分与伴随点积测试；
- [ ] 没把有限测试升级成一般可微性或训练收敛证明。

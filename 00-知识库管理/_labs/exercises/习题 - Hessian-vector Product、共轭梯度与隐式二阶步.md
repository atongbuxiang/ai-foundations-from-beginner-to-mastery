---
type: exercise
status: verified
area: [training, optimization, curvature]
topic: "[[Hessian-vector Product、共轭梯度与隐式二阶步]]"
solution: "[[解答 - Hessian-vector Product、共轭梯度与隐式二阶步]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Hessian-vector Product、共轭梯度与隐式二阶步

> [!abstract] 训练目标
> 把二阶方法写成线性算子接口；能验证 HVP、解释 CG 的 Krylov 结构与误差边界，并识别随机状态、不定曲率和有限差分的失败模式。

## A. 识别与复述

### TRN19-A01
定义 Hessian-vector product。为什么 $Hv$ 可以精确由自动微分得到，而无需显式构造 $P\times P$ Hessian？“精确”在这里不包括什么？

### TRN19-A02
比较 forward-over-reverse、reverse-over-reverse 与 gradient finite difference 三种 HVP 路径的用途和主要限制。

### TRN19-A03
写出 classical CG 需要的算子条件、Krylov 子空间与三种不能都叫“CG 收敛”的退出原因。

## B. 手算与构造

### TRN19-B01
令 $L(x,y)=x^2+xy+2y^2$，取 $v=(1,-1)^\top$。不显式依赖数值软件，计算 $Hv$；再用任意 $u=(2,1)^\top$ 验证 $u^\top Hv=v^\top Hu$。

### TRN19-B02
用初值 $p_0=0$ 对 $A=\operatorname{diag}(1,4)$、$b=(1,1)^\top$ 做两步 CG，列出 $r_k,d_k,\alpha_k,\beta_k$ 并验证得到精确解。

### TRN19-B03
对 $A=\operatorname{diag}(1,100)$，构造 residual $r=(0,10^{-3})$ 与 $r=(10^{-3},0)$，分别计算 error $e=A^{-1}r$ 的二范数。说明 residual 相同为何不代表参数误差相同。

## C. 推导与证明

### TRN19-C01
从 $\phi(\epsilon)=\nabla L(\theta+\epsilon v)$ 推导 $\phi'(0)=Hv$；再写出 reverse-over-reverse 的标量化公式 $\nabla_\theta(\nabla L^\top v)$。

### TRN19-C02
证明对 SPD 的 $A$，线性系统误差满足 $e=A^{-1}r$，并推出 $\|e\|_2\le\|r\|_2/\lambda_{\min}(A)$；解释相对 residual 阈值为何仍依赖 conditioning。

### TRN19-C03
推导 preconditioned system $M^{-1/2}AM^{-1/2}z=M^{-1/2}b$ 与 $p=M^{-1/2}z$，说明好的 $M$ 应改善哪个谱量，而不只是让 diagonal 数字“看起来更平”。

## D. 边界、反例与纠错

### TRN19-D01
构造每次 HVP 都重新采样 dropout mask 的例子，解释为何此时 CG 不再对同一个 $A$ 建立共轭方向与单一 residual 证书。

### TRN19-D02
为什么 finite-difference HVP 的步长既不能无限小也不能过大？给出截断误差与浮点消减误差的量级权衡。

### TRN19-D03
对不定矩阵给出 $d^\top Bd\le0$ 的方向，说明 classical CG 的 SPD 逻辑在哪里断裂，以及 Steihaug 方法应如何退出。

## E. AI 迁移

### TRN19-E01
设计 HVP oracle 的可复现合同，覆盖 batch、RNG、训练/评估模式、buffer、dtype、loss reduction、正则项与分布式归约。

### TRN19-E02
设计一个三层 HVP 验收：quadratic exact case、bilinear symmetry、directional finite difference。为每层写出数值断言和容差依据。

### TRN19-E03
大模型中报告“CG 只用了 10 次迭代”为什么不足？写出必须同时报告的 HVP 次数、预条件成本、global reductions、residual、model decrease 与 wall-clock 字段。

## 作答与复盘

每题记录 `independent / hinted / copied / blocked / careless`。先把所有答案写成“固定算子—迭代状态—数值证书”三栏，再打开 [[解答 - Hessian-vector Product、共轭梯度与隐式二阶步]]。

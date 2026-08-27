---
type: exercise
status: draft
topic: "[[范数、平坦性、Sharpness 与参数化不变性]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - 范数、平坦性、Sharpness 与参数化不变性]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - 范数、平坦性、Sharpness 与参数化不变性
## A
### LT-SHP-A01
定义 parameter、predictor 与 function-equivalence class。
### LT-SHP-A02
写 ReLU hidden-unit rescaling，并证明函数不变。
### LT-SHP-A03
列出四种 sharpness 定义，说明为何不能混用。
## B
### LT-SHP-B01
对 $L(a,b)=(ab-1)^2$ 推导 global-minimum Hessian 与非零 eigenvalue。
### LT-SHP-B02
比较 $(a,b)=(1,1)$ 与 $(100,0.01)$ 的 raw norm、sharpness 和 product/path measure。
### LT-SHP-B03
两层单 hidden unit 的 incoming 乘 5、outgoing 除 5，层平方 norm sum 如何变？
## C
### LT-SHP-C01
证明乘积模型同一 predictor 的 Hessian sharpness 可任意大。
### LT-SHP-C02
证明 node-wise rescaling 下每条经过该 node 的 path product 不变。
### LT-SHP-C03
构造 raw norm 与 generalization gap 排名完全相反的等价参数对。
## D
### LT-SHP-D01
审计“large batch 找到 sharper minima，因此 sharpness 导致 generalization gap”。
### LT-SHP-D02
SAM 提升 test accuracy 是否证明 raw Hessian sharpness 是因果机制？
### LT-SHP-D03
比较跨 architecture generalization measures 时必须控制哪些对象？
## E
### LT-SHP-E01
为 LoRA factor rescaling 设计 invariant complexity measure 压力测试。
### LT-SHP-E02
为量化模型定义 function-space perturbation 而非 raw parameter radius。
### LT-SHP-E03
写 generalization-measure claim card：invariance、normalization、scope、correlation、bound 与 intervention。

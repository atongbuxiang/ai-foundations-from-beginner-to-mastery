---
type: exercise
status: draft
area: [neural-networks/residual-stability, skip-connections, gating, dense-connectivity]
topic: "[[Highway、Dense Connection 与 Skip 结构比较]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Highway、Dense Connection 与 Skip 结构比较]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - Highway、Dense Connection 与 Skip 结构比较

## A

### NN-HDS-A01
定义 skip connection 的 source–transform–fusion–state shape–cost 五元组，并分别为 additive residual 与 Dense concat 填写一版。

### NN-HDS-A02
写出 additive residual、coupled Highway、Dense cumulative state 与 encoder–decoder long skip 的最小公式。

### NN-HDS-A03
解释 addition 的“坐标对齐”与 concatenation 的“坐标身份保留”分别意味着什么。

## B

### NN-HDS-B01
复算正文 Highway 标量例子 $x=2,H=-1,T=\sigma(0.5x)$ 的 $T,y,T'$ 与 $dy/dx$；再给出漏掉 gate 导数时的错误答案。

### NN-HDS-B02
Dense block 取 $C_0=48,k=16,L=5$。求每层输入通道、最终通道、输入通道总和与连接数 $L(L+1)/2$。

### NN-HDS-B03
设 $y=Px+Ax$，$P=\operatorname{diag}(1,0)$、$A=\operatorname{diag}(0,0.5)$。求 Jacobian、秩和两个坐标增益；projection shortcut 是否一定丢掉第二坐标？

## C

### NN-HDS-C01
从 $y=T\odot H+(1-T)\odot x$ 推导完整向量 Jacobian，解释三个项的来源。

### NN-HDS-C02
令 $c_\ell=[c_{\ell-1},H_\ell(c_{\ell-1})]$。推导 stacked Jacobian，并证明在精确实数与不做 compression 时，任意输入扰动都至少以原坐标出现在 $dc_\ell$ 中。

### NN-HDS-C03
证明 Dense block 第 $\ell$ 层输入宽度为 $C_0+(\ell-1)k$，最终宽度为 $C_0+Lk$；再推导所有层输入通道之和的闭式。

## D

### NN-HDS-D01
某模型把两个不同分辨率 feature maps 直接相加。列出 shape、坐标、padding、dtype 与语义对齐的检查，并说明一个合法 alignment operator 会怎样进入 Jacobian。

### NN-HDS-D02
比较参数量、FLOPs、activation memory、memory traffic 与 critical-path latency。为什么“五者中一个相同”不能推出系统成本相同？

### NN-HDS-D03
Highway gate bias 设得很负。分析 carry closeness、sigmoid saturation、gate gradient 和低精度下 gate quantization 的权衡，提出至少五项日志。

## E

### NN-HDS-E01
反驳：“DenseNet 有 $O(L^2)$ 条连接，因此参数、FLOPs、显存和有效独立路径都必为 $O(L^2)$。”分别处理四个对象。

### NN-HDS-E02
设计 add、gate、concat 三种 fusion 的公平对照，使参数/FLOPs 与宽度尽可能可比；说明无法同时完全匹配的资源以及报告方式。

### NN-HDS-E03
为一个带 long skip 的因果序列 encoder–decoder 制定泄漏审计：明确索引、mask、alignment、缓存和反事实测试。


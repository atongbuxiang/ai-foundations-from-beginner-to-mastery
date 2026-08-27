---
type: exercise
status: verified
area: [training, optimization, acceleration]
topic: "[[Nesterov、Lookahead 与动量形式的等价边界]]"
solution: "[[解答 - Nesterov、Lookahead 与动量形式的等价边界]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Nesterov、Lookahead 与动量形式的等价边界

## A. 识别与复述

### TRN05-A01
写出 heavy-ball 与 look-ahead NAG，圈出 gradient evaluation point。

### TRN05-A02
解释为什么 Nesterov look-ahead 不等同于名为 Lookahead 的 slow/fast optimizer。

### TRN05-A03
列出 NAG 与 current-gradient-plus-buffer 形式逐步映射的条件。

## B. 手算与构造

### TRN05-B01
$f(x)=x^2/2,x_0=1,v_0=0,\eta=.1,\mu=.9$。计算 $y_0,g_0,v_1,x_1,y_1$。

### TRN05-B02
用 $p_0=y_0,b_0=0$ 的 buffer 形式算 $b_1,p_1$，核对 $p_1=y_1$。

### TRN05-B03
取 $f(x)=x^4/4,x=1,v=-0.5,\mu=.9$，比较 $\nabla f(x)$ 与 $\nabla f(x+\mu v)$。

## C. 推导与证明

### TRN05-C01
从 $p_t=x_t+\mu v_t$ 推导 $p_{t+1}=p_t+\mu v_{t+1}-\eta g_t$。

### TRN05-C02
结合 $b_{t+1}=-v_{t+1}/\eta$，推导框架方向 $g_t+\mu b_{t+1}$。

### TRN05-C03
用 Taylor 展开 $\nabla f(x+\mu v)$，写出一阶 Hessian correction 和 remainder 条件。

## D. 边界、反例与纠错

### TRN05-D01
构造变化 LR 使 $b=-v/\eta$ 的常比例映射失效的两步例子。

### TRN05-D02
纠正“PyTorch Nesterov 没有在 look-ahead 点算梯度，所以只是近似 NAG”的草率说法。

### TRN05-D03
说明 dampening 或 momentum schedule 为什么要求重新推导变量映射。

## E. AI 迁移

### TRN05-E01
给出最小二次 objective 的 PyTorch Nesterov parity test，应记录哪些中间 tensor？

### TRN05-E02
审计论文“用了 Nesterov momentum”：提出关于公式、索引、初始化、LR placement 和框架版本的问题。

### TRN05-E03
设计 heavy-ball 与 NAG 的公平对照：除 final loss 外应记录 curvature、oscillation、update norm 和 wall time。

## 作答与复盘

完成独立尝试后打开 [[解答 - Nesterov、Lookahead 与动量形式的等价边界]]。

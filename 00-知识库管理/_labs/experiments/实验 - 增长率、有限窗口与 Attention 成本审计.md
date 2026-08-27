---
type: experiment
status: draft
area: [math/foundations, math/asymptotics, algorithms/complexity, ai/attention]
topic: "增长率、有限窗口与 Attention 成本审计"
prerequisites: ["[[渐近记号、增长率与复杂度]]", "[[数列、极限与完备性的直觉]]"]
related: ["[[习题 - 渐近记号、增长率与复杂度]]", "[[解答 - 渐近记号、增长率与复杂度]]", "[[推导与实验 MOC]]", "[[S-2020-Su-7546-线性Attention]]", "[[S-2023-Su-9607-量子化假设与尺度定律]]"]
code: "[[00-知识库管理/_labs/code/asymptotics_complexity_audit.py]]"
figure: "[[00-知识库管理/_assets/plots/math-foundations/plot-asymptotics-complexity-audit-v2.svg]]"
created: 2026-08-19
updated: 2026-08-23
---

# 实验 - 增长率、有限窗口与 Attention 成本审计

> [!abstract] 实验问题
> 本实验不用有限曲线“证明”渐近定理，而把四个常见误判放在同一张图里：经典增长族怎样在有限范围分离；精确operation counter的log–log斜率怎样趋近理论指数；低阶项与loss地板怎样制造随窗口变化的有效斜率；Dense Attention的projection、pairwise work与score memory怎样由$T/d$制度分界。

先看图判断：增长阶、有限窗口有效斜率、低阶项、loss floor 与 Attention 的 arithmetic/memory 制度分别会怎样改变“看起来像几次方”？

![[00-知识库管理/_assets/plots/math-foundations/plot-asymptotics-complexity-audit-v2.svg|880]]

> [!figure] 实验图｜增长层级、有限斜率与 Attention 成本制度
> A 绘制 $\log_2n,n,n\log_2n,n^2,2^n$；B 对线性与三角循环精确计数并拟合斜率；C 展示 $n^2+1000n$ 的局部指数和带地板 loss 的斜率塌缩；D 在 $d=512,h=8$ 下分开 projection、pairwise arithmetic 与 score 元素数。生成脚本：[[asymptotics_complexity_audit.py]]；无随机数，并对精确计数、斜率极限和 crossover 设断言。

**怎样读图。** A 只展示有限区间的分离；B 看到斜率接近理论值仍要回到精确计数式；C 用窗口移动解释有效指数变化；D 先比较 $T/d$ 决定 arithmetic 主项，再把不同单位的 score memory 单列，不能与 FLOPs 直接相加。

**适用边界（图没有证明什么）。** operation/memory 曲线不是 GPU wall-time，常数、带宽、kernel fusion、稀疏性和精度均未建模；有限回归斜率也不证明 Big-O/Theta，更不证明某个线性 Attention 变体在端到端任务上更优。

> [!question] 本实验的判别问题
> 如何从精确计数式、极限量词和规模制度三方面判断一条经验 scaling curve 是否真的支持所声称的复杂度结论？

## 一、复现合同

在知识库根目录运行：

    /Users/tong/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
      00-知识库管理/_labs/code/asymptotics_complexity_audit.py

环境与边界：

- Python 3标准库；
- 无网络、第三方库与随机数；
- Panel B真正枚举每个三角循环iteration，并与$n(n+1)/2$逐点assert；
- 斜率以普通最小二乘拟合$\log count$对$\log n$；
- Panel C的局部斜率使用解析导数，不用有限差分；
- Panel D只画解析operation/memory-element proxy，不冒充GPU秒数；
- 所有assertions在SVG写出前执行；
- SVG由同一脚本确定性生成。

确定性双跑：

    python3 00-知识库管理/_labs/code/asymptotics_complexity_audit.py \
      --output /tmp/asymptotics-run1.svg
    python3 00-知识库管理/_labs/code/asymptotics_complexity_audit.py \
      --output /tmp/asymptotics-run2.svg
    cmp /tmp/asymptotics-run1.svg /tmp/asymptotics-run2.svg

Canonical SVG SHA-256：

    ac3823bf754d042029d9e55bdfca30f381dbaf23f9382489678de22906f55aa3

## 二、轨道A：增长层级只在尾部承诺

### 2.1 设置

对$n=2,\ldots,32$绘制

$$
\log_2n,\quad n,\quad n\log_2n,\quad n^2,\quad2^n.
$$

纵轴取对数，只为在同一面板观察十个数量级。

### 2.2 观察

- 对数、线性与$n\log n$在小$n$时仍接近；
- $n^2$与$2^n$很快分离；
- $2^n$的指数底不能像对数底一样吸收到常数；
- 图像显示有限样本排序，但不证明任意大$n$的little-$o$关系。

正式证明仍需比值、级数界或ratio argument。例如

$$
\frac{n^2}{2^n}\to0
$$

不是由面板上“红线更陡”推出。

> [!experiment] 轨道A结论
> 增长族图最适合建立数量级直觉和寻找交叉区间；它不能替代对所有充分大$n$的统一常数与阈值。

## 三、轨道B：精确计数与有限回归

### 3.1 两个程序

线性计数：

$$
C_1(n)=n.
$$

三角计数：

$$
C_2(n)
=
\sum_{i=1}^n i
=
\frac{n(n+1)}2.
$$

脚本对$n=4,8,\ldots,1024$真正运行内层枚举，并assert计数与闭式完全相同。

### 3.2 回归结果

对$\log C$回归$\log n$：

| Counter | 拟合斜率 | 理论尾部 |
|---|---:|---|
| $C_1(n)=n$ | $1.000000$ | $\Theta(n)$ |
| $C_2(n)=n(n+1)/2$ | $1.966996$ | $\Theta(n^2)$ |

第二条没有恰好得到2，因为

$$
C_2(n)=\frac12n^2+\frac12n
$$

仍含低阶线性项。扩大$n$窗口会使斜率更接近2。

### 3.3 证据边界

即使所有点都落在完美直线上，有限回归也只验证当前计数实现和窗口；$\Theta(n^2)$来自精确闭式及其比值极限：

$$
\frac{C_2(n)}{n^2}
=
\frac12+\frac1{2n}
\to\frac12.
$$

## 四、轨道C：局部斜率、低阶项与loss地板

### 4.1 低阶项过渡

取

$$
y(n)=n^2+1000n.
$$

局部log–log斜率：

$$
p_{\rm loc}(n)
=
\frac{d\log y}{d\log n}
=
\frac{2n+1000}{n+1000}.
$$

脚本从$n=10$扫到$10^6$：

| 位置 | 局部斜率 |
|---|---:|
| $n=10$ | $1.009901$ |
| $n=10^6$ | $1.999001$ |

同一解析函数在不同窗口可以像线性、过渡幂或二次。

### 4.2 带地板loss

取

$$
L(N)=2+3N^{-0.6}.
$$

直接$\log L$的局部斜率为

$$
-0.6\frac{3N^{-0.6}}{2+3N^{-0.6}},
$$

随$N$增大趋于0；若准确扣除地板2，

$$
\log(L-2)=\log3-0.6\log N,
$$

斜率恒为$-0.6$。

> [!experiment] 轨道C结论
> 局部斜率是regime诊断器。它能暴露低阶项和地板，却不能独自识别无限尺度机制；地板估计错误会改变指数甚至令对数无定义。

## 五、轨道D：Attention中的多变量主导制度

### 5.1 Operation proxy

固定

$$
d=512,\qquad h=8
$$

并扫$T=32,\ldots,8192$。为保留实现常数直觉，使用

$$
W_{\rm proj}=4Td^2,
\qquad
W_{\rm pair}=2T^2d,
\qquad
M_{\rm score}=hT^2.
$$

前两者是operation proxy，第三者是元素数，单位不同，只能比较增长形状，不能在纵轴数值上直接说谁“更大成本”。

### 5.2 交叉

$$
4Td^2=2T^2d
\iff
T=2d=1024.
$$

所以在这个带常数的proxy中：

- $T<1024$时projection work更大；
- $T>1024$时pairwise work更大；
- score memory始终按$T^2$增长，但字节数还需乘batch、dtype和可能的head/materialization制度。

若忽略常数，只比较$\Theta(BTd^2)$与$\Theta(BT^2d)$，分界写成$T\asymp d$。

### 5.3 不可外推

本面板不能预测A100/H100/CPU的秒数，也不能比较Flash-style tiling、sparse Attention或linear Attention的quality。它只核验指定dense contraction的解析shape。

## 六、建议干预

1. 把Panel B的$n$最大值从$2^{10}$改为$2^6$与$2^{16}$，观察三角计数拟合斜率。
2. 把$1000n$改为$10^kn$，记录局部斜率过渡点怎样移动。
3. 把loss地板2改为0，再比较raw与corrected slope。
4. 将$d$改为256、1024，验证proxy交叉$T=2d$。
5. 改变投影/pairwise常数，解释“$\Theta$相同”与“交叉点改变”并存。
6. 新增一个wall-clock实验时，必须记录同步、warmup、dtype、shape、repeat、median、IQR与peak memory。

## 七、实验结论的证据边界

- 解析assert验证脚本实现与有限闭式一致；
- 双跑与hash验证产物确定性；
- XML/SVG渲染检查验证图可读；
- 曲线帮助解释有限交叉和局部斜率；
- 以上均不证明一般程序、无限规模、所有Attention实现或真实神经Scaling Law；
- 真正的渐近结论仍需定义中的统一常数、阈值与全尾部证明；
- 真实AI性能还需quality-controlled benchmark与hardware profiler。

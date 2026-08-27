---
type: derivation
status: verified
area: [training, optimization, averaging, ema, swa]
node_id: TRN-39
aliases: [权重平均总账, Parameter EMA SWA and Checkpoint Averaging]
prerequisites: ["[[数列、极限与完备性的直觉]]", "[[训练时域、Restart、Schedule-Free 与末端学习率]]", "[[Momentum、EMA、偏差修正与框架约定]]"]
related: ["[[Bayesian Posterior Predictive、Ensemble 与近似边界]]", "[[Checkpoint 选择、验证泄漏与 Compute-matched 比较]]", "[[遮蔽预测、Teacher–Student 与自监督目标]]"]
sources: ["[[S-2018-Izmailov-SWA]]", "[[S-2024-Morales-Brotons-EMA]]", "[[S-2025-Su-11459-WD-LR-Memory]]", "[[S-2019-Maddox-SWAG]]", "[[S-2017-Tarvainen-Valpola-Mean-Teacher]]"]
exercises: ["[[习题 - 参数 EMA、SWA 与 Checkpoint Averaging]]"]
solutions: ["[[解答 - 参数 EMA、SWA 与 Checkpoint Averaging]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-parameter-ema-swa-prediction-average-ledger-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# 参数 EMA、SWA 与 Checkpoint Averaging

> [!abstract] 一句话结论
> 参数 EMA、SWA、离线 checkpoint averaging 与 prediction ensemble 平均的是不同对象。非线性网络中“平均参数后预测”通常不等于“各模型预测后平均”；averaging 的窗口、时钟、归一化统计、对称性对齐和 checkpoint selection 都属于算法合同。

## 一、先分清五种“平均”

训练中常见：

1. optimizer momentum：平均梯度或更新方向；
2. parameter EMA：指数平均参数；
3. Polyak/SWA/checkpoint average：算术或加权平均参数；
4. prediction ensemble：平均概率、logit 或其他输出；
5. SWAG：用轨迹均值和协方差拟合参数分布并采样预测。

它们的对象分别是：

$$
g_t,\quad
\theta_t,\quad
f_{\theta_t}(x),\quad
\text{或参数分布}.
$$

只写“用了 EMA”是不完整的。

## 二、参数 EMA 的递推与权重

定义

$$
\bar\theta_t
=\beta\bar\theta_{t-1}
+(1-\beta)\theta_t,
\qquad 0\le\beta<1.
\tag{1}
$$

若 $\bar\theta_0=\theta_0$，展开：

$$
\bar\theta_t
=\beta^t\theta_0
+(1-\beta)\sum_{i=1}^{t}\beta^{t-i}\theta_i.
\tag{2}
$$

距离当前 $k$ 步的 checkpoint 权重为 $(1-\beta)\beta^k$。

### 有效窗口与半衰期

常用量级：

$$
N_{\mathrm{eff}}\approx\frac{1}{1-\beta},
\tag{3}
$$

半衰期为

$$
h_{1/2}
=\frac{\log(1/2)}{\log\beta}.
\tag{4}
$$

例如 $\beta=0.999$ 的 step 半衰期约 693 step。但若每 step 的 token 数翻倍，token 半衰期也翻倍；跨 batch 比较必须换算时钟。

### 零初始化与 Bias Correction

若 $\bar\theta_0=0$，权重总和为 $1-\beta^t$，可写

$$
\widehat{\bar\theta}_t
=\frac{\bar\theta_t}{1-\beta^t}.
\tag{5}
$$

多数 weight EMA 直接用 $\bar\theta_0=\theta_0$，不需要这种修正。必须记录初始化约定。

## 三、Checkpoint Averaging 与 SWA

给定选择的 $K$ 个 checkpoint：

$$
\theta_{\mathrm{avg}}
=\sum_{k=1}^K\alpha_k\theta_{t_k},
\qquad
\alpha_k\ge0,\quad \sum_k\alpha_k=1.
\tag{6}
$$

uniform checkpoint average 取 $\alpha_k=1/K$。

SWA 的典型合同是：

- 在训练后段使用常数或周期 LR；
- 从指定起点开始按间隔收集轨迹点；
- 对参数做均匀平均；
- 对 BatchNorm 等运行统计重新估计。

[[S-2018-Izmailov-SWA]] 报告这种平均可落在训练轨迹所围绕的更中心区域，并在其视觉任务协议上改善泛化。

> [!warning] “更平”不是坐标不变结论
> raw Hessian sharpness 会随参数重缩放改变。SWA 的实证结果与几何解释应分层，不把“宽极小”写成普遍泛化定理。

## 四、参数平均不等于预测平均

参数平均模型输出：

$$
f_{\theta_{\mathrm{avg}}}(x).
\tag{7}
$$

预测平均可能是：

$$
\sum_k\alpha_k f_{\theta_{t_k}}(x).
\tag{8}
$$

一般

$$
f_{\sum_k\alpha_k\theta_k}(x)
\ne
\sum_k\alpha_k f_{\theta_k}(x).
\tag{9}
$$

只有当 $f_\theta(x)$ 对 $\theta$ 仿射，或 checkpoints 足够近使局部线性化成立时，两者才近似。

### 二阶差异

令 $\theta_k=\bar\theta+\delta_k$ 且 $\sum\alpha_k\delta_k=0$。Taylor 展开：

$$
\sum_k\alpha_k f_{\theta_k}(x)
\approx
f_{\bar\theta}(x)
+\frac12
\sum_k\alpha_k
\delta_k^\top H_\theta f_{\bar\theta}(x)\delta_k.
\tag{10}
$$

差异由参数曲率与 checkpoint spread 决定。平均 logits、softmax probabilities、log probabilities 也互不等价。

## 五、参数对称性会让平均失效

两层网络存在 hidden-unit permutation symmetry：交换同一隐层单元及相邻权重，函数不变但参数坐标改变。

若 $\theta_1,\theta_2$ 表示同一函数却处在不同置换轨道，直接平均

$$
\frac{\theta_1+\theta_2}{2}
$$

可能得到很差模型。类似问题还包括：

- attention head permutation；
- ReLU 正齐次 rescaling；
- sign/rotation symmetry；
- 不同独立 run 的 mode connectivity 不保证。

同一连续训练轨迹中的近邻 checkpoint 往往对齐得更好，但也不能无条件保证。

## 六、Normalization 运行统计不是普通参数

BatchNorm 模型包含：

- trainable $\gamma,\beta$；
- running mean/variance；
- batch counter 或 momentum 约定。

只平均 trainable parameters、保留最后 checkpoint 的 running stats，会形成混合模型。SWA 常在平均后用训练数据重新估计 BN statistics。

对 LayerNorm/RMSNorm 没有同样的 running stats，但 dropout、EMA teacher buffer、quantization observer、tokenizer/data normalization 仍需检查。

## 七、EMA 的 Train/Eval 与 Teacher 语义

参数 EMA 可用于：

1. 只在 evaluation/deployment 使用；
2. 作为 self-distillation/consistency teacher；
3. 产生 pseudo-label；
4. 初始化下一阶段；
5. 参与 checkpoint selection。

Mean Teacher 中 teacher 预测进入训练目标，因此 EMA 改变后续 student trajectory；这与“训练不变、只在末尾评估 EMA”不同。

[[S-2024-Morales-Brotons-EMA]] 系统研究 weight EMA 的独立收益与调参；[[S-2017-Tarvainen-Valpola-Mean-Teacher]] 则是 EMA teacher 进入训练闭环的代表。

## 八、EMA 与 LR Schedule 的耦合

当 raw trajectory 的噪声和漂移随 $\eta_t$ 变化时，固定 $\beta$ 的意义也变化：

- 高 LR 时窗口内 checkpoint spread 大；
- cooldown 时 raw trajectory 移动变慢，EMA 可能滞后；
- 训练末尾刚改变数据分布，长 EMA 会混入旧域；
- batch/token 改变后同一个 $\beta$ 对应不同数据窗口。

若想固定 token half-life $H$，每 step 处理 $b_t$ token，可令

$$
\beta_t=2^{-b_t/H}.
\tag{11}
$$

这与固定 step-based $\beta$ 是不同算法。

## 九、SWA、EMA 与 SWAG 的边界

| 方法 | 保存对象 | 输出 | 主要额外成本 | 不自动等于 |
|---|---|---|---|---|
| EMA | 1 份平均参数 | 单模型 | 1×参数存储 | posterior mean |
| checkpoint avg | 多点或在线和 | 单模型 | checkpoint IO/或在线累加 | prediction ensemble |
| SWA | 后段轨迹均值 + 统计重估 | 单模型 | 低 | Bayesian averaging |
| ensemble | 多模型预测 | 多前向 | 推理乘成员数 | 参数平均 |
| SWAG | 均值+低秩/对角协方差 | 采样 ensemble | 协方差与多前向 | exact posterior |

[[S-2019-Maddox-SWAG]] 是 approximation contract，不把局部 Gaussian 轨迹分布当真实 posterior。

## 十、一个可复现 Averaging 合同

至少记录：

$$
\mathcal A
=(
\text{object},
\text{start},
\text{clock},
\text{weights},
\text{frequency},
\text{state init},
\text{BN policy},
\text{train/eval use},
\text{selection}
).
\tag{12}
$$

并保存：

- raw last checkpoint；
- averaged checkpoint；
- averaging counter/weight sum；
- source checkpoint 列表或可重建日志；
- optimizer/scheduler state 是否与 averaged weights 配套。

注意：把 averaged weights 与 raw optimizer moments 一起继续训练，通常不是原算法的无缝 resume。

## 十一、图：五种平均对象不要混账

先看图回答：EMA、SWA、checkpoint average、prediction ensemble 与 SWAG 平均了什么，何时可能等价？

![[00-知识库管理/_assets/figures/training-optimization/fig-parameter-ema-swa-prediction-average-ledger-v1.svg|880]]

> [!figure] 图 TRN-39　参数平均—预测平均—状态重估总账
> 左侧显示 EMA/SWA 对同一轨迹参数点加权，中间区分 $f_{\bar\theta}$ 与 $\sum\alpha f_{\theta_k}$，右侧列出 BN 重估、对称性、时钟和 teacher feedback 四个边界。来源：依据 [[S-2018-Izmailov-SWA]]、[[S-2024-Morales-Brotons-EMA]]、[[S-2019-Maddox-SWAG]] 原创绘制。

**怎样读图**：先沿箭头确认平均发生在 gradient、parameter 还是 prediction 空间；再看 checkpoints 是否坐标对齐；最后核对运行统计和 train/eval 输出。

**图没有证明什么**：它不证明参数平均必然改善泛化，也不把 EMA/SWA 等价为 Bayesian model averaging。

## 十二、科学空间研读框

[[S-2025-Su-11459-WD-LR-Memory]] 把 decay 后的参数写成历史 update 的加权和，这与 parameter averaging 有相似的“记忆核”语言。但两者不是同一状态：decay kernel 作用于 optimizer updates，weight EMA 作用于已经生成的参数 iterates；递推对象、系数和部署语义都不同。

## 十三、初学者自检

1. $\beta=0.999$ 的 step 半衰期约多少？
2. 为什么参数平均通常不等于预测平均？
3. SWA 后为什么常需重新估计 BatchNorm stats？
4. 两个函数相同但 hidden units 置换的网络，为何参数平均可能很差？
5. 把 averaged weights 和 raw optimizer moments 配对继续训练有什么问题？

## 十四、本节出口

你应能对任何“模型平均”声明：

$$
\text{averaged object}
\to
\text{weighting clock}
\to
\text{symmetry/statistics policy}
\to
\text{train/eval/deploy output},
$$

并用式 (10) 解释 parameter average 与 prediction ensemble 的差异。

## 练习与独立解答

- [[习题 - 参数 EMA、SWA 与 Checkpoint Averaging]]
- [[解答 - 参数 EMA、SWA 与 Checkpoint Averaging]]

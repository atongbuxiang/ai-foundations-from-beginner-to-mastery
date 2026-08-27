---
type: moc
status: active
area: [training, optimization, sgd]
aliases: [训练与优化第一卷, SGD 与随机优化噪声]
prerequisites: ["[[随机梯度与小批量估计]]", "[[加速梯度、动量与下界]]", "[[相图、平衡点与局部稳定性]]"]
related: ["[[训练与优化 MOC]]", "[[训练与优化完整课程地图与掌握标准]]", "[[科学空间 - 第六章训练与优化专题来源地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# SGD、Momentum 与随机优化噪声 MOC

> [!abstract] 分卷目标
> 本卷先把训练写成“数据迭代器—梯度估计—优化器状态—参数更新”的状态机，再进入 Momentum/Nesterov、二次稳定域和梯度噪声。读完后应能解释同名 SGD 在 reduction、accumulation、shuffle、momentum convention 不同时为何不是同一算法。

## 八个核心节点

| ID | 节点 | 主要出口 | 状态 |
|---|---|---|---|
| TRN-01 | [[训练系统的对象、状态与一步更新合同]] | 写出完整 step state transition | 静态验收通过；个人掌握另计 |
| TRN-02 | [[Mini-batch 梯度、平均求和与有效 Batch]] | 对齐 loss reduction 与 LR | 静态验收通过；个人掌握另计 |
| TRN-03 | [[SGD、采样顺序与梯度累积的等价边界]] | 判断 micro-batch equivalence | 静态验收通过；个人掌握另计 |
| TRN-04 | [[Momentum、EMA、偏差修正与框架约定]] | 互译 velocity/buffer/EMA | 静态验收通过；个人掌握另计 |
| TRN-05 | [[Nesterov、Lookahead 与动量形式的等价边界]] | 区分 gradient evaluation point | 静态验收通过；个人掌握另计 |
| TRN-06 | [[二次模型的学习率—动量稳定域与阻尼]] | 用根和谱分析振荡/发散 | 静态验收通过；个人掌握另计 |
| TRN-07 | [[梯度噪声协方差、Noise Scale 与 SDE 近似]] | 分账有限 batch 与连续近似 | 静态验收通过；个人掌握另计 |
| TRN-08 | [[Critical Batch、隐式偏置与 SGD 证据地图]] | 审计效率、sharpness、泛化主张 | 静态验收通过；个人掌握另计 |

## 贯穿符号

设参数 $\theta_t\in\mathbb R^d$，单样本损失 $\ell(\theta;Z)$，population gradient $g(\theta)=\mathbb E[\nabla\ell]$，batch estimator $\widehat g_{B,t}$，optimizer state $s_t$。统一把一步写成

$$
(\theta_{t+1},s_{t+1})=\mathcal U_t(\theta_t,s_t,\widehat g_{B,t};h_t),
$$

其中 $h_t$ 包含 LR、momentum、decay、clipping 和 precision。任何“等价”都必须说明是 estimator、单步 update、参数轨迹还是分布意义。

## 科学空间入口

- [[S-2018-Su-5655-SGD到动量加速]]：动力学与动量入口；
- [[S-2019-Su-6261-优化动力学整体视角]]：整体轨迹而非单步方向；
- [[S-2020-Su-7787-有限学习率与隐式正则]]：有限步长改变动力学的问题；
- [学习率—Batch Size 系列](https://spaces.ac.cn/archives/11260)：noise scale 与 critical batch 的当代推导入口。

## 分卷验收

- 手算 mean/sum reduction 下两步 SGD；
- 互译三种 Momentum convention 并逐步核对；
- 画出两个 Hessian eigenmode 的稳定/振荡区；
- 用 Monte Carlo 验证 covariance 的 $1/B$ 缩放并构造相关采样反例；
- 说明“更大 batch 更快”在 step、sample、FLOPs 和 wall time 四种口径下为何不同。

## 图、实验与练习闭环

- 每个核心节点各有一张教材式解释图，共 8 张；
- [[实验 - SGD、Momentum 与随机优化噪声最小数值审计]]生成 3 张可复现实验图和 JSON/CSV 结果；
- 每个节点 15 题，共 120 题，题目与独立解答文件分离；
- [[60.1 分卷累计测验与复现门]]包含 60 分闭卷推导与 40 分开卷复现；
- [[60.1 静态完成与质量审计]]记录交付物、机器检查、人工读图与完成边界；
- 静态材料完成不等于学习者通过，掌握状态仍以独立作答和复现为准。

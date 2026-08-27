---
type: concept
status: verified
area: [generative-models, gan, reproducibility]
node_id: GEN-24
prerequisites: ["[[Mode Collapse、模式覆盖与生成器熵]]", "[[Minimax 动力学、旋转、阻尼与局部收敛]]"]
related: ["[[采样器、条件控制、加速与评估 MOC]]", "[[IPM、Wasserstein-1 与 Kantorovich 对偶]]"]
sources: ["[[S-2021-Su-8244-WGAN成功与距离近似]]", "[[S-2017-Heusel-TTUR]]", "[[S-2018-Mescheder-GAN-Convergence]]", "[[S-2015-Theis-Generative-Evaluation]]"]
exercises: ["[[习题 - GAN 稳定化方法、受控比较与证据地图]]"]
solutions: ["[[解答 - GAN 稳定化方法、受控比较与证据地图]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-gan-stabilization-evidence-ledger-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# GAN 稳定化方法、受控比较与证据地图

> [!abstract] 本节主问题
> “稳定化技巧”可能改 objective、critic constraint、optimizer dynamics、architecture、data/evaluator 或部署采样。若一次改多项，只能证明组合 recipe 有效，不能判定是 Wasserstein 距离、gradient penalty 或网络结构单独造成提升。

## 一、六类干预

| 类别 | 例子 | 直接改变 |
|---|---|---|
| objective | logistic、hinge、Wasserstein、f-GAN | population/restricted game payoff |
| regularization | R1、GP、SN、instance noise | critic field/function class |
| optimizer | TTUR、extragradient、Adam betas | 离散 dynamics |
| schedule | critic steps、warm-up、EMA | 时间尺度/部署参数 |
| architecture | ResNet、normalization、attention | capacity/conditioning |
| data/eval | augmentation、preprocess、FID encoder | estimand 与 estimator |

## 二、常用 hinge game

Discriminator 最小化

$$
L_D=E_{real}\max(0,1-f(x))
+E_{fake}\max(0,1+f(\tilde x)),
$$

generator 常最小化

$$
L_G=-E_{fake}f(\tilde x).
$$

它不是概率 calibrated discriminator，也不能把 score 直接解释为 density ratio。margin 外 discriminator gradient 为零，是 design choice。

## 三、公平比较的最小因子表

比较 A/B 时至少锁定：

- dataset split、resolution、augmentation；
- generator/critic architecture 与参数/compute；
- batch size、optimizer、learning rates、betas、update ratio；
- regularization strength/frequency；
- training examples、wall-clock、NFE 与 hardware；
- EMA/truncation/checkpoint selection；
- evaluator version、preprocess、sample count；
- seed 数、failure/collapse 定义与置信区间。

只匹配 epoch 而 batch/update ratio 不同，不是同 compute。

## 四、WGAN 因果主张的对照

要声称改进来自 $W_1$ geometry，至少比较：

1. 同 architecture/optimizer 的 logistic vs Wasserstein payoff；
2. 同 payoff 下 clipping/GP/SN/R1；
3. 同 regularizer 下不同 critic class；
4. critic objective 与独立 OT estimate/coverage 的关系；
5. equal compute 与多 seed。

若只换整个 recipe，成功可能来自 smoother critic、capacity control、gradient scale 或 optimizer conditioning。

## 五、稳定的 operational definition

“稳定”需预注册为可测事件，例如：

- 训练 $T$ 步无 NaN/爆炸；
- 多 seed 中 FID/recall 在阈值内；
- mode count 不低于阈值；
- gradient/update norm 有界；
- checkpoint selection 不依赖测试集；
- 对超参数小扰动性能连续。

loss 看起来平滑不是充分条件。

## 六、证据等级

1. 单 seed 画廊：发现现象；
2. toy controlled modes：验证机制候选；
3. matched ablation + multi-seed：经验因果增强；
4. 多数据/架构复现：外推增强；
5. local theorem：在明确假设下解释动力学；
6. global/universal claim：需要远强于常见证据。

## 七、科学空间研读框

[[S-2021-Su-8244-WGAN成功与距离近似]]承担关键质疑：好结果不能反推 critic 准确估计 $W_1$。本节把该质疑转成可执行消融，而不采纳“Wasserstein 完全无关”的普遍否定。[[S-2019-Su-6280-Wasserstein距离与WGAN]]负责理论入口，[[S-2018-Su-6051-Lipschitz约束]]负责约束层，一级论文负责直接定义与证据。

## 八、图：一个结果可能由六层共同造成

先看图回答：论文同时换 hinge、SN、ResNet、TTUR、augmentation 与 EMA 时，最终 FID 箭头能归因给哪一项？还缺哪些消融？

![[00-知识库管理/_assets/figures/generative-models/fig-gan-stabilization-evidence-ledger-v1.svg|900]]

> [!figure] 图 50.3-08　GAN 稳定化干预—证据责任账
> 图将六类干预汇入训练结果，并在右侧设置 objective、compute、seed、metric 四道隔离门。来源：依据受控实验原则独立绘制。

**怎样读图**：从结果逆向追踪每个同时变化的因子；只有跨过匹配消融门的差异才可作有限因果归因。

**图没有证明什么**：图不证明任何 recipe 最优，也不保证常用指标不被 gaming；它规范主张强度。

## 九、本节回顾

- objective、constraint、optimizer、schedule、architecture 与 data/eval 是六类不同干预；
- hinge score 不是概率或 density ratio；
- 公平比较需匹配 compute、protocol、seed 与 evaluator；
- WGAN 成功可能含 geometry 与 regularization/dynamics 多重机制；
- “稳定”必须 operationalize；
- 组合 recipe 结果不能单组件归因。

## 十、练习与独立详解

- [[习题 - GAN 稳定化方法、受控比较与证据地图]]
- [[解答 - GAN 稳定化方法、受控比较与证据地图]]

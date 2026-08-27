---
type: moc
status: active
area: [generative-models, guidance, inverse-problems, sampling, evaluation]
aliases: [生成模型第九卷, 生成采样控制与评估课程地图]
prerequisites: ["[[DDPM、DDIM 与离散时间扩散 MOC]]", "[[SDE、概率流 ODE 与 Flow Matching MOC]]", "[[条件概率、全概率与 Bayes 公式]]", "[[Euler、Runge-Kutta 与离散化误差]]"]
related: ["[[生成模型 MOC]]", "[[生成模型完整课程地图与掌握标准]]", "[[科学空间 - 第五章生成模型专题来源地图]]"]
created: 2026-08-25
updated: 2026-08-25
---

# 采样器、条件控制、加速与评估 MOC

> [!abstract] 分卷目标
> 这一卷不再只问“模型学到了什么”，而是追问：**怎样把它引向条件、约束和观测？怎样用有限次网络调用把连续动力学算出来？怎样把多步教师压成一步模型？最后又凭什么说一个生成器更好？** 全卷坚持四本账：目标分布、learned field、finite sampler、evaluation protocol。任何一项改善都不能自动替另外三项作证。

## 一、八个核心节点

| ID | 节点 | 必须掌握的出口 | 状态 |
|---|---|---|---|
| GEN-65 | [[条件生成、Bayes 分解与 Classifier Guidance]] | 从 Bayes 推 conditional score，并把梯度正确放进 reverse SDE/ODE 或 Gaussian reverse kernel | verified |
| GEN-66 | [[Classifier-Free Guidance、尺度与质量多样性前沿]] | 固定 scale convention，解释条件/无条件外推、质量—覆盖与负提示 | verified |
| GEN-67 | [[逆问题、约束采样与 Plug-and-Play 控制]] | 分开 $p(y\mid x_0)$、$p(y\mid x_t)$、$\hat x_0$ 近似和 posterior sampler | verified |
| GEN-68 | [[扩散 SDE、ODE Solver、步长与 NFE 总账]] | 分开模型误差、数值误差、随机误差与 wall-time；按 NFE 比 Euler/Heun/DPM-Solver | verified |
| GEN-69 | [[扩散蒸馏、一致性模型与 Shortcut]] | 比较 teacher trajectory、trajectory consistency 与 step-conditioned composition | verified |
| GEN-70 | [[平均速度、MeanFlow 与有限步生成]] | 从 path average 推有限区间恒等式，区分 field、average velocity 与 finite map | verified |
| GEN-71 | [[Likelihood、FID、KID、Precision–Recall 与人类评估]] | 用多指标测 fidelity、coverage、conditionality、memorization 与成本 | verified |
| GEN-72 | [[生成模型实验协议、FD Loss 与前沿证据地图]] | 把 metric-as-loss、选择偏差、encoder gaming 和复现实验写成预注册协议 | verified |

## 二、贯穿全卷的四层对象

| 层 | 典型对象 | 问题 | 常见偷换 |
|---|---|---|---|
| 目标 | $p(x\mid y)$、$p(x\mid \text{measurement})$ | 想从哪个分布采样？ | 把 prompt adherence 当完整 posterior |
| 模型 | score、noise、velocity、endpoint map | 网络近似什么 population quantity？ | 把代数可换当训练等价 |
| 算法 | guidance、solver、distillation、finite map | 有限计算怎样近似目标？ | 把 ODE 阶数当生成质量保证 |
| 评价 | likelihood、FD/MMD、P/R、人评 | 哪个表示、样本量和任务口径？ | 把单个 FID 当“真实质量” |

如果一个实验只报告“FID 下降”，最少还缺：同一 evaluator 与预处理、样本数、随机区间、precision/recall 或 coverage、条件一致性、NFE/wall-time，以及是否用该指标选 checkpoint 或直接训练。

## 三、统一 guidance convention

本卷统一把无条件/条件预测记为 $r_u,r_c$，其中 $r$ 必须另注明是 score、noise、velocity 还是 data prediction。Classifier-free guidance 固定为

$$
\boxed{r_{cfg}=r_u+w(r_c-r_u).}
$$

因此：

- $w=0$：无条件预测；
- $w=1$：普通条件预测；
- $w>1$：从无条件穿过条件点继续外推；
- $w<0$：远离条件方向，通常不等于合法“负提示”语义。

有些软件把“额外 guidance”记为 $s=w-1$，或写成 $r_c+s(r_c-r_u)$。读论文/代码必须先代入零点和单位点测试，不能只比参数名。

## 四、Bayes 主桥

在 $p_t(y)>0$ 且可微时，

$$
\log p_t(x\mid y)=\log p_t(x)+\log p_t(y\mid x)-\log p_t(y),
$$

故

$$
\boxed{\nabla_x\log p_t(x\mid y)
=\nabla_x\log p_t(x)+\nabla_x\log p_t(y\mid x).}
$$

这一行连接 GEN-65—67，但不替代实现：

1. 分类器是否真估计 noisy $p_t(y\mid x_t)$；
2. 观测通常作用在 $x_0$，所以 $p(y\mid x_t)$ 是积分而非直接 likelihood；
3. score 修改进入 reverse SDE 与 probability-flow ODE 时系数不同；
4. finite step、clipping、thresholding 会改变实际 sampler。

## 五、低步数生成的三条路线

| 路线 | 学习/近似对象 | 训练信号 | 部署 | 核心风险 |
|---|---|---|---|---|
| solver | instantaneous field 的积分 | 已训练 field，无额外训练或少量校正 | 多次 NFE | learned field error 不随 order 消失 |
| distillation/consistency | teacher endpoint 或 trajectory invariant | teacher solver / EMA / adjacent pairs | 一步或少步 | teacher bias、off-trajectory error |
| Shortcut/MeanFlow | step-conditioned displacement / average velocity | composition identity / velocity identity | 可变步数或一步 | composition、interval 泛化与目标自依赖 |

“一步生成”只是部署预算，不是统一算法类别。两种 1-NFE 模型可能分别学习 endpoint、average velocity 或 adversarial generator，不能只按 NFE 合并。

## 六、NFE 与误差总账

对 $\dot x=v(x,t)$，如果 $v_\theta=v+e_\theta$，最终误差可概念性分解为

$$
\text{terminal error}
\lesssim \text{initial/terminal mismatch}
+\text{field error}
+\text{discretization error}
+\text{floating/stochastic error},
$$

并被 dynamics stability 常数放大。高阶 solver 主要降低第三项；更好的模型主要降低第二项。NFE 计数规则：每次 denoiser/score/velocity 网络 forward 算 1；Heun 一步通常 2 NFE；multistep 的 warm-up 单独记；classifier guidance 还要记录 classifier backward 成本，不能只算生成网络 forward。

## 七、评价矩阵

| 维度 | 候选测量 | 不能单独证明 |
|---|---|---|
| likelihood/calibration | NLL/BPD、ELBO、importance estimate | 感知质量、语义一致性 |
| fidelity | FID/FD、KID、precision、人类 realism | coverage 与新颖性 |
| coverage | recall、density/coverage、类别/属性覆盖 | 单样本美观 |
| conditionality | classifier/CLIP/task score、人工配对判断 | 无偏、因果遵循、事实正确 |
| memorization | nearest-neighbor、membership/copy audit | 完整隐私安全 |
| computation | NFE、latency、throughput、memory、energy | 质量等价 |

评价协议必须固定 dataset split、sample count、encoder、preprocessing、reference statistics、seed 与置信区间。FID/KID 数值跨不同 encoder 或 resize pipeline 不可直接横比。

## 八、科学空间研读主线

| 科学空间文章 | 本卷承担 | 一级来源补严 |
|---|---|---|
| [[S-2022-Su-9257-条件控制生成]] | Bayes、classifier guidance、CFG 中文入口 | [[S-2021-Dhariwal-Nichol-Classifier-Guidance]]、[[S-2022-Ho-Salimans-CFG]] |
| [[S-2024-Su-10055-信噪比与大图生成下]] | 非分类器 guidance 与 SNR 对齐案例 | 原论文与受控分辨率复现 |
| [[S-2023-Su-9881-中值定理加速ODE采样]]、[[S-2024-Su-10077-Skip-Tuning]] | solver/架构调用的加速入口 | [[S-2022-Lu-DPM-Solver]] 与数值分析 |
| [[S-2024-Su-10085-SiD上]]、[[S-2024-Su-10567-SiD下]] | identity distillation 与程序梯度 | 原论文、finite-difference audit |
| [[S-2024-Su-10617-Shortcut步长条件]]、[[S-2024-Su-10633-一致性模型]] | finite-step self-consistency | [[S-2023-Song-Consistency-Models]]、[[S-2024-Frans-Shortcut-Models]] |
| [[S-2025-Su-10958-瞬时速度与平均速度]] | instantaneous/average 对象区分 | [[S-2025-Geng-MeanFlow]] |
| [[S-2025-Su-11428-预测数据而非噪声]] | 参数化与低秩优化假说 | 特定架构消融，不能普遍外推 |
| [[S-2026-Su-11738-FD-Loss]] | FD gradient 与流式 population | [[S-2026-Yang-Representation-Frechet-Loss]]、FID/KID/P-R 文献 |

## 九、学习出口

- 数值审计：[[实验 - Guidance、Solver、MeanFlow 与评价指标最小审计]]
- 累计门：[[50.9 分卷累计测验与复现门]]
- 上一卷：[[离散扩散、潜空间与多模态生成 MOC]]
- 课程总出口：[[生成模型完整课程地图与掌握标准]]

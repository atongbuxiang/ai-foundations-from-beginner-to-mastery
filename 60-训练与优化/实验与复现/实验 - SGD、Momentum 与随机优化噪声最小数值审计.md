---
type: experiment
status: verified
area: [training, optimization, reproducibility]
experiment_id: EXP-TRN-601-V1
related: ["[[训练系统的对象、状态与一步更新合同]]", "[[Mini-batch 梯度、平均求和与有效 Batch]]", "[[SGD、采样顺序与梯度累积的等价边界]]", "[[Momentum、EMA、偏差修正与框架约定]]", "[[二次模型的学习率—动量稳定域与阻尼]]", "[[梯度噪声协方差、Noise Scale 与 SDE 近似]]", "[[Critical Batch、隐式偏置与 SGD 证据地图]]"]
script: "[[experiment_sgd_momentum_noise_audit_v1.py]]"
results: "[[00-知识库管理/_labs/experiments/trn60.1-sgd-momentum-noise-audit-v1/results.json]]"
created: 2026-08-26
updated: 2026-08-26
---

# 实验 - SGD、Momentum 与随机优化噪声最小数值审计

> [!abstract] 实验结论
> 标准库脚本以确定性小例子和 30,000 次 Monte Carlo 同时验证 60.1 的代数合同与统计缩放：正确翻译时应相等的量达到机器精度；clipping、sequential updates 与变化 LR 则产生可定位的不等价；batch-mean variance 与 $C/B$ 的最大相对误差为 1.22%。Critical-batch 图只复现经验模型形状，不当作真实训练结论。

## 一、研究问题与可证伪预期

| ID | 问题 | 预期 |
|---|---|---|
| H1 | mean/sum 能否靠 LR 翻译？ | 固定 $B$ 时误差 $<10^{-12}$ |
| H2 | accumulation 是否等于大 batch？ | 冻结参数时相等；sequential 与 clip 反例不等 |
| H3 | buffer/velocity 是否可互译？ | 常 LR 误差 $<10^{-12}$；变 LR 分叉 |
| H4 | heavy-ball 边界是否对齐解析式？ | $\mu=.9$ 时 upper $=3.8$ |
| H5 | iid batch variance 是否为 $C/B$？ | 各 $B$ Monte Carlo relative error $<5\%$ |
| H6 | critical-batch 双曲线是否在 $B_n$ 交于 2？ | $B_n=256$ 时两成本均为 2 |

## 二、环境与复现命令

- 脚本：[[experiment_sgd_momentum_noise_audit_v1.py]]；
- 依赖：Python 3 标准库，无 NumPy/PyTorch；
- seed：`20260826`；
- Monte Carlo repeats：`30000`；
- 结果：`00-知识库管理/_labs/experiments/trn60.1-sgd-momentum-noise-audit-v1/`；
- 正式 plots：`00-知识库管理/_assets/plots/training-optimization/`。

```bash
python3 "00-知识库管理/_labs/code/experiment_sgd_momentum_noise_audit_v1.py"
```

脚本退出码只有在六项检查全部通过时为 0，并写出 JSON、四个 CSV 与三张 SVG。

## 三、确定性合同结果

| 检查 | 结果 |
|---|---:|
| mean step $\theta^+$ | 0.7 |
| matched sum step $\theta^+$ | 0.7 |
| unmatched sum step | 0.4 |
| frozen batch/accumulated gradient | $-2/-2$ |
| one batch step / two sequential steps | $0.2/0.39$ |
| sum of micro clips / clip after sum | $0/1$ |
| constant-LR buffer–velocity max error | 0 |
| variable-LR second update | $-0.019$ vs $-0.1$ |

这组结果区分了三种情况：应该完全相等、由于有限精度只需容差相等、因算法合同不同而必须不等。

## 四、实验图 1：$1/B$ covariance law

先看图回答：经验点是否沿解析 $C/B$ 曲线下降，误差是否随 $B$ 出现系统偏离？

![[00-知识库管理/_assets/plots/training-optimization/plot-batch-covariance-scaling-v1.svg|900]]

> [!figure] 图 EXP-TRN-601-01　四点 gradient population 的 batch-mean variance
> 蓝点为 30,000 次 with-replacement Monte Carlo，绿线为 $C/B$；最大相对误差 1.22%。来源：脚本 [[experiment_sgd_momentum_noise_audit_v1.py]]，seed `20260826`，生成于 2026-08-26。

**怎样读图**：横轴按 $1,2,4,\ldots,64$ 倍增，纵轴为 batch mean 的 empirical variance；点线重合验证二阶矩公式，不是拟合出 $1/B$。

**图没有证明什么**：有限四点总体不代表深网 gradient distribution；实验没有 heavy tail、相关样本、BatchNorm 或数据非平稳性。

Without-replacement 端点也通过：$B=4=N$ 时经验与理论 variance 都为 0；$B=2$ 理论 $5/3$，经验约 1.6629。

## 五、实验图 2：Heavy-ball 根扫描

先看图回答：$\mu=.9$ 时为什么大部分复根区 spectral radius 几乎恒为 $\sqrt{.9}$，又在哪里越过 1？

![[00-知识库管理/_assets/plots/training-optimization/plot-heavy-ball-stability-audit-v1.svg|900]]

> [!figure] 图 EXP-TRN-601-02　Heavy-ball 根的数值扫描与解析边界
> 蓝线为 $\max|r_\pm|$；琥珀线标根类型边界约 0.00263 与 3.79737，红线标稳定上界 3.8。来源：同一标准库脚本直接计算复根，不用手工摆点。

**怎样读图**：在复根区 Vieta 公式给根模 $\sqrt\mu$，所以出现平台；跨过 3.8 后至少一根越出单位圆。

**图没有证明什么**：这是固定 scalar quadratic mode 的谱半径，不是神经网络 loss curve，也不包含 finite-time transient 与 stochastic forcing。

## 六、实验图 3：Critical-batch 经验双曲线

先看图回答：为何 $B=256$ 同时是 step 与 example 两条归一化成本为 2 的交点，而不是两者各自最小值？

![[00-知识库管理/_assets/plots/training-optimization/plot-critical-batch-tradeoff-v1.svg|900]]

> [!figure] 图 EXP-TRN-601-03　$B_{noise}=256$ 的经验 step–example tradeoff
> 蓝线为 $1+B_n/B$，琥珀线为 $1+B/B_n$，绿色点为 $B=B_n$。纵轴在 10 截断以保留交点可读性。来源：根据 [[S-2018-McCandlish-Noise-Scale]] 的经验模型由脚本绘制。

**怎样读图**：小 batch 端 sample efficient 但 step 多，大 batch 端 step 接近下限但 samples 昂贵；交点是对称折中。

**图没有证明什么**：曲线没有测量 hardware step time，不给真实任务最佳 batch，也不能推出 generalization。

## 七、结果文件与审计

| 文件 | 内容 |
|---|---|
| `results.json` | 全部配置、确定性结果和 Monte Carlo 统计 |
| `covariance_with_replacement.csv` | $B=1$ 到 64 的经验/理论 variance |
| `covariance_without_replacement.csv` | finite-population correction |
| `heavy_ball_scan.csv` | $\eta\lambda=0$ 到 4.2 的 roots class 与 radius |
| `critical_batch_tradeoff.csv` | $B=1$ 到 4096 的两类成本 |

> [!warning] 可复现边界
> Python `random` 在当前解释器上由固定 seed 控制；跨完全不同 Python 实现不承诺 bitwise RNG sequence。课程结论依赖的是带容差的统计量和精确解析检查，而不是某一行 CSV 的末位小数。

## 八、结论回链

- reduction：[[Mini-batch 梯度、平均求和与有效 Batch]]；
- accumulation/clipping：[[SGD、采样顺序与梯度累积的等价边界]]；
- convention：[[Momentum、EMA、偏差修正与框架约定]]；
- root map：[[二次模型的学习率—动量稳定域与阻尼]]；
- $1/B$ 与 SDE：[[梯度噪声协方差、Noise Scale 与 SDE 近似]]；
- critical batch：[[Critical Batch、隐式偏置与 SGD 证据地图]]。


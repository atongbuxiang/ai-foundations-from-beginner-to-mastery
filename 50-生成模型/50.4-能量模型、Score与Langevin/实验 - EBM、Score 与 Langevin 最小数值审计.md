---
type: experiment
status: verified
area: [generative-models, energy-based-models, score-matching, langevin]
prerequisites: ["[[能量模型、Score 与 Langevin MOC]]"]
related: ["[[50.4 分卷累计测验与复现门]]"]
code: "[[00-知识库管理/_labs/code/experiment_ebm_score_langevin_audit_v1.py]]"
created: 2026-08-25
updated: 2026-08-25
---
# 实验 - EBM、Score 与 Langevin 最小数值审计

> [!abstract] 实验目标
> 用不依赖深度学习框架的确定性脚本复算 GEN-25—32 的九个关键关节：energy gauge/temperature、正负相符号、Gaussian score matching、DSM 投影/Tweedie、多尺度双峰几何、ULA 偏差、MALA 校正、PC NFE 与非保守 score 反例。

## 一、运行

```bash
python3 00-知识库管理/_labs/code/experiment_ebm_score_langevin_audit_v1.py
```

固定随机种子 `50425`。依赖仅为 Python 标准库，不需要深度学习框架或第三方数值包。

## 二、每个 assertion 在审计什么

| 模块 | 复算对象 | 结论类型 | 不可外推 |
|---|---|---|---|
| GEN-25 | energy shift 后概率不变；降温改变 odds | 恒等式 | 不评价 neural EBM 质量 |
| GEN-26 | Bernoulli NLL 解析梯度 = 中心差分 | 符号校准 | 不证明短链负相无偏 |
| GEN-27 | Gaussian SM 最优 precision | population 可算例 | 不证明高维 trace 低方差 |
| GEN-28 | conditional/marginal MSE 常数差；Tweedie | Gaussian 恒等式 | 不覆盖非 Gaussian corruption |
| GEN-29 | 双峰中点 score 恒零但 valley/mode 随 $\sigma$ 变 | 反例 | 不给高维 mixing rate |
| GEN-30 ULA | 平稳方差 $1/(1-h/2)$ 与模拟一致 | 离散偏差 | 不代表所有非凸 target 有平稳律 |
| GEN-30 MALA | 标准正态均值/方差恢复且有拒绝 | MH 校准 | 不证明 iid/快速混合 |
| GEN-31 | PC NFE 与 SNR 步长代数 | 预算校准 | 不证明 heuristic 最优 |
| GEN-32 | 旋转场 curl 非零 | 不可积反例 | 不覆盖非单连通拓扑 |

## 三、关键预期输出

- Gauge residual 接近机器精度；$T=1$ 与 $T=.5$ 的 odds 为 2 与 4；
- Bernoulli analytic/numeric gradient 残差小于 $10^{-9}$；
- Gaussian SM 最优 $a=1/2.5=0.4$；
- DSM—marginal MSE 差恒为 $\tau^2/[\sigma^2(\tau^2+\sigma^2)]=1.6$；
- $\sigma=.5$ 时双峰中点是 valley，$\sigma=4$ 时变成 mode，但两者 score 都是 0；
- ULA 步长增大时方差从目标 1 系统上偏；
- MALA 在 $h=1$ 下恢复标准正态边缘，但 acceptance 明显小于 1；
- PC 示例总 NFE 为 150，不是 50；
- $s(x,y)=(-y,x)$ 的 curl 为 2，不能写成 $-\nabla E$。

本库基准运行还得到：ULA 在 $h=.1,.5,1$ 时解析平稳方差分别为 $1.052632,1.333333,2$，模拟值分别约为 $1.061562,1.334542,1.995835$；MALA 在 $h=1$ 时样本均值约 $0.00130$、方差约 $1.00080$、接受率约 $0.7843$。这些 Monte Carlo 数字允许随平台和随机实现小幅变化，解析值与 assertions 才是主验收对象。

## 四、必须独立完成的改写

1. 把 Gaussian target 改成方差 $\tau^2=3$，重新推 ULA 稳定区间与偏差；
2. 把 energy shift 改为 temperature sweep，画 entropy/odds 曲线；
3. 用 Monte Carlo 样本直接估 conditional/marginal 两个 MSE，验证常数差和 sampling error；
4. 将双峰权重改为 $.8/.2$，检查中点 score 不再为 0；
5. 扫描 MALA 步长，报告 acceptance 与 ESS-per-gradient；
6. 把旋转场加上保守分量 $(-x-y,-y+x)$，分别估 divergence 与 curl。

## 五、通过标准

- 原脚本全部 assertions 通过；
- 六项改写至少完成四项，其中 ULA 与 DSM 两项必做；
- 能说明每个 tolerance 是 floating-point/Monte Carlo engineering threshold 还是 theorem；
- 不把 Gaussian toy、边缘矩正确或单一 curl 检查升级为高维模型的一般保证。

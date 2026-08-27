---
type: experiment
status: verified
area: [generative-models, diffusion, numerical-audit]
prerequisites: ["[[DDPM、DDIM 与离散时间扩散 MOC]]"]
related: ["[[50.6 分卷累计测验与复现门]]"]
code: "[[00-知识库管理/_labs/code/experiment_ddpm_discrete_diffusion_audit_v1.py]]"
created: 2026-08-25
updated: 2026-08-25
---

# 实验 - DDPM、DDIM 与离散扩散最小数值审计

> [!abstract] 目的
> 用 Python 标准库把 GEN-41—48 的八个关键合同变成可执行断言：closed marginal、Gaussian posterior、参数化旋转、loss weighting、reverse variance、DDIM、probability kernel 与 implementation index。它验证低维公式和程序边界，不训练网络，也不代表图像生成质量。

## 一、运行方法

```bash
python3 -m py_compile "00-知识库管理/_labs/code/experiment_ddpm_discrete_diffusion_audit_v1.py"
python3 "00-知识库管理/_labs/code/experiment_ddpm_discrete_diffusion_audit_v1.py"
```

脚本不依赖 NumPy/PyTorch，随机试验固定 seed；成功运行必须以 `ALL ASSERTIONS PASSED` 结束。

## 二、断言—节点映射

| 节点 | 最小对象 | 主要可观察量 | 能抓住的错误 |
|---|---|---|---|
| GEN-41 | 三步 scalar Gaussian schedule | 累计乘积、Monte Carlo mean/variance | 单步/累计混淆、闭式边缘系数错 |
| GEN-42 | $t=2$ scalar posterior | $\tilde\beta_t$、两种 mean form gap | posterior 系数、noise form 符号错 |
| GEN-43 | $(x_0,\epsilon)\leftrightarrow(x_t,v)$ | 两个 round-trip residual | $v$ 号、$a_t/\sigma_t$ 交换 |
| GEN-44 | 两时刻共享 scalar、importance estimator | optimum 位移、corrected/uncorrected estimand | “正权重永不改有限模型”、漏 correction |
| GEN-45 | 二点 conditional law | conditional variance + mean error | 把不可约方差与均值误差混名 |
| GEN-46 | $\eta=0$ 跳步、相邻 $\eta=1$ | 对 $z$ 不变、方差与 $\tilde\beta_t$ 对齐 | deterministic 误读、skip variance 错 |
| GEN-47 | 两状态 kernel matrix | 两种 coupling 的同一输出 marginal | 合法 kernel 唯一/必然有信息的误解 |
| GEN-48 | dummy index 与 last-step mask | 0.72 vs 0.9、$(2,4)$ 输出 | off-by-one、$t=1$ 继续加噪 |

## 三、基准运行结果（2026-08-25）

```text
FORWARD alpha_bar_3=0.504000000000 mean_gap=-5.281e-04 variance_gap=5.468e-04
POSTERIOR beta_tilde=0.071428571429 mean_form_gap=-2.220e-16
PARAMETERIZATION x0_gap=0.000e+00 eps_gap=0.000e+00 single_pair_score_target=0.500000
LOSS shared_optimum=5.000->1.000 corrected=2.800 uncorrected=4.000 snr=(4.0, 0.25)
REVERSE_VARIANCE conditional=1.000000 mean_error=0.250000 optimal=1.250000
DDIM eta0_z_gap=0.000e+00 adjacent_variance_gap=0.000e+00
KERNEL correlated_out=(0.75, 0.25) independent_out=(0.75, 0.25) same_marginal=True
IMPLEMENTATION alpha_bar_t2=0.720 off_by_one=0.900 last_step_outputs=(2.0, 4.0)
ALL ASSERTIONS PASSED
```

Forward Monte Carlo 的末位依 Python/平台实现与样本波动变化；验收标准是代码内 tolerance，不是逐字符复制输出。

## 四、怎样解释结果

- `FORWARD` 同时验证 schedule 的确定性代数和有限样本 moment，不把 Monte Carlo 接近升级为闭式公式证明；
- `POSTERIOR` 的两种 mean form 对齐，是 posterior algebra 与 noise parameterization 的交叉检查；
- `PARAMETERIZATION` round-trip 为零不表示网络学得同样好，只说明目标换算实现一致；
- `LOSS` 明确展示正 weighting 在共享容量下改变 compromise，同时 importance correction 保持 estimand；
- `REVERSE_VARIANCE` 展示 NLL-optimal variance 会包含 mean error；
- `DDIM` 只验证给定输入的离散一步，不验证大跳步生成质量；
- `KERNEL` 用两个不同 coupling 产生同一 marginal，构成“一致性不唯一”的最小反例；
- `IMPLEMENTATION` 把最常见的 index 和 last-step bugs 变为数值差异。

## 五、必须亲自完成的改写

1. 把三步 schedule 改为更接近 1 的 $\beta_t$，比较直接累计与 log-domain 累计；
2. 故意把 posterior 的 $\bar\alpha_{t-1}$ 写成 $\bar\alpha_t$，确认 assertion 抓住错误；
3. 扫描 $\eta\in\{0,0.25,0.5,1\}$ 和多个 skip，列出新噪声系数、direction coefficient 与根号 margin；
4. 随机生成 100 个 finite-state kernels，保留 stochasticity 却破坏 consistency，输出最大 residual 与坏例；
5. 选做：加入 float32-style rounding，比较高 SNR 下 $1-\bar\alpha_t$ 的直接减法与稳定计算。

每项提交“解析预期—故意失败—assertion—修复后输出”；只提交成功截图不通过复现门。

## 六、实验没有证明什么

它不证明 U-Net/DiT 已学到数据 score，不给 ELBO/FID、coverage 或 scaling law，不测 mixed precision、GPU、EMA、CFG 和真实 sampler wall time，也不把 scalar/two-state identity 自动外推到高维非 Gaussian reverse conditional。

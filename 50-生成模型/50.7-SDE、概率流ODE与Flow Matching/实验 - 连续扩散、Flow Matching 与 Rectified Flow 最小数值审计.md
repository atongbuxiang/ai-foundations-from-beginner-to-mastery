---
type: experiment
status: verified
area: [generative-models, diffusion, flow-matching, numerical-audit]
prerequisites: ["[[SDE、概率流 ODE 与 Flow Matching MOC]]"]
related: ["[[50.7 分卷累计测验与复现门]]"]
code: "[[00-知识库管理/_labs/code/experiment_continuous_diffusion_flow_matching_audit_v1.py]]"
created: 2026-08-25
updated: 2026-08-25
---

# 实验 - 连续扩散、Flow Matching 与 Rectified Flow 最小数值审计

> [!abstract] 目的
> 用 Python 标准库把 GEN-49—56 的八个关键合同变成可执行断言：VP/VE/sub-VP 边缘、reverse-time 符号、PF ODE 同边缘异路径、conditional-score 投影、Flow Matching 弱矩、coupling 方差、Rectified Flow 有限步误差以及统一参数化。它验证低维公式和反例，不训练网络，也不代表真实生成质量。

## 一、运行方法

```bash
python3 -m py_compile "00-知识库管理/_labs/code/experiment_continuous_diffusion_flow_matching_audit_v1.py"
python3 "00-知识库管理/_labs/code/experiment_continuous_diffusion_flow_matching_audit_v1.py"
```

脚本只用 `math/random/statistics`，所有随机试验固定 seed；成功运行必须以 `ALL ASSERTIONS PASSED` 结束。

## 二、断言—节点映射

| 节点 | 最小对象 | 主要可观察量 | 能抓住的错误 |
|---|---|---|---|
| GEN-49 | 常数 $\beta$ 的 scalar VP/VE/sub-VP | $m,V$、方差 ODE、MC moments | 把 drift/noise/variance 公式混用 |
| GEN-50 | 平稳 OU 与 Brownian reverse drift | 两时钟 drift、实际 step gap | $t\downarrow$ 与 $\tau\uparrow$ 符号混搭 |
| GEN-51 | Brownian SDE 与解析 PF scaling | endpoint variance、quadratic variation | same marginals 误写为 same paths |
| GEN-52 | Gaussian data/corruption | 两 predictor 的 loss constant gap | 把 conditional/marginal loss 写成数值相等 |
| GEN-53 | stationary Gaussian interpolant | $\operatorname{Cov}(X,U)$、弱 $x^2$ residual | conditional target 在动就误判 density 在动 |
| GEN-54 | 两点 identity/swap coupling | target variance、平方配对成本 | endpoint marginals 与 coupling 混同 |
| GEN-55 | $\dot z=tz$ 与折线路径 | 1/2/4/8/32-step error、material acceleration | 确定 ODE/直线 teacher 推出 one-step exact |
| GEN-56 | angle/general path 与同密度 SDE | velocity gap、MSE metric 变化 | diffusion $v$ 与任意 instantaneous velocity 混名 |

## 三、基准运行结果（2026-08-25）

```text
GEN49 m=0.606531 vp_var=0.632121 subvp_var=0.399576 ve_var=1.000000 mc_mean_gap=1.981e-03 mc_var_gap=4.781e-03
GEN50 t_bracket=0.680000 tau_drift=-0.680000 actual_step_gap=0.000e+00 brownian_reverse=-0.173913
GEN51 sde_var=2.006801 ode_var=2.014535 brownian_qv=0.986439 ode_qv=1.733e-05
GEN52 analytic_gap=0.07111111 observed_gaps=(0.07120665,0.07176629) gap_difference=-5.596e-04
GEN53 marginal_var=0.992825 cov_XU=2.852e-04 weak_x2_residual=5.703e-04 conditional_U_var=1.194619
GEN54 identity_var=0.000000 swap_var=4.000000 same_order_cost=2.0 crossing_cost=20.0 batch_assignment=1.0<13.0
GEN55 exact=0.60653066 estimates=[0.0, 0.375, 0.49987793, 0.55477441, 0.59382641] errors=[0.60653066, 0.23153066, 0.10665273, 0.05175625, 0.01270425] length_ratio=1.400 material_accel=1.788000
GEN56 angle_v_gap=0.000e+00 general_v_gap=-1.175000 same_density_sde_drift=-1.600 diffusion=0.774597 mse_metric=1.0->5.0
ALL ASSERTIONS PASSED
```

Monte Carlo 末位依运行平台和 Python 随机实现波动；验收看代码 tolerance 与断言，不要求逐字符复制。

## 四、怎样解释结果

- `GEN49` 同时过解析方差 ODE 与样本 moments；MC 接近不是闭式公式的证明；
- `GEN50` 的两个 bracket 符号相反，但乘各自步长后位移相同；
- `GEN51` 的 endpoint variances 接近 2，而 quadratic variation 相差约五个数量级；
- `GEN52` 的两个 predictor 得到同一 analytic constant gap，sample loss 仍不同；
- `GEN53` 的 conditional velocity variance 大于 1，但 $E[2XU]\approx0$，所以边缘二阶矩不动；
- `GEN54` 只换 coupling，就把不可约 target variance 从 0 变成 4；
- `GEN55` 一步 Euler 得 0 而 exact 为 0.6065，细化步数后才收敛；
- `GEN56` 角度 schedule 的 diffusion $v$ 恰等于 path derivative，一般 schedule 明显不等；可逆 target scaling 也把 MSE metric 从 1 改成 5。

## 五、必须亲自完成的改写

1. 把常数 $\beta$ 改为线性/余弦 rate，数值积分 $B(t)$ 并验证 $m,V$ 的差分 ODE；
2. 故意把 reverse $t$-clock bracket 放进递增网格，确认 OU assertion 抓住 outward drift；
3. 对 PF ODE 用 100、1000、10000 个 partition 比较 smooth-path quadratic variation 的 $O(h)$ 衰减；
4. 把 Gaussian score projection 换成双峰 mixture，以数值 posterior 权重验证 conditional average；
5. 构造不同 coupling 的连续二维样本，报告 $C_\pi$、path length 与 finite-NFE endpoint error；
6. 为 $\dot z=tz$ 加 Heun/RK4，区分 solver order 与 flow straightness；
7. 随机生成合法 $(\alpha,\sigma)$ schedules，做 data/noise/score/velocity property tests。

每项提交“解析预期—故意失败—assertion—修复后输出”；只提交成功截图不通过复现门。

## 六、实验没有证明什么

它不证明 reverse-time theorem 的全部函数空间条件，不训练 score/velocity 网络，不验证 population OT 或 rectification theorem，不测 GPU、mixed precision、adaptive solvers 和真实 high-dimensional stiffness，也不给 likelihood、FID、coverage 或人类偏好。scalar/two-point 反例用于校准量词，不能替代实际模型的受控实验。

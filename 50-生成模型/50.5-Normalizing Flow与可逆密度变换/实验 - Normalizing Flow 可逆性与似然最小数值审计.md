---
type: experiment
status: verified
area: [generative-models, normalizing-flows, numerical-audit]
prerequisites: ["[[Normalizing Flow 与可逆密度变换 MOC]]"]
related: ["[[50.5 分卷累计测验与复现门]]"]
code: "[[00-知识库管理/_labs/code/experiment_normalizing_flow_audit_v1.py]]"
created: 2026-08-25
updated: 2026-08-25
---

# 实验 - Normalizing Flow 可逆性与似然最小数值审计

> [!abstract] 目的
> 用只依赖 Python 标准库的最小程序，把 GEN-33—40 的八个关键断言变成可执行单元测试。实验验证的是低维 identity、方向符号、round-trip 和近似误差；它不代表真实图像 flow 的训练性能。

## 一、运行方法

```bash
python3 -m py_compile "00-知识库管理/_labs/code/experiment_normalizing_flow_audit_v1.py"
python3 "00-知识库管理/_labs/code/experiment_normalizing_flow_audit_v1.py"
```

脚本固定随机种子，且不使用 NumPy、PyTorch 或网络。主输出应以 `ALL ASSERTIONS PASSED` 结束。

## 二、断言—实验映射

| 节点 | 最小对象 | 可观察量 | 断言性质 |
|---|---|---|---|
| GEN-33 | $X=3Z-2$ | 两方向 log-density gap | 解析恒等式 |
| GEN-34 | 二维 affine coupling | round-trip、numeric/analytic logdet | 解析 + finite difference |
| GEN-35 | diagonal channel mixing、squeeze | $HW$ logdet、维数、condition | 解析恒等式 |
| GEN-36 | 三维 unit triangular flow | 编码与串行 inverse | 计算图示例 |
| GEN-37 | 标量 residual map | inverse/series error 随阶数 | 数值收敛观察 |
| GEN-38 | 单 bin rational-quadratic | grid monotonicity、inverse residual | 有限网格 + 数值 inverse |
| GEN-39 | 线性 CNF、随机迹 | exact scale、density change、probe mean/SD | 解析 + Monte Carlo |
| GEN-40 | $p(y)=2y$、确定性 shrink | Jensen gap、部署方差变化 | 解析 + 有限样本 |

## 三、基准运行结果（2026-08-25）

```text
CHANGE_OF_VARIABLES log_p_x=-2.517550821872 direction_gap=0.000e+00
COUPLING roundtrip=0.000e+00 analytic_logdet=0.241747110847 numeric_gap≈1e-12
GLOW HW_logdet=0.000000000000 condition=4.0 squeeze_dims=3072->3072
AUTOREGRESSIVE x=(1.0, 3.0, 8.0) z=(1.0, 2.0, 4.0) sequential_inverse=(1.0, 3.0, 8.0)
RESIDUAL inverse_errors 随步数下降，series_errors 随阶数总体下降
SPLINE min_grid_increment>0，inverse_residual≈0
CNF scale=e，logp_change=-1，Hutchinson mean≈4，单 probe SD≈1
DEQUANT mass=1，uniform_bound=log2-1，deployment_variance_ratio=0.49
ALL ASSERTIONS PASSED
```

精确末位依平台数学库略有差异；判断依据是脚本中的 tolerance，而非复制这段文本。

## 四、怎样解释结果

- change-of-variables 两式数值相同，只说明方向合同一致；
- coupling finite difference 与解析 logdet 对齐，可抓常见符号/轴求和错误；
- residual inverse 与 series 是两条独立收敛曲线；
- Hutchinson sample mean 靠近 trace，但单 probe 有方差；
- spline 的有限 grid 单调不是全区间证明，正式保证仍来自正参数下的导数；
- deterministic denoise 改变方差，直观展示部署分布已不是 core distribution。

## 五、必须亲自改写的四项

1. 把 affine scale 从 3 改为 $1/3$，预测 logdet 符号后再运行；
2. 把 residual $a$ 改为 $0.9,0.99$，画步数—误差表；
3. 把 Hutchinson probes 从 1 扫到 1024，重复多 seed 画方差；
4. 把 spline 的端点导数推向 $10^{-4}$，比较 float64 monotonic margin 与 inverse residual；
5. 选做：实现 Euler 对 $\dot z=-2z$ 的 $h=0.5$ 反例，展示离散映射塌缩。

每次改写都记录“解析预期—数值结果—差异原因”；不能只贴终端截图。

## 六、实验没有证明什么

它不证明高维 neural flow 已训练成功，不测 CUDA 并行、图像 bpd、TARFlow latency 或真实 solver stiffness，也不把有限网格/Monte Carlo 观察升级为一般定理。

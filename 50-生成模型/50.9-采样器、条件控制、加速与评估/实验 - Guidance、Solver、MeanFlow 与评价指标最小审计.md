---
type: experiment
status: verified
area: [generative-models, guidance, inverse-problems, solvers, meanflow, evaluation]
related: ["[[条件生成、Bayes 分解与 Classifier Guidance]]", "[[Classifier-Free Guidance、尺度与质量多样性前沿]]", "[[逆问题、约束采样与 Plug-and-Play 控制]]", "[[扩散 SDE、ODE Solver、步长与 NFE 总账]]", "[[扩散蒸馏、一致性模型与 Shortcut]]", "[[平均速度、MeanFlow 与有限步生成]]", "[[Likelihood、FID、KID、Precision–Recall 与人类评估]]", "[[生成模型实验协议、FD Loss 与前沿证据地图]]"]
script: "[[00-知识库管理/_labs/code/experiment_guidance_solver_meanflow_evaluation_audit_v1.py]]"
created: 2026-08-25
updated: 2026-08-25
---

# 实验 - Guidance、Solver、MeanFlow 与评价指标最小审计

> [!abstract] 实验目标
> 不训练神经网络，只用 Python 标准库把 50.9 最容易写错的公式变成可执行断言：guidance scale 零点、inverse likelihood uncertainty、Euler/Heun、composition 反例、MeanFlow 全导数、FID/KID 与 FD gradient。它验证对象与算术，不验证论文级图像质量。

## 一、运行

```bash
python3 00-知识库管理/_labs/code/experiment_guidance_solver_meanflow_evaluation_audit_v1.py \
  --fd-step 1e-5
```

最后应出现：

```json
"all_assertions_passed": true
```

脚本已通过 `python3 -m py_compile`。

## 二、Guidance 与 CFG

对 $p(x)=N(0,1)$、$p(y\mid x)\propto\exp[-(x-2)^2/8]$：

| $w$ | tilted mean | tilted variance |
|---:|---:|---:|
| 1 | .4 | .8 |
| 3 | .8571428571 | .5714285714 |

scale 增大同时把均值推向条件中心并缩小方差。CFG 检查 $r_u=(1,2),r_c=(3,-1)$：

$$
w=0:(1,2),\quad .5:(2,.5),\quad1:(3,-1),\quad4:(9,-10).
$$

这核验本卷 convention 的零点/单位点和外推方向。

## 三、inverse problem 的 uncertainty correction

参数

$$
\tau_0=1,\ \alpha=.8,\ \sigma=.6,\ a=2,\ \sigma_y=.5,
\ x_t=.3,\ y=1.
$$

脚本得到

$$k=.8,\qquad c=.36,\qquad\operatorname{Var}(y\mid x_t)=1.69.$$

exact noisy-time likelihood score 为 $.49230769$，plug-in score 为 $3.328$，比例 $6.76$。这直接展示忽略 $a^2c$ 会显著放大高噪声 correction。

## 四、solver 与 finite map

对 $\dot x=x,x(0)=1,h=.5$：

| | 近似 | 绝对误差 |
|---|---:|---:|
| exact | 1.6487212707 | 0 |
| Euler | 1.5 | .1487212707 |
| Heun | 1.625 | .0237212707 |

对 teacher $T_h(x)=.9x+1$，两步 target 与 student $.81x+1.9$ 在 $x=2$ 都为 $3.52$。同时，常数 map 的 composition residual 为 0、相对目标端点 0 的误差却为 7：自洽不充分的反例被自动断言。

## 五、MeanFlow identity

对 $\dot z=z,z_0=1,t=1$：

$$v=e=2.7182818285,$$

$$u=e-1=1.7182818285,$$

端点速度算术平均为 $1.8591409142$，与 $u$ 不相等。中心差分得到 $D_tu\approx1.0000000000$，

$$|u-[v-(t-r)D_tu]|=1.77\times10^{-11}.$$

finite update 精确恢复 $z_r=1$。

## 六、评价指标与 FD gradient

- 一维真实 $(0,1)$、生成 $(2,4)$ 的 FID 为 5；
- linear-kernel unbiased MMD 对真实 $(0,2)$、生成 $(1,3)$ 为 $-1$，展示无偏 estimator 单次可为负；
- $\sigma_r^2=4,\sigma_g^2=9$ 的 covariance FD 梯度解析值 $1/3$；中心差分为 $.333333333291$，误差 $4.22\times10^{-11}$。

## 七、脚本证明了什么

- guidance/CFG scale convention 与 Gaussian tilt 算术一致；
- noisy-time likelihood 的 uncertainty term 不能无代价删除；
- oracle smooth ODE 上 Heun 单步误差小于 Euler；
- composition residual 为零不保证 endpoint 正确；
- MeanFlow identity 要使用沿轨迹的全导数；
- FID/KID 与一维 FD gradient 可独立复算。

## 八、脚本没有证明什么

- 不证明 classifier/CFG 的 neural predictions 精确；
- 不证明 DPS 是精确 posterior sampler；
- 不证明 Heun/DPM-Solver 在相同 NFE 的所有模型上更优；
- 不训练 Consistency/Shortcut/MeanFlow；
- 不验证 2026 FD Loss 的大规模流式训练结果；
- toy FID/KID 不替代图像 encoder、预处理、样本数与人评协议。

## 九、扩展实验

1. 加入 2D noncommuting covariance，比较对称夹心平方根与 naive product；
2. 在 analytic Gaussian diffusion 上比较 exact conditional sampler 与 CFG finite grid；
3. 扫 inverse noise misspecification，画 residual 与 coverage；
4. 对同一 learned toy field 画 solver error—NFE Pareto；
5. 为 finite-map 网络加入 on/off-trajectory composition test；
6. 模拟 EMA moments 的 staleness bias 与 exact replay FD gradient。

---
type: experiment
status: draft
area: [math/functional-analysis, math/kernel-methods, math/probability-metrics, ai/kernel-learning]
topic: "正定核、RKHS 与表示定理"
prerequisites: ["[[正定核、RKHS 与表示定理]]"]
related: ["[[推导与实验 MOC]]", "[[习题 - 正定核、RKHS 与表示定理]]", "[[解答 - 正定核、RKHS 与表示定理]]"]
code: "[[00-知识库管理/_labs/code/rkhs_kernel_audit.py]]"
figure: "[[00-知识库管理/_assets/plots/functional-analysis/plot-rkhs-krr-rff-v2.svg]]"
created: 2026-08-19
updated: 2026-08-23
---

# 实验 - Gram 正定性、KRR 表示与随机特征近似审计

> [!abstract] 研究问题
> 怎样把 GEO-07 的四个关键声明变成可失败的数值门：symmetric similarity 不自动 PSD；删去 sample-feature span 的 orthogonal component不改变训练点值却降低 norm；在 scaling 对齐后 KRR 与 GP posterior mean逐点相同；RFF error平均按约 $D^{-1/2}$ 下降，但单个随机 realization不必单调。本实验只验证这些有限设置中的机制，不用 finite computation替代 Moore–Aronszajn、Mercer 或泛化定理。

先看图判断：kernel PSD、representer projection、KRR–GP 均值等价和 RFF 的分布近似率，各自需要什么矩阵或概率证据？

![[00-知识库管理/_assets/plots/functional-analysis/plot-rkhs-krr-rff-v2.svg|880]]

> [!figure] 实验图｜Gram 正定、表示投影与随机特征近似
> A 比较 RBF Gram 与 symmetric negative squared-distance matrix 的谱；B 在 $80$ 维显式特征中投影到 sample row span，核对预测不变与 norm 下降；C 在 $\sigma^2=n\lambda$ 下叠加 GP posterior mean/KRR，并单列 GP latent variance；D 对 48 个独立 feature draws 报告 RFF Gram 相对误差的均值与 10–90% 区间。生成脚本：[[rkhs_kernel_audit.py]]；固定 root seed，并对谱、投影、scaling identity 与分布斜率设断言。

**怎样读图。** A 说明 symmetry 不推出 PSD；B 要同时验 sample predictions、Pythagoras 与 norm；C 的均值重合依赖 regularization/noise scaling，且不把 GP variance 归给 KRR；D 看跨 seed 的均值与区间，不要求单条随机特征路径单调。

**适用边界（图没有证明什么）。** 有限 Gram、有限显式特征与固定 RBF/RFF 设置不证明 Moore–Aronszajn、Mercer、核泛化界或任意随机特征实现；GP/KRR 身份也只对应已声明的 Gaussian likelihood 与 scaling。

> [!question] 本实验的判别问题
> 如何避免把“矩阵对称”“训练点预测不变”“KRR 与 GP 曲线重合”或“平均 RFF 误差下降”误读成更强的无限维或泛化结论？

## 1. 预注册假设与判断标准

### H1：Symmetry 与 PSD 必须分开

在 $24$ 个等距一维点上比较

$$
k_{RBF}(x,z)=\exp\left(-\frac{(x-z)^2}{2\ell^2}\right),
\quad \ell=0.42,
$$

与 $k_{bad}(x,z)=-|x-z|^2$。判断门：RBF minimum eigenvalue不低于 $-10^{-10}$；$K_{bad}$ 必须同时有低于 $-1$ 与高于 $1$ 的 eigenvalues。

### H2：Representer projection 的有限维影子

生成 $n=18$ 个样本的 $p=80$ dimensional RFF matrix $\Phi$，将任意 weight分解为

$$
w=w_{\parallel}+w_{\perp},
\qquad
w_{\parallel}\in\operatorname{row}(\Phi),
\quad w_{\perp}\perp\operatorname{row}(\Phi).
$$

判断门：

$$
\|\Phi w-\Phi w_{\parallel}\|_\infty<10^{-12},
\qquad
\|w_{\parallel}\|_2<\|w\|_2,
$$

且 Pythagoras residual低于 $10^{-10}$。这不是无限维 representer theorem 的证明，只是 projection proof 的数值实例。

### H3：KRR/GP 均值身份需对齐 scaling

对 $n=14$ 个 noisy nonlinear observations，KRR 使用

$$
\frac1n\|K\alpha-y\|^2+\lambda\alpha^\top K\alpha,
$$

GP noise variance为 $\sigma^2=0.18^2$，并设 $\lambda=\sigma^2/n$。判断门：360 个测试点的 maximum mean difference低于 $10^{-13}$；solve relative residual低于 $10^{-12}$。Posterior latent variance必须单独绘制，不能声称 KRR 自动产生该 uncertainty。

### H4：RFF 是分布趋势，不是逐 seed 单调定理

在固定 $72\times2$ points与 RBF $\ell=0.85$ 上，取

$$
D\in\{8,16,32,64,128,256,512,1024,2048\},
$$

每个 $D$ 用 48 个独立 draws。Metric是

$$
e_D=\frac{\|Z_DZ_D^\top-K\|_F}{\|K\|_F}.
$$

预注册：mean log–log slope在 $[-0.60,-0.40]$；至少 25% 的 seed paths在某次翻倍 $D$ 后 error上升，从而拒绝“每条路径严格单调”。

## 2. 环境与复现命令

| 项目 | 值 |
|---|---|
| 日期 | 2026-08-19 |
| OS | macOS 26.6.1 arm64 |
| Python | 3.12.13，Codex workspace bundled runtime |
| NumPy | 2.3.5 |
| Plot dependency | 无；脚本直接写 SVG |
| Root seed | `20260819`；各轨道/rep由固定 offset派生 |
| Hardware依赖 | Dense CPU `eigvalsh`/SVD/solve；无 GPU |
| 正式脚本 | `00-知识库管理/_labs/code/rkhs_kernel_audit.py` |

从 vault root 运行：

```bash
/Users/tong/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  "00-知识库管理/_labs/code/rkhs_kernel_audit.py"
```

渲染验收：

```bash
/Users/tong/.local/bin/svg-render \
  "00-知识库管理/_assets/plots/functional-analysis/plot-rkhs-krr-rff-v2.svg" \
  "/tmp/plot-rkhs-krr-rff-v1.png" 1200
```

## 3. 固定参数

| 轨道 | 参数 |
|---|---|
| Gram spectrum | 24 points in $[-1.5,1.5]$；RBF $\ell=0.42$ |
| Projection | $n=18,d=3,p=80$；RFF $\ell=0.9$；full SVD row basis |
| KRR/GP | $n=14$；RBF $\ell=0.72$；$\sigma=0.18$；360 test points |
| RFF | 72 fixed 2D points；$\ell=0.85$；9 dimensions；48 independent draws per $D$ |
| RFF normalization | $z_D(x)=\sqrt{2/D}\cos(\Omega x+b)$ |
| Error | Relative Gram Frobenius；不声称等于 spectral/downstream error |

## 4. Canonical 数值结果

| Metric | 结果 | 判定 |
|---|---:|---|
| RBF Gram minimum eigenvalue | `4.069676782081e-15` | PSD tolerance通过 |
| Invalid distance minimum eigenvalue | `-4.578425918118e+01` | 明确 negative direction |
| Invalid distance maximum eigenvalue | `3.913043478261e+01` | 确认 indefinite |
| Sample feature rank | `18 / 80` | 有 62-dimensional orthogonal complement |
| Projection max prediction gap | `2.942091015257e-15` | 机器精度级 |
| $\|w\|_2$ | `8.576300838545` | 基线 |
| $\|w_\parallel\|_2$ | `3.655984431277` | 严格下降 |
| $\|w_\perp\|_2$ | `7.758009661729` | 被 regularizer删除的方向 |
| Pythagoras residual | `7.105427357601e-15` | 通过 |
| KRR/GP max mean gap | `0.000000000000e+00` | 相同 solve矩阵下逐位相同 |
| $\sigma^2=n\lambda$ | `3.240000000000e-02` | scaling对齐 |
| KRR system condition number | `1.233439487126e+02` | 本设置可解但非单位条件 |
| Solve relative residual | `1.297672328647e-15` | 通过 |
| RFF mean log slope | `-0.501915835178` | 接近 $-1/2$ |
| Nonmonotone seed-path fraction | `0.479166666667` | 47.9%，拒绝逐路径单调 |
| Mean error, $D=8$ | `9.721520660748e-01` | 小 feature budget |
| Mean error, $D=2048$ | `6.037730528159e-02` | 下降但非零 |

正式 SVG SHA-256：

```text
cd35628d3df9ccc16308b0279d49d03a3ea751b0297724ca0c30d2807cc4f51e
```

## 5. 逐轨解释

### 5.1 轨道 A：一张坏矩阵足以否证，但一张好矩阵不足以证明全域

$K_{bad}$ 同时有大正、大负 eigenvalues，所以 symmetric similarity不满足 PSD quadratic-form contract。RBF Gram通过本样本的 numerical PSD check，并与 Bochner/closure theorem 的全域证明一致；但实验本身仍只是一组 finite check，不能替代普遍定理。

### 5.2 轨道 B：训练数据看不到 orthogonal component

$\Phi w_\perp\approx0$，所以删去它不改训练 predictions。Full norm平方由 parallel/perpendicular两部分相加；strictly increasing norm penalty会拒绝非零 $w_\perp$。Finite feature projection使表示定理的 proof mechanism可见，但 RKHS 版本还需 bounded evaluation与 Hilbert projection。

### 5.3 轨道 C：相同 posterior mean不等于相同统计对象

因为系统矩阵严格相同，mean gap exact到浮点零。蓝色 band来自 GP conditional covariance；它依赖 prior covariance和noise model。把同一 band贴给 KRR而不声明 probabilistic assumptions属于越界解释。

### 5.4 轨道 D：平均斜率与单路径波动可以同时为真

48-rep mean slope为 $-0.502$，符合 Monte Carlo $D^{-1/2}$ 量级；同时 47.9% 的独立 dimension paths至少发生一次 error上升。后者不是 RFF失效，而是“期望/高概率收敛”不等于“每个 seed、每个 $D$ 单调”。

## 6. 结论边界

本实验支持：

1. 本样本上合法/非法 Gram 的谱差异；
2. Finite feature row-space projection 的 prediction/norm机制；
3. 指定 scaling下 KRR/GP mean identity；
4. 本 domain/metric上的 RFF Monte Carlo rate与 seed variability。

本实验不支持：

- 由 finite eigenvalue check证明 kernel全域 PSD、strict PD或characteristic；
- 由 finite projection例子证明 infinite RKHS completeness；
- GP posterior interval具有无条件 frequentist coverage；
- RFF Gram Frobenius error直接给 test-risk或attention-output error；
- $D^{-1/2}$ 常数或 monotonicity对任意 kernel/domain成立；
- Kernel approximation越精确就一定带来更好 AI task performance。

## 7. 改参任务

- [ ] 把 RBF bandwidth改成 `0.15, 0.42, 1.5, 10`，比较 rank与 condition。
- [ ] 把 projection feature dimension改成 `12, 18, 40, 160`，观察 sample row-space维数和 orthogonal norm。
- [ ] 固定 $\sigma^2$ 却错误使用 $\lambda=\sigma^2$，量化 KRR/GP mean gap并解释 scaling bug。
- [ ] 把 KRR $\lambda$ 扫描 $10^{-6}$ 到 $1$，报告 smoother degrees of freedom与 conditioning。
- [ ] 对 RFF 增加 max-entry 与 spectral-norm proxy；比较三种 error metric的 slope/variance。
- [ ] 用同一 nested feature pool构造 path，并与当前 independent-$D$ draws比较；两者都不得被叫作必然单调。
- [ ] 把 kernel Gram error接入一个 held-out regression task，检查 kernel error与 risk是否同序。

## 8. 状态

- 代码：`composed`
- Canonical run：`composed`
- SVG XML/PNG render：`composed`
- 参数干预：`not-attempted`
- 学习者独立解释：`not-attempted`
- 因此本实验与主节点均保持 `draft`，不能升级为 `verified`。

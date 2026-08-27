---
type: experiment
status: draft
area: [math/information-theory, math/statistics, ai/generative-models]
question: "ELBO 的证据恒等式如何数值闭合，restricted variational family 与 shared amortized encoder 又分别留下什么 gap？"
hypothesis: "unrestricted Bernoulli q 在 model posterior 处达到 log evidence；若 posterior 不在 variational family 内会留下 approximation gap；若 encoder 不能依 x 改变 q，会留下 amortization gap。"
code: "[[plot_elbo_gap.py]]"
figure: "[[00-知识库管理/_assets/plots/information-theory/plot-elbo-gap-v2.svg]]"
figure_sha256: "d30dc78ab03b6919f276188619a125b45be6ccc284825b724e872f1b54d174dd"
data: "完全合成的二元 latent-variable model"
seed: "deterministic enumeration; no random seed"
related: ["[[变分推断、ELBO 与证据分解]]", "[[交叉熵与 KL 散度]]", "[[Bayesian 推断与后验预测]]"]
created: 2026-08-19
updated: 2026-08-23
---

# 实验 - ELBO 恒等式、变分族限制与摊销缺口

> [!abstract] 实验定位
> 这是一个可以枚举到底的教学实验，不用 neural network 或随机 optimizer 掩盖对象。它验证 evidence identity，并把“family 表示不了 posterior”和“shared inference mapping 没有使用 observation”造成的两类 gap 分开。

## 一、模型

latent prior：

$$
P(Z=1)=0.3.
$$

binary likelihood：

$$
P(X=1\mid Z=1)=0.9,
\qquad
P(X=1\mid Z=0)=0.2.
$$

因此

$$
P(X=1)=0.3(0.9)+0.7(0.2)=0.41,
$$

$$
P(Z=1\mid X=1)=\frac{0.27}{0.41}\approx0.6585366.
$$

取 variational distribution

$$
q_\phi(Z=1)=\phi.
$$

脚本对 $\phi\in(0,1)$ 网格直接计算 ELBO 与 posterior KL，不使用 Monte Carlo。

## 二、三项预注册检查

### A. identity

对所有 grid points 验证

$$
\log p(x)-\mathcal L(\phi;x)
=D_{\rm KL}(\operatorname{Ber}(\phi)
\|\operatorname{Ber}(p(z=1\mid x))).
$$

预期 maximum residual 接近 floating-point rounding，并在 $\phi=p(z=1\mid x)$ 处 gap 为零。

### B. restricted family

人为限制

$$
\phi\in[0.8,1).
$$

真实 posterior parameter $0.6585$ 不在 family 内，故最好点落在 boundary $\phi=0.8$，仍保留 positive approximation gap。

### C. amortization

令 encoder 完全看不到 $x$，对 $x=0,1$ 必须输出同一个 $\phi$。单样本 posterior 分别约为

$$
P(Z=1\mid X=0)=0.0508475,
$$

$$
P(Z=1\mid X=1)=0.6585366.
$$

即使 shared $\phi$ 已精确优化，也不可能同时等于两者，因此留下 amortization/representation gap。

## 三、结果

先用图回答实验问题：**unrestricted、restricted 与 shared-amortized 三种 $q$ 约束下，ELBO gap 在哪里闭合或残留？**

![[00-知识库管理/_assets/plots/information-theory/plot-elbo-gap-v2.svg|880]]

> [!figure] 实验图 INFO-LAB-01｜ELBO identity 与两类不可约 gap
> A 枚举全部 Bernoulli $q$ 并验证在 analytic posterior 处 ELBO 等于 log evidence；B 将 family 限制为 $q\ge0.8$，显示最优边界点仍有 positive approximation gap；C 让 $x=0,1$ 共用同一个 encoder 输出，显示逐例 posterior targets 与 shared optimum 不同。来源：完全合成二元 latent model；生成脚本：[[plot_elbo_gap.py]]；deterministic enumeration，无随机种子。

**怎样读图。** A 读蓝色曲线到绿色 evidence 线的竖直差；B 只在允许 family 内优化并读取红色 gap；C 比较两个 analytic posterior 点与 shared $q$，再用表格核对数值。

**适用边界（图没有证明什么）。** 该实验只验证一个可枚举 Bernoulli model；它不证明 neural VAE 的全部 gap 可由这两个数表示，不证明 train ELBO 足以评价模型，也不把 shared mapping 的限制归因于某个唯一网络超参数。

| 检查 | 结果 |
|---|---:|
| $x=1$ posterior | 0.65853659 |
| unrestricted identity maximum residual | $3.89\times10^{-16}$ |
| restricted-family best $\phi$ | 0.8 |
| restricted approximation gap | 0.04868868 nats |
| best shared $\phi$ | 0.24324324 |
| average shared/amortization gap | 0.28463684 nats |

图 A 的蓝线在 exact posterior 处碰到 green log-evidence line；图 B 即使完成 optimization 也碰不到 evidence；图 C 表明 shared inference mapping 的输入/容量限制与 variational family restriction 是不同原因。

## 四、可以推出与不能推出

可以推出：

- 对此精确枚举 model，ELBO identity 数值闭合；
- restricted family 与 shared mapping 可分别造成 positive gap；
- “optimizer 收敛”不等于“posterior approximation exact”。

不能推出：

- neural VAE 的全部 gap 都可由本二元例子量化；
- reverse KL 在所有 family 中都选择同一类 mode；
- train ELBO 高就意味着 model 对真实数据正确；
- amortization gap 只由 network width 决定。

## 五、复现

代码：[plot_elbo_gap.py](</Users/tong/Nodes/basic/00-知识库管理/_labs/code/plot_elbo_gap.py>)。

从仓库根目录执行：

```bash
python3 00-知识库管理/_labs/code/plot_elbo_gap.py
xmllint --noout 00-知识库管理/_assets/plots/information-theory/plot-elbo-gap-v2.svg
```

验收要求：

1. identity residual 小于 $10^{-12}$；
2. unrestricted optimum 与 analytic posterior 一致；
3. restricted optimum 位于 $0.8$ boundary；
4. 修改 encoder 可见信息后，重新解释 shared gap，而不是只看曲线变小。

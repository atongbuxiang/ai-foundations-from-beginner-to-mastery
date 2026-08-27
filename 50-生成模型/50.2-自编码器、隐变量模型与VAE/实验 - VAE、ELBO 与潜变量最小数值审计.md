---
type: experiment
status: verified
area: [generative-models, vae, reproducibility]
prerequisites: ["[[自编码器、隐变量模型与 VAE MOC]]"]
related: ["[[50.2 分卷累计测验与复现门]]"]
code: "[[00-知识库管理/_labs/code/experiment_vae_elbo_latent_audit_v1.py]]"
created: 2026-08-25
updated: 2026-08-25
---

# 实验 - VAE、ELBO 与潜变量最小数值审计

> [!abstract] 实验目标
> 不训练神经网络，而在 exact 可枚举或有解析答案的最小世界中核对六件事：ELBO identity、Gaussian KL、重参数化矩、IWAE 紧致性、rate decomposition 与 posterior collapse。脚本的每个随机结果都有解析靶值和失败断言。

## 一、运行

    python3 00-知识库管理/_labs/code/experiment_vae_elbo_latent_audit_v1.py

依赖仅为 Python 标准库。固定 seed 为 20260825；输出为 JSON，便于 diff 和保存。

## 二、六个审计块

| 块 | exact/解析靶值 | 必须观察 |
|---|---|---|
| exact ELBO | $\log p(x)=\mathcal L+KL(q\|posterior)$ | residual 近机器精度 |
| Gaussian KL | 闭式 = $E_q[\log q-\log p]$ | 非负、两算法相等 |
| reparameterization | $EZ=\mu,VarZ=\sigma^2$ 与 $(2\mu,2\sigma)$ | Monte Carlo 在容差内 |
| IWAE | $E\widehat p_K=p(x)$，$\mathcal L_1<\mathcal L_5<\mathcal L_{50}<\log p(x)$ | density 无偏而 log 向下 |
| rate decomposition | $R=I+KL(q(z)\|p(z))$ | residual 近机器精度 |
| collapse | decoder 与 $z$ 独立、$q=p$ | rate 0 且 ELBO=evidence |

## 三、为什么选择有限离散模型

神经网络训练失败可能来自 optimizer、初始化、数据和软件。有限 $X,Z$ 可枚举所有 joint、posterior 和 evidence，从而把概率恒等式与工程噪声分开。只有先通过这个层级，才有资格把大型训练曲线解释为模型现象。

## 四、结果解释合同

- IWAE 的单次 log estimate 不必单调；脚本比较 80,000 次重复的 expectation estimate；
- density mean 接近 exact evidence 是 Monte Carlo 检查，不声称任意有限样本精确等于靶值；
- 重参数化容差是本 seed/sample count 的工程门，不是概率定理；
- collapse 构造证明“存在不使用 latent 的 exact optimum”，不声称所有数据/decoder 都会 collapse；
- positive-rate zero-information 反例使用对所有 $x$ 相同的 $q(z\mid x)$，直接隔离 aggregate mismatch。

## 五、独立改写任务

通过不能只运行原脚本。需在不查看实现的情况下：

1. 换一组三状态 latent 与非均匀 proposal，复算 exact posterior/ELBO；
2. 换 Gaussian 维数、均值和方差，并加入 Monte Carlo density-ratio 检查；
3. 将 IWAE 重复次数减小，展示单次/小样本非单调；
4. 构造 rate 相同但 MI 不同的两套 encoder；
5. 构造 decoder 轻微依赖 $z$ 的 near-collapse，画 $D$ 与 $R$ 变化；
6. 保存 Python 版本、seed、参数、容差和失败断言。

## 六、失败意味着什么

- identity residual 大：公式、归一化或 log/概率域实现错；
- density mean 偏离：proposal sampling/weight 或重复数有问题；
- IWAE expectation 不按序：样本不足、seed 异常或实现错，先增加重复并给置信区间；
- rate residual 大：aggregate posterior 加权或 KL 方向错；
- collapse 不等于 evidence：decoder 仍依赖 $z$ 或 $q\ne p$。


---
type: experiment
status: verified
area: [generative-models, gan, reproducibility]
code: "[[00-知识库管理/_labs/code/experiment_gan_objectives_dynamics_audit_v1.py]]"
related: ["[[50.3 分卷累计测验与复现门]]"]
created: 2026-08-25
updated: 2026-08-25
---
# 实验 - GAN 目标、Wasserstein 与博弈动力学最小数值审计

> [!abstract] 实验目标
> 在无需训练神经网络的精确世界中核对六项：最优判别器—JS identity、两种 generator logit gradient、点质量 topology、有限点 GP 非全域证书、bilinear GDA 谱半径与 mode quality/coverage 分账。

## 一、运行

    python3 00-知识库管理/_labs/code/experiment_gan_objectives_dynamics_audit_v1.py

仅依赖 Python 标准库，输出 JSON，所有结论有 assertion。

## 二、审计表

| 块 | 必须命中 |
|---|---|
| $D^*$ / JS | value residual 近机器精度 |
| generator gradient | $D=.01$ 时 non-sat 系数远大于 sat |
| point masses | $\theta\ne0$ 时 JS=$\log2$，$W_1=|\theta|$ |
| sampled GP | $f'(0)=f'(1)=1$ 但 $f'(.25)>10$ |
| bilinear GDA | eigen modulus $\sqrt{1+\eta^2}>1$ |
| modes | precision 可 1 而 mode recall=.25 |

## 三、独立改写门

1. 换三点离散分布复算 $D^*$ 与 JS；
2. 画 $D\in[.001,.999]$ 两种梯度系数；
3. 换二维点质量和不同 ground norm；
4. 自构另一条 finite-sample GP 反例；
5. 实现 100 步 GDA 与 extragradient 轨迹；
6. 为非均匀 modes 报 precision、recall、TV 与 entropy。

保存参数、步长、dtype、误差容差和失败断言；只运行原脚本不通过。

## 四、解释边界

这个实验验证数学责任，不比较真实图像 GAN。point-mass 只证明 topology；bilinear 只给最小动态反例；GP 反例只否定“有限点检查就是全域证书”；mode count 只说明 quality 与 coverage 可分离。


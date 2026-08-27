---
type: source
status: verified
area: [sources, generative-models, invertible-networks]
source_type: blog
title: "细水长 flow 之可逆 ResNet：极致的暴力美学"
author: 苏剑林
year: 2019
url: "https://spaces.ac.cn/archives/6482"
accessed: 2026-08-25
source_tier: C
license: "科学空间站点许可；本库仅保存独立摘要、必要公式与链接"
scope_role: core
temporal_role: classical-exposition
related: ["[[Residual Flow、可逆 ResNet 与 Logdet 估计]]", "[[残差缩放、Lipschitz 界与深度稳定性]]"]
created: 2026-08-25
updated: 2026-08-25
---
# 细水长 flow 之可逆 ResNet

> [!abstract] 来源定位
> 文章以 $F(x)=x+g(x)$、$\operatorname{Lip}(g)<1$ 进入 Banach fixed point inverse 与 logdet trace series，是 GEN-37 的中文推导入口。课程把“可逆性证书”“逆迭代收敛”和“截断/随机 logdet estimator”三件事分开。

## 核心骨架

若 $y=x+g(x)$，逆解满足 $x=y-g(x)$。迭代 $x_{k+1}=y-g(x_k)$ 在 $\operatorname{Lip}(g)<1$ 时收敛。Jacobian

$$J_F=I+J_g,$$

当谱半径小于 1 时

$$\log\det(I+J_g)=\sum_{k\ge1}\frac{(-1)^{k+1}}k\operatorname{tr}(J_g^k).$$

有限截断、Hutchinson probe 和 Lipschitz upper bound 都会引入各自误差。一级来源：[[S-2019-Behrmann-iResNet]]。

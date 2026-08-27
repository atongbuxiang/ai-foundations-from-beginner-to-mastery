---
type: solution
status: verified
area: [training, optimization, curvature]
topic: "[[Hessian-vector Product、共轭梯度与隐式二阶步]]"
exercise: "[[习题 - Hessian-vector Product、共轭梯度与隐式二阶步]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Hessian-vector Product、共轭梯度与隐式二阶步

> [!warning] 使用边界
> “Matrix-free”不是“cost-free”。一次隐式步的证书必须同时包含算子是否固定、HVP 次数、residual、conditioning 与通信成本。

## A. 识别与复述

### TRN19-A01
$\operatorname{HVP}(v)=\nabla^2L(\theta)v$。自动微分先形成 gradient 的计算图，再对方向做 JVP，或把 $\nabla L^\top v$ 标量化后反传，因此只需算子作用而不存整个 Hessian。“精确”指遵循 AD 链式法则，不表示没有浮点舍入、混合精度误差、随机状态差异或实现 bug。

### TRN19-A02
Forward-over-reverse 常写成 `jvp(grad(L), v)`，方向维小且框架支持 forward AD 时直接；reverse-over-reverse 通用但需高阶反传图，内存与算子支持可能更差。Gradient finite difference 只适合独立诊断，会同时受截断与消减误差影响，不能替代生产 HVP。

### TRN19-A03
Classical CG 要求固定、对称正定的线性算子。第 $k$ 步解位于 $p_0+\mathcal K_k(A,r_0)$，其中 $\mathcal K_k=\operatorname{span}(r_0,Ar_0,\ldots,A^{k-1}r_0)$。Residual 达标、检测到 negative curvature、撞到 trust-region boundary 是不同退出语义，后两者不是“SPD 系统已收敛”。

## B. 手算与构造

### TRN19-B01
$H=\begin{bmatrix}2&1\\1&4\end{bmatrix}$，故 $Hv=(1,-3)^\top$。$u^\top Hv=2-3=-1$；$Hu=(5,6)^\top$，$v^\top Hu=5-6=-1$，满足对称 Hessian 的双线性一致性。

### TRN19-B02
$r_0=d_0=(1,1)$，$\alpha_0=2/5$，所以 $p_1=(2/5,2/5)$、$r_1=(3/5,-3/5)$。$\beta_0=9/25$，$d_1=(24/25,-6/25)$，$\alpha_1=5/8$。于是 $p_2=(1,1/4)=A^{-1}b$、$r_2=0$；二维精确算术至多两步结束。

### TRN19-B03
对 $r=(0,10^{-3})$，$e=A^{-1}r=(0,10^{-5})$，$\|e\|=10^{-5}$；对 $r=(10^{-3},0)$，$e=(10^{-3},0)$，$\|e\|=10^{-3}$。Residual 范数同为 $10^{-3}$，但低 eigenvalue 方向把同样 residual 变成更大 solution error。

## C. 推导与证明

### TRN19-C01
链式求导给 $\phi'(0)=\left.\partial_\epsilon\nabla L(\theta+\epsilon v)\right|_0=Hv$。若 $v$ 在求导时视为常量，则
$$\nabla_\theta[\nabla_\theta L(\theta)^\top v]=H^\top v=Hv,$$
最后一步使用标量二阶导的对称性。

### TRN19-C02
若 $Ap=b$、近似解 $\hat p$ 的 residual 定义为 $r=b-A\hat p$，则 $A(p-\hat p)=r$，即 $e=A^{-1}r$。SPD 下 $\|A^{-1}\|_2=1/\lambda_{\min}$，所以 $\|e\|_2\le\|r\|_2/\lambda_{\min}$。相对 residual 没有消掉小 eigenvalue，病态系统仍可能有大误差。

### TRN19-C03
令 $p=M^{-1/2}z$ 代入 $Ap=b$，左乘 $M^{-1/2}$，得到 $M^{-1/2}AM^{-1/2}z=M^{-1/2}b$。好的 $M$ 要让预条件矩阵的 eigenvalues 聚集、condition number 降低，同时 apply 成本可承受；仅让原坐标 diagonal 接近并不能保证整体谱改善。

## D. 边界、反例与纠错

### TRN19-D01
同一 $\theta,v$ 下，不同 dropout mask 给不同 loss Hessian $H_{\omega_k}$，于是第 $k$ 次所谓 $Ad_k$ 实际来自不同算子。先前构造的 $A$-共轭关系和 Krylov 子空间失去共同 $A$，记录的 $r_k$ 也不再等于某个固定线性系统的 residual。必须冻结 mask/RNG 或改用有相应理论的随机线性求解器。

### TRN19-D02
中心或前向差分的截断误差随步长约为 $O(h^2)$ 或 $O(h)$，太大时离开局部线性区；梯度相减的浮点误差约按 $O(\varepsilon_{mach}/h)$ 放大，太小时发生 catastrophic cancellation。因此误差常呈 U 形，应跨对数步长扫描并与 AD HVP 比较。

### TRN19-D03
取 $B=\operatorname{diag}(1,-1)$、$d=(0,1)$，则 $d^\top Bd=-1$。Classical CG 中用于步长的正曲率分母与能量范数最小化都失效。Steihaug CG 应标记 negative curvature，沿该方向走到 trust-region boundary，并返回受约束候选而非宣称线性系统收敛。

## E. AI 迁移

### TRN19-E01
合同至少固定 `parameter_checkpoint`、batch IDs/order、RNG states、dropout/BN mode、mutable buffers、dtype/autocast、loss reduction、正则项、gradient accumulation 与 distributed all-reduce 规则。每次调用还记录输入向量 norm、输出 norm、device 与图版本。

### TRN19-E02
一，对 quadratic $L=\tfrac12\theta^\top A\theta$ 断言 HVP 与 $Av$ 在舍入容差内相等；二，随机 $u,v$ 断言 $|u^THv-v^THu|$ 相对尺度足够小；三，扫描 $h$，断言至少存在中间区间使 gradient difference 与 HVP 的相对误差低于阈值，并保留 U 形数据。容差按 dtype、norm scale 与 conditioning 分层设置。

### TRN19-E03
还需报告实际 HVP 调用（包括重试/line search）、每次 HVP 时延、预条件器构建与 apply、global reductions、峰值内存、最终 relative residual、predicted decrease、退出原因、接受率和端到端 wall-clock。否则“10 次迭代”无法比较每次算子成本或结果质量。

## 无提示重做

- [ ] 48 小时后手算二维 CG 全轨迹。
- [ ] 一周后写出一个会破坏固定算子合同的训练细节，并给出检测断言。

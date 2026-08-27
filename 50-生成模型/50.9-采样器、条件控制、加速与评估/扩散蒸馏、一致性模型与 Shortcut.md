---
type: derivation
status: verified
area: [generative-models, diffusion, distillation, consistency-models, shortcut]
node_id: GEN-69
prerequisites: ["[[扩散 SDE、ODE Solver、步长与 NFE 总账]]", "[[DDPM、DDIM 与离散时间扩散 MOC]]", "[[SDE、概率流 ODE 与 Flow Matching MOC]]"]
related: ["[[平均速度、MeanFlow 与有限步生成]]", "[[生成模型实验协议、FD Loss 与前沿证据地图]]"]
sources: ["[[S-2022-Salimans-Ho-Progressive-Distillation]]", "[[S-2023-Song-Consistency-Models]]", "[[S-2024-Frans-Shortcut-Models]]", "[[S-2024-Su-10085-SiD上]]", "[[S-2024-Su-10567-SiD下]]", "[[S-2024-Su-10617-Shortcut步长条件]]", "[[S-2024-Su-10633-一致性模型]]"]
exercises: ["[[习题 - 扩散蒸馏、一致性模型与 Shortcut]]"]
solutions: ["[[解答 - 扩散蒸馏、一致性模型与 Shortcut]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-distillation-consistency-shortcut-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 扩散蒸馏、一致性模型与 Shortcut

> [!abstract] 一句话结论
> 少步生成至少有三种不同监督对象：蒸馏让 student 模仿 teacher 的有限步结果；consistency model 让同一轨迹上的各点映到共同端点；Shortcut 把步长输入模型，并约束“一次大步 = 两次小步”。它们都可做到 1-NFE，但 loss、teacher 依赖、可变步数能力与失败模式不同。

## 一、为什么换高阶 solver 还不够

假设模型学习的是 instantaneous field $v_\theta(x,t)$。一步 Euler

$$x_{t-h}\approx x_t-hv_\theta(x_t,t)$$

只用局部切线代替弯曲轨迹。若希望一步跨越整个区间，即使 $v_\theta$ 完全正确，Euler 也可能有巨大 discretization error。

低步数方法因此改变问题：不再只问“怎样更准地积分局部场”，而是直接学习一个有限区间对象。

## 二、先统一三个 map

- 精确/高精度 flow map：$\Phi_{t\to r}(x_t)$；
- teacher numerical map：$T_{t\to r}(x_t)$；
- student learned map：$F_\theta(x_t,t,r)$。

即使 teacher NFE 很大，也通常只有

$$T_{t\to r}\approx\Phi_{t\to r},$$

所以 student 拟合 $T$ 不自动等于真实 data transport。teacher bias 会被继承。

## 三、Progressive Distillation：两步老师变一步学生

设 teacher 的一个小步 map 为 $T_h$。从 $x_t$ 出发做两步：

$$
x_{t-h}^{(T)}=T_h(x_t,t),
$$

$$
x_{t-2h}^{(T)}=T_h(x_{t-h}^{(T)},t-h).
$$

student 训练一个 $2h$ 步：

$$
F_\theta(x_t,t,2h)\approx
\operatorname{sg}\left[x_{t-2h}^{(T)}\right],
$$

其中 $\operatorname{sg}$ 表示 target 不反传到 teacher。训练后把 student 复制/升级为下一轮 teacher，再把步数减半：

$$N\to N/2\to N/4\to\cdots.$$

[[S-2022-Salimans-Ho-Progressive-Distillation]] 还强调少步稳定参数化。$x_0/\epsilon/v$ 虽可代数换算，低 SNR 端点的条件数、loss weighting 与网络 preconditioning 仍不同。

### 3.1 误差传播

若每轮 student 对当前 teacher map 的误差为 $\delta_k$，最终误差不是简单“最后一轮 $\delta$”；早期 teacher approximation、每轮 optimization error 和新轨迹分布 shift 会复合。应在每个 stage 报 teacher/student 配对误差与终点样本指标。

## 四、SiD：不生成完整 teacher trajectory 的蒸馏

[[S-2024-Su-10085-SiD上]]、[[S-2024-Su-10567-SiD下]] 讨论 Score identity Distillation。核心 conditional-expectation identity 是：若

$$
\epsilon^*(x_t,t)=\mathbb E[\epsilon\mid x_t,t],
$$

则对只依赖 $(x_t,t)$ 的 $f$，

$$
\mathbb E\langle f(x_t,t),\epsilon^*(x_t,t)\rangle
=\mathbb E\langle f(x_t,t),\epsilon\rangle.
$$

这允许通过教师/学生分布诱导的 denoiser 差异构造 generator gradient，而不先让 teacher 多步生成大批配对终点。

但三种“相等”必须分开：

1. population loss value 的恒等变换；
2. 对理想最优辅助模型的 generator gradient；
3. 实际交替优化、stop-gradient 和有限容量网络的程序梯度。

任意 $f$ 若偷偷依赖独立 $x_0$ 或 $\epsilon$，tower property 替换就可能失效。

## 五、Consistency Model：同轨迹同终点

给定从 noise 到 data 的 probability-flow ODE trajectory $x(t)$，选一个很小的端点 $\epsilon$。consistency function 的理想条件是

$$
f(x(t),t)=x(\epsilon)
$$

对同一条 trajectory 的所有 $t$ 成立。于是

$$
f(x(t),t)=f(x(r),r),\qquad r<t.
$$

还需 boundary condition

$$f(x,\epsilon)=x.$$

实际训练用相邻时间对：teacher solver 从 $x_{t_{n+1}}$ 得到估计 $\hat x_{t_n}$，再最小化

$$
d\left(
f_\theta(x_{t_{n+1}},t_{n+1}),
\operatorname{sg}f_{\bar\theta}(\hat x_{t_n},t_n)
\right),
$$

$\bar\theta$ 常为 EMA/target network。[[S-2023-Song-Consistency-Models]] 同时讨论 consistency distillation 与无需预训练 teacher 的 consistency training；二者不能只因网络输出相同而合并。

### 5.1 一步与多步

一步直接 $x_T\mapsto f(x_T,T)$。多步通常在中间重新加适量噪声/跳到另一时间再调用 $f$，以改善质量或编辑能力。多步算法不是简单重复同一个 deterministic endpoint map，必须写清 noise injection 与 schedule。

## 六、Shortcut：把步长变成条件

Shortcut model 学习

$$v_\theta(x,t,h),$$

并用 finite update

$$F_{t,h}^\theta(x)=x+h v_\theta(x,t,h).$$

小步边界 $h\to0$ 用 flow-matching instantaneous velocity 监督。有限步用 composition consistency：

$$
F_{t,2h}^\theta(x)
\approx
F_{t+h,h}^{\bar\theta}\left(F_{t,h}^{\bar\theta}(x)\right).
$$

展开即

$$
v_\theta(x,t,2h)
\approx\frac12\left[
v_{\bar\theta}(x,t,h)
+v_{\bar\theta}(x+h v_{\bar\theta}(x,t,h),t+h,h)
\right].
$$

[[S-2024-Su-10617-Shortcut步长条件]] 用“一次两倍步长 = 两次单倍步长”直观解释这一约束。[[S-2024-Frans-Shortcut-Models]] 的一级实验表明单网络可适应多个 inference budgets。

### 6.1 自洽不等于正确

常数 map $F_h(x)=c$ 可以在很多 composition loss 下高度自洽，却不搬运到数据分布。必须同时有 base velocity/data supervision、boundary condition 与 distribution-level evaluation。consistency 是必要结构之一，不是充分正确性证书。

## 七、四条路线对照

| 路线 | 直接 target | teacher | 输入 | 一步输出的意义 |
|---|---|---|---|---|
| Progressive distillation | teacher 两步终点 | 必需，逐轮更新 | $(x,t)$ 或参数化输出 | 模仿压缩 teacher map |
| SiD/score identity | teacher/student score identity | 预训练 score teacher | noise $z$ 与 noisy samples | 单步 generator sample |
| Consistency model | 同轨迹公共端点 | 可有，也可独立训练 | $(x_t,t)$ | trajectory endpoint estimate |
| Shortcut | step composition + $h=0$ velocity | 不需多步 teacher | $(x,t,h)$ | 指定步长 displacement |

## 八、统一诊断：composition residual

对任意 finite map 定义

$$
R(x;t,h_1,h_2)=
\left\|
F_{t,h_1+h_2}(x)
-F_{t+h_1,h_2}(F_{t,h_1}(x))
\right\|.
$$

测试应覆盖：

- 训练见过/未见过的 $h$；
- on-trajectory 与 perturbed off-trajectory $x$；
- conditional/unconditional 与不同 CFG scales；
- one-step vs multi-step sample quality；
- 不同 precision 与 batch size。

residual 小不证明 distribution correct，但能定位 finite-map 自洽是否失败。

## 九、科学空间研读框

- [[S-2024-Su-10085-SiD上]]、[[S-2024-Su-10567-SiD下]]：帮助理解恒等变换与程序梯度边界；
- [[S-2024-Su-10633-一致性模型]]：把 trajectory invariant 与 boundary condition 拆成初学者可跟随的步骤；
- [[S-2024-Su-10617-Shortcut步长条件]]：把 step-conditioned finite map 写成组合公式；
- 课程用原论文和 composition counterexample 补上“自洽但错误”的边界。

## 十、图：同样 1-NFE，监督对象并不同

先回答：三条彩色路径分别把谁当 target？哪条依赖 teacher trajectory，哪条要求同轨迹端点，哪条显式输入 $h$？

![[00-知识库管理/_assets/figures/generative-models/fig-distillation-consistency-shortcut-v1.svg|900]]

> [!figure] 图 50.9-05　蒸馏、Consistency 与 Shortcut 的对象对照
> 图以同一 time line 排列 teacher two-step、endpoint invariant 与 step composition。来源：据 Progressive Distillation、Consistency Models、Shortcut Models 及科学空间 10085/10567/10617/10633 独立绘制。

**怎样读图**：不要先看“最终都一步”，而要先读每条路线的 target 箭头和 stop-gradient；再检查 boundary 与可变步数接口。

**图没有证明什么**：图不证明自洽 loss 足以保证正确分布，不证明 student 可超越 teacher，也不证明所有一步模型都有 continuous-time flow 解释。

## 十一、学习出口

- 能写 progressive two-to-one target；
- 能解释 consistency boundary 与同轨迹不变量；
- 能展开 Shortcut composition；
- 能构造“自洽但错误”的常数 map 反例；
- [[习题 - 扩散蒸馏、一致性模型与 Shortcut]]
- [[解答 - 扩散蒸馏、一致性模型与 Shortcut]]

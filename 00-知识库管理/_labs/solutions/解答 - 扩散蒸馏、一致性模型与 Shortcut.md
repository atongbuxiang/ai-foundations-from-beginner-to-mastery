---
type: solution
status: draft
topic: "[[扩散蒸馏、一致性模型与 Shortcut]]"
exercise: "[[习题 - 扩散蒸馏、一致性模型与 Shortcut]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - 扩散蒸馏、一致性模型与 Shortcut
## A. 识别与复述
### GEN69-A01
Progressive distillation 拟合 teacher 两小步终点；consistency model 拟合同一 trajectory 的共同端点；Shortcut 学显式步长条件的 displacement rate，并约束大步/小步 composition。
### GEN69-A02
$f(x,\epsilon)=x$（或参数化中等价的端点恒等），保证终点映射不漂移成任意常数。
### GEN69-A03
$f$ 必须只依赖被条件化的 $(x_t,t)$；若直接依赖独立 $x_0$ 或 $\epsilon$，就不能把 conditional expectation target 无条件替换成噪声样本。
## B. 手算与建模
### GEN69-B01
$T_h(T_h(x))=.9(.9x+1)+1=.81x+1.9$，故精确 affine student 为 $a=.81,b=1.9$。
### GEN69-B02
一次 $2h$ 得 $x+2h(x+2h)=x+2hx+4h^2$。两次 $h$ 得 $(1+2h+h^2)x+2h^2+h^3$。差为 $h^2(x-2+h)$，residual 是其绝对值/范数。
### GEN69-B03
$F_{2h}(x)=c$，而 $F_h(F_h(x))=F_h(c)=c$，residual 为 0。它证明 composition 自洽不保证 map 保留信息或生成正确分布。
## C. 推导与证明
### GEN69-C01
$x'=T_h(x,t)$，$x''=T_h(x',t-h)$，$L=\|F_\theta(x,t,2h)-\operatorname{sg}(x'')\|^2$。teacher 参数不接收该 loss 梯度。
### GEN69-C02
理想条件 $f(x(t),t)=x(\epsilon)$ 与 $f(x(r),r)=x(\epsilon)$，故两者相等。实际相邻对用 teacher solver 近似保证来自同轨迹。
### GEN69-C03
$x+2hv(x,t,2h)=x+hv(x,t,h)+hv(x+hv(x,t,h),t+h,h)$；消去 $x$、除 $2h$ 得两小步速度的平均 target。
## D. 边界、反例与纠错
### GEN69-D01
teacher numerical map 含 solver、field 与 terminal bias。student 至多逼近 teacher 在训练输入分布上的函数，不能凭模仿关系升级为真实 transport。
### GEN69-D02
训练 pair 位于 teacher trajectories 的薄集合；网络可在这些点一致、稍离轨迹就任意变化。多步部署或 guidance 扰动会访问 off-trajectory states。
### GEN69-D03
SiD 学 generator distribution gradient，progressive distill 学 teacher map，consistency 学 endpoint invariant，Shortcut 学 step-conditioned map；只有部署预算相同，目标并不相同。
## E. AI 迁移
### GEN69-E01
从 teacher path 取 on-trajectory states，再加正交/随机扰动形成 off-trajectory；扫 seen/unseen $h_1,h_2$，计算 composition residual 和终点误差，并按扰动幅度画曲线。
### GEN69-E02
每 stage 报 teacher/student NFE、配对 target solver、训练 examples/compute、map MSE、sample metrics、P/R、累计 wall-time、初始化/EMA、下一 stage 是否继承及 failures。
### GEN69-E03
固定 architecture/data/budget；distillation 使用同一 teacher 并计 teacher cost；training 路线从 scratch。统一 one/multi-step sampler、NFE、guidance 与评价，并分别报告 teacher dependence 和终点/coverage。

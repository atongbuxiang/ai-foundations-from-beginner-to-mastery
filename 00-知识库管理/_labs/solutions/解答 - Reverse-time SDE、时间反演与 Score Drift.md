---
type: solution
status: draft
topic: "[[Reverse-time SDE、时间反演与 Score Drift]]"
exercise: "[[习题 - Reverse-time SDE、时间反演与 Score Drift]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Reverse-time SDE、时间反演与 Score Drift
## A. 识别与复述
### GEN50-A01
若保留 $t$ 并从 $1$ 积到 $0$：
$$dX_t=[f(X_t,t)-g(t)^2s_t(X_t)]dt+g(t)d\bar W_t.$$
若 $Y_\tau=X_{1-\tau}$、$\tau$ 从 $0$ 到 $1$：
$$dY_\tau=[-f(Y_\tau,1-\tau)+g(1-\tau)^2s_{1-\tau}(Y_\tau)]d\tau+g(1-\tau)d\widetilde W_\tau.$$
### GEN50-A02
inverse map 要从一个 noisy sample 恢复同一个 forward sample/noise realization；扩散一般 many-to-one，做不到。reverse process 只要求 transition law 正确，使边缘按反序回到数据。生成采的是一个合法 posterior-like path，不是找回历史路径。
### GEN50-A03
Brownian motion 必须相对于所用 filtration 有独立增量。forward $W$ 适应过去信息；反向过程的信息流相反，需要新的 Brownian motion。逐项取负依赖整条保存的 forward path，不是只给当前状态时的 reverse Markov kernel。
## B. 手算与建模
### GEN50-B01
$s=-x,f=-\beta x/2,g^2=\beta$，故 $\tau$-drift
$$-f+g^2s=\beta x/2-\beta x=-\beta x/2.$$
与 forward OU drift 相同，符合平稳可逆性；这是时间符号最有效的回归测试。
### GEN50-B02
$p_t=N(0,4+t)$，所以 $s_t(x)=-x/(4+t)$。因 $f=0,g=1$，$\tau$-drift 就是 $-x/(4+t)$。
### GEN50-B03
$t$-clock bracket 为 $f-g^2s=0.4-4(-0.3)=1.6$。drift increment $1.6(-0.01)=-0.016$；noise increment $2\sqrt{0.01}(0.5)=0.1$。新状态 $1-0.016+0.1=1.084$。
## C. 推导与证明
### GEN50-C01
局部写 $Y=Z+g\sqrt h\epsilon$、$Z=X_t+fh$。Gaussian Tweedie identity 给 $E[Z|Y=y]=y+g^2h\nabla\log p_{t+h}(y)+o(h)$。减去 $fh$ 后，$E[X_t-Y|Y=y]=[-f+g^2s]h+o(h)$，这就是向过去走正反时钟小步的 drift。
### GEN50-C02
$dt=-d\tau$，且 $X_t=Y_\tau$。把 $[f-g^2s]dt$ 替换为 $[-f+g^2s]d\tau$，再把系数时间参数换成 $1-\tau$。反向 Brownian 重新按 $\tau$ 定义，diffusion amplitude 保持正。
### GEN50-C03
令 $D=GG^\top$。在 $t:1\downarrow0$ 记法中
$$b_{rev,i}=b_i-\sum_j\partial_jD_{ij}-\sum_jD_{ij}\partial_j\log p_t.$$
当 $D=g(t)^2I$ 与空间无关时 $\nabla\cdot D=0$，才化为 $f-g^2s$。
## D. 边界、反例与纠错
### GEN50-D01
递增 $\tau$ 应使用 $-f+g^2s$。误用 $f-g^2s$ 会把实际 drift 整体取反；平稳 OU 检查会得到 $+\beta x/2$ 或更离谱的 outward drift，而非正确的 $-\beta x/2$。
### GEN50-D02
生成时没有与 terminal sample 配套的 forward noise history。即使人为保存，倒放 noise 构成的是特定 coupled reconstruction，不是从 prior 独立采样的 generative Markov process。正确 reverse transition 还需要 density score 的 Bayes correction。
### GEN50-D03
定理假定真实 $s_t$、连续过程、正确 terminal law 和正则性。实现还加入 score approximation、finite data/optimization、prior mismatch、time grid 和 SDE discretization error；任一项都能使终点 law 偏离数据。
## E. AI 迁移
### GEN50-E01
检查：time grid 方向；drift step 保留 signed $h$；noise 用 $\sqrt{|h|}$；score shape/dtype；$g^2$ 与 $g$ 不混；$t$-clock/clock-$\tau$ 公式一致；最后一步噪声 policy；zero-score/zero-diffusion 特例；固定 seed 可复现；所有值 finite；stationary OU 统计保持 $N(0,I)$。
### GEN50-E02
$s_\theta=s+e$ 时 $t$-clock drift error 为 $-g^2e$，$\tau$-clock 为 $+g^2e$。按时间报告 $E\|e\|^2$、$g^4E\|e\|^2$、访问状态分布、step size 与累计 drift-error proxy，避免只给 unweighted score MSE。
### GEN50-E03
采 $X_1\sim N(0,I)$，在常数 $\beta$ 下用两种时钟分别反向模拟；解析上各时刻 mean 0、variance 1。自动比较两实现的样本统计与逐 seed coupling，并故意切换符号确认测试会失败。至少多组步长，防止误差偶然抵消。

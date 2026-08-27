---
type: solution
status: verified
area: [training, optimization, mup, mutransfer]
topic: "[[μTransfer、Base Shape 与超参数零样本迁移]]"
exercise: "[[习题 - μTransfer、Base Shape 与超参数零样本迁移]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - μTransfer、Base Shape 与超参数零样本迁移

> [!warning] 使用边界
> Base/delta oracle 只编码所声明的 width-like dimensions；depth、data、regularization 与系统变化不由它自动担保。

## A. 识别与复述

### TRN45-A01
base 是参数化兼容锚；delta 与 base 的 shape 差异标记 infinite dimensions；二者可完全不训练。proxy 是实际运行 HP 搜索/曲线验证的小模型，可等于 base 或更大；target 是最终训练对象。proxy 与 target 必须训练，base/delta 只在兼任它们时才训练。

### TRN45-A02
严格 zero-shot 指协议锁定后，不用 target-scale HP 搜索结果选择 target HP。它不表示 target 不训练、不做 NaN/health check、不做最终评估、不计 target confirm budget，也不允许看到 target 后无限改 recipe 仍保持名称。

### TRN45-A03
参数化/优化候选：base LR、momentum/betas、init multiplier、schedule shape；regularization：dropout、weight decay、label smoothing/early stop；额外跨轴：depth、batch、sequence length、training time。最后一类需要专门实验和 caveat。

## B. 手算与构造

### TRN45-B01
delta 两维都不同，故都标为 infinite。target/base multipliers 为
$$
1536/256=6,\qquad4096/1024=4.
$$
若 delta 第二维不变，它会被误标 finite，target 的第二维虽扩大，initializer/LR translator 可能不缩放，形成静默 FFN/fan-in bug。

### TRN45-B02
A 可取 $(512,8,64,2048)$：$d,h,d_{ff}$ infinite，$d_h$ finite。B 可取 $(512,4,128,2048)$：$d,d_h,d_{ff}$ infinite，$h$ finite。两者总 $d$ 相同，但 attention dot-product 与 head aggregation path 不同。

### TRN45-B03
proxy argmin 为 $h=2$，target argmin 为 $h=4$。在 $\log_2h$ 坐标距离为 $|1-2|=1$。transfer regret 为
$$
F_{target}(2)-F_{target}(4)=0.82-0.78=0.04.
$$
argmin 移动一个 grid level，但决策损失只有 0.04；两者回答不同问题。

## C. 推导与证明

### TRN45-C01
任取 $\varepsilon>0$。separation 给 $\gamma_\varepsilon>0$，使 $d(h,h^*)\ge\varepsilon$ 时
$$
F_\infty(h)\ge F_\infty(h^*)+\gamma_\varepsilon.
$$
一致收敛后 $\sup_h|F_n-F_\infty|<\gamma_\varepsilon/3$。于是远处
$$
F_n(h)>F_\infty(h^*)+2\gamma_\varepsilon/3,
$$
而 $F_n(h^*)<F_\infty(h^*)+\gamma_\varepsilon/3$，故 minimizer 不可能在远处。对所有 $\varepsilon$ 成立即 $h_n^*\to h^*$。

### TRN45-C02
令 $\mathcal H=[0,1]$、$F(h)=h^2$，并在 $h_n=1/2$ 附近宽度 $1/n^2$ 的小区间挖深度 1 的连续窄谷 $g_n$，令 $F_n=F-g_n$。对每个固定 $h\ne1/2$，最终不落在移动/收缩谷内；可再令谷中心轻微移动避免固定点，得到 pointwise $F_n\to F$，但 minimizer 追随窄谷而不去 0。sup error 始终约 1，所以非一致。

### TRN45-C03
$$
\mathcal H_n(\tau)=\{h:F_n(h)\le\min_gF_n(g)+\tau\}.
$$
若 proxy 选择 $\hat h\in\mathcal H_{target}(\tau)$，按定义
$$
R(target\leftarrow proxy)
=F_{target}(\hat h)-\min_hF_{target}(h)\le\tau.
$$
因此平坦谷中 argmin label 变化不妨碍实用迁移。

## D. 边界、反例与纠错

### TRN45-D01
极小 proxy 可能容量不足、head/norm 进入离散边界、batch/width 比极端、activation law 远离渐近区、最优曲线被 underfitting 主导或 flat/noisy。应在 proxy ladder 上先确认 curve/telemetry 进入近似稳定窗口。

### TRN45-D02
8 个 target LR 已构成 target-scale search。应称 target-assisted/few-shot tuning；若逐层缩邻域可称 telescoping。报告 8 次 target 训练、失败和选择成本到 $C_{confirm}$/$C_{tune}$，不能只报最终 run。

### TRN45-D03
regularization optimum 依数据量、capacity、训练时长和 validation target。例：μP 使各宽 train-loss LR 曲线对齐，但大模型过拟合更强，target 最佳 dropout/WD 增大；train loss 迁移不推出 validation regularization 迁移。

## E. AI 迁移

### TRN45-E01
八步：冻结 family/axes；设计 base/delta；打印并审计 infshape；设置 μP init/readout/optimizer；多 width coord check；预注册 HP space/seeds/selection/budget；在 proxy ladder 保存整条曲线并锁定 base HP；target 只执行 translator 后训练与预注册 health/final evaluation，记录所有 confirm/failure。

### TRN45-E02
测试每个 group 在 optimizer 建立后保存 base ratio，scheduler step 后验证所有 LR 仅乘同一相对因子；故意使用绝对赋值应触发测试失败。保存 checkpoint 后 fresh/resume 比较 infshape、optimizer groups、scheduler state 和下一步 $\Delta W$；恢复时禁止重复 rescale parameters。

### TRN45-E03
可写：“在固定 40M—4B family、width path、数据/optimizer 和预注册 HP space 下，40M 选择经 μP 直接用于 4B，并通过列明 health/metric；未验证其他 depth/data/regularization。”加入 200M/1B 搜索后应称 multiscale/telescoping transfer，累计所有中间 search 与 target confirm 成本。

## 无提示重做

- [ ] 48 小时后完整证明 argmin stability。
- [ ] 一周后从一份 base/delta shape diff 找三类静默 bug。

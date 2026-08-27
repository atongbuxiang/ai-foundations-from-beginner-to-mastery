---
type: solution
status: verified
area: [training, optimization, matrix-preconditioning]
topic: "[[SOAP、二阶混合优化器与成本证据地图]]"
exercise: "[[习题 - SOAP、二阶混合优化器与成本证据地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - SOAP、二阶混合优化器与成本证据地图

> [!warning] 使用边界
> SOAP 是带版本与实现合同的双时间尺度算法族。论文结果、preliminary code 与后续分布式实现不能在未核对方程和 state transport 时混为同一个对象。

## A. 识别与复述

### TRN24-A01
对 $G\in\mathbb R^{m\times n}$，$Q_L\in\mathbb R^{m\times m}$、$Q_R\in\mathbb R^{n\times n}$，先算 $\bar G=Q_L^TGQ_R$；在同 shape 的 rotated coordinates 更新 $\bar m,\bar v$ 并形成 $\bar U$；最后 $U=Q_L\bar UQ_R^T$ 返回原参数坐标。每个 state 都要注明当前 basis version。

### TRN24-A02
Fast state 是每步更新的 rotated first/second moments 与 parameter update；slow state 是 Gram statistics、eigenbasis 及低频 refresh。快 diagonal adaptation 可在旧 basis 内跟踪 eigenvalue scale 与部分非平稳性，但不消除 eigenvectors 已旋转、basis 退化或旧 moments 坐标语义失效。

### TRN24-A03
算法门锁定方程与 state transition；数值门检查 eig/root residual、gap、dtype 与 repair；系统门核对 bytes、通信和尾时延；调参门要求等额搜索并计失败；统计门要求 paired seeds、CI 与预注册指标。Iteration 变少只描述算法计数，尚未证明数值可靠、系统时间更短或统计上稳定。

## B. 手算与构造

### TRN24-B01
$Q$ 对称正交，直接算得
$$\bar G=Q^TGQ=\begin{bmatrix}1&1\\1&1\end{bmatrix}.$$
再乘 $Q\bar GQ^T=\operatorname{diag}(2,0)=G$。$\|G\|_F=2$，$\|\bar G\|_F=\sqrt{4}=2$，验证正交左右变换保持 Frobenius norm。

### TRN24-B02
$Q^Tg=(1/\sqrt2,1/\sqrt2)$，逐坐标除以绝对值后得 $(1,1)$，转回 $Q(1,1)=(\sqrt2,0)$。原 basis 直接 normalization 是 $(1,0)$；方向相同但长度不同，换其他 $g$ 还可改变方向。这说明 nonlinear elementwise map 不与一般 rotation commute。

### TRN24-B03
$$Q^TVQ=\begin{bmatrix}5&-4\\-4&5\end{bmatrix}.$$
若只保存 diagonal，只剩 $(5,5)$，丢掉 $-4$ 的 cross-coordinate correlation；若干脆沿用旧向量 $(1,9)$，又把旧坐标数字误解释为新坐标 statistics。二阶逐元素 state 没有无损的简单向量旋转规则。

## C. 推导与证明

### TRN24-C01
$$\|Q_L^TGQ_R\|_F^2=\operatorname{tr}(Q_R^TG^TQ_LQ_L^TGQ_R)=\operatorname{tr}(G^TG).$$
但 elementwise $\psi(x)=m/(\sqrt v+\epsilon)$ 不是线性 map，一般 $\psi(Q^Tg)\ne Q^T\psi(g)$；basis 因而决定哪些坐标各自积累平方与归一化。

### TRN24-C02
用 $L=Q_L\Lambda_LQ_L^T$、$R=Q_R\Lambda_RQ_R^T$，
$$L^{-1/4}GR^{-1/4}=Q_L[\Lambda_L^{-1/4}(Q_L^TGQ_R)\Lambda_R^{-1/4}]Q_R^T.$$
Shampoo 在 basis 中按左右 eigenvalue separably 缩放；SOAP 在该 basis 内再每步更新 Adam-like $m,v$，提供比低频 eigenbasis 更快的逐坐标 scale adaptation。

### TRN24-C03
若非 refresh step 为 $T_{base}$、refresh 额外成本为 $T_{eig}$，平均约 $T_{base}+T_{eig}/K$，但 refresh step tail 为 $T_{base}+T_{eig}$，还可能触发跨设备 barrier。平均吞吐能隐藏 p95/p99 spike、temporary peak memory 与 straggler 放大，故系统门要同时报告时间分布。

## D. 边界、反例与纠错

### TRN24-D01
$L=cI$ 时任意正交 $Q$ 都是 eigenbasis，而 matrix function 始终 $L^{-1/4}=c^{-1/4}I$，basis 在 $Qf(\Lambda)Q^T$ 中相消。若在所选 $Q$ 中维护 diagonal nonlinear moments，不同 $Q$ 会产生不同坐标平方与 normalization，且旧 state 在 basis 跳变时不自动相消。

### TRN24-D02
组合后的 state 不等于两个独立状态的直和：gradient 先被旋转，Adam moments 在随时间变化的坐标中累积，非线性 normalization 与 rotation 不交换，refresh/transport 还引入近似。任何保证都需对组合 transition 重新证明，不能把 Shampoo 与 Adam 的结论机械相加。

### TRN24-D03
不能直接外推，因为模型宽深/张量 shape 改变 eig/root 成本，硬件 kernel 与通信拓扑不同，batch/gradient noise regime 不同，refresh/block/precision policy 不同，调参预算与 baseline 强度可能不同，训练 token/checkpoint rule 不同，downstream/generalization 与 training loss 也不是同一指标。

## E. AI 迁移

### TRN24-E01
每次 refresh 记录 factor/eigenbasis version、min gap 与 cluster、$\|Q_t^TQ_{t-K}-I\|$ 或子空间 angle、在新 basis 的 off-diagonal residual、moment transport/reset/reuse policy、refresh 前后 direction cosine/norm/loss、eig residual、repair/NaN、耗时与 peak workspace。

### TRN24-E02
统一模型/数据/token/batch、初始化与 paired seeds；为三者给等额加速器小时和搜索 trials，预注册 LR/decay/epsilon/block/refresh 空间与 checkpoint rule，所有 OOM/NaN 计入。报告 CI、time-to-quality、最终质量、state/peak bytes、平均与 p95 time、通信和能耗。

### TRN24-E03
卡片依次写 curvature/scale object、label/data estimator、block/Kronecker/basis approximation、eig/root/solve residual、fast/slow clocks、bytes/FLOPs/communication/tail、search/seeds/CI。缺算法字段时对象不确定；缺数值字段只能称实现候选；缺系统或调参/统计字段时，性能结论最多是指定 run 的 tentative observation。

## 无提示重做

- [ ] 48 小时后手算一次 45° basis 旋转与 nonlinear normalization。
- [ ] 一周后用五道证据门审计一张 optimizer benchmark 表。

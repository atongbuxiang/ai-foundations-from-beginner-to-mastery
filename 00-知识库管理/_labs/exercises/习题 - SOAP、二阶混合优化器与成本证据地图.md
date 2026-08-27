---
type: exercise
status: verified
area: [training, optimization, matrix-preconditioning]
topic: "[[SOAP、二阶混合优化器与成本证据地图]]"
solution: "[[解答 - SOAP、二阶混合优化器与成本证据地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - SOAP、二阶混合优化器与成本证据地图

> [!abstract] 训练目标
> 追踪 gradient、basis 与 Adam-like moments 的坐标语义；识别双时间尺度、退化 eigenspace 和 state transport 风险，并用五道证据门限制性能外推。

## A. 识别与复述

### TRN24-A01
写出矩阵 gradient 从原坐标旋转到 Shampoo eigenbasis、在 basis 中更新、再转回的 shape-preserving 流程。

### TRN24-A02
SOAP 的 fast state 与 slow state 分别是什么？它试图缓解 Shampoo slow refresh 的哪种失配，又没有消除哪种失配？

### TRN24-A03
逐一解释算法门、数值门、系统门、调参门与统计门；为什么通过“少 iteration”只够进入下一道门？

## B. 手算与构造

### TRN24-B01
令 $Q=2^{-1/2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}$、$G=\operatorname{diag}(2,0)$。计算 $\bar G=Q^TGQ$，再验证 $Q\bar GQ^T=G$ 与 Frobenius norm 不变。

### TRN24-B02
一维向量在原 basis 的单步 Adam-like normalization（$\epsilon=0$）对 $g=(1,0)$ 给 $(1,0)$。把 $g$ 旋转 45° 后逐坐标 normalization，再转回，结果是什么？用它说明 elementwise nonlinear state 不具一般 rotation equivariance。

### TRN24-B03
旧 basis 中二阶矩的完整矩阵为 $V=\operatorname{diag}(1,9)$。用上一题的 $Q$ 变换到新 basis，计算 $Q^TVQ$；若实现只保存 diagonal，会丢掉什么？

## C. 推导与证明

### TRN24-C01
证明正交左右旋转 $\bar G=Q_L^TGQ_R$ 保持 Frobenius norm；再说明为何随后逐元素 $m/(\sqrt v+\epsilon)$ 会让最终 update 依赖 basis。

### TRN24-C02
把 Shampoo 的 $L^{-1/4}GR^{-1/4}$ 写到左右 eigenbasis 中，展示它是对 $\bar G$ 的 separable eigenvalue scaling；说明 SOAP 在同一 basis 加入了什么快适应。

### TRN24-C03
给定 refresh period $K$，写出 average step time 与 refresh-tail time；说明只报告平均吞吐为何可能掩盖训练抖动和同步瓶颈。

## D. 边界、反例与纠错

### TRN24-D01
当 $L=cI$ 有重复 eigenvalue 时，说明 eigensolver 可返回任意正交 basis。为什么 Shampoo matrix function 不受影响，而 basis 中的 diagonal nonlinear moments 可能受影响？

### TRN24-D02
反驳：“SOAP=Shampoo+Adam，所以两者各自的理论保证自动相加。”从 state space、坐标变换、非线性与近似刷新回答。

### TRN24-D03
一项 360M/660M 模型实验报告 SOAP 更快。列出不能直接外推到另一模型规模、硬件、batch regime 或 downstream 指标的至少五个原因。

## E. AI 迁移

### TRN24-E01
设计 basis-refresh 审计日志：包含 eigen-gap、basis alignment、off-diagonal residual、state transport、refresh spike、direction cosine 与 repair 行为。

### TRN24-E02
为 SOAP/AdamW/Shampoo 三方设计公平 benchmark，要求给出 paired seeds、equal search budget、failed trials、checkpoint rule、state bytes 与 time-to-quality。

### TRN24-E03
建立“算法对象→估计器→结构近似→数值线代→state clocks→系统→统计证据”的完整卡片，并说明哪一字段缺失时只能作 tentative 结论。

## 作答与复盘

每题记录 `independent / hinted / copied / blocked / careless`。性能题必须写清外推边界，完成后打开 [[解答 - SOAP、二阶混合优化器与成本证据地图]]。

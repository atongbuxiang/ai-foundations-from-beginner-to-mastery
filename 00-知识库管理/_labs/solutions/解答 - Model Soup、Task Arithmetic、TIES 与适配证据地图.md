---
type: solution
status: verified
area: [language-models, model-merging, task-arithmetic, ties]
topic: "[[Model Soup、Task Arithmetic、TIES 与适配证据地图]]"
exercise: "[[习题 - Model Soup、Task Arithmetic、TIES 与适配证据地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Model Soup、Task Arithmetic、TIES 与适配证据地图

## A. 识别与复述

### LM32-A01
需同架构/shapes、parameter names/order、共同 base 或明确 alignment、tokenizer/vocab/output head、config/norm/position、adapter target/merge status。只要坐标语义不一致，逐元素加法虽能运行也无明确 task-vector 含义。

### LM32-A02
Uniform soup 等权平均 checkpoints；greedy soup 用 validation 逐步选 ingredients；task arithmetic 先减共同 base 得 vectors再加/减/缩放；ensemble 同时运行多个模型并合输出。Soup/arithmetic 产一个参数模型。

### LM32-A03
Trim 将绝对值较小更新置零；elect sign 为每坐标选聚合方向；merge 只聚合同方向的保留更新，再按 scale 加回 base。Density、tie、aggregation、scale 都需声明。

## B. 手算与构造

### LM32-B01
Uniform soup $(\theta_1+\theta_2)/2=((2,0)+(1,3))/2=(1.5,1.5)$。$\tau_1=(1,-1)$、$\tau_2=(0,2)$；task-vector sum $\theta_0+\tau_1+\tau_2=(1,1)+(1,1)=(2,2)$。

### LM32-B02
Trim 得 $(.8,.6,0)$；sum 为 1.4，elect positive；aligned mean $(.8+.6)/2=.7$。该坐标的 merged task vector 为 +.7，再乘全局 scale 后加 base。

### LM32-B03
三值都通过阈值；sum=-.8，elect negative；aligned negatives 为 -.7、-.6，mean=-.65。普通均值 $(-.7+.5-.6)/3=-.8/3\approx-.2667$，因正冲突被一起平均而幅度更小。

## C. 推导与证明

### LM32-C01
$f_{\theta_0+\delta}\approx f_0+J_0\delta+\frac12\delta^\top H\delta$。令 $\delta=\tau_1+\tau_2$，一阶项线性分成 $J\tau_1+J\tau_2$；二阶含各自项和交叉 $\tau_1^\top H\tau_2$，大 vector/曲率/激活边界使近似失效。

### LM32-C02
由 rank 次可加性，$\operatorname{rank}(\sum_kB_kA_k)\le\sum_k\operatorname{rank}(B_kA_k)\le\sum_kr_k$。实际 rank 可因方向重合/抵消更小。

### LM32-C03
$\theta(\lambda)=(1-\lambda)\theta_1+\lambda\theta_2$；可定义 $B=\max_{\lambda\in[0,1]}\mathcal L(\theta(\lambda))-\max\{\mathcal L(\theta_1),\mathcal L(\theta_2)\}$。需在声明 distribution/metric 网格化估计，不是全空间证明。

## D. 边界、反例与纠错

### LM32-D01
一输入、两隐单元的线性网络：模型 A 有 $W=(1,-1)^\top,v=(1,-1)$，$f_A=v^\top Wx=2x$；模型 B 同两单元置换，$W=(-1,1)^\top,v=(-1,1)$，仍 $2x$。逐坐标平均得 $W=v=0$，函数变 0。

### LM32-D02
两个 tasks 可在不同坐标或同号方向上仍要求互斥 outputs；Hessian/activation/normalization 也会产生非线性交互。Sign conflict 只是参数 proxy，消除它不证明功能兼容。

### LM32-D03
Greedy soup 多次在同 validation 比 candidate/组合，winner 对该集乐观，且顺序/候选数量影响结果。应披露 candidates/order/search，使用独立 final test并计选择成本。

## E. AI 迁移

### LM32-E01
断言所有 config/name/shape/tokenizer/base hashes；计算 $\tau_k=\theta_k-\theta_0$ 后断言 $\theta_0+\tau_k=\theta_k$；在小 tensors 手算 soup/TIES；保存 coefficients/density/sign；serialize/reload 后 hash/逐元素与 logits一致。

### LM32-E02
行是 ingredients、single best、uniform/greedy soup、task arithmetic、TIES、ensemble、multitask FT；列为每 task、macro/worst、unseen/OOD、old base、calibration、安全、latency/memory；多 seed/CI，selection/final 分离并扫 coefficients。

### LM32-E03
平均分可掩最坏任务退化；未知 base/ingredients 无法复建 vectors；未知 search/coefficients 存在选择偏差。应索取 hashes、candidate pool、per-task results、OOD/safety、merge hyperparameters与成本，否则只接受 winner 的不可复现观察。

## 无提示重做

- [ ] 手算 soup、task-vector sum 与 TIES 三步。
- [ ] 用 permutation 反例和 Taylor 二阶项说明参数平均边界。


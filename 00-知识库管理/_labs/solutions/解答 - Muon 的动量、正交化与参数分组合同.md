---
type: solution
status: verified
area: [training, optimization, muon, implementation-contract]
topic: "[[Muon 的动量、正交化与参数分组合同]]"
exercise: "[[习题 - Muon 的动量、正交化与参数分组合同]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Muon 的动量、正交化与参数分组合同

> [!warning] 使用边界
> 这里的“当前 PyTorch”绑定 2026-08-26 访问日。软件默认值和 transition 可变；实现题必须同时记录版本/commit。

## A. 识别与复述

### TRN27-A01
对符合 filter 的二维 $W$：

1. 取得本步 gradient $G_t$；
2. $B_t=\mu B_{t-1}+(1-\mu)G_t$；
3. Nesterov 开启时 $M_t=(1-\mu)G_t+\mu B_t$，否则 $M_t=B_t$；
4. 缩放 $M_t$，用指定 coefficients/dtype 做 $K$ 步 NS，得 $\widehat Q_t$；
5. $\eta_{adj}=\eta s(A,B)$；
6. decoupled decay：$W\leftarrow(1-\eta\lambda)W$；
7. update：$W\leftarrow W-\eta_{adj}\widehat Q_t$。

任何 clipping、gradient scaling、distributed reduction 和 None-gradient rule 都应插入到确切位置，而不是写在流程之外。

### TRN27-A02
polar 是非线性 matrix map，改变矩阵分块/reshape 就改变 singular subspaces。fused QKV joint polar 与三块 polar 不等；embedding 有 token-frequency/sparse geometry；output head 与 logits/weight tying 耦合；bias/norm 是 1D，不满足当前接口；4D convolution reshape 的轴分组定义了新的矩阵 norm。故 group manifest 既决定计算，又决定理论对象。

### TRN27-A03
None 表示本步没有 gradient tensor，常见合同是跳过 state 和 update；显式零表示 gradient 已定义为零，旧 momentum 仍会衰减并可产生 update。若 decay 对有参数统一施加，None 是否 decay 还依框架而定。conditional/MoE 参数若把 None 错转成零，会改变 state clock、inactive-expert drift 和 checkpoint trajectory。

## B. 手算与构造

### TRN27-B01
EMA：
$$
B_1=0.1(2)=0.2,\qquad
B_2=0.9(0.2)+0.1(-1)=0.08.
$$
sum-style：
$$
\widetilde B_1=2,\qquad
\widetilde B_2=0.9(2)-1=0.8.
$$
当前风格 Nesterov：
$$
M_1=0.1(2)+0.9(0.2)=0.38,
$$
$$
M_2=0.1(-1)+0.9(0.08)=-0.028.
$$
若误把 sum buffer 代入相同 Nesterov 公式，方向/尺度都改变。

### TRN27-B02
正确 decay：
$$
W^{decay}=(1-10^{-3}\cdot0.1)3=2.9997.
$$
adjusted direction step 为 $10^{-3}\cdot2\cdot0.5=0.001$，故
$$
W_{t+1}=2.9987.
$$
若 decay 也用 adjusted LR，则
$$
(1-0.002\cdot0.1)3-0.001=2.9984.
$$
单步差 $3\times10^{-4}$；长期乘积会累积为不同 regularization path。

### TRN27-B03
一维 msign 为 sign：
$$
\operatorname{sign}(2+(-1))=1,
$$
而
$$
\operatorname{sign}(2)+\operatorname{sign}(-1)=1-1=0.
$$
把标量嵌入矩阵的一个对角 block 即得 matrix counterexample。nonlinear polar 不能与 sum/all-reduce 交换，所以要先定义 global gradient 还是 local update。

## C. 推导与证明

### TRN27-C01
零初始化、固定 $\mu$ 下：
$$
\widetilde B_t=\sum_{\tau=1}^t\mu^{t-\tau}G_\tau,
$$
$$
B_t=(1-\mu)\sum_{\tau=1}^t\mu^{t-\tau}G_\tau
=(1-\mu)\widetilde B_t.
$$
但这只是 buffer 的比例。后续若用 $\varepsilon$ normalization、clipping、finite-precision threshold、different Nesterov mix 或 state-dependent scaling，常数不能无条件穿过非线性；time-varying $\mu$ 使比例也不再固定。旧 checkpoint 若未声明 convention，无法安全推断其数值意义。

### TRN27-C02
取三个 $1\times1$ blocks 都等于 $[1]$。joint stack 是 $G=(1,1,1)^T$，其 polar 为
$$
\operatorname{polar}(G)=\frac1{\sqrt3}(1,1,1)^T.
$$
逐块 polar 再拼接得到 $(1,1,1)^T$，二者不同，后者 spectral norm 为 $\sqrt3$，不满足 joint spectral-unit budget。一般 block singular subspaces 还会耦合，所以不只是常数尺度差。

### TRN27-C03
restore 至少断言：

1. parameter stable name/ID；
2. exact shape 与 layout/stride；
3. unique optimizer owner；
4. Muon/fallback group membership；
5. buffer shape、dtype 和 EMA/sum semantics；
6. momentum、Nesterov 与 step clock；
7. NS steps、coefficients、normalization 与 compute dtype；
8. shape adjustment exact formula/global shape；
9. base LR、decay 与 order；
10. fused QKV/reshape manifest；
11. distributed shard placement；
12. save/load 后固定 gradient 的下一步在容差内一致。

## D. 边界、反例与纠错

### TRN27-D01
同为 0.95 仍可能一个用 EMA、一个用 sum；一个在 buffer 更新后做 Nesterov、另一个在 lookahead gradient 上做；一个按 optimizer step 更新、另一个按 microbatch 更新。还可能有 bias correction、dampening、None-gradient clock、dtype 与 initialization 差异。超参数名字相同不等于 transition 相同。

### TRN27-D02
polar 是 nonlinear，局部 polar 拼接不等于 global polar；global adjustment 可能用 $A/B$，local shard 则看到不同 ratio；global singular vectors常跨越 shard boundary，局部计算无法恢复它们。除非算法明确定义 block/shard geometry，否则 local operation 不是 global operation 的透明并行化。

### TRN27-D03
- 算法：实现/版本、EMA/sum、Nesterov、NS steps/coefficients/scaling、LR/decay order；
- 参数组：何为 weight、embedding/head/bias/norm、QKV/conv reshape、tied ownership、fallback optimizer；
- 数值：input/compute/accumulation dtype、epsilon、clipping、residual、NaN guard；
- 系统：batch/accumulation、all-reduce order、global/local shape、sharding、hardware、step time/state/peak。

缺失这些字段时，结果只能视为不完整配方观察。

## E. AI 迁移

### TRN27-E01
manifest 应含 framework/version/commit、parameter-name→owner/group/shape 映射、gradient reduction、buffer equation/clock/dtype、Nesterov、NS normalization/coefficients/steps/dtype、shape formula、base/adjusted LR、decay order、fallback optimizer、mixed precision、distributed layout、seed 和 checkpoint schema version。

### TRN27-E02
用单参数 toy 和固定 gradient：

- 设 $s\ne1$，手算 decay，断言 decay coefficient只含 base LR；
- 先建立非零 buffer，再传 None/zero，分别断言 state 是否不变/衰减；
- 对一次 buffer update 手算 Nesterov $M_t$；
- save state 后复制模型，reload，两边施加同一 gradient，比较 parameter/buffer；
- 对错误顺序建立 mutation tests，保证测试确实会失败。

### TRN27-E03
三组只改变 matrix partition，保持 data order、initial weights、global batch、token budget、base schedule、总调参预算和 fallback groups。每组分别搜索必要的 LR/scale，报告 per-block NS residual、actual update RMS/spectral norm、loss-vs-token/wall-clock、NS kernel time、communication、peak memory、seed/trial distribution。joint geometry 用 global fused shape；per-QKV/per-head 必须明确 block ownership 和 aggregate budget。

## 无提示重做

- [ ] 48 小时后从空白写出 current Muon 单步。
- [ ] 一周后用 scalar all-reduce 反例和 stacked-block 反例解释两种非交换性。

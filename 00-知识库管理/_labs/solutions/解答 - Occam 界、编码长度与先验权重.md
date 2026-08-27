---
type: solution
status: draft
area: [learning-theory/pac, description-length]
topic: "[[Occam 界、编码长度与先验权重]]"
exercise: "[[习题 - Occam 界、编码长度与先验权重]]"
prerequisites: ["[[有限假设类、Union Bound 与一致收敛]]", "[[数学归纳、递归与组合计数]]"]
related: ["[[PAC-Bayes Bound 的测度变换主线]]", "[[样本压缩方案与泛化]]"]
sources: ["[[S-1987-Blumer-Ehrenfeucht-Haussler-Warmuth-Occam-Razor]]", "[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]"]
created: 2026-08-20
updated: 2026-08-20
---

# 解答 - Occam 界、编码长度与先验权重

> [!warning] 使用边界
> prior、code language、decoder 与 compression protocol 必须在观察用于 guarantee 的 sample 前固定；否则短描述可能只是把 sample information 藏进编码器。

## A. 识别与复述

### LT-OCC-A01

若 $\pi(h)>0$、$\sum_h\pi(h)\le1$，则以至少 $1-\delta$ 概率，同时对所有 $h$：

$$
|R_S(h)-R_P(h)|
\le
\sqrt{\frac{\log(2/(\delta\pi(h)))}{2m}}.
$$

$\pi(h)$ 是 sample-independent failure-budget weight/prior preference；它不是由 theorem 保证的“$h$ 为真概率”，也不是 data-dependent posterior。

### LT-OCC-A02

prefix-free 指无 codeword 是另一个 codeword 的前缀。Kraft：

$$
\sum_h2^{-L(h)}\le1.
$$

所以可令 $\pi(h)=2^{-L(h)}$，把 bit length 转成合法的 sub-probability weights。

### LT-OCC-A03

Occam bound 是逐假设 weighted simultaneous certificate；MDL 是按 empirical fit 加 description penalty 的选择原则；sample compression 用少量训练 examples 和 side information 重建输出；Bayesian prior 属于 generative model；PAC-Bayes 用 data-dependent posterior 与 KL change-of-measure 控制 randomized/Gibbs risk。它们有压缩/先验类比，但对象与证明不相同。

## B. 手算与构造

### LT-OCC-B01

权重和

$$
0.5+0.25+0.125+0.0625=0.9375\le1,
$$

合法。半径

$$
\alpha_h=\sqrt{\frac{\log(2/(0.04\pi(h)))}{2000}}
$$

依次约为：

| $\pi(h)$ | radius |
|---:|---:|
| $0.5$ | $0.04799$ |
| $0.25$ | $0.05147$ |
| $0.125$ | $0.05473$ |
| $0.0625$ | $0.05781$ |

prior weight 越小，penalty 越大。

### LT-OCC-B02

$$
\begin{aligned}
\alpha
&=\sqrt{\frac{200\log2+\log40}{10000}}\\
&\approx\sqrt{0.0142318}\\
&\approx0.11930.
\end{aligned}
$$

### LT-OCC-B03

realizable consistent bound：

$$
R_P(h)
\le\frac{60\log2+\log20}{2000}
\approx0.02229.
$$

即在完整条件下，该 consistent hypothesis 的总体 0–1 错误率 certificate 约为 $2.23\%$。

## C. 推导与证明

### LT-OCC-C01

对每个 fixed $h$ 选择

$$
\alpha_h=\sqrt{\frac{\log(2/(\delta\pi(h)))}{2m}}.
$$

Hoeffding 给

$$
\Pr(|R_S(h)-R_P(h)|>\alpha_h)
\le\delta\pi(h).
$$

对可数 hypotheses 求并：

$$
\Pr(\exists h:\text{bound fails})
\le\sum_h\delta\pi(h)
\le\delta.
$$

取补集即得 simultaneous bound。可数 Union Bound 可由有限前缀并集单调极限严格化。

### LT-OCC-C02

长度 $L$ bit string 对应 $[0,1)$ 中长度 $2^{-L}$ 的 dyadic interval。若某 codeword 是另一者前缀，短串区间包含长串区间；prefix-free 保证所有对应区间互不相交。它们都包含在 $[0,1)$，故

$$
\sum_h2^{-L(h)}
=\sum_h|I_h|
\le1.
$$

非 prefix-free 时 intervals 可嵌套，长度和可超过 1，$2^{-L(h)}$ 不再自动构成合法 failure-budget weights；可改用显式 separators/self-delimiting encoding 后重新计算长度。

### LT-OCC-C03

在 weighted simultaneous event 上：

$$
\begin{aligned}
R_P(\widehat h)
&\le R_S(\widehat h)+\operatorname{rad}(\widehat h)\\
&\le R_S(h)+\operatorname{rad}(h)\\
&\le R_P(h)+2\operatorname{rad}(h)
\end{aligned}
$$

对每个 $h$ 成立。最后对 $h$ 取 infimum：

$$
R_P(\widehat h)
\le\inf_h[R_P(h)+2\operatorname{rad}(h)].
$$

第一、三步是 simultaneous deviations，中间是 penalized empirical optimality。

## D. 边界、反例与纠错

### LT-OCC-D01

看完 validation 后，定义一种新语言：把获胜模型编码为 `0`，其余模型用很长串。若直接代 $L=1$，就把“从所有模型和所有语言中搜索获胜者”的信息藏进 decoder/language。修复：预先冻结语言；或编码 language index/decoder 和 model；或用独立数据选择语言，再在新 sample 上使用 bound。

### LT-OCC-D02

int4 payload 约为 float32 的 $1/8$，不表示完整 code 也恰为 $1/8$：还需 scales、zero points、codebook、shapes、mask 与 decoder。量化改变函数，可能提高 empirical/population loss。gap penalty 近似按 $\sqrt L$，但 total risk bound 是 empirical risk 加 penalty；且 worst-case bound 可能两者都 vacuous。因此不能单凭 bit ratio 推断实际 gap 精确缩小 $\sqrt8$。

### LT-OCC-D03

参数个数不记录每个值所需 bits；非零数还需 indices；文件包含格式/压缩冗余；function description 可利用 weight sharing、symmetry 和程序生成。ReLU 两层可用 $W_1\mapsto cW_1,W_2\mapsto W_2/c$ 表示同一函数，却改变 parameter magnitudes/byte patterns。卷积核共享也使 function/program description 与展开 parameter matrix 大小显著不同。

## E. AI 迁移

### LT-OCC-E01

若 base model 在 evaluation sample 前固定，可把它作为 shared decoder；否则其描述也需支付。adapter code 至少含：family/architecture ID、每层是否有 adapter 的 mask、rank $r$、matrix shapes、quantization schema、quantized entries、scale/zero-point/codebook、merge rule、tokenizer/config version 和 decoder。所有字段须 self-delimiting；只数 $2dr$ values 不足。

### LT-OCC-E02

选择分数可写

$$
R_S(h)+\sqrt{\frac{L(h)\log2+\log(2/\delta)}{2m}}.
$$

经验 risk 相同会偏向短 rule list。但若真实 decision boundary 需要复杂交互，短规则可能有较大 approximation error；Occam 只控制 selection complexity，不保证短 class 含接近 Bayes 的 predictor。

### LT-OCC-E03

给 families 权重 $w_k$，$\sum_kw_k\le1$；family 内 $\sum_{h\in\mathcal H_k}\pi_k(h)\le1$。令

$$
\pi(h)=w_k\pi_k(h).
$$

则

$$
\sum_h\pi(h)
=\sum_kw_k\sum_{h\in\mathcal H_k}\pi_k(h)
\le\sum_kw_k\le1.
$$

penalty 复杂度分解：

$$
\log\frac1{\pi(h)}
=\log\frac1{w_k}
+\log\frac1{\pi_k(h)},
$$

分别支付 architecture-family selection 和 family 内 model selection。

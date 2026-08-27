---
type: concept
status: draft
area: [learning-theory/pac, description-length, machine-learning/model-selection]
aliases: [Occam Bound, Prior-Weighted Union Bound, MDL Generalization]
node_id: LT-14
prerequisites: ["[[不可知 PAC、ERM 与双侧一致收敛]]", "[[有限假设类、Union Bound 与一致收敛]]", "[[数学归纳、递归与组合计数]]", "[[命题、量词与逻辑等价]]"]
related: ["[[结构风险最小化与非一致可学习性]]", "[[样本压缩方案与泛化]]", "[[PAC-Bayes 先验、后验与数据依赖边界]]", "[[正则化、交叉验证与模型选择]]"]
sources: ["[[S-1987-Blumer-Ehrenfeucht-Haussler-Warmuth-Occam-Razor]]", "[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]", "[[S-1984-Valiant-Theory-of-the-Learnable]]"]
exercises: ["[[习题 - Occam 界、编码长度与先验权重]]"]
solutions: ["[[解答 - Occam 界、编码长度与先验权重]]"]
created: 2026-08-20
updated: 2026-08-23
---

# Occam 界、编码长度与先验权重

> [!abstract] 本章主问题
> 对有限或可数假设类，若在看评价样本前给每个 $h$ 指定权重 $\pi(h)>0$ 且 $\sum_h\pi(h)\le1$，那么把第 $h$ 个坏事件的失败预算设为 $\delta\pi(h)$，可同时得到
> $$
> |R_S(h)-R_P(h)|
> \le
> \sqrt{\frac{\log(2/\delta\pi(h))}{2m}}.
> $$
> prefix-free code 的 Kraft 不等式允许取 $\pi(h)=2^{-L(h)}$，于是复杂度由 code length $L(h)$ 决定。Occam 的数学内容不是“短的一定正确”，而是：在预先固定的编码/先验合同下，短假设消耗较少的 simultaneous-testing 预算。

> [!question] 初学者读完必须能回答
> 1. 为什么令第 $h$ 个失败预算为 $\delta\pi(h)$ 就能控制可数类？
> 2. Prior weight 为什么是证明预算，而不是 posterior correctness？
> 3. Prefix-free code 与 Kraft inequality 怎样产生 $\pi(h)=2^{-L(h)}$？
> 4. 描述长度如何进入 Hoeffding/Occam penalty？
> 5. 数据后选编码、遗漏 decoder 或把模型文件压缩等同于真理，分别错在哪里？

先用下图回答一个视觉问题：**怎样把有限类的均匀失败预算推广为可数类的非均匀预算，并把编码长度变成复杂度罚项？**

![[00-知识库管理/_assets/figures/learning-theory/fig-occam-code-prior-weight-v2.svg|880]]

> [!figure] 图 20.2.6｜Occam 界、编码长度与先验权重
> A 将总失败预算 $\delta$ 按预先固定的 $\pi(h)$ 非均匀切分；B 用 prefix-free code 和 Kraft inequality 把 $L(h)$ 转成权重 $2^{-L(h)}$ 与风险罚项；C 对照合法合同和常见越界。来源：独立绘制；理论接口参考 weighted Union Bound、Kraft inequality 与 Occam bounds；生成脚本：[[plot_pac_finite_class_v2.py]]；确定性证明地图，无随机种子。

**怎样读图。** 先在 A 检查 $\sum_h\pi(h)\le1$ 且权重不使用评价样本；再对第 $h$ 个坏事件分配 $\delta\pi(h)$ 并相加。B 中 prefix-free 不是装饰条件，它保证码长权重总和可控；代入尾界后，短码的 $\log(1/\pi(h))$ 较小。

**适用边界（图没有证明什么）。** 图不证明短模型更真实，也不把 Occam、MDL、Bayesian prior、sample compression 与 PAC-Bayes 视为同一定理。编码语言、decoder、数值精度和 metadata 都是合同的一部分；若在看到测试误差后设计 prior/code，必须支付数据依赖代价或使用合法的 data-dependent-prior 理论。

## 一、学习目标

1. 从 weighted Union Bound 推导 countable-class simultaneous bound；
2. 理解 prior weight 是失败预算，而不是后验正确概率；
3. 证明 prefix-free code 的 Kraft inequality；
4. 把 $\pi(h)=2^{-L(h)}$ 代入得到 description-length penalty；
5. 推导 realizable consistent Occam 的 $1/m$ risk certificate；
6. 推导 penalized ERM/MDL 的 oracle inequality；
7. 区分有限类统一 penalty 与非均匀 penalty；
8. 识别 data-dependent prior/code language 的双重使用问题；
9. 区分 Occam bound、MDL、sample compression、Bayesian prior 与 PAC-Bayes；
10. 审计 pruning、quantization 与 model-file compression 是否真的对应 theorem 中的 code。

## 二、从均匀预算到非均匀预算

有限类证明通常给每个假设相同失败预算

$$
\delta_h=\frac\delta M.
$$

但候选可能有明显层级：简单规则应比巨大 lookup table 获得较小 penalty。令 $\mathcal H$ 有限或可数，并预先指定

$$
\pi:\mathcal H\to(0,1],
\qquad
\sum_{h\in\mathcal H}\pi(h)\le1.
$$

分配

$$
\delta_h=\delta\pi(h).
$$

因为

$$
\sum_h\delta_h
=\delta\sum_h\pi(h)
\le\delta,
$$

所有 individual failure budgets 的总和仍受控。

> [!important] $\pi$ 的逻辑角色
> 它在样本前固定，用来决定 simultaneous guarantee 的预算。它可以表达 prior preference，但 theorem 并没有声称 $\pi(h)$ 是“$h$ 为真的概率”。

## 三、weighted Hoeffding bound

对每个预先固定的 $h$，Hoeffding 给出

$$
\Pr\left(
|R_S(h)-R_P(h)|>\alpha_h
\right)
\le2e^{-2m\alpha_h^2}.
$$

令右端等于 $\delta\pi(h)$：

$$
2e^{-2m\alpha_h^2}
=\delta\pi(h).
$$

反解：

$$
\boxed{
\alpha_h
=\sqrt{
\frac{
\log\frac{2}{\delta\pi(h)}
}{2m}
}.
}
$$

定义第 $h$ 个坏事件

$$
B_h=\{|R_S(h)-R_P(h)|>\alpha_h\}.
$$

对有限或可数并集使用 Union Bound：

$$
\Pr\left(\bigcup_hB_h\right)
\le\sum_h\Pr(B_h)
\le\delta\sum_h\pi(h)
\le\delta.
$$

所以以至少 $1-\delta$ 的概率，**同时对所有** $h\in\mathcal H$：

$$
\boxed{
|R_S(h)-R_P(h)|
\le
\sqrt{
\frac{
\log(1/\pi(h))+\log(2/\delta)
}{2m}
}.
}
$$

## 四、有限类是 special case

若 $|\mathcal H|=M$，取均匀权重

$$
\pi(h)=\frac1M,
$$

则

$$
\log\frac1{\pi(h)}=\log M,
$$

恢复 LT-11：

$$
\sqrt{\frac{\log M+\log(2/\delta)}{2m}}
=\sqrt{\frac{\log(2M/\delta)}{2m}}.
$$

所以 Occam bound 不是与 finite-class bound 无关的新魔法，而是把 uniform counting 改成 prior-weighted counting。

## 五、prefix-free code

设编码函数

$$
c:\mathcal H\to\{0,1\}^*,
$$

并记 code length

$$
L(h)=|c(h)|.
$$

若没有一个 codeword 是另一个 codeword 的前缀，则称编码 prefix-free。

### 5.1 为什么需要 prefix-free

若 codewords 可互为前缀，串联读取时可能无法判断一个描述何时结束。例如 `0` 与 `01` 同时出现时，读到 `0` 尚不能判断是否结束。prefix-free 使码字在 binary tree 中对应互不祖先的 leaves。

### 5.2 Kraft inequality

对 prefix-free 二进制码：

$$
\boxed{
\sum_{h\in\mathcal H}2^{-L(h)}\le1.
}
$$

#### 二叉区间证明

把每个长度为 $L$ 的 bit string 对应到 $[0,1)$ 中长度 $2^{-L}$ 的 dyadic interval：

- `0` 对应 $[0,1/2)$；
- `10` 对应 $[1/2,3/4)$；
- 一般 codeword 对应 binary prefix 指定的区间。

若一个 codeword 是另一个的前缀，短码区间包含长码区间。prefix-free 排除了这种包含，因此所有对应区间互不相交。它们都在 $[0,1)$ 内，所以长度总和至多 1。

### 5.3 从 code 到 prior weight

令

$$
\pi(h)=2^{-L(h)}.
$$

Kraft 保证 $\sum_h\pi(h)\le1$，于是可代入 weighted Union Bound。

## 六、description-length bound

代入 $\pi(h)=2^{-L(h)}$：

$$
\log\frac1{\pi(h)}
=L(h)\log2.
$$

所以以至少 $1-\delta$ 的概率，同时对所有 $h$：

$$
\boxed{
|R_S(h)-R_P(h)|
\le
\sqrt{
\frac{L(h)\log2+\log(2/\delta)}{2m}
}.
}
$$

因为 $\log2<1$，可写更简洁但稍松的版本：

$$
\boxed{
R_P(h)
\le R_S(h)
+\sqrt{
\frac{L(h)+\log(2/\delta)}{2m}
}.
}
$$

这里 $L(h)$ 以 bits 计，而概率推导使用自然对数；$\log2$ 正是换底常数。

## 七、realizable consistent Occam 界

0–1 realizable setting 下，还能使用 LT-12 的零错生存机制得到 $1/m$ 而非 $1/\sqrt m$ 的 risk certificate。

对每个 $h$ 定义 threshold

$$
r_h
=\frac{
\log(1/\pi(h))+\log(1/\delta)
}{m}.
$$

若 $R_P(h)>r_h$，它在 $m$ 个样本上零错的概率满足

$$
\Pr(R_S(h)=0)
\le e^{-mR_P(h)}
<e^{-mr_h}
=\delta\pi(h).
$$

对全部 $h$ 求并集，得：以至少 $1-\delta$ 的概率，所有 consistent hypotheses 同时满足

$$
\boxed{
R_P(h)
\le
\frac{
\log(1/\pi(h))+\log(1/\delta)
}{m}.
}
$$

prefix-free 形式：

$$
\boxed{
R_P(h)
\le
\frac{L(h)\log2+\log(1/\delta)}{m}
\qquad\text{for every consistent }h.
}
$$

它说明同样零训练错误时，短描述 hypothesis 获得更小 population-risk certificate。

## 八、从 bound 到 MDL / penalized ERM

定义 data-independent penalty

$$
\operatorname{rad}_m(h)
=\sqrt{
\frac{\log(1/\pi(h))+\log(2/\delta)}{2m}
}.
$$

考虑选择规则

$$
\widehat h_S
\in\arg\min_{h\in\mathcal H}
\left{
R_S(h)+\operatorname{rad}_m(h)
\right}.
$$

在 simultaneous event 上，对任意 comparator $h$：

$$
\begin{aligned}
R_P(\widehat h_S)
&\le R_S(\widehat h_S)+\operatorname{rad}_m(\widehat h_S)\\
&\le R_S(h)+\operatorname{rad}_m(h)\\
&\le R_P(h)+2\operatorname{rad}_m(h).
\end{aligned}
$$

所以得到 oracle inequality：

$$
\boxed{
R_P(\widehat h_S)
\le
\inf_{h\in\mathcal H}
\left{
R_P(h)+2\operatorname{rad}_m(h)
\right}.
}
$$

选择器自动平衡 empirical fit 与 description/prior complexity。这是 Structural Risk Minimization 与 MDL 风格规则的最简单形式。

### 8.1 approximate score minimization

若算法只把 penalized empirical score 优化到 $\rho$：

$$
R_S(\widetilde h)+\operatorname{rad}_m(\widetilde h)
\le
\inf_h[R_S(h)+\operatorname{rad}_m(h)]+\rho,
$$

则 oracle bound 右端再加 $\rho$。

## 九、prior weight 不等于 Bayesian posterior

weighted bound 中 $\pi(h)$：

- 必须在观察用于 theorem 的 sample 前固定；
- 用于分配 frequentist failure probability；
- 不要求 data-generating process 先从 $\pi$ 抽一个真实 $h$；
- theorem 对每个允许 $P$ 仍成立。

Bayesian prior 则是 generative model 的组成部分，并通过 likelihood 得 posterior。相同符号和“prior”直觉不意味着解释完全相同。

## 十、与 PAC-Bayes 的接口

若 posterior $Q$ 是 point mass $\delta_h$，则

$$
\mathrm{KL}(\delta_h\|\pi)
=\log\frac1{\pi(h)}.
$$

这说明 point-hypothesis Occam penalty 与 PAC-Bayes KL complexity 有形式连接。但完整 PAC-Bayes：

- 控制 randomized/Gibbs predictor 的 posterior-averaged risk；
- 允许数据依赖 posterior；
- 使用 change-of-measure 而非逐点 Union Bound；
- 对连续 parameter distributions 仍有意义。

因此 Occam 是很好的入口，不是 PAC-Bayes 的完整替代。

## 十一、编码语言不是中性的

同一个函数可以在一种语言中很短、另一种语言中很长。若允许看过数据后专门发明语言，让最终模型获得 1-bit code，那么 complexity 已藏进“语言选择”本身。

合法路线包括：

1. 在评价样本前冻结编码器/解码器；
2. 用独立数据选择 code/prior；
3. 把语言 index 也编码进去；
4. 对 data-dependent prior 使用专门 PAC-Bayes/holdout 工具。

> [!warning] 不能免费选择最有利坐标系
> parameter norm、压缩率、稀疏度与 sharpness 都可能随重参数化变化。理论 complexity 必须说明 representation contract。

## 十二、prefix-free 的实际构造

### 12.1 固定长度类

若所有 $M$ 个 hypothesis 都用长度 $\lceil\log_2M\rceil$ 编码，恢复近似均匀 finite-class penalty。

### 12.2 先编码结构，再编码参数

可用 self-delimiting code：

$$
L(h)=L(\text{architecture})
+L(\text{quantization schema})
+L(\text{weights}\mid\text{schema}).
$$

每个字段必须可唯一解析，不能只数 weight payload 而忽略模型结构、字典和 scale metadata。

### 12.3 分层 class

若

$$
\mathcal H=\bigcup_{k\ge1}\mathcal H_k,
$$

先给层 $k$ 权重 $w_k$，再在层内给 $h$ 条件权重 $\pi_k(h)$：

$$
\pi(h)=w_k\pi_k(h).
$$

complexity 分解成

$$
\log\frac1{\pi(h)}
=\log\frac1{w_k}
+\log\frac1{\pi_k(h)}.
$$

这正对应“先付模型阶数，再付层内参数”的 SRM 账本。

## 十三、AI compression 场景审计

### 13.1 pruning

只报告非零 weight 数量不够。还需编码：

- mask/indices；
- quantized values；
- layer shapes；
- codebook 与 scales；
- decoder/program。

### 13.2 quantization

从 float32 变成 int4 可降低 payload bits，但会改变函数与 empirical risk。完整 bound 必须同时记 approximation/quantization loss 与 code penalty。

### 13.3 LoRA

低秩 adapters 可能有较短 task-specific description，但 base model 由谁承担？若 base model 在下游 evaluation sample 前固定，可把它视为 shared decoder；若 base 也用同一 sample 训练，不能免费忽略其信息。

### 13.4 model file gzip

通用 compressor 输出长度可作为一个合法 code 的候选，但：

- 必须连同 decompressor 固定；
- 浮点文件包含格式冗余；
- gzip length 未必对应 function-level effective complexity；
- 文件短与 bound 数值非空仍是两回事。

## 十四、与 sample compression 的差别

description-length Occam 说 output 可用较少 bits 描述；sample compression 说 classifier 可由训练集中的少数 examples 加 side information 重建。后者的计数依赖

$$
\binom{m}{k}
$$

及 side-message 长度，常产生不同形式的 generalization bound。二者都利用“输出没有携带任意多选择信息”，但证书对象不同。

## 十五、一个数值例子

设两模型 empirical risk 都是 $0.08$，样本量 $m=5000$、$\delta=0.05$：

- $h_1$ code length $L_1=100$ bits；
- $h_2$ code length $L_2=10000$ bits。

用精确 $L\log2$ 形式：

$$
\operatorname{rad}(h_1)
=\sqrt{\frac{100\log2+\log40}{10000}}
\approx0.0855,
$$

$$
\operatorname{rad}(h_2)
=\sqrt{\frac{10000\log2+\log40}{10000}}
\approx0.833.
$$

第二个 certificate 几乎 vacuous。这不证明 $h_2$ 实际泛化差，只说明当前 worst-case code-based evidence 无法给出紧保证。

## 十六、常见误解

> [!failure] “短模型更真实”
> theorem 只给固定语言下的 risk upper bound，不给本体论真理排序。

> [!failure] “训练后选择最短压缩器仍然免费”
> 选择 compressor/language 也使用了数据，必须预先固定或编码/校正。

> [!failure] “$\pi(h)$ 是模型正确的 posterior probability”
> 它首先是 simultaneous failure budget；Bayesian 解释需额外 generative assumptions。

> [!failure] “参数少就等于 code 短”
> 实值参数需精度、范围、结构和 decoder；连续值不能用有限 bits 无损表示。

> [!failure] “压缩后 accuracy 不变，所以已经证明泛化”
> 还需独立 sampling、code contract、simultaneous theorem 和 target distribution 条件。

## 十七、证明模板

1. 固定可数 $\mathcal H$ 与 sample-independent $\pi$；
2. 检查 $\sum_h\pi(h)\le1$；
3. 给第 $h$ 个 event 预算 $\delta\pi(h)$；
4. 反解 fixed-$h$ tail；
5. 对可数 events Union Bound；
6. 若用 code，先证明 prefix-free/Kraft；
7. 区分 bounded-loss 双侧 bound 与 realizable zero-error bound；
8. 若用 penalized selection，建立 simultaneous event 后推 oracle inequality；
9. 把 language/decoder metadata 计入 code；
10. 检查 prior/code 是否偷看同一 evaluation sample。

## 十八、本节边界与来源说明

- Occam algorithm 的历史连接来自 Blumer 等 1987；
- weighted union、Kraft 与显式 description-length bound 以标准教材现代表述为准；
- 本节不把任意哲学简约原则、gzip 长度或 Bayesian posterior 与 theorem 自动等同。

## 十九、掌握检查

- [ ] 我能推导 weighted simultaneous bound；
- [ ] 我能解释 $\pi(h)$ 的失败预算含义；
- [ ] 我能证明 Kraft inequality；
- [ ] 我能正确处理 bits 与 nats；
- [ ] 我能推导 realizable consistent Occam bound；
- [ ] 我能推导 penalized ERM oracle inequality；
- [ ] 我能区分 Occam、MDL、sample compression 与 PAC-Bayes；
- [ ] 我能审计 data-dependent code/prior 和实际模型压缩 metadata。

## 二十、进一步连接

- [[结构风险最小化与非一致可学习性]]：把 countable layers 与 layer-specific complexity 系统化；
- [[样本压缩方案与泛化]]：把短 bit description 换成少量训练样本证书；
- [[PAC-Bayes Bound 的测度变换主线]]：从 point hypothesis penalty 进入 posterior/KL；
- [[正则化、交叉验证与模型选择]]：比较 theoretical penalty 与 validation-based selection。

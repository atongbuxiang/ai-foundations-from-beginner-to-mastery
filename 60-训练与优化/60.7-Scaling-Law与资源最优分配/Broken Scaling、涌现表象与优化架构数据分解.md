---
type: research-map
status: verified
area: [training, scaling-laws, emergence, diagnostics]
node_id: TRN-55
aliases: [Broken Neural Scaling Laws, Emergent Abilities, Scaling Kinks]
prerequisites: ["[[经验 Scaling Law、幂律拟合与不可约项]]", "[[Kaplan 参数数据律、联合拟合与有限区间]]", "[[统计模型、估计量与偏差方差]]"]
related: ["[[插值、双下降与经典偏差方差边界]]", "[[模型可辨识性、选择与 Misspecification]]", "[[Scaling 实验设计、外推不确定性与证据地图]]"]
sources: ["[[S-2022-Caballero-Broken-Neural-Scaling-Laws]]", "[[S-2023-Schaeffer-Emergent-Mirage]]", "[[S-2023-Su-9607-量子化假设与尺度定律]]", "[[S-2026-Su-11833-解构ScalingLaw]]", "[[S-2024-Porian-Resolving-Compute-Optimal-Scaling]]"]
exercises: ["[[习题 - Broken Scaling、涌现表象与优化架构数据分解]]"]
solutions: ["[[解答 - Broken Scaling、涌现表象与优化架构数据分解]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-broken-scaling-emergence-diagnosis-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Broken Scaling、涌现表象与优化架构数据分解

> [!abstract] 一句话结论
> 曲线出现 kink、斜率变化或“突然会了”，至少有六类竞争解释：真实机制切换、优化不足、架构/参数口径变化、数据/评测分布变化、非线性离散指标和有限样本噪声。Broken power law 可以描述转折，却不能仅凭更好拟合证明转折的机制。

## 一、先定义 Local Slope

对 excess loss $R(x)=L(x)-E$，定义

$$
s(x)=\frac{d\log R}{d\log x}.
\tag{1}
$$

单一 power law 有常数 $s(x)=-\alpha$。若 $s(x)$ 随尺度显著改变，称观察到 slope drift 或 broken scaling 候选。

“Broken”是曲线性质，不先等于：

- phase transition；
- emergent capability；
- 新算法突然启动；
- 测量错误。

机制需要额外干预。

## 二、一个平滑 Break 模型

教学上可用两段平滑插值：

$$
R(x)
=A x^{-\alpha_1}
\left[
1+\left(\frac{x}{x_b}\right)^k
\right]^{-(\alpha_2-\alpha_1)/k}.
\tag{2}
$$

当 $x\ll x_b$，局部 slope 接近 $-\alpha_1$；当 $x\gg x_b$，接近 $-\alpha_2$；$k$ 控制转折锐度。

[[S-2022-Caballero-Broken-Neural-Scaling-Laws]] 提出更一般的 smoothly broken power-law 函数族，可表达多 breakpoint、延迟转折与非单调形态。

但模型更灵活意味着：

- 参数更多；
- breakpoint 与 slope 高相关；
- 小窗口更容易过拟合；
- 必须用 held-out scales 比较，而不是只看训练残差。

## 三、六类竞争解释

### H1：真实学习机制/表示变化

模型容量跨过任务所需结构，底层连续指标也发生可重复 kink。

### H2：Optimization regime

大模型没有调好 LR/warmup/batch 或小模型训练不充分。[[S-2024-Porian-Resolving-Compute-Optimal-Scaling]] 说明这些因素足以改变 compute-optimal slope。

### H3：Architecture/counting change

depth/width/head/context、MoE sparsity、embedding 占比或 parameterization 在某尺度改变。

### H4：Data regime

mixture、quality、duplication、tokenizer、contamination 或 evaluation distribution 在某尺度改变。

### H5：Metric transformation

底层概率平滑，但 exact match、argmax、threshold 把它显示成跳变。

### H6：Finite-sample/selection

小模型成功率低且测试集小，观测全为 0；或研究者事后挑选出现转折的任务。

## 四、平滑能力怎样变成“突然会了”

设每个子步骤正确概率平滑增长：

$$
p(x)=\sigma(a\log x-b).
\tag{3}
$$

长度 $m$ 的 exact-match 成功率是

$$
P_{\rm exact}(x)=p(x)^m.
\tag{4}
$$

当 $m$ 大时，$p$ 从 0.8 到 0.9 的平滑变化会让

$$
0.8^{20}\approx0.012,
\qquad
0.9^{20}\approx0.122,
\tag{5}
$$

提高约 10 倍。若再用有限样本和 0/1 grade，曲线看起来可近似“突然出现”。

[[S-2023-Schaeffer-Emergent-Mirage]] 在语言与视觉实验中展示：改变为连续/线性指标可以削弱许多表面 emergence。

正确结论是“metric-induced emergence 是重要替代解释”，不是“所有 emergence 都不存在”。

## 五、有限样本的零成功错觉

真实成功率为 $p$，测试样本数 $n$。观测零成功概率是

$$
\Pr(K=0)=(1-p)^n.
\tag{6}
$$

若 $p=0.01,n=50$：

$$
\Pr(K=0)=0.99^{50}\approx0.605.
\tag{7}
$$

超过一半实验会显示“完全不会”。规模稍增到 $p=0.05$ 时，

$$
0.95^{50}\approx0.077,
\tag{8}
$$

突然很可能观察到成功。这是检测功效变化，不一定是能力从无到有。

## 六、科学空间的三重分解

[[S-2026-Su-11833-解构ScalingLaw]] 组织：

$$
L(\mathcal E\mid\mathcal D,\mathcal A,\mathcal O)
=F_{\rm data}+F_{\rm opt}+F_{\rm arch}+L_{\rm ideal}.
\tag{9}
$$

它的价值在于把 kink 假说分派给：

- data：mixture、size、multi-epoch、target mismatch；
- optimizer：LR、batch、steps、optimizer family；
- architecture：$N$、width/depth、context、结构变化。

但真实 loss 不一定可严格加性分解，因为存在交互：

$$
L=F_{\rm data}+F_{\rm opt}+F_{\rm arch}
+F_{\rm data\times arch}
+F_{\rm opt\times arch}
+\cdots.
\tag{10}
$$

课程把三重奏当诊断坐标，不当唯一生成模型。

## 七、量子化/Tail 解释的证据身份

[[S-2023-Su-9607-量子化假设与尺度定律]] 假设能力单元的难度/频率具有 tail，规模增大逐步覆盖更多能力，从 tail sum 导出幂律。

若能力分布有多个 tail regime，可能导出 broken slope；若某一 benchmark 只在一组能力全部具备后得分，可能产生 threshold。

然而需要验证：

- 能力单元怎样定义；
- 是否独立/可加；
- 难度 tail 是否随模型 family 不变；
- optimizer/data 如何改变学习阈值；
- 指标是否忠实测量能力。

条件推导不能反向证明假设真实。

## 八、Kink 诊断的干预矩阵

| 观察 | 首要干预 |
|---|---|
| loss kink 与 optimizer state 同时变 | retune LR/warmup/batch；固定训练时域 |
| total parameter kink，non-embedding 不 kink | 重算参数口径 |
| exact match kink，token log-prob 平滑 | metric intervention |
| 只在一个 benchmark 出现 | 扩大样本、检查 contamination/threshold |
| mixture 更新处出现 | 固定 data snapshot 与 sampling |
| width path 出现、depth path 不出现 | 架构轴 factorial |
| 多 seeds breakpoint 不稳定 | 估计 breakpoint interval/否定 sharp claim |
| 多指标、多协议都在同尺度 kink | 增强真实 regime-change 假说，但仍需机制实验 |

## 九、如何比较 Single 与 Broken Law

不能只比较 in-sample $R^2$。至少报告：

1. calibration fit；
2. validation function selection；
3. held-out larger-scale prediction；
4. AIC/BIC 或复杂度惩罚作为辅助；
5. breakpoint/slope bootstrap interval；
6. leave-one-scale-out sensitivity；
7. 对 optimizer/data/metric 干预后的 breakpoint 是否保持。

若 broken model 只在加入 target scale 后才显示 breakpoint，它是事后描述，不是预测。

## 十、图：一个 Kink，六条诊断路径

先看图回答：左侧平滑 latent probability 为什么在 exact match 下变陡？右侧哪个证据能区分 metric artifact 与优化不足？

![[00-知识库管理/_assets/figures/training-optimization/fig-broken-scaling-emergence-diagnosis-v1.svg|900]]

> [!figure] 图 TRN-55-01　Broken curve、metric transform 与竞争解释
> 来源：课程原创教材图；左栏把平滑 $p(x)$ 映射为 $p(x)^m$；中栏显示 single/broken local slope；右栏以优化、架构、数据、指标、采样、机制六分支组织干预。概念依据：[[S-2022-Caballero-Broken-Neural-Scaling-Laws]]、[[S-2023-Schaeffer-Emergent-Mirage]]、[[S-2026-Su-11833-解构ScalingLaw]]。

**怎样读图**：从 observation 出发，不先给 kink 命名；每条假说都配一个改变该因素而保持其他项的干预。

**图没有证明什么**：图没有断言所有 kink 都是伪影，也没有证明三重 gap 严格可加；它是竞争解释地图。

## 十一、允许措辞

低证据：

> 在观测窗口和当前 metric 下，broken function 的插值残差更小。

更强：

> 在预注册 held-out scales 上，broken function 改善预测，breakpoint 在 seeds/窗口下稳定。

机制级：

> metric、optimizer、data 与 parameter-count interventions 后 kink 仍存在，并与预注册 representation mediator 同时变化。

只有第三层才开始支持具体机制，仍不等于跨架构普遍定理。

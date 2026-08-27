---
type: theorem
status: draft
area: [learning-theory/self-supervised-learning, masked-prediction, teacher-student, target-generation]
aliases: [Masked Prediction Contract, Self-Supervised Target Generation, Teacher Student Theory]
node_id: LT-59
prerequisites: ["[[表示坍缩、非坍缩与可辨识边界]]", "[[条件概率、全概率与 Bayes 公式]]", "[[交叉熵与 KL 散度]]", "[[自动微分：前向、反向与高阶模式]]"]
related: ["[[Linear Probe、Fine-Tuning 与迁移评估]]", "[[变分推断、ELBO 与证据分解]]", "[[生成模型 MOC]]"]
sources: ["[[S-2019-Devlin-BERT]]", "[[S-2022-He-MAE]]", "[[S-2017-Tarvainen-Valpola-Mean-Teacher]]", "[[S-2020-Grill-BYOL]]", "[[S-2021-Caron-DINO]]", "[[S-2021-Chen-He-SimSiam]]"]
exercises: ["[[习题 - 遮蔽预测、Teacher–Student 与自监督目标]]"]
solutions: ["[[解答 - 遮蔽预测、Teacher–Student 与自监督目标]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-masked-teacher-targets-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# 遮蔽预测、Teacher–Student 与自监督目标

> [!abstract] 本章主问题
> 自监督不等于“没有监督信号”，而是 target 由数据变换、输入未观测部分、另一个模态、聚类器或历史模型自动生成。必须逐项说明：谁看见什么、谁生成 target、target 是否 stop-gradient、损失在哪些位置计算，以及 target 随训练如何变化。

## 一、学习目标

完成本章后，应能：

1. 用 clean object、corruption、visible context、target 与 prediction space 写自监督合同；
2. 推导 log loss 的 population optimum 是条件分布、square loss 的 optimum 是条件均值；
3. 区分 token、pixel、latent、cluster 与 teacher-distribution targets；
4. 比较 BERT-style masking 与 MAE visible-only encoding；
5. 写出 Mean Teacher、BYOL 与 DINO 的参数/target 更新；
6. 解释 stop-gradient、EMA、temperature、centering 与 sharpening 的不同作用；
7. 识别 leakage、shortcut、self-confirmation 与 target collapse；
8. 把 pretext loss、representation quality 与 downstream risk 分账。

## 二、统一 Target-Generation Contract

clean object $X\sim P_X$，随机 mask/corruption $M\sim Q(\cdot\mid X)$。模型实际看见

$$
\widetilde X=C(X,M,\xi),
$$

target 由

$$
T=\mathcal T(X,M,\omega)
$$

生成，其中 $\omega$ 可为空、可为 tokenizer/quantizer，也可为 teacher 参数。student prediction 为

$$
q_\theta(\cdot\mid \widetilde X,M),
$$

population pretext risk：

$$
R_{\rm pre}(\theta)
=
E_{X,M,\xi,\omega}
\bigl[\ell(q_\theta(\widetilde X,M),T)\bigr].
$$

这个合同必须补充：loss 只在 masked positions 还是全位置、target 是否由 student history 产生、teacher branch 是否反传、mask pattern 与 source split。

## 三、Log Loss 学到什么

离散 target $T$，给定 visible context $V=(\widetilde X,M)$，任意预测分布 $q(t\mid V)$ 的 conditional cross-entropy 为

$$
E[-\log q(T\mid V)\mid V]
=
H(P_{T\mid V})
+
D_{\rm KL}(P_{T\mid V}\|q_{T\mid V}).
$$

因此 unrestricted population optimum 是

$$
\boxed{q^*(t\mid V)=P(T=t\mid V).}
$$

这证明 masked token prediction 在理想条件下估计 conditional law；它没有证明 hidden state 是所有下游任务的 sufficient statistic。

## 四、Square Loss 学到什么

连续 target $T\in\mathbb R^p$，预测 $a(V)$。由条件平方损失分解：

$$
E[\|T-a(V)\|^2\mid V]
=
\operatorname{tr}\operatorname{Cov}(T\mid V)
+
\|E[T\mid V]-a(V)\|^2.
$$

所以

$$
\boxed{a^*(V)=E[T\mid V].}
$$

若条件分布多峰，均值可能是“模糊像素”或不存在于数据流形的折中；这不是 optimizer 失败，而是 square-loss estimand。

## 五、Mask Law 决定任务难度与可识别信息

mask $M$ 需要声明：

- 独立 token/patch、contiguous span/block 还是结构化 region；
- mask rate 与长度分布；
- mask 是否依赖内容；
- replacement 是 special token、random token、zero、noise 还是 removal；
- positional information 是否仍暴露；
- loss denominator 是 masked count、all tokens 还是 batch size。

mask 太少时，任务可由局部 copying/texture 完成；太多时，conditional entropy 高，target 接近不可预测。最优比例依赖模态冗余、decoder capacity 与下游任务。

## 六、BERT 式 Masked Language Modeling

给 token sequence $X_{1:L}$，选择 mask set $M$，objective 典型写为

$$
L_{\rm MLM}
=
-\sum_{i\in M}\log q_\theta(X_i\mid \widetilde X,M).
$$

BERT 的经典 recipe 对选中位置混用 `[MASK]`、随机 token 与 unchanged token，以缓解 special-mask 与 downstream clean input 的不匹配。需要区分：

1. pseudo-likelihood 式条件预测不是完整 joint likelihood；
2. tokenizer 决定 target alphabet 与难度；
3. bidirectional context 可能泄露局部 shortcut；
4. only-masked normalization 会让不同 mask count 的 batch 权重不同；
5. token recovery 高不等于 reasoning、truthfulness 或 long-horizon generation 高。

## 七、MAE 式视觉遮蔽

设 image patches $X_{1:L}$，visible set $V=M^c$。MAE 类结构：

$$
H_V=E_\theta(X_V),
$$

encoder 只处理 visible patches；decoder 接收 $H_V$、mask tokens 与 positions，输出

$$
\widehat X_M=D_\phi(H_V,M).
$$

masked reconstruction loss：

$$
L_{\rm MAE}
=
\frac1{|M|}\sum_{i\in M}\|X_i-\widehat X_i\|^2.
$$

高 mask ratio 同时：减少 encoder compute、降低局部 redundancy shortcut、提高 reconstruction ambiguity。decoder 过强也可能吸收任务，使 encoder representation 并不理想。

## 八、Target 类型决定归纳偏置

| target | loss空间 | 直接鼓励 | 主要风险 |
|---|---|---|---|
| raw token | vocabulary CE | conditional symbolic prediction | tokenizer/mask mismatch |
| pixel/patch | Euclidean/normalized pixels | local structure与appearance | conditional mean/低层纹理 |
| latent feature | feature distance | teacher-defined invariance | teacher bias/collapse |
| discrete code | codebook CE | quantized semantics | codebook collapse/commitment |
| cluster assignment | CE/OT | prototype separation | balanced-cluster artifact |
| teacher distribution | CE/KL | historical ensemble consistency | confirmation error |
| other modality | contrastive/generative | cross-modal shared signal | pairing/noise/shortcut |

“更抽象 target 更语义”不是普遍定理；target generator 自己的偏差会传给 student。

## 九、Teacher–Student 的两个时间尺度

student 参数通过梯度：

$$
\theta_{t+1}
=
\theta_t-\eta_t\widehat g_t.
$$

teacher 参数通过 EMA：

$$
\xi_{t+1}
=
\tau\xi_t+(1-\tau)\theta_{t+1}.
$$

展开得到

$$
\xi_t
=
(1-\tau)\sum_{k=0}^{t-1}\tau^k\theta_{t-k}
+\tau^t\xi_0.
$$

所以 teacher 是 student history 的指数加权低通平均；有效记忆尺度约为 $1/(1-\tau)$ steps。它减少短期抖动，却引入 lag，并不保证 target 无偏。

## 十、Mean Teacher：Label Loss 与 Consistency 分开

对 labeled $(X,Y)$ 与 unlabeled $U$，典型目标：

$$
L
=
L_{\rm sup}(f_\theta(\widetilde X),Y)
+
\lambda_t
D\bigl(f_\theta(\widetilde U_s),
\operatorname{sg}(f_\xi(\widetilde U_t))\bigr).
$$

必须声明 labeled/unlabeled sampling ratio、两侧 perturbations、ramp-up $\lambda_t$、teacher eval mode 与 confidence filtering。若 augmentation 改标签，consistency 会强化错误。

## 十一、BYOL：预测 Target Representation

online encoder/projector/predictor 产生

$$
p_\theta(z_\theta(X_1)),
$$

target encoder/projector 产生

$$
\operatorname{sg}(z_\xi(X_2)).
$$

对称交换 views 后优化 normalized representation distance。其 target 既不是 raw data，也不是 fixed label，而是 EMA teacher 的当前 latent；predictor、stop-gradient 与 EMA 都属于 objective dynamics。

## 十二、DINO：Teacher Distribution、Centering 与 Sharpening

teacher logits $u_\xi(x)$ 经 center $c$ 与温度 $\tau_t$：

$$
p_t(k\mid x)
=
\frac{\exp((u_{\xi,k}(x)-c_k)/\tau_t)}
{\sum_j\exp((u_{\xi,j}(x)-c_j)/\tau_t)}.
$$

student distribution用温度 $\tau_s$，以 cross-entropy 匹配不同 crops。这里：

- sharpening（小 $\tau_t$）降低 target entropy，避免 uniform target；
- centering 抑制某一 prototype 长期独占；
- 两者过强也可能产生 one-hot instability 或过度均衡；
- center、teacher 与 batch/global statistics 的更新次序属于可复现合同。

## 十三、Stop-Gradient 与 Target Leakage

若 target branch 也反传，双方可能共同移动以降低 loss；若 target 直接含 prediction position 的 clean value，任务可能泄漏。需要检查：

1. target 是否看见 student 不该看的 token/label；
2. teacher 是否由 test/validation data 更新；
3. mask metadata 是否暴露答案；
4. multi-crop pairing 是否跨 source identity；
5. batch normalization 是否让同一样本另一 view 泄漏；
6. pseudo-label threshold 是否在 test 上选择。

## 十四、自举错误与 Confirmation Bias

设 teacher target error rate 为 $e_t$。若 student 只模仿 teacher 且没有独立监督/结构约束，则最优 student 可复制同样错误。要获得改善，需要额外来源：

- augmentation consistency 下的正确不变性；
- temporal averaging 降噪；
- independent labeled loss；
- cross-view/cross-modal complementary information；
- entropy/balance/covariance constraints；
- model/optimization inductive bias。

“student 超过 teacher”是可能的算法现象，不是从 imitation loss 单独推出的定理。

## 十五、图：Target 从哪里来

先看图回答：masked prediction 与 teacher–student consistency 看似都是“预测未知量”，但未知量分别由 clean data、decoder target 与历史模型中的哪一部分生成？

![[00-知识库管理/_assets/figures/learning-theory/fig-masked-teacher-targets-v2.svg|900]]

> [!figure] 图 20.7-07　Corruption–target 合同与四类自监督目标
> 左栏分开 clean object、mask/corruption、visible input 与 target；中栏比较 token/pixel masked prediction 和 latent/teacher targets；右栏给出 stop-gradient、EMA、temperature/centering 与 leakage/confirmation 审计。来源：依据 Devlin et al.、He et al.、Tarvainen–Valpola、Grill et al. 与 Caron et al. 独立绘制；确定性 SVG，由 [[plot_selfsupervised_transfer_v2.py]] 生成。

**怎样读图**：先沿 target 反向追溯它来自 clean data、quantizer 还是历史模型；再检查 target 生成路径是否用了不可用信息，最后才解释 loss 的统计意义。

**图没有证明什么**：它没有证明重建 loss 更低会带来更好语义，也没有证明 EMA/centering 在任意网络中足以防坍缩；这些是需要下游与动力学证据的独立命题。

## 十六、Pretext Error Ledger

$$
\text{downstream error}
\not\equiv
\text{pretext error}.
$$

至少分开：

1. corruption/mask design gap；
2. target-generator bias/noise；
3. model approximation error；
4. finite-sample estimation；
5. optimization and target-drift error；
6. representation extraction/layer choice；
7. downstream head estimation；
8. pretrain–deployment shift。

## 十七、Protocol Card

每个实验登记：

- clean unit 与 split；
- corruption/mask distribution；
- visible/target positions；
- target representation与 normalization；
- student/teacher architectures；
- gradient-stop boundaries；
- EMA/center/temperature schedules；
- loss reduction 与 multi-view pairing；
- projection/decoder 是否在评估时丢弃；
- pretext、linear probe、fine-tune 与 scratch 四类结果。

## 十八、AI 接口

### 18.1 Language Models

MLM 学 conditional token recovery；causal LM 学 ordered factorization。两者的 attention visibility、loss positions 与 generation interface 不同。

### 18.2 Vision Transformers

MAE 的 visible-only encoder 让 mask ratio 影响 compute；DINO 的 multi-crop/teacher distribution 则影响 target entropy 与 global/local alignment。

### 18.3 Speech and Time Series

mask spans 过短会局部插值，过长会不可辨；forecasting task 还必须避免未来泄漏。

### 18.4 Multimodal Foundation Models

另一模态既可作 target 也可作 shortcut。caption/image pairing noise 与 modality dropout 必须单独审计。

## 十九、常见错误

1. 把 self-supervised 解释成没有 target；
2. 不区分 clean object、corrupted input 与 supervised positions；
3. 把 square-loss reconstruction 当成完整 conditional distribution；
4. 把 teacher 当独立 ground truth；
5. 省略 stop-gradient 与 EMA update order；
6. 只报最优 mask ratio，不报曲线；
7. 用 pretext accuracy 证明语义/推理能力；
8. target generation 使用 validation/test 信息。

## 二十、最小记忆

> [!summary]
> - 自监督 target 来自数据结构或历史模型，来源必须可追溯；
> - log loss 的 oracle 是条件分布，square loss 的 oracle 是条件均值；
> - mask law、target type、decoder 与 loss positions 共同定义 estimand；
> - EMA teacher 是 student history，不是真值；
> - pretext objective 只是一座桥，必须由 downstream protocol 验收。

## 二十一、掌握标准

### A. 定义

能写统一 corruption–target–student–teacher 合同。

### B. 推导

能推导 conditional cross-entropy 与 conditional-mean optimum、EMA 展开式。

### C. 反例

能构造低 reconstruction error 但低 semantic utility，或高 consistency 但共同错误的系统。

### D. 实验

能实施 mask ratio、target type、stop-gradient、EMA 与 decoder capacity ablation。

### E. 迁移

面对新模态，能选择 target granularity/loss，并写出 leakage 与 self-confirmation 审计。

## 二十二、练习与独立详解

- [[习题 - 遮蔽预测、Teacher–Student 与自监督目标]]
- [[解答 - 遮蔽预测、Teacher–Student 与自监督目标]]

## 参考来源

- [[S-2019-Devlin-BERT]]
- [[S-2022-He-MAE]]
- [[S-2017-Tarvainen-Valpola-Mean-Teacher]]
- [[S-2020-Grill-BYOL]]
- [[S-2021-Caron-DINO]]
- [[S-2021-Chen-He-SimSiam]]

---
type: theorem
status: draft
area: [learning-theory/representation-learning, transfer-learning, linear-probe, evaluation]
aliases: [Linear Evaluation Protocol, Fine-Tuning Risk, Transfer Evaluation Matrix]
node_id: LT-60
prerequisites: ["[[表示学习的任务、表示与下游风险]]", "[[正则化、交叉验证与模型选择]]", "[[线性回归的统计学习理论]]", "[[逻辑回归、复合损失与概率分类]]", "[[遮蔽预测、Teacher–Student 与自监督目标]]"]
related: ["[[训练集、验证集、测试集与自适应复用]]", "[[概率校准、Proper Scoring Rule 与可靠性图]]", "[[Domain Adaptation 与 Domain Generalization Bound]]"]
sources: ["[[S-2014-Yosinski-Transferability]]", "[[S-2019-Kornblith-Shlens-Le-Transfer]]", "[[S-2020-Chen-SimCLR]]", "[[S-2022-He-MAE]]", "[[S-2013-Bengio-Courville-Vincent-Representation-Learning]]"]
exercises: ["[[习题 - Linear Probe、Fine-Tuning 与迁移评估]]"]
solutions: ["[[解答 - Linear Probe、Fine-Tuning 与迁移评估]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-transfer-evaluation-matrix-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# Linear Probe、Fine-Tuning 与迁移评估

> [!abstract] 本章主问题
> linear probe 测量“目标能否被给定表示上的指定线性训练程序以有限标签读出”；fine-tuning 测量“给定初始化、优化器、预算与选择规则能否适配”。二者都不是表示质量的无条件标量，更不能用一个数据集的一次 top-1 排名代替 task-family transfer evidence。

## 一、学习目标

完成本章后，应能：

1. 区分 oracle probe risk 与 finite-label trained-probe risk；
2. 说明 linear probe 能证明和不能证明什么；
3. 把 fine-tuning 写成 initialization-dependent learning algorithm；
4. 用 XOR/非线性可逆映射构造 probe 排名反例；
5. 设计 label-budget、layer、head、shift 与 compute 多轴 transfer matrix；
6. 区分 positive transfer、negative transfer、optimization speedup 与 asymptotic gain；
7. 用 nested selection、paired seeds 与 task aggregation 避免 optimistic ranking；
8. 为 foundation model 建立可复现的 representation evaluation card。

## 二、Oracle Linear Risk

固定 encoder $h:\mathcal X\to\mathbb R^d$、task $t$ 与 affine head class

$$
\mathcal G_{\rm lin}
=
\{z\mapsto Wz+b\}.
$$

oracle linear risk：

$$
\boxed{
R_{t,\rm lin}^{\star}(h)
=
\inf_{W,b}
E_{P_t}[\ell_t(W h(X)+b,Y)].
}
$$

它是 population approximation object，假定可无限优化且知道分布；实验中的 linear probe 不是它。

## 三、Finite-Label Probe Risk

令 downstream training set $S_n\sim P_t^n$，probe algorithm

$$
\widehat g
=
\mathcal A_{\rm probe}
(h,S_n,\lambda,\text{schedule},\text{seed}).
$$

其期望风险

$$
R_{t,\rm probe}^{(n)}(h)
=
E_{S_n,\xi}
R_t(\widehat g\circ h)
$$

包含：

1. linear approximation gap；
2. finite-label estimation error；
3. regularization/optimization error；
4. hyperparameter selection bias；
5. feature preprocessing 与 numerical error。

所以“linear probe accuracy”必须附带 $n$、head、regularization、optimizer 与 selection protocol。

## 四、Linear Probe 能证明什么

在固定 task、data law、representation layer、normalization、head class、label budget 与训练程序下，较低风险说明 target 对该 readout 更容易访问。

它不能单独证明：

- representation 含有更多 mutual information；
- representation 对所有 nonlinear heads 更好；
- fine-tuning 后仍排名相同；
- feature 是因果、鲁棒或校准的；
- pretraining objective 恢复了真实语义因素；
- 更差 probe 的 representation 不含 label information。

## 五、XOR 反例：信息存在但线性不可读

令 $X=(X_1,X_2)$，$X_i\in\{-1,+1\}$ 均匀，label

$$
Y=X_1X_2.
$$

表示 $h_1(X)=(X_1,X_2)$ 完整保留输入，因此 $Y$ 是 $h_1$ 的确定函数；但四个点按 XOR 排列，不存在零误差 affine separator。允许 bias 时可单独切出一个角，最佳 affine 0–1 error 为 $1/4$；若限制 homogeneous separator $b=0$，最佳 error 为 $1/2$。这也说明 probe 是否含 bias 属于定义。

表示

$$
h_2(X)=(X_1,X_2,X_1X_2)
$$

允许线性 head 直接读第三维，error 为 0。

因此 probe 差异反映 linear accessibility，不等于 $h_1$ 丢失了信息。

## 六、可逆变换也能改变 Linear Accessibility

若 $A$ 是 invertible linear map，线性 head 可吸收 $A^{-1}$，oracle linear risk 不变。但一般 invertible nonlinear map $\phi$ 虽不丢信息，却可弯曲 decision boundary，使

$$
R_{\rm lin}^{\star}(\phi\circ h)
\ne
R_{\rm lin}^{\star}(h).
$$

所以“表示信息等价”与“线性 probe 等价”只在特定 transformation group 下重合。

## 七、Fine-Tuning 是算法对象

预训练参数 $\theta_0$，downstream algorithm

$$
\widehat\theta
=
\mathcal A_{\rm FT}
(\theta_0,S_n,\eta_{1:T},T,\lambda,\text{layer policy},\xi).
$$

fine-tuning risk：

$$
R_{t,\rm FT}^{(n,C)}(\theta_0)
=
\mathbb E\!\left[R_t(f_{\widehat\theta})\right],
$$

其中 $C$ 表示 compute/step/memory budget。它同时测量：

- initialization geometry；
- feature reuse；
- optimization speed；
- regularization/implicit bias；
- catastrophic forgetting 或 beneficial adaptation。

当全部层充分训练到相同 function-space optimum 时，初始化差异可能消失；有限数据、有限预算与非凸路径下则不会。

## 八、五种下游 Protocol

| protocol | 更新参数 | 主要 estimand | 主要混杂 |
|---|---|---|---|
| zero-shot | 无或 prompt | pretrained interface alignment | prompt/template/calibration |
| kNN/retrieval | 无 | chosen metric geometry | normalization/index/gallery |
| linear probe | head | linear accessibility | head regularization/label budget |
| partial fine-tune | head + top blocks/adapters | localized adaptability | cut layer/adapter rank |
| full fine-tune | 全部 | initialization + adaptation | optimizer/compute/forgetting |
| from scratch | 全部随机初始化 | architecture/data baseline | training budget fairness |

同一个 encoder 在不同 protocol 上排序反转是合理现象，而不是评测“出错”。

## 九、Positive、Negative 与 Optimization Transfer

设相同 downstream algorithm/budget 下：

$$
\Delta_t(C,n)
=
R_{t,\rm scratch}^{(n,C)}
-
R_{t,\rm pretrained}^{(n,C)}.
$$

- $\Delta_t>0$：在该预算下 positive transfer；
- $\Delta_t<0$：negative transfer；
- early steps positive、large $C$ gap 消失：主要是 optimization speedup；
- large $C$ 仍正：可能改变 generalization/implicit bias；
- source 与 target 越远，higher-layer specialization 可能更强。

必须画完整 learning curve，而非只比较一个 checkpoint。

## 十、Label-Budget Curve

对

$$
n\in\{1,2,4,8,\ldots,n_{\max}\}
$$

每个 class/total label budget 重复采样并评估。可报告：

- risk curve $R(n)$；
- low-shot slope；
- 达到目标 risk 的 label complexity；
- log-budget area under curve；
- subgroup/tail label efficiency。

只报 full-data accuracy 会掩盖表示在低标签区的价值，也可能掩盖大数据下的 negative transfer。

## 十一、Layer 与 Feature Extraction Contract

必须固定：

- backbone output、projection output、pre/post normalization；
- CLS token、mean pooling、last token 或 multi-layer mixture；
- train/eval mode 与 BatchNorm statistics；
- input resolution、tokenization 与 preprocessing；
- frozen encoder 是否允许 dropout；
- feature cache dtype、quantization 与 standardization；
- sequence/image aggregation 与 missing modality 规则。

挑选最佳 layer 本身是 model selection，需要 validation correction。

## 十二、Head Capacity Ladder

建议同一表示至少比较：

1. constant/base-rate；
2. kNN；
3. linear/logistic ridge；
4. shallow MLP；
5. partial fine-tune；
6. full fine-tune。

若 linear 差、MLP 好，可能是信息存在但非线性可访问；若所有 frozen heads 差、fine-tune 好，可能主要提供 optimization initialization；若连 fine-tune 都差，需考虑错误 invariance、domain mismatch 或 negative transfer。

## 十三、Transfer Matrix 而非单分数

定义 axes：

$$
\mathcal E
=
\text{task}
\times\text{protocol}
\times\text{label budget}
\times\text{shift}
\times\text{compute}
\times\text{seed}.
$$

对 task distribution $\Pi$ 可汇总平均风险

$$
E_{t\sim\Pi}[R_t],
$$

也应报告 worst-task、lower quantile、subgroup 与 Pareto frontier。汇总权重必须在看结果前声明。

## 十四、Nested Selection 与 Test Reuse

若在同一个 downstream test set 上选择：

- pretraining checkpoint；
- feature layer；
- normalization；
- head regularization；
- fine-tuning schedule；
- prompt/template；
- best seed；

最终 test score 已被自适应污染。正确结构是 train → inner validation selection → locked outer test；多数据集排行榜反复调参还需要独立 final benchmark 或 reusable-holdout 思路。

## 十五、不确定性与比较

应报告：

1. downstream sample variation；
2. pretraining seed variation；
3. probe/fine-tune seed variation；
4. label-subsample variation；
5. paired difference：相同 split/seed 下模型差值；
6. task-level hierarchical aggregation；
7. 多模型/多任务选择修正；
8. effect size 与 practical threshold，而非只报显著性。

对 identity/group/time dependent data，应按 source unit bootstrap，而不是 sample-level iid bootstrap。

## 十六、公平 Compute Contract

fine-tuning 与 scratch 至少对齐或同时披露：

- total examples/tokens；
- optimizer steps、batch 与 accumulation；
- FLOPs、wall time、memory；
- augmentation 与 regularization search budget；
- early stopping opportunity；
- architecture/parameter count；
- checkpoint selection次数。

“相同 epochs”在数据量、batch 或冻结层不同下不等于相同计算预算。

## 十七、图：表示评估是一张矩阵

先看图回答：一个 encoder 在线性 probe 上领先、full fine-tuning 上落后，是否矛盾？还需要哪几个轴才能解释？

![[00-知识库管理/_assets/figures/learning-theory/fig-transfer-evaluation-matrix-v2.svg|900]]

> [!figure] 图 20.7-08　Oracle/finite probe、fine-tuning 与 transfer matrix
> 左栏分开 oracle linear risk、finite probe 与 fine-tuning algorithm；中栏展示 label budget × head capacity × compute；右栏把 multi-task、shift、seed、selection 与 scratch baseline 纳入最终 claim。来源：依据 Yosinski et al.、Kornblith–Shlens–Le、SimCLR/MAE evaluation protocols 与本库模型选择节点独立绘制；确定性 SVG，由 [[plot_selfsupervised_transfer_v2.py]] 生成。

**怎样读图**：先选左栏 estimand，再沿中栏固定资源轴，最后在右栏决定能否从单任务结果外推到 task family；任意一轴未锁定，排行榜差异都可能不是 representation 本身。

**图没有证明什么**：它没有证明 linear probe 或 fine-tuning 谁“更正确”，也没有给出 upstream accuracy 与 transfer 的普遍单调关系；它只规定可证伪的评估合同。

## 十八、结果解释模式

### 18.1 Linear 高、Fine-Tune 高

目标易线性访问，初始化也适配；仍需 shift 与 calibration 检查。

### 18.2 Linear 高、Fine-Tune 低

可能 fine-tuning 过拟合、学习率过大、forgetting、优化预算不公平。

### 18.3 Linear 低、Fine-Tune 高

表示含可适配结构但 target 非线性不可读，或预训练主要改善优化路径。

### 18.4 两者都低

可能 task information 被增强商掉、source–target mismatch、architecture 不适配或 pretraining 本身失败。

## 十九、Foundation Model Evaluation Card

至少登记：

- model/checkpoint/data cutoff/license；
- encoder layer/pooling/normalization；
- task definitions、loss 与 metrics；
- label budgets 与 split units；
- zero/kNN/linear/MLP/partial/full/scratch protocols；
- hyperparameter search spaces 与 selection data；
- compute、seed 与 uncertainty；
- in-distribution、subgroup、temporal/OOD shifts；
- calibration、latency、memory 与 safety constraints；
- failed tasks 与 negative-transfer cases。

## 二十、AI 接口

### 20.1 Vision/Speech Encoders

分类 linear probe 不足以评价 localization、speaker/content disentangling、temporal precision；必须加入结构化任务。

### 20.2 LLM Hidden States

probe 可测某属性是否易读，但强 probe 可能学习任务本身；causal intervention 与 controlled counterfactual 是额外证据。

### 20.3 Multimodal Models

zero-shot prompt 与 frozen embedding retrieval 同时受 tokenizer、template、gallery 和 calibration 影响，不应混称“表示质量”。

### 20.4 Parameter-Efficient Fine-Tuning

LoRA/adapter/prefix 的 rank、插入层与 trainable budget 是 head-capacity axis；不能与 full fine-tune 只按最终 accuracy 粗比。

## 二十一、常见错误

1. 把 empirical linear probe 当 oracle linear risk；
2. 从低 linear score 推断 label information 不存在；
3. probe 与 fine-tune 使用不同数据处理却归因于 encoder；
4. 不做 scratch baseline；
5. 只报一个 label budget/checkpoint；
6. 在 test 上挑 layer、regularization、seed；
7. 用相同 epochs 冒充相同 compute；
8. 从单任务 top-1 宣称 universal representation。

## 二十二、最小记忆

> [!summary]
> - oracle linear risk 与 finite probe risk 不同；
> - linear probe 测 linear accessibility，不测全部信息；
> - fine-tuning 测初始化 + adaptation algorithm；
> - scratch、label curve、layer/head ladder、shift 与 compute 都是必要对照；
> - representation evaluation 应是一张预先声明的 transfer matrix。

## 二十三、掌握标准

### A. 定义

能写 oracle probe、finite probe、fine-tune 与 scratch estimands。

### B. 推导

能分解 probe error，并用 XOR 证明 information retention 不等于 linear accessibility。

### C. 反例

能构造 probe/fine-tune 排名反转或 finite-budget positive、large-budget gap 消失的情形。

### D. 实验

能设计 nested task × protocol × budget × shift × seed matrix，报告 paired uncertainty。

### E. 迁移

能读懂一个 foundation-model benchmark 的 claim boundary，并指出缺失 baseline 或自适应复用。

## 二十四、练习与独立详解

- [[习题 - Linear Probe、Fine-Tuning 与迁移评估]]
- [[解答 - Linear Probe、Fine-Tuning 与迁移评估]]

## 参考来源

- [[S-2014-Yosinski-Transferability]]
- [[S-2019-Kornblith-Shlens-Le-Transfer]]
- [[S-2020-Chen-SimCLR]]
- [[S-2022-He-MAE]]
- [[S-2013-Bengio-Courville-Vincent-Representation-Learning]]

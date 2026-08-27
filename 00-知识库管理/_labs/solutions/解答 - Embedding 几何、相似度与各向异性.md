---
type: solution
status: draft
area: [neural-networks/embedding-output, representation-geometry, anisotropy]
topic: "[[Embedding 几何、相似度与各向异性]]"
exercise: "[[习题 - Embedding 几何、相似度与各向异性]]"
sources: ["[[S-2019-Ethayarajh-Contextual-Anisotropy]]", "[[S-2002-Xing-Ng-Jordan-Russell-Metric-Learning]]"]
created: 2026-08-24
updated: 2026-08-24
---
# 解答 - Embedding 几何、相似度与各向异性

## A

### NN-EGA-A01

token embedding row 是词表 Parameter 的一行，通常与 token type 一一对应；contextual hidden state 还依赖句子、位置、层和当前参数；output prototype 是分类 head 中与某类 logit 配对的行。三者的抽样分布、训练梯度和允许的重参数化不同：同一 token 可产生很多 contextual states，output row 还可能经过 projection 或 tying。因而对象、层和条件不相同的几何统计不能直接互相替代。

### NN-EGA-A02

$$
\operatorname{dot}(a,b)=a^\mathsf Tb,
\quad
\cos(a,b)=\frac{a^\mathsf Tb}{\|a\|\|b\|},
\quad
d(a,b)=\|a-b\|_2.
$$

共同正交变换保持三者。把两向量都乘正数 $c$ 时，cosine 不变，dot 乘 $c^2$，distance 乘 $c$。共同平移 $a,b\mapsto a+m,b+m$ 保持 distance，但一般改变 dot 与 cosine。若只缩放其中一个向量，cosine 对正尺度不变，另两者仍改变。

### NN-EGA-A03

可检查均值范数、平均/分位 pairwise cosine、centered covariance spectrum、participation-ratio 或 entropy effective rank、主方向解释方差、局部邻域密度和 cluster balance。平均 cosine 既依赖是否 centering，也不能区分少数强主方向、局部簇、norm 分布与长尾；不同谱和局部结构完全可能给出同一个均值。

## B

### NN-EGA-B01

原始向量满足

$$
a^\mathsf Tb=24,\qquad
\cos(a,b)=\frac{24}{5\cdot5}=0.96,
$$

$$
\|a-b\|=\sqrt{(-1)^2+1^2}=\sqrt2.
$$

替换为 $10a=(30,40)$ 后，dot 为 $240$，cosine 仍为 $0.96$，distance 为

$$
\sqrt{(30-4)^2+(40-3)^2}=\sqrt{2045}\approx45.22.
$$

所以 cosine nearest neighbor 对单向量正缩放不变，dot 与 distance 排序可能随 norm 改变。

### NN-EGA-B02

样本均值为 $\mu=(10,0)$。centered vectors 是 $(0,1),(0,-1),(0,2),(0,-2)$，所以

$$
C=\frac14\sum_i(x_i-\mu)(x_i-\mu)^\mathsf T
=\begin{bmatrix}0&0\\0&2.5\end{bmatrix}.
$$

特征值为 $(2.5,0)$，秩为 1，且

$$
r_{\mathrm{PR}}=\frac{(2.5)^2}{(2.5)^2}=1.
$$

原始向量看似都朝 $x$ 正方向，center 后却揭示所有变化只有一维。

### NN-EGA-B03

$$
r_{\mathrm{PR}}=\frac{(9+1)^2}{9^2+1^2}=\frac{100}{82}\approx1.2195.
$$

非零归一化谱是 $(0.9,0.1)$，故

$$
H=-0.9\log0.9-0.1\log0.1\approx0.32508,
$$

$$
r_{\mathrm{ent}}=e^H\approx1.3841.
$$

两种有效秩采用不同谱函数，数值不必相同，因此报告时必须注明定义。

## C

### NN-EGA-C01

若 $Q^\mathsf TQ=I$，则

$$
(Qa)^\mathsf T(Qb)=a^\mathsf TQ^\mathsf TQb=a^\mathsf Tb,
$$

且 $\|Qa\|^2=a^\mathsf Ta$、$\|Qa-Qb\|=\|Q(a-b)\|=\|a-b\|$，所以三者全保持。取一般可逆 $A=\operatorname{diag}(2,1)$，$a=(1,0),b=(1,1)$；dot 从 $1$ 变为 $4$，cosine 从 $1/\sqrt2$ 变为 $2/\sqrt5$。一般可逆变换只保持线性可逆性，不保持 Euclidean geometry。

### NN-EGA-C02

代入定义：

$$
W'x'=(WA^{-1})(Ax)=Wx=z.
$$

因此所有输入上的输出函数完全相同。但若 $A$ 非正交，$x$ 间的 dot、cosine、distance、covariance spectrum 都可改变。只观察端到端函数无法识别内部坐标系；几何结论必须声明模型接口是否固定，或把允许的 $A$ 商掉后再谈可辨识对象。

### NN-EGA-C03

协方差乘正数 $c$ 后特征值变为 $c\lambda_i$，所以

$$
\frac{(\sum_i c\lambda_i)^2}{\sum_i(c\lambda_i)^2}
=\frac{c^2(\sum_i\lambda_i)^2}{c^2\sum_i\lambda_i^2}
=r_{\mathrm{PR}}.
$$

若恰有 $r$ 个非零特征值且都等于 $\lambda$，则

$$
r_{\mathrm{PR}}=\frac{(r\lambda)^2}{r\lambda^2}=r.
$$

它可解释为“均匀承载能量的等效维数”，但不是重构意义的整数秩。

## D

### NN-EGA-D01

测试样本参与估计均值和 whitening matrix，测试分布信息已经改变了训练/预处理映射；随后检索分数不再是对完全未见数据的条件评估。正确流程是在 train split 拟合 mean/covariance/regularization，冻结变换；validation 只选超参数；最终对 validation/test 使用同一冻结变换。若部署允许在线更新，必须把它作为 transductive/online protocol 单独报告，并用时间顺序避免未来泄漏。

### NN-EGA-D02

平均 cosine 接近零可能来自真正均匀，也可能来自两团相反方向的坍缩；随机噪声可近似各向同性却不含语义；一个对任务有用的低维流形也可能强各向异性。因此需增加 covariance spectrum、局部邻域/cluster、frequency/norm 分层，以及冻结表示后的 linear probe、retrieval、鲁棒性等任务指标。是否“好”取决于任务和允许的读出器，不是单个全局统计。

### NN-EGA-D03

raw 保留训练产生的 mean、norm 与 covariance；centered 去掉共同均值但保留尺度和相关；unit normalization 删除逐样本正 norm；whitening 进一步旋转并按逆标准差缩放方向，且需正则化小特征值。预注册应事先指定主 metric/管线、超参数选择 split 和允许的备选分析；全部管线可作为敏感性分析同时报告，但不能看测试结果后挑最有利的一项当主结论。

## E

### NN-EGA-E01

从固定 tokenizer 的 token rows 抽样，并从 held-out 语料按 token/句子两级抽取 contextual states；按词频分桶或重加权，避免高频词主导。预先选定层、是否去除特殊符号、train-fitted centering、cosine 和 centered spectrum/effective rank。以句子或 token type 为 bootstrap 单位给置信区间，并在相同样本上运行 retrieval/linear probe。这样对象差异、频率、层和统计不确定性都有单独账本。

### NN-EGA-E02

解释一：retrieval 的 cosine 与 whitening 目标更匹配，而线性分类依赖被压低的高方差方向；解释二：小特征值方向的噪声被放大；解释三：whitening 参数在有限样本上估计过拟合，或分类器超参数未重新调。可比较 PCA-only、标准化但不旋转、带 ridge 的 $\lambda$-whitening；画性能随保留维数/正则强度的曲线；在严格 train-fitted 变换下分别重调 retrieval 与 classifier，并检查每个谱方向的 label signal-to-noise。

### NN-EGA-E03

第一层只验证“统计不同”：在预注册抽样下给 cosine/spectrum 及区间。第二层提出机制，如 common mean 或少数主方向挤占容量，并给可证伪预测。第三层做干预：centering、移除主方向、whitening或训练正则，同时控制函数与预算。第四层用多个语义下游、校准和鲁棒性检验效用。只有干预稳定地改变中介几何且任务随预测改善，才比相关性更接近机制证据；仍需排除 scale、频率与容量等共同原因。

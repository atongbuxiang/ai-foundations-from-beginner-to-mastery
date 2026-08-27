---
type: synthesis
status: verified
area: [generative-models, quantization, optimization, frontier]
node_id: GEN-61
prerequisites: ["[[VQ-VAE、离散 Tokenizer 与 Straight-Through Estimator]]", "[[自信息、熵与编码长度]]", "[[交叉熵与 KL 散度]]", "[[隐式偏置、最大间隔与优化选择]]"]
related: ["[[Latent Diffusion、压缩瓶颈与两阶段误差]]", "[[DDCM、离散生成路线比较与证据地图]]"]
sources: ["[[S-2024-Mentzer-FSQ]]", "[[S-2025-Fifty-Rotation-VQ]]", "[[S-2024-Zhu-SimVQ]]", "[[S-2025-Vali-DiVeQ]]", "[[S-2023-Su-9826-FSQ]]", "[[S-2024-Su-10489-VQ旋转技巧]]", "[[S-2024-Su-10519-VQ编码表线性变换]]", "[[S-2025-Su-11328-DiVeQ]]"]
exercises: ["[[习题 - Codebook Collapse、FSQ、Rotation、SimVQ 与 DiVeQ]]"]
solutions: ["[[解答 - Codebook Collapse、FSQ、Rotation、SimVQ 与 DiVeQ]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-vq-fsq-gradient-design-evidence-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Codebook Collapse、FSQ、Rotation、SimVQ 与 DiVeQ

> [!abstract] 一句话结论
> “VQ 训练不好”不是一个单一故障：可能是 code 使用集中、encoder 表征坍缩、量化失真、梯度错配或 prior 难学。FSQ 改变量化几何，Rotation 改代理 Jacobian，SimVQ 改 codebook 参数化与优化耦合，DiVeQ 改 error-vector gradient path。它们解决的是不同接口，不能按一列 benchmark 排成普遍优劣。

## 一、先定义什么叫 collapse

给定 code assignment frequency

$$
\hat p_k=\frac{1}{N}\sum_{r=1}^N\mathbf1[k_r=k],
$$

至少有四个不同现象：

### 1.1 Dead codes

$$U=\frac1K\sum_{k=1}^K\mathbf1[\hat p_k>0]$$

很低，表示大量 codes 在统计窗口中没被使用。窗口长度、数据 split 和 distributed aggregation 都会改变 $U$。

### 1.2 低 assignment entropy

$$H(\hat p)=-\sum_k\hat p_k\log\hat p_k,
\qquad \operatorname{PPL}=e^{H(\hat p)}.$$

perplexity 低表示有效 codes 少，但均匀利用并非天然目标：真实数据模式本来可能不均匀。高 perplexity 也可能只是 encoder 在无意义地散列样本。

### 1.3 Representation collapse

encoder outputs $z$ 集中到低维/小区域，导致 codebook 再大也只覆盖局部。这要看 covariance spectrum、pairwise distance 或 downstream information，不能只看 code count。

### 1.4 Quantization mismatch

$$D_q=\mathbb E\|z-q(z)\|^2$$

很大。它可能来自 codebook 未覆盖、latent dimension 太高、scale 不匹配或 STE 把 encoder 推向不适合 nearest-neighbor 的方向。

这四项可以不同步：利用率 100% 仍可能重构差；量化误差小也可能所有样本都挤到一个 code 附近。

## 二、FSQ：取消 learned codebook

FSQ 先把 latent 投影到小维度 $d$，每维压到有限区间并 round。例如对每维 $j$ 取 $L_j$ 个 levels：

$$
u_j=\frac{L_j-1}{2}\tanh(z_j)+\frac{L_j-1}{2},
\qquad q_j=\operatorname{Round}(u_j).
$$

隐式 codebook 是

$$
\mathcal C=\{0,\ldots,L_1-1\}\times\cdots\times
\{0,\ldots,L_d-1\},
$$

名义大小

$$K=\prod_{j=1}^dL_j.$$

优点来自删除了一整类优化问题：没有可学习 centers、没有 nearest-neighbor search、没有 codebook/commitment loss。round 通常仍用 STE，因此它没有消除代理梯度，只是让代理梯度更简单。

### 2.1 不能误读的地方

- 没有 stored codebook collapse，不等于所有笛卡尔积组合都被用到；
- 若 $K=2^{12}$ 且每维二值，$d=12$；但若 encoder 原 latent $D=256$，必须先压到 12 维，这个投影可能是主要瓶颈；
- VQ 的 code geometry 可任意学习，FSQ 是轴对齐 product levels；相同 $K$ 不代表相同 distortion；
- [[S-2023-Su-9826-FSQ]] 和原论文的“竞争性/超越”必须限定数据、模型、码率与任务。

## 三、Rotation Trick：改变代理 Jacobian

标准 STE 把代理 Jacobian 设为 $I$。Rotation Trick 寻找线性变换 $G$，前向把 $z$ 映到所选 $q$，反向把 $G$ 当常量：

$$
z_q=\operatorname{sg}(G)z+\operatorname{sg}(q-Gz).
$$

于是前向 $z_q=q$，代理导数为 $G$。一种构造是

$$
G=\frac{\|q\|}{\|z\|}R,
$$

其中正交矩阵 $R$ 把 $z/\|z\|$ 旋到 $q/\|q\|$。这样 decoder gradient 经过反向旋转/缩放，使 $z,q$ 的夹角和模长比进入更新。

### 3.1 科学空间给出的关键反例

[[S-2024-Su-10489-VQ旋转技巧]] 记录：若初始化时 $\|q\|\ll\|z\|$，尺度 $\|q\|/\|z\|$ 会压小 reconstruction gradient，commitment gradient 可能占主导，把 $q,z$ 一起拉向原点。作者在自己的 VQ-VAE 配置中未得到改进。

这不推翻原论文的 11 类训练配置结果，但否定了“替换 STE 后无需重调”的普遍主张。至少 sweep：codebook 初始化、norm ratio、commitment weight、distance/normalization 与 seed。

## 四、SimVQ：表达可合并，优化不可合并

SimVQ 把有效 codebook 写成

$$E=QW,$$

量化仍在 rows of $E$ 中 nearest-neighbor。推理时 $QW$ 可预先合并，因此表示族未必比直接学 $E$ 更大；训练时梯度却不同。

对 SGD，一阶近似说明某个未命中 row $q_i$ 即使自身梯度为零，有效 code $e_i=q_iW$ 仍会因共享 $W$ 更新：

$$
\Delta e_i\approx
-\eta\left[
\frac{\partial\mathcal L}{\partial e_i}W^\top W
+q_i\sum_j q_j^\top\frac{\partial\mathcal L}{\partial e_j}
\right].
$$

第二项耦合所有 codes。[[S-2024-Su-10519-VQ编码表线性变换]] 用“共享基底”解释它；课程更谨慎地写：factorization 改变 parameter-space geometry 和 optimizer path，是否改善要靠受控实验。

还要区分：固定 $Q$ 只训练 $W$、同时训练 $Q,W$、用何种初始化和 regularization。它们不是同一个 SimVQ 实验单元。

## 五、DiVeQ：让距离进入 gradient path

标准 VQ 的 hard forward $q$ 与 STE backward $z$ 分离。DiVeQ-detach 构造

$$
z_q=z+\|q-z\|
\operatorname{sg}\left(
\frac{q-z}{\|q-z\|}
\right).
$$

前向第二项等于 $q-z$，故 $z_q=q$；反向除了 identity path，还保留 $\|q-z\|$ 对 $q,z$ 的梯度，使 codebook 可从主任务 loss 获得更新。原 DiVeQ 在方向中加入 Gaussian perturbation：

$$
z_q=z+\|q-z\|
\operatorname{sg}\left(
\frac{q-z+\varepsilon}{\|q-z+\varepsilon\|}
\right).
$$

它可减少显式 Aux Loss，但引入噪声尺度和一定训练—推理差异。

[[S-2025-Su-11328-DiVeQ]] 对一般距离 $r(q,z)$ 推导了额外微分项，并把它解释为自适应 auxiliary pressure。这个分析依赖局部线性近似与内积符号，课程标为机制分析，不称为充分性定理。

## 六、五条路线放在共同坐标中

| 方法 | hard forward | surrogate backward | code parameters | 显式量化 Aux Loss | 主要风险 |
|---|---|---|---|---|---|
| VQ + STE | nearest code | $I$ | learned $E$ | 通常有 | dead codes、梯度错配 |
| FSQ | coordinate round | 通常 identity STE | 固定 levels | 无 codebook loss | 低维轴对齐瓶颈 |
| Rotation VQ | nearest code | rotate + rescale $G$ | learned $E$ | 通常仍有 | norm ratio、原点依赖 |
| SimVQ | nearest row of $QW$ | 通常 STE | factorized/shared basis | 通常有 | 参数化/优化器依赖 |
| DiVeQ | nearest code | error-vector path | learned $E$ | 可无 | surrogate bias、噪声/一致性 |

“无 Aux Loss”“无 codebook”“高利用率”“低 distortion”是四个不同卖点，不能互相替代。

## 七、怎样设计可信实验

同一 tokenizer benchmark 至少固定：

- encoder/decoder 架构、训练 token 数、augmentations；
- nominal $K$、实际 latent dimension、token grid 与 bitrate；
- reconstruction/perceptual/adversarial losses；
- optimizer、learning rate、EMA、initialization 与 seed；
- sampling prior 是否相同、是否重训；
- code utilization 统计窗口和 dead-code 阈值。

报告矩阵：

| 层 | 指标 |
|---|---|
| representation | MSE/PSNR、LPIPS、rFID、downstream probe |
| quantization | $D_q$、usage、entropy、code switches |
| optimization | gradient norm ratio、收敛曲线、seed spread |
| generation | prior NLL、sample FID/precision–recall、人评 |
| system | search/softmax cost、memory、throughput |

若某方法提高 utilization 但 rFID 变差，应如实写 trade-off，而不是挑一列胜出。

## 八、图：改的是哪一根箭头

先看图回答：FSQ、Rotation、SimVQ、DiVeQ 分别改了量化器、代理梯度、参数化还是损失路径中的哪一处？

![[00-知识库管理/_assets/figures/generative-models/fig-vq-fsq-gradient-design-evidence-v1.svg|900]]

> [!figure] 图 50.8-05　VQ 改进方法的接口—证据矩阵
> 上半部在同一 encoder–quantizer–decoder 图上标出四种改动，下半部把代数性质、机制假说和协议实验分层。来源：据 FSQ、Rotation、SimVQ、DiVeQ 原论文及科学空间核读独立绘制。

**怎样读图**：先找每种颜色改动的箭头，再向下对齐它能直接支持的结论；不要从“表达可合并”跳到“训练等价”，也不要从单项 utilization 跳到生成质量。

**图没有证明什么**：图不证明任何方法普遍支配 VQ，不证明高 code entropy 表示语义更好，也不证明无 Aux Loss 的 surrogate gradient 更接近真实 hard-quantizer 导数。

## 九、本节回顾与训练

- collapse 必须拆成 usage、entropy、representation 与 quantization mismatch；
- FSQ 删除 learned codebook，却保留低维投影和 round STE；
- Rotation 改 surrogate Jacobian，尺度与初始化是核心边界；
- SimVQ 函数可合并但优化路径改变；
- DiVeQ 让 quantization distance 进入主 loss gradient，不等于 hard argmin 变可微；
- [[习题 - Codebook Collapse、FSQ、Rotation、SimVQ 与 DiVeQ]]
- [[解答 - Codebook Collapse、FSQ、Rotation、SimVQ 与 DiVeQ]]

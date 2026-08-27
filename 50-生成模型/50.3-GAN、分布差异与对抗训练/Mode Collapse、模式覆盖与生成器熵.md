---
type: concept
status: verified
area: [generative-models, gan, mode-collapse]
node_id: GEN-23
prerequisites: ["[[隐式 Pushforward 分布、生成器与判别博弈]]", "[[互信息与依赖性]]"]
related: ["[[Minimax 动力学、旋转、阻尼与局部收敛]]", "[[GAN 稳定化方法、受控比较与证据地图]]"]
sources: ["[[S-2019-Su-6316-GAN能量视角]]", "[[S-2016-Salimans-Improved-GAN]]", "[[S-2016-Metz-Unrolled-GAN]]", "[[S-2015-Theis-Generative-Evaluation]]"]
exercises: ["[[习题 - Mode Collapse、模式覆盖与生成器熵]]"]
solutions: ["[[解答 - Mode Collapse、模式覆盖与生成器熵]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-gan-quality-coverage-collapse-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Mode Collapse、模式覆盖与生成器熵

> [!abstract] 本节主问题
> Mode collapse 是生成分布把过多 latent mass 映到少数输出区域，造成 coverage/recall 低；它可以与单样本质量/precision 高并存。图片重复、latent collision、低 entropy 与漏掉语义 mode 有关却不等价，必须按任务空间和 evaluator 分账。

## 一、四种“重复”现象

1. **exact duplicate**：不同 $z$ 得几乎相同文件；
2. **perceptual collapse**：feature/人类看相同，像素略变；
3. **semantic mode dropping**：整个类别/姿态/组合缺失；
4. **conditional collapse**：固定条件 $c$ 时 diversity 低。

有限画廊只容易发现前两种，不能估计稀有 mode coverage。

## 二、质量—覆盖二维账

定义概念上的：

- precision：生成样本有多少落在数据支持/高质量区域；
- recall：数据支持有多少被生成覆盖。

单一 FID/IS 会合并二者。precision–recall curve、density/coverage、已知 mode count 与人为分层可以定位“清晰但漏模态”。

## 三、生成器熵不是万能诊断

若离散 finite output，collapse 常降低 $H(X_g)$；但高 entropy 也可由无意义噪声产生。连续 differential entropy 依赖单位，降维 pushforward 还可能为 $-\infty$/无 ambient density。任务应测语义/feature coverage，而非只最大化 entropy。

## 四、many-to-one 与 Jacobian

若 $G(z_1)\approx G(z_2)$ 对大量远离 latent，出现 collision。局部可查 generator Jacobian singular values；小 singular values 表示某些 latent 方向不改输出，但：

- 局部 rank 高不保证全局 mode coverage；
- Jacobian volume 大可能放大噪声；
- 语义 modes 未必对应 Euclidean volume。

## 五、为什么 game 容易 collapse

当前 critic 对某个“容易骗”的 mode 给强 generator gradient，许多 latent 同时向它移动；critic 之后修复，generator 又追逐别处，形成 cycling。若 critic 只看单样本，无法直接惩罚 batch 内重复。它是动态机制之一，不是所有 collapse 的唯一解释。

## 六、干预方法与直接作用

- minibatch discrimination：让 critic 看到 batch 相似性；
- feature matching：generator 对齐 feature mean，改变 surrogate；
- unrolled GAN：预见若干步 critic response；
- diversity/repulsion loss：直接惩罚 latent-output contraction；
- conditioning/labels：显式拆 modes；
- architecture/data augmentation：改变表示和 sample complexity。

每项都可能以质量、计算或 bias 换 coverage。

## 七、最小 mode-count 实验

若真实分布均匀含 8 个离散 modes，生成器只覆盖 2 个且各一半：

$$
H(P_*)=\log8,\qquad H(P_g)=\log2.
$$

若生成样本都位于真实 mode 中，precision 可为 1，recall 只有 $2/8=.25$。这就是“看起来都对，但缺很多”的定量原型。

## 八、科学空间研读框

[[S-2019-Su-6316-GAN能量视角]]的“挖坑—跳坑”直觉适合解释生成 mass 追逐少数低能区；课程以[[S-2016-Metz-Unrolled-GAN]]和[[S-2016-Salimans-Improved-GAN]]提供具体动态/批次干预，再用[[S-2015-Theis-Generative-Evaluation]]限制跨指标结论。

## 九、图：清晰度与覆盖不是一条轴

先看图回答：哪一象限是典型 mode collapse？同样高 precision 的两个模型为何 recall 不同？latent collision 图只能说明什么？

![[00-知识库管理/_assets/figures/generative-models/fig-gan-quality-coverage-collapse-v1.svg|900]]

> [!figure] 图 50.3-07　质量—覆盖平面与 latent collision
> 左侧以 precision/recall 二维定位 collapse，右侧画多个 latent 区域映到同一输出 mode。来源：依据生成分布 coverage 定义独立绘制。

**怎样读图**：先按真实 task modes 读 recall，再看生成点是否有效读 precision；collision 是 generator map 的补充机制证据。

**图没有证明什么**：示意图不证明某个指标忠实于人类语义，也不证明 entropy/Jacobian 单独足以诊断 mode collapse。

## 十、本节回顾

- mode collapse 的核心是分布覆盖不足，可与样本清晰并存；
- exact duplicate、perceptual collapse、semantic dropping 与 conditional collapse 分层；
- entropy、Jacobian 与 collision 是辅助量，不是充分诊断；
- 批次、unrolling、repulsion 和 conditioning 改不同机制；
- 评价必须将 precision/quality 与 recall/coverage 分开。

## 十一、练习与独立详解

- [[习题 - Mode Collapse、模式覆盖与生成器熵]]
- [[解答 - Mode Collapse、模式覆盖与生成器熵]]


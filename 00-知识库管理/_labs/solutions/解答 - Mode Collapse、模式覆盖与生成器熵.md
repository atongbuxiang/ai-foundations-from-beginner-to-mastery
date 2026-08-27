---
type: solution
status: draft
topic: "[[Mode Collapse、模式覆盖与生成器熵]]"
exercise: "[[习题 - Mode Collapse、模式覆盖与生成器熵]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Mode Collapse、模式覆盖与生成器熵
## A. 识别与复述
### GEN23-A01
exact 是文件/点重复；perceptual 是 feature/人看同；semantic 是类别/姿态缺失；conditional 是固定 $c$ 的多样性不足。
### GEN23-A02
precision问生成质量/有效性，recall问数据 modes 被覆盖多少；应二维报告。
### GEN23-A03
高 entropy可来自噪声，differential entropy依单位；Jacobian仅局部，不能证明全局 injective或语义覆盖。
## B. 手算与建模
### GEN23-B01
$H_*=\log8,H_g=\log2$，mode recall=$2/8=.25$。
### GEN23-B02
若定义重复比例 $1-\text{unique}/N$，为 $.99$。
### GEN23-B03
$TV=\frac12(|.95-.5|+|.05-.5|)=.45$。
## C. 推导与证明
### GEN23-C01
取 $G(z)=z^2$，$z$ 与 $-z$ 映同一输出；两个正概率区域可对称映到同一区域。
### GEN23-C02
$G(t)=(\cos t,\sin t)$ 局部 derivative非零，但 $G(t)=G(t+2\pi)$，非全局 injective。
### GEN23-C03
令生成均匀分布在远离数据的巨大区间，entropy随区间长度增大，却 precision为0。
## D. 边界、反例与纠错
### GEN23-D01
八真实 modes只生成其中两个且样本都有效，precision=1、recall=.25。
### GEN23-D02
只生成同一“猫脸”语义，但每张添加独特高频噪声，文件不重复而语义 collapse。
### GEN23-D03
连续 entropy可通过放大尺度/噪声提高，完全不要求落在数据支持。
## E. AI 迁移
### GEN23-E01
toy报告mode count/频率/KL与轨迹；真实图像报告feature precision-recall、多标签属性覆盖、人工稀有mode和重复近邻。
### GEN23-E02
minibatch discrimination改critic batch依赖；feature matching改generator objective；unrolling近似未来对手响应。三者不可只按“防collapse”合并。
### GEN23-E03
每个 $c$ 固定多采样，报conditional recall/diversity、rare subgroup频率；匹配训练/部署 $P(c)$，防 evaluator shortcut。


---
type: solution
status: draft
area: [architecture, attention, tensor-shapes]
topic: "[[Self-Attention、Cross-Attention 与张量形状]]"
exercise: "[[习题 - Self-Attention、Cross-Attention 与张量形状]]"
sources: ["[[S-2015-Bahdanau-Attention]]", "[[S-2020-Yun-Transformer-Universal-Approximation]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Self-Attention、Cross-Attention 与张量形状

## A. 识别与复述

### ARCH-SC-A01
二者都用 $\mathcal A(Q,K,V)$。Self 的 Q/K/V 由同一 token collection 投影；cross 的 Q 来自 query stream，K/V 来自另一 memory stream。统一是算子和 inner dimensions，差异是来源、长度、mask/position 合同。

### ARCH-SC-A02
Q $(T_q,d_k)$，K $(T_k,d_k)$，V $(T_k,d_v)$，A $(T_q,T_k)$，O $(T_q,d_v)$。

### ARCH-SC-A03
Self 只表示同源；mask 可允许每个 token 看全局，故不只看自身；三个投影承担检索请求、地址、内容的不同角色，通常参数不同。

## B. 手算与建模

### ARCH-SC-B01
Q：$8\cdot32\cdot64=16,384$；K：$8\cdot128\cdot64=65,536$；V：$8\cdot128\cdot80=81,920$；A：$8\cdot32\cdot128=32,768$；O：$8\cdot32\cdot80=20,480$。

### ARCH-SC-B02
Score 为 $(20,196)$，output 为 $(20,128)$（batch/head 省略）。输出 token 数 20 由 queries 决定；196 是被求和掉的 memory candidate 轴。

### ARCH-SC-B03
Q/K $(10,64)$，V $(10,96)$，score/weight $(10,10)$，output $(10,96)$。若再用 $W_O\in R^{96\times512}$，block attention branch 回到 $(10,512)$。

## C. 推导与证明

### ARCH-SC-C01
对置换 P，$Q'=PQ,K'=PK,V'=PV$，score $S'=PSP^T$。Row-softmax 同步重排列行得 $A'=PAP^T$，故 $O'=A'V'=PAP^TPV=PO$。若固定 mask/position 未同步重排，此证明的假设失效。

### ARCH-SC-C02
$K'=PK,V'=PV$，score $S'=QK^TP^T$，softmax 只重排列，$A'=AP^T$。因此 $A'V'=AP^TPV=AV$。必须同步重排 K/V pairs；只重排一个会改变语义。

### ARCH-SC-C03
$Q'=P_qQ$ 使 score/weights 只重排行：$A'=P_qA$，输出 $P_qAV$，故等变。每个 query 产生一行 distribution 和一个 value-weighted sum，所以输出有 $T_q$ 行。

## D. 边界、反例与纠错

### ARCH-SC-D01
令 keys 分别表示“猫”“狗”，values 分别是猫/狗图特征。若只交换 V 行，shape 仍 $(2,d_v)$，但“猫”地址返回狗内容。数学乘法合法，候选身份合同已破坏；这类 bug 不能靠 shape checker 发现。

### ARCH-SC-D02
无位置 self-attention 能表示任何合适的 permutation-equivariant set/sequence mapping，例如按内容计算全局均值并回传每行、检测是否存在某类 token、set 分类前的等变特征。它不能区分纯顺序置换并不等于没有用。

### ARCH-SC-D03
通用逼近只在连续目标、紧致域、允许构造所需深宽等条件下给存在参数；不提供 SGD 可达、有限数据、精度资源随长度、离散算法外推或任意长度统一保证。有限模型在训练长度外失败与定理不矛盾。

## E. AI 迁移

### ARCH-SC-E01
Decoder Q：$(B,T_{tgt},d_k)$；encoder K/V：$(B,T_{src},d_k/d_v)$；score $(B,T_{tgt},T_{src})$；output $(B,T_{tgt},d_v)$。Source key padding 屏蔽 encoder padding；target query padding 屏蔽无效 decoder outputs/loss。Decoder causal mask 属其 self-attention，不应错误加到 source cross columns。

### ARCH-SC-E02
Text-to-image 可令 image latents 为 Q、text tokens 为 K/V；记录 $T_{latent},T_{text}$、投影宽、text padding、2D latent position、text position，以及两模态 normalization/norm。若方向相反，输出 token 数也随 Q 侧改变；必须记录架构版本而非只写 cross-attention。

### ARCH-SC-E03
无位置 self：随机 P，核验 $F(PX)=PF(X)$；cross memory：核验 $A(Q,PK,PV)=A(Q,K,V)$；query：核验 $A(PQ,K,V)=PA(Q,K,V)$。再加入固定 absolute position 或 causal mask，不同步变换 position/mask，预期一般不再相等；以这个负对照确认测试敏感。

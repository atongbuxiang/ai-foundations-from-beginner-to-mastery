---
type: exercise
status: draft
area: [neural-networks/embedding-output, representation-geometry, anisotropy]
topic: "[[Embedding 几何、相似度与各向异性]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Embedding 几何、相似度与各向异性]]"
created: 2026-08-24
updated: 2026-08-24
---
# 习题 - Embedding 几何、相似度与各向异性

## A

### NN-EGA-A01
区分 token embedding row、contextual hidden state 与 output prototype。为什么不能把其中一类对象上的几何观察自动推广到另两类？

### NN-EGA-A02
分别写出 dot product、cosine similarity 与 Euclidean distance；说明它们对正尺度、共同平移与正交变换各有什么不变性。

### NN-EGA-A03
给出至少四种“各向异性”诊断，并说明为什么报告一个平均 pairwise cosine 不能唯一刻画表示空间。

## B

### NN-EGA-B01
对 $a=(3,4),b=(4,3)$ 计算 dot、cosine 与 Euclidean distance。再把 $a$ 替换为 $10a$，重算三者并解释排序可能如何改变。

### NN-EGA-B02
给定四个向量 $(10,1),(10,-1),(10,2),(10,-2)$，计算样本均值、centered covariance（除以 $n$）、其特征值、秩与 participation-ratio effective rank。

### NN-EGA-B03
某 centered covariance 的特征值为 $(9,1,0,0)$。计算 participation-ratio effective rank；再以 $p_i=\lambda_i/\sum_j\lambda_j$ 计算 entropy effective rank $\exp[-\sum_i p_i\log p_i]$。

## C

### NN-EGA-C01
证明正交变换同时保持 dot、cosine 与 Euclidean distance；构造一个一般可逆非正交变换，使至少其中两者改变。

### NN-EGA-C02
若模型接口为 $z=Wx$，令 $x'=Ax,W'=WA^{-1}$，其中 $A$ 可逆。证明输入—输出函数不变；解释这为何构成“功能不变但内部几何改变”的可辨识边界。

### NN-EGA-C03
证明 participation-ratio effective rank
$$
r_{\mathrm{PR}}=\frac{(\sum_i\lambda_i)^2}{\sum_i\lambda_i^2}
$$
对协方差的正尺度不变，且在恰有 $r$ 个相等非零特征值时等于 $r$。

## D

### NN-EGA-D01
一个团队先用全数据（含测试集）估计均值与 whitening matrix，再评估测试集检索。指出信息泄漏在哪里，并给出 split-safe 流程。

### NN-EGA-D02
反驳：“平均 cosine 越接近零，表示就越好。”给出至少两个反例或缺失条件，并说明应增加哪些下游或局部诊断。

### NN-EGA-D03
比较 raw、centered、unit-normalized 与 whitened 四种表示管线。写出每种管线改变的量，并设计避免 metric cherry-picking 的预注册规则。

## E

### NN-EGA-E01
设计 token rows 与 contextual states 的各向异性对比实验。要求明确抽样单位、频率控制、层、centering、metric、置信区间与下游任务。

### NN-EGA-E02
你发现 whitening 提高 cosine retrieval，却降低线性分类准确率。给出至少三种可检验解释，并设计能区分它们的消融。

### NN-EGA-E03
如何审计论文中“模型 A 的表示更各向同性，因此语义更好”的因果链？请把观察性事实、机制假说、干预与任务效用四层证据分开。

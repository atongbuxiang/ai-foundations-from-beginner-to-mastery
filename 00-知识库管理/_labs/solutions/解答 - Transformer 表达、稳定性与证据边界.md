---
type: solution
status: draft
area: [architecture, transformer, expressivity, stability, evidence]
topic: "[[Transformer 表达、稳定性与证据边界]]"
exercise: "[[习题 - Transformer 表达、稳定性与证据边界]]"
sources: ["[[S-2020-Yun-Transformer-Universal-Approximation]]", "[[S-2021-Dong-Pure-Attention-RankCollapse]]", "[[S-2020-Xiong-Transformer-LayerNorm]]", "[[S-2022-Wang-DeepNet]]", "[[S-2022-Su-9009-PreNorm-PostNorm]]", "[[S-2026-Chen-Attention-Residuals]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Transformer 表达、稳定性与证据边界

## A. 识别与复述

### ARCH-STAB-A01
Attention做内容依赖token mixing；FFN逐token做非线性channel mixing；residual组合历层增量并提供identity路径；position/structure打破或编码token置换对称。完整表达性质来自组合，不能归功单一组件。

### ARCH-STAB-A02
Universal approximation说模型类中存在参数逼近目标；optimization问给定算法能否找到；generalization问有限训练数据学到的参数能否在目标分布表现；efficiency问所需参数、样本、FLOPs、内存与时间。四者没有逻辑等价。

### ARCH-STAB-A03
I：定义/代数恒等式；T：保留假设与量词的定理；E：特定可复现协议下实验；H：尚待区分替代机制的解释/外推；O：教学或调试观察。层级不是“可信度分数”，而是证据类型。

## B. 手算与建模

### ARCH-STAB-B01
Pre Jacobian为 $1+ac$，Post为 $c(1+a)$。取 $a=1,c=1/4$，Pre为 $1.25$ 放大，Post为 $0.5$ 收缩。反例只说明接线可产生不同尺度，真实LN Jacobian依输入方向且非标量。

### ARCH-STAB-B02
总增量为 $\sum_l\varepsilon\Delta_l$，独立零均值给方差 $L\varepsilon^2\sigma^2$。$\varepsilon=1/L$ 时为 $\sigma^2/L$；$\varepsilon=1/\sqrt L$ 时为 $\sigma^2$。若层相关或非零均值，公式需加协方差/均值项。

### ARCH-STAB-B03
Stable rank
$$
r_s=\frac{\|A\|_F^2}{\|A\|_2^2}
=\frac{10^2+1^2+0.1^2+0.01^2}{10^2}
=1.010101.
$$
四个奇异值皆非零时代数秩为4；stable rank约1说明能量高度集中在第一方向。

## C. 推导与证明

### ARCH-STAB-C01
骨架为：对指定紧域 $K$ 上某函数类中的每个目标 $f$，对每个 $\varepsilon>0$，存在满足论文结构/宽深条件的参数 $\theta$，使所指定范数/距离 $d_K(f,g_\theta)<\varepsilon$。它没有量化给定SGD、初始化、数据样本和计算预算以多大概率找到该 $\theta$，也未自动给泛化或部署成本。

### ARCH-STAB-C02
$$
y_{pre}=x+F(N(x)),\quad J_{pre}=I+J_FJ_N;
$$
$$
y_{post}=N(x+F(x)),\quad J_{post}=J_N(I+J_F).
$$
若 $x_{l+1}=x_l+F_l(N(x_l))$，逐层相消得
$$
x_L=x_0+\sum_{l=0}^{L-1}F_l(N(x_l)).
$$
前两式为链式法则，后一式为递推展开；都没有单独给全网谱范数或性能界。

### ARCH-STAB-C03
检查论文层是否去掉 residual/skip、FFN、normalization和position；attention是单/多头、矩阵是否正随机、权重/输入是否有界；参数是否固定、结论用何种rank与收敛范数、深度与宽度条件。目标完整模型任一处不满足，就只能把定理当机制线索，再实测奇异谱、层间表示和任务指标。

## D. 边界、反例与纠错

### ARCH-STAB-D01
高阶网络函数类能表示 XOR，但若训练集只含 $(0,0)\mapsto0,(1,1)\mapsto0$，另两点标签不可由数据识别；多种目标函数同样拟合训练集。即使给全数据，某个饱和初始化/零梯度优化也可能不找到正确参数。表达存在不补足信息或算法。

### ARCH-STAB-D02
DeepNorm支持的是特定接线/参数化下的更新分析和特定协议下千层可训练。增加层数改变参数/FLOPs、优化难度和过拟合/深度稀释；边际增益可能为零或负，系统成本上升。需同预算depth sweep和最终/迁移指标，不能由“未发散”推出单调性能。

### ARCH-STAB-D03
Depth weight是模型内部相关性和routing coefficient；历史层表示高度相关，后续非线性可抵消，且多个weight配置可给同输出。它也受参数化和softmax竞争影响。因果贡献需做层表示替换、遮断、重训练/干预与输出变化，并处理分布外干预；热图本身只是O/E描述。

## E. AI 迁移

### ARCH-STAB-E01
固定数据/token、总参数或明确depth-width预算、训练FLOPs、optimizer家族和评价；为每种方法按预注册同等搜索预算调初始化、residual scale、warm-up/learning rate。稳定性报梯度/更新/activation范数、NaN/失败率和loss曲线；效果报最终/迁移/鲁棒；系统报吞吐/显存。多深度多seed，不用更易启动代替最终质量。

### ARCH-STAB-E02
逐层记录centered token singular spectrum、stable/effective rank、token cosine/variance、residual branch相对范数 $\|\Delta_l\|/\|x_l\|$、相邻层CKA/差分、梯度/更新范数和任务probe。对去residual/FFN、改变scale做消融。不能只看attention entropy或单一rank：低rank可由任务结构产生，高rank也不保证有用，需与干预和任务质量同步。

### ARCH-STAB-E03
I：写新旧routing的精确方程、shape与退化特例。T：列任何update/stability bound的初始化、宽深和随机假设。E：匹配参数/FLOPs/data的多规模多seed结果、消融、失败率、memory/communication。H：为何内容依赖depth routing可能改善信息访问，以及替代解释。O：训练曲线/可视化。卡片还需版本、代码commit、未覆盖任务和不把routing weights当归因的边界。

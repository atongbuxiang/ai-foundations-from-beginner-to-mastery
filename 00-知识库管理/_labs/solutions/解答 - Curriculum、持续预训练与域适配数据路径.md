---
type: solution
status: verified
area: [language-models, pretraining-data, curriculum]
topic: "[[Curriculum、持续预训练与域适配数据路径]]"
exercise: "[[习题 - Curriculum、持续预训练与域适配数据路径]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Curriculum、持续预训练与域适配数据路径

## A. 识别与复述

### LM23-A01
静态 mixture 只给一个 $q(g)$；curriculum 的对象是随 step 变化的 $q_t(g)$，还包含顺序、阶段长度、学习率、optimizer state、checkpoint 起点与 replay。梯度更新一般不交换，所以相同累计份额也可能得到不同终点。

### LM23-A02
Continued pretraining 是从已有 checkpoint 继续自监督预训练的总称；DAPT 用目标领域的未标注文本；TAPT 用目标任务附近的未标注文本；supervised fine-tuning 用有标签/指令目标。数据、损失与证据问题不同，不能都简称“微调”。

### LM23-A03
参数漂移是 $\|\theta_1-\theta_0\|$ 等权重空间变化；功能遗忘是旧域能力/行为指标退化。参数有对称性和非均匀敏感性，所以距离大不必忘、距离小也不保证关键行为保持。

## B. 手算与构造

### LM23-B01
AB：先 A，$\theta_1=0-.1(-1)=.1$；再 B，$g_B(.1)=2.2$，故 $\theta_2=.1-.22=-.12$。BA：先 B，$\theta_1=0-.1(2)=-.2$；再 A，$g_A(-.2)=-1.2$，故 $\theta_2=-.2+.12=-.08$。累计各见一次仍有 $-.12\ne-.08$，显示路径依赖。

### LM23-B02
$\Delta_{new}=1.2-2.0=-0.8$，新域改善；$\Delta_{old}=1.4-1.0=+0.4$，旧域退化。只报新域 -0.8 会漏掉 stability–plasticity trade-off，至少应联合报告两者和约束。

### LM23-B03
平均 exposure 为 $40B/2B=20$ 次/unique token。它不能给 median、尾部分位数或最大次数：抽样可近均匀，也可让少数 tokens 被重复极多；需要 per-item/dedup-cluster counts 或分布模型。

## C. 推导与证明

### LM23-C01
写 $U_A(\theta)=\theta-\eta g_A(\theta)$。则
$$U_BU_A(\theta)=\theta-\eta g_A(\theta)-\eta g_B(\theta-\eta g_A(\theta)).$$
一阶 Taylor 给额外项 $+\eta^2H_Bg_A$；反序则为 $+\eta^2H_Ag_B$。一般 $H_Bg_A\ne H_Ag_B$，再加 optimizer state/非线性，故更新不交换。

### LM23-C02
令 $g_t\sim q_t$、$x_t\sim P_{g_t}$，
$$\theta_{t+1}=\theta_t-\eta_t\nabla\ell(\theta_t;x_t).$$
最终 $\theta_T$ 是有序复合 $U_{T-1}\circ\cdots\circ U_0(\theta_0)$。即使两条路径的 $\sum_t1\{g_t=g\}$ 相同，$q_t$ 的顺序会改变梯度被评估的位置与 optimizer state，因此终点一般不同。

### LM23-C03
若多个 checkpoints 都计算新域 validation 并选择最小值，所选 checkpoint 的新域指标带选择乐观；同时旧域未参与选择，报告其在 winner 上的值会条件化于“新域表现最好”的事件。应预注册 stopping rule，或用独立 selection/final sets，并画全 checkpoint 新旧域轨迹和 Pareto front。

## D. 边界、反例与纠错

### LM23-D01
若“easy”数据含 shortcut 或窄模板，先学它可能把模型送入不利 basin；hard examples 早期也可能提供更有信息的表示。凸问题中顺序差异可能消退，非凸/有限预算中可能正负皆有。因此 easy-to-hard 是需对照验证的 hypothesis，不是定理。

### LM23-D02
方法加入 replay 后旧域更好，但如果它额外训练 20% tokens，改进可能来自更多 compute。应比较同总 targets/FLOPs/wall-time 的 no-replay、replay 和新鲜旧域数据，并把 buffer 构建/选择成本计入；否则只能说该完整预算方案更好。

### LM23-D03
二参数模型 $f(x)=\theta_1x_1+M\theta_2x_2$，令 $M$ 很大。只把 $\theta_2$ 改变 $\varepsilon$，参数距离为 $\varepsilon$ 很小，但在 $x_2=1$ 的关键切片输出变 $M\varepsilon$，足以翻转分类。功能风险取决于数据 Jacobian，而非裸参数距离。

## E. AI 迁移

### LM23-E01
Manifest 至少写 base checkpoint ID/hash、parent run、tokenizer、DAPT/TAPT corpus manifest、mixture schedule、unique/draw/effective tokens、optimizer/scheduler/RNG、code/container、每阶段 start/end checkpoint hashes 和 eval set versions。用 DAG 表示 lineage，禁止仅用 `latest.pt`。

### LM23-E02
固定起点与总 FLOPs，比 static mix、domain-only、replay 和 curriculum；在多个中间 checkpoint 测 new-domain、old-general、safety、temporal pre-cutoff/post-cutoff 与 contamination-clean 五类切片，多 seed 给 CI。选择集与 final audit 分离，并报告每阶段 exposure。

### LM23-E03
只报最佳 curriculum 产生多重尝试后的 winner's curse，也隐藏计算与失败路径。需披露 tried paths、选择规则、搜索空间/预算、每条 validation 结果与 final independent test；若缺失，应把结论降级为“在未完整披露的路径搜索后观察到”。

## 无提示重做

- [ ] 手算同两种梯度的 AB/BA 两步更新。
- [ ] 用有序更新复合解释 curriculum 的路径依赖。


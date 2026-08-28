---
type: experiment
status: draft
material_status: regression-passed
learning_status: not-attempted
area: [learning-theory/vc, learning-theory/uniform-convergence, reproducible-evidence]
assessment_id: VC-CUM-01
scope: [LT-17, LT-18, LT-19, LT-20, LT-21, LT-22, LT-23, LT-24]
script: "[[vc_uniform_convergence_cumulative_gate.py]]"
assessment: "[[阶段测验 - VC 维与一致收敛（20.3）]]"
solution: "[[阶段测验解答 - VC 维与一致收敛（20.3）]]"
figure: "[[plot-vc-uniform-convergence-cumulative-gate-v2.svg]]"
related: ["[[VC 维与一致收敛 MOC]]", "[[学习理论完整课程地图与掌握标准]]", "[[推导与实验 MOC]]"]
created: 2026-08-28
updated: 2026-08-28
---

# 实验 - VC 维与一致收敛累计复现门

> [!abstract] 实验问题
> VC 维为什么不是一句“模型复杂度”口号？本实验从可逐个枚举的 labeling strings 开始，找到 shattering 转折并核对 Sauer 包络；随后在有限有序域上精确计算 threshold class 的共同偏差分布，与 DKW、有限类 Union Bound 和通用 VC radius 对照；最后让 SRM 在预注册层级中选择，并用有限 multiclass/pseudo witnesses 训练“下界见证不等于完整维数证明”。

![[00-知识库管理/_assets/plots/learning-theory/plot-vc-uniform-convergence-cumulative-gate-v2.svg|1200]]

> [!figure] 实验图｜增长—共同事件—层级选择的三段证据链
> **对象与结论：** A 穷举有序点上 threshold、单区间与至多 $s$ 段 1 的模式，并把后者同 Sauer binomial sum 对齐；B 用 multinomial dynamic program 精确求有限域 empirical-CDF supremum 的分布，再和三种通用程度不同的半径比较；C 计算 weighted SRM score，并单列 Natarajan/Graph 与 pseudo-shattering 的有限 lower witnesses。生成脚本：[[vc_uniform_convergence_cumulative_gate.py]]；无 Monte Carlo，canonical 与盲参均做字节确定性回归。
>
> **怎样读图：** A 先看蓝线与红线在 $m=d$ 前重合、在 $d+1$ 分离；B 从 exact radius 向更少利用结构的证书依次读，半径更大不等于 theorem 错误；C 比较 selected layer、best true-risk layer 与 best oracle-bound layer，随后把两个 witness 卡片只读成维数下界。
>
> **适用边界（图没有证明什么）：** A 只覆盖实轴有序点上的区间并类；B 的 exact law 使用已知有限均匀分布和 prefix nesting；C 的 risks 是预设解析账本，witness 不证明维数上界。图不覆盖 data-dependent class、dependent prompts、distribution shift、无界 loss、不可测 supremum 或计算上找不到 ERM/SRM 的问题。

## 一、它验证什么，不验证什么

本实验验证：

1. 至多 $s$ 段连续 1 的 bit strings 数量与 $d=2s$ 的 shattering 转折；
2. 该 ordered interval-union class 达到 Sauer–Shelah envelope；
3. 离散均匀域上 prefix/threshold class 的 exact finite-sample uniform-deviation distribution；
4. exact、DKW、finite-$\mathcal H$ 与本卷 VC inequality 的半径层级；
5. 预注册 SRM 权重怎样进入 penalty、score 与 oracle comparison；
6. full multiclass class 的 Natarajan/Graph lower witnesses，以及 affine two-point pseudo-witness；
7. canonical/盲参 stdout、SVG、XML 和 SHA-256 的确定性与覆盖保护。

它不验证：

- 所有 VC 维为 $2s$ 的类都达到 Sauer 上界；
- 任意现实数据的 empirical-CDF law 等于本实验有限均匀模型；
- DKW 总比所有 VC/Rademacher bounds 更好；
- 观察到的单 batch patterns 给出 worst-case growth upper bound；
- 一个 witness 给出完整 Natarajan/Graph/Pdim 等式；
- 参数量等于 VC 维；
- SRM penalty 对自适应生成的层级仍自动有效；
- 材料回归通过等于学习者已经掌握证明。

## 二、执行顺序、答案隔离与 scorer nonce

1. 完成 20 分钟口试与 210 分钟闭卷；
2. 冻结 `attempt_id`、原稿、时间和 SHA-256；
3. 未看 canonical 数字时完成三轨解析校准；
4. 评分者公布 `scorer nonce`，指定主轨和跨轨盲参；
5. 学习者先写精确计数、半径区间、选择层和边界预测；
6. 使用新 `--output` 运行；
7. 保存 command、stdout、SVG、hash 与运行前预测；
8. 才可打开 canonical 输出和封存详解；
9. 48 小时换类/机制，14 天迁移到陌生容量问题。

nonce 建议映射：SHA-256 首字节模 3 对应 A/B/C；下一字节决定干预模板。公开 fixture 只用于材料审计，不可充当个人盲参。

> [!warning] 防止循环认证
> 先运行脚本后补写“我预测蓝线较低”，或照着 canonical 图复述 VC=4，只能记 practice。个人 evidence 必须保留运行前冻结的组合推导和新的参数输出。

## 三、进入实验前的解析校准门

### 3.1 Track A：模式计数

设有序点上的 labeling 是长度 $m$ 的 bit string，允许至多 $s$ 段连续 1：

1. 证明恰有 $k$ 段 1 的字符串数为 $\binom{m+1}{2k}$；
2. 写出

   $$
   \tau_s(m)=\sum_{k=0}^s\binom{m+1}{2k};
   $$

3. 手算 $s=2$ 时 $m=4,5,10$ 的值；
4. 写出 Sauer sum $\sum_{i=0}^{2s}\binom mi$，说明为什么这里与 $\tau_s(m)$ 相等；
5. 预测增大 $s$、固定 $m$ 时 shattering 转折和曲线怎样移动。

### 3.2 Track B：精确共同偏差

令 $X\sim\operatorname{Uniform}\{1,\ldots,D\}$，prefix class $h_j(x)=\mathbf1\{x\le j\}$：

1. 写出 $R_P(h_j)=j/D$ 和 $R_S(h_j)=N_{\le j}/m$；
2. 给定 count vector $(c_1,\ldots,c_D)$，写出 supremum gap；
3. 写出 multinomial probability

   $$
   \frac{m!}{D^m\prod_{j=1}^D c_j!};
   $$

4. 解释 exact success probability 是对满足所有 prefix constraints 的 count vectors 求和；
5. 手算 DKW、finite-$H$、VC 三个 radius 的方向关系，允许先只给区间；
6. 说明哪个结果利用已知 $P$、哪个利用 CDF nesting、哪个只利用有限类/VC growth。

### 3.3 Track C：层级与见证

1. 检查 $\sum_k\pi_k\le1$；
2. 手算每层

   $$
   \alpha_k=\min\left\{1,
   \sqrt{\frac8m\left[d_k\log\frac{2em}{d_k}+\log\frac4{\delta\pi_k}\right]}
   \right\};
   $$

3. 比较 $R_{S,k}+\alpha_k$，预测 selected layer；
4. 比较 true risks 与 $R_{P,k}+2\alpha_k$，解释三种“最佳层”为何可能不同；
5. 对 $q$ 点 full multiclass class 写出 $K^q$ 与 $2^q$ witness patterns；
6. 对 $x=(-1,1),r=(0,0)$ 写出 affine pseudo-witness 的四组参数。

三轨解析校准未完成时，脚本输出不计入证据门。

## 四、三轨统一对象合同

| 字段 | Track A | Track B | Track C |
|---|---|---|---|
| 基本对象 | bit string / trace | prefix empirical risks | layer-function pair；extension witness |
| 取 supremum | 所有有序 $m$ 点 patterns | 全部 prefixes | 全部预注册 layers/functions |
| 精确量 | enumeration count | multinomial CDF-deviation law | penalty/score；finite witness count |
| theorem 量 | VC 转折、Sauer envelope | DKW/finite/VC radius | weighted common event/oracle inequality |
| comparator | $2^m$ 全 labeling | exact $1-\delta$ quantile | selected、true oracle、penalized oracle |
| 关键边界 | 特定 maximum class | 已知有限均匀 $P$ | witness 只给 lower bound；weights 预先固定 |

## 五、轨道 A：从连续 1 段到 Sauer 极值类

### 5.1 枚举器

脚本显式生成 ${0,1}^m$ 的每个 bit string，计算 0→1 transitions 数：

$$
\operatorname{runs}(b)
=\sum_{i=1}^m\mathbf1\{b_i=1,\ i=1\text{ 或 }b_{i-1}=0\}.
$$

保留 $\operatorname{runs}(b)\le s$ 的模式。`max-size` 被限制在 18，确保这是真正穷举而非隐藏近似。

### 5.2 解析 count

每一段 1 由 $m+1$ gaps 中两个依次排列的 boundaries 确定；$k$ 段对应选 $2k$ 个 gaps。因此

$$
\tau_s(m)=\sum_{k=0}^s\binom{m+1}{2k}.
$$

利用 Pascal identity，可验证

$$
\sum_{k=0}^s\binom{m+1}{2k}
=\sum_{i=0}^{2s}\binom mi
$$

（当 $2s\ge m$ 时按完整 binomial sum 处理）。所以该类 VC 维为 $2s$ 且达到 Sauer envelope，是 maximum class 的具体例子；不能推广成每个 VC-$d$ 类都达到上界。

### 5.3 shattering 转折

脚本要求

$$
\tau_s(2s)=2^{2s},
\qquad
\tau_s(2s+1)<2^{2s+1}.
$$

第一式给 lower witness，第二式给任意 ordered $(2s+1)$ 点上的 upper obstruction。二者缺一不可。

### 5.4 盲参干预

- 把 $s=2$ 改成 3，同时把 `max-size` 提高到至少 7；
- 固定 $s$，增加 `max-size`，预测 polynomial 与 $2^m$ 的分离；
- 单独重算 threshold、one interval 与 $s$ intervals 的 log-growth；
- 48 小时门换成 decision stumps 或有限 depth trees，不得只改 $s$。

## 六、轨道 B：精确 uniform deviation 与通用证书

### 6.1 离散 KS 对象

counts $C_j$ 满足 $\sum_jC_j=m$。对 prefix $r=1,\ldots,D-1$：

$$
F_m(r)=\frac1m\sum_{j\le r}C_j,
\qquad
F(r)=\frac rD.
$$

exact statistic 为 $\max_r|F_m(r)-F(r)|$。

### 6.2 动态规划而非 Monte Carlo

对给定半径 $a$，exact success 是

$$
\sum_{\substack{c_1+\cdots+c_D=m\\
|m^{-1}\sum_{j\le r}c_j-r/D|\le a\ \forall r<D}}
\frac{m!}{D^m\prod_jc_j!}.
$$

脚本逐 category 保存“已分配 count → $1/\prod c_j!$ 系数”，每一步删除违反 prefix constraint 的 state，最后乘 $m!/D^m$。候选半径来自有限集合

$$
\left\{\left|\frac cm-\frac rD\right|:0\le c\le m,1\le r<D\right\};
$$

从小到大寻找 success 至少 $1-\delta$ 的第一个值。因此 `exact_radius` 是有限模型的离散 quantile，不是数值搜索近似。

### 6.3 四种半径的证据层级

1. exact：使用 $D,m,P$ 的全部有限结构；
2. DKW：使用 empirical CDF nesting，但 distribution-free；
3. finite-H：只知道实际有 $D+1$ 个固定 prefixes；
4. VC route：只知道 threshold growth $\tau(n)=n+1$，还支付 ghost-sample 常数。

更通用的证书可能更松。半径 $>1$ 在 0–1 risk 上是 vacuous，不是假结论。

### 6.4 盲参干预

- 固定 $D,\delta$，增加 $m$；
- 固定 $m$，改变 $D$；
- 改变 $\delta$；
- 48 小时门改为非均匀离散 probabilities，并重写 multinomial coefficient $\prod p_j^{c_j}$。

运行前预测 exact quantile 的离散跳跃，不得假设随每次 $m+1$ 都严格下降。

## 七、轨道 C：SRM 与扩展见证的责任边界

### 7.1 SRM 账本

给定 $(d_k,\pi_k,R_{S,k},R_{P,k})$，脚本计算本卷 VC penalty、score 与

$$
B_k=R_{P,k}+2\alpha_k.
$$

- selected layer 最小化 empirical score；
- best true-risk layer 只作解析对照，算法看不到；
- best oracle-bound layer 最小化当前 theorem ledger。

三者不一致是结构选择的正常现象。$B_k$ 不是实际输出风险，也不保证等于最紧可能界。

### 7.2 Multiclass witness

在 $q$ 点、$K$ 标签 full class 中有 $K^q$ 个 functions。固定每点两标签得到 $2^q$ 个 Natarajan choices；固定 reference label 并选择 match/deviate subset 得 $2^q$ 个 Graph patterns。脚本核对这些 counts，只证明 $d_N,d_G\ge q$；特定有限 domain 的 $\le q$ 上界来自不存在 $q+1$ 个不同点，不是 witness 自己给出的。

### 7.3 Pseudo-witness

脚本只枚举有限 slope/intercept grid，检查一维 affine functions 在两点、零阈值上实现 4/4 binary threshold patterns。它证明 Pdim 至少 2；“一维 affine Pdim 恰为 2”的上界仍需独立几何/线性代数证明。

### 7.4 盲参干预

- 合法改变 layer weights，预测 penalty 与选择层；
- 新增一层并保持 weight sum 不超过 1；
- 改变 $q,K$，分开 $K^q$ 与 $2^q$；
- 构造 weight sum 超过 1，确认程序拒绝；
- 换 pseudo points/thresholds，先判断当前有限 parameter grid 是否仍提供 witness。

## 八、评分者随机指定、跨轨盲参与防挑题协议

| 项目 | 分值 |
|---|---:|
| 主轨对象、supremum 与量词 | 3 |
| 主轨解析计数/概率 | 5 |
| 运行前区间和方向预测 | 3 |
| 跨轨盲参及一个手算锚点 | 3 |
| stdout/SVG/hash 可复现 | 2 |
| exact 与 theorem envelope 分离 | 2 |
| 见证/上界或适用边界 | 2 |

14/20 通过；对象、解析式、见证/上界任一为 0 则不通过。

## 九、命令行协议

### 9.1 canonical 材料回归

```bash
python3 00-知识库管理/_labs/code/vc_uniform_convergence_cumulative_gate.py
```

canonical 参数：

```text
max_size=10, interval_runs=2
domain_size=6, uniform_size=40, delta=0.05
layer_dims=1,2,4,8
layer_weights=0.5,0.25,0.125,0.0625
empirical_risks=0.26,0.18,0.115,0.09
true_risks=0.255,0.185,0.13,0.105
srm_size=3000, multiclass_points=3, label_count=4
```

canonical SVG SHA-256：

```text
94a22793710901fde04a3e4e6ea89ad94e0954a2abba9041f4cf1819a76afd31
```

### 9.2 固定审计 fixture

```bash
python3 00-知识库管理/_labs/code/vc_uniform_convergence_cumulative_gate.py \
  --max-size 12 --interval-runs 3 \
  --domain-size 5 --uniform-size 32 --delta 0.08 \
  --layer-dims 1,3,6 --layer-weights 0.5,0.25,0.125 \
  --empirical-risks 0.24,0.15,0.11 --true-risks 0.23,0.16,0.12 \
  --srm-size 2500 --multiclass-points 4 --label-count 3 \
  --output /tmp/vc-cum-blind.svg
```

固定 blind SHA-256：

```text
16c35bb8c37c47fc401e6112809015cde6c721a2ac475d7522255a01658e64ad
```

这些公开参数只用于独立审计，不可作为个人盲参。

### 9.3 覆盖与输入保护

非 canonical 参数不带 `--output` 时必须拒绝；即使显式把 output 指向 canonical 总图也必须拒绝。以下输入也必须在写文件前失败：

- `max-size < 2*interval-runs+1`；
- layer arrays 长度不同；
- weights 非正或和超过 1；
- risk 不在 $[0,1]$；
- enumeration/DP 超过脚本声明的安全范围。

## 十、独立审计固定 fixture

[[vc_uniform_convergence_cumulative_contract_audit.py]]独立检查：

1. LT-17—24 的 8/8 node scope、图片与 MOC mapping；
2. 14/14 题解、100 分、答案与输出隔离；
3. interval-run enumeration、Sauer count、离散 CDF exact DP、三种半径和 SRM penalties；
4. canonical 双跑、stdout markers、SVG XML/viewBox/text density 与 hash；
5. blind fixture 双跑和固定 hash；
6. canonical 覆盖拒绝、非法 weights 拒绝；
7. 六处状态面同时写明 `VC-CUM-01`、`regression-passed`、`not-attempted`、材料门 3/10 与个人 0/10。

审计端重新计算关键有限和与动态规划，不 import gate 的核心函数，避免同一实现自证。

## 十一、盲参数干预怎样才算独立

- 评分者在预测前不公布 stdout/hash；
- 参数不同于 canonical 和公开 fixture；
- 预测文本先冻结；
- 输出为新路径；
- 至少改变两个机制参数；
- 至少跨两轨；
- 对误差分类：组合边界错、概率事件错、数值错、选择账错或见证责任越界。

只改变绘图尺寸、文件名或颜色不算干预。

## 十二、常见失败模式

1. 把 observed trace 当 growth supremum；
2. 只有 shattering lower witness，没有 non-shattering upper proof；
3. 把 interval-union 达到 Sauer 推广为所有 VC 类都达到；
4. 用 `max-size` 截断后的最大模式数冒充渐近增长率；
5. 把 exact uniform radius 当 distribution-free theorem；
6. 把 VC radius $>1$ 解释为定理错误；
7. 把 selected layer 当 true-risk oracle；
8. weights 看数据后选择；
9. 用 $K^q$ 的对数冒充 Natarajan 维；
10. 用 4/4 pseudo patterns 宣称 Pdim 上界；
11. canonical 图替代个人盲参；
12. 先运行后补预测。

## 十三、证据状态机

```text
not-attempted
  -> attempted          有冻结原稿，但未过全部硬门
  -> passed             口试 + 闭卷 + nonce 主轨 + 跨轨盲参通过
  -> retained           passed + 48 h 换类/机制 + 14 d 迁移通过
  -> verified-node      retained 后另有逐节点独立证据
```

材料状态单独记录：

```text
draft material
  -> regression-passed  题卷、详解、实验、脚本、图和独立审计通过
```

两条状态机不得相互替代。

## 十四、48 小时换机制与 14 天迁移

48 小时门必须改变 hypothesis structure、sampling law、layer hierarchy 或 witness family 中至少一项，并说明原证明哪一行改变。只改 $m,\delta$ 不能通过。

14 天门选择陌生 AI capacity 问题，提交：

1. prediction/loss class 与 feedback；
2. lower witness；
3. upper-bound obligation；
4. concentration/selection 路线；
5. data dependence 与 shift 边界；
6. 可证伪实验。

## 十五、结论边界

本门建立的链条是：

$$
\text{trace}
\longrightarrow
\text{growth}
\longrightarrow
\text{Sauer envelope}
\longrightarrow
\text{uniform event}
\longrightarrow
\text{ERM/SRM guarantee},
$$

并在 multiclass/real-valued 出口明确更换见证对象。它不替代下一卷的 data-dependent complexity、margin、localization 与 fast rates。下一入口是[[数据依赖复杂度、间隔与快率 MOC]]。

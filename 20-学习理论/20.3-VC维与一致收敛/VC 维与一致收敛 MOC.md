---
type: moc
status: active
area: [learning-theory/vc]
prerequisites: ["[[PAC 学习与有限假设类 MOC]]", "[[数学归纳、递归与组合计数]]"]
related: ["[[学习理论完整课程地图与掌握标准]]", "[[数据依赖复杂度、间隔与快率 MOC]]", "[[阶段测验 - VC 维与一致收敛（20.3）]]", "[[实验 - VC 维与一致收敛累计复现门]]"]
created: 2026-08-20
updated: 2026-08-28
---

# VC 维与一致收敛 MOC

> [!abstract] 本卷任务
> 用样本上的 labeling patterns 代替无限 $|\mathcal H|$，从 shattering、growth function 与 Sauer–Shelah 进入 binary learning fundamental theorem，再明确 multiclass 与 real-valued 推广。

> [!question] 初学者读完本卷必须能回答
> 1. $d$、$\Pi_{\mathcal H}(C)$ 与 $\tau_{\mathcal H}(m)$ 是哪三种不同对象？
> 2. Sauer–Shelah 怎样把有限 VC 维转成多项式模式上界？
> 3. 对称化、随机交换与有限模式 Union Bound 怎样把组合容量转成概率保证？
> 4. 哪些结论只覆盖 binary、0–1 loss、iid 样本和预先固定的函数类？

进入正文前，先回答路线问题：**VC 维这个单一整数，经过哪些中间对象，才会变成有限样本的概率保证？**

![[00-知识库管理/_assets/figures/learning-theory/fig-vc-growth-sauer-uniform-v2.svg|900]]

> [!figure] LT-17—20 卷级路线总览
> 路线依次把“可完全自由的最大点数”细化为每个样本量上的最坏模式数，再用 Sauer–Shelah 得到多项式包络，最后经对称化与集中不等式变成一致收敛界。来源：依据本卷四个节点独立绘制；确定性 SVG 路线图，无随机种子。

**怎样读图。** 每个箭头都改变了对象类型：$d$ 是一个容量坐标，$\tau_{\mathcal H}(m)$ 是关于 $m$ 的组合函数，Sauer–Shelah 提供确定性上界，而最后一步才引入抽样概率。卷级图只负责导航，不替代各节点中的定义、反例、证明与数值尺度。

**适用边界（图没有证明什么）。** 路线图没有证明四个箭头中的任何一个，也没有覆盖 multiclass、real-valued loss、data-dependent class、dependent sampling 或 optimal-rate refinements；它只导航 LT-17—20 的经典 binary VC 主线。

| ID | 节点 | 关键出口 | 状态 |
|---|---|---|---|
| LT-17 | [[打散、增长与 VC 维]] | combinatorial capacity | draft + A–E 闭环 |
| LT-18 | [[增长函数与经验二分模式]] | $\Pi_\mathcal H(C)$ / $\tau_\mathcal H(m)$ | draft + A–E 闭环 |
| LT-19 | [[Sauer-Shelah 引理]] | finite VC 的多项式增长 | draft + A–E 闭环 |
| LT-20 | [[VC 一致收敛与泛化界]] | distribution-free risk bound | draft + A–E 闭环 |
| LT-21 | [[二分类统计学习基本定理]] | learnability equivalences | draft + A–E 闭环 |
| LT-22 | [[结构风险最小化与非一致可学习性]] | nested classes / SRM | draft + A–E 闭环 |
| LT-23 | [[多分类的 Natarajan 维与 Graph 维]] | multiclass capacity | draft + A–E 闭环 |
| LT-24 | [[实值函数类、伪维与阈值化]] | regression capacity entry | draft + A–E 闭环 |

当前为 **8/8 正文、8/8 A—E 习题与独立详解、0/8 经真实验收**。LT-17—24 共使用 15 张独立自绘/程序生成 v2 图，并保留杨辉三角、VC 几何图库与 D2L 容量示意三组已登记外部来源；全部节点均有引图问题、正式图注、读图方法和适用边界。LT-21—24 已补齐基本定理的必要/充分证明、SRM oracle inequality、多分类 Natarajan/Graph 维与实值 pseudo-dimension，并完成 SVG 结构、XML 与 1200 px 渲染复核。课程顺序随后进入 20.4；`draft` 只表示课程材料成稿，不替代闭卷证明、延迟复测与迁移证据。

## 卷级累计证据门

- 题卷：[[阶段测验 - VC 维与一致收敛（20.3）|VC-CUM-01]]，20 分钟口试加 210 分钟闭卷；
- 独立详解：[[阶段测验解答 - VC 维与一致收敛（20.3）]]，只在原稿、nonce 和运行前预测冻结后开放；
- 三轨实验：[[实验 - VC 维与一致收敛累计复现门]]，贯通 interval-run growth/Sauer、有限域 threshold exact uniform law 与 SRM/extension witnesses；
- 确定性总图：[[plot-vc-uniform-convergence-cumulative-gate-v2.svg]]，由[[vc_uniform_convergence_cumulative_gate.py]]生成；
- 独立回归：[[vc_uniform_convergence_cumulative_contract_audit.py]]复核 8/8 scope、14/14 题解与 100 分、exact dynamic program、canonical/盲参双跑、SVG/XML/hash、非法权重与覆盖保护、六处状态面；
- 延迟门：48 小时换类/机制与 14 天陌生容量迁移。

> [!success] 材料门已建立，个人状态未改变
> VC-CUM-01 为 `regression-passed material / not-attempted learner`。八篇正文继续保持 `draft`，0/8 经真实验收；总图与脚本不能充当个人 shattering、Sauer 或对称化证明。

课程顺序上的下一卷是[[数据依赖复杂度、间隔与快率 MOC]]，它从 worst-case growth 进入 sample-dependent complexity、contraction、margin、localization 与 fast-rate conditions。当前全章已形成 **10/10 卷级材料门与 2/2 资格考材料门（LT-QUAL-01 / LT-QUAL-02）**，个人仍为 **0/10、0/2 / `not-attempted`**；下一步是按前置顺序执行个人证据。

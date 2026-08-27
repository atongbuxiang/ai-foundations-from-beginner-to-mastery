---
type: experiment
status: verified
area: [training, optimization, muon, reproducibility]
experiment_id: EXP-TRN-604-V1
related: ["[[最速下降、范数选择与对偶范数]]", "[[矩阵梯度、谱核范数对偶与 Matrix Sign]]", "[[Muon 的动量、正交化与参数分组合同]]", "[[Newton–Schulz Matrix Sign 的收敛与有限精度]]", "[[Muon 形状缩放、Update RMS 与版本差异]]", "[[Muon、Shampoo、SOAP 与隐式曲率关系]]", "[[Stiefel、谱球面、旋转 Muon 与约束更新]]", "[[Muon 的扩展证据、系统成本与迁移边界]]"]
script: "[[experiment_muon_matrix_geometry_audit_v1.py]]"
results: "[[00-知识库管理/_labs/experiments/trn60.4-muon-matrix-geometry-audit-v1/results.json]]"
created: 2026-08-26
updated: 2026-08-26
---

# 实验 - Muon 矩阵几何、数值迭代与迁移边界审计

> [!abstract] 实验结论
> Python 标准库脚本以 10 条实验轨道、21 项机器断言，把 exact norm/polar identity、rank-deficient non-uniqueness、finite-step NS residual、shape-scaling identity、state-semantics counterexample、Stiefel feasibility 与 systems proxy 分层。所有断言通过；另一目录复跑的 JSON、10 CSV 与 3 SVG 共 14 个文件逐字节一致。实验同时证伪“5 步必然精确正交”“同当前 gradient 即同矩阵优化器 state”“tangent step 即 finite feasible step”三类常见偷换。

## 一、研究问题与预注册门

| ID | 对象 | 可证伪预期 |
|---|---|---|
| H1 | norm oracle | $\ell_2/\ell_\infty/\ell_1$ 候选可行，pairing 分别达到 $-\sqrt{10},-4,-3$ |
| H2 | spectral/nuclear duality | 四个 $2\times2$ case 的 polar pairing 等于 nuclear norm；support residual $<10^{-10}$ |
| H3 | rank deficiency | $G=\operatorname{diag}(3,0)$ 的五个 null-space extensions pairing 都为 3；canonical choice Frobenius norm 最小 |
| H4 | Newton–Schulz | zero singular value 永久为 0；ill-conditioned case 的固定五步不能冒充 exact polar |
| H5 | shape scaling | full-rank original RMS 精确为 $1/\sqrt B$；match_rms_adamw 精确为 $.2$ |
| H6 | momentum/communication | 受控固定 $\mu$ 下 EMA $=(1-\mu)$ sum；但 sign/polar 与 worker sum 不交换 |
| H7 | optimizer boundary | 同 current $G=I$、不同历史产生不同 Shampoo update，而 reset-Muon update 相同 |
| H8 | Stiefel | tangent residual 为 0，Euler finite-step residual 非零，polar retraction residual $<10^{-10}$ |
| H9 | double rotation | 左右正交旋转保持 singular values 至 $10^{-10}$ |
| H10 | systems proxy | GEMM/state 公式为正且显式标记 proxy，不误报 measured wall-clock |

## 二、环境、命令与 artifacts

- 脚本：[[experiment_muon_matrix_geometry_audit_v1.py]]；
- 环境：Python 3 标准库，无 NumPy、PyTorch、Matplotlib 或网络；
- seed：20260826；本版为确定性构造，seed 作为跨卷实验标识；
- shape convention：$y=xW$，$A=$ rows/input，$B=$ columns/output；
- 输出目录：00-知识库管理/_labs/experiments/trn60.4-muon-matrix-geometry-audit-v1/；
- 正式图目录：00-知识库管理/_assets/plots/training-optimization/。

运行：

    python3 "00-知识库管理/_labs/code/experiment_muon_matrix_geometry_audit_v1.py"

脚本只有在 21 项 checks 全为真时返回退出码 0。用另一组 output/plot directory 复跑后，results.json、10 CSV 与 3 SVG 共 14/14 个文件通过逐字节比较。

## 三、关键数值摘要

| 轨道 | 观测 | 证据层级 |
|---|---:|---|
| $g=(3,1)$ | $\ell_2,\ell_\infty,\ell_1$ 最大预测下降为 $3.1623,4,3$ | exact identity |
| $G=\operatorname{diag}(4,1)$ | nuclear norm = polar pairing = 5 | exact identity |
| rotated $2\times2$ case | duality gap $8.88\times10^{-16}$ | numerical certificate |
| rank-one null extensions | pairing 恒为 3；Frobenius norm 在 null value 0 时最小 | exact non-uniqueness |
| classic NS，moderate，5 步 | polar-direction residual $.3413$ | finite-step boundary |
| classic NS，condition $10^4$，5 步 | residual $.99924$ | controlled failure |
| Jordan，flat，5 步 | residual $.15289$ | fixed-step approximation |
| original，$4096\times1024$ | scaled RMS $=.03125=1/\sqrt{1024}$ | exact shape identity |
| original，$1024\times4096$ | scaled RMS $=.015625=1/\sqrt{4096}$ | clamp branch identity |
| match_rms_adamw | 两种 full-rank shape 均为 $.2$ | exact shape identity |
| Shampoo history swap | update $(.0995,.7071)$ 与 $(.7071,.0995)$ | state counterexample |
| Stiefel Euler，$\eta=.1$ | feasibility residual $.014142$；retraction $3.14\times10^{-16}$ | first/finite split |
| double rotation | singular-value gap $4.44\times10^{-16}$ | exact invariant |
| 5-step $4096^2$ | GEMM proxy $2.0616\times10^{12}$ operations | declared proxy only |

## 四、实验图 1：向量与矩阵的两次 support-function 验收

先看图回答：左栏为什么不能直接用柱高给三种 optimizer 排名，右栏的两组柱重合又精确验证了哪一个对偶恒等式？

![[00-知识库管理/_assets/plots/training-optimization/plot-muon-norm-polar-geometry-v1.svg|900]]

> [!figure] 图 EXP-TRN-604-01　Vector norm oracle 与 matrix polar pairing
> 左图固定 $g=(3,1)$，只改变 step unit ball；右图对 diagonal、off-diagonal、rank-one 与 rotated 矩阵比较 nuclear norm 和 exact polar pairing。来源：[[experiment_muon_matrix_geometry_audit_v1.py]] 确定性生成；SVG SHA-256 3864e55b3efc23303ce060ca9843f1437523a8041626b90ed0be50e04b28bcc1。

**怎样读图**：左侧每根柱都在自己的单位球内达到对偶极值，回答“给定几何的一阶最优”；右侧每对灰/绿柱重合，回答 spectral/nuclear duality 是否被 2×2 polar reference 实现复现。rank-one 仍需另看 null-space family。

**图没有证明什么**：左栏不同单位球没有相同物理步长，不能用柱高判断真实 optimizer 优劣；右栏小矩阵 exact identity 也不证明 finite-step BF16 NS 或深网训练效果。

## 五、实验图 2：五步不是数值证书

先看图回答：为什么 classic $s_0=.5$ 很快到达 reference floor，而 $s_0=.01$ 八步仍很慢；Jordan 曲线的振荡又说明了什么？

![[00-知识库管理/_assets/plots/training-optimization/plot-muon-newton-schulz-spectral-audit-v1.svg|900]]

> [!figure] 图 EXP-TRN-604-02　Classic 与 Jordan singular-value residual trajectory
> 图在 exact Python float arithmetic 中，从 $s_0=.5$ 与 $.01$ 运行 0—8 步；纵轴为 $|s_k-1|$ 的对数刻度，绘图区下限截到 $10^{-6}$。来源：同一标准库脚本；SVG SHA-256 63e00960b79de0a216faa69a0d9b5a2c04253083ff4766dba64ebbbce18bb610。

**怎样读图**：先固定初始 singular-value interval，再沿同色曲线看 residual；classic 的局部二次收敛不拯救任意 tiny 初值，Jordan 系数则体现有限步近似的 oscillatory map，而非单调精确极分解。

**图没有证明什么**：图未模拟 BF16 rounding、GEMM reassociation、singular-vector perturbation 或真实 layer spectrum；它不能给出通用的五步误差上界，只证明 iteration count 不能脱离输入区间单独验收。

## 六、实验图 3：shape、state 与 systems 属于三种证据

先看图回答：哪一栏是 exact algebra，哪一栏是状态时钟，哪一栏只是成本代理；为什么三者不能合成一句“Muon 更快”？

![[00-知识库管理/_assets/plots/training-optimization/plot-muon-scaling-state-system-v1.svg|900]]

> [!figure] 图 EXP-TRN-604-03　Shape scaling、momentum semantics 与 NS systems proxy
> 左图比较 tall/wide full-rank ideal polar 在三种 current adjustment 下的 RMS；中图显示同一 gradient 序列的 EMA 与 sum buffer；右图用声明式三-GEMM/步公式比较四种 shape 的五步 FLOP proxy。来源：同一脚本；SVG SHA-256 353c0abb93fe4e0e591089fe0d029b6116150495fda65e7ea5572cde1ef077ef。

**怎样读图**：左侧绿色高柱对应 match_rms_adamw 的固定 $.2$ 目标；中间两线的比例关系只在固定 $\mu$、零初始化受控条件下成立；右侧平方矩阵高柱说明 shape 对 proxy 的非线性影响。

**图没有证明什么**：FLOP proxy 未测 kernel efficiency、sharding、communication、energy、allocator peak 或 P95 tail；EMA 与 sum 的受控比例也不授权无 metadata checkpoint 互载。

## 七、结果文件

| 文件 | 内容 |
|---|---|
| results.json | 全部配置、10 条轨道、21 项 checks 与证据边界 |
| norm_duality.csv | 三种 vector norm oracle 的 feasibility/pairing |
| polar_geometry.csv | 四个 2×2 case 的 singular values、pairing 与 residual |
| rank_nonuniqueness.csv | rank-one null-space extensions 的 objective/Frobenius |
| newton_schulz_scalar.csv | 两组 coefficients、五个初值、0—8 步 scalar map |
| newton_schulz_matrix.csv | 四类 spectrum 的 matrix residual 轨迹 |
| shape_scaling.csv | shape/rank 与三种 current adjustment |
| momentum_semantics.csv | EMA/sum/Nesterov state 与 communication 反例 |
| optimizer_boundary.csv | 相同 current gradient、不同 history 的 Muon/Shampoo 分离 |
| stiefel_rotation.csv | tangent、Euler、polar retraction 与双旋转不变量 |
| system_proxy.csv | GEMM FLOPs、momentum、Gram 与 temporary bytes proxy |

> [!warning] 复现边界
> 本实验刻意使用可手算的向量和 $2\times2$ matrix reference，以定位对象错误；不是 LLM benchmark。下一层框架实验必须补真实 BF16/FP32 kernel、global/local shard、activation output probe、distributed tail、state/peak 和 time-to-quality。

## 八、回链与继续实验

- 数学 target：[[最速下降、范数选择与对偶范数]]、[[矩阵梯度、谱核范数对偶与 Matrix Sign]]；
- 程序与数值：[[Muon 的动量、正交化与参数分组合同]]、[[Newton–Schulz Matrix Sign 的收敛与有限精度]]、[[Muon 形状缩放、Update RMS 与版本差异]]；
- 对象/约束边界：[[Muon、Shampoo、SOAP 与隐式曲率关系]]、[[Stiefel、谱球面、旋转 Muon 与约束更新]]；
- 真实迁移：[[Muon 的扩展证据、系统成本与迁移边界]]。

学习者至少完成一次干预：把 ill-conditioned singular value 改为 $10^{-6}$、把 global $4096^2$ 改成四个 column shards，或交换 momentum convention；运行前先写定量预测，运行后指出改变的是 identity、finite-step residual、state 还是 systems proxy。


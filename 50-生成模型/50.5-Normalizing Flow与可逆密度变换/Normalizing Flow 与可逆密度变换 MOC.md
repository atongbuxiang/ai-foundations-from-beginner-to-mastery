---
type: moc
status: active
area: [generative-models, normalizing-flows]
aliases: [生成模型第五卷, Flow课程地图]
prerequisites: ["[[生成建模对象、似然与自回归 MOC]]", "[[随机变量变换与密度换元]]", "[[多重积分、换元公式与积分变换]]"]
related: ["[[生成模型 MOC]]", "[[生成模型完整课程地图与掌握标准]]", "[[科学空间 - 第五章生成模型专题来源地图]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Normalizing Flow 与可逆密度变换 MOC

> [!abstract] 分卷目标
> Normalizing flow 把“容易采样、容易求密度”的基分布，经一串可逆变换搬到数据空间。本卷不把 `exact likelihood` 当口号：你将逐层核对映射方向、Jacobian 符号、可逆性证书、有限精度逆、logdet 成本、离散数据预处理和部署后处理，并能解释为什么精确密度仍不保证语义样本好。

## 一、八个核心节点

| ID | 节点 | 主要出口 | 状态 |
|---|---|---|---|
| GEN-33 | [[变量替换、基分布与 Exact Likelihood Flow]] | 手算双向换元并建立 density/sample/round-trip 三本账 | verified |
| GEN-34 | [[Coupling Layer、NICE 与 RealNVP]] | 推导块三角 Jacobian、逆变换与 mask mixing | verified |
| GEN-35 | [[Glow、ActNorm、可逆 1×1 卷积与多尺度结构]] | 区分 ActNorm、channel mixing、squeeze 与 factor-out | verified |
| GEN-36 | [[Autoregressive Flow、MAF 与 IAF 的方向权衡]] | 根据任务判断哪个方向并行、哪个方向串行 | verified |
| GEN-37 | [[Residual Flow、可逆 ResNet 与 Logdet 估计]] | 分开可逆性证书、逆迭代误差与随机 logdet 误差 | verified |
| GEN-38 | [[Neural Spline Flow 与单调可逆变换]] | 构造正参数样条并审计解析逆与边界稳定性 | verified |
| GEN-39 | [[Continuous Normalizing Flow、Liouville 与 FFJORD]] | 从连续换元式推导 divergence integral 与 NFE 合同 | verified |
| GEN-40 | [[Flow 的 Support、Dequantization、TARFLOW 与证据地图]] | 审计 support、离散 likelihood、后处理和前沿经验结论 | verified |

静态材料完成不等于个人掌握；个人证据记录在[[50.5 分卷累计测验与复现门]]。

## 二、一条统一计算链

设生成方向为 $g_\theta:\mathbb R^d\to\mathbb R^d$，编码方向为 $f_\theta=g_\theta^{-1}$：

$$
Z\sim p_Z,\qquad X=g_\theta(Z),\qquad
\log p_X(x)=\log p_Z(f_\theta(x))+\log|\det J_{f_\theta}(x)|.
$$

真正可部署的 flow 要同时通过六道门：

1. 对声明的定义域，数学映射确实为双射；
2. forward/inverse 方向和 Jacobian 符号一致；
3. log-determinant 可在预算内精确算或带误差地估计；
4. 浮点 round-trip、最小奇异值与 scale 范围可接受；
5. 数据是离散、连续还是 dequantized 的口径明确；
6. sampling、denoise、guidance 后输出分布没有被偷换。

## 三、架构不是任选：它由计算瓶颈反推

| 结构 | 可逆性来源 | logdet | 主要代价 |
|---|---|---|---|
| coupling | 保留一块、仿射变换另一块 | scale 求和 | 单层更新不完全，需 mixing |
| autoregressive | 三角依赖与非零对角 | 对角项求和 | 一方向存在串行临界路径 |
| residual | $\operatorname{Lip}(g)<1$ 的压缩证书 | trace power series | 逆与 logdet 均为迭代近似 |
| spline | 每维严格单调 | log derivative 求和 | bin/根选择的数值稳定 |
| continuous flow | ODE 解的唯一性 | divergence 积分 | 自适应 solver、trace 方差、NFE |

## 四、科学空间—一级来源路径

1. [[S-2018-Su-5776-NICE流模型]]：换元与 additive coupling 的中文入口；
2. [[S-2018-Su-5807-RealNVP与Glow]]：affine coupling、multiscale 与 Glow；
3. [[S-2018-Su-5977-fVAEs]]：flow posterior 与 generative flow 的接口边界；
4. [[S-2019-Su-6482-可逆ResNet]]：压缩映射、逆迭代和 trace series；
5. [[S-2025-Su-10667-TARFLOW]]：Transformer autoregressive flow 的当代案例。

严格定义与方法分别对照 [[S-2016-Dinh-RealNVP]]、[[S-2018-Kingma-Dhariwal-Glow]]、[[S-2017-Papamakarios-MAF]]、[[S-2016-Kingma-IAF]]、[[S-2019-Behrmann-iResNet]]、[[S-2019-Durkan-Neural-Spline-Flows]]、[[S-2019-Grathwohl-FFJORD]]、[[S-2019-Ho-FlowPlusPlus]]和[[S-2025-Zhai-TARFlow]]。

## 五、卷终通过标准

- 无提示写出两个方向的 change-of-variables，并用一维 affine 例子验符号；
- 手算 additive/affine coupling 的 Jacobian、inverse 与 logdet；
- 写出 Glow 中 $HW\log|\det W|$ 并解释为何 split 不丢维；
- 在 MAF/IAF 中分别标出 density 与 sampling 的串行临界路径；
- 证明 residual inverse 的几何收敛，并区分 truncation bias 与 Hutchinson variance；
- 说明 spline 正宽、正高、正导数各保证什么；
- 推导 CNF instantaneous change-of-variables，报告 NFE/容差；
- 从离散 bin mass 推导 uniform/variational dequantization 下界；
- 运行并改写[[实验 - Normalizing Flow 可逆性与似然最小数值审计]]。

## 六、入口与出口

- 前置：[[能量模型、Score 与 Langevin MOC]]
- 数学底座：[[随机变量变换与密度换元]]、[[流映射、Liouville 公式与连续正规化流]]
- 累计门：[[50.5 分卷累计测验与复现门]]
- 下一卷：[[生成模型完整课程地图与掌握标准#九、50.6 DDPM、DDIM 与离散时间扩散（GEN-41—48）|50.6 DDPM、DDIM 与离散时间扩散]]

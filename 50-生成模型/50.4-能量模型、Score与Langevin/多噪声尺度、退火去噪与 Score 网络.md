---
type: concept
status: verified
area: [generative-models, score-based-models, denoising]
node_id: GEN-29
prerequisites: ["[[去噪 Score Matching、Tweedie 公式与条件期望]]", "[[常用连续分布与指数族]]"]
related: ["[[Langevin、ULA、MALA 与平稳分布]]", "[[Predictor–Corrector 与 Score-based 生成程序]]"]
sources: ["[[S-2019-Su-7038-从去噪自编码器到生成模型]]", "[[S-2019-Song-Ermon-NCSN]]"]
exercises: ["[[习题 - 多噪声尺度、退火去噪与 Score 网络]]"]
solutions: ["[[解答 - 多噪声尺度、退火去噪与 Score 网络]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-score-noise-ladder-modes-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 多噪声尺度、退火去噪与 Score 网络

> [!abstract] 本节主问题
> 小噪声保留数据细节，却让不同模式之间仍隔着低密度屏障；大噪声抹去细节，却把分离模式连接成较平滑的分布。多尺度 score model 学习整条 $p_\sigma=p_0*\mathcal N(0,\sigma^2I)$ 路径，并让 sampler 从易探索的大噪声逐级降到小噪声。它解决的是几何与条件数问题，不是免费消除有限步误差。

## 一、为什么原始数据 score 可能不好定义

图像等高维数据常近似集中在低维流形 $\mathcal M\subset\mathbb R^d$。若 $p_0$ 相对于 $d$ 维 Lebesgue measure 是奇异的，$\log p_0(x)$ 和 $\nabla_x\log p_0(x)$ 在环境空间未必存在。

Gaussian smoothing

$$
p_\sigma(y)
=\int p_0(x)\varphi_{\sigma}(y-x)dx
$$

把质量扩散到全维空间；对 $\sigma>0$，score 通常可定义。这既是统计平滑，也是改变学习对象：模型首先学 $p_\sigma$，不是直接学奇异的 $p_0$。

## 二、一个双峰例说明单尺度困难

令

$$
p_0=\tfrac12\delta_{-a}+\tfrac12\delta_a.
$$

加噪后

$$
p_\sigma(x)
=\tfrac12\varphi_\sigma(x+a)
+\tfrac12\varphi_\sigma(x-a).
$$

其 score 可写为

$$
s_\sigma(x)
=\frac{- (x+a)\varphi_\sigma(x+a)
-(x-a)\varphi_\sigma(x-a)}
{\sigma^2[\varphi_\sigma(x+a)+\varphi_\sigma(x-a)]}.
$$

当 $a\gg\sigma$ 时，两个模式几乎分离；中点 $x=0$ 因对称性有 $s_\sigma(0)=0$，但那里密度极低。局部梯度既不告诉链应选左峰还是右峰，有限噪声也很难越过 barrier。增大 $\sigma$ 后两峰重叠，跨模式移动更容易。

> [!warning] Score 大小不是 density 大小
> $s(x)=0$ 可能是 mode，也可能是对称 valley 或 saddle。只看向量为零不能判断该点概率高。

## 三、Noise-conditional score network

取噪声序列

$$
\sigma_1>\sigma_2>\cdots>\sigma_L>0,
$$

训练单一网络

$$
s_\theta(y,\sigma_i)\approx\nabla_y\log p_{\sigma_i}(y).
$$

DSM 目标常写

$$
\mathcal L(\theta)
=\sum_{i=1}^L\lambda_i
E\left\|s_\theta(X+\sigma_i\varepsilon,\sigma_i)
+\frac{\varepsilon}{\sigma_i}\right\|^2.
$$

conditional target 的平方范数期望为 $d/\sigma_i^2$。若不加权，小 $\sigma$ 层可能在数值上支配 loss；选择 $\lambda_i\propto\sigma_i^2$ 可平衡 target scale，但不必然平衡梯度方差、感知重要性或 sampler error。

## 四、Noise ladder 怎样设计

常用几何序列：

$$
\sigma_i=\sigma_{max}
\left(\frac{\sigma_{min}}{\sigma_{max}}\right)^{\frac{i-1}{L-1}}.
$$

设计时至少回答：

- $\sigma_{max}$ 是否足以抹平全局模式结构，使初始化能覆盖？
- $\sigma_{min}$ 是否与数据离散化/量化噪声相容？
- 相邻尺度分布是否有足够 overlap？
- 训练抽样 $p(i)$ 与 loss weight $\lambda_i$ 是否分开记录？
- 网络怎样嵌入连续或离散 noise level？

“层数更多”不自动更好；它改变训练分配和 sampling NFE。

## 五、Annealed Langevin Dynamics

一个经典离散协议是在每个尺度运行 $K_i$ 步：

$$
x\leftarrow x+\alpha_i s_\theta(x,\sigma_i)
+\sqrt{2\alpha_i}\,\xi,\qquad \xi\sim N(0,I).
$$

再从 $\sigma_i$ 降到 $\sigma_{i+1}$。NCSN 文献常让 $\alpha_i$ 随 $\sigma_i^2$ 缩放，以近似保持 signal-to-noise 行为；这是一种 protocol，不能脱离 score magnitude、维度和预条件写成普遍最优步长定理。

每一级的目标其实是 $p_{\sigma_i}$；当切换到下一层时，chain state 只是 warm start，不是从新目标精确抽得的独立样本。

## 六、最后去噪做了什么

若最终 state 近似来自 $p_{\sigma_L}$，可用

$$
\hat x=x+\sigma_L^2s_\theta(x,\sigma_L)
$$

作 Tweedie posterior-mean denoise。它改变输出分布，通常降低残余噪声；是否改善 FID、coverage 或 likelihood 必须实测。$\sigma_L>0$ 与 posterior mean 本身都意味着最终输出不严格等于原始数据抽样。

## 七、误差分账

$$
\text{final gap}
=\text{smoothing}
+\text{score approximation}
+\text{noise-grid interpolation}
+\text{finite-step/mixing}
+\text{discretization}
+\text{final-denoise shift}.
$$

它们可能互相抵消，不能只凭视觉样本反推出某一项很小。

## 八、科学空间研读框

[[S-2019-Su-7038-从去噪自编码器到生成模型]]把去噪器和退火 Langevin 串成生成流程；[[S-2019-Song-Ermon-NCSN]]给出 noise-conditional network、DSM 与 annealed sampler 的一级协议。本节增加双峰反例和误差分账，避免把“平滑后可学习”升级为“有限步精确采样”。

## 九、图：噪声尺度是一架几何梯子

先看图回答：为什么从大噪声往小噪声走，比直接在最小噪声层从随机初始化采样更可能跨越模式？

![[00-知识库管理/_assets/figures/generative-models/fig-score-noise-ladder-modes-v1.svg|900]]

> [!figure] 图 50.4-05　双峰分布的 Gaussian smoothing、score field 与退火噪声梯
> 上方比较大、中、小三个噪声尺度的 density 连接性；下方展示 sampler 逐级 warm-start，并将细节恢复与模式选择分开。来源：依据 Gaussian mixture 独立计算并作示意重绘。

**怎样读图**：大 $\sigma$ 层的宽峰让链能作全局移动；尺度降低后，score 逐渐恢复局部结构。中点的零 score 在小尺度可能是低密度对称点，不应误读为高概率 mode。

**图没有证明什么**：二维示意不证明高维链快速混合，不给出最优 ladder/步长，也不证明 posterior-mean 最后去噪保持模式概率。

## 十、本节回顾

- Gaussian smoothing 使奇异/尖锐数据分布得到全维 score；
- 大噪声改善全局连接，小噪声恢复细节；
- noise weighting、training sampling 与 inference ladder 是三套合同；
- annealed Langevin 在每层只作有限步近似；
- 最终误差必须包括 smoothing、score、grid、mixing、discretization 与 denoise shift。

## 十一、练习与独立详解

- [[习题 - 多噪声尺度、退火去噪与 Score 网络]]
- [[解答 - 多噪声尺度、退火去噪与 Score 网络]]

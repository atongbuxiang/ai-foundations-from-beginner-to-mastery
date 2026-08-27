---
type: solution
status: draft
topic: "[[Classifier-Free Guidance、尺度与质量多样性前沿]]"
exercise: "[[习题 - Classifier-Free Guidance、尺度与质量多样性前沿]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Classifier-Free Guidance、尺度与质量多样性前沿
## A. 识别与复述
### GEN66-A01
$r_{cfg}=r_u+w(r_c-r_u)$。$w=0$ 为无条件，$w=1$ 为普通条件，$w>1$ 是越过条件点的外推。
### GEN66-A02
它省去独立 noisy classifier 及其输入反向梯度；但通常仍需 conditional/unconditional 两次生成网络 forward，且没有消除 scale sweep、外推误差和质量—覆盖权衡。
### GEN66-A03
不同 prediction type 与 score 的换算含 $\alpha_t,\sigma_t$ 和符号；scheduler 还按类型解释输出。只有在相同线性换算且无 clipping 时，相同 CFG 线性组合才相容。
## B. 手算与建模
### GEN66-B01
$d=(2,-3)$。依次为 $(1,2)$、$(2,.5)$、$(3,-1)$、$(9,-10)$。
### GEN66-B02
$r_c+s(r_c-r_u)=r_u+(1+s)(r_c-r_u)$，故 $w=1+s$：分别为 $0,1,3$。
### GEN66-B03
$e_c-e_u=(-.2,.2)$，所以 $e_{cfg}=(.1,0)+5(-.2,.2)=(-.9,1)$；原本各支至多约 $.2$ 的误差被外推成约 1 的误差。
## C. 推导与证明
### GEN66-C01
$s_c=\nabla\log p(x\mid y)=s_u+\nabla\log p(y\mid x)$，移项即得。
### GEN66-C02
$s_{cfg}=ws_c+(1-w)s_u=\nabla\log[p(x\mid y)^wp(x)^{1-w}]$；用 Bayes 又等价于 $\nabla\log[p(x)p(y\mid x)^w]$，差一个归一化常数。
### GEN66-C03
$s_c-s_u=-(\epsilon_c-\epsilon_u)/\sigma_t$。因此 $s_u+w(s_c-s_u)=-[\epsilon_u+w(\epsilon_c-\epsilon_u)]/\sigma_t$。同一线性算子与线性组合可交换。
## D. 边界、反例与纠错
### GEN66-D01
threshold/clipping 是非线性 $C$，一般 $C(r_u+w(r_c-r_u))\ne C(r_u)+w[C(r_c)-C(r_u)]$；还会改变有效 score field。
### GEN66-D02
从 $r_-$ 向 $r_+$ 外推只是 embedding/prediction-space 几何。自然语言“不是猫”并不等于事件补集的精确 likelihood，训练数据也未必支持逻辑否定。
### GEN66-D03
GEN-65 的 Gaussian tilt：$w$ 增大使方差 $\tau^2/(\tau^2+w)$ 下降，同时条件 mode 更集中。条件证据/分类分数上升而 coverage 明确下降。
## E. AI 迁移
### GEN66-E01
固定 prompts、initial noises、sampler/grid，扫预注册 $w$；对每个样本配对比较，报告条件性、FID/KID、P/R、saturation、人评、NFE/latency，并用 validation 选 $w$ 后锁定 test。
### GEN66-E02
分别运行 $w=0,1$ 并直接比较 raw $r_u,r_c$：若 1 返回 $r_c$，采用本卷 convention；若“无 guidance”仍返回 $r_c$，API 参数可能是 $s=w-1$。查看公式和单元测试，不凭名字判断。
### GEN66-E03
记录 down/up sampler、pooling 对噪声方差的影响、SNR 定义、$t\leftrightarrow\tau$ 映射、主次项权重、分辨率、模型 padding/architecture、NFE 与跨尺度基线。

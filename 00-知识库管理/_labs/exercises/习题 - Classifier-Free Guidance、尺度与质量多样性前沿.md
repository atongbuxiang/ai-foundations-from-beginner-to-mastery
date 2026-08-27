---
type: exercise
status: draft
area: [generative-models, classifier-free-guidance]
topic: "[[Classifier-Free Guidance、尺度与质量多样性前沿]]"
solution: "[[解答 - Classifier-Free Guidance、尺度与质量多样性前沿]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Classifier-Free Guidance、尺度与质量多样性前沿
## A. 识别与复述
### GEN66-A01
写出本卷 CFG convention，并说明 $w=0,1,>1$。
### GEN66-A02
“classifier-free”节省了什么，又没有节省什么？
### GEN66-A03
为什么必须注明 $r$ 是 score、noise、velocity 还是 data prediction？
## B. 手算与建模
### GEN66-B01
$r_u=(1,2)$、$r_c=(3,-1)$。求 $w=0,.5,1,4$ 的 $r_{cfg}$。
### GEN66-B02
某库写 $r=r_c+s(r_c-r_u)$。把 $s=-1,0,2$ 换成本卷 $w$。
### GEN66-B03
若 $e_u=(.1,0)$、$e_c=(-.1,.2)$，求 $w=5$ 时 $e_{cfg}$，解释误差放大。
## C. 推导与证明
### GEN66-C01
用 Bayes identity 推导 $s_c-s_u=\nabla_x\log p_t(y\mid x)$。
### GEN66-C02
推导理想 CFG 的 tilted density $p_t(x\mid y)^w p_t(x)^{1-w}$。
### GEN66-C03
证明固定 $t$ 且无非线性后处理时，在 $s=-\epsilon/\sigma_t$ 下 score/noise CFG 相容。
## D. 边界、反例与纠错
### GEN66-D01
解释 dynamic thresholding 为什么破坏简单参数化等价。
### GEN66-D02
反驳“negative prompt 就是严格条件 $\neg y$”。
### GEN66-D03
构造一个条件分数上升而 coverage 下降的最小例子。
## E. AI 迁移
### GEN66-E01
设计配对 seed 的 CFG scale sweep。
### GEN66-E02
诊断某 pipeline 在 `guidance_scale=1` 时究竟是否 guidance-free。
### GEN66-E03
为跨分辨率 guidance 列出 SNR/time 对齐与复现字段。
## 解答入口
[[解答 - Classifier-Free Guidance、尺度与质量多样性前沿]]

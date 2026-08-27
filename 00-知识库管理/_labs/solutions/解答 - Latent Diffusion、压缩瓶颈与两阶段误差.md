---
type: solution
status: draft
topic: "[[Latent Diffusion、压缩瓶颈与两阶段误差]]"
exercise: "[[习题 - Latent Diffusion、压缩瓶颈与两阶段误差]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Latent Diffusion、压缩瓶颈与两阶段误差
## A. 识别与复述
### GEN62-A01
$z_0=E(x)$、$\hat x=D(z_0)$；forward $z_t=\sqrt{\bar\alpha_t}z_0+\sqrt{1-\bar\alpha_t}\epsilon$；生成 $z_T\to z_0^{gen}$ 经 latent denoiser，再 $D(z_0^{gen})$ 得图像。
### GEN62-A02
continuous latent 是 $\mathbb R^d$ 张量；VQ clean latent 是有限 code lookup/vector；categorical noisy state 始终在有限 indices 上按 $Q_t$ 跳。VQ vectors 上加 Gaussian 后 noisy state 又是连续的，必须单独说明。
### GEN62-A03
representation：AE 丢失；prior/model：latent distribution 近似；sampler：finite steps/solver/guidance；decoder/evaluation：decoder sensitivity/hallucination 和指标偏好。
## B. 手算与建模
### GEN62-B01
pixel spatial sites $512^2=262144$；latent $64^2=4096$，缩小 64 倍。dimension ratio $4\times4096/(3\times262144)=1/48\approx.02083$。
### GEN62-B02
取 $s=1/5=.2$，使 $\tilde z=sE(x)$ 标准差约 1。生成出的 $\tilde z$ 在送入原 decoder 前用 $z=\tilde z/s=5\tilde z$ 还原尺度。
### GEN62-B03
$4096\log_216384=4096\times14=57344$ bits=7168 bytes。continuous float16 为 $4096\times4\times2=32768$ bytes。前者还需 codebook/model，且 entropy coding 可低于 nominal。
## C. 推导与证明
### GEN62-C01
插入 $D(E(x^*))$：$d(x^*,D(z^\theta))\le d(x^*,D(E(x^*)))+d(D(E(x^*)),D(z^\theta))$。第一项是 representation floor，第二项含 latent prior/sampler 与 decoder sensitivity。
### GEN62-C02
若两者都无误，则 $D(E(x_a))=x_a$ 且 $D(E(x_b))=x_b$。但 $E(x_a)=E(x_b)=z$ 且 $D$ 确定，左侧均为同一个 $D(z)$，推出 $x_a=x_b$，与假设矛盾。
### GEN62-C03
$h=H/f,w=W/f$，故 $hw/HW=1/f^2$。实际计算还乘 channels/kernel/blocks，并受 attention、decoder、memory、batch 和硬件影响，所以只是一阶 shape ledger，不是速度定理。
## D. 边界、反例与纠错
### GEN62-D01
多数 LDM 在连续 $z$ 上加 Gaussian noise；离散 token diffusion 在 finite alphabet 上用 stochastic matrix/CTMC。只有明确 VQ indices 与 categorical corruption 才是后者。
### GEN62-D02
相同 latent 对应多个原输入时，posterior over originals 有不确定性。denoiser只能生成符合 latent/data distribution 的可能细节，无法知道某个原样本被 encoder 删除的 bit；这是信息不可辨识，不是优化不足。
### GEN62-D03
perceptual/GAN loss 可选择视觉上锐利但像素位置不同的纹理，降低感知距离却增加 MSE。锐利度、逐像素 fidelity 与 likelihood 是不同评价。
## E. AI 迁移
### GEN62-E01
保存 encoder/decoder architecture+weights、posterior mean/sample policy、downsample $f$、channels、latent scale/normalization、AE losses、diffusion parameterization/schedule、condition encoder/cross-attention、sampler、precision 与版本 hashes。
### GEN62-E02
对多个 $f$ 重新训练/等预算调优 AE 与 diffusion；先报 reconstruction table，再在相同 data/compute/NFE 下报 generation；记录 tensor shapes、params、FLOPs、memory、wall-clock 和 seed spread，不能只对齐 epoch。
### GEN62-E03
训练前测 $E(x)$ 每通道 mean/std、finite 和 quantiles；assert 缩放后总体 std 在预设区间、训练/推理使用同 $s$、decoder 前精确除回、checkpoint metadata 匹配。用已知输入做 encode–scale–unscale–decode round trip。

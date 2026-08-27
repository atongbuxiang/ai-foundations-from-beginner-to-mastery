---
type: source
status: active
area: [sources, learning-theory, sample-compression]
source_type: paper
title: "Relating Data Compression and Learnability"
author: [Nick Littlestone, Manfred K. Warmuth]
year: 1986
url: "https://mwarmuth.bitbucket.io/pubs/T1.pdf"
accessed: 2026-08-23
source_tier: A
license: "Author-hosted paper; retain citation, independent derivations, and link only"
venue: "Technical Report, University of California, Santa Cruz"
scope_role: primary
temporal_role: classical-foundation
related: ["[[样本压缩方案与泛化]]", "[[Occam 界、编码长度与先验权重]]", "[[S-1987-Blumer-Ehrenfeucht-Haussler-Warmuth-Occam-Razor]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Relating Data Compression and Learnability

> [!abstract] 来源定位
> Littlestone 与 Warmuth 研究把一个一致标注样本压成固定数量的标注样本点，再由 reconstruction map 恢复与全样本一致的 hypothesis。其核心计数式把“可能被选中的 kernel 子集数量”转成 realizable generalization bound，是本库区分 sample compression、bit compression 与 model-file compression 的原始坐标。

## 元数据与纳入

- 作者公开全文：[PDF](https://mwarmuth.bitbucket.io/pubs/T1.pdf)；
- 正式引用：Littlestone, N. & Warmuth, M. K. (1986), *Relating Data Compression and Learnability*；
- 证据角色：compression/reconstruction pair、kernel size、side information、consistency 与 learnability；
- 版权边界：课程自行重画 compress–reconstruct–certify 流程并独立推导 union bound。

## 本库调用的断言

1. size-$k$ sample compression scheme 由 compression map $\kappa$ 与 reconstruction map $\rho$ 共同定义；
2. reconstructed hypothesis 必须与完整 realizable sample 一致，不能只在 retained subset 上表现好；
3. 对固定大小 $k$、无 side information 的 scheme，真实误差超过 $\varepsilon$ 的概率至多
   $$
   {m\choose k}(1-\varepsilon)^{m-k};
   $$
4. 若有有限 side-message set $Q$，计数预算乘以 $|Q|$；
5. sample point 可以包含高精度实数，因此 kernel size 与 bit length 是不同复杂度；
6. 允许重构误差、噪声或 data-dependent kernel size 时，需要扩展 theorem，不能沿用最基础的 realizable 式。

> [!warning] 术语纪律
> “模型被量化到 4 bit”“权重文件能压缩”“只保存若干 support vectors”分别属于 bit/parameter/sample description；只有给出合法的 sample compressor、side information 预算和全样本 reconstruction consistency，才能调用本来源的基础界。

## 后续调用

- [[样本压缩方案与泛化]]：定义、计数证明与 AI 反例；
- [[容量界、稳定性界与 PAC-Bayes 的比较]]：证书对象比较；
- 后续支持向量机、最近邻和 prototype methods：压缩集大小审计。

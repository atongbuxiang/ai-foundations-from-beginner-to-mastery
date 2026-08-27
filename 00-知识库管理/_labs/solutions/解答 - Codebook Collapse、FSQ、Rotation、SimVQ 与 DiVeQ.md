---
type: solution
status: draft
topic: "[[Codebook Collapse、FSQ、Rotation、SimVQ 与 DiVeQ]]"
exercise: "[[习题 - Codebook Collapse、FSQ、Rotation、SimVQ 与 DiVeQ]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Codebook Collapse、FSQ、Rotation、SimVQ 与 DiVeQ
## A. 识别与复述
### GEN61-A01
dead codes 指统计窗口零使用；低 entropy 指使用高度集中；representation collapse 指 encoder outputs 本身集中/低秩；高 quantization error 指 $z$ 与所选 $q$ 距离大。它们相关但可互相分离。
### GEN61-A02
FSQ 改量化几何为低维逐坐标 round；Rotation 改 surrogate Jacobian；SimVQ 改 codebook 参数化 $E=QW$ 与更新耦合；DiVeQ 改 error-vector gradient path，使主 loss 可更新 codebook。
### GEN61-A03
无 Aux Loss 是 objective/gradient path 性质；无 learned codebook 是参数化性质；高 utilization 是数据与训练后的统计。任一项都不能推出另两项，也不能推出低 distortion。
## B. 手算与建模
### GEN61-B01
$K=8^3\times5^2=512\times25=12800$。固定长 nominal bits/token 为 $\log_2 12800\approx13.644$；整数打包可能用 14 bits，entropy coding 可不同。
### GEN61-B02
若只看尺度，gradient norm 乘 $.05$，即缩小 20 倍。旋转保持 norm，不补回该尺度；因此 commitment 等其它梯度的相对权重会放大约 20 倍。
### GEN61-B03
以自然对数，$H=-[.5\ln.5+.25\ln.25+2(.125\ln.125)]\approx1.213$，PPL $e^H\approx3.364$。四类均非零，usage=100%，但有效数小于 4。
## C. 推导与证明
### GEN61-C01
推理函数只使用乘积矩阵 $E=QW$，可预计算合并。训练时 gradient 分别作用于 $Q,W$，诱导的 $\Delta E$ 含预条件与跨 code 耦合项；Adam 等状态也按 factors 保存，所以不等价于直接优化 $E$。
### GEN61-C02
$z_q=z+\|q-z\|\operatorname{sg}((q-z)/\|q-z\|)=z+q-z=q$。反向 stop-gradient 冻结方向，但距离 $\|q-z\|$ 可微，故其导数把主 loss 信号传给 $q,z$；这正是新增路径。
### GEN61-C03
第 $j$ 维可取 $L_j$ 个值，独立组合的乘法原理给总数 $\prod_jL_j$。这是名义可取组合数；encoder 实际是否访问每个组合是经验问题。
## D. 边界、反例与纠错
### GEN61-D01
令 100 个 codes 都在错误尺度上远离有意义 latent，并强制 round-robin 分配每个样本，usage 100%；decoder capacity 很小，输入 code 与图像内容无关，重构近似均值图，误差很大。
### GEN61-D02
原论文陈述多个指定配置的总体实验结果；博客作者测试的是不同初始化、norm ratio、loss weights 和代码。平均 treatment effect 与新 domain/config 的负结果不矛盾，后者揭示外部有效性边界。
### GEN61-D03
FSQ 只保证隐式 levels 固定，不会因 center 未更新而“死”。若 encoder 总输出同一角落，只有一个组合被用，组合 entropy 仍近零。因此 product code space 不保证均匀 occupancy。
## E. AI 迁移
### GEN61-E01
表格同时固定 encoder/decoder、tokens、$K$/effective dimension、grid、loss、optimizer/seed；列出 forward quantizer、backward surrogate、parameter update。结果报 distortion/rFID、usage/entropy、$D_q$、prior NLL/sample quality、params/FLOPs/wall-clock。
### GEN61-E02
训练初期和全程记录 $\|q\|/\|z\|$、reconstruction/commitment/codebook gradient norms 到 encoder 的比值、code occupancy 与 loss。做 K-means vs random init、不同 commitment weight 的 factorial sweep，验证 Rotation 失败是否由尺度机制预测。
### GEN61-E03
先写可观测预测，例如“若共享 $W$ 的耦合是原因，冻结 $Q$ 仍应提高未命中 code 的有效位移”；再设计对照、预注册指标和否证条件。若只在看到结果后换解释，标为 post-hoc hypothesis，不称机制证据。

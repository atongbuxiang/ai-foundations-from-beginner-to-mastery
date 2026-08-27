---
type: solution
status: verified
area: [language-models, pretraining-data, contamination]
topic: "[[Benchmark 污染、时间截止与成员重叠审计]]"
exercise: "[[习题 - Benchmark 污染、时间截止与成员重叠审计]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Benchmark 污染、时间截止与成员重叠审计

## A. 识别与复述

### LM20-A01
Exposure 是 item/相关表示进入训练阶段；memorization 是参数保留可检测信息；retrieval 是给定 prompt 能唤起；exploitation 是这种 exposure 对决策/分数有因果贡献。四者可能断链，overlap detector 主要测 exposure proxy。

### LM20-A02
可分别暴露 question/input、answer/label、rationale/explanation、metadata/order以及 task instruction/template。完整 item 之外，ancestor、翻译、paraphrase或 options 也可能给不同程度优势。

### LM20-A03
Exact 漏格式/片段/改写；n-gram受 common phrases、长度和阈值影响；semantic提高改写召回但易同题误合并且 detector 也可污染；black-box 无需语料却难唯一归因版本/训练阶段，阴性 power有限。

## B. 手算与构造

### LM20-B01
后验为 $.9(.02)/[.9(.02)+.01(.98)]=.018/.0278\approx0.6475$。即 detector 阳性约 64.7% 真污染，在给定假设下仍有约 35.3% 假阳。

### LM20-B02
若 public release 早于 crawl 且 crawl 早于 cutoff，则公开 exposure 时间上可能；若 release 晚于 cutoff，直接公开版本风险低。例外含 draft/private leak、ancestor data、镜像提前、post-training/SFT/RAG晚于 cutoff、模型/API silent update。

### LM20-B03
令 dirty detector更易命中 web 上常见、简单事实题，其本来正确率 80%；clean 组是新颖难题，本来 60%。即使污染处理对每题因果效应为 0，分组均值仍差 20 点。需要同难度/同 item 的随机注入或反事实变体。

## C. 推导与证明

### LM20-C01
$P(C\mid+)=P(+\mid C)P(C)/P(+)$，分母按全概率为 $r\pi+f(1-\pi)$，即公式。它说明 base rate 与 detector FPR 同等重要。

### LM20-C02
因果效应需同一 item 在 exposed/unexposed 两种潜在结果 $Y_i(1)-Y_i(0)$；observed dirty/clean 比较的是不同 items，且 $H_i$ 受难度/频率/域影响。无随机化/可交换性和准确 exposure label，均值差混合了选择差异。

### LM20-C03
若 sensitivity r、FPR f、true rate π，则 observed positive rate $\tilde\pi=r\pi+f(1-\pi)=f+(r-f)\pi$。若 r≠f，可校正 $\pi=(\tilde\pi-f)/(r-f)$，但 r/f估计误差和切片漂移需传播不确定性。

## D. 边界、反例与纠错

### LM20-D01
训练可含 paraphrase、翻译、OCR、answer explanation、ancestor dataset或局部长 n-gram，exact normalization 都不命中。只能说“此 canonical exact detector 未发现”。

### LM20-D02
Overlap 证明文本相似，不证明 model attended/memorized/retrieved，更不证明正确答案因它而来；重复内容可能无 label或模型已会。需 controlled exposure/ablation、behavioral probe与难度匹配。

### LM20-D03
每次看 test overlap/分数再调阈值，会把 test 信息反馈进训练数据选择，最终 clean set针对该 test优化。应预注册 detector或用独立 calibration benchmark，final test 只作一次审计。

## E. AI 迁移

### LM20-E01
为 pretrain、continued、SFT、preference、prompt library、RAG index分别存 cutoff/manifest；exclusion list 版本化含 input/label/rationale/variants；所有 stage 在摄入前扫描并记录 removed IDs/reasons；API/model version继承事件记录。

### LM20-E02
注入已知 exact/format/paraphrase/translation positives及 hard negatives/common phrases，按长度/语言/task分层；扫 threshold报告 precision/recall/PR curve和 candidate cost；验证集选 operating point，测试集冻结；人工复核边界并给 CI。

### LM20-E03
发布日期不等于所有训练阶段 cutoff；可能有 draft/ancestor、SFT/RAG/API更新。模型卡需给各 stage cutoff、benchmark version、detectors与不可观察数据。结论改为“在已声明阶段/检测器下，时间证据不支持公开版本 exposure”。

## 无提示重做

- [ ] 由 π、r、f 手算 detector 阳性后验。
- [ ] 用潜在结果语言解释 dirty–clean gap 的混杂。

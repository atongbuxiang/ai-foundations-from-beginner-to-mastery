---
type: concept
status: verified
area: [language-models, tokenization, evaluation, fairness, security]
node_id: LM-08
aliases: [Tokenizer 审计, Tokenizer 公平评估]
prerequisites: ["[[BPE、合并规则与确定性编码解码]]", "[[WordPiece、词表构建与最长匹配边界]]", "[[Unigram LM、Viterbi、EM 与 Subword Regularization]]", "[[Byte-level、Byte Fallback、特殊 Token 与 Chat Template]]"]
related: ["[[NLL、Perplexity、Bits-per-Byte 与 Tokenizer 公平比较]]", "[[语言模型评估对象、任务单位与 Benchmark 合同]]"]
sources: ["[[S-2023-Su-9752-BytePiece]]", "[[S-2018-Kudo-Subword-Regularization]]", "[[S-2025-Unicode-UAX29-Text-Segmentation]]"]
exercises: ["[[习题 - Tokenizer 评估、多语言公平、安全与证据地图]]"]
solutions: ["[[解答 - Tokenizer 评估、多语言公平、安全与证据地图]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-tokenizer-audit-fairness-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Tokenizer 评估、多语言公平、安全与证据地图

> [!abstract] 一句话结论
> Tokenizer 没有脱离语料、模型和预算的单一“最好”。合格评估同时报告可逆/覆盖、压缩与序列尾部、多语言/领域切片、训练与推理成本、下游质量、随机分段鲁棒性和控制通道安全，并把定义、实验和机制假说分开。

## 一、先定义评估单位

给评估集文档 $x_1,\ldots,x_n$，tokenizer $\mathcal T$。常见 denominator：

$$
B=\sum_i |x_i|_{bytes},\quad
C=\sum_i |x_i|_{codepoints},\quad
G=\sum_i |x_i|_{graphemes},\quad
T=\sum_i |\mathcal T(x_i)|.
$$

可计算：

$$\text{bytes/token}=B/T,\qquad
\text{tokens/grapheme}=T/G.$$

不同 denominator 回答不同问题。bytes 适合跨 tokenizer 的固定原始存储单位；grapheme 更接近用户感知字符；word fertility 依赖语言特定 word segmenter。报告“每字符”但不说明 $C$ 或 $G$ 不可验收。

## 二、六类指标总账

| 维度 | 指标示例 | 必须同时记录 |
|---|---|---|
| 可逆/覆盖 | round-trip failure、UNK/fallback rate | normalization 与错误策略 |
| 压缩 | bytes/token、tokens/grapheme | 均值、分位数、最长序列 |
| 词表 | size、有效使用率、频率尾部 | special/byte/reserved token 占比 |
| 计算 | embedding 参数、FLOPs、wall time、显存 | 固定文本还是固定 token 预算 |
| 质量 | BPB/NLL、下游任务、鲁棒性 | 模型容量、训练预算与 seed |
| 安全 | special injection、confusable、控制字符、DoS 长度 | threat model 与攻击适应性 |

更高 bytes/token 只说明序列更短，不说明模型概率更好；更少 UNK 也不说明尾部 token 长度合理。

## 三、公平性：比较分布，而不是总体平均

对语言/脚本/领域组 $g$，定义

$$F_g=\mathbb E[|\mathcal T(X)|/|X|_{grapheme}\mid G=g].$$

至少报告 $F_g$ 的均值、中位数、P95/P99 和文档截断率。总体平均

$$\sum_g\pi_gF_g$$

会被语料权重 $\pi_g$ 主导；英语占比高时，少数语言的高 fertility 可能被隐藏。还需切片：

- 拉丁/汉字/阿拉伯/南亚等 script；
- 形态丰富语言；
- emoji、数学、代码、URL；
- 口语、拼写变体、方言与低资源文本；
- normalization 前后和 byte fallback 区域。

> [!warning] “语言无关”不是公平结论
> 不使用语言特定规则只描述算法输入；公平需比较不同群体承担的 token、延迟、截断、价格和质量成本。

## 四、固定模型还是固定资源

比较 tokenizer A/B 可采用：

### 协议 1：固定架构与 token steps

模型 shape、训练 token 数相同，但 A/B 看到的 raw bytes 不同。适合问“每个 token step 的训练行为”，不适合问固定原始语料效率。

### 协议 2：固定 raw corpus 与 epoch

看到相同文本，但 token 数、steps、FLOPs 不同。适合数据等价，性能不等算力。

### 协议 3：固定总 FLOPs/wall time

调整 batch/steps 使资源近似相同，再比较 held-out BPB 与任务质量。最接近系统决策，但实现复杂，需要记录 kernel 和硬件。

最好同时报告三种，避免把某一预算下优势外推到全部场景。

## 五、Tokenizer 的安全测试

1. **控制通道**：用户字面文本能否生成 role/tool/system special ID；
2. **不可见字符**：零宽、双向控制、variation selector 是否改变边界或日志显示；
3. **confusable**：视觉相近标识是否被错误合并/混淆；
4. **长度放大**：短 grapheme 串是否产生极长 token 序列，形成费用/延迟 DoS；
5. **decode discrepancy**：skip_special_tokens、cleanup spaces 是否使审计日志与模型输入不一致；
6. **版本替换**：服务端 tokenizer/template 更新是否未改变模型名却改变请求 IDs。

安全不是 tokenizer 单独可解决的问题，但 tokenizer 是输入 trust boundary 的第一层。

## 六、证据地图

| 声明 | 证据类型 | 最低补证 |
|---|---|---|
| `decode(encode(x))=x` | `I`/实现不变量 | 明确输入域 + conformance/property tests |
| A 的 bytes/token 更高 | `E` | 同 raw corpus、normalization、词表预算与区间 |
| A 对某语言更公平 | `E/H` | 多切片成本与下游质量；定义公平目标 |
| 分段采样提高鲁棒性 | `E` | 多 seed、相同预算、域外/扰动集 |
| byte-based 因而语言无关 | `H` | 不能由 256-byte 覆盖恒等式直接推出 |
| tokenizer A 普遍更好 | 过强声明 | 至少给 Pareto frontier 与适用范围 |

[[S-2023-Su-9752-BytePiece]]中的压缩实验是很好的候选证据，但必须绑定其语料、词表、normalization 与实现；不能从 bytes/token 单指标推出模型质量或公平。

## 七、图：从平均压缩到分组审计

先看图回答：为什么总体 bytes/token 领先，仍可能让某些语言付出更高 token 成本？

![[00-知识库管理/_assets/figures/language-models/fig-lm-tokenizer-audit-fairness-v1.svg|900]]

> [!figure] 图 LM-08　Tokenizer 的多目标审计
> A 列出四类基础量，B 以示意 fertility 展示总体均值如何隐藏群体尾部，C 给出固定语料—模板—切片—资源的审计顺序。来源：本课程独立绘制；数值仅为示意，不代表真实语言统计。

**怎样读图**：先检查 round-trip 与 denominator，再按语言/域画分布，最后在固定 FLOPs 或 wall time 下进入模型质量比较。

**图没有证明什么**：该图只解释Tokenizer 的压缩、公平、安全与资源切片的结构和本节样例，不证明任意模型、数据、语言或部署环境都会得到同一性能；真实结论仍需独立实验、区间与版本化工件。


**图没有证明什么**：B 中数字是示意，不可作为任何真实 tokenizer 的公平结论。

## 八、最小实验设计

预注册：

```yaml
corpus: fixed documents + license + hash
unicode_version: ...
normalization: identity/NFC/...
tokenizers: model files + hashes + versions
groups: language/script/domain/attack slices
budgets: vocab, raw bytes, token steps, FLOPs, wall time
metrics: roundtrip, fertility quantiles, truncation, BPB, downstream
models: same architecture or parameter-matched variants
seeds: paired
primary_claim: one sentence that can fail
```

对 paired documents，比较 token length 差值，置信区间优先以文档/来源 block 为采样单位，而不是把每个 token 当独立样本。

## 九、卷内证据闭环

- Unicode 标准决定规范化和字素边界的 P0 定义；
- BPE/WordPiece/Unigram 原论文承担算法历史和实验；
- 科学空间承担中文推导、BytePiece 与随机分段假说；
- 官方 tokenizer/config 承担当前实现；
- 本卷确定性实验承担 toy corpus 的可复算 oracle；
- 下游规模结论必须另做模型训练，静态 tokenizer 指标不能替代。

下一卷从[[概率语言模型、链式法则与自回归因子化]]开始。任何 NLL/PPL 比较都要继承本节的 tokenizer 与 denominator 合同。

## 练习与独立解答

- [[习题 - Tokenizer 评估、多语言公平、安全与证据地图]]
- [[解答 - Tokenizer 评估、多语言公平、安全与证据地图]]

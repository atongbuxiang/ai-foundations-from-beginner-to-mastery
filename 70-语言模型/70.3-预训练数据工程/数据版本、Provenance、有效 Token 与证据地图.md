---
type: concept
status: verified
area: [language-models, pretraining-data, provenance, effective-tokens]
node_id: LM-24
aliases: [Data provenance, Effective tokens, 数据版本与谱系]
prerequisites: ["[[预训练语料来源、许可、隐私与文档单位合同]]", "[[Packing、文档边界、Position ID 与 Loss Mask]]", "[[Curriculum、持续预训练与域适配数据路径]]"]
related: ["[[Scaling 实验设计、外推不确定性与证据地图]]", "[[语言模型研究协议、Model-Data-System Card 与证据地图]]"]
sources: ["[[S-2013-W3C-PROV-DM]]", "[[S-2023-Longpre-Data-Provenance]]", "[[S-2021-Gebru-Datasheets]]", "[[S-2018-Bender-Data-Statements]]"]
exercises: ["[[习题 - 数据版本、Provenance、有效 Token 与证据地图]]"]
solutions: ["[[解答 - 数据版本、Provenance、有效 Token 与证据地图]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-data-provenance-effective-token-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# 数据版本、Provenance、有效 Token 与证据地图

> [!abstract] 一句话结论
> 一个可复现预训练数据集不是一个目录名，而是内容寻址的实体、版本化 transformation、责任 agent、选择/删除记录和分层计数构成的 provenance graph。只有从 raw bytes 一直追到有效 loss targets，“训练了多少 token”才有确定含义。

## 一、PROV 的三类核心对象

沿用 W3C PROV 的抽象：

- **Entity**：WARC record、parsed document、filter manifest、dedup cluster、tokenized shard、checkpoint；
- **Activity**：crawl、parse、classify、filter、dedup、tokenize、pack、train、delete；
- **Agent**：组织、系统、审核者、pipeline owner。

典型关系：activity `used` parent entities，entity `wasGeneratedBy` activity，child `wasDerivedFrom` parent，activity `wasAssociatedWith` agent。

$$
E_{WARC}\overset{A_{parse}}{\longrightarrow}E_{text}
\overset{A_{filter}}{\longrightarrow}E_{kept}
\overset{A_{tokenize}}{\longrightarrow}E_{ids}
\overset{A_{pack}}{\longrightarrow}E_{shard}.
$$

Graph 可表达 lineage，不保证声明真实；仍需要 immutable logs、权限、review、签名和独立抽查。

## 二、内容寻址与 manifest

路径 `data/final-v2/` 会被覆盖或移动，不能唯一标识内容。对每个 immutable artifact 保存 cryptographic digest：

$$
h(E)=\operatorname{SHA256}(\operatorname{canonical\_bytes}(E)).
$$

Manifest 至少含：

```yaml
artifact_hash: ...
schema_version: ...
parent_hashes: [...]
activity: {code_commit, container, config_hash, seed, started_at, ended_at}
counts_and_slice_stats: ...
rejection_or_cluster_manifest: ...
rights_privacy_approvals: ...
agent_and_review: ...
```

大型 shards 可用 Merkle tree：叶为 records/chunks hash，根标识全集；局部删除/差分生成新根并保留旧→新 proof。Hash 证明 bytes 相同，不证明语义、许可或 parser 正确。

## 三、数据版本不是一个整数

以下任一变化都应生成新数据版本：

- raw crawl IDs/下载快照；
- parser、normalization、LID/filter model/threshold/order；
- dedup shingles/hash/LSH/representative；
- benchmark exclusion list 与 cutoff；
- domain taxonomy/mixture/schedule；
- tokenizer、special tokens、document boundaries；
- packing、position/loss policy；
- deletion/appeal 与 license evidence。

可用语义化标签作人类接口，但复现身份必须由完整 manifest hash 给出。`v3` 在两个实验中未必同内容。

## 四、“Token 数”有六种以上

逐层记账：

1. raw bytes $B_{raw}$；
2. parsed text bytes/code points $B_{text}$；
3. retained documents $N_{doc}$；
4. unique/canonical documents 或 raw unique tokens $T_{unique}$；
5. tokenizer 输出 model tokens $T_{model}$；
6. sampler 实际 draws/exposures $T_{draw}$；
7. packed tensor positions $T_{packed}$；
8. effective loss targets

$$
T_{eff}=\sum_{b,t}m_{bt}.
$$

训练总 NLL：

$$
N=\sum_{b,t}m_{bt}\ell_{bt},
\qquad \bar\ell=N/T_{eff}.
$$

Scaling law 里的 $D$ 必须注明是哪一种。若 padding、prompt、MLM mask rate 或 response-only loss 不同，相同 $T_{packed}$ 可有不同 $T_{eff}$。

## 五、去重、重复与“有效”不能只用一个数

“有效 token”有两种含义常冲突：

- **计分定义**：loss mask 为 1 的 target，精确可数；
- **信息/质量含义**：对学习有多少独立、有用信息，无法由一个通用公式直接观察。

去重后 unique-token 比例增加，不意味着 token 信息独立；相邻文本、同源 paraphrase 与模板仍相关。反之 repeated token 也可用于优化收敛。应使用不同字段：`loss_eligible_tokens`、`unique_content_tokens`、`exposure_tokens`、`estimated_information_proxy`，不把 proxy 命名为 exact effective tokens。

### 域级总账

对每域 $g$ 保存

$$
(B_g,N_g,T_{unique,g},T_{draw,g},T_{eff,g},NLL_g,FLOPs_g).
$$

它连接 LM-21 mixture 与实际贡献。若只有全局 $T_{eff}$，低资源域可能被长文、高 fertility 或 ignore policy 隐藏。

## 六、删除与可追溯影响

收到合法删除/纠错请求时，至少回答：

1. 哪些 raw/source entities 命中？
2. 经哪些 parse/dedup cluster 派生为哪些 documents？
3. 哪些 token shards 与 training runs 使用过？
4. 删除生成哪个新 manifest/hash？
5. 旧 checkpoints 仍受何影响，采用 retrain/unlearning/限制/记录哪种处置？

不能真正从已训练 checkpoint“删除一个 token”而只改数据目录。Data deletion、model unlearning 与 deployment mitigation 是三层 activity，证据分别记录。

为了支持删除而永久保存敏感原文可能违反最小化原则。可采用受控 raw vault、pseudonymous deletion keys、hash/secure index 与有限保留期；设计需经隐私/安全审批。

## 七、数据卡与 provenance graph 的分工

- Datasheet/Data Statement：面向人解释动机、组成、收集语境、群体、用途、风险与维护；
- Provenance graph/manifest：面向机器重放实体、活动、版本与 derivation；
- Audit report：记录抽查、失败、未知字段、权利/隐私决定与责任人；
- Model/Data/System card：把数据版本连接到 checkpoint、训练和部署结果。

只做漂亮数据卡但没有 hashes 无法重放；只有 hashes 没有语境与风险也无法判断适用性。

## 八、证据等级

| 主张 | 类型 | 最低证据 |
|---|---|---|
| shard bytes 未变 | `I/O` | cryptographic hash 与 canonical serialization |
| pipeline 可重放 | `E` | clean-room rerun 与 artifact equality/diff |
| filter 提升某模型结果 | `E` | 固定预算对照、多 seed、slice metrics |
| 数据许可适用于用途 | 专业判断 | 来源证据、法域/用途、资格审查；非纯 ML 定理 |
| 数据无隐私风险 | 过强主张 | 不可由一次 PII scan 证明；改为 threat-model 范围 |
| 更多有效 token 导致提升 | `H/E` | 明确 token 定义、scale/mixture 控制与实验 |

Provenance 提高可证伪性，但不把经验相关变成因果定理。

## 九、图：从 lineage 到 token 瀑布

先看图回答：图中 `100M raw bytes` 到 `42M loss targets` 的每一步为什么都需要不同单位和 hash？

![[00-知识库管理/_assets/figures/language-models/fig-lm-data-provenance-effective-token-v1.svg|900]]

> [!figure] 图 LM-24　Entity–Activity lineage 与有效 token 瀑布
> 上方由 WARC、parsed text、kept corpus、tokenized、packed、shard 构成有向 provenance；下方逐层计 raw/parsed/filtered/unique/packed/loss。来源：本课程依据 W3C PROV-DM、Datasheets 与 Data Provenance Initiative 独立绘制；数字为教学构造。

**怎样读图**：从最终 shard 逆向沿 parent hashes 回到 raw entity，再顺向核对每层 count 的单位、拒绝 manifest 和 agent；不要把柱高差都叫“清洗掉的噪声”。

**图没有证明什么**：hash 与 graph 不认证输入权利、隐私或质量；toy waterfall 不代表真实数据损耗，也不定义信息论上的独立样本量。

## 十、本卷最小 manifest 门

- 任意最终 token shard 可回到 raw/capture parent；
- 每个 activity 的 code/config/container/seed/hash 可定位；
- keep/reject/dedup/exclusion manifests 齐全且受控；
- data/version、tokenizer、mixture、packing 与 checkpoint 双向链接；
- raw bytes、documents、unique、draw、packed、effective targets 分列；
- per-domain/语言/来源切片计数可重算；
- 删除产生新版本并保留 tombstone/impact report；
- data card 写明 unknowns、intended/prohibited use、维护责任与复审日期；
- clean-room 复跑能得到相同 hash，或解释每一处 diff。

## 十一、本节出口

你应能用 Entity–Activity–Agent 图重建数据谱系，区分六类以上规模数，计算 $T_{eff}$，并设计可重放与删除影响报告。完成[[70.3 预训练数据工程 MOC]]后，你已具备进入指令适配数据前的最低数据研究资格。

## 练习与独立解答

- [[习题 - 数据版本、Provenance、有效 Token 与证据地图]]
- [[解答 - 数据版本、Provenance、有效 Token 与证据地图]]

---
type: solution
status: verified
area: [language-models, pretraining-data, provenance]
topic: "[[数据版本、Provenance、有效 Token 与证据地图]]"
exercise: "[[习题 - 数据版本、Provenance、有效 Token 与证据地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - 数据版本、Provenance、有效 Token 与证据地图

## A. 识别与复述

### LM24-A01
PROV Entity 是可描述的对象/状态，如 WARC snapshot、parsed shard；Activity 是对实体发生的过程，如 crawl、dedup；Agent 是承担责任的主体，如 crawler service、审核者/组织。关系要表达哪些 entity 被 activity 使用/生成、activity 与 agent 如何关联。

### LM24-A02
Raw bytes 是抓取载荷；unique tokens 是去重后唯一内容的 tokenizer 计数；draw tokens 含训练重复抽样；packed positions 含真实 token、special/pad 等物理位置；effective targets 是 loss mask 为 1、真正进入目标归一化的位置。五个量回答不同问题，通常不相等。

### LM24-A03
Datasheet 是面向人类的动机、组成、采集、用途、维护与限制说明，帮助责任沟通；machine-readable provenance graph 给可计算 IDs、hash、版本和 derivation edges，支持追溯、差分和影响分析。一个提供语义叙事，一个提供可执行链路，不能互相替代。

## B. 手算与构造

### LM24-B01
两 mask 的和分别为 3 与 1，故 $T_{eff}=4$。若这些有效位置的 NLL 总和为 6，全局 mean NLL 为 $6/4=1.5$；不能除以两个 batch 或八个物理位置。

### LM24-B02
可写：`E0 WARC(hash h0) --A1 parse(parser p)→ E1 text(hash h1) --A2 filter(config f)→ E2 kept-manifest(h2) --A3 dedup(config d)→ E3 unique-manifest(h3) --A4 tokenize(tok t)→ E4 token-shard(h4) --A5 pack(mask/position v)→ E5 packed-batch-manifest(h5)`。每个 activity 关联 code/config/container agent；每个子 entity 保存 parent ID/offset/reason。

### LM24-B03
相邻比率依次是 parsed/raw $80/100=0.8$；filtered/parsed $60/80=0.75$；unique/filtered $45/60=0.75$。draw/unique $50/45\approx1.1111$ 是平均抽样 exposure 比，不应称 retention；targets/draw $42/50=0.84$ 是有效 target fraction。Bytes 与 tokens 若单位不同则前几步只能在各自同单位定义下比较。

## C. 推导与证明

### LM24-C01
在固定 hash 算法与 canonical serialization 下，同 digest 提供“内容相同”的强计算证据，并可验证下载/传输未变；它不证明来源真实、解析正确、许可有效、无 PII、语义等价或数据代表性。碰撞假设与所 hash 的边界也必须声明。

### LM24-C02
取同一四个 packed positions，mask $m=(1,1,1,1)$ 时 $T_{eff}=4$；mask $m'=(1,0,1,0)$ 时 $T_{eff}=2$。物理张量完全相同，仅 objective contract 不同就改变分母与梯度。因此“训练了 N positions”不唯一决定学习信号规模。

### LM24-C03
把 shard hashes 作为叶子，两两 hash 到 Merkle root。修改一个 record 只会改变其叶子及到根的一条路径，产生新 root；比较两版本路径可定位不同子树，未变子树用旧 hash 复用。Root 证明集合/顺序承诺，仍需 manifest 解释叶子语义与序列化。

## D. 边界、反例与纠错

### LM24-D01
`final-v3` 不编码 parent、内容 digest、生成代码、配置、tokenizer、顺序或时间，同名目录可被覆盖且不同机器可不同。最低要求是 immutable manifest、content hashes、lineage、environment 和生成命令；人类标签只能作别名。

### LM24-D02
去重只按某 similarity/object unit 减少重复表示；paraphrases、事实冗余与同源衍生仍相关，反之相同 boilerplate 也可能被误删。Unique tokens 是 pipeline-relative count，不是 Shannon 信息、独立样本数或有效样本量的同义词。

### LM24-D03
删除 shard 不能撤销已训练参数中的影响，派生 cache、packed manifests、checkpoints 和发布模型仍存在。声明必须区分 source deletion、future-run exclusion、artifact purge、checkpoint retrain/unlearning 与无法撤销部分，并输出 data→run→checkpoint impact report。

## E. AI 迁移

### LM24-E01
最小 manifest 可含 `dataset_id, parent_manifest_hash, created_at, source_snapshot_ids, schema_version, ordered_shards[{uri,bytes,sha256,records}], transforms[{code,config,container}], tokenizer_hash, counts{raw,parsed,unique,draw,effective_targets}, rights/privacy status, exclusions, approver`，对 canonical manifest 自身再计算 hash。

### LM24-E02
从 deletion key 查 source/entity IDs，沿 `wasDerivedFrom/wasGeneratedBy/used` 正向遍历到 parsed docs、dedup representatives、token shards、packed batches、runs 与 checkpoints。报告每节点 hash、状态、可删除性、已执行动作和残余风险；生成新 exclusion manifest，并为受影响未来 runs 阻断。

### LM24-E03
“1T tokens”若无 tokenizer/version，无法复算 tokenization；无 unique/draw 区分，无法知重复 exposure；无 loss mask，无法知 $T_{eff}$；无 document/domain shares，无法知分布。模型卡应至少并列 unique model tokens、draw tokens、packed positions、effective targets 与 tokenizer/manifest hashes；否则规模只能标为未定义计数。

## 无提示重做

- [ ] 从 loss mask 计算全局 effective-target mean。
- [ ] 画 source entity 到 checkpoint 的可遍历 provenance DAG。


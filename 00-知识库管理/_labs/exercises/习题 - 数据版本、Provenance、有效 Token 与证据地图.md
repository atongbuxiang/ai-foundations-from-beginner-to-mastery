---
type: exercise
status: verified
area: [language-models, pretraining-data, provenance]
topic: "[[数据版本、Provenance、有效 Token 与证据地图]]"
solution: "[[解答 - 数据版本、Provenance、有效 Token 与证据地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 数据版本、Provenance、有效 Token 与证据地图

## A. 识别与复述

### LM24-A01
定义 PROV Entity、Activity、Agent 并各举两个本卷实例。

### LM24-A02
区分 raw bytes、unique tokens、draw tokens、packed positions 与 effective targets。

### LM24-A03
Datasheet 与 machine-readable provenance graph 各解决什么？

## B. 手算与构造

### LM24-B01
给两 batch loss masks `[1,1,0,1]`、`[1,0,0,0]`，算 $T_{eff}$；若 NLL 和为 6 算 mean。

### LM24-B02
构造 WARC→parse→filter→dedup→tokenize→pack 的 entities/activities 图。

### LM24-B03
raw 100M bytes→80M parsed→60M filtered→45M unique→50M draws→42M targets，计算各相邻 retention。

## C. 推导与证明

### LM24-C01
说明 cryptographic hash 能证明哪些 equality，又不能证明哪些语义。

### LM24-C02
证明相同 packed positions 在不同 loss mask 下可有不同 $T_{eff}$。

### LM24-C03
说明 Merkle root 如何允许局部变更产生新版本并定位差异。

## D. 边界、反例与纠错

### LM24-D01
反驳“目录名 final-v3 足以复现数据集”。

### LM24-D02
反驳“去重后 unique tokens 就等于独立信息量”。

### LM24-D03
指出只删数据 shard、不处理已有 checkpoint 的删除声明问题。

## E. AI 迁移

### LM24-E01
写一个最小 content-addressed manifest。

### LM24-E02
设计删除请求的 data→shard→run→checkpoint impact report。

### LM24-E03
审计“训练 1T tokens”但无 tokenizer/unique/draw/loss 定义的规模声明。

独立完成后查看[[解答 - 数据版本、Provenance、有效 Token 与证据地图]]。

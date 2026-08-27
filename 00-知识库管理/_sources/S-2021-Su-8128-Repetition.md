---
type: source
status: verified
area: [sources, scientific-spaces, language-models]
source_type: blog
title: "Seq2Seq重复解码现象的理论分析尝试"
author: "苏剑林"
year: 2021
url: "https://spaces.ac.cn/archives/8128"
accessed: 2026-08-26
source_tier: P3
license: "CC BY-NC-SA indicated by site; independent summary"
scope_role: chinese-markov-analysis
related: ["[[EOS、停止规则、重复惩罚与退化循环]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 科学空间 8128：二元马尔可夫近似下的重复环

> [!abstract] 来源定位
> 文章以固定转移矩阵分析重复子序列概率，讨论截断后非零率、谱量与循环风险，并明确一般自回归模型只在额外近似下与该二元模型联系。

课程采用构造性小模型和其边界，不把“稀疏截断导致重复”写成所有 LLM repetition 的唯一原因。

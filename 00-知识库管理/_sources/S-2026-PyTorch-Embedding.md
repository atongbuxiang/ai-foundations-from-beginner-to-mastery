---
type: source
status: active
area: [sources, neural-networks, embedding, sparse-gradients, pytorch]
source_type: official-docs
title: "PyTorch Embedding"
author: "PyTorch Contributors"
year: 2026
url: "https://docs.pytorch.org/docs/stable/generated/torch.nn.Embedding.html"
accessed: 2026-08-29
source_tier: B
license: "PyTorch official documentation；本库仅保存独立摘要、接口事实与链接"
scope_role: implementation-contract
temporal_role: current-api
related: ["[[Embedding Lookup、稀疏梯度与参数规模]]", "[[Padding、Mask、特殊符号与词表边界]]", "[[Embedding 初始化、缩放、分解与量化接口]]"]
created: 2026-08-24
updated: 2026-08-29
---

# PyTorch：Embedding 实现合同

> [!abstract] 来源定位
> 官方文档定义 `Embedding(num_embeddings, embedding_dim, ...)` 的当前 shape、`padding_idx`、`max_norm`、`scale_grad_by_freq` 与 `sparse` 语义。它承担框架事实；lookup 等价、row-gradient 累加与参数规模由本库独立推导，版本相关的 optimizer 支持不得外推为永久事实。

## 当前接口事实

- 权重形状为 $(V,d)$；任意整数索引 shape $S$ 输出 shape $S+(d,)$；
- `padding_idx` 对应行默认不贡献梯度；
- `scale_grad_by_freq=True` 按 mini-batch 内词频反向缩放；
- `sparse=True` 使 weight gradient 使用稀疏表示，但不保证所有后续 optimizer/regularizer 都保持稀疏；
- `max_norm` 会在 forward 中原位重归一化被访问的行，因此与对 weight 的其他可微操作存在顺序/clone 边界；
- 访问日文档列出的 sparse-gradient optimizer 支持有限，必须随框架版本复核。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| PTE-C1 | 输入索引 shape 后追加 embedding dimension | API | 当前 PyTorch | 版本内成立 |
| PTE-C2 | `sparse=True` 让全部训练过程都为稀疏计算 | 系统外推 | optimizer、decay、通信可能 densify | 错误 |
| PTE-C3 | `padding_idx` 行不由 lookup backward 更新 | API | 当前实现合同 | 版本内成立 |
| PTE-C4 | `max_norm` 只是无状态读取 | API 误读 | forward 可原位修改 weight | 错误 |

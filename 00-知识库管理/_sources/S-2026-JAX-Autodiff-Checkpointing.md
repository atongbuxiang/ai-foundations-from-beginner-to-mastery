---
type: source
status: active
area: [sources, automatic-differentiation, software/jax]
source_type: documentation
title: "The Autodiff Cookbook and Control Autodiff Saved Values with jax.checkpoint"
author: [JAX Authors]
year: 2026
url: "https://docs.jax.dev/en/latest/notebooks/autodiff_cookbook.html"
accessed: 2026-08-23
source_tier: B
venue: "JAX official documentation"
scope_role: implementation
temporal_role: current-interface
related: ["[[Forward_Reverse AD、Tape 与复杂度]]", "[[Gradient Checking、Checkpointing 与高阶微分边界]]"]
created: 2026-08-23
updated: 2026-08-23
---
# JAX 2026：Autodiff Cookbook 与 Checkpoint/Remat
> [!abstract] 来源定位
> JAX 官方实现语义入口，用于 JVP/VJP/HVP 组合、PyTree 和伴随测试，并通过 [`jax.checkpoint`/`jax.remat`](https://docs.jax.dev/en/latest/notebooks/autodiff_remat.html) 说明 residual 保存—重算语义。这是当前 API 证据，不替代 AD 复杂度定理或任意程序 effects 的正确性证明。

---
type: source
status: active
area: [sources, learning-theory, gaussian-processes, kernel-methods]
source_type: book
title: "Gaussian Processes for Machine Learning"
author: [Carl Edward Rasmussen, Christopher K. I. Williams]
year: 2006
url: "https://gaussianprocess.org/gpml/chapters/"
accessed: 2026-08-23
source_tier: A
license: "MIT Press open web edition; retain citation and independent derivations"
edition: "Second printing web version"
scope_role: primary-textbook
temporal_role: classical-foundation
related: ["[[核岭回归与 Gaussian Process 接口]]", "[[正定核、RKHS 与表示定理]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Gaussian Processes for Machine Learning

> [!abstract] 来源定位
> GPML 是 Gaussian-process regression、covariance functions、posterior prediction、marginal likelihood、RKHS/regularization 关系与低秩 approximation 的权威开放专著。它承担本库 KRR 与 GP “posterior mean 形式相同，但 probability object 不同”的正式桥梁。

## 元数据与纳入

- 官方章节：[GPML web edition](https://gaussianprocess.org/gpml/chapters/)；
- MIT Press DOI：[10.7551/mitpress/3206.001.0001](https://doi.org/10.7551/mitpress/3206.001.0001)；
- 正式引用：Rasmussen, C. E. & Williams, C. K. I. (2006), MIT Press；
- 证据角色：weight/function-space GP、regression posterior、marginal likelihood、covariance design、KRR/RKHS relationship 与 approximation；
- 边界：GP posterior calibration 依 prior/likelihood/hyperparameter correctness，不由 closed-form algebra 自动保证。

## 本库调用的断言

1. Gaussian prior 与 Gaussian observation noise 给 closed-form posterior mean/covariance；
2. 匹配尺度后 GP posterior mean 与 KRR estimator 具有相同 Gram formula；
3. GP 额外定义 posterior covariance、marginal likelihood 与 joint predictive law；
4. covariance hyperparameters 可用 marginal likelihood/CV 选择，但 selection uncertainty 与 misspecification 仍需审计；
5. Cholesky、low-rank 与 inducing approximations 改变 computation，并可能改变 statistical target。

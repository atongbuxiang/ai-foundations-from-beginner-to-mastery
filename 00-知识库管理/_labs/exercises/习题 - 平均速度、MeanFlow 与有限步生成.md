---
type: exercise
status: draft
area: [generative-models, meanflow]
topic: "[[平均速度、MeanFlow 与有限步生成]]"
solution: "[[解答 - 平均速度、MeanFlow 与有限步生成]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - 平均速度、MeanFlow 与有限步生成
## A. 识别与复述
### GEN70-A01
区分 instantaneous velocity、average velocity 与 finite map。
### GEN70-A02
average velocity 的积分必须沿哪条路径？
### GEN70-A03
写出 $D_tu$ 的 JVP 展开与固定变量。
## B. 手算与建模
### GEN70-B01
对 $\dot z=2$，求任意区间平均速度与 finite update。
### GEN70-B02
对 $\dot z=z,z_0=1,[0,1]$，比较真实平均速度与端点速度算术平均。
### GEN70-B03
若 $u(z,r,t)=2z+t$、$v(z,t)=z-t$，计算固定 $r$ 的 $D_tu$。
## C. 推导与证明
### GEN70-C01
从积分定义推导 $z_r=z_t-(t-r)u$。
### GEN70-C02
逐步推导 $u=v-(t-r)D_tu$。
### GEN70-C03
在连续性条件下证明 $r\uparrow t$ 时 $u\to v$。
## D. 边界、反例与纠错
### GEN70-D01
反驳“average velocity 就是两端 velocity 的平均”。
### GEN70-D02
解释 endpoint residual 小为何不决定中间 trajectory。
### GEN70-D03
为什么 learned $u_\theta$ 不自动给 continuous likelihood？
## E. AI 迁移
### GEN70-E01
设计 identity/boundary/composition residual 单元测试。
### GEN70-E02
审计 MeanFlow JVP 实现的切向量和 stop-gradient。
### GEN70-E03
比较预测 endpoint、instantaneous velocity、average velocity 的数值条件数。
## 解答入口
[[解答 - 平均速度、MeanFlow 与有限步生成]]

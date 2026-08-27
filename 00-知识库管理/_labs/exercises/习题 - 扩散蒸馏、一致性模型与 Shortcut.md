---
type: exercise
status: draft
area: [generative-models, distillation, consistency]
topic: "[[扩散蒸馏、一致性模型与 Shortcut]]"
solution: "[[解答 - 扩散蒸馏、一致性模型与 Shortcut]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - 扩散蒸馏、一致性模型与 Shortcut
## A. 识别与复述
### GEN69-A01
分别说出 progressive distillation、consistency model、Shortcut 的监督对象。
### GEN69-A02
consistency model 的 boundary condition 是什么？
### GEN69-A03
SiD 的 conditional-expectation identity 对 $f$ 有什么依赖限制？
## B. 手算与建模
### GEN69-B01
teacher 小步 map $T_h(x)=.9x+1$。求两步 teacher target，并拟合 affine student $F_{2h}(x)=ax+b$。
### GEN69-B02
$v(x,t,h)=x+h$。计算一次 $2h$ 与两次 $h$ 的 endpoint residual。
### GEN69-B03
常数 map $F_h(x)=c$ 的 composition residual 是多少？它说明什么？
## C. 推导与证明
### GEN69-C01
写出 progressive two-to-one distillation loss 与 stop-gradient。
### GEN69-C02
由“同轨迹同端点”推出相邻时间 consistency equality。
### GEN69-C03
展开 Shortcut 的 $F_{t,2h}=F_{t+h,h}\circ F_{t,h}$ 得 velocity target。
## D. 边界、反例与纠错
### GEN69-D01
反驳“student 拟合 teacher 就等于真实 data transport”。
### GEN69-D02
为什么 pairwise consistency loss 小不保证 off-trajectory 正确？
### GEN69-D03
纠正“所有 1-NFE 方法只是不同名字的蒸馏”。
## E. AI 迁移
### GEN69-E01
设计 on/off-trajectory composition audit。
### GEN69-E02
列出 progressive distillation 每一 stage 的必报量。
### GEN69-E03
为 consistency distillation 与 consistency training 设计公平对照。
## 解答入口
[[解答 - 扩散蒸馏、一致性模型与 Shortcut]]

---
type: solution
status: draft
topic: "[[扩散 SDE、ODE Solver、步长与 NFE 总账]]"
exercise: "[[习题 - 扩散 SDE、ODE Solver、步长与 NFE 总账]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - 扩散 SDE、ODE Solver、步长与 NFE 总账
## A. 识别与复述
### GEN68-A01
local truncation error 是从精确当前点做一步的误差；global error 是多步传播后的终点误差；field error 是 $v_\theta-v$，即使连续精确积分 learned ODE 也存在。
### GEN68-A02
Euler 常为 1 NFE/step，Heun 2，RK 更多；multistep 有 warm-up，adaptive 有 rejected steps，guidance 可能要额外网络/反向。必须计实际函数调用。
### GEN68-A03
strong error 比同一 Brownian path 的轨迹；weak error比终点测试函数期望；Monte Carlo error来自用有限生成样本估计这些期望/指标。
## B. 手算与建模
### GEN68-B01
Euler：$1+.5(1)=1.5$，误差 $1.5-e^{.5}\approx-.14872$。Heun predictor $1.5$，corrector $1+.25(1+1.5)=1.625$，误差约 $-.02372$。
### GEN68-B02
Euler 20 步；Heun 10 步；multistep 先花 3 NFE 后还剩 17 次主循环评估，即 17 个 main steps。warm-up 本身推进多少时间取决于具体启动法，需另报。
### GEN68-B03
$h_3=.5-1=-.5$，$h_2=.1-.5=-.4$，$h_1=0-.1=-.1$。
## C. 推导与证明
### GEN68-C01
Euler 与 exact Taylor 差首项为 $h^2x''/2$。Heun 将 $v(x+hv,t+h)$ 展开为 $v+h(v_t+J_vv)+O(h^2)$，平均斜率给 $hv+h^2(v_t+J_vv)/2+O(h^3)$，匹配 Taylor 到二阶。
### GEN68-C02
令 $e(t)=x(t)-\tilde x(t)$，则 $\|e'\|\le L\|e\|+\|e_\theta(\tilde x,t)\|$。Gronwall 得 $\|e(0)\|\le e^{LT}[\|e(T)\|+\int_0^T\|e_\theta\|dt]$（时间方向重参数化后同式）。
### GEN68-C03
已知线性部分可解析积分，避免数值法重复近似其快速/刚性结构，并把误差集中在 neural integral 的插值；但 integrand 本身若由错误 $v_\theta$ 给出，解析积分仍精确积分“错误场”。
## D. 边界、反例与纠错
### GEN68-D01
同 20 NFE，Euler 可做 20 小步，Heun 仅 10 步；若 field 不光滑、误差常数大、model error 主导或 Heun evaluation 更慢，二阶法不必更优。order 是 $h\to0$ 渐近陈述。
### GEN68-D02
$f(s)=(\cos s,\sin s)$ 在 $[0,2\pi]$ 的积分平均为 $(0,0)$，但任意 $s$ 的 $f(s)$ 范数为 1，不存在共同 $s^*$ 使 $f(s^*)$ 等于平均。
### GEN68-D03
大 CFG 放大 conditional difference 与曲率，可能把轨迹推入训练外区域并形成更快变化/近刚性段；原 grid 的误差分配不再合适，solver 排名也可能改变。
## E. AI 迁移
### GEN68-E01
先用有解析解的线性/非线性 ODE 测 order；再固定同一 learned field checkpoint 测 solver-only；最后与 oracle field 比较分出 model error。每层用相同端点、grid family 与 NFE。
### GEN68-E02
字段：denoiser/classifier/JVP NFE，accepted/rejected steps，warm-up/corrector，batch、precision、hardware、compile、latency p50/p95、throughput、memory、energy（若有）与 quality CI。
### GEN68-E03
追问 checkpoint/prediction type、SDE/ODE、grid/endpoints、NFE 而非 steps、guidance/threshold、teacher/tuning cost、hardware/precision、sample count/evaluator、P/R/conditionality 与 seed/CI。

---
type: concept
status: verified
area: [language-models, decoding, inference-acceleration]
node_id: LM-55
aliases: [推测解码, Speculative Sampling]
prerequisites: ["[[Logits、Softmax、Temperature 与 Categorical Sampling]]", "[[Prefill、Decode、KV Cache 与 Continuous Batching]]"]
related: ["[[Grammar-constrained Decoding、Schema 与结构化输出]]", "[[解码质量、延迟、吞吐、随机性与证据地图]]"]
sources: ["[[S-2023-Leviathan-Speculative-Decoding]]", "[[S-2023-Chen-Speculative-Sampling]]"]
exercises: ["[[习题 - Speculative Decoding、Acceptance 与分布精确性]]"]
solutions: ["[[解答 - Speculative Decoding、Acceptance 与分布精确性]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-speculative-acceptance-waterfall-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Speculative Decoding、Acceptance 与分布精确性

> [!abstract] 一句话结论
> 小 draft 模型先廉价提出若干 token，大 target 模型并行验证；精确的接受—残差校正可以保持 target 的采样分布。加速来自“每次昂贵验证推进多个 token”，不是省略 target 的概率判断。

## 一、为什么可能加速

普通自回归 decode 每轮只让 target 前进一步，且下一步依赖上一步 token。若 draft 模型便宜，可串行提出 $\gamma$ 个候选；target 对这一整段做一次前向，得到各位置的验证分布。若前若干 draft token 被接受，一次 target 调用便推进多个位置。

但 wall-clock speedup 不是接受率本身。近似写成

$$
\text{speedup}
\approx
\frac{\mathbb E[\text{committed tokens per round}]\,C_T(1)}
{C_D(\gamma)+C_T(\gamma)+C_{\mathrm{verify}}},
$$

其中 $C_T(\gamma)$ 受硬件并行、batch、KV、序列长度影响，并不等于 $\gamma C_T(1)$。draft 太大或接受率太低都可能没有收益。

## 二、单步接受—校正算法

先固定同一历史 $h$。target 分布为 $p(x)$，draft 分布为 $q(x)$。

1. 采样候选 $X\sim q$；
2. 以

$$
a(X)=\min\left(1,\frac{p(X)}{q(X)}\right)
$$

接受；
3. 若拒绝，则从 residual 分布

$$
r(x)=
\frac{(p(x)-q(x))_+}
{\sum_u(p(u)-q(u))_+}
$$

重新采样。

这里 $(z)_+=\max(z,0)$。实现时不能盲算 $p/q$：对 $q(x)=0$ 的 token，它不会由 draft 提出，但 target 多出的质量会进入 residual。

## 三、为什么输出恰好服从 target

候选 $x$ 被提出并接受的概率质量为

$$
q(x)a(x)
=q(x)\min\left(1,\frac{p(x)}{q(x)}\right)
=\min(p(x),q(x)).
$$

总拒绝概率为

$$
R=1-\sum_x\min(p(x),q(x))
=\sum_x(p(x)-q(x))_+.
$$

拒绝后产生 $x$ 的无条件质量是 $Rr(x)=(p(x)-q(x))_+$。两条路径相加：

$$
\Pr(Y=x)
=\min(p(x),q(x))+(p(x)-q(x))_+
=p(x).
$$

这就是单步的分布精确性。平均接受概率为

$$
\alpha=\sum_x\min(p(x),q(x))
=1-\operatorname{TV}(p,q),
$$

其中 $\operatorname{TV}(p,q)=\tfrac12\sum_x|p(x)-q(x)|$。draft 越接近 target，重叠质量越大。

## 四、多 token waterfall

draft 从当前 history 依次提出 $x_1,\ldots,x_\gamma$，target 一次计算对应位置的 $p_1,\ldots,p_\gamma$。验证从左到右：

- $x_i$ 接受后，下一位置仍以包含 $x_i$ 的同一 history 验证；
- 首次拒绝位置用该位置 residual 采样，然后丢弃其后的 draft token；
- 若全部接受，一些算法再从 target 的“bonus”位置采一个 token；
- EOS、grammar、penalty、top-$p$ 等 processor 必须在 draft/target 概率定义中一致处理。

不能先独立接受所有位置再拼接，因为后面分布依赖前面的真实历史。waterfall 的首拒绝原则维持自回归条件链。

## 五、“exact”到底精确什么

论文中的 exact/distribution preserving 通常表示：在算法假设、相同 target sampling kernel 与理想数值下，输出序列分布与逐 token target sampling 相同。它不自动表示：

- 相同 seed 必得逐字节相同输出；
- 不同 GPU、batch scheduler 或 kernel 的浮点结果相同；
- greedy 与 sampling 版本可混用同一证明；
- draft 和 target 使用不同 tokenizer/stop/grammar 仍精确；
- speculative server 与基线具有相同延迟分布。

要验证分布精确性，应在小词表上枚举理论概率，并用大量独立样本做频率区间或两样本检验；固定一个 seed 比较一条字符串不是分布证据。

## 六、系统收益的决定因素

需要同时记录：

| 变量 | 为什么重要 |
|---|---|
| $\gamma$ | 候选越长，潜在推进越多，也更易在中途拒绝 |
| draft/target cost ratio | draft 不够便宜会吃掉收益 |
| acceptance by position | 后部候选只有在前部全过时才有价值 |
| target verification shape | 硬件能否高效并行验证 |
| batch/concurrency | 高负载下验证可能与普通 batching 竞争 |
| KV policy | 被拒绝候选的临时 KV 如何回滚/复用 |
| processors | 动态 grammar、penalty 会影响两模型一致性与接受率 |

理想化地，若每个位置独立以常数 $\alpha$ 接受，至少提交 $k$ 个 draft token 的概率为 $\alpha^k$，期望接受数为

$$
\mathbb E[A]=\sum_{k=1}^{\gamma}\alpha^k
=\frac{\alpha(1-\alpha^\gamma)}{1-\alpha}.
$$

这只是诊断近似；真实接受事件随位置和 history 改变，不能用单一平均 $\alpha$ 代替 trace。

## 七、图解：接受质量与 residual 瀑布

**读图问题**：draft 与 target 的重叠质量怎样被接受，target 多出的概率缺口又怎样在首次拒绝后被 residual 精确补回？

![[00-知识库管理/_assets/figures/language-models/fig-lm-speculative-acceptance-waterfall-v1.svg|900]]

> [!figure] 图 LM-55　单步质量分解与多 token 首拒绝流程
> **生成：**本库按 $\min(p,q)$、$(p-q)_+$ 与首拒绝算法确定性绘制；左侧为质量分解，右侧为多 token 教学执行轨迹。

**怎样读图**：先逐 token 把接受路径的重叠质量与拒绝路径的 target 缺口相加，核对结果恰为 $p$；再沿右侧 waterfall 找首次拒绝位置和所有被丢弃后缀。

**图没有证明什么**：质量守恒只支持算法假设下的分布精确，不等于任意硬件、kernel 或 scheduler 上固定 seed 字节一致，也不保证加入 draft 与回滚开销后 wall-clock 一定加速。

## 八、常见错误与出口标准

错误包括：把 accept rate 当 speedup；拒绝后从 $p$ 而非 residual 采样；忽略 $q=0$；并行独立接受所有位置；draft/target processor 不一致；用单条输出证明 exact；不记录被拒 token 的 KV 回滚。

完成本节后，应能推导单步质量恒等式，计算 TV 与平均接受率，解释多 token waterfall，列出 exactness 前提，并用成本模型判断 speculative decoding 何时可能得不偿失。

## 九、来源与练习

- [[S-2023-Leviathan-Speculative-Decoding]]；
- [[S-2023-Chen-Speculative-Sampling]]；
- [[习题 - Speculative Decoding、Acceptance 与分布精确性]]；
- [[解答 - Speculative Decoding、Acceptance 与分布精确性]]。

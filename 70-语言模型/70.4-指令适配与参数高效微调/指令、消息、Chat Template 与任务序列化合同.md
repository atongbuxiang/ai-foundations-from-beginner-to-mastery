---
type: concept
status: verified
area: [language-models, instruction-tuning, chat-template, serialization]
node_id: LM-25
aliases: [Chat Template 合同, 消息序列化, 对话编译器]
prerequisites: ["[[Unicode、字节、码点、字素簇与规范化合同]]", "[[Causal LM 的 Shift、Attention Mask 与 Token Loss]]"]
related: ["[[监督微调、Teacher Forcing 与 Response-only Loss]]", "[[Model、API、Tokenizer、Template 版本与复现合同]]"]
sources: ["[[S-2026-HuggingFace-Chat-Templates]]", "[[S-2023-Longpre-Flan-Collection]]"]
exercises: ["[[习题 - 指令、消息、Chat Template 与任务序列化合同]]"]
solutions: ["[[解答 - 指令、消息、Chat Template 与任务序列化合同]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-adapt-chat-template-contract-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# 指令、消息、Chat Template 与任务序列化合同

> [!abstract] 一句话结论
> Chat 模型的输入不是抽象的“若干条消息”，而是消息对象经过模板、转义、特殊 token 和调用参数编译出的一个精确 token 序列。模板是模型接口的一部分；同一消息换模板，就换了条件概率事件。

## 一、先把五个对象分开

初学者最容易把下列对象都叫作 prompt：

1. **语义任务**：例如“回答用户问题”；
2. **结构化消息**：有 role、content、name、tool call 等字段的记录；
3. **渲染字符串**：模板插入 role marker、分隔符与 EOS 后的文本；
4. **模型 token 序列**：tokenizer 输出的整数 IDs；
5. **生成边界**：模型从哪个位置开始续写，何时停止，怎样反解析为消息。

把消息序列记为

$$
M=(m_1,\ldots,m_K),\qquad
m_k=(r_k,c_k,a_k),
$$

其中 $r_k$ 是 role，$c_k$ 是 content，$a_k$ 是 name、tool schema、attachments 等附加字段。模板编译器是

$$
s=T_{\phi}(M;z),\qquad
x=\operatorname{Tok}_{\psi}(s),
$$

$\phi$ 是模板版本，$z$ 是 add-generation-prompt 等 flags，$\psi$ 是 tokenizer 与 special-token 版本。模型真正条件化的是 $x$，不是自然语言中“看起来一样”的 $M$。

## 二、模板不是装饰字符串

模板至少决定：

- system/user/assistant/tool 的 role marker；
- 每条消息前后是否加入 BOS、EOS、end-of-turn；
- 空白、换行、缩进和 escaping；
- assistant generation prefix 是否追加；
- 最后一条 assistant content 是被继续还是被视为已结束；
- tool call 的 JSON/schema 以何种顺序和编码进入上下文。

例如两个模板可能把同一 user 消息编译为：

$$
x^{(A)}=[\text{BOS},\text{USER},q,\text{EOT},\text{ASSISTANT}],
$$

$$
x^{(B)}=[\text{INST\_OPEN},q,\text{INST\_CLOSE}].
$$

即使人类都读成“问题 $q$”，模型看到的前缀、位置、特殊 token 与训练频率不同，所以

$$
p_\theta(y\mid x^{(A)})\ne p_\theta(y\mid x^{(B)})
$$

一般没有相等保证。

## 三、训练模板与推理模板必须闭合

设训练示例由 prompt 部分 $x$ 和 assistant response $y$ 组成。训练编译器应生成

$$
z_{\text{train}}=T_\phi(M_{\le user}\oplus M_{assistant}),
$$

推理编译器只生成 assistant 回答之前的前缀：

$$
z_{\text{infer}}=T_\phi(M_{\le user};\text{generation-prefix}=1).
$$

理想的不变量是：

$$
z_{\text{train}}[0:b]=z_{\text{infer}},
$$

其中 $b$ 是 assistant 内容开始位置。若训练中有 assistant marker，而推理漏了；或推理重复插入 BOS/EOS，模型就处在训练分布之外。

### 一个最小 golden case

对消息：

- system：You are concise.
- user：2+3=?
- assistant：5

必须保存：

- 原始结构化 JSON；
- template bytes/hash；
- tokenizer revision 与 special-token map；
- 渲染文本；
- input IDs；
- assistant 内容的起止 offsets；
- 训练 loss mask；
- 推理 generation start。

只保存最终字符串不足以检查 role 字段丢失；只保存消息 JSON 又不能复现实际 token。

## 四、两个容易混淆的推理 flags

### 1. add generation prompt

它通常在消息末尾追加“下一条消息由 assistant 开始”的控制前缀。它不生成回答，只改变条件序列。

### 2. continue final message

它表示最后一条消息已经开始但未结束，让模型继续该内容。例如预填 JSON 前缀时，最后一条可能是 assistant 的半成品。

两者语义不同，通常不应同时盲开。是否支持、具体行为和互斥规则都依模板/库版本；需以实际 IDs 做 golden test，不能凭参数名猜。

## 五、特殊 token 的双重插入

常见失败是先把模板渲染成含 BOS/EOS 的文本，再让 tokenizer 自动 add special tokens，于是同一边界被插两次。模型可能看到：

$$
[\text{BOS},\text{BOS},\ldots,\text{EOS},\text{EOS}].
$$

因此要明确谁拥有 special-token 插入权：

1. 模板已经输出全部控制 token，tokenizer 禁止再加；
2. 模板只输出普通文本，由 tokenizer 加；
3. 混合方案必须逐 token 声明，不依赖默认值。

“字符串看起来正确”无法发现某个 special token 被 tokenizer 当普通字符拆分；最终 IDs 才是 oracle。

## 六、多轮消息不是简单拼接

多轮对话还需定义：

- 是否对历史 assistant turns 计 loss；
- 被截断时从左删、按 turn 删，还是保留 system；
- tool result 是否可见给后续 assistant；
- 同一 tool call ID 如何绑定 request/result；
- malformed JSON 是丢弃、修复还是作为失败示例；
- content 中恰好出现 role marker 时如何 escape。

消息语法可用有限状态机描述。例如允许的主路径为：

$$
\text{system?}\to(\text{user}\to\text{assistant})^*,
$$

有工具时扩展为：

$$
\text{assistant(tool\_call)}
\to \text{tool(result)}
\to \text{assistant}.
$$

结构验证应发生在渲染前，否则缺失 tool result 的非法样本可能被压成貌似合法的 token 流。

## 七、反解析也是合同

模型输出 token 后，系统还要决定：

- 哪个 token/string 表示消息结束；
- tool call 从哪里开始、是否必须符合 schema；
- stop string 是否保留在输出；
- invalid UTF-8/JSON 怎样恢复；
- parser 失败是否重试、转文本还是报错。

所以系统合同是

$$
M_{\text{in}}
\xrightarrow{T_\phi,\operatorname{Tok}_\psi}
x
\xrightarrow{p_\theta,\mathcal D}
\hat y
\xrightarrow{P_\omega}
\hat M_{\text{out}},
$$

其中 $\mathcal D$ 是解码器，$P_\omega$ 是输出 parser。只版本化模型权重而不版本化 $\phi,\psi,\omega$，不能复现实际行为。

## 八、图解：从消息到生成边界

先看图回答：同一消息在哪三个位置可能被改变为不同条件事件？

![[00-知识库管理/_assets/figures/language-models/fig-lm-adapt-chat-template-contract-v1.svg|900]]

> [!figure] 图 LM-25　Chat Template 编译链
> 左侧是结构化 messages，中间是模板源码与 flags，右侧分别保存 rendered text 与 tokenizer output；下方分开训练序列和推理 generation prefix。图由本库按 Hugging Face 官方模板接口重新绘制。
> **生成：**本图由本库依据本节定义、正文列出的一级来源和固定绘图脚本重新绘制；图中的小规模数值或结构用于教学，不复刻论文原图。

**怎样读图**：沿消息→模板→字符串→IDs 顺序核对；然后分别走 training 和 inference 两条出口，检查前缀是否一致。

**图没有证明什么**：它不证明某一套 role markers 最优，不证明不同模板可互换，也不规定任一模型仓库的最新模板内容。

## 九、工程测试门

每个 template 至少有以下测试：

1. **golden IDs**：固定消息得到固定 IDs；
2. **prefix equality**：训练序列在回答前的前缀等于推理序列；
3. **no duplicate specials**：BOS/EOS/EOT 次数和位置符合规则；
4. **role sensitivity**：交换 user/assistant 必须改变 IDs；
5. **escaping**：content 含 marker/JSON/Unicode 边界仍可解析；
6. **tool round-trip**：call/result ID 与 schema 不丢失；
7. **truncation**：删 turn 不留下孤立 marker；
8. **version diff**：template/tokenizer 升级输出显式 diff。

## 十、证据等级与边界

- 官方文档承担当前 API/参数语义；必须绑定版本和访问日期；
- 模型仓库 template 承担该 checkpoint 的默认序列化，但不证明训练时确实完全相同；
- 论文中的“prompt 格式”若未给 exact bytes/IDs，只能支持高层描述；
- 模板 A 比 B 好是经验结论，需固定模型、数据、loss、sampler 与评估，不能写成格式定理。

## 本节出口

你应能拿到任意 messages，手工指出模板、tokenizer、special tokens、generation prefix 和 parser 五个版本对象，并为训练/推理生成可比较的 IDs。下一节把这些 IDs 变成 SFT 的 labels 与 loss mask：[[监督微调、Teacher Forcing 与 Response-only Loss]]。

## 练习与独立解答

- [[习题 - 指令、消息、Chat Template 与任务序列化合同]]
- [[解答 - 指令、消息、Chat Template 与任务序列化合同]]


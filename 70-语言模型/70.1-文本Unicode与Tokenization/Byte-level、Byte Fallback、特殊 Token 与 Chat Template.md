---
type: concept
status: verified
area: [language-models, tokenization, bytes, special-tokens]
node_id: LM-07
aliases: [Byte Fallback, 特殊 Token 与聊天模板]
prerequisites: ["[[Unicode、字节、码点、字素簇与规范化合同]]", "[[Tokenizer 作为码本、分段路径与压缩接口]]"]
related: ["[[指令、消息、Chat Template 与任务序列化合同]]", "[[Prompt Injection、Indirect Injection 与 Tool-RAG 威胁模型]]"]
sources: ["[[S-2023-Su-9752-BytePiece]]", "[[S-2018-Kudo-Richardson-SentencePiece]]", "[[S-2026-HuggingFace-Tokenizer-Special-Tokens]]"]
exercises: ["[[习题 - Byte-level、Byte Fallback、特殊 Token 与 Chat Template]]"]
solutions: ["[[解答 - Byte-level、Byte Fallback、特殊 Token 与 Chat Template]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-byte-special-template-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Byte-level、Byte Fallback、特殊 Token 与 Chat Template

> [!abstract] 一句话结论
> byte-level 与 byte fallback 都可减少 OOV，但前者从一开始就在 byte 字母表上分段，后者通常先做 Unicode piece、遇到未知片段再回退为 bytes。特殊 token 是受信控制符号，chat template 则把结构化消息编译为 token 序列；二者若与普通文本混淆，会同时破坏训练一致性与安全边界。

## 一、三种覆盖策略

给输入文本 $x$：

1. **character/subword + UNK**：无法覆盖时输出 `[UNK]`；总可执行但有信息损失；
2. **Unicode pieces + byte fallback**：先匹配常见 piece，失败子串按 UTF-8 bytes 输出保底 ID；
3. **fully byte-level**：先编码成 bytes，256 个 byte 单元构成基本 alphabet，再学习多 byte merges/pieces。

若 256 个 byte 值都有独立 token，且 decode 反向拼接 bytes，可实现任意 byte stream 的覆盖。实际系统常把 byte 映射到一组可打印 Unicode 符号以方便词表文件，这个映射本身也必须保存。

## 二、byte-level 与 fallback 的概率/成本差异

对常见中文字符，UTF-8 常需 3 bytes。若未被合并：

- fully byte-level 可能输出 3 个 byte tokens；
- Unicode tokenizer 若该字符在基本 alphabet 中可能输出 1 个 token；
- byte fallback 只有在 piece 未覆盖时才输出多个 byte tokens。

所以“没有 OOV”不等于“长度公平”。不同语言、emoji、罕见字符和损坏文本的 tail fertility 仍可能很高。

## 三、特殊 token 是词表中的受信控制通道

常见角色：

| token | 可能用途 | 不自动意味着 |
|---|---|---|
| BOS | 序列起点/初始条件 | 一定参与 loss |
| EOS | 模型预测的终止事件 | 与 padding 相同 |
| PAD | batch 对齐占位 | attention/loss 自动屏蔽 |
| UNK | 无法编码的占位 | 保留原文 |
| MASK | corruption 输入占位 | 自动计算 MLM loss |
| role/tool tokens | 消息角色、工具边界 | 用户文本无法伪造 |

token 被注册为 special 只会影响 tokenizer 的拆分、添加或解码行为；attention mask 和 labels 仍由模型/数据 collator 显式构造。

### 字面文本与特殊 token

用户输入字符串 `<|assistant|>` 有两种完全不同的解释：

- 作为普通文本，经 tokenizer 拆成普通 piece；
- 作为 `AddedToken(special=True)` 直接映射到受信 role ID。

API 必须决定用户是否允许注入 special token。将两者静默等同会形成 prompt boundary 攻击面。

## 四、Chat Template 是一个编译器

结构化消息

```yaml
- role: system
  content: 你是助教。
- role: user
  content: 解释 BPE。
```

经模板 $C$ 编译为字符串/ID 序列：

$$
z=C(messages;template\_version,special\_ids,add\_generation\_prompt).
$$

模板负责 role token、分隔符、换行、BOS/EOS、tool schema 和 assistant generation prefix。训练模板与推理模板不一致，相当于训练与部署条件分布不同。

> [!warning] 不要“手工字符串拼接 + 自动 add_special_tokens”双重处理
> 模板已插入 BOS/EOS 后，tokenizer 若再次自动添加，会产生双 BOS/EOS；反之关闭了自动添加但模板未补齐，也会错位。

## 五、Embedding 与词表变更

新增 $k$ 个 token 后，tokenizer 的 ID 范围变为 $V+k$。若模型 embedding $E\in\mathbb R^{V\times d}$ 未 resize，新 ID 越界；若 resize 但新行随机初始化，则“只加 token”已经改变模型参数和输出 softmax。

若 input/output embedding tied，新增行同时影响输入表示和输出 logits；若 untied，两张表都需处理。合并 tokenizer 与 checkpoint 必须检查：

```text
len(tokenizer) == input_embedding.num_embeddings
special token string -> expected id
output head rows == vocabulary size
```

## 六、EOS 与 PAD 不能无条件复用

把 PAD ID 设为 EOS 有时是部署捷径，但要明确：

- attention mask 是否屏蔽 PAD；
- loss labels 是否把 PAD 设为 ignore index；
- generation 看到 EOS 是否停止；
- prompt 内真实 EOS 是否被当 padding；
- left/right padding 怎样影响 position IDs 和 batch decode。

同一个整数 ID 承担两种角色会使语义依赖外部 mask。不能仅凭“数值一样”宣称等价。

## 七、图：三条 token 通道与模板编译

先看图回答：byte fallback 何时触发，用户文本为什么不应自动拥有 role token 权限？

![[00-知识库管理/_assets/figures/language-models/fig-lm-byte-special-template-v1.svg|900]]

> [!figure] 图 LM-07　未知输入覆盖、特殊 token 与 chat template
> A 展示 subword/byte fallback，B 分开文本、控制和 byte 通道，C 把消息模板表示为到 IDs/loss mask 的编译器。来源：本课程独立绘制。

**怎样读图**：先检查未知输入能否无损回退，再区分普通 token 与 special token 的权限，最后验证模板输出和 labels。

**图没有证明什么**：图不说明某个具体模型的 special strings 或模板；这些必须从 checkpoint 的官方 tokenizer 配置读取。

## 八、科学空间与实现证据

[[S-2023-Su-9752-BytePiece]]把 byte 作为基本单元并报告特定语料上的 bytes/token 优势；课程采用其“基本单元—分词算法—训练算法”拆分，但把语言公平和下游质量保留为待验证 `E/H`。[[S-2026-HuggingFace-Tokenizer-Special-Tokens]]承担当前 API 事实；模型仓库中的模板与源码优先级高于通用文档。

## 九、最小安全/复现测试

- 随机 bytes/多语言/emoji 能否按承诺 round-trip；
- 用户字面输入所有 special token 字符串时，是否被错误提升为控制 ID；
- train 与 inference template 对同一消息是否生成相同 prefix；
- 单/双 BOS、EOS、left/right padding、空 assistant turn；
- tool 输出包含 role-like 字符串、零宽字符和 invalid UTF-8 时的隔离；
- tokenizer/checkpoint/template hash 是否写入实验记录。

下一节[[Tokenizer 评估、多语言公平、安全与证据地图]]将把这些测试组织为完整比较协议。

## 练习与独立解答

- [[习题 - Byte-level、Byte Fallback、特殊 Token 与 Chat Template]]
- [[解答 - Byte-level、Byte Fallback、特殊 Token 与 Chat Template]]


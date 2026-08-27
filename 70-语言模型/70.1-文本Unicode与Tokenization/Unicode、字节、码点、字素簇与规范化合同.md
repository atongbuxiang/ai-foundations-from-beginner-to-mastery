---
type: concept
status: verified
area: [language-models, unicode, text]
node_id: LM-02
aliases: [Unicode 文本合同, 字节码点字素簇]
prerequisites: ["[[语言模型的文本对象、文档边界与序列样本空间]]"]
related: ["[[Byte-level、Byte Fallback、特殊 Token 与 Chat Template]]", "[[Tokenizer 评估、多语言公平、安全与证据地图]]"]
sources: ["[[S-2025-Unicode-UAX15-Normalization]]", "[[S-2025-Unicode-UAX29-Text-Segmentation]]", "[[S-2023-Su-9752-BytePiece]]"]
exercises: ["[[习题 - Unicode、字节、码点、字素簇与规范化合同]]"]
solutions: ["[[解答 - Unicode、字节、码点、字素簇与规范化合同]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-unicode-layers-normalization-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Unicode、字节、码点、字素簇与规范化合同

> [!abstract] 一句话结论
> “字符”至少可能指编码字节、Unicode 码点、编程语言 code unit、用户感知的字素簇或屏幕 glyph。语言模型管线必须声明在哪一层分割、计数和规范化；否则长度、边界、可逆性、公平性与安全判断都可能错位。

## 一、五个经常被混称为字符的对象

| 层 | 形式 | 例子 `中` / `é` | 由谁定义 |
|---|---|---|---|
| byte | $0\ldots255$ 的整数 | `中` 的 UTF-8 为 `E4 B8 AD` | 字符编码 UTF-8 等 |
| code point | `U+...` 抽象编号 | `U+4E2D`；`é` 可为 `U+00E9` | Unicode |
| code unit | API 的存储单元 | UTF-16 中补充平面码点占 surrogate pair | 编程语言/编码 API |
| grapheme cluster | 默认用户感知字符边界 | `e + ◌́` 可构成一个字素簇 | UAX #29/CLDR tailoring |
| glyph | 实际绘制形状 | 字体、连字、方向塑造后的图形 | font/shaping engine |

因此 `len(text)` 没有脱离 API 的普遍含义。Python 3 常按码点计数；JavaScript string length 按 UTF-16 code units；用户光标移动常按字素簇；byte-level tokenizer 按 UTF-8 bytes 起步。

## 二、UTF-8 不是 Unicode 本身

Unicode 给字符分配码点；UTF-8 是把码点编码为字节的可变长方案。令

$$
E_{UTF8}:\mathcal U^*\to\{0,\ldots,255\}^*,\qquad
D_{UTF8}:\mathcal B_{valid}^*\to\mathcal U^*.
$$

对合法 Unicode scalar value 序列，应有

$$D_{UTF8}(E_{UTF8}(u))=u.$$

但任意 byte stream 未必是合法 UTF-8。错误策略可能是 reject、replacement character `U+FFFD`、忽略字节或保留原始 byte。replacement 会破坏严格往返：多个不同坏字节序列可能映到同一个 `�`。

### 手算：`中` 为什么是 3 bytes

`中` 为 `U+4E2D`，落在 UTF-8 三字节区间。按位模板

```text
1110xxxx 10xxxxxx 10xxxxxx
```

填入码点二进制后得到 `E4 B8 AD`。所以“中文一个字符、英文一个字符”并不意味着相同 byte 成本。

## 三、canonical equivalence：看起来同，还可规范等价

`é` 可以写成：

$$
[\mathrm{U+00E9}]
\quad\text{或}\quad
[\mathrm{U+0065},\mathrm{U+0301}].
$$

两者 canonical equivalent。若 tokenizer 在码点层直接工作而不统一规范化，它们可能得到不同 token 序列。UAX #15 定义四个 form：

| form | 操作 | 是否使用 compatibility decomposition |
|---|---|---|
| NFD | canonical decomposition | 否 |
| NFC | canonical decomposition + composition | 否 |
| NFKD | compatibility decomposition | 是 |
| NFKC | compatibility decomposition + composition | 是 |

规范化算子 $N$ 应满足幂等性

$$N(N(x))=N(x).$$

但“等价形式变成同一二进制串”不等于“保持所有任务信息”。NFKC 可把 `①` 变为 `1`、全角变半角、上标折叠为普通数字；在搜索中也许有益，在数学、身份标识、代码或取证中可能丢信息。

> [!warning] 规范化不是越强越好
> NFC 通常保留 compatibility distinctions；NFKC 主动折叠它们。必须根据任务和威胁模型选择，且 train/inference 完全一致。

## 四、字素簇：用户看到的一个符号可由多码点组成

家庭 emoji、肤色修饰、国旗区域指示符、combining mark 都可能形成 extended grapheme cluster。例如 ZWJ 序列把多个 emoji 码点组合为一个用户感知图形。

令 $G_{ver}(u)$ 按某版 UAX #29 把码点串分成字素簇：

$$G_{ver}(u)=(g_1,\ldots,g_m).$$

这里 $m$ 不是 UTF-8 bytes 数、码点数或 tokenizer token 数。若评估“每字符 tokens”，必须说明 denominator 是 code point 还是 grapheme cluster。

## 五、规范化、大小写与安全

即便 normalization 相同，视觉相似也不保证码点相同：Latin `a` 与 Cyrillic `а` 是不同码点。反之，相同码点串在不同字体/方向 shaping 下也可出现不同 glyph。安全审计至少分开：

- canonical/compatibility equivalence；
- confusable/homoglyph；
- bidirectional control characters；
- zero-width/format characters；
- invalid byte 与 replacement；
- tokenizer 是否把控制通道与文本通道隔离。

不要用“肉眼看起来一样”作为 ID、域名、引用或 prompt boundary 的等价判据。

## 六、图：从码点序列到用户感知字符

先看图回答：为什么 NFC/NFD 可保持 canonical equivalence，而 NFKC 可能丢失任务信息？

![[00-知识库管理/_assets/figures/language-models/fig-lm-unicode-layers-normalization-v1.svg|900]]

> [!figure] 图 LM-02　码点序列、字素簇与规范化形式
> A 对比预组合/分解 `é`，B 展示多码点字素簇，C 对比 canonical 与 compatibility normalization。来源：本课程依据 Unicode UAX #15/#29 独立绘制。

**怎样读图**：先数 bytes/code points/graphemes，再问哪一个 normalization form 使哪些序列相等，最后记录可能丢失的 compatibility distinction。

**图没有证明什么**：少数示例不覆盖 Unicode conformance；实现必须运行对应版本的官方测试数据。

## 七、最小可执行审计

对一组固定字符串至少输出：

```text
raw bytes (hex)
decoded code points (U+....)
NFC/NFD/NFKC/NFKD code points
extended grapheme clusters
token ids
decode(token ids) bytes
```

并断言：

1. 合法输入在承诺的层次上 round-trip；
2. normalization 幂等；
3. train/inference 使用相同 form/Unicode/tokenizer 版本；
4. 安全切片中的 invisible/confusable 不被静默删除而无记录。

## 八、研究边界与下一节

UAX #15/#29 的定义是版本化标准 `P0`；“byte 起点更公平”是需要数据切片和下游任务验证的 `H/E`。[[S-2023-Su-9752-BytePiece]]提供 byte-based 设计动机，但压缩提升不能自动推出公平或质量提升。

下一节[[Tokenizer 作为码本、分段路径与压缩接口]]把这些文本单元映射到有限 token 词表。

## 练习与独立解答

- [[习题 - Unicode、字节、码点、字素簇与规范化合同]]
- [[解答 - Unicode、字节、码点、字素簇与规范化合同]]


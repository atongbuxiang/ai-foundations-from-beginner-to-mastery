---
type: solution
status: verified
area: [language-models, unicode, text]
topic: "[[Unicode、字节、码点、字素簇与规范化合同]]"
exercise: "[[习题 - Unicode、字节、码点、字素簇与规范化合同]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Unicode、字节、码点、字素簇与规范化合同

## A. 识别与复述

### LM02-A01
Byte 是编码后的 8-bit 数；code point 是 Unicode 抽象编号；code unit 是 UTF-8/16/32 或语言 API 的存储单位；grapheme cluster 是默认用户感知字符边界；glyph 是字体 shaping 后图形。同一字素可多码点，同一码点可多 bytes，同一文本可因字体产生不同 glyph。

### LM02-A02
第一轴是 canonical vs compatibility decomposition；第二轴是 decomposition-only(D) vs 再 composition(C)。NFD/NFC 只用 canonical，NFKD/NFKC 还折叠 compatibility distinction。

### LM02-A03
Invalid bytes 可被 reject、替换、忽略或保留。不同策略改变样本、可逆性与安全日志；replacement/ignore 会把不同 byte 序列合并，必须版本化。

## B. 手算与构造

### LM02-B01
预组合 `[U+00E9]`；分解 `[U+0065,U+0301]`。在标准 canonical mapping 下两者 NFC 都为前者，NFD 都为后者。

### LM02-B02
UTF-8 bytes 数 3，code points 数 1，默认 grapheme cluster 数 1。若语言 API 按 UTF-16 code units，该 BMP 字符也是 1，但不能由此概括 emoji。

### LM02-B03
例如 `①Ａ²` 经 NFKC 可趋向 `1A2`。圈号、全角和上标身份丢失；在编号、排版、变量名或取证中可能有意义。

## C. 推导与证明

### LM02-C01
规范化输出已处于该 normal form，再应用不应变化。幂等失败说明版本/配置不一致、边界串处理错误或实现不合规；重复预处理会制造数据漂移。

### LM02-C02
取两个不同 invalid byte 串，error handler 都输出 U+FFFD。则 $D(b_1)=D(b_2)$ 而 $b_1\ne b_2$，解码非单射，不存在能同时恢复两者的逆函数。

### LM02-C03
一个 emoji 字素可能含 5 个码点。Tokenizer A 输出 5 tokens、B 输出 2：按字素 fertility 为 5 vs 2；若另一语言主要单码点，汇总 code-point denominator 会给 emoji 串额外大分母，可能改变加权平均与排名。

## D. 边界、反例与纠错

### LM02-D01
Latin `a` 与 Cyrillic `а` 可视觉近似但语义/标识不同，且不是 canonical equivalent。盲目合并可把不同用户名、域名或代码标识折叠。

### LM02-D02
UAX #15 给出边界效应：NFC 串 `a` 与 combining circumflex 各自可视为规范化片段，拼接 `a+◌̂` 还能 compose 为 `â`，所以拼接结果需重新 normalization。

### LM02-D03
Python 3 常按 code points，JS 按 UTF-16 code units；两者对补充平面 emoji 计数不同。报告应明确 UTF-8 bytes/UAX #29 graphemes/Unicode version，并使用同一实现测试。

## E. AI 迁移

### LM02-E01
含 NFC/NFD 对、compatibility chars、combining order、ZWJ emoji、flags、skin tones、bidi/zero-width、invalid UTF-8、长 combining sequence、各 script；对官方 normalization/segmentation tests 与 round-trip、幂等作断言。

### LM02-E02
日志渲染可能隐藏/重排字符，使审核者看到的 prompt 与模型接收码点不同；homoglyph 可伪装 role/domain。应保存 escaped code points/raw bytes、规范显示，限制受信控制通道并监测异常长度。

### LM02-E03
记录 encoding/error policy、Unicode 数据版本、normalization form、case/accent/whitespace、segmentation library/version、测试集 hash。升级时在固定 corpus 比较 normalized bytes、grapheme boundaries、token IDs、长度分布和安全切片，任何差异都触发 tokenizer/data version 变更。

## 无提示重做

- [ ] 手工解释一个 ZWJ emoji 的 bytes/code points/grapheme/token 四层。
- [ ] 给出 NFC 安全但 NFKC 不安全的任务反例。


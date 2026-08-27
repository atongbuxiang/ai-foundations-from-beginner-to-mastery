---
type: template-guide
status: active
area: [templates, visualization]
created: 2026-08-20
updated: 2026-08-20
---

# SVG 教材插图模板

本目录保存自绘图的**起始骨架**，不是可直接嵌入正文的成品。复制后必须替换 `<title>`、`<desc>`、占位文字、对象和结论，并按[[06-图文编排与制图工作流]]验收。

| 模板 | 使用场景 | 默认画布 |
|---|---|---:|
| `template-paper-ink.svg` | 定义、几何、最小例子、反例 | 1200×520 |
| `template-proof-map.svg` | 证明、递推、对称化、算法机制 | 1200×620 |
| `template-research-plot.svg` | 曲线、上界、误差、实验布局原型 | 1200×680 |

## 使用方法

```bash
cp "00-知识库管理/_templates/svg/template-paper-ink.svg" \
   "00-知识库管理/_assets/figures/<topic>/fig-<topic>-<purpose>-v1.svg"
```

完成编辑后：

```bash
node "00-知识库管理/_labs/code/lib/validate-svg-figure.mjs" \
  "00-知识库管理/_assets/figures/<topic>/fig-<topic>-<purpose>-v1.svg"

xmllint --noout INPUT.svg
svg-render INPUT.svg /tmp/figure-preview.png 1200
```

## 固定视觉 token

```text
ink       #1F2937   正文、主轮廓、坐标轴
muted     #64748B   次要文字
hairline  #D7DEE8   网格、分隔线
blue      #2563EB   当前研究对象
green     #0F766E   可行、保持、证明路径
amber     #B7791F   近似、上界、放松
red       #C24135   反例、矛盾、危险边界
paper     #FFFEFB   解释图背景
white     #FFFFFF   实验图背景
```

默认字体栈：

```css
font-family: Inter, "PingFang SC", "Noto Sans CJK SC", sans-serif;
```

数学符号或代码可局部使用：

```css
font-family: "STIX Two Text", "Times New Roman", serif;
font-family: "SFMono-Regular", Menlo, monospace;
```

## 复制后必须完成

- [ ] 用具体图名替换 `<title>`；
- [ ] 用一到三句写清关系与结论的 `<desc>`；
- [ ] 删除所有方括号占位文字；
- [ ] 一张图只保留一个主问题；
- [ ] 单图不超过三个强调色；
- [ ] 不在图内重复 Markdown 小节标题和长图注；
- [ ] 正式实验数据由脚本生成，不手工修改曲线；
- [ ] 写清独立绘制、重绘来源或实验脚本。


#!/usr/bin/env python3
"""Generate eight deterministic textbook figures for LM-01--LM-08."""

from pathlib import Path
from plot_calculus_operator_figures_v2 import (
    AMBER, BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)

OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "language-models"


def text_objects():
    out = begin("文本怎样成为语言模型样本", "同一屏幕字符串依次经过字节解码、Unicode 处理、文档切分、tokenizer 和样本窗口；每个边界都属于版本合同。", (BLUE, TEAL, RED))
    heading(out, 42, "A", "一条可逆主链", BLUE)
    stages = ((95,"bytes","UTF-8"),(190,"Unicode string","normalize?"),(285,"document","boundary"),(380,"token ids","encode"))
    for y, title, sub in stages:
        node(out, 55, y, 285, 58, title, BLUE if y < 280 else TEAL, "#F8FAFC", 16)
        out += [text(198, y+83, sub, 13, 650, "middle", MUTED)]
        if y < 380: out.append(line(198, y+86, 198, y+91, INK, 2, marker="a3"))
    heading(out, 430, "B", "边界改变样本空间", TEAL)
    out += [text(445,112,"doc 1",14,700,fill=TEAL),rect(445,130,310,48,TEAL,"#ECFDF5",5,2),text(600,160,"[BOS] A B [EOS]",15,650,"middle"),
            text(445,222,"错误拼接",14,700,fill=RED),rect(445,240,310,48,RED,"#FEE2E2",5,2),text(600,270,"A B C D (跨文档条件)",15,650,"middle",RED),
            text(445,332,"显式边界",14,700,fill=BLUE),rect(445,350,310,48,BLUE,"#EFF6FF",5,2),text(600,380,"A B [EOS] C D",15,650,"middle",BLUE)]
    heading(out, 830, "C", "样本窗口不是文档", RED)
    for i,(lab,col) in enumerate((("document stream",TEAL),("packing",AMBER),("T-token windows",BLUE),("loss mask",RED))):
        y=100+i*92; node(out,845,y,285,52,lab,col,"#F8FAFC",15)
        if i<3: out.append(line(987,y+55,987,y+87,INK,2,marker="a3"))
    return finish(out,"能复现一个语言模型，必须先复现文本、文档和窗口的生成函数。")


def unicode_layers():
    out = begin("Unicode 的四个层次与规范化边界", "字节、码点、字素簇和 glyph 不是同一对象；canonical normalization 与 compatibility normalization 保留的信息不同。", (AMBER, BLUE, TEAL))
    heading(out,42,"A","同一个 é 的两种码点序列",AMBER)
    out += [text(55,120,"NFC",14,800,fill=AMBER),rect(105,90,210,52,AMBER,"#FFF7ED",5,2),text(210,123,"U+00E9",17,700,"middle",AMBER),
            text(55,220,"NFD",14,800,fill=BLUE),rect(105,190,95,52,BLUE,"#EFF6FF",5,2),text(152,223,"U+0065",14,700,"middle",BLUE),text(220,223,"+",18,700),rect(245,190,95,52,BLUE,"#EFF6FF",5,2),text(292,223,"U+0301",14,700,"middle",BLUE),
            line(210,150,210,180,INK,2,marker="a3"),text(55,310,"视觉可同；len(code points) 不同",15,650,fill=MUTED)]
    heading(out,430,"B","一个字素簇可含多个码点",BLUE)
    cps=(("👩",465),("ZWJ",535),("👩",605),("ZWJ",675),("👧",745))
    for lab,x in cps: out += [circle(x,145,27,BLUE,"#EFF6FF",2),text(x,151,lab,15,700,"middle",BLUE)]
    out += [line(465,190,745,190,TEAL,4),text(605,222,"用户感知：一个家庭 emoji",15,700,"middle",TEAL),text(445,310,"grapheme boundary 由 UAX #29 规则定义，",14,fill=MUTED),text(445,342,"不是 Python/JS 的 code-unit 长度。",14,fill=MUTED)]
    heading(out,830,"C","NFC 与 NFKC 不可静默互换",TEAL)
    rows=((112,"①","NFC","①",BLUE),(215,"①","NFKC","1",RED),(318,"ｶ","NFKC","カ",RED))
    for y,src,op,dst,col in rows:
        out += [rect(845,y-27,52,42,col,"#F8FAFC",5,2),text(871,y,src,18,700,"middle"),line(905,y-7,1000,y-7,col,2.5,marker="a1"),text(952,y-17,op,13,650,"middle",col),rect(1015,y-27,72,42,col,"#F8FAFC",5,2),text(1051,y,dst,18,700,"middle",col)]
    out += [text(845,405,"compatibility normalization 可能丢失格式/身份信息。",13,650,fill=RED)]
    return finish(out,"“字符数”必须绑定层次；规范化必须绑定形式、Unicode 版本与任务风险。")


def tokenizer_codebook():
    out = begin("Tokenizer = 码本 + 分段器 + 可逆接口", "同一字符串可有多条合法分段路径；词表改变 token 数、概率因子和计算成本，但不自动保证下游质量。", (TEAL, BLUE, AMBER))
    heading(out,42,"A","分段是路径选择",TEAL)
    pts=[(65,210,"0"),(155,125,"a"),(155,295,"ab"),(255,125,"b"),(255,295,"c"),(345,210,"c")]
    for x,y,lab in pts: out += [circle(x,y,21,TEAL,"#ECFDF5",2),text(x,y+6,lab,14,700,"middle",TEAL)]
    edges=((86,205,134,139,"a"),(86,220,134,284,"ab"),(176,125,234,125,"b"),(176,295,234,295,"c"),(276,125,326,198,"c"),(276,295,326,222,"c"))
    for x1,y1,x2,y2,lab in edges: out += [line(x1,y1,x2,y2,BLUE,2,marker="a0"),text((x1+x2)/2,(y1+y2)/2-8,lab,13,650,"middle",BLUE)]
    out += [text(55,390,"encode(x) = 选一条覆盖全串的 token 路径",15,650)]
    heading(out,430,"B","三项合同",BLUE)
    for y,title,desc,col in ((100,"Vocabulary","token ↔ id; versioned",BLUE),(220,"Segmentation","deterministic or sampled",TEAL),(340,"Decoder","ids → bytes/text; total?",AMBER)):
        node(out,445,y,300,55,title,col,"#F8FAFC",15); out += [text(445,y+82,desc,13,fill=MUTED)]
    heading(out,830,"C","码本粒度的三角权衡",AMBER)
    out += [path("M985 100L850 410L1120 410Z",AMBER,3,"#FFF7ED"),text(985,85,"短序列",15,800,"middle",AMBER),text(835,440,"小词表 / 覆盖",14,800,fill=TEAL),text(1130,440,"参数 / 稀疏性",14,800,"end",BLUE),circle(980,290,10,RED,RED),text(1000,295,"任务相关 Pareto 点",13,650,fill=RED)]
    return finish(out,"Tokenizer 不是无损预处理的同义词，而是模型概率空间和资源预算的一部分。")


def bpe_merges():
    out = begin("BPE：频繁 pair 合并与确定性版本合同", "训练阶段重复计数并合并 pair；编码阶段按固定 merge rank 重放。并列频数、预切分和词尾标记都会改变模型文件。", (BLUE, AMBER, RED))
    heading(out,42,"A","教学语料与 pair 计数",BLUE)
    out += [text(55,112,"l o w </w>   ×5",16,700),text(55,152,"l o w e r </w> ×2",16,700),text(55,192,"n e w e s t </w> ×6",16,700),text(55,250,"count(e,s)=6",15,700,fill=BLUE),text(55,285,"count(s,t)=6",15,700,fill=RED),text(55,330,"并列！需要固定 tie-break",15,800,fill=RED)]
    heading(out,430,"B","一次 merge 是全局重写",AMBER)
    out += [rect(445,105,52,42,BLUE,"#EFF6FF",5,2),text(471,132,"e",17,700,"middle"),rect(510,105,52,42,BLUE,"#EFF6FF",5,2),text(536,132,"s",17,700,"middle"),line(570,125,635,125,AMBER,3,marker="a1"),rect(655,105,82,42,AMBER,"#FFF7ED",5,2),text(696,132,"es",17,700,"middle",AMBER),
            text(445,210,"merge rank 0: (e,s) → es",15,700),text(445,250,"rank 1: (es,t) → est",15,700),text(445,310,"encoding 只按 rank，不重新看语料频率",14,fill=MUTED),text(445,365,"预切分/空格标记也属于算法输入。",14,650,fill=RED)]
    heading(out,830,"C","同频 tie 产生分叉版本",RED)
    out += [rect(865,95,235,45,BLUE,"#EFF6FF",5,2),text(982,124,"e s t",17,700,"middle"),line(925,145,890,210,BLUE,2,marker="a0"),line(1040,145,1075,210,RED,2,marker="a2"),
            rect(835,225,145,48,BLUE,"#EFF6FF",5,2),text(907,255,"es t",16,700,"middle",BLUE),rect(1020,225,145,48,RED,"#FEE2E2",5,2),text(1092,255,"e st",16,700,"middle",RED),
            text(845,340,"词表大小相同 ≠ tokenizer 相同",14,700,fill=RED),text(845,380,"保存 corpus hash、pretokenizer、tie rule、merges。",13,fill=MUTED)]
    return finish(out,"BPE 的可复现对象不是“算法名”，而是预切分、初始符号、计数、并列规则与有序 merges。")


def wordpiece():
    out = begin("WordPiece：词表学习与最长匹配是两个阶段", "编码通常从词首向右选择词表中最长片段；局部贪心可能进入死路，未知词语义取决于实现合同。", (TEAL, BLUE, RED))
    heading(out,42,"A","词表含词首/续接标记",TEAL)
    vocab=(("play",70,110),("player",70,175),("##er",220,110),("##ing",220,175),("[UNK]",145,260))
    for lab,x,y in vocab: node(out,x,y,105,42,lab,TEAL if "UNK" not in lab else RED,"#F8FAFC",14)
    out += [text(55,350,"play + ##er",17,800,fill=BLUE),text(55,392,"## 不是自然语言符号，而是位置约束。",14,fill=MUTED)]
    heading(out,430,"B","Longest-match-first",BLUE)
    out += [text(445,112,"player",19,800),line(445,135,735,135,GRID,2),path("M445 160L650 160",BLUE,5),text(547,190,"player ✓",15,700,"middle",BLUE),
            text(445,250,"playing",19,800),path("M445 290L585 290",TEAL,5),text(515,322,"play",15,700,"middle",TEAL),path("M590 290L735 290",AMBER,5),text(662,322,"##ing",15,700,"middle",AMBER)]
    heading(out,830,"C","贪心可失败，即使存在全局分段",RED)
    out += [text(845,110,"词表: ab, a, ##bc",15,700),text(845,165,"输入: abc",18,800),rect(845,205,95,42,RED,"#FEE2E2",5,2),text(892,232,"ab",16,700,"middle",RED),line(945,226,1020,226,RED,2.5,marker="a2"),text(1030,232,"c 无匹配",14,700,fill=RED),
            rect(845,305,75,42,TEAL,"#ECFDF5",5,2),text(882,332,"a",16,700,"middle",TEAL),rect(940,305,100,42,TEAL,"#ECFDF5",5,2),text(990,332,"##bc",16,700,"middle",TEAL),text(845,410,"因此编码器规则必须独立于词表集合声明。",13,fill=MUTED)]
    return finish(out,"WordPiece 不能只写“像 BPE”；词表评分、位置标记、贪心顺序与 unknown 行为都要分账。")


def unigram():
    out = begin("Unigram LM：分段潜变量、Viterbi 与 EM", "为每个 token 赋概率，句子概率由分段路径概率构成；Viterbi 求 MAP，forward-backward 给后验计数，EM 更新码本。", (AMBER, TEAL, BLUE))
    heading(out,42,"A","字符串 ab 的路径和",AMBER)
    out += [circle(65,210,20,AMBER,"#FFF7ED",2),circle(200,130,20,TEAL,"#ECFDF5",2),circle(335,210,20,AMBER,"#FFF7ED",2),line(86,202,180,142,TEAL,2.5,marker="a1"),line(220,142,315,202,TEAL,2.5,marker="a1"),line(86,220,315,220,BLUE,2.5,marker="a2"),text(130,150,"a:.4",14,700,fill=TEAL),text(265,150,"b:.3",14,700,fill=TEAL),text(200,244,"ab:.2",14,700,"middle",BLUE),text(55,335,"P(ab)=.4×.3 + .2 = .32",17,800)]
    heading(out,430,"B","Viterbi 与总似然不同",TEAL)
    out += [text(445,115,"MAP path",14,700,fill=TEAL),text(445,155,"max(.12, .20) = .20",18,800),text(445,230,"marginal likelihood",14,700,fill=BLUE),text(445,270,"sum(.12, .20) = .32",18,800),text(445,350,"Viterbi 选一条；forward 求所有路径和。",14,fill=MUTED)]
    heading(out,830,"C","EM / pruning 循环",BLUE)
    for i,(lab,col) in enumerate((("E: path posterior",TEAL),("expected token counts",AMBER),("M: normalize p(v)",BLUE),("prune low utility",RED))):
        y=95+i*92; node(out,845,y,285,52,lab,col,"#F8FAFC",15)
        if i<3: out.append(line(987,y+55,987,y+87,INK,2,marker="a3"))
    return finish(out,"先区分 MAP 分段、边缘似然和采样分段；三者相同词表也会产生不同训练信号。")


def byte_special():
    out = begin("Byte fallback、特殊 Token 与 Chat Template", "普通文本、控制符号和原始字节是三类不同通道；若模板或特殊 token 注册不一致，训练与推理会条件错位。", (BLUE, RED, TEAL))
    heading(out,42,"A","开放输入的兜底路径",BLUE)
    node(out,55,100,285,50,"Unicode text",BLUE,"#EFF6FF",15)
    out += [line(197,153,197,190,INK,2,marker="a3")]
    node(out,55,205,285,55,"known pieces?",AMBER,"#FFF7ED",15)
    out += [line(125,263,90,310,TEAL,2,marker="a1"),line(270,263,310,310,RED,2,marker="a2"),text(75,300,"yes",13,650,fill=TEAL),text(305,300,"no",13,650,fill=RED)]
    node(out,45,330,125,48,"subword id",TEAL,"#ECFDF5",14); node(out,225,330,145,48,"byte fallback ids",RED,"#FEE2E2",14)
    heading(out,430,"B","三类 token 不应混淆",RED)
    for y,title,desc,col in ((100,"text token","由用户文本编码",BLUE),(220,"special token","BOS/EOS/role/tool 控制",RED),(340,"byte token","保证任意 byte 可表示",TEAL)):
        node(out,445,y,145,50,title,col,"#F8FAFC",14); out += [text(605,y+31,desc,13,650,fill=MUTED)]
    heading(out,830,"C","Chat template 是编译器",TEAL)
    out += [text(845,103,"messages",14,800,fill=TEAL),text(845,143,"system / user / assistant",13,650),line(985,160,985,195,INK,2,marker="a3"),rect(845,210,285,58,TEAL,"#ECFDF5",6,2),text(987,245,"role tokens + separators",14,700,"middle",TEAL),line(985,272,985,307,INK,2,marker="a3"),rect(845,322,285,58,BLUE,"#EFF6FF",6,2),text(987,357,"token ids + loss mask",14,700,"middle",BLUE),text(845,435,"模板版本不同 = 条件事件不同。",14,800,fill=RED)]
    return finish(out,"可逆性要求覆盖未知输入；安全性要求文本通道不能静默伪装成控制通道。")


def audit_map():
    out = begin("Tokenizer 评估：压缩、公平、鲁棒与安全", "单一平均 token/字符不足以判定 tokenizer；需要语言切片、尾部风险、往返不变量、版本和下游预算匹配。", (TEAL, AMBER, RED))
    heading(out,42,"A","四类可计算指标",TEAL)
    rows=((105,"compression","tokens / byte; bits / byte",BLUE),(195,"fertility","tokens / word or grapheme",TEAL),(285,"coverage","UNK / fallback / max length",AMBER),(375,"round trip","decode(encode(x)) = x?",RED))
    for y,title,metric,col in rows:
        out += [text(55,y,title,14,800,fill=col),text(165,y,metric,14,650)]
    heading(out,430,"B","平均值会隐藏群体尾部",AMBER)
    langs=(("English",1.1,BLUE),("中文",1.0,TEAL),("தமிழ்",2.8,RED),("emoji",4.2,AMBER))
    for i,(name,val,col) in enumerate(langs):
        y=105+i*82; out += [text(445,y,name,14,700),rect(520,y-22,val*45,28,col,col,2,1),text(535+val*45,y,f"{val:.1f}",13,700,fill=col)]
    out += [text(445,445,"示意 fertility；必须报告分布/切片，不只总体均值。",12,fill=MUTED)]
    heading(out,830,"C","审计顺序",RED)
    for i,(lab,col) in enumerate((("1  固定语料/Unicode/normalization",BLUE),("2  固定词表预算与模板",TEAL),("3  分语言/域/攻击切片",AMBER),("4  固定模型 FLOPs 或 wall time",RED))):
        y=100+i*92; node(out,845,y,290,52,lab,col,"#F8FAFC",14)
        if i<3: out.append(line(990,y+55,990,y+87,INK,2,marker="a3"))
    return finish(out,"Tokenizer 优劣是多目标、任务相关的 Pareto 判断；总体均值不能替代公平与安全切片。")


FIGURES = {
    "fig-lm-text-object-boundaries-v1.svg": text_objects,
    "fig-lm-unicode-layers-normalization-v1.svg": unicode_layers,
    "fig-lm-tokenizer-codebook-lattice-v1.svg": tokenizer_codebook,
    "fig-lm-bpe-merges-tie-contract-v1.svg": bpe_merges,
    "fig-lm-wordpiece-longest-match-v1.svg": wordpiece,
    "fig-lm-unigram-viterbi-em-v1.svg": unigram,
    "fig-lm-byte-special-template-v1.svg": byte_special,
    "fig-lm-tokenizer-audit-fairness-v1.svg": audit_map,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in FIGURES.items():
        target = OUT / name
        target.write_text(fn(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate the eight original ARCH-33--40 Transformer teaching figures."""

from pathlib import Path
from plot_calculus_operator_figures_v2 import (
    AMBER, BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, rect, text,
)

OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "architecture"


def transformer_block():
    out = begin("Transformer Block：两次子层、两条残差与归一化位置",
                "Token mixing 由 Attention 承担，channel mixing 由逐位置 FFN 承担；Pre/Post-Norm 改变 Jacobian 接线。", (BLUE, TEAL, RED))
    heading(out, 42, "A", "Pre-Norm block", BLUE)
    x=195
    for y,lab,col in ((100,"x",BLUE),(165,"LN",AMBER),(235,"MHA",TEAL),(330,"x + MHA(LN(x))",BLUE),(400,"LN → FFN → add",RED)):
        node(out,65,y,260,48,lab,col,"#F8FAFC",14)
        if y<400: out.append(line(x,y+51,x,[165,235,330,400,470][(100,165,235,330,400).index(y)],INK,2,marker="a3"))
    out += [text(55,485,"identity path 不穿过 LN Jacobian",14,700,fill=BLUE)]
    heading(out,430,"B","Post-Norm block",TEAL)
    for y,lab,col in ((100,"x",BLUE),(180,"MHA",TEAL),(270,"x + MHA(x)",BLUE),(350,"LN",AMBER),(425,"FFN → add → LN",RED)):
        node(out,455,y,290,48,lab,col,"#F8FAFC",14)
        if y<425: out.append(line(600,y+51,600,y+75,INK,2,marker="a3"))
    out += [text(445,485,"identity branch 也被 LN Jacobian 左乘",14,700,fill=TEAL)]
    heading(out,830,"C","FFN 是逐 token 的通道变换",RED)
    node(out,845,105,280,55,"h → d_ff",BLUE,"#EFF6FF",15)
    out += [line(985,163,985,198,INK,2,marker="a3")]
    node(out,845,210,280,55,"activation / gate",AMBER,"#FFF7ED",15)
    out += [line(985,268,985,303,INK,2,marker="a3")]
    node(out,845,315,280,55,"d_ff → h",TEAL,"#ECFDF5",15)
    out += [text(845,415,"同一权重独立作用于每个位置；",14,fill=MUTED),text(845,450,"位置信息混合发生在 Attention。",14,700,fill=RED)]
    return finish(out,"先重建两类 mixing 和 residual wiring，再讨论 normalization、初始化与深度。")


def encoder():
    out=begin("Transformer Encoder：双向可见、逐位置表示与任务读出",
              "Encoder 每层让有效 tokens 双向交互；输出仍是一列 token states，pooling/head 决定任务出口。",(TEAL,BLUE,AMBER))
    heading(out,42,"A","双向 self-attention",TEAL)
    x0,y0,s=65,115,52
    for i in range(5):
        for j in range(5):
            out += [rect(x0+j*s,y0+i*s,45,45,TEAL,"#D1FAE5",3,1.5),text(x0+j*s+22,y0+i*s+28,"✓",14,700,"middle",TEAL)]
    out += [text(55,420,"padding 列另屏蔽；双向不等于无位置。",14,fill=MUTED)]
    heading(out,430,"B","每层仍输出 T × d",BLUE)
    for y,lab,col in ((100,"token + position",BLUE),(200,"encoder block × L",TEAL),(300,"contextual states H_L",AMBER)):
        node(out,455,y,290,58,lab,col,"#F8FAFC",15)
        if y<300: out.append(line(600,y+61,600,y+96,INK,2,marker="a3"))
    out += [text(455,405,"每行可依赖全部有效输入，",14,fill=MUTED),text(455,438,"但行身份仍由位置/结构合同保留。",14,700,fill=BLUE)]
    heading(out,830,"C","三类常见出口",AMBER)
    for y,title,desc,col in ((105,"token","tag / span / dense output",BLUE),(225,"pool","CLS / mean / attention pool",TEAL),(345,"masked","predict corrupted positions",RED)):
        out += [rect(845,y-30,90,42,col,"#F8FAFC",6,2),text(890,y-3,title,14,800,"middle",col),text(950,y-3,desc,13,650)]
    out += [text(845,450,"BERT 的 MLM 是训练目标，不是 encoder 定义。",13,fill=MUTED)]
    return finish(out,"Encoder 的架构合同是双向有效集、等长 token states 与显式任务读出。")


def decoder():
    out=begin("Transformer Decoder：右移输入、因果可见与增量缓存",
              "训练可并行计算所有位置，但每个位置只能读取前缀；生成时逐 token 扩展并复用历史 K/V。",(RED,BLUE,TEAL))
    heading(out,42,"A","Teacher forcing 的错位",RED)
    toks=("<B>","我","爱","AI")
    tgts=("我","爱","AI","<E>")
    for i,(x,y) in enumerate(zip(toks,tgts)):
        yy=105+i*85
        out += [rect(55,yy-25,95,40,BLUE,"#EFF6FF",5,2),text(102,yy+1,x,14,700,"middle",BLUE),line(155,yy-5,225,yy-5,RED,2.5,marker="a2"),rect(235,yy-25,95,40,RED,"#FEE2E2",5,2),text(282,yy+1,y,14,700,"middle",RED)]
    out += [text(55,465,"input[t] 预测 target[t]；不得把 target 原位喂入。",13,fill=MUTED)]
    heading(out,430,"B","因果矩阵仍可整批训练",BLUE)
    x0,y0,s=470,115,48
    for i in range(6):
        for j in range(6):
            vis=j<=i
            out += [rect(x0+j*s,y0+i*s,40,40,TEAL if vis else GRID,"#D1FAE5" if vis else "#F1F5F9",2,1.3),text(x0+j*s+20,y0+i*s+25,"✓" if vis else "×",13,700,"middle",TEAL if vis else MUTED)]
    out += [text(455,430,"训练 parallel across rows；",14,700,fill=BLUE),text(455,460,"生成依 token dependency 串行。",14,700,fill=RED)]
    heading(out,830,"C","Decode step t 的 cache",TEAL)
    node(out,845,100,280,52,"new q_t, k_t, v_t",BLUE,"#EFF6FF",14)
    out += [line(985,155,985,190,INK,2,marker="a3")]
    node(out,845,205,280,64,"K_1:t / V_1:t cache",TEAL,"#ECFDF5",15)
    out += [line(985,272,985,307,INK,2,marker="a3")]
    node(out,845,320,280,52,"one new output row",RED,"#FEE2E2",14)
    out += [text(845,410,"Cache 改计算复用，不改变 exact mask 语义。",13,fill=MUTED)]
    return finish(out,"把 shift、mask、loss 与 cache 写成同一时间索引合同，才能排除未来泄漏。")


def encdec():
    out=begin("Encoder–Decoder：Source memory 与 Target queries 的三子层接口",
              "Encoder 只处理 source；decoder 每层先做 target causal mixing，再用 cross-attention 读取固定 source memory。",(BLUE,TEAL,RED))
    heading(out,42,"A","Source encoder",BLUE)
    node(out,55,105,280,60,"source tokens + positions",BLUE,"#EFF6FF",15)
    out += [line(195,168,195,220,INK,2,marker="a3")]
    node(out,55,235,280,70,"bidirectional encoder × L_e",TEAL,"#ECFDF5",14)
    out += [line(195,308,195,360,INK,2,marker="a3")]
    node(out,55,375,280,60,"memory H_e : T_s × d",AMBER,"#FFF7ED",15)
    heading(out,430,"B","Target decoder layer",TEAL)
    for y,lab,col in ((90,"target causal self-attn",RED),(190,"cross-attn: Q from target",TEAL),(290,"K,V from encoder memory",BLUE),(390,"FFN + output states",AMBER)):
        node(out,455,y,300,56,lab,col,"#F8FAFC",14)
        if y<390: out.append(line(605,y+59,605,y+96,INK,2,marker="a3"))
    out += [line(338,405,452,318,BLUE,3,marker="a0")]
    heading(out,830,"C","两条长度轴",RED)
    rows=((110,"source","T_s","encoder + K/V"),(210,"target","T_t","decoder Q + outputs"),(310,"cross score","T_t × T_s","每层每头"),(410,"generation","one row / step","cache source once"))
    for y,name,shape,role in rows:
        out += [text(845,y,name,14,800,fill=RED),text(930,y,shape,15,700),text(930,y+27,role,13,fill=MUTED)]
    return finish(out,"Source 与 target 不是一条拼接序列的别名；它们有不同可见性、长度和缓存生命周期。")


def families():
    out=begin("Transformer 三大家族：Mask、训练目标与任务出口",
              "Encoder-only、encoder–decoder 与 decoder-only 的核心差异先由可见关系和目标定义，再谈规模与应用。",(TEAL,BLUE,RED))
    specs=((42,"A","Encoder-only",TEAL,"all↔all","token/pool","MLM / supervised"),(430,"B","Encoder–Decoder",BLUE,"src↔src; tgt←past+src","target sequence","denoise / seq2seq"),(830,"C","Decoder-only",RED,"prefix causal","next token","LM / prompted tasks"))
    for x,tag,title,col,mask,outlet,obj in specs:
        heading(out,x,tag,title,col)
        node(out,x+15,105,300,62,mask,col,"#F8FAFC",14)
        out += [text(x+15,220,"training objective",13,700,fill=col),text(x+15,252,obj,14,650),text(x+15,320,"task outlet",13,700,fill=col),text(x+15,352,outlet,14,650)]
        if title=="Decoder-only": out += [text(x+15,425,"prefix-LM 可改变 mask；",13,fill=MUTED),text(x+15,452,"仍需精确定义 loss 区域。",13,fill=MUTED)]
        else: out += [text(x+15,425,"家族 ≠ 单一预训练目标",13,fill=MUTED)]
    return finish(out,"架构家族由信息流合同决定；BERT、T5、GPT 是代表实例，不是所有实现的唯一模板。")


def vit():
    out=begin("Vision Transformer：从像素网格到 Patch Tokens",
              "Patchification 把二维局部块展平/投影成序列；patch size 同时控制信息粒度、token 数和二次成本。",(AMBER,BLUE,TEAL))
    heading(out,42,"A","H×W 图像切 P×P patches",AMBER)
    x0,y0=75,115
    for i in range(4):
        for j in range(4):
            out += [rect(x0+j*62,y0+i*62,55,55,AMBER if (i+j)%2 else BLUE,"#FFF7ED" if (i+j)%2 else "#EFF6FF",3,1.5)]
    out += [text(55,405,"N=(H/P)(W/P)",18,800,fill=AMBER),text(55,445,"每块维度 P²C",15,700)]
    heading(out,430,"B","线性 patch embedding + position",BLUE)
    for y,lab,col in ((105,"patch matrix: N × P²C",AMBER),(205,"projection E: P²C × d",BLUE),(305,"tokens: N × d",TEAL),(405,"prepend [CLS] + position",RED)):
        node(out,455,y,300,55,lab,col,"#F8FAFC",14)
        if y<405: out.append(line(605,y+58,605,y+96,INK,2,marker="a3"))
    heading(out,830,"C","分辨率与成本联动",TEAL)
    out += [text(845,115,"H,W ×2; P fixed",15,750,fill=RED),text(845,155,"N ×4, attention pairs ×16",14,700),
            text(845,235,"P ×2; H,W fixed",15,750,fill=BLUE),text(845,275,"N ÷4, finer detail lost",14,700),
            text(845,355,"position table",15,750,fill=TEAL),text(845,395,"resize/interpolate is a new contract",14,fill=MUTED)]
    return finish(out,"ViT 的关键不是把图像叫作句子，而是明确二维切块、位置、读出与分辨率变化。")


def costs():
    out=begin("Transformer 成本总账：参数、投影、Pairwise 与 FFN",
              "一个 block 的主参数约 4d²+2dd_ff；work 还含 T²d，训练/预填充/解码必须分阶段。",(BLUE,RED,TEAL))
    heading(out,42,"A","参数账（忽略 bias）",BLUE)
    rows=((110,"MHA Q/K/V/O","4d²",BLUE),(210,"FFN up/down","2dd_ff",TEAL),(310,"LayerNorm","≈4d",AMBER),(410,"L blocks","L(4d²+2dd_ff)",RED))
    for y,name,val,col in rows:
        out += [text(55,y,name,14,700,fill=col),text(250,y,val,17,800,"middle",col)]
    heading(out,430,"B","每 block 前向 work",RED)
    out += [text(450,110,"projections",14,700,fill=BLUE),text(450,145,"≈ 4 T d²",18,800),text(450,215,"attention pairs",14,700,fill=RED),text(450,250,"≈ 2 T² d",18,800),text(450,320,"FFN",14,700,fill=TEAL),text(450,355,"≈ 2 T d d_ff",18,800),text(450,435,"constants vary with MAC/FLOP convention",12,fill=MUTED)]
    heading(out,830,"C","阶段不同，主导项不同",TEAL)
    for y,title,desc,col in ((105,"training","forward + activations + backward",BLUE),(225,"prefill","all prompt rows; T² pairwise",RED),(345,"decode","one query row; KV grows with t",TEAL)):
        out += [rect(845,y-30,95,42,col,"#F8FAFC",6,2),text(892,y-3,title,13,800,"middle",col),text(955,y-3,desc,12,650)]
    out += [text(845,450,"wall-clock 还依 kernel、IO、batch、dtype。",13,fill=MUTED)]
    return finish(out,"先声明 d、d_ff、T、L、batch、heads 与阶段，再用参数/FLOP/显存/IO 四本账比较。")


def stability():
    out=begin("Transformer 稳定性与表达：结构事实、条件定理与前沿实验",
              "Pre/Post-LN、DeepNorm 与 AttnRes 改变不同接线；可训练、表达、最终质量和系统代价不能互相替代。",(RED,TEAL,AMBER))
    heading(out,42,"A","四种深度接线",RED)
    for y,title,form,col in ((100,"Pre-LN","x + F(LN x)",BLUE),(195,"Post-LN","LN(x + F(x))",TEAL),(290,"DeepNorm","LN(αx + Fβ(x))",AMBER),(385,"AttnRes","depth-attend previous states",RED)):
        out += [text(55,y,title,14,800,fill=col),rect(145,y-27,205,40,col,"#F8FAFC",5,2),text(247,y-2,form,13,700,"middle",col)]
    heading(out,430,"B","问题不止梯度爆炸",TEAL)
    checks=((105,"forward scale"),(175,"input Jacobian"),(245,"parameter update"),(315,"relative layer contribution"),(385,"optimization + generalization"),(455,"memory / communication"))
    for y,lab in checks: out += [circle(465,y-5,8,TEAL,"#ECFDF5",2),text(485,y,lab,14,650)]
    heading(out,830,"C","证据等级",AMBER)
    for y,tag,desc,col in ((110,"I","wiring / shape / exact expansion",TEAL),(190,"T","assumptions + quantified conclusion",BLUE),(270,"E","depth/model/data/kernel version",AMBER),(350,"H","mechanism interpretation",RED),(430,"O","untested scale / task",RED)):
        out += [rect(845,y-25,42,34,col,"#F8FAFC",5,2),text(866,y-2,tag,13,800,"middle",col),text(900,y-2,desc,12,650)]
    return finish(out,"稳定性结论必须说明接线、初始化、深度、优化器和测量对象；前沿方案先作为版本化证据。")


FIGURES={
 "fig-transformer-block-wiring-v1.svg":transformer_block,
 "fig-transformer-encoder-bidirectional-v1.svg":encoder,
 "fig-transformer-decoder-causal-cache-v1.svg":decoder,
 "fig-transformer-encoder-decoder-flow-v1.svg":encdec,
 "fig-transformer-family-contracts-v1.svg":families,
 "fig-vit-patch-tokenization-v1.svg":vit,
 "fig-transformer-cost-ledger-v1.svg":costs,
 "fig-transformer-stability-evidence-v1.svg":stability,
}

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for name,fn in FIGURES.items():
        target=OUT/name
        target.write_text(fn(),encoding="utf-8")
        print(target)

if __name__=="__main__": main()

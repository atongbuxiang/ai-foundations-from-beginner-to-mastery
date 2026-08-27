#!/usr/bin/env python3
"""Generate eight deterministic textbook figures for LM-09--LM-16."""

from pathlib import Path
from plot_calculus_operator_figures_v2 import (
    AMBER, BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)

OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "language-models"


def probability_chain():
    out=begin("序列概率：链式法则、前缀树与 EOS", "联合分布由条件概率沿前缀树相乘；EOS 把长度并入样本空间；负对数把乘积变为逐 token 求和。",(BLUE,TEAL,AMBER))
    heading(out,42,"A","链式法则不是独立假设",BLUE)
    out += [text(55,115,"p(x1,x2,x3)",18,800,fill=BLUE),text(55,165,"= p(x1)",17,650),text(55,205,"× p(x2 | x1)",17,650),text(55,245,"× p(x3 | x1,x2)",17,650),text(55,315,"identity: any joint distribution",14,fill=MUTED)]
    heading(out,430,"B","前缀树分配概率质量",TEAL)
    pts=((470,125,"BOS"),(535,220,"A"),(685,220,"B"),(500,345,"EOS"),(585,345,"B"),(655,345,"A"),(735,345,"EOS"))
    for x,y,lab in pts: out += [circle(x,y,24,TEAL if lab!="EOS" else AMBER,"#ECFDF5" if lab!="EOS" else "#FFF7ED",2),text(x,y+6,lab,13,700,"middle")]
    for x1,y1,x2,y2,p in ((490,140,520,200,".6"),(490,140,670,200,".4"),(535,245,500,320,".2"),(550,245,585,320,".8"),(675,245,655,320,".7"),(695,245,735,320,".3")):
        out += [line(x1,y1,x2,y2,BLUE,2,marker="a0"),text((x1+x2)/2,(y1+y2)/2,p,13,650,"middle",BLUE)]
    heading(out,830,"C","Log loss 是路径码长",AMBER)
    out += [text(845,115,"NLL(x)",18,800,fill=AMBER),text(845,165,"= - log p(x)",18,650),text(845,215,"= sum_t -log p(xt | x<t)",16,650),rect(845,275,285,58,AMBER,"#FFF7ED",6,2),text(987,310,"EOS loss learns length",15,750,"middle",AMBER),text(845,390,"teacher forcing evaluates known prefixes;",13,fill=MUTED),text(845,420,"free generation samples new prefixes.",13,fill=MUTED)]
    return finish(out,"链式法则给联合概率坐标；因果模型的限制来自条件函数族、数据与有限训练，而不是法则本身。")


def causal_shift():
    out=begin("Causal LM：Shift、可见性与 Loss region", "同一训练 batch 中 input token、next-token label、causal attention 和有效 loss mask 是四个独立轴，错一位即可泄漏或漏学。",(RED,BLUE,TEAL))
    heading(out,42,"A","Input / label 右移",RED)
    ins=("<B>","我","爱","AI"); labs=("我","爱","AI","<E>")
    for i,(a,b) in enumerate(zip(ins,labs)):
        y=105+i*78; out += [rect(55,y-25,95,40,BLUE,"#EFF6FF",5,2),text(102,y+1,a,14,700,"middle",BLUE),line(160,y-5,225,y-5,RED,2,marker="a2"),rect(235,y-25,95,40,RED,"#FEE2E2",5,2),text(282,y+1,b,14,700,"middle",RED)]
    out += [text(55,438,"logits[t] predicts label[t] = original[t+1]",13,fill=MUTED)]
    heading(out,430,"B","Inclusive causal relation",BLUE)
    x0,y0,s=470,105,48
    for i in range(6):
        for j in range(6):
            vis=j<=i; out += [rect(x0+j*s,y0+i*s,40,40,TEAL if vis else GRID,"#D1FAE5" if vis else "#F1F5F9",2,1.2),text(x0+j*s+20,y0+i*s+25,"✓" if vis else "×",13,700,"middle",TEAL if vis else MUTED)]
    out += [text(455,430,"mask controls hidden-state information",13,fill=MUTED)]
    heading(out,830,"C","Loss mask controls estimator",TEAL)
    for i,(lab,val,col) in enumerate((("BOS",0,GRID),("prompt",0,AMBER),("answer",1,TEAL),("PAD",0,RED))):
        y=105+i*82; out += [text(845,y,lab,14,700),rect(930,y-24,80,36,col,"#F8FAFC",5,2),text(970,y,val,15,800,"middle",col)]
    out += [text(845,430,"denominator = sum effective targets",13,700,fill=TEAL)]
    return finish(out,"Attention mask 决定能看什么，loss mask 决定学什么；shift 决定第 t 行到底预测哪个 token。")


def mlm_corruption():
    out=begin("Masked LM：Clean、Corruption 与条件预测", "先从 corruption law 抽 mask set，再构造 corrupted input；loss 只在选中位置估计条件分布，不能直接称为规范化 joint likelihood。",(TEAL,RED,BLUE))
    heading(out,42,"A","三个随机对象",TEAL)
    for y,lab,col in ((100,"clean X",BLUE),(210,"mask set M ~ q(M|X)",AMBER),(320,"corrupted X-tilde ~ q(.|X,M)",RED),(430,"targets X_M",TEAL)):
        node(out,55,y,285,52,lab,col,"#F8FAFC",14)
        if y<430: out.append(line(197,y+55,197,y+102,INK,2,marker="a3"))
    heading(out,430,"B","BERT-style 80 / 10 / 10",RED)
    out += [rect(455,125,245,46,RED,"#FEE2E2",5,2),text(577,154,"80%  [MASK]",15,750,"middle",RED),rect(455,215,150,46,AMBER,"#FFF7ED",5,2),text(530,244,"10% random",14,700,"middle",AMBER),rect(455,305,150,46,TEAL,"#ECFDF5",5,2),text(530,334,"10% unchanged",14,700,"middle",TEAL),text(445,420,"ratios are recipe choices, not MLM definition",13,fill=MUTED)]
    heading(out,830,"C","Objective vs pseudo-score",BLUE)
    out += [text(845,115,"training",14,800,fill=TEAL),text(845,155,"E_M sum_{i in M} -log p(x_i | X-tilde)",14,650),text(845,245,"PLL scoring",14,800,fill=BLUE),text(845,285,"sum_i log p(x_i | x_-i)",14,650),rect(845,345,285,60,RED,"#FEE2E2",6,2),text(987,372,"conditionals need not define",13,700,"middle",RED),text(987,394,"one normalized joint",13,700,"middle",RED)]
    return finish(out,"MLM 的核心是 corruption-conditioned prediction；mask recipe、loss denominator 与 pseudo-likelihood 评分必须分别声明。")


def t5_spans():
    out=begin("T5 Span Corruption：Sentinel 建立可逆对齐", "连续被删 spans 在 encoder input 中各由唯一 sentinel 代替；decoder target 按 sentinel 顺序串联被删内容并以最终 sentinel/EOS 收尾。",(AMBER,BLUE,TEAL))
    heading(out,42,"A","Clean sequence + sampled spans",AMBER)
    toks=("A","B","C","D","E","F","G")
    for i,t in enumerate(toks):
        x=55+i*43; col=RED if i in (1,2,5) else BLUE; out += [rect(x,125,36,40,col,"#FEE2E2" if col==RED else "#EFF6FF",4,1.5),text(x+18,151,t,14,700,"middle",col)]
    out += [text(55,220,"spans: [B C], [F]",15,750,fill=RED)]
    heading(out,430,"B","Encoder input",BLUE)
    seq=("A","<X>","D","E","<Y>","G")
    for i,t in enumerate(seq):
        x=445+i*50; col=AMBER if t.startswith("<") else BLUE; out += [rect(x,125,44,40,col,"#FFF7ED" if col==AMBER else "#EFF6FF",4,1.5),text(x+22,151,t,13,700,"middle",col)]
    out += [text(445,220,"sentinel is unique per span",14,fill=MUTED)]
    heading(out,830,"C","Decoder target",TEAL)
    tgt=("<X>","B","C","<Y>","F","<Z>")
    for i,t in enumerate(tgt):
        x=835+i*52; col=AMBER if t.startswith("<") else TEAL; out += [rect(x,125,46,40,col,"#FFF7ED" if col==AMBER else "#ECFDF5",4,1.5),text(x+23,151,t,13,700,"middle",col)]
    out += [text(845,220,"p(target | corrupted input)",16,750,fill=TEAL),text(845,280,"decoder teacher forcing:",14,fill=MUTED),text(845,315,"[BOS,<X>,B,C,<Y>,F] →",14,650),text(845,345,"[<X>,B,C,<Y>,F,<Z>]",14,650),rect(845,395,285,48,RED,"#FEE2E2",5,2),text(987,425,"sentinel order = alignment contract",13,750,"middle",RED)]
    return finish(out,"Span corruption 提高每个 sentinel 的信息负载；唯一 sentinel 与 target 顺序使多 span 重建保持可对齐。")


def prefix_masks():
    out=begin("Prefix LM / UniLM：同一序列的分块可见性", "Prefix 内双向，suffix 读取全部 prefix 与过去 suffix；可见性矩阵、segment IDs 和 loss region 联合定义 seq2seq 目标。",(BLUE,TEAL,RED))
    heading(out,42,"A","Sequence blocks",BLUE)
    out += [rect(55,120,200,55,BLUE,"#EFF6FF",6,2),text(155,154,"prefix / source",16,750,"middle",BLUE),rect(265,120,95,55,TEAL,"#ECFDF5",6,2),text(312,154,"suffix",15,750,"middle",TEAL),text(55,230,"[source tokens | target tokens]",15,650)]
    heading(out,430,"B","Relation matrix",TEAL)
    x0,y0,s=465,100,52; P=3; T=6
    for i in range(T):
        for j in range(T):
            vis=(i<P and j<P) or (i>=P and j<=i)
            col=BLUE if i<P and j<P else TEAL
            out += [rect(x0+j*s,y0+i*s,43,43,col if vis else GRID,"#DBEAFE" if vis and col==BLUE else "#D1FAE5" if vis else "#F1F5F9",2,1.2),text(x0+j*s+21,y0+i*s+27,"✓" if vis else "×",13,700,"middle",col if vis else MUTED)]
    heading(out,830,"C","Loss region remains separate",RED)
    for i,(lab,val,col) in enumerate((("prefix targets",0,BLUE),("suffix targets",1,TEAL),("padding",0,RED))):
        y=110+i*90; out += [text(845,y,lab,14,700),rect(1010,y-24,75,36,col,"#F8FAFC",5,2),text(1047,y,val,15,800,"middle",col)]
    out += [text(845,395,"same stack ≠ same objective",14,800,fill=RED),text(845,430,"mask relation and labels are independent",13,fill=MUTED)]
    return finish(out,"Prefix/UniLM 通过 relation 改变条件集；是否预测 prefix、suffix 或 masked positions 仍由独立 loss mask 决定。")


def mixture_denoisers():
    out=begin("Mixture-of-Denoisers：先抽 Mode，再抽 Corruption", "多目标训练是层级随机实验：mode weight、corruption severity、target count 和 sequence cost 共同决定实际梯度份额。",(TEAL,AMBER,RED))
    heading(out,42,"A","Hierarchical sampler",TEAL)
    node(out,55,100,285,52,"m ~ Categorical(pi)",TEAL,"#ECFDF5",15)
    out += [line(197,155,197,195,INK,2,marker="a3")]
    node(out,55,210,285,52,"c ~ q_m(c | x)",AMBER,"#FFF7ED",15)
    out += [line(197,265,197,305,INK,2,marker="a3")]
    node(out,55,320,285,52,"loss L_m(theta;x,c)",RED,"#FEE2E2",15)
    out += [text(55,425,"E[L] = sum_m pi_m E_c[L_m]",15,700)]
    heading(out,430,"B","UL2-style denoiser families",AMBER)
    for y,tag,desc,col in ((105,"R","regular short-span denoising",TEAL),(220,"S","sequential / causal-like",BLUE),(335,"X","extreme long-span denoising",RED)):
        out += [rect(445,y-25,55,42,col,"#F8FAFC",5,2),text(472,y+2,tag,15,800,"middle",col),text(520,y+2,desc,13,650)]
    heading(out,830,"C","Nominal pi is not gradient share",RED)
    out += [text(845,110,"mode frequency",14,700,fill=BLUE),text(845,150,"× target tokens",14,700,fill=TEAL),text(845,190,"× loss reduction",14,700,fill=AMBER),text(845,230,"× gradient norm/covariance",14,700,fill=RED),line(845,255,1120,255,INK,2),text(845,300,"= realized optimization pressure",15,800),rect(845,355,285,55,RED,"#FEE2E2",6,2),text(987,388,"log numerator + denominator per mode",13,750,"middle",RED)]
    return finish(out,"多目标的权重必须落实到样本、有效 targets、归约和梯度；配置中的 mixture probability 不是全部答案。")


def metrics():
    out=begin("NLL、Perplexity 与 BPB：分母决定可比性", "同一字符串概率可以在不同 tokenizer 下拥有不同 per-token NLL/PPL；按相同 raw bytes 归一的 BPB 才有共同单位。",(BLUE,AMBER,TEAL))
    heading(out,42,"A","同一 total NLL，不同 token count",BLUE)
    out += [text(55,115,"-log p(x) = 12 nats",17,800,fill=BLUE),text(55,185,"Tokenizer A: T=4",15,700),text(55,225,"NLL/token=3, PPL=e^3",15,650),text(55,300,"Tokenizer B: T=8",15,700),text(55,340,"NLL/token=1.5, PPL=e^1.5",15,650),text(55,420,"PPL ranking differs though string probability same",13,fill=RED)]
    heading(out,430,"B","共同 raw-byte 分母",AMBER)
    out += [text(445,115,"B = 16 UTF-8 bytes",16,700),text(445,175,"BPB = NLL_nats / (B ln 2)",17,800,fill=AMBER),text(445,235,"= 12 / (16 ln 2)",16,650),text(445,285,"≈ 1.082 bits/byte",18,800,fill=TEAL),rect(445,350,310,55,BLUE,"#EFF6FF",6,2),text(600,383,"same for A and B",15,750,"middle",BLUE)]
    heading(out,830,"C","Four denominators",TEAL)
    for i,(lab,col) in enumerate((("loss-bearing tokens",BLUE),("all sequence tokens",AMBER),("Unicode graphemes",TEAL),("raw UTF-8 bytes",RED))):
        y=100+i*85; out += [rect(845,y,285,48,col,"#F8FAFC",5,2),text(987,y+30,lab,14,700,"middle",col)]
    out += [text(845,450,"state tokenizer + BOS/EOS + mask + log base",13,fill=MUTED)]
    return finish(out,"PPL 是指定 token 坐标下的几何平均分支因子；跨 tokenizer 比较必须回到 total likelihood 与共同原始单位。")


def evidence_map():
    out=begin("GPT、BERT、T5：目标—架构—证据拆分", "代表模型同时改变 objective、visibility、architecture、data 和 transfer protocol；观察到的能力差异不能只归因于模型家族名。",(RED,TEAL,BLUE))
    heading(out,42,"A","GPT-like",RED)
    out += [text(55,115,"objective",13,700,fill=RED),text(55,150,"next-token CLM",15,750),text(55,215,"visibility",13,700,fill=RED),text(55,250,"causal",15,750),text(55,315,"outlet",13,700,fill=RED),text(55,350,"autoregressive text",15,750),text(55,420,"evidence: model/data/scale specific",13,fill=MUTED)]
    heading(out,430,"B","BERT-like",TEAL)
    out += [text(445,115,"objective",13,700,fill=TEAL),text(445,150,"corrupted-token MLM",15,750),text(445,215,"visibility",13,700,fill=TEAL),text(445,250,"bidirectional corrupted input",15,750),text(445,315,"outlet",13,700,fill=TEAL),text(445,350,"representations / fill mask",15,750),text(445,420,"PLL is a derived score",13,fill=MUTED)]
    heading(out,830,"C","T5-like",BLUE)
    out += [text(845,115,"objective",13,700,fill=BLUE),text(845,150,"span denoising seq2seq",15,750),text(845,215,"visibility",13,700,fill=BLUE),text(845,250,"encoder full + decoder causal",15,750),text(845,315,"outlet",13,700,fill=BLUE),text(845,350,"conditional target text",15,750),text(845,420,"sentinels bind removed spans",13,fill=MUTED)]
    return finish(out,"架构、可见性、corruption、loss 与数据必须逐轴比较；“GPT/BERT/T5 更强”不是无条件科学命题。")


FIGURES={
 "fig-lm-probability-chain-eos-v1.svg":probability_chain,
 "fig-lm-causal-shift-mask-loss-v1.svg":causal_shift,
 "fig-lm-mlm-corruption-pseudolikelihood-v1.svg":mlm_corruption,
 "fig-lm-t5-span-sentinel-v1.svg":t5_spans,
 "fig-lm-prefix-unilm-mask-v1.svg":prefix_masks,
 "fig-lm-mixture-denoisers-ledger-v1.svg":mixture_denoisers,
 "fig-lm-nll-ppl-bpb-denominator-v1.svg":metrics,
 "fig-lm-gpt-bert-t5-evidence-v1.svg":evidence_map,
}


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for name,fn in FIGURES.items():
        target=OUT/name; target.write_text(fn(),encoding="utf-8"); print(target)


if __name__=="__main__": main()

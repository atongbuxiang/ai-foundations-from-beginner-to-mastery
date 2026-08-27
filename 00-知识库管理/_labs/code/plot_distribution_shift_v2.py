#!/usr/bin/env python3
"""Generate LT-65--68 paper-ink shift and robustness figures."""
from pathlib import Path
from plot_calculus_operator_figures_v2 import BLUE,TEAL,RED,INK,MUTED,begin,finish,heading,line,node,text
OUT=Path(__file__).resolve().parents[2]/"_assets"/"figures"/"learning-theory"

def panel(title,desc,heads,rows,foot):
    out=begin(title,desc,(BLUE,TEAL,RED))
    colors=(BLUE,TEAL,RED)
    for j,(lab,head) in enumerate(zip(("A","B","C"),heads)):
        x=42+400*j; heading(out,x,lab,head,colors[j])
        for i,(txt,col) in enumerate(rows[j]):
            node(out,x+13,92+84*i,300,56,txt,col,size=15)
            if i<4: out.append(line(x+163,151+84*i,x+163,173+84*i,INK,2,marker="a3"))
        out.append(text(x+3,515,foot[j],15,fill=MUTED))
    return finish(out,desc)

def shift():
    return panel("Dataset Shift：因子、识别与证据流","先定位joint law中改变的因子，再判断target evidence是否足以识别与校正。",
      ("两种 Joint Factorization","三类 Shift 与硬边界","从 Detection 到 Evaluation"),
      ((("p(x,y)=p(y|x)p(x)",BLUE),("p(x,y)=p(x|y)p(y)",TEAL),("same joint, different assumptions",RED)),
       (("covariate: p(x) changes",BLUE),("label: p(y) changes",TEAL),("concept: p(y|x) changes",RED),("support gap: not identifiable",RED)),
       (("detect observable change",BLUE),("diagnose factor + assumptions",TEAL),("correct under overlap / rank",RED),("locked target evaluation",BLUE))),
      ("factorization prevents name confusion。","shift types may overlap。","detection is not diagnosis。"))

def weighting():
    return panel("Importance Weighting：期望恒等式与有限样本稳定性","covariate shift下target risk可重写；weight tail、ratio error和selection决定实际可靠性。",
      ("Target Risk Change of Measure","Ratio、Tail 与 ESS","训练—选择—部署合同"),
      ((("p_t(y|x)=p_s(y|x)",BLUE),("w(x)=p_t(x)/p_s(x)",TEAL),("R_t=E_s[w loss]",RED),("target support inside source",BLUE)),
       (("domain odds / direct ratio",BLUE),("large weights -> high variance",RED),("ESS=(sum w)^2/sum w^2",TEAL),("clip / normalize adds bias",RED)),
       (("cross-fit ratio estimates",BLUE),("weighted validation",TEAL),("locked target test",RED),("concept shift: stop",RED))),
      ("identity is population-level。","mean weight=1 is insufficient。","weights cannot create labels。"))

def adaptation():
    return panel("Domain Adaptation Bound：三账户与表示对齐","target risk由source risk、hypothesis-relative discrepancy和joint ideal error共同控制。",
      ("经典 Target-Risk Bound","DANN 控制哪一部分","不可省略的 Compatibility"),
      ((("R_T(h)",RED),("<= R_S(h)",BLUE),("+ 1/2 HDeltaH discrepancy",TEAL),("+ lambda joint ideal error",RED)),
       (("feature extractor Phi",BLUE),("source label head",TEAL),("domain adversary",RED),("chance domain accuracy",BLUE)),
       (("lambda may be large",RED),("constant feature is invariant",RED),("DG has no target inputs",BLUE),("target validation leaks",TEAL))),
      ("proof uses disagreement triangle。","domain confusion is only one term。","invariance is not sufficiency。"))

def ood():
    return panel("OOD、Robustness 与 Causal Claim Ladder","score ranking、部署效用、自然shift与因果识别是逐级增强而非同义结论。",
      ("先锁定任务与 Out-Law","Metric、Group 与 Shift Family","因果声明需要额外结构"),
      ((("misclassification detection",BLUE),("specified OOD pair",TEAL),("selective prediction",RED),("natural / adversarial robustness",BLUE)),
       (("AUROC is ranking",BLUE),("threshold needs prevalence + cost",TEAL),("average != worst group",RED),("synthetic != natural shift",RED)),
       (("SCM + variable semantics",BLUE),("intervention targets",TEAL),("mechanism invariance",RED),("finite environments may fail",RED))),
      ("no universal OOD score。","benchmark gain is local evidence。","domain invariance is not causality。"))

FIGURES={"fig-dataset-shift-factorizations-v2.svg":shift,"fig-importance-weighting-overlap-v2.svg":weighting,"fig-domain-adaptation-bound-v2.svg":adaptation,"fig-ood-robustness-causal-boundaries-v2.svg":ood}
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for n,f in FIGURES.items():
        p=OUT/n;p.write_text(f(),encoding="utf-8");print(p)
if __name__=="__main__":main()

#!/usr/bin/env python3
"""Generate deterministic NN-05--08 expressivity figures."""
from pathlib import Path
from plot_calculus_operator_figures_v2 import BG, BLUE, GRID, INK, MUTED, RED, TEAL, begin, circle, finish, heading, line, node, path, rect, text
OUT=Path(__file__).resolve().parents[2]/"_assets"/"figures"/"neural-networks"

def xor():
 o=begin("XOR、非线性折叠与隐藏读出","XOR 的两类凸包相交；ReLU hinges 把和坐标折成 hat；隐藏空间中线性输出即可读出。",(BLUE,TEAL,RED)); heading(o,42,"A","原空间：凸包相交",BLUE)
 for x,y,c,l in ((90,390,RED,"0"),(310,140,RED,"0"),(90,140,BLUE,"1"),(310,390,BLUE,"1")): o += [circle(x,y,10,c,c),text(x+15,y-8,l,15,700,fill=c)]
 o += [line(90,390,310,140,RED,4),line(90,140,310,390,BLUE,4),circle(200,265,8,INK,BG,2),text(45,465,"conv(positive) ∩ conv(negative) ≠ ∅",16,700,fill=RED),text(45,500,"单个 affine threshold 不可能严格分离。",15,fill=MUTED)]
 heading(o,430,"B","三个 hinge 拼成 hat",TEAL); o += [line(450,430,760,430,GRID,2),line(475,455,475,105,GRID,2),path("M475 430L615 145L755 430",TEAL,4),text(610,125,"f(s)",17,700,"middle",TEAL)]
 for x,l in ((475,"0"),(615,"1"),(755,"2")): o += [circle(x,430,5,INK,INK),text(x,458,l,15,650,"middle")]
 o += [text(430,495,"ReLU(s) − 2ReLU(s−1) + ReLU(s−2)",15,650,cls="math")]
 heading(o,830,"C","隐藏表示 → 线性读出",RED); node(o,845,105,285,62,"x → s=x1+x2",BLUE); node(o,845,215,285,72,"h=(R(s),R(s−1),R(s−2))",TEAL,size=15); node(o,845,340,285,62,"v=(1,−2,1) → y",RED); o += [line(987,170,987,208,INK,2,marker="a3"),line(987,290,987,333,INK,2,marker="a3"),text(842,465,"表示可有意合并任务等价输入。",15,fill=MUTED)]
 return finish(o,"非线性先改变几何，再由线性层读出；有限点拟合不等于全域函数唯一。")

def uat():
 o=begin("万能逼近：对象合同、稠密性与三座桥","UAT 绑定 domain、target、activation、network union 与 norm；其结论停在表示存在性。",(BLUE,TEAL,RED)); heading(o,42,"A","五个对象缺一不可",BLUE)
 for i,s in enumerate(("compact K","target C(K)","activation σ","all finite widths","sup norm")): node(o,55,92+i*78,290,52,s,BLUE if i<2 else TEAL,size=15)
 heading(o,430,"B","量词与反证骨架",TEAL); o += [text(435,110,"∀f  ∀ε>0  ∃m,θ",20,700,fill=TEAL,cls="math"),text(435,150,"||f−gθ||∞ < ε",18,650,cls="math")]
 for i,s in enumerate(("not dense","Hahn–Banach functional","Riesz signed measure","halfspaces force μ=0")): node(o,445,205+i*70,305,48,s,RED if i==0 else TEAL,size=15)
 heading(o,830,"C","结论停在哪里",RED)
 for i,(s,c) in enumerate((("representation exists",TEAL),("optimizer reaches it?",BLUE),("finite data selects it?",RED),("resource rate efficient?",BLUE))): node(o,845,95+i*92,285,56,s,c,size=15)
 o += [text(840,487,"UAT 只回答第一行。",16,700,fill=RED)]
 return finish(o,"先补全函数空间和误差，再区分存在、训练、统计与资源效率。")

def depth():
 o=begin("深度分离：复合折叠与浅层枚举","tent map 的重复复合指数增加单调线性段；浅层一维 ReLU 每个 unit 至多添加一个 breakpoint。",(BLUE,TEAL,RED)); heading(o,42,"A","复合次数增加折叠",BLUE)
 for j,n in enumerate((2,4,8)):
  y=145+j*125; pts=[]
  for k in range(n+1):
   x=60+300*k/n; yy=y-55 if k%2 else y+35; pts.append((x,yy))
  o.append(path("M"+"L".join(f"{x} {yy}" for x,yy in pts),BLUE if j==0 else TEAL,3)); o.append(text(45,y+62,f"T composed {j+1}: {n} pieces",15,650))
 heading(o,430,"B","deep reuse vs shallow list",TEAL); node(o,455,110,125,55,"tent module",TEAL); node(o,640,110,110,55,"repeat L",BLUE); o += [line(585,138,635,138,INK,2,marker="a3"),text(430,230,"constant-width composition",16,700,fill=TEAL),text(430,275,"→ about 2^L pieces",18,700,fill=RED),text(430,350,"one hidden layer: m ReLUs",16,700,fill=BLUE),text(430,395,"→ at most m+1 intervals",18,700,fill=RED),text(430,470,"lower bound 还需指定误差与目标分布。",15,fill=MUTED)]
 heading(o,830,"C","四种结论分账",RED)
 for i,s in enumerate(("expressivity / regions","approximation lower bound","optimization reachability","generalization + hardware")): node(o,845,100+i*92,285,56,s,(TEAL,BLUE,RED,BLUE)[i],size=15)
 return finish(o,"指数表达优势是目标族—资源—误差定理，不是越深越好的一般经验律。")

def symmetry():
 o=begin("参数对称性：轨道、纤维与函数商空间","隐藏置换和 ReLU 正缩放改变坐标却保持函数；冗余单元形成连续纤维。",(BLUE,TEAL,RED)); heading(o,42,"A","置换需相邻层补偿",BLUE)
 node(o,55,115,95,52,"W1",BLUE); node(o,185,115,95,52,"hidden",TEAL); node(o,315,115,55,52,"W2",RED); o += [line(155,141,180,141,INK,2,marker="a3"),line(285,141,310,141,INK,2,marker="a3"),text(45,235,"W1→W1P, b1→b1P",16,650),text(45,280,"W2→P⁻¹W2",16,650),text(45,350,"hidden units 只是内部坐标名字。",15,fill=MUTED)]
 heading(o,430,"B","ReLU 连续缩放纤维",TEAL); o += [text(440,120,"ReLU(cz)=c ReLU(z), c>0",17,700,fill=TEAL,cls="math"),path("M455 330C520 170 650 170 755 330",TEAL,4),circle(485,280,7,BLUE,BLUE),circle(720,280,7,RED,RED),text(605,365,"同一 function 的参数轨道",16,650,"middle"),text(430,440,"incoming ×c；outgoing ÷c",16,700),text(430,482,"参数距离可变，函数距离为 0。",15,fill=MUTED)]
 heading(o,830,"C","投影到 quotient 后",RED); o += [circle(900,145,34,BLUE,BG,3),circle(1065,145,34,TEAL,BG,3),path("M870 260C920 205 1030 205 1095 260",GRID,3),line(980,270,980,335,INK,2,marker="a3")]; node(o,870,345,220,62,"one equivalence class [θ]",RED,size=15); o += [text(840,455,"Hessian flatness / merging / posterior",15,650),text(840,492,"都应先处理 symmetry。",16,700,fill=RED)]
 return finish(o,"比较模型时优先使用函数或对齐后的参数；可辨识性必须写成 modulo symmetry。")

FIG={"fig-xor-hidden-representation-v2.svg":xor,"fig-universal-approximation-contract-v2.svg":uat,"fig-depth-separation-regions-v2.svg":depth,"fig-parameter-symmetry-quotient-v2.svg":symmetry}
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 for n,b in FIG.items(): (OUT/n).write_text(b(),encoding="utf-8"); print(OUT/n)
if __name__=="__main__": main()

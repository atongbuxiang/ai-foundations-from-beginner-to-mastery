import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../..');
const outDir = path.join(root, '00-知识库管理/_assets/figures/training-optimization');
fs.mkdirSync(outDir, { recursive: true });

const C = {
  ink: '#1F2937', gray: '#64748B', grid: '#D7DEE8', blue: '#2563EB',
  teal: '#0F766E', amber: '#B7791F', red: '#C24135', paper: '#FFFEFB',
  paleBlue: '#EFF6FF', paleTeal: '#ECFDF5', paleAmber: '#FFFBEB', paleRed: '#FEF2F2'
};
const FONT = 'Inter, PingFang SC, Noto Sans CJK SC, sans-serif';
const MONO = 'SFMono-Regular, Consolas, monospace';
const esc = s => String(s).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
const attrs = o => Object.entries(o).map(([k, v]) => `${k.replaceAll('_', '-')}="${esc(v)}"`).join(' ');
const t = (x, y, s, o = {}) => `<text x="${x}" y="${y}" ${attrs({
  'font-family': o.mono ? MONO : FONT, 'font-size': o.size ?? 18,
  'font-weight': o.weight ?? 400, fill: o.fill ?? C.ink,
  'text-anchor': o.anchor ?? 'start', 'dominant-baseline': o.base ?? 'alphabetic'
})}>${esc(s)}</text>`;
const line = (x1, y1, x2, y2, o = {}) => `<line ${attrs({x1, y1, x2, y2, stroke: o.stroke ?? C.ink, 'stroke-width': o.width ?? 2, 'stroke-dasharray': o.dash ?? '', 'marker-end': o.arrow ? 'url(#arrow)' : ''})}/>`;
const rect = (x, y, w, h, o = {}) => `<rect ${attrs({x, y, width: w, height: h, rx: o.rx ?? 0, fill: o.fill ?? 'none', stroke: o.stroke ?? C.grid, 'stroke-width': o.width ?? 1.8, 'stroke-dasharray': o.dash ?? ''})}/>`;
const circ = (x, y, r, o = {}) => `<circle ${attrs({cx: x, cy: y, r, fill: o.fill ?? C.paper, stroke: o.stroke ?? C.ink, 'stroke-width': o.width ?? 2})}/>`;
const poly = (points, o = {}) => `<polyline ${attrs({points, fill: o.fill ?? 'none', stroke: o.stroke ?? C.ink, 'stroke-width': o.width ?? 2.5, 'stroke-dasharray': o.dash ?? '', 'marker-end': o.arrow ? 'url(#arrow)' : '', 'stroke-linejoin': 'round', 'stroke-linecap': 'round'})}/>`;
const pathEl = (d, o = {}) => `<path ${attrs({d, fill: o.fill ?? 'none', stroke: o.stroke ?? C.ink, 'stroke-width': o.width ?? 2.5, 'stroke-dasharray': o.dash ?? '', 'marker-end': o.arrow ? 'url(#arrow)' : '', 'stroke-linejoin': 'round', 'stroke-linecap': 'round'})}/>`;
const defs = `<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="${C.ink}"/></marker><marker id="arrowBlue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="${C.blue}"/></marker></defs>`;
const svg = (title, desc, h, body) => `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="${h}" viewBox="0 0 1200 ${h}" role="img" aria-labelledby="title desc">
<title id="title">${esc(title)}</title><desc id="desc">${esc(desc)}</desc><style>text{font-family:${FONT};}</style>${defs}<rect width="1200" height="${h}" fill="${C.paper}"/>${body}</svg>\n`;

const figures = new Map();

// TRN-65: layered ledger over a shared multi-clock rail.
{
  let b = '';
  b += t(66, 55, '同一事件，五个时钟', {size: 25, weight: 700});
  b += line(250, 72, 1130, 72, {stroke: C.grid, width: 1.5});
  const clocks = [['wall', '10:31:08'], ['micro', '48012'], ['update', '12003'], ['token', '8.6B'], ['schedule', 'warmup→stable']];
  clocks.forEach(([a, v], i) => { const x = 290 + i * 178; b += circ(x, 92, 7, {fill: C.blue, stroke: C.blue}); b += t(x, 119, a, {size: 16, weight: 650, anchor: 'middle', fill: C.gray}); b += t(x, 143, v, {size: 17, mono: true, anchor: 'middle'}); });
  b += line(290, 92, 1002, 92, {stroke: C.blue, width: 2.5});
  b += t(66, 190, '六本账沿同一 step 对齐', {size: 24, weight: 700});
  const ledgers = [
    ['数据', 'token IDs · length · mask', C.blue, C.paleBlue],
    ['目标', 'loss numerator / denominator', C.ink, '#F8FAFC'],
    ['梯度', 'RMS · amax · nonfinite · clip', C.red, C.paleRed],
    ['更新', 'direction · decay · actual delta', C.amber, C.paleAmber],
    ['参数/激活', 'layer · unit · quantile · spectrum', C.teal, C.paleTeal],
    ['系统', 'input · compute · comm · memory', C.gray, '#F8FAFC']
  ];
  ledgers.forEach(([name, detail, col, fill], i) => { const y = 222 + i * 64; b += rect(72, y, 1040, 46, {fill, stroke: col, width: 1.8}); b += t(104, y + 29, name, {size: 18, weight: 700, fill: col}); b += t(250, y + 29, detail, {size: 17}); b += line(720, y + 23, 1070, y + 23, {stroke: C.grid, width: 1.8}); b += circ(880 + (i % 3) * 55, y + 23, 5, {fill: col, stroke: col}); });
  b += t(72, 626, 'L0 每步标量', {size: 18, weight: 700, fill: C.blue});
  b += line(205, 620, 350, 620, {stroke: C.blue, arrow: true});
  b += t(380, 626, 'L1 低频分层', {size: 18, weight: 700, fill: C.teal});
  b += line(525, 620, 670, 620, {stroke: C.teal, arrow: true});
  b += t(700, 626, 'L2 告警后窄窗重诊断', {size: 18, weight: 700, fill: C.red});
  b += t(72, 661, '先对齐时钟，再比较 first-change time；先后顺序仍不是因果证明。', {size: 17, fill: C.gray});
  figures.set('fig-training-telemetry-ledger-v1.svg', svg('训练 Telemetry 的时钟与六本账', '五个训练时钟对齐六类数据、目标、梯度、更新、激活和系统记录，并以三级采集控制观测开销。', 690, b));
}

// TRN-66: top timeline plus open decision tree.
{
  let b = '';
  b += t(66, 54, '时间二分：正常边界 → 第一异常步', {size: 24, weight: 700});
  b += line(92, 103, 1110, 103, {stroke: C.ink, width: 2.8});
  const pts = [[130,'ckpt 12k',C.teal],[390,'18k',C.teal],[650,'21k ?',C.amber],[910,'22.5k',C.red],[1080,'loss NaN',C.red]];
  pts.forEach(([x,s,c]) => { b += circ(x, 103, 9, {fill: c, stroke: c}); b += t(x, 137, s, {size: 16, anchor: 'middle', fill: c, weight: 650}); });
  b += pathEl('M 390 83 Q 650 20 910 83', {stroke: C.amber, dash: '7 6'});
  b += t(650, 38, 'checkpoint replay：O(log interval)', {size: 17, anchor: 'middle', fill: C.amber});
  b += t(66, 190, '在哪一道合同边界首次违约？', {size: 24, weight: 700});
  const xs = [125, 340, 555, 770, 985];
  const labels = [['数据','ID · mask · target'],['前向','activation · loss'],['反向','gradient · scale'],['更新','state · actual delta'],['系统','rank · collective']];
  xs.forEach((x,i) => { const col = i===2 ? C.red : (i<2 ? C.blue : C.amber); b += circ(x, 255, 38, {fill: C.paper, stroke: col, width: 3}); b += t(x, 251, `${i+1}`, {size: 20, weight: 750, anchor: 'middle', fill: col}); b += t(x, 283, labels[i][0], {size: 18, weight: 700, anchor: 'middle'}); if (i<4) b += line(x+40,255,xs[i+1]-42,255,{stroke:C.grid,arrow:true}); b += t(x, 326, labels[i][1], {size: 16, anchor:'middle',fill:C.gray}); });
  b += line(555, 340, 555, 388, {stroke: C.red, width: 3, arrow: true});
  b += t(555, 379, 'first bad event', {size: 18, anchor: 'middle', fill: C.red, weight: 700});
  b += t(66, 430, '候选修复必须通过四格反事实', {size: 23, weight: 700});
  const cells = [
    [90,470,'Replay A','原配置 + 触发 batch','应复现',C.red,C.paleRed],
    [590,470,'Replay B','候选修复 + 触发 batch','异常消失',C.teal,C.paleTeal],
    [90,570,'Control C','原配置 + 对照 batch','不故障',C.blue,C.paleBlue],
    [590,570,'Quality D','修复 + 正常数据流','质量/成本不过界',C.amber,C.paleAmber]
  ];
  cells.forEach(([x,y,a,d,r,c,f]) => { b += rect(x,y,445,72,{fill:f,stroke:c,width:2}); b += t(x+18,y+27,a,{size:18,weight:750,fill:c}); b += t(x+150,y+27,d,{size:16}); b += t(x+150,y+54,`→ ${r}`,{size:16,weight:650,fill:c}); });
  b += t(90, 680, '“不再 NaN”只表示止血；复现 + 对照 + 质量门共同支持修复。', {size: 17, fill: C.gray});
  figures.set('fig-first-bad-event-tree-v1.svg', svg('训练失败的 first-bad-event 决策树', '先在 checkpoint 时间轴二分，再沿数据、前向、反向、更新与系统边界定位，最后用四格反事实验证修复。', 710, b));
}

// TRN-67: contrasting scalar/layer/spectrum views, not a card dashboard.
{
  let b = '';
  b += t(66, 54, '同一次更新的三种分辨率', {size: 25, weight: 700});
  b += line(398, 82, 398, 590, {stroke: C.grid, dash: '6 7'}); b += line(802, 82, 802, 590, {stroke: C.grid, dash: '6 7'});
  b += t(210, 100, '全局 scalar', {size: 22, weight: 700, anchor: 'middle'});
  b += circ(210, 250, 115, {fill: C.paper, stroke: C.blue, width: 4});
  b += t(210, 238, 'UWR', {size: 24, weight: 750, anchor: 'middle', fill: C.blue});
  b += t(210, 272, '||delta|| / ||weight||', {size: 17, anchor: 'middle', mono: true});
  b += t(210, 318, '正常范围', {size: 18, anchor: 'middle', fill: C.teal, weight: 700});
  b += t(210, 425, '大层支配平均', {size: 18, anchor: 'middle', fill: C.gray});
  b += t(210, 453, '局部异常可被抵消', {size: 18, anchor: 'middle', fill: C.gray});
  b += t(600, 100, 'layer / unit', {size: 22, weight: 700, anchor: 'middle'});
  const vals = [0.18,0.24,0.31,0.20,0.86,0.27,0.22];
  vals.forEach((v,i)=>{const y=155+i*52; b+=t(455,y+18,`L${i+1}`,{size:16,mono:true}); b+=line(500,y+12,750,y+12,{stroke:C.grid,width:7}); b+=line(500,y+12,500+v*270,y+12,{stroke:i===4?C.red:C.blue,width:7}); b+=t(765,i===4?y-2:y+18,i===4?'0.86 ↑':v.toFixed(2),{size:16,anchor:'end',fill:i===4?C.red:C.gray,weight:i===4?700:400});});
  b += t(600, 552, 'global mean 不会替 layer 说话', {size: 17, anchor: 'middle', fill: C.red});
  b += t(1000, 100, 'operator / spectrum', {size: 22, weight: 700, anchor: 'middle'});
  b += line(855, 470, 1135, 470, {stroke:C.ink,width:2}); b += line(855, 470, 855, 155, {stroke:C.ink,width:2});
  b += t(995, 505, 'singular direction', {size:16,anchor:'middle',fill:C.gray});
  const sp = [[870,180],[905,330],[940,382],[975,411],[1010,430],[1045,442],[1080,450],[1120,455]];
  b += poly(sp.map(p=>p.join(',')).join(' '), {stroke:C.red,width:4});
  b += circ(870,180,8,{fill:C.red,stroke:C.red}); b += t(890,172,'rank-one spike',{size:17,fill:C.red,weight:700});
  b += t(997, 540, 'RMS 小，top singular value 仍可大', {size:17,anchor:'middle',fill:C.red});
  b += line(210,585,1000,585,{stroke:C.ink,width:2.5,arrow:true});
  b += t(600, 621, '再沿 gradient → preconditioned direction → realized update 比较时钟', {size:18,anchor:'middle',weight:650});
  figures.set('fig-update-weight-spectrum-cube-v1.svg', svg('Update-to-Weight Ratio 的三种分辨率', '同一次更新分别从全局标量、层与单元、谱方向观察，说明正常的全局 RMS 可以隐藏局部或低秩尖峰。', 655, b));
}

// TRN-68: causal DAG with explicit node shapes and blocked/open paths.
{
  let b = '';
  b += t(64, 54, 'Recipe bundle 不是单一 treatment', {size: 24, weight: 700});
  const nodes = [
    [80,95,170,58,'Data mix','D',C.blue,C.paleBlue], [300,95,170,58,'Optimizer','O',C.blue,C.paleBlue],
    [520,95,170,58,'Schedule','S',C.blue,C.paleBlue], [740,95,170,58,'Precision/system','P',C.blue,C.paleBlue]
  ];
  nodes.forEach(([x,y,w,h,a,d,c,f])=>{b+=rect(x,y,w,h,{fill:f,stroke:c,width:2});b+=t(x+w/2,y+25,a,{size:17,anchor:'middle',weight:700,fill:c});b+=t(x+w/2,y+47,d,{size:16,anchor:'middle',mono:true,fill:c});});
  b += rect(965,95,155,58,{fill:C.paleAmber,stroke:C.amber,width:2}); b += t(1042,121,'完整 bundle',{size:17,anchor:'middle',weight:700,fill:C.amber}); b+=t(1042,144,'A=(D,O,S,P)',{size:16,anchor:'middle',mono:true});
  nodes.forEach(([x,y,w,h])=>b+=line(x+w,y+h/2,960,124,{stroke:C.gray,width:1.7,arrow:true}));
  b += t(64, 212, '因果图：先标变量角色，再决定是否控制', {size: 24, weight: 700});
  const nd = (x,y,w,h,label,sub,col,fill,shape='rect') => { b += shape==='circle'?circ(x,y,w/2,{fill,stroke:col,width:2.5}):rect(x-w/2,y-h/2,w,h,{fill,stroke:col,width:2.5}); b += t(x,y-3,label,{size:18,anchor:'middle',weight:700,fill:col}); b += t(x,y+20,sub,{size:15,anchor:'middle',fill:C.gray}); };
  nd(160,330,118,58,'U','time / drift',C.red,C.paleRed,'circle'); nd(390,330,150,64,'A','training recipe',C.blue,C.paleBlue); nd(625,330,150,64,'M','update / act.',C.amber,C.paleAmber); nd(855,330,150,64,'V','validation',C.teal,C.paleTeal); nd(1060,330,120,64,'Y','test / deploy',C.teal,C.paleTeal);
  b += line(220,330,310,330,{stroke:C.red,arrow:true}); b += pathEl('M 190 292 C 420 242 820 242 1015 298',{stroke:C.red,dash:'7 6',arrow:true}); b += t(590,247,'未记录共同原因路径',{size:16,anchor:'middle',fill:C.red});
  b += line(466,330,545,330,{stroke:C.ink,arrow:true}); b += line(701,330,775,330,{stroke:C.ink,arrow:true}); b += line(931,330,997,330,{stroke:C.ink,arrow:true});
  b += t(540,382,'mediator：估总效应时不随意控制',{size:16,anchor:'middle',fill:C.amber});
  b += rect(570,430,250,58,{fill:C.paper,stroke:C.red,width:2,dash:'6 5'}); b += t(695,455,'Success / selected only',{size:17,anchor:'middle',weight:700,fill:C.red}); b += t(695,478,'A → C ← run difficulty',{size:16,anchor:'middle',mono:true});
  b += line(445,362,615,426,{stroke:C.red,arrow:true}); b += line(1020,382,780,430,{stroke:C.red,dash:'6 5',arrow:true});
  b += t(64, 548, '设计阶段关闭偏差路径', {size: 23, weight: 700});
  const fixes=[['随机化','break U→A',C.blue],['阻断/配对','吸收已知 nuisance',C.teal],['全因子','估计 O×S×D',C.amber],['locked test','隔离 selection',C.red]];
  fixes.forEach(([a,d,c],i)=>{const x=80+i*275;b+=line(x,590,x+210,590,{stroke:c,width:5});b+=t(x,620,a,{size:18,weight:750,fill:c});b+=t(x,645,d,{size:16,fill:C.gray});});
  b += t(64, 683, 'DAG 是可辩驳的研究假设；遗漏共同原因时，调整后仍可能有偏。', {size: 17, fill: C.gray});
  figures.set('fig-training-confounding-dag-v1.svg', svg('训练配置的因果图与混杂边界', '数据、优化器、调度和系统组成处理包；因果图区分混杂、中介与选择碰撞点，并映射到随机化、阻断、全因子和锁定测试。', 710, b));
}

// TRN-69: four cells, interaction plot, alias relation.
{
  let b='';
  b += t(66,52,'全因子看见 OFAT 看不见的角', {size:24,weight:700});
  b += t(70,95,'A / B 四个组合', {size:21,weight:700});
  const x0=95,y0=145,s=145;
  [['70','70'],['70','82']].forEach((row,j)=>row.forEach((v,i)=>{const x=x0+i*s,y=y0+j*s; const hot=i===1&&j===1;b+=rect(x,y,118,118,{fill:hot?C.paleTeal:C.paper,stroke:hot?C.teal:C.grid,width:hot?3:2});b+=t(x+59,y+52,`A=${i}, B=${j}`,{size:16,anchor:'middle'});b+=t(x+59,y+84,v,{size:25,weight:750,anchor:'middle',fill:hot?C.teal:C.ink});}));
  b += pathEl('M 154 138 L 154 125 L 299 125 L 299 138', {stroke:C.red,dash:'6 5'}); b += t(226,118,'OFAT 两条边都为 0',{size:16,anchor:'middle',fill:C.red});
  b += t(468,95,'Interaction plot', {size:21,weight:700});
  b += line(470,385,765,385,{stroke:C.ink}); b+=line(470,385,470,125,{stroke:C.ink});
  b += t(615,420,'A: low → high',{size:16,anchor:'middle',fill:C.gray}); b += t(448,260,'Y',{size:17,anchor:'middle',fill:C.gray});
  b += poly('510,325 720,325',{stroke:C.blue,width:4}); b += poly('510,325 720,165',{stroke:C.teal,width:4});
  b += circ(510,325,7,{fill:C.blue,stroke:C.blue});b+=circ(720,325,7,{fill:C.blue,stroke:C.blue});b+=circ(510,325,7,{fill:C.teal,stroke:C.teal});b+=circ(720,165,7,{fill:C.teal,stroke:C.teal});
  b += t(730,330,'B=0',{size:16,fill:C.blue}); b += t(730,170,'B=1',{size:16,fill:C.teal});
  b += t(615,460,'斜率差 = interaction', {size:18,anchor:'middle',weight:700,fill:C.teal});
  b += t(860,95,'Fraction：节省 run，牺牲可分性', {size:21,weight:700});
  b += circ(985,230,90,{fill:C.paper,stroke:C.amber,width:3}); b += t(985,208,'I = A B C',{size:20,mono:true,anchor:'middle',weight:700,fill:C.amber}); b += t(985,244,'A  ≡  B C',{size:20,mono:true,anchor:'middle'}); b += t(985,278,'effect alias',{size:17,anchor:'middle',fill:C.red,weight:700});
  b += t(860,350,'筛选结论：', {size:18,weight:700}); b += t(860,378,'“A 或 BC 与响应相关”', {size:17,fill:C.amber}); b += t(860,406,'不是“A 已被单独证明”', {size:17,fill:C.red});
  b += line(66,500,1134,500,{stroke:C.grid,dash:'6 6'});
  const principles=[['随机化','打散时间漂移'],['阻断','吸收已知难度'],['重复','估计运行变异'],['确认','新 runs 解 alias']];
  principles.forEach(([a,d],i)=>{const x=80+i*275;b+=t(x,548,`${i+1}`,{size:20,weight:750,fill:[C.blue,C.teal,C.amber,C.red][i]});b+=t(x+34,548,a,{size:19,weight:750});b+=t(x+34,579,d,{size:16,fill:C.gray});});
  figures.set('fig-factorial-interaction-v1.svg', svg('全因子消融、交互与别名', '二乘二四格和交互线展示协同，右侧说明半分数设计中主效应与交互的别名关系。', 620, b));
}

// TRN-70: pair lines, CI ruler, sequential path.
{
  let b='';
  b += t(66,52,'配对先消去共同难度', {size:24,weight:700});
  b += line(190,100,190,370,{stroke:C.grid}); b+=line(390,100,390,370,{stroke:C.grid});
  b += t(190,90,'A',{size:20,anchor:'middle',weight:700,fill:C.blue});b+=t(390,90,'B',{size:20,anchor:'middle',weight:700,fill:C.teal});
  const pa=[150,188,220,255,305,335], pb=[130,174,205,236,284,320];
  pa.forEach((y,i)=>{b+=line(190,y,390,pb[i],{stroke:C.grid,width:2});b+=circ(190,y,6,{fill:C.blue,stroke:C.blue});b+=circ(390,pb[i],6,{fill:C.teal,stroke:C.teal});});
  b += t(290,405,'每条线是一对共享 seed / block', {size:16,anchor:'middle',fill:C.gray});
  b += line(495,88,495,430,{stroke:C.grid,dash:'6 6'});
  b += t(550,90,'差值区间', {size:21,weight:700});
  b += line(555,250,785,250,{stroke:C.ink,width:2});
  [0,1,2,3,4].forEach(i=>{const x=565+i*52;b+=line(x,242,x,258,{stroke:C.ink});b+=t(x,278,`${i-2}d`,{size:15,anchor:'middle',fill:C.gray});});
  b += line(630,195,735,195,{stroke:C.blue,width:5}); b += circ(690,195,8,{fill:C.blue,stroke:C.blue});
  b += line(669,180,669,210,{stroke:C.red,dash:'5 4'}); b += t(669,157,'practical margin',{size:16,anchor:'middle',fill:C.red});
  b += t(670,330,'paired mean difference', {size:17,anchor:'middle',weight:700});
  b += t(670,360,'+ interval + failure denominator', {size:16,anchor:'middle',fill:C.gray});
  b += line(820,88,820,430,{stroke:C.grid,dash:'6 6'});
  b += t(875,90,'序贯查看', {size:21,weight:700});
  b += line(865,370,1130,370,{stroke:C.ink});b+=line(865,370,865,120,{stroke:C.ink});
  b += t(1000,405,'number of pairs',{size:15,anchor:'middle',fill:C.gray});b+=t(843,240,'effect',{size:15,anchor:'middle',fill:C.gray});
  b += pathEl('M 870 175 Q 980 125 1125 160',{stroke:C.red,dash:'7 5'});b+=pathEl('M 870 315 Q 980 365 1125 330',{stroke:C.red,dash:'7 5'});
  b += poly('875,250 910,265 945,235 980,220 1015,205 1050,190 1085,170 1120,165',{stroke:C.blue,width:4});
  b += t(1000,126,'time-uniform boundary',{size:16,anchor:'middle',fill:C.red});
  b += t(1000,455,'fixed-n CI 不能因“每次都看”而自动变成 CS', {size:16,anchor:'middle',fill:C.red});
  b += line(66,500,1134,500,{stroke:C.grid});
  b += t(80,545,'设计', {size:19,weight:750,fill:C.blue}); b+=t(155,545,'experimental unit · pairing · margin', {size:17});
  b += t(515,545,'推断', {size:19,weight:750,fill:C.teal}); b+=t(590,545,'effect · interval · multiplicity', {size:17});
  b += t(80,587,'决策', {size:19,weight:750,fill:C.amber}); b+=t(155,587,'efficacy · harm · equivalence · max budget', {size:17});
  figures.set('fig-paired-seeds-confidence-sequence-v1.svg', svg('配对种子、差值区间与序贯边界', '共享随机难度的配对连线、差值置信区间和随样本时刻同时有效的序贯边界被分成三个视图。', 625, b));
}

// TRN-71: trajectory, selection operator, firewall and budget rails.
{
  let b='';
  b += t(66,52,'一条训练轨迹产生 K 个候选', {size:24,weight:700});
  b += line(78,330,560,330,{stroke:C.ink}); b+=line(78,330,78,92,{stroke:C.ink});
  b += t(318,365,'training step / token',{size:16,anchor:'middle',fill:C.gray}); b+=t(55,210,'risk',{size:16,anchor:'middle',fill:C.gray});
  const curve='M 90 130 C 170 180, 245 260, 330 285 C 400 307, 455 302, 545 250';
  b += pathEl(curve,{stroke:C.blue,width:4});
  const cps=[[130,158],[205,215],[280,267],[355,294],[430,304],[510,270]];
  cps.forEach(([x,y],i)=>{const sel=i===4;b+=circ(x,y,sel?10:6,{fill:sel?C.red:C.paper,stroke:sel?C.red:C.blue,width:2}); if(!sel)b+=t(x,y+25,`c${i+1}`,{size:15,anchor:'middle',fill:C.gray}); else b+=t(x+18,y+6,'selected c5',{size:15,fill:C.red,weight:700});});
  b += t(430,120,'validation selects min observed risk',{size:17,anchor:'middle',fill:C.red}); b+=line(430,133,430,286,{stroke:C.red,dash:'6 5',arrow:true});
  b += line(605,82,605,410,{stroke:C.grid,dash:'6 6'});
  b += t(650,112,'Freeze', {size:21,weight:750,fill:C.amber});
  b += line(650,145,650,350,{stroke:C.amber,width:5});
  b += t(680,170,'recipe', {size:17});b+=t(680,205,'checkpoint rule',{size:17});b+=t(680,240,'seeds / failures',{size:17});b+=t(680,275,'analysis / budget',{size:17});
  b += t(680,330,'test 不参与选择',{size:17,weight:700,fill:C.red});
  b += line(855,82,855,410,{stroke:C.grid,dash:'6 6'});
  b += t(900,112,'Locked test', {size:21,weight:750,fill:C.teal});
  b += rect(900,155,215,78,{fill:C.paleTeal,stroke:C.teal,width:2.5}); b+=t(1007,188,'评估完整 procedure',{size:18,anchor:'middle',weight:700,fill:C.teal});b+=t(1007,216,'不是 oracle best test',{size:16,anchor:'middle'});
  b += line(900,280,1115,280,{stroke:C.red,width:3});b+=t(1007,315,'信息只向右流一次',{size:17,anchor:'middle',fill:C.red});
  b += t(66,462,'“Compute-matched”必须点名分母', {size:23,weight:700});
  const budgets=[['tokens','数据曝光',0.78,C.blue],['FLOPs','算术预算',0.62,C.teal],['device-time','平台成本',0.88,C.amber],['tuning+fail','研发总账',0.48,C.red]];
  budgets.forEach(([a,d,v,c],i)=>{const y=500+i*38;b+=t(80,y+6,a,{size:16,mono:true,weight:700,fill:c});b+=line(230,y,970,y,{stroke:C.grid,width:8});b+=line(230,y,230+v*740,y,{stroke:c,width:8});b+=t(995,y+6,d,{size:16,fill:C.gray});});
  b += t(80,672,'throughput 更高不保证 time-to-quality 更短；失败 run 仍在分母中。', {size:17,fill:C.gray});
  figures.set('fig-checkpoint-selection-firewall-v1.svg', svg('Checkpoint 选择与验证防火墙', '训练轨迹产生多个候选，validation 选择后冻结完整过程，再由锁定测试集评估；底部区分四种计算预算分母。', 700, b));
}

// TRN-72: open ledger loop and evidence staircase.
{
  let b='';
  b += t(66,52,'Research ledger：每条结论都能反向追溯', {size:24,weight:700});
  const cycle=[
    [150,170,'Claim','estimand · DAG',C.blue,C.paleBlue],
    [410,120,'Protocol','design · budget',C.teal,C.paleTeal],
    [680,170,'Run','manifest · telemetry',C.ink,'#F8FAFC'],
    [680,350,'Incident','first bad · replay',C.red,C.paleRed],
    [410,405,'Evidence','support · null · conflict',C.amber,C.paleAmber],
    [150,350,'Decision','scope · next test',C.teal,C.paleTeal]
  ];
  cycle.forEach(([x,y,a,d,c,f])=>{b+=rect(x-90,y-38,180,76,{fill:f,stroke:c,width:2.5});b+=t(x,y-5,a,{size:19,anchor:'middle',weight:750,fill:c});b+=t(x,y+22,d,{size:15,anchor:'middle',fill:C.gray});});
  for(let i=0;i<cycle.length;i++){const a=cycle[i],d=cycle[(i+1)%cycle.length]; const sx=a[0]+(d[0]>a[0]?92:d[0]<a[0]?-92:0), sy=a[1]+(d[1]>a[1]?40:d[1]<a[1]?-40:0); const ex=d[0]+(a[0]>d[0]?92:a[0]<d[0]?-92:0), ey=d[1]+(a[1]>d[1]?40:a[1]<d[1]?-40:0); b+=line(sx,sy,ex,ey,{stroke:C.ink,width:2.2,arrow:true});}
  b += t(410,275,'artifact hash + event ID',{size:17,anchor:'middle',weight:700,fill:C.blue});
  b += line(820,82,820,475,{stroke:C.grid,dash:'6 6'});
  b += t(865,112,'因果证据阶梯', {size:21,weight:750});
  const ev=[['E0','合同/推导',C.gray],['E1','toy oracle',C.blue],['E2','观测时间线',C.amber],['E3','随机干预',C.teal],['E4','机制干预',C.teal],['E5','外部复验',C.red]];
  ev.forEach(([id,label,c],i)=>{const y=400-i*48, x=865+i*35; b+=rect(x,y,235-i*20,34,{fill:i===5?C.paleRed:C.paper,stroke:c,width:2});b+=t(x+15,y+23,id,{size:16,mono:true,weight:750,fill:c});b+=t(x+60,y+23,label,{size:16});});
  b += t(860,472,'E2 不能写成 E3', {size:17,weight:700,fill:C.red});
  b += line(66,510,1134,510,{stroke:C.grid});
  b += t(70,552,'完整不等于正确', {size:20,weight:750,fill:C.red});
  b += t(270,552,'账本让错误可发现、可复算、可修正', {size:18});
  const end=[['失败也入账','failure denominator'],['偏离有版本','protocol deviation'],['结论有边界','scope + unresolved'],['交接可独立','artifact + owner']];
  end.forEach(([a,d],i)=>{const x=75+i*280;b+=t(x,606,a,{size:17,weight:700,fill:[C.red,C.amber,C.blue,C.teal][i]});b+=t(x,636,d,{size:15,mono:true,fill:C.gray});});
  b += t(70,680,'卷终门：至少包含一次真实失败、first-bad-event 复现包与修复反事实。', {size:17,fill:C.gray});
  figures.set('fig-training-research-ledger-v1.svg', svg('训练研究账本闭环', 'Claim、protocol、run、incident、evidence 和 decision 形成可追溯闭环，右侧证据阶梯限制因果语言。', 710, b));
}

for (const [name, content] of figures) fs.writeFileSync(path.join(outDir, name), content, 'utf8');
if (figures.size !== 8) throw new Error(`expected 8 figures, wrote ${figures.size}`);
console.log([...figures.keys()].join('\n'));

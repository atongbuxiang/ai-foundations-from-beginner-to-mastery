import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outputDir = resolve(here, '../../_assets/plots/learning-theory');
mkdirSync(outputDir, { recursive: true });

const palette = {
  ink: '#182235', muted: '#64748b', grid: '#d7dee8', blue: '#2457d6',
  green: '#147d64', red: '#c83d32', gold: '#b7791f', paper: '#ffffff',
};

const esc = (value) => String(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
const pathFrom = (points) => points.map(([x, y], i) => `${i ? 'L' : 'M'}${x.toFixed(1)},${y.toFixed(1)}`).join(' ');

function frame({ title, subtitle, body, width = 1200, height = 720 }) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
  <rect width="${width}" height="${height}" fill="${palette.paper}"/>
  <style>.s{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif}.m{font-family:"SFMono-Regular",Menlo,monospace}.ink{fill:${palette.ink}}.muted{fill:${palette.muted}}</style>
  <text x="64" y="60" class="s ink" font-size="31" font-weight="750">${esc(title)}</text>
  <text x="64" y="96" class="s muted" font-size="17">${esc(subtitle)}</text>
  ${body}
</svg>`;
}

function cartesian({ x0 = 100, y0 = 150, w = 980, h = 470, xTicks, yTicks, xScale, yScale, xLabel, yLabel }) {
  const lines = [];
  for (const t of yTicks) {
    const y = yScale(t);
    lines.push(`<line x1="${x0}" y1="${y}" x2="${x0 + w}" y2="${y}" stroke="${palette.grid}"/>`);
    lines.push(`<text x="${x0 - 14}" y="${y + 5}" text-anchor="end" class="s muted" font-size="14">${esc(t)}</text>`);
  }
  for (const t of xTicks) {
    const x = xScale(t.value ?? t);
    lines.push(`<line x1="${x}" y1="${y0}" x2="${x}" y2="${y0 + h}" stroke="${palette.grid}" stroke-dasharray="4 6"/>`);
    lines.push(`<text x="${x}" y="${y0 + h + 27}" text-anchor="middle" class="s muted" font-size="14">${esc(t.label ?? t)}</text>`);
  }
  lines.push(`<rect x="${x0}" y="${y0}" width="${w}" height="${h}" fill="none" stroke="#94a3b8" stroke-width="2"/>`);
  lines.push(`<text x="${x0 + w / 2}" y="${y0 + h + 67}" text-anchor="middle" class="s ink" font-size="16">${esc(xLabel)}</text>`);
  lines.push(`<text x="29" y="${y0 + h / 2}" text-anchor="middle" transform="rotate(-90 29 ${y0 + h / 2})" class="s ink" font-size="16">${esc(yLabel)}</text>`);
  return lines.join('\n');
}

function growthPlot() {
  const x0 = 100, y0 = 150, w = 980, h = 470;
  const xs = Array.from({ length: 13 }, (_, i) => i);
  const xScale = (x) => x0 + (x / 12) * w;
  const yScale = (y) => y0 + h - (y / 12) * h;
  const series = [
    { name: '全部二分标记 2^m', color: palette.red, values: xs.map(m => [xScale(m), yScale(m)]) },
    { name: '区间 1+m(m+1)/2', color: palette.green, values: xs.map(m => [xScale(m), yScale(Math.log2(1 + m * (m + 1) / 2))]) },
    { name: '右阈值 m+1', color: palette.blue, values: xs.map(m => [xScale(m), yScale(Math.log2(m + 1))]) },
  ];
  const axes = cartesian({ x0, y0, w, h, xTicks: xs.filter(m => m % 2 === 0), yTicks: [0, 2, 4, 6, 8, 10, 12], xScale, yScale, xLabel: '样本点数 m', yLabel: 'log₂ τ(m)：可区分标签模式的 bits' });
  const lines = series.map(s => `<path d="${pathFrom(s.values)}" fill="none" stroke="${s.color}" stroke-width="4"/>`).join('\n');
  const legend = series.map((s, i) => `<line x1="${660 + (i % 2) * 250}" y1="${128 + Math.floor(i / 2) * 25}" x2="${694 + (i % 2) * 250}" y2="${128 + Math.floor(i / 2) * 25}" stroke="${s.color}" stroke-width="4"/><text x="${704 + (i % 2) * 250}" y="${133 + Math.floor(i / 2) * 25}" class="s ink" font-size="14">${esc(s.name)}</text>`).join('');
  const marks = `<line x1="${xScale(1)}" y1="${y0}" x2="${xScale(1)}" y2="${y0 + h}" stroke="${palette.blue}" stroke-width="2" stroke-dasharray="7 6"/><text x="${xScale(1) + 9}" y="190" class="s" fill="${palette.blue}" font-size="14">threshold VC=1</text>
  <line x1="${xScale(2)}" y1="${y0}" x2="${xScale(2)}" y2="${y0 + h}" stroke="${palette.green}" stroke-width="2" stroke-dasharray="7 6"/><text x="${xScale(2) + 9}" y="217" class="s" fill="${palette.green}" font-size="14">interval VC=2</text>`;
  return frame({ title: '增长曲线：VC 维只记录最后一次碰到 2^m 的位置', subtitle: '纵轴取 log₂，指数包络成为直线；阈值与区间在跨过各自 VC 维后转为多项式增长。', body: `${legend}${axes}${lines}${marks}` });
}

function binomialSum(m, d) {
  let term = 1, total = 1;
  for (let i = 1; i <= d; i += 1) { term *= (m - i + 1) / i; total += term; }
  return total;
}

function sauerPlot() {
  const d = 2, x0 = 100, y0 = 150, w = 980, h = 470;
  const xs = Array.from({ length: 19 }, (_, i) => i + 2);
  const xScale = (x) => x0 + ((x - 2) / 18) * w;
  const yMax = 20, yScale = (y) => y0 + h - (y / yMax) * h;
  const values = [
    { name: 'trivial: 2^m', color: palette.red, vals: xs.map(m => [xScale(m), yScale(m)]) },
    { name: 'analytic: (em/d)^d', color: palette.gold, vals: xs.map(m => [xScale(m), yScale(Math.log2((Math.E * m / d) ** d))]) },
    { name: 'exact Sauer sum', color: palette.green, vals: xs.map(m => [xScale(m), yScale(Math.log2(binomialSum(m, d)))]) },
  ];
  const axes = cartesian({ x0, y0, w, h, xTicks: [2, 5, 8, 11, 14, 17, 20], yTicks: [0, 4, 8, 12, 16, 20], xScale, yScale, xLabel: '样本点数 m（固定 VC 维 d=2）', yLabel: 'log₂ 上界：有效模式的 bits' });
  const lines = values.map(s => `<path d="${pathFrom(s.vals)}" fill="none" stroke="${s.color}" stroke-width="4"/>`).join('');
  const legend = values.map((s, i) => `<line x1="${650 + i * 165}" y1="130" x2="${680 + i * 165}" y2="130" stroke="${s.color}" stroke-width="4"/><text x="${688 + i * 165}" y="135" class="s ink" font-size="13">${esc(s.name)}</text>`).join('');
  const m5 = xScale(5), exact5 = yScale(Math.log2(16)), coarse5 = yScale(Math.log2((5 * Math.E / 2) ** 2));
  const annotation = `<circle cx="${m5}" cy="${exact5}" r="6" fill="${palette.green}"/><text x="${m5 + 12}" y="${exact5 + 5}" class="s" fill="${palette.green}" font-size="14">m=5: exact=16</text><circle cx="${m5}" cy="${coarse5}" r="6" fill="${palette.gold}"/><text x="${m5 + 12}" y="${coarse5 - 10}" class="s" fill="${palette.gold}" font-size="14">coarse≈46.2 &gt; 2^5</text>`;
  return frame({ title: 'Sauer–Shelah 的三层上界：精确、解析与 trivial', subtitle: '解析式适合推导渐近阶，却不保证小样本下最紧；实际使用应取三者的最小值。', body: `${legend}${axes}${lines}${annotation}` });
}

function radiusPlot() {
  const delta = 0.05, x0 = 100, y0 = 150, w = 980, h = 470;
  const ratios = Array.from({ length: 121 }, (_, i) => 10 ** (i * 5 / 120));
  const xScale = (r) => x0 + (Math.log10(r) / 5) * w;
  const yMax = 5, yScale = (y) => y0 + h - (Math.min(y, yMax) / yMax) * h;
  const gamma = (m, d) => Math.sqrt((8 / m) * (d * Math.log(2 * Math.E * m / d) + Math.log(4 / delta)));
  const specs = [{ d: 10, color: palette.blue }, { d: 100, color: palette.green }, { d: 1000, color: palette.gold }];
  const series = specs.map(s => ({ ...s, values: ratios.map(r => [xScale(r), yScale(gamma(r * s.d, s.d))]) }));
  const axes = cartesian({ x0, y0, w, h, xTicks: [1, 10, 100, 1000, 10000, 100000].map(v => ({ value: v, label: `10^${Math.log10(v)}` })), yTicks: [0, 1, 2, 3, 4, 5], xScale, yScale, xLabel: '每个 VC 自由度对应的样本数 m/d（对数刻度）', yLabel: '经典显式 VC radius γ_m' });
  const lines = series.map(s => `<path d="${pathFrom(s.values)}" fill="none" stroke="${s.color}" stroke-width="4"/>`).join('');
  const legend = specs.map((s, i) => `<line x1="${720 + i * 120}" y1="130" x2="${750 + i * 120}" y2="130" stroke="${s.color}" stroke-width="4"/><text x="${758 + i * 120}" y="135" class="s ink" font-size="14">d=${s.d}</text>`).join('');
  const vacuousY = yScale(1);
  const note = `<line x1="${x0}" y1="${vacuousY}" x2="${x0 + w}" y2="${vacuousY}" stroke="${palette.red}" stroke-width="2" stroke-dasharray="8 7"/><text x="${x0 + 12}" y="${vacuousY - 10}" class="s" fill="${palette.red}" font-size="14">γ=1：高于此线虽正确，但对 0–1 risk 没有非平凡信息</text>`;
  return frame({ title: '经典 VC 半径的工作区：m 远大于 d 才开始非平凡', subtitle: '固定 δ=0.05。横轴用 m/d 揭示容量与样本规模的比例；这是一条保守的 worst-case 保证，不是实际测试误差预测。', body: `${legend}${axes}${lines}${note}` });
}

// v2 follows the textbook-figure convention used by the notes: the Markdown
// supplies the heading and interpretation; the SVG keeps only axes, evidence,
// direct labels, and accessible metadata.
const paletteV2 = {
  ink: '#1f2937', muted: '#64748b', grid: '#e2e8f0', blue: '#2563eb',
  green: '#047857', amber: '#b45309', red: '#b91c1c', paper: '#ffffff',
};

function frameV2({ title, desc, body, width = 1200, height = 650 }) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="title desc">
  <title id="title">${esc(title)}</title>
  <desc id="desc">${esc(desc)}</desc>
  <rect width="${width}" height="${height}" fill="${paletteV2.paper}"/>
  <style>.s{font-family:"Noto Sans SC","PingFang SC","Microsoft YaHei",sans-serif}.m{font-family:"STIX Two Math","Times New Roman",serif}.ink{fill:${paletteV2.ink}}.muted{fill:${paletteV2.muted}}</style>
  ${body}
</svg>`;
}

function cartesianV2({ x0 = 92, y0 = 42, w = 1038, h = 510, xTicks, yTicks, xScale, yScale, xLabel, yLabel }) {
  const lines = [];
  for (const t of yTicks) {
    const y = yScale(t);
    lines.push(`<line x1="${x0}" y1="${y}" x2="${x0 + w}" y2="${y}" stroke="${paletteV2.grid}" stroke-width="1.2"/>`);
    lines.push(`<text x="${x0 - 13}" y="${y + 5}" text-anchor="end" class="s muted" font-size="15">${esc(t)}</text>`);
  }
  for (const t of xTicks) {
    const x = xScale(t.value ?? t);
    lines.push(`<line x1="${x}" y1="${y0}" x2="${x}" y2="${y0 + h}" stroke="${paletteV2.grid}" stroke-width="1.2" stroke-dasharray="3 7"/>`);
    lines.push(`<text x="${x}" y="${y0 + h + 28}" text-anchor="middle" class="s muted" font-size="15">${esc(t.label ?? t)}</text>`);
  }
  lines.push(`<line x1="${x0}" y1="${y0 + h}" x2="${x0 + w}" y2="${y0 + h}" stroke="#475569" stroke-width="2"/>`);
  lines.push(`<line x1="${x0}" y1="${y0}" x2="${x0}" y2="${y0 + h}" stroke="#475569" stroke-width="2"/>`);
  lines.push(`<text x="${x0 + w / 2}" y="${y0 + h + 69}" text-anchor="middle" class="s ink" font-size="17">${esc(xLabel)}</text>`);
  lines.push(`<text x="27" y="${y0 + h / 2}" text-anchor="middle" transform="rotate(-90 27 ${y0 + h / 2})" class="s ink" font-size="17">${esc(yLabel)}</text>`);
  return lines.join('\n');
}

function growthPlotV2() {
  const x0 = 92, y0 = 42, w = 1038, h = 510;
  const xs = Array.from({ length: 13 }, (_, i) => i);
  const xScale = (x) => x0 + (x / 12) * w;
  const yScale = (y) => y0 + h - (y / 12) * h;
  const series = [
    { label: '全部二分：2ᵐ', color: paletteV2.red, values: xs.map(m => [xScale(m), yScale(m)]), dy: 20 },
    { label: '区间：1+m(m+1)/2', color: paletteV2.green, values: xs.map(m => [xScale(m), yScale(Math.log2(1 + m * (m + 1) / 2))]), dy: -10 },
    { label: '右阈值：m+1', color: paletteV2.blue, values: xs.map(m => [xScale(m), yScale(Math.log2(m + 1))]), dy: 21 },
  ];
  const axes = cartesianV2({ x0, y0, w, h, xTicks: xs.filter(m => m % 2 === 0), yTicks: [0, 2, 4, 6, 8, 10, 12], xScale, yScale, xLabel: '样本点数 m', yLabel: 'log₂ tau_H(m)' });
  const lines = series.map(s => `<path d="${pathFrom(s.values)}" fill="none" stroke="${s.color}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>`).join('\n');
  const labels = series.map(s => {
    const [x, y] = s.values.at(-1);
    return `<text x="${x - 12}" y="${y + s.dy}" text-anchor="end" class="s" fill="${s.color}" font-size="16" font-weight="600">${esc(s.label)}</text>`;
  }).join('\n');
  const marks = `<line x1="${xScale(1)}" y1="${y0}" x2="${xScale(1)}" y2="${y0 + h}" stroke="${paletteV2.blue}" stroke-width="1.8" stroke-dasharray="7 6"/>
  <text x="${xScale(1) + 8}" y="${y0 + 28}" class="s" fill="${paletteV2.blue}" font-size="15">阈值 VC 维 = 1</text>
  <line x1="${xScale(2)}" y1="${y0}" x2="${xScale(2)}" y2="${y0 + h}" stroke="${paletteV2.green}" stroke-width="1.8" stroke-dasharray="7 6"/>
  <text x="${xScale(2) + 8}" y="${y0 + 54}" class="s" fill="${paletteV2.green}" font-size="15">区间 VC 维 = 2</text>`;
  return frameV2({
    title: '阈值类与区间类的增长函数',
    desc: '对数坐标下，全部二分标记线性增长；右阈值和区间类在超过各自 VC 维后明显偏离指数包络。',
    body: `${axes}${marks}${lines}${labels}`,
  });
}

function sauerPlotV2() {
  const d = 2, x0 = 92, y0 = 42, w = 1038, h = 510;
  const xs = Array.from({ length: 19 }, (_, i) => i + 2);
  const xScale = (x) => x0 + ((x - 2) / 18) * w;
  const yScale = (y) => y0 + h - (y / 20) * h;
  const series = [
    { label: 'trivial：2ᵐ', color: paletteV2.red, vals: xs.map(m => [xScale(m), yScale(m)]), dy: 21 },
    { label: '解析松弛：(em/d)ᵈ', color: paletteV2.amber, vals: xs.map(m => [xScale(m), yScale(Math.log2((Math.E * m / d) ** d))]), dy: -12 },
    { label: 'Sauer 精确和', color: paletteV2.green, vals: xs.map(m => [xScale(m), yScale(Math.log2(binomialSum(m, d)))]), dy: 21 },
  ];
  const axes = cartesianV2({ x0, y0, w, h, xTicks: [2, 5, 8, 11, 14, 17, 20], yTicks: [0, 4, 8, 12, 16, 20], xScale, yScale, xLabel: '样本点数 m（固定 d = 2）', yLabel: 'log₂ 上界' });
  const lines = series.map(s => `<path d="${pathFrom(s.vals)}" fill="none" stroke="${s.color}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>`).join('\n');
  const labels = series.map(s => {
    const [x, y] = s.vals.at(-1);
    return `<text x="${x - 12}" y="${y + s.dy}" text-anchor="end" class="s" fill="${s.color}" font-size="16" font-weight="600">${esc(s.label)}</text>`;
  }).join('\n');
  const m5 = xScale(5), exact5 = yScale(Math.log2(16)), coarse5 = yScale(Math.log2((5 * Math.E / 2) ** 2));
  const annotation = `<circle cx="${m5}" cy="${exact5}" r="5.5" fill="${paletteV2.green}"/>
  <text x="${m5 + 13}" y="${exact5 + 20}" class="s" fill="${paletteV2.green}" font-size="15">m=5：精确和为 16</text>
  <circle cx="${m5}" cy="${coarse5}" r="5.5" fill="${paletteV2.amber}"/>
  <text x="${m5 + 13}" y="${coarse5 - 11}" class="s" fill="${paletteV2.amber}" font-size="15">解析式约 46.2，甚至大于 2⁵</text>`;
  return frameV2({
    title: 'Sauer–Shelah 精确上界、解析松弛与平凡上界',
    desc: '固定 VC 维为二，比较二项式精确和、常用解析松弛和全部二分模式上界，显示小样本时解析松弛可能比平凡上界更差。',
    body: `${axes}${lines}${labels}${annotation}`,
  });
}

function radiusPlotV2() {
  const delta = 0.05, x0 = 92, y0 = 42, w = 1038, h = 510;
  const ratios = Array.from({ length: 121 }, (_, i) => 10 ** (i * 5 / 120));
  const xScale = (r) => x0 + (Math.log10(r) / 5) * w;
  const yScale = (y) => y0 + h - (Math.min(y, 5) / 5) * h;
  const gamma = (m, d) => Math.sqrt((8 / m) * (d * Math.log(2 * Math.E * m / d) + Math.log(4 / delta)));
  const specs = [{ d: 10, color: paletteV2.blue }, { d: 100, color: paletteV2.green }, { d: 1000, color: paletteV2.amber }];
  const series = specs.map(s => ({ ...s, values: ratios.map(r => [xScale(r), yScale(gamma(r * s.d, s.d))]) }));
  const axes = cartesianV2({ x0, y0, w, h, xTicks: [1, 10, 100, 1000, 10000, 100000].map(v => ({ value: v, label: `10^${Math.log10(v)}` })), yTicks: [0, 1, 2, 3, 4, 5], xScale, yScale, xLabel: '每个 VC 自由度对应的样本数 m/d（对数刻度）', yLabel: '显式 VC 半径 gamma_m' });
  const lines = series.map(s => `<path d="${pathFrom(s.values)}" fill="none" stroke="${s.color}" stroke-width="3.5" stroke-linecap="round"/>`).join('\n');
  const legend = specs.map((s, i) => `<line x1="${780 + i * 115}" y1="67" x2="${810 + i * 115}" y2="67" stroke="${s.color}" stroke-width="3.5"/><text x="${818 + i * 115}" y="73" class="s ink" font-size="15">d=${s.d}</text>`).join('');
  const vacuousY = yScale(1);
  const note = `<line x1="${x0}" y1="${vacuousY}" x2="${x0 + w}" y2="${vacuousY}" stroke="${paletteV2.ink}" stroke-width="1.8" stroke-dasharray="8 7"/>
  <rect x="${x0 + 12}" y="${vacuousY - 31}" width="345" height="25" fill="#ffffff" opacity="0.92"/>
  <text x="${x0 + 18}" y="${vacuousY - 12}" class="s" fill="${paletteV2.ink}" font-size="15">gamma_m = 1：0–1 风险界开始提供非平凡信息</text>`;
  return frameV2({
    title: '不同 VC 维下经典显式半径的工作区',
    desc: '固定置信失败概率为零点零五，以样本复杂度比值 m 除以 d 为横轴，展示经典最坏情形 VC 半径何时降到一以下。',
    body: `${axes}${note}${lines}${legend}`,
  });
}

const outputs = [
  ['plot-growth-threshold-interval-v1.svg', growthPlot()],
  ['plot-sauer-bounds-v1.svg', sauerPlot()],
  ['plot-vc-radius-regimes-v1.svg', radiusPlot()],
  ['plot-growth-threshold-interval-v2.svg', growthPlotV2()],
  ['plot-sauer-bounds-v2.svg', sauerPlotV2()],
  ['plot-vc-radius-regimes-v2.svg', radiusPlotV2()],
];

for (const [name, svg] of outputs) writeFileSync(resolve(outputDir, name), svg, 'utf8');
console.log(outputs.map(([name]) => resolve(outputDir, name)).join('\n'));

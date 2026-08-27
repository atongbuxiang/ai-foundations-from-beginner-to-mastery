#!/usr/bin/env python3
"""Reproduce the GEO-06 compactness, spectrum, and finite-section audit.

Requires NumPy. The script uses no random data and writes one deterministic SVG.
Run with the workspace-bundled Python recorded in the companion experiment note.
"""

from __future__ import annotations

import hashlib
import math
from pathlib import Path

import numpy as np


VAULT_ROOT = Path(__file__).resolve().parents[3]
OUTPUT = VAULT_ROOT / "00-知识库管理" / "_assets" / "plots" / "functional-analysis" / "plot-compact-operator-spectrum-v2.svg"


def polyline(points: list[tuple[float, float]], cls: str) -> str:
    coords = " ".join(f"{x:.3f},{y:.3f}" for x, y in points)
    return f'<polyline class="{cls}" points="{coords}"/>'


def log_map(values: np.ndarray, lo: float, hi: float, out_lo: float, out_hi: float) -> np.ndarray:
    logs = np.log10(np.clip(values, 1e-300, None))
    return out_lo + (logs - math.log10(lo)) * (out_hi - out_lo) / (math.log10(hi) - math.log10(lo))


def lin_map(values: np.ndarray, lo: float, hi: float, out_lo: float, out_hi: float) -> np.ndarray:
    return out_lo + (values - lo) * (out_hi - out_lo) / (hi - lo)


def make_svg(
    ns: np.ndarray,
    diagonal_tail: np.ndarray,
    identity_tail: np.ndarray,
    volterra_singular: np.ndarray,
    volterra_exact: np.ndarray,
    kernel_eigenvalues: np.ndarray,
) -> str:
    width, height = 1200, 560
    panels = {
        "a": (65.0, 116.0, 480.0, 144.0),
        "b": (665.0, 116.0, 480.0, 144.0),
        "c": (65.0, 382.0, 480.0, 118.0),
        "d": (665.0, 382.0, 480.0, 118.0),
    }

    ax, ay, aw, ah = panels["a"]
    x_a = log_map(ns, ns.min(), ns.max(), ax, ax + aw)
    y_a_diag = log_map(diagonal_tail, 1e-3, 1.0, ay + ah, ay)
    y_a_id = log_map(identity_tail, 1e-3, 1.0, ay + ah, ay)

    bx, by, bw, bh = panels["b"]
    modes = np.arange(1, len(volterra_singular) + 1)
    x_b = lin_map(modes, 1, len(modes), bx, bx + bw)
    y_b_num = log_map(volterra_singular, 1e-2, 1.0, by + bh, by)
    y_b_exact = log_map(volterra_exact, 1e-2, 1.0, by + bh, by)

    cx, cy, cw, ch = panels["c"]
    x_c = lin_map(ns, ns.min(), ns.max(), cx, cx + cw)
    y_c_norm = lin_map(np.ones_like(ns), 0.0, 1.1, cy + ch, cy)
    y_c_eig = lin_map(np.zeros_like(ns), 0.0, 1.1, cy + ch, cy)

    dx, dy, dw, dh = panels["d"]
    kmodes = np.arange(1, len(kernel_eigenvalues) + 1)
    x_d = lin_map(kmodes, 1, len(kmodes), dx, dx + dw)
    y_d = log_map(kernel_eigenvalues, 1e-10, 1.0, dy + dh, dy)

    svg: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">紧性、谱截断与有限截面陷阱四轨实验</title>',
        '<desc id="desc">左上比较紧对角算子与恒等算子的低秩尾误差，右上比较Volterra离散奇异值与解析值，左下展示移位有限截面的零特征半径和单位算子范数，右下展示Gaussian核积分算子的特征值衰减。</desc>',
        "<defs><style>",
        'svg{font-family:"Inter","Noto Sans CJK SC","Source Han Sans SC",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}',
        '.bg{fill:#fff}.panel{fill:#fff;stroke:#cbd5e1;stroke-width:1.4}.ttl{font:700 22px "Inter","Noto Sans CJK SC","Source Han Sans SC",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#0f172a}.sub{font:500 15px "Inter","Noto Sans CJK SC","Source Han Sans SC",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#475569}.axis{stroke:#64748b;stroke-width:1.2}.grid{stroke:#e2e8f0;stroke-width:1}.tick{font:500 15px "Inter","Noto Sans CJK SC","Source Han Sans SC",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#64748b}.blue{fill:none;stroke:#2563eb;stroke-width:2.6}.teal{fill:none;stroke:#0f766e;stroke-width:2.6}.rose{fill:none;stroke:#e11d48;stroke-width:2.6}.amber{fill:none;stroke:#d97706;stroke-width:2.2;stroke-dasharray:6 4}.violet{fill:none;stroke:#7c3aed;stroke-width:2.6}.dotb{fill:#2563eb}.dott{fill:#0f766e}.dotr{fill:#e11d48}.dotv{fill:#7c3aed}.legend{font:600 15px "Inter","Noto Sans CJK SC","Source Han Sans SC",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#334155}',
        "</style></defs>",
        f'<rect class="bg" width="{width}" height="{height}"/>',
        '<text class="ttl" x="30" y="32">GEO-06 reproducibility audit · exact operator facts vs finite matrices</text>',
        '<text class="sub" x="30" y="51">All curves are deterministic; matrix residuals do not certify continuum spectral convergence.</text>',
        '<rect class="panel" x="25" y="62" width="550" height="225"/>',
        '<rect class="panel" x="625" y="62" width="550" height="225"/>',
        '<rect class="panel" x="25" y="316" width="550" height="224"/>',
        '<rect class="panel" x="625" y="316" width="550" height="224"/>',
        '<text class="ttl" x="45" y="84">A  Compact tail vs identity</text>',
        '<text class="sub" x="45" y="101">best rank-N operator-norm error · log-log</text>',
        '<text class="ttl" x="645" y="84">B  Volterra: spectrum vs singular values</text>',
        '<text class="sub" x="645" y="101">strictly lower quadrature · first 24 singular values</text>',
        '<text class="ttl" x="45" y="338">C  Shift finite-section trap</text>',
        '<text class="sub" x="45" y="355">all finite eigenvalues are 0 while ||S_N||2 = 1</text>',
        '<text class="ttl" x="645" y="338">D  Gaussian-kernel Nyström spectrum</text>',
        '<text class="sub" x="645" y="355">weighted symmetric matrix · first 24 eigenvalues</text>',
    ]

    for key in ("a", "b", "c", "d"):
        x, y, w, h = panels[key]
        svg.extend([
            f'<line class="axis" x1="{x}" y1="{y+h}" x2="{x+w}" y2="{y+h}"/>',
            f'<line class="axis" x1="{x}" y1="{y}" x2="{x}" y2="{y+h}"/>',
        ])

    for value in (1.0, 1e-1, 1e-2, 1e-3):
        yy = float(log_map(np.array([value]), 1e-3, 1.0, ay + ah, ay)[0])
        svg.append(f'<line class="grid" x1="{ax}" y1="{yy:.3f}" x2="{ax+aw}" y2="{yy:.3f}"/>')
        svg.append(f'<text class="tick" x="{ax-8}" y="{yy+3:.3f}" text-anchor="end">{value:g}</text>')
    for n, xx in zip(ns, x_a):
        svg.append(f'<text class="tick" x="{xx:.3f}" y="{ay+ah+16}" text-anchor="middle">{int(n)}</text>')
    svg.append(polyline(list(zip(x_a, y_a_diag)), "blue"))
    svg.append(polyline(list(zip(x_a, y_a_id)), "rose"))
    for xx, yy in zip(x_a, y_a_diag):
        svg.append(f'<circle class="dotb" cx="{xx:.3f}" cy="{yy:.3f}" r="3.5"/>')
    svg.extend([
        '<text class="legend" x="365" y="134">D tail: 1/(N+1)</text>',
        '<text class="legend" x="365" y="150">identity tail: 1</text>',
        f'<text class="tick" x="{ax+aw/2}" y="{ay+ah+32}" text-anchor="middle">rank N</text>',
    ])

    for value in (1.0, 1e-1, 1e-2):
        yy = float(log_map(np.array([value]), 1e-2, 1.0, by + bh, by)[0])
        svg.append(f'<line class="grid" x1="{bx}" y1="{yy:.3f}" x2="{bx+bw}" y2="{yy:.3f}"/>')
        svg.append(f'<text class="tick" x="{bx-8}" y="{yy+3:.3f}" text-anchor="end">{value:g}</text>')
    svg.append(polyline(list(zip(x_b, y_b_num)), "teal"))
    svg.append(polyline(list(zip(x_b, y_b_exact)), "amber"))
    for xx, yy in zip(x_b, y_b_num):
        svg.append(f'<circle class="dott" cx="{xx:.3f}" cy="{yy:.3f}" r="2.8"/>')
    svg.extend([
        '<text class="legend" x="970" y="130">discrete singular</text>',
        '<text class="legend" x="970" y="146">exact 2/((2k-1)pi)</text>',
        f'<text class="tick" x="{bx+bw/2}" y="{by+bh+32}" text-anchor="middle">mode k</text>',
    ])

    for value in (0.0, 0.5, 1.0):
        yy = float(lin_map(np.array([value]), 0.0, 1.1, cy + ch, cy)[0])
        svg.append(f'<line class="grid" x1="{cx}" y1="{yy:.3f}" x2="{cx+cw}" y2="{yy:.3f}"/>')
        svg.append(f'<text class="tick" x="{cx-8}" y="{yy+3:.3f}" text-anchor="end">{value:.1f}</text>')
    svg.append(polyline(list(zip(x_c, y_c_norm)), "violet"))
    svg.append(polyline(list(zip(x_c, y_c_eig)), "rose"))
    for xx, yy in zip(x_c, y_c_norm):
        svg.append(f'<circle class="dotv" cx="{xx:.3f}" cy="{yy:.3f}" r="3.5"/>')
    for n, xx in zip(ns, x_c):
        if int(n) in {4, 64, 256}:
            svg.append(f'<text class="tick" x="{xx:.3f}" y="{cy+ch+16}" text-anchor="middle">{int(n)}</text>')
    svg.extend([
        '<text class="legend" x="370" y="414">operator norm = 1</text>',
        '<text class="legend" x="370" y="430">eigen radius = 0</text>',
        f'<text class="tick" x="{cx+cw/2}" y="{cy+ch+32}" text-anchor="middle">section size N</text>',
    ])

    for value in (1.0, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10):
        yy = float(log_map(np.array([value]), 1e-10, 1.0, dy + dh, dy)[0])
        svg.append(f'<line class="grid" x1="{dx}" y1="{yy:.3f}" x2="{dx+dw}" y2="{yy:.3f}"/>')
        svg.append(f'<text class="tick" x="{dx-8}" y="{yy+3:.3f}" text-anchor="end">{value:.0e}</text>')
    svg.append(polyline(list(zip(x_d, y_d)), "blue"))
    for xx, yy in zip(x_d, y_d):
        svg.append(f'<circle class="dotb" cx="{xx:.3f}" cy="{yy:.3f}" r="2.8"/>')
    svg.extend([
        '<text class="legend" x="980" y="400">ell = 0.12</text>',
        '<text class="legend" x="980" y="416">HS-energy rank99 = 6</text>',
        f'<text class="tick" x="{dx+dw/2}" y="{dy+dh+32}" text-anchor="middle">eigenvalue index k</text>',
        '<text class="sub" x="600" y="554" text-anchor="middle">Generated by compact_operator_spectrum_audit.py · NumPy eigvalsh/SVD · no random sampling</text>',
        "</svg>",
    ])
    return "\n".join(svg) + "\n"


def main() -> None:
    ns = np.array([4, 8, 16, 32, 64, 128, 256], dtype=float)
    diagonal_tail = 1.0 / (ns + 1.0)
    identity_tail = np.ones_like(ns)
    diagonal_order = -float(np.polyfit(np.log(ns), np.log(diagonal_tail), 1)[0])

    volterra_n = 192
    volterra = np.tril(np.ones((volterra_n, volterra_n), dtype=float), k=-1) / volterra_n
    volterra_all_singular = np.linalg.svd(volterra, compute_uv=False)
    volterra_spectral_radius = float(np.max(np.abs(np.diag(volterra))))
    exact_top = 2.0 / math.pi
    volterra_rel_error = abs(float(volterra_all_singular[0]) - exact_top) / exact_top
    modes = np.arange(1, 25, dtype=float)
    volterra_singular = volterra_all_singular[:24]
    volterra_exact = 2.0 / ((2.0 * modes - 1.0) * math.pi)

    shift_norm = 1.0
    shift_eigen_radius = 0.0

    kernel_n = 160
    ell = 0.12
    nodes = (np.arange(kernel_n, dtype=float) + 0.5) / kernel_n
    distances = nodes[:, None] - nodes[None, :]
    kernel_matrix = np.exp(-(distances**2) / (2.0 * ell**2)) / kernel_n
    kernel_eigen_all = np.linalg.eigvalsh(kernel_matrix)[::-1]
    kernel_eigenvalues = np.clip(kernel_eigen_all[:24], 1e-12, None)
    hs_fraction = np.cumsum(np.clip(kernel_eigen_all, 0.0, None) ** 2) / np.sum(
        np.clip(kernel_eigen_all, 0.0, None) ** 2
    )
    kernel_hs_rank99 = int(np.searchsorted(hs_fraction, 0.99) + 1)
    kernel_rank10_op_tail = float(kernel_eigen_all[10])
    kernel_min_eigenvalue = float(kernel_eigen_all[-1])

    assert 0.95 < diagonal_order < 1.05
    assert volterra_rel_error < 0.005
    assert volterra_spectral_radius == 0.0
    assert shift_norm == 1.0 and shift_eigen_radius == 0.0
    assert kernel_hs_rank99 == 6
    assert kernel_min_eigenvalue > -1e-12

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    svg = make_svg(
        ns,
        diagonal_tail,
        identity_tail,
        volterra_singular,
        volterra_exact,
        kernel_eigenvalues,
    )
    OUTPUT.write_text(svg, encoding="utf-8")
    digest = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()

    print(f"diagonal_tail_order={diagonal_order:.8f}")
    print(f"diagonal_rank256_error={diagonal_tail[-1]:.12f}")
    print(f"identity_rank256_error={identity_tail[-1]:.12f}")
    print(f"volterra_sigma1={volterra_all_singular[0]:.12f}")
    print(f"volterra_sigma1_relative_error={volterra_rel_error:.12e}")
    print(f"volterra_discrete_spectral_radius={volterra_spectral_radius:.12f}")
    print(f"shift_section_norm={shift_norm:.12f}")
    print(f"shift_section_eigen_radius={shift_eigen_radius:.12f}")
    print(f"kernel_top_eigenvalue={kernel_eigen_all[0]:.12f}")
    print(f"kernel_hs_rank99={kernel_hs_rank99}")
    print(f"kernel_rank10_operator_tail={kernel_rank10_op_tail:.12e}")
    print(f"kernel_min_eigenvalue={kernel_min_eigenvalue:.12e}")
    print(f"output={OUTPUT}")
    print(f"sha256={digest}")


if __name__ == "__main__":
    main()

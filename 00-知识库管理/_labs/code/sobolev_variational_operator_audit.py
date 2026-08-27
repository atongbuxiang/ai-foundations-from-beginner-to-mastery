#!/usr/bin/env python3
"""Reproduce the GEO-08 weak-derivative, FEM, residual, and operator audit.

Requires NumPy only. The experiment is deterministic and writes a standalone SVG.
"""

from __future__ import annotations

import hashlib
import math
from pathlib import Path

import numpy as np


VAULT_ROOT = Path(__file__).resolve().parents[3]
OUTPUT = (
    VAULT_ROOT
    / "00-知识库管理"
    / "_assets"
    / "plots"
    / "functional-analysis"
    / "plot-sobolev-weak-fem-operator-v2.svg"
)


def track_weak_derivative() -> dict[str, np.ndarray | float]:
    """Delta concentration of d² sqrt(x²+eps²) and weak identity for |x|."""
    eps = np.array([0.40, 0.20, 0.10, 0.05, 0.025, 0.0125])
    x = np.linspace(-1.0, 1.0, 400_001)
    masses = []
    peaks = []
    for e in eps:
        second = e * e / np.power(x * x + e * e, 1.5)
        masses.append(float(np.trapezoid(second, x)))
        peaks.append(float(second[len(x) // 2]))

    ns = np.array([50, 100, 200, 400, 800, 1600, 3200])
    identity_errors = []
    for n in ns:
        grid = np.linspace(-1.0, 1.0, int(n) + 1)
        phi = np.power(np.maximum(1.0 - grid * grid, 0.0), 4)
        dphi = -8.0 * grid * np.power(np.maximum(1.0 - grid * grid, 0.0), 3)
        lhs = np.trapezoid(np.abs(grid) * dphi, grid)
        rhs = np.trapezoid(np.sign(grid) * phi, grid)
        identity_errors.append(abs(float(lhs + rhs)))

    curve_x = np.linspace(-0.45, 0.45, 1000)
    curve_eps = np.array([0.20, 0.08, 0.03])
    curves = np.array(
        [e * e / np.power(curve_x * curve_x + e * e, 1.5) for e in curve_eps]
    )
    return {
        "eps": eps,
        "masses": np.asarray(masses),
        "peaks": np.asarray(peaks),
        "identity_ns": ns,
        "identity_errors": np.asarray(identity_errors),
        "curve_x": curve_x,
        "curve_eps": curve_eps,
        "curves": curves,
        "mass_limit_error": abs(masses[-1] - 2.0),
        "peak_scaling_residual": float(np.max(np.abs(eps * np.asarray(peaks) - 1.0))),
        "identity_max_error": float(np.max(identity_errors)),
    }


def gauss_legendre_on_unit(order: int = 8) -> tuple[np.ndarray, np.ndarray]:
    points, weights = np.polynomial.legendre.leggauss(order)
    return (points + 1.0) / 2.0, weights / 2.0


def solve_linear_fem(elements: int) -> dict[str, np.ndarray | float]:
    """Conforming P1 FEM for -u''=pi² sin(pi x), homogeneous Dirichlet."""
    n = elements
    h = 1.0 / n
    nodes = np.linspace(0.0, 1.0, n + 1)
    interior = n - 1
    stiffness = (
        np.diag(np.full(interior, 2.0))
        + np.diag(np.full(interior - 1, -1.0), 1)
        + np.diag(np.full(interior - 1, -1.0), -1)
    ) / h
    load = np.zeros(interior)
    qx, qw = gauss_legendre_on_unit(8)
    for elem in range(n):
        left = nodes[elem]
        xq = left + h * qx
        fq = math.pi**2 * np.sin(math.pi * xq)
        shape_left = 1.0 - qx
        shape_right = qx
        if elem > 0:
            load[elem - 1] += h * float(np.sum(qw * fq * shape_left))
        if elem < n - 1:
            load[elem] += h * float(np.sum(qw * fq * shape_right))

    coeff = np.linalg.solve(stiffness, load)
    nodal = np.concatenate([[0.0], coeff, [0.0]])
    l2_sq = 0.0
    h1_sq = 0.0
    for elem in range(n):
        left = nodes[elem]
        xq = left + h * qx
        uh = nodal[elem] * (1.0 - qx) + nodal[elem + 1] * qx
        duh = (nodal[elem + 1] - nodal[elem]) / h
        exact = np.sin(math.pi * xq)
        dexact = math.pi * np.cos(math.pi * xq)
        l2_sq += h * float(np.sum(qw * (uh - exact) ** 2))
        h1_sq += h * float(np.sum(qw * (duh - dexact) ** 2))

    algebraic_residual = stiffness @ coeff - load
    weak_relative = float(
        np.linalg.norm(algebraic_residual) / max(np.linalg.norm(load), np.finfo(float).tiny)
    )
    strong_interior = math.pi**2 / math.sqrt(2.0)
    return {
        "nodes": nodes,
        "nodal": nodal,
        "l2_error": math.sqrt(l2_sq),
        "h1_error": math.sqrt(h1_sq),
        "weak_relative": weak_relative,
        "strong_interior": strong_interior,
        "solve_condition": float(np.linalg.cond(stiffness)),
    }


def track_fem() -> dict[str, np.ndarray | float]:
    elements = np.array([8, 16, 32, 64, 128])
    records = [solve_linear_fem(int(n)) for n in elements]
    h = 1.0 / elements
    l2 = np.array([r["l2_error"] for r in records])
    h1 = np.array([r["h1_error"] for r in records])
    weak = np.array([r["weak_relative"] for r in records])
    strong = np.array([r["strong_interior"] for r in records])
    return {
        "elements": elements,
        "h": h,
        "l2": l2,
        "h1": h1,
        "weak": weak,
        "strong": strong,
        "l2_slope": float(np.polyfit(np.log(h), np.log(l2), 1)[0]),
        "h1_slope": float(np.polyfit(np.log(h), np.log(h1), 1)[0]),
        "weak_max": float(np.max(weak)),
        "strong_exact": math.pi**2 / math.sqrt(2.0),
        "condition_128": float(records[-1]["solve_condition"]),
    }


def track_operator() -> dict[str, np.ndarray | float]:
    modes = np.arange(1, 65)
    gains = 1.0 / (math.pi * modes) ** 2
    cutoff = 8
    truncated = gains.copy()
    truncated[modes > cutoff] = 0.0
    rel_mode_error = np.where(modes <= cutoff, 0.0, 1.0)
    return {
        "modes": modes,
        "gains": gains,
        "truncated": truncated,
        "rel_mode_error": rel_mode_error,
        "cutoff": cutoff,
        "operator_tail": float(gains[cutoff]),
        "train_relative": float(np.max(rel_mode_error[:cutoff])),
        "ood_relative": float(np.min(rel_mode_error[cutoff:])),
        "mode64_absolute": float(gains[-1]),
    }


def _lin(values: np.ndarray, lo: float, hi: float, out_lo: float, out_hi: float) -> np.ndarray:
    return out_lo + (values - lo) * (out_hi - out_lo) / (hi - lo)


def _log(values: np.ndarray, lo: float, hi: float, out_lo: float, out_hi: float) -> np.ndarray:
    lv = np.log10(np.clip(values, 1e-300, None))
    return _lin(lv, math.log10(lo), math.log10(hi), out_lo, out_hi)


def _polyline(x: np.ndarray, y: np.ndarray, cls: str) -> str:
    points = " ".join(f"{a:.2f},{b:.2f}" for a, b in zip(x, y))
    return f'<polyline class="{cls}" points="{points}"/>'


def make_plot(
    weak: dict[str, np.ndarray | float],
    fem: dict[str, np.ndarray | float],
    operator: dict[str, np.ndarray | float],
) -> None:
    width, height = 1200, 720
    panels = {
        "a": (65.0, 132.0, 470.0, 175.0),
        "b": (665.0, 132.0, 470.0, 175.0),
        "c": (65.0, 455.0, 470.0, 175.0),
        "d": (665.0, 455.0, 470.0, 175.0),
    }
    svg: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">GEO-08 weak derivative, FEM residual, and solution-operator audit</title>',
        '<desc id="desc">Four panels show delta concentration, finite-element convergence, the separation of strong and Galerkin residuals, and failure of a low-mode truncated Poisson solution operator on high frequencies.</desc>',
        '<defs><style>',
        'svg{font-family:"Inter","Noto Sans CJK SC","Source Han Sans SC",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}',
        '.bg{fill:#fff}.panel{fill:#fff;stroke:#cbd5e1;stroke-width:1.4}.ttl{font:700 22px "Inter","Noto Sans CJK SC","Source Han Sans SC",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#0f172a}.sub{font:500 15px "Inter","Noto Sans CJK SC","Source Han Sans SC",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#475569}.axis{stroke:#64748b;stroke-width:1.2}.grid{stroke:#e2e8f0;stroke-width:1}.tick{font:500 15px "Inter","Noto Sans CJK SC","Source Han Sans SC",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#64748b}.blue{fill:none;stroke:#2563eb;stroke-width:2.4}.cyan{fill:none;stroke:#0891b2;stroke-width:2.2}.green{fill:none;stroke:#059669;stroke-width:2.5}.rose{fill:none;stroke:#e11d48;stroke-width:2.3}.amber{fill:none;stroke:#d97706;stroke-width:2.2}.violet{fill:none;stroke:#7c3aed;stroke-width:2.2}.dash{stroke-dasharray:6 4}.dotb{fill:#2563eb}.dotg{fill:#059669}.dotr{fill:#e11d48}.dotv{fill:#7c3aed}.legend{font:600 15px "Inter","Noto Sans CJK SC","Source Han Sans SC",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#334155}.note{font:600 15px "Inter","Noto Sans CJK SC","Source Han Sans SC",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#0f172a}.cut{stroke:#e11d48;stroke-width:1.4;stroke-dasharray:5 4}',
        '</style></defs>',
        f'<rect class="bg" width="{width}" height="{height}"/>',
        '<text class="ttl" x="30" y="31">GEO-08 reproducibility audit · weak objects, variational balance, and operator spectra</text>',
        '<text class="sub" x="30" y="52">Deterministic · NumPy only · continuum identities, discretization errors, and OOD claims are reported separately.</text>',
        '<rect class="panel" x="25" y="74" width="550" height="275"/>',
        '<rect class="panel" x="625" y="74" width="550" height="275"/>',
        '<rect class="panel" x="25" y="397" width="550" height="275"/>',
        '<rect class="panel" x="625" y="397" width="550" height="275"/>',
        '<text class="ttl" x="45" y="98">A  Delta concentration</text>',
        '<text class="sub" x="45" y="115">u_eps = sqrt(x^2+eps^2): u_eps\'\' concentrates while its mass approaches 2 delta_0</text>',
        '<text class="ttl" x="645" y="98">B  P1 FEM: L2/H1 orders</text>',
        '<text class="sub" x="645" y="115">−u″=π²sin(πx), u=0 · exact load quadrature · uniform meshes</text>',
        '<text class="ttl" x="45" y="421">C  Strong ≠ Galerkin residual</text>',
        '<text class="sub" x="45" y="438">piecewise-linear u_h has u_h\'\'=0 inside elements but exact discrete weak balance</text>',
        '<text class="ttl" x="645" y="421">D  Low-mode fit fails OOD</text>',
        '<text class="sub" x="645" y="438">Dirichlet Poisson gain sigma_k=(pi k)^-2 · learned truncation keeps k≤8</text>',
    ]
    for x, y, w, h in panels.values():
        svg.extend([
            f'<line class="axis" x1="{x}" y1="{y+h}" x2="{x+w}" y2="{y+h}"/>',
            f'<line class="axis" x1="{x}" y1="{y}" x2="{x}" y2="{y+h}"/>',
        ])

    # A: mollified absolute-value second derivatives.
    ax, ay, aw, ah = panels["a"]
    cx = _lin(weak["curve_x"], -0.45, 0.45, ax, ax + aw)
    colors = ["blue", "amber", "rose"]
    ymax = float(np.max(weak["curves"])) * 1.05
    for curve, cls in zip(weak["curves"], colors):
        cy = _lin(curve, 0.0, ymax, ay + ah, ay)
        svg.append(_polyline(cx, cy, cls))
    for val in [0, 10, 20, 30]:
        yy = float(_lin(np.array([val]), 0.0, ymax, ay + ah, ay)[0])
        svg.append(f'<line class="grid" x1="{ax}" y1="{yy:.2f}" x2="{ax+aw}" y2="{yy:.2f}"/><text class="tick" x="{ax-8}" y="{yy+4:.2f}" text-anchor="end">{val}</text>')
    for val in [-0.4, -0.2, 0.0, 0.2, 0.4]:
        xx = float(_lin(np.array([val]), -0.45, 0.45, ax, ax + aw)[0])
        svg.append(f'<text class="tick" x="{xx:.2f}" y="{ay+ah+17}" text-anchor="middle">{val:g}</text>')
    svg.extend([
        '<line class="blue" x1="82" y1="340" x2="103" y2="340"/><text class="legend" x="109" y="344">ε=.20</text>',
        '<line class="amber" x1="171" y1="340" x2="192" y2="340"/><text class="legend" x="198" y="344">ε=.08</text>',
        '<line class="rose" x1="260" y1="340" x2="281" y2="340"/><text class="legend" x="287" y="344">ε=.03</text>',
        f'<text class="note" x="382" y="344">mass(ε=.0125)={weak["masses"][-1]:.6f}</text>',
    ])

    # B: log-log FEM errors.
    bx, by, bw, bh = panels["b"]
    xvals = _log(fem["h"], float(np.min(fem["h"])), float(np.max(fem["h"])), bx + bw, bx)
    ymin = float(min(np.min(fem["l2"]), np.min(fem["h1"]))) / 1.4
    ymax_b = float(max(np.max(fem["l2"]), np.max(fem["h1"]))) * 1.4
    yl2 = _log(fem["l2"], ymin, ymax_b, by + bh, by)
    yh1 = _log(fem["h1"], ymin, ymax_b, by + bh, by)
    svg.append(_polyline(xvals, yl2, "blue"))
    svg.append(_polyline(xvals, yh1, "green"))
    for xx, yy in zip(xvals, yl2): svg.append(f'<circle class="dotb" cx="{xx:.2f}" cy="{yy:.2f}" r="3.5"/>')
    for xx, yy in zip(xvals, yh1): svg.append(f'<circle class="dotg" cx="{xx:.2f}" cy="{yy:.2f}" r="3.5"/>')
    for hval, xx in zip(fem["h"], xvals):
        svg.append(f'<text class="tick" x="{xx:.2f}" y="{by+bh+17}" text-anchor="middle">1/{round(1/hval):d}</text>')
    svg.extend([
        '<line class="blue" x1="684" y1="340" x2="705" y2="340"/><text class="legend" x="711" y="344">L² error</text>',
        '<line class="green" x1="785" y1="340" x2="806" y2="340"/><text class="legend" x="812" y="344">H¹ seminorm</text>',
        f'<text class="note" x="935" y="344">slopes {fem["l2_slope"]:.3f} / {fem["h1_slope"]:.3f}</text>',
    ])

    # C: normalized strong residual vs algebraic Galerkin residual.
    cx0, cy0, cw, ch = panels["c"]
    cxv = _lin(fem["elements"].astype(float), 8.0, 128.0, cx0, cx0 + cw)
    strong_norm = fem["strong"] / fem["strong_exact"]
    weak_floor = np.maximum(fem["weak"], 1e-17)
    ys = _log(strong_norm, 1e-17, 2.0, cy0 + ch, cy0)
    yw = _log(weak_floor, 1e-17, 2.0, cy0 + ch, cy0)
    for exponent in [0, -4, -8, -12, -16]:
        yy = float(_log(np.array([10.0**exponent]), 1e-17, 2.0, cy0 + ch, cy0)[0])
        svg.append(f'<line class="grid" x1="{cx0}" y1="{yy:.2f}" x2="{cx0+cw}" y2="{yy:.2f}"/><text class="tick" x="{cx0-8}" y="{yy+4:.2f}" text-anchor="end">10^{exponent}</text>')
    svg.append(_polyline(cxv, ys, "rose"))
    svg.append(_polyline(cxv, yw, "violet"))
    for xx, yy in zip(cxv, ys): svg.append(f'<circle class="dotr" cx="{xx:.2f}" cy="{yy:.2f}" r="3.5"/>')
    for xx, yy in zip(cxv, yw): svg.append(f'<circle class="dotv" cx="{xx:.2f}" cy="{yy:.2f}" r="3.5"/>')
    for val, xx in zip(fem["elements"], cxv):
        svg.append(f'<text class="tick" x="{xx:.2f}" y="{cy0+ch+17}" text-anchor="middle">{val}</text>')
    svg.extend([
        '<line class="rose" x1="82" y1="663" x2="103" y2="663"/><text class="legend" x="109" y="667">interior strong / ‖f‖ = 1</text>',
        '<line class="violet" x1="263" y1="663" x2="284" y2="663"/><text class="legend" x="290" y="667">‖Ku−F‖ / ‖F‖</text>',
    ])

    # D: exact vs truncated Poisson singular gains.
    dx, dy, dw, dh = panels["d"]
    mode_x = _log(operator["modes"].astype(float), 1.0, 64.0, dx, dx + dw)
    floor = 1e-6
    gy = _log(operator["gains"], floor, 0.2, dy + dh, dy)
    ty = _log(np.maximum(operator["truncated"], floor), floor, 0.2, dy + dh, dy)
    svg.append(_polyline(mode_x, gy, "green"))
    svg.append(_polyline(mode_x, ty, "blue dash"))
    cutoff_x = float(_log(np.array([operator["cutoff"] + 0.5]), 1.0, 64.0, dx, dx + dw)[0])
    svg.append(f'<line class="cut" x1="{cutoff_x:.2f}" y1="{dy}" x2="{cutoff_x:.2f}" y2="{dy+dh}"/>')
    for k in [1, 2, 4, 8, 16, 32, 64]:
        xx = float(_log(np.array([k]), 1.0, 64.0, dx, dx + dw)[0])
        svg.append(f'<text class="tick" x="{xx:.2f}" y="{dy+dh+17}" text-anchor="middle">{k}</text>')
    for exponent in [-1, -2, -3, -4, -5, -6]:
        yy = float(_log(np.array([10.0**exponent]), floor, 0.2, dy + dh, dy)[0])
        svg.append(f'<line class="grid" x1="{dx}" y1="{yy:.2f}" x2="{dx+dw}" y2="{yy:.2f}"/><text class="tick" x="{dx-8}" y="{yy+4:.2f}" text-anchor="end">10^{exponent}</text>')
    svg.extend([
        '<line class="green" x1="682" y1="663" x2="703" y2="663"/><text class="legend" x="709" y="667">exact gain</text>',
        '<line class="blue dash" x1="786" y1="663" x2="807" y2="663"/><text class="legend" x="813" y="667">truncated gain</text>',
        f'<text class="note" x="925" y="667">OOD relative={operator["ood_relative"]:.0%} · tail op={operator["operator_tail"]:.3e}</text>',
    ])

    svg.append('<text class="sub" x="30" y="705">Reading rule: panel A concerns distributions, B approximation error, C residual topology, D operator-distribution shift. No panel substitutes for the others.</text>')
    svg.append('</svg>')
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(svg), encoding="utf-8")


def main() -> None:
    weak = track_weak_derivative()
    fem = track_fem()
    operator = track_operator()
    make_plot(weak, fem, operator)
    digest = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    print(f"output={OUTPUT}")
    print(f"weak.mass_eps_min={weak['masses'][-1]:.12e}")
    print(f"weak.mass_limit_error={weak['mass_limit_error']:.12e}")
    print(f"weak.peak_scaling_residual={weak['peak_scaling_residual']:.12e}")
    print(f"weak.identity_max_error={weak['identity_max_error']:.12e}")
    print(f"fem.l2_slope={fem['l2_slope']:.12f}")
    print(f"fem.h1_slope={fem['h1_slope']:.12f}")
    print(f"fem.l2_n128={fem['l2'][-1]:.12e}")
    print(f"fem.h1_n128={fem['h1'][-1]:.12e}")
    print(f"fem.weak_max={fem['weak_max']:.12e}")
    print(f"fem.strong_interior={fem['strong_exact']:.12e}")
    print(f"fem.condition_n128={fem['condition_128']:.12e}")
    print(f"operator.cutoff={operator['cutoff']}")
    print(f"operator.tail_norm={operator['operator_tail']:.12e}")
    print(f"operator.train_relative={operator['train_relative']:.12e}")
    print(f"operator.ood_relative={operator['ood_relative']:.12e}")
    print(f"operator.mode64_absolute={operator['mode64_absolute']:.12e}")
    print(f"svg.sha256={digest}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Deterministic ELBO identity and gap research plot (v2)."""

from __future__ import annotations

import math
from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG,
    BLUE,
    GRID,
    INK,
    MUTED,
    RED,
    TEAL,
    begin,
    circle,
    finish,
    heading,
    line,
    path,
    text,
)


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "00-知识库管理/_assets/plots/information-theory/plot-elbo-gap-v2.svg"


def kl_ber(q: float, p: float) -> float:
    return q * math.log(q / p) + (1.0 - q) * math.log((1.0 - q) / (1.0 - p))


def evidence_and_posterior(x: int) -> tuple[float, float]:
    prior1 = 0.3
    likelihood_x_given_1 = 0.9 if x == 1 else 0.1
    likelihood_x_given_0 = 0.2 if x == 1 else 0.8
    joint1 = prior1 * likelihood_x_given_1
    joint0 = (1.0 - prior1) * likelihood_x_given_0
    evidence = joint1 + joint0
    return evidence, joint1 / evidence


def elbo(q: float, x: int) -> float:
    prior1 = 0.3
    likelihood1 = 0.9 if x == 1 else 0.1
    likelihood0 = 0.2 if x == 1 else 0.8
    return q * math.log(likelihood1) + (1.0 - q) * math.log(likelihood0) - kl_ber(q, prior1)


def sx(q: float, x0: float, width: float) -> float:
    return x0 + q * width


def sy(value: float, lo: float, hi: float, y0: float, height: float) -> float:
    return y0 + (hi - value) / (hi - lo) * height


def polyline(points, color, width=2.5, dash=None):
    d = "M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in points)
    return path(d, color, width, "none", dash)


def build() -> tuple[str, dict[str, float]]:
    ev1, post1 = evidence_and_posterior(1)
    _, post0 = evidence_and_posterior(0)
    logev1 = math.log(ev1)
    grid = [0.002 + i * 0.996 / 249 for i in range(250)]
    residual = max(abs(logev1 - elbo(q, 1) - kl_ber(q, post1)) for q in grid)
    assert residual < 2e-15

    restricted_q = 0.8
    restricted_gap = kl_ber(restricted_q, post1)
    shared_logit = 0.5 * (math.log(post1 / (1.0 - post1)) + math.log(post0 / (1.0 - post0)))
    shared_q = 1.0 / (1.0 + math.exp(-shared_logit))
    shared_gap = 0.5 * (kl_ber(shared_q, post1) + kl_ber(shared_q, post0))

    out = begin(
        "ELBO 恒等式、变分族限制与摊销缺口",
        "二元 latent model 的精确枚举：unrestricted Bernoulli q 在 posterior 处碰到 log evidence；q>=0.8 留下 approximation gap；共享 q 无法同时匹配 x=0/1 posterior，留下 amortization gap。",
        (BLUE, TEAL, RED),
    )

    lo, hi = -4.2, -0.7
    y0, h = 110.0, 280.0

    heading(out, 42, "A", "恒等式：ELBO + KL = evidence", BLUE)
    ax0, aw = 60.0, 310.0
    out += [line(ax0, y0 + h, ax0 + aw, y0 + h, GRID, 2), line(ax0, y0 + h, ax0, y0, GRID, 2)]
    curve = [(sx(q, ax0, aw), sy(elbo(q, 1), lo, hi, y0, h)) for q in grid]
    out.append(polyline(curve, BLUE, 3))
    evidence_y = sy(logev1, lo, hi, y0, h)
    out.append(line(ax0, evidence_y, ax0 + aw, evidence_y, TEAL, 2.5, "8 5"))
    out.append(circle(sx(post1, ax0, aw), evidence_y, 7, TEAL, TEAL))
    audit_q = 0.22
    audit_y = sy(elbo(audit_q, 1), lo, hi, y0, h)
    out.append(line(sx(audit_q, ax0, aw), evidence_y, sx(audit_q, ax0, aw), audit_y, RED, 3))
    out += [
        text(45, 95, f"x=1; posterior q*={post1:.4f}", 15, 650),
        text(60, 420, "q=P(z=1)", 15, 650),
        text(230, 130, f"log p(x)={logev1:.4f}", 15, 700, fill=TEAL),
        text(118, 225, "KL gap", 15, 700, fill=RED),
        text(45, 465, f"max identity residual < {residual:.1e}", 15, fill=MUTED),
        text(45, 498, "绿色点：q=posterior，gap=0。", 15, fill=TEAL),
    ]

    heading(out, 430, "B", "受限 family：approximation gap", TEAL)
    bx0, bw = 450.0, 320.0
    out += [line(bx0, y0 + h, bx0 + bw, y0 + h, GRID, 2), line(bx0, y0 + h, bx0, y0, GRID, 2)]
    out.append(line(bx0, evidence_y, bx0 + bw, evidence_y, TEAL, 2.5, "8 5"))
    restricted = [q for q in grid if q >= 0.8]
    bcurve = [(sx(q, bx0, bw), sy(elbo(q, 1), lo, hi, y0, h)) for q in restricted]
    out.append(polyline(bcurve, BLUE, 3))
    best_x = sx(restricted_q, bx0, bw)
    best_y = sy(elbo(restricted_q, 1), lo, hi, y0, h)
    out += [line(best_x, y0, best_x, y0 + h, RED, 2, "6 4"), circle(best_x, best_y, 7, RED, RED), line(best_x, evidence_y, best_x, best_y, RED, 3)]
    out += [
        text(430, 95, f"family q>=0.8; posterior={post1:.4f}", 15, 650),
        text(450, 420, "q=P(z=1)", 15, 650),
        text(690, 350, "best q=0.8", 15, 700, fill=RED),
        text(430, 465, f"irreducible approximation gap={restricted_gap:.4f} nats", 15, fill=RED),
        text(430, 498, "优化完成也无法跨出 variational family。", 15, fill=MUTED),
    ]

    heading(out, 830, "C", "共享 encoder：amortization gap", RED)
    x0, width, axis_y = 855.0, 275.0, 215.0
    out += [line(x0, axis_y, x0 + width, axis_y, GRID, 2)]
    for tick, label in ((0.0, "0"), (0.5, "q=P(z=1)"), (1.0, "1")):
        out.append(text(sx(tick, x0, width), axis_y + 35, label, 15, 650, "middle"))
    points = ((post0, BLUE, "q*(x=0)", 155), (post1, TEAL, "q*(x=1)", 155), (shared_q, RED, "shared q", 290))
    for q, color, label, label_y in points:
        px = sx(q, x0, width)
        out += [circle(px, axis_y, 8, color, color), text(px, label_y, label, 15, 700, "middle", color)]
    out += [line(sx(shared_q, x0, width), axis_y + 10, sx(post0, x0, width), axis_y + 65, RED, 2, "6 4"), line(sx(shared_q, x0, width), axis_y + 10, sx(post1, x0, width), axis_y + 65, RED, 2, "6 4")]
    out += [
        text(830, 345, f"posterior targets: {post0:.4f}, {post1:.4f}", 15, 650),
        text(830, 385, f"best shared q: {shared_q:.4f}", 15, 650),
        text(830, 425, f"average amortization gap: {shared_gap:.4f} nats", 15, 700, fill=RED),
        text(830, 470, "encoder 看不到 x；即使精确优化仍不能逐例匹配。", 15, fill=MUTED),
    ]

    svg = finish(out, "精确枚举把 identity、family restriction 与 amortized mapping 限制分开；optimizer 收敛不等于 posterior exact。")
    return svg, {
        "posterior_x0": post0,
        "posterior_x1": post1,
        "restricted_gap": restricted_gap,
        "shared_q": shared_q,
        "shared_gap": shared_gap,
        "identity_max_residual": residual,
    }


def main() -> None:
    svg, values = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"posterior_x0={values['posterior_x0']:.8f} posterior_x1={values['posterior_x1']:.8f}")
    print(f"restricted_gap={values['restricted_gap']:.8f} shared_q={values['shared_q']:.8f} shared_gap={values['shared_gap']:.8f}")
    print(f"identity_max_residual={values['identity_max_residual']:.3e}")


if __name__ == "__main__":
    main()

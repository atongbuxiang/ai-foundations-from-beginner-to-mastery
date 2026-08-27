#!/usr/bin/env python3
"""Pure-standard-library numerical audits for ARCH-25--32 Attention foundations."""

from __future__ import annotations

from math import exp, inf, isclose, isfinite, sqrt
from random import Random


Matrix = list[list[float]]


def transpose(a: Matrix) -> Matrix:
    return [list(col) for col in zip(*a)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def row_softmax(z: Matrix) -> Matrix:
    out: Matrix = []
    for row in z:
        finite = [x for x in row if isfinite(x)]
        if not finite:
            raise ValueError("all-masked row is undefined by this audit contract")
        m = max(finite)
        e = [0.0 if x == -inf else exp(x - m) for x in row]
        total = sum(e)
        out.append([x / total for x in e])
    return out


def attention(q: Matrix, k: Matrix, v: Matrix, mask: list[list[bool]] | None = None) -> tuple[Matrix, Matrix]:
    scale = sqrt(len(q[0]))
    scores = [[x / scale for x in row] for row in matmul(q, transpose(k))]
    if mask is not None:
        scores = [[x if keep else -inf for x, keep in zip(row, mrow)] for row, mrow in zip(scores, mask)]
    weights = row_softmax(scores)
    return weights, matmul(weights, v)


def close(a: float, b: float, tol: float = 1e-9) -> bool:
    return isclose(a, b, rel_tol=tol, abs_tol=tol)


def matrix_close(a: Matrix, b: Matrix, tol: float = 1e-9) -> bool:
    return len(a) == len(b) and all(
        len(x) == len(y) and all(close(u, v, tol) for u, v in zip(x, y)) for x, y in zip(a, b)
    )


def rank(a: Matrix, tol: float = 1e-12) -> int:
    m = [row[:] for row in a]
    rows, cols = len(m), len(m[0])
    r = 0
    for c in range(cols):
        if r >= rows:
            break
        pivot = max(range(r, rows), key=lambda i: abs(m[i][c]))
        if abs(m[pivot][c]) <= tol:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        p = m[r][c]
        m[r] = [x / p for x in m[r]]
        for i in range(rows):
            if i != r and abs(m[i][c]) > tol:
                f = m[i][c]
                m[i] = [x - f * y for x, y in zip(m[i], m[r])]
        r += 1
    return r


def random_matrix(rng: Random, rows: int, cols: int, positive: bool = False) -> Matrix:
    if positive:
        return [[exp(rng.gauss(0, 1)) for _ in range(cols)] for _ in range(rows)]
    return [[rng.gauss(0, 1) for _ in range(cols)] for _ in range(rows)]


def reorder_rows(a: Matrix, p: list[int]) -> Matrix:
    return [a[i][:] for i in p]


def reorder_cols(a: Matrix, p: list[int]) -> Matrix:
    return [[row[j] for j in p] for row in a]


def audit_qkv_roles_and_shapes() -> None:
    rng = Random(25)
    q = random_matrix(rng, 5, 8); k = random_matrix(rng, 12, 8); v = random_matrix(rng, 12, 16)
    a, o = attention(q, k, v)
    assert len(a) == 5 and len(a[0]) == 12 and len(o) == 5 and len(o[0]) == 16
    assert all(close(sum(row), 1) and min(row) >= 0 for row in a)
    for c in range(16):
        lo, hi = min(row[c] for row in v), max(row[c] for row in v)
        assert all(lo - 1e-12 <= row[c] <= hi + 1e-12 for row in o)
    v2 = [row[:] for row in v]
    v2[3] = [x + 2 for x in v2[3]]
    a2, o2 = attention(q, k, v2)
    assert matrix_close(a, a2)
    for i in range(5):
        assert all(close(o2[i][c] - o[i][c], 2 * a[i][3]) for c in range(16))


def audit_scaling_variance() -> None:
    rng = Random(26)
    n, d = 30_000, 64
    dots = [sum(rng.gauss(0, 1) * rng.gauss(0, 1) for _ in range(d)) for _ in range(n)]
    mean = sum(dots) / n
    var = sum((x - mean) ** 2 for x in dots) / n
    scaled_var = var / d
    assert abs(var - d) / d < 0.035 and abs(scaled_var - 1) < 0.035


def audit_stable_softmax_and_mask_edge() -> None:
    a = row_softmax([[1000.0, 1001.0, 999.0]])[0]
    expected = [0.24472847, 0.66524096, 0.09003057]
    assert all(close(x, y, 1e-7) for x, y in zip(a, expected))
    shifted = row_softmax([[x + 12345 for x in [1000.0, 1001.0, 999.0]]])[0]
    assert all(close(x, y) for x, y in zip(a, shifted))
    post = [x * m for x, m in zip(row_softmax([[0, 0, 0]])[0], [1, 1, 0])]
    pre = row_softmax([[0, 0, -inf]])[0]
    assert close(sum(post), 2 / 3) and all(close(x, y) for x, y in zip(pre, [.5, .5, 0]))
    try:
        attention([[1, 1]], [[1, 1], [1, 1]], [[1], [1]], [[False, False]])
    except ValueError:
        pass
    else:
        raise AssertionError("all-masked row must not pass silently")


def audit_causal_mask_and_equivariance() -> None:
    rng = Random(27); t, d = 7, 5
    q = random_matrix(rng, t, d); k = random_matrix(rng, t, d); v = random_matrix(rng, t, 3)
    causal = [[j <= i for j in range(t)] for i in range(t)]
    a, o = attention(q, k, v, causal)
    assert all(close(a[i][j], 0) for i in range(t) for j in range(i + 1, t)) and rank(a) == t
    v2 = [row[:] for row in v]
    for i in range(5, t):
        v2[i] = [x + 100 for x in v2[i]]
    _, o2 = attention(q, k, v2, causal)
    assert matrix_close(o[:5], o2[:5])
    p = list(range(t)); rng.shuffle(p)
    mask_float = [[float(x) for x in row] for row in causal]
    mask_p = reorder_cols(reorder_rows(mask_float, p), p)
    mask_p_bool = [[bool(x) for x in row] for row in mask_p]
    a_p, o_p = attention(reorder_rows(q, p), reorder_rows(k, p), reorder_rows(v, p), mask_p_bool)
    assert matrix_close(a_p, reorder_cols(reorder_rows(a, p), p)) and matrix_close(o_p, reorder_rows(o, p))


def audit_self_cross_shapes_and_memory_permutation() -> None:
    rng = Random(28)
    q = random_matrix(rng, 4, 6); k = random_matrix(rng, 9, 6); v = random_matrix(rng, 9, 7)
    a, o = attention(q, k, v)
    p = list(range(9)); rng.shuffle(p)
    a_p, o_p = attention(q, reorder_rows(k, p), reorder_rows(v, p))
    assert len(a) == 4 and len(a[0]) == 9 and len(o) == 4 and len(o[0]) == 7
    assert matrix_close(a_p, reorder_cols(a, p)) and matrix_close(o_p, o)
    pq = list(range(4)); rng.shuffle(pq)
    _, o_q = attention(reorder_rows(q, pq), k, v)
    assert matrix_close(o_q, reorder_rows(o, pq))


def audit_multihead_parameter_and_storage_ledgers() -> None:
    d = 512
    for h in (4, 8, 16, 32):
        dh = d // h
        assert 3 * d * (h * dh) + (h * dh) * d == 4 * d * d
    b, tq, tk = 2, 32, 128
    assert b * 16 * tq * tk == 2 * (b * 8 * tq * tk)


def audit_kernel_factorization_and_denominator() -> None:
    rng = Random(30)
    phi_q = random_matrix(rng, 5, 4, positive=True); phi_k = random_matrix(rng, 7, 4, positive=True)
    v = random_matrix(rng, 7, 3)
    affinity = matmul(phi_q, transpose(phi_k))
    exact_num = matmul(affinity, v)
    exact = [[x / sum(affinity[i]) for x in exact_num[i]] for i in range(5)]
    sv = matmul(transpose(phi_k), v)
    s1 = [[sum(row[j] for row in phi_k)] for j in range(4)]
    re_num = matmul(phi_q, sv); re_den = matmul(phi_q, s1)
    reassociated = [[x / re_den[i][0] for x in re_num[i]] for i in range(5)]
    assert matrix_close(exact, reassociated)
    n = d = 1e-6; nhat = 1e-6; dhat = 2e-6
    assert close(abs(nhat / dhat - n / d), .5)


def audit_rank_distinctions_and_effective_rank() -> None:
    l = [[0.0, 0.0], [0.0, 1.0]]; a = row_softmax(l)
    assert rank(l) == 1 and rank(a) == 2
    eps = 1e-7
    diagonal = [[1, 0, 0, 0], [0, eps, 0, 0], [0, 0, eps, 0], [0, 0, 0, eps]]
    stable = 1 + 3 * eps**2
    assert rank(diagonal, tol=0) == 4 and stable < 1.000000000001
    qf = [[float(i * 3 + j + 1) for j in range(3)] for i in range(5)]
    kf = [[float(i * 3 + j + 1) for j in range(3)] for i in range(7)]
    af = matmul(qf, transpose(kf))
    normalized = [[x / sum(row) for x in row] for row in af]
    assert rank(normalized) <= 3


AUDITS = (
    ("QKV roles, shapes, convex readout", audit_qkv_roles_and_shapes),
    ("scaled-dot-product variance", audit_scaling_variance),
    ("stable softmax, mask order, all-masked row", audit_stable_softmax_and_mask_edge),
    ("causal visibility, full rank, equivariance", audit_causal_mask_and_equivariance),
    ("self/cross shape and permutation contracts", audit_self_cross_shapes_and_memory_permutation),
    ("multi-head parameter and storage ledgers", audit_multihead_parameter_and_storage_ledgers),
    ("kernel reassociation and denominator sensitivity", audit_kernel_factorization_and_denominator),
    ("logit/weight/factorized/effective rank distinctions", audit_rank_distinctions_and_effective_rank),
)


def main() -> None:
    for name, fn in AUDITS:
        fn()
        print(f"PASS  {name}")
    print(f"PASS  {len(AUDITS)}/{len(AUDITS)} Attention audits")


if __name__ == "__main__":
    main()

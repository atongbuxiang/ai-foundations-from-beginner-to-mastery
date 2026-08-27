#!/usr/bin/env python3
"""Pure-standard-library deterministic audits for ARCH-33--40 Transformer architecture."""

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
            raise ValueError("all-masked row")
        m = max(finite)
        values = [0.0 if x == -inf else exp(x - m) for x in row]
        total = sum(values)
        out.append([x / total for x in values])
    return out


def attention(
    q: Matrix,
    k: Matrix,
    v: Matrix,
    mask: list[list[bool]] | None = None,
) -> tuple[Matrix, Matrix]:
    scale = sqrt(len(q[0]))
    scores = [[x / scale for x in row] for row in matmul(q, transpose(k))]
    if mask is not None:
        scores = [
            [x if keep else -inf for x, keep in zip(row, mrow)]
            for row, mrow in zip(scores, mask)
        ]
    weights = row_softmax(scores)
    return weights, matmul(weights, v)


def close(a: float, b: float, tol: float = 1e-9) -> bool:
    return isclose(a, b, rel_tol=tol, abs_tol=tol)


def matrix_close(a: Matrix, b: Matrix, tol: float = 1e-9) -> bool:
    return len(a) == len(b) and all(
        len(x) == len(y) and all(close(u, v, tol) for u, v in zip(x, y))
        for x, y in zip(a, b)
    )


def random_matrix(rng: Random, rows: int, cols: int) -> Matrix:
    return [[rng.gauss(0, 1) for _ in range(cols)] for _ in range(rows)]


def rank(a: Matrix, tol: float = 1e-12) -> int:
    m = [row[:] for row in a]
    rows, cols = len(m), len(m[0])
    r = 0
    for col in range(cols):
        if r == rows:
            break
        pivot = max(range(r, rows), key=lambda i: abs(m[i][col]))
        if abs(m[pivot][col]) <= tol:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        scale = m[r][col]
        m[r] = [x / scale for x in m[r]]
        for i in range(rows):
            if i != r and abs(m[i][col]) > tol:
                factor = m[i][col]
                m[i] = [x - factor * y for x, y in zip(m[i], m[r])]
        r += 1
    return r


def audit_block_wiring_and_depth_scale() -> None:
    a, c, x = 0.7, 0.3, 1.2
    pre = lambda z: z + a * (c * z)
    post = lambda z: c * (z + a * z)
    eps = 1e-6
    dpre = (pre(x + eps) - pre(x - eps)) / (2 * eps)
    dpost = (post(x + eps) - post(x - eps)) / (2 * eps)
    assert close(dpre, 1 + a * c, 1e-7)
    assert close(dpost, c * (1 + a), 1e-7)
    for layers in (4, 16, 64, 256):
        variance_sqrt = layers * (1 / sqrt(layers)) ** 2
        variance_linear = layers * (1 / layers) ** 2
        assert close(variance_sqrt, 1.0)
        assert close(variance_linear, 1 / layers)
    d, dff = 512, 2048
    assert 2 * d * dff == 2_097_152
    assert 3 * d * dff == 3_145_728


def audit_encoder_bidirectionality_and_padding() -> None:
    rng = Random(34)
    q = random_matrix(rng, 3, 4)
    k = random_matrix(rng, 3, 4)
    v = random_matrix(rng, 3, 2)
    _, base = attention(q, k, v)
    k_pad = k + random_matrix(rng, 2, 4)
    v_pad = v + [[100.0, -100.0], [-50.0, 50.0]]
    keep = [[True, True, True, False, False] for _ in range(3)]
    _, padded = attention(q, k_pad, v_pad, keep)
    assert matrix_close(base, padded)
    v_changed = [row[:] for row in v]
    v_changed[2] = [x + 7.0 for x in v_changed[2]]
    _, changed = attention(q, k, v_changed)
    assert any(not close(x, y) for x, y in zip(base[0], changed[0]))
    states = [[1.0, 0.0], [3.0, 2.0], [2.0, 4.0], [99.0, 99.0]]
    mean = [sum(states[i][j] for i in range(3)) / 3 for j in range(2)]
    assert mean == [2.0, 2.0]


def audit_decoder_causality_and_shift() -> None:
    rng = Random(35)
    t, d = 6, 5
    q = random_matrix(rng, t, d)
    k = random_matrix(rng, t, d)
    v = random_matrix(rng, t, 3)
    causal = [[j <= i for j in range(t)] for i in range(t)]
    weights, out = attention(q, k, v, causal)
    assert all(close(weights[i][j], 0.0) for i in range(t) for j in range(i + 1, t))
    v_pulse = [row[:] for row in v]
    v_pulse[4] = [x + 1000.0 for x in v_pulse[4]]
    _, out_pulse = attention(q, k, v_pulse, causal)
    assert matrix_close(out[:4], out_pulse[:4])
    tokens = ["A", "B", "C", "D"]
    inputs = ["BOS"] + tokens[:-1]
    assert list(zip(inputs, tokens)) == [("BOS", "A"), ("A", "B"), ("B", "C"), ("C", "D")]


def audit_full_vs_cached_decode() -> None:
    rng = Random(36)
    t, d = 8, 6
    q = random_matrix(rng, t, d)
    k = random_matrix(rng, t, d)
    v = random_matrix(rng, t, 4)
    causal = [[j <= i for j in range(t)] for i in range(t)]
    _, full = attention(q, k, v, causal)
    cached: Matrix = []
    for i in range(t):
        _, step = attention([q[i]], k[: i + 1], v[: i + 1])
        cached.append(step[0])
    assert matrix_close(full, cached)
    layers, batch, length, dkv = 24, 2, 1024, 1024
    scalars = 2 * layers * batch * length * dkv
    assert scalars == 100_663_296 and scalars * 2 == 201_326_592


def audit_encoder_decoder_cross_attention() -> None:
    rng = Random(37)
    tq, ts, dk, dv = 5, 7, 4, 3
    q = random_matrix(rng, tq, dk)
    source_k = random_matrix(rng, ts, dk)
    source_v = random_matrix(rng, ts, dv)
    weights, out = attention(q, source_k, source_v)
    assert len(weights) == tq and len(weights[0]) == ts
    assert len(out) == tq and len(out[0]) == dv
    permutation = [6, 2, 0, 5, 1, 4, 3]
    k_perm = [source_k[i] for i in permutation]
    v_perm = [source_v[i] for i in permutation]
    _, out_perm = attention(q, k_perm, v_perm)
    assert matrix_close(out, out_perm)
    pair_macs = 2 * 1 * 32 * 128 * 512
    assert pair_macs == 4_194_304


def audit_family_and_prefix_contracts() -> None:
    p, s = 2, 3
    n = p + s
    prefix = [
        [
            (i < p and j < p) or (i >= p and (j < p or j <= i))
            for j in range(n)
        ]
        for i in range(n)
    ]
    expected = [
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [1, 1, 1, 0, 0],
        [1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1],
    ]
    assert [[int(x) for x in row] for row in prefix] == expected
    causal = [[j <= i for j in range(n)] for i in range(n)]
    scores = [[0.1 * (i + 1) * (j + 1) for j in range(n)] for i in range(n)]
    masked = [[x if causal[i][j] else -inf for j, x in enumerate(row)] for i, row in enumerate(scores)]
    weights = row_softmax(masked)
    assert all(weights[i][i] > 0 for i in range(n))
    assert rank(weights) == n


def patchify(image: list[list[list[int]]], patch: int) -> list[list[int]]:
    height, width, channels = len(image), len(image[0]), len(image[0][0])
    if height % patch or width % patch:
        raise ValueError("image dimensions must be divisible by patch")
    patches: list[list[int]] = []
    for row in range(0, height, patch):
        for col in range(0, width, patch):
            token: list[int] = []
            for u in range(patch):
                for v in range(patch):
                    token.extend(image[row + u][col + v][:])
            assert len(token) == patch * patch * channels
            patches.append(token)
    return patches


def unpatchify(
    patches: list[list[int]],
    height: int,
    width: int,
    channels: int,
    patch: int,
) -> list[list[list[int]]]:
    image = [[[0 for _ in range(channels)] for _ in range(width)] for _ in range(height)]
    index = 0
    for row in range(0, height, patch):
        for col in range(0, width, patch):
            token = patches[index]
            index += 1
            offset = 0
            for u in range(patch):
                for v in range(patch):
                    image[row + u][col + v] = token[offset : offset + channels]
                    offset += channels
    return image


def audit_vit_patch_contract() -> None:
    height, width, channels, patch = 8, 12, 3, 4
    image = [
        [[1000 * r + 10 * c + k for k in range(channels)] for c in range(width)]
        for r in range(height)
    ]
    patches = patchify(image, patch)
    assert len(patches) == (height // patch) * (width // patch) == 6
    assert len(patches[0]) == patch * patch * channels == 48
    assert unpatchify(patches, height, width, channels, patch) == image
    try:
        patchify(image[:7], patch)
    except ValueError:
        pass
    else:
        raise AssertionError("non-divisible image must not pass silently")
    assert (224 // 16) ** 2 == 196
    assert (448 // 16) ** 2 == 4 * 196


def audit_parameter_and_compute_ledger() -> None:
    d, dff, b, t = 768, 3072, 2, 512
    mha = 4 * d * d
    ffn = 2 * d * dff
    assert mha == 2_359_296 and ffn == 4_718_592
    assert mha + ffn == 7_077_888
    projections = 4 * b * t * d * d
    pairs = 2 * b * t * t * d
    ffn_macs = 2 * b * t * d * dff
    assert projections == 2_415_919_104
    assert pairs == 805_306_368
    assert ffn_macs == 4_831_838_208
    assert 2 * t * t * d < 4 * t * d * d
    ts, tt = 128, 32
    cross_pairs = 2 * tt * ts * d
    assert cross_pairs == 6_291_456


AUDITS = (
    ("block wiring, FFN parameters, residual depth scale", audit_block_wiring_and_depth_scale),
    ("encoder bidirectionality, padding, masked pooling", audit_encoder_bidirectionality_and_padding),
    ("decoder shift and future invariance", audit_decoder_causality_and_shift),
    ("full causal forward versus cached rows", audit_full_vs_cached_decode),
    ("encoder-decoder cross shapes and memory reuse", audit_encoder_decoder_cross_attention),
    ("encoder/causal/prefix family mask contracts", audit_family_and_prefix_contracts),
    ("ViT patchify/unpatchify and token counts", audit_vit_patch_contract),
    ("parameter, MAC, and stage ledger identities", audit_parameter_and_compute_ledger),
)


def main() -> None:
    for name, fn in AUDITS:
        fn()
        print(f"PASS  {name}")
    print(f"PASS  {len(AUDITS)}/{len(AUDITS)} Transformer audits")


if __name__ == "__main__":
    main()

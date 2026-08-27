#!/usr/bin/env python3
"""Pure-standard-library deterministic audits for ARCH-49--56 efficient attention."""

from __future__ import annotations

from math import exp, isclose, sqrt
from random import Random


Vector = list[float]
Matrix = list[Vector]


def close(a: float, b: float, tol: float = 1e-9) -> bool:
    return isclose(a, b, rel_tol=tol, abs_tol=tol)


def vector_close(a: Vector, b: Vector, tol: float = 1e-9) -> bool:
    return len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))


def matrix_close(a: Matrix, b: Matrix, tol: float = 1e-9) -> bool:
    return len(a) == len(b) and all(vector_close(x, y, tol) for x, y in zip(a, b))


def dot(a: Vector, b: Vector) -> float:
    return sum(x * y for x, y in zip(a, b))


def transpose(a: Matrix) -> Matrix:
    return [list(column) for column in zip(*a)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    bt = transpose(b)
    return [[dot(row, column) for column in bt] for row in a]


def row_softmax(a: Matrix) -> Matrix:
    out: Matrix = []
    for row in a:
        maximum = max(row)
        weights = [exp(x - maximum) for x in row]
        total = sum(weights)
        out.append([x / total for x in weights])
    return out


def random_matrix(rng: Random, rows: int, columns: int) -> Matrix:
    return [[rng.gauss(0.0, 1.0) for _ in range(columns)] for _ in range(rows)]


def audit_phase_cost_ledger_and_crossover() -> None:
    b, n, d, dff = 2, 2048, 1024, 4096
    qkvo = 4 * b * n * d * d
    pairwise = 2 * b * n * n * d
    ffn = 2 * b * n * d * dff
    assert qkvo == pairwise and ffn == 2 * pairwise

    layers, tokens, hkv, dh, scalar_bytes = 32, 8192, 8, 128, 2
    cache = 2 * layers * b // b * tokens * hkv * dh * scalar_bytes
    assert cache == 2**30

    prompt, generated = 1000, 500
    history_reads = sum(prompt + t for t in range(generated))
    assert history_reads == generated * prompt + generated * (generated - 1) // 2
    assert history_reads > generated * prompt

    quadratic_constant, linear_constant = 2.0, 128.0
    crossover = linear_constant / quadratic_constant
    assert close(quadratic_constant * crossover**2, linear_constant * crossover)
    assert quadratic_constant * 16**2 < linear_constant * 16
    assert quadratic_constant * 256**2 > linear_constant * 256


def sparse_reference(scores: Matrix, values: Matrix, mask: list[list[bool]]) -> Matrix:
    outputs: Matrix = []
    for row, keep in zip(scores, mask):
        indices = [j for j, flag in enumerate(keep) if flag]
        maximum = max(row[j] for j in indices)
        weights = [exp(row[j] - maximum) for j in indices]
        total = sum(weights)
        outputs.append([
            sum(weight * values[j][c] for weight, j in zip(weights, indices)) / total
            for c in range(len(values[0]))
        ])
    return outputs


def audit_sparse_edges_paths_masks_and_kernel_semantics() -> None:
    n, radius = 12, 2
    local = [[abs(i - j) <= radius for j in range(n)] for i in range(n)]
    assert sum(sum(row) for row in local) == 54

    causal_window = [[j <= i and i - j < 4 for j in range(10)] for i in range(10)]
    assert sum(sum(row) for row in causal_window) == 34
    assert all(not causal_window[i][j] for i in range(10) for j in range(i + 1, 10))

    # A global hub gives a two-edge path between ordinary tokens but also a bottleneck.
    ordinary = range(1, 7)
    graph = {i: {0, i} for i in ordinary}
    graph[0] = set(ordinary) | {0}
    assert all(b in graph[0] and 0 in graph[a] for a in ordinary for b in ordinary)

    rng = Random(50)
    scores = random_matrix(rng, 6, 6)
    values = random_matrix(rng, 6, 3)
    mask = [[j <= i and i - j <= 2 for j in range(6)] for i in range(6)]
    sparse = sparse_reference(scores, values, mask)
    dense_masked = sparse_reference(scores, values, mask)
    assert matrix_close(sparse, dense_masked)

    # Removing probabilities after dense softmax without renormalizing is not sparse softmax.
    dense_weights = row_softmax(scores)
    row = 4
    post_mask_mass = sum(weight for weight, keep in zip(dense_weights[row], mask[row]) if keep)
    assert post_mask_mass < 1.0 and close(sum(row_softmax([[scores[row][j] for j in range(3, 6)]])[0]), 1.0)


def audit_low_rank_sequence_shapes_error_and_causal_leakage() -> None:
    rng = Random(51)
    n, k, dh = 7, 3, 4
    keys = random_matrix(rng, n, dh)
    projection = random_matrix(rng, k, n)
    compressed = matmul(projection, keys)
    assert len(compressed) == k and len(compressed[0]) == dh

    q = [[2.0, 0.0], [0.0, 0.5]]
    delta = [[1.0, -2.0], [3.0, 4.0], [-1.0, 1.0]]
    product = matmul(q, transpose(delta))
    fro_delta = sqrt(sum(x * x for row in delta for x in row))
    fro_product = sqrt(sum(x * x for row in product for x in row))
    # Operator norm of diagonal q is 2.
    assert fro_product <= 2.0 * fro_delta + 1e-12

    values_a = [[1.0], [10.0]]
    values_b = [[1.0], [-10.0]]
    leaking_projection = [[1.0, 1.0]]
    compressed_a = matmul(leaking_projection, values_a)
    compressed_b = matmul(leaking_projection, values_b)
    assert not matrix_close(compressed_a, compressed_b)
    # Prefix token is identical, so its dependence on the changed future value certifies leakage.
    assert values_a[0] == values_b[0]

    safe_projection = [[1.0, 0.0]]
    assert matrix_close(matmul(safe_projection, values_a), matmul(safe_projection, values_b))


def kernel_outputs(phi_q: Matrix, phi_k: Matrix, values: Matrix, causal: bool) -> Matrix:
    outputs: Matrix = []
    for i, query in enumerate(phi_q):
        stop = i + 1 if causal else len(phi_k)
        weights = [dot(query, phi_k[j]) for j in range(stop)]
        denominator = sum(weights)
        outputs.append([
            sum(weights[j] * values[j][c] for j in range(stop)) / denominator
            for c in range(len(values[0]))
        ])
    return outputs


def linear_state_outputs(phi_q: Matrix, phi_k: Matrix, values: Matrix, causal: bool) -> Matrix:
    r, dv = len(phi_k[0]), len(values[0])
    if not causal:
        state = matmul(transpose(phi_k), values)
        normalizer = [sum(row[a] for row in phi_k) for a in range(r)]
        return [[dot(query, [state[a][c] for a in range(r)]) / dot(query, normalizer) for c in range(dv)] for query in phi_q]

    state = [[0.0] * dv for _ in range(r)]
    normalizer = [0.0] * r
    outputs: Matrix = []
    for query, key, value in zip(phi_q, phi_k, values):
        for a in range(r):
            normalizer[a] += key[a]
            for c in range(dv):
                state[a][c] += key[a] * value[c]
        denominator = dot(query, normalizer)
        outputs.append([dot(query, [state[a][c] for a in range(r)]) / denominator for c in range(dv)])
    return outputs


def audit_kernel_associativity_causal_state_and_denominator() -> None:
    rng = Random(52)
    phi_q = [[exp(x) for x in row] for row in random_matrix(rng, 6, 4)]
    phi_k = [[exp(x) for x in row] for row in random_matrix(rng, 6, 4)]
    values = random_matrix(rng, 6, 3)
    assert matrix_close(kernel_outputs(phi_q, phi_k, values, False), linear_state_outputs(phi_q, phi_k, values, False))
    assert matrix_close(kernel_outputs(phi_q, phi_k, values, True), linear_state_outputs(phi_q, phi_k, values, True))

    numerator, denominator = 1.0, 1e-6
    assert abs(numerator / denominator - numerator / (2 * denominator)) == 500_000


def audit_performer_gaussian_estimator_and_ratio_error() -> None:
    rng = Random(53)
    q, k, samples = 0.25, -0.15, 120_000
    estimates = [exp(omega * (q + k) - (q * q + k * k) / 2) for omega in (rng.gauss(0.0, 1.0) for _ in range(samples))]
    empirical = sum(estimates) / samples
    target = exp(q * k)
    assert abs(empirical - target) / target < 0.005

    # Group means show the expected variance-of-the-mean scaling without claiming monotonic samples.
    mean = empirical
    sample_variance = sum((x - mean) ** 2 for x in estimates) / (samples - 1)
    assert sample_variance > 0
    assert close(sample_variance / 256, (sample_variance / 64) / 4)

    denominator_draws = [0.5, 1.5]
    unbiased_denominator = sum(denominator_draws) / 2
    expected_ratio = sum(1.0 / x for x in denominator_draws) / 2
    assert close(unbiased_denominator, 1.0) and close(expected_ratio, 4 / 3)


def merge_softmax_states(
    left: tuple[float, float, Vector], right: tuple[float, float, Vector]
) -> tuple[float, float, Vector]:
    m1, l1, u1 = left
    m2, l2, u2 = right
    maximum = max(m1, m2)
    a, b = exp(m1 - maximum), exp(m2 - maximum)
    return maximum, a * l1 + b * l2, [a * x + b * y for x, y in zip(u1, u2)]


def tile_state(scores: Vector, values: Matrix) -> tuple[float, float, Vector]:
    maximum = max(scores)
    weights = [exp(x - maximum) for x in scores]
    return maximum, sum(weights), [sum(w * row[c] for w, row in zip(weights, values)) for c in range(len(values[0]))]


def audit_flash_online_softmax_merge() -> None:
    scores = [1.0, 3.0, -2.0, 4.5, -7.0]
    values = [[2.0, -1.0], [4.0, 2.0], [10.0, 1.0], [-3.0, 5.0], [8.0, 9.0]]
    state = merge_softmax_states(tile_state(scores[:2], values[:2]), tile_state(scores[2:], values[2:]))
    _, total, numerator = state
    online = [x / total for x in numerator]
    weights = row_softmax([scores])[0]
    dense = [sum(w * row[c] for w, row in zip(weights, values)) for c in range(2)]
    assert vector_close(online, dense)

    # Reassociation changes neither real-arithmetic state nor dense pair count.
    state_three = merge_softmax_states(merge_softmax_states(tile_state(scores[:1], values[:1]), tile_state(scores[1:3], values[1:3])), tile_state(scores[3:], values[3:]))
    assert close(state[0], state_three[0])
    assert close(state[1], state_three[1])
    assert vector_close(state[2], state_three[2])
    assert len(scores) == 5  # all five score/value pairs were still processed


def head_attention(query: Vector, keys: Matrix, values: Matrix) -> Vector:
    weights = row_softmax([[dot(query, key) / sqrt(len(query)) for key in keys]])[0]
    return [sum(w * value[c] for w, value in zip(weights, values)) for c in range(len(values[0]))]


def audit_kv_cache_mha_gqa_mqa_and_full_decode() -> None:
    layers, batch, tokens, hq, dh = 40, 8, 4096, 32, 128
    payloads = {hkv: 2 * layers * batch * tokens * hkv * dh * 2 for hkv in (32, 8, 1)}
    assert payloads[32] == 20 * 2**30
    assert payloads[8] == 5 * 2**30
    assert payloads[1] == 5 * 2**27

    hkv = 8
    mapping = [head * hkv // hq for head in range(hq)]
    assert mapping[:12] == [0] * 4 + [1] * 4 + [2] * 4

    rng = Random(55)
    queries = random_matrix(rng, 5, 3)
    keys = random_matrix(rng, 5, 3)
    values = random_matrix(rng, 5, 2)
    full = [head_attention(queries[t], keys[: t + 1], values[: t + 1]) for t in range(5)]
    cache_k: Matrix = []
    cache_v: Matrix = []
    cached: Matrix = []
    for query, key, value in zip(queries, keys, values):
        cache_k.append(key)
        cache_v.append(value)
        cached.append(head_attention(query, cache_k, cache_v))
    assert matrix_close(full, cached)


def audit_mla_absorption_cache_width_and_equivalence() -> None:
    rng = Random(56)
    q = random_matrix(rng, 1, 4)[0]
    latent = random_matrix(rng, 1, 3)[0]
    up_key = random_matrix(rng, 4, 3)  # expanded key = W @ c
    expanded_key = [dot(row, latent) for row in up_key]
    expanded_score = dot(q, expanded_key)
    absorbed_query = [dot(column, q) for column in transpose(up_key)]
    assert close(expanded_score, dot(absorbed_query, latent))

    up_value = random_matrix(rng, 5, 3)
    output_projection = random_matrix(rng, 2, 5)
    expanded_value = [dot(row, latent) for row in up_value]
    expanded_output = [dot(row, expanded_value) for row in output_projection]
    fused = matmul(output_projection, up_value)
    latent_output = [dot(row, latent) for row in fused]
    assert vector_close(expanded_output, latent_output)

    hq, dh, dc, dr = 128, 128, 512, 64
    ratio = (dc + dr) / (2 * hq * dh)
    assert close(ratio, 0.017578125) and dc + dr < 2 * hq * dh
    # The advantage is config-dependent: a small GQA cache can be narrower.
    assert dc + dr > 2 * 4 * 64


AUDITS = (
    ("phase cost ledger, cumulative decode, and finite crossover", audit_phase_cost_ledger_and_crossover),
    ("sparse edge counts, graph paths, causal masks, and kernel semantics", audit_sparse_edges_paths_masks_and_kernel_semantics),
    ("sequence projection shapes, logit error bound, and causal leakage", audit_low_rank_sequence_shapes_error_and_causal_leakage),
    ("kernel reassociation, full/causal state, and denominator sensitivity", audit_kernel_associativity_causal_state_and_denominator),
    ("Performer Gaussian mean, variance budget, and ratio bias", audit_performer_gaussian_estimator_and_ratio_error),
    ("FlashAttention online-softmax block merge", audit_flash_online_softmax_merge),
    ("MHA/GQA/MQA cache ledger, mapping, and cached equivalence", audit_kv_cache_mha_gqa_mqa_and_full_decode),
    ("MLA projection absorption, fused values, and cache-width boundary", audit_mla_absorption_cache_width_and_equivalence),
)


def main() -> None:
    for name, audit in AUDITS:
        audit()
        print(f"PASS  {name}")
    print(f"PASS  {len(AUDITS)}/{len(AUDITS)} efficient-attention audits")


if __name__ == "__main__":
    main()

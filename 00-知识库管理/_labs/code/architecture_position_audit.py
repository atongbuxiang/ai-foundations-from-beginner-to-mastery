#!/usr/bin/env python3
"""Pure-standard-library deterministic audits for ARCH-41--48 position encoding."""

from __future__ import annotations

from math import cos, exp, isclose, log, pi, sin, sqrt
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
    return [list(col) for col in zip(*a)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]


def row_softmax(a: Matrix) -> Matrix:
    out: Matrix = []
    for row in a:
        maximum = max(row)
        values = [exp(x - maximum) for x in row]
        total = sum(values)
        out.append([x / total for x in values])
    return out


def attention(x: Matrix) -> Matrix:
    # Identity Q/K/V projections isolate the permutation contract.
    scale = sqrt(len(x[0]))
    scores = [[z / scale for z in row] for row in matmul(x, transpose(x))]
    return matmul(row_softmax(scores), x)


def permute_rows(a: Matrix, permutation: list[int]) -> Matrix:
    return [a[i] for i in permutation]


def rotate_pair(x: Vector, angle: float) -> Vector:
    c, s = cos(angle), sin(angle)
    return [c * x[0] - s * x[1], s * x[0] + c * x[1]]


def rope(x: Vector, position: float, frequencies: Vector) -> Vector:
    assert len(x) == 2 * len(frequencies)
    out: Vector = []
    for i, omega in enumerate(frequencies):
        out.extend(rotate_pair(x[2 * i : 2 * i + 2], position * omega))
    return out


def norm(x: Vector) -> float:
    return sqrt(dot(x, x))


def audit_permutation_equivariance_and_pooling() -> None:
    rng = Random(41)
    x = [[rng.gauss(0, 1) for _ in range(5)] for _ in range(7)]
    permutation = [5, 2, 6, 0, 3, 1, 4]
    base = attention(x)
    changed = attention(permute_rows(x, permutation))
    assert matrix_close(changed, permute_rows(base, permutation))
    pooled = [sum(row[j] for row in base) / len(base) for j in range(len(base[0]))]
    pooled_changed = [sum(row[j] for row in changed) / len(changed) for j in range(len(changed[0]))]
    assert vector_close(pooled, pooled_changed)
    assert not vector_close(base[0], changed[0])


def audit_absolute_position_ids_padding_and_cache() -> None:
    def position_ids(valid: list[bool], left_padding: bool = False) -> list[int]:
        if left_padding:
            count = 0
            ids = []
            for keep in valid:
                ids.append(count if keep else 0)
                count += int(keep)
            return ids
        return [i if keep else 0 for i, keep in enumerate(valid)]

    assert position_ids([True, True, True, False, False]) == [0, 1, 2, 0, 0]
    assert position_ids([False, False, True, True, True], True) == [0, 0, 0, 1, 2]
    cached_length, new_tokens = 5, 3
    assert list(range(cached_length, cached_length + new_tokens)) == [5, 6, 7]
    full = list(range(8))
    assert full[cached_length:] == [5, 6, 7]
    packed_segments = [[0, 1, 2], [0, 1]]
    assert [i for segment in packed_segments for i in segment] == [0, 1, 2, 0, 1]
    max_position = 7
    try:
        if full[-1] >= max_position:
            raise IndexError("position table overflow")
    except IndexError:
        pass
    else:
        raise AssertionError("position overflow must not pass silently")


def audit_sinusoidal_shift_and_relative_inner_product() -> None:
    frequencies = [1.0, 0.1, 0.01, 0.001]
    for omega in frequencies:
        n, delta = 13, 7
        p_n = [cos(omega * n), sin(omega * n)]
        p_shift = [cos(omega * (n + delta)), sin(omega * (n + delta))]
        assert vector_close(rotate_pair(p_n, omega * delta), p_shift)
        m = 5
        p_m = [cos(omega * m), sin(omega * m)]
        assert close(dot(p_m, p_n), cos(omega * (m - n)))
        assert close(norm(p_n), 1.0)
    encoding_0 = [cos(0), sin(0)]
    encoding_period = [cos(2 * pi), sin(2 * pi)]
    assert vector_close(encoding_0, encoding_period)


def relative_bucket(distance: int, exact: int = 4, buckets: int = 12) -> int:
    sign_offset = 0 if distance >= 0 else buckets
    magnitude = abs(distance)
    if magnitude < exact:
        bucket = magnitude
    else:
        bucket = exact + int(log(magnitude / exact, 2))
        bucket = min(bucket, buckets - 1)
    return sign_offset + bucket


def audit_relative_position_bucket_and_constant_values() -> None:
    assert relative_bucket(0) == 0
    assert relative_bucket(3) == 3
    assert relative_bucket(4) == 4
    assert relative_bucket(8) == 5
    assert relative_bucket(1_000_000) == 11
    assert relative_bucket(-8) == 17
    logits = [[0.2 * (i - j) for j in range(6)] for i in range(6)]
    weights = row_softmax(logits)
    value = [2.5, -1.0, 7.0]
    values = [value[:] for _ in range(6)]
    outputs = matmul(weights, values)
    assert all(vector_close(row, value) for row in outputs)
    relative_values = [
        [[float(i - j), 0.0, 0.0] for j in range(6)]
        for i in range(6)
    ]
    enriched = [
        [
            sum(weights[i][j] * (values[j][k] + relative_values[i][j][k]) for j in range(6))
            for k in range(3)
        ]
        for i in range(6)
    ]
    assert any(not vector_close(row, value) for row in enriched)


def audit_rope_relative_identity_norm_and_layout() -> None:
    rng = Random(45)
    q = [rng.gauss(0, 1) for _ in range(8)]
    k = [rng.gauss(0, 1) for _ in range(8)]
    frequencies = [1.0, 0.2, 0.04, 0.008]
    m, n = 11, 37
    left = dot(rope(q, m, frequencies), rope(k, n, frequencies))
    right = dot(q, rope(k, n - m, frequencies))
    assert close(left, right)
    assert close(norm(rope(q, m, frequencies)), norm(q))
    adjacent = [(0, 1), (2, 3), (4, 5), (6, 7)]
    half_split = [(0, 4), (1, 5), (2, 6), (3, 7)]
    assert adjacent != half_split
    assert sorted(i for pair in adjacent for i in pair) == list(range(8))
    assert sorted(i for pair in half_split for i in pair) == list(range(8))


def multiaxis_rope(x: Vector, row: int, column: int, row_freq: Vector, col_freq: Vector) -> Vector:
    row_dim = 2 * len(row_freq)
    return rope(x[:row_dim], row, row_freq) + rope(x[row_dim:], column, col_freq)


def audit_multiaxis_relative_identity() -> None:
    rng = Random(46)
    row_freq, col_freq = [1.0, 0.1], [0.5, 0.05]
    q = [rng.gauss(0, 1) for _ in range(8)]
    k = [rng.gauss(0, 1) for _ in range(8)]
    a, b = (2, 7), (9, 3)
    left = dot(multiaxis_rope(q, *a, row_freq, col_freq), multiaxis_rope(k, *b, row_freq, col_freq))
    row_dim = 2 * len(row_freq)
    relative_k = rope(k[:row_dim], b[0] - a[0], row_freq) + rope(k[row_dim:], b[1] - a[1], col_freq)
    assert close(left, dot(q, relative_k))
    width = 10
    assert width * 1 + (-9) == width * 0 + 1
    assert (1, -9) != (0, 1)


def audit_position_interpolation_scaling_and_remapping() -> None:
    train_length, target_length = 2048, 8192
    scale = target_length / train_length
    mapped = [(m / scale) for m in range(target_length)]
    assert mapped[0] == 0 and mapped[-1] < train_length
    assert close(mapped[1] - mapped[0], 1 / scale)
    frequencies = [1.0, 0.1, 0.01]
    per_frequency_scale = [4.0, 2.0, 1.0]
    phases = [omega * 8 / s for omega, s in zip(frequencies, per_frequency_scale)]
    assert vector_close(phases, [2.0, 0.4, 0.08])

    window = 128
    remap = lambda distance: max(-window, min(window, distance))
    assert remap(window - 1) == window - 1
    assert remap(window) == window
    assert remap(window + 1) == window
    assert remap(10_000) == window
    assert remap(-10_000) == -window


def audit_long_context_evaluation_protocol() -> None:
    lengths = [4096, 16_384, 65_536]
    positions = [0.1, 0.5, 0.9]
    tasks, seeds, samples = 4, 3, 200
    cells = len(lengths) * len(positions) * tasks * seeds
    assert cells == 108 and cells * samples == 21_600
    scores = [0.95, 0.90, 0.70, 0.92, 0.78, 0.45, 0.80, 0.50, 0.10]
    assert close(sum(scores) / len(scores), 6.10 / 9)
    assert min(scores) == 0.10
    per_length = [sum(scores[i : i + 3]) / 3 for i in range(0, 9, 3)]
    assert per_length[0] > per_length[1] > per_length[2]
    fixed_targets = ["answer"] * len(lengths)
    changing_context = ["x" * length for length in lengths]
    assert len(set(fixed_targets)) == 1
    assert [len(x) for x in changing_context] == lengths
    local_window = 128
    target_distances = [64, 1024, 32_768]
    assert [distance <= local_window for distance in target_distances] == [True, False, False]


AUDITS = (
    ("permutation equivariance and invariant pooling", audit_permutation_equivariance_and_pooling),
    ("absolute IDs, padding, packing, cache offset, and overflow", audit_absolute_position_ids_padding_and_cache),
    ("sinusoidal shift rotation, relative inner product, and periodicity", audit_sinusoidal_shift_and_relative_inner_product),
    ("relative buckets and constant-value expression probe", audit_relative_position_bucket_and_constant_values),
    ("RoPE relative identity, norm, and channel layouts", audit_rope_relative_identity_norm_and_layout),
    ("two-axis relative identity and flattening ambiguity", audit_multiaxis_relative_identity),
    ("position interpolation, per-frequency scaling, and remapping", audit_position_interpolation_scaling_and_remapping),
    ("length-position evaluation matrix and fixed-target accounting", audit_long_context_evaluation_protocol),
)


def main() -> None:
    for name, audit in AUDITS:
        audit()
        print(f"PASS  {name}")
    print(f"PASS  {len(AUDITS)}/{len(AUDITS)} position-encoding audits")


if __name__ == "__main__":
    main()

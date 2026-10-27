# Task 2 · Watch distance stop meaning anything

## A7 · Machine

MacBook Pro 16" (M4 Pro, 24 GB), runs done inside a Linux VM on it (aarch64, 4 cores, 3 GB RAM, Python 3.10.12), as recorded in `curse.json`.
Every run is fast: the largest one (d = 1000, 2,000 points, 20,000 pairs) took 1.48 s, the whole set of runs about 3 s.

## A1, A2 · Contrast against dimension (from `out/curse.json`)

20,000 random pairs of uniform points in the unit cube. Contrast = (max − min) / min, rel. sd = stdev / mean.

| d | points | mean | √(d/6) | min | max | contrast | rel. sd |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 1,000 | 0.521 | 0.577 | 0.003 | 1.326 | 488.6 | 0.476 |
| 5 | 1,000 | 0.884 | 0.913 | 0.111 | 1.687 | 14.26 | 0.282 |
| 10 | 1,000 | 1.274 | 1.291 | 0.438 | 2.159 | 3.93 | 0.193 |
| 20 | 1,000 | 1.815 | 1.826 | 0.821 | 2.670 | 2.25 | 0.135 |
| 50 | 1,000 | 2.867 | 2.887 | 1.909 | 3.785 | 0.98 | 0.083 |
| 100 | 1,000 | 4.068 | 4.082 | 3.206 | 4.954 | 0.55 | 0.060 |
| 200 | 1,000 | 5.776 | 5.774 | 4.871 | 6.682 | 0.37 | 0.041 |
| 500 | 2,000 | 9.126 | 9.129 | 8.099 | 10.176 | 0.26 | 0.026 |
| 1000 | 2,000 | 12.909 | 12.910 | 11.970 | 13.806 | 0.15 | 0.019 |

## A3 · What happens to contrast

It collapses. In 2-d the farthest pair is about 490 times farther than the nearest one; at d = 10 only 3.9 times, at d = 50 the gap is already smaller than the minimum itself (0.98), and at d = 1000 the nearest and farthest pairs differ by only 15%.
With 1,000 points, contrast drops **below 1 at about d = 50** and **below 0.5 between d = 100 and d = 200** (0.55 → 0.37), so roughly d ≈ 120.

## A4 · How the mean grows

Not linearly: like the square root of d. Each coordinate contributes E[(x − y)²] = 1/6, so the squared distance is about d/6 and the distance about √(d/6) ≈ 0.41·√d. The measured means match √(d/6) to 3 decimals from d = 20 up (4.068 vs 4.082 at d = 100, 12.909 vs 12.910 at d = 1000).
In low dimension the mean is a bit below the prediction (0.521 vs 0.577 at d = 2) because √(d/6) is the square root of the *mean squared* distance, and the mean of a square root is smaller than the square root of the mean; the gap vanishes as the distances concentrate.

## A5 · Relative standard deviation

It falls steadily too: 0.476 at d = 2, 0.135 at d = 20, 0.060 at d = 100, 0.019 at d = 1000 (roughly like 1/√d). I think **rel. sd is the better measure** of "distance stopped meaning anything": it describes the whole distribution of distances, it is stable (identical for 100, 1,000 or 10,000 points at d = 100), while contrast only uses the two most extreme pairs, so it is noisy and depends on how many points you have (see A6).

## A6 · Does contrast depend on n?

Yes. At d = 100: contrast 0.52 with 100 points, 0.55 with 1,000, 0.68 with 10,000 — while the mean (4.07–4.08) and rel. sd (0.060) do not move. At d = 2 it is even more unstable (99, 489, 301), because the minimum is a tiny number close to 0.
The reason: contrast depends on the closest and farthest pairs, and with more points you are more likely to find an unusually close pair. So "the dimension where distance stops meaning anything" is not a property of d alone: with a larger dataset the curse arrives a bit later for nearest-neighbour questions.

## A8 · Does this threaten week 3 (LSH on Jaccard)?

Not really, for the problem LSH was used for. The curse is about random, uniform, unstructured points, where every coordinate adds the same amount of noise and all distances concentrate around the mean. Shingle sets are not like that: near-duplicates share most of their shingles, so their Jaccard similarity stays high no matter how many possible shingles exist. In week 3 the true pairs had similarity 0.62–0.88 against about 0.01 for random pairs: a huge contrast, nothing like 0.15. LSH also only needs to separate "above the threshold" from "below", not to rank exact nearest neighbours.
It would become a problem if we tried to use LSH to find *moderately* similar documents among random ones in a huge, sparse space, where most pairs have similarity close to 0 and the differences are tiny.

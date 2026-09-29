# Task 2 · Crossover curve

Machine: MacBook Pro 16" (nov. 2024), Apple M4 Pro, 24 GB RAM, macOS Tahoe 26.6.2.
Nothing heavy running alongside during the measurements.

## Timings

| n    | brute time | brute comparisons | LSH time | LSH comparisons |
|------|-----------|--------------------|----------|-------------------|
| 125  | 0.03s     | 7,750              | 0.74s    | 1                 |
| 250  | 0.10s     | 31,125             | 1.48s    | 3                 |
| 500  | 0.39s     | 124,750            | 2.98s    | 15                |
| 1000 | 1.59s     | 499,500            | 5.94s    | 53                |
| 2000 | 6.44s     | 1,999,000          | 11.99s   | 196               |

At n=4000 and n=8000 the numbers are identical to n≈2120 (2,246,140 comparisons,
~7.3s / ~12.6s): `bench.build()` only generates 2,120 documents, so any
`--sizes` value above that re-measures the same fixed dataset instead of a
bigger one.

## A4 — is brute force really quadratic?

| n step      | time ratio |
|-------------|-----------|
| 125 -> 250  | x3.3      |
| 250 -> 500  | x3.9      |
| 500 -> 1000 | x4.08     |
| 1000 -> 2000| x4.05     |

Yes. From n=250 onward, doubling n roughly quadruples the time, matching the
comparison counts exactly quadrupling (7,750 -> 31,125 -> 124,750 -> 499,500
-> 1,999,000). The first step is noisy because 0.03s is too short to measure
precisely.

## A7/A8 — the crossover

No crossover was observed in this range: LSH is slower than brute force at
every size tested, from n=125 up to n=2000 (and the plateau at n>2120).

Why: each document only holds 60 shingles, so a single `similarity()` call is
very cheap. Brute force does up to ~2 million of these cheap calls. LSH must
first build a 120-number signature for every document (120 hash evaluations x
60 shingles, per document) before comparing anything - that upfront cost
outweighs the comparisons it then avoids, at this scale. LSH's own time grows
roughly linearly with n (doubles when n doubles: 0.74 -> 1.48 -> 2.98 -> 5.94
-> 11.99s), while brute force grows quadratically, so extrapolating past the
dataset's 2,120-document cap, the two curves would eventually cross somewhere
above n=2000 - but this generator cannot produce enough documents to measure
that point directly.

## A5 — peak memory at largest n (n=2000)

Brute force: 21,400 bytes (~21 KB) — it holds almost nothing, just compares
pairs one at a time and discards the result.

LSH: 10,246,228 bytes (~10.2 MB) — about 480x more. It has to hold the full
signature matrix (2,000 documents x 120 numbers) plus the per-band buckets
used to group documents, all at once, in exchange for skipping most
comparisons.

## What became unpleasant first

Time, not memory - brute force at n=2000 already takes several seconds, while
nothing in the measurements suggests memory pressure. The real limit here was
the dataset generator's fixed size (2,120 documents), not the machine.
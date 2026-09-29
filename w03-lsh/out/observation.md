# Task 1

One pass over the rows, because it lets the matrix be read as a stream (row by
row) without ever holding it fully in memory. A per-column scan would need
either the whole matrix in memory or one re-read of the whole file per column,
which does not scale.

R5: leftover rows are folded into the last band, so it ends up slightly longer
(and stricter) than the others, but no signature row is dropped.

The S1-S4 estimate was 1.0 vs the true 2/3 because two hash functions is a
tiny sample. Using more hash functions would shrink that error (roughly
proportional to 1/sqrt(n_hashes)), at the cost of a longer signature — more
time to build it and more memory to store it.

# Task 2

Machine: MacBook Pro 16" (M4 Pro, 24 GB RAM). No crossover found: LSH was
slower than brute force at every size up to n=2000, because each document
only has 60 shingles, making a single similarity() call very cheap - brute
force's 2M cheap calls beat LSH's fixed cost of building 2,000 signatures
upfront. The quadratic check (A4) held from n=250 onward (doubling n roughly
quadrupled brute-force time, matching exact 4x growth in comparison counts).

What became unpleasant first was time, not memory: brute force reached ~6.4s
at n=2000, and LSH used ~480x more memory (10.2 MB vs 21 KB) despite still
being slower. The real ceiling was the dataset generator itself, capped at
2,120 documents - sizes above that (tested at 4,000 and 8,000) returned
identical numbers, so the true crossover point could not be measured.

# Task 3

I use 120 hashes split into 40 bands (r = 3 rows per band). A pair with
similarity s becomes a candidate with probability 1 - (1 - s^3)^40, and the
step of that curve sits near (1/40)^(1/3) ≈ 0.29. The real near-duplicates
have s between about 0.62 and 0.88, well above the step, so they are found
with probability ≈ 1, while random pairs (s ≈ 0.01) are candidates ≈ 0.004%
of the time. A false candidate only costs one comparison but a missed pair
lowers recall, so I put the step well below the 0.6 threshold.

Result: 222 comparisons instead of 2,246,140 (99.99% avoided), recall 100%.

Bad setting for contrast: 100 hashes / 10 bands puts the step near 0.79,
above many true pairs, and recall drops to 48.8% (59 comparisons).

On "free hashing": my Task 2 timings show it is not free at this scale. At
n=2,000 the 2M brute-force comparisons took 6.44s (~3.2 us each), while
building 2,000 signatures took 11.99s (~6.0 ms each). Setting
n(n-1)/2 x 3.2us = n x 6.0ms gives n ≈ 3,700 - below that, hashing dominates
and treating it as free flatters LSH; above it, the quadratic comparison term
takes over and the simplification becomes fair. It is a reasonable model for
the millions-of-documents case the course is about, not for 2,120.
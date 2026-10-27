# Task 1

R3: an empty cluster keeps its previous centroid. It is the conservative choice and the same rule as the task 3 baseline; the alternative (moving it to the point farthest from its centroid) would rescue a lost cluster faster but makes the result depend on a single outlier.
Over 40 seeds on the nine-point blobs, random initialisation found the three blobs only 24 times out of 40 (SSE 0.12); the other 16 runs got stuck at SSE about 96 with two blobs merged. k-means++ found them 40 out of 40 (mean SSE 0.120 vs 38.5 for random).
k-means++ pays extra distance computations before the first iteration (each new centre needs the distance from every point to the nearest chosen centre: here 9 + 18 = 27, as much as a whole iteration). It buys a start with centres far apart, so fewer bad local optima and usually fewer iterations; I would not pay it when k is large and n is huge (k passes over the data just to start), or when I restart many times anyway.
SSE always decreases with k (256 for k = 1, 96 for 2, 0.12 for 3, 0.09 for 4, 0.05 for 6) and reaches 0 when every point is its own cluster, so minimising it always picks the largest k. You have to look for the elbow instead: here SSE falls hugely until k = 3, then almost not at all.

# Task 2

With 1,000 uniform points, contrast (max − min)/min drops below 1 at about d = 50 (0.98) and below 0.5 between d = 100 and 200 (0.55 → 0.37); the mean distance grows like √(d/6), matching the measurements to 3 decimals from d = 20.
A6: n matters for contrast (0.52 / 0.55 / 0.68 with 100 / 1,000 / 10,000 points at d = 100) but not for the mean or the relative standard deviation (0.060 each time), because contrast depends only on the extreme pairs and more points give a closer nearest pair. So relative stdev is the better measure, and the "bad" dimension depends on the data size.
A8: this does not threaten week 3's LSH, because shingle sets are not uniform random points: near-duplicates keep a high Jaccard similarity (0.62–0.88 against 0.01 for random pairs in week 3), and LSH only separates above/below a threshold. It would hurt if we looked for weakly similar documents in a huge sparse space.

# Task 3

I used Hamerly's bounds: per point I store an upper bound on the distance to its own centroid and a lower bound on the distance to the second-closest centroid, so 2 extra numbers per point (40,000 for 20,000 points), plus half the distance from each centroid to its nearest other centroid (k numbers).
R5: a point is skipped without any distance if its upper bound is below max(lower bound, half-distance to the nearest centroid). 724,191 of the 840,000 point checks after the first iteration (86%) were skipped this way; the lower bound alone was enough in 510,680 of them, the centroid-separation bound in 280,203, so the lower bound does most of the work. Maintaining it costs k = 12 distances per iteration (how far each centroid moved) plus k(k−1)/2 = 66 centroid-to-centroid distances, about 3,300 calls in total, and an O(n) loop to loosen the bounds.
Result: 1,218,585 distance computations instead of 10,320,000 (88.2% cut), 2.45 s instead of 14.45 s, same 43 iterations and exactly the same SSE (10,737,882.94, difference 0). It had to be exactly zero: the bounds only skip points that provably cannot change cluster, so every iteration gives the same labels as the naive version, hence the same means computed in the same order.
The first iteration cannot prune anything: it made 240,000 calls (n × k), which is 19.7% of all my distance computations.

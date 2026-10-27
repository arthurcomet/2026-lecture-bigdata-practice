#!/usr/bin/env python3
"""Week 7 · Task 3 — The same clustering, with far fewer distances.

Textbook §7.3, and §7.1.3 for why distance is the expensive part.

`NaiveKMeans` does what the definition says: every iteration, compare every
point with every centroid. That is n x k distance computations per pass, and on
a real dataset the distance computation is almost the entire cost.

Most of that work is wasted. After the first couple of iterations, most points
do not change cluster, and most centroids barely move. The triangle inequality
lets you prove a point cannot have changed cluster **without measuring it**.

    python3 bench.py
    python3 bench.py --yours

Correctness first: your final SSE must match the baseline's. Fewer distances
with a worse clustering is not an improvement, it is a different algorithm.
"""


class NaiveKMeans:
    """Every point against every centroid, every iteration."""

    def __init__(self, k, max_iter=50):
        self.k, self.max_iter = k, max_iter

    def run(self, points, initial_centroids, distance):
        centroids = list(initial_centroids)
        labels = [None] * len(points)
        for self.iterations in range(1, self.max_iter + 1):
            changed = False
            for i, p in enumerate(points):
                best, bi = None, 0
                for j, c in enumerate(centroids):
                    d = distance(p, c)
                    if best is None or d < best - 1e-12:
                        best, bi = d, j
                if labels[i] != bi:
                    labels[i] = bi
                    changed = True
            centroids = _means(points, labels, self.k, centroids)
            if not changed:
                break
        return labels, centroids


def _means(points, labels, k, previous):
    out = []
    for j in range(k):
        group = [p for p, l in zip(points, labels) if l == j]
        if group:
            out.append(tuple(sum(v) / len(group) for v in zip(*group)))
        else:
            out.append(previous[j])
    return out


class YourKMeans:
    """Your k-means.

        __init__(k, max_iter=50)
        run(points, initial_centroids, distance) -> (labels, centroids)

    Same starting centroids, same `distance` function - which is counted. That
    counter is your score.

    The idea, from §7.3 and the triangle inequality:

        if a point is much closer to its current centroid than that centroid
        moved, and than any other centroid could have come, then it cannot have
        changed cluster, and you do not have to measure anything

    Keeping enough bookkeeping to make that test cheap, without keeping so much
    that the bookkeeping costs more than the distances, is the task.

    You may call `distance` on two centroids, and those calls are counted too -
    which is the correct accounting, since that is real work. There are k of
    them and n points, and k is much smaller than n. That asymmetry is the
    whole opening.
    """

    def __init__(self, k, max_iter=50):
        self.k, self.max_iter = k, max_iter
        self.first_iteration_calls = 0

    def run(self, points, initial_centroids, distance):
        # Hamerly's algorithm: per point, one upper bound u (distance to its own
        # centroid) and one lower bound l (distance to the second-closest one).
        k, n = self.k, len(points)
        centroids = list(initial_centroids)
        labels = [0] * n
        upper = [0.0] * n
        lower = [0.0] * n

        def full_scan(i):
            """Measure point i against every centroid; same tie rule as the baseline."""
            best, bi, second = None, 0, float("inf")
            for j, c in enumerate(centroids):
                d = distance(points[i], c)
                if best is None or d < best - 1e-12:
                    if best is not None:
                        second = min(second, best)
                    best, bi = d, j
                else:
                    second = min(second, d)
            return bi, best, second

        for self.iterations in range(1, self.max_iter + 1):
            changed = False
            if self.iterations == 1:
                calls_before = getattr(distance, "calls", 0)
                for i in range(n):                       # nothing to prune yet
                    labels[i], upper[i], lower[i] = full_scan(i)
                changed = True
                self.first_iteration_calls = getattr(distance, "calls", 0) - calls_before
            else:
                # s[j] = half the distance from centroid j to its nearest other centroid
                s = [float("inf")] * k
                for a in range(k):
                    for b in range(a + 1, k):
                        d = distance(centroids[a], centroids[b])
                        s[a] = min(s[a], d / 2)
                        s[b] = min(s[b], d / 2)
                for i in range(n):
                    a = labels[i]
                    bound = max(s[a], lower[i])
                    if upper[i] <= bound:
                        continue                         # provably still in cluster a
                    upper[i] = distance(points[i], centroids[a])   # tighten, 1 call
                    if upper[i] <= bound:
                        continue
                    bi, upper[i], lower[i] = full_scan(i)
                    if bi != a:
                        labels[i] = bi
                        changed = True

            new_centroids = _means(points, labels, k, centroids)
            # how far each centroid moved: k calls, then loosen the bounds
            moved = [distance(c0, c1) for c0, c1 in zip(centroids, new_centroids)]
            centroids = new_centroids
            if not changed:
                break
            biggest = max(moved)
            second_biggest = sorted(moved)[-2] if k > 1 else 0.0
            for i in range(n):
                a = labels[i]
                upper[i] += moved[a]
                # the closest other centroid can have come at most this much nearer
                lower[i] -= second_biggest if moved[a] == biggest else biggest
        return labels, centroids

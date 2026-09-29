#!/usr/bin/env python3
"""Week 3 · Task 3 — Find the same pairs without comparing everything.

Textbook §3.4.

`BruteForce` compares every pair. On 3,000 documents that is 4.5 million
comparisons and it is completely correct. On 3 million documents it is 4.5
trillion and it is completely useless.

Beat it. Find the same near-duplicate pairs while making far fewer comparisons.

    python3 bench.py
    python3 bench.py --yours

The harness counts every call you make to `similarity()`. That is your score.
It also checks **recall** - which of the truly similar pairs you found. Skipping
comparisons is easy; skipping comparisons without losing the pairs is the task.
"""


class BruteForce:
    """Correct, and quadratic."""

    def __init__(self, threshold):
        self.threshold = threshold

    def find(self, docs, similarity):
        """docs is [set_of_shingles, ...]. Return {(i, j), ...} with i < j."""
        out = set()
        for i in range(len(docs)):
            for j in range(i + 1, len(docs)):
                if similarity(docs[i], docs[j]) >= self.threshold:
                    out.add((i, j))
        return out


class YourFinder:
    """Your near-duplicate finder.

        __init__(threshold)
        find(docs, similarity) -> {(i, j), ...}

    `similarity(a, b)` is the only way to compare two documents, and every call
    is counted. Everything else - signatures, banding, bucketing - is free, in
    the sense that the harness does not charge you for it. That is deliberate:
    it is also roughly true at scale, where the comparison is the expensive
    part and the hashing is linear.

    Two knobs decide everything:

        the number of hashes in a signature
        how many bands you split it into

    §3.4.2 gives you the relationship between those and the probability that a
    pair at similarity s becomes a candidate. It is an S-curve, and where its
    step sits is something you choose. Choose it on purpose and be able to say
    why in observation.md - a threshold of 0.8 does not mean bands should be
    anything in particular until you have done the arithmetic.

    You may reuse your Task 1 code.
    """

    def __init__(self, threshold, n_hashes=120, bands=40, seed=0):
        import random
        self.threshold = threshold
        self.n_hashes = n_hashes
        self.bands = bands
        rng = random.Random(seed)
        self.p = 2_147_483_647
        self.coefs = []
        for _ in range(n_hashes):
            a = rng.randrange(1, self.p)
            b = rng.randrange(0, self.p)
            self.coefs.append((a, b))

    def signature(self, doc):
        sig = []
        for a, b in self.coefs:
            smallest = None
            for number in doc:
                mixed = (a * number + b) % self.p
                if smallest is None or mixed < smallest:
                    smallest = mixed
            sig.append(smallest)
        return sig

    def find(self, docs, similarity):
        from task1_minhash import lsh_candidates
        signatures = []
        for doc in docs:
            signatures.append(self.signature(doc))
        suspects = lsh_candidates(signatures, self.bands)
        found = set()
        for i, j in suspects:
            if similarity(docs[i], docs[j]) >= self.threshold:
                found.add((i, j))
        return found

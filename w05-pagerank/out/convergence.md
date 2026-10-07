# Task 2 · How long does PageRank take to converge?

## A7 · Machine

MacBook Pro, Apple M4 Pro, 24 GB RAM, macOS 26.6.2, Python 3.13.7. Other apps open: Claude desktop app, Adobe Creative Cloud, Telegram. Timings are about this machine; iteration counts are not.

Note: I made the iteration cap a `--max-iter` option (default 5000) in `task2_convergence.py`, because the original cap of 500 would have stopped before convergence for the high betas in the worst case.

## A1, A2, A4 · Iterations against beta and graph size (tolerance 1e-10)

| beta | 1,200 nodes | 6,000 nodes | 20,000 nodes |
|---:|---:|---:|---:|
| 0.5 | 14 | 14 | 14 |
| 0.7 | 17 | 18 | 18 |
| 0.85 | 20 | 22 | 21 |
| 0.95 | 23 | 24 | 24 |
| 0.99 | 24 | 25 | 25 |

Wall time at beta = 0.85: 0.009 s (1,200 nodes), 0.052 s (6,000), 0.178 s (20,000).

## A3 · Shape as beta goes to 1

The iteration count grows with beta, but slowly on this graph: 14 iterations at beta 0.5 and 24 at 0.99, and the increase gets smaller near 1. In general each iteration only removes a fraction of the remaining error, about beta times how fast the graph mixes. In the worst case that is just beta, which would need about 2,300 iterations at beta 0.99. Here the error shrinks by about 0.35 to 0.4 per iteration (I checked: the change per step falls 0.72, 0.29, 0.024 ... 2e-11 for beta 0.99), because the graph has hubs and dead ends that spread rank everywhere quickly. So beta matters, but this graph hides most of it.

## A4 · Graph size

Going from 1,200 to 20,000 nodes (17x), the iteration count does not change (20, 22, 21 at beta 0.85). The wall time does: 0.009 s to 0.178 s (about 20x). One iteration walks every edge once, so its cost grows with the graph, but the number of iterations depends on beta and on how well the graph mixes, not on its size.

## A5 · Tolerance (1,200 nodes)

| tolerance | beta 0.85 | beta 0.95 |
|---:|---:|---:|
| 1e-4 | 9 | 9 |
| 1e-6 | 12 | 13 |
| 1e-8 | 16 | 17 |
| 1e-10 | 20 | 23 |

Each extra digit of accuracy costs about 2 more iterations (9 to 20 over 6 digits at beta 0.85), so asking for more digits is cheap here.

## A6 · Does the top 10 change with beta?

The same 10 pages are in the top 10 for every beta, at all three sizes. The order is identical from beta 0.7 to 0.99. It first changes at beta 0.5 (going down from 0.85): `p00000` and `p00004` swap places (positions 7 and 8). So on this graph the ranking is stable and beta is a tuning detail, except for the ordering of two close pages at small beta. Caveat: the top 10 are the hub pages the generator builds links toward, so this is an easy case.

# Task 2 · Where exact stops fitting

## A6 · Machine

MacBook Pro, Apple M4 Pro, 24 GB RAM, macOS 26.6.2, Python 3.13.7. Other apps open during the runs: Claude desktop app, Adobe Creative Cloud, Telegram (nothing heavy).

## A3 · Memory and time against n (from `out/limits.json`)

Stream: n items, about 0.4 n distinct. Both methods measured with `tracemalloc` in the same harness.

| n | distinct | exact time (s) | exact peak (MB) | FM time (s) | FM peak (MB) | FM estimate | FM / true |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 100,000 | 36,702 | 0.14 | 3.9 | 10.2 | 0.008 | 41,006 | 1.12x |
| 400,000 | 146,970 | 0.60 | 11.6 | 41.0 | 0.007 | 217,371 | 1.48x |
| 1,600,000 | 587,625 | 2.46 | 46.6 | 165.3 | 0.007 | 677,765 | 1.15x |
| 6,400,000 | 2,349,909 | 10.29 | 188.3 | 674.0 | 0.008 | 2,001,881 | 0.85x |

The sizes span 64x (100k to 6.4M).

Extra point, exact only (Flajolet-Martin not run, see A2): n = 25,000,000, 9,179,304 distinct, 41.1 s, 745 MB. It is not in `limits.json`.

## A4 · Growth rates

- Exact `set`: memory grows linearly with n. 64x more items gave 48x more memory (3.9 MB to 188 MB). Per distinct item it stays at about 80 bytes (79 to 80 B from 400k up, 107 B at 100k where fixed costs still show), and about 30 bytes per stream item. The 25M point agrees: 745 MB / 9.18M distinct = 81 B each.
- Flajolet-Martin: memory is flat, 0.007 to 0.008 MB at every size. It stores 64 integers, one per hash function, so its memory depends on the number of hashes and not on the data.
- Time grows linearly with n for both: every item is looked at once.

## A5 · FM accuracy against n

Ratios to the truth: 1.12x, 1.48x, 1.15x, 0.85x. They do not get better or worse as n grows, they wander inside the factor of two (range 0.85x to 1.48x). The error is set by the 64 hashes, not by n. What FM gives for free is memory; the price is that the answer stays about 15 to 50 percent off.

## A2 · Where exact stopped being possible

It did not, on this machine, and that is the result. At 6.4M items the exact set takes 10 s and 188 MB, and at 25M items it takes 41 s and 745 MB, on 24 GB of RAM. I stopped at 25M because the exact version was still comfortable there, not because anything ran out.

What became unpleasant first was **time, and it was FM, not exact**: 674 s at 6.4M, about 42 minutes projected for 25M, so I did not run FM at 25M. Most of that is a measurement effect. `tracemalloc` traces every small allocation and makes FM about 17x slower (about 100 microseconds per item under it, about 6 microseconds without it).

Extrapolation, not measured: at about 30 bytes per stream item, 24 GB would be reached around 800 million items, in practice earlier with other apps open. FM would still use about 8 KB.

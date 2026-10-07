# Task 1

A Bloom filter has no false negative because `add` only turns bits on and nothing turns them off. Predicted false-positive rate 0.860% (formula (1 - e^(-kn/m))^k), measured 0.755% on 20,000 absent items: close, the gap is random noise.
For Flajolet-Martin I average the exponents R over 64 hashes and divide by 1.26. Averaging 2^R gave about 3x too much (one lucky hash dominates), grouping then median gave about 2.4x, the median of 2^R is within 2x but always a power of two (0.82x or 1.64x), the average of R gave 0.76x to 1.29x.
Reservoir sampling never learns the length: it is the `n` in `for n, item in enumerate(stream, start=1)`, and each new item is kept with probability k/n.

# Task 2

On my MacBook Pro (M4 Pro, 24 GB) exact never became unbearable: 10 s and 188 MB at 6.4M items, 41 s and 745 MB at 25M, so nothing ran out. What got slow first was FM (674 s at 6.4M, mostly because `tracemalloc` slows it about 17x), so I ran FM up to 6.4M and only the exact set at 25M.
Growth: the exact set's memory is linear in n, about 80 bytes per distinct item (64x more items gave 48x more memory); FM's memory is flat at about 0.008 MB because it keeps only 64 numbers. FM's accuracy does not improve with n: 1.12x, 1.48x, 1.15x, 0.85x.
A factor of two is good enough for "how many distinct users today" to size a server or tell 100,000 from 1,000,000, but not for billing or reporting (2x on 40,000 users is 20,000 people) or to see a 10% change between two days.

# Task 3

I changed the number of hashes k from 1 to 7: p = (1 - e^(-kn/m))^k, and setting the derivative to zero gives k = (m/n) ln 2 = 10 x 0.693 = 6.93, so 7 (the baseline's k = 1 gives 1 - e^(-0.1) = 9.5%, matching its 9.511%).
R6: the floor for 10 bits per item is 0.6185^10 = 0.82%; I got 0.825% (1,650 of 200,000), so I reached it, with zero false negatives and exactly 80,000 bits (91% fewer false positives than the baseline).
If n were unknown: guessing too low fills the filter with 1s and errors climb fast (twice the items with k = 7 gives about 14%); guessing too high wastes bits. I would start small and add a new bigger filter when the first is half full, checking all filters on a query.

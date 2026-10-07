# Task 1

Confidence is not symmetric: on the benchmark baskets (support 50) item 1468 -> 0 has confidence 0.839 but 0 -> 1468 only 0.004, because item 0 is in 13,080 of the 20,000 baskets and 1468 in only 62. The highest-confidence rule is exactly that one, 1468 -> 0, with lift 1.28, and I do not believe it: item 0 is in 65% of all baskets anyway, so it is a rule about a popular item, not a relationship. The real relationships have the best lift, for example 270 -> 252 (confidence 0.24, lift 15.1), and it is one of the 25 pairs the generator planted.
With 2,000 items brute force needs 1,999,000 pair counters. After pass one at support 50, 1,849 items survive, so A-Priori could need up to 1,708,476 counters, and on this data it actually holds 820,259 (6,397 of them end up frequent).

# Task 2

It did not become unbearable on my MacBook Pro (M4 Pro, 24 GB): even at support 1 it takes 3.7 s and 327 MB, so nothing ran out, and I stopped there because a lower support is impossible. The counters stop growing at 893,456, the number of different pairs in these baskets, so this data is too small to break the laptop (I estimate a shop with 10,000 items would need about 6 GB).
A4: the counters grow faster than doubling per halving of the support: 5.5x (400 to 200), 4.7x (200 to 100), 3.0x (100 to 50), then they stop at 893,456 from support 25 down.
A5: the answers grow slowly and steadily, about 2.4 to 3.1 times more pairs per halving (249 at support 400, 6,397 at 50, 893,456 at 1), while the counters jump first and then stop. At support 50 I hold 820,259 counters for 6,397 answers (128 counters per answer), so a slightly lower threshold gives a few times more answers but costs several times more memory.

# Task 3

I use 120,000 buckets, chosen by testing: pass one holds the bucket array (about 122,000 numbers with the item counts) and pass two holds the counters plus the bitmap (about 135,000), so with 120,000 neither pass is much bigger than the other. The result is 117,627 peak counters instead of 820,259 (85.7% less) and exactly the same 6,397 pairs.
R5, honest accounting: with 1,000,003 buckets I got 97.2% fewer counters (23,356), but pass one then holds a million integers, which is more than the baseline's 820,259 counters. So I had only moved the memory. With 120,000 buckets the total peak is about 135,000 numbers (the bitmap is one byte per bucket, about 15,000 numbers), which is about 6 times less than 820,259. The bucket array is a fixed cost, so PCY wins when the baseline would hold more counters than about the number of buckets. In my test the baseline won at 1,000 baskets (112,650 counters against 122,000), and PCY won at 1,500 baskets (143,893 against 122,000), so the crossover here is around 1,000 to 1,500 baskets.
With a much smaller array it stops working: 1,000 and 10,000 buckets gave 0% fewer counters (820,259, the same as the baseline), because each bucket receives 340 to 3,400 pairs, far above the support of 50, so every bucket is frequent and the filter lets everything through. At 50,000 buckets it was 38% fewer and at 100,000 it was 83% fewer.

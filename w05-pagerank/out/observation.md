# Task 1

In the broken version, a dead end's rank just disappears because nobody receives it, so the total rank falls to 0. In my fixed version I share that rank equally between all nodes (1/n each), which is the same as the surfer jumping to a random page.
The same fix works for both problems because it is teleporting: a surfer who is stuck on a dead end or inside a trap still jumps to a random page. So rank cannot leak out, and it cannot stay locked in the trap (A and B keep 0.04 and 0.07 instead of 0).
`beta` is the chance that the surfer follows a link. With probability 1 - beta, the surfer gets bored and jumps to a random page, chosen uniformly.

# Task 2

When beta goes to 1, the number of iterations goes up (14 at beta 0.5, 24 at beta 0.99, with tolerance 1e-10). Each iteration only removes part of the error, and that part gets smaller when beta is closer to 1. In the worst case it would need about 2,300 iterations at 0.99, but my graph has hubs and dead ends that spread rank fast, so the growth is small.
A4: the number of iterations did not grow with the graph size (20, 22 and 21 at beta 0.85 for 1,200, 6,000 and 20,000 nodes), but the time did (0.009 s to 0.178 s, about 20 times more). The count depends on beta and on how fast the graph mixes, but one iteration reads every edge, so each iteration costs more on a bigger graph.
A6: the same 10 pages are in the top 10 for every beta, and the order only changes at beta 0.5, where two close pages swap. So on this graph beta is just a detail, but a published ranking depends on someone's choice of 0.85, so I would first check how stable it is.

# Task 3

Instead of the n x n matrix, I store the adjacency list (one entry per edge, 5,877) and two rank vectors (1,200 numbers each). That is 2n + edges = 8,277 numbers instead of 1,440,000, so 174 times less memory, and it runs 53 times faster.
R5: the teleport share (1 - beta)/n is the same number for every node, so I compute it once and add it to each node. I never build a vector or a matrix for it. Dead ends work the same way: I add up their rank once, then share it equally, which is again one number added to every node.
My worst difference from the dense answer is 1.2e-15, which is not exactly zero. The two versions add the same numbers in a different order, and floating-point rounding depends on the order. It is not a bug, and it is far below the 1e-9 limit.

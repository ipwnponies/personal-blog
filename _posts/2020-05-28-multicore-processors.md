---
title: Multi-Core Processors
categories:
- technology
- analogy
---

Multi-core processing has been mainstream for the last 15 years.
Prior to that, there was a reluctance to design programs around concurrency.

## Analogy

A great analogy for explaining multi-core processing vs. single core:

> There is a classroom consisting of 1 fast student and 10 slow students.
There are two sets of math problems for complete, with 10 questions each.
The fast student works alone on one set, while the 10 slow students work independently on the other set.

In the beginning, each student self-assigns a task.
This means the fast student will have 9 pending tasks, while the slow students have no more.

If the math problem is hard, the fast student will be able to complete the task quickly and move on to the next.
Meanwhile the slow students will struggle to complete each task.
The fast student might be able to finish all the tasks in the same time it takes a slow student to completed their
single task.
There is no advantage here.

If the math problem is easy, the slow students will complete their task quickly.
The fast student will also finish each task quickly but the individual overhead of reading each new problem statement will
slow them down.
By the time each slow student has completed their assigned task, the fast student might have only completed 5 or 6,
having spent a lot of time simply reading the question.

## Vertical vs. Horizontal Scaling

Multi-processing is not "better".
It's a choice between vertical scaling or horizontal scaling.

Vertical scaling is where the raw performance is improved.
With CPUs, this is typically increasing the frequency, efficiency of instruction set, and work done in each stage of pipeline.
The [Pentium 4][1] is a great example, where performance gains in that family was achieved solely by increasing frequency.

[1]: https://en.wikipedia.org/wiki/Pentium_4

Horizontal scaling is where the use of multiple workers is employed and tasks are divided into smaller pieces that can
be independently completed.
Independent means no order dependency or waiting on results or communication.
It is generally a good practice to write code this way anyways, even if targeting a a single-core.
Concurrency with thread-switching can still reduce the individual turnaround time of each task.

## Embarrassingly Parallel Problems

[*Embarrassingly parallel problems*][2] are workloads that benefit greatly from parallelization.
The problem in the analogy above was contrived and designed to be embarrassingly parallel.

[2]: https://en.wikipedia.org/wiki/Embarrassingly_parallel

These are tasks that are independent of each other, having few interdependencies and communications.
Multi-core processors excel at these as, each core can run off with a task and run it to completion, maximizing utilization.

### Examples

- password cracking: each candidate password does not depend on the result of another password before it can begin
- computer graphics: each frame is rendered independently and only relies on game state.
  Contrast this with video encoding schemes, where each frame **relies** on the previous frame to perform inter-diff compression.
- block chain: identical to password cracking, the candidate nonce or hash is independent of results of a previous candidate

## Heterogeneity

Multi-core processors can be homogenous (all cores are identical) or [heterogenous][3].

[3]: https://en.wikipedia.org/wiki/Heterogeneous_computing

A homogenous architecture is easy to scale and schedule work, as each worker is identical.
The choice boils down to whoever is available.
There are no degrees of freedom, w.r.t. choice of core.

A heterogeneous architecture has different cores.
This can be different CPU frequency, cache size, bus connections, etc.
The two main advantages are performance efficiency or energy efficiency.

Performance efficiency can be gained by better fitting the workload.

- tasks require a massive cache, they can be assigned to a big-cache core
- tasks that perform complex arithmetic can be assigned to a core with more FPU

This can be due to constraint on CPU size and choosing to beef up one core to handle specialized workloads.

Energy efficiency can be gained by adding energy efficient cores.
They may not perform well but have low energy footprint, allowing for cheap compute.
Examples:

- ARM big.LITTLE, a popular architecture for smartphones and portable devices
- PS2 Emotion Engine
- PS3 Cell processor

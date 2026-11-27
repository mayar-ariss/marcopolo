# Ways to break an assumption

Use in step 5. For each baseline assumption, try several of these moves and
keep the candidates where the move changes the mechanism, not just the
wording. Each example is an established technique, so it can also serve as
prior work to check against.

| Move | Breaks the assumption that... | Example | Watch for |
|---|---|---|---|
| Invert | work flows in the current direction | Push changes from the source instead of polling; index documents by term (inverted index) instead of scanning per query | The new direction may concentrate load on the other side |
| Remove | a requirement is real | Drop global ordering and use CRDTs instead of consensus for counters and sets | The requirement may turn out to be real for some users |
| Relax exactness | the answer must be exact | HyperLogLog for distinct counts, Bloom filters for membership, Count-Min sketch for frequencies | Error bounds must be stated and acceptable to the consumer |
| Change representation | the data must stay in its current form | Intervals as sorted endpoint events (sweep line); graph search as sparse matrix products; substring queries on a suffix array | Conversion cost and the cost of keeping both forms in sync |
| Move work in time | work happens when it is requested | Prefix sums for range queries; materialized views; or the reverse, lazy evaluation that defers work until a result is needed | Staleness, and precompute cost when queries are rare |
| Move work elsewhere | the current component must do the work | Push filtering into the database query; enforce invariants in the type system instead of at run time; validate on the client | Trust boundaries: work moved to an untrusted party must be rechecked |
| Change the unit of work | items are processed one at a time, or all at once | Batch writes in a log-structured merge tree; vectorize per-element loops; stream instead of loading everything | Latency for batching, memory for whole-set processing |
| Exploit the distribution | inputs are arbitrary | Counting sort for small key ranges; cache the hot keys; special-case already sorted input | Performance cliffs when the distribution shifts |
| Randomize | the procedure must be deterministic | Random pivots in quicksort; power-of-two-choices load balancing; reservoir sampling | Reproducibility; seed and report it |
| Trade space and time | the current balance is right | Memoization; recomputing instead of storing (gradient checkpointing) | Memory limits, cache invalidation |
| Make it incremental | the answer is recomputed from scratch | Incremental view maintenance; union-find for connectivity under edge insertions | Deletions are often much harder than insertions |
| Dualize | the problem must be solved as stated | Max-flow through min-cut; LP duality; Lagrangian relaxation | The dual may give bounds rather than a direct solution |
| Reduce to a solved problem | the problem needs a custom algorithm | Encode scheduling or dependency resolution as SAT, MaxSAT, or ILP and use a solver | Encoding size, and solver time on hard instances |
| Change the failure model | failure must be prevented | Optimistic concurrency instead of locks; idempotent operations with retries; crash-only design | Retry storms and contention under load |

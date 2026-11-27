# Example: sorting many small integers

A complete engineering-mode run on a small problem, chosen so every number
can be reproduced in a minute. The outcome is a conditional win: the
candidate is about 3x faster on the inputs it targets and 2-5x slower on
others, so the conventional solution stays the default. Reports like this,
including the parts that fail, are what the skill is meant to produce.

Measured with `scripts/compare.py` on Python 3.13, 2 CPU cores, 7 repeats.

## 1. Problem statement

Input: a Python list of `n` integers. Output: a new list with the same
elements in ascending order. Metric: median wall time at `n = 1,000,000`.

## 2. Constraints

Input and output are plain Python lists. Keys are integers. The motivating
case has keys in a small range, `[0, 1000)`, so most values repeat. Nothing
is known in advance about the order of the input.

## 3. Baseline

`sorted(xs)`: Timsort, implemented in C. It is the strongest standard
choice for a Python list. It rests on the assumption that only comparisons
between keys are available, which costs `O(n log n)`.

## 4. Prior work and early-stop check

Counting sort and radix sort are textbook techniques for small integer
keys; `numpy.bincount` provides the counting step. Nothing here is novel.
Early-stop check: with at most 1,000 distinct keys, counting needs
`O(n + k log k)` work instead of `O(n log n)`, so there is room to beat the
baseline. Continue.

## 5. Candidates

Each breaks the comparison-only assumption a different way (see
`references/operators.md`):

- **A. Counter (exploit the distribution).** Count keys with
  `collections.Counter`, sort the distinct keys, expand.
- **B. NumPy bincount (change representation).** Convert to an array,
  `bincount`, `repeat`, convert back.
- **C. LSD radix sort (change the unit of work).** Bucket by byte in pure
  Python.

## 6. Pre-commit

- Inputs: three distributions, keys in `[0, 1000)` (target), keys in
  `[0, 10^9)` (almost all distinct), and all elements equal, at sizes
  0, 1, 1000, 100,000 and 1,000,000.
- Noise floor: baseline against itself at 1,000,000 gave 0.92x and 1.05x
  on two seeds, so differences within about 10% are ties.
- General win: at least 1.5x at 1,000,000 on the target distribution, at
  least 0.9x at 1,000,000 on the other two, and outputs agree everywhere.
- Conditional win: the first condition holds but not the second. The
  baseline stays the default.
- Ruled out: any disagreement on integer inputs.

## 7. Probe

Speedup over `sorted` on the target distribution (seed 0, 5 repeats):

| candidate | n = 10,000 | n = 100,000 | n = 1,000,000 | peak memory at 1,000,000 |
|---|---|---|---|---|
| A. Counter | 1.70x | 3.37x | 3.41x | 8.0 MiB (baseline 11.4 MiB) |
| B. NumPy | 3.45x | 3.90x | 3.87x | 45.6 MiB |
| C. Radix | 0.82x | 0.87x | 0.89x | 24.0 MiB |

C loses at every size and its speedup grows only slowly, so it is dropped.
A and B differ by about 13% at 1,000,000, close to the noise floor. A is
selected: it needs no third-party dependency and uses a sixth of B's memory.

## 8. Build

Counting gains nothing when most keys are distinct, so the build falls
back to `sorted` in that case:

```python
from collections import Counter


def solve(xs):
    """Sort a list of ints by counting equal keys.

    Precondition: elements are ints (or another type where equal values are
    interchangeable). Counter merges equal keys, so 1 and 1.0, or 0.0 and
    -0.0, would come back as copies of whichever was seen first.
    """
    counts = Counter(xs)
    # Mostly distinct keys: counting saves nothing, so use the baseline.
    if len(counts) * 4 > len(xs):
        return sorted(xs)
    out = []
    for k in sorted(counts):
        out.extend([k] * counts[k])
    return out
```

Baseline (`baseline.py`) and input generators (`gen.py`, `gen_wide.py`,
`gen_same.py`):

```python
def solve(xs):
    return sorted(xs)
```

```python
import random

def make_input(n, seed):            # gen.py: keys in [0, 1000)
    r = random.Random(seed)
    return [r.randrange(1000) for _ in range(n)]

def make_input(n, seed):            # gen_wide.py: keys in [0, 10**9)
    r = random.Random(seed)
    return [r.randrange(10**9) for _ in range(n)]

def make_input(n, seed):            # gen_same.py: all elements equal
    return [7] * n
```

## 9. Verify

Fresh seed (2), 7 repeats:

    python /path/to/marcopolo/scripts/compare.py --baseline baseline.py:solve \
        --candidate candidate.py:solve --inputs gen.py:make_input \
        --sizes 0,1,1000,100000,1000000 --repeats 7 --seed 2

Keys in `[0, 1000)`:

| n | baseline median (best) | candidate median (best) | speedup | baseline peak | candidate peak | outputs |
|---|---|---|---|---|---|---|
| 0 | 1.1 us (0.8 us) | 6.4 us (4.3 us) | 0.169x | 566 B | 656 B | agree |
| 1 | 1.0 us (0.6 us) | 5.6 us (4.3 us) | 0.177x | 566 B | 776 B | agree |
| 1000 | 81.4 us (80.6 us) | 131.5 us (125.8 us) | 0.619x | 11.9 KiB | 30.3 KiB | agree |
| 100000 | 11.40 ms (11.14 ms) | 3.40 ms (3.24 ms) | 3.35x | 1.1 MiB | 836.2 KiB | agree |
| 1000000 | 131.22 ms (120.48 ms) | 41.04 ms (40.32 ms) | 3.2x | 11.4 MiB | 8.2 MiB | agree |

Keys in `[0, 10^9)`:

| n | baseline median (best) | candidate median (best) | speedup | baseline peak | candidate peak | outputs |
|---|---|---|---|---|---|---|
| 0 | 2.0 us (1.6 us) | 11.5 us (10.8 us) | 0.172x | 566 B | 656 B | agree |
| 1 | 1.9 us (1.6 us) | 10.3 us (9.5 us) | 0.18x | 566 B | 776 B | agree |
| 1000 | 83.4 us (81.6 us) | 145.0 us (129.9 us) | 0.575x | 12.0 KiB | 54.6 KiB | agree |
| 100000 | 14.21 ms (13.91 ms) | 20.54 ms (20.36 ms) | 0.692x | 1.1 MiB | 7.5 MiB | agree |
| 1000000 | 204.58 ms (203.66 ms) | 342.95 ms (299.50 ms) | 0.597x | 11.4 MiB | 60.0 MiB | agree |

All elements equal:

| n | baseline median (best) | candidate median (best) | speedup | baseline peak | candidate peak | outputs |
|---|---|---|---|---|---|---|
| 0 | 1.9 us (1.7 us) | 11.8 us (10.5 us) | 0.162x | 566 B | 656 B | agree |
| 1 | 2.1 us (1.8 us) | 10.7 us (9.8 us) | 0.198x | 566 B | 776 B | agree |
| 1000 | 7.2 us (6.5 us) | 40.0 us (37.7 us) | 0.18x | 8.1 KiB | 16.6 KiB | agree |
| 100000 | 404.8 us (365.3 us) | 2.33 ms (2.29 ms) | 0.174x | 781.5 KiB | 1.5 MiB | agree |
| 1000000 | 5.31 ms (4.74 ms) | 23.59 ms (23.34 ms) | 0.225x | 7.6 MiB | 15.3 MiB | agree |

The fallback roughly halves the loss on almost-distinct keys (on seed 1,
0.26x without it and 0.52x with it) but cannot remove it, because the
`Counter` is built before the candidate knows to fall back.

## 10. Critique

A separate pass over only the problem, the criteria, both implementations
and the tables. It was run by the same agent, so it is not independent in
the sense step 10 asks for. It found:

- **Wrong output on mixed types.** `solve([1, 1.0, ...])` returns only
  `1`s, and `True` swallows `1`. Integer inputs are correct; the
  precondition is now stated in the docstring.
- **The baseline was not weak, it was adaptive.** Timsort finds runs, so
  on all-equal input it is close to linear and beats counting by about 4x.
  Presorted input was not measured and is likely to behave the same way.
- **Small inputs lose.** At 1,000 elements and below, the `Counter`
  overhead dominates; the probe already won at 10,000.
- **No novelty.** Counting sort is textbook; the value here is knowing
  exactly when it pays.

## 11. Report

- **Verdict:** conditional win. 3.2x faster at 1,000,000 on keys from a
  small range (above the 1.5x threshold and the noise floor), but 0.60x on
  almost-distinct keys and 0.23x on all-equal input, below the 0.9x floor.
- **Deliver:** keep `sorted` as the default. Use the counting version only
  where the caller knows the keys are ints from a small range with many
  repeats, the input is not already ordered, and `n` is at least about
  10,000.
- **Cost:** about 10 lines of logic and a type precondition that `sorted` does not have.
- **To win generally:** a cheap way to detect the key range and existing
  order before committing to counting, such as sampling a prefix.

## Process note

The criteria in step 6 were written down after the probes in step 7 and
after an exploratory verification run on seed 1, which is out of order and
the kind of slip step 6 exists to prevent. To limit the damage, the final
verification above was run on a seed that had not been used before, after
the criteria were fixed. Seed 1 gave the same verdict.

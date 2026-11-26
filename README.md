# marcopolo

A skill for exploring unconventional designs for coding, architecture, and
research problems. It reduces a problem to its hard constraints, names the
conventional solutions and the assumptions they rest on, and generates
alternatives that each break a different assumption. It fixes success and
failure criteria before running anything, probes the most promising
candidates, builds the winner, benchmarks it against the baseline, and puts
it through an independent critique. If no alternative wins, it says so and
delivers the conventional solution.

## Usage

Invoke it by name:

    marcopolo: design a rate limiter for a multi-tenant API

Add `engineering:` or `research:` after the name to choose a mode.
Engineering requires working code; research allows unverified theory and
requires a literature search:

    marcopolo research: abductive inference from sparse observations

It also applies when you explicitly ask for a non-standard, novel, or
first-principles alternative to the usual approach.

## Files

- `SKILL.md`: the process and rules.
- `scripts/compare.py`: benchmark harness that runs a baseline and a
  candidate over a range of input sizes and reports time, peak memory,
  speedup, and whether the outputs agree. Standard library only; run
  `python scripts/compare.py --help` for options.
- `references/operators.md`: ways to break an assumption, each with an
  established example and its risks.
- `references/transfers.md`: structures from other fields that have working
  implementations, with costs, plus transfers that do not hold up.

# marcopolo

**Unconventional designs that have to beat a strong baseline, or it tells you
they don't.**

A skill for exploring unconventional designs for coding, architecture, and
research problems. It reduces a problem to its hard constraints, names the
conventional solutions and the assumptions they rest on, and generates
alternatives that each break a different assumption. It fixes success and
failure criteria before running anything, probes the most promising
candidates, builds the winner, benchmarks it against the baseline, and puts
it through an independent critique. If no alternative wins, it says so and
delivers the conventional solution.

## Install

**Claude Code**, as a plugin (updates with `claude plugin update`):

    /plugin install marcopolo --marketplace mayar-ariss/marcopolo

or from your shell:

    claude plugin marketplace add mayar-ariss/marcopolo
    claude plugin install marcopolo@marcopolo

**Claude Code**, as a plain skill:

    git clone https://github.com/mayar-ariss/marcopolo ~/.claude/skills/marcopolo

**claude.ai**: download this repository as a zip and upload it as a custom
skill.

`SKILL.md` follows the Agent Skills format, so other agents that read that
format can load it from a clone of this repository.

## Usage

Invoke it by name:

    marcopolo: design a rate limiter for a multi-tenant API

Add `engineering:` or `research:` after the name to choose a mode.
Engineering requires working code; research allows unverified theory and
requires a literature search:

    marcopolo research: abductive inference from sparse observations

It also applies when you explicitly ask for a non-standard, novel, or
first-principles alternative to the usual approach.

## Example

[`examples/counting-sort.md`](examples/counting-sort.md) is a complete run
with real measurements. The candidate was 3.2x faster on the inputs it
targeted and 2-5x slower on others, so the skill kept `sorted()` as the
default and said exactly when the alternative pays off.

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
- `examples/`: worked runs, including the measurements.
- `.claude-plugin/`: plugin and marketplace manifests for Claude Code.

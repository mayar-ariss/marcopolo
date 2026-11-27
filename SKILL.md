---
name: marcopolo
description: Explore unconventional designs for a coding, architecture, or research problem. Use when the user invokes "marcopolo" or explicitly asks for a non-standard, novel, or first-principles alternative to the usual approach.
---

# marcopolo

Goal: find a solution that differs from the conventional one in mechanism
(algorithm, data model, architecture), not in surface syntax, and that works.

## Modes

State the mode at the start. The user can set it with "marcopolo
engineering:" or "marcopolo research:". Otherwise choose engineering when
there is code to ship and research when the request is an open question or
a research area.

- **Engineering.** Working code is required. Step 4 is a quick check for
  existing libraries and known algorithms. Theory-only output is not
  allowed unless the user agrees.
- **Research.** Step 4 is a full literature search that lists what was
  searched. Theory-only output is allowed. The report separates verified
  results from unverified ones.

## Process

1. **Problem statement.** Restate the problem formally: inputs, outputs,
   and the metric or benchmark that decides success. If the request is a
   broad area rather than a problem, narrow it to one concrete problem and
   say which one was chosen and why.
2. **Constraints.** Reduce the problem to its hard constraints: data sizes,
   complexity bounds, state and mutation, failure modes. Separate real
   constraints from habits.
3. **Baseline.** Name the 2-3 conventional solutions and the assumption each
   one rests on. These are the comparison point, not the answer. Use the
   strongest standard version of each: an established library or a tuned
   implementation, not a naive one written for the comparison.
4. **Prior work.** Search the literature if tools allow. For each direction
   under consideration, name the closest existing work. If no search was
   possible, say so and treat every novelty claim as unchecked. Then decide
   whether there is room to beat the baseline: is it already near a known
   lower bound for these constraints, or does existing work already cover
   the directions under consideration? If so, stop here: deliver the
   conventional solution, give the evidence, and say what would have to
   change for an alternative to be worth exploring.
5. **Candidates.** Generate at least three alternatives, each breaking a
   different baseline assumption. Borrow structures from other fields
   (biology, physics, linguistics, mathematics, etc.) only where the
   borrowed model changes how the solution works and is formal enough to
   compute with. Drop analogies that only rename things. For each
   candidate, state what it adds over the closest prior work. See
   `references/operators.md` for concrete ways to break an assumption and
   `references/transfers.md` for borrowed structures that have working
   implementations.
6. **Pre-commit.** Before running anything, write down the metric, the
   input sizes, the threshold that counts as beating the baseline, and the
   result that would rule each candidate out. Include sizes at the scale
   the problem actually runs at, not only small ones. Set the threshold
   above the noise floor: run the baseline against itself in the harness
   and treat any speedup within that spread as a tie. Do not change these
   after seeing results. If a change is unavoidable, report what changed
   and why.
7. **Probe and select.** Prototype the two or three most promising
   candidates with minimal code on small inputs: a few dozen lines and a
   run of seconds each, not full implementations. Run each probe at two or
   three sizes spaced about 10x apart and compare how cost grows, not only
   absolute times: a candidate that loses at small sizes but grows more
   slowly may win at the pre-committed sizes. Extrapolate to those sizes
   and label it as an extrapolation. Select by what the probes show, not by
   how novel a candidate sounds, and record which probe results decided
   it. If code cannot be run, say that the selection was made by judgement
   alone.
8. **Build.** Implement the selected candidate fully using only real
   libraries and APIs. Keep the code readable.
9. **Verify.** Compare against the baseline on correctness and on the
   pre-committed metric, including edge cases: empty input, a single
   element, duplicates, and worst-case distributions. For Python, use the
   harness below; for other languages, write an equivalent harness that
   reports the same columns. If the pre-committed metric is not time or
   memory (throughput under contention, error rate, latency percentiles),
   write a harness that measures that metric directly rather than
   substituting run time. If the candidate fails the pre-committed
   criteria, record the cause as a new constraint. If the next-ranked
   candidate's probe still looks viable under that constraint, build and
   verify it once against the same criteria. Do not retry beyond that.
10. **Critique.** Have a reviewer that has not seen the reasoning behind
    steps 5-9 try to break the result. Give it only the problem statement,
    the pre-committed criteria, the candidate and baseline code, and the
    measurements, and ask for failing inputs, flawed measurements, a
    baseline that was weakened or misconfigured, and existing work that
    already does the same thing. Use a separate agent if one is available;
    otherwise do a separate pass that rereads only those materials. Fix or
    report every finding.
11. **Report.** State what is different, how it measured against the
    pre-committed criteria, where it breaks, what it costs in
    maintainability, how it relates to prior work, and what the critique
    found.

## Harness

`scripts/compare.py` in this skill's folder runs a baseline and a candidate
over a range of input sizes and reports median and best time, peak memory,
speedup, and whether the outputs agree. Run it from the directory that holds
the solution files, giving the script's full path inside this skill's
folder, since the `file.py:function` arguments are resolved relative to the
current directory:

    python /path/to/marcopolo/scripts/compare.py \
        --baseline baseline.py:solve \
        --candidate candidate.py:solve \
        --inputs gen.py:make_input \
        --sizes 0,1,100,10000,1000000

Each solution takes one input and returns a result. `make_input(n, seed)`
returns one input of size n. Outputs are compared with `==` unless
`--check file.py:check` is given, which is needed for floating-point
tolerance or when several outputs are valid. The exit status is 1 if the
candidate fails, times out, or disagrees with the baseline. To measure the
noise floor for step 6, pass the baseline as both `--baseline` and
`--candidate`. Run with `--help` for all options. Paste the table into the
report.

## Rules

- Never invent libraries, APIs, citations, or results. Every number in the
  report comes from a run, not an estimate.
- Claim novelty only relative to the prior work actually checked, and say
  what was checked.
- If a candidate cannot be built or tested yet, it may be delivered as
  theory only, in research mode or with the user's agreement. Label it
  "unverified", state the formal definitions it depends on, and describe
  the experiment that would test it.
- If no alternative beats the conventional solution after the one retry,
  say so, deliver the conventional solution, and describe the most
  promising alternative and what would have to be true for it to win.

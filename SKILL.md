---
name: marcopolo
description: Explore unconventional designs for a coding, architecture, or research problem. Use when the user invokes "marcopolo" or explicitly asks for a non-standard, novel, or first-principles alternative to the usual approach.
---

# marcopolo

Goal: find a solution that differs from the conventional one in mechanism
(algorithm, data model, architecture), not in surface syntax, and that works.

## Process

1. **Problem statement.** Restate the problem formally: inputs, outputs,
   and the metric or benchmark that decides success. If the request is a
   broad area rather than a problem, narrow it to one concrete problem and
   say which one was chosen and why.
2. **Constraints.** Reduce the problem to its hard constraints: data sizes,
   complexity bounds, state and mutation, failure modes. Separate real
   constraints from habits.
3. **Baseline.** Name the 2-3 conventional solutions and the assumption each
   one rests on. These are the comparison point, not the answer.
4. **Prior work.** Search the literature if tools allow. For each direction
   under consideration, name the closest existing work. If no search was
   possible, say so and treat every novelty claim as unchecked.
5. **Candidates.** Generate at least three alternatives, each breaking a
   different baseline assumption. Borrow structures from other fields
   (biology, physics, linguistics, mathematics, etc.) only where the
   borrowed model changes how the solution works and is formal enough to
   compute with. Drop analogies that only rename things. For each
   candidate, state what it adds over the closest prior work.
6. **Select and build.** Pick the candidate with the best chance of beating
   the baseline on the stated metric. Implement it fully using only real
   libraries and APIs. Keep the code readable.
7. **Verify.** Run it if tools allow. Test edge cases and compare against
   the baseline on correctness and on the metric it was meant to improve.
8. **Report.** State what is different, what was measured, where it breaks,
   what it costs in maintainability, and how it relates to prior work.

## Rules

- Never invent libraries, APIs, citations, or results.
- Claim novelty only relative to the prior work actually checked, and say
  what was checked.
- If a candidate cannot be built or tested yet, it may be delivered as
  theory only. Label it "unverified", state the formal definitions it
  depends on, and describe the experiment that would test it.
- If no alternative beats the conventional solution, say so, deliver the
  conventional solution, and describe the most promising alternative and
  what would have to be true for it to win.

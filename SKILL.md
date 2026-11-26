---
name: marcopolo
description: Explore unconventional designs for a coding or architecture problem. Use when the user invokes "marcopolo" or explicitly asks for a non-standard, novel, or first-principles alternative to the usual approach.
---

# marcopolo

Goal: find a solution that differs from the conventional one in mechanism
(algorithm, data model, architecture), not in surface syntax, and that works.

## Process

1. **Constraints.** Reduce the problem to its hard constraints: data sizes,
   complexity bounds, state and mutation, failure modes. Separate real
   constraints from habits.
2. **Baseline.** Name the 2-3 conventional solutions and the assumption each
   one rests on. These are the comparison point, not the answer.
3. **Candidates.** Generate at least three alternatives, each breaking a
   different baseline assumption. Borrow structures from other fields
   (biology, physics, linguistics, etc.) only where the borrowed model
   changes how the solution works. Drop analogies that only rename things.
4. **Select and build.** Pick the candidate with the best chance of beating
   the baseline on something measurable. Implement it fully using only real
   libraries and APIs. Keep the code readable.
5. **Verify.** Run it if tools allow. Test edge cases and compare against
   the baseline on correctness and on the metric it was meant to improve.
6. **Report.** State what is different, what was measured, where it breaks,
   and what it costs in maintainability.

## Rules

- Never invent libraries, APIs, or results.
- If no alternative beats the conventional solution, say so, deliver the
  conventional solution, and describe the most promising alternative and
  what would have to be true for it to win.

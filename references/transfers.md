# Transfers from other fields

Use in step 5 when borrowing a structure from another field. Each entry
names the formal object that carries over, what it changes about how a
solution works, implementations that exist, the problems it suits, and its
costs. Check current versions and APIs before relying on any of them. Add an
entry only with a named implementation or paper.

## Logic programming: abduction as model search

- **Formal object:** abductive logic programs and answer set programs.
  Explanations are minimal sets of assumptions that, with the rules, entail
  the observations.
- **Changes:** hypotheses are declared instead of hand-searched; a solver
  enumerates or optimizes them.
- **Implementations:** clingo (Potassco), SWI-Prolog.
- **Suits:** abduction over discrete hypotheses with hard constraints,
  diagnosis, configuration.
- **Costs:** grounding can blow up on large domains.

## Satisfiability: minimal explanations and diagnoses

- **Formal object:** SAT, SMT, and MaxSAT; minimal unsatisfiable cores and
  minimal correction sets.
- **Changes:** "smallest set of assumptions that explains or contradicts the
  observations" becomes a solver query.
- **Implementations:** Z3 (`z3-solver`), PySAT (`python-sat`).
- **Suits:** fault diagnosis, explaining why a configuration fails,
  constraint-based abduction.
- **Costs:** worst-case exponential; encoding effort.

## Bayesian statistics: abduction as posterior inference

- **Formal object:** generative models over hidden causes; the posterior
  ranks explanations.
- **Changes:** explanations are graded by probability instead of accepted
  or rejected.
- **Implementations:** PyMC, NumPyro, Pyro, Stan.
- **Suits:** noisy or incomplete observations, competing explanations.
- **Costs:** inference can be slow or fail to converge; check diagnostics.

## Causal inference: counterfactuals

- **Formal object:** structural causal models. Pearl computes
  counterfactuals in three steps: abduction (infer the hidden background
  from evidence), action (intervene), and prediction.
- **Changes:** separates correlation from intervention; "what caused this"
  and "what would have happened" become computable given a causal model.
- **Implementations:** DoWhy (effect estimation, counterfactuals),
  causal-learn (causal discovery).
- **Suits:** root-cause analysis, decision support, auditing models.
- **Costs:** results depend on causal assumptions; discovery from
  observational data needs strong assumptions.

## Control theory: online state estimation

- **Formal object:** Kalman filters and particle filters infer a hidden
  state from a stream of noisy observations.
- **Changes:** explanation is updated incrementally as data arrives instead
  of recomputed.
- **Implementations:** FilterPy, python-control.
- **Suits:** streaming sensor or telemetry data, tracking.
- **Costs:** the Kalman filter assumes linear dynamics and Gaussian noise;
  particle filters need many samples in high dimensions.

## Information theory: relevance as information about a target

- **Formal object:** the information bottleneck. Compress an input while
  keeping as much information as possible about a target variable; relevant
  means informative about the target.
- **Changes:** gives relevance a measurable definition and a trade-off
  parameter.
- **Implementations:** no standard library. Variational information
  bottleneck (Alemi et al., 2017) is implemented in PyTorch or JAX; mutual
  information estimates are available in scikit-learn
  (`mutual_info_classif`, `mutual_info_regression`).
- **Suits:** feature and evidence selection, representation learning.
- **Costs:** mutual information estimates are unreliable in high
  dimensions.

## Optimal transport: matching and comparing distributions

- **Formal object:** transport plans and Wasserstein distances.
- **Changes:** compares or aligns distributions by moving mass at minimum
  cost, which respects geometry where pointwise measures do not.
- **Implementations:** POT (`pot`, imported as `ot`), GeomLoss.
- **Suits:** assignment with costs, domain alignment, comparing histograms
  or point clouds.
- **Costs:** exact solvers scale roughly cubically; entropic (Sinkhorn)
  solvers are faster but biased by the regularization.

## Algebraic topology: shape and local-to-global consistency

- **Formal object:** persistent homology summarizes the shape of data
  across scales. Cellular sheaves attach data to the nodes and edges of a
  graph and measure whether local pieces agree on overlaps.
- **Changes:** sheaves turn "do these local explanations fit together" into
  a linear-algebra question (the sheaf Laplacian).
- **Implementations:** GUDHI, Ripser, giotto-tda for persistent homology.
  For sheaves, the Neural Sheaf Diffusion reference code (Bodnar et al.,
  NeurIPS 2022), or build sheaf Laplacians with `scipy.sparse`.
- **Suits:** combining local hypotheses into a consistent global one,
  sensor fusion, graphs where neighbors differ (heterophily).
- **Costs:** persistent homology cost grows quickly with the number of
  points and the homology dimension.

## Statistical physics: energy minimization and message passing

- **Formal object:** energy-based models (Ising, Potts), annealing, belief
  propagation on factor graphs.
- **Changes:** global consistency emerges from local interactions.
- **Implementations:** `scipy.optimize.dual_annealing`; pgmpy for belief
  propagation.
- **Suits:** combinatorial optimization, marginal inference on graphs.
- **Costs:** loopy belief propagation may not converge; annealing gives no
  optimality guarantee.

## Neuroscience: active inference

- **Formal object:** agents in partially observable Markov decision
  processes choose actions that reduce expected free energy, which includes
  uncertainty about hidden states.
- **Changes:** the system acts to gather evidence for or against
  explanations instead of waiting for data.
- **Implementations:** pymdp.
- **Suits:** small discrete settings where choosing what to observe next
  matters.
- **Costs:** limited to discrete state spaces of modest size; the broader
  claims of the free energy principle are debated.

## Biology: evolutionary search

- **Formal object:** populations under selection and variation; CMA-ES
  adapts a search distribution.
- **Changes:** optimizes without gradients or a closed-form model.
- **Implementations:** DEAP, `cma` (CMA-ES).
- **Suits:** black-box and non-differentiable objectives.
- **Costs:** needs many evaluations; on small budgets Bayesian
  optimization often does better.

## Category theory: composition by construction

- **Formal object:** wiring diagrams and operads describe how components
  compose.
- **Changes:** correctness of a composite system follows from the
  correctness of its parts and the composition rules.
- **Implementations:** Catlab.jl (AlgebraicJulia).
- **Suits:** systems assembled from many typed parts, scientific model
  composition.
- **Costs:** Julia only; steep learning curve; the benefit is structure,
  rarely speed.

## Weak or unsupported transfers

- **Integrated information theory.** PyPhi computes integrated information
  (Φ) exactly, but the cost grows faster than exponentially with system
  size, so it is practical only for small systems of binary elements. The
  theory is contested as an account of consciousness. Use Φ as a measure on
  small systems, not as a design principle.
- **Relevance logic.** Formal and well studied, but general-purpose
  tooling is scarce. Expect to encode it in a general prover or write a
  custom proof search.
- **Relevance theory (Sperber and Wilson).** A linguistic theory, not
  formal enough to compute with directly. The information bottleneck is the
  nearest computable counterpart.
- **Quantum-inspired methods on classical hardware.** Check whether any
  claimed speedup survives classical "dequantization" (Tang, 2019).
- **Metaphors without a formal object.** "Neural", "organic", or "swarm"
  used as labels. Drop them unless a concrete model is specified, such as
  the pheromone update rule of ant colony optimization.

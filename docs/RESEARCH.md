# Research Notes & Technical Report Plan

This is the "IIT-level" layer: understand why each technique works, prove or measure it, and write it up.

## 1. Theory to Master (by phase)

### Phase 0–1: Game search
- Zero-sum games and the minimax theorem
- Game tree size: O(b^d); chess branching factor is roughly 30–35
- Alpha-Beta: correctness (same value as Minimax); best case O(b^(d/2)) with perfect ordering (Knuth–Moore analysis); worst case O(b^d)
- Negamax as a rewrite of Minimax using max(a, b) = -min(-a, -b)
- Effective branching factor: measure it, don't just state it

### Phase 2: Search engineering
- Why iterative deepening is cheap: the last level dominates the cost
- Horizon effect and why quiescence fixes it
- Transposition table soundness: why bound flags (EXACT/LOWER/UPPER) are needed
- Hash collision probability for 64-bit keys
- Search instability from the graph-history-interaction problem (repetition and TT)

### Phase 3: Pruning and reductions
- Null-move pruning assumption and zugzwang failure cases
- Why LMR works: ordering quality makes late moves unlikely to be best
- PVS: zero-window searches and re-search cost
- Futility pruning margins and when they are unsafe
- SEE: swap algorithm and why it beats MVV-LVA

### Phase 4: Evaluation
- Tapered evaluation as linear interpolation by game phase
- Texel tuning: model P(win) = 1 / (1 + 10^(-K·eval/400)); minimize mean squared error against outcomes; fit by gradient descent
- Overfitting and validation splits on positions from different games

### Phase 5: Performance
- Bitboards and bit-parallel move generation
- Cache effects on TT size
- Lazy SMP and why parallel alpha-beta scales sub-linearly

### Phase 6: Neural evaluation
- Supervised regression on evaluation targets; loss choices (MSE vs cross-entropy on WDL)
- NNUE: first-layer sparsity and incremental accumulator updates make evaluation cheap
- Quantization and its accuracy trade-off

### Phase 7: RL and MCTS
- MCTS: selection, expansion, evaluation, backup
- PUCT formula and the role of priors, exploration constant, Dirichlet noise
- AlphaZero loss: `L = (z − v)² − πᵀ log p + c‖θ‖²`
- Why gating and replay buffers stabilize training

## 2. Experiments to Run (each becomes a report section)

| # | Experiment | Output |
|---|------------|--------|
| E1 | Minimax vs Alpha-Beta node counts by depth | Table + log-scale chart |
| E2 | Effective branching factor with and without move ordering | Chart |
| E3 | Ordering heuristics ablation (MVV-LVA, killers, history, SEE) | Cutoff rate table |
| E4 | TT size vs nodes and hit rate | Curve |
| E5 | Pruning ablation (null-move, LMR, futility): Elo gain and tactical solve rate | SPRT table |
| E6 | Texel tuning: loss curve and Elo before/after | Chart |
| E7 | Speedup from native core and threads | nps and scaling curve |
| E8 | Classical vs NN vs NNUE at equal time control | Elo table |
| E9 | Self-play iterations vs Elo | Curve |
| E10 | Failure analysis: positions the engine plays badly and why | Case studies |

## 3. Report Outline (target: 8–12 pages)

1. Abstract
2. Introduction and motivation
3. Background: adversarial search, chess engines
4. System design (architecture summary)
5. Search techniques and ablations (E1–E5)
6. Evaluation and tuning (E6)
7. Performance engineering (E7)
8. Learning-based evaluation and self-play (E8–E9)
9. Statistical testing methodology (SPRT, Elo)
10. Limitations and failure analysis (E10)
11. Conclusion and future work
12. References

Publish as a PDF in `docs/report/` (LaTeX or Markdown → PDF); optionally post to arXiv or a personal site.

## 4. Reading List

- C. Shannon, *Programming a Computer for Playing Chess* (1950)
- D. Knuth and R. Moore, *An Analysis of Alpha-Beta Pruning* (1975)
- J. Schaeffer, work on the history heuristic and transposition tables
- D. Silver et al., *Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm* (2017)
- Stockfish NNUE documentation and the Chess Programming Wiki (search, evaluation, Texel tuning, Lazy SMP)
- Russell and Norvig, *Artificial Intelligence: A Modern Approach* (adversarial search chapters)

## 5. Habits That Make It Research-Grade

- State a hypothesis before each experiment ("move ordering will cut nodes by X").
- Change one variable at a time.
- Report negative results.
- Seed everything and record hardware and versions.
- Keep a lab notebook in `docs/notes/` with dates, commits and results.

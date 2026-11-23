# Benchmarking & Statistical Testing

Claims need numbers, and numbers need error bars.

## 1. Metrics

| Metric | Definition |
|--------|------------|
| Max completed depth | Deepest fully finished iteration within the time limit |
| Nodes | Positions visited (including quiescence) |
| Nodes/second (nps) | Nodes ÷ elapsed time |
| Time per move | Wall-clock time |
| Effective branching factor | (nodes at depth d / nodes at depth d−1), averaged |
| Cutoff rate / first-move cutoff % | Quality of move ordering |
| TT hit rate, fill % | Table efficiency |
| Tactical solve rate | EPD positions solved within a time limit |
| Elo (± error) | From match results, see below |
| Bench signature | Total node count at fixed depth over a fixed position set; changes only when behavior changes |

## 2. Ablation Ladder

Run each step on the same positions at fixed depth (compare nodes) and at fixed time (compare depth and strength):

1. Minimax
2. + Alpha-Beta
3. + Move ordering (MVV-LVA → killers → history → SEE)
4. + Iterative deepening
5. + Transposition table
6. + Quiescence
7. + PVS and aspiration windows
8. + Null-move, LMR, futility, extensions
9. + Tapered/advanced evaluation, then Texel-tuned evaluation
10. + Native core, then multi-threading
11. Classical vs Neural vs NNUE (equal time control)
12. MCTS + policy/value network vs alpha-beta engine

## 3. Positions & Suites

- `experiments/benchmarks/positions.json`: 50+ FENs (opening, middlegame, endgame)
- Tactical EPD suites (e.g. WAC, Bratko-Kopec, ECM) for solve-rate curves
- Mate-in-N puzzle set
- Opening suite (book lines or randomized 4–8 ply openings) for match play

## 4. Method

- Fix seeds; record CPU, RAM, OS, Python and compiler versions.
- Warm up, then take the median of at least 3 runs.
- Same machine, plugged in, background tasks closed.
- Fixed-depth comparisons measure search efficiency; fixed-time comparisons measure real strength.
- Never change two things between runs.

## 5. Match Play with cutechess-cli

```bash
cutechess-cli \
  -engine cmd=./run_engine_new.sh name=new \
  -engine cmd=./run_engine_base.sh name=base \
  -each proto=uci tc=10+0.1 option.Hash=64 \
  -openings file=openings.pgn format=pgn order=random \
  -games 2 -rounds 500 -repeat -concurrency 4 \
  -sprt elo0=0 elo1=5 alpha=0.05 beta=0.05 \
  -pgnout experiments/results/match.pgn
```

Notes:
- Play each opening with colors swapped (`-repeat`).
- Use time controls, not just fixed depth, so speed counts.
- Run enough games; small samples mislead.

## 6. SPRT (Sequential Probability Ratio Test)

Decide if a change is an improvement without fixing the game count in advance.

- H0: Elo gain ≤ elo0 (e.g. 0); H1: Elo gain ≥ elo1 (e.g. +5)
- Error rates alpha (false accept) and beta (false reject), typically 0.05
- Games continue until the log-likelihood ratio crosses a bound: accept the change, reject it, or hit the game cap
- Rule: **a change merges only if it passes SPRT or a deterministic test shows it is a pure speedup**

## 7. Elo Estimation

From a match with W wins, D draws, L losses over N games:

- score = (W + 0.5·D) / N
- Elo difference = −400 · log10(1/score − 1)
- Report the 95% confidence interval (use the trinomial variance; the standard error shrinks roughly as 1/√N)

Ladder to publish: random mover → Phase 1 → 2 → 3 → 4 → neural → Stockfish at fixed low skill levels. Anchor Elo to a known opponent and state the time control.

## 8. Output

Results go to `experiments/results/` as CSV/JSON plus charts:

- Nodes vs configuration (log scale)
- Depth vs time limit
- nps by build (Python, Numba/native, threads)
- Elo ladder with error bars
- SPRT progress plot per change
- Effective branching factor with/without ordering

## 9. CI Regression Checks

- Bench signature must match unless the change is intentionally behavioral
- nps must not drop more than a set percentage
- Tactical suite solve rate must not decrease

## 10. Report Template

```
Build: <commit / phase>        Hardware: <CPU / RAM>, Python <ver>
Positions: <count>             Depth / Time control: <value>
Nodes (median): <n>   nps: <n>   Time/move: <s>   Depth reached: <d>
EBF: <x>   First-move cutoff: <%>   TT hit rate: <%>
Tactical solve rate: <%>
Match vs <baseline>: +<W> =<D> -<L>   Elo: <x> ± <y>   SPRT: <accepted/rejected>
```

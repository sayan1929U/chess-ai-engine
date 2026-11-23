# Roadmap — Phase 0 to Phase 9

From zero to a research-grade chess engine. Each phase is a complete release: **learn → implement → test → benchmark → write up**. Do not start the next phase until the exit criteria of the current one are met.

## Overview

| Phase | Name | Weeks | Outcome | Rough strength target* |
|-------|------|-------|---------|------------------------|
| 0 | Foundations & Setup | 1 | Repo, CI, theory notes, perft | — |
| 1 | Core Engine | 2 | Minimax + Alpha-Beta, playable CLI | ~1000–1300 |
| 2 | Search Engineering | 3 | ID, ordering, Zobrist, TT, quiescence | ~1500–1800 |
| 3 | Professional Search | 3 | PVS, null-move, LMR, SEE, book, UCI | ~1900–2200 |
| 4 | Strong Evaluation | 3 | Tapered eval, king safety, Texel tuning | +100–200 Elo |
| 5 | Performance Engineering | 3 | Profiling, bitboards/native core, Lazy SMP | 5–50x nodes/sec |
| 6 | Neural Evaluation | 4 | PyTorch value net, NNUE-style eval | measured vs classical |
| 7 | Self-Play RL & MCTS | 4 | AlphaZero-style policy/value + MCTS | experimental |
| 8 | Rigorous Testing & Elo | 2 | SPRT, cutechess-cli, Elo ladder | calibrated Elo |
| 9 | Product & Research Output | 3 | UI, dashboard, Lichess bot, technical report | portfolio-ready |

\*Estimates only. Measure your own Elo in Phase 8. Pure Python is slow; Phase 5 exists to fix that.

Total: about 28 weeks. Run it alongside DSA/interview prep; Phases 0–3 alone already make a strong project.

---

## Phase 0 — Foundations & Setup (Week 1)

**Goal:** a clean base and the theory you need before writing search code.

**Learn**
- Zero-sum games, minimax theorem, game trees, branching factor, search complexity O(b^d)
- Chess rules edge cases: castling, en passant, promotion, repetition, 50-move rule
- python-chess API; FEN and PGN formats

**Build**
- [ ] Repo, venv, `requirements.txt`, `pyproject.toml`
- [ ] Folder layout from ARCHITECTURE.md
- [ ] pytest, ruff/flake8, mypy, pre-commit
- [ ] GitHub Actions CI
- [ ] Perft test runner (validates move generation setup)
- [ ] `docs/notes/` with theory notes in your own words

**Exit criteria:** CI green, perft matches known counts, notes on minimax and alpha-beta written.

---

## Phase 1 — Core Engine (Weeks 2–3)

**Goal:** a working engine that plays legal, sensible chess.

**Learn:** Minimax, Negamax, Alpha-Beta, recursion, backtracking, depth-limited search.

**Build**
- [ ] Board wrapper and game-end detection
- [ ] Material evaluation (centipawns)
- [ ] Plain Minimax (kept forever as the baseline)
- [ ] Negamax + Alpha-Beta
- [ ] Mate scoring with ply adjustment (prefer faster mates)
- [ ] Search stats (nodes, time)
- [ ] CLI: human vs AI, depth option
- [ ] Tests: mate-in-1/2, hanging pieces, Minimax == Alpha-Beta score

**Deliverables:** playable CLI, first node-count comparison (Minimax vs Alpha-Beta).

**Exit criteria:** beats a random mover 100/100; solves mate-in-2 puzzles; Alpha-Beta gives identical scores with far fewer nodes.

---

## Phase 2 — Search Engineering (Weeks 4–6)

**Goal:** search deeper and smarter with the same hardware.

**Learn:** iterative deepening, move ordering, hashing, transpositions, horizon effect.

**Build**
- [ ] Iterative deepening with time management
- [ ] Move ordering: MVV-LVA, promotions, checks
- [ ] Killer moves and history heuristic
- [ ] Zobrist hashing (incremental), verified against `chess.polyglot`
- [ ] Transposition table (EXACT/LOWER/UPPER, depth-preferred replacement)
- [ ] Quiescence search
- [ ] Piece-square tables
- [ ] Principal variation tracking
- [ ] Benchmark harness v1

**Deliverables:** ablation table (each feature's effect on nodes and depth).

**Exit criteria:** TT on/off gives same score at fixed depth; ordering reduces nodes measurably; Phase 2 beats Phase 1 in a 100-game match.

---

## Phase 3 — Professional Search (Weeks 7–9)

**Goal:** the techniques used in real engines.

**Learn:** zero-window search, null-move assumption (zugzwang), reductions, static exchange evaluation.

**Build**
- [ ] Principal Variation Search
- [ ] Aspiration windows
- [ ] Null-move pruning (with zugzwang guard)
- [ ] Late Move Reductions
- [ ] Check extensions
- [ ] Futility / delta pruning
- [ ] Static Exchange Evaluation (SEE) for capture ordering
- [ ] Opening book (Polyglot)
- [ ] Syzygy endgame tablebases
- [ ] **UCI protocol** so the engine runs in standard GUIs (Arena, Cute Chess)

**Deliverables:** full ablation of Phase 3 features; engine playable in a chess GUI.

**Exit criteria:** every technique shows a measured gain or is removed; UCI works end to end.

---

## Phase 4 — Strong Evaluation (Weeks 10–12)

**Goal:** a much better evaluation function, tuned with data instead of guesswork.

**Learn:** tapered evaluation, logistic regression for evaluation tuning, feature engineering.

**Build**
- [ ] Tapered eval (middlegame/endgame interpolation by game phase)
- [ ] King safety (pawn shield, attackers, open files)
- [ ] Pawn structure (doubled, isolated, passed, backward)
- [ ] Mobility, bishop pair, rook on open/semi-open file, outposts
- [ ] Pawn hash table
- [ ] **Texel tuning:** fit evaluation weights to game outcomes with gradient descent
- [ ] Evaluation unit tests (symmetry, mirrored positions)

**Deliverables:** tuned parameter set, before/after match results.

**Exit criteria:** tuned eval beats hand-set eval by a statistically significant margin (see Phase 8 method).

---

## Phase 5 — Performance Engineering (Weeks 13–15)

**Goal:** make it fast. Depth is Elo.

**Learn:** profiling, bitboards, cache behavior, parallel search.

**Build**
- [ ] Profile with `cProfile` and `py-spy`; find hot paths
- [ ] Optimize move generation and evaluation (NumPy, Numba, or Cython)
- [ ] Choose one: custom bitboard core in **C++/Rust with Python bindings**, or Numba-compiled hot loops
- [ ] Lazy SMP multi-threaded/multi-process search with shared TT
- [ ] Memory tuning of TT (size, replacement scheme)
- [ ] Regression guard: nodes/sec tracked in CI

**Deliverables:** performance report with flame graphs and before/after nps.

**Exit criteria:** documented speedup (target 5–50x nodes/sec depending on approach), identical search results single-thread vs optimized.

---

## Phase 6 — Neural Evaluation (Weeks 16–19)

**Goal:** a learned evaluator integrated into the search. This is the hybrid-AI step.

**Learn:** supervised regression for value functions, board encodings, NNUE idea (efficiently updatable networks), quantization.

**Build**
- [ ] Board encoding (12 piece planes + side, castling, en passant)
- [ ] Data pipeline: positions labeled from deep classical search and game outcomes
- [ ] PyTorch value network (MLP first, then small CNN)
- [ ] Training loop with validation split, LR schedule, experiment tracking
- [ ] NNUE-style architecture: sparse input features, incremental accumulator update
- [ ] Integrate as `Evaluator`; compare at equal time, not equal depth
- [ ] Optional: int8 quantization, ONNX export

**Deliverables:** training report (loss curves, data size), classical vs neural match results.

**Exit criteria:** neural eval runs inside search; comparison reported honestly, including if it loses.

---

## Phase 7 — Self-Play RL & MCTS (Weeks 20–23)

**Goal:** AlphaZero-style learning, at small scale.

**Learn:** Monte Carlo Tree Search, PUCT, policy and value heads, self-play loop.

**Build**
- [ ] Move encoding (action space)
- [ ] Policy + value network (PyTorch)
- [ ] MCTS with PUCT and neural priors
- [ ] Self-play game generation with Dirichlet noise and temperature
- [ ] Replay buffer and training loop
- [ ] Evaluation gating: new network must beat the old one to be promoted
- [ ] Start small (e.g. endgames or a reduced game) before full chess

**Deliverables:** self-play training curves, Elo progression over iterations.

**Exit criteria:** network measurably improves over iterations against a fixed baseline.

---

## Phase 8 — Rigorous Testing & Elo (Weeks 24–25)

**Goal:** claims backed by statistics.

**Build**
- [ ] Automated matches via **cutechess-cli**
- [ ] **SPRT** (sequential probability ratio test) for accept/reject of changes
- [ ] Elo estimation with confidence intervals
- [ ] Ladder: random → Phase 1 → 2 → 3 → 4 → neural → Stockfish at fixed low skill levels
- [ ] Tactical test suites (EPD): solve rate vs time
- [ ] Regression suite in CI (fixed-depth node counts and bench signature)

**Exit criteria:** an Elo table with error bars and a reproducible test script.

---

## Phase 9 — Product & Research Output (Weeks 26–28)

**Goal:** make it visible and credible.

**Build**
- [ ] Pygame (or web) GUI with eval bar, PV display, move analysis
- [ ] Matplotlib/Plotly performance dashboard
- [ ] Lichess bot deployment (via Lichess Bot API) for live games
- [ ] Technical report (see RESEARCH.md) — arXiv-style PDF
- [ ] Demo video/GIF, polished README with real numbers
- [ ] Release tags per phase

**Exit criteria:** public repo, live demo or bot, report, and a CV entry with measured results.

---

## Suggested CV Bullets (fill in after measuring)

> Built a chess engine in Python/C++ with Negamax, Alpha-Beta, PVS, null-move pruning, LMR, Zobrist-hashed transposition tables and quiescence search; reached depth N at M nodes/sec and an estimated Elo of X (SPRT-tested over K games).

> Trained a PyTorch/NNUE-style evaluation network and an AlphaZero-style policy/value network with MCTS self-play; improved over the classical evaluator by Y Elo.

## Working Rules

1. One feature per branch; merge only with a benchmark or test showing it helps.
2. Keep every baseline runnable for comparison.
3. Write a short note per phase: what you learned, what surprised you, what failed.
4. If a technique does not help, remove it and document why. That is a result too.

# Product Requirements Document (PRD)

**Product:** Advanced Chess AI Engine
**Owner:** Sayan Dey
**Status:** Draft v2.0 (phase-based)
**Last updated:** 2026-11-08

---

## 1. Overview

A chess engine built in ten phases, from a basic Minimax player to a research-grade system with professional search, tuned evaluation, native performance, neural evaluation and AlphaZero-style self-play. It is both a strong portfolio project and a learning vehicle for algorithms, systems performance and machine learning.

## 2. Goals

1. Build a correct, playable engine, then make it strong through measurable steps.
2. Prove every improvement with benchmarks and statistical testing (SPRT, Elo with error bars).
3. Reach professional-engine techniques: PVS, null-move, LMR, SEE, tablebases, UCI.
4. Add a hybrid AI layer: neural evaluation and self-play RL with MCTS.
5. Produce a public technical report, a live demo (Lichess bot), and CV-ready results.

## 3. Non-Goals

- Beating Stockfish or Leela Chess Zero.
- Re-implementing chess rules in early phases (python-chess handles legality).
- Online accounts, payments, or mobile apps.

## 4. Users

| User | Need |
|------|------|
| Recruiter / interviewer | Clear docs, measured results, readable code |
| Player | Playable opponent, adjustable strength |
| Learner | Visible search internals and theory notes |
| Researcher | Reproducible experiments and ablations |

## 5. Requirements by Phase

### Phase 0 — Foundations
| ID | Requirement |
|----|-------------|
| P0-1 | Repo, CI, linting, type checks |
| P0-2 | Perft tests for move generation validation |
| P0-3 | Theory notes (minimax, alpha-beta, complexity) |

### Phase 1 — Core Engine
| ID | Requirement |
|----|-------------|
| P1-1 | Minimax and Negamax with Alpha-Beta |
| P1-2 | Material evaluation, mate scoring by ply |
| P1-3 | Game-end detection, CLI human vs AI |
| P1-4 | Search stats (nodes, time) |

### Phase 2 — Search Engineering
| ID | Requirement |
|----|-------------|
| P2-1 | Iterative deepening with time management |
| P2-2 | Move ordering (MVV-LVA, killers, history) |
| P2-3 | Zobrist hashing and transposition table |
| P2-4 | Quiescence search, piece-square tables |
| P2-5 | Principal variation output |

### Phase 3 — Professional Search
| ID | Requirement |
|----|-------------|
| P3-1 | PVS, aspiration windows |
| P3-2 | Null-move pruning, LMR, check extensions, futility pruning |
| P3-3 | SEE-based capture ordering |
| P3-4 | Opening book, Syzygy tablebases |
| P3-5 | UCI protocol support |

### Phase 4 — Strong Evaluation
| ID | Requirement |
|----|-------------|
| P4-1 | Tapered evaluation |
| P4-2 | King safety, pawn structure, mobility, piece bonuses |
| P4-3 | Pawn hash table |
| P4-4 | Texel tuning pipeline |

### Phase 5 — Performance
| ID | Requirement |
|----|-------------|
| P5-1 | Profiling reports and optimized hot paths |
| P5-2 | Native or JIT-compiled core |
| P5-3 | Lazy SMP multi-threaded search |
| P5-4 | nps regression tracking |

### Phase 6 — Neural Evaluation
| ID | Requirement |
|----|-------------|
| P6-1 | Board encoding and labeled dataset pipeline |
| P6-2 | PyTorch value network and training loop |
| P6-3 | NNUE-style incremental evaluation |
| P6-4 | Neural evaluator integrated into search |

### Phase 7 — Self-Play RL & MCTS
| ID | Requirement |
|----|-------------|
| P7-1 | Policy/value network |
| P7-2 | MCTS with PUCT |
| P7-3 | Self-play generation, replay buffer, training, gating |

### Phase 8 — Testing & Elo
| ID | Requirement |
|----|-------------|
| P8-1 | cutechess-cli match automation |
| P8-2 | SPRT and Elo with confidence intervals |
| P8-3 | EPD tactical suites, regression suite in CI |

### Phase 9 — Product & Research
| ID | Requirement |
|----|-------------|
| P9-1 | GUI with eval bar and PV display |
| P9-2 | Performance dashboard |
| P9-3 | Lichess bot deployment |
| P9-4 | Technical report and polished README |

## 6. Non-Functional Requirements

| Area | Requirement |
|------|-------------|
| Correctness | Perft passes; optimized and baseline search agree at fixed depth |
| Reproducibility | Seeded runs; pinned dependencies; recorded hardware |
| Modularity | Search and evaluators swappable by interface |
| Quality | Type hints, linting, 80%+ coverage on search and evaluation |
| Documentation | Notes per phase, report, architecture docs |

## 7. Success Metrics

| Phase | Metric | Target |
|-------|--------|--------|
| 1 | Alpha-Beta vs Minimax nodes at equal depth | 10x+ reduction |
| 1 | Win rate vs random | 100% |
| 2 | Phase 2 vs Phase 1 (100 games) | 70%+ score |
| 2 | Depth in 5s | 6+ |
| 3 | Each pruning technique | Measured gain or removed |
| 3 | UCI compatibility | Runs in Cute Chess / Arena |
| 4 | Tuned vs hand-set eval | Statistically significant gain (SPRT) |
| 5 | nodes/sec speedup | 5–50x vs Phase 3 baseline |
| 6 | Neural vs classical eval | Reported honestly at equal time |
| 7 | Self-play improvement | Positive Elo trend over iterations |
| 8 | Elo estimate | Reported with confidence interval |
| 9 | Public deliverables | Repo, report, bot or demo |

## 8. Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Python too slow | Phase 5 native/JIT core; profile before optimizing |
| Subtle search bugs | Perft, baseline-vs-optimized comparisons, tactics suites |
| TT corruption | Test TT on/off equivalence, bound-type tests |
| Neural net underperforms | Present as an experiment; compare at equal time |
| RL training too costly | Start with endgames or reduced settings; use Colab/Kaggle GPUs |
| Scope too large | Each phase ships independently; Phases 0–3 are already a strong project |
| Stalled progress | Weekly goals, one feature per branch, short phase write-ups |

## 9. Dependencies

`python-chess`, `numpy`, `numba` or a C++/Rust toolchain, `torch`, `pygame`, `pytest`, `matplotlib`, `cutechess-cli`, Stockfish (as a test opponent only).

## 10. Open Questions

- Native core language: C++ (pybind11) or Rust (PyO3)?
- GPU access for Phases 6–7 (Colab, Kaggle, college lab)?
- GUI: Pygame or web?
- Training data: self-play only, or bootstrapped from labeled positions?

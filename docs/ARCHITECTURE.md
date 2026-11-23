# Architecture

## 1. Design Principles

- **Separation of concerns:** rules, search, evaluation, learning and UI are independent.
- **Swappable parts:** any searcher can use any evaluator through shared interfaces.
- **Measurable:** every search returns stats; every feature has an on/off flag for ablation.
- **Phase-incremental:** each phase adds modules without rewriting earlier ones. Baselines stay runnable.

## 2. System Overview

```
        ┌────────────┐   ┌─────────────┐   ┌──────────────┐
        │  CLI / GUI │   │ UCI adapter │   │ Lichess bot  │
        └─────┬──────┘   └──────┬──────┘   └──────┬───────┘
              └─────────────────┼─────────────────┘
                                ▼
                        ┌──────────────┐
                        │ Engine facade│  config, time control, stats
                        └──────┬───────┘
                 ┌─────────────┼───────────────┐
                 ▼             ▼               ▼
          ┌───────────┐  ┌───────────┐   ┌───────────┐
          │ Book /    │  │ Searcher  │   │   MCTS    │
          │ Syzygy    │  │ (AB / PVS)│   │  (PUCT)   │
          └───────────┘  └─────┬─────┘   └─────┬─────┘
                               │               │
                  ┌────────────┼───────┐       │
                  ▼            ▼       ▼       ▼
             ┌────────┐  ┌─────────┐ ┌──────────────┐
             │  TT    │  │ Ordering│ │  Evaluator   │
             │Zobrist │  │ SEE/KH  │ │ classical /  │
             └────────┘  └─────────┘ │ NNUE / NN    │
                                     └──────────────┘
                               ▲
                      Board layer (python-chess → native core in Phase 5)
```

## 3. Phase-to-Module Map

| Phase | Modules added |
|-------|---------------|
| 0 | project skeleton, `perft.py`, CI |
| 1 | `search/minimax.py`, `search/negamax.py`, `evaluation/material.py`, `engine.py`, `interfaces/cli.py` |
| 2 | `search/iterative.py`, `search/ordering.py`, `search/quiescence.py`, `search/zobrist.py`, `search/table.py`, `evaluation/pst.py` |
| 3 | `search/pvs.py`, `search/see.py`, `book/`, `interfaces/uci.py` |
| 4 | `evaluation/features.py`, `evaluation/tapered.py`, `experiments/tuning/` |
| 5 | `native/`, `search/smp.py` |
| 6 | `learning/encoding.py`, `learning/dataset.py`, `learning/model.py`, `learning/train.py`, `evaluation/neural.py`, `evaluation/nnue.py` |
| 7 | `learning/mcts.py`, `learning/policy_value.py`, `learning/selfplay.py` |
| 8 | `experiments/benchmarks/` (match, SPRT and Elo scripts) |
| 9 | `interfaces/gui.py`, dashboard, `interfaces/lichess.py` |

## 4. Module Layout

Five packages, one job each: `search` decides, `evaluation` judges, `book` remembers, `learning` trains, `interfaces` talks to the outside world.

```
src/chess_ai/
├── perft.py                # P0: move-generation check
├── engine.py               # P1: Engine facade (config in, SearchResult out)
├── types.py                # P1: SearchResult, SearchConfig, score constants
├── search/
│   ├── minimax.py          # P1: baseline, kept forever
│   ├── negamax.py          # P1: alpha-beta
│   ├── iterative.py        # P2: iterative deepening, time management
│   ├── ordering.py         # P2: TT move, MVV-LVA, killers, history
│   ├── quiescence.py       # P2
│   ├── zobrist.py          # P2: position hashing
│   ├── table.py            # P2: transposition table
│   ├── pvs.py              # P3: PVS, aspiration, null-move, LMR, futility
│   ├── see.py              # P3: static exchange evaluation
│   └── smp.py              # P5: Lazy SMP
├── evaluation/
│   ├── base.py             # P1: Evaluator protocol
│   ├── material.py         # P1
│   ├── pst.py              # P2
│   ├── features.py         # P4: king safety, pawns, mobility
│   ├── tapered.py          # P4
│   ├── neural.py           # P6
│   └── nnue.py             # P6
├── book/
│   ├── opening_book.py     # P3
│   └── syzygy.py           # P3
├── learning/
│   ├── encoding.py         # P6: board to tensor
│   ├── dataset.py          # P6
│   ├── model.py            # P6: value network
│   ├── train.py            # P6/P7
│   ├── policy_value.py     # P7
│   ├── mcts.py             # P7: PUCT search
│   └── selfplay.py         # P7
├── interfaces/
│   ├── cli.py              # P1
│   ├── uci.py              # P3
│   ├── gui.py              # P9
│   └── lichess.py          # P9
└── native/                 # P5: C++/Rust or Numba hot paths (created then)

experiments/                # everything that produces numbers
├── benchmarks/             # depth, nodes, nps, match, SPRT scripts, positions.json
├── tuning/                 # Texel tuning
└── results/                # CSV, JSON, charts (gitignored)
```

## 5. Core Interfaces

```python
class Evaluator(Protocol):
    def evaluate(self, board) -> int: ...           # centipawns, side-to-move perspective

class Searcher(Protocol):
    def search(self, board, limits: SearchLimits) -> SearchResult: ...

@dataclass
class SearchResult:
    best_move: chess.Move
    score: int
    depth: int
    nodes: int
    nps: float
    time: float
    pv: list[chess.Move]
```

## 6. Search Pipeline (Phases 1–3)

```python
def negamax(board, depth, alpha, beta, ply):
    if tt_hit := tt.probe(key) and usable: return tt_hit.score
    if depth <= 0: return quiescence(board, alpha, beta)
    if can_null_move(board, depth): ...            # null-move pruning
    for i, move in enumerate(order_moves(board)):
        board.push(move)
        if i == 0:
            score = -negamax(board, depth - 1, -beta, -alpha, ply + 1)
        else:
            reduce = lmr_reduction(depth, i)       # late move reduction
            score = -negamax(board, depth - 1 - reduce, -alpha - 1, -alpha, ply + 1)
            if score > alpha:                      # re-search on surprise
                score = -negamax(board, depth - 1, -beta, -alpha, ply + 1)
        board.pop()
        if score >= beta: update_killers_history(move); tt.store(...); return score
        alpha = max(alpha, score)
    tt.store(...)
    return alpha
```

Move ordering priority: TT move → winning captures (SEE/MVV-LVA) → promotions → killers → history → quiet moves.

## 7. Transposition Table

- Zobrist key: random 64-bit per (piece, square) + side + castling + en passant file; updated incrementally.
- Entry: `key`, `depth`, `score`, `flag` (EXACT / LOWER / UPPER), `best_move`, `age`.
- Replacement: depth-preferred with aging; fixed memory budget.
- Mate scores stored relative to the node, adjusted by ply on retrieval.
- Verified against `chess.polyglot.zobrist_hash` and with TT on/off equivalence tests.

## 8. Evaluation

| Layer | Phase | Notes |
|-------|-------|-------|
| Material | 1 | Piece values |
| PST | 2 | Piece-square tables |
| Features + tapering | 4 | King safety, pawn structure, mobility; interpolate by game phase |
| Texel-tuned | 4 | Weights fit to game outcomes via gradient descent |
| Neural / NNUE | 6 | Learned; NNUE uses sparse features and incremental accumulator updates |

## 9. Learning Stack (Phases 6–7)

**Value network:** input = board tensor (12×8×8 + metadata) or sparse NNUE features; output = scalar value.

**Policy/value network (AlphaZero-style):** shared trunk, policy head over the move space, value head in [-1, 1].

**MCTS (PUCT):** select child maximizing `Q + c_puct · P · √N_parent / (1 + N_child)`, expand with network priors, back up the value.

**Self-play loop:** generate games → store (state, visit distribution, outcome) → train → evaluate new vs old → promote if it wins the gate match.

## 10. Performance Layer (Phase 5)

- Profile first; optimize only what the profiler shows.
- Move to bitboards in a native core (C++/pybind11 or Rust/PyO3) or Numba-compiled kernels.
- Lazy SMP: multiple threads/processes search the same root with a shared TT and slightly different depths.
- Track nodes/sec in CI to catch regressions.

## 11. Integration Layer

- **UCI adapter:** implements `uci`, `isready`, `position`, `go`, `stop`, `quit`; reports `info depth score nodes nps pv`.
- **Lichess bot:** wraps the UCI engine with the Lichess Bot API for live games.

## 12. Testing Hooks

Deterministic seeds, per-feature flags, bench signature (fixed-depth node count on a fixed position set) to detect accidental behavior changes. See [TESTING.md](TESTING.md) and [BENCHMARKING.md](BENCHMARKING.md).

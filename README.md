# Advanced Chess AI Engine

A research-grade chess engine built phase by phase: **adversarial search, search engineering, professional pruning, tuned evaluation, native performance, neural evaluation, self-play RL with MCTS.** Every claim is backed by benchmarks and statistically tested Elo.

> Minimax and Alpha-Beta are classical search, not machine learning. The neural evaluator (Phase 6) and the AlphaZero-style network (Phase 7) are what make this a hybrid AI engine.

## Phases

| Phase | Name | What you build |
|-------|------|----------------|
| 0 | Foundations | Repo, CI, perft tests, theory notes |
| 1 | Core Engine | Minimax, Negamax, Alpha-Beta, material evaluation, CLI |
| 2 | Search Engineering | Iterative deepening, move ordering, Zobrist hashing, transposition table, quiescence |
| 3 | Professional Search | PVS, null-move, LMR, SEE, opening book, tablebases, UCI |
| 4 | Strong Evaluation | Tapered eval, king safety, pawn structure, Texel tuning |
| 5 | Performance | Profiling, native or Numba core, multi-threaded search |
| 6 | Neural Evaluation | PyTorch value net, NNUE-style evaluation |
| 7 | Self-Play RL and MCTS | Policy/value network, PUCT, self-play loop |
| 8 | Testing and Elo | cutechess-cli, SPRT, Elo with confidence intervals |
| 9 | Product and Research | GUI, dashboard, Lichess bot, technical report |

Full checklists and exit criteria: [docs/ROADMAP.md](docs/ROADMAP.md). **Current phase: 0.**

## Quick Start

```bash
git clone https://github.com/sayan1929U/chess-ai-engine.git
cd chess-ai-engine

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

pytest                             # run the tests
python -m chess_ai.perft --depth 4 # validate move generation
```

Later phases add `python -m chess_ai.interfaces.cli` (play) and `python -m chess_ai.interfaces.uci` (chess GUIs).

## Project Structure

```
chess-ai-engine/
├── README.md, LICENSE, pyproject.toml, requirements.txt, .pre-commit-config.yaml
├── .github/workflows/ci.yml      # lint, type check, tests
│
├── docs/
│   ├── PRD.md  ARCHITECTURE.md  ROADMAP.md  RESEARCH.md  BENCHMARKING.md  TESTING.md
│   ├── notes/                    # phase0.md ... phase9.md: learn / build / exit / your notes
│   ├── report/                   # final technical report
│   └── images/                   # charts, diagrams, demo GIF
│
├── src/chess_ai/
│   ├── perft.py                  # P0  move-generation check (done)
│   ├── types.py                  # P1  SearchConfig, SearchResult, score constants (done)
│   ├── engine.py                 # P1  Engine facade
│   ├── search/                   # minimax, negamax, iterative, ordering, quiescence,
│   │                             #   zobrist, table, pvs, see, smp
│   ├── evaluation/               # base, material, pst, features, tapered, pawn_hash,
│   │                             #   neural, nnue
│   ├── book/                     # opening_book, syzygy
│   ├── learning/                 # encoding, dataset, model, train, policy_value, mcts, selfplay
│   ├── interfaces/               # cli, uci, gui, lichess
│   └── native/                   # P5  Numba or C++/Rust hot paths
│
├── experiments/                  # everything that produces numbers
│   ├── benchmarks/               # positions.json, openings.pgn, suites/,
│   │                             #   run_depth / run_match / run_sprt / run_all
│   ├── tuning/                   # texel.py
│   └── results/                  # CSV, JSON, charts (gitignored)
│
├── tests/                        # one test file per module; unimplemented phases are skipped
├── data/                         # training data (gitignored)
└── models/                       # trained weights (gitignored)
```

Rule of thumb: **`src/` is the engine, `experiments/` is the evidence, `docs/` is the explanation.**

## Documentation

| File | Contents |
|------|----------|
| [docs/ROADMAP.md](docs/ROADMAP.md) | Phase 0 to 9 plan |
| [docs/notes/](docs/notes/) | Per-phase learning guide, checklist and your notes (phase0 to phase9) |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Components, data flow, interfaces |
| [docs/PRD.md](docs/PRD.md) | Requirements and success metrics |
| [docs/RESEARCH.md](docs/RESEARCH.md) | Theory, experiments, report outline |
| [docs/BENCHMARKING.md](docs/BENCHMARKING.md) | Metrics, SPRT, Elo |
| [docs/TESTING.md](docs/TESTING.md) | Test strategy |

## Results (fill in as you go)

| Version | Depth @ 5s | Nodes/sec | Elo (± error) | Notes |
|---------|-----------|-----------|---------------|-------|
| Phase 1 | | | | |
| Phase 2 | | | | |
| Phase 3 | | | | |
| Phase 4 | | | | |
| Phase 5 | | | | |
| Phase 6 | | | | |

## Tech Stack

Python, python-chess, NumPy, PyTorch, Pygame, Matplotlib, pytest, ruff, mypy, cutechess-cli, GitHub Actions. Native core (C++/Rust or Numba) in Phase 5.

`python-chess` handles rules and legality. Search, hashing, evaluation and learning are written from scratch.

## Author

**Sayan Dey** — [GitHub](https://github.com/sayan1929U) · [LinkedIn](https://linkedin.com/in/sayandey1111)

## License

MIT

# Testing

## Tools

`pytest` for tests, `pytest-cov` for coverage. Run:

```bash
pytest -q
pytest --cov=chess_ai --cov-report=term-missing
```

## Layout

```
tests/
├── test_board.py          # wrapper and game-end detection
├── test_evaluation.py     # material, PST, symmetry
├── test_zobrist.py        # hashing correctness
├── test_tt.py             # table store/probe/replacement
├── test_search_basic.py   # minimax vs alpha-beta equivalence
├── test_search_tactics.py # mate-in-N and tactical puzzles
├── test_ordering.py       # move ordering behavior
├── test_quiescence.py     # stability on capture sequences
├── test_engine_api.py     # Engine facade and config
├── test_ml_encoding.py    # board-to-tensor
└── test_integration.py    # full game vs random mover
```

## What to Test

### Correctness
- **Perft:** node counts for the starting position and standard test positions match known values (validates move generation setup).
- **Game end:** checkmate, stalemate, insufficient material, threefold repetition, fifty-move rule.

### Evaluation
- Symmetry: a position and its color-flipped mirror evaluate to opposite scores.
- Starting position evaluates to about 0.
- Extra queen scores higher than extra pawn.

### Search
- **Equivalence:** Minimax and Alpha-Beta return the same score at the same depth.
- **TT correctness:** search with TT on and off returns the same score at fixed depth (best move may differ on ties).
- **Tactics:** finds mate in 1, 2 and 3; captures a hanging queen; avoids a one-move blunder.
- **Move ordering:** with ordering, node count is less than or equal to without it.
- **Iterative deepening:** respects the time limit and always returns a legal move.

### Zobrist / TT
- Same position reached by different move orders gives the same key (transposition).
- Key matches `chess.polyglot.zobrist_hash` when using the same random table, or incremental key equals full recomputation.
- Replacement keeps deeper entries; stale entries do not corrupt results; mate scores are ply-adjusted.

### ML
- Encoding shape and values are correct.
- Model forward pass returns a scalar per position.
- Neural evaluator plugs into search and returns legal moves.
- Training runs a few steps and loss decreases on a tiny dataset.

### Integration
- Engine plays a full game vs a random mover without illegal moves or crashes.
- CLI handles invalid input gracefully.

## Conventions

- Use FEN strings for positions; keep puzzle positions in `tests/fixtures/`.
- Seed all randomness.
- Mark slow tests with `@pytest.mark.slow`; run them in CI nightly or manually.
- Target 80%+ coverage on `search/` and `evaluation/`.

## CI (GitHub Actions)

On every push and pull request: install dependencies, run `ruff`/`flake8`, run `pytest -m "not slow"`, upload coverage.

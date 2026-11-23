# Phase 0 — Foundations (Week 1)

Goal: a clean, tested base, plus the theory you need before writing any search code.
Time: about 8–12 hours in total.

## 1. What to learn (in this order)

| # | Topic | Why it matters | Time |
|---|-------|----------------|------|
| 1 | **Chess rules that break naive code**: castling rights, en passant, promotion, check, stalemate, threefold repetition, 50-move rule, insufficient material | A wrong rule makes every later result wrong | 1h |
| 2 | **FEN** (position string) and **PGN** (game record) | Every test, benchmark and tool uses them | 1h |
| 3 | **python-chess API**: `Board`, `legal_moves`, `push`/`pop`, `is_checkmate`, `outcome`, `chess.polyglot` | You will use it in every phase | 1h |
| 4 | **Game trees**: nodes, plies, branching factor b, depth d, size ~ b^d (chess b is about 35) | Explains why brute force fails and why pruning exists | 1h |
| 5 | **Zero-sum games** and the idea of minimax (preview only; you implement it in Phase 1) | Sets up Phase 1 | 1h |
| 6 | **Perft**: what it is and why engine authors use it | Your first correctness test | 30m |
| 7 | **Project hygiene**: virtualenv, pytest, ruff, mypy, GitHub Actions | Research-grade means reproducible | 1h |

## 2. What to do (step by step)

1. Create the GitHub repo `chess-ai-engine` and push this folder.
2. Set up the environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate          # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Read `src/chess_ai/perft.py` and `tests/test_perft.py` line by line. Make sure you can explain every line.
4. Run the tests and the perft tool:
   ```bash
   pytest                              # fast tests
   pytest -m slow                      # deeper perft (about a minute)
   python -m chess_ai.perft --depth 4
   python -m chess_ai.perft --depth 3 --divide
   ```
5. Run the linters: `ruff check src tests` and `mypy src`.
6. Push to GitHub and confirm the CI badge turns green.
7. Write the theory notes below in your own words. Do not copy.
8. Play with python-chess in a Python shell for 30 minutes: make moves, check game-end states, print boards.

## 3. Questions to answer in your own words (your Phase 0 notes)

1. Why is the chess game tree too big to search completely? Compute roughly 35^6 and 35^10.
2. What does a *ply* mean, and how is it different from a *move*?
3. What is perft, and why does a matching count prove move generation is right?
4. What is a zero-sum game? Why can one score represent both players?
5. In your own words, what does minimax assume about the opponent?
6. List 3 chess rules that are easy to implement wrongly, and how perft would reveal each.
7. What is FEN? Write the FEN for the start position and decode each field.

Write your answers below this line.

---

## 4. Exit checklist

- [ ] CI is green on GitHub
- [ ] `pytest` passes, `pytest -m slow` passes
- [ ] You can run `python -m chess_ai.perft --depth 4` and explain the output
- [ ] Questions above answered in this file
- [ ] You can explain minimax in 2 minutes without notes

## 5. Reading

- Chess Programming Wiki: Perft, Perft Results, Forsyth-Edwards Notation, Minimax
- python-chess documentation: Core, Polyglot
- Russell and Norvig, *AIMA*, Chapter on adversarial search (read the minimax part only)

## 6. Log

| Date | What I did | Problems / surprises |
|------|-----------|----------------------|
| | | |

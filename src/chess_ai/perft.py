"""Perft: count the leaf nodes of the legal-move tree to a fixed depth.

Perft results for standard positions are published and exact, so a match proves
that move generation and board updates are correct. Every later phase relies on
this, because a search on top of a wrong board is meaningless.

Run:  python -m chess_ai.perft --depth 4
      python -m chess_ai.perft --depth 3 --divide --fen "<FEN>"
"""

from __future__ import annotations

import argparse
import time

import chess


def perft(board: chess.Board, depth: int) -> int:
    """Number of leaf nodes reachable from `board` in exactly `depth` plies."""
    if depth == 0:
        return 1
    if depth == 1:
        # Bulk counting: no need to push each move just to count it.
        return board.legal_moves.count()
    nodes = 0
    for move in board.legal_moves:
        board.push(move)
        nodes += perft(board, depth - 1)
        board.pop()
    return nodes


def divide(board: chess.Board, depth: int) -> dict[str, int]:
    """Perft split by root move. Useful to locate a bug by comparing with a reference engine."""
    result: dict[str, int] = {}
    for move in board.legal_moves:
        board.push(move)
        result[move.uci()] = perft(board, depth - 1)
        board.pop()
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Count legal-move tree leaves (perft).")
    parser.add_argument("--fen", default=chess.STARTING_FEN, help="FEN (default: start position)")
    parser.add_argument("--depth", type=int, default=4)
    parser.add_argument("--divide", action="store_true", help="Show counts per root move")
    args = parser.parse_args()

    board = chess.Board(args.fen)
    start = time.perf_counter()
    if args.divide:
        counts = divide(board, args.depth)
        for uci, n in sorted(counts.items()):
            print(f"{uci}: {n}")
        total = sum(counts.values())
    else:
        total = perft(board, args.depth)
    elapsed = time.perf_counter() - start
    print(f"nodes: {total}  time: {elapsed:.2f}s  nps: {total / max(elapsed, 1e-9):,.0f}")


if __name__ == "__main__":
    main()

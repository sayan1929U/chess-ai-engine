"""Plain Minimax: the baseline every optimisation is compared against.

Phase 1. See docs/notes/phase1.md.

No pruning, no ordering, no cleverness. White maximises, Black minimises, and every
leg of the tree is visited. Keep this file unchanged forever: Alpha-Beta must return
the same score with far fewer nodes, and this is the proof.
"""

from __future__ import annotations

import time

import chess

from chess_ai.evaluation.base import Evaluator
from chess_ai.search.terminal import has_legal_move, is_draw, mated_score
from chess_ai.types import INF, SearchResult


class _Minimax:
    def __init__(self, evaluator: Evaluator) -> None:
        self.evaluator = evaluator
        self.nodes = 0

    def value(self, board: chess.Board, depth: int, ply: int) -> int:
        """Score from WHITE's perspective (positive = good for White)."""
        self.nodes += 1
        white_to_move = board.turn == chess.WHITE

        if depth == 0:
            if not has_legal_move(board):
                return self._terminal(board, ply, white_to_move)
            if is_draw(board):
                return 0
            score = self.evaluator.evaluate(board)
            return score if white_to_move else -score

        moves = list(board.legal_moves)
        if not moves:
            return self._terminal(board, ply, white_to_move)
        if is_draw(board):
            return 0

        best = -INF if white_to_move else INF
        for move in moves:
            board.push(move)
            score = self.value(board, depth - 1, ply + 1)
            board.pop()
            best = max(best, score) if white_to_move else min(best, score)
        return best

    @staticmethod
    def _terminal(board: chess.Board, ply: int, white_to_move: bool) -> int:
        if not board.is_check():
            return 0  # stalemate
        mated = mated_score(ply)  # negative for the side that is mated
        return mated if white_to_move else -mated


def minimax(board: chess.Board, depth: int, evaluator: Evaluator) -> SearchResult:
    """Full-width Minimax to a fixed depth. Score is from the side-to-move perspective."""
    if depth < 1:
        raise ValueError("depth must be at least 1")
    start = time.perf_counter()
    searcher = _Minimax(evaluator)
    white_to_move = board.turn == chess.WHITE

    moves = list(board.legal_moves)
    if not moves:
        score = searcher._terminal(board, 0, white_to_move)
        score = score if white_to_move else -score
        return SearchResult(None, score, depth, 1, time.perf_counter() - start)

    best_move = moves[0]
    best = -INF if white_to_move else INF
    for move in moves:
        board.push(move)
        score = searcher.value(board, depth - 1, 1)
        board.pop()
        if (white_to_move and score > best) or (not white_to_move and score < best):
            best, best_move = score, move

    side_score = best if white_to_move else -best
    return SearchResult(
        best_move, side_score, depth, searcher.nodes + 1, time.perf_counter() - start, [best_move]
    )

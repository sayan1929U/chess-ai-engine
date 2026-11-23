"""Game-end rules shared by every searcher, so Minimax and Alpha-Beta agree exactly.

Phase 1. See docs/notes/phase1.md.

Mate scores include the distance from the root: being mated at ply 3 scores
-(MATE - 3). A mate that arrives sooner is therefore worth more to the side
delivering it, and a mate that arrives later is worth less to the side suffering it.
"""

from __future__ import annotations

import chess

from chess_ai.types import MATE


def mated_score(ply: int) -> int:
    """Score for the side to move when it is checkmated `ply` plies from the root."""
    return -(MATE - ply)


def has_legal_move(board: chess.Board) -> bool:
    return any(board.legal_moves)


def is_draw(board: chess.Board) -> bool:
    """Draws the search treats as final. Checkmate must be tested before calling this."""
    return (
        board.is_insufficient_material()
        or board.halfmove_clock >= 100  # fifty-move rule
        or board.is_repetition(2)  # a repeated position inside the search is scored as a draw
    )

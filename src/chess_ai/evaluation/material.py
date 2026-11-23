"""Material-only evaluation in centipawns.

Phase 1. See docs/notes/phase1.md.

100 centipawns = one pawn. Knights and bishops are worth slightly more than three
pawns, a convention that comes from decades of engine tuning. The king has no value
here because both sides always have exactly one.
"""

from __future__ import annotations

import chess

PIECE_VALUES: dict[chess.PieceType, int] = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
}


class MaterialEvaluator:
    def evaluate(self, board: chess.Board) -> int:
        """White material minus Black material, from the side-to-move perspective."""
        score = 0
        for piece_type, value in PIECE_VALUES.items():
            white = chess.popcount(board.pieces_mask(piece_type, chess.WHITE))
            black = chess.popcount(board.pieces_mask(piece_type, chess.BLACK))
            score += value * (white - black)
        return score if board.turn == chess.WHITE else -score

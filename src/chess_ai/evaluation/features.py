"""Hand-crafted features: king safety, pawn structure, mobility, piece bonuses.

Phase 4. See docs/notes/phase4.md.
"""

import chess


def king_safety(board: chess.Board, color: chess.Color) -> int:
    raise NotImplementedError("Phase 4")


def pawn_structure(board: chess.Board, color: chess.Color) -> int:
    raise NotImplementedError("Phase 4")


def mobility(board: chess.Board, color: chess.Color) -> int:
    raise NotImplementedError("Phase 4")

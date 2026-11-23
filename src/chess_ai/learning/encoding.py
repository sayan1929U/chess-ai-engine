"""Board to tensor: 12 piece planes plus side, castling, en passant.

Phase 6. See docs/notes/phase6.md.
"""

import chess


def encode_board(board: chess.Board) -> list[list[list[float]]]:
    """Return a 12x8x8 nested list (convert to a torch tensor in the dataset code)."""
    raise NotImplementedError("Phase 6")

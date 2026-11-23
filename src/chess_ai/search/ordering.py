"""Move ordering: TT move, MVV-LVA captures, promotions, checks, killers, history.

Phase 2. See docs/notes/phase2.md.
"""

from __future__ import annotations

import chess


def order_moves(board: chess.Board, tt_move: chess.Move | None = None) -> list[chess.Move]:
    """Best-looking moves first, so alpha-beta cuts off earlier."""
    raise NotImplementedError("Phase 2")

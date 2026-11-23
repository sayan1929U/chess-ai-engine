"""Principal Variation Search with aspiration windows, null-move, LMR, futility.

Phase 3. See docs/notes/phase3.md.
"""

from __future__ import annotations

import chess

from chess_ai.types import SearchConfig, SearchResult


def pvs(board: chess.Board, config: SearchConfig) -> SearchResult:
    raise NotImplementedError("Phase 3")

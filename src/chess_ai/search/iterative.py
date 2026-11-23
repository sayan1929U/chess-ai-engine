"""Iterative deepening with time management and principal-variation tracking.

Phase 2. See docs/notes/phase2.md.
"""

from __future__ import annotations

import chess

from chess_ai.types import SearchConfig, SearchResult


def iterative_deepening(board: chess.Board, config: SearchConfig) -> SearchResult:
    """Search depth 1, 2, 3 ... until time or max depth; always return the last finished depth."""
    raise NotImplementedError("Phase 2")

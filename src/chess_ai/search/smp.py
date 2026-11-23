"""Lazy SMP: several workers search the same root with a shared table.

Phase 5. See docs/notes/phase5.md.
"""

from __future__ import annotations

import chess

from chess_ai.types import SearchConfig, SearchResult


def smp_search(board: chess.Board, config: SearchConfig) -> SearchResult:
    raise NotImplementedError("Phase 5")

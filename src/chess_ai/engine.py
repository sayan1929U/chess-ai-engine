"""Public Engine facade: config in, SearchResult out.

Phase 1. See docs/notes/phase1.md.
"""

from __future__ import annotations

import chess

from chess_ai.types import SearchConfig, SearchResult


class Engine:
    """Single entry point used by the CLI, UCI adapter, GUI, benchmarks and tests."""

    def __init__(self, config: SearchConfig | None = None) -> None:
        self.config = config or SearchConfig()

    def search(self, board: chess.Board) -> SearchResult:
        """Pick the searcher and evaluator named in `self.config` and run it."""
        raise NotImplementedError("Phase 1")

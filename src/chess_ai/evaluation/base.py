"""Evaluator interface: every evaluator (material, PST, tuned, neural) implements this.

Phase 1. See docs/notes/phase1.md.
"""

from __future__ import annotations

from typing import Protocol

import chess


class Evaluator(Protocol):
    def evaluate(self, board: chess.Board) -> int:
        """Centipawns from the side-to-move perspective (positive = good for side to move)."""
        ...

"""Negamax with Alpha-Beta pruning and mate-distance scoring.

Phase 1. See docs/notes/phase1.md.
"""

from __future__ import annotations

import chess

from chess_ai.evaluation.base import Evaluator
from chess_ai.types import SearchResult


def negamax(board: chess.Board, depth: int, evaluator: Evaluator) -> SearchResult:
    """score = -negamax(child); prune when alpha >= beta."""
    raise NotImplementedError("Phase 1")

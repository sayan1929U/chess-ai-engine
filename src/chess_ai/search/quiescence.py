"""Quiescence search: resolve captures before evaluating (fixes the horizon effect).

Phase 2. See docs/notes/phase2.md.
"""

from __future__ import annotations

import chess

from chess_ai.evaluation.base import Evaluator


def quiescence(board: chess.Board, alpha: int, beta: int, evaluator: Evaluator) -> int:
    raise NotImplementedError("Phase 2")

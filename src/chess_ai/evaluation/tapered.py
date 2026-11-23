"""Tapered evaluation: blend middlegame and endgame scores by game phase.

Phase 4. See docs/notes/phase4.md.
"""

import chess


class TaperedEvaluator:
    def evaluate(self, board: chess.Board) -> int:
        raise NotImplementedError("Phase 4")

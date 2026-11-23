"""Material plus piece-square tables.

Phase 2. See docs/notes/phase2.md.
"""

import chess


class PSTEvaluator:
    def evaluate(self, board: chess.Board) -> int:
        raise NotImplementedError("Phase 2")

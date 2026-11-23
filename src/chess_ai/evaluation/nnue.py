"""NNUE-style evaluator: sparse features with an incrementally updated accumulator.

Phase 6. See docs/notes/phase6.md.
"""

import chess


class NNUEEvaluator:
    def evaluate(self, board: chess.Board) -> int:
        raise NotImplementedError("Phase 6")

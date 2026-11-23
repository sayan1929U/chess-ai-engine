"""Evaluator backed by a PyTorch value network.

Phase 6. See docs/notes/phase6.md.
"""

import chess


class NeuralEvaluator:
    def __init__(self, weights_path: str) -> None:
        self.weights_path = weights_path

    def evaluate(self, board: chess.Board) -> int:
        raise NotImplementedError("Phase 6")

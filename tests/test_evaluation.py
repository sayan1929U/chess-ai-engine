"""Material evaluation (Phase 1)."""

import chess

from chess_ai.evaluation.material import MaterialEvaluator

ev = MaterialEvaluator()


def test_start_position_is_equal() -> None:
    assert ev.evaluate(chess.Board()) == 0


def test_mirror_gives_same_score() -> None:
    # mirror() swaps colours AND the side to move, so the side-to-move score is unchanged
    board = chess.Board("rnb1kbnr/pppp1ppp/8/4p3/4P2q/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3")
    assert ev.evaluate(board) == ev.evaluate(board.mirror())


def test_score_flips_with_side_to_move() -> None:
    board = chess.Board()
    board.remove_piece_at(chess.D1)  # White loses its queen
    assert ev.evaluate(board) == -900  # White to move
    board.turn = chess.BLACK
    assert ev.evaluate(board) == 900


def test_queen_worth_more_than_pawn() -> None:
    queen_up = chess.Board("4k3/8/8/8/8/8/8/3QK3 w - - 0 1")
    pawn_up = chess.Board("4k3/8/8/8/8/8/4P3/4K3 w - - 0 1")
    assert ev.evaluate(queen_up) > ev.evaluate(pawn_up) > 0

"""Game-end helpers (Phase 1)."""

import chess

from chess_ai.search.terminal import has_legal_move, is_draw, mated_score
from chess_ai.types import MATE

STALEMATE = "7k/5Q2/6K1/8/8/8/8/8 b - - 0 1"
KK = "8/8/4k3/8/8/3K4/8/8 w - - 0 1"


def test_mated_score_prefers_later_mate_for_the_loser() -> None:
    assert mated_score(0) == -MATE
    assert mated_score(3) == -(MATE - 3)
    assert mated_score(3) > mated_score(1)  # being mated later is less bad


def test_has_legal_move() -> None:
    assert has_legal_move(chess.Board())
    assert not has_legal_move(chess.Board(STALEMATE))


def test_insufficient_material_is_draw() -> None:
    assert is_draw(chess.Board(KK))


def test_fifty_move_rule_is_draw() -> None:
    assert is_draw(chess.Board("8/8/4k3/8/8/3K4/R7/8 w - - 100 80"))


def test_repetition_is_draw() -> None:
    board = chess.Board()
    for uci in ["g1f3", "g8f6", "f3g1", "f6g8"]:
        board.push_uci(uci)
    assert is_draw(board)


def test_normal_position_is_not_draw() -> None:
    assert not is_draw(chess.Board())

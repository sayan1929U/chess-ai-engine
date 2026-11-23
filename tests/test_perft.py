"""Perft correctness tests. Expected values are the standard published perft counts
(see the Chess Programming Wiki, "Perft Results")."""

import chess
import pytest

from chess_ai.perft import divide, perft

START = chess.STARTING_FEN
KIWIPETE = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
POSITION_3 = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1"
POSITION_4 = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"
POSITION_5 = "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8"
POSITION_6 = "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10"

FAST = [
    (START, 1, 20),
    (START, 2, 400),
    (START, 3, 8902),
    (START, 4, 197281),
    (KIWIPETE, 1, 48),
    (KIWIPETE, 2, 2039),
    (KIWIPETE, 3, 97862),
    (POSITION_3, 1, 14),
    (POSITION_3, 2, 191),
    (POSITION_3, 3, 2812),
    (POSITION_3, 4, 43238),
    (POSITION_4, 1, 6),
    (POSITION_4, 2, 264),
    (POSITION_4, 3, 9467),
    (POSITION_5, 1, 44),
    (POSITION_5, 2, 1486),
    (POSITION_5, 3, 62379),
    (POSITION_6, 1, 46),
    (POSITION_6, 2, 2079),
    (POSITION_6, 3, 89890),
]

SLOW = [
    (START, 5, 4865609),
    (KIWIPETE, 4, 4085603),
    (POSITION_3, 5, 674624),
    (POSITION_4, 4, 422333),
    (POSITION_5, 4, 2103487),
]


@pytest.mark.parametrize("fen,depth,expected", FAST)
def test_perft_fast(fen: str, depth: int, expected: int) -> None:
    assert perft(chess.Board(fen), depth) == expected


@pytest.mark.slow
@pytest.mark.parametrize("fen,depth,expected", SLOW)
def test_perft_slow(fen: str, depth: int, expected: int) -> None:
    assert perft(chess.Board(fen), depth) == expected


def test_perft_depth_zero_is_one() -> None:
    assert perft(chess.Board(), 0) == 1


def test_divide_sums_to_perft() -> None:
    board = chess.Board(KIWIPETE)
    assert sum(divide(board, 2).values()) == perft(board, 2)


def test_perft_restores_board() -> None:
    board = chess.Board(KIWIPETE)
    fen_before = board.fen()
    perft(board, 3)
    assert board.fen() == fen_before

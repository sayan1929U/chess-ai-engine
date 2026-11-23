"""Plain Minimax (Phase 1)."""

import chess
import pytest

from chess_ai.evaluation.material import MaterialEvaluator
from chess_ai.search.minimax import minimax
from chess_ai.types import MATE

ev = MaterialEvaluator()
CHECKMATED = "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3"  # fool's mate
STALEMATE = "7k/5Q2/6K1/8/8/8/8/8 b - - 0 1"


def test_node_counts_match_the_game_tree() -> None:
    # 1 root + 20 moves = 21; + 400 replies = 421; + 8902 = 9323
    assert minimax(chess.Board(), 1, ev).nodes == 21
    assert minimax(chess.Board(), 2, ev).nodes == 421
    assert minimax(chess.Board(), 3, ev).nodes == 9323


def test_returns_a_legal_move() -> None:
    board = chess.Board()
    assert minimax(board, 2, ev).best_move in board.legal_moves


def test_mate_in_1_for_white() -> None:
    result = minimax(chess.Board("6k1/5ppp/8/8/8/8/8/R3K3 w - - 0 1"), 2, ev)
    assert result.best_move == chess.Move.from_uci("a1a8")
    assert result.score == MATE - 1


def test_mate_in_1_for_black() -> None:
    fen = "rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq - 0 2"
    result = minimax(chess.Board(fen), 2, ev)
    assert result.best_move == chess.Move.from_uci("d8h4")
    assert result.score == MATE - 1


def test_captures_hanging_queen() -> None:
    fen = "rnb1kbnr/pppp1ppp/8/4p3/4P2q/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
    result = minimax(chess.Board(fen), 2, ev)
    assert result.best_move == chess.Move.from_uci("f3h4")
    assert result.score == 900


def test_checkmated_root() -> None:
    result = minimax(chess.Board(CHECKMATED), 2, ev)
    assert result.best_move is None
    assert result.score == -MATE


def test_stalemate_root() -> None:
    result = minimax(chess.Board(STALEMATE), 2, ev)
    assert result.best_move is None
    assert result.score == 0


def test_restores_board() -> None:
    board = chess.Board()
    minimax(board, 3, ev)
    assert board.fen() == chess.STARTING_FEN


def test_invalid_depth_rejected() -> None:
    with pytest.raises(ValueError):
        minimax(chess.Board(), 0, ev)

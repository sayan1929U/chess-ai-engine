"""Shared data types: search configuration, search result, score constants.

Phase 1. See docs/notes/phase1.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import chess

INF = 1_000_000
MATE = 100_000  # mate score; "mate in n plies" is MATE - n, so faster mates score higher
MATE_BOUND = MATE - 1_000  # any |score| above this is a forced mate


@dataclass
class SearchConfig:
    """Every optimisation has an on/off flag so ablations are one line."""

    max_depth: int = 4
    time_limit: float | None = None  # seconds per move
    evaluator: str = "material"  # material | pst | tapered | neural | nnue
    search: str = "negamax"  # minimax | negamax | pvs | mcts
    use_tt: bool = False
    tt_size_mb: int = 64
    use_ordering: bool = False
    use_quiescence: bool = False
    use_iterative_deepening: bool = False
    threads: int = 1
    seed: int = 0


@dataclass
class SearchResult:
    best_move: chess.Move | None
    score: int  # centipawns, side-to-move perspective
    depth: int
    nodes: int
    time: float
    pv: list[chess.Move] = field(default_factory=list)

    @property
    def nps(self) -> float:
        return self.nodes / self.time if self.time > 0 else 0.0

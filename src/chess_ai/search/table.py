"""Transposition table: EXACT / LOWER / UPPER bounds, depth-preferred replacement.

Phase 2. See docs/notes/phase2.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

import chess


class Bound(IntEnum):
    EXACT = 0
    LOWER = 1
    UPPER = 2


@dataclass
class TTEntry:
    key: int
    depth: int
    score: int
    bound: Bound
    best_move: chess.Move | None
    age: int = 0


class TranspositionTable:
    def __init__(self, size_mb: int = 64) -> None:
        self.size_mb = size_mb

    def probe(self, key: int) -> TTEntry | None:
        raise NotImplementedError("Phase 2")

    def store(self, entry: TTEntry) -> None:
        raise NotImplementedError("Phase 2")

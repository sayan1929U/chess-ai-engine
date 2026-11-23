"""Zobrist hashing: 64-bit position keys. Verify against chess.polyglot.zobrist_hash.

Phase 2. See docs/notes/phase2.md.
"""

import chess


def zobrist_key(board: chess.Board) -> int:
    raise NotImplementedError("Phase 2")

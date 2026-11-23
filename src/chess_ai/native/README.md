# native/ (Phase 5)

Hot paths moved out of pure Python. Pick ONE after profiling:

- **Numba**: JIT-compile evaluation and move-ordering kernels (fastest to try).
- **C++ + pybind11** or **Rust + PyO3**: bitboard move generation and search core (largest speedup).

Rule: the native core must return identical search results to the Python version at fixed depth.

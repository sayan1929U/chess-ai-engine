# Texel tuning (Phase 4)

Model: P(win) = 1 / (1 + 10^(-K * eval / 400)). Minimise mean squared error vs game results.
Use a validation split from different games to avoid overfitting.

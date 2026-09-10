# Evidence and Robustness

## Frozen development period

The development window runs from 2023-07-01 through 2025-12-31 UTC. Signals,
positions, and data hashes were frozen before the terminal evaluation.

| One-way cost plus historical realized funding | Total return | CAGR | Sharpe | Maximum drawdown |
|---|---:|---:|---:|---:|
| 7 bps | +64.83% | 22.08% | 1.62 | -15.33% |
| 14 bps | +53.86% | 18.77% | 1.37 | -17.67% |
| 28 bps | +31.93% | 11.70% | 0.85 | -23.62% |

The cost comparison reprices the frozen position path. It does not rerun the
signal or sizing process under each cost assumption.

## Time and concentration checks

- 20 of 30 calendar months were profitable.
- 6 of 10 calendar quarters were profitable.
- Partial 2023 returned +31.73%; 2024 returned +32.08%; 2025 returned -5.27%.
- 66.47% of rolling 90-day windows were positive at the 7 bps baseline.
- Maximum profitable-pair concentration was 2.36%, measured as the largest
  positive pair P&L divided by total positive pair P&L.
- Realized volatility at 7 bps was 12.80%.
- Frozen-path one-way cost break-even was approximately 48.38 bps.

## Dependence on strong observations

- Removing the best day leaves 20.31% CAGR and 1.55 Sharpe.
- Removing the best three days leaves 17.80% CAGR and 1.40 Sharpe.
- A 2,000-sample moving-block bootstrap used five-day blocks.
- The bootstrap was cumulatively positive in 99.45% of samples.
- The 95% intervals were 4.22%–41.80% for CAGR and 0.39–2.81 for Sharpe.
- An approximate 18-trial deflated-Sharpe probability was 82.65%.

These checks do not convert development evidence into prospective evidence.
The wide intervals, weaker 2025 path, and sensitivity to strong days remain
part of the interpretation.

## Candidate-selection boundary

The development candidate was frozen under reviewed practical thresholds
before the terminal evaluation. It did not meet every earlier aspirational
performance gate; the original experiment manifest remains unchanged and
records that outcome. Terminal results were not used to revise the candidate.

## Correctness checks

The frozen run passed pair-to-symbol-to-portfolio reconciliation, independent
SQL metric recalculation, pair/symbol/total exposure, average gross, pair-count,
and pair-overlap checks. The private implementation currently has 40 passing
automated tests.

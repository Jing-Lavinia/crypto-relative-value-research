# Locked Terminal Evaluation

## Evaluation contract

The terminal period runs from 2026-01-01 through 2026-06-30 UTC. It had been
observed during earlier exploratory work, so it is not described as a pristine
holdout. The frozen research state was evaluated once, the evaluation lock was
consumed, and no parameters were changed afterward.

## Results

| One-way cost plus historical realized funding | Total return | Descriptive annualized return | Sharpe | Maximum drawdown |
|---|---:|---:|---:|---:|
| 7 bps | +4.12% | 8.49% | 0.65 | -6.98% |
| 14 bps | +2.73% | 5.59% | 0.46 | -7.36% |
| 28 bps | -0.047% | -0.09% | 0.06 | -8.13% |

Four of six months were positive. Q1 returned -2.08% and Q2 returned +6.34%.
The baseline positive rolling 90-day fraction was 74.67%. The annualized
figures are descriptive because the evaluation covers only six months.

## Baseline attribution

On $1 million initial capital:

| Component | Additive P&L |
|---|---:|
| Market P&L | +$1,446.69 |
| Funding P&L | +$53,668.56 |
| Trading costs | -$13,895.44 |
| Net P&L | +$41,219.81 |

The additive dollar attribution reconciles to the final ledger. The +4.12%
portfolio result is the compounded return and is not presented as an additive
component.

No mean-reversion pair traded in the terminal period. The positive portfolio
result therefore supports continued monitoring of the active funding-carry
sleeve but does not independently validate mean reversion. The 28 bps path was
approximately $467 below break-even per $1 million initial capital.

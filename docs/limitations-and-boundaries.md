# Limitations and Boundaries

## Evidence boundaries

- All reported results are simulated rather than live performance.
- The development period was used for research decisions.
- The terminal period is locked but was observed during earlier exploratory
  work; it is not a pristine holdout.
- The terminal portfolio result was dominated by funding, and the
  mean-reversion sleeve had no terminal trades.
- Funding regimes, exchange rules, and the available contract set can change.

## Execution boundaries

Historical hourly bars cannot reproduce queue position, intrabar market impact,
exchange outages, every liquidation-engine detail, or production capacity.
Linear 7, 14, and 28 bps scenarios are sensitivity tests, not capacity claims.

## Public implementation boundary

The executable package in this repository uses synthetic data and simplified
signal inputs. Private relationship features, thresholds, sizing parameters,
raw data, configurations, and empirical run artifacts are not included. The
public package did not generate the performance reported in the README.

## Supported conclusions

The evidence supports a frozen research candidate with positive development
and baseline terminal portfolio results, exact accounting, and explicit
market-mechanics controls. It does not establish live profitability, capacity,
future performance, or terminal validation of an inactive mean-reversion
sleeve.


# System Design

## Data contract

The private research system consumes hourly Binance USD-M perpetual kline,
mark-price, and funding archives. Each accepted object is tied to its official
object key, published checksum, local checksum, size, and processing record.
Duplicate timestamp-symbol keys, invalid OHLC rows, null fields, and
insufficient active source coverage are rejected before research begins.

The frozen data state contains 26,051 verified objects and 11,496,302 accepted
hourly kline rows. Historical eligibility is recalculated at 157 weekly refits.
Each refit selects 20 contracts from information available at that timestamp;
the historical union contains 150 contracts.

## Decision clock

```text
data ending before the weekly refit
  → eligibility and relationship review
  → state observed at close t
  → target holdings formed
  → lifecycle and market-availability checks
  → first eligible open strictly after t
  → funding and subsequent market P&L
```

A future data append must not change an earlier universe, relationship state,
or funding ranking. The public package includes this timing contract without
the private signal definitions.

## Research sleeves

### Sparse mean reversion

The private selection process uses past observations for PCA representation,
DBSCAN grouping, Engle–Granger relationship tests, false-discovery-rate
control, stability and half-life screens, and a past-only Kalman hedge state.
Public documentation names the method classes but omits feature definitions,
lags, thresholds, acceptance rules, and parameter values.

### Cross-sectional funding carry

The carry sleeve ranks the eligible contract set using funding observations
known by the decision time. It builds relative long/short positions between
lower- and higher-funding contracts. It is not a spot-perpetual cash-and-carry
trade and not a risk-free arbitrage claim.

## Portfolio controls

Both sleeves enter a shared portfolio engine. Controls cover pair gross,
symbol gross, total gross, maximum active pairs, maximum pair overlap per
symbol, position-aware Ledoit–Wolf covariance risk, maintenance margin, and a
liquidation buffer. Scaling preserves pair hedge proportions. Covariance
lookbacks, targets, and sizing parameters remain private.

## Lifecycle and execution

Listing age and data availability determine historical entry into the eligible
set. Known delisting events prevent new exposure and produce a controlled exit.
If either pair leg has no executable volume at the next open, the whole pair
carries its previous position.

## Accounting lineage

```text
sleeve → pair → contract leg → symbol → portfolio
```

Each leg records position notional, market P&L, funding P&L, traded notional,
trading cost, and net P&L. Pair legs are aggregated once to symbols; symbols
are aggregated once to the portfolio. Independent reconciliation and metric
paths must agree before evidence is eligible for promotion.

## Research-state controls

Run directories are immutable, configurations and input states are hashed, and
promotion recomputes the required checks. The locked terminal evaluation can
be consumed once and cannot be used for later parameter selection.

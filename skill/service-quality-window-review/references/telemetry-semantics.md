# Format semantics and the example's stronger contract

Official documentation consulted on 2026-10-02:

- [Prometheus metric types](https://prometheus.io/docs/concepts/metric_types/#histogram): classic histograms expose cumulative upper-inclusive `le` buckets, a count matching `+Inf`, and a sum; counters accumulate and may reset. A classic histogram's component series can be transferred separately. This does not promise an atomic, exactly boundary-aligned application snapshot.
- [Prometheus histograms and summaries](https://prometheus.io/docs/practices/histograms/): aggregate compatible observation populations before deriving a percentile. A threshold coinciding with an available bucket boundary supports a direct count fraction. Per-instance summary quantiles cannot generally be pooled into a service quantile.
- [Prometheus query functions](https://prometheus.io/docs/prometheus/latest/querying/functions/#increase): `increase` adjusts observed resets and extrapolates over the query interval. [`histogram_quantile`](https://prometheus.io/docs/prometheus/latest/querying/functions/#histogram_quantile) interpolates within classic buckets and has special behavior for the final open-ended bucket. Those returned values are not exact empirical quantiles recovered from raw samples.
- [OpenTelemetry metric data model](https://opentelemetry.io/docs/specs/otel/metrics/data-model/#histogram): histogram temporality may be delta or cumulative over time; explicit bucket counts describe separate value intervals, with upper-inclusive/lower-exclusive finite boundaries. Metric-point time intervals use `(start, end]`. Temporality is distinct from whether buckets accumulate across boundaries. Preserve start timestamps, gaps, attributes and units when converting.

The fixture is an original fictional JSON export, `quality-window-v1`. It is neither Prometheus exposition text nor an OTLP payload. Its `cumulative_le` values borrow classic histogram bucket arithmetic. Its named epochs, atomic `before` snapshots, `[start, end)` selection, request taxonomy, complete-observation attestations and target policy are explicit fictional producer contracts, not guarantees inherited from either system above. The calculator deliberately accepts only this small representation.

In this fixture, a snapshot at `t` contains terminal observations with event time strictly less than `t` since the stated epoch. Thus `snapshot(end) - snapshot(start)` represents `[start, end)` only where the producer's continuity assertion is present and epochs agree. Ordinary scrapes rarely establish this exact boundary contract by themselves.

The fixture supplies cumulative counts across time and cumulative counts across latency upper bounds. First difference compatible snapshots over time. The resulting interval vector still accumulates across bounds. To obtain disjoint latency bins, difference neighboring bucket counts within that vector. Adding the cumulative bucket values together would count observations repeatedly.

For finite nonnegative durations with bounds `0.1, 0.3, 1, +Inf` seconds, the disjoint bins are `[0, 0.1]`, `(0.1, 0.3]`, `(0.3, 1]`, `(1, +Inf)`. A nearest-rank p95 in the last bin is strictly greater than 1 second with no finite upper bound. It is not an exact p95 of 1 second, even if a query system's special-case estimator returns that value.

## Executed example checks

The original calculation was executed with Python 3.12.14 on 2026-10-02 and reproduced byte-for-byte. Independent readback checked the interval arithmetic, separate attempt/logical denominators, coverage and quantile ranks against the supplied source. Changed-input checks covered identity conflicts, reset continuity, observation gaps, incompatible histogram populations/units/buckets, zero observations and target changes. Invalid diagnostic records leave independent metrics available. A missing or malformed histogram container leaves supported counts intact while limiting the latency population to usable intervals.

Two explicitly hypothetical gap completions yielded different whole-window decisions while leaving the original observed subset unchanged. They demonstrate why the original verdict is undetermined; they are not recovered traffic. All checks used local fictional data. No endpoint, monitoring, live producer assertion or production outcome was verified.

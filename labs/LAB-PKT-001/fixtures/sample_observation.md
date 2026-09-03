# Sample observation (fixture)

**Route:** B — supplied fixture (`ILLUSTRATIVE_FIXTURE`)  
**Honesty banner:** These rows are **not** the learner’s device measurements.

## Prediction

Expected failure family: **latency** (long waiting / TTFB feel) rather than hard reliability errors.

## Access network

Fixture labels access as **Wi-Fi** for run 1 and **cellular** for run 2. Wi-Fi ≠ Internet ≠ cellular ≠ cloud.

## Observation

- Fixture Ethernet ethertype `0x0800` (IPv4); IPv4 TTL equals **64**.
- Timing table shows larger `waiting_ttfb` on cellular condition than Wi-Fi condition.
- UI outcome still succeeds in both illustrative runs (reliability held; latency changed).

## Inference

- “Cloud-far placement” is marked **inference** in the path fixture—bars or icons alone do not prove region or tower congestion.
- Higher cellular TTFB *could* be access latency, radio conditions, or remote load; additional evidence would be required before a causal claim.

## Metric family judgment

Primary family for this stall story: **latency**. Throughput download ms stayed similar; no hard failure for reliability.

## Limits

Illustrative teaching data only. No published benchmark claim. `PHYSICAL_PENDING` for RF drive-test truths.

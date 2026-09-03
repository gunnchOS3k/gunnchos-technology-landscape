# Pathway extensions — LAB-TRUST-001

## Operator

Classify one failure symptom from Route C fixture or a live run as exactly one of:

- authn
- authz
- network
- model quality

Write the UX symptom you saw and why the other three are less likely (observation vs inference).

## Builder

Using `fixtures/sample_log_line.txt`, write one redaction rule and the safer log line. Synthetic tokens only.

## Engineer

Sketch trust boundaries crossed by Route C (device → browser → TLS → remote inference → logs/operators). Mark unknown hops.

## Researcher

State one hypothesis comparing Route L vs Route C privacy exposure, then name limitations: n=1, fixture bias, unknown OS telemetry.

## Educator

### No-device storyboard

Three panels: ask → wait → read answer. For each panel, ask learners what might be local vs remote.

### Misconception drill

True/false with repair sentence:

1. “The assistant knows the library’s server city.”  
2. “Signing in is the same as being allowed to delete training copies.”  
3. “If it works offline, nothing else on the phone can phone home.” (Answer: unknown without evidence.)

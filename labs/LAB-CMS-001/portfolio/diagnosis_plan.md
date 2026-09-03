# Diagnosis plan — LAB-CMS-001 (Engineer)

## Inspection order

1. Connectivity rule-out (icon / optional airplane mode for local-only action)  
2. CPU activity (before → during)  
3. Memory / RAM  
4. Disk / persistent storage activity  
5. Qualitative thermal / power mode (plugged vs battery; stop on warnings)

## Claim-upgrade criteria

| Tempting claim | Additional evidence required |
|---|---|
| CPU-bound root cause | Sustained CPU with low I/O wait; process-level attribution; repeatable timing |
| Memory thrashing | Page faults / swap use / severe RAM exhaustion—not a single memory rise |
| Storage bottleneck | Prolonged disk busy / wait coincident with hangs |
| Thermal throttle | Disclosed sensor or OS thermal event—not “felt warm” alone |
| Durable forever | Multiple save/reopen cycles + integrity checks; one success ≠ forever |

## Wall-clock optional

- Action definition:
- Condition A duration:
- Condition B duration:
- N (small):
- Confounders disclosed:

# Path diagram — LAB-PKT-001

Text-first diagram (required for accessibility):

```text
[Human action: sync/send]
        |
        v
[Device / local app] ---- observed UI cues
        |
        v
[Access network: Wi-Fi XOR cellular XOR unknown/fixture]
        |   (Wi-Fi ≠ Internet ≠ cellular)
        v
[LAN / gateway / NAT] ---- often inferred unless you administer it
        |
        +--> [DNS name resolution] ---- observe only with timing/resolver evidence
        |
        v
[Internet path]
        |
        v
[Service endpoint]
        |
        +--> placement hypothesis: edge-near OR cloud-far (INFERENCE without extra evidence)
```

Metric family for this run: latency / reliability / throughput (circle one).

Label each arrow **observed** or **inferred**.

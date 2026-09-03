# Route L fixture transcript — LAB-TRUST-001

**Label:** `FIXTURE` / `illustrative`  
**Route:** L (local / offline-capable simulator)  
**Network required (claimed):** N  
**Data leaving device (claimed):** N for prompt body; unknown for OS telemetry  
**Safety:** Synthetic teaching content only. No real secrets, private messages, precise location, or confidential data.

## Practical question (input / data)

> How can I tell whether a public library website is slow because of my phone or because of the site, without logging into any personal accounts?

## Simulated local path (data → model → inference)

1. **Data:** prompt text held in a local process buffer (fixture claim).
2. **Model:** tiny on-device rule table (`toy-local-rules-v0`), not a neural net and not a person.
3. **Inference:** deterministic template answer produced offline.

## Output (inference)

Try these checks on a public page you already open without signing in:

1. Reload once and note whether the address bar spinner stops before readable text appears.
2. Open the same public URL on a second network you control (for example phone hotspot vs home Wi-Fi) and compare wall time by feel—not as a lab benchmark.
3. If the page is still slow on both networks, the site or a shared upstream path is a better first guess than “only my phone.”

**Hedge (uncertainty):** This is a checklist, not a diagnosis. One slow load is not proof of a root cause.

## Authn / authz note (observation)

- **Authn:** not required for this public-page checklist.
- **Authz:** you are only observing a public page; do not attempt privileged admin actions.

## Consent/lifecycle hints visible in simulator UI (fixture)

- Audience: learner device only  
- Purpose: educational comparison  
- Retention: session buffer cleared on exit (claimed)  
- AI disclosure: “Simulated local inference — not a cloud model”

## Dual-ledger seed

- Human-trust feeling: “It felt private because nothing asked me to sign in.”  
- Technical-trust control: local process + no outbound HTTP in the simulator log.

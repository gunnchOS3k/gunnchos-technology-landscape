# LAB-PKT-001 — Trace One Connected Action Across Path and Access

**Chapter:** CE-4  
**Statuses:** `IMPLEMENTED_DIGITAL` | `FIXTURE_VALIDATED` | `PHYSICAL_PENDING` | `EXTERNAL_DEPENDENCY`  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

## Observable question

> When a connected action feels stuck, what parts of the path can I **observe** on a device I already own—and what must I treat as **inference**—including whether the issue looks like **latency**, **reliability**, or **throughput**, and whether **Wi-Fi**, **cellular**, or a **fixture** path was in play?

## Distinctions to practice

| Term | Keep distinct from |
|---|---|
| Device | LAN, Internet, cloud |
| LAN | Internet, Wi-Fi (Wi-Fi can *provide* LAN access) |
| Internet | Wi-Fi, cellular, cloud |
| DNS | connectivity; name lookup is a dependency, not “the network” |
| Service | path; the remote app may be edge-near or cloud-far |
| Wi-Fi | Internet, cellular |
| Cellular | Internet, Wi-Fi |
| Edge | cloud (placement hypothesis; needs evidence) |
| Cloud | Internet access network |
| Latency | throughput, reliability |
| Throughput | latency, reliability |
| Reliability | latency, throughput |

## Safety / privacy

See `PRIVACY_AND_SAFETY.md`. Short rules:

- Do **not** capture other users’ traffic.
- Do **not** store passwords, tokens, private payloads, or banking amounts.
- Prefer demo pages, public documentation URLs, or fixtures.
- On public Wi-Fi classrooms, prefer **Route B**.

## Accessibility

See `ACCESSIBILITY.md`. Fixture Route B is mandatory for learners without stable broadband or personal hotspots. Do not rely on color-only status icons.

## Time estimate

About 45–60 minutes for the baseline.

## Prediction

Before running, write which failure family you expect:

1. **Latency** — long wait / spinner / TTFB feel  
2. **Reliability** — retries, errors, “couldn’t reach”  
3. **Throughput** — long transfer / slow download of a larger body  

Also name access mode if known: Wi-Fi / cellular / unknown / fixture.

## Route A — Browser or CLI (live commodity)

**Status:** `IMPLEMENTED_DIGITAL` with `EXTERNAL_DEPENDENCY` when live DNS/Internet is used.

### A1 — Browser

1. Open `labs/LAB-PKT-001/browser/index.html` in a desktop browser.
2. Open developer tools Network (optional Resource Timing phases: DNS / connect / waiting / download).
3. Select access mode from the form (what your OS icons **show**—text label required, not color alone).
4. Click **Run fixture-timed sync demo** (always safe; no private payloads).
5. Optional: click **Fetch public documentation sample** only if policy allows; scrub screenshots.
6. Change **one** condition (Wi-Fi off→cellular, brief airplane mode, or location) and repeat—or switch to Route B if unsafe.
7. Fill the on-page observation table; copy into portfolio.

### A2 — CLI (optional)

```bash
python3 labs/LAB-PKT-001/cli/path_inspect.py --fixture
# optional live check (EXTERNAL_DEPENDENCY; may fail offline — that is still evidence):
python3 labs/LAB-PKT-001/cli/path_inspect.py --dns-check example.com
```

Do not pass credentials. Do not scan networks you do not administer.

## Route B — Fixture fallback (mandatory accessible path)

**Status:** `FIXTURE_VALIDATED`

When live networks are unavailable, unsafe, or inaccessible:

1. Open `fixtures/sample_path_trace.json`, `fixtures/sample_timing_table.csv`, and `fixtures/sample_observation.md`.
2. Answer the parse/identification questions (TTL, ethertype/IPv4, scopes, access vs Internet).
3. Redraw the path using portfolio `diagram.md`.
4. Record the fixture honesty banner: rows are **not** your device measurements.
5. Place a fixture note in `portfolio/evidence/` proving Route B was used.

```bash
python3 labs/LAB-PKT-001/cli/path_inspect.py --fixture --quiz
```

## Evidence (portfolio)

Minimum in `labs/LAB-PKT-001/portfolio/`:

- observation / timing table  
- path diagram (device / LAN / Internet + access + edge/cloud hypothesis)  
- screenshot **or** fixture note proving route  
- reflection (observation vs inference)  
- teach-back (Wi-Fi ≠ Internet ≠ cellular ≠ cloud)

Bare `PASS` is not evidence.

## Interpretation

### Observation examples

UI said “waiting for network”; browser showed DNS time; Wi-Fi icon on; cellular icon on; fixture TTL equals N.

### Inference examples

“The tower is congested”; “the cloud region failed”; “DNS is broken” without name-resolution evidence.

### Causal caution

Causal claims need extra named evidence (ordered hypotheses: access → DNS → reachability → transport/retries → remote placement).

## Pathway depth

| Pathway | Learner action |
|---|---|
| Explorer | Observe UI cues; label local vs LAN vs Internet; name access if known |
| Operator | Inspect browser/OS indicators; compare two conditions; fill table |
| Builder | Create labeled path diagram; optionally edit fixture timing JSON/Markdown |
| Engineer | Diagnose ordered hypotheses (access → DNS → reachability → transport → placement) |
| Researcher | N≥3 runs with confounders listed; no published benchmark claim |
| Educator | Misconception check; run fixture route when live networks unsafe |

## Limits

- Software timestamps ≠ physical RF measurements (`PHYSICAL_PENDING`).
- Bars/waves alone do not prove tower congestion.
- One run is learning, not a benchmark.
- Live Route A depends on external networks (`EXTERNAL_DEPENDENCY`).

## WAIKE adjacency (not identity)

Closest accepted-main neighbors include `COMPUTER_NETWORKING` / `lab_datapath` and `GENERAL_IT` / `lab_dns_hosts`. This lab remains publication-owned; do not invent a WAIKE module ID named LAB-PKT-001.

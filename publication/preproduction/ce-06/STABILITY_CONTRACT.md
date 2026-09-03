# CE-6 Stability Contract — Formal Teaching Model

**Chapter:** CE-6  
**Anchor experience:** Connected-but-unusable send/submit/sync (see `EXPERIENCE_MAP.md`)  
**Definition (publication teaching model):**

> A user experience exists only while multiple hidden technical conditions remain within acceptable bounds.

**Signature distinction:** A system can remain technically **connected** while the human experience has already **failed**.

**Numeric rule:** Use qualitative language where no measured threshold exists. Do **not** invent performance budgets or product SLOs.

---

## Formal teaching model (how to teach it)

1. **Name the human experience** — what success looks like for a person.  
2. **List concurrent conditions** — not a single villain metric.  
3. **Separate status chrome from experience outcomes.**  
4. **Assign symptoms to failure domains** with evidence gates.  
5. **Label every datum** observed / inferred / illustrative.  
6. **Climb the evidence hierarchy** only as far as tools and ethics allow.  
7. **State tradeoffs and who is excluded** when conditions are tuned.  
8. **Close with teach-back** — can another person use the model?

CE-6 **synthesizes** CE-1…CE-5 into this loop; it does not re-lecture each prior chapter.

---

## Concurrent hidden conditions (anchor)

For a successful send/submit/sync experience, conditions such as the following must remain *good enough together*:

| Condition ID | Hidden condition | Depends on |
|---|---|---|
| SC-01 | Input / intent recognized and delivered into the software path | Device I/O, OS input stack, app listeners |
| SC-02 | Application scheduled; handler not hung | OS scheduler, event loop, concurrency |
| SC-03 | Memory / working state available | RAM pressure, leaks, caching policy |
| SC-04 | Storage responsive if persistence required | Disk/flash IO, quotas, sync queues |
| SC-05 | Network path usable *if* remote work is required | Link association, DNS, routing, transport |
| SC-06 | Remote service available and authorized *if* required | Service health, auth/session, API contracts |
| SC-07 | Coherent render / UI feedback reaches the human | UI thread, compositor, display path |
| SC-08 | Power / thermal state not collapsing performance | Battery modes, thermals |
| SC-09 | Trust / permissions allow the action | Identity, scopes, secure storage |
| SC-10 | Accessibility / alternative path provides equivalent feedback | AT APIs, captions, non-pointer input |
| SC-11 | Total delay and variability remain acceptable *to this person in this context* | All of the above + expectations |

**Teaching note:** Acceptable bounds are **context-dependent**. Do not publish fake universal millisecond tables as gunnchOS truth.

---

## Failure domains

| Domain | Example locally observable symptoms | Common mis-blame |
|---|---|---|
| Input / interaction | Taps ignored; focus lost; AT silent | “App is broken” only |
| Compute / schedule | UI frozen; spinner CPU-bound | “Wi‑Fi” |
| Memory / storage | Hitches after large attachments; save failures | “Cloud” |
| Network path | Connected icon + timeouts; captive portal | “Server” |
| Service / backend | HTTP 5xx/401; success UI without durable effect | “My phone” |
| Render / display | Work finished, frame late/janky | “Network” |
| Power / thermal | Sudden slowdown when warm / low power | “Software update” |
| Trust / privacy controls | Permission denied; session expired | “Bug” |
| Equity / access path | Works on author’s setup only | “User error” |

---

## Dependencies (cross-chapter synthesis)

- **CE-1:** ecosystem and dependency thinking  
- **CE-2:** experience-first path; first Stability Contract exposure  
- **CE-3:** CPU/memory/storage/OS symptoms  
- **CE-4:** packets, access networks, edge/cloud placement  
- **CE-5:** identity, privacy, AI uncertainty as contract conditions  

---

## Locally observable symptoms (commodity)

- OS network status vs actual action completion  
- Browser DevTools: request timing, main-thread long tasks (when web)  
- Visible UI state transitions (immediate local update vs remote confirmation)  
- Retry/backoff behavior  
- Accessibility announcements / focus order failures  
- Qualitative: “felt stuck,” “completed for me / not for peer”

## Measurements that would support diagnosis

- Timestamp table for local handler vs network wait vs paint (where exposed)  
- Comparison runs under two network classes or local-only vs remote  
- HTTP status / error strings from benign endpoints  
- Resource timing entries (Performance API)  
- Structured logs **with secrets redacted**  
- Fixture traces when live capture impossible  

## Measurements we cannot yet obtain (honesty list)

- Carrier-grade QoE MOS campaigns for this publication wave  
- Kernel/ftrace on locked consumer phones without unsupported mods  
- Physical Device Quartet EVT measurements (`PHYSICAL_PENDING`)  
- Vendor-private radio KPI dumps as a CE requirement  
- Any invented gunnchOS product latency budget  

## Human consequence

When the contract fails, people lose trust, waste time, miss deadlines, or are **excluded** (weaker devices, metered links, assistive paths, offline contexts). CE-6 treats that consequence as part of the technical story—not a footnote.

---

## Capstone application

Learners instantiate this contract on **their** chosen experience, then **Explain, Measure, Improve, and Teach** it (`LAB-CE06-001`).

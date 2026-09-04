---
status: draft
chapter_id: CH17
chapter_number: 17
title: "Wi-Fi, Cellular, 5G, and the Road to 6G"
author: "Edmund Gunn, Jr."
part: IV
concept_edition: false
manuscript_status: WORKING_DRAFT_COMPLETE
human_validation_status: PENDING_FULL_MANUSCRIPT_REVIEW
publication_status: NOT_PUBLICATION_READY
labs: [LAB-PKT-001]
figures:
  - FIG-CH17-001
  - FIG-CH17-002
  - FIG-CH17-003
---

# Chapter 17 — Wi-Fi, Cellular, 5G, and the Road to 6G

**Status:** `draft` · **Chapter ID:** `CH17`  
**Author:** Edmund Gunn, Jr.  
**Manuscript:** working draft complete · human validation pending · not publication-ready

---

## 1. The moment {#sec-ch17-moment}

You leave a building. The Wi-Fi icon disappears—or stays, weakly—and a cellular icon takes over. A call continues, or it does not. A chat that felt instant now stalls. Sometimes a **5G** badge appears while the experience still feels bad. From your seat it feels like one story: *I have signal, so it should be fine.*

Underneath that feeling, different **radio access technologies (RATs)** are competing for ownership of the last hop. Wi-Fi is a local wireless LAN family; cellular is an operator mobile access family; neither is “the Internet,” and neither is “the cloud” [@ieee80211-2020; @threegpp-ts23501; @kurose-ross-8]. A generation label on the status bar is not a guarantee that your app’s latency or reliability class is what marketing implied (CLM-CH17-001; CLM-CH17-002).

This chapter is Part IV access-network literacy—not a full RF course, not a 6G product brochure, and not a claim that Device Quartet drive-test numbers exist yet (CLM-CH17-005 remains **PHYSICAL_PENDING**). It follows the book’s arc—**human experience → system → component**—until bars, badges, and “online” stop being synonyms.

The governing question:

> When my access icon changes—or stays lit while the experience fails—what actually changed: the radio path, the operator/core path, or only my story about the icon?

---

## 2. What you notice {#sec-ch17-notice}

Before names like *handover* or *5G System* enter, notice the human contract you already expect.

You expect a call or message to keep working when you walk. You expect “Wi-Fi” and “cellular” icons to mean something different. You expect a **5G** badge to mean *better*—faster, more reliable, somehow fairer. You also expect “connected” to mean the thing you are trying to do can finish.

Those expectations are not decorations around radios. They *are* the product, from the person’s point of view.

**A lit access icon is a partial status report, not a completed Stability Contract for the human task.**

Notice the split timelines. Association or attachment can succeed while a chat still waits. A 5G icon can stay lit while a handover or Wi-Fi offload briefly breaks the experience (CLM-CH17-004). Moving outdoors can improve bars and still leave a captive portal, DNS stall, or remote service outage untouched—those failures belong to other layers Chapter 16 and CE-4 already separated.

Optional comparison, available on a phone or laptop you already own (or via fixtures if you have no plan): note the **text label** of the active access (Wi-Fi / cellular / unknown), try one ordinary send or sync, then change **one** condition—walk toward a door, toggle Wi-Fi once, or use the lab fixture route. Do not climb for signal. Do not transmit on unlicensed equipment you are not authorized to operate. The point is not a drive test. The point is to notice that icons and usable outcomes can disagree.

---

## 3. Exploded ecosystem {#sec-ch17-ecosystem}

An everyday walk is not one radio. It is a path through an ecosystem. **FIG-CH17-001** is the first-minute map: device ↔ Wi-Fi access point path **versus** cellular radio access network (RAN) path ↔ operator or campus backhaul ↔ Internet path ↔ edge/cloud service. Treat it as **Representative educational architecture**, not a claim that your phone’s sealed internals look exactly like the diagram.

Walk the layers in ordinary language, then keep the same layers when vocabulary deepens.

### Human

You form intent: keep the call, finish the send, stay on the map. Eyes read icons. Ears and hands judge whether the experience held.

### Device radios and policy

Commodity devices often carry **both** Wi-Fi and cellular radios. OS and modem policy choose which path carries which traffic, when to prefer Wi-Fi, and when to fall back. Dual-path does not mean dual success.

### Wi-Fi access (local wireless LAN)

**Wi-Fi** names consumer and enterprise wireless LAN technologies built on the IEEE 802.11 family [@ieee80211-2020]. An access point (AP) or mesh node is a local on-ramp. Wi-Fi can provide LAN reachability without guaranteeing Internet reachability—guest isolation and captive portals are everyday counterexamples [@kurose-ross-8].

### Cellular access (operator mobile)

**Cellular** names wide-area mobile access operated as a service: cells, base stations, operator identity, and mobility procedures across coverage areas [@threegpp-ts23501; @kurose-ross-8]. Generations (2G→5G at survey depth) are standards stories, not bar-count synonyms.

### Radio access network and core (cellular path)

On the cellular side, the **radio access network** sits between the device and a **core** that authenticates subscribers and connects onward toward Internet or operator services [@threegpp-ts23501]. You rarely see that split. You feel attachment, mobility, and policy.

### Internet path and placement (not access)

Packets that leave the access network still need addressing, routing, and a place where the service runs—edge-near or cloud-far. Those are Chapter 15–16 concerns. Collapsing them into “5G” or “Wi-Fi” is the Part IV misconception this chapter refuses (CLM-CH17-001).

### Icons, bars, and badges

Status UI summarizes radio and attachment state for humans. It is an interpretation layer—not a QoE meter, not a latency class certificate, and not proof that a particular 5G feature set is active for your app (CLM-CH17-002).

**FIG-CH17-002** later places cellular generations through 5G and marks **6G as roadmap**—research and standards direction, not a deployed consumer fact in this manuscript (CLM-CH17-003; `SOURCE_NEEDED` for a dated 3GPP study-item primary).

---

## 4. Follow the signal {#sec-ch17-signal}

**FIG-CH17-003** shows a walk: indoor Wi-Fi association → approach exit → Wi-Fi weakens → cellular attachment or handover/offload → app traffic continues or stalls. Read it as a logical story, not as a measured drive test of your city.

1. **Intent.** A person starts or continues a task that needs a path.
2. **Access choice.** The device uses Wi-Fi, cellular, or switches between them according to policy and conditions [@kurose-ross-8].
3. **Local wireless LAN path (when Wi-Fi).** Association with an AP; LAN forwarding; optional captive/auth gates before Internet scope [@ieee80211-2020; @kurose-ross-8].
4. **Cellular path (when cellular).** Attachment to a cell/RAN; authentication and session context in the operator system; onward toward the Internet or operator service [@threegpp-ts23501].
5. **Mobility event.** Handover between cells, or offload between Wi-Fi and cellular, tries to preserve service. Transient failures can occur while icons remain lit (CLM-CH17-004).
6. **Beyond-access path.** DNS (if used), routing, transport, and remote placement still have to succeed—CE-4 / CH16 adjacency.
7. **Human feedback.** Call audio, checkmarks, maps, or “waiting for network” close the loop—or fail to.

### Alternate paths (the honesty rule)

Not every “5G” badge implies the same radio band, core feature set, or network slice. Not every Wi-Fi SSID provides Internet. Not every stall is radio: CPU, storage, app logic, or remote overload can impersonate “bad signal.” Teaching those forks prevents the encyclopedia trap—listing every generation marketing name instead of tracing one honest walk.

### Failure branch without drama

When something fails, prefer failure *domains* over confident blame:

- Access attachment / association
- Mobility (handover / offload) interruption
- Captive portal / policy block
- Beyond-access path (DNS, routing, transport)
- Remote service placement
- On-device stack or app logic

Outside observation rarely distinguishes those cleanly. That limitation is literacy, not a bug in the reader.

---

## 5. Component cards {#sec-ch17-components}

For each object: plain language, analogy, technical function, constraints, common symptoms. Analogies are labeled as analogies.

### Wi-Fi (IEEE 802.11 family)

- **Plain language.** Local wireless LAN access—usually your building, café, or campus on-ramp.
- **Analogy (labeled).** Like a neighborhood side street onto the larger road system—not the highway itself.
- **Technical function.** Wireless LAN medium access and PHY/MAC families standardized under IEEE 802.11 [@ieee80211-2020].
- **Constraints.** Shared medium, coverage of APs, authentication/captive gates, interference (qualitative; no invented SNR tables here).
- **Symptoms.** Associated but no Internet; works near AP only; captive portal loop.

### Cellular access

- **Plain language.** Operator mobile wide-area radio access you subscribe to (or roam on).
- **Analogy (labeled).** Like a municipal transit system with stations (cells) and rules for transferring—not the destination city.
- **Technical function.** Mobile attachment, mobility, and operator-mediated connectivity toward services and the Internet [@threegpp-ts23501; @kurose-ross-8].
- **Constraints.** Coverage, operator policy, plan/capability, device bands (survey depth only).
- **Symptoms.** Bars with no usable data; works outdoors not indoors; generation badge without better feel.

### Radio access technology (RAT)

- **Plain language.** A family of radio methods for attaching a device to a network.
- **Analogy (labeled).** Like different vehicle types that can use roads—bike path vs bus lane—not the map of the city.
- **Technical function.** Names the access *kind* (e.g., Wi-Fi vs cellular generations) so readers stop treating “wireless” as one thing [@kurose-ross-8].
- **Constraints.** Device support, regulatory bands, operator/AP deployment.
- **Symptoms.** Confusion when dual-radio devices switch without explaining why the experience changed.

### 5G system (survey)

- **Plain language.** Fifth-generation mobile system as specified in the 3GPP architecture family—at teaching survey depth.
- **Analogy (labeled).** Like a building code for a generation of transit—not a promise that every trip will be on-time.
- **Technical function.** 3GPP describes a 5G System architecture (access and core concerns) distinct from IEEE 802.11 Wi-Fi [@threegpp-ts23501].
- **Constraints.** Deployment choices vary by operator and region; icon ≠ feature proof (CLM-CH17-002).
- **Symptoms.** “I have 5G” used as a diagnosis for stalls that are DNS, congestion beyond the RAN, or app-side.

### 6G roadmap

- **Plain language.** Research and standards *direction* after 5G—not a present consumer network fact in this book.
- **Analogy (labeled).** Like a published transit expansion plan—useful for orientation, not a ticket you can punch today.
- **Technical function.** Teaching humility: roadmap ≠ deployment. This manuscript does **not** invent 6G radio parameters, commercial availability dates, or performance guarantees (CLM-CH17-003; primary study-item cite remains `SOURCE_NEEDED`).
- **Constraints.** Any consumer “6G” marketing claim needs dated primary evidence before it becomes fact language.
- **Symptoms.** Treating “road to 6G” as “my phone already has 6G bars.”

### Handover / mobility (intro)

- **Plain language.** Changing cells or APs while trying to keep service.
- **Analogy (labeled).** Like transferring trains without dropping your luggage—sometimes the transfer itself is the delay.
- **Technical function.** Mobility procedures aim to preserve sessions across radio changes; offload moves traffic between Wi-Fi and cellular [@threegpp-ts23501; @kurose-ross-8].
- **Constraints.** Timing, coverage overlap, policy; transient failure possible (CLM-CH17-004).
- **Symptoms.** Brief mute, stalled send, then recovery—while the icon never “looked” offline.

### Bars vs experience

- **Plain language.** Signal icons are not quality of experience.
- **Analogy (labeled).** Like a fuel light that does not tell you whether the road ahead is closed.
- **Technical function.** Separates radio/attachment summary UI from task success [@kurose-ross-8].
- **Constraints.** Accessibility: do not teach color-only legends; use text labels.
- **Symptoms.** Full bars, failed task; empty-feeling bars, task still works on another path.

---

## 6. Stability contract {#sec-ch17-stability}

A connected walk continues only while multiple hidden conditions stay within acceptable bounds.

Access technologies attach devices; backhaul and core paths carry traffic onward; mobility events must not interrupt beyond what the human task can tolerate; icons must not be mistaken for contract success. Those statements are **qualitative**. They are not a table of invented latency budgets, and they are not a promise that every operator’s “5G” means the same thing.

For the ordinary “I walked outside and it kept working” feeling, conditions like these must hold together:

1. **Chosen access** remains associated/attached as the task requires (Wi-Fi, cellular, or an intentional switch).
2. **Backhaul / core / onward path** remains usable toward the service—not merely a lit RAT icon.
3. **Mobility events** (handover, offload) stay within interruption the experience can absorb (CLM-CH17-004).
4. **Beyond-access dependencies** (DNS, routing, transport, remote placement) still succeed when the task needs them.
5. **Device policy and radios** agree on which path owns the traffic.
6. **Human-visible status** is honest enough not to train false confidence (icon ≠ QoE).
7. **Plan / authorization / captive gates** do not silently strand Internet scope.

A system can remain *radio-connected* while the human experience has already failed. Conversely, an icon can look weak while a dual-path device still completes the task on another RAT. Stability is concurrent conditions—not a single badge.

**Honesty bound for this edition:** Any gunnchOS / Device Quartet cellular or Wi-Fi drive-test numbers remain **PHYSICAL_PENDING** (CLM-CH17-005). Commodity observation in **LAB-PKT-001** produces *your* evidence for *your* path—or fixture honesty—not a universal RF score. **6G stays roadmap language** until a dated primary can be pinned (CLM-CH17-003).

---

## 7. Try it {#sec-ch17-try}

### LAB-PKT-001 — Trace One Connected Action Across Path and Access

**Goal.** Label a commodity (or fixture) path with device / LAN / Internet scopes **and** access network as Wi-Fi / cellular / unknown / fixture—practicing **Wi-Fi ≠ cellular ≠ Internet ≠ cloud**.

**CE / WAIKE alignment note.** This lab inherits CE-4 preproduction and publication lab ownership. WAIKE `WIRELESS_6G` / `wireless_dsp_6g` are **adjacent** competencies only—do not treat this chapter as that full course, and do not invent WAIKE lab IDs.

**Safety (hard stops).**

- No unlicensed RF transmitters, SDRs used as TXers, jammers, evil-twin APs, or cracking tutorials.
- No unauthorized scanning or packet capture on networks you do not administer.
- Do not capture other users’ traffic; scrub PII, tokens, and message bodies from artifacts.
- Do not climb for signal; avoid distracted walk-and-test near traffic.
- No Device Quartet RF field campaign required or claimed.
- Learners without cellular plans: use **fixture Route B** (equity default).

**Routes.**

- **Route A — Commodity.** Browser or CLI path inspect on a device you already use; label access from OS text (not color alone); change one condition carefully or stop.
- **Route B — Fixture (mandatory accessible path).** Use `labs/LAB-PKT-001/fixtures/` and the CLI `--fixture` quiz; record that rows are not your radio measurements.

**Explorer baseline (about 45–60 minutes).**

1. Predict failure family (latency / reliability / throughput) and access mode before running.
2. Run Route A demo or Route B fixtures per `labs/LAB-PKT-001/README.md`.
3. Record observations only: icon/text labels, UI phrases, coarse timing phases if visible.
4. Draw a path diagram with access labeled Wi-Fi XOR cellular XOR unknown/fixture.
5. Fill observation-vs-inference; teach-back the four-way distinction.

**Operator extension.** Log icon/text vs usable send across one access change (doorway walk or Wi-Fi toggle)—or fixture comparison rows. Do not claim tower congestion without evidence.

**Builder extension.** Diagram a dual-path device (Wi-Fi + cellular) with policy choice as a labeled fork—no RF math required.

**Engineer extension.** Place “5G” at survey depth: cite architecture literacy via 3GPP TS 23.501 family without pinning undownloaded clause numbers [@threegpp-ts23501]. List which failure domains your observations cannot distinguish.

**Researcher extension.** Separate roadmap claims from deployed facts with dates. For 6G, state explicitly: **not deployed consumer fact here**; primary study-item cite `SOURCE_NEEDED` (CLM-CH17-003). Forbid inventing Quartet drive-test numbers (CLM-CH17-005).

**Proposed observation-only stretch (not a separate shipping lab ID).** `LAB-ACCESS-OBS-001` in the chapter packet remains a **proposed** name for a walk-test icon-vs-outcome log with fixture alternative—still **no RF TX**.

**Evidence to keep.** Path diagram; timing/observation table; scrubbed notes or fixture proof; teach-back paragraph.

---

## 8. Build it {#sec-ch17-build}

Extend LAB-PKT-001 without turning Part IV into a spectrum encyclopedia.

### Explorer

Build a pocket card: Wi-Fi / cellular / Internet / cloud—one plain sentence each that forbids synonym collapse.

### Operator

Build an “icon vs outcome” checklist: access text label → task result → next evidence needed. End with “needs more evidence,” never with fake tower certainty.

### Builder

Build a dual-path diagram: human → device policy → Wi-Fi AP path and cellular RAN/core path → Internet → service placement hypothesis. Mark visible vs sealed.

### Engineer

Build a one-page generation survey: 2G→5G as standards evolution bullets at teaching depth, plus a clearly labeled **6G = roadmap** box with no invented specs [@threegpp-ts23501]. Mark CLM-CH17-003 as bounded.

### Researcher

Build an evidence plan for a claim you are *not* allowed to make yet—for example, “operator X’s 5G icon guarantees URLLC-class latency for app Y,” or “consumer 6G is live in region Z.” Specify dated standards/operator evidence required; keep Quartet measurements **PHYSICAL_PENDING**.

Educators can facilitate teach-backs from Section 11 and keep classrooms on Route B when plans, privacy, or public Wi-Fi make Route A unsafe.

---

## 9. Secure and include it {#sec-ch17-secure-include}

### Security

Access networks are attack and abuse surface: rogue APs, captive-portal phishing, and unauthorized radio transmission. This book’s labs forbid jamming, cracking, and unlicensed TX experiments. Prefer known networks, fixture routes, and user consent over “interesting” radio mischief. Survey literacy here foreshadows later trust and privacy chapters without becoming an offensive wireless lab.

### Privacy

Access mode and timing logs can imply location patterns. LAB-PKT-001 artifacts record access as a category, not a GPS trail. Redact accounts, message previews, and classmate screens.

### Accessibility

Status icons must not be taught by color alone—require text legends (Wi-Fi / cellular / 5G badge names as text). Fixture Route B is mandatory for learners without stable broadband or personal cellular plans. Document walk-test steps in words; do not require climbing or hazardous mobility.

### Equity

Cellular plans, indoor coverage, and café Wi-Fi quality shape who can participate. Teaching access literacy includes naming those barriers and shipping a fixture path so literacy is not gated on a subscription.

### Safety

No RF transmitter kits in classroom procedures. No distracted street testing. Physical and spectrum safety are part of professional wireless culture, not optional footnotes.

### Ethics

Do not claim deployed consumer 6G, invent drive-test dB tables, or present Quartet radio results you do not have. Overclaiming coverage is still false evidence.

---

## 10. Career lens {#sec-ch17-career}

One doorway walk crosses many ownership domains. No table promises employment; roles vary by organization. LAB-PKT-001 artifacts resemble early professional evidence in miniature: labeled access, observation discipline, and explicit uncertainty.

| Role lens | Typical artifacts | Review questions |
|---|---|---|
| Wireless engineer (`ROLE-WIRELESS`) | Link/access observations, RF plans when authorized | Access vs beyond-access ownership clear? |
| Network engineer (`ROLE-NET`) | Path timing, reachability notes | Icon failure or path/DNS failure? |
| Mobile / systems (operator adjacency) | Mobility/attach incident notes | Handover/offload vs core/policy? |
| SRE (`ROLE-SRE`) | Connected vs usable evidence | Did the service placement fail while RAT looked fine? |
| Security (`ROLE-SEC`) | Threat notes for rogue AP / portal abuse | Did we forbid unauthorized TX and capture? |
| Accessibility (`ROLE-A11Y`) | Non-color status legends, fixture routes | Can learners without plans complete the lab? |

Portfolio hint: a scrubbed access-labeled path diagram plus observation-vs-inference beats a vibes-based “5G is broken” claim.

---

## 11. Check understanding {#sec-ch17-check}

**Concept.** In one sentence each, define *Wi-Fi*, *cellular*, and *Internet* so that none of them swallows the other two—and add why *cloud* is still a fourth idea.

**System tracing.** Trace a doorway walk from indoor Wi-Fi to outdoor cellular in numbered steps. Mark which steps you observed and which you inferred.

**Misconception check.** Why is “I have 5G, so latency must be fine” incomplete? What does the icon fail to prove (CLM-CH17-002)?

**Misconception check.** Why must this chapter refuse deployed-consumer 6G language without dated primary evidence (CLM-CH17-003)?

**Teach-it-back.** Explain to a newcomer—using only LAB-PKT-001 vocabulary—why a phone can show bars and still fail a send during a Wi-Fi↔cellular transition.

**Researcher prompt.** What evidence would convert a PHYSICAL_PENDING Quartet Wi-Fi/cellular measurement claim into a documented physical claim? What remains out of scope for a no-TX classroom lab?

---

## References

Selected authoritative sources for this chapter’s general technical explanations are listed in the bibliography (`book/references/references.bib`). Project-specific Device Quartet RF status remains in `evidence/claim_registry.yaml` and in the chapter claim plan (CLM-CH17-005), separately from external literature.

Inline citations used in this chapter include @ieee80211-2020, @threegpp-ts23501, and @kurose-ross-8. Claim CLM-CH17-003 (6G roadmap primary) remains `SOURCE_NEEDED`—bounded in prose without fabricated study-item IDs.

---

## 12. Glossary links {#sec-ch17-glossary}

Candidate terms introduced or reinforced here (see also chapter glossary candidates; do not treat this list as an auto-merge into the live glossary):

| Term | Plain link |
|---|---|
| Wi-Fi | Wireless LAN access based on IEEE 802.11 technologies |
| Cellular | Mobile wide-area radio access operated as a service |
| Radio access technology (RAT) | Family of radio methods attaching devices to networks |
| 5G | Fifth-generation 3GPP mobile system (survey sense) |
| 6G roadmap | Next-generation research/standards direction—not a present consumer fact here |
| Handover | Transfer of a connection between cells or access points |
| Radio access network | Radio portion of a mobile network between device and core |
| Bars vs experience | Signal icons are not QoE |
| Stability contract | Concurrent conditions that keep the access experience alive |

Related earlier chapters: packets/Internet (CH16), cloud/edge placement (CH15), CE-4 survey inheritance. Related later chapters: spectrum/radio depth (CH18), NTN continuity (CH19), latency/reliability/QoE (CH20).

---

## Figure references (planned embeds; **draft-blocked** until SVG + a11y land)

All three figures are **conceptual / illustrative teaching aids** unless a future revision replaces them with measured evidence. No fabricated telemetry or drive-test plots.

### FIG-CH17-001 — Wi-Fi AP path vs cellular RAN path vs Internet

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Comparative layers.
- **Reader should notice.** Access technologies are on-ramps; Internet path and cloud/edge placement sit beyond; Wi-Fi ≠ cellular ≠ Internet.
- **Truth class.** Conceptual / Representative educational architecture.
- **Alt text requirement.** Name Wi-Fi AP path, cellular RAN/core path, Internet onward path, and service placement; state conceptual truth class; color not sole encoding.

### FIG-CH17-002 — Generations survey to 5G to 6G roadmap

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Timeline.
- **Reader should notice.** 5G as deployed-generation survey language vs **6G clearly labeled roadmap** (not consumer deployment fact).
- **Truth class.** Illustrative.
- **Alt text requirement.** Enumerate generation labels in order; explicitly mark 6G as roadmap; deny invented 6G specs.

### FIG-CH17-003 — Wi-Fi to cellular transition during a walk

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Sequence.
- **Reader should notice.** Numbered mobility/offload steps plus a failure branch where icons stay lit.
- **Truth class.** Conceptual.
- **Alt text requirement.** Enumerate steps; label transient failure while icon lit; state non-measured teaching sequence.

---

## Claim footnotes used in this chapter (project-specific)

- **CLM-CH17-001.** Wi-Fi and cellular are different access technologies; neither is the Internet—framed with IEEE 802.11, 3GPP TS 23.501, and textbook survey depth [@ieee80211-2020; @threegpp-ts23501; @kurose-ross-8].
- **CLM-CH17-002.** 5G denotes a 3GPP system generation; icon presence does not prove a specific latency/reliability class for the user’s app [@threegpp-ts23501].
- **CLM-CH17-003.** 6G is future/roadmap; do not claim deployed consumer 6G as present fact without dated evidence. Status: `SOURCE_NEEDED` (no fabricated study-item cite in this draft).
- **CLM-CH17-004.** Handover and offload can cause transient experience failures while icons stay lit [@threegpp-ts23501; @kurose-ross-8].
- **CLM-CH17-005.** Any gunnchOS/Quartet cellular/Wi-Fi drive-test numbers are **PHYSICAL_PENDING**.

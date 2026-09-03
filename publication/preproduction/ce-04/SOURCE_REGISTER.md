# CE-4 Source Register (chapter-local proposal)

**Module:** CE-4  
**Status:** `preproduction` — not merged into canonical global bibliography  
**Verified on:** 2026-09-02 (HTTP checks + page metadata where noted)  
**Rule:** No invented DOI/ISBN/pages/years/revision numbers. Living standards marked as living.

Gate note: `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

---

## Verification method

1. Prefer primary standards URLs on `rfc-editor.org`, NIST CSRC, IEEE Standards sites.  
2. Confirm HTTP reachability with ordinary GET.  
3. For books, confirm edition/ISBN via publisher catalog pages.  
4. For project claims, cite accepted-main SHA from a local fetch of `gunnchOS3k/waike-research-ops`.

---

## A. Standards / specifications

| Local ID | Work | Type | Year / status | URL | Verification |
|---|---|---|---|---|---|
| SRC-CE4-RFC791 | RFC 791 Internet Protocol | IETF RFC (fixed) | 1981 | https://www.rfc-editor.org/rfc/rfc791 | HTTP 200 |
| SRC-CE4-RFC768 | RFC 768 User Datagram Protocol | IETF RFC (fixed) | 1980 | https://www.rfc-editor.org/rfc/rfc768 | HTTP 200 |
| SRC-CE4-RFC9293 | RFC 9293 TCP | IETF RFC (fixed) | 2022 | https://www.rfc-editor.org/rfc/rfc9293 | HTTP 200 |
| SRC-CE4-RFC8200 | RFC 8200 IPv6 | IETF RFC (fixed) | 2017 | https://www.rfc-editor.org/rfc/rfc8200 | HTTP 200 |
| SRC-CE4-RFC1034 | RFC 1034 Domain concepts | IETF RFC (fixed) | 1987 | https://www.rfc-editor.org/rfc/rfc1034 | HTTP 200 |
| SRC-CE4-RFC1035 | RFC 1035 DNS implementation/spec | IETF RFC (fixed) | 1987 | https://www.rfc-editor.org/rfc/rfc1035 | HTTP 200 |
| SRC-CE4-RFC1918 | RFC 1918 Private Address Space | IETF RFC (fixed) | 1996 | https://www.rfc-editor.org/rfc/rfc1918 | HTTP 200 |
| SRC-CE4-RFC1122 | RFC 1122 Host Requirements | IETF RFC (fixed) | 1989 | https://www.rfc-editor.org/rfc/rfc1122 | HTTP 200 |
| SRC-CE4-RFC3022 | RFC 3022 Traditional NAT (informational) | IETF RFC (fixed) | 2001 | https://www.rfc-editor.org/rfc/rfc3022 | HTTP 200 |
| SRC-CE4-RFC9000 | RFC 9000 QUIC | IETF RFC (fixed) | 2021 | https://www.rfc-editor.org/rfc/rfc9000 | HTTP 200 |
| SRC-CE4-RFC8446 | RFC 8446 TLS 1.3 | IETF RFC (fixed) | 2018 | https://www.rfc-editor.org/rfc/rfc8446 | HTTP 200 (security adjacency) |
| SRC-CE4-NIST800145 | NIST SP 800-145 Cloud Computing definition | NIST SP (fixed) | Sep 2011 | https://csrc.nist.gov/pubs/sp/800/145/final | HTTP 200; title/authors Mell & Grance confirmed on page |
| SRC-CE4-NIST500325 | NIST SP 500-325 Fog Computing Conceptual Model | NIST SP (fixed) | Mar 2018 | https://csrc.nist.gov/pubs/sp/500/325/final | HTTP 200; PDF also 200 |
| SRC-CE4-IEEE80211WG | IEEE 802.11 Working Group | living WG hub | living | https://www.ieee802.org/11/ | HTTP 200 |
| SRC-CE4-IEEE80211-2020 | IEEE Std 802.11-2020 listing page | IEEE standard listing | 2020 listing page | https://standards.ieee.org/standard/802_11-2020.html | HTTP 200 (do not invent clause page cites) |
| SRC-CE4-3GPP23501 | 3GPP TS 23.501 System architecture for the 5G System | 3GPP TS (living revisions) | living family; **no revision pinned here** | https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=3144 | Portal HTTP 200; Cloudflare may block scrapers—cite by spec number, not invented rev |

### Living vs fixed

- **Fixed publications:** numbered IETF RFCs above; NIST SP 800-145; NIST SP 500-325; IEEE Std 802.11-2020 as a dated standard edition.  
- **Living / revisioned:** 3GPP TS 23.501 (always name the TS number; pin a specific version only after integrator download of a dated PDF).  
- **Living docs:** IEEE 802.11 WG hub; MDN pages.

---

## B. Official technical documentation

| Local ID | Work | Notes | URL | Verification |
|---|---|---|---|---|
| SRC-CE4-MDN-NETMON | MDN Network Monitor | Browser-visible network inspection | https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor | HTTP 200 |
| SRC-CE4-MDN-RESTIMING | MDN Resource Timing | Timing phases for requests | https://developer.mozilla.org/en-US/docs/Web/API/Performance_API/Resource_timing | HTTP 200 |
| SRC-CE4-WIFI-ALLIANCE | Wi-Fi Alliance Discover Wi-Fi | Non-normative industry explainer; secondary to IEEE | https://www.wi-fi.org/discover-wi-fi | HTTP 200 |

---

## C. Peer-reviewed / agency conceptual publications

Covered primarily via NIST SPs above (agency standards publications). No additional journal DOIs invented for CE-4 preproduction.

---

## D. Textbooks

| Local ID | Work | Edition | Year | ISBN-13 | Verification |
|---|---|---|---|---|---|
| SRC-CE4-KUROSE8 | Kurose & Ross, *Computer Networking: A Top-Down Approach* | 8 | Pearson page lists Published 2020 (© 2021) | 9780136681557 (US rental/edition listing) | Pearson catalog HTTP 200: https://www.pearson.com/en-us/subject-catalog/p/computer-networking/P200000003334 |

**Note:** Do not cite page numbers until a physical/ebook copy is checked in integration. Global edition ISBN 9781292405469 exists; prefer one edition consistently in prose.

---

## E. Project evidence (accepted main)

| Local ID | Repository | Branch | SHA | Role |
|---|---|---|---|---|
| SRC-CE4-WAIKE | `gunnchOS3k/waike-research-ops` | `main` | `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0` | Curriculum adjacency for networking/wireless/cloud labs |
| SRC-CE4-PUB | `gunnchOS3k/gunnchos-technology-landscape` | `main` | `166e9544bc6e2aee344bc962ace76d49ee3e04e4` | Publication accepted main containing PR #2 |

Prior publication audit SHA for WAIKE (`8eb2827…`) is an ancestor of current WAIKE main; CE-4 crosswalk uses the **newer** accepted-main SHA above.

---

## F. Explicitly rejected / deferred sources

| Candidate | Reason |
|---|---|
| Unsourced “typical 5G latency is X ms” blog numbers | Invented/unstable measurements |
| Paywalled 3GPP PDF revision without on-hand file | Cannot invent revision/page |
| Marketing 6G whitepapers as Concept Edition core | Out of CE-4 scope |
| Random GitHub gists for RF formulas | Prefer standards/textbooks |

---

## Counts by source class (verified for this package)

| Class | Count |
|---|---|
| Standards/specifications (IETF/NIST/IEEE/3GPP entries) | 16 |
| Official technical documentation (MDN/Wi-Fi Alliance) | 3 |
| Textbooks | 1 |
| Project accepted-main audits | 2 |
| Peer-reviewed journal articles with DOIs | 0 (none added) |
| **Total chapter-local proposed sources** | **22** |

---

## Integrator handoff

- Do **not** silently copy into `book/references/references.bib` until conflict check.  
- Reuse existing global keys (`rfc791`, `rfc9293`) where identical.  
- Keep chapter-local keys in `references.local.bib` for CE-4-only items.

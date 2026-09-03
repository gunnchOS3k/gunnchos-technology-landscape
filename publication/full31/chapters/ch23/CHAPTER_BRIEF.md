# CH23 — Cybersecurity from Chip to Cloud

**Package status:** `preproduction`  
**Manuscript status:** scaffold (no canonical chapter prose in this wave)  
**Full-book chapter:** CH23 (ch23)  
**Part:** V — Intelligence, security, and responsibility  
**Agent:** J (`agent-j/full31-part-v-vi`)  
**Accepted-main base:** `0e694176652d4729c7f2b71df08b871a863afb8c` (PR #3 merge)  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`. Do not claim PASS. Do not alter `CH02-REVIEW-R1`. Do not fabricate reader evidence.

---

## Reader promise

Follow security as UX-linked conditions from chip/boot trust through identity and cloud dependencies—principles and symptoms, never exploit recipes.

## Anchor human moment

A login succeeds but an action is denied—or a 'verify it's you' step appears—while the app still looks 'connected'.

## Teaching model

`moment → notice → ecosystem → signal → components → Stability Contract → Try/Build → secure/include → career → check → glossary`

Central chain: **Human experience → system → component → code → network → society**

## Measurable outcomes (Explorer → Researcher)

| Pathway | Outcome |
|---|---|
| Explorer | Name identity vs authentication vs authorization in ordinary language. |
| Operator | Map lockouts, MFA prompts, and permission denials to likely domains. |
| Builder | Fill an authz matrix (desk/reader/bot) for a toy service. |
| Engineer | Apply least privilege / fail-safe defaults to a component boundary sketch. |
| Researcher | State what evidence would support a trust claim without overclaiming. |

## Stability Contract (chapter conditions)

- Authentication assurance appropriate to risk
- Authorization decisions consistent with least privilege
- Crypto boundaries for transit/at-rest goals (with endpoint limits)
- Session/recovery paths remain usable and accessible
- Incident restore returns usable trust without security theater alone

## Security / equity / accessibility (integrated)

Teach principles + UX symptoms only—no scanning, phishing kits, or exploit PoCs. Accessible MFA alternatives; equity of recovery paths.

## Career lens

| Role family | Portfolio evidence |
|---|---|
| Security engineer | UX-linked threat-model worksheet (no exploits) |
| IAM engineer | authn/authz decision card |
| SRE / incident responder | restore-usable-trust playbook adjacency |

Employment is **not** guaranteed by completing artifacts.

## CE / lab inheritance (link — do not duplicate depth)

### Concept Edition
- CE-5 attack-surface / identity / crypto-goal slices
- CH11 firmware/trust adjacency (link)

### Labs
- LAB-TRUST-001 authn/authz + trust restore adjacency

## Device Quartet

not required; chip-to-cloud is conceptual across form factors

## Twelve-section anatomy (section intent only)

1. The moment — anchor above  
2. What you notice — human symptoms  
3. Exploded ecosystem — layers for this chapter  
4. Follow the signal — numbered path  
5. Component cards — plain language + constraints + failure symptoms  
6. Stability contract — conditions listed above  
7. Try it — lab opportunities  
8. Build it — small extension  
9. Secure and include it — integrated, not appendix  
10. Career lens — table above  
11. Check understanding — misconceptions + teach-back  
12. Glossary links — see `GLOSSARY_CANDIDATES.yaml`

## Explicit non-goals this wave

- Final canonical prose  
- Gate 3 PASS / fabricated human reviews  
- Invented WAIKE course/lab IDs  
- Fake citations or marketing Device Quartet claims  
- Representing illustrative EMIT / fixture examples as human evidence

## Next automatable action

Inherit CE-5 FIG-CE5-003/004/007 IDs into CH23 figure plan; keep security content non-offensive in drafting checklist

# LAB-IO-001 fixture — pipeline map (no live capture required)

**Status:** digital fixture · permission-safe  
**Truth class:** conceptual teaching aid

## Choose one experience (pick exactly one)

1. Play a local video or audio file you already own.  
2. Open a camera *permission prompt* and **deny** or cancel (do not record others).  
3. Watch a notification banner animate while music plays (observe contention, no capture).  
4. Use this textual fixture only (offline).

## Fixture story (offline)

You open a short clip of a public-domain waveform visualization while a banner slides in. The clip is local. No microphone is armed. No camera preview of another person appears.

### Capture → process → present (example fill)

| Stage | What happens in this fixture | Observable? |
|---|---|---|
| Capture | Not used (local file already stored) | N/A — skip live sensing |
| Decode / process | Player decodes media; compositor layers banner | Partially (UI layers) |
| Present | Frames to display; samples to speakers | Yes (see / hear) |
| Contended budget | Banner animation + media playback share GPU/CPU | Inferred until measured |

## Permission drill (safe)

If your platform shows a camera or microphone permission dialog, record only:

- whether the dialog appeared,
- what you chose (Allow / Deny / Cancel),
- whether the app continued with a non-sensing path.

Do **not** grant permission in shared spaces if it would expose classmates or bystanders.

## Observation vs inference

- **Observation:** “Banner appeared while audio continued.”  
- **Inference until more evidence:** “GPU was overloaded.”

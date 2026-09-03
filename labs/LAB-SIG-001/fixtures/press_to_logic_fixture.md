# Press → Logic fixture (offline)

**Lab:** LAB-SIG-001  
**Truth classification:** Conceptual educational fixture (not measured Device Quartet telemetry)  
**PHYSICAL_PENDING:** Any Quartet / EVT electrical numbers stay pending.

## Stages to label

| Stage | Plain-language name | Your mark (observed / inferred / not evidenced) | Notes |
|---|---|---|---|
| 1 | Human action (press) | | |
| 2 | Transducer / input interface | | |
| 3 | Signal (quantity over time) | | |
| 4 | Clock / timing reference (if synchronous) | | |
| 5 | Logic decision | | |
| 6 | Effect the person notices | | |

## Scenario narrative (cartoon)

A learner presses **Button B**. Inside the educational story:

1. Contact closes a sensing path (**transducer**).
2. A voltage level changes over a short time (**signal**).
3. A shared **clock** edge marks when logic should sample.
4. Logic implements: IF button_down AND unlock_ok THEN light_on.
5. An **effect** path turns on indicator L.

You do **not** have a real oscilloscope capture here. Mark stages you can only infer.

## Failure toggles (pick one; mark complaint)

| Toggle | What the fixture claims | Human complaint it can mimic |
|---|---|---|
| F1 Power missing on input domain | Display may still look awake | “Dead button” |
| F2 Noise high | Levels chatter near the threshold | “It double-fires” / “random presses” |
| F3 Clock paused | Samples never accepted | “Press does nothing until reboot” (cartoon) |
| F4 Effect disconnected | Decision happens; light path open | “Software thinks it worked; I see nothing” |

Chosen toggle: _____________  
Observation (what you saw in the fixture): _____________  
Interpretation (what might explain a real device—labeled as inference): _____________

## Prediction (before filling the table)

If nothing happens after a press, I expect the first failure at stage: _____________

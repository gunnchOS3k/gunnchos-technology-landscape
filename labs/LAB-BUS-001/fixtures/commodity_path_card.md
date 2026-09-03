# LAB-BUS-001 fixture — commodity interconnect path card

**Truth class:** illustrative teaching aid (not measured EVT; not Quartet fabrication).

## Path to label

```
Human hand
  → cable / accessory body (packaging you can see)
    → external port / connector face
      → host-side port electronics (inside the sealed host)
        → board traces / shared bus domain (conceptual)
          → protocol rules that make bits meaningful
            → device function (charge, data, both, or neither)
```

## What you may observe safely

- Connector shape and orientation marks
- Whether the cable seats fully without force
- Host UI text: connected / charging / error / nothing
- Accessory LED or screen change (if any)

## What you must not claim from outside observation alone

- Factory yield percentages
- Specific PCB layer stackups for a sealed product
- Root-cause certainty ("the bus is broken") without more evidence
- Device Quartet EVT results (**PHYSICAL_PENDING**)

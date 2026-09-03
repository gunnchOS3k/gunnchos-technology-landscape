# Diagram — data → model → inference + trust boundary

Sketch or describe:

```text
[Person + safe prompt]
        |
        v
   (privacy boundary)
    /            \
Route L          Route C
local buffer     network / remote service
toy rules        hosted model (or FIXTURE)
inference out    streamed tokens
        \            /
         v          v
      comparison table + consent card
```

Mark which side claimed `data leaving device = Y`.

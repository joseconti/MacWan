---
schema: keel.sprint/1
items:
  - id: S-073
    title: Speech to Video (Wan2.2 S2V)
    status: not-started
    hours: 8
    actual_hours: null
    actual_source: measured
    depends_on: []
    criteria: []
    target: v1.x
    reason: no Mac-capable pipeline exists yet; needs a port or an upstream diffusers pipeline
  - id: S-074
    title: Wan-Animate-2
    status: not-started
    hours: 6
    actual_hours: null
    actual_source: measured
    depends_on: []
    criteria: []
    target: v1.x
    reason: waiting for diffusers support and RAM validation
  - id: S-075
    title: Cloud engine (Alibaba Model Studio, Wan 2.5–3.0)
    status: not-started
    hours: 10
    actual_hours: null
    actual_source: measured
    depends_on: []
    criteria: []
    target: v1.x
    reason: D-008 — José chose v1.x
  - id: S-076
    title: LoRA training
    status: not-started
    hours: 12
    actual_hours: null
    actual_source: measured
    depends_on: []
    criteria: []
    target: null
    reason: out of v1 scope; no target version proposed
  - id: S-077
    title: Wan-Dancer
    status: not-started
    hours: 8
    actual_hours: null
    actual_source: measured
    depends_on: []
    criteria: []
    target: null
    reason: CUDA-only upstream; revisit when a Mac path exists
  - id: S-078
    title: Multi-shot storyboard
    status: not-started
    hours: 8
    actual_hours: null
    actual_source: measured
    depends_on: []
    criteria: []
    target: null
    reason: out of v1 scope
  - id: S-079
    title: Agent / MCP control of the app
    status: not-started
    hours: 8
    actual_hours: null
    actual_source: measured
    depends_on: []
    criteria: []
    target: null
    reason: out of v1 scope
  - id: S-080
    title: Product website (Keel Phase 8)
    status: not-started
    hours: 16
    actual_hours: null
    actual_source: measured
    depends_on: []
    criteria: []
    target: after v1.0
    reason: D-008 — website intent yes, at a later date
---

# Deferred backlog

Everything wanted and not in v1. Ids share one namespace with the sprint slices, so promoting an
item is a move that keeps its id. Hours are a first rough figure of what the item would cost (AI
working time plus supervision) and are **not** part of the plan total.

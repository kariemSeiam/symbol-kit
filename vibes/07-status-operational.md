---
vibe: status-operational
weight: W1–W2
---

# 07 — Status Operational

> Green/red signal carried by fill state. Severity ladders, retry notices, SRE dashboards. Datadog, PagerDuty, Grafana.

## Signature

`● ◐ ○ ⊘ ▰▱ ⚠ ⚡ ↻`

## Philosophy

Status-operational is the language of uptime. Every glyph answers a binary or ternary question: up, degraded, or down? The signal is in the fill state, not the color (this is the monochrome guarantee).

This vibe is the default for health pages, monitoring dashboards, and incident response.

## When to Choose

- Health checks and status pages
- Build pipelines and CI/CD dashboards
- Alert severity indicators
- Any UI where "is it working?" is the primary question

## When Not to Choose

- Decorative contexts (the severity reads as alarmist)
- Game or entertainment UIs (too clinical)
- Arabic-primary text without RTL-aware arrows

## Starter Set

### Severity dots (primary)
● ◐ ○ ⊘

### Progress (modern-minimal borrow)
▰ ▱

### Alert
⚠ ⚡

### Retry / spin
↻

### Check / cross
✓ ✗

### Separators
· —

### Full set count: ~30 atoms

## Worked Widgets

### Widget 1: Service Grid

```text
● geolink-api   ◐ hvar-cron   ○ taxi-arab
```

Vibe: status-operational · Weight: W1 · Atoms: ●◐○

### Widget 2: Pipeline Stage

```text
▰▰▰▰▰▰▱▱▱▱  build  60%
```

Vibe: status-operational · Weight: W2 · Atoms: ▰▱·

### Widget 3: Incident Card

```text
⚠ DEGRADED
↻ retry in 30s
```

Vibe: status-operational · Weight: W1 · Atoms: ⚠↻·

## Do Not Mix With

- **maximalist-decorative** — ornaments dilute the urgency signal
- **game-ui** — suits and stars confuse the severity read
- **scientific-technical** — math symbols add no operational value

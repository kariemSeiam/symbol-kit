# Standard Library

## STATUS_DOT(state) → string

```text
STATUS_DOT("live")    → ●
STATUS_DOT("idle")    → ◐
STATUS_DOT("offline") → ○
STATUS_DOT("error")   → ⊘
```

## PROGRESS(pct, n=10) → string

```text
PROGRESS(0.6)      → ▰▰▰▰▰▰▱▱▱▱
PROGRESS(0.23, 20) → ▰▰▰▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱
```

## SEVERITY(level, max=4) → string

```text
SEVERITY(2)     → ●●○○
SEVERITY(3, 5)  → ●●●○○
SEVERITY(0, 3)  → ○○○
```

## BAR(value, max, n=20) → string

```text
BAR(12, 20, 10)  → ▓▓▓▓▓▓░░░░
BAR(0.6, 1.0, 8) → ▓▓▓▓▓░░░
```

## SPARK(values) → string

```text
SPARK([0.1, 0.5, 0.9, 0.3]) → ▂▄▇▃
```

Maps normalized values to the sparkline ladder: ▁▂▃▄▅▆▇█

## TREE(depth, last) → string

```text
TREE(1, false) → ├──
TREE(1, true)  → └──
TREE(2, false) → │   ├──
TREE(2, true)  → │   └──
```

## KASHIDA_FILL(text, width) → string

```text
KASHIDA_FILL("جيولينك", 15) → جيولينكـــــــــ
```

## RATING(stars, max=5) → string

```text
RATING(3)     → ●●●○○
RATING(4, 10) → ●●●●○○○○○○
```

## RETRY_NOTICE(seconds) → string

```text
RETRY_NOTICE(30) → ↻ 30s
```

## HEALTH_DOT(status) → string

Alias for STATUS_DOT.

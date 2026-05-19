---
vibe: game-ui
weight: W2–W3
---

# 06 — Game UI

> Chess pieces, card suits, hearts, weather, retro game feel. Playful, competitive, nostalgic.

## Signature

`♠♣♥♦ ♔♕ ★☆ ⚔ ⚒ ⚓`

## Philosophy

Game-ui borrows from the oldest symbol systems — cards, chess, dice. These glyphs carry cultural weight. A ♠ is not just a shape; it is a suit. A ★ is not just a star; it is a reward.

## When to Choose

- Achievement and reward systems
- Game lobbies and matchmaking
- Inventory and equipment screens
- Leaderboards

## When Not to Choose

- Enterprise dashboards (undermines professionalism)
- Scientific contexts (meaning collision)
- Minimal UIs (too visually heavy)

## Starter Set

### Card suits
♠ ♣ ♥ ♦

### Chess pieces
♔ ♕ ♖ ♗ ♘ ♙

### Stars (rewards)
★ ☆

### Weapons & tools
⚔ ⚒ ⚓

### Weather
☀ ☁ ☂ ☃

### Status (universal)
● ○ ✓ ✗

### Full set count: ~40 atoms

## Worked Widgets

### Widget 1: Card Hand

```text
♠ A  ♥ K  ♦ Q  ♣ J
```

Vibe: game-ui · Weight: W2 · Atoms: ♠♥♦♣

### Widget 2: Leaderboard Rank

```text
★ 1.  PlayerOne   9999
☆ 2.  PlayerTwo   8750
☆ 3.  PlayerThree 8200
```

Vibe: game-ui · Weight: W2 · Atoms: ★☆·

### Widget 3: Equipment Slot

```text
[⚔] Sword of Flames
[⚓] Anchor of Depths
```

Vibe: game-ui · Weight: W2 · Atoms: [⚔⚓]

## Do Not Mix With

- **scientific-technical** — chess pieces in equations are nonsense
- **diff-patch** — game symbols in code review are noise
- **terminal-hacker** — many game glyphs lack monospace alignment

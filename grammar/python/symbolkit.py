"""
symbolkit — reference implementation in pure Python.
No dependencies. ~200 LOC.
"""

import re
from typing import Any, Callable, Dict, List


class SymbolKitError(Exception):
    pass


class Env:
    def __init__(self):
        self.atoms: Dict[str, str] = {}
        self.functions: Dict[str, Callable] = {}

    def register_atom(self, name: str, glyph: str):
        self.atoms[name] = glyph

    def register_function(self, name: str, fn: Callable):
        self.functions[name] = fn


def _default_env() -> Env:
    e = Env()
    # Tier 0 atoms
    e.register_atom("black-circle", "●")
    e.register_atom("white-circle", "○")
    e.register_atom("circle-with-left-half-black", "◐")
    e.register_atom("check-mark", "✓")
    e.register_atom("ballot-x", "✗")
    e.register_atom("warning-sign", "⚠")
    e.register_atom("rightwards-arrow", "→")
    e.register_atom("middle-dot", "·")
    e.register_atom("em-dash", "—")
    e.register_atom("black-parallelogram", "▰")
    e.register_atom("white-parallelogram", "▱")
    e.register_atom("midline-horizontal-ellipsis", "⋯")
    # Additional atoms
    e.register_atom("full-block", "█")
    e.register_atom("dark-shade", "▓")
    e.register_atom("light-shade", "░")
    e.register_atom("leftwards-arrow", "←")
    e.register_atom("upwards-arrow", "↑")
    e.register_atom("downwards-arrow", "↓")
    e.register_atom("horizontal-ellipsis", "…")
    e.register_atom("bullet", "•")
    e.register_atom("en-dash", "–")

    # stdlib
    def STATUS_DOT(state: str) -> str:
        return {"live": "●", "idle": "◐", "offline": "○", "error": "⊘"}.get(state, "○")

    def PROGRESS(pct: float, n: int = 10) -> str:
        filled = round(pct * n)
        return "▰" * filled + "▱" * (n - filled)

    def SEVERITY(level: int, max_: int = 4) -> str:
        return "●" * level + "○" * (max_ - level)

    def BAR(value: float, max_: float, n: int = 20) -> str:
        filled = round((value / max_) * n) if max_ else 0
        return "▓" * filled + "░" * (n - filled)

    def SPARK(values: List[float]) -> str:
        ladder = "▁▂▃▄▅▆▇█"
        out = ""
        for v in values:
            idx = min(int(v * (len(ladder) - 1)), len(ladder) - 1)
            out += ladder[idx]
        return out

    def TREE(depth: int, last: bool) -> str:
        indent = "│   " * (depth - 1)
        branch = "└── " if last else "├── "
        return indent + branch

    def KASHIDA_FILL(text: str, width: int) -> str:
        pad = max(0, width - len(text))
        return text + "ـ" * pad

    def RATING(stars: int, max_: int = 5) -> str:
        return "●" * stars + "○" * (max_ - stars)

    def RETRY_NOTICE(seconds: int) -> str:
        return f"↻ {seconds}s"

    def HEALTH_DOT(status: str) -> str:
        return STATUS_DOT(status)

    e.register_function("STATUS_DOT", STATUS_DOT)
    e.register_function("PROGRESS", PROGRESS)
    e.register_function("SEVERITY", SEVERITY)
    e.register_function("BAR", BAR)
    e.register_function("SPARK", SPARK)
    e.register_function("TREE", TREE)
    e.register_function("KASHIDA_FILL", KASHIDA_FILL)
    e.register_function("RATING", RATING)
    e.register_function("RETRY_NOTICE", RETRY_NOTICE)
    e.register_function("HEALTH_DOT", HEALTH_DOT)

    return e


ENV = _default_env()


def tokenize(expr: str) -> List[str]:
    pattern = r'"(?:\\.|[^"\\])*"|\(|\)|,|×|\+|@|[A-Za-z0-9_\-]+'
    return re.findall(pattern, expr)


def _parse_and_eval(tokens: List[str], pos: int, env: Env) -> tuple[str, int]:
    if pos >= len(tokens):
        raise SymbolKitError("Unexpected end of expression")

    tok = tokens[pos]

    if tok.startswith('"'):
        return tok[1:-1], pos + 1

    if tok == "@":
        name = tokens[pos + 1]
        glyph = env.atoms.get(name)
        if glyph is None:
            raise SymbolKitError(f"Unknown atom: {name}")
        return glyph, pos + 2

    if tok in env.functions:
        fn = env.functions[tok]
        if tokens[pos + 1] != "(":
            raise SymbolKitError(f"Expected ( after {tok}")
        pos += 2
        args: List[Any] = []
        while pos < len(tokens) and tokens[pos] != ")":
            if tokens[pos] == ",":
                pos += 1
                continue
            val, pos = _parse_and_eval(tokens, pos, env)
            if isinstance(val, str):
                if val.isdigit():
                    val = int(val)
                else:
                    try:
                        val = float(val)
                    except ValueError:
                        pass
            args.append(val)
        if pos >= len(tokens) or tokens[pos] != ")":
            raise SymbolKitError("Missing )")
        return fn(*args), pos + 1

    if tok.isdigit():
        return str(int(tok)), pos + 1
    try:
        return str(float(tok)), pos + 1
    except ValueError:
        return tok, pos + 1


def render(expr: str, env: Env = None) -> str:
    env = env or ENV
    tokens = tokenize(expr)
    if not tokens:
        return ""
    result, pos = _parse_and_eval(tokens, 0, env)
    while pos < len(tokens):
        op = tokens[pos]
        if op == "+":
            rhs, pos = _parse_and_eval(tokens, pos + 1, env)
            result = str(result) + str(rhs)
        elif op == "×":
            count = int(tokens[pos + 1])
            result = str(result) * count
            pos += 2
        else:
            break
    return str(result)

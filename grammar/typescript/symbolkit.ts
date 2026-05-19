/**
 * symbolkit — reference implementation in TypeScript.
 * Pure TS, no runtime dependencies.
 */

export type AtomMap = Map<string, string>;
export type FnMap = Map<string, (...args: any[]) => string>;

export class Env {
  atoms: AtomMap = new Map();
  functions: FnMap = new Map();

  registerAtom(name: string, glyph: string): void {
    this.atoms.set(name, glyph);
  }

  registerFunction(name: string, fn: (...args: any[]) => string): void {
    this.functions.set(name, fn);
  }
}

export class SymbolKitError extends Error {}

function defaultEnv(): Env {
  const e = new Env();

  // Tier 0 atoms
  e.registerAtom("black-circle", "●");
  e.registerAtom("white-circle", "○");
  e.registerAtom("circle-with-left-half-black", "◐");
  e.registerAtom("check-mark", "✓");
  e.registerAtom("ballot-x", "✗");
  e.registerAtom("warning-sign", "⚠");
  e.registerAtom("rightwards-arrow", "→");
  e.registerAtom("middle-dot", "·");
  e.registerAtom("em-dash", "—");
  e.registerAtom("black-parallelogram", "▰");
  e.registerAtom("white-parallelogram", "▱");
  e.registerAtom("midline-horizontal-ellipsis", "⋯");
  // Additional
  e.registerAtom("full-block", "█");
  e.registerAtom("dark-shade", "▓");
  e.registerAtom("light-shade", "░");
  e.registerAtom("leftwards-arrow", "←");
  e.registerAtom("upwards-arrow", "↑");
  e.registerAtom("downwards-arrow", "↓");
  e.registerAtom("horizontal-ellipsis", "…");
  e.registerAtom("bullet", "•");
  e.registerAtom("en-dash", "–");

  // stdlib
  e.registerFunction("STATUS_DOT", (state: string) => {
    return { live: "●", idle: "◐", offline: "○", error: "⊘" }[state] ?? "○";
  });

  e.registerFunction("PROGRESS", (pct: number, n: number = 10) => {
    const filled = Math.round(pct * n);
    return "▰".repeat(filled) + "▱".repeat(n - filled);
  });

  e.registerFunction("SEVERITY", (level: number, max: number = 4) => {
    return "●".repeat(level) + "○".repeat(max - level);
  });

  e.registerFunction("BAR", (value: number, max: number, n: number = 20) => {
    const filled = max ? Math.round((value / max) * n) : 0;
    return "▓".repeat(filled) + "░".repeat(n - filled);
  });

  e.registerFunction("SPARK", (...values: number[]) => {
    const ladder = "▁▂▃▄▅▆▇█";
    return values
      .map((v) => ladder[Math.min(Math.round(v * (ladder.length - 1)), ladder.length - 1)])
      .join("");
  });

  e.registerFunction("TREE", (depth: number, last: boolean) => {
    const indent = "│   ".repeat(depth - 1);
    const branch = last ? "└── " : "├── ";
    return indent + branch;
  });

  e.registerFunction("KASHIDA_FILL", (text: string, width: number) => {
    const pad = Math.max(0, width - text.length);
    return text + "ـ".repeat(pad);
  });

  e.registerFunction("RATING", (stars: number, max: number = 5) => {
    return "●".repeat(stars) + "○".repeat(max - stars);
  });

  e.registerFunction("RETRY_NOTICE", (seconds: number) => {
    return `↻ ${seconds}s`;
  });

  e.registerFunction("HEALTH_DOT", (status: string) => {
    return e.functions.get("STATUS_DOT")!(status);
  });

  return e;
}

const GLOBAL_ENV = defaultEnv();

function tokenize(expr: string): string[] {
  const pattern = /"(?:\\.|[^"\\])*"|\d+\.\d+|\(|\)|,|×|\+|@|[A-Za-z0-9_\-]+/g;
  return expr.match(pattern) ?? [];
}

function parseAndEval(tokens: string[], pos: number, env: Env): [string, number] {
  if (pos >= tokens.length) throw new SymbolKitError("Unexpected end of expression");

  const tok = tokens[pos];

  if (tok.startsWith('"')) return [tok.slice(1, -1), pos + 1];

  if (tok === "@") {
    const name = tokens[pos + 1];
    const glyph = env.atoms.get(name);
    if (!glyph) throw new SymbolKitError(`Unknown atom: ${name}`);
    return [glyph, pos + 2];
  }

  if (env.functions.has(tok)) {
    const fn = env.functions.get(tok)!;
    if (tokens[pos + 1] !== "(") throw new SymbolKitError(`Expected ( after ${tok}`);
    let p = pos + 2;
    const args: any[] = [];
    while (p < tokens.length && tokens[p] !== ")") {
      if (tokens[p] === ",") {
        p++;
        continue;
      }
      const [val, np] = parseAndEval(tokens, p, env);
      args.push(val);
      p = np;
    }
    if (p >= tokens.length || tokens[p] !== ")") throw new SymbolKitError("Missing )");
    return [fn(...args), p + 1];
  }

  if (tok === "true" || tok === "false") return [tok === "true", pos + 1];
  if (/^\d+$/.test(tok)) return [parseInt(tok, 10), pos + 1];
  if (!isNaN(Number(tok))) return [Number(tok), pos + 1];
  return [tok, pos + 1];
}

export function render(expr: string, env: Env = GLOBAL_ENV): string {
  const tokens = tokenize(expr);
  if (!tokens.length) return "";
  let [result, pos] = parseAndEval(tokens, 0, env);
  while (pos < tokens.length) {
    const op = tokens[pos];
    if (op === "+") {
      const [rhs, np] = parseAndEval(tokens, pos + 1, env);
      result += rhs;
      pos = np;
    } else if (op === "×") {
      const count = parseInt(tokens[pos + 1], 10);
      result = result.repeat(count);
      pos += 2;
    } else {
      break;
    }
  }
  return result;
}

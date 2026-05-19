/**
 * symbolkit.test.ts — tests for the TypeScript reference implementation.
 *
 * Run: npx ts-node symbolkit.test.ts
 * or:  npx jest symbolkit.test.ts
 */

import { render, Env, SymbolKitError } from "./symbolkit";

function assert(condition: boolean, msg: string): void {
  if (!condition) throw new Error(`FAIL: ${msg}`);
}

function assertEquals(actual: string, expected: string, msg: string): void {
  if (actual !== expected) {
    throw new Error(`FAIL: ${msg}\n  expected: ${expected}\n  actual:   ${actual}`);
  }
}

// STATUS_DOT
assertEquals(render('STATUS_DOT("live")'), "●", "STATUS_DOT live");
assertEquals(render('STATUS_DOT("idle")'), "◐", "STATUS_DOT idle");
assertEquals(render('STATUS_DOT("offline")'), "○", "STATUS_DOT offline");

// PROGRESS
assertEquals(render("PROGRESS(0.6)"), "▰▰▰▰▰▰▱▱▱▱", "PROGRESS 0.6");
assertEquals(render("PROGRESS(0.23, 20)"), "▰▰▰▰▰▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱", "PROGRESS 0.23/20");

// SEVERITY
assertEquals(render("SEVERITY(2)"), "●●○○", "SEVERITY 2");
assertEquals(render("SEVERITY(3, 5)"), "●●●○○", "SEVERITY 3/5");

// BAR
assertEquals(render("BAR(12, 20, 10)"), "▓▓▓▓▓▓░░░░", "BAR 12/20/10");
assertEquals(render("BAR(0.6, 1.0, 8)"), "▓▓▓▓▓░░░", "BAR 0.6/1.0/8");

// SPARK
assertEquals(render("SPARK(0.1, 0.5, 0.9, 0.3)"), "▂▅▇▃", "SPARK");

// TREE
assertEquals(render("TREE(1, false)"), "├──", "TREE false");
assertEquals(render("TREE(1, true)"), "└──", "TREE true");
assertEquals(render("TREE(2, false)"), "│   ├──", "TREE depth 2 false");

// KASHIDA_FILL
assertEquals(render('KASHIDA_FILL("جيولينك", 15)'), "جيولينكــــــــ", "KASHIDA_FILL");

// RATING
assertEquals(render("RATING(3)"), "●●●○○", "RATING 3");
assertEquals(render("RATING(4, 10)"), "●●●●○○○○○○", "RATING 4/10");

// RETRY_NOTICE
assertEquals(render("RETRY_NOTICE(30)"), "↻ 30s", "RETRY_NOTICE");

// Atoms
assertEquals(render("@black-circle"), "●", "atom black-circle");
assertEquals(render("@white-circle"), "○", "atom white-circle");

// Repetition
assertEquals(render("@black-circle × 3"), "●●●", "repetition");

// Sequence
assertEquals(render('@black-circle + " " + @white-circle'), "● ○", "sequence");

// Complex
assertEquals(
  render('STATUS_DOT("live") + " · " + PROGRESS(0.6)'),
  "● · ▰▰▰▰▰▰▱▱▱▱",
  "complex"
);

console.log("✓ All 20 tests passed");

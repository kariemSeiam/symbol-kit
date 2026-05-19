#!/usr/bin/env python3
"""
validate-atom.py — enforce the §3 atom schema from CLAUDE.md.

Every YAML in atoms/ (recursively) is checked against the canonical schema.
A single missing or wrong-typed field fails the build. There are no warnings.

Usage:
    python3 scripts/validate-atom.py atoms/
    python3 scripts/validate-atom.py atoms/black-circle.yaml
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Iterable

import yaml


WEIGHT_CLASSES = {"W0", "W1", "W2", "W3", "W4"}
WIDTH_CLASSES = {"narrow", "variable", "2ch", "emoji-wide"}
FORM_VALUES = {"text", "emoji"}
TIERS = {0, 1, 2, 3, 4}
RENDERS_VALUES = {True, "tofu", "fallback", "unverified"}

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[A-Za-z0-9.\-]+)?$")
UNICODE_VERSION_RE = re.compile(r"^\d+\.\d+$")
CODEPOINT_RE = re.compile(r"^U\+[0-9A-F]{4,6}(?: U\+[0-9A-F]{4,6})*$")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TEST_ID_RE = re.compile(r"^PLAT-\d{3,}$")
PLATFORM_KEY_RE = re.compile(r"^[a-z][a-z0-9_]*$")


class AtomError(Exception):
    def __init__(self, path: Path, field: str, message: str):
        self.path = path
        self.field = field
        self.message = message
        super().__init__(f"{path}: [{field}] {message}")


def fail(path: Path, field: str, message: str) -> AtomError:
    return AtomError(path, field, message)


def require(path: Path, doc: dict, key: str) -> Any:
    if key not in doc:
        raise fail(path, key, "missing required field")
    return doc[key]


def require_type(path: Path, value: Any, field: str, types: type | tuple[type, ...]) -> Any:
    if not isinstance(value, types):
        names = (
            types.__name__ if isinstance(types, type)
            else " | ".join(t.__name__ for t in types)
        )
        raise fail(path, field, f"must be {names}, got {type(value).__name__}")
    return value


def require_list_of_str(path: Path, value: Any, field: str, allow_empty: bool = True) -> list[str]:
    require_type(path, value, field, list)
    for i, item in enumerate(value):
        if not isinstance(item, str):
            raise fail(path, f"{field}[{i}]", f"must be string, got {type(item).__name__}")
        if not item.strip():
            raise fail(path, f"{field}[{i}]", "must be non-empty string")
    if not allow_empty and len(value) == 0:
        raise fail(path, field, "must have at least one entry")
    return value


def require_enum(path: Path, value: Any, field: str, allowed: Iterable[Any]) -> Any:
    if value not in allowed:
        allowed_str = ", ".join(repr(a) for a in allowed)
        raise fail(path, field, f"must be one of [{allowed_str}], got {value!r}")
    return value


def glyph_codepoints(glyph: str) -> list[int]:
    return [ord(ch) for ch in glyph]


def codepoint_string(cps: Iterable[int]) -> str:
    return " ".join(f"U+{cp:04X}" for cp in cps)


def kebab_from_name(name: str) -> str:
    return name.lower().replace(" ", "-")


def validate_form(path: Path, form: Any) -> None:
    require_type(path, form, "form", dict)
    default = require(path, form, "form.default" if False else "default")
    if "default" not in form:
        raise fail(path, "form.default", "missing")
    require_enum(path, form["default"], "form.default", FORM_VALUES)

    if "variation_selectors" not in form:
        raise fail(path, "form.variation_selectors", "missing")
    require_type(path, form["variation_selectors"], "form.variation_selectors", dict)
    for k, v in form["variation_selectors"].items():
        if not isinstance(k, str):
            raise fail(path, f"form.variation_selectors[{k!r}]", "key must be string")
        require_enum(path, v, f"form.variation_selectors[{k}]", FORM_VALUES)

    if "emoji_form_exists" not in form:
        raise fail(path, "form.emoji_form_exists", "missing")
    require_type(path, form["emoji_form_exists"], "form.emoji_form_exists", bool)


def validate_semantic(path: Path, sem: Any) -> None:
    require_type(path, sem, "semantic", dict)
    if "primary" not in sem:
        raise fail(path, "semantic.primary", "missing")
    require_type(path, sem["primary"], "semantic.primary", str)
    if not sem["primary"].strip():
        raise fail(path, "semantic.primary", "must be non-empty")
    if "also" not in sem:
        raise fail(path, "semantic.also", "missing")
    require_list_of_str(path, sem["also"], "semantic.also")
    if "not" not in sem:
        raise fail(path, "semantic.not", "missing")
    require_list_of_str(path, sem["not"], "semantic.not")


def validate_pairs_with(path: Path, pw: Any) -> None:
    require_type(path, pw, "pairs_with", dict)
    for required in ("complement", "next_in_set", "family"):
        if required not in pw:
            raise fail(path, f"pairs_with.{required}", "missing")
    comp = pw["complement"]
    if comp is not None and not isinstance(comp, str):
        raise fail(path, "pairs_with.complement", "must be string or null")
    if isinstance(comp, str) and not comp.strip():
        raise fail(path, "pairs_with.complement", "must be non-empty string or null")
    require_list_of_str(path, pw["next_in_set"], "pairs_with.next_in_set")
    require_list_of_str(path, pw["family"], "pairs_with.family")


def validate_platforms(path: Path, platforms: Any) -> None:
    require_type(path, platforms, "platforms", dict)
    if not platforms:
        raise fail(path, "platforms", "must list at least one platform")
    for name, record in platforms.items():
        if not isinstance(name, str) or not PLATFORM_KEY_RE.match(name):
            raise fail(path, f"platforms.{name!r}", "platform key must be snake_case identifier")
        require_type(path, record, f"platforms.{name}", dict)
        if "renders" not in record:
            raise fail(path, f"platforms.{name}.renders", "missing")
        renders = record["renders"]
        require_enum(path, renders, f"platforms.{name}.renders", RENDERS_VALUES)
        if renders == "unverified":
            if "test_id" in record and record["test_id"] is not None:
                raise fail(
                    path,
                    f"platforms.{name}.test_id",
                    "must be omitted or null when renders=unverified",
                )
        else:
            if "test_id" not in record:
                raise fail(path, f"platforms.{name}.test_id", "required when renders is verified")
            tid = record["test_id"]
            if not isinstance(tid, str) or not TEST_ID_RE.match(tid):
                raise fail(
                    path,
                    f"platforms.{name}.test_id",
                    f"must match {TEST_ID_RE.pattern}, got {tid!r}",
                )


def validate_rtl_behavior(path: Path, rtl: Any) -> None:
    require_type(path, rtl, "rtl_behavior", dict)
    for required in ("mirrors", "arabic_equivalent", "safe_in_rtl"):
        if required not in rtl:
            raise fail(path, f"rtl_behavior.{required}", "missing")
    require_type(path, rtl["mirrors"], "rtl_behavior.mirrors", bool)
    ae = rtl["arabic_equivalent"]
    if ae is not None and not isinstance(ae, str):
        raise fail(path, "rtl_behavior.arabic_equivalent", "must be string or null")
    require_type(path, rtl["safe_in_rtl"], "rtl_behavior.safe_in_rtl", bool)


def validate_examples(path: Path, examples: Any) -> None:
    require_type(path, examples, "examples", list)
    if len(examples) < 2 or len(examples) > 4:
        raise fail(path, "examples", f"must have 2–4 entries, got {len(examples)}")
    for i, ex in enumerate(examples):
        require_type(path, ex, f"examples[{i}]", dict)
        for key in ("context", "snippet"):
            if key not in ex:
                raise fail(path, f"examples[{i}].{key}", "missing")
            require_type(path, ex[key], f"examples[{i}].{key}", str)
            if not ex[key].strip():
                raise fail(path, f"examples[{i}].{key}", "must be non-empty")


def validate_cross_references(path: Path, xrefs: Any) -> None:
    require_type(path, xrefs, "cross_references", dict)
    for required in ("pairs", "sets", "widgets"):
        if required not in xrefs:
            raise fail(path, f"cross_references.{required}", "missing")
        require_list_of_str(path, xrefs[required], f"cross_references.{required}")


def validate_atom_file(path: Path) -> list[AtomError]:
    errors: list[AtomError] = []

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        return [fail(path, "<file>", f"cannot read: {e}")]

    try:
        doc = yaml.safe_load(text)
    except yaml.YAMLError as e:
        return [fail(path, "<yaml>", f"parse error: {e}")]

    if not isinstance(doc, dict):
        return [fail(path, "<root>", "must be a YAML mapping")]

    try:
        glyph = require(path, doc, "glyph")
        require_type(path, glyph, "glyph", str)
        if not glyph:
            raise fail(path, "glyph", "must be non-empty")

        name = require(path, doc, "name")
        require_type(path, name, "name", str)
        if name != name.upper():
            raise fail(path, "name", f"must be UPPERCASE Unicode name, got {name!r}")

        codepoint = require(path, doc, "codepoint")
        require_type(path, codepoint, "codepoint", str)
        if not CODEPOINT_RE.match(codepoint):
            raise fail(path, "codepoint", f"must match {CODEPOINT_RE.pattern}, got {codepoint!r}")

        declared_cps = [int(part[2:], 16) for part in codepoint.split(" ")]
        actual_cps = glyph_codepoints(glyph)
        non_vs_actual = [cp for cp in actual_cps if not (0xFE00 <= cp <= 0xFE0F)]
        if declared_cps != non_vs_actual:
            raise fail(
                path,
                "codepoint",
                f"declared {codepoint} but glyph encodes {codepoint_string(actual_cps)}",
            )

        try:
            official = unicodedata.name(glyph[0])
        except ValueError:
            official = None
        if official is not None and official != name:
            raise fail(
                path,
                "name",
                f"must equal Unicode name {official!r} for {codepoint}, got {name!r}",
            )

        expected_stem = kebab_from_name(name)
        if path.stem != expected_stem:
            raise fail(
                path,
                "<filename>",
                f"file stem must be {expected_stem!r}, got {path.stem!r}",
            )

        require_type(path, require(path, doc, "unicode_block"), "unicode_block", str)
        uv = require(path, doc, "unicode_version")
        require_type(path, uv, "unicode_version", str)
        if not UNICODE_VERSION_RE.match(uv):
            raise fail(path, "unicode_version", f"must match X.Y, got {uv!r}")

        require_list_of_str(path, require(path, doc, "aliases"), "aliases", allow_empty=False)

        validate_form(path, require(path, doc, "form"))

        require_enum(path, require(path, doc, "weight_class"), "weight_class", WEIGHT_CLASSES)
        require_enum(path, require(path, doc, "width_class"), "width_class", WIDTH_CLASSES)
        require_enum(path, require(path, doc, "tier"), "tier", TIERS)

        validate_semantic(path, require(path, doc, "semantic"))
        validate_pairs_with(path, require(path, doc, "pairs_with"))

        require_list_of_str(path, require(path, doc, "visual_neighbors"), "visual_neighbors")
        require_list_of_str(path, require(path, doc, "prefer_over"), "prefer_over")
        require_list_of_str(path, require(path, doc, "prefer_under"), "prefer_under")
        require_list_of_str(path, require(path, doc, "anti_uses"), "anti_uses", allow_empty=False)

        validate_platforms(path, require(path, doc, "platforms"))
        validate_rtl_behavior(path, require(path, doc, "rtl_behavior"))

        require_type(
            path, require(path, doc, "copy_paste_safe"), "copy_paste_safe", bool
        )
        require_type(
            path,
            require(path, doc, "monochrome_guaranteed"),
            "monochrome_guaranteed",
            bool,
        )

        require_list_of_str(path, require(path, doc, "vibes"), "vibes", allow_empty=False)

        validate_examples(path, require(path, doc, "examples"))
        validate_cross_references(path, require(path, doc, "cross_references"))

        added_in = require(path, doc, "added_in")
        require_type(path, added_in, "added_in", str)
        if not SEMVER_RE.match(added_in):
            raise fail(path, "added_in", f"must be semver MAJOR.MINOR.PATCH, got {added_in!r}")

        last_verified = require(path, doc, "last_verified")
        if isinstance(last_verified, _dt.date):
            pass
        elif isinstance(last_verified, str) and ISO_DATE_RE.match(last_verified):
            try:
                _dt.date.fromisoformat(last_verified)
            except ValueError as e:
                raise fail(path, "last_verified", f"invalid date: {e}")
        else:
            raise fail(
                path,
                "last_verified",
                f"must be ISO date YYYY-MM-DD, got {last_verified!r}",
            )

    except AtomError as e:
        errors.append(e)

    return errors


def iter_atom_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target] if target.suffix in (".yaml", ".yml") else []
    return sorted(p for p in target.rglob("*.yaml") if p.is_file())


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate atom YAML files against §3 schema.")
    parser.add_argument("target", type=Path, help="atoms/ directory or a single .yaml file")
    parser.add_argument(
        "--quiet", action="store_true", help="suppress per-file OK output"
    )
    args = parser.parse_args(argv)

    if not args.target.exists():
        print(f"error: {args.target} does not exist", file=sys.stderr)
        return 2

    files = iter_atom_files(args.target)
    if not files:
        print(f"error: no .yaml files found under {args.target}", file=sys.stderr)
        return 2

    total_errors = 0
    for path in files:
        errs = validate_atom_file(path)
        if errs:
            for e in errs:
                print(f"FAIL {e.path}\n     [{e.field}] {e.message}", file=sys.stderr)
            total_errors += len(errs)
        elif not args.quiet:
            print(f"ok   {path}")

    if total_errors:
        print(
            f"\n{total_errors} error(s) across {len(files)} file(s).",
            file=sys.stderr,
        )
        return 1

    print(f"\n{len(files)} atom(s) valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

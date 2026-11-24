#!/usr/bin/env python3
"""Skill novelty tooling: static scan, item extraction, and two-arm scoring.

Standard library only. Makes no network or model calls; the model runs and the
judging are performed by whatever agent or eval harness the caller uses.

Subcommands:
  scan   Heuristic specificity report for SKILL.md files (no model needed).
  items  Decompose one SKILL.md into JSONL item stubs for question authoring.
  score  Classify graded with/without results into the four novelty quadrants.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

FENCE = re.compile(r"^\s*(```|~~~)")
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(.*)")
TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$")
TABLE_RULE = re.compile(r"^\s*\|?[\s:|-]+\|?\s*$")

# Signals that a line carries content a model cannot derive from general knowledge.
SPECIFIC_SIGNALS = [
    re.compile(r"`[^`]+`"),  # inline code: names, flags, paths
    re.compile(r"\b\d+(?:\.\d+)?\s*(?:%|ms|s|sec|min|kb|mb|gb|x|days?|hours?)\b", re.I),
    re.compile(r"\b\d{2,}\b"),  # thresholds, limits, versions, codes
    re.compile(r"(?:[\w.-]+[\\/]){1,}[\w.-]+"),  # paths
    re.compile(r"https?://"),
    re.compile(r"\b[A-Z][A-Z0-9_]{3,}\b"),  # constants, env vars
    re.compile(r"\b(?:this repo|this repository|our|we use|company|internal)\b", re.I),
]
# Phrases typical of generic concept explanation.
GENERIC_SIGNALS = [
    re.compile(r"\b(?:is a|are a|refers to|is defined as|is the process of|is when|best practice|"
               r"it is important to|ensure that|make sure|in general|typically|"
               r"helps? (?:to )?(?:improve|ensure|reduce))\b", re.I),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def body_start(lines: list[str]) -> int:
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return i + 1
    return 0


def decompose(text: str) -> list[dict]:
    """Split a skill body into atomic-ish items: list entries, table rows,
    paragraphs, and fenced code blocks. Headings are kept as context only."""
    lines = text.split("\n")
    items: list[dict] = []
    heading = ""
    para: list[str] = []
    para_start = 0
    code: list[str] = []
    code_start = 0
    in_code = False

    def flush_para() -> None:
        nonlocal para
        if para:
            items.append({"line": para_start, "kind": "prose", "heading": heading,
                          "text": " ".join(s.strip() for s in para)})
            para = []

    for idx in range(body_start(lines), len(lines)):
        raw = lines[idx]
        n = idx + 1
        if FENCE.match(raw):
            if in_code:
                items.append({"line": code_start, "kind": "code", "heading": heading,
                              "text": "\n".join(code)})
                code, in_code = [], False
            else:
                flush_para()
                in_code, code_start = True, n
            continue
        if in_code:
            code.append(raw)
            continue
        if raw.startswith("#"):
            flush_para()
            heading = raw.lstrip("#").strip()
            continue
        if not raw.strip():
            flush_para()
            continue
        if TABLE_ROW.match(raw):
            flush_para()
            if not TABLE_RULE.match(raw):
                items.append({"line": n, "kind": "table-row", "heading": heading, "text": raw.strip()})
            continue
        m = LIST_ITEM.match(raw)
        if m:
            flush_para()
            items.append({"line": n, "kind": "list", "heading": heading, "text": m.group(1).strip()})
            continue
        if not para:
            para_start = n
        para.append(raw)
    flush_para()
    return items


def specificity(text: str) -> int:
    score = sum(1 for p in SPECIFIC_SIGNALS if p.search(text))
    score -= sum(1 for p in GENERIC_SIGNALS if p.search(text))
    return score


def classify(item: dict) -> str:
    if item["kind"] == "code":
        return "specific"
    return "specific" if specificity(item["text"]) >= 1 else "generic"


def approx_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def find_skills(paths: list[str]) -> list[Path]:
    found: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_file():
            found.append(p)
        elif p.is_dir():
            found.extend(sorted(p.rglob("SKILL.md")))
    return found


def cmd_scan(args: argparse.Namespace) -> int:
    rows = []
    for path in find_skills(args.paths):
        items = decompose(read_text(path))
        generic = [i for i in items if classify(i) == "generic"]
        tokens = sum(approx_tokens(i["text"]) for i in items)
        gen_tokens = sum(approx_tokens(i["text"]) for i in generic)
        rows.append({
            "skill": path.parent.name if path.name == "SKILL.md" else path.name,
            "path": str(path),
            "items": len(items),
            "tokens": tokens,
            "generic_items": len(generic),
            "generic_token_share": round(gen_tokens / tokens, 3) if tokens else 0.0,
            "candidates": [{"line": i["line"], "text": i["text"][:160]} for i in
                           sorted(generic, key=lambda i: -len(i["text"]))[: args.top]],
        })
    rows.sort(key=lambda r: (-r["generic_token_share"], -r["tokens"]))
    flagged = [r for r in rows if r["items"] >= args.min_items
               and r["generic_token_share"] >= args.max_generic_share]
    if args.json:
        json.dump({"skills": rows if args.all else flagged, "scanned": len(rows)}, sys.stdout, indent=2)
        print()
    else:
        print(f"scanned {len(rows)} skills; {len(flagged)} at or above "
              f"{args.max_generic_share:.0%} generic token share (min {args.min_items} items)")
        for r in (rows if args.all else flagged)[: args.limit]:
            print(f"\n{r['skill']}: {r['generic_token_share']:.0%} generic "
                  f"({r['generic_items']}/{r['items']} items, ~{r['tokens']} tokens)")
            for c in r["candidates"]:
                print(f"  L{c['line']}: {c['text']}")
    return 1 if args.fail_on_flagged and flagged else 0


def cmd_items(args: argparse.Namespace) -> int:
    path = Path(args.skill)
    skill = path.parent.name if path.name == "SKILL.md" else path.stem
    out = open(args.out, "w", encoding="utf-8", newline="\n") if args.out else sys.stdout
    try:
        for n, item in enumerate(decompose(read_text(path)), 1):
            if len(item["text"]) < args.min_chars:
                continue
            row = {"id": f"{skill}#{n}", "skill": skill, "line": item["line"], "kind": item["kind"],
                   "heading": item["heading"], "heuristic": classify(item), "text": item["text"],
                   "question": "", "expected": ""}
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
    finally:
        if args.out:
            out.close()
    return 0


GRADES = {"correct": 2, "concept": 1, "wrong": 0}


def quadrant(without: int, with_: int, threshold: int) -> str:
    wo, wi = without >= threshold, with_ >= threshold
    if wo and wi:
        return "already-known"
    if wo and not wi:
        return "harmful"
    if not wo and wi:
        return "novel"
    return "missed"


def cmd_score(args: argparse.Namespace) -> int:
    rows = []
    for ln, raw in enumerate(Path(args.results).read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        row = json.loads(raw)
        for key in ("without", "with"):
            if row.get(key) not in GRADES:
                sys.exit(f"{args.results}:{ln}: '{key}' must be one of {sorted(GRADES)}")
        rows.append(row)
    report = {}
    for label, threshold in (("lenient", 1), ("strict", 2)):
        total = Counter()
        per_skill: dict[str, Counter] = {}
        buckets: dict[str, list[str]] = {"already-known": [], "harmful": [], "novel": [], "missed": []}
        for r in rows:
            q = quadrant(GRADES[r["without"]], GRADES[r["with"]], threshold)
            total[q] += 1
            per_skill.setdefault(r.get("skill", "?"), Counter())[q] += 1
            buckets[q].append(r.get("id", "?"))
        n = len(rows) or 1
        report[label] = {
            "items": len(rows),
            "share": {k: round(total[k] / n, 3) for k in buckets},
            "novelty": round(total["novel"] / n, 3),
            "by_skill": {s: dict(c) for s, c in sorted(per_skill.items())},
            "ids": buckets,
        }
    if args.json:
        json.dump(report, sys.stdout, indent=2)
        print()
        return 0
    for label, data in report.items():
        print(f"[{label}] items={data['items']} novelty={data['novelty']:.0%}")
        for k, v in data["share"].items():
            print(f"  {k:<14}{v:>6.0%}  ({len(data['ids'][k])})")
    print("\nActions (strict grading):")
    print("  harmful       -> remove or rewrite first; strict improvement")
    print("  already-known -> trim concept explanation; keep only if it steers a process")
    print("  missed        -> rewrite so the item lands, or drop it")
    print("  novel         -> keep; this is the content being paid for")
    for k in ("harmful", "missed", "already-known"):
        ids = report["strict"]["ids"][k]
        if ids:
            print(f"\n{k}: {', '.join(ids[: args.list])}{' ...' if len(ids) > args.list else ''}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scan", help="heuristic specificity report")
    s.add_argument("paths", nargs="+", help="SKILL.md files or directories to search")
    s.add_argument("--max-generic-share", type=float, default=0.5)
    s.add_argument("--min-items", type=int, default=5)
    s.add_argument("--top", type=int, default=3, help="candidate lines per skill")
    s.add_argument("--limit", type=int, default=25, help="skills shown in text mode")
    s.add_argument("--all", action="store_true", help="include skills below the threshold")
    s.add_argument("--json", action="store_true")
    s.add_argument("--fail-on-flagged", action="store_true")
    s.set_defaults(fn=cmd_scan)

    i = sub.add_parser("items", help="emit JSONL item stubs for question authoring")
    i.add_argument("skill")
    i.add_argument("--out")
    i.add_argument("--min-chars", type=int, default=20)
    i.set_defaults(fn=cmd_items)

    c = sub.add_parser("score", help="score graded two-arm results (JSONL)")
    c.add_argument("results", help='rows: {"id","skill","without","with"}; grades: correct|concept|wrong')
    c.add_argument("--json", action="store_true")
    c.add_argument("--list", type=int, default=20)
    c.set_defaults(fn=cmd_score)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())

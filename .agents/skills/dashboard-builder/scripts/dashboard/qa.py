"""Payload validation for public_equity_investing_dashboard.v1 (stdlib only)."""

from __future__ import annotations

import json
import re
import statistics
from datetime import datetime
from pathlib import Path
from typing import Any

KIND = "public_equity_investing_dashboard.v1"

SUPPORTED_MODULES = frozenset(
    {
        "decision_box",
        "metric_tiles",
        "highlight_tiles",
        "executive_summary",
        "key_metrics",
        "growth_trajectory",
        "cards",
        "table",
        "scenario_map",
        "question_list",
        "transcript_qa",
        "read_throughs",
        "market_events",
        "bar_chart",
        "financial_trend_chart",
        "eps_actual_vs_estimate_chart",
        "equity_price_event_chart",
        "timeline",
        "text_block",
        "missing_evidence",
        "source_list",
    }
)

PRODUCTION_METADATA = (
    "freeze_time",
    "source_posture",
    "readiness_label",
    "readiness_posture",
    "decision_context",
)

READY_POSTURES = frozenset(
    {"pm_ready", "client_ready", "committee_ready", "senior_review_ready", "external", "publication_ready"}
)
READY_CLAIM = re.compile(
    r"(?<!not )(?<!not-)(?<!not_)\b(pm|client|committee|publication|senior[- ]review)[-_ ]ready\b", re.I
)
DRAFT_STAGES = frozenset({"draft", "support"})
LAYOUTS = frozenset({"tabs", "single_page"})
TAB_ID = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")
PLACEHOLDER = re.compile(r"\bTODO\b|\bFIXME\b|\bTBD\b|PLACEHOLDER|\{\{.*?\}\}|\[TOKEN\]|\bundefined\b|lorem ipsum", re.S)
ID_TOKEN = re.compile(r"^(?:model-output:[\w.:-]+|[A-Za-z][\w.-]*\d[\w.-]*)$")
BRACKET = re.compile(r"\[([^\[\]]{1,80})\]")

# Keys whose values are labels, identifiers, or ledger fields rather than material claims.
NUMERIC_EXEMPT_KEYS = frozenset(
    {
        "id", "type", "label", "title", "eyebrow", "period", "date", "timestamp", "time", "as_of", "status",
        "mode", "key", "name", "ticker", "url", "source", "source_url", "source_title", "number", "rank",
        "order", "bar_value", "price_granularity", "price_frequency", "price_interval", "margin_metric",
        "margin_label", "mobile_label", "columns", "exchange", "sector", "density", "kind", "layout",
        "accent_color", "brand_color", "brand_dark_color", "identity_color", "brand_colors", "citations",
        "source_id", "source_ids", "pinpoint",
    }
)
NUMERIC_SKIP_MODULES = frozenset({"missing_evidence", "source_list"})
FINANCIAL_FIELDS = ("revenue", "gross_profit", "net_income")


def load_payload(path: str | Path) -> dict[str, Any]:
    """Load a dashboard payload JSON file and remember where it came from."""
    file_path = Path(path)
    payload = json.loads(file_path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        payload["_source_path"] = str(file_path.resolve())
    return payload


def parse_number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str):
        return None
    text = value.strip()
    if not text:
        return None
    negative = text.startswith("(") and text.endswith(")")
    text = text.strip("()")
    text = re.sub(r"[$€£,\s]", "", text)
    text = re.sub(r"(%|x|bn|mm|m|b|k|t)$", "", text, flags=re.I)
    if not re.fullmatch(r"[-+]?(\d+\.?\d*|\.\d+)", text):
        return None
    number = float(text)
    return -number if negative else number


def parse_margin(value: Any) -> float | None:
    """Return a margin in percentage points from a decimal ratio or percent string."""
    number = parse_number(value)
    if number is None:
        return None
    if isinstance(value, str) and value.strip().endswith("%"):
        return number
    return number * 100 if abs(number) <= 1 else number


def parse_when(value: Any) -> tuple[datetime, bool] | None:
    """Parse a date or timestamp; the flag says whether it carries a time of day."""
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        for fmt in ("%m/%d/%Y", "%b %d, %Y", "%B %d, %Y"):
            try:
                return datetime.strptime(value.strip(), fmt), False
            except ValueError:
                continue
        return None
    has_time = bool(re.search(r"[T ]\d{1,2}:\d{2}", text))
    return parsed.replace(tzinfo=None), has_time


def model_citation_records(payload: dict[str, Any]) -> tuple[list[dict[str, Any]], str | None]:
    """Return workbook citation records plus an error when the referenced file is unreadable."""
    records: list[Any] = []
    inline = payload.get("model_citations")
    if isinstance(inline, list):
        records.extend(inline)
    error = None
    path = payload.get("model_citations_path")
    if isinstance(path, str) and path.strip():
        candidate = Path(path)
        if not candidate.is_absolute() and payload.get("_source_path"):
            candidate = Path(payload["_source_path"]).parent / candidate
        try:
            loaded = json.loads(candidate.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                loaded = loaded.get("model_citations") or loaded.get("citations") or []
            if isinstance(loaded, list):
                records.extend(loaded)
        except (OSError, ValueError):
            error = f"model_citations_path '{path}' could not be read."
    return [r for r in records if isinstance(r, dict) and r.get("id")], error


def known_source_ids(payload: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for source in payload.get("sources") or []:
        if isinstance(source, dict) and source.get("id"):
            ids.add(str(source["id"]))
    for module in iter_modules(payload):
        if module.get("type") == "source_list":
            for source in (module.get("data") or {}).get("sources") or []:
                if isinstance(source, dict) and source.get("id"):
                    ids.add(str(source["id"]))
    records, _ = model_citation_records(payload)
    ids.update(str(r["id"]) for r in records)
    return ids


def iter_modules(payload: dict[str, Any]):
    for tab in payload.get("tabs") or []:
        if isinstance(tab, dict):
            for module in tab.get("modules") or []:
                if isinstance(module, dict):
                    yield module


def node_citation_ids(node: dict[str, Any]) -> list[str]:
    ids: list[str] = []
    cites = node.get("citations")
    if isinstance(cites, (str, dict)):
        cites = [cites]
    for cite in cites or []:
        if isinstance(cite, dict):
            cite = cite.get("id") or cite.get("source_id")
        if cite:
            ids.append(str(cite))
    if node.get("source_id"):
        ids.append(str(node["source_id"]))
    source_ids = node.get("source_ids")
    if isinstance(source_ids, str):
        source_ids = [source_ids]
    ids.extend(str(s) for s in source_ids or [] if s)
    return ids


def has_support(node: dict[str, Any]) -> bool:
    if node_citation_ids(node):
        return True
    return bool(node.get("source_url") or node.get("source_title"))


def text_markers(text: str) -> list[str]:
    markers: list[str] = []
    for match in BRACKET.finditer(text):
        tokens = [t.strip() for t in re.split(r"[;,]", match.group(1)) if t.strip()]
        if tokens and all(ID_TOKEN.match(t) for t in tokens):
            markers.extend(tokens)
    return markers


def walk_strings(node: Any, path: str = ""):
    if isinstance(node, dict):
        for key, value in node.items():
            if key in {"qa", "_source_path"}:
                continue
            yield from walk_strings(value, f"{path}.{key}" if path else key)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk_strings(value, f"{path}[{index}]")
    elif isinstance(node, str):
        yield path, node


def collect_citation_refs(node: Any, path: str, out: list[tuple[str, str]]) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            if key in {"qa", "_source_path", "model_citations"}:
                continue
            collect_citation_refs(value, f"{path}.{key}", out)
        out.extend((path, cid) for cid in node_citation_ids(node))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            collect_citation_refs(value, f"{path}[{index}]", out)
    elif isinstance(node, str):
        out.extend((path, marker) for marker in text_markers(node))


def find_uncited_numbers(node: Any, cited: bool, path: str, out: list[str]) -> None:
    if isinstance(node, dict):
        scoped = cited or has_support(node)
        for key, value in node.items():
            if key in NUMERIC_EXEMPT_KEYS or key.startswith("_"):
                continue
            find_uncited_numbers(value, scoped, f"{path}.{key}", out)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            find_uncited_numbers(value, cited, f"{path}[{index}]", out)
    elif isinstance(node, bool) or node is None:
        return
    elif isinstance(node, (int, float)):
        if not cited:
            out.append(path)
    elif isinstance(node, str):
        if re.search(r"\d", node) and not cited and not text_markers(node):
            out.append(path)


def chart_rows(module_type: str, data: dict[str, Any]) -> list[dict[str, Any]]:
    """Return rows that satisfy the renderer field requirements for a chart module."""
    ready = []
    for row in data.get("periods") or []:
        if not isinstance(row, dict) or not str(row.get("period") or "").strip():
            continue
        if module_type == "financial_trend_chart":
            metric = data.get("margin_metric") or "net_margin"
            if any(parse_number(row.get(f)) is None for f in FINANCIAL_FIELDS):
                continue
            if parse_margin(row.get(metric)) is None:
                continue
        elif parse_number(row.get("estimated_eps")) is None or parse_number(row.get("actual_eps")) is None:
            continue
        ready.append(row)
    return ready


def price_rows(data: dict[str, Any]) -> list[tuple[datetime, bool, float]]:
    rows = []
    for row in data.get("prices") or []:
        if not isinstance(row, dict):
            continue
        when = parse_when(row.get("timestamp") or row.get("date") or row.get("time"))
        price = parse_number(row.get("price", row.get("close")))
        if when and price is not None:
            rows.append((when[0], when[1], price))
    return rows


def price_tape_problem(data: dict[str, Any]) -> str | None:
    rows = price_rows(data)
    declared = str(data.get("price_granularity") or data.get("price_frequency") or data.get("price_interval") or "").lower()
    timed = sorted({r[0] for r in rows if r[1]})
    if declared.startswith(("min", "intra")):
        family = "minute"
    elif declared.startswith("hour"):
        family = "hourly"
    elif declared.startswith("dai"):
        family = "daily"
    elif len(timed) >= 2 and len(timed) == len({r[0] for r in rows}):
        gap = statistics.median((b - a).total_seconds() for a, b in zip(timed, timed[1:]))
        family = "minute" if gap < 1800 else "hourly" if gap < 43200 else "daily"
    else:
        family = "daily"

    if family == "daily":
        days = sorted({r[0].date() for r in rows})
        span = (days[-1] - days[0]).days if days else 0
        if len(days) < 10 or span < 7:
            return f"daily price tape has {len(days)} distinct rows over {span} days (needs 10 rows over 7 days)"
        return None
    span_minutes = (timed[-1] - timed[0]).total_seconds() / 60 if timed else 0
    need_rows, need_minutes = (24, 360) if family == "hourly" else (60, 45)
    if len(timed) < need_rows or span_minutes < need_minutes:
        return (
            f"{family} price tape has {len(timed)} time-stamped rows over {span_minutes:.0f} minutes "
            f"(needs {need_rows} rows over {need_minutes} minutes)"
        )
    return None


def validate_payload(payload: Any, profile: str = "production") -> dict[str, Any]:
    strict = profile == "production"
    warnings: list[str] = []
    failures: list[str] = []

    def soft(message: str) -> None:
        (failures if strict else warnings).append(message)

    if not isinstance(payload, dict):
        return {"status": "fail", "warnings": [], "hard_failures": ["Payload must be a JSON object."]}

    if payload.get("kind") != KIND:
        failures.append(f"kind must be '{KIND}'.")

    metadata = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {}
    if not metadata:
        soft("metadata object is missing.")
    stage = str(metadata.get("payload_stage") or "").lower()
    policy = str(metadata.get("citation_policy") or "").lower()
    if strict:
        if stage != "production":
            failures.append("metadata.payload_stage must be 'production' for the production profile.")
        if policy != "strict":
            failures.append("metadata.citation_policy must be 'strict' for the production profile.")
        for field in PRODUCTION_METADATA:
            if not str(metadata.get(field) or "").strip():
                failures.append(f"metadata.{field} is required for production payloads.")
    elif stage not in DRAFT_STAGES | {"production"}:
        warnings.append("metadata.payload_stage should be 'production', 'draft', or 'support'.")

    posture = str(metadata.get("readiness_posture") or "").lower()
    label = str(metadata.get("readiness_label") or "")
    if stage != "production" and (
        posture in READY_POSTURES or READY_CLAIM.search(label) or READY_CLAIM.search(posture)
    ):
        failures.append("Draft or support payloads must not claim a ready/publication readiness posture.")

    layout = payload.get("layout")
    if layout is not None and layout not in LAYOUTS:
        warnings.append(f"layout '{layout}' is not supported; use 'tabs' or 'single_page'.")

    hero = payload.get("hero") if isinstance(payload.get("hero"), dict) else {}
    if not str(hero.get("headline") or "").strip():
        soft("hero.headline is missing.")
    if not str(payload.get("title") or "").strip():
        soft("title is missing.")

    sources = payload.get("sources")
    seen_sources: set[str] = set()
    if not isinstance(sources, list) or not sources:
        soft("Source ledger (sources) is missing or empty.")
    else:
        for index, source in enumerate(sources):
            if not isinstance(source, dict) or not source.get("id"):
                soft(f"sources[{index}] needs an id.")
                continue
            sid = str(source["id"])
            if sid in seen_sources:
                soft(f"Duplicate source id '{sid}'.")
            seen_sources.add(sid)
            if not (source.get("title") or source.get("url")):
                warnings.append(f"sources[{sid}] has neither title nor url.")

    _, model_error = model_citation_records(payload)
    if model_error:
        soft(model_error)

    tabs = payload.get("tabs")
    if not isinstance(tabs, list) or not tabs:
        failures.append("tabs must be a non-empty list.")
        tabs = []
    tab_ids: set[str] = set()
    for t_index, tab in enumerate(tabs):
        if not isinstance(tab, dict):
            failures.append(f"tabs[{t_index}] must be an object.")
            continue
        tab_id = tab.get("id")
        if not isinstance(tab_id, str) or not TAB_ID.match(tab_id):
            failures.append(f"tabs[{t_index}].id is missing or invalid (use letters, digits, '-' or '_').")
        elif tab_id in tab_ids:
            failures.append(f"Duplicate tab id '{tab_id}'.")
        else:
            tab_ids.add(tab_id)
        modules = tab.get("modules")
        if not isinstance(modules, list) or not modules:
            warnings.append(f"tabs[{t_index}] has no modules.")
            continue
        for m_index, module in enumerate(modules):
            where = f"tabs[{t_index}].modules[{m_index}]"
            if not isinstance(module, dict):
                failures.append(f"{where} must be an object.")
                continue
            mtype = module.get("type")
            if mtype not in SUPPORTED_MODULES:
                failures.append(f"{where} has unsupported module type '{mtype}'.")
                continue
            data = module.get("data")
            if not isinstance(data, dict):
                warnings.append(f"{where} ({mtype}) has no data object.")
                continue
            _validate_chart(mtype, data, where, soft)

    known = known_source_ids(payload)
    refs: list[tuple[str, str]] = []
    for section in ("hero", "snapshot", "tabs"):
        collect_citation_refs(payload.get(section), section, refs)
    unresolved: dict[str, list[str]] = {}
    for path, cid in refs:
        if cid not in known:
            unresolved.setdefault(cid, []).append(path)
    for cid, paths in sorted(unresolved.items()):
        soft(f"Unresolved citation id '{cid}' (first at {paths[0]}).")

    uncited: list[str] = []
    find_uncited_numbers(hero, bool(hero.get("citations")), "hero", uncited)
    find_uncited_numbers(payload.get("snapshot") or [], False, "snapshot", uncited)
    for t_index, tab in enumerate(tabs):
        if not isinstance(tab, dict):
            continue
        tab_cited = has_support(tab)
        for m_index, module in enumerate(tab.get("modules") or []):
            if isinstance(module, dict) and module.get("type") not in NUMERIC_SKIP_MODULES:
                find_uncited_numbers(module, tab_cited, f"tabs[{t_index}].modules[{m_index}]", uncited)
    if uncited:
        sample = ", ".join(uncited[:5])
        more = f" (+{len(uncited) - 5} more)" if len(uncited) > 5 else ""
        soft(f"Numeric material without citation support at {sample}{more}.")

    found = [(p, PLACEHOLDER.search(t).group(0)) for p, t in walk_strings(payload) if PLACEHOLDER.search(t)]
    for path, token in found[:10]:
        soft(f"Unresolved placeholder text at {path}: '{token}'.")

    status = "fail" if failures else "warn" if warnings else "pass"
    return {"status": status, "warnings": warnings, "hard_failures": failures}


def _validate_chart(mtype: str, data: dict[str, Any], where: str, soft) -> None:
    if mtype in {"financial_trend_chart", "eps_actual_vs_estimate_chart"}:
        ready = chart_rows(mtype, data)
        if len(ready) < 2:
            soft(
                f"{where} ({mtype}) has {len(ready)} chart-ready rows; at least 2 are required. "
                "Omit the chart and list the gap in missing_evidence."
            )
    elif mtype == "equity_price_event_chart":
        problem = price_tape_problem(data)
        if problem:
            soft(f"{where} (equity_price_event_chart): {problem}.")
        events = data.get("events") if isinstance(data.get("events"), list) else []
        if not any(isinstance(e, dict) and e.get("event") for e in events):
            soft(f"{where} (equity_price_event_chart) needs at least one sourced event.")

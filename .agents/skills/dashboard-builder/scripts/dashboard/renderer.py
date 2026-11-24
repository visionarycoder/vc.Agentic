"""Standalone HTML renderer for public_equity_investing_dashboard.v1 (stdlib only)."""

from __future__ import annotations

import math
import re
from datetime import datetime
from html import escape
from typing import Any

from dashboard.qa import (
    BRACKET,
    chart_rows,
    model_citation_records,
    node_citation_ids,
    parse_margin,
    parse_number,
    parse_when,
    price_rows,
    text_markers,
    validate_payload,
)

DEFAULT_TITLES = {
    "decision_box": "PM View",
    "metric_tiles": "Key Metrics",
    "highlight_tiles": "Highlights",
    "executive_summary": "Executive Summary",
    "key_metrics": "Quarterly Key Metrics",
    "growth_trajectory": "Growth Trajectory",
    "scenario_map": "Scenarios",
    "question_list": "Questions",
    "transcript_qa": "Transcript Q&A",
    "read_throughs": "Read-Throughs",
    "market_events": "Market Events",
    "financial_trend_chart": "Financial Trend",
    "eps_actual_vs_estimate_chart": "EPS: Actual vs Estimate",
    "equity_price_event_chart": "Price and Events",
    "timeline": "Timeline",
    "missing_evidence": "Missing Evidence",
    "source_list": "Sources",
}

DEFAULT_COLUMNS = {
    "key_metrics": ["metric", "current", "growth", "compare", "trajectory", "read"],
    "growth_trajectory": ["metric", "prior", "current", "trajectory", "read"],
    "transcript_qa": ["number", "analyst", "topic", "response", "quote", "quality"],
    "read_throughs": ["name", "relationship", "parent_said", "read_through", "implication", "confidence"],
    "market_events": ["date", "event", "type", "impact", "investor_read", "source"],
}

CSS = """
:root{--ink:#1c2430;--muted:#5b6675;--line:#d9dee5;--bg:#f4f6f8;--card:#fff;--accent:#245f5a;--good:#1a7f4b;--watch:#a16207;--bad:#b42318;--gap:#6b7280}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:64px}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}
.page{max-width:1180px;margin:0 auto;padding:12px}
h1{font-size:28px;line-height:1.2;margin:4px 0 6px}h2{font-size:20px;margin:0 0 8px}h3{font-size:16px;margin:0 0 6px}p{margin:0 0 8px}
.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:0 0 2px}
.hero{background:var(--card);border:1px solid var(--line);border-left:6px solid var(--accent);border-radius:8px;padding:14px;display:flex;gap:14px;align-items:flex-start}
.badge{flex:none;min-width:64px;padding:12px 10px;border-radius:8px;background:var(--accent);color:#fff;font-weight:700;text-align:center;letter-spacing:.04em}
.hero-main{min-width:0;flex:1}.dek{color:var(--muted);font-size:16px}
.callout{margin-top:8px;padding:8px 10px;background:#eef3f2;border-radius:6px}.callout b{display:block;font-size:12px;text-transform:uppercase;color:var(--muted)}
.banner{margin:10px 0;padding:10px 12px;border:1px solid var(--watch);background:#fff8e6;border-radius:6px}.banner ul{margin:6px 0 0;padding-left:18px}
.snap{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:8px;margin:10px 0}
.tile{background:var(--card);border:1px solid var(--line);border-top:3px solid var(--gap);border-radius:6px;padding:8px 10px;min-width:0;overflow-wrap:anywhere}
.tile .v{font-size:20px;font-weight:700}.tile .d{color:var(--muted);font-size:13px}.tile .l{font-size:12px;text-transform:uppercase;color:var(--muted)}
.st-good{border-top-color:var(--good)}.st-watch,.st-base{border-top-color:var(--watch)}.st-bad,.st-bear{border-top-color:var(--bad)}.st-bull{border-top-color:var(--good)}
nav.toc,.tabs{position:sticky;top:0;z-index:5;display:flex;gap:6px;overflow-x:auto;background:var(--bg);padding:6px 0;margin:0 0 8px}
nav.toc a,.tabs button{flex:none;min-height:44px;display:inline-flex;align-items:center;padding:0 14px;border:1px solid var(--line);border-radius:22px;background:var(--card);color:var(--ink);text-decoration:none;font:inherit;cursor:pointer}
.tabs button[aria-selected=true]{background:var(--accent);color:#fff;border-color:var(--accent)}
.panel{margin-bottom:12px}.panel[hidden]{display:none}
.module{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px;margin:0 0 10px;min-width:0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px}
.card{border:1px solid var(--line);border-radius:6px;padding:8px 10px;border-top:3px solid var(--gap);overflow-wrap:anywhere}
.card ul,.module ul{margin:4px 0 0;padding-left:18px}
.stance{font-size:18px;font-weight:700}.kv{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:6px;margin:8px 0}
.kv div{background:#f7f9fa;border-radius:6px;padding:6px 8px}.kv b{display:block;font-size:12px;text-transform:uppercase;color:var(--muted)}
.table-wrap{overflow-x:auto;max-width:100%}table{border-collapse:collapse;width:100%;font-size:14px}
th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top;overflow-wrap:anywhere}th{background:#f1f4f6;font-size:12px;text-transform:uppercase;color:var(--muted)}
.dense th,.dense td{padding:4px 6px;font-size:13px}
.cite{color:inherit;text-decoration:none;position:relative}
a.cite.chip{display:inline-block;margin:0 2px;padding:0 6px;border:1px solid var(--line);border-radius:10px;background:#f1f4f6;font-size:11px;color:var(--muted);vertical-align:baseline;overflow-wrap:anywhere}
a.cite.num{border-bottom:1px dotted var(--accent);background:#eef6f4}
a.cite.unresolved{border-color:var(--bad);color:var(--bad)}
.pop{display:none;position:absolute;left:0;top:100%;z-index:20;width:min(320px,80vw);padding:8px 10px;background:#111827;color:#fff;border-radius:6px;font-size:12px;font-weight:400;line-height:1.35;text-align:left;text-transform:none;letter-spacing:0;white-space:normal}
a.cite:hover .pop,a.cite:focus .pop{display:block}.pop b{display:block}.pop i{display:block;opacity:.8;font-style:normal}
.srcnote{margin:8px 0 0;font-size:12px;color:var(--muted)}
.bars .row{display:grid;grid-template-columns:minmax(90px,30%) 1fr auto;gap:8px;align-items:center;margin:4px 0}
.bars .track{background:#e9edf1;border-radius:4px;height:14px}.bars .fill{background:var(--accent);height:14px;border-radius:4px}
.legend{display:flex;flex-wrap:wrap;gap:10px;font-size:12px;color:var(--muted);margin:4px 0}.legend i{display:inline-block;width:10px;height:10px;margin-right:4px;border-radius:2px}
svg.chart{width:100%;height:auto;max-width:100%}svg.chart text{font-size:11px;fill:#4b5563}svg.chart .grid{stroke:#e5e7eb}
.timeline{list-style:none;margin:0;padding:0}.timeline li{border-left:3px solid var(--accent);padding:2px 0 8px 10px;margin-left:4px}
.src-ledger .src{padding:6px 0;border-bottom:1px solid var(--line);overflow-wrap:anywhere}.src:target{background:#fff8e6}
footer{color:var(--muted);font-size:12px;padding:8px 0}
@media(max-width:700px){h1{font-size:22px}.hero{flex-direction:column}.module{padding:10px}
table.stack thead{display:none}table.stack,table.stack tbody,table.stack tr,table.stack td{display:block;width:100%}
table.stack tr{border:1px solid var(--line);border-radius:6px;margin:0 0 8px;padding:4px}table.stack td{border:0;padding:3px 6px}
table.stack td::before{content:attr(data-label);display:block;font-size:11px;text-transform:uppercase;color:var(--muted)}}
"""

JS = """
(function(){var tabs=[].slice.call(document.querySelectorAll('[role=tab]'));if(!tabs.length)return;
function show(id){tabs.forEach(function(t){t.setAttribute('aria-selected',String(t.dataset.tab===id))});
[].slice.call(document.querySelectorAll('.panel')).forEach(function(p){p.hidden=p.dataset.tab!==id})}
tabs.forEach(function(t){t.addEventListener('click',function(){show(t.dataset.tab)})});
function fromHash(){var h=decodeURIComponent(location.hash.slice(1));if(!h)return;var el=document.getElementById(h);
var p=el&&el.closest('.panel');if(p){show(p.dataset.tab);el.scrollIntoView()}}
window.addEventListener('hashchange',fromHash);fromHash()})();
"""


def esc(value: Any) -> str:
    return escape("" if value is None else str(value), quote=True)


def slug(value: Any) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "-", str(value)).strip("-") or "x"


def safe_url(url: Any) -> str | None:
    return str(url) if isinstance(url, str) and re.match(r"https?://", url.strip(), re.I) else None


def label_of(key: str) -> str:
    return key.replace("_", " ").title()


def color_ok(value: Any) -> str | None:
    return value if isinstance(value, str) and re.fullmatch(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})", value) else None


def luminance(color: str) -> float:
    c = color.lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    r, g, b = (int(c[i : i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def accent_color(issuer: dict[str, Any]) -> str:
    candidates = [issuer.get(k) for k in ("brand_dark_color", "identity_color", "brand_color", "accent_color")]
    if isinstance(issuer.get("brand_colors"), list):
        candidates += issuer["brand_colors"]
    valid = [c for c in map(color_ok, candidates) if c]
    if not valid:
        return "#245f5a"
    color = min(valid, key=luminance)
    while luminance(color) > 0.22:
        c = color.lstrip("#")
        if len(c) == 3:
            c = "".join(ch * 2 for ch in c)
        color = "#" + "".join(f"{int(int(c[i:i+2], 16) * 0.8):02x}" for i in (0, 2, 4))
    return color


class Context:
    def __init__(self, payload: dict[str, Any]) -> None:
        self.sources: dict[str, dict[str, Any]] = {}
        for source in payload.get("sources") or []:
            if isinstance(source, dict) and source.get("id"):
                self.sources[str(source["id"])] = source
        for tab in payload.get("tabs") or []:
            for module in (tab.get("modules") or []) if isinstance(tab, dict) else []:
                if isinstance(module, dict) and module.get("type") == "source_list":
                    for source in (module.get("data") or {}).get("sources") or []:
                        if isinstance(source, dict) and source.get("id"):
                            self.sources.setdefault(str(source["id"]), source)
        records, _ = model_citation_records(payload)
        self.model_ids: list[str] = []
        for rec in records:
            where = " ".join(str(rec[k]) for k in ("workbook_path", "sheet") if rec.get(k))
            cell = rec.get("cell") or rec.get("range")
            detail = f"{where}!{cell}" if cell else where
            if rec.get("value") is not None:
                detail += f" = {rec['value']}"
            if rec.get("formula"):
                detail += f" ({rec['formula']})"
            self.sources[str(rec["id"])] = {
                "id": rec["id"],
                "title": rec.get("line_item") or rec["id"],
                "type": "Model output",
                "status": rec.get("evidence_label"),
                "excerpt": detail.strip(),
                "note": f"Underlying source: {rec['source_id']}" if rec.get("source_id") else None,
            }
            self.model_ids.append(str(rec["id"]))


Ref = tuple[str, Any]


def refs_of(node: Any) -> list[Ref]:
    if not isinstance(node, dict):
        return []
    refs: list[Ref] = [("id", cid) for cid in dict.fromkeys(node_citation_ids(node))]
    url = safe_url(node.get("source_url"))
    if url or node.get("source_title"):
        refs.append(
            ("ext", {"url": url, "title": node.get("source_title") or url, "as_of": node.get("as_of"), "excerpt": node.get("excerpt")})
        )
    return refs


def popover(src: dict[str, Any]) -> str:
    meta = " · ".join(str(x) for x in (src.get("type"), src.get("status"), src.get("as_of")) if x)
    parts = [f"<b>{esc(src.get('title') or src.get('id') or 'Source')}</b>"]
    if meta:
        parts.append(f"<i>{esc(meta)}</i>")
    for key in ("excerpt", "pinpoint", "note"):
        if src.get(key):
            parts.append(esc(src[key]))
            break
    return f'<span class="pop" role="tooltip">{"".join(parts)}</span>'


def cite_link(ctx: Context, ref: Ref, text: str | None = None, numeric: bool = False) -> str:
    kind, target = ref
    cls = "cite num" if numeric else "cite chip"
    if kind == "ext":
        label = text if text is not None else (target.get("title") or "Source")
        url = target.get("url")
        attrs = f' href="{esc(url)}" target="_blank" rel="noopener noreferrer"' if url else ' tabindex="0"'
        return f'<a class="{cls}"{attrs}>{esc(label)}{popover(target)}</a>'
    src = ctx.sources.get(str(target))
    label = text if text is not None else str(target)
    if src is None:
        return f'<a class="{cls} unresolved" tabindex="0">{esc(label)}<span class="pop" role="tooltip">Unresolved source {esc(target)}</span></a>'
    return f'<a class="{cls}" href="#src-{esc(slug(target))}">{esc(label)}{popover(src)}</a>'


def chips(ctx: Context, refs: list[Ref]) -> str:
    return "".join(cite_link(ctx, r) for r in refs)


def val(ctx: Context, text: Any, refs: list[Ref] | None = None) -> str:
    """Render text with escaped content, bracket markers as chips, and numeric values as source links."""
    if isinstance(text, dict) and "value" in text:
        return val(ctx, text["value"], refs_of(text) or refs)
    s = "" if text is None else str(text)
    out, pos, had_marker = [], 0, False
    for match in BRACKET.finditer(s):
        ids = text_markers(match.group(0))
        if not ids:
            continue
        out.append(esc(s[pos : match.start()]))
        out.append(chips(ctx, [("id", i) for i in ids]))
        pos, had_marker = match.end(), True
    out.append(esc(s[pos:]))
    body = "".join(out)
    if refs and not had_marker:
        if re.search(r"\d", s) and len(s) <= 40:
            return cite_link(ctx, refs[0], s, numeric=True) + chips(ctx, refs[1:])
        return body + chips(ctx, refs)
    return body


def tile_class(status: Any) -> str:
    return f"st-{slug(status).lower()}" if status else ""


def source_note(ctx: Context, node: Any) -> str:
    refs = refs_of(node)
    return f'<p class="srcnote">Sources: {chips(ctx, refs)}</p>' if refs else ""


def bullets(ctx: Context, items: Any) -> str:
    if not isinstance(items, list) or not items:
        return ""
    lis = "".join(f"<li>{val(ctx, i, refs_of(i))}</li>" for i in items)
    return f"<ul>{lis}</ul>"


def col_list(columns: Any, default: list[str]) -> list[tuple[str, str]]:
    columns = columns or default
    result = []
    for col in columns:
        if isinstance(col, dict):
            key = str(col.get("key") or col.get("label") or "")
            result.append((key, str(col.get("label") or label_of(key))))
        else:
            result.append((str(col), label_of(str(col)) if re.fullmatch(r"[a-z_]+", str(col)) else str(col)))
    return result


def cell_value(row: dict[str, Any], key: str, label: str) -> Any:
    for candidate in (key, label, label.lower().replace(" ", "_"), key.lower().replace(" ", "_")):
        if candidate in row:
            return row[candidate]
    return ""


def table_html(
    ctx: Context, columns: list[tuple[str, str]], rows: list[Any], mobile_label: Any = None,
    dense: bool = False, chip_keys: frozenset[str] = frozenset(),
) -> str:
    head = "".join(f"<th scope=\"col\">{esc(label)}</th>" for _, label in columns)
    body = []
    for row in rows:
        if not isinstance(row, dict):
            row = {columns[0][0]: row} if columns else {}
        refs = refs_of(row)
        row_refs = [r for r in refs if r[0] == "id" or row.get("source_url") is None] if refs else []
        cells, linked = [], False
        for key, label in columns:
            raw = cell_value(row, key, label)
            if key == "source" and (row.get("source_title") or row.get("source_url")):
                url = safe_url(row.get("source_url"))
                title = esc(row.get("source_title") or url)
                html_val = f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{title}</a>' if url else title
            elif isinstance(raw, dict):
                html_val = val(ctx, raw)
                linked = linked or bool(refs_of(raw))
            else:
                text = "" if raw is None else str(raw)
                own = row_refs if (row_refs and re.search(r"\d", text) and len(text) <= 40) else None
                if key in chip_keys and row_refs:
                    html_val = val(ctx, text) + chips(ctx, row_refs)
                    linked = True
                else:
                    html_val = val(ctx, text, own)
                    linked = linked or bool(own)
            cells.append(f'<td data-label="{esc(label)}">{html_val}</td>')
        if row_refs and not linked and cells:
            cells[-1] = cells[-1][: -len("</td>")] + chips(ctx, row_refs) + "</td>"
        body.append(f"<tr>{''.join(cells)}</tr>")
    caption = f"<caption class=\"eyebrow\">{esc(mobile_label)}</caption>" if mobile_label else ""
    cls = "stack dense" if dense else "stack"
    return f'<div class="table-wrap"><table class="{cls}">{caption}<thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def tiles(ctx: Context, items: list[Any]) -> str:
    out = []
    for item in items:
        if not isinstance(item, dict):
            continue
        refs = refs_of(item)
        detail = f'<div class="d">{val(ctx, item["detail"])}</div>' if item.get("detail") else ""
        extra = chips(ctx, refs) if refs and not re.search(r"\d", str(item.get("value", ""))) else ""
        out.append(
            f'<div class="tile {tile_class(item.get("status"))}"><div class="l">{esc(item.get("label"))}</div>'
            f'<div class="v">{val(ctx, item.get("value"), refs if not extra else None)}{extra}</div>{detail}</div>'
        )
    return f'<div class="snap">{"".join(out)}</div>'


# ---------- charts ----------

def nice_ticks(lo: float, hi: float, target: int = 5, zero: bool = True) -> list[float]:
    if zero:
        lo, hi = min(lo, 0.0), max(hi, 0.0)
    span = hi - lo or 1.0
    raw = span / target
    mag = 10 ** math.floor(math.log10(raw))
    step = next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw)
    start = math.floor(lo / step) * step
    ticks, t = [], start
    while t < hi + step * 0.999:
        ticks.append(round(t, 10))
        t += step
        if len(ticks) > 12:
            break
    return ticks


def fmt_num(value: float) -> str:
    return f"{value:,.0f}" if abs(value) >= 100 or value == int(value) else f"{value:,.2f}".rstrip("0").rstrip(".")


SERIES_COLORS = ["#245f5a", "#7aa6a1", "#c9a227", "#b42318"]


def grouped_bar_svg(periods: list[str], series: list[tuple[str, list[float]]], line: tuple[str, list[float]] | None, aria: str) -> str:
    w, h, left, right, top, bottom = 720, 320, 56, 56 if line else 16, 16, 40
    pw, ph = w - left - right, h - top - bottom
    values = [v for _, vs in series for v in vs]
    ticks = nice_ticks(min(values), max(values))
    lo, hi = ticks[0], ticks[-1]

    def y(v: float) -> float:
        return top + ph - (v - lo) / (hi - lo) * ph

    parts = [f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">']
    for t in ticks:
        parts.append(f'<line class="grid" x1="{left}" x2="{left + pw}" y1="{y(t):.1f}" y2="{y(t):.1f}"/>')
        parts.append(f'<text x="{left - 6}" y="{y(t) + 4:.1f}" text-anchor="end">{esc(fmt_num(t))}</text>')
    group = pw / len(periods)
    bar = min(36, group * 0.8 / len(series))
    for i, period in enumerate(periods):
        gx = left + group * i + (group - bar * len(series)) / 2
        for s, (_, vs) in enumerate(series):
            top_y, base = y(max(vs[i], 0)), y(0)
            parts.append(
                f'<rect x="{gx + s * bar:.1f}" y="{top_y:.1f}" width="{bar - 2:.1f}" height="{abs(y(vs[i]) - base):.1f}" fill="{SERIES_COLORS[s % 4]}"/>'
                if vs[i] >= 0
                else f'<rect x="{gx + s * bar:.1f}" y="{base:.1f}" width="{bar - 2:.1f}" height="{abs(y(vs[i]) - base):.1f}" fill="{SERIES_COLORS[s % 4]}"/>'
            )
        parts.append(f'<text x="{left + group * (i + 0.5):.1f}" y="{h - 18}" text-anchor="middle">{esc(period)}</text>')
    if line:
        lticks = nice_ticks(min(line[1]), max(line[1]))
        llo, lhi = lticks[0], lticks[-1]

        def ly(v: float) -> float:
            return top + ph - (v - llo) / (lhi - llo) * ph

        for t in lticks:
            parts.append(f'<text x="{left + pw + 6}" y="{ly(t) + 4:.1f}">{esc(fmt_num(t))}%</text>')
        pts = [(left + group * (i + 0.5), ly(v)) for i, v in enumerate(line[1])]
        parts.append(f'<polyline fill="none" stroke="#111827" stroke-width="2" points="{" ".join(f"{x:.1f},{yy:.1f}" for x, yy in pts)}"/>')
        parts.extend(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="3.5" fill="#111827"/>' for x, yy in pts)
    parts.append("</svg>")
    return "".join(parts)


def legend(items: list[tuple[str, str]]) -> str:
    return '<div class="legend">' + "".join(f'<span><i style="background:{c}"></i>{esc(n)}</span>' for n, c in items) + "</div>"


def financial_trend(ctx: Context, data: dict[str, Any]) -> str:
    rows = chart_rows("financial_trend_chart", data)
    if len(rows) < 1:
        return '<p class="srcnote">Chart omitted: no complete rows.</p>'
    metric = data.get("margin_metric") or "net_margin"
    mlabel = data.get("margin_label") or label_of(metric)
    series = [(label_of(f), [parse_number(r[f]) for r in rows]) for f in ("revenue", "gross_profit", "net_income")]
    svg = grouped_bar_svg([str(r["period"]) for r in rows], series, (mlabel, [parse_margin(r[metric]) for r in rows]), "Financial trend")
    leg = legend([(n, SERIES_COLORS[i]) for i, (n, _) in enumerate(series)] + [(f"{mlabel} (right axis)", "#111827")])
    note = f'<p class="srcnote">{esc(data["margin_rationale"])}</p>' if data.get("margin_rationale") else ""
    cols = [("period", "Period"), ("revenue", "Revenue"), ("gross_profit", "Gross Profit"), ("net_income", "Net Income"), (metric, mlabel)]
    return leg + svg + note + table_html(ctx, cols, rows, data.get("mobile_label"), True)


def eps_chart(ctx: Context, data: dict[str, Any]) -> str:
    rows = chart_rows("eps_actual_vs_estimate_chart", data)
    series = [("Estimated EPS", [parse_number(r["estimated_eps"]) for r in rows]), ("Actual EPS", [parse_number(r["actual_eps"]) for r in rows])]
    svg = grouped_bar_svg([str(r["period"]) for r in rows], series, None, "EPS actual versus estimate")
    table_rows = []
    for r, est, act in zip(rows, series[0][1], series[1][1]):
        row = dict(r)
        if row.get("surprise") in (None, ""):
            row["surprise"] = f"{act - est:+.2f}"
        table_rows.append(row)
    cols = [("period", "Period"), ("basis", "Basis"), ("estimated_eps", "Estimate"), ("actual_eps", "Actual"), ("surprise", "Surprise")]
    return legend([(n, SERIES_COLORS[i]) for i, (n, _) in enumerate(series)]) + svg + table_html(ctx, cols, table_rows, data.get("mobile_label"), True)


def price_chart(ctx: Context, data: dict[str, Any]) -> str:
    rows = sorted(price_rows(data), key=lambda r: r[0])
    events = [e for e in data.get("events") or [] if isinstance(e, dict)]
    out = ""
    if rows:
        w, h, left, top, bottom = 720, 300, 56, 16, 30
        pw, ph = w - left - 16, h - top - bottom
        prices = [r[2] for r in rows]
        lo, hi = min(prices), max(prices)
        pad = (hi - lo) * 0.1 or 1
        ticks = nice_ticks(lo - pad, hi + pad, zero=False)
        tlo, thi = ticks[0], ticks[-1]
        t0, t1 = rows[0][0], rows[-1][0]
        total = (t1 - t0).total_seconds() or 1

        def px(t: datetime) -> float:
            return left + (t - t0).total_seconds() / total * pw

        def py(v: float) -> float:
            return top + ph - (v - tlo) / (thi - tlo) * ph

        svg = [f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="Equity price with event markers">']
        for t in ticks:
            svg.append(f'<line class="grid" x1="{left}" x2="{w - 16}" y1="{py(t):.1f}" y2="{py(t):.1f}"/><text x="{left - 6}" y="{py(t) + 4:.1f}" text-anchor="end">{esc(fmt_num(t))}</text>')
        svg.append(f'<polyline fill="none" stroke="#245f5a" stroke-width="2" points="{" ".join(f"{px(r[0]):.1f},{py(r[2]):.1f}" for r in rows)}"/>')
        svg.append(f'<text x="{left}" y="{h - 8}">{esc(t0.strftime("%Y-%m-%d %H:%M") if rows[0][1] else t0.strftime("%Y-%m-%d"))}</text>')
        svg.append(f'<text x="{w - 16}" y="{h - 8}" text-anchor="end">{esc(t1.strftime("%Y-%m-%d %H:%M") if rows[-1][1] else t1.strftime("%Y-%m-%d"))}</text>')
        for n, event in enumerate(events, 1):
            when = parse_when(event.get("date") or event.get("timestamp"))
            if when and t0 <= when[0] <= t1:
                x = px(when[0])
                nearest = min(rows, key=lambda r: abs((r[0] - when[0]).total_seconds()))
                yy = py(nearest[2])
            else:
                x = left + pw * n / (len(events) + 1)
                yy = py(rows[min(len(rows) - 1, int(len(rows) * n / (len(events) + 1)))][2])
            svg.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="9" fill="#b42318"/><text x="{x:.1f}" y="{yy + 4:.1f}" text-anchor="middle" style="fill:#fff;font-weight:700">{n}</text>')
        svg.append("</svg>")
        out += "".join(svg)
    numbered = [dict(e, number=n) for n, e in enumerate(events, 1)]
    cols = [("number", "#"), ("date", "Date"), ("event", "Event"), ("type", "Type"), ("impact", "Impact"), ("investor_read", "Investor Read"), ("source", "Source")]
    return out + table_html(ctx, cols, numbered, data.get("mobile_label"), True, frozenset({"event", "investor_read"}))


def bar_chart(ctx: Context, data: dict[str, Any]) -> str:
    items = [i for i in data.get("items") or [] if isinstance(i, dict)]
    scale = [v for v in (parse_number(i.get("bar_value", i.get("value"))) for i in items) if v is not None]
    top = max([abs(v) for v in scale] + [1e-9])
    rows = []
    for item in items:
        num = parse_number(item.get("bar_value", item.get("value"))) or 0
        pct = max(0.0, min(100.0, abs(num) / top * 100))
        detail = f'<div class="srcnote">{esc(item["detail"])}</div>' if item.get("detail") else ""
        display = item.get("display", item.get("value"))
        rows.append(
            f'<div class="row"><div>{esc(item.get("label"))}{detail}</div><div class="track"><div class="fill" style="width:{pct:.1f}%"></div></div>'
            f'<div>{val(ctx, display, refs_of(item))}</div></div>'
        )
    return f'<div class="bars">{"".join(rows)}</div>'


# ---------- modules ----------

def render_module(ctx: Context, module: dict[str, Any]) -> str:
    mtype = module.get("type")
    data = module.get("data") if isinstance(module.get("data"), dict) else {}
    body = MODULES[mtype](ctx, data) if mtype in MODULES else "<p>Unsupported module.</p>"
    title = module.get("title") or data.get("title") or DEFAULT_TITLES.get(str(mtype))
    eyebrow = f'<p class="eyebrow">{esc(module.get("eyebrow"))}</p>' if module.get("eyebrow") else ""
    head = f"{eyebrow}<h3>{esc(title)}</h3>" if title else eyebrow
    note = "" if mtype == "source_list" else source_note(ctx, data)
    return f'<section class="module m-{esc(slug(mtype))}">{head}{body}{note}</section>'


def decision_box(ctx: Context, d: dict[str, Any]) -> str:
    label = f'<p class="eyebrow">{esc(d["label"])}</p>' if d.get("label") else ""
    stance = f'<p class="stance">{val(ctx, d["stance"])}</p>' if d.get("stance") else ""
    summary = f"<p>{val(ctx, d['summary'])}</p>" if d.get("summary") else ""
    kv = "".join(
        f"<div><b>{label_of(k)}</b>{val(ctx, d[k])}</div>"
        for k in ("thesis_change", "estimate_revision", "stock_skew", "next_catalyst")
        if d.get(k)
    )
    return label + stance + summary + (f'<div class="kv">{kv}</div>' if kv else "") + bullets(ctx, d.get("key_points"))


def metric_tiles(ctx: Context, d: dict[str, Any]) -> str:
    return tiles(ctx, d.get("items") or [])


def executive_summary(ctx: Context, d: dict[str, Any]) -> str:
    out = f"<h4>{val(ctx, d['headline'])}</h4>" if d.get("headline") else ""
    out += f"<p>{val(ctx, d['body'])}</p>" if d.get("body") else ""
    out += bullets(ctx, d.get("bullets"))
    out += f'<p class="callout"><b>Net read</b>{val(ctx, d["net_read"])}</p>' if d.get("net_read") else ""
    return out


def make_table(kind: str):
    def render(ctx: Context, d: dict[str, Any]) -> str:
        rows = d.get("rows") or d.get("events") or []
        chip_keys = frozenset({"event", "investor_read"}) if kind == "market_events" else frozenset()
        return table_html(
            ctx, col_list(d.get("columns"), DEFAULT_COLUMNS.get(kind, [])), rows, d.get("mobile_label"),
            d.get("density") == "dense" or kind in DEFAULT_COLUMNS, chip_keys,
        )

    return render


def cards(ctx: Context, d: dict[str, Any]) -> str:
    out = []
    for item in d.get("items") or []:
        if not isinstance(item, dict):
            continue
        refs = refs_of(item)
        eyebrow = f'<p class="eyebrow">{esc(item["eyebrow"])}</p>' if item.get("eyebrow") else ""
        title = f"<h3>{esc(item['title'])}</h3>" if item.get("title") else ""
        body = f"<p>{val(ctx, item['body'])}</p>" if item.get("body") else ""
        out.append(
            f'<article class="card {tile_class(item.get("status"))}">{eyebrow}{title}{body}{bullets(ctx, item.get("bullets"))}'
            f'{source_note(ctx, item) if refs else ""}</article>'
        )
    return f'<div class="grid">{"".join(out)}</div>'


def table(ctx: Context, d: dict[str, Any]) -> str:
    columns = col_list(d.get("columns"), [])
    rows = d.get("rows") or []
    if not columns and rows and isinstance(rows[0], dict):
        columns = [(k, label_of(k)) for k in rows[0] if k not in {"citations", "source_id", "source_ids", "source_url", "source_title"}]
    return table_html(ctx, columns, rows, d.get("mobile_label"), d.get("density") == "dense")


def scenario_map(ctx: Context, d: dict[str, Any]) -> str:
    out = []
    for case in d.get("cases") or []:
        if not isinstance(case, dict):
            continue
        kind = case.get("type") or case.get("status")
        title = case.get("title") or case.get("label")
        headline = case.get("headline") or case.get("summary")
        refs = refs_of(case)
        out.append(
            f'<article class="card {tile_class(kind)}"><p class="eyebrow">{esc(kind)}</p>'
            f'{f"<h3>{esc(title)}</h3>" if title else ""}{f"<p>{val(ctx, headline)}</p>" if headline else ""}'
            f'{bullets(ctx, case.get("bullets"))}{source_note(ctx, case) if refs else ""}</article>'
        )
    return f'<div class="grid">{"".join(out)}</div>'


def question_list(ctx: Context, d: dict[str, Any]) -> str:
    out = []
    for q in d.get("questions") or []:
        if isinstance(q, dict):
            why = f"<p><b>Why:</b> {val(ctx, q['why'])}</p>" if q.get("why") else ""
            listen = f"<p><b>Listen for:</b> {val(ctx, q['listen_for'])}</p>" if q.get("listen_for") else ""
            out.append(f'<article class="card"><h3>{val(ctx, q.get("question"), refs_of(q))}</h3>{why}{listen}</article>')
        else:
            out.append(f'<article class="card"><h3>{val(ctx, q)}</h3></article>')
    return f'<div class="grid">{"".join(out)}</div>'


def timeline(ctx: Context, d: dict[str, Any]) -> str:
    out = []
    for e in d.get("events") or []:
        if isinstance(e, dict):
            detail = f"<div>{val(ctx, e['detail'])}</div>" if e.get("detail") else ""
            out.append(f'<li><b>{esc(e.get("date"))}</b> {val(ctx, e.get("title"), refs_of(e))}{detail}</li>')
    return f'<ol class="timeline">{"".join(out)}</ol>'


def text_block(ctx: Context, d: dict[str, Any]) -> str:
    return (f"<p>{val(ctx, d['body'])}</p>" if d.get("body") else "") + bullets(ctx, d.get("bullets"))


def missing_evidence(ctx: Context, d: dict[str, Any]) -> str:
    lis = []
    for item in d.get("items") or []:
        if isinstance(item, dict):
            needed = f" <i>Needed: {esc(item['needed'])}</i>" if item.get("needed") else ""
            lis.append(f"<li>{esc(item.get('item'))}{needed}</li>")
        else:
            lis.append(f"<li>{esc(item)}</li>")
    return f"<ul>{''.join(lis)}</ul>"


def ledger(ctx: Context, sources: list[Any], anchors: bool) -> str:
    out = []
    for s in sources:
        if not isinstance(s, dict):
            continue
        sid = s.get("id")
        url = safe_url(s.get("url"))
        title = esc(s.get("title") or sid)
        link = f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{title}</a>' if url else title
        meta = " · ".join(esc(x) for x in (s.get("type"), s.get("status"), s.get("as_of")) if x)
        extra = "".join(f"<div>{esc(s[k])}</div>" for k in ("excerpt", "pinpoint", "note") if s.get(k))
        anchor = f' id="src-{esc(slug(sid))}"' if anchors and sid else ""
        out.append(f'<div class="src"{anchor}><b>{esc(sid)}</b> {link}{f"<div class=srcnote>{meta}</div>" if meta else ""}{extra}</div>')
    return f'<div class="src-ledger">{"".join(out)}</div>'


def source_list(ctx: Context, d: dict[str, Any]) -> str:
    return ledger(ctx, d.get("sources") or [], False)


MODULES = {
    "decision_box": decision_box,
    "metric_tiles": metric_tiles,
    "highlight_tiles": metric_tiles,
    "executive_summary": executive_summary,
    "key_metrics": make_table("key_metrics"),
    "growth_trajectory": make_table("growth_trajectory"),
    "cards": cards,
    "table": table,
    "scenario_map": scenario_map,
    "question_list": question_list,
    "transcript_qa": make_table("transcript_qa"),
    "read_throughs": make_table("read_throughs"),
    "market_events": make_table("market_events"),
    "bar_chart": bar_chart,
    "financial_trend_chart": financial_trend,
    "eps_actual_vs_estimate_chart": eps_chart,
    "equity_price_event_chart": price_chart,
    "timeline": timeline,
    "text_block": text_block,
    "missing_evidence": missing_evidence,
    "source_list": source_list,
}


def render_dashboard(payload: dict[str, Any], validate: bool = True) -> str:
    if validate:
        report = validate_payload(payload, profile="production")
        if report["hard_failures"]:
            raise ValueError("Dashboard payload failed validation: " + "; ".join(report["hard_failures"]))

    ctx = Context(payload)
    issuer = payload.get("issuer") if isinstance(payload.get("issuer"), dict) else {}
    metadata = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {}
    hero = payload.get("hero") if isinstance(payload.get("hero"), dict) else {}
    layout = "single_page" if payload.get("layout") == "single_page" else "tabs"
    accent = accent_color(issuer)
    hero_refs = refs_of(hero)
    title = payload.get("title") or hero.get("headline") or "Dashboard"

    badge = f'<div class="badge" aria-label="Ticker">{esc(issuer.get("ticker"))}</div>' if issuer.get("ticker") else ""
    callout = ""
    if hero.get("callout"):
        callout = f'<div class="callout"><b>{esc(hero.get("callout_label") or "Core Debate")}</b>{val(ctx, hero["callout"], hero_refs)}</div>'
    dek = f'<p class="dek">{val(ctx, hero["dek"], hero_refs)}</p>' if hero.get("dek") else ""
    sub = f'<p class="dek">{esc(payload["subtitle"])}</p>' if payload.get("subtitle") and not hero.get("dek") else ""
    hero_html = (
        f'<header class="hero">{badge}<div class="hero-main"><p class="eyebrow">{esc(hero.get("eyebrow") or payload.get("mode"))}</p>'
        f'<h1>{esc(hero.get("headline") or title)}</h1>{dek}{sub}{callout}</div></header>'
    )

    banner = ""
    stage = str(metadata.get("payload_stage") or "").lower()
    if stage != "production":
        gaps = validate_payload(payload, profile="draft")["warnings"][:8]
        lis = "".join(f"<li>{esc(g)}</li>" for g in gaps)
        banner = (
            '<div class="banner" role="note"><b>Draft / support payload.</b> Open gaps are retained below; '
            f"this is not PM-ready, client-ready, committee-ready, or publication-ready.{f'<ul>{lis}</ul>' if lis else ''}</div>"
        )

    snapshot = tiles(ctx, payload["snapshot"]) if isinstance(payload.get("snapshot"), list) and payload["snapshot"] else ""

    sections = []
    for tab in payload.get("tabs") or []:
        if isinstance(tab, dict):
            mods = "".join(render_module(ctx, m) for m in tab.get("modules") or [] if isinstance(m, dict))
            sections.append((str(tab.get("id")), str(tab.get("label") or tab.get("id")), mods))
    ledger_sources = [s for s in payload.get("sources") or [] if isinstance(s, dict)]
    model_sources = [ctx.sources[i] for i in ctx.model_ids if i in ctx.sources]
    all_sources = ledger_sources + model_sources
    if all_sources and not any(sid == "sources" for sid, _, _ in sections):
        sections.append(("sources", "Sources", f'<section class="module"><h3>Source Ledger</h3>{ledger(ctx, all_sources, True)}</section>'))

    if layout == "single_page":
        nav = '<nav class="toc" aria-label="Sections">' + "".join(f'<a href="#sec-{esc(slug(i))}">{esc(l)}</a>' for i, l, _ in sections) + "</nav>"
        main = "".join(
            f'<section class="panel" id="sec-{esc(slug(i))}" data-tab="{esc(slug(i))}"><h2>{esc(l)}</h2>{body}</section>' for i, l, body in sections
        )
    else:
        nav = '<div class="tabs" role="tablist">' + "".join(
            f'<button role="tab" type="button" data-tab="{esc(slug(i))}" aria-selected="{"true" if n == 0 else "false"}">{esc(l)}</button>'
            for n, (i, l, _) in enumerate(sections)
        ) + "</div>"
        main = "".join(
            f'<section class="panel" id="sec-{esc(slug(i))}" data-tab="{esc(slug(i))}" role="tabpanel"{"" if n == 0 else " hidden"}><h2>{esc(l)}</h2>{body}</section>'
            for n, (i, l, body) in enumerate(sections)
        )

    foot = " · ".join(esc(metadata[k]) for k in ("freeze_time", "source_posture", "readiness_label") if metadata.get(k))
    noscript = "<noscript><style>.panel[hidden]{display:block}</style></noscript>"
    return (
        '<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>{esc(title)}</title><style>{CSS}:root{{--accent:{accent}}}</style>{noscript}</head>"
        f'<body><div class="page">{hero_html}{banner}{snapshot}{nav}<main>{main}</main><footer>{foot}</footer></div>'
        f"<script>{JS}</script></body></html>\n"
    )

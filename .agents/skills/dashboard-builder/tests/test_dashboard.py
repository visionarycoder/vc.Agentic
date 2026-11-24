import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))

from dashboard.qa import load_payload, validate_payload  # noqa: E402
from dashboard.renderer import render_dashboard  # noqa: E402

EXAMPLES = sorted((SKILL / "assets" / "example_payloads").glob("*.json"))


def chart_payload():
    periods = [
        {"period": f"Q{i}", "revenue": 100 + i * 10, "gross_profit": 60 + i, "net_income": 20 + i, "net_margin": "20%"}
        for i in range(1, 6)
    ]
    eps = [{"period": f"Q{i}", "estimated_eps": 1.0 + i / 10, "actual_eps": 1.1 + i / 10, "basis": "adjusted"} for i in range(1, 4)]
    prices = [{"date": f"2026-05-{d:02d}", "price": 100 + d} for d in range(1, 13)]
    events = [{"date": "2026-05-06", "event": "Guide raised <b>x</b>", "citations": ["S1"]}]
    return {
        "kind": "public_equity_investing_dashboard.v1",
        "layout": "tabs",
        "title": "Charts <script>alert(1)</script>",
        "metadata": {
            "payload_stage": "production", "citation_policy": "strict", "freeze_time": "t", "source_posture": "p",
            "readiness_label": "PM-ready", "readiness_posture": "pm_ready", "decision_context": "c",
        },
        "hero": {"headline": "Charts hero"},
        "tabs": [
            {
                "id": "charts",
                "label": "Charts",
                "modules": [
                    {"type": "financial_trend_chart", "data": {"periods": periods, "citations": ["S1"]}},
                    {"type": "eps_actual_vs_estimate_chart", "data": {"periods": eps, "citations": ["S1"]}},
                    {"type": "equity_price_event_chart", "data": {"prices": prices, "events": events, "citations": ["S1"]}},
                    {"type": "bar_chart", "data": {"items": [{"label": "A", "value": "5", "bar_value": 5}], "citations": ["S1"]}},
                ],
            }
        ],
        "sources": [{"id": "S1", "title": "Src", "url": "https://example.com"}],
    }


class ExamplePayloads(unittest.TestCase):
    def test_expectations(self):
        self.assertTrue(EXAMPLES)
        for path in EXAMPLES:
            payload = load_payload(path)
            production = validate_payload(payload, profile="production")
            with self.subTest(path.name):
                if "fails" in path.name:
                    self.assertTrue(production["hard_failures"])
                    continue
                if path.name == "production-complete-sample.json":
                    self.assertEqual(production["status"], "pass")
                draft = validate_payload(payload, profile="draft")
                self.assertFalse(draft["hard_failures"], draft)
                html = render_dashboard(payload, validate=False)
                self.assertIn(payload.get("hero", {}).get("headline", payload["title"]).replace("&", "&amp;"), html)

    def test_script_cli(self):
        sample = SKILL / "assets" / "example_payloads" / "production-complete-sample.json"
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "index.html"
            result = subprocess.run(
                [sys.executable, str(SKILL / "scripts" / "render_dashboard.py"), str(sample), str(out)],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(out.read_text(encoding="utf-8"))


def chart_html():
    return render_dashboard(chart_payload())


class Rules(unittest.TestCase):
    def test_charts_render_and_escape(self):
        html = chart_html()
        self.assertEqual(html.count("<svg"), 3)
        self.assertNotIn("<script>alert", html)
        self.assertNotIn("<b>x</b>", html)

    def test_thin_price_tape_and_placeholders_fail(self):
        payload = chart_payload()
        payload["tabs"][0]["modules"][2]["data"]["prices"] = payload["tabs"][0]["modules"][2]["data"]["prices"][:4]
        payload["hero"]["dek"] = "TODO write this"
        report = validate_payload(payload)
        text = " ".join(report["hard_failures"])
        self.assertIn("price tape", text)
        self.assertIn("placeholder", text)
        with self.assertRaises(ValueError):
            render_dashboard(payload)

    def test_model_output_citation_and_draft_claims(self):
        payload = chart_payload()
        payload["tabs"][0]["modules"][3]["data"]["citations"] = ["model-output:dcf"]
        self.assertTrue(any("model-output:dcf" in f for f in validate_payload(payload)["hard_failures"]))
        payload["model_citations"] = [{"id": "model-output:dcf", "sheet": "DCF", "cell": "B2"}]
        self.assertFalse(validate_payload(payload)["hard_failures"])
        payload["metadata"]["payload_stage"] = "draft"
        self.assertTrue(validate_payload(payload, profile="draft")["hard_failures"])


if __name__ == "__main__":
    unittest.main()

---
name: "data-analytics-routing"
description: "Route analytical questions to the smallest relevant data workflow using actual sources and available tools."
metadata:
  metadata-version: "1.0.0"
  title: "Data workflow selection"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "data"
---

# Data workflow selection

1. Identify the user's decision, required evidence, available sources, and expected artifact. A task that only asks for a text correction does not require a data workflow.
2. Verify source access and key definitions. Use supplied files, authorized databases, connectors, or documented APIs; do not assume a particular plugin manifest or bundled demo dataset.
3. Select the narrowest matching workflow:

| Need | Workflow |
| --- | --- |
| Trustworthiness, missingness, grain, joins | Data-quality assessment |
| Explain a metric change | Metric diagnosis |
| Define measures and targets | KPI design |
| Make a business or product decision | Evidence-backed analysis |
| Communicate findings | Report or dashboard |
| Explain quantitative relationships | Visualization |

4. Locate the corresponding skill in the current library if present. Use host capabilities that actually exist. Do not require a fixed connector, application, query engine, or provider-specific tool namespace.
5. Keep methods and sources inspectable. State limits when required evidence is unavailable instead of inventing results or silently substituting a weaker source.
6. Deliver in an available format. Analysis does not authorize publishing, messaging, or live data changes.

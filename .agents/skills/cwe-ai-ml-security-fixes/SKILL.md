---
name: "cwe-ai-ml-security-fixes"
description: "Consolidated guidance for AI and ML specific CWE fixes in .NET LLM, generative AI, and classifier integrations."
metadata:
  metadata-version: "1.0.0"
  title: "CWE AI/ML Security Fixes"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "security"
---

# CWE AI/ML Security Fixes

Agent uses this bundle for AI and ML specific weaknesses in .NET services that call LLM or ML inference clients.

## When to Use

| User prompt | Use |
|---|---|
| User asks for prompt-injection fixes in .NET AI code | Use this skill |
| User asks for generative-output validation before execution or rendering | Use this skill |
| User asks for safe inference-parameter handling | Use this skill |
| User asks for adversarial-input handling in custom classifiers | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| User asks for classic SQL, shell, XSS, SSRF, upload, or auth fixes with no AI path | Use the owning CWE skill |
| User asks for model quality, bias review, or product policy | Use a non-security AI skill |
| User asks for broad threat modeling with no code-fix scope | Use `security-controller` |

## Required Inputs

| Input | Required | Description |
|---|---|---|
| Repo or component path | Yes | Scope that contains the AI or ML integration |
| AI surface | Yes | Prompt flow, tool path, hosted client, or classifier |
| CWE subset | No | Default covers CWE-1039, CWE-1426, CWE-1427, and CWE-1434 |
| Validation assets | No | Existing tests, fixtures, allow-lists, or audit needs |

## CWE Coverage

| CWE | Concern | Trigger Pattern | Fix Pattern | Verification |
|---|---|---|---|---|
| 1039 | Adversarial perturbations against recognition | Custom image, audio, text, or sensor classifier accepts crafted near-boundary input with no confidence threshold or reject path | Add confidence thresholds, ambiguity reject paths, secondary verification, rate limits, and telemetry. Use this row only for custom or directly hosted recognition. Hosted AI consumption rarely fits. | Run borderline-input tests. Pass: Low-confidence or inconsistent results trigger reject. |
| 1426 | Improper validation of generative output | LLM output reaches code execution, tool dispatch, SQL, HTML, file writes, or policy decisions as trusted content | Parse into typed DTOs, validate schema and allow-listed values, encode by output context, and keep high-impact actions behind human or policy gates | Run hostile-output tests. Pass: Output fails validation or stays inert. |
| 1427 | Improper neutralization of prompt input | Untrusted user, document, email, web, or ticket text is concatenated directly into a system prompt or tool directive | Separate system instructions from untrusted content with stable delimiters and role boundaries, keep tool policy outside user text, and validate tool arguments before execution | Run prompt-injection fixtures that request override, secret exfiltration, or tool misuse. Pass: Protected instructions remain effective and unsafe tool calls fail validation. |
| 1434 | Insecure inference-parameter settings | End users or low-trust callers set raw temperature, top-p, max tokens, response format, system prompt, model choice, or tool-access flags | Keep parameter selection server-side, apply safe defaults, cap ranges, bind model and tool access to policy, and log approved changes for audit | Run unsafe-parameter tests. Pass: Policy rejects unsafe values and audit log captures changes. |

## Related General Weaknesses (Already Covered)

| CWE | Owning Skill | AI or ML Twist |
|---|---|---|
| CWE-22 | `cwe-miscellaneous-security-fixes` | Retrieval, fine-tuning, or artifact paths use user-controlled filenames or archive entries. |
| CWE-77 | `cwe-injection-attack-fixes` | Agent output or tool arguments reach an interpreter or shell sink. |
| CWE-78 | `cwe-injection-attack-fixes` | Tool-calling or orchestration features pass model-produced command text to OS execution. |
| CWE-79 | `cwe-injection-attack-fixes` | Generated summaries or rich responses render into HTML or chat UI without encoding. |
| CWE-94 | `cwe-injection-attack-fixes` | Generated code or script text reaches a runtime execution surface. |
| CWE-95 | Not yet covered | Generated expression text reaches an eval-like expression engine. |
| CWE-116 | Not yet covered | Prompt and output normalization gaps leave hostile control tokens intact. |
| CWE-250 | Not yet covered | AI agent actions run with broader privileges than the caller or task policy. |
| CWE-434 | `cwe-miscellaneous-security-fixes` | Model, prompt-template, or embedding artifact upload accepts hostile file types or content. |
| CWE-502 | `cwe-data-protection-fixes` | Serialized or pickled model artifacts deserialize from untrusted sources. |
| CWE-862 | `cwe-authentication-authz-fixes` | Tool invocation or agent action lacks per-action authorization. |
| CWE-918 | `cwe-miscellaneous-security-fixes` | Agentic fetch, browse, or connector features let the model reach internal URLs. |
| CWE-1336 | Not yet covered | Prompt-construction mistakes create template or expression injection in transformation logic. |

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 1 | Agent inventories prompt assembly, tool-calling, output use, parameter binding, and classifier entry points. | Run `rg -n "AzureOpenAI|Prompt|temperature|tool|MLContext|PredictionEngine" -g "**/*.{cs,json,md}"`. | Hotspot list exists for every touched file. |
| 2 | Agent maps each hotspot to one AI-specific CWE row or to a related general weakness row. | Review hotspot list. | Every hotspot has one label or explicit out-of-scope note. |
| 3 | Agent adds instruction separation, output validation, policy-gated tool execution, or safe parameter control. | Run targeted build for touched project. | Build passes with zero new errors. |
| 4 | Agent runs existing prompt, integration, API, or policy tests for the touched scope. | Run existing tests for the touched component. | All targeted tests pass. |
| 5 | Agent re-scans prompt and inference code for direct concatenation and unsafe override paths. | Re-run inventory command and targeted grep. | Zero unexplained targeted hits remain in touched files. |

## Verification Checklist

- [ ] Agent verified that generative output stays untrusted until validation passes.
- [ ] Agent verified that system instructions and tool policy stay outside untrusted prompt text.
- [ ] Agent verified that tool arguments pass validation before execution.
- [ ] Agent verified that unsafe inference-parameter overrides are blocked or policy-gated.
- [ ] Agent verified that CWE-1039 guidance appears only on custom recognition or classifier scope.

## Common Pitfalls

| Pitfall | Agent fix |
|---|---|
| Prompt text mixes system policy and user content in one raw string | Agent splits trusted instructions from untrusted content with stable delimiters and roles. |
| Tool call executes model output directly | Agent validates tool name and arguments against typed policy before execution. |
| Structured output is treated as trusted without schema validation | Agent parses into typed DTOs and rejects unknown or out-of-range values. |
| User-facing settings expose raw model parameters | Agent moves parameter control to server policy with bounded overrides and audit logging. |
| Hosted AI client usage is mislabeled as adversarial-model hardening work | Agent limits CWE-1039 use to custom recognition components that the repo owns. |

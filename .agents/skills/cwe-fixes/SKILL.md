---
name: "cwe-fixes"
description: "Route broad security hardening or CWE remediation requests to correct thematic bundle skills. Aggregate results into one verified report."
metadata:
  metadata-version: "1.0.0"
  title: "CWE Fixes Bundle"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "security"
---

# CWE Fixes Bundle

Agent uses this bundle for broad security remediation requests touching multiple CWE families or needing one coordinated hardening pass.

Agent acts as the primary broad-security execution skill after `security-intake-router` classifies a mixed or sweep-style request.

## When to Use

Use when:
- User asks for CWE sweep, MITRE Top 25 pass, or broad hardening review
- Request names multiple vulnerabilities: injection, auth, SSRF, deserialization, path traversal
- One report covering multiple security themes is needed

## When Not to Use

Do not use when:
- Single narrow vulnerability family maps cleanly to one thematic bundle
- Penetration testing or external scanner orchestration
- Unrelated code cleanup that only incidentally mentions security

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Scope | Yes | Repo, app area, controller set, or other target surface |
| Threat focus | No | Specific CWEs, OWASP-style concerns, or broad sweep |
| Stack context | No | Language, framework, entry-point hints help skip irrelevant bundles |
| Verification expectations | No | Build, tests, analyzer, or endpoint checks required after fixes |

## Workflow

Agent performs:

1. Agent decides which CWE families are in scope. Agent marks rest explicitly as out of scope or not applicable.
2. Agent routes each in-scope concern to correct thematic bundle.
3. Agent groups findings, fixes by file to reduce churn.
4. Agent verifies every touched area with existing build, test, analyzer coverage.
Test: Run `dotnet build`, `dotnet test`
Pass: Zero new build errors. Zero test failures.
5. Agent delivers one consolidated remediation report.

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Treat every CWE as applicable to every stack | Skip irrelevant families explicitly |
| Fix issues one finding at a time across same file | Batch file-local changes together |
| Claim remediation without verification | Build, test, or otherwise verify touched areas |
| Mix scanner output with unverified code claims | Ground findings in actual repository evidence |

## Bundle Routing Matrix

| User Request Contains | Route To | Covers |
|---|---|---|
| "validation" / "bounds" / "buffer" / "overflow" | `cwe-input-validation-fixes` | Validation, bounds, memory-safety style input issues |
| "authentication" / "authorization" / "CSRF" / "access control" | `cwe-authentication-authz-fixes` | Authentication, authorization, CSRF, access-control issues |
| "injection" / "SQL" / "command" / "XSS" / "code execution" | `cwe-injection-attack-fixes` | Command, code, HTML, SQL, related injection issues |
| "disclosure" / "deserialization" / "secret" / "leak" | `cwe-data-protection-fixes` | Information disclosure, deserialization, secret handling, ownership leaks |
| "logging injection" / "DoS" / "resource" / "privilege" | `cwe-resource-management-fixes` | Logging injection, integer/resource misuse, privilege, DoS, lifecycle issues |
| "path traversal" / "upload" / "redirect" / "SSRF" / "null pointer" | `cwe-miscellaneous-security-fixes` | Path traversal, upload, null-deref, open redirect, SSRF, filesystem permission issues |
| "search path" / "DLL hijacking" / "format string" | `cwe-format-external-fixes` | External search-path / format-specific issues |

## Cross-Cutting Security Rules

| Rule | Pattern |
|---|---|
| Input handling | Verify at trust boundary with framework-native validation |
| Dangerous sinks | Never concatenate untrusted input into SQL, shell, HTML, URLs, paths, logs |
| Logging | Use structured logging. Sanitize hostile input. |
| Errors | Expose safe external messages. Keep sensitive detail server-side. |
| Access control | Require authn/authz, ownership checks for state-changing or sensitive operations |
| Deserialization | Avoid type-open or unsafe serializers for untrusted input |
| Secrets | Keep out of source, static config |
| Resource use | Enforce request, concurrency, timeout, pagination limits |

## Verification Checklist

Agent verifies:
- [ ] Applicability stated per CWE family instead of assuming all 42 apply
- [ ] Every in-scope concern routed to correct thematic bundle
- [ ] Fixes grouped by file, kept surgical
- [ ] Existing builds, tests, analyzers used for verification
- [ ] Final report marks clean, fixed, follow-up items clearly
- [ ] Out-of-scope or non-applicable CWE families include rationale

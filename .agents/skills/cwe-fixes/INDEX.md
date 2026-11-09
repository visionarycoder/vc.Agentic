---
title: CWE Skill Routing Index
doc_type: reference
status: active
last_updated: 2026-07-25
target_audience: ai
complexity: low
estimated_tokens: 822
prerequisites:
  - cwe-fixes-bundle
related_skills:
  - cwe-fixes-bundle
appliesTo: '**/*.{cs,csproj,json,md}'
tags:
  - cwe
  - reference
---
# CWE Skill Routing Index

Load only the skills you need. Each is self-contained.

## By CWE number

| CWE | Title | Skill |
|---:|---|---|
| 20 | Improper Input Validation | `cwe20-fix` |
| 22 | Path Traversal | `cwe22-fix` |
| 77 | Command Injection (Generic) | `cwe77-fix` |
| 78 | OS Command Injection | `cwe78-fix` |
| 79 | Cross-Site Scripting (XSS) | `cwe79-fix` |
| 89 | SQL Injection | `cwe89-fix` |
| 94 | Code Injection | `cwe94-fix` |
| 98 | PHP Remote File Inclusion | `cwe98-fix` |
| 117 | Log Injection | `cwe117-fix` |
| 119 | Buffer bounds (native) | `cwe119-fix` |
| 120 | Classic Buffer Overflow | `cwe120-fix` |
| 121 | Stack Buffer Overflow | `cwe121-fix` |
| 122 | Heap Buffer Overflow | `cwe122-fix` |
| 125 | Out-of-bounds Read | `cwe125-fix` |
| 190 | Integer Overflow | `cwe190-fix` |
| 200 | Sensitive Info Exposure | `cwe200-fix` |
| 266 | Incorrect Privilege Assignment | `cwe266-fix` |
| 269 | Improper Privilege Management | `cwe269-fix` |
| 276 | Incorrect Default Permissions | `cwe276-fix` |
| 284 | Improper Access Control (umbrella) | `cwe284-fix` |
| 287 | Improper Authentication | `cwe287-fix` |
| 288 | Auth Bypass via Alternate Path | `cwe288-fix` |
| 306 | Missing Auth for Critical Function | `cwe306-fix` |
| 352 | CSRF | `cwe352-fix` |
| 363 | TOCTOU Link Following | `cwe363-fix` |
| 400 | Uncontrolled Resource Consumption | `cwe400-fix` |
| 401 | Missing Resource Release | `cwe401-fix` |
| 416 | Use After Free | `cwe416-fix` |
| 427 | Uncontrolled Search Path (DLL Hijack) | `cwe427-fix` |
| 434 | Unrestricted File Upload | `cwe434-fix` |
| 476 | NULL Pointer Dereference | `cwe476-fix` |
| 502 | Deserialization of Untrusted Data | `cwe502-fix` |
| 601 | Open Redirect | `cwe601-fix` |
| 639 | IDOR | `cwe639-fix` |
| 732 | Critical Resource Permissions | `cwe732-fix` |
| 770 | Allocation Without Limits | `cwe770-fix` |
| 787 | Out-of-bounds Write | `cwe787-fix` |
| 798 | Hard-coded Credentials | `cwe798-fix` |
| 862 | Missing Authorization | `cwe862-fix` |
| 863 | Incorrect Authorization | `cwe863-fix` |
| 918 | SSRF | `cwe918-fix` |
| 1174 | ASP.NET Improper Model Validation | `cwe1174-fix` |

## By category (load these together)

- **Injection:** 77, 78, 79, 89, 94, 98, 117
- **Memory safety (native):** 119, 120, 121, 122, 125, 416, 476, 787
- **Access control:** 266, 269, 276, 284, 352, 639, 732, 862, 863
- **Authentication:** 287, 288, 306, 798
- **Deserialization / files / assemblies:** 427, 434, 502
- **Resource / concurrency:** 190, 363, 400, 401, 770
- **Path / URL / SSRF:** 22, 601, 918
- **Info exposure:** 200
- **Input validation / framework misconfig:** 20, 1174

## By likely applicability

- **Every managed web API (.NET/Java/Node/Python):** 20, 22, 79, 89, 94, 117, 200, 284, 287, 306, 352, 400, 434, 502, 601, 639, 770, 798, 862, 863, 918, 1174
- **Native / unsafe code only:** 119, 120, 121, 122, 125, 416, 476, 787, 363
- **Ops / IaC / packaging:** 266, 269, 276, 288, 427, 732, 798
- **PHP-only:** 98

---
name: "cwe-data-protection-fixes"
description: "Consolidated guidance for data-protection CWEs (CWE-200, CWE-209, CWE-295, CWE-319, CWE-502, CWE-798, CWE-639, CWE-401, CWE-363) with detection patterns, fix patterns, and measurable verification."
metadata:
  metadata-version: "1.0.0"
  title: "CWE Data Protection Fixes"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "security"
---

# CWE Data Protection Fixes

Agent uses this bundle for disclosure, unsafe deserialization, secret exposure, IDOR, resource leak, and file race defects.

## Activation

**USE FOR:** CWE-200, CWE-209, CWE-295, CWE-319, CWE-502, CWE-798, CWE-639, CWE-401, CWE-363.
**DO NOT USE FOR:** General authorization routing, input bounds defects, or style-only refactors.

## Critical Rules

| Rule | Test | Pass |
|---|---|---|
| Agent keeps secrets out of source, config literals, and image layers. | Run secret scan on touched files. | Zero active secret hits remain. |
| Agent replaces unsafe type-open deserialization on untrusted input. | Run grep for banned serializers. | Zero banned serializer hits remain in touched files. |
| Agent returns safe error payloads to callers. | Run exception-path tests. | External responses exclude stack traces, SQL, and environment values. |
| Agent validates server certificates and host keys on outbound connections. | Run connection tests against a mismatched or self-signed endpoint. | Connection fails closed on validation mismatch; no blanket accept-all callback remains. |
| Agent encrypts data in transit for credential-bearing and sensitive-data protocols. | Run protocol/config review for touched transport clients. | Touched clients negotiate TLS/FTPS/SFTP rather than defaulting to cleartext. |
| Agent verifies ownership for user-supplied identifiers. | Run owner and non-owner tests. | Non-owner returns 404 or 403. |
| Agent closes disposable resources with scope-based disposal. | Run analyzers and leak-focused tests already in repo. | Zero new disposal findings appear. |

## CWE Coverage

| CWE | Concern | Trigger Pattern | Fix Pattern | Verification | SFP Cluster |
|---|---|---|---|---|---|
| 200 | Sensitive information exposure | `ex.ToString()`, developer page, entity serialization, verbose headers | Use DTOs, central exception handler, safe Problem Details | Run error-path tests. Pass: No sensitive fields in response. | Information Leak (895) > Exposed Data (963) |
| 209 | Error message with sensitive information | Caught-exception message, class/method name, config path, or query text written straight into an HTTP response or client-facing log | Gate `ex.Message`/internal identifiers behind an environment check (e.g. `IHostEnvironment.IsProduction()`); return a generic message plus correlation ID to the caller and log full detail server-side only | Run exception-path tests in a production-mode host config. Pass: Client response contains no exception text, internal type/method names, or file paths. | Information Leak (895) > Exposed Data (963) |
| 502 | Unsafe deserialization | `BinaryFormatter`, `NetDataContractSerializer`, `TypeNameHandling` | Use `System.Text.Json` typed DTOs and explicit discriminators | Run grep and deserialization tests. Pass: Invalid polymorphic payloads fail. | Tainted Input (896) > Tainted Input to Variable (994) |
| 295 | Improper certificate/host-key validation | Blanket-accept TLS certificate callback, SSH/SFTP client with no `HostKeyReceived` handler, `ValidateAnyCertificate = true` | Validate the certificate chain/host-key fingerprint against a pinned or CA-trusted value; reject on mismatch instead of trusting by default | Run connection tests against a mismatched certificate/host key. Pass: Connection is rejected. | Authentication (898) > Digital Certificate (948) |
| 319 | Cleartext transmission of sensitive information | FTP/HTTP client with no encryption mode set, credentials or financial data sent over plain sockets | Set explicit TLS/FTPS/SFTP encryption mode as the default; fail closed if the target cannot negotiate encryption | Run a protocol-level check confirming the negotiated session is encrypted. Pass: Plaintext fallback is not silently accepted. | Information Leak (895) > Exposed Data (963) |
| 798 | Hard-coded credentials | Secrets in code, Dockerfile, config, scripts | Move secrets to Key Vault or secret store and rotate exposed values | Run secret scan. Pass: Zero active secret hits remain. | Not present in CWE-888 SFP taxonomy. |
| 639 | IDOR | Query by route id without ownership predicate | Scope query by authenticated principal | Run access tests. Pass: Non-owner cannot read or write data. | Not present in CWE-888 SFP taxonomy. |
| 401 | Resource leak | Missing `using`, new `HttpClient` per request, unclosed stream | Use `using`, `await using`, or factory pattern | Run analyzers or stability tests. Pass: Zero new leak findings. | Not present in CWE-888 SFP taxonomy. |
| 363 | TOCTOU race | `File.Exists` before later open or delete | Open stable handle first and verify handle state | Run race or symlink tests when present. Pass: Swap attack fails. | Not present in CWE-888 SFP taxonomy. |

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 1. Inventory | Agent runs scans for secrets, serializers, error leaks, IDOR, disposables, and pre-open file race logic. | Run repo grep and secret scan commands already used by the repo. | Hotspot list exists for every touched file. |
| 2. Classify | Agent maps each hotspot to one CWE row. | Review hotspot list. | Every hotspot has one CWE label or explicit out-of-scope note. |
| 3. Fix | Agent moves secrets, replaces serializers, adds ownership gates, and closes resource scope. | Run targeted build for touched project. | Build passes with zero new errors. |
| 4. Run tests | Agent runs unit tests, integration tests, and scan jobs for touched scope. | Run existing tests and secret scans for touched scope. | All targeted tests pass. Zero secret hits remain. |
| 5. Re-scan | Agent runs grep and secret scans again. | Re-run inventory commands. | Zero unexplained banned patterns remain in touched files. |

## Decision Matrix

| Condition | Use |
|---|---|
| Input deserializes from network or queue | Use typed DTOs and explicit discriminators |
| Request accesses user-owned resource | Use ownership predicate in query or handler |
| Secret appears in code or config | Move to secret store and rotate value |
| File workflow uses pre-open existence logic | Use handle-first logic |
| Disposable object has request scope | Use `using`, `await using`, or factory-managed scope |

## Detection Commands

| Concern | Command | Pass |
|---|---|---|
| Unsafe serializers | `rg -n "BinaryFormatter|SoapFormatter|NetDataContractSerializer|TypeNameHandling\." -g "**/*.cs"` | Zero targeted hits in touched files |
| Error leaks | `rg -n "UseDeveloperExceptionPage|ex\.ToString\(|ex\.Message.*WriteAsJsonAsync|X-Powered-By|X-AspNet-Version" -g "**/*.cs"` | Zero targeted hits in touched files |
| Weak transport trust | `rg -n "HostKeyReceived|ValidateAnyCertificate|EncryptionMode|ServerCertificateCustomValidationCallback|CanTrust\s*=\s*true" -g "**/*.cs"` | Every hit is reviewed for a fail-closed validation path |
| Secret literals | Use repo secret scan or `gitleaks` command already present in CI | Zero active secret hits |
| IDOR entry points | `rg -n "\{id\}|\{userId\}|\{orderId\}" -g "**/*.cs"` | Every route has ownership review |

## Verification Checklist

Agent verifies:
- [ ] Secret scans report zero active secrets in touched files
- [ ] Banned serializers are absent from touched files
- [ ] Error responses are safe for external users
- [ ] Certificate/host-key validation fails closed on mismatch
- [ ] Credential-bearing transport clients negotiate encryption by default
- [ ] Ownership tests pass for positive and negative cases
- [ ] Disposal and resource-scope defects do not increase

## Inputs

| Input | Required | Default |
|---|---|---|
| Repo or project path | Yes | - |
| CWE subset | No | All 7 |
| Secret scan command | No | Existing repo default |

## Outputs

Agent generates:
- Hotspot list with CWE labels
- Patch set for disclosure, serializer, secret, IDOR, and leak fixes
- Verification notes with scan and test results
- Rotation note when a real secret is exposed

## References

- MITRE CWE-209: https://cwe.mitre.org/data/definitions/209.html
- MITRE CWE-295 (Improper Certificate Validation): https://cwe.mitre.org/data/definitions/295.html
- MITRE CWE-319 (Cleartext Transmission of Sensitive Information): https://cwe.mitre.org/data/definitions/319.html
- RFC 9457 Problem Details
- OWASP IDOR guidance
- Microsoft BinaryFormatter migration guidance
- GitHub secret scanning and gitleaks guidance

## Additional source coverage

The selected version is the preferred starting point by the recorded date/context basis. Distinct source coverage is retained in the scoped references; do not apply superseded or conflicting defaults automatically.

- [cwe-data-protection-fixes-alternative-1](references/contexts/cwe-data-protection-fixes-alternative-1/guide.md)
- [cwe-data-protection-fixes-alternative-2](references/contexts/cwe-data-protection-fixes-alternative-2/guide.md)

---
name: "cwe-data-protection-fixes"
description: "Consolidated guidance for data-protection CWEs (CWE-200, CWE-209, CWE-295, CWE-319, CWE-502, CWE-798, CWE-639, CWE-401, CWE-363) with detection patterns, fix patterns, and measurable verification."
metadata:
  metadata-version: "1.0.0"
  title: "CWE Data Protection Fixes"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "security"
---

# CWE Data Protection Fixes

Agent uses this bundle for disclosure, unsafe deserialization, secret exposure, IDOR, resource leak, and file race defects.

## Activation

**USE FOR:** CWE-200, CWE-209, CWE-295, CWE-319, CWE-502, CWE-798, CWE-639, CWE-401, CWE-363.
**DO NOT USE FOR:** General authorization routing, input bounds defects, or style-only refactors.

## Rules

- Keep secrets out of source, config, and image layers; rotate any real exposed secret and note the rotation.
- Return safe error payloads (generic message plus correlation ID); gate `ex.Message` behind `IHostEnvironment.IsProduction()`.
- Validate server certificates and host keys; fail closed, no accept-all callbacks. Default to TLS/FTPS/SFTP with no plaintext fallback.
- Check ownership for user-supplied identifiers; non-owners get 404 or 403.
- Dispose with `using`, `await using`, or factory-managed scope.

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

## Detection Commands

| Concern | Command | Pass |
|---|---|---|
| Unsafe serializers | `rg -n "BinaryFormatter|SoapFormatter|NetDataContractSerializer|TypeNameHandling\." -g "**/*.cs"` | Zero targeted hits in touched files |
| Error leaks | `rg -n "UseDeveloperExceptionPage|ex\.ToString\(|ex\.Message.*WriteAsJsonAsync|X-Powered-By|X-AspNet-Version" -g "**/*.cs"` | Zero targeted hits in touched files |
| Weak transport trust | `rg -n "HostKeyReceived|ValidateAnyCertificate|EncryptionMode|ServerCertificateCustomValidationCallback|CanTrust\s*=\s*true" -g "**/*.cs"` | Every hit is reviewed for a fail-closed validation path |
| Secret literals | Use repo secret scan or `gitleaks` command already present in CI | Zero active secret hits |
| IDOR entry points | `rg -n "\{id\}|\{userId\}|\{orderId\}" -g "**/*.cs"` | Every route has ownership review |

## Inputs

| Input | Required | Default |
|---|---|---|
| Repo or project path | Yes | - |
| CWE subset | No | All listed |
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

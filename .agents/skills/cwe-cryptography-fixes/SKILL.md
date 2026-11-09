---
name: "cwe-cryptography-fixes"
description: "Guidance for C#/.NET cryptography and predictability CWEs with trigger patterns, fix patterns, and verification."
metadata:
  metadata-version: "1.0.0"
  title: "CWE Cryptography Fixes"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "security"
---

# CWE Cryptography Fixes

Agent uses this bundle for algorithm, key, hash, IV, nonce, signature, and randomness defects.

## Activation

**USE FOR:** CWE-327, CWE-328, CWE-321, CWE-323, CWE-326, CWE-329, CWE-347, CWE-330, CWE-338, CWE-335, CWE-336, CWE-337, CWE-759, CWE-760.
**DO NOT USE FOR:** Certificate validation, cleartext transport, unsafe deserialization, or data-protection defects covered by `cwe-data-protection-fixes`; general authorization routing; style-only refactors.

## Critical Rules

| Rule | Test | Pass |
|---|---|---|
| Agent replaces broken and weak algorithms with current primitives. | Run analyzers and grep for legacy algorithms and weak hashes. | Zero touched hits remain for `DES`, `RC2`, `TripleDES`, `MD5`, and `SHA1` in security paths. |
| Agent keeps cryptographic keys out of source and checked-in config. | Run secret and source scans. | Zero hard-coded production keys remain. |
| Agent generates a fresh random IV or nonce for each encryption operation. | Run repeated-encrypt tests. | IV and nonce values do not repeat across the sample. |
| Agent uses cryptographic RNG and explicit signature verification for trust decisions. | Run CA5394 and signature tests. | Zero security `System.Random` hits remain; tampered signatures fail. |

## CWE Coverage

| CWE | Concern | Trigger Pattern | Fix Pattern | Verification |
|---|---|---|---|---|
| 327 | Broken or risky algorithm | `DES`, `RC2`, `TripleDES`, `MD5`, `SHA1`, `System.Security.Cryptography.DES` | Use `AesGcm`, `SHA256` or `SHA512`, `RSA`, or `ECDsa` | CA5350 and CA5351. Pass: No weak-algorithm hits. |
| 328 | Weak hash | `MD5` or `SHA1` for password or integrity logic | Use `SHA256`, `SHA512`, `SHA3`, or platform password hashing APIs | Unit and analyzer checks. Pass: No weak-hash security path remains. |
| 759 | One-way hash without salt | Raw password hash with no per-password salt | Use `PasswordHasher<T>`, `Rfc2898DeriveBytes`, or approved Argon2 | Password tests. Pass: Same password yields different stored output. |
| 760 | One-way hash with predictable salt | Salt from username, email, tenant id, static bytes, or config | Use `RandomNumberGenerator` salt or `PasswordHasher<T>` | Password tests. Pass: Salt source is random. |
| 321 | Hard-coded cryptographic key | AES, HMAC, JWT, or RSA key literal in source or checked-in config | Load keys from Azure Key Vault or approved secret configuration | Secret scan and config review. Pass: No key literal remains. |
| 323 | Reused nonce or key pair | Static IV or nonce reused across `AesGcm`, `AesCcm`, or `Aes` | Generate a fresh nonce or IV with `RandomNumberGenerator` per encrypt call | N-call test. Pass: No IV or nonce repeats. |
| 326 | Inadequate encryption strength | `RSA` below 2048, `AES` below 128, or downgraded parameters | Enforce current minimum key sizes and reject weak config | Config and unit tests. Pass: Weak sizes fail validation. |
| 329 | Predictable IV with CBC mode | Zero IV, static IV, or IV from timestamp or record id | Prefer `AesGcm`; if CBC remains, generate random IV per message | Repeated-encrypt test. Pass: CBC IV stays random and unique. |
| 347 | Improper signature verification | Verify branch skipped, result ignored, or normal equality in trust compare | Use framework verify APIs and `CryptographicOperations.FixedTimeEquals` | Positive and tampered tests. Pass: Tampered signatures fail. |
| 330, 338 | Insufficient randomness or weak PRNG | `System.Random`, `Random.Shared`, or GUID slicing for tokens, salts, or keys | Use `RandomNumberGenerator` APIs or approved wrapper | CA5394 and token tests. Pass: Security randomness uses cryptographic RNG only. |
| 335, 336, 337 | Incorrect, same, or predictable seed | `new Random(0)`, `new Random(DateTime.Now.Millisecond)`, reused seed | Remove manual seeding and use `RandomNumberGenerator` | Grep and repeatability tests. Pass: Security output is not seed-based. |

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 1. Inventory | Agent scans for legacy algorithms, weak hashes, hard-coded keys, reused IVs and nonces, weak key sizes, skipped signature checks, and `Random` in trust-sensitive paths. | Run grep and analyzers. | Hotspot list exists for every touched file. |
| 2. Classify | Agent maps each hotspot to one CWE row and one primary cluster: Cryptography or Predictability. | Review hotspot list. | Every hotspot has one CWE label or explicit out-of-scope note. |
| 3. Fix | Agent replaces risky primitives, externalizes keys, randomizes IVs and nonces, hardens signature checks, and upgrades password hashing. | Run targeted build. | Build passes with zero new errors. |
| 4. Run tests | Agent runs unit tests and analyzer jobs already in the repo for touched scope. | Run existing tests and analyzer commands. | All targeted tests pass. |
| 5. Re-scan | Agent runs inventory commands again after the patch. | Re-run grep and analyzers. | Zero unexplained weak-crypto and weak-randomness hits remain in touched files. |

## Decision Matrix

| Condition | Use |
|---|---|
| Code encrypts new sensitive payloads | Use `AesGcm` with per-operation random nonce |
| Code hashes or verifies passwords | Use ASP.NET Core Identity `PasswordHasher<T>` or approved PBKDF or Argon2 |
| Code needs signing or signature verification | Use framework verify APIs and constant-time byte comparison for trust decisions |
| Code stores or loads cryptographic keys | Use Azure Key Vault backed configuration, not literals |
| Code generates tokens, salts, IVs, or session ids | Use `RandomNumberGenerator`, not `System.Random` |

## Repo Notes

| Area | Agent Uses | Agent Avoids |
|---|---|---|
| Key storage | Azure Key Vault and typed options | Source literals and checked-in secrets |
| Password hashing | ASP.NET Core Identity `PasswordHasher<T>` or approved KDF wrapper | Raw `SHA256`, `SHA512`, and home-grown salt logic |
| Randomness and encryption | `RandomNumberGenerator` and `AesGcm` | `System.Random`, GUID slicing, static IV arrays, and predictable CBC IVs |

## Verification Checklist

Agent verifies:
- [ ] Touched files contain no broken or weak algorithm usage
- [ ] Production key material is absent from source and checked-in config
- [ ] IV and nonce generation is random and non-repeating across the test sample
- [ ] Password hashing uses salted KDF or platform identity hashing
- [ ] Security-sensitive randomness does not use `System.Random`
- [ ] Signature verification rejects tampered inputs

## Inputs

| Input | Required | Default |
|---|---|---|
| Repo or component path | Yes | - |
| CWE subset | No | All 14 covered CWEs |
| Analyzer and test commands | No | Existing repo defaults |

## Outputs

Agent generates:
- Hotspot list with CWE and cluster labels
- Patch set for crypto and predictability fixes
- Verification notes with analyzer and test results

## References

- MITRE CWE-888: https://cwe.mitre.org/data/definitions/888.html
- MITRE CWE-903, CWE-958, CWE-959, and CWE-905 cluster pages
- MITRE base CWEs: 321, 323, 326, 327, 328, 329, 330, 335, 336, 337, 338, 347, 759, 760
- Microsoft CA5350, CA5351, and CA5394 analyzers
- Microsoft `RandomNumberGenerator`, `AesGcm`, `PasswordHasher<T>`, and `CryptographicOperations.FixedTimeEquals` guidance

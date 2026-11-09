---
name: "cwe-channel-fixes"
description: "Consolidated guidance for channel spoofing, replay, proxy, integrity, downgrade, and protected-channel CWEs with measurable fixes and verification."
metadata:
  metadata-version: "1.0.0"
  title: "CWE Channel Fixes"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "security"
---

# CWE Channel Fixes

Agent uses this bundle for channel-layer spoofing, replay, downgrade, proxy, integrity, and protected-channel defects.

## Activation

**USE FOR:** CWE-290, CWE-294, CWE-300, CWE-353, CWE-419, CWE-420, CWE-441, CWE-757.
**DO NOT USE FOR:** App-layer identity, session, authorization, or CSRF defects handled by `cwe-authentication-authz-fixes`; broad cryptography storage defects; unrelated network architecture redesign.

## Critical Rules

| Rule | Test | Pass |
|---|---|---|
| Agent blocks authorization decisions that trust source IP, hostname, or proxy headers without channel proof. | Run requests with forged forwarding headers or peer metadata. | Forged network identity does not grant access. |
| Agent rejects replayable requests and tokens on sensitive operations. | Run the same signed request twice inside the allowed window. | Replay attempt is rejected or marked duplicate. |
| Agent protects primary and alternate channels with authenticated encryption and endpoint trust. | Run transport checks on public, admin, debug, and callback paths. | Touched channels require approved protection. |
| Agent verifies message integrity before processing privileged content. | Run tampered payload tests against signed or MAC-protected messages. | Tampered message is rejected before side effects. |
| Agent enforces minimum secure protocol and algorithm negotiation. | Run config tests for deprecated TLS versions and weak ciphers. | Deprecated versions and weak suites are disabled. |

## CWE Coverage

| CWE | Concern | Trigger Pattern | Fix Pattern | Verification |
|---|---|---|---|---|
| 290 | Authentication bypass by spoofing | Authorization trusts `RemoteIpAddress`, hostname, or `X-Forwarded-For` | Use authenticated principals, trusted proxy configuration, and mutual channel proof where required | Run forged-header tests. Pass: Access decision ignores spoofed network identity. |
| 294 | Authentication bypass by capture-replay | Signed URL, token, webhook, or command lacks nonce, timestamp, or replay cache | Add nonce, timestamp, expiry, replay cache, and bounded clock-skew validation | Run replay test. Pass: Second use is rejected. |
| 300 | Channel accessible by non-endpoint | Sensitive channel accepts traffic without mutual TLS, pinning, or endpoint validation | Require mutual TLS, certificate validation, pinning when the repo pattern uses it, and explicit peer allow-list | Run untrusted-peer test. Pass: Non-endpoint intermediary cannot complete session. |
| 353 | Missing support for integrity check | Queue, webhook, callback, or file transfer accepts content without HMAC or signature verification | Verify HMAC or signature before parse or execution and reject unsigned payloads | Run tampered-payload test. Pass: Modified content fails verification. |
| 419 | Unprotected primary channel | Primary admin, control, or data channel allows plaintext or unauthenticated access | Require authenticated encryption and endpoint authentication on the primary channel | Run channel probe. Pass: Primary channel rejects insecure access. |
| 420 | Unprotected alternate channel | Debug, maintenance, failover, callback, or management side channel bypasses normal transport controls | Apply the same transport policy to alternate channels or disable the channel | Run alternate-path probe. Pass: Side channel is protected or unavailable. |
| 441 | Unintended proxy or intermediary | Service forwards caller input to downstream target without validating target or delegated permission | Validate downstream target, scope delegated credentials, and bind forwarding to explicit policy | Run confused-deputy test. Pass: Service refuses unauthorized forwarding. |
| 757 | Selection of less-secure algorithm during negotiation | TLS negotiation permits deprecated versions, weak ciphers, or downgrade fallback | Set minimum protocol, approved cipher policy, and disable insecure fallback | Run protocol scan. Pass: Downgrade path fails and weak options stay disabled. |

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 1. Inventory | Agent scans transport, proxy, webhook, callback, forwarding, and TLS configuration paths. | Run `rg -n "RemoteIpAddress|X-Forwarded|Forwarded|ClientCertificate|SslProtocols|webhook|HMAC|signature|proxy|callback" -g "**/*.{cs,json,yml,yaml,config,xml,props,targets}"`. | Hotspot list exists for each touched file. |
| 2. Classify | Agent maps each hotspot to one CWE row. | Review hotspot list. | Every hotspot has one CWE label or explicit out-of-scope note. |
| 3. Fix | Agent adds replay protection, trusted proxy rules, endpoint validation, integrity checks, and secure negotiation settings. | Run targeted build for the touched project. | Build passes with zero new errors. |
| 4. Run tests | Agent runs existing transport, webhook, integration, or configuration tests for touched scope. | Run existing tests for touched scope. | All targeted tests pass. |
| 5. Re-scan | Agent runs grep and config checks again. | Re-run inventory commands. | Zero unexplained targeted hits remain in touched files. |

## Decision Matrix

| Condition | Use |
|---|---|
| Access decision depends on network origin | Use authenticated principal or trusted proxy boundary, not raw peer data |
| Request can be captured and replayed | Use nonce, timestamp, expiry, and replay cache |
| Service accepts privileged callback or webhook | Use signature or HMAC verification before processing |
| Service forwards caller intent to downstream target | Use explicit target allow-list and delegated authorization checks |
| Service negotiates transport algorithms | Use minimum secure protocol and approved cipher set |

## ASP.NET Core Patterns

| Area | Agent Uses | Agent Avoids |
|---|---|---|
| Forwarded headers | Known proxies, known networks, and explicit header processing | Trusting arbitrary forwarding headers from the public internet |
| Client identity | `HttpContext.User`, validated certificates, or signed message identity | IP or DNS identity as the sole authorization source |
| Replay defense | Nonce store, timestamp window, idempotency key, or one-time token | Long-lived reusable signed requests |
| TLS settings | Explicit minimum TLS version and hardened server defaults | Legacy protocol fallback and weak suites |

## Verification Checklist

Agent verifies:
- [ ] Spoofed network identity does not grant access
- [ ] Replayed requests or tokens are rejected
- [ ] Primary and alternate channels require approved protection
- [ ] Tampered privileged messages fail integrity checks
- [ ] Weak or downgraded protocol negotiation stays disabled

## Inputs

| Input | Required | Default |
|---|---|---|
| Repo or component path | Yes | - |
| CWE subset | No | All 8 |
| Trust-boundary inputs | No | Existing repo defaults |

## Outputs

Agent generates:
- Hotspot list with CWE labels
- Patch set for replay, spoofing, proxy, integrity, and channel-protection fixes
- Verification notes with transport, webhook, and negotiation results

## References

- CWE-888 SFP Primary Cluster: Channel
- OWASP Transport Layer Security Cheat Sheet
- OWASP Webhook Security guidance
- ASP.NET Core proxy and forwarded headers guidance

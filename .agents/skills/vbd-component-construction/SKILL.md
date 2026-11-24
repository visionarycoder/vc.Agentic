---
name: "vbd-component-construction"
description: "Scaffold an accepted VBD Manager, Engine, or Access boundary with contracts, services, tests, and explicitly requested hosting or persistence projects."
metadata:
  metadata-version: "1.0.0"
  title: "VBD component construction"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-09"
  collection: "vbd"
---

# VBD component construction

Use to create one component's structural skeleton from an assigned scope and accepted design. Do not invent component boundaries, domain behavior, operations, entities, or deployment authority.

Record the capability-to-existing-code assessment in the accepted detailed design:
examined Ifx package/API and version, suitability evidence, selection and any gap.
Reuse suitable existing mechanisms before creating infrastructure. Construct the
white-box test client with the component. Verify exact design inputs and expected
dependencies through the consuming project's independently controlled integration
checks. A self-generated snapshot cannot establish the approved baseline.

1. Read the target repository's governing instructions, accepted component design, actual Ifx API, SDK/package baseline, and testing conventions. Resolve missing design decisions through the assigned owner before construction depends on them.
2. Identify capability, approved Manager/Engine/Access classification, contract surface, namespaces, collaborators, and resource boundaries. Reuse supplied answers instead of repeatedly interviewing the user.
3. Read [repository discovery](references/repository-discovery.md), [naming](references/naming.md), and [project topology](references/project-topology.md). Adapt examples to the accepted graph rather than treating historical defaults as new architecture policy.
4. Follow [component initialization](references/component-base.md), [registration](references/module-registration.md), and [testing](references/testing.md). Preserve the requested ILoggerFactory constructor and verified base-class signature, separate top-level type files, and unprefixed fields.
5. Include a host, substitutes, or Access ORM projects only when assigned. Use the matching bundled references for that selected scope. Follow the consuming project's mandatory proxy policy; do not introduce reflection proxies or direct caller-to-target bypasses.
6. Validate the skeleton under the existing project checks and reconcile references using [reconciliation guidance](references/reconciliation.md). Report generated structure, tests, placeholders, and incomplete design inputs. A scaffold does not establish lifecycle acceptance or permission to deploy.

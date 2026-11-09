---
title: Skill Suite Optimization Patterns
description: Proven optimization patterns from 2026-08-22 optimization cycle with reusable workflows.
doc_type: reference
status: active
last_updated: 2026-08-22
target_audience: ai
complexity: medium
estimated_tokens: 500
parent_skill: skill-suite-optimization
tags:
  - optimization
  - patterns
  - meta
  - reusable
---

# Skill Suite Optimization Patterns

Proven patterns from the 2026-08-22 optimization cycle that optimized 237 skills to 99.8% compliance.

## Token Burn Reduction Pattern

**When to Use:** Skills with bloated `related_skills` lists (>5 for execution, >15 for routers)

**Workflow:**
1. Audit all skills: count `related_skills` entries
2. Identify violations: execution >5, router >15
3. Trim each skill: keep router + 4 most essential related skills
4. Verify routing: ensure no broken discovery paths
5. Test: verify skills still load correctly via routers

**2026-08-22 Results:**
- 20 skills optimized
- 32 skill references removed
- ~1600 tokens/session saved
- Zero broken discovery paths

**Example Trim:**
```yaml
# Before (8 related skills)
related_skills:
  - security-intake-router
  - cwe-input-validation-fixes
  - cwe-injection-attack-fixes
  - cwe-data-protection-fixes
  - cwe-resource-management-fixes
  - cwe-miscellaneous-security-fixes
  - cwe-fixes
  - webapi-authz-hardening

# After (5 related skills)
related_skills:
  - security-intake-router
  - cwe-fixes
  - webapi-authz-hardening
  - cwe-injection-attack-fixes
  - cwe-data-protection-fixes
```

## Near-Limit Extraction Pattern

**When to Use:** Skills at 1800-1999 tokens (approaching 2000 limit)

**Workflow:**
1. Identify at-risk skills: 1800-1999 token range
2. Create `references/` directory for each skill
3. Extract verbose content:
   - Code examples >20 lines
   - Detailed migration guides
   - Comprehensive pattern catalogs
   - Performance benchmarks
4. Add `## References` section linking extracted files
5. Verify token reduction and link validity

**2026-08-22 Results:**
- 10 skills buffered
- Average: 1900→1856 tokens (-44 avg)
- 140-600 token buffer per skill
- Content preserved, discoverability improved

**Extraction Targets:**
- Long code blocks (```...```)
- Before/after comparisons
- Step-by-step tutorials
- Exhaustive scenario matrices
- Benchmark data tables

## Orphaned References Pattern

**When to Use:** `references/` directories exist but aren't linked in SKILL.md

**Workflow:**
1. Scan all skills for `references/` directories
2. Check each SKILL.md for `## References` section
3. Add `## References` section if missing
4. List all reference files with descriptions
5. Verify links work and content is discoverable

**2026-08-22 Results:**
- 3 skills reconnected
- 10 reference documents now discoverable
- Zero orphaned content

**Example References Section:**
```markdown
## References

- Activation flow diagrams: `references/activation-flow.md`
- COM activation specifics: `references/com-activation.md`
- Log format reference: `references/log-format.md`
```

## STE Compliance Pattern

**When to Use:** Skills with modal verbs (should, must, could, may, might, consider, prefer, try, ensure)

**Workflow:**
1. Grep for modal verbs: `\b(should|must|could|may|might|consider|prefer|try|ensure)\b`
2. Rewrite with imperatives or explicit conditions
3. Replace "Agent should X" with "Agent does X" or "Agent X when Y"
4. Verify compliance: zero modal verbs remaining

**Common Replacements:**
- "should X" → "X" (imperative) or "X when Y" (conditional)
- "must X" → "X" (imperative) or "Agent X" (explicit subject)
- "consider X" → "Agent X when Y" (conditional)

## Skills Used During Optimization

The following skills were actively used during the 2026-08-22 optimization cycle:

| Skill | Purpose |
|---|---|
| `skill-intake-router` | Route requests to correct domain suite |
| `documentation-frontmatter` | Normalize metadata across skills |
| `dotnet-intake-router` | Classify .NET-specific skills |
| `testing-intake-router` | Classify testing-related skills |
| `security-intake-router` | Classify security/CWE skills |
| `webapi-intake-router` | Classify Web API skills |
| `vbd-intake-router` | Classify VBD architecture skills |
| `azure-intake-router` | Classify Azure-specific skills |

These routers enable deterministic skill discovery and prevent routing conflicts.

## Applying Patterns to New Optimizations

Agent loads this reference when executing `skill-suite-optimization` and applies patterns automatically:

1. Run audit scripts from `references/audit-script.md`
2. Apply Token Burn Reduction Pattern to identified violations
3. Apply Near-Limit Extraction Pattern to at-risk skills
4. Apply Orphaned References Pattern to unlinked content
5. Apply STE Compliance Pattern to modal verb violations
6. Generate before/after metrics
7. Update `references/optimization-history.md` with results

Patterns evolve with each optimization cycle while maintaining backward compatibility.

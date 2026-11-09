---
name: "roslyn-ca1859-solution-fix"
description: "Plan and execute CA1859 (use concrete types when possible) safely across a full .NET solution."
metadata:
  metadata-version: "1.0.0"
  title: "CA1859 Solution Fix Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# CA1859 Solution Fix Skill

Use this skill to plan and apply CA1859 remediations without introducing API breaks.

## Intent

Improve performance by replacing interface/abstract type declarations with concrete types when concrete usage is guaranteed.

## Planning-First Workflow

1. **Discover** candidate sites:
   - private/internal fields and locals typed as interfaces/abstract types,
   - helper method parameters/returns used only with a single concrete type.
2. **Classify risk** for each candidate:
   - safe (private/internal + concrete usage guaranteed),
   - review-needed (cross-file usage unclear),
   - reject (public/protected API, abstraction boundary, test seam).
3. **Apply minimal edits** only for safe candidates.
4. **Validate** by rebuilding touched projects, then full solution if available.

## Safe Replacement Rules

Prefer concrete types when all call sites and assignments are concrete and local.

- `ISet<T>` -> `HashSet<T>`
- `IList<T>`/`ICollection<T>` -> `List<T>`
- `IDictionary<TKey,TValue>` -> `Dictionary<TKey,TValue>`

Only apply when:
- the member/method is private or internal,
- no external contract compatibility is affected,
- no mocking/abstraction requirement is lost.

## Do Not Rewrite

Do not convert types when:
- declaration is public/protected API,
- declaration intentionally represents an abstraction boundary,
- multiple concrete implementations are used,
- dependency injection or test seams rely on interface typing.

## Validation Checklist

- Touched projects compile.
- Full solution build succeeds, or unrelated pre-existing failures are documented.
- No public API signatures were unintentionally changed.
- No behavioral changes beyond static type narrowing.

## Notes

For generator code, update only deterministic helper signatures and keep emitted output behavior unchanged.

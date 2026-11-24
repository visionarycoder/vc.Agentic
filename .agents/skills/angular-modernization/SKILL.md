---
name: "angular-modernization"
description: "Upgrade Angular applications to current patterns with standalone components, signals, modern control flow, and measured validation."
metadata:
  metadata-version: "1.0.0"
  title: "Angular Modernization"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# Angular Modernization

Agent upgrades Angular applications in small verified steps.

## When to Use

| Condition | Route |
|---|---|
| Angular 12-17 application needs current Angular patterns | Agent uses this skill |
| Team needs standalone components or signals | Agent uses this skill |
| Team needs framework migration to Vue | Agent uses `angular-to-vue3-migration` |
| Team needs AngularJS migration | Agent uses a dedicated AngularJS path |

## Baseline

Before changing anything, record the Angular version, build warnings, and test status (`ng build`, `ng test --watch=false`). Compare against this baseline after each step: no new deprecation warnings, and no changed route loses content or actions.

## Output

Agent returns the version change, migrated features, validation results, and remaining upgrade blockers.

---
metadata-version: "1.0.0"
title: "Test Analysis Extensions"
description: "Preserve scoped source guidance for test-analysis-extensions."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Test Analysis Extensions

Agent uses this helper skill to locate framework-specific reference files before running polyglot test analysis.

## Purpose

Agent treats each extension file as structured detection guidance.

## Available Extension Files

| File | Languages or frameworks | Agent uses it for |
|---|---|---|
| `extensions/dotnet.md` | MSTest, xUnit, NUnit, TUnit | Markers, assertions, skips, waits, fixtures, integration hints, tag support |
| `extensions/python.md` | pytest, unittest | Markers, assertions, fixtures, skips, waits, environment signals |
| `extensions/typescript.md` | Jest, Vitest, Mocha, `node:test` | Assertions, async pitfalls, skips, fixtures, tag behavior |
| `extensions/java.md` | JUnit 4, JUnit 5, TestNG | Assertions, tags, lifecycle, integration markers |
| `extensions/go.md` | Go `testing`, testify | Table-driven idioms, assertions, skips, waits |
| `extensions/ruby.md` | RSpec, Minitest | Matchers, metadata, hooks, skips |
| `extensions/rust.md` | Rust `#[test]` | Assertions, ignores, feature flags, panic patterns |
| `extensions/swift.md` | XCTest, Swift Testing | Assertions, tags, suite markers, skips |
| `extensions/kotlin.md` | JUnit 5, Kotest, MockK | Assertions, tags, lifecycle, mocks |
| `extensions/powershell.md` | Pester v5 | Assertions, tags, `Skip`, setup blocks |
| `extensions/cpp.md` | GoogleTest, Catch2, doctest | Assertions, tags, skips, fixtures |

## Capability Table

| Capability | Agent question |
|---|---|
| Test discovery | Which markers define test files, classes, and methods? |
| Assertion detection | Which framework APIs count as verification? |
| Wait detection | Which delay APIs signal timing risk? |
| Skip detection | Which attributes or calls skip tests? |
| Fixture detection | Which hooks define setup and teardown? |
| Mystery guest detection | Which APIs imply hidden file, DB, network, or env coupling? |
| Integration markers | Which names or attributes mark broader test scope? |
| Tag support | Can the skill edit native tags safely? |

## Workflow

| Step | Agent action | Test | Pass |
|---|---|---|---|
| 1 | Agent detects the active language and framework. | Review project files and test markers. | At least one likely framework is identified. |
| 2 | Agent reads every matching extension file. | Review chosen references. | Mixed-framework repos load multiple references when needed. |
| 3 | Agent passes the extension guidance into the calling analysis skill. | Review downstream analysis. | Findings use framework-correct markers and terms. |
| 4 | Agent names fallback behavior when no exact extension exists. | Review final note. | Closest supported framework is explicit. |

## Verification Checklist

- [ ] Agent read the extension file before analysis.
- [ ] Agent loaded multiple extensions when the repo mixed frameworks.
- [ ] Agent treated extension content as detection data.
- [ ] Agent reported fallback choices explicitly when coverage was imperfect.

## Common Pitfalls

| Pitfall | Agent fix |
|---|---|
| Agent guesses framework behavior from memory | Agent reads the extension file first. |
| Agent loads one extension for a mixed repo | Agent reads all relevant files. |
| Agent edits tags without checking capability mode | Agent reads tag support metadata first. |
